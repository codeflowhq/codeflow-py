from dataclasses import dataclass

from code_visualizer.rendering.graphviz.linked_list_graphviz import (
    render_graphviz_linked_list,
)


@dataclass
class Node:
    val: int
    next: "Node | None" = None


def test_render_graphviz_linked_list_returns_digraph() -> None:
    head = Node(1, Node(2))
    dot = render_graphviz_linked_list(head, title="list")

    assert "digraph" in dot
    assert "None" in dot
