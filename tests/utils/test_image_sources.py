from __future__ import annotations

import base64
from pathlib import Path

import pytest

from code_visualizer.utils import image_sources
from code_visualizer.utils.image_sources import (
    VisualizationImageError,
    _detect_image_source,
    _image_html,
    _is_image_path,
    _looks_like_image_candidate,
    _materialize_data_uri,
    _render_dot_to_image,
)

PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wn8nS4AAAAASUVORK5CYII="
)


class _FakeSource:
    def __init__(self, source: str) -> None:
        self.source = source
        self.format = "png"

    def render(self, filename: str, directory: str, cleanup: bool) -> str:
        target = Path(directory) / f"{filename}.{self.format}"
        target.write_bytes(PNG_BYTES)
        return str(target)



def test_image_candidate_detection_handles_paths_urls_and_data_uri() -> None:
    assert _is_image_path("avatar.PNG")
    assert _looks_like_image_candidate("https://example.com/a.jpg")
    assert _looks_like_image_candidate("data:image/png;base64,AAAA")
    assert not _looks_like_image_candidate("https://example.com/a")
    assert not _looks_like_image_candidate(123)



def test_materialize_data_uri_and_detect_local_path(tmp_path: Path) -> None:
    data_uri = "data:image/png;base64," + base64.b64encode(PNG_BYTES).decode("ascii")
    cached = _materialize_data_uri(data_uri)
    assert cached is not None and Path(cached).exists()

    image_path = tmp_path / "avatar.png"
    image_path.write_bytes(PNG_BYTES)
    assert _detect_image_source(str(image_path)) == str(image_path.resolve())
    assert _detect_image_source(image_path) == str(image_path.resolve())



def test_detect_image_source_strict_errors_and_remote_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(VisualizationImageError):
        _detect_image_source("", strict=True)
    with pytest.raises(VisualizationImageError):
        _detect_image_source("missing.png", strict=True)
    with pytest.raises(VisualizationImageError):
        _detect_image_source("notes.txt", strict=True)

    monkeypatch.setattr(image_sources, "_is_pyodide_runtime", lambda: False)
    monkeypatch.setattr(image_sources, "_download_remote_image", lambda url: (None, "blocked"))
    assert _detect_image_source("https://example.com/a.png", strict=True) == "https://example.com/a.png"
    assert _detect_image_source("https://example.com/a.png") is None



def test_image_html_and_dot_render(monkeypatch: pytest.MonkeyPatch) -> None:
    html = _image_html('https://example.com/a.png?x="1"')
    assert "&quot;1&quot;" in html

    monkeypatch.setattr(image_sources, "Source", _FakeSource)
    rendered = _render_dot_to_image("digraph { a -> b }", fmt="svg")
    assert rendered is not None
    assert rendered.endswith(".svg")

    rendered_default = _render_dot_to_image("digraph { a -> b }", fmt="bmp")
    assert rendered_default is not None
    assert rendered_default.endswith(".png")
