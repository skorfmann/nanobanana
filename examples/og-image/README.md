# Open Graph Image Example

This example shows how to generate a social preview / Open Graph image for a GitHub repository.

## Generated Image

![OG Image](og-image.jpg)

*Note: Image has been resized and compressed for repository sharing. Original output was 2K resolution.*

## Commands Used

### 1. Generate initial image

```bash
./nanobanana -aspect 16:9 -size 2K -o og-image.jpg \
"A sleek developer tool banner image for 'nanobanana' - an AI image generation CLI.
Dark gradient background (deep purple to dark blue).
Center: a stylized glowing banana icon made of geometric shapes and circuit-like lines, emitting soft golden light particles.
Subtle code/terminal aesthetics in the background.
Modern, minimal, techy vibe.
Text: 'nanobanana' in a clean monospace font below the icon, with a subtle tagline 'AI Image Generation CLI'.
Professional GitHub social preview style. No photorealism, use flat design with subtle gradients."
```

### 2. Edit to fix text

```bash
./nanobanana -i og-image.jpg -aspect 16:9 -size 2K -o og-image-fixed.jpg \
"Keep this exact image but change any text that says 'pip install' to 'brew install nanobanana'. Keep everything else identical."
```

## Parameters

- **Aspect ratio:** 16:9 (standard for social previews)
- **Size:** 2K (GitHub recommends 1280x640)
- **Output:** `og-image.jpg`

## Tips for OG Images

- Use 16:9 aspect ratio (GitHub recommends 1280x640)
- Keep text minimal and readable at small sizes
- Use contrasting colors for visibility
- Consider how it looks as a small thumbnail
