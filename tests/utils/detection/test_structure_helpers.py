from __future__ import annotations

import pytest

from code_visualizer.utils.detection.graph import (
    _looks_like_graph_mapping,
    _try_networkx_edges_nodes,
)
from code_visualizer.utils.detection.linked import (
    _collect_linked_list_labels,
    _hash_bucket_entries,
    _looks_like_hash_table,
)


class _Node:
    def __init__(self, value: int, next_node: _Node | None = None) -> None:
        self.value = value
        self.next = next_node



def test_looks_like_graph_mapping_accepts_common_edge_shapes() -> None:
    assert _looks_like_graph_mapping({"nodes": ["A"], "edges": [("A", "B")]})
    assert _looks_like_graph_mapping({"edges": [{"source": "A", "target": "B"}]})
    assert not _looks_like_graph_mapping({"edges": "A-B"})
    assert not _looks_like_graph_mapping({"nodes": ["A"]})



def test_try_networkx_edges_nodes_snapshots_graph_when_available() -> None:
    nx = pytest.importorskip("networkx")
    graph = nx.DiGraph()
    graph.add_node("A", color="blue")
    graph.add_edge("A", "B", weight=2)

    snapshot = _try_networkx_edges_nodes(graph)

    assert snapshot is not None
    nodes, edges, directed = snapshot
    assert nodes == [("A", {"color": "blue"}), ("B", {})]
    assert edges == [("A", "B", {"weight": 2})]
    assert directed is True



def test_collect_linked_list_labels_handles_cycles_and_missing_next() -> None:
    first = _Node(1)
    second = _Node(2)
    first.next = second
    second.next = first

    assert _collect_linked_list_labels(None, 3) == ([], False)
    assert _collect_linked_list_labels(123, 3) is None
    assert _collect_linked_list_labels(first, 5) == ([1, 2], True)



def test_looks_like_hash_table_accepts_bucket_shapes() -> None:
    linked_bucket = _Node(1, _Node(2))

    assert _looks_like_hash_table([None, {"a": 1}])
    assert _looks_like_hash_table([[], [("a", 1)]])
    assert _looks_like_hash_table([None, linked_bucket])
    assert not _looks_like_hash_table([1, 2, 3])



def test_hash_bucket_entries_handles_mapping_set_sequence_and_linked_list() -> None:
    linked_bucket = _Node(1, _Node(2, _Node(3)))

    assert _hash_bucket_entries({"a": 1}, 5) == (["a:1"], False)
    entries, truncated = _hash_bucket_entries({"b", "a"}, 5)
    assert entries == ["a", "b"]
    assert truncated is False
    assert _hash_bucket_entries([(1, 2), (3, 4)], 1) == ([(1, 2)], True)
    assert _hash_bucket_entries(linked_bucket, 2) == ([1, 2], True)
