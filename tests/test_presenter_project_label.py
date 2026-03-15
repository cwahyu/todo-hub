# tests/test_presenter_project_label.py

from todohub.presenter import project_label


def test_project_label():

    label = project_label("demo")

    assert "#demo" in label
