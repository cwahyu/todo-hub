# tests/test_presenter_status.py

from todohub.presenter import doctor_status


def test_doctor_status(capsys):

    doctor_status("✓", "ok")

    out = capsys.readouterr().out

    assert "✓ ok" in out
