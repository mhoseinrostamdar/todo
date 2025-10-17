import textwrap
from application import ToDoManager


def short(p): return f"{p.id[:8]} - {p.name}"


def print_project(p):
    print(f"\nProject: {p.name} (id: {p.id})")
    if p.description:
        print(f"  Description: {p.description}")
    print(f"  Number of tasks: {len(p.tasks)}\n")


def print_task(t):
    dl = t.deadline.isoformat() if t.deadline else "—"
    print(f"  Task: {t.title} (id: {t.id})")
    print(f"    Status: {t.status}")
    print(f"    Deadline: {dl}")
    if t.description:
        print(f"    Description: {t.description}")
    print("")


class CLI:
    def __init__(self):
        self.mgr = ToDoManager()

    def run(self):
        print("Welcome to ToDoList CLI (Phase 1 - In-Memory)")
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
        if sub == "create":
            name = input("Project name: ").strip()
            desc = input("Description (optional): ").strip()
            p = self.mgr.create_project(name, desc)
            print(f"Project created: {short(p)}")
        elif sub == "list":
            projects = self.mgr.list_projects()
            if not projects:
                print("No projects found.")
                return
            for p in projects:
                print_project(p)
        elif sub == "show":
            if len(args) < 2:
                print("Usage: project show <id>")
                return
            p = self.mgr.storage.get_project(args[1])
            if not p:
                print("Project not found.")
                return
            print_project(p)
            for t in p.tasks.values():
                print_task(t)
        elif sub == "edit":
            if len(args) < 2:
                print("Usage: project edit <id>")
                return
            pid = args[1]
            new_name = input("New name (press Enter to keep current): ").strip() or None
            new_desc = input("New description (press Enter to keep current): ").strip() or None
            p = self.mgr.edit_project(pid, new_name, new_desc)
            print(f"Project updated: {p.name}")
        elif sub == "delete":
            if len(args) < 2:
                print("Usage: project delete <id>")
                return
            pid = args[1]
            confirm = input("Delete this project and all tasks? (y/N): ").lower()
            if confirm == "y":
                self.mgr.delete_project(pid)
                print("Project deleted.")
        else:
            print("Unknown project command.")

    def handle_task(self, args):
        if not args:
            print("Incomplete command.")
            return
        sub = args[0]
        if sub == "add":
            if len(args) < 2:
                print("Usage: task add <project_id>")
                return
            pid = args[1]
            title = input("Task title: ").strip()
            desc = input("Description (optional): ").strip()
            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            status = input("Initial status (todo/doing/done): ").strip() or None
            t = self.mgr.add_task(pid, title, desc, status, deadline or None)
            print(f"Task created: {t.id[:8]} - {t.title}")
        elif sub == "list":
            if len(args) < 2:
                print("Usage: task list <project_id>")
                return
            tasks = self.mgr.list_tasks_of_project(args[1])
            if not tasks:
                print("No tasks found.")
                return
            for t in tasks:
                print_task(t)
        elif sub == "edit":
            if len(args) < 3:
                print("Usage: task edit <project_id> <task_id>")
                return
            pid, tid = args[1], args[2]
            new_title = input("New title (press Enter to keep current): ").strip() or None
            new_desc = input("New description (press Enter to keep current): ").strip() or None
            new_status = input("New status (todo/doing/done, press Enter to keep current): ").strip() or None
            new_deadline = input("New deadline (YYYY-MM-DD, press Enter to keep current): ").strip() or None
            t = self.mgr.edit_task(pid, tid, title=new_title, description=new_desc, status=new_status, deadline_str=new_deadline)
            print(f"Task updated: {t.title}")
        elif sub == "status":
            if len(args) < 4:
                print("Usage: task status <project_id> <task_id> <status>")
                return
            self.mgr.change_task_status(args[1], args[2], args[3])
            print("Task status changed.")
        elif sub == "delete":
            if len(args) < 3:
                print("Usage: task delete <project_id> <task_id>")
                return
            confirm = input("Are you sure? (y/N): ").lower()
            if confirm == "y":
                self.mgr.delete_task(args[1], args[2])
                print("Task deleted.")
        else:
            print("Unknown task command.")


if __name__ == "__main__":
    CLI().run()
