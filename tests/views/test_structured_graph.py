from __future__ import annotations

import pytest

from code_visualizer.shared.models import EdgeKind
from code_visualizer.shared.view_kinds import ViewKind
from code_visualizer.views.dispatcher import build_graph_view
from code_visualizer.views.graph_view import (
    _extract_graph_data,
    _graph_data_from_mapping,
)


def test_graph_data_from_mapping_supports_multiple_shapes() -> None:
    mapped = _graph_data_from_mapping(
        {
            "nodes": [{"id": "A", "value": 1}, ("B", 2)],
            "edges": [{"source": "A", "target": "B", "label": "ab"}, ("B", "C", "bc")],
            "directed": False,
        }
    )

    assert mapped is not None
    nodes, edges, directed = mapped
    assert ("A", 1) in nodes
    assert ("B", 2) in nodes
    assert ("A", "B", "ab") in edges
    assert directed is False


def test_extract_graph_data_supports_networkx_when_available() -> None:
    nx = pytest.importorskip("networkx")
    graph = nx.Graph()
    graph.add_node("A", label="Alpha")
    graph.add_edge("A", "B", weight=3)

    data = _extract_graph_data(graph)

    assert data is not None
    nodes, edges, directed = data
    assert ("A", "Alpha") in nodes
    assert ("A", "B", 3) in edges
    assert directed is False


def test_build_graph_view_entry_renders_directed_and_undirected_graphs() -> None:
    _, graph = build_graph_view(
        {"nodes": ["A", "B"], "edges": [("A", "B", "ab")], "directed": False},
        "graph",
        ViewKind.GRAPH,
        2,
        item_limit=5,
    )

    labels = [edge.label for edge in graph.edges if edge.type is EdgeKind.LINK]
    assert "ab" in labels
    undirected_edges = [edge for edge in graph.edges if edge.type is EdgeKind.LINK]
    assert undirected_edges[0].meta["edge_attrs"]["dir"] == "none"


def test_build_graph_view_rejects_invalid_input() -> None:
    with pytest.raises(TypeError):
        build_graph_view([1, 2, 3], "graph", ViewKind.GRAPH, 2, item_limit=5)
