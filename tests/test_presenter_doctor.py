# tests/test_presenter_doctor.py

from todohub.presenter import display_doctor


def test_display_doctor(capsys):

    config_path = "/tmp/config.toml"

    projects = [
        {"name": "demo", "path": "/tmp"},
    ]

    results = {
        "projects": [("demo", True)],
        "todos": [("demo", "ok")],
    }

    display_doctor(config_path, projects, results)

    out = capsys.readouterr().out

    assert "todo-hub doctor" in out
    assert "Config file" in out
    assert "demo" in out
