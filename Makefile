.PHONY: help setup install run test clean venv deps

# Project configuration
PROJECT_NAME = average-price-calculator
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
POETRY = $(VENV_DIR)/bin/poetry
VENV_ACTIVATE = . $(VENV_DIR)/bin/activate

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m # No Color

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "$(BLUE)$(PROJECT_NAME) - Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Usage:$(NC) make [target]"
	@echo ""
	@echo "$(YELLOW)Targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Main setup and run targets
setup: check-python venv deps ## First-time setup: Create venv and install dependencies
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  make run        # Run the Streamlit app"
	@echo "  make test       # Run tests"
	@echo "  source $(VENV_DIR)/bin/activate  # Activate virtual env manually"

run: check-venv ## Run Streamlit application
	@echo "$(BLUE)Starting Streamlit application...$(NC)"
	@echo "$(YELLOW)Opening browser at http://localhost:8501$(NC)"
	$(VENV_ACTIVATE) && streamlit run streamlit_app.py

# Virtual environment management
venv: ##  Create virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(BLUE)Creating virtual environment...$(NC)"; \
		python3 -m venv $(VENV_DIR); \
		echo "$(GREEN)✅ Virtual environment created at $(VENV_DIR)$(NC)"; \
	else \
		echo "$(YELLOW)Virtual environment already exists at $(VENV_DIR)$(NC)"; \
	fi

check-venv: ## Check if virtual environment exists
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Virtual environment not found!$(NC)"; \
		echo "Run 'make setup' first"; \
		exit 1; \
	fi

activate: ## Show activation command
	@echo "$(YELLOW)To activate virtual environment:$(NC)"
	@echo "  source $(VENV_DIR)/bin/activate"
	@echo ""
	@echo "$(YELLOW)To deactivate:$(NC)"
	@echo "  deactivate"

deactivate: ## Deactivate virtual environment
	@echo "$(YELLOW)Deactivating virtual environment...$(NC)"
	deactivate 2>/dev/null || true

# Dependencies
deps: check-venv ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(VENV_ACTIVATE) && pip install --upgrade pip
	$(VENV_ACTIVATE) && pip install poetry
	$(VENV_ACTIVATE) && poetry install
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

install: deps ## Alias for deps
	@echo "$(GREEN)✅ Installation complete$(NC)"

# Development commands
test: check-venv ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	$(VENV_ACTIVATE) && python -m pytest -v

lint: check-venv ##  Run linter
	@echo "$(BLUE)Running linter...$(NC)"
	$(VENV_ACTIVATE) && python -m ruff check .

format: check-venv ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	$(VENV_ACTIVATE) && python -m black .

check-all: lint test ##  Run all checks

# CLI commands
run-cli: check-venv ## Run CLI tool
	@echo "$(BLUE)Running CLI tool...$(NC)"
	$(VENV_ACTIVATE) && python -m average_price_calculator.cli

run-cli-example: check-venv ## Run CLI with example
	$(VENV_ACTIVATE) && avg-price-calc example

run-cli-calc: check-venv ##  Run CLI calculation
	$(VENV_ACTIVATE) && avg-price-calc calculate --initial-qty 4.37562 --initial-price 3.602 --new-qty 2.93867 --new-price 2.11

# Project management
clean: ## Clean project files
	@echo "$(BLUE)Cleaning project...$(NC)"
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov *.egg-info dist build
	@echo "$(GREEN)✅ Project cleaned$(NC)"

reset: clean setup ## Clean and re-setup project
	@echo "$(GREEN)✅ Project reset complete$(NC)"

info: ## Show project information
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "  Name: $(PROJECT_NAME)"
	@echo "  Python: $$(python3 --version 2>/dev/null || echo 'Not found')"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "  Virtual env: $(VENV_DIR)"; \
		echo "  Python (venv): $$($(PYTHON) --version 2>/dev/null)"; \
	else \
		echo "  Virtual env: Not created"; \
	fi
	@if [ -f "pyproject.toml" ]; then \
		echo "  Poetry: Available"; \
	else \
		echo "  Poetry: pyproject.toml not found"; \
	fi

# System checks
check-python: ##  Check Python installation
	@echo "$(BLUE)Checking Python...$(NC)"
	@if command -v python3 >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Python3 found: $$(python3 --version)$(NC)"; \
	else \
		echo "$(RED)❌ Python3 not found!$(NC)"; \
		echo "Please install Python 3.8 or higher"; \
		exit 1; \
	fi

# Auto-activation for all targets (except setup and clean)
ifneq (,$(findstring $(MAKECMDGOALS),setup clean reset))
    # Don't auto-activate for setup/clean
else
    ifeq (,$(VIRTUAL_ENV))
        ifneq (,$(wildcard $(VENV_DIR)))
            AUTO_ACTIVATE = 1
        endif
    endif
endif

# Auto-activation logic
ifdef AUTO_ACTIVATE
    .SILENT: $(MAKECMDGOALS)
    $(MAKECMDGOALS): check-venv
	@echo "$(YELLOW) Auto-activating virtual environment...$(NC)"
	$(VENV_ACTIVATE) && $(MAKE) $(MAKECMDGOALS)
endif

# Create required files if they don't exist
streamlit_app.py:
	@if [ ! -f "streamlit_app.py" ]; then \
		echo "$(YELLOW)Creating streamlit_app.py...$(NC)"; \
		echo 'import streamlit as st' > streamlit_app.py; \
		echo '' >> streamlit_app.py; \
		echo 'st.title("Average Price Calculator")' >> streamlit_app.py; \
		echo 'st.write("Welcome to the Average Price Calculator!")' >> streamlit_app.py; \
		echo 'st.write("Run \`make setup\` first to install dependencies.")' >> streamlit_app.py; \
		echo "$(GREEN)✅ Created streamlit_app.py$(NC)"; \
	fi

# Default streamlit file creation before run
run: streamlit_app.py