"""Slide subtemplates for board deck artifacts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SlideTemplate:
    """A named slide subtemplate with its prompt."""

    name: str
    title: str
    template: str


SLIDE_TEMPLATES: dict[str, SlideTemplate] = {
    "funnel": SlideTemplate(
        name="funnel",
        title="Funnel Diagnostic + Hypotheses Dashboard",
        template="""\
TASK
Create a "Funnel Diagnostic + Hypotheses" dashboard — a single 16:9 image for a Weekly Business Review that shows funnel performance, trend lines, leak diagnosis, and prioritized experiments.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC (3 ZONES)

A) TOP HEADER (full width)
- Left: dashboard title
- Right: as-of date
- Subtitle: goal statement

B) MAIN BODY (two columns)

LEFT COLUMN (~65% width): FUNNEL + TRENDS
1) FUNNEL VISUALIZATION (top-left)
- Draw a 5-8 stage funnel with wide-to-narrow blocks
- Left-aligned stage labels, right-aligned counts
- Each stage shows: stage name, count (formatted with k/M), conversion % from prior stage, WoW delta (in pp, with +/- and color coding)
- Highlight the stage with LOWEST conversion % as "Biggest Leak" with a subtle red callout

2) MICRO-TRENDS (below funnel)
- 4 small sparkline charts (last 6-8 weeks)
- Minimal axes, clean lines
- Latest point marked with dot and value label

RIGHT COLUMN (~35% width): DIAGNOSIS PANEL
3) LEAKS + HYPOTHESES TABLE (top-right)
- Title: "Top Leaks (Ranked by Severity)"
- Columns: Leak | Severity | Evidence | Hypothesis | Owner | This Week Action
- Severity Score = (Lost users at leak) x (strategic weight)
- Sort by Severity descending
- Highlight highest severity row in subtle red

4) EXPERIMENTS BACKLOG TABLE (below)
- Title: "Experiments (Next 2 Weeks)"
- Columns: Experiment | Type | Primary Metric | Expected Lift | Effort | Confidence | Priority
- Priority = (Expected Lift x Confidence) / Effort Weight (S=1, M=2, L=3)
- Sort by Priority descending

C) FOOTER (full width)
- Left: "Assumptions / Notes" (2 bullets)
- Right: "Decision Needed" (1 bullet)

DESIGN RULES
- Executive-clean: white background, subtle borders (#DDD), text near-black (#111)
- Use ONE accent color for highlights
- Red only for "Biggest Leak" callout and highest severity row
- No gradients, no 3D, no heavy shadows
- Typography readable at projector distance""",
    ),
    "ost": SlideTemplate(
        name="ost",
        title="Opportunity Solution Tree (Teresa Torres)",
        template="""\
TASK
Create an "Opportunity Solution Tree" — a single 16:9 image showing the left-to-right flow from Outcome to Opportunities to Solutions to Experiments, with a summary panel for prioritization.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

GLOBAL HEADER
- Top-left: "Opportunity Solution Tree" with product area
- Top-right: as-of date
- Subtitle: "Outcome -> Opportunities -> Solutions -> Experiments"

MAIN DIAGRAM (left-to-right tree, ~75% of width)

Level 1 — OUTCOME (far left)
- Largest box, subtle accent header band
- Contains: Outcome statement, North Star metric + target, Time horizon

Level 2 — OPPORTUNITIES (next column)
- Medium boxes, one per opportunity
- Contains: Title, Evidence tag (colored chip), Evidence note, Reach estimate
- Connected to Outcome with orthogonal lines

Level 3 — SOLUTIONS (next column)
- Medium-small boxes, branching from parent opportunity
- Contains: Solution name, Impact chip (1-5), Confidence chip (1-5), Owner
- Connected to parent Opportunity

Level 4 — EXPERIMENTS (far right)
- Smallest boxes, branching from parent solution
- Contains: Experiment name, Type chip (A/B/Prototype/etc.), Success metric
- Connected to parent Solution

RIGHT-SIDE SUMMARY PANEL (~25% of width)
- Title: "This Cycle Focus"
- "Top 3 Solutions" (by Impact x Confidence score, with owner)
- "Top 3 Experiments" (by priority, then by parent solution score)
- "Key Risks" (2 bullets)
- "Decision Needed" (1 bullet)

LEGEND (bottom-left)
- Evidence tags: VoC / Funnel / Support / Sales (colored chips)
- Impact: 1-5 scale
- Confidence: 1-5 scale

DESIGN RULES
- White background, subtle borders (#DDD), near-black text (#111)
- Orthogonal connectors (right angles), thin lines, minimize crossings
- Use small colored chips (not full box fills) for tags and scores
- Max ~32 characters per line; truncate with ellipsis
- No overlapping boxes or connectors
- No gradients, no 3D""",
    ),
    "arr": SlideTemplate(
        name="arr",
        title="ARR Revenue Bridge (Waterfall)",
        template="""\
TASK
Create an "ARR Revenue Bridge" — a single 16:9 waterfall chart showing how ARR changed from period start to period end.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "ARR Bridge" with period
- Right: as-of date

WATERFALL CHART (main area)
- Steps in order:
  1) Starting ARR (dark gray bar, grounded)
  2) + New ARR (green bar, floating from Starting)
  3) + Expansion ARR (green bar, floating from prior)
  4) - Contraction ARR (red bar, floating downward)
  5) - Churn ARR (red bar, floating downward)
  6) Ending ARR (dark gray bar, grounded)
