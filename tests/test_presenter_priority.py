# tests/test_presenter_priority.py

from datetime import date
from todohub.presenter import print_task
from todohub.models import TodoItem


def test_print_task_with_priority(capsys):

    task = TodoItem(
        text="Fix bug",
        project="demo",
        due=date.today(),
        priority="high",
    )

    print_task(task)

    out = capsys.readouterr().out

    assert "!high" in out
    assert "Fix bug" in out
