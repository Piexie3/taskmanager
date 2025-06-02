# Task Manager

A task management application to demonstrate CRUD operations and monitoring using prometheous and grafana

## Features

- User registration and authentication (JWT)
- CRUD operations for tasks
- PostgreSQL database with Alembic migrations
- Prometheus metrics and Grafana monitoring
- Docker containerization
- CI/CD pipeline with GitHub Actions
- AWS deployment ready

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Tasks (Authenticated)
- `GET /api/tasks` - Get user tasks (with pagination and filtering)
- `POST /api/create_task` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/delete/{id}` - Delete a task

### Health Check
- `GET /health` - Application health status

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Piexie3/taskmanager.git
cd taskmanager
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run with Docker Compose:
```bash
docker-compose up --build
```

4. Initialize the database:
```bash
docker-compose exec  flask db upgrade
```

The API will be available at `http://localhost:5000`

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update DATABASE_URL

3. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. Run the application:
```bash
python wsgi.py
```

## Configuration

Environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `FLASK_ENV` - Environment (development/production)



Run linting:
```bash
flake8 app/
black --check app/
```

## Monitoring

- Prometheus metrics: `http://localhost:9090`
- Grafana dashboard: `http://localhost:3000` (admin/admin)
