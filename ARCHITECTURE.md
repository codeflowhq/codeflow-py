# CodeFlow Python Library Architecture

## Purpose

`code_visualizer` is the import package for the `codeflow-py` distribution.
The public surface is intentionally small:

- `visualize(...)`
- `visualize_algorithm(...)`

Everything else is organized as internal boundaries that support one
visualization pipeline.

## Top-Level Structure

`src/code_visualizer/`

- `shared/`
  - shared config, models, and `ViewKind`
- `pipeline/`
  - value-visualization orchestration
- `converters/`
  - value coercion adapters
- `views/`
  - semantic view builders
- `renderers/`
  - Graphviz and HTML renderers
- `tracing/`
  - trace collection, filtering, processing, and rendering
- `utils/`
  - narrow helper packages only

Repository-level assets live outside `src/`:

- `demo/codeflow_demo/`
- `demo/outputs/`
- `tests/`

## Shared Boundary

`shared/` owns stable definitions that multiple layers depend on.

- `shared/config.py`
  - `VisualizerConfig`
- `shared/models.py`
  - graph, artifact, and trace models
- `shared/view_kinds.py`
  - `ViewKind`

`shared/` is for architectural definitions. Pure helpers belong in `utils/`.

## Value Visualization Pipeline

Entry point:

- `pipeline/pipeline.py`

Flow:

1. `pipeline.py` prepares config and coercion.
2. `resolver.py` resolves `ViewKind`, recursion depth, and compatibility.
3. `render_dispatch.py` dispatches to one of three paths:
   - scalar rendering
   - structured view rendering
   - fallback node-link rendering
4. Structured rendering delegates to `views/dispatcher.py`.
5. Concrete view modules organize semantic graph structure.
6. `renderers/` emit Graphviz or HTML labels.

`pipeline/` owns orchestration. It should not own view semantics or output code.

Compact view of the same flow:

```text
visualize(...)
  -> pipeline/pipeline.py
  -> pipeline/resolver.py
  -> pipeline/render_dispatch.py
     -> scalar path
     -> structured path -> views/dispatcher.py -> views/* -> renderers/*
     -> fallback path   -> views/nodelink_*    -> renderers/graphviz/renderer.py
```

## Views

`views/` answers: “what structure should represent this value?”

Key modules:

- `dispatcher.py`
  - routes resolved `ViewKind` values to view builders
- `composite_view.py`
  - nested/composite inline rendering support
- `graph_view.py`, `tree_view.py`, `image_view.py`, `bar_view.py`
  - top-level semantic views
- `nodelink_view.py`
  - fallback node-link view entry point
- `nodelink_graph.py`
  - generic object-to-node-link graph extraction
- `node_views/`
  - array, matrix, table, hash table, linked list, and heap views

`views/` does not emit DOT directly. That belongs in `renderers/`.

## Renderers

`renderers/` owns output formatting.

- `renderers/graphviz/`
  - `*_renderer.py` modules for each view family
- `renderers/html/`
  - label builders and nested HTML table formatting
- `renderers/shared/`
  - renderer-only shared constants and DOT helpers

Renderer naming matches view naming where practical:

- `views/graph_view.py` -> `renderers/graphviz/graph_renderer.py`
- `views/tree_view.py` -> `renderers/graphviz/tree_renderer.py`
- `views/nodelink_view.py` -> `renderers/graphviz/renderer.py`

## Trace Pipeline

Entry point:

- `tracing/pipeline.py`

Trace flow:

1. `pipeline.py` runs StepTracer and collects snapshots.
2. `filtering.py` normalizes watch targets and access-path rules.
3. `processing.py` augments and compacts events.
4. `rendering.py` groups events into traces and renders frames.
5. Each frame delegates back into the normal value pipeline.

Browser-style manifest output is a parameterized mode on
`visualize_algorithm(...)`, not a separate API package.

Compact view of the trace flow:

```text
visualize_algorithm(...)
  -> tracing/pipeline.py
  -> tracing/filtering.py
  -> tracing/processing.py
  -> tracing/rendering.py
  -> pipeline/pipeline.py   # per rendered frame
```

## Naming Rules

- `shared/*`
  - stable definitions
- `pipeline/*`
  - orchestration roles (`pipeline.py`, `resolver.py`, `render_dispatch.py`)
- `views/*`
  - semantic view builders (`*_view.py` where appropriate)
- `renderers/*`
  - output emitters (`*_renderer.py` where appropriate)
- `tracing/*`
  - trace pipeline stages (`pipeline.py`, `filtering.py`, `processing.py`, `rendering.py`, `types.py`)

Avoid generic names such as `common.py`, `helpers.py`, or browser-only API wrappers.

## Testing Layout

Tests mirror the same boundaries.

- `tests/shared/`
- `tests/pipeline/`
- `tests/renderers/graphviz/`
- `tests/views/`
- `tests/views/node_views/`
- `tests/tracing/`
- `tests/converters/`
- `tests/utils/`

## Public API

Root package exports remain intentionally minimal:

- `visualize`
- `visualize_algorithm`

Lower-level tracing helpers, config types, and models stay in subpackages.
They are internal building blocks first, convenience imports second.
