from code_visualizer.view_types import ViewKind, ensure_view_kind


def test_ensure_view_kind_accepts_legacy_aliases() -> None:
    assert ensure_view_kind("array_cells_node") is ViewKind.ARRAY_CELLS
    assert ensure_view_kind("matrix_node") is ViewKind.MATRIX
    assert ensure_view_kind("table_node") is ViewKind.TABLE
    assert ensure_view_kind("hash_table_node") is ViewKind.HASH_TABLE
    assert ensure_view_kind("linked_list_node") is ViewKind.LINKED_LIST
    assert ensure_view_kind("heap_dual_node") is ViewKind.HEAP_DUAL
    assert ensure_view_kind("bar_node") is ViewKind.BAR


def test_ensure_view_kind_keeps_canonical_values() -> None:
    assert ensure_view_kind(ViewKind.TREE) is ViewKind.TREE
    assert ensure_view_kind("graph") is ViewKind.GRAPH
