from code_visualizer.shared.models import NodeKind, VisualGraph
from code_visualizer.views.node_views.hash_table_helpers import (
    configure_hash_table_graph,
    hash_bucket_head_node,
    hash_chain_node,
    hash_table_focus_indices,
)


def test_hash_table_focus_indices_extracts_bucket_and_item() -> None:
    assert hash_table_focus_indices("data[2][1]", "data") == (2, 1)
    assert hash_table_focus_indices("data[2]", "data") == (2, None)
    assert hash_table_focus_indices("other[2]", "data") == (None, None)


def test_configure_hash_table_graph_sets_title_when_enabled() -> None:
    graph = VisualGraph()

    configure_hash_table_graph(graph, "data", show_titles=True)

    assert graph.graph_attrs["rankdir"] == "TB"
    assert "data" in graph.graph_attrs["label"]


def test_hash_bucket_head_node_marks_focus_style() -> None:
    focused = hash_bucket_head_node("data", 1, is_focused=True)
    plain = hash_bucket_head_node("data", 1, is_focused=False)

    assert focused.type is NodeKind.OBJECT
    assert (
        focused.meta["node_attrs"]["penwidth"] != plain.meta["node_attrs"]["penwidth"]
    )


def test_hash_chain_node_marks_focus_style() -> None:
    focused = hash_chain_node("data", 0, 0, "x", chain_focus=True)
    plain = hash_chain_node("data", 0, 0, "x", chain_focus=False)

    assert focused.type is NodeKind.OBJECT
    assert focused.meta["node_attrs"]["color"] != plain.meta["node_attrs"]["color"]
