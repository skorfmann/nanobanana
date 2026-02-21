"""MIME type and file extension mapping."""

from pathlib import Path


def extension_from_mime(mime_type: str) -> str:
    """Return file extension for a MIME type (including dot)."""
    mapping = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
    }
    return mapping.get(mime_type, ".png")


def mime_from_extension(path: str) -> str:
    """Return MIME type for a file path based on its extension."""
    ext = Path(path).suffix.lower()
    mapping = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return mapping.get(ext, "image/png")
