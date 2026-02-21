"""Prompt templates for subcommands."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Command:
    """A subcommand with its prompt template and defaults."""

    name: str
    description: str
    default_aspect: str
    default_size: str
    template: str

    def apply(self, user_prompt: str, aspect: str, size: str) -> str:
        """Wrap user prompt in the command template."""
        return self.template.format(
            user_prompt=user_prompt,
            aspect=aspect,
            size=size,
        )


COMMANDS: dict[str, Command] = {
    "dashboard": Command(
        name="dashboard",
        description="KPI/analytics dashboard mockup (enterprise BI aesthetic)",
        default_aspect="16:9",
        default_size="2K",
        template="""\
TASK
Create a KPI/analytics dashboard mockup — a single raster image showing an executive-ready data dashboard.

SOURCE MATERIAL
{user_prompt}

STYLE
- Enterprise BI aesthetic: clean white background, subtle grid, near-black text (#111)
- One accent color for highlights and key metrics
- No gradients, no 3D, no heavy shadows
- Typography readable at projector distance
- Use data visualization best practices: clear axis labels, legends, consistent color coding

LAYOUT
- Top bar: dashboard title, date range, filter pills
- KPI row: 3-5 large metric cards with sparklines and delta indicators
- Main area: 2-3 charts (line, bar, or area) arranged in a balanced grid
- Optional: data table or breakdown panel at bottom

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "moodboard": Command(
        name="moodboard",
        description="Website/app moodboard for early design exploration (collage style)",
        default_aspect="1:1",
        default_size="2K",
        template="""\
TASK
Create a design moodboard — a single raster image showing a curated collage of visual references for website or app design exploration.

SOURCE MATERIAL
{user_prompt}

STYLE
- Collage-style composition with overlapping elements and varied scales
- Mix of UI fragments, typography samples, color swatches, texture patches, and imagery
- Cohesive color palette tying all elements together
- Subtle drop shadows to separate overlapping layers
- Handpicked editorial feel, not random

LAYOUT
- Asymmetric grid with intentional white space
- Dominant hero image or UI fragment as focal point (~40% of area)
- Color palette strip along one edge (5-7 swatches with hex codes)
- Typography samples showing heading and body font pairings
- Scatter of supporting imagery, texture swatches, and UI component fragments

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "explore": Command(
        name="explore",
        description="Render same concept in 4 style variations (4 quadrants)",
        default_aspect="1:1",
        default_size="2K",
        template="""\
TASK
Create a design exploration sheet — a single raster image showing the same concept rendered in 4 distinct visual styles, arranged in a 2x2 grid.

SOURCE MATERIAL
{user_prompt}

STYLE
- Each quadrant renders the concept in a different visual treatment:
  - Top-left: Clean and minimal (flat design, limited palette)
  - Top-right: Rich and detailed (textured, layered, depth)
  - Bottom-left: Bold and graphic (strong contrast, geometric shapes)
  - Bottom-right: Soft and organic (rounded forms, gradients, natural tones)
- Consistent content across all four, only style changes
- Each quadrant labeled with its style name in small caption text

LAYOUT
- 2x2 grid with thin divider lines between quadrants
- Small header at top: concept title
- Each quadrant gets equal space
- Style label in bottom-left corner of each quadrant

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "wireframe": Command(
        name="wireframe",
        description="UI wireframe or screen layout",
        default_aspect="16:9",
        default_size="2K",
        template="""\
TASK
Create a UI wireframe — a single raster image showing a screen layout with clear component hierarchy and spatial arrangement.

SOURCE MATERIAL
{user_prompt}

STYLE
- Mid-fidelity wireframe: grayscale with one accent color for interactive elements
- Placeholder text shown as readable labels (not lorem ipsum)
- Clean lines, consistent spacing, visible grid alignment
- Component boundaries clearly defined with subtle borders
- Icons as simple recognizable outlines

LAYOUT
- Standard screen structure: navigation (top or side), content area, optional sidebar
- Component hierarchy clearly communicated through size and position
- Consistent padding and margins throughout
- Annotations or labels for key interactive elements where helpful

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "slide": Command(
        name="slide",
        description="Presentation slide (20+ subtemplates for board decks)",
        default_aspect="16:9",
        default_size="2K",
        template="""\
TASK
Create a presentation slide — a single raster image suitable for a professional slide deck.

SOURCE MATERIAL
{user_prompt}

STYLE
- Executive-clean: white or dark background, minimal decoration
- Strong typographic hierarchy: large headline, supporting body text
- One accent color for emphasis and visual elements
- No clip art or stock photo aesthetic
- Data visualizations (if any) should be simple and readable at distance

LAYOUT
- Clear focal point — headline or key visual dominates
- Supporting text or data arranged with generous white space
- Visual elements (charts, diagrams, icons) balanced with text
- Bottom strip for source attribution or slide number if relevant

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "social": Command(
        name="social",
        description="Social media post image",
        default_aspect="1:1",
        default_size="2K",
        template="""\
TASK
Create a social media post image — a single raster image optimized for engagement on social platforms.

SOURCE MATERIAL
{user_prompt}

STYLE
- Bold, scroll-stopping visual with high contrast
- Clean typography with large readable text
- Vibrant but cohesive color palette
- Modern graphic design aesthetic
- Minimal text — the image should communicate the message visually

LAYOUT
- Strong central visual or focal point
- Text overlay (if any) in high-contrast area with room to breathe
- Safe zones maintained for platform UI elements (profile pic overlay, like/comment buttons)
- Brand element (logo or watermark) subtle in corner if relevant

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "icon": Command(
        name="icon",
        description="App icon",
        default_aspect="1:1",
        default_size="1K",
        template="""\
TASK
Create an app icon — a single raster image showing a distinctive, recognizable icon suitable for app stores and home screens.

SOURCE MATERIAL
{user_prompt}

STYLE
- Simple, bold, instantly recognizable at small sizes
- Limited color palette (2-4 colors max)
- No text or at most a single letter/symbol
- Subtle depth through gradients or shadows (iOS/Android style)
- Clean geometric forms or a single distinctive glyph

LAYOUT
- Single centered symbol or glyph filling ~60-70% of the canvas
- Solid or gradient background
- Rounded-corner square format (standard app icon shape)
- No fine details that disappear at 64x64px

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "architecture": Command(
        name="architecture",
        description="System/cloud architecture diagram",
        default_aspect="16:9",
        default_size="2K",
        template="""\
TASK
Create a system architecture diagram — a single raster image showing components, services, and their connections in a technical system.

SOURCE MATERIAL
{user_prompt}

STYLE
- Technical diagram aesthetic: clean lines, consistent icon style
- Cloud/system icons in a flat or outlined style (AWS/GCP/Azure-inspired where relevant)
- Color-coded groups for different tiers or domains
- Clear directional arrows showing data flow or dependencies
- Labels on all components and connections

LAYOUT
- Left-to-right or top-to-bottom flow depending on complexity
- Components grouped by tier (clients, API layer, services, data stores)
- Groups enclosed in labeled dashed-line boundaries
- Legend in corner explaining color coding and arrow types
- Title at top with system name

OUTPUT RULES
- Single raster image
- {aspect} aspect ratio
- {size} resolution""",
    ),
    "generate": Command(
        name="generate",
        description="Free-form image generation (default behavior)",
        default_aspect="1:1",
        default_size="1K",
        template="{user_prompt}",
    ),
}


def get_command(name: str) -> Command | None:
    """Look up a command by name. Returns None if not found."""
    return COMMANDS.get(name)


def format_help_overview() -> str:
    """Format help text listing all commands with descriptions."""
    lines = [
        "nanobanana - Generate images using Gemini or OpenRouter API",
        "",
        "Usage:",
        '  nanobanana <command> [options] "prompt"',
        '  nanobanana [options] "prompt"            (defaults to generate)',
        "",
        "Commands:",
    ]

    # Calculate padding for alignment
    max_name = max(len(name) for name in COMMANDS)
    for name, cmd in COMMANDS.items():
        lines.append(f"  {name:<{max_name}}  {cmd.description}")

    lines.extend([
        "",
        f"  {'help':<{max_name}}  Show help for all commands or a specific command",
        f"  {'version':<{max_name}}  Show version",
        "",
        "Options:",
        "  -i <file>       Input image file (repeatable)",
        "  -o <file>       Output filename",
        "  -aspect <ratio> Aspect ratio (overrides command default)",
        "  -size <size>    Image size (overrides command default)",
        "  -model <model>  OpenRouter model",
        "  -h              Show this help",
        "  -version        Show version",
        "",
        'Run "nanobanana help <command>" for details on a specific command.',
        'Run "nanobanana help slide templates" to list board deck subtemplates.',
    ])
    return "\n".join(lines) + "\n"


def format_command_help(cmd: Command) -> str:
    """Format detailed help for a single command."""
    lines = [
        f"nanobanana {cmd.name} - {cmd.description}",
        "",
        "Usage:",
        f'  nanobanana {cmd.name} [options] "prompt"',
        "",
        f"Defaults:",
        f"  Aspect ratio: {cmd.default_aspect}",
        f"  Size:         {cmd.default_size}",
        "",
        "Template:",
    ]
    # Show template with indentation
    for line in cmd.template.split("\n"):
        lines.append(f"  {line}")

    lines.extend([
        "",
        "Example:",
    ])
    match cmd.name:
        case "dashboard":
            lines.append(f'  nanobanana dashboard "SaaS metrics dashboard with MRR, churn rate, and user growth"')
        case "moodboard":
            lines.append(f'  nanobanana moodboard "fintech app targeting young professionals, trustworthy yet modern"')
        case "explore":
            lines.append(f'  nanobanana explore "landing page hero for a meditation app"')
        case "wireframe":
            lines.append(f'  nanobanana wireframe "settings page with account, notifications, and billing sections"')
        case "slide":
            lines.append(f'  nanobanana slide "Q4 revenue highlights: 40% YoY growth, 3 new enterprise clients"')
            lines.append(f'  nanobanana slide funnel "our SaaS product funnel"')
            lines.append(f'  nanobanana slide arr "Q4 2025 ARR bridge"')
            lines.append("")
            lines.append("This command has 20 board deck subtemplates. Run:")
            lines.append('  nanobanana help slide templates')
        case "social":
            lines.append(f'  nanobanana social "product launch announcement for a new AI writing tool"')
        case "icon":
            lines.append(f'  nanobanana icon "podcast app with a microphone and sound waves"')
        case "architecture":
            lines.append(f'  nanobanana architecture "microservices with API gateway, 3 services, Redis cache, and PostgreSQL"')
        case "generate":
            lines.append(f'  nanobanana generate "a cute cat sitting on a windowsill"')

    return "\n".join(lines) + "\n"
