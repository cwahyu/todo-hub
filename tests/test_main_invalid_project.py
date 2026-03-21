# tests/test_main_invalid_project.py

import sys

from todohub.main import main


def test_invalid_project_path(monkeypatch, capsys):

    monkeypatch.setattr(
        "todohub.main.load_config",
        lambda: {"project": [{"name": "demo", "path": "/not/exist"}]},
    )

    monkeypatch.setattr(sys, "argv", ["todo-hub"])

    main()

    out = capsys.readouterr().out

    assert "Project path not found" in out
