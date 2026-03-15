# tests/test_scheduler.py

from datetime import date, timedelta

import pytest

from todohub.models import TodoItem
from todohub.scheduler import group_todos


@pytest.mark.parametrize(
    "delta, expected_group",
    [
        (-5, "overdue"),
        (0, "week"),
        (1, "week"),
        (3, "week"),
        (10, "later"),
    ],
)
def test_scheduler_date_groups(delta, expected_group):

    today = date.today()

    task = TodoItem(
        text="task",
        project="demo",
        due=today + timedelta(days=delta),
    )

    groups = group_todos([task])

    assert len(groups[expected_group]) == 1


def test_scheduler_unscheduled():

    task = TodoItem(
        text="task",
        project="demo",
        due=None,
    )

    groups = group_todos([task])

    assert len(groups["unscheduled"]) == 1
