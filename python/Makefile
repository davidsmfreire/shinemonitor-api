dev-setup:
	uv sync --all-groups
	uv run pre-commit install

build:
	uv build

test:
	uv run pytest tests/

lock:
	uv lock
