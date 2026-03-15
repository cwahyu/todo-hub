from pathlib import Path
import shutil
import tomllib
from importlib import resources

from platformdirs import user_config_dir


APP_NAME = "todohub"


def get_config_dir() -> Path:
    """Return platform standard config directory."""
    return Path(user_config_dir(APP_NAME))


def get_config_file() -> Path:
    """Return config.toml path."""
    return get_config_dir() / "config.toml"


def ensure_config() -> Path:
    """
    Ensure config file exists.
    If not, create it from the default template.
    """

    config_dir = get_config_dir()
    config_file = get_config_file()

    if not config_file.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

        default = resources.files("todohub").joinpath("config_default.toml")

        shutil.copy(default, config_file)

        print(f"""
        TodoHub config created.

        Please edit:

        {config_file}
        """)

    return config_file


def load_config() -> dict:
    """Load user config."""

    config_file = ensure_config()

    with open(config_file, "rb") as f:
        return tomllib.load(f)
