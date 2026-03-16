# tests/test_parser_priority.py

from todohub.parser import parse_todo_file


def test_priority_parsing(tmp_path):

    todo = tmp_path / "TODO.md"

    todo.write_text(
        "- [ ] Fix bug !high @2026-03-16\n- [ ] Write docs @2026-03-20 !low\n"
    )

    items = parse_todo_file(todo, "demo")

    assert items[0].priority == "high"
    assert items[1].priority == "low"
