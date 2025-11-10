# 📝 ToDoList Project

A simple **To-Do List** application built with **Python OOP** and **in-memory storage** (Phase 1).  
Designed to be modular, clean, and easily extensible for future phases (persistence, API, web interface, etc).

---

## 📂 Project Structure

```
.
├── application.py        # Business logic (create, edit, delete, list for projects & tasks)
├── cli.py                # Command-Line Interface for user interaction
├── models.py             # Data models (Project, Task)
├── repository.py         # In-memory storage layer
├── .env                  # Environment configuration file
├── pyproject.toml        # Poetry configuration and dependencies
└── README.md             # Project documentation (this file)
```

---

## ⚙️ Requirements

- **Python** ≥ 3.9  
- **Poetry** (recommended) or `pip`
- Optional `.env` file for configuration variables

Example `.env` file:
```env
MAX_NUMBER_OF_PROJECT=50
MAX_NUMBER_OF_TASK=1000
TITLE_MAX=30
DESC_MAX=150
STATUS_VALUES=todo,doing,done
```

---

## 🚀 Setup & Run

### 🔹 Using Poetry (recommended)

Install dependencies:
```bash
poetry install
```

Run the CLI application:
```bash
poetry run python cli.py
```

Or enter Poetry shell and run manually:
```bash
poetry shell
python cli.py
```

---

### 🔹 Without Poetry (manual setup)

If you prefer pip:
```bash
pip install python-dotenv
python cli.py
```

---

## 🧭 CLI Commands

| Category | Command | Description |
|-----------|----------|-------------|
| **Project** | `project create` | Create a new project |
| | `project list` | List all projects |
| | `project show <project_id>` | Show details of a project |
| | `project edit <project_id>` | Edit project name or description |
| | `project delete <project_id>` | Delete a project (and all its tasks) |
| **Task** | `task add <project_id>` | Add a task to a project |
| | `task list <project_id>` | List all tasks for a project |
| | `task edit <project_id> <task_id>` | Edit a task (title, description, status, deadline) |
| | `task status <project_id> <task_id> <todo|doing|done>` | Change task status |
| | `task delete <project_id> <task_id>` | Delete a task |
| **General** | `help` | Show command list |
| | `exit` or `quit` | Exit the app |

---

## 💡 Example Usage

```bash
> project create
Project name: Work
Description (optional): Tasks for office work
Project created: e12f3ab4 - Work

> project list
Project: Work (id: e12f3ab4)
  Number of tasks: 0

> task add e12f3ab4
Task title: Finish report
Description (optional): Monthly report for finance
Deadline (YYYY-MM-DD): 2025-10-20
Initial status (todo/doing/done): todo
Task created: 9f8b1c23 - Finish report

> task list e12f3ab4
  Task: Finish report (id: 9f8b1c23)
    Status: todo
    Deadline: 2025-10-20
    Description: Monthly report for finance

> task status e12f3ab4 9f8b1c23 done
Task status changed.

> project edit e12f3ab4
New name (press Enter to keep current): Work Projects
New description (press Enter to keep current): All work-related tasks
Project updated: Work Projects

> task edit e12f3ab4 9f8b1c23
New title (press Enter to keep current): Final Report
New description (press Enter to keep current): Reviewed and submitted
New status (todo/doing/done, press Enter to keep current): done
New deadline (YYYY-MM-DD, press Enter to keep current):
Task updated: Final Report

> project delete e12f3ab4
Delete this project and all tasks? (y/N): y
Project deleted.

> exit
Goodbye!
```

---

## 🧩 Architecture & Design

- **OOP Design:** Modular, extensible classes (`Project`, `Task`, `Repository`, `ToDoManager`).
- **Three-layer architecture:**
  1. `application.py` → Core logic and validation  
  2. `repository.py` → Data layer (in-memory for now)  
  3. `cli.py` → User interface layer (command-line interaction)
- **Validation:**  
  - Enforced title/description length  
  - Status must be one of `todo`, `doing`, `done`  
  - Max project/task count enforced  
- **Edit Methods:** Both `edit_project` and `edit_task` support partial updates (empty input keeps current values).

---

## 🔮 Future Improvements

- Add persistent storage (JSON, SQLite, or database)  
- Build REST API with FastAPI  
- Add automated tests (pytest)  
- Improve CLI UX (colored output, command suggestions)  
- Implement sorting and filtering for tasks/projects  

---

## 📜 License & Contributions

This project is open-source and developed for educational and practical purposes.  
Feel free to **fork**, **contribute**, or **open issues**.

> Created by [@mhoseinrostamdar](https://github.com/mhoseinrostamdar)
