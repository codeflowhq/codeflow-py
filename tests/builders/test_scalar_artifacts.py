from code_visualizer.builders.scalar_artifacts import render_scalar_artifact
from code_visualizer.models import ArtifactKind


def test_render_scalar_artifact_returns_graphviz_output() -> None:
    artifact = render_scalar_artifact("value", 42, "LR", show_titles=True)

    assert artifact.kind is ArtifactKind.GRAPHVIZ
    assert "digraph" in artifact.content
    assert artifact.title == "value: value"
