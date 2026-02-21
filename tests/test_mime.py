"""Tests for MIME type / extension mapping — ported from Go tests."""

import pytest

from nanobanana.mime import extension_from_mime, mime_from_extension


@pytest.mark.parametrize(
    "mime_type, expected",
    [
        ("image/png", ".png"),
        ("image/jpeg", ".jpg"),
        ("image/webp", ".webp"),
        ("image/gif", ".png"),     # unsupported, defaults to .png
        ("unknown/type", ".png"),  # unknown, defaults to .png
        ("", ".png"),              # empty, defaults to .png
    ],
)
def test_extension_from_mime(mime_type: str, expected: str) -> None:
    assert extension_from_mime(mime_type) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("image.png", "image/png"),
        ("image.PNG", "image/png"),
        ("image.jpg", "image/jpeg"),
        ("image.jpeg", "image/jpeg"),
        ("image.JPEG", "image/jpeg"),
        ("image.webp", "image/webp"),
        ("image.gif", "image/gif"),
        ("image.bmp", "image/png"),           # unsupported, defaults to image/png
        ("image", "image/png"),               # no extension, defaults to image/png
        ("/path/to/image.jpg", "image/jpeg"),
    ],
)
def test_mime_from_extension(path: str, expected: str) -> None:
    assert mime_from_extension(path) == expected
