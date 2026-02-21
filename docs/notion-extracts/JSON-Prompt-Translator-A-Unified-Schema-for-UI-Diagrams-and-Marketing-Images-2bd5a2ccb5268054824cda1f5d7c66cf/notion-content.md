# JSON Prompt Translator: A Unified Schema for UI, Diagrams, and Marketing Images

> Source: https://www.notion.so/product-templates/JSON-Prompt-Translator-A-Unified-Schema-for-UI-Diagrams-and-Marketing-Images-2bd5a2ccb5268054824cda1f5d7c66cf
> Extracted via: agent-browser (NotionAdapter)

---

JSON Prompt Translator: A Unified Schema for UI, Diagrams, and Marketing Images
I know this looks scary, but JSON is just a way to write structured data as text: labeled boxes inside boxes. Instead of a vague paragraph like “cool alien dashboard,” you get a clear object: screens, components, nodes, edges, subject, camera, etc. That matters because models and tools can’t reliably follow vibes, but they can follow structure.
How to use it here:
Use the prompt translator to talk in plain English about what you want
Look at the result
Change only the fields that matter to you, or leave it
Put it into Nano Banana Pro!
This spec defines:
A JSON Prompt Translator behavior (how the LLM talks to the user and then emits JSON).
Three output JSON types:
ui_builder – for UI/UX layouts.
diagram_spec – for flow charts and system diagrams.
marketing_image – for product/brand photos and hero images.
You wire this into your stack so humans speak in natural language, the LLM runs a short clarification dialog, and then outputs one of these JSON specs—ready for rendering, generation, or further automation.
2. JSON Prompt Translator (Behavior & Prompt)
2.1 High-level behavior
The JSON Prompt Translator:
Classifies intent
From the human utterance, decide which target they’re asking for:
UI/UX → ui_builder
Diagram/Flow chart → diagram_spec
Marketing photo / image → marketing_image
Runs a clarification loop
It asks targeted questions only about missing required fields for that schema (platform/aspect ratio, main nodes, product type, brand constraints, etc.).
It stays conversational but structured.
Assembles and validates JSON
Once it has enough detail, it builds a single JSON object matching one of the three schemas, checks it for:
Required fields present.
Types correct (strings vs numbers vs arrays).
Internal references valid (e.g., component.screen_id points to an existing screen).
Emits JSON only
Final answer = one JSON object, no commentary, no Markdown, no extra text.
2.2 Translator operating rules
Intent classification
If the user talks about screens, buttons, dashboards, apps, navigation → use ui_builder.
If the user talks about flows, processes, systems, nodes, boxes-and-arrows → use diagram_spec.
If the user talks about hero shots, product photos, brand imagery, campaigns → use marketing_image.
If ambiguous, ask 1–2 short questions to disambiguate; then commit to one type.
Clarification strategy
For each type:
UI/UX (ui_builder)
Ask about:
Platform (web / mobile / desktop).
Number of screens and their roles.
Major layout areas (top nav, sidebar, content panels).
Key components (charts, tables, cards, forms).
Brand/theme constraints (colors, tone).
Diagram (diagram_spec)
Ask about:
Diagram type (flowchart, architecture, swimlane, sequence, mind map, etc.).
Key entities (nodes) and their roles.
Main relationships (edges) and labels (e.g., “yes/no”, “async call”).
Any grouping (lanes, subsystems).
Direction (left-to-right, top-to-bottom).
Marketing image (marketing_image)
Ask about:
Main subject (product type, size, name, variant).
Props (foreground, around subject, background).
Environment (surface, background, atmosphere).
Camera/angle and framing (front, 3/4, close-up, etc.).
Lighting (direction, intensity, color).
Brand locks (logos, colors, what must never change).
Stop asking once you can fill all required fields; non-required fields can be inferred or left null.
2.3 System prompt for the JSON Prompt Translator
You can drop this directly as a system prompt (or tool spec) for the translator model:
You are JSON_PROMPT_TRANSLATOR.

GOAL
- Take a human brief for either:
  1) a UI/UX layout,
  2) a diagram/flow chart, or
  3) a marketing image / product photo,
- Ask a short series of targeted clarification questions,
- Then respond with a SINGLE JSON object that matches ONE of the three schemas below:
  - UI/UX → root key "ui_builder"
  - Diagram/Flow chart → root key "diagram_spec"
  - Marketing image / photo → root key "marketing_image"

MODES

