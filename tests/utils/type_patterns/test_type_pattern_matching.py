from code_visualizer.utils.type_patterns.matching import (
    _compile_type_pattern,
    _match_type_pattern_override,
)
from code_visualizer.utils.type_patterns.naming import _match_named_override
from code_visualizer.view_types import ViewKind


class _Tree:
    def __init__(self, value: str, children: list[object] | None = None) -> None:
        self.value = value
        self.children = children or []


def test_compile_type_pattern_parses_nested_generics() -> None:
    pattern = _compile_type_pattern("dict[str, list[number]]")

    assert pattern.kind == "dict"
    assert pattern.args[0].kind == "str"
    assert pattern.args[1].kind == "list"
    assert pattern.args[1].args[0].kind == "number"


def test_match_type_pattern_override_matches_tree_pattern() -> None:
    view = _match_type_pattern_override(_Tree("root"), {"tree": ViewKind.TREE})

    assert view is ViewKind.TREE


def test_match_named_override_ignores_spacing() -> None:
    view = _match_named_override('data["users"]', {' data [ "users" ] ': ViewKind.TABLE})

    assert view is ViewKind.TABLE
