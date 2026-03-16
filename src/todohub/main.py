# src/todohub/main.py

import argparse
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

from colorama import init
from platformdirs import user_config_dir

from .config import load_config
from .scanner import find_todo_file
from .parser import parse_todo_file
from .scheduler import (
    group_todos,
    filter_today,
    filter_week,
    project_summary,
    doctor_check,
)
from .presenter import (
    display,
    display_today,
    display_week,
    display_projects,
    display_doctor,
)


init(autoreset=True)


APP_NAME = "todohub"


def get_version():
    try:
        return version("todo-hub")
    except PackageNotFoundError:
        return "unknown"


def get_config_path():
    config_dir = Path(user_config_dir(APP_NAME))
    return config_dir / "config.toml"


def run():

    config = load_config()

    projects = config.get("project", [])

    if not projects:
        print("No projects configured in config.toml")
        return

    todos = []

    for project in projects:
        name = project.get("name")
        path_str = project.get("path")

        if not name or not path_str:
            print("Skipping invalid project entry in config.toml")
            continue

        path = Path(path_str).expanduser()

        if not path.exists():
            print(f"Project path not found: {path}")
            continue

        # optional debug
        # print(f"Scanning {name}...")

        todo_files = find_todo_file(path)

        for todo_file in todo_files:
            items = parse_todo_file(todo_file, name)
            todos.extend(items)

    groups = group_todos(todos)

    display(groups)


def collect_todos(projects):

    todos = []

    for project in projects:
        name = project.get("name")
        path_str = project.get("path")

        if not name or not path_str:
            continue

        path = Path(path_str).expanduser()

        if not path.exists():
            print(f"Project path not found: {path}")
            continue

        todo_files = find_todo_file(path)

        for todo_file in todo_files:
            items = parse_todo_file(todo_file, name)
            todos.extend(items)

    return todos


def main():

    parser = argparse.ArgumentParser(
        prog="todo-hub",
        description="Aggregate TODO deadlines across projects",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser(
        "config",
        help="Show the config file location",
    )

    subparsers.add_parser(
        "today",
        help="Show overdue and today's tasks",
    )

    subparsers.add_parser(
        "week",
        help="Show tasks for the next 7 days",
    )

    subparsers.add_parser(
        "projects",
        help="Show task count per project",
    )

    subparsers.add_parser(
        "doctor",
        help="Check configuration and project health",
    )

    args = parser.parse_args()

    if args.command == "config":
        print("\ntodo-hub configuration file:")
        print(get_config_path())
        print("\n")
        return

    if args.command == "today":
        config = load_config()
        projects = config.get("project", [])

        todos = collect_todos(projects)

        groups = group_todos(todos)

        today_groups = filter_today(groups)

        display_today(today_groups)

        return

    if args.command == "week":
        config = load_config()

        projects = config.get("project", [])

        todos = collect_todos(projects)

        groups = group_todos(todos)

        week_tasks = filter_week(groups)

        display_week(week_tasks)

        return

    if args.command == "projects":
        config = load_config()

        projects = config.get("project", [])

        todos = collect_todos(projects)

        summary = project_summary(todos)

        display_projects(summary)

        return

    if args.command == "doctor":
        config = load_config()

        projects = config.get("project", [])

        config_path = get_config_path()

        results = doctor_check(projects, find_todo_file)

        display_doctor(config_path, projects, results)

        return

    run()


if __name__ == "__main__":
    main()
