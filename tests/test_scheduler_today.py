# tests/test_scheduler_today.py

from datetime import date, timedelta

from todohub.scheduler import filter_today
from todohub.models import TodoItem


def test_filter_today():

    today = date.today()

    groups = {
        "overdue": [TodoItem("overdue", "demo", today - timedelta(days=1))],
        "week": [
            TodoItem("today", "demo", today),
            TodoItem("later_week", "demo", today + timedelta(days=3)),
        ],
    }

    result = filter_today(groups)

    assert len(result["overdue"]) == 1
    assert len(result["today"]) == 1
