.PHONY: install run clean dev

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