from code_visualizer.renderers.graphviz.array_renderer import (
    render_graphviz_array_cells,
)


def test_render_graphviz_array_cells_returns_digraph() -> None:
    dot = render_graphviz_array_cells([1, 2, 3], title="data")

    assert "digraph" in dot
    assert "CELL 0" in dot
