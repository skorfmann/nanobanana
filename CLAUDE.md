# CLAUDE.md

This file provides context for Claude Code when working on this project.

## ⚠️ IMPORTANT: API Models

**Default model**: `gemini-3.1-flash-image` (Nano Banana 2)

Supported models (selectable via `-model` flag, aliases in parentheses):

| Alias | Model ID | Notes |
|-------|----------|-------|
| `lite` | `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite — fastest/cheapest, 1K only, standard ratios only |
| `flash` | `gemini-3.1-flash-image` | Nano Banana 2 — default; 0.5K–4K, adds extreme ratios 1:4/4:1/1:8/8:1 |
| `pro` | `gemini-3-pro-image` | Nano Banana Pro — highest quality, 1K/2K/4K |
| - | `gemini-2.5-flash-image` | Legacy Nano Banana — 1K only, no `imageSize` param sent |

Unknown model IDs pass through unvalidated so future models work without a rebuild.

Do NOT change the default or the capability tables (`modelCapabilities` in main.go) without checking the current API docs — models have different capabilities, pricing, and availability. The previous default `gemini-3-pro-image-preview` was shut down on 2026-06-25.

**Quirk**: the `generateContent` endpoint expects `"512px"` for the half-resolution size, while the docs/Interactions API call it `"0.5K"`. The CLI accepts `0.5K` and translates it in `generateImage()`.

## Project Overview

Nanobanana is a single-file Go CLI tool that wraps Google's Gemini image generation API. It enables text-to-image generation, image editing, and multi-image composition.

## Architecture

- **Single file**: All code lives in `main.go` (~365 lines)
- **Zero dependencies**: Uses only Go standard library
- **Cross-platform**: Builds for Linux, macOS, and Windows (amd64/arm64)
- **CI/CD**: GitHub Actions releases on every push to main

## Code Structure (main.go)

| Lines | Section |
|-------|---------|
| 17-30 | Version variable, `stringSlice` flag type |
| 33-38 | Constants (endpoint template, default model, timeout) |
| 40-116 | Model registry: aliases, `modelCaps`, per-model ratios/sizes |
| 119-134 | `resolveModel()`, `sortedKeys()` helpers |
| 136-189 | Type definitions (request/response structs) |
| 191-196 | `main()` - entry point |
| 198-287 | `run()` - CLI orchestration (flags, per-model validation) |
| 289-386 | `generateImage()` - API interaction |
| 388-415 | MIME type helpers |
| 417-427 | `loadImage()` - file loading |
| 429-477 | `printUsage()` - help text |

## Key Types

- `Version` - Build version string (set via `-ldflags`)
- `stringSlice` - Custom flag type for repeatable `-i` flags
- `modelCaps` - Per-model capabilities (aspect ratios, sizes, whether `imageSize` is sent)
- `GenerateRequest` / `GenerateResponse` - API payload structures
- `Part` - Content part (text or inline image data)

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

## Environment Variables

- `GEMINI_API_KEY` (required) - Google Gemini API key

## API Details

- **Default model**: `gemini-3.1-flash-image` (see model table above)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent` (built from `apiEndpointTemplate`)
- **Timeout**: 120 seconds
- **Auth**: API key passed via `x-goog-api-key` header

### Pricing (approximate, paid tier, as of July 2026)

| Model | 0.5K | 1K | 2K | 4K |
|-------|------|----|----|----|
| lite | - | ~$0.034 | - | - |
| flash (default) | ~$0.045 | ~$0.067 | ~$0.101 | ~$0.151 |
| pro | - | ~$0.134 | ~$0.134 | ~$0.24 |

See [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) for current rates.

## Common Tasks

### Adding a new model
1. Add an alias to `modelAliases` (line ~40) if it deserves a short name
2. Add a `modelCapabilities` entry (line ~84) with its aspect ratios and sizes
3. Update help text in `printUsage()` and the model tables in README.md/CLAUDE.md

### Adding a new aspect ratio
1. Add to `standardAspectRatios` and/or `extendedAspectRatios` maps (line ~53)
2. Update help text in `printUsage()`

### Adding a new size option
1. Add to `validSizes` map (line ~111) and the relevant `modelCapabilities` entries
2. Update help text in `printUsage()`

### Adding a new image format
1. Add case to `mimeFromExtension()` (line ~401)
2. Add case to `extensionFromMime()` (line ~388)

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
- `resolveModel` - alias resolution and pass-through
- `modelCapabilities` - per-model aspect ratio/size combinations
- Legacy model `imageSize` omission
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

- Missing `GEMINI_API_KEY`
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
