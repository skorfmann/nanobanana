"""Tests for API request building — no network calls."""

import base64
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from nanobanana.mime import mime_from_extension


def test_openrouter_data_url_building(tmp_path: Path) -> None:
    """Verify data URL construction for OpenRouter image uploads."""
    from nanobanana.openrouter import _load_image_as_data_url

    # Create a small test image file
    test_file = tmp_path / "test.png"
    test_data = b"\x89PNG\r\n\x1a\nfake"
    test_file.write_bytes(test_data)

    data_url = _load_image_as_data_url(str(test_file))

    assert data_url.startswith("data:image/png;base64,")
    # Verify the base64 payload decodes back
    b64_part = data_url.split(",", 1)[1]
    assert base64.b64decode(b64_part) == test_data


def test_openrouter_data_url_jpeg(tmp_path: Path) -> None:
    test_file = tmp_path / "photo.jpg"
    test_file.write_bytes(b"\xff\xd8\xff\xe0fake")

    from nanobanana.openrouter import _load_image_as_data_url

    data_url = _load_image_as_data_url(str(test_file))
    assert data_url.startswith("data:image/jpeg;base64,")


def test_openrouter_load_missing_file() -> None:
    from nanobanana.openrouter import _load_image_as_data_url

    with pytest.raises(RuntimeError, match="failed to read image"):
        _load_image_as_data_url("/nonexistent/file.png")


def test_gemini_load_missing_file() -> None:
    """Verify Gemini generate_image raises on missing input file."""
    from nanobanana.gemini import generate_image

    with pytest.raises(RuntimeError, match="failed to read image"):
        generate_image(
            api_key="fake",
            prompt="test",
            input_images=["/nonexistent/file.png"],
            aspect_ratio="1:1",
            image_size="1K",
        )
