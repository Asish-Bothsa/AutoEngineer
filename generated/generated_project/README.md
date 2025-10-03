# CODER Assistant Toolkit

## Overview

The **CODER Assistant Toolkit** is a lightweight, modular framework for building AI‑driven coding assistants. It separates core agent logic, tool integrations, and UI scaffolding, enabling rapid prototyping of agents that can safely read, write, and manipulate files within a sandboxed project root.

---

## Tech Stack

- **Python 3.10+** – Core language for the agents and tooling.
- **OpenAI / Anthropic APIs** – Optional back‑ends for LLM inference (plug‑and‑play).
- **Tkinter** – Simple cross‑platform UI for the demo (can be swapped for a web UI).
- **pytest** – Test framework for unit and integration tests.
- **flake8 & black** – Code style enforcement.
- **Virtualenv** – Recommended environment isolation.

---

## Features

- **File System Tools** – `read_file`, `write_file`, `list_files`, `get_current_directory` are provided out‑of‑the‑box and sandboxed to the project root.
- **Modular Architecture** – Core agents, tool wrappers, and UI components live in separate modules, making the codebase easy to navigate and extend.
- **Extensible UI** – Button‑driven interface with optional keyboard shortcuts for rapid interaction.
- **Safety‑First** – All file operations are confined to the repository directory, preventing accidental host‑system access.
- **Open‑Source Friendly** – Clear contribution guidelines, permissive MIT license, and a comprehensive test suite.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/coder-assistant-toolkit.git
cd coder-assistant-toolkit

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

---

## Usage Guide

Run the demo application:

```bash
python main.py
```

The console UI presents a set of action buttons and a text area for interacting with the CODER agent.

### Button Layout

| Button | Description | Typical Use |
|--------|-------------|-------------|
| 🗂️ **List Files** | Calls `list_files` for the current project directory. | Quickly view the repository structure. |
| 📂 **Open File** | Prompts for a file path and uses `read_file`. | Inspect source code or config files. |
| 💾 **Save File** | Opens a dialog to specify a path and writes using `write_file`. | Persist changes made by the agent or yourself. |
| 📁 **Current Dir** | Executes `get_current_directory`. | Verify the sandbox root for debugging. |
| 🚀 **Run Agent** | Sends the current prompt to the CODER agent. | Main interaction – ask the agent to generate, refactor, or analyze code. |
| ❓ **Help** | Shows a short help overlay with shortcuts. | Quick reference while working. |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | List files (`list_files`). |
| `Ctrl+O` | Open file (`read_file`). |
| `Ctrl+S` | Save file (`write_file`). |
| `Ctrl+D` | Show current directory (`get_current_directory`). |
| `Ctrl+Enter` | Send prompt to the CODER agent. |
| `F1` | Open the Help overlay. |
| `Esc` | Clear the current input field. |

Shortcuts can be customized in `config/shortcuts.json`.

---

## Contribution Guidelines

We welcome contributions! Follow these steps:

1. **Fork the repository** and clone your fork.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write tests** for any new functionality (`pytest`).
4. **Update documentation** – ensure the README and relevant docstrings reflect your changes.
5. **Run the test suite** to verify nothing is broken:
   ```bash
   pytest
   ```
6. **Submit a Pull Request** with a clear description of what you changed and why.

### Code Style
- Follow **PEP 8**.
- Use **type hints** for all public functions.
- Keep line length ≤ 100 characters.
- Run `flake8` and `black` before committing.

### Reporting Issues
Open an issue with a short description, steps to reproduce (if applicable), and expected vs. actual behavior.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

*Happy coding with CODER!*