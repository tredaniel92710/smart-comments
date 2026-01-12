# Docker Setup Guide

This project includes Docker support for easy deployment and development.

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

### Services

- **Backend**: Django REST API on `http://localhost:8000`
- **Frontend**: React app on `http://localhost:3000`
- **Database**: PostgreSQL on port `5432`

## Environment Variables

Create a `.env` file in the project root (optional):

```env
OPENAI_API_KEY=your_openai_api_key_here
CLASSIFIER_TYPE=rules
DEBUG=True
SECRET_KEY=your-secret-key-here
```

## Individual Docker Commands

### Build Backend Only
```bash
cd backend
docker build -t smart-comments-backend .
docker run -p 8000:8000 smart-comments-backend
```

### Build Frontend Only
```bash
cd frontend
docker build -t smart-comments-frontend .
docker run -p 3000:80 smart-comments-frontend
```

## Development with Docker

For development, you can mount volumes to enable hot-reloading:

```yaml
# In docker-compose.yml, volumes are already configured for development
volumes:
  - ./backend:/app
  - ./frontend:/app  # For frontend development
```

## Production Deployment

For production, use the built images without volume mounts and set appropriate environment variables:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

1. **Port already in use**: Change ports in `docker-compose.yml`
2. **Database connection errors**: Wait for database to be healthy before starting backend
3. **Permission errors**: Ensure Docker has proper permissions
