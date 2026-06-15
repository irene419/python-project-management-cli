# Python Project Management CLI Tool

A command-line application for managing users, projects, and tasks. Built with Python, `argparse`, and `rich`, with JSON-based persistence.

## Features

- Create users with name and email
- Add projects to users (with title, description, and due date)
- Add tasks to projects (with status and assignee)
- List a user's projects and tasks in a formatted table
- Mark tasks as complete
- Data is automatically saved to and loaded from `data/data.json`

## Setup Instructions

1. Clone this repository:
```bash
   git clone https://github.com/irene419/python-project-management-cli.git
   cd python-project-management-cli
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Running the CLI

### Add a user
```bash
python3 main.py add-user --name "Alex" --email "alex@email.com"
```

### List all users
```bash
python3 main.py list-users
```

### Add a project to a user
```bash
python3 main.py add-project --user "Alex" --title "CLI Tool" --description "Build a CLI app" --due-date "2026-07-01"
```

### Add a task to a project
```bash
python3 main.py add-task --project "CLI Tool" --title "Write README" --status pending --assigned-to "Alex"
```

### List a user's projects and tasks
```bash
python3 main.py list-projects --user "Alex"
```

### Mark a task as complete
```bash
python3 main.py complete-task --project "CLI Tool" --task "Write README"
```

## Project Structure