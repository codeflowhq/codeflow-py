from code_visualizer.pipeline.resolver import choose_view
from code_visualizer.shared.view_kinds import ViewKind


def test_choose_view_prefers_table_for_plain_dict() -> None:
    assert choose_view({"a": 1}) is ViewKind.TABLE
