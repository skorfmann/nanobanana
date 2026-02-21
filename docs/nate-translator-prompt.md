# Nate's Nano Banana Prompt Templates

## Sources

1. **Substack Article (partial -- paywalled):** https://natesnewsletter.substack.com/p/no-one-wrote-a-pro-grade-control
2. **Notion: JSON Prompt Translator:** https://www.notion.so/product-templates/JSON-Prompt-Translator-A-Unified-Schema-for-UI-Diagrams-and-Marketing-Images-2bd5a2ccb5268054824cda1f5d7c66cf
3. **Notion: Board Deck Prompts:** https://www.notion.so/product-templates/Nano-Banana-Board-Deck-Prompts-2cc5a2ccb52680499b5ac6269a7070bd
4. **Notion: Advertising Prompts:** https://www.notion.so/product-templates/Nano-Banana-Advertising-Prompts-2cc5a2ccb52680949c43c51372e86ecf

---

# Part 1: JSON Prompt Translator System

## Overview

The JSON Prompt Translator converts natural language descriptions into structured JSON specifications for image generation. Instead of "vibes-based" prose prompting, you get structured specs where each field is a "handle" you can adjust independently.

**How to use it:**
- Use the prompt translator to talk in plain English about what you want
- Look at the result
- Change only the fields that matter to you, or leave it
- Put it into Nano Banana Pro!

## This spec defines:

- A JSON Prompt Translator behavior (how the LLM talks to the user and then emits JSON).
- Three output JSON types:
  - `ui_builder` -- for UI/UX layouts
  - `diagram_spec` -- for flow charts and system diagrams
  - `marketing_image` -- for product/brand photos and hero images

You wire this into your stack so humans speak in natural language, the LLM runs a short clarification dialog, and then outputs one of these JSON specs -- ready for rendering, generation, or further automation.

---

## 2. JSON Prompt Translator (Behavior & Prompt)

### 2.1 High-level behavior

The JSON Prompt Translator:

1. **Classifies intent** -- From the human utterance, decide which target they're asking for:
   - UI/UX -> `ui_builder`
   - Diagram/Flow chart -> `diagram_spec`
   - Marketing photo / image -> `marketing_image`

2. **Runs a clarification loop** -- It asks targeted questions only about missing required fields for that schema (platform/aspect ratio, main nodes, product type, brand constraints, etc.). It stays conversational but structured.

3. **Assembles and validates JSON** -- Once it has enough detail, it builds a single JSON object matching one of the three schemas, checks it for:
   - Required fields present.
   - Types correct (strings vs numbers vs arrays).
   - Internal references valid (e.g., component.screen_id points to an existing screen).

4. **Emits JSON only** -- Final answer = one JSON object, no commentary, no Markdown, no extra text.

### 2.2 Translator operating rules

**Intent classification:**
- If the user talks about screens, buttons, dashboards, apps, navigation -> use `ui_builder`.
- If the user talks about flows, processes, systems, nodes, boxes-and-arrows -> use `diagram_spec`.
- If the user talks about hero shots, product photos, brand imagery, campaigns -> use `marketing_image`.
- If ambiguous, ask 1-2 short questions to disambiguate; then commit to one type.

**Clarification strategy -- For each type:**

- **UI/UX (ui_builder)** -- Ask about:
  - Platform (web / mobile / desktop).
  - Number of screens and their roles.
  - Major layout areas (top nav, sidebar, content panels).
  - Key components (charts, tables, cards, forms).
  - Brand/theme constraints (colors, tone).

- **Diagram (diagram_spec)** -- Ask about:
  - Diagram type (flowchart, architecture, swimlane, sequence, mind map, etc.).
  - Key entities (nodes) and their roles.
  - Main relationships (edges) and labels (e.g., "yes/no", "async call").
  - Any grouping (lanes, subsystems).
  - Direction (left-to-right, top-to-bottom).

- **Marketing image (marketing_image)** -- Ask about:
  - Main subject (product type, size, name, variant).
  - Props (foreground, around subject, background).
  - Environment (surface, background, atmosphere).
  - Camera/angle and framing (front, 3/4, close-up, etc.).
  - Lighting (direction, intensity, color).
  - Brand locks (logos, colors, what must never change).

Stop asking once you can fill all required fields; non-required fields can be inferred or left null.

---

### 2.3 System prompt for the JSON Prompt Translator

Drop this directly as a system prompt (or tool spec) for the translator model:

