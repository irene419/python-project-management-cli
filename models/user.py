class User:
    """Represents a user who can own multiple projects."""

    all_users = []

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []  

        
        User.all_users.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Email must be a valid string containing '@'")
        self._email = value

    def add_project(self, project):
        """Adds a Project object to this user's list of projects."""
        self.projects.append(project)

    @classmethod
    def find_by_name(cls, name):
        """Returns the first user matching the given name, or None."""
        for user in cls.all_users:
            if user.name == name:
                return user
        return None

    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}', projects={len(self.projects)})"