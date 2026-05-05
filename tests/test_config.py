"""Tests for TermChat configuration module."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from termchat.config import (
    Config,
    ProviderConfig,
    load_config,
    save_config,
    create_default_config,
    _load_env_overrides,
)


class TestProviderConfig:
    """Tests for ProviderConfig dataclass."""

    def test_default_values(self):
        prov = ProviderConfig()
        assert prov.api_key == ""
        assert prov.base_url == ""
        assert prov.model == ""
        assert prov.max_tokens == 4096
        assert prov.temperature == 0.7
        assert prov.top_p == 1.0
        assert prov.system_prompt == "You are a helpful assistant."
        assert prov.timeout == 120

    def test_custom_values(self):
        prov = ProviderConfig(
            api_key="test-key",
            base_url="https://api.test.com/v1",
            model="test-model",
            max_tokens=2048,
            temperature=0.5,
        )
        assert prov.api_key == "test-key"
        assert prov.base_url == "https://api.test.com/v1"
        assert prov.model == "test-model"
        assert prov.max_tokens == 2048
        assert prov.temperature == 0.5


class TestConfig:
    """Tests for Config dataclass."""

    def test_default_config(self):
        config = Config()
        assert config.default_provider == "openai"
        assert config.theme == "monokai"
        assert config.max_history == 50
        assert config.auto_save is True
        assert config.stream is True

    def test_preset_providers(self):
        config = Config()
        for name, preset in Config.PRESET_PROVIDERS.items():
            prov = config.get_provider(name)
            assert prov is not None
            assert prov.base_url == preset["base_url"]
            assert prov.model == preset["model"]

    def test_list_providers(self):
        config = Config()
        providers = config.list_providers()
        assert len(providers) >= 6
        assert "openai" in providers
        assert "deepseek" in providers
        assert "ollama" in providers

    def test_to_dict(self):
        config = Config()
        data = config.to_dict()
        assert "default_provider" in data
        assert "providers" in data
        assert "openai" in data["providers"]


class TestLoadSaveConfig:
    """Tests for config loading and saving."""

    def test_create_default_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = create_default_config(config_path)
            assert config_path.exists()
            assert config.default_provider == "openai"
            assert len(config.list_providers()) >= 6

    def test_load_existing_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            # Create a config file
            data = {
                "default_provider": "deepseek",
                "theme": "dark",
                "max_history": 100,
                "providers": {
                    "openai": {
                        "api_key": "sk-test",
                        "model": "gpt-4",
                    },
                },
            }
            with open(config_path, "w") as f:
                yaml.dump(data, f)

            config = load_config(config_path)
            assert config.default_provider == "deepseek"
            assert config.theme == "dark"
            assert config.max_history == 100
            openai_prov = config.get_provider("openai")
            assert openai_prov.api_key == "sk-test"
            assert openai_prov.model == "gpt-4"

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-env-key")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-deepseek-env")
        overrides = _load_env_overrides()
        assert overrides["openai"] == "sk-env-key"
        assert overrides["deepseek"] == "sk-deepseek-env"

    def test_load_nonexistent_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "nonexistent.yaml"
            config = load_config(config_path)
            # Should return default config
            assert config.default_provider == "openai"

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = load_config(config_path)
            config.default_provider = "ollama"
            config.theme = "light"
            save_config(config, config_path)

            reloaded = load_config(config_path)
            assert reloaded.default_provider == "ollama"
            assert reloaded.theme == "light"


class TestMessage:
    """Tests for Message class."""

    def test_message_creation(self):
        from termchat.provider import Message

        msg = Message("user", "Hello, world!")
        assert msg.role == "user"
        assert msg.content == "Hello, world!"

    def test_message_to_dict(self):
        from termchat.provider import Message

        msg = Message("assistant", "Hi there!")
        d = msg.to_dict()
        assert d == {"role": "assistant", "content": "Hi there!"}

    def test_message_repr(self):
        from termchat.provider import Message

        msg = Message("user", "Hello")
        assert "user" in repr(msg)
        assert "Hello" in repr(msg)
