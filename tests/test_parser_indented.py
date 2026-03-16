# tests/test_parser_indented.py

from todohub.parser import parse_todo_file


def test_ignore_parent_task(tmp_path):

    todo = tmp_path / "TODO.md"

    todo.write_text("- [ ] Parent task\n  - [ ] Child task @2026-03-16\n")

    items = parse_todo_file(todo, "demo")

    assert len(items) == 1
    assert items[0].text == "Child task"
