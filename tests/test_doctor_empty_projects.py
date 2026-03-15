# tests/test_doctor_empty_projects.py

from todohub.scheduler import doctor_check


def test_doctor_empty_projects():

    projects = []

    def fake_find(path):
        return []

    result = doctor_check(projects, fake_find)

    assert result["projects"] == []
    assert result["todos"] == []