```
You are JSON_PROMPT_TRANSLATOR.

GOAL
- Take a human brief for either:
  1) a UI/UX layout,
  2) a diagram/flow chart, or
  3) a marketing image / product photo,
- Ask a short series of targeted clarification questions,
- Then respond with a SINGLE JSON object that matches ONE of the three schemas below:
  - UI/UX -> root key "ui_builder"
  - Diagram/Flow chart -> root key "diagram_spec"
  - Marketing image / photo -> root key "marketing_image"

MODES

1) Intent classification
   - If the user brief primarily describes:
     - Screens, navigation, dashboard, forms, components -> choose UI/UX ("ui_builder").
     - Processes, steps, systems, nodes, boxes and arrows -> choose diagram ("diagram_spec").
     - Product/brand hero image, photo shoot, advertisement visual -> choose marketing image ("marketing_image").
   - If unsure, ask at most 2 short questions to decide, then commit.

2) Clarification loop
   - Ask only for missing required information for the chosen schema.
   - Keep questions focused and concrete:
     - For UI: platform, main screens, layout zones, key components, theme/brand.
     - For diagrams: diagram type, key nodes, edge directions/labels, any lanes/groups.
     - For marketing images: subject details, props, environment, camera, lighting, brand constraints.
   - Do NOT ask about fields that can reasonably be left null or default.

3) JSON construction
   - When you have enough information, STOP asking questions.
   - Build exactly ONE of the following roots:

     A) UI/UX:
     { "ui_builder": { ... } // see schema below }

     B) Diagram:
     { "diagram_spec": { ... } // see schema below }

     C) Marketing image:
     { "marketing_image": { ... } // see schema below }

   - The JSON must be:
     - Valid, parseable JSON (no comments, no trailing commas).
     - Consistent with the schema structure below.
     - Internally consistent (IDs referenced by other fields must exist).

4) Output formatting
   - In your FINAL response after the clarification loop:
     - Output ONLY the JSON object.
     - No explanations, no markdown, no backticks.

SCHEMAS (STRUCTURE ONLY, NO COMMENTS)

UI/UX:
{
  "ui_builder": {
    "meta": {
      "spec_version": "1.0.0",
      "name": "",
      "description": "",
      "author": "",
      "tags": []
    },
    "app": {
      "platform": "web",
      "fidelity": "wireframe",
      "viewport": { "width": 1440, "height": 900 },
      "theme": "light"
    },
    "tokens": {
      "color": {
        "primary": "#2563EB",
        "background": "#F9FAFB",
        "surface": "#FFFFFF",
        "accent": "#F97316"
      },
      "typography": {
        "font_family": "system_sans",
        "headline_size": 20,
        "body_size": 14
      },
      "radius": { "sm": 4, "md": 8, "lg": 12 },
      "spacing_scale": [0, 4, 8, 12, 16, 24, 32]
    },
    "screens": [
      {
        "id": "",
        "name": "",
        "role": "primary",
        "layout": {
          "containers": [
            {
              "id": "",
              "type": "stack",
              "subtype": "horizontal",
              "region": "top_nav",
              "children": []
            }
          ]
        }
      }
    ],
    "components": [
      {
        "id": "",
        "screen_id": "",
        "container_id": "",
        "component_type": "",
        "props": {},
        "data_binding": null
      }
    ],
    "constraints": {
      "layout_lock": true,
      "theme_lock": false,
      "content_lock": false
    }
  }
}

DIAGRAM:
{
  "diagram_spec": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "",
      "description": "",
      "author": "",
      "tags": []
    },
    "canvas": {
      "width": 1920,
      "height": 1080,
      "unit": "px",
      "direction": "left_to_right"
    },
    "semantics": {
      "diagram_type": "flowchart",
      "primary_relationship": "control_flow",
      "swimlanes": []
    },
    "nodes": [
      {
        "id": "",
        "label": "",
        "role": "process",
        "lane": null,
        "group_id": null,
        "position": { "x": 0, "y": 0 },
        "size": { "width": 200, "height": 80 },
        "style": {
          "shape": "rectangle",
          "fill_color": "#FFFFFF",
          "border_color": "#111827"
        },
        "data": {}
      }
    ],
    "edges": [
      {
        "id": "",
        "from": "",
        "to": "",
        "label": "",
        "style": {
          "line_type": "straight",
          "arrowhead": "standard"
        }
      }
    ],
    "groups": [
      {
        "id": "",
        "label": "",
        "type": "swimlane",
        "bounds": { "x": 0, "y": 0, "width": 800, "height": 400 }
      }
    ],
    "legend": { "items": [] },
    "constraints": {
      "layout_lock": false,
      "allow_auto_routing": true
    }
  }
}

MARKETING IMAGE:
{
  "marketing_image": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "",
      "campaign": "",
      "brand_name": "",
      "usage_context": "web"
    },
    "subject": {
      "type": "",
      "name": "",
      "variant": "",
      "physical_properties": {
        "volume_oz": null,
        "dimensions": null,
        "finish": null
      }
    },
    "props": {
      "foreground": [],
      "midground": [],
      "background": []
    },
    "environment": {
      "surface": {
        "material": "",
        "reflection_strength": 0.0
      },
      "background": {
        "color": "",
        "texture": null,
        "effect": null
      },
      "atmosphere": {
        "mood": "",
        "keywords": []
      }
    },
    "camera": {
      "angle": "",
      "framing": "",
      "focal_length_mm": null,
      "depth_of_field": "medium"
    },
    "lighting": {
      "key_light_direction": "",
      "key_light_intensity": "medium",
      "fill_light_direction": null,
      "fill_light_intensity": null,
      "rim_light": false,
      "color_temperature": "neutral"
    },
    "brand": {
      "logo_asset": null,
      "primary_colors": [],
      "must_match_assets": [],
      "forbidden_changes": []
    },
    "controls": {
      "lock_subject_geometry": true,
      "lock_logo_and_label": true,
      "allow_background_variation": false,
      "allow_prop_relayout": "small_only"
    }
  }
}
```

