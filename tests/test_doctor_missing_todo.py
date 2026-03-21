# tests/test_doctor_missing_todo.py

import tempfile

from todohub.scheduler import doctor_check


def test_doctor_missing_todo():

    with tempfile.TemporaryDirectory() as tmp:
        projects = [{"name": "demo", "path": tmp}]

        def fake_find(path):
            return []

        result = doctor_check(projects, fake_find)

        assert result["projects"][0][1] is True
        assert result["todos"][0][1] == "missing"
