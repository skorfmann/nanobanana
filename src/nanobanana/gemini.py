"""Gemini API image generation using google-genai SDK."""

import base64
from pathlib import Path

from google import genai
from google.genai import types

from nanobanana.config import GEMINI_MODEL, HTTP_TIMEOUT
from nanobanana.mime import mime_from_extension


def generate_image(
    api_key: str,
    prompt: str,
    input_images: list[str],
    aspect_ratio: str,
    image_size: str,
) -> tuple[bytes, str]:
    """Generate an image using the Gemini API.

    Returns (image_data, mime_type).
    Raises RuntimeError on failure.
    """
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=HTTP_TIMEOUT * 1000),
    )

    # Build content parts: input images first, then text prompt
    parts: list[types.Part] = []

    for img_path in input_images:
        try:
            data = Path(img_path).read_bytes()
        except OSError as e:
            raise RuntimeError(f"failed to read image {img_path}: {e}") from e
        mime_type = mime_from_extension(img_path)
        parts.append(types.Part.from_bytes(data=data, mime_type=mime_type))

    parts.append(types.Part.from_text(text=prompt))

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=parts,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
                image_generation_config=types.ImageGenerationConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size,
                ),
            ),
        )
    except Exception as e:
        raise RuntimeError(f"request failed: {e}") from e

    # Extract image from response
    if not response.candidates:
        raise RuntimeError("no candidates in response")

    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            return part.inline_data.data, part.inline_data.mime_type

    raise RuntimeError("no image data in response")
