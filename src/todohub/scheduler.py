# src/todohub/scheduler.py

from datetime import date, timedelta
from collections import Counter
from pathlib import Path


def group_todos(todos):
    today = date.today()
    soon = today + timedelta(days=7)

    groups = {
        "overdue": [],
        "week": [],
        "later": [],
        "unscheduled": [],
    }

    for t in todos:
        if t.due is None:
            groups["unscheduled"].append(t)

        elif t.due < today:
            groups["overdue"].append(t)

        elif t.due <= soon:
            groups["week"].append(t)

        else:
            groups["later"].append(t)

    # sorting
    groups["overdue"].sort(key=lambda x: (x.due, x.project), reverse=True)
    groups["week"].sort(key=lambda x: (x.due, x.project))
    groups["later"].sort(key=lambda x: (x.due, x.project))
    groups["unscheduled"].sort(key=lambda x: x.project)

    return groups


def filter_today(groups):

    today = date.today()

    today_tasks = []
    overdue_tasks = groups.get("overdue", [])

    for task in groups.get("week", []):
        if task.due == today:
            today_tasks.append(task)

    return {
        "overdue": overdue_tasks,
        "today": today_tasks,
    }


def filter_week(groups):

    today = date.today()
    week_limit = today + timedelta(days=7)

    week_tasks = []

    for task in groups.get("week", []):
        if today <= task.due <= week_limit:
            week_tasks.append(task)

    return week_tasks


def project_summary(todos):

    counter = Counter()

    for t in todos:
        counter[t.project] += 1

    return counter


def doctor_check(projects, find_todo_file):

    results = {
        "projects": [],
        "todos": [],
    }

    for project in projects:
        name = project.get("name")
        path_str = project.get("path")

        path = Path(path_str).expanduser()

        if not path.exists():
            results["projects"].append((name, False))
            results["todos"].append((name, "invalid"))
            continue

        results["projects"].append((name, True))

        todo_files = find_todo_file(path)

        if todo_files:
            results["todos"].append((name, "ok"))
        else:
            results["todos"].append((name, "missing"))

    return results
