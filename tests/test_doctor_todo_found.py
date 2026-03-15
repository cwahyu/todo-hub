# tests/test_doctor_todo_found.py

from pathlib import Path
import tempfile

from todohub.scheduler import doctor_check


def test_doctor_todo_found():

    with tempfile.TemporaryDirectory() as tmp:
        projects = [{"name": "demo", "path": tmp}]

        # simulate TODO file being found
        def fake_find(path):
            return [Path(tmp) / "TODO.md"]

        result = doctor_check(projects, fake_find)

        assert result["projects"][0][1] is True
        assert result["todos"][0][1] == "ok"
