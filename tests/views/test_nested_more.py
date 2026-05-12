from __future__ import annotations

from itertools import count

import pytest

from code_visualizer.models import NodeKind, VisualGraph, VisualNode
from code_visualizer.view_types import ViewKind
from code_visualizer.views.context import ViewBuildContext
from code_visualizer.views.nested import make_nested_renderer, render_inline_child_view


def _runtime() -> ViewBuildContext:
    return ViewBuildContext(
        graph=VisualGraph(),
        item_limit=5,
        coerce=lambda value: value,
        resolver=None,
        focus_path=None,
        counter=count(1),
        show_titles=False,
    )


def test_render_inline_child_view_returns_html_label_for_single_html_node(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from code_visualizer import graph_view_builder

    def _fake_build(*args: object, **kwargs: object) -> tuple[str, VisualGraph]:
        graph = VisualGraph()
        graph.add_node(
            VisualNode("root", NodeKind.OBJECT, "<b>x</b>", {"html_label": True})
        )
        return "root", graph

    monkeypatch.setattr(graph_view_builder, "build_graph_view", _fake_build)
    assert (
        render_inline_child_view(_runtime(), {"a": 1}, "slot", ViewKind.TABLE, 2)
        == "<b>x</b>"
    )


def test_render_inline_child_view_returns_none_on_build_or_render_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from code_visualizer import graph_view_builder
    from code_visualizer.views import nested

    monkeypatch.setattr(
        graph_view_builder,
        "build_graph_view",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("boom")),
    )
    assert (
        render_inline_child_view(_runtime(), [1, 2], "slot", ViewKind.ARRAY_CELLS, 2)
        is None
    )

    def _graph_build(*args: object, **kwargs: object) -> tuple[str, VisualGraph]:
        graph = VisualGraph()
        graph.add_node(VisualNode("root", NodeKind.OBJECT, "plain", {}))
        return "root", graph

    monkeypatch.setattr(graph_view_builder, "build_graph_view", _graph_build)
    monkeypatch.setattr(
        nested, "_render_dot_to_image", lambda dot_source, fmt="png": None
    )
    assert (
        render_inline_child_view(_runtime(), [1, 2], "slot", ViewKind.ARRAY_CELLS, 2)
        is None
    )


def test_make_nested_renderer_returns_none_or_adds_edge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = _runtime()
    parent_id = "parent"
    runtime.graph.add_node(VisualNode(parent_id, NodeKind.OBJECT, "parent", {}))
    renderer = make_nested_renderer(runtime, parent_id, "p0", "slot")

    assert renderer(123, "ignored", 0) is None

    from code_visualizer import graph_view_builder
    from code_visualizer.views import nested

    monkeypatch.setattr(
        nested, "render_inline_child_view", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        nested, "select_nested_view", lambda *args, **kwargs: ViewKind.TABLE
    )
    monkeypatch.setattr(
        graph_view_builder,
        "_build_view",
        lambda runtime, value, name, view, depth: "child",
    )

    result = renderer({"a": 1}, "ignored", 2)
    assert result == ""
    assert runtime.graph.edges[-1].src == "parent"
    assert runtime.graph.edges[-1].meta["tailport"] == "p0"
