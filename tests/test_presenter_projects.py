# tests/test_presenter_projects.py

from todohub.presenter import display_projects


def test_display_projects(capsys):

    summary = {
        "mudita": 4,
        "pulse": 2,
    }

    display_projects(summary)

    out = capsys.readouterr().out

    assert "mudita" in out
    assert "4 tasks" in out
