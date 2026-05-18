from pathlib import Path

from code_visualizer.renderers.graphviz.image_renderer import render_graphviz_image


def test_render_graphviz_image_uses_local_path() -> None:
    image_path = Path("demo/outputs/avatar.png")
    dot = render_graphviz_image(str(image_path), title="image")

    assert "digraph" in dot
    assert "image_value" in dot
