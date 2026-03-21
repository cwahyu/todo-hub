# src/todohub/scanner.py

from pathlib import Path

IGNORED = {".git", ".venv", "__pycache__", "node_modules"}


def find_todo_file(project_path: Path):

    results = []

    for path in project_path.rglob("*"):
        if any(part in IGNORED for part in path.parts):
            continue

        if path.is_file() and path.name.lower() == "todo.md":
            results.append(path)

    return sorted(results)