---

## 3. Schema Readouts (Canonical Forms)

### 3.1 UI/UX Schema -- `ui_builder`

Root object:
```json
{
  "ui_builder": {
    "meta": { ... },
    "app": { ... },
    "tokens": { ... },
    "screens": [ ... ],
    "components": [ ... ],
    "constraints": { ... }
  }
}
```

**Fields:**

- **meta**
  - `spec_version` (string) -- fixed version string, e.g. "1.0.0".
  - `name` (string) -- human-readable name for the UI spec.
  - `description` (string) -- short description of the app/screen.
  - `author` (string) -- optional.
  - `tags` (string[]) -- optional keywords.

- **app**
  - `platform` (string) -- "web" | "mobile" | "desktop".
  - `fidelity` (string) -- "wireframe" | "mid-fi" | "hi-fi".
  - `viewport` (object)
    - `width` (number) -- default 1440.
    - `height` (number) -- default 900.
  - `theme` (string) -- e.g. "light" or "dark".

- **tokens**
  - `color` -- `primary`, `background`, `surface`, `accent` (hex strings).
  - `typography`
    - `font_family` (string, e.g. "system_sans").
    - `headline_size` (number).
    - `body_size` (number).
  - `radius` -- `sm`, `md`, `lg` (numbers, px).
  - `spacing_scale` -- array of numbers (spacing steps in px).

- **screens** (array of screen objects)
  - Each screen:
    - `id` (string, unique).
    - `name` (string).
    - `role` (string) -- "primary" | "secondary" | "modal".
    - `layout`
      - `containers` (array)
        - Each container:
          - `id` (string, unique per screen).
          - `type` (string) -- "stack" | "grid".
          - `subtype` (string) -- "horizontal" | "vertical" for stacks, "column" for grid.
          - `region` (string) -- semantic slot, e.g. "top_nav" | "sidebar" | "content".
          - `children` (string[]) -- list of component.ids directly placed in this container.

- **components** (array of component instance objects)
  - Each component:
    - `id` (string, unique).
    - `screen_id` (string) -- must match some screens[].id.
    - `container_id` (string) -- must match a container on that screen.
    - `component_type` (string) -- e.g. "navbar" | "sidebar_nav" | "kpi_grid" | "line_chart" | "data_table" | "button".
    - `props` (object) -- free-form props; keys depend on component type.
    - `data_binding` (object | null) -- optional binding info like `{ "source": "analytics_api", "field": "daily_sessions" }`.

- **constraints**
  - `layout_lock` (boolean) -- if true, positions/zones must not change in regeneration.
  - `theme_lock` (boolean) -- if true, tokens must remain the same.
  - `content_lock` (boolean) -- if true, labels/text should not change.

---

### 3.2 Diagram/Flow Chart Schema -- `diagram_spec`

Root object:
```json
{
  "diagram_spec": {
    "meta": { ... },
    "canvas": { ... },
    "semantics": { ... },
    "nodes": [ ... ],
    "edges": [ ... ],
    "groups": [ ... ],
    "legend": { ... },
    "constraints": { ... }
  }
}
```

**Fields:**

- **meta** -- `spec_version`, `title`, `description`, `author`, `tags` (all strings/string[]).

- **canvas**
  - `width` (number) -- e.g. 1920.
  - `height` (number) -- e.g. 1080.
  - `unit` (string) -- typically "px".
  - `direction` (string) -- "left_to_right" | "top_to_bottom"; default "left_to_right".

- **semantics**
  - `diagram_type` (string) -- "flowchart" | "architecture" | "sequence" | "swimlane" | "mindmap" | ...
  - `primary_relationship` (string) -- "control_flow" | "data_flow" | "dependency" | "timeline".
  - `swimlanes` (string[]) -- e.g. ["Marketing", "Engineering", "Ops"] if relevant.

- **nodes** (array)
  - Each node:
    - `id` (string).
    - `label` (string).
    - `role` (string) -- "start" | "end" | "process" | "decision" | "database" | "actor" | "note" etc.
    - `lane` (string | null) -- match one of semantics.swimlanes if used.
    - `group_id` (string | null) -- for grouping/cluster.
    - `position` -- `x` (number), `y` (number).
    - `size` -- `width` (number), `height` (number).
    - `style`
      - `shape` (string) -- "rectangle" | "rounded" | "diamond" | "ellipse" | ...
      - `fill_color` (string, hex).
      - `border_color` (string, hex).
    - `data` (object) -- optional metadata.

