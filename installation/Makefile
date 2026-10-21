# Devian Makefile

.PHONY: help install lint test clean

help:
	@echo "Devian AI Ecosystem Commands:"
	@echo "  make install  - Run the autonomous installer script"
	@echo "  make lint     - Check Python syntax and lint code"
	@echo "  make clean    - Remove build artifacts, caches, and venv"

install:
	python install.py

lint:
	python -m py_compile tools/*.py install.py

clean:
	rm -rf .venv __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
