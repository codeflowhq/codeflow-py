from collections import deque

from code_visualizer.converters.defaults import (
    apply_converter_pipeline,
    deque_converter,
    identity_converter,
)
from code_visualizer.converters.pipeline import ConverterPipeline


def test_deque_converter_converts_deque_to_list() -> None:
    handled, converted = deque_converter(deque([1, 2, 3]))

    assert handled is True
    assert converted == [1, 2, 3]


def test_converter_pipeline_returns_first_match() -> None:
    pipeline = ConverterPipeline((deque_converter, identity_converter))

    converted, handled = pipeline.coerce(deque([1]))

    assert handled is True
    assert converted == [1]


def test_apply_converter_pipeline_preserves_unhandled_values() -> None:
    converted, handled = apply_converter_pipeline(
        "x", (deque_converter, identity_converter)
    )

    assert handled is False
    assert converted == "x"
