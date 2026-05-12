from code_visualizer.rendering.graphviz.matrix_graphviz import render_graphviz_matrix


def test_render_graphviz_matrix_returns_digraph() -> None:
    dot = render_graphviz_matrix([[1, 2], [3, 4]], title="data")

    assert "digraph" in dot
    assert "matrix" in dot
