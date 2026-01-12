# Code Quality and Linting

## Backend (Python)

### Tools Used

- **Black**: Code formatter
- **Flake8**: Linter
- **MyPy**: Type checker
- **Coverage**: Test coverage

### Running Linters

```bash
cd backend

# Format code with Black
black .

# Check formatting (without changing files)
black --check .

# Run Flake8
flake8 . --exclude=migrations,venv,env,.venv

# Type checking with MyPy
mypy .

# Run all checks
make lint  # From project root
```

### Configuration

- `.flake8` - Flake8 configuration
- `pyproject.toml` - Black and MyPy configuration

## Frontend (TypeScript/React)

### Tools Used

- **ESLint**: JavaScript/TypeScript linter
- **TypeScript**: Type checking

### Running Linters

```bash
cd frontend

# Run ESLint
npm run lint          # Auto-fix issues
npm run lint:check    # Check only

# Type checking
npm run type-check

# Run all checks
make lint  # From project root
```

### Configuration

- `.eslintrc.json` - ESLint configuration
- `tsconfig.json` - TypeScript configuration

## Pre-commit Hooks

Install pre-commit hooks to automatically run linters before commits:

```bash
pip install pre-commit
pre-commit install
```

Hooks will run automatically on `git commit`.

## Makefile Commands

From project root:

```bash
make lint      # Run all linters
make format    # Format all code
make test      # Run all tests
make test-coverage  # Run tests with coverage
```
