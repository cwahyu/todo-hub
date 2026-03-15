# tests/test_doctor.py

from todohub.scheduler import doctor_check


def test_doctor_check():

    projects = [
        {"name": "demo", "path": "/tmp"},
    ]

    def fake_find(path):
        return ["TODO.md"]

    result = doctor_check(projects, fake_find)

    assert result["projects"][0][1] is True
    assert result["todos"][0][1] == "ok"
