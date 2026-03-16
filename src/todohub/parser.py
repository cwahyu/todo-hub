# src/todohub/parser.py

import re
from datetime import date
from .models import TodoItem


DATE_PATTERN = re.compile(r"@(\d{4}-\d{2}-\d{2})")
PRIORITY_PATTERN = re.compile(r"!(high|medium|low)", re.IGNORECASE)


def parse_todo_file(path, project_name):

    lines = path.read_text().splitlines()
    todos = []

    for i, raw_line in enumerate(lines):
        stripped = raw_line.lstrip()

        if not stripped.startswith("- [ ]"):
            continue

        indent = len(raw_line) - len(stripped)

        text = stripped[5:].strip()

        # --- parse due date ---
        due = None
        date_match = DATE_PATTERN.search(text)

        if date_match:
            due = date.fromisoformat(date_match.group(1))
            text = DATE_PATTERN.sub("", text)

        # --- parse priority ---
        priority = None
        priority_match = PRIORITY_PATTERN.search(text)

        if priority_match:
            priority = priority_match.group(1).lower()
            text = PRIORITY_PATTERN.sub("", text)

        text = text.strip()

        # --- detect if this task has children ---
        has_child = False

        for next_line in lines[i + 1 :]:
            next_stripped = next_line.lstrip()

            if not next_stripped.startswith("- [ ]"):
                continue

            next_indent = len(next_line) - len(next_stripped)

            if next_indent > indent:
                has_child = True

            break

        # --- ignore parent tasks without due date ---
        if has_child and due is None:
            continue

        todos.append(
            TodoItem(
                text=text,
                project=project_name,
                due=due,
                priority=priority,
            )
        )

    return todos
