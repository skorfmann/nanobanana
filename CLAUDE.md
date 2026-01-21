# CLAUDE.md

This file provides context for Claude Code when working on this project.

## ⚠️ IMPORTANT: API Model

**Model**: `gemini-3-pro-image-preview`

This is the specific Gemini model used for image generation. Do NOT change this without understanding the implications - different models have different capabilities, pricing, and availability.

## Project Overview

Nanobanana is a single-file Go CLI tool that wraps Google's Gemini image generation API. It enables text-to-image generation, image editing, and multi-image composition.

## Architecture

- **Single file**: All code lives in `main.go` (~710 lines)
- **Zero dependencies**: Uses only Go standard library
- **Cross-platform**: Builds for Linux, macOS, and Windows (amd64/arm64)
- **CI/CD**: GitHub Actions releases on every push to main

## Code Structure (main.go)

| Section | Description |
|---------|-------------|
| Type definitions | Request/response structs for Gemini and OpenRouter APIs |
| Configuration | Constants (API endpoints, valid ratios/sizes) |
| `FileConfig` | XDG config file structure and loading |
| `main()` / `run()` | CLI orchestration |
| `generateImageGemini()` | Direct Gemini API interaction |
| `generateImageOpenRouter()` | OpenRouter API interaction |
| MIME helpers | Extension/MIME type conversions |
| `loadImage()` | File loading for input images |
| `printUsage()` | Help text |

## Key Types

- `Version` - Build version string (set via `-ldflags`)
- `stringSlice` - Custom flag type for repeatable `-i` flags
- `FileConfig` - XDG config file structure (`api`, `model`, `aspect`, `size`)
- `APIConfig` - Runtime API configuration
- `GenerateRequest` / `GenerateResponse` - Gemini API payload structures
- `OpenRouterRequest` / `OpenRouterResponse` - OpenRouter API payload structures

## Build Commands

```bash
# Local dev build (version = "dev")
go build -o nanobanana main.go

# Release build with version injection
VERSION=$(date -u +%Y%m%d.%H%M%S)
go build -ldflags="-s -w -X main.Version=$VERSION" -o nanobanana main.go

# Cross-compile for specific platform
GOOS=linux GOARCH=amd64 go build -ldflags="-s -w -X main.Version=$VERSION" -o nanobanana-linux-amd64 main.go

# Run
./nanobanana "prompt"

# Check version
./nanobanana -version
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

- `GEMINI_API_KEY` - Google Gemini API key
- `OPENROUTER_API_KEY` - OpenRouter API key

### Priority (highest to lowest)

1. CLI flags
2. Config file
3. Environment variables (API keys only)
4. Built-in defaults

## API Details

- **Model**: `gemini-3-pro-image-preview`
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent`
- **Timeout**: 120 seconds
- **Auth**: API key passed via `x-goog-api-key` header

### Pricing (approximate)

| Size | Cost per Image |
|------|----------------|
| 1K-2K | ~$0.13 |
| 4K | ~$0.24 |

See [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) for current rates.

## Common Tasks

### Adding a new aspect ratio
1. Add to `validAspectRatios` map (line ~40)
2. Update help text in `printUsage()`

### Adding a new size option
1. Add to `validSizes` map (line ~48)
2. Update help text in `printUsage()`

### Adding a new image format
1. Add case to `mimeFromExtension()` (line ~291)
2. Add case to `extensionFromMime()` (line ~278)

## Testing

### Unit Tests

Run automated tests:

```bash
go test -v ./...
```

Tests cover:
- `stringSlice` flag type (String, Set methods)
- `extensionFromMime` - MIME type to extension mapping
- `mimeFromExtension` - extension to MIME type mapping
- `validAspectRatios` - aspect ratio validation
- `validSizes` - size validation
- Extension auto-correction logic

### Manual Testing

```bash
# Text-to-image
./nanobanana "test prompt"

# Image editing
./nanobanana -i test.jpg "edit instruction"

# Check output file was created
ls -la image_*.jpg
```

## Error Handling

Errors are wrapped with context using `fmt.Errorf("context: %w", err)`. The main error paths:

- Missing API key (`GEMINI_API_KEY` or `OPENROUTER_API_KEY`)
- Invalid config file (parse error)
- Invalid aspect ratio or size
- Failed to load input image
- API request failure
- No image in API response

## Versioning

- **Format**: `YYYYMMDD.HHMMSS` (e.g., `20260118.153045`)
- **Local builds**: Show `dev` as version
- **Release builds**: Version injected via `-ldflags="-X main.Version=$VERSION"`
- **Check version**: `./nanobanana -version`

## Release Workflow

GitHub Actions automatically creates releases on every push to main:

1. **Trigger**: Push to `main` branch
2. **Checks**: `go fmt` and `go vet`
3. **Version**: Generated from UTC datetime
4. **Build matrix**: 6 platform/arch combinations
5. **Artifacts**: Binaries + `checksums.txt`
6. **Release**: Created with datetime tag (e.g., `20260118.153045`)

### Build Matrix

| OS | Architecture | Binary Name |
|----|--------------|-------------|
| Linux | amd64 | `nanobanana-linux-amd64` |
| Linux | arm64 | `nanobanana-linux-arm64` |
| macOS | amd64 | `nanobanana-darwin-amd64` |
| macOS | arm64 | `nanobanana-darwin-arm64` |
| Windows | amd64 | `nanobanana-windows-amd64.exe` |
| Windows | arm64 | `nanobanana-windows-arm64.exe` |

### Workflow File

Located at `.github/workflows/release.yml`

### Homebrew Tap

Releases automatically update the Homebrew tap at `skorfmann/homebrew-nanobanana`.

```bash
brew tap skorfmann/nanobanana
brew install nanobanana
```

Requires `HOMEBREW_TAP_TOKEN` secret (PAT with `repo` scope).

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
./nanobanana -o output.png "prompt"
```

### Presentation slides (16:9, high-res)
```bash
./nanobanana -aspect 16:9 -size 2K -o slide.png "prompt"
```

### Template-based consistency
```bash
# Generate template first
./nanobanana -aspect 16:9 -size 2K -o template.png "visual style template..."

# Use template as reference for each slide
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_01.png "slide content..."
./nanobanana -i template.png -aspect 16:9 -size 2K -o slide_02.png "slide content..."
```

## Workflow Pattern for Claude Code

When generating multiple related images (like presentation slides):

1. Read the markdown file describing the images/slides
2. Extract prompts for each image
3. If consistency is needed, generate a template first
4. Run nanobanana for each image, passing template with `-i` if applicable
5. Use `-aspect 16:9 -size 2K` for presentation slides
