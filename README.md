# Nanobanana

A lightweight CLI tool for generating and editing images using Google's Gemini API.

> **Best used with your coding agent CLI of choice!** This tool pairs excellently with [Claude Code](https://claude.ai/claude-code) and similar AI coding assistants for automated image generation workflows.

## Features

- **Text-to-image generation** - Create images from text prompts
- **Image editing** - Transform existing images with text instructions
- **Multi-image composition** - Combine multiple input images
- **Model selection** - All current Nano Banana models (Lite, 2, Pro) via `-model`
- **Flexible output** - Up to 14 aspect ratios and 4 size options (model-dependent)

## Requirements

- Go 1.25+ (for building from source)
- Google Gemini API key with access to the Gemini image models (Nano Banana)

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

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set it as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
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
| `-model <name>` | Model: `lite`, `flash`, `pro`, or a full model ID | `flash` |
| `-aspect <ratio>` | Aspect ratio | `1:1` |
| `-size <size>` | Image size | `1K` |
| `-h` | Show help | - |
| `-version` | Show version | - |

### Models

| Alias | Model ID | Best For | Sizes |
|-------|----------|----------|-------|
| `lite` | `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite) | Fast, cheap drafts and high volume | 1K |
| `flash` | `gemini-3.1-flash-image` (Nano Banana 2) | Go-to model, best balance (default) | 0.5K, 1K, 2K, 4K |
| `pro` | `gemini-3-pro-image` (Nano Banana Pro) | Highest quality, complex compositions | 1K, 2K, 4K |

Full Gemini model IDs (e.g. `gemini-2.5-flash-image`) are also accepted, so new models work without a rebuild.

### Supported Aspect Ratios

All models: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

`flash` only: `1:4`, `4:1`, `1:8`, `8:1` (extreme banners/skyscrapers)

### Supported Sizes

| Size | Resolution | Models |
|------|------------|--------|
| `0.5K` | ~512px | flash |
| `1K` | ~1024px | all |
| `2K` | ~2048px | flash, pro |
| `4K` | ~4096px | flash, pro |

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

# Cheap draft with the lite model
nanobanana -model lite "quick concept sketch of a logo"

# Maximum quality with the pro model
nanobanana -model pro -size 4K "detailed product shot of a watch"

# Extreme banner ratio (flash only)
nanobanana -aspect 4:1 -size 0.5K "website header, abstract gradient"
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

Approximate cost per image (paid tier, July 2026):

| Model | 0.5K | 1K | 2K | 4K |
|-------|------|----|----|----|
| `lite` | - | ~$0.034 | - | - |
| `flash` (default) | ~$0.045 | ~$0.067 | ~$0.101 | ~$0.151 |
| `pro` | - | ~$0.134 | ~$0.134 | ~$0.24 |

See [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) for current rates.

## License

MIT
