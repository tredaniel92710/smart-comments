# Backend Setup

## Quick Start

1. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Run server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the backend directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
