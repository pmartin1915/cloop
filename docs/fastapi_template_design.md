# FastAPI Project Template Design

This document defines the complete structure and content for the FastAPI scaffolder.

## Directory Structure

```
{project_name}/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── {project_name}/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py
│       │       └── endpoints/
│       │           ├── __init__.py
│       │           └── health.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── logging.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── schemas.py
│       └── services/
│           ├── __init__.py
│           └── example_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── test_health.py
│   └── services/
│       └── __init__.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## File Contents

### pyproject.toml

```toml
[project]
name = "{{project_name}}"
version = "0.1.0"
description = "FastAPI application"
authors = [
    {name = "{{author_name}}", email = "{{author_email}}"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
{{project_name}} = "{{project_name}}.main:main"

[tool.poetry]
packages = [{include = "{{project_name}}", from = "src"}]

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "httpx>=0.28.0",
    "ruff>=0.8.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
```

### src/{{project_name}}/main.py

```python
"""
{{project_name}} - FastAPI Application

A modern FastAPI application with best practices.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .core.config import settings
from .core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logging.info(f"Starting {settings.PROJECT_NAME}")
    yield
    # Shutdown
    logging.info(f"Shutting down {settings.PROJECT_NAME}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="{{project_description}}",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to {{project_name}}",
        "version": settings.VERSION,
        "docs": "/docs",
    }


def main():
    """CLI entry point"""
    import uvicorn

    setup_logging()
    uvicorn.run(
        "{{project_name}}.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
```

### src/{{project_name}}/core/config.py

```python
"""
Configuration management using Pydantic Settings
"""
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Project info
    PROJECT_NAME: str = "{{project_name}}"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "{{project_description}}"

    # Server config
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # API config
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )

    # Database (example)
    DATABASE_URL: str = Field(
        default="sqlite:///./{{project_name}}.db",
        description="Database connection URL"
    )


# Global settings instance
settings = Settings()
```

### src/{{project_name}}/core/logging.py

```python
"""
Logging configuration
"""
import logging
import sys


def setup_logging(level: str = "INFO"):
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
    )

    # Set third-party loggers to WARNING
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
```

### src/{{project_name}}/api/v1/router.py

```python
"""
API v1 Router
"""
from fastapi import APIRouter

from .endpoints import health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
```

### src/{{project_name}}/api/v1/endpoints/health.py

```python
"""
Health check endpoint
"""
from fastapi import APIRouter

from ....models.schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Service is running"
    )
```

### src/{{project_name}}/api/dependencies.py

```python
"""
Shared API dependencies
"""
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status


async def get_api_key(
    x_api_key: Annotated[str | None, Header()] = None
) -> str:
    """
    Example dependency: API key validation

    Remove or modify based on your authentication needs
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    return x_api_key
```

### src/{{project_name}}/models/schemas.py

```python
"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")


class ExampleRequest(BaseModel):
    """Example request model"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class ExampleResponse(BaseModel):
    """Example response model"""
    id: int
    name: str
    description: str | None = None
```

### src/{{project_name}}/services/example_service.py

```python
"""
Example business logic service
"""
import logging

logger = logging.getLogger(__name__)


class ExampleService:
    """Example service for business logic"""

    def __init__(self):
        self.data = {}

    async def create_item(self, name: str, description: str | None = None) -> dict:
        """Create a new item"""
        item_id = len(self.data) + 1
        item = {
            "id": item_id,
            "name": name,
            "description": description
        }
        self.data[item_id] = item
        logger.info(f"Created item: {item_id}")
        return item

    async def get_item(self, item_id: int) -> dict | None:
        """Get item by ID"""
        return self.data.get(item_id)
```

### tests/conftest.py

```python
"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient

from {{project_name}}.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def example_service():
    """Example service fixture"""
    from {{project_name}}.services.example_service import ExampleService
    return ExampleService()
```

### tests/api/test_health.py

```python
"""
Tests for health check endpoint
"""
import pytest


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
```

### .env.example

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# API Configuration
API_V1_PREFIX=/api/v1

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Database
DATABASE_URL=sqlite:///./{{project_name}}.db
```

### .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
env/
venv/
ENV/
env.bak/
venv.bak/
.venv/

# Environment Variables
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.hypothesis/

# Linting
.ruff_cache/
.mypy_cache/

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# OS
Thumbs.db
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
COPY src/ src/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Expose port
EXPOSE 8000

# Run application
CMD ["poetry", "run", "{{project_name}}"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=sqlite:///./{{project_name}}.db
    volumes:
      - ./src:/app/src
    command: poetry run uvicorn {{project_name}}.main:app --host 0.0.0.0 --port 8000 --reload
```

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Poetry
      run: pip install poetry

    - name: Install dependencies
      run: poetry install

    - name: Lint with Ruff
      run: poetry run ruff check src/

    - name: Test with pytest
      run: poetry run pytest --cov={{project_name}} --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### README.md

```markdown
# {{project_name}}

{{project_description}}

## Features

- ⚡ **FastAPI** - Modern, fast web framework
- 🔧 **Poetry** - Dependency management
- 🧪 **Pytest** - Testing framework
- 🎨 **Ruff** - Fast Python linter
- 🐳 **Docker** - Containerization support
- 📝 **Pydantic** - Data validation

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry

### Installation

```bash
# Install dependencies
poetry install

# Copy environment variables
cp .env.example .env

# Run development server
poetry run {{project_name}}
```

The API will be available at http://localhost:8000

- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build
```

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov={{project_name}}

# Run specific test file
poetry run pytest tests/api/test_health.py
```

### Linting

```bash
# Check code style
poetry run ruff check src/

# Auto-fix issues
poetry run ruff check --fix src/
```

## Project Structure

```
src/{{project_name}}/
├── api/              # API endpoints
│   └── v1/          # API version 1
│       └── endpoints/
├── core/            # Core configuration
├── models/          # Pydantic models
└── services/        # Business logic
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `GET /docs` - API documentation

## Configuration

Configuration is managed through environment variables and `.env` file:

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: False)
- `DATABASE_URL` - Database connection string

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License

---

Generated with ❤️ by [Ultrathink](https://github.com/yourusername/ultrathink)
```

### src/{{project_name}}/__init__.py

```python
"""
{{project_name}} package
"""
__version__ = "0.1.0"
```

## Template Variables

The template uses the following variables:

- `{{project_name}}` - Project name (snake_case)
- `{{project_description}}` - Project description
- `{{author_name}}` - Author name
- `{{author_email}}` - Author email

## Design Principles

1. **Modern Stack** - FastAPI, Pydantic v2, Python 3.11+
2. **Src Layout** - Clean separation of source code
3. **API Versioning** - Built-in v1 structure for future versions
4. **Configuration Management** - Pydantic Settings with .env support
5. **Testing Ready** - Pytest with async support and fixtures
6. **Production Ready** - Docker, logging, health checks
7. **Type Safety** - Full type hints throughout
8. **Clean Architecture** - Separation of concerns (API, services, models)
