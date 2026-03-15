# tests/test_presenter_week.py

from datetime import date, timedelta

from todohub.presenter import display_week
from todohub.models import TodoItem


def test_display_week(capsys):

    today = date.today()

    tasks = [
        TodoItem("today task", "demo", today),
        TodoItem("tomorrow task", "demo", today + timedelta(days=1)),
    ]

    display_week(tasks)

    out = capsys.readouterr().out

    assert "Today" in out
    assert "Tomorrow" in out
