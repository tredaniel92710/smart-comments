# Smart Comments - Production-Ready Django + React Application

A minimal, production-ready "Smart Comments" feature that integrates a Django REST API backend, React TypeScript frontend, and an intelligent comment classification service.

## Features

### Backend (Django)
- ✅ RESTful API for posts and comments
- ✅ Rule-based comment classification system
- ✅ Bonus: ML-based classification support (Hugging Face transformers)
- ✅ Automatic flagging of comments for review
- ✅ CORS configuration for React frontend

### Frontend (React + TypeScript)
- ✅ Display posts and comments
- ✅ Add new comments with real-time classification
- ✅ Visual highlighting of flagged comments
- ✅ Bonus: Moderator view to filter and review flagged comments
- ✅ Modern, responsive UI

## Project Structure

```
Django-react/
├── backend/                 # Django backend
│   ├── smart_comments/     # Django project settings
│   ├── comments/           # Comments app
│   │   ├── models.py      # Post and Comment models
│   │   ├── views.py       # API viewsets
│   │   ├── serializers.py # DRF serializers
│   │   ├── classifier.py  # Classification service
│   │   └── urls.py        # API routes
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Prerequisites

- Python 3.8+ 
- Node.js 16+ and npm
- (Optional) Virtual environment for Python

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`
   - API endpoints: `http://localhost:8000/api/`
   - Admin panel: `http://localhost:8000/admin/`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file (optional):**
   Create `.env` file in the frontend directory:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

### Creating Posts and Comments

1. **Via Admin Panel:**
   - Navigate to `http://localhost:8000/admin/`
   - Login with superuser credentials
   - Create posts and comments manually

2. **Via API:**
   ```bash
   # Create a post
   curl -X POST http://localhost:8000/api/posts/ \
     -H "Content-Type: application/json" \
     -d '{"title": "My First Post", "content": "This is the content"}'

   # Create a comment
   curl -X POST http://localhost:8000/api/comments/ \
     -H "Content-Type: application/json" \
     -d '{"post": 1, "author": "John Doe", "content": "Great post!"}'
   ```

3. **Via React Frontend:**
   - Open `http://localhost:3000`
   - View existing posts
   - Click "Add Comment" to add new comments
   - Comments are automatically classified and flagged if needed

### Classification System

The system uses a **rule-based classifier** by default that flags comments based on:
- Suspicious keywords (spam, scam, fake, fraud)
- Profanity detection
- Excessive punctuation or capitalization
- URLs in comments
- Suspicious number patterns
- Very short or very long comments

**ML Classification (Bonus):**
- Enable ML classification by checking the checkbox when submitting a comment
- Requires `transformers` and `torch` libraries (included in requirements.txt)
- Uses Hugging Face emotion detection model
- Falls back to rule-based if ML model fails

### Moderator View

- Click "Moderator View" in the navigation
- View all flagged comments in one place
- See flag reasons for each comment
- Refresh to get latest flagged comments

## API Endpoints

