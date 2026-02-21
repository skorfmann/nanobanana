"""OpenRouter API image generation using httpx."""

import base64

import httpx

from nanobanana.config import HTTP_TIMEOUT
from nanobanana.mime import mime_from_extension

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


def _load_image_as_data_url(path: str) -> str:
    """Load an image file and return a data URL."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise RuntimeError(f"failed to read image {path}: {e}") from e

    mime_type = mime_from_extension(path)
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime_type};base64,{b64}"


def generate_image(
    api_key: str,
    model: str,
    prompt: str,
    input_images: list[str],
    aspect_ratio: str,
    image_size: str,
) -> tuple[bytes, str]:
    """Generate an image using the OpenRouter API.

    Returns (image_data, mime_type).
    Raises RuntimeError on failure.
    """
    # Build content parts
    content_parts: list[dict] = []

    for img_path in input_images:
        data_url = _load_image_as_data_url(img_path)
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": data_url},
        })

    content_parts.append({"type": "text", "text": prompt})

    # Build request payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content_parts}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
        },
    }

    try:
        resp = httpx.post(
            OPENROUTER_ENDPOINT,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            timeout=HTTP_TIMEOUT,
        )
    except httpx.HTTPError as e:
        raise RuntimeError(f"request failed: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(
            f"HTTP error: {resp.status_code} {resp.reason_phrase} - {resp.text}"
        )

    data = resp.json()

    if data.get("error"):
        raise RuntimeError(f"API error: {data['error'].get('message', data['error'])}")

    # Extract image data
    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError("no choices in response")

    images = choices[0].get("message", {}).get("images", [])
    if not images:
        raise RuntimeError("no images in response")

    # Parse data URL (format: data:image/png;base64,iVBORw0KGgo...)
    data_url = images[0].get("image_url", {}).get("url", "")
    if not data_url.startswith("data:"):
        raise RuntimeError(
            f"unexpected image URL format: {data_url[:50]}"
        )

    parts = data_url.split(",", 1)
    if len(parts) != 2:
        raise RuntimeError("invalid data URL format")

    header, b64_data = parts

    # Extract MIME type from header
    mime_type = "image/png"  # default
    if header.startswith("data:"):
        header_parts = header[5:].split(";")
        if header_parts and header_parts[0]:
            mime_type = header_parts[0]

    try:
        image_data = base64.b64decode(b64_data)
    except Exception as e:
        raise RuntimeError(f"failed to decode image data: {e}") from e

    return image_data, mime_type
