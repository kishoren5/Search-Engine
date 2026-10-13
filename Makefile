.PHONY: install test lint format api

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

api:
	uvicorn search_engine.api.app:app --host 0.0.0.0 --port 8000
