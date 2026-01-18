---
name: Nanobanana Image Generation
description: Generate and edit images using nanobanana CLI with Google Gemini API. Use for creating images, slides, banners, and visual content from text prompts.
dependencies: nanobanana (brew tap skorfmann/nanobanana && brew install nanobanana)
---

# Nanobanana Image Generation Skill

Generate images using Google's Gemini API via the nanobanana CLI tool.

## Prerequisites

1. Install nanobanana:
   ```bash
   brew tap skorfmann/nanobanana
   brew install nanobanana
   ```

2. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
   Get a key at: https://aistudio.google.com/apikey

## When to Use This Skill

Use this skill when the user asks to:
- Generate images from text descriptions
- Create presentation slides
- Design banners, thumbnails, or social media images
- Edit or transform existing images
- Combine multiple images
- Create consistent branded visuals using templates

## Basic Commands

### Text-to-Image Generation
```bash
nanobanana "your prompt here"
nanobanana -o output.jpg "your prompt here"
nanobanana -aspect 16:9 -size 2K -o slide.jpg "your prompt here"
```

### Image Editing (with input image)
```bash
nanobanana -i input.jpg "transform into watercolor style"
nanobanana -i photo.jpg "add sunglasses to the person"
```

### Multi-Image Composition
```bash
nanobanana -i background.jpg -i subject.jpg "place the subject in the scene"
nanobanana -i template.jpg -i content.jpg "apply the template style"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-i <file>` | Input image (repeatable) | none |
| `-o <file>` | Output filename | auto-generated |
| `-aspect <ratio>` | Aspect ratio | `1:1` |
| `-size <size>` | Image size (1K, 2K, 4K) | `1K` |
| `-version` | Show version | - |

## Supported Aspect Ratios

`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Workflow Patterns

### Single Image
```bash
nanobanana -o hero.jpg "a futuristic cityscape at sunset, cyberpunk style"
```

### Presentation Slides (Consistent Style)
```bash
# 1. Generate a template first
nanobanana -aspect 16:9 -size 2K -o template.jpg \
  "presentation slide template with dark blue gradient, modern minimal style"

# 2. Generate each slide using template as style reference
nanobanana -i template.jpg -aspect 16:9 -size 2K -o slide_01.jpg \
  "using this template style, create a title slide for 'Project Alpha'"

nanobanana -i template.jpg -aspect 16:9 -size 2K -o slide_02.jpg \
  "using this template style, create a slide showing three key features"
```

### Image Editing Workflow
```bash
# Generate initial image
nanobanana -o draft.jpg "a logo for a tech startup"

# Refine with edits
nanobanana -i draft.jpg -o final.jpg "make the colors more vibrant and add a subtle glow effect"
```

## Prompting Tips

1. **Be specific**: Include style, mood, colors, composition details
2. **For edits**: Reference "this image" or "keep everything else identical"
3. **For consistency**: Use a template image with `-i` flag
4. **For slides**: Always use `-aspect 16:9 -size 2K`

## Pricing

- 1K-2K images: ~$0.13 per image
- 4K images: ~$0.24 per image

## Example Prompts

### Marketing Banner
```bash
nanobanana -aspect 16:9 -size 2K -o banner.jpg \
  "professional marketing banner for a SaaS product launch,
   dark gradient background, glowing tech elements,
   modern minimal design, no text"
```

### App Icon
```bash
nanobanana -aspect 1:1 -size 1K -o icon.jpg \
  "app icon for a meditation app,
   soft purple gradient, lotus flower symbol,
   simple flat design, rounded corners style"
```

### Social Media Post
```bash
nanobanana -aspect 1:1 -size 2K -o social.jpg \
  "instagram post announcing a new feature,
   bright cheerful colors, confetti elements,
   celebratory mood, tech startup aesthetic"
```

## Troubleshooting

- **No GEMINI_API_KEY**: Set the environment variable
- **Wrong file extension**: nanobanana auto-corrects to match actual format (usually .jpg)
- **Image too large**: Use smaller `-size` option (1K instead of 4K)

## More Information

- Repository: https://github.com/skorfmann/nanobanana
- Examples: https://github.com/skorfmann/nanobanana/tree/main/examples
