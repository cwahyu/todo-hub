# src/todohub/presenter.py

from colorama import Fore, Style
from datetime import date, timedelta
from collections import defaultdict


PROJECT_COLORS = [
    Fore.CYAN,
    Fore.MAGENTA,
    Fore.BLUE,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
]


PRIORITY_COLORS = {
    "high": Fore.RED,
    "medium": Fore.YELLOW,
    "low": Fore.BLUE,
}


def project_color(project: str):
    idx = abs(hash(project)) % len(PROJECT_COLORS)
    return PROJECT_COLORS[idx]


def color_project(project: str):
    color = project_color(project)
    return f"{color}{Style.BRIGHT}#{project}{Style.RESET_ALL}"


def color_priority(priority):

    if not priority:
        return ""

    color = PRIORITY_COLORS.get(priority, "")
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


def project_label(name):

    return Fore.CYAN + Style.BRIGHT + f"#{name}" + Style.RESET_ALL


def print_task(t):

    project = color_project(t.project)
    priority = color_priority(getattr(t, "priority", None))

    if t.due:
        label = days_label(t.due)

        if priority:
            print(f"  - [ ] {t.text} {label} {priority} {project}")
        else:
            print(f"  - [ ] {t.text} {label} {project}")

    else:
        if priority:
            print(f"  - [ ] {t.text} {priority} {project}")
        else:
            print(f"  - [ ] {t.text} {project}")


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

    for t in items:
        if t.due != current_day:
            current_day = t.due

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


def display_week(tasks):

    today = date.today()

    grouped = defaultdict(list)

    for task in tasks:
        grouped[task.due].append(task)

    for due_date in sorted(grouped):
        if due_date == today:
            title = "Today"
        elif due_date == today + timedelta(days=1):
            title = "Tomorrow"
        else:
            title = due_date.strftime("%b %d")

        print(title)

        for t in grouped[due_date]:
            label = days_label(t.due)
            project = project_label(t.project)

            print(f"- [ ] {t.text} {label} {project}")

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
