import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save_data, load_data
from rich.console import Console
from rich.table import Table

console = Console()


def add_user(args):
    """Creates a new user."""
    if User.find_by_name(args.name):
        print(f"User '{args.name}' already exists.")
    else:
        User(args.name, args.email)
        print(f"User '{args.name}' created.")
    save_data()


def list_users(args):
    """Lists all users."""
    if not User.all_users:
        print("No users found.")
        return

    for user in User.all_users:
        print(f"  - {user.name} ({user.email}) - {len(user.projects)} project(s)")


def add_project(args):
    """Adds a project to an existing user."""
    user = User.find_by_name(args.user)
    if user is None:
        print(f"User '{args.user}' not found.")
        return

    Project(args.title, args.description, args.due_date, user)
    print(f"Project '{args.title}' added to {args.user}.")
    save_data()


def list_projects(args):
    """Lists all projects (and their tasks) for a given user using a rich table."""
    user = User.find_by_name(args.user)
    if user is None:
        print(f"User '{args.user}' not found.")
        return

    if not user.projects:
        print(f"{user.name} has no projects.")
        return

    for project in user.projects:
        table = Table(title=f"{project.title} (due {project.due_date}) - {user.name}")
        table.add_column("Task", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Assigned To", style="green")

        for task in project.tasks:
            table.add_row(task.title, task.status, task.assigned_to)

        console.print(table)


def add_task(args):
    """Adds a task to an existing project."""
    project = Project.find_by_title(args.project)
    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    Task(args.title, args.status, args.assigned_to, project)
    print(f"Task '{args.title}' added to project '{args.project}'.")
    save_data()


def complete_task(args):
    """Marks a task as complete."""
    project = Project.find_by_title(args.project)
    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    task = Task.find_by_title(args.task, project)
    if task is None:
        print(f"Task '{args.task}' not found in project '{args.project}'.")
        return

    task.complete()
    print(f"Task '{args.task}' marked as complete.")
    save_data()


def main():
    load_data()

    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add-user
    p = subparsers.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True, help="User's name")
    p.add_argument("--email", required=True, help="User's email")
    p.set_defaults(func=add_user)

    # list-users
    p = subparsers.add_parser("list-users", help="List all users")
    p.set_defaults(func=list_users)

    # add-project
    p = subparsers.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True, help="Owner's name")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--description", default="", help="Project description")
    p.add_argument("--due-date", dest="due_date", default="", help="Due date (YYYY-MM-DD)")
    p.set_defaults(func=add_project)

    # list-projects
    p = subparsers.add_parser("list-projects", help="List projects for a user")
    p.add_argument("--user", required=True, help="User's name")
    p.set_defaults(func=list_projects)

    # add-task
    p = subparsers.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--status", default="pending", choices=Task.VALID_STATUSES, help="Task status")
    p.add_argument("--assigned-to", dest="assigned_to", required=True, help="Person assigned to the task")
    p.set_defaults(func=add_task)

    # complete-task
    p = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--task", required=True, help="Task title")
    p.set_defaults(func=complete_task)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()