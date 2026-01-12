# Development Guide

This guide covers development setup, testing, linting, and Docker usage.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Development](#docker-development)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Type Safety](#type-safety)

## Prerequisites

- **Backend**: Python 3.12+ (or 3.11/3.13 for compatibility)
- **Frontend**: Node.js 18+
- **Database**: SQLite (dev) or PostgreSQL (production)
- **Docker**: Docker and Docker Compose (optional)

## Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Docker Development

See [DOCKER.md](./DOCKER.md) for detailed Docker instructions.

Quick start:
```bash
docker-compose up --build
```

## Testing

See [TESTING.md](./TESTING.md) for detailed testing instructions.

### Quick Test Commands

```bash
# Backend tests
cd backend && python manage.py test

# Frontend tests
cd frontend && npm test -- --watchAll=false

# All tests with coverage
make test-coverage
```

## Code Quality

See [LINTING.md](./LINTING.md) for detailed linting instructions.

### Quick Lint Commands

```bash
# Format and lint all code
make format
make lint

# Or individually:
# Backend
cd backend && black . && flake8 .

# Frontend
cd frontend && npm run lint && npm run type-check
```

## Type Safety

### Backend

- Type hints in function signatures
- MyPy type checking (configured in `pyproject.toml`)
- Django stubs for better IDE support

### Frontend

- TypeScript with strict mode enabled
- Interface definitions in `src/types/index.ts`
- Type checking: `npm run type-check`

## Project Structure

```
Django-react/
├── backend/              # Django backend
│   ├── comments/         # Main app
│   │   ├── models.py    # Database models
│   │   ├── views.py     # API views
│   │   ├── serializers.py
│   │   ├── classifier.py
│   │   └── tests.py     # Unit tests
│   └── smart_comments/  # Project settings
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       ├── services/   # API services
│       └── types/      # TypeScript types
├── docker-compose.yml   # Docker orchestration
├── Makefile            # Common commands
└── .github/workflows/  # CI/CD
```

## Common Tasks

### Add a new feature

1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Run tests and linters
5. Submit PR

### Debugging

- **Backend**: Use Django debug toolbar or print statements
- **Frontend**: React DevTools and browser console
- **Docker**: `docker-compose logs -f [service-name]`

### Database Changes

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=True
CLASSIFIER_TYPE=rules
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
HUGGINGFACE_MODEL=j-hartmann/emotion-english-distilroberta-base

# For PostgreSQL
POSTGRES_DB=smart_comments
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Troubleshooting

### Backend Issues

- **Migration errors**: Delete `db.sqlite3` and re-run migrations
- **Import errors**: Ensure virtual environment is activated
- **Port conflicts**: Change port in `manage.py runserver 8001`

### Frontend Issues

- **Module not found**: Run `npm install`
- **Type errors**: Run `npm run type-check`
- **Build errors**: Clear `node_modules` and reinstall

### Docker Issues

- **Build fails**: Check Dockerfile syntax and dependencies
- **Connection refused**: Ensure services are healthy
- **Volume issues**: Check file permissions
