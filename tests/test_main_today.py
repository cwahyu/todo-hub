# tests/test_main_today.py

from datetime import date
import sys

from todohub.main import main
from todohub.models import TodoItem


def test_today_command(monkeypatch, capsys):

    today = date.today()

    fake_items = [
        TodoItem("task today", "demo", today),
    ]

    monkeypatch.setattr(
        "todohub.main.collect_todos",
        lambda projects: fake_items,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["todo-hub", "today"],
    )

    monkeypatch.setattr(
        "todohub.main.load_config",
        lambda: {"project": [{"name": "demo", "path": "/tmp"}]},
    )

    main()

    out = capsys.readouterr().out

    assert "Today" in out
