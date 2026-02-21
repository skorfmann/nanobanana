# Guided Discovery Workflow

When a user's request is vague, complex, data-driven, or needs multiple decisions, use guided discovery before generating.

## Step 1: Classify Intent

| Signal words | Intent | Approach |
|-------------|--------|----------|
| screens, buttons, dashboard, app, navigation, forms | UI/UX | `ui_builder` discovery |
| flow, process, architecture, nodes, boxes-and-arrows, system diagram | Diagram | `diagram_spec` discovery |
| hero shot, product photo, brand imagery, campaign, advertisement | Marketing image | `marketing_image` discovery |
| KPIs, funnel, revenue, OKRs, board meeting, cohort, pipeline, churn | Business slide | Board Deck discovery |

If ambiguous, ask 1-2 short questions to disambiguate, then commit to one type.

## Step 2: Ask Discovery Questions

Ask one group at a time. WHY: Dumping all questions at once overwhelms the user and yields shallow answers. Skip questions the user has already answered.

### UI/UX Discovery

1. **Platform & fidelity**: Web, mobile, or desktop? Wireframe, mid-fi, or hi-fi?
2. **Screens**: How many screens? What role does each serve? (e.g., dashboard, settings, onboarding)
3. **Layout zones**: What are the major areas? (top nav, sidebar, content panels, footer)
4. **Key components**: What goes in each zone? (charts, tables, cards, forms, KPI grids)
5. **Theme & brand**: Light or dark? Any brand colors, font preferences, or existing style guide?

### Diagram Discovery

1. **Diagram type**: Flowchart, architecture, swimlane, sequence, mind map, or something else?
2. **Key nodes**: What are the main entities/steps? (aim for 5-15)
3. **Relationships**: How do nodes connect? Any labels on edges? (e.g., "yes/no", "async", "HTTP")
4. **Grouping**: Any lanes, subsystems, or clusters to visually group nodes?
5. **Direction**: Left-to-right or top-to-bottom?

### Marketing Image Discovery

1. **Subject**: What's the main subject? (product type, name, variant, physical properties)
2. **Props**: What surrounds the subject? (foreground items, midground, background elements)
3. **Environment**: What surface and backdrop? What mood/atmosphere?
4. **Camera & framing**: Angle (front, 3/4, top-down)? Framing (close-up, medium, wide)?
5. **Lighting**: Key light direction and intensity? Color temperature (cool, neutral, warm)?
6. **Brand constraints**: Any logos, colors, or assets that must appear or must not change?

### Business Slide (Board Deck) Discovery

Board Deck artifacts are exec-ready 16:9 slides for board meetings, business reviews, and strategic planning.

**First, identify which artifact the user needs:**

| Context | Recommended artifacts |
|---------|----------------------|
| Board meeting | Executive Summary, ARR Bridge, Market Sizing |
| Weekly business review | Funnel Diagnostic, Pipeline Coverage, Scorecard |
| Product planning | Opportunity Solution Tree, RICE Matrix, Scenario Planning |
| Investor pitch | TAM/SAM/SOM, Cohort Retention, Pricing & Packaging |
| Strategic planning | Scenario Planning, Investment Portfolio, OKR Cascade |
| Operational review | RACI/Operating Model, Capacity Planning, Release Readiness |

**Then gather data using discovery groups:**

- **GROUP 1 -- CONTEXT**: What is this for? Who is the audience? As-of date? Goal?
- **GROUP 2 -- STRUCTURE**: The core elements specific to the artifact (funnel stages, OKR hierarchy, cohort rows, etc.)
- **GROUP 3 -- DATA**: The numbers, metrics, and values to display
- **GROUP 4 -- ANALYSIS**: Diagnosis, hypotheses, risks, or insights to highlight
- **GROUP 5 -- ACTIONS**: Experiments, decisions needed, next steps
- **GROUP 6 -- NOTES**: Assumptions, caveats, decisions needed from leadership

## Step 3: Construct the Prompt

Build a structured prompt from collected answers:

- **For UI/UX, Diagram, Marketing**: Optionally use a JSON spec (see `references/json-schemas.md`). JSON gives Gemini precise control over every element.
- **For Board Deck**: Construct a detailed prose prompt including:
  - Role preamble: "You are a senior GTM + product ops designer creating exec-ready artifacts."
  - TASK description
  - All gathered data inline
  - Layout spec with zones
  - Calculations to perform
  - Design rules (exec-clean, projector-ready)
  - Output rules (single raster image, 16:9, no SVG/code/markdown)

## Step 4: Execute

| Intent | Subcommand | Typical flags |
|--------|-----------|---------------|
| UI/UX | `dashboard`, `wireframe`, or `generate` | `-aspect 16:9 -size 2K` |
| Diagram | `architecture` or `generate` | `-aspect 16:9 -size 2K` |
| Marketing image | `generate` or `social` | varies by use case |
| Business slide | `slide` or `generate` | `-aspect 16:9 -size 2K` |

For complex prompts, write to a temp file. WHY: Prompts with quotes and newlines break shell escaping when passed inline.

```bash
nanobanana slide -aspect 16:9 -size 2K -o artifact.jpg "$(cat /tmp/prompt.txt)"
```
