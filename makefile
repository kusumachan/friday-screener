# Detect OS
ifeq ($(OS),Windows_NT)
	VENV_PYTHON := venv/Scripts/python.exe
	VENV_PIP := venv/Scripts/pip.exe
	RUFF := venv/Scripts/ruff.exe
else
	VENV_PYTHON := venv/bin/python
	VENV_PIP := venv/bin/pip
	RUFF := venv/bin/ruff
endif

# Config
APP_DIR := src
APP_MODULE := src.main

# Targets
.PHONY: help venv install run test test-cov format lint build build/exe build/dist clean/all clean/cache clean/build

help:
	@echo "🛠️  Makefile commands:"
	@echo "  🐍 make venv          - Create virtual environment"
	@echo "  📦 make install       - Install dependencies"
	@echo "  🚀 make run           - Run the CLI application"
	@echo "  🧪 make test          - Run tests with pytest"
	@echo "  📊 make test-cov      - Run tests with coverage report"
	@echo "  🎨 make format        - Format code with Black and auto fix with Ruff"
	@echo "  🧹 make lint          - Lint code with Ruff"
	@echo "  🔨 make build         - Build executable with PyInstaller"
	@echo "  📦 make build/exe     - Build single executable file"
	@echo "  📂 make build/dist    - Build with dependencies folder"
	@echo "  🧼 make clean/all     - Remove venv and all caches"
	@echo "  🗑️  make clean/cache   - Remove Python caches only"
	@echo "  🧹 make clean/build   - Remove build artifacts"

venv:
ifeq ($(OS),Windows_NT)
	@if not exist "venv" ( \
		echo 🔧 Creating virtual environment... && \
		python3 -m venv venv \
	) else ( \
		echo ✅ Virtual environment already exists. \
	)
else
	@if [ ! -d "venv" ]; then \
		echo "🔧 Creating virtual environment..."; \
		python3 -m venv venv; \
	else \
		echo "✅ Virtual environment already exists."; \
	fi
endif

install: venv
	$(VENV_PIP) install --upgrade pip
ifeq ($(OS),Windows_NT)
	@if exist "requirements.txt" ( \
		$(VENV_PIP) install -r requirements.txt \
	) else ( \
		echo ⚠️  requirements.txt not found. Skipping package installation. \
	)
else
	@if [ -f "requirements.txt" ]; then \
		$(VENV_PIP) install -r requirements.txt; \
	else \
		echo "⚠️  requirements.txt not found. Skipping package installation."; \
	fi
endif

run:
	$(VENV_PYTHON) -m $(APP_MODULE)

test:
	$(VENV_PYTHON) -m pytest

test-cov:
	$(VENV_PYTHON) -m pytest --cov=src --cov-report=term-missing --cov-report=html

format:
	@echo "🎨 Running Black formatter..."
	$(VENV_PYTHON) -m black $(APP_DIR)
	@echo "🧹 Running Ruff autofix..."
	$(RUFF) check $(APP_DIR) --fix

lint:
	@echo "🧹 Running Ruff linter..."
	$(RUFF) check $(APP_DIR)

clean/all:
ifeq ($(OS),Windows_NT)
	@if exist "venv\" rmdir /s /q venv
	@if exist "__pycache__" rmdir /s /q __pycache__
	@if exist ".pytest_cache" rmdir /s /q .pytest_cache
	@if exist ".mypy_cache" rmdir /s /q .mypy_cache
	@if exist "$(APP_DIR)" for /d /r $(APP_DIR) %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
else
	rm -rf venv __pycache__ .pytest_cache .mypy_cache || true
	@if [ -d "$(APP_DIR)" ]; then find $(APP_DIR) -type d -name "__pycache__" -exec rm -rf {} + || true; fi
endif

clean/cache:
ifeq ($(OS),Windows_NT)
	@if exist "__pycache__" rmdir /s /q __pycache__
	@if exist ".pytest_cache" rmdir /s /q .pytest_cache
	@if exist ".mypy_cache" rmdir /s /q .mypy_cache
	@if exist "$(APP_DIR)" for /d /r $(APP_DIR) %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
else
	rm -rf __pycache__ .pytest_cache .mypy_cache || true
	@if [ -d "$(APP_DIR)" ]; then find $(APP_DIR) -type d -name "__pycache__" -exec rm -rf {} + || true; fi
endif

build: build/exe

build/exe:
	@echo "🔨 Building single executable..."
	$(VENV_PYTHON) -m PyInstaller friday-screener.spec --clean --noconfirm
	@echo "✅ Build complete! Executable in dist/ folder"

build/dist:
	@echo "🔨 Building with dependencies folder..."
	$(VENV_PYTHON) -m PyInstaller src/main.py --name friday-screener --onedir --clean --noconfirm
	@echo "✅ Build complete! Application in dist/friday-screener/ folder"

clean/build:
ifeq ($(OS),Windows_NT)
	@if exist "build" rmdir /s /q build
	@if exist "dist" rmdir /s /q dist
else
	rm -rf build dist || true
endif