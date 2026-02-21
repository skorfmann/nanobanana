# CLAUDE.md

This file provides context for Claude Code when working on this project.

## IMPORTANT: API Model

**Model**: `gemini-3-pro-image-preview`

This is the specific Gemini model used for image generation. Do NOT change this without understanding the implications - different models have different capabilities, pricing, and availability.

## Project Overview

Nanobanana is a Python CLI tool that wraps Google's Gemini image generation API. It enables text-to-image generation, image editing, and multi-image composition.

## Architecture

- **Package layout**: `src/nanobanana/` with 7 focused modules
- **Dependencies**: `google-genai` (Gemini SDK), `httpx` (OpenRouter HTTP client)
- **Dev deps**: `pytest`
- **Build**: `hatchling` backend, `uv` toolchain
- **Distribution**: PyPI via `uv tool install nanobanana`
- **CI/CD**: GitHub Actions — test + publish to PyPI on every push to main

## Code Structure

```
src/nanobanana/
  __init__.py       # Version via importlib.metadata
  __main__.py       # python -m nanobanana
  cli.py            # argparse, subcommand routing, run(), main()
  templates.py      # Command dataclass, COMMANDS dict, prompt templates
  gemini.py         # Gemini via google-genai SDK
  openrouter.py     # OpenRouter via httpx
  config.py         # XDG config, validation, resolution
  mime.py           # MIME <-> extension mapping
tests/
  test_mime.py      # MIME/extension tests
  test_config.py    # Config validation + resolution tests
  test_cli.py       # CLI flag parsing + subcommand routing tests
  test_api.py       # Request building tests (no network)
```

## Key Modules

- **`cli.py`** — Entry point. `_extract_subcommand()` detects subcommands before argparse. `build_parser()` creates argparse with single-dash flags. `run()` orchestrates subcommand dispatch, template application, config loading, API call, and file output. `main()` wraps `run()` with error handling.
- **`templates.py`** — `Command` dataclass (frozen, slots) with name, description, defaults, and template string. `COMMANDS` dict maps names to commands. `apply()` wraps user prompts in structured TASK/SOURCE MATERIAL/STYLE/LAYOUT/OUTPUT RULES blocks.
- **`config.py`** — Constants (valid aspect ratios, sizes, model names). `FileConfig` dataclass for JSON config. `resolve_config()` applies priority: CLI > config file > env > defaults.
- **`gemini.py`** — Uses `google.genai.Client` for image generation. Passes input images as `Part.from_bytes()`, configures `response_modalities=["IMAGE", "TEXT"]`.
- **`openrouter.py`** — Uses `httpx.post()` with data URL encoding for images. Parses data URL response to extract image bytes + MIME type.
- **`mime.py`** — Bidirectional mapping: `extension_from_mime()` and `mime_from_extension()`.

## Build & Run Commands

```bash
# Run tests
uv run pytest -v

# Run the CLI
uv run nanobanana "prompt"
uv run nanobanana -version
uv run nanobanana -h

# Build package
uv build

# Install as tool
uv tool install .
```

## Configuration

### Config File

Location: `$XDG_CONFIG_HOME/nanobanana/config.json` (default: `~/.config/nanobanana/config.json`)

```json
{
  "api": "openrouter",
  "model": "google/gemini-3-pro-image-preview",
  "aspect": "16:9",
  "size": "2K"
}
```

### Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key
- `OPENROUTER_API_KEY` — OpenRouter API key

### Priority (highest to lowest)

1. CLI flags
2. Config file
3. Environment variables (API keys only)
4. Built-in defaults

## API Details

- **Model**: `gemini-3-pro-image-preview`
- **Timeout**: 120 seconds
- **Gemini auth**: API key via `google.genai.Client(api_key=...)`
- **OpenRouter auth**: Bearer token in Authorization header

### Pricing (approximate)

| Size | Cost per Image |
|------|----------------|
| 1K-2K | ~$0.13 |
| 4K | ~$0.24 |

See [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) for current rates.

## Common Tasks

### Adding a new aspect ratio
1. Add to `VALID_ASPECT_RATIOS` in `config.py`
2. Update help text in `cli.py` (`USAGE_TEXT`)

### Adding a new size option
1. Add to `VALID_SIZES` in `config.py`
2. Update help text in `cli.py` (`USAGE_TEXT`)

### Adding a new image format
1. Add to `extension_from_mime()` in `mime.py`
2. Add to `mime_from_extension()` in `mime.py`

## Testing

```bash
uv run pytest -v
```

Tests cover:
- `extension_from_mime` — MIME type to extension mapping
- `mime_from_extension` — extension to MIME type mapping
- `VALID_ASPECT_RATIOS` — aspect ratio validation
- `VALID_SIZES` — size validation
- Config resolution priority (CLI > config file > env > defaults)
- Config file loading from XDG path
- CLI flag parsing including repeatable `-i`
- Extension auto-correction logic
- API request building (data URLs, missing files)

## Error Handling

Errors are raised as `RuntimeError` with descriptive messages. `main()` catches them, prints `Error: <message>` to stderr, and exits with code 1.

## Versioning

- **Format**: `YYYYMMDD.HHMMSS` (e.g., `20260118.153045`)
- **Local/dev builds**: Show `dev` as version (via `importlib.metadata` fallback)
- **Release builds**: Version stamped into `pyproject.toml` by CI before `uv build`
- **Check version**: `nanobanana -version`

## Release Workflow

GitHub Actions automatically creates releases on every push to main:

1. **Test job**: `uv run pytest -v`
2. **Publish job** (after test passes):
   - Generate version from UTC datetime
   - Stamp version into `pyproject.toml`
   - `uv build` → wheel + sdist
   - `uv publish` → PyPI
   - Create GitHub Release with install instructions

## Examples Directory

The `examples/` folder contains working examples:

| Folder | Purpose |
|--------|---------|
| `basic/` | Simple text-to-image generation |
| `presentation/` | Slide generation from prompts |
| `branded-presentation/` | Template-based consistent styling |

Each example has a README and markdown source with full prompts.

## Image Generation Workflows

### Basic generation
```bash
nanobanana -o output.png "prompt"
```

### Presentation slides (16:9, high-res)
```bash
nanobanana -aspect 16:9 -size 2K -o slide.png "prompt"
```

### Template-based consistency
```bash
# Generate template first
nanobanana -aspect 16:9 -size 2K -o template.png "visual style template..."

# Use template as reference for each slide
nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01.png "slide content..."
nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02.png "slide content..."
```

## Workflow Pattern for Claude Code

When generating multiple related images (like presentation slides):

1. Read the markdown file describing the images/slides
2. Extract prompts for each image
3. If consistency is needed, generate a template first
4. Run nanobanana for each image, passing template with `-i` if applicable
5. Use `-aspect 16:9 -size 2K` for presentation slides
