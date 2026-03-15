# tests/test_scheduler_week.py

from datetime import date, timedelta

from todohub.scheduler import filter_week
from todohub.models import TodoItem


def test_filter_week():

    today = date.today()

    groups = {
        "week": [
            TodoItem("today", "demo", today),
            TodoItem("tomorrow", "demo", today + timedelta(days=1)),
            TodoItem("later", "demo", today + timedelta(days=6)),
        ]
    }

    result = filter_week(groups)

    assert len(result) == 3
