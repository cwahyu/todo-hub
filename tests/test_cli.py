from datetime import date, timedelta
from pathlib import Path

from todohub.main import main


def test_cli_output(tmp_path, monkeypatch, capsys):

    # create fake project
    project = tmp_path / "demo"
    project.mkdir()

    todo = project / "TODO.md"

    todo.write_text(
        f"- [ ] overdue task @{date.today() - timedelta(days=1)}\n"
        f"- [ ] today task @{date.today()}\n"
        f"- [ ] later task @{date.today() + timedelta(days=10)}\n"
    )

    # create fake config
    config = tmp_path / "config.toml"

    config.write_text(
        f"""
[[project]]
name = "demo"
path = "{project}"
"""
    )

    # patch config loader
    from todohub import config as config_module

    monkeypatch.setattr(
        config_module,
        "get_config_file",
        lambda: Path(config),
    )

    # run CLI
    main()

    output = capsys.readouterr().out

    assert "Overdue" in output
    assert "Today" in output
    assert "Later" in output
