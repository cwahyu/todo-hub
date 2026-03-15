from todohub.scanner import find_todo_file


def test_find_todo_recursive(tmp_path):

    project = tmp_path / "project"
    folder = project / "docs"

    folder.mkdir(parents=True)

    todo = folder / "TODO.md"
    todo.write_text("test")

    results = find_todo_file(project)

    assert len(results) == 1
    assert results[0].name.lower() == "todo.md"