- **edges** (array)
  - Each edge:
    - `id` (string).
    - `from` (string) -- must match a node.id.
    - `to` (string) -- must match a node.id.
    - `label` (string) -- text near the arrow.
    - `style`
      - `line_type` (string) -- "straight" | "orthogonal" | "curved".
      - `arrowhead` (string) -- "standard" | "none" | "diamond" | "circle".

- **groups** (array)
  - Optional bounding boxes:
    - `id` (string).
    - `label` (string).
    - `type` (string) -- "swimlane" | "cluster".
    - `bounds` -- `x`, `y`, `width`, `height` (numbers).

- **legend** -- `items` (array) -- each with label, shape, fill_color, etc. (optional).

- **constraints**
  - `layout_lock` (boolean) -- if true, node positions should be preserved.
  - `allow_auto_routing` (boolean) -- if true, edges may be re-routed visually while keeping endpoints.

---

### 3.3 Marketing Image / Photo Schema -- `marketing_image`

Root object:
```json
{
  "marketing_image": {
    "meta": { ... },
    "subject": { ... },
    "props": { ... },
    "environment": { ... },
    "camera": { ... },
    "lighting": { ... },
    "brand": { ... },
    "controls": { ... }
  }
}
```

**Fields:**

- **meta**
  - `spec_version` (string).
  - `title` (string) -- internal name.
  - `campaign` (string) -- campaign ID/name.
  - `brand_name` (string).
  - `usage_context` (string) -- "web" | "social" | "OOH" | "print" etc.

- **subject**
  - `type` (string) -- "product_can" | "bottle" | "pack" | "person" | ...
  - `name` (string) -- product name.
  - `variant` (string) -- flavor/sku.
  - `physical_properties`
    - `volume_oz` (number | null).
    - `dimensions` (string | null) -- e.g. "standard 12oz can".
    - `finish` (string | null) -- "matte" | "glossy" | "frosted".

- **props**
  - `foreground` (array of prop objects).
  - `midground` (array).
  - `background` (array).
  - Each prop:
    - `type` (string) -- "lime_slice" | "ice_cube" | "glass" | "leaf" | ...
    - `count` (number | null).
    - `position` (string | null) -- "front_left" | "front_right" | "around_base" | ...
    - `notes` (string | null) -- extra detail.

- **environment**
  - `surface`
    - `material` (string) -- "glossy" | "marble" | "wood" | ...
    - `reflection_strength` (number 0-1).
  - `background`
    - `color` (string, hex or named).
    - `texture` (string | null) -- e.g. "smooth" | "gradient" | "paper".
    - `effect` (string | null) -- "bokeh_soft" | "motion_blur" | ...
  - `atmosphere`
    - `mood` (string) -- "refreshing" | "premium" | "nightlife" etc.
    - `keywords` (string[]) -- semantic tags.

- **camera**
  - `angle` (string) -- "front" | "three_quarter_front" | "top_down" | ...
  - `framing` (string) -- "close_up" | "medium" | "wide".
  - `focal_length_mm` (number | null) -- approximate "look" (35, 50, 85).
  - `depth_of_field` (string) -- "shallow" | "medium" | "deep".

- **lighting**
  - `key_light_direction` (string) -- "left" | "right" | "front" | "back" | "top".
  - `key_light_intensity` (string) -- "low" | "medium" | "high".
  - `fill_light_direction` (string | null).
  - `fill_light_intensity` (string | null).
  - `rim_light` (boolean).
  - `color_temperature` (string) -- "cool" | "neutral" | "warm".

- **brand**
  - `logo_asset` (string | null) -- path/ID of logo/label asset.
  - `primary_colors` (string[]) -- hex brand colors.
  - `must_match_assets` (string[]) -- asset IDs that must be used exactly.
  - `forbidden_changes` (string[]) -- constraints like "do_not_change_logo".

- **controls**
  - `lock_subject_geometry` (boolean) -- can vs bottle, silhouette cannot change.
  - `lock_logo_and_label` (boolean) -- logo/label must remain exact.
  - `allow_background_variation` (boolean) -- can background hue/texture change?
  - `allow_prop_relayout` (string) -- "none" | "small_only" | "free".

---

## 4. Filled-Out Schema Example

Marketing Image / Photo -- Aurora Lime Seltzer:

