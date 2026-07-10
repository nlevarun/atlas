# Atlas Makefile
# Convenience commands for development

.PHONY: help install start stop clean test lint

help:
	@echo "Atlas Development Commands"
	@echo "=========================="
	@echo "make install    - Install all dependencies"
	@echo "make start      - Start all services (infra + api + web)"
	@echo "make stop       - Stop all services"
	@echo "make clean      - Clean up containers and volumes"
	@echo "make test       - Run tests"
	@echo "make lint       - Run linters"
	@echo "make logs       - View Docker logs"

install:
	@echo "Installing dependencies..."
	cd apps/api && pip install -r requirements.txt
	cd apps/web && npm install
	@echo "✓ Dependencies installed"

start-infra:
	@echo "Starting infrastructure services..."
	cd infra && docker compose up -d
	@echo "✓ Infrastructure started"
	@echo "  - Postgres: localhost:5432"
	@echo "  - Neo4j: localhost:7474 (browser)"
	@echo "  - Qdrant: localhost:6333"
	@echo "  - Redis: localhost:6379"
	@echo "  - Temporal: localhost:8233 (UI)"

start-api:
	@echo "Starting FastAPI backend..."
	cd apps/api && python main.py

start-web:
	@echo "Starting Next.js frontend..."
	cd apps/web && npm run dev

stop:
	@echo "Stopping services..."
	cd infra && docker compose down
	@echo "✓ Services stopped"

clean:
	@echo "Cleaning up..."
	cd infra && docker compose down -v
	rm -rf apps/web/node_modules
	rm -rf apps/web/.next
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned up"

test:
	@echo "Running tests..."
	pytest

lint:
	@echo "Running linters..."
	ruff check .
	cd apps/web && npm run lint

logs:
	cd infra && docker compose logs -f

status:
	@echo "Service Status:"
	cd infra && docker compose ps
