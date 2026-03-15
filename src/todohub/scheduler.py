# src/todohub/scheduler.py

from datetime import date, timedelta


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
