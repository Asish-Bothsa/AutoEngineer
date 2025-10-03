from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.globals import set_debug, set_verbose
from langgraph.prebuilt import create_react_agent
from langsmith import traceable
load_dotenv()
from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files
from langgraph.graph import StateGraph
from langgraph.constants import END
from langchain.tools import Tool
import time
from groq import RateLimitError
from pydantic import BaseModel, Field
set_debug(True)
set_verbose(True)

llm=ChatGroq(model="openai/gpt-oss-120b")
class ReadFileInput(BaseModel):
    path: str = Field(description="The file path to read")

class WriteFileInput(BaseModel):
    path: str = Field(description="The file path to write to")
    content: str = Field(description="The content to write to the file")

class ListFilesInput(BaseModel):
    directory: str = Field(default=".", description="The directory to list files from")

class GetDirectoryInput(BaseModel):
    pass
@traceable
def planner_agent(state:dict)->dict:
    user_prompt=state["user_prompt"]
    response=llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan":response}
@traceable
def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    resp.plan = plan
    print(resp.model_dump_json())
    return {"task_plan": resp}

@traceable
def retry_invoke(agent, payload, max_retries=5, wait_time=70):
    """Retry helper: wait 1 minute on RateLimitError, then resume."""
    for attempt in range(max_retries):
        try:
            return agent.invoke(payload)
        except RateLimitError as e:
            print(f"[Retry {attempt+1}] Rate limit hit. Sleeping {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            # If it's not a rate limit, raise immediately
            raise
    raise RuntimeError(f"Failed after {max_retries} retries due to rate limits.")

@traceable
def coder_agent(state:dict)->dict:  #recieve task plan as input
      #for multiple steps we maintain coder_state and update it
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)
    steps=coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return{"coder_state":coder_state,"status":"DONE"}
    
    current_task=steps[coder_state.current_step_idx]
    existing_content=read_file(current_task.filepath)
    
    system_prompt=coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )
    # Provide both the standard tool names and an alias expected by some models
    repo_browser_list_files = Tool.from_function(
        name="repo_browser.list_files",
        func=list_files,
        description="Lists files within the generated project. Argument: directory (str)."
    )
    coder_tools = [read_file, write_file, list_files, get_current_directory, repo_browser_list_files]

    react_agent = create_react_agent(llm, coder_tools)
    
    payload = {"messages":[
    {"role":"system","content":system_prompt},
    {"role":"user","content":user_prompt}   
    ]}
    result = retry_invoke(react_agent, payload)
    coder_state.current_step_idx+=1
    return {"coder_state":coder_state, "result": result}
graph=StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.set_entry_point("planner")
graph.add_node("architect",architect_agent)
graph.add_node("coder",coder_agent)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")
graph.add_conditional_edges(
    "coder",
    lambda s:"END" if s.get("status")=="DONE" else "coder",
    {"END": END, "coder": "coder"}
)
agent=graph.compile()

    
    # user_prompt="Create simple caclulstoer web application similar to the iphone calculator"      
    # prompt=planner_prompt(user_prompt)
    # result=agent.invoke({"user_prompt":user_prompt},
    #                     {"recursion_limit":100})
    # print("Final State",result)


