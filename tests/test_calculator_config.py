
import os, pytest
from app.calculator_config import Config
from app.exceptions import ConfigurationError

def test_config_load_defaults(monkeypatch, tmp_path):
    monkeypatch.delenv("HISTORY_CSV", raising=False)
    monkeypatch.setenv("AUTOSAVE", "true")
    cfg = Config.load()
    assert cfg.autosave is True
    assert cfg.history_csv == "history.csv"

def test_config_validation(monkeypatch):
    monkeypatch.setenv("AUTOSAVE", "maybe")
    with pytest.raises(ConfigurationError):
        Config.load()
