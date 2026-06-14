class Project:
    """Represents a project that belongs to a user and contains multiple tasks."""

    # Class attributes: track all projects + auto-incrementing ID counter
    all_projects = []
    next_id = 1

    def __init__(self, title, description, due_date, user):
        self.id = Project.next_id
        Project.next_id += 1

        self.title = title
        self.description = description
        self.due_date = due_date
        self.user = user
        self.tasks = []

        # Link this project to its user (one-to-many: User -> Projects)
        user.add_project(self)

        Project.all_projects.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Title must be a non-empty string")
        self._title = value

    def add_task(self, task):
        """Adds a Task object to this project's list of tasks."""
        self.tasks.append(task)

    @classmethod
    def find_by_title(cls, title):
        """Returns the first project matching the given title, or None."""
        for project in cls.all_projects:
            if project.title == title:
                return project
        return None

    def to_dict(self):
        """Converts this Project (and its tasks) into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', tasks={len(self.tasks)})"