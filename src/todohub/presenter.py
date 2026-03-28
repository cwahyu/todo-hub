# src/todohub/presenter.py

import hashlib
import re
import shutil
import textwrap
from collections import defaultdict
from datetime import date, timedelta

from colorama import Fore, Style

ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


PROJECT_COLORS = [
    Fore.CYAN,
    Fore.BLUE,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.YELLOW,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
]


PRIORITY_COLORS = {
    "high": Fore.RED,
    "medium": Fore.YELLOW,
    "low": Fore.BLUE,
}


PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
    None: 3,
}


def visible_len(text: str) -> int:
    return len(ANSI_PATTERN.sub("", text))


def terminal_width():
    return max(60, shutil.get_terminal_size(fallback=(100, 20)).columns)


def project_color(project: str):

    digest = hashlib.md5(project.encode("utf-8")).hexdigest()

    idx = int(digest, 16) % len(PROJECT_COLORS)

    return PROJECT_COLORS[idx]


def color_project(project: str):
    color = project_color(project)
    return f"{color}{Style.BRIGHT}#{project}{Style.RESET_ALL}"


def color_priority(priority):

    if not priority:
        return ""

    color = PRIORITY_COLORS.get(priority)
    if not color:
        return ""

    return f"{color}!{priority}{Style.RESET_ALL}"


def days_label(due):

    today = date.today()
    delta = (due - today).days

    label = f"({delta}d)"

    if delta < 0:
        return Fore.RED + label + Style.RESET_ALL

    if delta <= 7:
        return Fore.YELLOW + label + Style.RESET_ALL

    return Fore.GREEN + label + Style.RESET_ALL


def print_task(t):

    project = color_project(t.project)
    priority = color_priority(getattr(t, "priority", None))

    prefix = "  - [ ] "
    indent = " " * len(prefix)

    metadata = []

    if t.due:
        metadata.append(days_label(t.due))

    if priority:
        metadata.append(priority)

    metadata.append(project)

    meta_str = " ".join(metadata)

    width = terminal_width()

    candidate = f"{prefix}{t.text} {meta_str}"

    if visible_len(candidate) <= width:
        print(candidate)
        return

    text_width = width - len(prefix)

    wrapped = textwrap.wrap(t.text, width=text_width)

    if not wrapped:
        wrapped = [""]

    meta_len = visible_len(meta_str) + 1
    safe_width = max(10, text_width - meta_len)

    if visible_len(wrapped[-1]) + meta_len > text_width:
        wrapped = textwrap.wrap(t.text, width=safe_width)

    print(f"{prefix}{wrapped[0]}")

    for line in wrapped[1:-1]:
        print(f"{indent}{line}")

    print(f"{indent}{wrapped[-1]} {meta_str}")


def print_group(title, items, color):

    if not items:
        return

    print(color + Style.BRIGHT + title + ":" + Style.RESET_ALL)

    for t in items:
        print_task(t)

    print()


def print_week_agenda(items):

    if not items:
        return

    today = date.today()
    tomorrow = today + timedelta(days=1)

    print(Fore.YELLOW + Style.BRIGHT + "This week:" + Style.RESET_ALL)

    current_day = None
    first_group = True

    for t in items:
        if t.due != current_day:
            if not first_group:
                print()

            current_day = t.due
            first_group = False

            if current_day == today:
                label = "Today"
            elif current_day == tomorrow:
                label = "Tomorrow"
            else:
                label = current_day.strftime("%b %d")

            print(Fore.LIGHTWHITE_EX + f"  {label}" + Style.RESET_ALL)

        print_task(t)

    print()


def display(groups):

    print_group("Overdue", groups["overdue"], Fore.RED)

    print_week_agenda(groups["week"])

    print_group("Later", groups["later"], Fore.GREEN)

    print_group("Unscheduled", groups["unscheduled"], Fore.LIGHTBLACK_EX)


def display_today(groups):

    overdue = groups.get("overdue", [])
    today = groups.get("today", [])

    if overdue:
        print_group("Overdue", overdue, Fore.RED)

    if today:
        print_group("Today", today, Fore.YELLOW)


def display_week(data):

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # --- detect input type ---
    if isinstance(data, dict):
        overdue = data.get("overdue", [])
        week_tasks = data.get("week", [])
    else:
        overdue = []
        week_tasks = data

    # --- Overdue ---
    if overdue:
        print("Overdue")
        for t in overdue:
            print_task(t)
        print()

    if not week_tasks:
        return

    # --- Group by date ---
    grouped = defaultdict(list)

    for task in week_tasks:
        grouped[task.due].append(task)

    # --- Week agenda ---
    for due_date in sorted(grouped):
        if due_date == today:
            title = "Today"
        elif due_date == tomorrow:
            title = "Tomorrow"
        else:
            title = due_date.strftime("%b %d")

        print(title)

        for t in grouped[due_date]:
            print_task(t)

        print()


def display_projects(summary):

    if not summary:
        print("No tasks found.")
        return

    for project, count in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"{project:<12} {count} tasks")


def doctor_status(symbol, message):
    print(f"{symbol} {message}")


def display_doctor(config_path, projects, results):

    print("todo-hub doctor\n")

    print("Config file")
    doctor_status("✓", config_path)
    print()

    print("Projects")

    for name, path_ok in results["projects"]:
        if path_ok:
            doctor_status("✓", name)
        else:
            doctor_status("✗", f"{name} (path not found)")

    print()

    print("TODO files")

    for name, status in results["todos"]:
        if status == "ok":
            doctor_status("✓", name)
        elif status == "missing":
            doctor_status("⚠", f"{name} (no TODO.md found)")
        else:
            doctor_status("✗", f"{name} (invalid path)")
