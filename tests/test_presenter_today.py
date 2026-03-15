# tests/test_presenter_today.py

from datetime import date

from todohub.presenter import display_today
from todohub.models import TodoItem


def test_display_today(capsys):

    today = date.today()

    groups = {
        "overdue": [],
        "today": [TodoItem("task", "demo", today)],
    }

    display_today(groups)

    out = capsys.readouterr().out

    assert "Today" in out
