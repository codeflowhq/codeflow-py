from code_visualizer.models import NodeKind, VisualGraph, VisualNode
from code_visualizer.rendering.graphviz.graphviz_export import render_graphviz_node_link


def test_render_graphviz_node_link_returns_digraph_source() -> None:
    graph = VisualGraph()
    graph.add_node(VisualNode("n1", NodeKind.OBJECT, "hello"))

    dot = render_graphviz_node_link(graph)

    assert "digraph" in dot
    assert "hello" in dot