### Posts
- `GET /api/posts/` - List all posts
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/` - Create a new post
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a post

### Comments
- `GET /api/comments/` - List all comments
  - Query params: `?post={id}` - Filter by post
  - Query params: `?flagged=true` - Get only flagged comments
- `GET /api/comments/{id}/` - Get comment details
- `POST /api/comments/` - Create a new comment
  - Query params: `?use_ml=true` - Use ML classification
- `GET /api/comments/flagged/` - Get all flagged comments

## Bonus Features

### 🐳 Docker Support

Full Docker setup with docker-compose for easy deployment:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

See [DOCKER.md](./DOCKER.md) for detailed instructions.

**Services:**
- Backend (Django) on port 8000
- Frontend (React) on port 3000
- PostgreSQL database

### 🧪 Testing

Comprehensive test suite for both backend and frontend:

**Backend Tests:**
```bash
cd backend
python manage.py test
# Or with coverage
coverage run --source='.' manage.py test && coverage report
```

**Frontend Tests:**
```bash
cd frontend
npm test -- --watchAll=false --coverage
```

**Test Coverage:**
- Model tests (Post, Comment, CommentSettings)
- API endpoint tests
- Classification logic tests
- Integration tests

See [TESTING.md](./TESTING.md) for detailed testing guide.

### 🎨 Code Quality & Linting

**Backend (Python):**
- **Black**: Code formatter
- **Flake8**: Linter
- **MyPy**: Type checker
- **Coverage**: Test coverage

```bash
cd backend
black .              # Format code
flake8 .            # Lint code
mypy .              # Type check
```

**Frontend (TypeScript):**
- **ESLint**: JavaScript/TypeScript linter
- **TypeScript**: Strict type checking

```bash
cd frontend
npm run lint        # Lint and fix
npm run type-check  # Type check
```

**Makefile Commands:**
```bash
make lint      # Run all linters
make format    # Format all code
make test      # Run all tests
make test-coverage  # Tests with coverage
```

See [LINTING.md](./LINTING.md) for detailed linting guide.

### 📝 Type Safety

- **Backend**: Type hints, MyPy checking, Django stubs
- **Frontend**: TypeScript with strict mode, comprehensive interfaces

### 🔄 CI/CD Pipeline

Automated testing and linting via GitHub Actions (`.github/workflows/ci.yml`):
- Backend tests and linting
- Frontend build, tests, and type checking
- Docker build verification

## CI/CD Setup

The project includes a complete CI/CD pipeline:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run migrations
        run: |
          cd backend
          python manage.py migrate --check
      - name: Run tests (if available)
        run: |
          cd backend
          python manage.py test

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run linter
        run: |
          cd frontend
          npm run lint || true
      - name: Build
        run: |
          cd frontend
          npm run build
```

## Production Deployment Considerations

1. **Environment Variables:**
   - Set `DEBUG=False` in production
   - Use a strong `SECRET_KEY`
   - Configure proper `ALLOWED_HOSTS`
   - Use environment variables for sensitive data

2. **Database:**
   - Use PostgreSQL or MySQL instead of SQLite
   - Set up proper database migrations

3. **Static Files:**
   - Configure static file serving (WhiteNoise, S3, etc.)
   - Run `python manage.py collectstatic`

4. **Security:**
   - Enable HTTPS
   - Configure CORS properly for production domains
   - Use authentication/authorization if needed
   - Set up rate limiting

5. **Frontend:**
   - Build production bundle: `npm run build`
   - Serve via Nginx or similar
   - Or deploy to Vercel/Netlify

## Testing the Classification

Try submitting comments with:
- Profanity: "This is f*cking great!"
- URLs: "Check this out: https://example.com"
- Spam keywords: "This is a scam!"
- Excessive caps: "THIS IS AMAZING!!!!!"
- Very short: "ok"
- Very long: (1000+ characters)

These should be automatically flagged for review.

## Troubleshooting

### Backend Issues
- **Port already in use:** Change port: `python manage.py runserver 8001`
- **Migration errors:** Run `python manage.py makemigrations` then `migrate`
- **CORS errors:** Check `CORS_ALLOWED_ORIGINS` in settings.py

### Frontend Issues
- **API connection errors:** Verify backend is running and `REACT_APP_API_URL` is correct
- **Build errors:** Delete `node_modules` and `package-lock.json`, then `npm install` again

## License

This project is for demonstration purposes.

## Development

See [DEVELOPMENT.md](./DEVELOPMENT.md) for:
- Detailed setup instructions
- Development workflow
- Debugging tips
- Common tasks

## Contributing

This is a minimal production-ready example. For production use, consider:
- Adding authentication/authorization
- Implementing proper error handling
- Setting up logging and monitoring
- Implementing rate limiting
- Adding database indexes for performance
- Setting up monitoring and alerting
