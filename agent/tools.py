import pathlib
import subprocess
import logging
from typing import Tuple, Optional
from langchain.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"

class ProjectPathError(Exception):
    """Custom exception for path validation errors."""
    pass

def safe_path_for_project(path: str) -> pathlib.Path:
    """
    Validates and resolves a path within the project root.
    
    Args:
        path: The path to validate (relative to project root)
        
    Returns:
        pathlib.Path: The resolved path
        
    Raises:
        ProjectPathError: If path is outside project root
        ValueError: If path is invalid
    """
    if not path or not path.strip():
        raise ValueError("Path cannot be empty or whitespace")
    
    try:
        # Normalize the path and resolve it
        p = (PROJECT_ROOT / path).resolve()
        project_root_resolved = PROJECT_ROOT.resolve()
        
        # More robust path validation
        if not (p == project_root_resolved or project_root_resolved in p.parents):
            raise ProjectPathError(f"Path '{path}' resolves outside project root")
            
        return p
        
    except (OSError, RuntimeError) as e:
        logger.error(f"Path resolution failed for '{path}': {e}")
        raise ValueError(f"Invalid path '{path}': {e}")

@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file at the specified path within the project root.
    Creates parent directories if they don't exist.
    
    Args:
        path: File path relative to project root
        content: Content to write to the file
        
    Returns:
        str: Success message with file path or error message
    """
    try:
        # Handle None content gracefully
        if content is None:
            content = ""
            
        p = safe_path_for_project(path)
        
        # Create parent directories if they don't exist
        p.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file with explicit encoding and error handling
        with open(p, "w", encoding="utf-8", newline='') as f:
            f.write(content)
            
        logger.info(f"Successfully wrote {len(content)} characters to: {p.relative_to(PROJECT_ROOT)}")
        return f"WROTE:{p.relative_to(PROJECT_ROOT)}"
        
    except (ProjectPathError, ValueError) as e:
        error_msg = f"Invalid path '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except (OSError, IOError) as e:
        error_msg = f"Failed to write file '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error writing file '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"

@tool 
def read_file(path: str) -> str:
    """
    Reads content from a file at the specified path within the project root.
    
    Args:
        path: File path relative to project root
        
    Returns:
        str: File content, empty string if file doesn't exist, or error message
    """
    try:
        p = safe_path_for_project(path)
        
        # Check if file exists
        if not p.exists():
            logger.info(f"File does not exist: {p.relative_to(PROJECT_ROOT)}")
            return ""
            
        # Verify it's actually a file
        if not p.is_file():
            error_msg = f"Path '{path}' exists but is not a file"
            logger.error(error_msg)
            return f"ERROR: {error_msg}"
            
        # Read file with proper encoding and error handling
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            
        logger.info(f"Successfully read {len(content)} characters from: {p.relative_to(PROJECT_ROOT)}")
        return content
        
    except (ProjectPathError, ValueError) as e:
        error_msg = f"Invalid path '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except (OSError, IOError, UnicodeDecodeError) as e:
        error_msg = f"Failed to read file '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error reading file '{path}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"

@tool
def get_current_directory() -> str:
    """
    Returns the current working directory (project root).
    
    Returns:
        str: Absolute path to project root
    """
    try:
        # Ensure project root exists
        if not PROJECT_ROOT.exists():
            logger.warning(f"Project root does not exist: {PROJECT_ROOT}")
            
        return str(PROJECT_ROOT.resolve())
        
    except Exception as e:
        logger.error(f"Error getting current directory: {e}")
        return str(PROJECT_ROOT)

@tool
def list_files(directory: str) -> str:
    """
    Lists all files in the specified directory within the project root.
    Recursively searches subdirectories.
    
    Args:
        directory: Directory path relative to project root
        
    Returns:
        str: Newline-separated list of relative file paths or error message
    """
    try:
        p = safe_path_for_project(directory)
        
        # Check if directory exists
        if not p.exists():
            error_msg = f"Directory '{directory}' does not exist"
            logger.error(error_msg)
            return f"ERROR: {error_msg}"
            
        # Verify it's actually a directory
        if not p.is_dir():
            error_msg = f"Path '{directory}' exists but is not a directory"
            logger.error(error_msg)
            return f"ERROR: {error_msg}"
        
        # Collect all files recursively
        files = []
        try:
            for item in p.rglob("*"):
                if item.is_file():
                    # Store relative path from PROJECT_ROOT for consistency
                    rel_path = item.relative_to(PROJECT_ROOT)
                    files.append(str(rel_path))
        except (OSError, PermissionError) as e:
            logger.warning(f"Error accessing some files in '{directory}': {e}")
            
        # Sort files for consistent output
        files.sort()
        
        if not files:
            logger.info(f"No files found in directory: {p.relative_to(PROJECT_ROOT)}")
            return "No files found."
            
        logger.info(f"Found {len(files)} files in directory: {p.relative_to(PROJECT_ROOT)}")
        return "\n".join(files)
        
    except (ProjectPathError, ValueError) as e:
        error_msg = f"Invalid directory path '{directory}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error listing files in '{directory}': {e}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"

def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
    """
    Runs a shell command in the specified directory and returns the result.
    
    Args:
        cmd: Command to execute
        cwd: Working directory relative to project root (default: project root)
        timeout: Command timeout in seconds (default: 30)
        
    Returns:
        Tuple[int, str, str]: (return_code, stdout, stderr)
    """
    try:
        # Validate command input
        if not cmd or not cmd.strip():
            logger.error("Command cannot be empty")
            return 1, "", "Command cannot be empty"
            
        # Determine working directory
        if cwd:
            try:
                cwd_dir = safe_path_for_project(cwd)
            except (ProjectPathError, ValueError) as e:
                error_msg = f"Invalid working directory '{cwd}': {e}"
                logger.error(error_msg)
                return 1, "", error_msg
        else:
            cwd_dir = PROJECT_ROOT
            
        # Check if working directory exists
        if not cwd_dir.exists():
            error_msg = f"Working directory does not exist: {cwd_dir.relative_to(PROJECT_ROOT) if cwd else 'PROJECT_ROOT'}"
            logger.error(error_msg)
            return 1, "", error_msg
            
        if not cwd_dir.is_dir():
            error_msg = f"Working directory path is not a directory: {cwd_dir.relative_to(PROJECT_ROOT) if cwd else 'PROJECT_ROOT'}"
            logger.error(error_msg)
            return 1, "", error_msg
        
        logger.info(f"Executing command: '{cmd}' in {cwd_dir.relative_to(PROJECT_ROOT) if cwd else 'PROJECT_ROOT'}")
        
        # Execute command with proper error handling
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=str(cwd_dir), 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            # Security: Don't inherit environment variables that might be sensitive
            env=None
        )
        
        # Log command completion
        if result.returncode == 0:
            logger.info(f"Command completed successfully with {len(result.stdout)} chars stdout, {len(result.stderr)} chars stderr")
        else:
            logger.warning(f"Command failed with return code {result.returncode}")
            
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        error_msg = f"Command '{cmd}' timed out after {timeout} seconds"
        logger.error(error_msg)
        return 1, "", error_msg
    except (OSError, ValueError) as e:
        error_msg = f"Failed to execute command '{cmd}': {e}"
        logger.error(error_msg)
        return 1, "", error_msg
    except Exception as e:
        error_msg = f"Unexpected error executing command '{cmd}': {e}"
        logger.error(error_msg)
        return 1, "", error_msg

def init_project_root() -> str:
    """
    Initializes the project root directory if it doesn't exist.
    
    Returns:
        str: Absolute path to project root
        
    Raises:
        OSError: If directory creation fails
    """
    try:
        PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
        logger.info(f"Project root initialized: {PROJECT_ROOT.resolve()}")
        return str(PROJECT_ROOT.resolve())
        
    except (OSError, PermissionError) as e:
        error_msg = f"Failed to initialize project root '{PROJECT_ROOT}': {e}"
        logger.error(error_msg)
        raise OSError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error initializing project root: {e}"
        logger.error(error_msg)
        raise