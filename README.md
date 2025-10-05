# 🚀 AutoEngineer — Multi-Agent AI Code Generator

> **“From idea → to code → to project — AutoEngineer builds software like an AI engineer.”**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-LangGraph-orange)](https://www.langchain.com/)
[![LangSmith](https://img.shields.io/badge/Monitoring-LangSmith-blueviolet)](https://smith.langchain.com/)

---

## 🧠 Overview

**AutoEngineer** is a **multi-agent AI system** that autonomously plans, structures, and generates full software projects from **natural language prompts**.

It uses **LangGraph**, **LangChain**  to orchestrate specialized agents that work together like a real engineering team — planning the architecture, writing modular code, validating logic, and ensuring consistent structure.

With integrated **LangSmith** experiment tracking and **Pydantic**-based schema validation, AutoEngineer provides a transparent and reliable framework for AI-driven software development.

---

## ✨ Key Features

✅ **Multi-Agent Orchestration** — Planner, Architect, and Coder agents collaborate to transform user prompts into working projects.  
✅ **Natural Language → Code** — Describe your app idea in plain English and watch AutoEngineer generate the codebase.  
✅ **Structured Validation** — All agent outputs validated using **Pydantic models** to ensure type safety and consistency.  
✅ **LangSmith Tracking** — Integrated observability and debugging with **LangSmith** for real-time trace and performance tracking.  
✅ **Robust Retry Logic** — Automatically handles rate limits and failed API calls gracefully.  
✅ **Modular Architecture** — Each agent and tool is fully extensible — add new roles or capabilities easily.  
✅ **File-System Safe Tools** — Built-in utilities for secure reading/writing/listing files in isolated project directories.  
✅ **CLI Interface** — Simple command-line interface for running and experimenting with project generation.  

---

## 📂 Project Structure

```bash
AutoEngineer/
│
├── agent/
│   ├── graph.py          # LangGraph agent orchestration and state management
│   ├── prompts.py        # Agent system prompts and templates
│   ├── states.py         # Pydantic models for Plan, TaskPlan, etc.
│   └── tools.py          # Safe file operation tools for agents
│
├── generated_project/    # Auto-generated project files created by the agents
│
├── main.py               # Entry point (CLI for user prompt → project build)
├── requirements.txt      # Dependencies
├── .env.example          # Example environment configuration
├── README.md             # Project documentation
└── LICENSE               # MIT license

```



## 🧠 LangSmith Tracing Dashboard

Monitor agent activity, track prompts, and analyze performance across each stage (Planner → Architect → Coder).

<img width="100%" alt="LangSmith Trace" src="https://github.com/user-attachments/assets/e7e8885f-929e-49f5-8873-daa61a415933" />

---
## ⚙️ Installation

You can install and run **AutoEngineer** locally using either `pip` or [`uv`](https://github.com/astral-sh/uv).

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/AutoEngineer.git
cd AutoEngineer
```

### 2️⃣ Create a virtual environment

Using uv (recommended):

uv venv
source .venv/bin/activate

### 3️⃣ Install dependencies
pip install -r requirements.txt


### 📜 License

This project is licensed under the MIT License — see the LICENSE
 file for details.

