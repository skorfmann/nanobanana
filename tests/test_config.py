"""Tests for config validation and resolution — ported from Go tests."""

import json
import os

import pytest

from nanobanana.config import (
    VALID_ASPECT_RATIOS,
    VALID_SIZES,
    FileConfig,
    _run_key_command,
    load_config,
    resolve_config,
)


# --- Aspect ratio validation (ported from TestValidAspectRatios) ---

@pytest.mark.parametrize(
    "ratio",
    ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
)
def test_valid_aspect_ratios(ratio: str) -> None:
    assert ratio in VALID_ASPECT_RATIOS


@pytest.mark.parametrize("ratio", ["1:2", "16:10", "4:4", "invalid", ""])
def test_invalid_aspect_ratios(ratio: str) -> None:
    assert ratio not in VALID_ASPECT_RATIOS


# --- Size validation (ported from TestValidSizes) ---

@pytest.mark.parametrize("size", ["1K", "2K", "4K"])
def test_valid_sizes(size: str) -> None:
    assert size in VALID_SIZES


@pytest.mark.parametrize("size", ["1k", "3K", "8K", "HD", ""])
def test_invalid_sizes(size: str) -> None:
    assert size not in VALID_SIZES


# --- Config resolution ---

def test_resolve_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    aspect, size, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=None,
    )
    assert aspect == "1:1"
    assert size == "1K"
    assert config.use_openrouter is False
    assert config.api_key == "test-key"


def test_resolve_file_config_overrides_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    fc = FileConfig(api="openrouter", model="my/model", aspect="16:9", size="2K")
    aspect, size, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=fc,
    )
    assert aspect == "16:9"
    assert size == "2K"
    assert config.use_openrouter is True
    assert config.model == "my/model"


def test_resolve_cli_flags_override_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "gem-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    fc = FileConfig(aspect="16:9", size="2K")
    aspect, size, config = resolve_config(
        aspect_flag="3:2", size_flag="4K", model_flag="", file_config=fc,
    )
    assert aspect == "3:2"
    assert size == "4K"
    assert config.use_openrouter is False


def test_resolve_model_flag_forces_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    aspect, size, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="custom/model", file_config=None,
    )
    assert config.use_openrouter is True
    assert config.model == "custom/model"


def test_resolve_missing_gemini_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        resolve_config(
            aspect_flag="", size_flag="", model_flag="", file_config=None,
        )


def test_resolve_missing_openrouter_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        resolve_config(
            aspect_flag="", size_flag="", model_flag="custom/m", file_config=None,
        )


def test_resolve_invalid_aspect_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "key")

    with pytest.raises(RuntimeError, match="invalid aspect ratio"):
        resolve_config(
            aspect_flag="99:1", size_flag="", model_flag="", file_config=None,
        )


def test_resolve_invalid_size_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "key")

    with pytest.raises(RuntimeError, match="invalid size"):
        resolve_config(
            aspect_flag="", size_flag="8K", model_flag="", file_config=None,
        )


def test_load_config_from_file(tmp_path: str, monkeypatch: pytest.MonkeyPatch) -> None:
    config_dir = tmp_path / "nanobanana"
    config_dir.mkdir()
    config_file = config_dir / "config.json"
    config_file.write_text(json.dumps({
        "api": "openrouter",
        "model": "test/model",
        "aspect": "4:3",
        "size": "2K",
    }))

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    fc = load_config()
    assert fc is not None
    assert fc.api == "openrouter"
    assert fc.model == "test/model"
    assert fc.aspect == "4:3"
    assert fc.size == "2K"


def test_load_config_missing_returns_none(tmp_path: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert load_config() is None


def test_openrouter_fallback_when_only_or_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """When only OPENROUTER_API_KEY is set and no explicit model, use OpenRouter."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    _, _, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=None,
    )
    assert config.use_openrouter is True
    assert config.model == "google/gemini-3-pro-image-preview"


# --- key_command ---

def test_run_key_command_success() -> None:
    assert _run_key_command("echo secret-key-123") == "secret-key-123"


def test_run_key_command_failure() -> None:
    with pytest.raises(RuntimeError, match="key_command failed"):
        _run_key_command("false")


def test_run_key_command_empty_output() -> None:
    with pytest.raises(RuntimeError, match="key_command returned empty output"):
        _run_key_command("echo ''")


def test_key_command_used_for_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    """key_command provides API key when env var is not set."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    fc = FileConfig(api="openrouter", key_command="echo my-secret-key")
    _, _, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=fc,
    )
    assert config.use_openrouter is True
    assert config.api_key == "my-secret-key"


def test_key_command_used_for_gemini(monkeypatch: pytest.MonkeyPatch) -> None:
    """key_command provides Gemini API key when env var is not set."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    fc = FileConfig(key_command="echo gemini-secret")
    _, _, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=fc,
    )
    assert config.use_openrouter is False
    assert config.api_key == "gemini-secret"


def test_env_var_takes_priority_over_key_command(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variable should be used even when key_command is set."""
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    fc = FileConfig(key_command="echo should-not-be-called")
    _, _, config = resolve_config(
        aspect_flag="", size_flag="", model_flag="", file_config=fc,
    )
    assert config.api_key == "env-key"


def test_load_config_with_key_command(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_dir = tmp_path / "nanobanana"
    config_dir.mkdir()
    config_file = config_dir / "config.json"
    config_file.write_text(json.dumps({
        "api": "openrouter",
        "key_command": "op read 'op://API Keys/OpenRouter/credential'",
    }))

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    fc = load_config()
    assert fc is not None
    assert fc.key_command == "op read 'op://API Keys/OpenRouter/credential'"
