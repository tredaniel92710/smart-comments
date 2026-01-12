# Testing Guide

## Backend Tests

### Running Tests

```bash
# Run all tests
cd backend
python manage.py test

# Run specific test file
python manage.py test comments.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Using pytest (Alternative)

```bash
cd backend
pytest
pytest --cov=comments --cov-report=html
```

### Test Structure

- `comments/tests.py` - Contains all unit and integration tests
- Tests cover:
  - Model creation and validation
  - API endpoints
  - Comment classification
  - Settings management

## Frontend Tests

### Running Tests

```bash
cd frontend
npm test                    # Interactive mode
npm test -- --watchAll=false  # Run once
npm test -- --coverage     # With coverage
```

### Writing Tests

Create test files with `.test.tsx` or `.spec.tsx` extension:

```typescript
import { render, screen } from '@testing-library/react';
import Component from './Component';

test('renders component', () => {
  render(<Component />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Integration Tests

Integration tests verify the interaction between frontend and backend:

```bash
# Run backend API tests
cd backend
python manage.py test comments.tests.CommentAPITest

# Run frontend API integration tests
cd frontend
npm test -- api.test.ts
```

## Continuous Integration

Tests are automatically run in CI (see `.github/workflows/ci.yml`).
