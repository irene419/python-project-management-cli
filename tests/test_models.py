import pytest
from models.user import User
from models.project import Project
from models.task import Task


@pytest.fixture(autouse=True)
def reset_data():
    """Resets class-level data before each test so tests don't interfere with each other."""
    User.all_users = []
    Project.all_projects = []
    Task.all_tasks = []
    Project.next_id = 1
    Task.next_id = 1
    yield


def test_create_user():
    user = User("Alex", "alex@email.com")
    assert user.name == "Alex"
    assert user.email == "alex@email.com"
    assert user.projects == []
    assert user in User.all_users


def test_user_invalid_email():
    with pytest.raises(ValueError):
        User("Alex", "not-an-email")


def test_user_invalid_name():
    with pytest.raises(ValueError):
        User("", "alex@email.com")


def test_find_user_by_name():
    user = User("Alex", "alex@email.com")
    found = User.find_by_name("Alex")
    assert found is user

    not_found = User.find_by_name("Nobody")
    assert not_found is None


def test_create_project_links_to_user():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)

    assert project.title == "CLI Tool"
    assert project in user.projects
    assert project.user is user
    assert project.id == 1


def test_find_project_by_title():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)

    found = Project.find_by_title("CLI Tool")
    assert found is project

    not_found = Project.find_by_title("Nonexistent")
    assert not_found is None


def test_create_task_links_to_project():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)
    task = Task("Write README", "pending", "Alex", project)

    assert task.title == "Write README"
    assert task.status == "pending"
    assert task in project.tasks
    assert task.project is project
    assert task.id == 1


def test_task_invalid_status():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)

    with pytest.raises(ValueError):
        Task("Write README", "not-a-status", "Alex", project)


def test_complete_task():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)
    task = Task("Write README", "pending", "Alex", project)

    task.complete()
    assert task.status == "complete"


def test_to_dict_serialization():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool", "Build a CLI app", "2026-07-01", user)
    task = Task("Write README", "pending", "Alex", project)

    user_dict = user.to_dict()

    assert user_dict["name"] == "Alex"
    assert user_dict["email"] == "alex@email.com"
    assert len(user_dict["projects"]) == 1
    assert user_dict["projects"][0]["title"] == "CLI Tool"
    assert len(user_dict["projects"][0]["tasks"]) == 1
    assert user_dict["projects"][0]["tasks"][0]["title"] == "Write README"