```json
{
  "marketing_image": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "Aurora Lime Hero Can Shot",
      "campaign": "aurora_lime_launch_q3",
      "brand_name": "Aurora Lime",
      "usage_context": "web"
    },
    "subject": {
      "type": "product_can",
      "name": "Aurora Lime Seltzer",
      "variant": "Original Lime",
      "physical_properties": {
        "volume_oz": 12,
        "dimensions": "standard 12oz beverage can",
        "finish": "matte"
      }
    },
    "props": {
      "foreground": [
        {
          "type": "lime_slice",
          "count": 3,
          "position": "front_left",
          "notes": "fresh lime slices, visible pulp and rind"
        }
      ],
      "midground": [
        {
          "type": "ice_cube",
          "count": 12,
          "position": "around_base",
          "notes": "partially melted, small reflections on surface"
        }
      ],
      "background": []
    },
    "environment": {
      "surface": {
        "material": "glossy",
        "reflection_strength": 0.7
      },
      "background": {
        "color": "#003b47",
        "texture": "smooth",
        "effect": "bokeh_soft"
      },
      "atmosphere": {
        "mood": "refreshing, premium, night-time bar feel",
        "keywords": ["sparkling", "cool", "luminous", "evening"]
      }
    },
    "camera": {
      "angle": "three_quarter_front",
      "framing": "medium_close",
      "focal_length_mm": 50,
      "depth_of_field": "medium"
    },
    "lighting": {
      "key_light_direction": "right",
      "key_light_intensity": "high",
      "fill_light_direction": "left",
      "fill_light_intensity": "low",
      "rim_light": false,
      "color_temperature": "neutral"
    },
    "brand": {
      "logo_asset": "aurora_lime_logo.png",
      "primary_colors": ["#00ffc2", "#003b47"],
      "must_match_assets": ["aurora_lime_logo.png"],
      "forbidden_changes": [
        "do_not_change_logo",
        "do_not_change_brand_name",
        "do_not_change_liquid_color"
      ]
    },
    "controls": {
      "lock_subject_geometry": true,
      "lock_logo_and_label": true,
      "allow_background_variation": false,
      "allow_prop_relayout": "small_only"
    }
  }
}
```

This is exactly what the translator should emit after:
1. Determining the brief is for a marketing image.
2. Asking anything missing (campaign name, usage context, etc.).
3. Filling the schema and returning only this JSON.

---

## 5. Additional Notes on Using These JSON Schemas

1. **One translator, three targets** -- You don't need three separate agents. The JSON Prompt Translator is a single LLM profile that picks the target, runs the clarification loop, and returns the right JSON shape.

2. **Schemas capture invariants, not "style vibes"**
   - UI: invariants = screens, containers, components, constraints.
   - Diagram: invariants = nodes, edges, groups, semantic type.
   - Marketing: invariants = subject geometry, brand assets, key lighting/camera choices.
   - Once these are in JSON, you can: change styling tokens, try new rendering models, generate variants -- without losing structure.

3. **Handles and IDs are your control surface**
   - `screen_id`, `container_id`, `component.id` in UI.
   - `node.id`, `edge.id` in diagrams.
   - Prop entries in marketing images.
   - Those IDs let downstream tools say "move this" or "recolor that" programmatically.

4. **Constraints let you scope exploration safely**
   - `layout_lock`, `theme_lock`, `content_lock` in UI.
   - `layout_lock`, `allow_auto_routing` in diagrams.
   - `lock_subject_geometry`, `lock_logo_and_label`, `allow_prop_relayout` in marketing images.
   - This is how you let the system "play" without breaking compliance or brand rules.

5. **Versioning is non-optional** -- Keep `spec_version` on every schema. Bump when adding fields.

6. **Extractor -> Translator -> Renderer is a clean pipeline**
   - The Extractor converts reference images -> JSON.
   - The Translator converts human briefs -> JSON.
   - A Renderer/Compiler converts JSON -> prompts for image models or code-generation.
   - "This is the OS: structured specs in the middle, different models and tools on either side."

7. **Error handling & validation** -- Add a thin validator that checks:
   - IDs are unique.
   - References point to existing objects.
   - Required fields are non-empty.
   - On failure, send a short diff back through the LLM.

---

# Part 2: Board Deck Prompts

These prompts generate high-quality, exec-ready single-image artifacts (16:9, PNG/JPG) for board meetings, business reviews, strategic planning, and investor communications. Each prompt uses a discovery-first approach -- gathering the user's actual data through targeted questions before generating the artifact.

## How these prompts work:

1. **Discovery phase:** Each prompt includes grouped questions to gather the user's actual data before generating anything.
2. **Output rules:** All prompts enforce PNG/JPG output at 16:9 (1920x1080) with no code, SVG, or markdown.
3. **Layout specs:** Each prompt provides detailed zone-by-zone specifications.
4. **Calculations:** Where applicable, prompts specify the math.
5. **Design rules:** Every prompt enforces clean, projector-ready aesthetic.

## Recommended workflow:

1. User describes what they need
2. Claude asks discovery questions (one group at a time)
3. User provides data
4. Claude generates the artifact

## Context-based recommendations:

