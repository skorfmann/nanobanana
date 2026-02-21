# Nanobanana

A lightweight CLI tool for generating and editing images using Google's Gemini API or OpenRouter.

> **Best used with your coding agent CLI of choice!** This tool pairs excellently with [Claude Code](https://claude.ai/claude-code) and similar AI coding assistants for automated image generation workflows.

## Features

- **Text-to-image generation** - Create images from text prompts
- **Image editing** - Transform existing images with text instructions
- **Multi-image composition** - Combine multiple input images
- **Flexible output** - 10 aspect ratios and 3 size options
- **Multiple API backends** - Use Gemini API directly or via OpenRouter

## Requirements

- Python 3.14+
- Google Gemini API key OR OpenRouter API key

## Installation

### From source (recommended — installs CLI + Claude Code skill)

```bash
git clone https://github.com/sussdorff/nanobanana.git
cd nanobanana
./install.sh
```

This installs the CLI via `uv tool install` and copies the Claude Code skill to `~/.claude/skills/nanobanana/`. Run it again to upgrade both.

### CLI only (via uv)

```bash
uv tool install nanobanana
```

### CLI only (via pip)

```bash
pip install nanobanana
```

## Setup

### Option 1: Gemini API (Direct)

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set it as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Option 2: OpenRouter

1. Get an API key from [OpenRouter](https://openrouter.ai/keys)
2. Set it as an environment variable:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Configuration

### Config File (Recommended)

Create a config file at `~/.config/nanobanana/config.json`:

```json
{
  "api": "openrouter",
  "model": "google/gemini-3-pro-image-preview",
  "aspect": "16:9",
  "size": "2K"
}
```

| Field | Description | Values |
|-------|-------------|--------|
| `api` | API backend | `gemini` or `openrouter` |
| `model` | OpenRouter model | e.g., `google/gemini-3-pro-image-preview` |
| `aspect` | Default aspect ratio | `1:1`, `16:9`, etc. |
| `size` | Default image size | `1K`, `2K`, `4K` |

The config file location follows the XDG spec: `$XDG_CONFIG_HOME/nanobanana/config.json`

### Priority

Settings are resolved in this order (highest to lowest):

1. CLI flags
2. Config file
3. Environment variables (API keys only)
4. Built-in defaults

### Shell Wrapper Example

For 1Password users, a simple wrapper in `.zshrc`:

```bash
nanobanana() {
  if [[ -z "$OPENROUTER_API_KEY" ]]; then
    export OPENROUTER_API_KEY="$(op read 'op://API Keys/OpenRouter/credential')"
  fi
  command nanobanana "$@"
}
```

## Usage

```bash
nanobanana <command> [options] "prompt"
nanobanana [options] "prompt"            # defaults to free-form generation
```

### Commands

Each command wraps your prompt in an optimized template with sensible defaults.

**Design Exploration:**

| Command | Description | Default Aspect | Default Size |
|---------|-------------|----------------|--------------|
| `dashboard` | KPI/analytics dashboard mockup | 16:9 | 2K |
| `moodboard` | Website/app moodboard collage | 1:1 | 2K |
| `explore` | Same concept in 4 style variations | 1:1 | 2K |
| `wireframe` | UI wireframe or screen layout | 16:9 | 2K |

**Content Creation:**

| Command | Description | Default Aspect | Default Size |
|---------|-------------|----------------|--------------|
| `slide` | Presentation slide | 16:9 | 2K |
| `social` | Social media post image | 1:1 | 2K |
| `icon` | App icon | 1:1 | 1K |
| `architecture` | System/cloud architecture diagram | 16:9 | 2K |

**Base:**

| Command | Description |
|---------|-------------|
| `generate` | Free-form prompt (explicit version of default) |
| `help` | Show help for all commands or a specific command |
| `version` | Show version |

If the first argument is not a known command, it is treated as a free-form prompt (backwards compatible).

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable for multiple images) | none |
| `-o <file>` | Output filename | `image_YYYYMMDD_HHMMSS.png` |
| `-aspect <ratio>` | Aspect ratio (overrides command default) | `1:1` |
| `-size <size>` | Image size (overrides command default) | `1K` |
| `-model <model>` | OpenRouter model (enables OpenRouter API) | `google/gemini-3-pro-image-preview` |
| `-h` | Show help | - |
| `-version` | Show version | - |

### Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Supported Sizes

| Size | Resolution |
|------|------------|
| `1K` | ~1024px |
| `2K` | ~2048px |
| `4K` | ~4096px |

### Supported Image Formats

PNG, JPEG, WebP, GIF

## Examples

### Subcommands

```bash
# Dashboard mockup (16:9, 2K by default)
nanobanana dashboard "SaaS metrics with MRR, churn rate, and user growth"

# Presentation slide
nanobanana slide "Q4 revenue highlights: 40% YoY growth, 3 new enterprise clients"

# App icon
nanobanana icon "podcast app with microphone and sound waves"

# Architecture diagram
nanobanana architecture "microservices with API gateway, 3 services, Redis cache, PostgreSQL"

# Design exploration (4 style variations)
nanobanana explore "landing page hero for a meditation app"

# Moodboard
nanobanana moodboard "fintech app targeting young professionals"

# Wireframe
nanobanana wireframe "settings page with account, notifications, and billing"

# Social media post
nanobanana social "product launch announcement for an AI writing tool"

# Override command defaults
nanobanana dashboard -size 4K "quarterly revenue breakdown"
nanobanana social -aspect 9:16 "instagram story for product launch"

# Get help for a specific command
nanobanana help dashboard
```

### Free-form generation

```bash
# Simple generation (no command = free-form)
nanobanana "a cute cat sitting on a windowsill"

# With aspect ratio and size
nanobanana -aspect 16:9 -size 2K "cinematic mountain landscape at sunset"

# Custom output filename
nanobanana -o hero-image.png "abstract geometric pattern"
```

### Using OpenRouter

```bash
# Use default model (gemini-3-pro-image-preview)
nanobanana -model google/gemini-3-pro-image-preview "a cute cat"

# Use a different model
nanobanana -model google/gemini-2.5-flash-image-preview "a sunset over mountains"
```

### Image editing

```bash
# Style transfer
nanobanana -i photo.jpg "transform into watercolor painting"

# Modifications
nanobanana -i portrait.png "add sunglasses"
```

### Multi-image composition

```bash
# Combine images
nanobanana -i background.png -i subject.png "place the subject in the scene"

# Style reference
nanobanana -i content.jpg -i style.jpg "apply the style to the content image"
```

## Examples Directory

The `examples/` folder contains working examples with generated images:

### basic/
Simple text-to-image generation.

```bash
nanobanana -o basic_example.png "a friendly yellow banana character"
```

### presentation/
Generate presentation slides from text prompts.

```bash
nanobanana -aspect 16:9 -size 2K -o slide_01.png "title slide prompt..."
nanobanana -aspect 16:9 -size 2K -o slide_02.png "content slide prompt..."
```

### branded-presentation/
Use a template image as a style reference for consistent branding across slides.

```bash
# 1. Generate a style template first
nanobanana -aspect 16:9 -size 2K -o template.png "slide template with brand colors..."

# 2. Generate slides using template as reference
nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01.png "title slide..."
nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02.png "content slide..."
```

Each example includes a README and the markdown source used to generate the images. See the `examples/` folder for full prompts and generated outputs.

## Using with Coding Agents

Nanobanana works great with AI coding assistants like Claude Code for automated image generation workflows:

1. Describe slides/images in a markdown file
2. Your coding agent reads the markdown and extracts prompts
3. The agent runs nanobanana to generate each image

See `examples/branded-presentation/` for a complete workflow demonstration.

## API Pricing

### Gemini API (Direct)

Uses `gemini-3-pro-image-preview` model. Approximate costs:

| Size | Cost per Image |
|------|----------------|
| 1K-2K | ~$0.13 |
| 4K | ~$0.24 |

See [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) for current rates.

### OpenRouter

Pricing varies by model. See [OpenRouter Pricing](https://openrouter.ai/models) for current rates.

## Development

```bash
# Run tests
uv run pytest -v

# Run the CLI locally
uv run nanobanana -version
uv run nanobanana -h
```

## License

MIT
