from code_visualizer.rendering.graphviz.scalar_graphviz import render_graphviz_scalar


def test_render_graphviz_scalar_returns_digraph() -> None:
    dot = render_graphviz_scalar(42, title="value")

    assert "digraph" in dot
    assert "42" in dot