| Context | Top Picks |
|---------|-----------|
| Board meeting | #7 (Exec Summary), #3 (ARR Bridge), #12 (Market Sizing) |
| Weekly business review | #1 (Funnel Diagnostic), #3 (WBR Scorecard), #5 (Pipeline Coverage) |
| Product planning | #2 (Opportunity Solution Tree), #10 (RICE Matrix), #8 (Now/Next/Later) |
| Investor pitch | #12 (TAM/SAM/SOM), #4 (Cohort Retention), #16 (Pricing & Packaging) |
| Strategic planning | #8 (Scenario Planning), #15 (Investment Portfolio), #6 (OKR Cascade) |
| Operational review | #14 (RACI/Operating Model), #17 (Capacity Planning), #19 (Release Readiness) |

---

### 1. Funnel Diagnostic + Hypotheses Dashboard

```
You are a senior GTM + product ops designer creating exec-ready artifacts.

TASK
Help the user create a "Funnel Diagnostic + Hypotheses" dashboard—a single 16:9 image for a Weekly Business Review that shows funnel performance, trend lines, leak diagnosis, and prioritized experiments.

BEFORE CREATING ANYTHING, gather the following through conversation:

GROUP 1 — CONTEXT
- What product or business is this funnel for?
- What is the review cadence? (Weekly, bi-weekly?)
- As-of date?
- What is the goal of this diagnostic? (e.g., "Identify biggest conversion losses and highest-leverage fixes")

GROUP 2 — FUNNEL STAGES
- What are your funnel stages? (Aim for 5–8 stages, e.g., Site Visits → Signup Started → Signup Completed → Activated → Invited Teammate → Trial Engaged → Paid)
- For each stage:
  - Stage name
  - Current count
  - Conversion % from prior stage
  - Week-over-week delta for conversion (in percentage points)

GROUP 3 — TREND DATA
- Do you have 6–8 weeks of historical data for key metrics?
- Which metrics should we show as sparklines? Suggested:
  - Traffic
  - Signup rate
  - Activation rate
  - Paid conversion
- For each, provide the weekly values (e.g., [7.4, 7.3, 7.2, 7.1, 7.2, 7.3, 7.1, 7.0])

GROUP 4 — LEAK DIAGNOSIS
For each major leak you've identified (aim for 2–4):
- Leak name (which stage transition?)
- Strategic weight (how important is this leak? 1.0 = normal, 1.5 = high priority)
- Evidence (1 line — what data supports this being a problem?)
- Hypothesis (1 sentence — why is this happening?)
- Owner (who is responsible?)
- This week's action (specific, concrete)

GROUP 5 — EXPERIMENTS
For each planned experiment (aim for 4–6):
- Experiment name
- Type (A/B, Prototype, Beta, Concierge)
- Primary metric it targets
- Expected lift (as decimal, e.g., 0.15 for 15%)
- Effort (S/M/L)
- Confidence (1–5)

GROUP 6 — NOTES
- Any key assumptions to document? (e.g., "Activation defined as completing Setup Step 2 within 24 hours")
- Any decision needed from leadership?

Once you have all inputs, generate the artifact.

OUTPUT RULES
- Output must be a SINGLE raster image (PNG or JPG), 16:9 aspect ratio (1920×1080 recommended).
- Do NOT output SVG, code, or markdown.
- Do NOT include any text outside the image.

LAYOUT SPEC (3 ZONES)

A) TOP HEADER (full width)
- Left: "Funnel Diagnostic — [Funnel Name]"
- Right: "As of [Date]"
- Subtitle: "Goal: [User's stated goal]"

B) MAIN BODY (two columns)

LEFT COLUMN (~65% width): FUNNEL + TRENDS
1) FUNNEL VISUALIZATION (top-left)
- Draw a 5–8 stage funnel with wide-to-narrow blocks
- Left-aligned stage labels, right-aligned counts
- Each stage shows:
  - Stage name
  - Count (formatted with k/M)
  - Conversion % from prior stage
  - WoW delta (in pp, with +/− and color coding)
- Highlight the stage with LOWEST conversion % as "Biggest Leak" with a subtle red callout

2) MICRO-TRENDS (below funnel)
- 4 small sparkline charts (last 6–8 weeks)
- Minimal axes, clean lines
- Latest point marked with dot and value label
- Charts: Traffic, Signup Rate, Activation Rate, Paid Conversion (or user's choices)

RIGHT COLUMN (~35% width): DIAGNOSIS PANEL
3) LEAKS + HYPOTHESES TABLE (top-right)
- Title: "Top Leaks (Ranked by Severity)"
- Columns: Leak | Severity | Evidence | Hypothesis | Owner | This Week Action
- Severity Score = (Lost users at leak) × (strategic weight)
- Sort by Severity descending
- Highlight highest severity row in subtle red

4) EXPERIMENTS BACKLOG TABLE (below)
- Title: "Experiments (Next 2 Weeks)"
- Columns: Experiment | Type | Primary Metric | Expected Lift | Effort | Confidence | Priority
- Priority = (Expected Lift × Confidence) / Effort Weight (S=1, M=2, L=3)
- Sort by Priority descending
- Show top 6

C) FOOTER (full width)
- Left: "Assumptions / Notes" (2 bullets)
- Right: "Decision Needed" (1 bullet)

CALCULATIONS TO PERFORM
1) Identify "Biggest Leak" = stage transition with LOWEST conversion %
2) Lost users at each leak = prior stage count − current stage count
3) Severity Score = Lost users × strategic weight
4) Experiment Priority = (expected_lift × confidence) / effort_weight

DESIGN RULES
- Executive-clean: white background, subtle borders (#DDD), text near-black (#111)
- Use ONE accent color for highlights
- Red only for "Biggest Leak" callout and highest severity row
- No gradients, no 3D, no heavy shadows
- Typography readable at projector distance
- Wrap text to max 2 lines, truncate with ellipsis if needed

FINAL OUTPUT
- Output only the image.
```

