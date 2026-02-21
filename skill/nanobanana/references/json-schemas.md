# JSON Translator Schemas

Structured JSON specs give precise control over image generation. Each field is a "handle" you can adjust independently -- change lighting without affecting composition, swap a component without rebuilding the layout.

Use JSON specs when:
- The user needs precise control over layout, components, or visual elements
- Iterating on a design -- change individual fields without rewriting the whole prompt
- Building a consistent series of images with shared tokens/constraints

Use prose prompts instead when:
- Board Deck artifacts (they have their own structured format)
- Simple one-shot generations where JSON overhead isn't worth it

## ui_builder -- UI/UX Layouts

```json
{
  "ui_builder": {
    "meta": { "name": "", "description": "" },
    "app": { "platform": "web", "fidelity": "wireframe", "viewport": { "width": 1440, "height": 900 }, "theme": "light" },
    "tokens": {
      "color": { "primary": "#2563EB", "background": "#F9FAFB", "surface": "#FFFFFF", "accent": "#F97316" },
      "typography": { "font_family": "system_sans", "headline_size": 20, "body_size": 14 }
    },
    "screens": [{
      "id": "", "name": "", "role": "primary",
      "layout": { "containers": [{ "id": "", "type": "stack", "subtype": "horizontal", "region": "top_nav", "children": [] }] }
    }],
    "components": [{ "id": "", "screen_id": "", "container_id": "", "component_type": "", "props": {} }],
    "constraints": { "layout_lock": true, "theme_lock": false, "content_lock": false }
  }
}
```

**Key fields:** `app.platform` (web/mobile/desktop), `app.fidelity` (wireframe/mid-fi/hi-fi), `tokens` (design system), `screens[].layout.containers` (spatial arrangement), `components` (what goes where), `constraints` (what must stay fixed).

## diagram_spec -- Diagrams & Flowcharts

```json
{
  "diagram_spec": {
    "meta": { "title": "", "description": "" },
    "canvas": { "width": 1920, "height": 1080, "direction": "left_to_right" },
    "semantics": { "diagram_type": "flowchart", "primary_relationship": "control_flow", "swimlanes": [] },
    "nodes": [{ "id": "", "label": "", "role": "process", "style": { "shape": "rectangle", "fill_color": "#FFFFFF", "border_color": "#111827" } }],
    "edges": [{ "id": "", "from": "", "to": "", "label": "", "style": { "line_type": "straight", "arrowhead": "standard" } }],
    "groups": [{ "id": "", "label": "", "type": "swimlane" }],
    "constraints": { "layout_lock": false, "allow_auto_routing": true }
  }
}
```

**Key fields:** `semantics.diagram_type` (flowchart/architecture/sequence/swimlane/mindmap), `nodes` with roles (start/end/process/decision/database), `edges` with labels, `groups` for swimlanes or clusters.

## marketing_image -- Product Photos & Hero Images

```json
{
  "marketing_image": {
    "meta": { "title": "", "campaign": "", "brand_name": "", "usage_context": "web" },
    "subject": { "type": "", "name": "", "variant": "" },
    "props": { "foreground": [], "midground": [], "background": [] },
    "environment": {
      "surface": { "material": "", "reflection_strength": 0.0 },
      "background": { "color": "" },
      "atmosphere": { "mood": "", "keywords": [] }
    },
    "camera": { "angle": "", "framing": "", "depth_of_field": "medium" },
    "lighting": { "key_light_direction": "", "key_light_intensity": "medium", "color_temperature": "neutral" },
    "brand": { "primary_colors": [], "forbidden_changes": [] },
    "controls": { "lock_subject_geometry": true, "lock_logo_and_label": true }
  }
}
```

**Key fields:** `subject` (what you're photographing), `props` (foreground/midground/background elements), `camera` (angle/framing/DoF), `lighting` (direction/intensity/color temp), `brand` (colors, constraints), `controls` (what must stay fixed).

## Passing JSON to Nanobanana

```bash
nanobanana generate -aspect 16:9 -size 2K -o output.jpg "$(cat /tmp/spec.json)"
```

Full schema documentation: `docs/nate-translator-prompt.md`
