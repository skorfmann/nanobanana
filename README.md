# Nanobanana

A lightweight CLI tool for generating and editing images using Google's Gemini API or OpenRouter.

> **Best used with your coding agent CLI of choice!** This tool pairs excellently with [Claude Code](https://claude.ai/claude-code) and similar AI coding assistants for automated image generation workflows.

## Features

- **Text-to-image generation** - Create images from text prompts
- **Image editing** - Transform existing images with text instructions
- **Multi-image composition** - Combine multiple input images
- **Flexible output** - 9 aspect ratios and 3 size options
- **Multiple API backends** - Use Gemini API directly or via OpenRouter

## Requirements

- Go 1.25+ (for building from source)
- Google Gemini API key OR OpenRouter API key

## Installation

### Homebrew (macOS/Linux)

```bash
brew tap skorfmann/nanobanana
brew install nanobanana
```

To upgrade to the latest version:

```bash
brew upgrade nanobanana
```

### From GitHub Releases

Download the latest binary for your platform from the [Releases](../../releases) page.

```bash
# Example for macOS arm64
curl -L -o nanobanana https://github.com/skorfmann/nanobanana/releases/latest/download/nanobanana-darwin-arm64
chmod +x nanobanana
./nanobanana -version
```

### From source

```bash
git clone https://github.com/skorfmann/nanobanana.git
cd nanobanana
go build -o nanobanana main.go
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
  /path/to/nanobanana "$@"
}
```

## Usage

```bash
nanobanana [options] "prompt"
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable for multiple images) | none |
| `-o <file>` | Output filename | `image_YYYYMMDD_HHMMSS.png` |
| `-aspect <ratio>` | Aspect ratio | `1:1` |
| `-size <size>` | Image size | `1K` |
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

### Text-to-image

```bash
# Simple generation
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

## Examples

The `examples/` folder contains working examples with generated images:

### basic/
Simple text-to-image generation.

```bash
./nanobanana -o basic_example.png "a friendly yellow banana character"
```

### presentation/
Generate presentation slides from text prompts.

```bash
./nanobanana -aspect 16:9 -size 2K -o slide_01.png "title slide prompt..."
./nanobanana -aspect 16:9 -size 2K -o slide_02.png "content slide prompt..."
```

### branded-presentation/
Use a template image as a style reference for consistent branding across slides.

```bash
# 1. Generate a style template first
./nanobanana -aspect 16:9 -size 2K -o template.png "slide template with brand colors..."

# 2. Generate slides using template as reference
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01.png "title slide..."
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02.png "content slide..."
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

## License

MIT
