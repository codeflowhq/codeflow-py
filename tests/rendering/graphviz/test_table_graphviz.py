from code_visualizer.rendering.graphviz.table_graphviz import render_graphviz_table


def test_render_graphviz_table_returns_digraph() -> None:
    dot = render_graphviz_table({"a": 1}, title="data")

    assert "digraph" in dot
    assert "Key" in dot
    assert "Value" in dot
