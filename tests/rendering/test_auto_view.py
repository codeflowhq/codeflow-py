from code_visualizer.rendering.auto_view import choose_view
from code_visualizer.view_types import ViewKind


def test_choose_view_prefers_table_for_plain_dict() -> None:
    assert choose_view({"a": 1}) is ViewKind.TABLE
