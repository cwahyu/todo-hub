# tests/test_config_missing.py

from todohub.config import load_config


def test_load_config_creates_file(tmp_path, monkeypatch):

    config_file = tmp_path / "config.toml"

    monkeypatch.setattr(
        "todohub.config.get_config_dir",
        lambda: config_file,
    )

    cfg = load_config()

    assert config_file.exists()
    assert isinstance(cfg, dict)
