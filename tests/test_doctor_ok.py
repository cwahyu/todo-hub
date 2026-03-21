# tests/test_doctor_ok.py

import tempfile

from todohub.scheduler import doctor_check


def test_doctor_ok():

    with tempfile.TemporaryDirectory() as tmp:
        projects = [{"name": "demo", "path": tmp}]

        # simulate a TODO file being found
        def fake_find(path):
            return ["TODO.md"]

        result = doctor_check(projects, fake_find)

        assert result["projects"][0][1] is True
        assert result["todos"][0][1] == "ok"
