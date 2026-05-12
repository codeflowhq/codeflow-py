from code_visualizer.rendering.graphviz.hash_table_graphviz import (
    render_graphviz_hash_table,
)


def test_render_graphviz_hash_table_returns_digraph() -> None:
    dot = render_graphviz_hash_table([[{"id": 1}], []], title="hash")

    assert "digraph" in dot
    assert "buckets=2" in dot
