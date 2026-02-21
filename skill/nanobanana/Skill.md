---
name: nanobanana
description: >
  Generate images via Gemini/OpenRouter API using nanobanana CLI.
  Use when user wants image generation, slides, dashboards, wireframes, moodboards, icons, or architecture diagrams.
  Do NOT use for image analysis, OCR, classification, video, or SVG output.
---

# Nanobanana Image Generation

Generate images using nanobanana CLI with subcommands that wrap prompts in structured templates.

## Prerequisites

```bash
uv tool install nanobanana
```

API key via env var (`GEMINI_API_KEY` or `OPENROUTER_API_KEY`) or config file at `~/.config/nanobanana/config.json` with `key_command` for dynamic retrieval (e.g., 1Password).

## When to Use

- Generate images from text descriptions
- Create slides, dashboards, wireframes, moodboards, icons, architecture diagrams
- Edit or transform existing images (`-i` flag)
- Explore design variations for a concept

## Do NOT

- Use for image analysis, OCR, or classification (nanobanana generates, not analyzes)
- Generate SVG, HTML, or code output (output is always raster PNG/JPG)
- Run more than 3 parallel generations (API rate limits)
- Use for video or animation

## Subcommands

| Command | Description | Default Aspect | Default Size |
|---------|-------------|----------------|--------------|
| `dashboard` | KPI/analytics dashboard mockup | 16:9 | 2K |
| `moodboard` | Design moodboard (collage) | 1:1 | 2K |
| `explore` | 4 style variations in 2x2 grid | 1:1 | 2K |
| `wireframe` | UI wireframe / screen layout | 16:9 | 2K |
| `slide` | Presentation slide | 16:9 | 2K |
| `social` | Social media post image | 1:1 | 2K |
| `icon` | App icon | 1:1 | 1K |
| `architecture` | System/cloud architecture diagram | 16:9 | 2K |
| `generate` | Free-form (default if no command given) | 1:1 | 1K |

No command = free-form prompt (backwards compatible).

## Usage

```bash
# Subcommands (auto-set aspect + size)
nanobanana dashboard "SaaS metrics with MRR, churn rate, user growth"
nanobanana slide "Q4 revenue: 40% YoY growth, 3 new enterprise clients"
nanobanana icon "podcast app with microphone and sound waves"
nanobanana architecture "microservices with API gateway, Redis, PostgreSQL"
nanobanana explore "landing page hero for a meditation app"

# Override defaults
nanobanana dashboard -size 4K "quarterly revenue breakdown"
nanobanana social -aspect 9:16 "instagram story for product launch"

# Free-form
nanobanana "a cute cat sitting on a windowsill"
nanobanana -o output.jpg "a sunset over mountains"

# Image editing
nanobanana -i input.jpg "transform into watercolor style"

# Multi-image composition
nanobanana -i background.jpg -i subject.jpg "place the subject in the scene"

# Consistent series with template
nanobanana slide -o template.jpg "dark blue gradient, modern minimal style"
nanobanana -i template.jpg slide -o slide_01.jpg "title slide for Project Alpha"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable) | none |
| `-o <file>` | Output filename | auto-generated |
| `-aspect <ratio>` | Aspect ratio (overrides command default) | per command |
| `-size <size>` | 1K, 2K, or 4K | per command |
| `-model <model>` | OpenRouter model | config default |

Aspect ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Direct vs Guided Mode

**Direct** -- User gives a specific prompt. Pick the right subcommand and run it.

**Guided discovery** -- User request is vague or data-driven. Use the discovery workflow:
1. Classify intent (UI/UX, Diagram, Marketing, Business slide)
2. Ask targeted discovery questions (one group at a time)
3. Construct structured prompt from answers
4. Execute with appropriate subcommand

See `references/guided-discovery.md` for the full workflow with question groups per intent type.

For structured JSON specs (precise control over layout, components, lighting): see `references/json-schemas.md`.

## Expected Output

After running nanobanana, report to the user:
- The command you executed (with flags)
- The output file path
- Any warnings (e.g., file extension auto-corrected)
- Offer to iterate if the result needs adjustments

## Pricing

- 1K-2K images: ~$0.13 per image
- 4K images: ~$0.24 per image

## Troubleshooting

- **No API key**: Set env var or use `key_command` in config
- **Wrong extension**: nanobanana auto-corrects to match API response format
- **Command help**: `nanobanana help` or `nanobanana help <command>`
