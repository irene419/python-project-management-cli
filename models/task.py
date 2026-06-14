class Task:
    """Represents a task belonging to a project."""

    all_tasks = []
    next_id = 1

    VALID_STATUSES = ["pending", "in-progress", "complete"]

    def __init__(self, title, status, assigned_to, project):
        self.id = Task.next_id
        Task.next_id += 1

        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.project = project

        # Link this task to its project (one-to-many: Project -> Tasks)
        project.add_task(self)

        Task.all_tasks.append(self)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of {Task.VALID_STATUSES}")
        self._status = value

    def complete(self):
        """Marks this task as complete."""
        self.status = "complete"

    @classmethod
    def find_by_title(cls, title, project=None):
        """Returns the first task matching the title (optionally within a specific project)."""
        for task in cls.all_tasks:
            if task.title == title:
                if project is None or task.project == project:
                    return task
        return None

    def to_dict(self):
        """Converts this Task into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', assigned_to='{self.assigned_to}')"