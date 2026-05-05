"""
Configuration management for TermChat.

Handles loading, saving, and validating configuration from YAML files
and environment variables.
"""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


DEFAULT_CONFIG_PATH = Path.home() / ".termchat" / "config.yaml"
DEFAULT_SESSIONS_DIR = Path.home() / ".termchat" / "sessions"


@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider."""

    api_key: str = ""
    base_url: str = ""
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 1.0
    system_prompt: str = "You are a helpful assistant."
    timeout: int = 120


@dataclass
class Config:
    """Main application configuration."""

    default_provider: str = "openai"
    theme: str = "monokai"
    max_history: int = 50
    auto_save: bool = True
    stream: bool = True
    providers: Dict[str, ProviderConfig] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize preset providers if providers dict is empty."""
        if not self.providers:
            for name, preset in self.PRESET_PROVIDERS.items():
                self.providers[name] = ProviderConfig(
                    base_url=preset["base_url"],
                    model=preset["model"],
                )

    # Preset provider configurations
    PRESET_PROVIDERS = {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini",
        },
        "deepseek": {
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
        },
        "ollama": {
            "base_url": "http://localhost:11434/v1",
            "model": "llama3",
            "api_key": "ollama",
        },
        "groq": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "llama-3.1-70b-versatile",
        },
        "together": {
            "base_url": "https://api.together.xyz/v1",
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        },
        "openrouter": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "openai/gpt-4o-mini",
        },
    }

    def get_provider(self, name: str) -> Optional[ProviderConfig]:
        """Get provider configuration by name."""
        return self.providers.get(name)

    def list_providers(self) -> list:
        """List all configured provider names."""
        return list(self.providers.keys())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize config to dictionary."""
        providers_dict = {}
        for name, prov in self.providers.items():
            providers_dict[name] = {
                "api_key": prov.api_key,
                "base_url": prov.base_url,
                "model": prov.model,
                "max_tokens": prov.max_tokens,
                "temperature": prov.temperature,
                "top_p": prov.top_p,
                "system_prompt": prov.system_prompt,
                "timeout": prov.timeout,
            }
        return {
            "default_provider": self.default_provider,
            "theme": self.theme,
            "max_history": self.max_history,
            "auto_save": self.auto_save,
            "stream": self.stream,
            "providers": providers_dict,
        }


def _load_env_overrides() -> Dict[str, str]:
    """Load API keys from environment variables."""
    env_map = {
        "openai": "OPENAI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "groq": "GROQ_API_KEY",
        "together": "TOGETHER_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    result = {}
    for provider, env_var in env_map.items():
        val = os.environ.get(env_var, "")
        if val:
            result[provider] = val
    return result


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from file, with environment variable overrides."""
    config_path = config_path or DEFAULT_CONFIG_PATH
    config = Config()

    # Initialize preset providers
    for name, preset in Config.PRESET_PROVIDERS.items():
        config.providers[name] = ProviderConfig(
            base_url=preset["base_url"],
            model=preset["model"],
        )

    # Load from file if exists
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            config.default_provider = data.get("default_provider", config.default_provider)
            config.theme = data.get("theme", config.theme)
            config.max_history = data.get("max_history", config.max_history)
            config.auto_save = data.get("auto_save", config.auto_save)
            config.stream = data.get("stream", config.stream)

            for name, prov_data in data.get("providers", {}).items():
                if name in config.providers:
                    p = config.providers[name]
                    p.api_key = prov_data.get("api_key", p.api_key)
                    p.base_url = prov_data.get("base_url", p.base_url)
                    p.model = prov_data.get("model", p.model)
                    p.max_tokens = prov_data.get("max_tokens", p.max_tokens)
                    p.temperature = prov_data.get("temperature", p.temperature)
                    p.top_p = prov_data.get("top_p", p.top_p)
                    p.system_prompt = prov_data.get("system_prompt", p.system_prompt)
                    p.timeout = prov_data.get("timeout", p.timeout)
                else:
                    config.providers[name] = ProviderConfig(**prov_data)
        except (yaml.YAMLError, IOError) as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")

    # Environment variable overrides for API keys
    env_overrides = _load_env_overrides()
    for provider, api_key in env_overrides.items():
        if provider in config.providers:
            config.providers[provider].api_key = api_key

    return config


def save_config(config: Config, config_path: Optional[Path] = None) -> None:
    """Save configuration to file."""
    config_path = config_path or DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)

    data = config.to_dict()
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def create_default_config(config_path: Optional[Path] = None) -> Config:
    """Create and save a default configuration file."""
    config = load_config(config_path)
    save_config(config, config_path)
    return config
