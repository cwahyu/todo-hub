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


def project_color(project: str):
    idx = abs(hash(project)) % len(PROJECT_COLORS)
    return PROJECT_COLORS[idx]


def color_project(project: str):
    color = project_color(project)
    return f"{color}{Style.BRIGHT}#{project}{Style.RESET_ALL}"


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

    if t.due:
        label = days_label(t.due)
        print(f"  - [ ] {t.text} {label} {project}")
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
