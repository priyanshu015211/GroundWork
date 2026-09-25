import pytest

from groundwork.config import ConfigurationError, Settings


def test_config_can_load_without_keys_for_local_bootstrap(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    settings = Settings.from_env(require_api_keys=False)
    assert settings.max_research_rounds == 3


def test_config_requires_keys_for_live_clients(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("TAVILY_API_KEY", "test")
    with pytest.raises(ConfigurationError):
        Settings.from_env(require_api_keys=True)
