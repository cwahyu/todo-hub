# tests/test_main_week.py

import sys
from datetime import date

from todohub.main import main
from todohub.models import TodoItem


def test_week_command(monkeypatch, capsys):

    today = date.today()

    fake_items = [
        TodoItem("task", "demo", today),
    ]

    monkeypatch.setattr(
        "todohub.main.collect_todos",
        lambda projects: fake_items,
    )

    monkeypatch.setattr(
        "todohub.main.load_config",
        lambda: {"project": [{"name": "demo", "path": "/tmp"}]},
    )

    monkeypatch.setattr(sys, "argv", ["todo-hub", "week"])

    main()

    out = capsys.readouterr().out

    assert "Today" in out
