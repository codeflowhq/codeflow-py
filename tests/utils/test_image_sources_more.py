from __future__ import annotations

import base64
from pathlib import Path

import pytest

from code_visualizer.utils import image_sources
from code_visualizer.utils.image_sources import (
    VisualizationImageError,
    _assert_ascii_path,
    _download_remote_image,
    _is_pyodide_runtime,
    _materialize_matplotlib_image,
    _materialize_pil_image,
    _remote_url_suffix,
    _write_cached_image,
)

PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wn8nS4AAAAASUVORK5CYII="
)


class _FailResponse:
    def __enter__(self):
        raise OSError("blocked")

    def __exit__(self, exc_type, exc, tb):
        return False


class _SuccessResponse:
    def __init__(self, data: bytes, content_type: str) -> None:
        self._data = data
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self._data


def test_remote_helpers_and_ascii_path(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _remote_url_suffix("https://example.com/a.jpg?x=1") == ".jpg"
    assert _remote_url_suffix("https://example.com/a") == ""

    monkeypatch.setattr(
        image_sources, "urlopen", lambda request, timeout=5: _FailResponse()
    )
    cached, error = _download_remote_image("https://example.com/a.png")
    assert cached is None
    assert "blocked" in (error or "")

    monkeypatch.setattr(
        image_sources,
        "urlopen",
        lambda request, timeout=5: _SuccessResponse(PNG_BYTES, "image/png"),
    )
    cached, error = _download_remote_image("https://example.com/a")
    assert error is None
    assert cached is not None and Path(cached).exists()

    with pytest.raises(ValueError):
        _assert_ascii_path(Path.cwd() / "图像.png")


def test_runtime_and_cache_write_helpers() -> None:
    path = _write_cached_image(PNG_BYTES, ".png")
    assert Path(path).exists()
    assert _is_pyodide_runtime() is False


def test_materialize_matplotlib_and_pil_helpers() -> None:
    pytest.importorskip("matplotlib")
    pyplot = pytest.importorskip("matplotlib.pyplot")
    fig = pyplot.figure()
    fig.add_subplot(111).plot([0, 1], [0, 1])
    try:
        fig_path = _materialize_matplotlib_image(fig)
        assert fig_path is not None and Path(fig_path).exists()
    finally:
        pyplot.close(fig)

    pil = pytest.importorskip("PIL.Image")
    img = pil.new("RGB", (1, 1), color=(255, 0, 0))
    img_path = _materialize_pil_image(img)
    assert img_path is not None and Path(img_path).exists()

    with pytest.raises(VisualizationImageError):
        image_sources._detect_image_source(object(), strict=True)
