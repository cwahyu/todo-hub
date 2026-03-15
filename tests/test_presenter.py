# tests/test_presenter.py

from datetime import date, timedelta

from todohub.presenter import days_label


def test_days_label_overdue():

    label = days_label(date.today() - timedelta(days=3))

    assert "3d" in label


def test_days_label_future():

    label = days_label(date.today() + timedelta(days=5))

    assert "5d" in label
