# Branded Presentation Example

Demonstrates using a template image as a style reference to maintain visual consistency across slides.

## Key Technique

Generate a template first, then pass it with `-i` to each slide generation. This ensures consistent:
- Color palette (dark navy + electric cyan)
- Layout structure (accent bar, logo placement)
- Design elements (lines, geometric shapes)
- Overall brand aesthetic

## Files

| File | Description |
|------|-------------|
| `template.jpg` | Base style template (no content) |
| `presentation.md` | Full documentation with prompts |
| `slide_01_title.jpg` | "NEXUS AI" title slide |
| `slide_02_pillars.jpg` | Three pillars: Analyze, Automate, Accelerate |
| `slide_03_contact.jpg` | Contact/closing slide |

## Generated Slides

*Note: Images have been resized and compressed for repository sharing. Original output was 2K resolution.*

### Template (Style Reference)
![Template](template.jpg)

### Slide 1: Title
![Title](slide_01_title.jpg)

### Slide 2: Three Pillars
![Pillars](slide_02_pillars.jpg)

### Slide 3: Contact
![Contact](slide_03_contact.jpg)

## Commands

```bash
# 1. Generate template
./nanobanana -aspect 16:9 -size 2K -o template.jpg \
  "A presentation slide template with dark navy blue background..."

# 2. Generate slides using template as reference
./nanobanana -i template.jpg -aspect 16:9 -size 2K -o slide_01_title.jpg \
  "Using this template style exactly, create a title slide..."

./nanobanana -i template.jpg -aspect 16:9 -size 2K -o slide_02_pillars.jpg \
  "Using this template style exactly, create a slide showing three columns..."

./nanobanana -i template.jpg -aspect 16:9 -size 2K -o slide_03_contact.jpg \
  "Using this template style exactly, create a closing slide..."
```

## Workflow for Claude Code

1. Read `presentation.md` for slide descriptions
2. Generate template first (if not exists)
3. For each slide, run nanobanana with `-i template.jpg` and the slide-specific prompt