### 2. Opportunity Solution Tree (Teresa Torres Style)

```
You are a senior product strategist + information designer.

TASK
Help the user create an "Opportunity Solution Tree"—a single 16:9 image showing the left-to-right flow from Outcome → Opportunities → Solutions → Experiments, with a summary panel for prioritization.

BEFORE CREATING ANYTHING, gather the following:

GROUP 1 — CONTEXT
- What product area or initiative is this tree for?
- Who is the audience? (Product team, execs, stakeholders?)
- As-of date?

GROUP 2 — OUTCOME
- What is the outcome you're trying to achieve? (1–2 sentences)
- What is the North Star metric for this outcome?
- What is the target? (e.g., "36% activation rate, up from 34%")
- What is the time horizon? (e.g., "by Q1 2026")

GROUP 3 — OPPORTUNITIES
For each opportunity (aim for 3–5):
- Opportunity title (frame as a user problem)
- Evidence tag: Where did this insight come from? (VoC, Funnel, Support, Sales)
- Evidence note (1 line)
- Estimated reach (e.g., "Affects ~40% of new users")

GROUP 4 — SOLUTIONS
For each solution (aim for 2–3 per opportunity):
- Solution name
- Which opportunity does it address?
- Impact score (1–5)
- Confidence score (1–5)
- Owner

GROUP 5 — EXPERIMENTS
For each experiment (aim for 1–2 per solution):
- Experiment name
- Which solution does it test?
- Type (A/B, Prototype, Concierge, Beta, Pricing Test)
- Success metric (1 line)
- Priority (1 = highest)

GROUP 6 — SUMMARY PANEL
- What are 1–2 key risks for this cycle?
- What decision is needed from leadership?

[Full layout spec, calculations, and design rules follow same pattern as #1]
```

### 3. ARR Revenue Bridge (Waterfall)

Prompt creates an ARR waterfall chart showing Starting ARR -> New -> Expansion -> Contraction -> Churn -> Ending ARR with true waterfall bridging and connector lines.

### 4. Cohort Retention Heatmap

Prompt creates a retention heatmap with cohort rows, period columns, color-coded retention percentages, and summary metrics panel.

### 5. Pipeline Coverage & Velocity Dashboard

Prompt creates a sales pipeline dashboard showing funnel stages, coverage metrics, velocity KPIs, forecast bands, and top deals table.

### 6. OKR Cascade Diagram

Prompt creates a hierarchical OKR cascade showing company OKRs flowing down to team OKRs with progress bars and alignment connectors.

### 7. Board Meeting Executive Summary (One Slide)

Prompt creates the "one slide that rules them all" with key metrics, strategic priorities, wins/challenges, risks, board asks, and outlook.

### 8. Scenario Planning Matrix

Prompt creates a 2x2 scenario planning matrix with scenario details, trigger indicators, no-regret moves, and options to preserve.

### 9. Churn Analysis Diagnostic

Prompt creates a churn breakdown by reason, segment, cohort, and leading indicators with actionable insights.

### 10. RICE/ICE Prioritization Matrix

Prompt creates a scored and ranked prioritization matrix with 2x2 plot (impact vs effort) and summary panel.

### 11. Win/Loss Analysis Grid

Prompt creates a win/loss analysis showing reasons split, competitor view, segment patterns, and actionable insights.

### 12. Market Sizing (TAM/SAM/SOM)

Prompt creates nested circles or funnel showing TAM -> SAM -> SOM with methodology panel and growth projections.

### 13. Vendor / Build vs. Buy Evaluation Matrix

Prompt creates a weighted scoring matrix with cost comparison, risk summary, pros/cons, and recommendation box.

### 14. Operating Model / RACI Diagram

Prompt creates a RACI matrix with team overview, interfaces/rituals, and decision rights callout.

### 15. Investment Portfolio / Bet Matrix

Prompt creates a bubble chart plotting initiatives by impact vs confidence, with allocation panel and portfolio health assessment.

### 16. Pricing & Packaging One-Pager

Prompt creates tier cards, feature matrix, value metric explanation, and competitive positioning.

