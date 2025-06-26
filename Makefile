.PHONY: help install run dev clean test lint format

# Default target
help:
	@echo "🔧 Azure Document Intelligence App - Makefile"
	@echo ""
	@echo "Tillgängliga kommandon:"
	@echo "  install    - Installera dependencies med uv"
	@echo "  run        - Kör Streamlit-appen"
	@echo "  dev        - Kör i development-läge med auto-reload"
	@echo "  clean      - Rensa cache och temporära filer"
	@echo "  test       - Kör tester (om de finns)"
	@echo "  lint       - Kör linting med ruff"
	@echo "  format     - Formatera kod med ruff"
	@echo "  build      - Bygg paketet med uv"
	@echo "  publish    - Publicera paketet (om konfigurerat)"

# Installera dependencies
install:
	@echo "📦 Installerar dependencies med uv..."
	uv pip install -e .
	@echo "✅ Installation klar!"

# Kör appen
run:
	@echo "🚀 Startar Azure Document Intelligence app..."
	uv run streamlit run streamlit_app.py

# Development-läge med auto-reload
dev:
	@echo "🔧 Startar i development-läge..."
	uv run streamlit run streamlit_app.py --server.runOnSave true

# Rensa cache och temporära filer
clean:
	@echo "🧹 Rensar cache och temporära filer..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf output/
	rm -rf dist/
	rm -rf build/
	@echo "✅ Rengöring klar!"

# Kör tester (placeholder)
test:
	@echo "🧪 Kör tester..."
	@echo "⚠️  Inga tester konfigurerade ännu"
	# uv run pytest tests/

# Linting med ruff
lint:
	@echo "🔍 Kör linting med ruff..."
	uv run ruff check .

# Formatera kod med ruff
format:
	@echo "✨ Formaterar kod med ruff..."
	uv run ruff format .

# Bygg paketet
build:
	@echo "🔨 Bygger paketet..."
	python -m build

# Installera development dependencies
install-dev:
	@echo "📦 Installerar development dependencies..."
	uv pip install ruff pytest
	@echo "✅ Development dependencies installerade!"

# Visa projektinfo
info:
	@echo "📋 Projektinformation:"
	@echo "  Namn: azure-docintelligence-app"
	@echo "  Version: 0.1.0"
	@echo "  Python: $(shell python --version)"
	@echo "  UV: $(shell uv --version)"
	@echo "  Streamlit: $(shell uv run streamlit --version 2>/dev/null || echo 'Ej installerat')"

# Setup hela projektet
setup: install install-dev
	@echo "🎉 Projektet är redo att användas!"
	@echo "Kör 'make run' för att starta appen" 