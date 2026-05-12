# CodeFlow Python Library Architecture

This document describes the current structure of the `code_visualizer` Python
library after the refactor away from the earlier monolithic renderer design.

The goal of the library is narrow:

- trace Python execution,
- resolve an appropriate visualization for each watched value,
- render stable graph/image artifacts,
- expose a small public API for Python callers and browser adapters.

## Design Principles

- Strongly typed internal boundaries
- One module owns one concern
- Clear separation between orchestration, rendering, tracing, and adapters
- Minimal compatibility layers
- Small public API, larger internal implementation surface

## Top-Level Package Layout

`src/code_visualizer/`

- `__init__.py`
  - Public package API only
  - Re-exports stable entry points such as `visualize`, `trace_algorithm`,
    `visualize_algorithm`, and browser-manifest helpers
- `api/`
  - Browser-facing adapters that serialize internal Python models into
    JSON-like payloads
  - This layer exists to avoid coupling web clients to internal dataclasses and
    enum details
- `builders/`
  - High-level orchestration from runtime values to artifacts
  - Decides whether to use a structured view builder, scalar renderer, or
    generic IR extractor
- `converters/`
  - Value coercion pipeline for types such as `deque`, `numpy`, `pandas`, etc.
- `ir/`
  - Generic object extraction into the internal visual graph representation
  - Used when no specialized structured view applies
- `rendering/`
  - Rendering helpers and backends
  - Contains:
    - `graphviz/` for DOT generation
    - `value_html/` for nested HTML label formatting
    - `html_labels.py` for Graphviz HTML-like label primitives
    - `theme.py` for shared visual constants
- `tracing/`
  - Step-tracer integration, event processing, watch filters, and trace-to-frame
    rendering
- `utils/`
  - Focused helper packages:
    - `detection/` for graph/tree/linked/hash-like structure detection
    - `type_patterns/` for override matching
    - `value_formatting/` for text, size, and SVG id helpers
    - `image_sources.py` and `value_shapes.py` for domain-specific helpers
- `views/`
  - Structured visualization builders
  - `node_views/` contains node-style views such as array, matrix, hash table,
    linked list, and heap dual

## Core Data Flow

### 1. Direct value visualization

`visualize(value, name, config)` in
`src/code_visualizer/builders/visualization.py`

Flow:

1. Clone config and build a coercion pipeline
2. Coerce the incoming value
3. Resolve the view kind via `builders/view_resolution.py`
4. If the value matches a structured view:
   - delegate to `builders/structured_artifacts.py`
   - which uses `graph_view_builder.py`
   - which dispatches to `views/` builders
5. If the value is scalar:
   - delegate to `builders/scalar_artifacts.py`
6. Otherwise:
   - extract generic IR via `ir/extractor.py`
   - render with `rendering/graphviz/graphviz_export.py`

### 2. Trace visualization

`trace_algorithm(...)` and `visualize_algorithm(...)` in `tracing/pipeline.py`

Flow:

1. Transform code through the step-tracer integration
2. Collect variable events and normalize watch filters
3. Post-process events in `tracing/event_processing.py`
4. Build per-variable traces
5. Render each frame using the same `visualize(...)` value pipeline

### 3. Browser/web payload generation

`build_browser_manifest_payload(...)` in
`src/code_visualizer/api/browser_manifest.py`

Flow:

1. Call `visualize_algorithm(...)`
2. Convert `RenderedTraceFrame` + `Artifact` models into browser-safe
   dataclasses
3. Serialize them into a plain `dict[str, Any]`

This adapter layer is intentionally separate from the core API so the browser
does not depend on internal Python model layout.

## Internal Model Boundaries

### Config

`src/code_visualizer/config.py`

- Defines the library configuration model
- Contains defaults and override maps
- Must remain the single source of truth for runtime options

### View Resolution

`src/code_visualizer/builders/view_resolution.py`

- Determines which `ViewKind` to use
- Applies explicit overrides, type-pattern overrides, and auto-detection
- Computes recursion depth precedence

### View Execution Context

`src/code_visualizer/views/context.py`

- Replaces the old untyped runtime dictionary
- Provides typed access to:
  - output graph
  - resolver
  - item limit
  - focus path
  - title visibility
  - ID counter

This is a critical boundary. New view builders should depend on
`ViewBuildContext`, not on ad-hoc dictionaries.

### HTML Label Construction

`src/code_visualizer/rendering/html_labels.py`

- Provides small composable functions:
  - `html_table`
  - `html_row`
  - `html_cell`
  - `html_font`
  - `html_img`
  - `html_single_cell_table`

View modules should prefer these helpers over raw f-string table assembly.

### Visual Theme

`src/code_visualizer/rendering/theme.py`

- Owns shared colors, font family, font sizes, and recurring visual tokens
- Avoid adding new scattered hex literals in view/rendering files unless there
  is a good reason not to reuse the theme

## Graph Rendering Layers

There are two Graphviz-oriented rendering styles in the codebase.

### Structured view builders

- Build a `VisualGraph`
- Use `graph_view_builder.py`
- Render through `rendering/graphviz/graphviz_export.py`

This is the primary path for modern structured views.

### Standalone graphviz helpers

Located in `src/code_visualizer/rendering/graphviz/`

Examples:

- `array_graphviz.py`
- `table_graphviz.py`
- `linked_list_graphviz.py`
- `hash_table_graphviz.py`

These are smaller focused renderers and remain valid, but they should still use
shared theme and HTML helper infrastructure.

## Testing Structure

Tests mirror the source tree:

- `tests/api/`
- `tests/builders/`
- `tests/converters/`
- `tests/ir/`
- `tests/rendering/graphviz/`
- `tests/tracing/`
- `tests/utils/detection/`
- `tests/utils/type_patterns/`
- `tests/views/`
- `tests/views/node_views/`

Rule:

- new source module -> corresponding test module in the mirrored test subtree

## Public API vs Internal API

### Public

Keep stable:

- `visualize`
- `trace_algorithm`
- `visualize_algorithm`
- `build_browser_manifest`
- `build_browser_manifest_payload`
- `visualize_algorithm_manifest`
- `visualize_algorithm_manifest_payload`
- `ViewKind`
- `VisualizerConfig`
- `default_visualizer_config`

### Internal

Everything else should be treated as internal implementation detail unless it is
explicitly re-exported from a package `__init__.py`.

## What To Avoid Going Forward

- Reintroducing root-level shim modules
- New catch-all files like `common.py`, `helpers.py`, or `utils.py`
- Passing untyped dict bags across module boundaries
- Duplicating view-selection logic in multiple places
- Adding new raw HTML table strings where `html_labels.py` is sufficient
- Embedding browser-specific payload logic into tracing or rendering layers

## Current Improvement Frontier

The major architecture work is complete. Remaining work is refinement rather
than redesign:

- continue migrating any remaining raw HTML snippets to helper-based builders
- keep consolidating recurring visual constants into `theme.py`
- maintain strict separation between browser adapters and core Python logic
- keep tests aligned with new modules as the codebase evolves
