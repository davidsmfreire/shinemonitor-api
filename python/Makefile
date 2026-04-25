dev-setup:
	uv sync --all-groups
	uv run pre-commit install

build:
	uv build

test:
	uv run pytest tests/

codegen:
	uv run --with pyyaml python ../scripts/codegen.py

lock:
	uv lock