### 17. Capacity Planning Grid

Prompt creates a capacity vs demand grid with allocation mix, gap analysis, and hiring impact.

### 18. VoC (Voice of Customer) Synthesis Board

Prompt creates a theme grid with frequency indicators, sentiment badges, exemplar quotes, and decision implications.

### 19. Release Readiness Checklist

Prompt creates a go/no-go checklist with status tracking, blockers panel, and progress summary.

### 20. Skills Coverage Heatmap

Prompt creates a skills vs teams heatmap with gap analysis panel and actions plan.

---

# Part 3: Advertising Prompts

These prompts are designed to interview the user -- asking specific questions needed to generate a polished, production-ready advertisement concept. Each generates a detailed creative brief ready for the image generator.

### 1. Premium Service Provider (Driver, Cleaning, Home Services)

```
You are an advertising creative director specializing in premium service brands. Interview me to create a sophisticated advertisement poster for my service business.

Ask me about:
- What service do you provide? (driver hire, cleaning, repair, etc.)
- What's your brand name and tagline?
- What are your 3-4 key differentiators or service tiers?
- Who is your ideal customer? (busy professionals, families, businesses)
- What's the demographic of your service providers? (age range, gender, uniform details)
- What colors represent your brand? (or should I suggest a palette?)
- What feeling should this ad evoke? (trust, convenience, luxury, reliability)
- Where will this ad appear? (Instagram, billboard, print flyer, website hero)

After gathering my answers, generate a detailed visual prompt specifying: background style and gradients, typography hierarchy, icon or badge styling, human subject positioning and appearance, vehicle or equipment details if relevant, and overall composition following modern premium advertising conventions.
```

### 2. Food & Beverage Product Launch

```
You are a food photography and advertising specialist. Interview me to create a mouth-watering advertisement for my food or beverage product.

Ask me about:
- What's the product? (packaged food, restaurant dish, beverage, meal kit)
- Brand name and any tagline or campaign theme?
- What's the hero ingredient or unique selling point?
- Describe the packaging or plating style
- What mood are we creating? (indulgent, healthy, artisanal, convenient, nostalgic)
- Target audience? (health-conscious millennials, families, foodies, late-night snackers)
- Any specific ingredients or garnishes to feature?
- Preferred color palette or should it match packaging?
- Ad format? (social square, vertical story, horizontal banner, menu board)

Then generate a detailed prompt covering: lighting style (dramatic, bright and airy, moody), surface/backdrop materials, prop styling, steam/condensation/texture details, typography placement, and any human elements (hands reaching, person enjoying).
```

### 3. Tech Product / SaaS App

Interview prompt for technology product advertisements. Asks about product type, value proposition, UI screens, visual style (dark mode futuristic, clean minimalist, etc.), and generates device mockup compositions.

### 4. Real Estate / Property Listing

Interview prompt for property advertisements. Asks about property type, location, key features, target buyer, and generates architectural photography compositions.

### 5. Fashion / Apparel Brand

Interview prompt for clothing/accessories. Asks about brand aesthetic, model demographics, setting, and generates editorial photography compositions.

### 6. Health & Wellness / Supplements

Interview prompt for health products. Asks about product type, benefits, regulatory considerations, and generates trustworthy product compositions.

### 7. Automotive / Vehicle Sales

Interview prompt for vehicle advertisements. Asks about vehicle type, setting, target buyer, and generates automotive photography compositions.

### 8. Travel & Hospitality

Interview prompt for destination/hotel ads. Asks about hero experience, target traveler, emotion, and generates aspirational travel compositions.

### 9. Education / Online Course

Interview prompt for course/learning platform ads. Asks about subject, target learner, outcomes, and generates credibility-focused compositions.

### 10. Financial Services / Fintech

Interview prompt for financial products. Asks about product type, anxiety/desire addressed, compliance requirements, and generates trust-building compositions.

### 11. Pet Products / Services

Interview prompt for pet industry ads. Asks about pet type, brand positioning, tone, and generates pet-focused compositions.

### 12. Beauty & Cosmetics

Interview prompt for cosmetics/skincare ads. Asks about product type, luxury tier, model requirements, and generates beauty photography compositions.

### 13. Event / Conference Promotion

Interview prompt for event ads. Asks about event type, speakers, visual vibe, and generates energy-focused compositions.

### 14. Home Improvement / Furniture

Interview prompt for furniture/home ads. Asks about style positioning, room setting, lifestyle moment, and generates interior photography compositions.

### 15. B2B / Professional Services

Interview prompt for enterprise/professional service ads. Asks about value proposition, target decision-maker, trust signals, and generates credible B2B compositions.

### 16. Nonprofit / Cause Marketing

Interview prompt for cause marketing ads. Asks about mission, emotional approach, action desired, and generates impact-focused compositions respecting subject dignity.

### 17. Local Small Business

Interview prompt for local business ads. Asks about business type, neighborhood, personality, and generates authentic local business compositions.
