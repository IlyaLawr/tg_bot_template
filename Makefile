.PHONY: init up test down


init:
	@test -f .env || cp .env.example .env
	@test -f .env.test || cp .env.test.example .env.test
	@if [ ! -d .venv ]; then \
		python3 -m venv .venv; \
	fi; \
	if ! .venv/bin/python -m pip --version >/dev/null 2>&1; then \
		.venv/bin/python -m ensurepip; \
	fi; \
	if ! .venv/bin/python -m uv --version >/dev/null 2>&1; then \
		.venv/bin/python -m pip install uv; \
	fi; \
	.venv/bin/python -m uv sync --inexact


up: init
	docker compose up --build


test-services:
	@if docker ps -a --format "table {{.Names}}" | grep -q "^postgres_tg_bot$$"; then \
		if docker ps --format "table {{.Names}}" | grep -q "^postgres_tg_bot$$"; then \
			:; \
		else \
			docker start postgres_tg_bot; \
		fi; \
	else \
		docker compose up -d postgres; \
	fi

	@if docker ps -a --format "table {{.Names}}" | grep -q "^redis_tg_bot$$"; then \
		if docker ps --format "table {{.Names}}" | grep -q "^redis_tg_bot$$"; then \
			:; \
		else \
			docker start redis_tg_bot; \
		fi; \
	else \
		docker compose up -d redis; \
	fi

	@sleep 3


test: init test-services
	@if command -v uv >/dev/null 2>&1; then \
		cd test/use_case && uv run pytest; \
	else \
		cd test/use_case && ../../.venv/bin/uv run pytest; \
	fi


down:
	docker compose down
