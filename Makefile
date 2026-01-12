.PHONY: help install test lint format docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install          - Install all dependencies"
	@echo "  make test             - Run all tests"
	@echo "  make lint             - Run linters"
	@echo "  make format           - Format code"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"

# Install dependencies
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Testing
test:
	@echo "Running backend tests..."
	cd backend && python manage.py test
	@echo "Running frontend tests..."
	cd frontend && npm test -- --watchAll=false

test-backend:
	cd backend && python manage.py test

test-frontend:
	cd frontend && npm test -- --watchAll=false

test-coverage:
	cd backend && coverage run --source='.' manage.py test && coverage report
	cd frontend && npm test -- --coverage --watchAll=false

# Linting
lint:
	@echo "Linting backend..."
	cd backend && flake8 . --exclude=migrations,venv,env,.venv
	cd backend && black --check .
	@echo "Linting frontend..."
	cd frontend && npm run lint:check
	cd frontend && npm run type-check

# Formatting
format:
	@echo "Formatting backend..."
	cd backend && black .
	@echo "Formatting frontend..."
	cd frontend && npm run lint

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development
dev-backend:
	cd backend && python manage.py runserver

dev-frontend:
	cd frontend && npm start
