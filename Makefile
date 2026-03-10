########################
# Variables

MEMDB := "file:memdb1?mode=memory&cache=shared"

########################
# Setup

submodule:
	git submodule init; git submodule update

########################
# Django Project

help:
	@echo "Available commands:"
	@echo "  submodule"
	@echo "  sync"
	@echo "  run-debug"
	@echo "  run"
	@echo "  migrate"
	@echo "  test-django"
	@echo "  test-django-fast"
	@echo "  lint"
	@echo "  lint-check"
	@echo "  type-check"
	@echo "  verify"

sync:
	uv sync --extra dev

run-debug:
	DEBUG=True uv run python manage.py runserver 0.0.0.0:8000

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver 0.0.0.0:8000

test-django:
	DEBUG=True uv run python manage.py test apps

test-django-fast:
	DEBUG=True DATABASE_URL=$(MEMDB) USE_FAST_HASHER=True uv run python manage.py test apps

lint:
	uv run ruff check --fix; uv run ruff format

lint-check:
	uv run ruff check --no-fix && uv run ruff format --check

type-check:
	uv run ty check

verify:
	make lint-check && make type-check && make test-django-fast
