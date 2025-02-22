-include env.sh
export

cur-dir := $(shell pwd)
base-dir := $(shell basename $(cur-dir))

help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

generate-requirements-txt: ## Generate a requirements.txt from pyproject.toml. Specify deps=<opt-deps> for specific optional dependencies. Specify output-file=<file.txt> from specific output file.
	@if [ -z $(deps) ]; then \
		pip-compile \
			--output-file=requirements/requirements.txt \
			--verbose \
			pyproject.toml; \
	else \
		pip-compile \
			--extra=$(deps) \
			--output-file=requirements/requirements-$(deps).txt \
			--verbose \
			pyproject.toml; \
		sed -i '/xrcs\[[^]]*\] @ file/,+1d' requirements/requirements-$(deps).txt; \
	fi

setup-venv: ## Set up local environment for Python development on pipelines
	@python -m venv .venv && \
	. .venv/bin/activate && \
	pip install --upgrade pip setuptools setuptools-scm && \
	pip install -r requirements/requirements-all.txt

pre-commit-install: ## Install pre-commit hooks
	@. .venv/bin/activate && \
	pre-commit install --install-hooks

pre-commit: ## Runs the pre-commit checks over entire repo
	@. .venv/bin/activate && \
	pre-commit run --all-files --color=always

ruff: ## Runs ruff linting and formatting
	@. .venv/bin/activate && \
	ruff check --fix && \
	ruff format

run: ## Run application.
	@. .venv/bin/activate && \
	python -m src.main

run-debug: ## Run application with debug mode enabled.
	@. .venv/bin/activate && \
	python -m src.main -d

serve-local-docs: ## Serve documentation locally
	@. .venv/bin/activate && \
	mkdocs serve

build-docs: ## Build documentation
	@. .venv/bin/activate && \
	mkdocs build
