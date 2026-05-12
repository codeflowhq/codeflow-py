from __future__ import annotations

import pytest

from code_visualizer.rendering.graphviz.bar_graphviz import render_graphviz_bar


def test_render_graphviz_bar_handles_empty_and_truncation() -> None:
    empty = render_graphviz_bar([], title="data")
    assert "∅" in empty

    dot = render_graphviz_bar([1, -2, 3], title="data", max_items=2)
    assert "cv-data-bar-0" in dot
    assert "cv-data-bar-1" in dot
    assert ">…<" in dot or "…" in dot



def test_render_graphviz_bar_rejects_non_numeric_lists() -> None:
    with pytest.raises(TypeError):
        render_graphviz_bar([1, "x"])
