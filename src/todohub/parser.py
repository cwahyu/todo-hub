import re
from datetime import date
from .models import TodoItem


DATE_PATTERN = re.compile(r"@(\d{4}-\d{2}-\d{2})")


def parse_todo_file(path, project_name):
    todos = []

    for line in path.read_text().splitlines():
        if not line.startswith("- [ ]"):
            continue

        text = line[5:].strip()

        match = DATE_PATTERN.search(text)

        due = None
        if match:
            due = date.fromisoformat(match.group(1))

        todos.append(
            TodoItem(
                text=text,
                project=project_name,
                due=due,
            )
        )

    return todos
