.PHONY: help install init test lint format type-check clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Average Price Calculator - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies with poetry
	poetry install --no-root

project-init: install pre-commit ## Initialize project (install dependencies and pre-commit)
	@echo "Project initialized successfully!"

pre-commit: ## Install pre-commit hooks
	poetry run pre-commit install

test: ## Run tests with pytest and coverage
	poetry run pytest -v --cov=average_price_calculator --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage (faster)
	poetry run pytest -v

lint: ## Run linters (ruff)
	poetry run ruff check .
	poetry run ruff format --check .

format: ## Format code with black and ruff
	poetry run black .
	poetry run ruff format .

type-check: ## Run type checker (mypy)
	poetry run mypy average_price_calculator tests streamlit_app.py

check-all: lint type-check test ## Run all checks (lint, type-check, test)

clean: ## Clean temporary files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf htmlcov dist build *.egg-info .coverage

run-cli: ## Run CLI with example
	poetry run avg-price-calc example

run-cli-calc: ## Run CLI calculation with default values
	poetry run avg-price-calc calculate --initial-qty 4.37562 --initial-price 3.602 --new-qty 2.93867 --new-price 2.11

run-streamlit: ## Run Streamlit web application
	streamlit run streamlit_app.py

build: ## Build package
	poetry build

publish-test: ## Publish to TestPyPI
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

publish: ## Publish to PyPI
	poetry publish