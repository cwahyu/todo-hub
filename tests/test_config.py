# tests/test_config.py

from pathlib import Path

import tomllib

CONFIG_PATH = Path(__file__).parent / "config.toml"


def load_projects(config_path=None):

    path = config_path or CONFIG_PATH

    config = tomllib.loads(path.read_text())

    projects = []

    for p in config["project"]:
        project_path = Path(p["path"]).expanduser()

        projects.append(
            {
                "name": p["name"],
                "path": project_path,
            }
        )

    return projects
