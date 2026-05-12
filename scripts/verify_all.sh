#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_DIR="/Users/bbnb/sg/code_visualizer_web/web_app"

cd "$ROOT_DIR"
uv run pytest tests -q
uv run mypy src/code_visualizer
uv run ruff check src/code_visualizer tests
cd "$WEB_DIR"
npm run build
