from code_visualizer.ir.extractor import VisualIRExtractor
from code_visualizer.ir.options import ExtractOptions
from code_visualizer.models import NodeKind


class _Node:
    def __init__(self, value: int, next_node: "_Node | None" = None) -> None:
        self.value = value
        self.next = next_node


def test_visual_ir_extractor_adds_anchor_for_named_root() -> None:
    graph = VisualIRExtractor().extract([1, 2, 3], name="data")

    assert graph.anchors[0].name == "data"
    assert graph.anchors[0].node_id in graph.nodes


def test_visual_ir_extractor_respects_depth_limit() -> None:
    extractor = VisualIRExtractor(ExtractOptions(max_depth=1, max_items=5))

    graph = extractor.extract({"outer": {"inner": {"value": 3}}}, name="data")

    assert any(node.type is NodeKind.ELLIPSIS and "max depth" in node.label for node in graph.nodes.values())


def test_visual_ir_extractor_deduplicates_shared_objects() -> None:
    shared = [1, 2]
    graph = VisualIRExtractor().extract({"left": shared, "right": shared}, name="data")

    list_nodes = [node for node in graph.nodes.values() if node.type is NodeKind.LIST]
    assert len(list_nodes) == 1
