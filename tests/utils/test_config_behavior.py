from __future__ import annotations

from code_visualizer.config import (
    VisualizerConfig,
    default_visualizer_config,
    merge_override_map,
)
from code_visualizer.view_types import ViewKind


def test_visualizer_config_output_and_step_limit_precedence() -> None:
    config = VisualizerConfig(output_format="png", trace_step_limit_default=7)
    config.trace_step_limit_map["data"] = -3

    assert config.ensure_output_format("jpeg") == "jpg"
    assert config.ensure_output_format("gif") == "png"
    assert config.step_limit_for("data", override=9) == 0
    assert config.step_limit_for("other", override=9) == 9
    assert config.step_limit_for("missing") == 7


def test_visualizer_config_copy_and_with_converters_preserve_value_semantics() -> None:
    config = default_visualizer_config()
    copied = config.copy()
    copied.view_name_map["data"] = ViewKind.TABLE

    assert "data" not in config.view_name_map

    same = config.with_converters()
    assert same is config

    updated = config.with_converters(lambda value: (True, value), prepend=True)
    assert updated is not config
    assert (
        len(updated.converter_pipeline.converters)
        == len(config.converter_pipeline.converters) + 1
    )


def test_merge_override_map_normalizes_string_views() -> None:
    merged = merge_override_map({list: ViewKind.ARRAY_CELLS}, {"data": "table"})

    assert merged[list] is ViewKind.ARRAY_CELLS
    assert merged["data"] is ViewKind.TABLE
