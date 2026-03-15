# tests/test_main_no_projects.py

import sys
from todohub.main import main


def test_no_projects(monkeypatch, capsys):

    monkeypatch.setattr(
        "todohub.main.load_config",
        lambda: {"project": []},
    )

    monkeypatch.setattr(sys, "argv", ["todo-hub"])

    main()

    out = capsys.readouterr().out

    assert "No projects configured" in out
