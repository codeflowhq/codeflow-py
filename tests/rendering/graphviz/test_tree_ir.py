from dataclasses import dataclass

from code_visualizer.rendering.graphviz.tree_ir import build_tree


@dataclass
class Node:
    val: int
    left: "Node | None" = None
    right: "Node | None" = None


def test_build_tree_returns_root_and_graph() -> None:
    root = Node(1, left=Node(2), right=Node(3))

    root_id, graph = build_tree(root)

    assert root_id in graph.nodes
    assert len(graph.edges) == 2


def test_build_tree_uses_subtree_structure_for_stable_ids() -> None:
    before = {
        "label": "A",
        "children": [
            {"label": "B", "children": []},
            {"label": "C", "children": [{"label": "D", "children": []}]},
        ],
    }
    after = {
        "label": "B",
        "children": [
            {"label": "B", "children": []},
            {"label": "A", "children": [{"label": "D", "children": []}]},
        ],
    }

    before_root, before_graph = build_tree(before)
    after_root, after_graph = build_tree(after)

    assert before_root != after_root
    shared_ids = (set(before_graph.nodes) & set(after_graph.nodes)) - {"CUT"}
    assert shared_ids
