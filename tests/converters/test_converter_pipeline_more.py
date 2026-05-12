from __future__ import annotations

from code_visualizer.converters.pipeline import ConverterPipeline


def _first(value: object) -> tuple[bool, object]:
    return (True, "first") if value == "x" else (False, value)


def _second(value: object) -> tuple[bool, object]:
    return True, "second"


def test_converter_pipeline_with_converters_supports_append_and_prepend() -> None:
    base = ConverterPipeline((_first,))

    appended = base.with_converters(_second)
    prepended = base.with_converters(_second, prepend=True)

    assert appended.coerce("x") == ("first", True)
    assert appended.coerce("y") == ("second", True)
    assert prepended.coerce("x") == ("second", True)


def test_converter_pipeline_extend_handles_empty_and_prepend() -> None:
    base = ConverterPipeline((_first,))

    assert base.extend([]) is base
    extended = base.extend([_second], prepend=True)
    assert extended.coerce("y") == ("second", True)