- True waterfall with cumulative bridging (each bar starts where prior ends)
- Thin connector lines between bars
- Labels on EVERY bar:
  - Deltas: "+$380k", "-$95k"
  - Totals: "$4.20M", "$4.53M"

OPTIONAL: SEGMENT BREAKDOWN
- If provided, show small stacked sub-bars within New/Expansion/Churn

NOTES BOX (bottom-left)
- 1-2 lines of commentary

COMPARISON (bottom-right, optional)
- YoY or QoQ delta
- Target vs. Actual

DESIGN RULES
- Executive-clean: white background, high contrast, no gradients, no 3D
- Colors:
  - Positive deltas: green (#2EA043)
  - Negative deltas: red (#D64545)
  - Totals: dark gray (#333)
- Currency with $ and k/M abbreviations
- Labels readable at projector distance
- No heavy gridlines""",
    ),
    "retention": SlideTemplate(
        name="retention",
        title="Cohort Retention Heatmap",
        template="""\
TASK
Create a "Cohort Retention Heatmap" — a single 16:9 image showing user or revenue retention by signup cohort over time, with trend analysis and benchmarks.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Cohort Retention" with product/metric type
- Right: as-of date
- Subtitle: retention definition

MAIN HEATMAP (~70% of space)
- Rows = Cohorts (newest at top or bottom, be consistent)
- Columns = Periods (0, 1, 2, 3, ... N)
- Each cell shows retention % with color intensity:
  - High retention (>target): green shades
  - Medium retention (near target): yellow shades
  - Low retention (<threshold): red shades
- Cells for future periods (not yet reached) shown as gray/hatched

COHORT SIZE COLUMN
- Add a column showing starting cohort size (users or $) for context

SUMMARY METRICS (right panel, ~30%)
- "Latest Cohort Performance" — key retention points
- "Trend" — arrow showing direction
- "Best Performing Cohort" — which and why
- "Worst Performing Cohort" — which and why
- "Benchmark Comparison" — how you compare

RETENTION CURVE (optional, below heatmap)
- Line chart overlay showing average retention curve
- With benchmark curve if provided

FOOTER
- Legend for color scale
- "Target" indicators
- Key assumptions or notes

DESIGN RULES
- Clean heatmap with clear cell boundaries
- Color scale: green (high) -> yellow (medium) -> red (low)
- Percentages formatted as whole numbers (e.g., "68%")
- Cohort sizes formatted with k/M abbreviations
- White background, subtle gridlines
- No gradients within cells, no 3D""",
    ),
    "pipeline": SlideTemplate(
        name="pipeline",
        title="Pipeline Coverage & Velocity Dashboard",
        template="""\
TASK
Create a "Pipeline Coverage & Velocity Dashboard" — a single 16:9 image showing pipeline health, stage conversion, velocity metrics, and forecast confidence.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Pipeline & Velocity" with team/segment
- Right: period and as-of date
- Subtitle: "Quota: $[X] | Coverage: [X]x | Gap: $[X]"

MAIN BODY (3 zones)

ZONE 1 — PIPELINE FUNNEL (left, ~40%)
- Horizontal or vertical funnel showing stages
- Each stage shows: stage name, deal count, pipeline value, conversion % to next stage, avg days in stage
- Highlight the stage with lowest conversion as "Bottleneck"

ZONE 2 — COVERAGE & FORECAST (top-right, ~30%)
- Coverage gauge or bar:
  - Unweighted pipeline vs. quota
  - Weighted pipeline vs. quota
  - Required coverage line
- Forecast bands: Commit, Best Case, Pipeline (each as % of quota)

ZONE 3 — VELOCITY METRICS (bottom-right, ~30%)
- 4 metric cards:
  - Average Deal Size (with delta)
  - Sales Cycle (days, with delta)
  - Win Rate (%, with delta)
  - Pipeline Created This Period (with delta)
- Green/red arrows for positive/negative trends

TOP DEALS TABLE (bottom, full width)
- Columns: Deal Name | Value | Stage | Expected Close | Risk Level | Owner
- Risk Level as colored badge (Low/Med/High)
- Sort by value descending

FOOTER
- "Key Risks" (1-2 bullets)
- "Action Needed" (1 bullet)

DESIGN RULES
- Executive-clean: white background, subtle borders
- Coverage: green if >= required ratio, yellow if close, red if below
- Velocity trends: green for improvement, red for decline
- Currency formatted with $ and k/M
- No gradients, no 3D""",
    ),
    "okr": SlideTemplate(
        name="okr",
        title="OKR Cascade Diagram",
        template="""\
TASK
Create an "OKR Cascade Diagram" — a single 16:9 image showing how company-level OKRs flow down to team-level OKRs with clear alignment and progress tracking.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "OKR Cascade" with company/org
- Right: period and as-of date
- Subtitle: "Company -> Team Alignment"

MAIN DIAGRAM (top-down cascade)

LEVEL 1 — COMPANY OKRs (top row)
- Each Objective as a card:
  - Objective statement (bold)
  - Owner
  - Key Results listed with: KR text (abbreviated if needed), progress bar (% filled), status indicator (green/yellow/red dot)

LEVEL 2 — TEAM OKRs (rows below, grouped by contributing company OKR)
- Each Team as a card:
  - Team name (header)
  - Team Objective
  - Key Results with progress bars and status
- Connector lines from Team OKRs to parent Company OKRs
- If a Team contributes to multiple Company OKRs, show multiple connectors

ALIGNMENT INDICATORS
- Clear visual connection (lines, color coding) showing which teams contribute to which company OKRs
- Highlight any unaligned or orphaned OKRs

SUMMARY PANEL (right side or bottom)
- "Overall Progress" — aggregate % across all OKRs
- "On Track" count, "At Risk" count, "Off Track" count
- "Key Wins" (1-2 bullets)
- "Key Risks" (1-2 bullets)

FOOTER
- Legend for status colors
- "Mid-Cycle Adjustments" note (if any)

DESIGN RULES
- Clean hierarchical layout with clear parent-child relationships
- Progress bars: filled portion in accent color, remainder in light gray
- Status colors: Green (#2EA043), Yellow (#E3B341), Red (#D64545)
- White background, subtle card borders
- Text wrapping at ~40 chars; truncate with ellipsis if needed
- Connectors should not overlap text; use curved or orthogonal lines
- No gradients, no 3D""",
    ),
    "exec": SlideTemplate(
        name="exec",
        title="Board Meeting Executive Summary",
        template="""\
TASK
Create a "Board Meeting Executive Summary" — a single 16:9 image that captures the essential state of the business: key metrics, strategic progress, risks, and asks. This is the "one slide that rules them all."

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER (full width)
- Left: company name + "Board Update"
- Center: meeting date/period
- Right: "Presented by [Name]"

ZONE 1 — KEY METRICS (top band, full width)
- 6-8 metric cards in a row
- Each card: metric name, current value (large), vs. target (smaller), delta indicator (arrow + %), status dot (green/yellow/red)

ZONE 2 — STRATEGIC PRIORITIES (left column, ~50%)
- Title: "Strategic Priorities"
- 3-4 rows, each showing: priority name, status badge, progress note

ZONE 3 — WINS & CHALLENGES (right column, ~50%)
- Split into two sections:
  - "Wins" (2-3 bullets with checkmarks)
  - "Challenges" (2-3 bullets with warning icons)

ZONE 4 — RISKS TABLE (middle band, full width)
- Compact table:
  - Columns: Risk | Likelihood | Impact | Mitigation Status
  - 2-3 rows, color-coded by severity

ZONE 5 — ASKS & OUTLOOK (bottom band, full width)
- Left: "Board Asks" (1-2 bullets, prominent)
- Right: "Outlook" (1-2 sentences + confidence badge)

DESIGN RULES
- Ultra-clean, maximum information density while remaining scannable
- Status colors: Green (#2EA043), Yellow (#E3B341), Red (#D64545)
- Hierarchy: Asks should be visually prominent (this is what matters to the board)
- White background, subtle section dividers
- Typography: clear hierarchy, readable at projector distance
- No gradients, no 3D, no decorative elements""",
    ),
    "scenario": SlideTemplate(
        name="scenario",
        title="Scenario Planning Matrix",
        template="""\
TASK
Create a "Scenario Planning Matrix" — a single 16:9 image showing 3-4 future scenarios with key drivers, implications, strategic responses, and trigger indicators.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Scenario Planning" with planning horizon
- Right: as-of date
- Subtitle: strategic question being addressed

MAIN MATRIX (center, ~60% of width)
- 2x2 matrix using 2 uncertainty dimensions
- Axes labeled with uncertainty dimensions
- Each quadrant contains:
  - Scenario name (bold)
  - Probability badge (e.g., "25%")
  - Key characteristics (2-3 bullets, small text)
- Base case scenario highlighted with accent border

SCENARIO DETAIL CARDS (right panel, ~40%)
For each scenario (stacked):
- Scenario name
- "Implications" section (2-3 bullets)
- "Strategic Response" section (1-2 bullets)
- "Trigger Indicators" section (1-2 bullets)

BOTTOM PANEL (full width)
- "No-Regret Moves" (actions robust across scenarios)
- "Options to Preserve" (flexibility plays)
- "Key Monitoring Metrics" (what to watch)

DESIGN RULES
- Clean 2x2 matrix with clear quadrant separation
- Probability badges: larger % = more prominent
- Base case: accent border or subtle highlight
- Color-code scenarios subtly (avoid garish colors)
- White background, subtle gridlines
- Text wrapping; truncate long items with ellipsis
- No gradients, no 3D""",
    ),
    "churn": SlideTemplate(
        name="churn",
        title="Churn Analysis Diagnostic",
        template="""\
TASK
Create a "Churn Analysis Diagnostic" — a single 16:9 image showing churn breakdown by reason, segment, cohort, and leading indicators, with actionable insights.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Churn Diagnostic" with product name
- Right: period and as-of date
- Subtitle: "Total Churn: [X] accounts ($[Y]) | Churn Rate: [Z]%"

ZONE 1 — CHURN BY REASON (left, ~40%)
- Horizontal bar chart or treemap
- Ranked by $ impact or count
- Each bar shows: reason, count, $ value, trend arrow
- Highlight top 2-3 reasons

ZONE 2 — CHURN BY SEGMENT (top-right, ~30%)
- Small multiples or heatmap
- Rows: segments (size, tenure, etc.)
- Show churn rate per segment
- Color intensity = churn severity
- Highlight worst-performing segments

ZONE 3 — LEADING INDICATORS (middle-right, ~30%)
- Table or card format:
  - Indicator name
  - Detection window (e.g., "30 days before")
  - Correlation strength (High/Med/Low)
  - Current alert count

ZONE 4 — TREND & COHORT (bottom-left, ~50%)
- Line chart: churn rate over last 6-12 months
- Cohort comparison: bars showing churn rate by cohort vintage

ZONE 5 — INSIGHTS & ACTIONS (bottom-right, ~50%)
- "Key Insights" (3 bullets)
- "Planned Interventions" (2-3 bullets with owner)
- "Expected Impact" (1 line)

DESIGN RULES
- Executive-clean: white background, subtle borders
- Churn = red color palette (but not garish)
- Improvements = green accents
- Clear hierarchy: headline metrics most prominent
- Numbers formatted appropriately (%, $, counts)
- No gradients, no 3D""",
    ),
    "rice": SlideTemplate(
        name="rice",
        title="RICE/ICE Prioritization Matrix",
        template="""\
TASK
Create a "Prioritization Matrix" — a single 16:9 image showing features or initiatives scored and ranked using RICE (Reach, Impact, Confidence, Effort) or ICE (Impact, Confidence, Ease) methodology.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "[RICE/ICE] Prioritization" with product/team
- Right: period and as-of date
- Subtitle: methodology and scoring definitions summary

MAIN TABLE (center, ~70% of space)
- Columns: Rank (calculated) | Item Name | Theme/Tag (colored chip) | Reach/Impact | Impact/Confidence | Confidence/Ease | Effort (RICE only) | Score (calculated) | Owner | Status
- Rows sorted by Score descending
- Highlight top 5 with subtle accent
- Strikethrough or gray out "Ruled Out" items

2x2 PLOT (right side, ~30%)
- X-axis: Impact (or Score)
- Y-axis: Effort (inverted, so low effort = high) — or Ease
- Plot each item as a bubble (size = Reach or Score)
- Quadrant labels:
  - Top-right: "Quick Wins" (high impact, low effort)
  - Top-left: "Big Bets" (high impact, high effort)
  - Bottom-right: "Fill-ins" (low impact, low effort)
  - Bottom-left: "Avoid" (low impact, high effort)

SUMMARY PANEL (bottom)
- "Committed This Cycle" (items with Committed status)
- "Top Candidates" (next 3-5 by score)
- "Capacity Note" (any constraints)

FOOTER
- Scoring formula:
  - RICE: Score = (Reach x Impact x Confidence) / Effort
  - ICE: Score = Impact x Confidence x Ease

DESIGN RULES
- Clean table with alternating row shading
- Theme chips: use consistent color palette
- 2x2 plot: subtle quadrant shading, Quick Wins quadrant highlighted
- White background, subtle borders
- Numbers formatted appropriately
- No gradients, no 3D""",
    ),
    "winloss": SlideTemplate(
        name="winloss",
        title="Win/Loss Analysis Grid",
        template="""\
TASK
Create a "Win/Loss Analysis Grid" — a single 16:9 image showing why deals were won or lost, patterns by segment, and actionable insights for sales and product.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Win/Loss Analysis" with team/product
- Right: period and as-of date
- Subtitle: "Deals Analyzed: [X] | Win Rate: [Y]%"

ZONE 1 — WIN RATE OVERVIEW (top band)
- Overall win rate (large number with trend)
- Win rate by segment (horizontal bars)
- Comparison to target/benchmark

ZONE 2 — REASONS SPLIT (middle, two columns)

LEFT: WIN REASONS (~40%)
- Horizontal bar chart or ranked list
- Each reason with % frequency
- Green accent
- Top quote (if provided)

RIGHT: LOSS REASONS (~40%)
- Horizontal bar chart or ranked list
- Each reason with % frequency and $ lost
- Red accent
- Competitor callout if applicable

ZONE 3 — COMPETITOR VIEW (bottom-left, ~50%)
- Table: Competitor | Deals Lost To | Win Rate Against | Key Differentiator
- Highlight biggest competitive threat

ZONE 4 — INSIGHTS & ACTIONS (bottom-right, ~50%)
- "For Sales" (2-3 bullets)
- "For Product" (2 bullets)
- "Priority Actions" (with owners)

FOOTER
- Data source note
- Confidence/sample size caveat if relevant

DESIGN RULES
- Clean split layout: wins (green accents) vs. losses (red accents)
- Dollar values formatted with $ and k/M
- Percentages as whole numbers
- White background, subtle section dividers
- Quotes in italics, smaller text
- No gradients, no 3D""",
    ),
    "tam": SlideTemplate(
        name="tam",
        title="Market Sizing (TAM/SAM/SOM)",
        template="""\
TASK
Create a "Market Sizing" slide — a single 16:9 image showing TAM (Total Addressable Market), SAM (Serviceable Addressable Market), and SOM (Serviceable Obtainable Market) with methodology and growth projections.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Market Opportunity" with product/market
- Right: as-of date
- Subtitle: "TAM / SAM / SOM Analysis"

MAIN VISUAL (center, ~60%)
- Nested circles or funnel showing TAM -> SAM -> SOM
- Each ring/level labeled with:
  - Name (TAM, SAM, SOM)
  - $ value (large)
  - Growth rate (CAGR)
  - Brief definition (1 line)
- Current position indicator (if existing market share provided)

METHODOLOGY PANEL (right side, ~40%)
- "TAM Methodology" (2-3 bullets)
- "SAM Filters" (what narrows TAM to SAM)
- "SOM Assumptions" (realistic share assumptions)
- Key sources cited

GROWTH PROJECTION (bottom-left)
- Simple bar or line chart showing TAM/SAM/SOM growth over time
- Base year vs. projection year
- CAGR labels

MARKET DYNAMICS (bottom-right)
- "Growth Drivers" (2-3 bullets)
- "Headwinds" (1-2 bullets)
- "Key Trend" (1 line)

FOOTER
- Sources
- Key caveats or assumptions

DESIGN RULES
- Classic TAM/SAM/SOM nested visual (circles or funnel)
- TAM = largest, lightest shade
- SAM = medium, medium shade
- SOM = smallest, darkest/accent shade
- Dollar values prominent (with B/M formatting)
- White background, professional styling
- No gradients (flat colors), no 3D effects that distort data""",
    ),
    "buildvsbuy": SlideTemplate(
        name="buildvsbuy",
        title="Vendor/Build vs Buy Evaluation",
        template="""\
TASK
Create a "Vendor Evaluation Matrix" or "Build vs. Buy Analysis" — a single 16:9 image showing options scored across weighted criteria with a clear recommendation.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Build vs. Buy / Vendor Evaluation" with capability name
- Right: as-of date
- Subtitle: decision timeline

MAIN SCORING MATRIX (center, ~60%)
- Table format:
  - Rows = Criteria
  - Columns = Options
  - First column: Criterion name + Weight
  - Each cell: raw score
  - Bottom row: Weighted Total Score
- Color-code cells: green (high scores), yellow (medium), red (low)
- Highlight winning option column

COST COMPARISON (top-right, ~20%)
- Bar chart or table showing 3-year TCO per option
- Highlight lowest cost and best value

RISK SUMMARY (bottom-left, ~20%)
- Table: Option | Key Risk | Risk Level (badge)
- Risk badges: High (red), Med (yellow), Low (green)

PROS/CONS PANEL (bottom-center, ~30%)
- For top 2 options:
  - Pros (checkmarks)
  - Cons (warning icons)

RECOMMENDATION BOX (bottom-right, ~20%, prominent)
- "Recommendation: [Option Name]"
- Rationale (2-3 lines)
- Conditions (if any)
- Accent border to highlight

FOOTER
- Evaluation team / sources
- Next steps

DESIGN RULES
- Clear scoring matrix with cell color coding
- Winning option visually prominent
- TCO formatted with $ and k/M
- White background, subtle table borders
- No gradients, no 3D""",
    ),
    "raci": SlideTemplate(
        name="raci",
        title="Operating Model / RACI Diagram",
        template="""\
TASK
Create an "Operating Model" or "RACI Diagram" — a single 16:9 image showing team responsibilities, decision rights, and interfaces for a key process or function.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Operating Model" with process/function name
- Right: as-of date

MAIN RACI MATRIX (center, ~70%)
- Table format:
  - Rows = Activities (grouped by phase if applicable)
  - Columns = Teams/Roles
  - Each cell: R, A, C, I, or blank
- Color-code: R = blue, A = dark blue or bold, C = light blue, I = gray
- Phase headers if activities are grouped

TEAM OVERVIEW (left sidebar, ~15%)
- List of teams with brief scope
- Color-coded to match matrix columns

INTERFACES & RITUALS (right sidebar, ~15%)
- "Key Handoffs" (2-3 bullets with arrows showing direction)
- "Sync Cadence" (e.g., "Weekly product sync: PM + Eng + Design")
- "Escalation Path" (who to escalate to)

DECISION RIGHTS CALLOUT (bottom)
- Table: Decision | Final Authority | Consulted
- For 3-4 key decisions

FOOTER
- Known gaps or friction points (1 line)
- Planned changes (1 line)

DESIGN RULES
- Clean matrix with clear cell boundaries
- RACI letters large enough to read easily
- Phase groupings with subtle dividers
- White background, subtle gridlines
- No gradients, no 3D""",
    ),
    "bets": SlideTemplate(
        name="bets",
        title="Investment Portfolio / Bet Matrix",
        template="""\
TASK
Create an "Investment Portfolio Matrix" — a single 16:9 image showing strategic initiatives plotted by impact vs. confidence, with investment levels and portfolio balance.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Investment Portfolio" with portfolio name
- Right: time horizon and as-of date
- Subtitle: "Total Budget: $[X] | [Count] Initiatives"

MAIN 2x2 MATRIX (center, ~60%)
- X-axis: Expected Impact (Low -> High)
- Y-axis: Confidence (Low -> High)
- Each initiative as a bubble:
  - Size = Investment amount
  - Color = Category (Core/Adjacent/Transformational)
  - Label = Initiative name
- Quadrant labels:
  - Top-right: "High Conviction Bets"
  - Top-left: "Safe Investments"
  - Bottom-right: "Moonshots"
  - Bottom-left: "Reconsider"

ALLOCATION PANEL (right side, ~25%)
- "Target Allocation" (stacked bar or pie)
- "Actual Allocation" (stacked bar or pie)
- Variance callout (over/under in each category)
- Time horizon mix (Near/Mid/Long-term)

INITIATIVE LIST (bottom, ~15%)
- Table: Initiative | Category | Investment | Impact | Confidence | Status
- Sorted by investment descending
- Top 5-8 shown; note if more exist

PORTFOLIO HEALTH BOX (bottom-right corner)
- "Balance Assessment" (1-2 sentences)
- "Gaps" (1 bullet)
- "Watch Items" (1 bullet)

FOOTER
- Legend for bubble size and colors
- Investment guidelines reference

DESIGN RULES
- Clean bubble chart with clear quadrant separation
- Category colors: Core (blue), Adjacent (green), Transformational (orange)
- Bubble sizes proportional to investment
- Don't overcrowd; offset labels if needed
- White background, subtle gridlines
- Dollar values formatted with $ and M/k
- No gradients, no 3D""",
    ),
    "pricing": SlideTemplate(
        name="pricing",
        title="Pricing & Packaging One-Pager",
        template="""\
TASK
Create a "Pricing & Packaging One-Pager" — a single 16:9 image showing pricing tiers, value metrics, feature fences, and target personas for each tier.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Pricing & Packaging" with product name
- Right: as-of date
- Subtitle: "[Current/Proposed] Pricing"

TIER CARDS (top, full width)
- 3-4 cards side by side, one per tier
- Each card:
  - Tier name (header, largest for recommended tier)
  - Price (large, with billing cadence)
  - "Best for: [target persona]"
  - Value prop (1 line)
  - "Highlight" badge on recommended tier

FEATURE MATRIX (middle, full width)
- Rows = Features (grouped by category if helpful)
- Columns = Tiers
- Each cell: checkmark, dash, or limit text
- Highlight key "fence" features (upgrade drivers) with accent color

VALUE METRIC & LIMITS (bottom-left, ~40%)
- "Value Metric" explanation
- Usage limits by tier (table or visual)

COMPETITIVE POSITIONING (bottom-center, ~30%, optional)
- Simple comparison: "vs. Competitor X: [positioning note]"
- Or: price positioning chart

STRATEGY NOTES (bottom-right, ~30%)
- "Discounting Guidance" (1-2 bullets)
- "Upgrade Drivers" (what triggers upgrades)
- "Coming Soon" (if relevant)

FOOTER
- Effective date
- Any caveats

DESIGN RULES
- Clean tier card layout with clear visual hierarchy
- Recommended tier: subtle accent border or "Most Popular" badge
- Feature matrix: alternating row shading, clear checkmarks
- Prices prominent and easy to compare
- White background, professional styling
- No gradients, no 3D""",
    ),
    "capacity": SlideTemplate(
        name="capacity",
        title="Capacity Planning Grid",
        template="""\
TASK
Create a "Capacity Planning Grid" — a single 16:9 image showing team capacity vs. demand by initiative, with allocation percentages, gaps, and hiring implications.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Capacity Planning" with team/org
- Right: period and as-of date

MAIN GRID (center, ~60%)
- Table format:
  - Rows = Initiatives (sorted by priority)
  - Columns = Teams/Skill Groups
  - Each cell: capacity required (person-weeks or %)
  - Row total: total demand
  - Column footer: team capacity available
- Color-code cells:
  - Within capacity: green
  - At capacity: yellow
  - Over capacity: red

CAPACITY SUMMARY (right side, ~25%)
- Per team:
  - Available capacity bar
  - Allocated capacity (stacked by initiative type)
  - Gap indicator (over/under)
- Visual: horizontal stacked bars

ALLOCATION MIX (top-right corner)
- Pie or bar showing:
  - Committed roadmap
  - Tech debt
  - Buffer/unplanned
  - New initiatives

GAP & TRADE-OFF PANEL (bottom, ~20%)
- "Capacity Gaps" (which teams, how much)
- "At Risk Initiatives" (list)
- "Trade-off Options" (2-3 bullets)

HIRING IMPACT (bottom-right)
- Table: Role | Start Date | Capacity Added
- Net capacity change

FOOTER
- Assumptions (e.g., "Assumes 80% utilization after meetings/overhead")
- Planning caveats

DESIGN RULES
- Clean grid with clear capacity vs. demand comparison
- Over-capacity cells clearly flagged (red)
- Hiring shown as dotted/future capacity
- White background, subtle gridlines
- No gradients, no 3D""",
    ),
    "voc": SlideTemplate(
        name="voc",
        title="VoC Synthesis Board",
        template="""\
TASK
Create a "VoC Synthesis Board" — a single 16:9 image showing customer feedback themes, supporting evidence, frequency, and decision implications.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Voice of Customer Synthesis" with product/area
- Right: as-of date
- Subtitle: "Sources: [List] | Sample: [N] | Period: [X]"

MAIN THEME GRID (center, ~70%)
- Cards or rows for each theme:
  - Theme name (bold)
  - Frequency indicator (bar, badge, or #)
  - Sentiment badge (Positive=green, Negative=red, Mixed=yellow)
  - Segment affected (small text)
  - Exemplar quote (italics, in quote marks)
  - Priority ranking (#1, #2, etc.)
- Sorted by priority

DECISION IMPLICATIONS (right panel, ~30%)
- For each top theme:
  - Theme name
  - "Implication" (1 line)
  - "Recommended Action" (1 line)
  - Owner + Timeline

INSIGHTS CALLOUT BOX (bottom-left)
- "Surprising Findings" (2-3 bullets)
- "Emerging Trends" (1-2 bullets)

DATA CONFIDENCE (bottom-right)
- "Data Quality" note
- "Confidence Level" badge (High/Med/Low)
- Key limitations

FOOTER
- Methodology note
- Next steps

DESIGN RULES
- Clean card-based layout for themes
- Quotes in italics, clearly attributed to "Customer" or role
- Frequency visualization: consistent bars or badges
- Sentiment colors: green (positive), red (negative), yellow (mixed)
- White background, subtle card borders
- No gradients, no 3D""",
    ),
    "release": SlideTemplate(
        name="release",
        title="Release Readiness Checklist",
        template="""\
TASK
Create a "Release Readiness Checklist" — a single 16:9 image showing go/no-go criteria for a major release, with status tracking, owners, and blockers.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Release Readiness" with release name
- Right: "Target: [Date] | As of [Date]"
- GO/NO-GO BADGE (prominent): large badge showing current status (Green=Go, Yellow=Conditional, Red=No-Go)

MAIN CHECKLIST (center, ~70%)
- Grouped by category (Engineering, QA, Security, Documentation, Support, Legal/Compliance, GTM, Operations)
- Each criterion row:
  - Criterion name
  - Owner
  - Status badge (Complete=green, In Progress=yellow, Not Started=gray, Blocked=red)
  - Target date
  - Notes (truncated if long)
- Category headers with rollup status (% complete)

BLOCKERS PANEL (right side, ~30%)
- Title: "Current Blockers"
- Each blocker: description, owner, expected resolution
- Red accent

RELEASE PLAN SUMMARY (bottom-left)
- "Release Plan" box:
  - Date/time
  - Rollout strategy
  - Rollback plan
  - On-call

PROGRESS SUMMARY (bottom-right)
- Visual: progress bar or donut showing % complete
- Counts: Complete / In Progress / Not Started / Blocked

FOOTER
- "Go Criteria" (what must be green)
- "Acceptable Risks" (if conditional go)

DESIGN RULES
- Clean checklist format with clear status indicators
- Go/No-Go badge very prominent
- Blockers highlighted in red
- White background, subtle category dividers
- Status colors: Complete=green, In Progress=yellow, Not Started=gray, Blocked=red
- No gradients, no 3D""",
    ),
    "skills": SlideTemplate(
        name="skills",
        title="Skills Coverage Heatmap",
        template="""\
TASK
Create a "Skills Coverage Heatmap" — a single 16:9 image showing capabilities vs. teams with gap analysis and hiring/development implications.

SOURCE MATERIAL
{user_prompt}

OUTPUT RULES
- Single raster image, 16:9 aspect ratio, {size} resolution
- Do NOT output SVG, code, or markdown

LAYOUT SPEC

HEADER
- Left: "Skills Coverage" with org/function
- Right: as-of date

MAIN HEATMAP (center, ~70%)
- Table/matrix:
  - Rows = Skills (grouped by category)
  - Columns = Teams
  - Each cell: coverage level (color-coded)
- Color scale:
  - Strong: dark green
  - Adequate: light green
  - Developing: yellow
  - Gap: red
- Category headers for skill groups
- Criticality indicator (star or badge) on high-priority skills

TEAM SUMMARY (column headers or top band)
- Team name
- Headcount
- Overall coverage score (% of skills at Adequate or better)

GAP ANALYSIS PANEL (right side, ~30%)
- "Priority Gaps" (ranked list)
- For each: skill name, teams affected, recommended approach (Hire/Develop/Partner), owner

ACTIONS PANEL (bottom)
- "Planned Hires" (roles addressing gaps)
- "Development Programs" (training, rotation)
- "Timeline" (when gaps will be addressed)

FOOTER
- Legend for coverage levels
- Criticality indicator explanation
- Assessment methodology note

DESIGN RULES
- Clean heatmap with clear cell boundaries
- Gap cells (red) immediately visible
- Critical skills marked distinctly
- White background, subtle gridlines
- Coverage colors: gradient from red (gap) -> yellow -> green (strong)
- No gradients within cells, no 3D""",
    ),
}


def get_slide_template(name: str) -> SlideTemplate | None:
    """Look up a slide template by name. Returns None if not found."""
    return SLIDE_TEMPLATES.get(name)


def format_slide_help() -> str:
    """Format help text listing all available slide subtemplates."""
    lines = [
        "Available slide subtemplates:",
        "",
    ]
    max_name = max(len(name) for name in SLIDE_TEMPLATES)
    for name, tmpl in SLIDE_TEMPLATES.items():
        lines.append(f"  {name:<{max_name}}  {tmpl.title}")
    lines.extend([
        "",
        "Usage:",
        '  nanobanana slide <subtemplate> "prompt"',
        '  nanobanana slide "prompt"               (generic slide template)',
        "",
        "Examples:",
        '  nanobanana slide funnel "our SaaS product funnel"',
        '  nanobanana slide arr "Q4 2025 ARR bridge"',
        '  nanobanana slide okr "company OKR cascade for Q1"',
    ])
    return "\n".join(lines) + "\n"
