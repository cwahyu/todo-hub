# tests/test_main_config.py

from todohub.main import main
import sys


def test_config_command(monkeypatch, capsys):

    monkeypatch.setattr(sys, "argv", ["todo-hub", "config"])

    main()

    out = capsys.readouterr().out

    assert "config.toml" in out
