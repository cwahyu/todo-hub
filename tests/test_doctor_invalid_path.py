# tests/test_doctor_invalid_path.py

from todohub.scheduler import doctor_check


def test_doctor_invalid_project_path():

    projects = [{"name": "demo", "path": "/path/does/not/exist"}]

    def fake_find(path):
        return []

    result = doctor_check(projects, fake_find)

    assert result["projects"][0][1] is False
    assert result["todos"][0][1] == "invalid"
