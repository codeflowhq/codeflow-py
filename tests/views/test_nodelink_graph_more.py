from __future__ import annotations

import pytest

from code_visualizer.shared.models import EdgeKind, NodeKind
from code_visualizer.views.nodelink_graph import ExtractOptions
from code_visualizer.views.nodelink_graph import (
    NodelinkGraphBuilder as VisualIRExtractor,
)


class _Attrs:
    def __init__(self) -> None:
        self.left = [1, 2]
        self.right = {"a": 1, "b": 2}
        self.extra = "hello"


class _NoDict:
    __slots__ = ()


def test_scalar_labels_respect_repr_and_pretty_options() -> None:
    pretty = VisualIRExtractor(ExtractOptions(max_str_len=6, string_style="pretty"))
    repr_style = VisualIRExtractor(ExtractOptions(max_str_len=6, string_style="repr"))

    pretty_graph = pretty.extract("a\nlong\ntext", name="data")
    repr_graph = repr_style.extract("abcdefghi")

    assert any("⏎" in node.label for node in pretty_graph.nodes.values())
    assert any("'abc..." in node.label for node in repr_graph.nodes.values())


def test_extract_handles_empty_and_truncated_containers() -> None:
    extractor = VisualIRExtractor(ExtractOptions(max_items=1, max_depth=5))

    dict_graph = extractor.extract({"a": 1, "b": 2})
    assert any(node.type is NodeKind.ENTRY for node in dict_graph.nodes.values())
    assert any(node.label == "… (+1 entries)" for node in dict_graph.nodes.values())

    list_graph = extractor.extract([1, 2])
    assert any(
        edge.type is EdgeKind.INDEX and edge.label == "0" for edge in list_graph.edges
    )
    assert any(node.label == "… (+1 items)" for node in list_graph.nodes.values())

    empty_graph = extractor.extract(set())
    assert any(node.meta.get("empty") is True for node in empty_graph.nodes.values())


def test_extract_handles_object_attrs_and_attr_limit() -> None:
    extractor = VisualIRExtractor(
        ExtractOptions(max_items=2, include_object_attrs=True)
    )
    graph = extractor.extract(_Attrs(), name="obj")

    assert any(
        edge.type is EdgeKind.ATTR and edge.label == "left" for edge in graph.edges
    )
    assert any(node.label == "… (+1 attrs)" for node in graph.nodes.values())


def test_extract_skips_attrs_when_disabled_or_no_dict() -> None:
    disabled = VisualIRExtractor(ExtractOptions(include_object_attrs=False)).extract(
        _Attrs()
    )
    assert not any(edge.type is EdgeKind.ATTR for edge in disabled.edges)

    nodict = VisualIRExtractor().extract(_NoDict())
    assert not any(edge.type is EdgeKind.ATTR for edge in nodict.edges)


def test_extract_networkx_graph_when_available() -> None:
    nx = pytest.importorskip("networkx")
    graph = nx.Graph()
    graph.add_edge("A", "B")

    visual = VisualIRExtractor().extract(graph, name="g")

    assert any(node.meta.get("graph") == "networkx" for node in visual.nodes.values())
    assert any(
        edge.type is EdgeKind.REF and edge.label == "edge" for edge in visual.edges
    )
