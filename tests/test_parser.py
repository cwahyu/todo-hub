from datetime import date

from todohub.parser import parse_todo_file


def test_parse_todo_with_date(tmp_path):

    file = tmp_path / "TODO.md"

    file.write_text("- [ ] finish CLI @2026-03-14\n- [ ] improve parser @2026-03-16\n")

    items = parse_todo_file(file, "demo")

    assert len(items) == 2
    assert items[0].project == "demo"
    assert items[0].due == date(2026, 3, 14)


def test_parse_todo_without_date(tmp_path):

    file = tmp_path / "TODO.md"

    file.write_text("- [ ] write documentation\n")

    items = parse_todo_file(file, "demo")

    assert len(items) == 1
    assert items[0].due is None


def test_ignore_completed_tasks(tmp_path):

    file = tmp_path / "TODO.md"

    file.write_text("- [x] completed task\n- [ ] open task\n")

    items = parse_todo_file(file, "demo")

    assert len(items) == 1
    assert items[0].text.startswith("open")
