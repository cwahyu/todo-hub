# tests/test_scheduler_projects.py

from todohub.models import TodoItem
from todohub.scheduler import project_summary


def test_project_summary():

    todos = [
        TodoItem("task1", "mudita", None),
        TodoItem("task2", "mudita", None),
        TodoItem("task3", "pulse", None),
    ]

    result = project_summary(todos)

    assert result["mudita"] == 2
    assert result["pulse"] == 1
