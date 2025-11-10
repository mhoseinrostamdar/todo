#!/usr/bin/env python3
"""
ToDoList CLI - Phase 2 (Database Version)
"""
import textwrap
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid

# Database setup
DATABASE_URL = "postgresql+psycopg2://myapp_user:mysecretpassword@localhost:5432/myapp_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    return SessionLocal()

def short(project_id):
    return project_id[:8] if project_id else "N/A"

def print_project(p):
    print(f"\nProject: {p['name']} (id: {p['id']})")
    if p['description']:
        print(f"  Description: {p['description']}")
    print(f"  Created: {p['created_at']}")

def print_task(t):
    dl = t['deadline'].strftime('%Y-%m-%d') if t['deadline'] else "—"
    print(f"  Task: {t['title']} (id: {t['id']})")
    print(f"    Status: {t['status']}")
    print(f"    Deadline: {dl}")
    if t['description']:
        print(f"    Description: {t['description']}")
    print("")

class CLI:
    def __init__(self):
        self.db = get_db()

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def run(self):
        print("Welcome to ToDoList CLI (Phase 2 - Database)")
        print("Type 'help' for available commands.")
        while True:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                if cmd in ("exit", "quit"):
                    print("Goodbye!")
                    break
                if cmd == "help":
                    self.print_help()
                    continue
                self.handle(cmd)
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting.")
                break
            except Exception as e:
                print(f"Error: {e}")

    def print_help(self):
        print(textwrap.dedent("""
        Commands:
          project create
          project list
          project show <project_id>
          project edit <project_id>
          project delete <project_id>
          task add <project_id>
          task list <project_id>
          task edit <project_id> <task_id>
          task status <project_id> <task_id> <todo|doing|done>
          task delete <project_id> <task_id>
          exit
        """))

    def handle(self, cmd: str):
        parts = cmd.split()
        if parts[0] == "project":
            self.handle_project(parts[1:])
        elif parts[0] == "task":
            self.handle_task(parts[1:])
        else:
            print("Unknown command.")

    def handle_project(self, args):
        if not args:
            print("Incomplete command.")
            return
        sub = args[0]
        try:
            if sub == "create":
                name = input("Project name: ").strip()
                desc = input("Description (optional): ").strip()
                if not name:
                    print("Error: Project name cannot be empty.")
                    return

                # Check if name exists
                result = self.db.execute(text("SELECT id FROM projects WHERE name = :name"), {"name": name})
                if result.fetchone():
                    print("Error: Project name already exists.")
                    return

                # Create project
                project_id = str(uuid.uuid4())
                self.db.execute(text("""
                    INSERT INTO projects (id, name, description, created_at, updated_at)
                    VALUES (:id, :name, :desc, :now, :now)
                """), {
                    "id": project_id,
                    "name": name,
                    "desc": desc,
                    "now": datetime.utcnow()
                })
                self.db.commit()

                # Get the created project
                result = self.db.execute(text("SELECT id FROM projects WHERE name = :name"), {"name": name})
                project_id = result.fetchone()[0]
                print(f"Project created: {short(project_id)} - {name}")

            elif sub == "list":
                result = self.db.execute(text("SELECT id, name, description, created_at FROM projects ORDER BY created_at"))
                projects = result.fetchall()
                if not projects:
                    print("No projects found.")
                    return
                for p in projects:
                    print_project({
                        'id': p[0],
                        'name': p[1],
                        'description': p[2],
                        'created_at': p[3]
                    })

            elif sub == "show":
                if len(args) < 2:
                    print("Usage: project show <id>")
                    return
                project_id = args[1]

                # Get project
                result = self.db.execute(text("SELECT id, name, description, created_at FROM projects WHERE id = :id"), {"id": project_id})
                project = result.fetchone()
                if not project:
                    print("Project not found.")
                    return

                print_project({
                    'id': project[0],
                    'name': project[1],
                    'description': project[2],
                    'created_at': project[3]
                })

                # Get tasks
                result = self.db.execute(text("SELECT id, title, description, status, deadline FROM tasks WHERE project_id = :pid ORDER BY created_at"), {"pid": project_id})
                tasks = result.fetchall()
                for t in tasks:
                    print_task({
                        'id': t[0],
                        'title': t[1],
                        'description': t[2],
                        'status': t[3],
                        'deadline': t[4]
                    })

            elif sub == "delete":
                if len(args) < 2:
                    print("Usage: project delete <id>")
                    return
                project_id = args[1]

                # Check if project exists
                result = self.db.execute(text("SELECT id FROM projects WHERE id = :id"), {"id": project_id})
                if not result.fetchone():
                    print("Project not found.")
                    return

                confirm = input("Delete this project and all tasks? (y/N): ").lower()
                if confirm == "y":
                    # Delete tasks first (cascade should handle this, but let's be safe)
                    self.db.execute(text("DELETE FROM tasks WHERE project_id = :id"), {"id": project_id})
                    self.db.execute(text("DELETE FROM projects WHERE id = :id"), {"id": project_id})
                    self.db.commit()
                    print("Project deleted.")

        except Exception as e:
            print(f"Error: {e}")
            self.db.rollback()

    def handle_task(self, args):
        if not args:
            print("Incomplete command.")
            return
        sub = args[0]
        try:
            if sub == "add":
                if len(args) < 2:
                    print("Usage: task add <project_id>")
                    return
                project_id = args[1]

                # Check if project exists
                result = self.db.execute(text("SELECT id FROM projects WHERE id = :id"), {"id": project_id})
                if not result.fetchone():
                    print("Project not found.")
                    return

                title = input("Task title: ").strip()
                desc = input("Description (optional): ").strip()
                deadline_str = input("Deadline (YYYY-MM-DD, optional): ").strip()
                status = input("Initial status (todo/doing/done): ").strip() or "todo"

                if not title:
                    print("Error: Task title cannot be empty.")
                    return

                deadline = None
                if deadline_str:
                    try:
                        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                    except ValueError:
                        print("Error: Invalid date format. Use YYYY-MM-DD.")
                        return

                # Create task
                task_id = str(uuid.uuid4())
                self.db.execute(text("""
                    INSERT INTO tasks (id, title, description, status, deadline, project_id, created_at, updated_at)
                    VALUES (:id, :title, :desc, :status, :deadline, :project_id, :now, :now)
                """), {
                    "id": task_id,
                    "title": title,
                    "desc": desc,
                    "status": status,
                    "deadline": deadline,
                    "project_id": project_id,
                    "now": datetime.utcnow()
                })
                self.db.commit()

                # Get the created task
                result = self.db.execute(text("SELECT id FROM tasks WHERE title = :title AND project_id = :pid"), {"title": title, "pid": project_id})
                task_id = result.fetchone()[0]
                print(f"Task created: {task_id[:8]} - {title}")

            elif sub == "list":
                if len(args) < 2:
                    print("Usage: task list <project_id>")
                    return
                project_id = args[1]

                # Check if project exists
                result = self.db.execute(text("SELECT id FROM projects WHERE id = :id"), {"id": project_id})
                if not result.fetchone():
                    print("Project not found.")
                    return

                result = self.db.execute(text("SELECT id, title, description, status, deadline FROM tasks WHERE project_id = :pid ORDER BY created_at"), {"pid": project_id})
                tasks = result.fetchall()
                if not tasks:
                    print("No tasks found.")
                    return
                for t in tasks:
                    print_task({
                        'id': t[0],
                        'title': t[1],
                        'description': t[2],
                        'status': t[3],
                        'deadline': t[4]
                    })

            elif sub == "status":
                if len(args) < 4:
                    print("Usage: task status <project_id> <task_id> <status>")
                    return
                project_id, task_id, new_status = args[1], args[2], args[3]

                if new_status not in ['todo', 'doing', 'done']:
                    print("Error: Status must be todo, doing, or done.")
                    return

                # Update task
                result = self.db.execute(text("""
                    UPDATE tasks SET status = :status, updated_at = :now
                    WHERE id = :id AND project_id = :pid
                """), {
                    "status": new_status,
                    "now": datetime.utcnow(),
                    "id": task_id,
                    "pid": project_id
                })

                if result.rowcount == 0:
                    print("Task not found.")
                else:
                    self.db.commit()
                    print("Task status changed.")

            elif sub == "delete":
                if len(args) < 3:
                    print("Usage: task delete <project_id> <task_id>")
                    return
                project_id, task_id = args[1], args[2]

                confirm = input("Are you sure? (y/N): ").lower()
                if confirm == "y":
                    result = self.db.execute(text("DELETE FROM tasks WHERE id = :id AND project_id = :pid"), {"id": task_id, "pid": project_id})
                    if result.rowcount == 0:
                        print("Task not found.")
                    else:
                        self.db.commit()
                        print("Task deleted.")

        except Exception as e:
            print(f"Error: {e}")
            self.db.rollback()


if __name__ == "__main__":
    CLI().run()
