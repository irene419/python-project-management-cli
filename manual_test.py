from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save_data, load_data

# Create some sample data
alex = User("Alex", "alex@email.com")
project1 = Project("CLI Tool", "Build a command-line app", "2026-07-01", alex)
task1 = Task("Write README", "pending", "Alex", project1)
task2 = Task("Implement add-task", "in-progress", "Alex", project1)

# Save it to JSON
save_data()

print("\n--- Reloading from file ---\n")

# Load it back
load_data()

# Check that everything came back correctly
for user in User.all_users:
    print(user)
    for project in user.projects:
        print(f"  {project}")
        for task in project.tasks:
            print(f"    {task}")