1) Intent classification
- If the user brief primarily describes:
  - Screens, navigation, dashboard, forms, components → choose UI/UX ("ui_builder").
  - Processes, steps, systems, nodes, boxes and arrows → choose diagram ("diagram_spec").
  - Product/brand hero image, photo shoot, advertisement visual → choose marketing image ("marketing_image").
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
     {
       "ui_builder": { ... }   // see schema below
     }
  B) Diagram:
     {
       "diagram_spec": { ... } // see schema below
     }
  C) Marketing image:
     {
       "marketing_image": { ... } // see schema below
     }

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
      "viewport": {
        "width": 1440,
        "height": 900
      },
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
      "radius": {
        "sm": 4,
        "md": 8,
        "lg": 12
      },
      "spacing_scale": [0,4,8,12,16,24,32]
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
        "position": {
          "x": 0,
          "y": 0
        },
        "size": {
          "width": 200,
          "height": 80
        },
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
        "bounds": {
          "x": 0,
          "y": 0,
          "width": 800,
          "height": 400
        }
      }
    ],
    "legend": {
      "items": []
    },
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
​
3. Schema Readouts (Canonical Forms)
Below are the same schemas, documented more clearly (still JSON-shaped, but with explanations in text rather than in-line comments).
3.1 UI/UX Schema –
ui_builder
Root object
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
​
Fields
meta
spec_version (string) – fixed version string, e.g. "1.0.0".
name (string) – human-readable name for the UI spec.
description (string) – short description of the app/screen.
author (string) – optional.
tags (string[]) – optional keywords.
app
platform (string) – "web" | "mobile" | "desktop".
fidelity (string) – "wireframe" | "mid-fi" | "hi-fi".
viewport (object)
width (number) – default 1440.
height (number) – default 900.
theme (string) – e.g. "light" or "dark".
tokens
color
primary, background, surface, accent (hex strings).
typography
font_family (string, e.g. "system_sans").
headline_size (number).
body_size (number).
radius
sm, md, lg (numbers, px).
spacing_scale
array of numbers (spacing steps in px).
screens (array of screen objects)
Each screen:
id (string, unique).
name (string).
role (string) – "primary" | "secondary" | "modal".
layout
containers (array)
Each container:
id (string, unique per screen).
type (string) – "stack" | "grid".
subtype (string) – "horizontal" | "vertical" for stacks, "column" for grid.
region (string) – semantic slot, e.g. "top_nav" | "sidebar" | "content".
children (string[]) – list of component.ids directly placed in this container (optional, can also be implied via components[].container_id).
components (array of component instance objects)
Each component:
id (string, unique).
screen_id (string) – must match some screens[].id.
container_id (string) – must match a container on that screen.
component_type (string) – e.g. "navbar" | "sidebar_nav" | "kpi_grid" | "line_chart" | "data_table" | "button".
props (object) – free-form props; keys depend on component type.
data_binding (object | null) – optional binding info like { "source": "analytics_api", "field": "daily_sessions" }.
constraints
layout_lock (boolean) – if true, positions/zones must not change in regeneration.
theme_lock (boolean) – if true, tokens must remain the same.
content_lock (boolean) – if true, labels/text should not change.
3.2 Diagram/Flow Chart Schema –
diagram_spec
Root object
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
​
Fields
meta
spec_version (string).
title (string).
description (string).
author (string).
tags (string[]).
canvas
width (number) – e.g. 1920.
height (number) – e.g. 1080.
unit (string) – typically "px".
direction (string) – "left_to_right" | "top_to_bottom"; default "left_to_right".
semantics
diagram_type (string) – "flowchart" | "architecture" | "sequence" | "swimlane" | "mindmap" | ....
primary_relationship (string) – "control_flow" | "data_flow" | "dependency" | "timeline".
swimlanes (string[]) – e.g. ["Marketing", "Engineering", "Ops"] if relevant.
nodes (array)
Each node:
id (string).
label (string).
role (string) – "start" | "end" | "process" | "decision" | "database" | "actor" | "note" etc.
lane (string | null) – match one of semantics.swimlanes if used.
group_id (string | null) – for grouping/cluster.
position
x (number).
y (number).
size
width (number).
height (number).
style
shape (string) – "rectangle" | "rounded" | "diamond" | "ellipse" | ....
fill_color (string, hex).
border_color (string, hex).
data (object) – optional metadata; e.g. underlying system, SLA, etc.
edges (array)
Each edge:
id (string).
from (string) – must match a node.id.
to (string) – must match a node.id.
label (string) – text near the arrow (yes/no, GET/POST, etc.).
style
line_type (string) – "straight" | "orthogonal" | "curved".
arrowhead (string) – "standard" | "none" | "diamond" | "circle".
groups (array)
Optional bounding boxes:
id (string).
label (string).
type (string) – "swimlane" | "cluster".
bounds
x, y, width, height (numbers).
legend
items (array) – each with label, shape, fill_color, etc. (optional).
constraints
layout_lock (boolean) – if true, node positions should be preserved.
allow_auto_routing (boolean) – if true, edges may be re-routed visually while keeping endpoints.
3.3 Marketing Image / Photo Schema –
marketing_image
Root object
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
​
Fields
meta
spec_version (string).
title (string) – internal name.
campaign (string) – campaign ID/name.
brand_name (string).
usage_context (string) – "web" | "social" | "OOH" | "print" etc.
subject
type (string) – "product_can" | "bottle" | "pack" | "person" | ....
name (string) – product name.
variant (string) – flavor/sku.
physical_properties
volume_oz (number | null) – for beverages if applicable.
dimensions (string | null) – free-form, e.g. "standard 12oz can".
finish (string | null) – "matte" | "glossy" | "frosted".
props
foreground (array of prop objects).
midground (array).
background (array).
Each prop:
type (string) – "lime_slice" | "ice_cube" | "glass" | "leaf" | ....
count (number | null).
position (string | null) – "front_left" | "front_right" | "around_base" | ....
notes (string | null) – extra detail.
environment
surface
material (string) – "glossy" | "marble" | "wood" | ....
reflection_strength (number 0–1).
background
color (string, hex or named).
texture (string | null) – e.g. "smooth" | "gradient" | "paper".
effect (string | null) – "bokeh_soft" | "motion_blur" | ....
atmosphere
mood (string) – "refreshing" | "premium" | "nightlife" etc.
keywords (string[]) – semantic tags.
camera
angle (string) – "front" | "three_quarter_front" | "top_down" | ....
framing (string) – "close_up" | "medium" | "wide".
focal_length_mm (number | null) – approximate “look” (35, 50, 85).
depth_of_field (string) – "shallow" | "medium" | "deep".
lighting
key_light_direction (string) – "left" | "right" | "front" | "back" | "top".
key_light_intensity (string) – "low" | "medium" | "high".
fill_light_direction (string | null).
fill_light_intensity (string | null).
rim_light (boolean).
color_temperature (string) – "cool" | "neutral" | "warm".
brand
logo_asset (string | null) – path/ID of logo/label asset.
primary_colors (string[]) – hex brand colors.
must_match_assets (string[]) – asset IDs that must be used exactly.
forbidden_changes (string[]) – constraints like "do_not_change_logo", "do_not_change_liquid_color".
controls
lock_subject_geometry (boolean) – can vs bottle, silhouette cannot change.
lock_logo_and_label (boolean) – logo/label must remain exact.
allow_background_variation (boolean) – can background hue/texture change?
allow_prop_relayout (string) – "none" | "small_only" | "free".
4. Filled-Out Schema Example
(Marketing Image / Photo – Aurora Lime Seltzer)
Below is a complete marketing_image instance using your Aurora Lime beverage example.
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
        "keywords": [
          "sparkling",
          "cool",
          "luminous",
          "evening"
        ]
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
      "primary_colors": [
        "#00ffc2",
        "#003b47"
      ],
      "must_match_assets": [
        "aurora_lime_logo.png"
      ],
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
​
This is exactly what the translator should emit after:
Determining the brief is for a marketing image.
Asking anything missing (campaign name, usage context, etc.).
Filling the schema and returning only this JSON.
5. Additional Notes on Using These JSON Schemas
One translator, three targets
You don’t need three separate agents.
The JSON Prompt Translator is a single LLM profile that:
picks the target (ui_builder / diagram_spec / marketing_image),
runs the clarification loop,
returns the right JSON shape.
Schemas capture invariants, not “style vibes”
UI: invariants = screens, containers, components, constraints.
Diagram: invariants = nodes, edges, groups, semantic type.
Marketing: invariants = subject geometry, brand assets, key lighting/camera choices.
Once these are in JSON, you can:
Change styling tokens.
Try new rendering models.
Generate variants—without losing structure.
Handles and IDs are your control surface
screen_id, container_id, component.id in UI.
node.id, edge.id in diagrams.
Prop entries in marketing images.
Those IDs let downstream tools say “move this” or “recolor that” programmatically, instead of hoping an LLM reinterprets a paragraph correctly.
Constraints let you scope exploration safely
layout_lock, theme_lock, content_lock in UI.
layout_lock, allow_auto_routing in diagrams.
lock_subject_geometry, lock_logo_and_label, allow_prop_relayout in marketing images.
This is how you let the system “play” (e.g., alternative cropping, extra glow, minor prop tweaks) without breaking compliance or brand rules.
Versioning is non-optional
Keep spec_version on every schema.
When you add fields (e.g., responsiveness to UI, or new prop categories for marketing), bump the version and keep translators/renderers aligned.
Extractor → Translator → Renderer is a clean pipeline
The Extractor (like your Nano Banana image extractor) converts reference images → JSON using similar taxonomies.
The Translator converts human briefs → JSON using these schemas.
A Renderer/Compiler converts JSON → prompts for image models or code-generation.
This is the OS: structured specs in the middle, different models and tools on either side.
Error handling & validation
It’s worth adding a thin validator that checks:
IDs are unique.
References point to existing objects.
Required fields are non-empty.
On failure, you can send a short diff back through the LLM: “fix this JSON to match the schema and validation errors.”
If you want, the next step is the Compiler layer: JSON → concrete prompt strings for your visual generator or React/Tailwind code generator, driven directly off these schemas.
