import json
from models.user import User
from models.project import Project
from models.task import Task

DATA_FILE = "data/data.json"


def save_data(filepath=DATA_FILE):
    """Saves all users (and their projects/tasks) to a JSON file."""
    data = {
        "users": [user.to_dict() for user in User.all_users]
    }

    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Data saved to {filepath}")


def load_data(filepath=DATA_FILE):
    """Loads users, projects, and tasks from a JSON file."""
    # Reset in-memory data so reloading doesn't create duplicates
    User.all_users = []
    Project.all_projects = []
    Task.all_tasks = []

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing data found. Starting fresh.")
        return

    max_project_id = 0
    max_task_id = 0

    for user_data in data.get("users", []):
        user = User(user_data["name"], user_data["email"])

        for project_data in user_data.get("projects", []):
            project = Project(
                project_data["title"],
                project_data["description"],
                project_data["due_date"],
                user
            )
            project.id = project_data["id"]
            if project.id > max_project_id:
                max_project_id = project.id

            for task_data in project_data.get("tasks", []):
                task = Task(
                    task_data["title"],
                    task_data["status"],
                    task_data["assigned_to"],
                    project
                )
                task.id = task_data["id"]
                if task.id > max_task_id:
                    max_task_id = task.id

    # Make sure future new items get unique IDs (don't collide with loaded ones)
    Project.next_id = max_project_id + 1
    Task.next_id = max_task_id + 1

    print(f"Data loaded from {filepath}")