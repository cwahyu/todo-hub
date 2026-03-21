# tests/test_main_config.py

import sys

from todohub.main import main


def test_config_command(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["todo-hub", "config"])

    main()

    out = capsys.readouterr().out

    assert "config.toml" in out
