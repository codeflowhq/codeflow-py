from code_visualizer.views.node_views.heap_payload import build_heap_tree_payload


def test_build_heap_tree_payload_returns_none_for_empty_heap() -> None:
    assert build_heap_tree_payload([], 5) is None


def test_build_heap_tree_payload_builds_binary_tree_shape() -> None:
    payload = build_heap_tree_payload([10, 6, 8, 3, 4], 5)

    assert payload == {
        "label": 10,
        "children": [
            {
                "label": 6,
                "children": [
                    {"label": 3, "children": []},
                    {"label": 4, "children": []},
                ],
            },
            {"label": 8, "children": []},
        ],
    }


def test_build_heap_tree_payload_honors_item_limit() -> None:
    payload = build_heap_tree_payload([10, 6, 8, 3, 4], 3)

    assert payload == {
        "label": 10,
        "children": [
            {"label": 6, "children": []},
            {"label": 8, "children": []},
        ],
    }
