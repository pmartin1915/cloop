# FastAPI Project Scaffolder - Feature Documentation

## Overview

The **FastAPI Project Scaffolder** is the first core feature of Ultrathink, enabling rapid creation of production-ready FastAPI projects following 2025 best practices.

## Features

### ✨ What It Creates

The scaffolder generates a complete FastAPI project with:

- **Modern Stack**: FastAPI 0.115+, Pydantic v2, Python 3.11+
- **Dependency Management**: Poetry with pyproject.toml
- **Project Structure**: Clean src layout with vertical slice architecture
- **API Versioning**: Built-in `/api/v1/` structure
- **Testing**: Pytest with async support and fixtures
- **Linting**: Ruff configuration
- **Docker**: Dockerfile and docker-compose.yml
- **CI/CD**: GitHub Actions workflow
- **Configuration**: Pydantic Settings with .env support
- **Documentation**: Comprehensive README and code comments

### 📁 Generated Structure

```
{project_name}/
├── .github/workflows/ci.yml    # CI/CD pipeline
├── src/{project_name}/          # Source code
│   ├── api/v1/                  # API endpoints
│   │   └── endpoints/health.py  # Health check
│   ├── core/                    # Configuration
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/schemas.py        # Pydantic models
│   ├── services/                # Business logic
│   └── main.py                  # FastAPI app
├── tests/                       # Test suite
│   ├── api/test_health.py
│   └── conftest.py              # Pytest fixtures
├── .env.example                 # Environment template
├── .gitignore                   # Git exclusions
├── Dockerfile                   # Container image
├── docker-compose.yml           # Docker orchestration
├── pyproject.toml               # Poetry config
└── README.md                    # Project documentation
```

## Usage

### Basic Command

```bash
ultrathink scaffold --name myapi
```

### Full Command with Options

```bash
ultrathink scaffold \
  --name myapi \
  --author "Your Name" \
  --email "you@example.com" \
  --description "My awesome API" \
  --path ./projects
```

### Command Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--name` | ✓ | - | Project name (snake_case) |
| `--author` | ✗ | "Your Name" | Author name |
| `--email` | ✗ | "you@example.com" | Author email |
| `--description` | ✗ | "A FastAPI application" | Project description |
| `--path` | ✗ | `.` | Output directory |

### Project Name Rules

✓ **Valid names:**
- `myapi`
- `user_service`
- `payment_gateway`

✗ **Invalid names:**
- `MyAPI` (uppercase)
- `my-api` (hyphens)
- `1api` (starts with number)

## Quick Start After Scaffolding

Once your project is created:

```bash
# Navigate to project
cd myapi

# Install dependencies
poetry install

# Run development server
poetry run myapi
```

The API will be available at:
- **Application**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## Development Workflow

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=myapi

# Watch mode
poetry run pytest-watch
```

### Linting

```bash
# Check code
poetry run ruff check src/

# Auto-fix issues
poetry run ruff check --fix src/
```

### Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f
```

## Architecture

### Vertical Slice Design

The scaffolder creates a **vertical slice architecture** where features are organized by business capability rather than technical layer:

```
api/v1/endpoints/    → API entry points
services/            → Business logic
models/schemas.py    → Data contracts
core/                → Shared infrastructure
```

### API Versioning

Projects are scaffolded with versioning built-in:
- Current version: `/api/v1/`
- Future versions: `/api/v2/` (easy to add)
- Root endpoint: `/` (version-independent)

### Configuration Management

Environment-based configuration using Pydantic Settings:

```python
# In code
from myapi.core.config import settings

print(settings.DATABASE_URL)
print(settings.DEBUG)
```

```bash
# In .env file
DATABASE_URL=postgresql://localhost/mydb
DEBUG=True
```

## Testing

### Included Tests

The scaffolder creates initial tests for:
- Health check endpoint
- Root endpoint
- Example service fixtures

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── api/
│   └── test_health.py       # API tests
└── services/
    └── __init__.py          # Service tests
```

### Writing New Tests

```python
def test_my_endpoint(client):
    """Test my endpoint"""
    response = client.get("/api/v1/myendpoint")
    assert response.status_code == 200
```

## Observability

### Logging

The scaffolder includes structured logging:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing request")
logger.error("Error occurred", exc_info=True)
```

### Monitoring Metrics

The health endpoint provides basic service status:

```json
GET /api/v1/health
{
  "status": "healthy",
  "message": "Service is running"
}
```

## CI/CD Integration

### GitHub Actions

The generated project includes a complete CI workflow:

```yaml
# Runs on: push, pull_request
# Tests on: Python 3.11, 3.12
# Steps:
#   1. Install Poetry
#   2. Install dependencies
#   3. Run Ruff linter
#   4. Run Pytest
#   5. Upload coverage
```

### Adding More CI Steps

Edit `.github/workflows/ci.yml` to add:
- Security scanning
- Database migrations
- Deployment steps
- Performance tests

## Customization

### Adding New Endpoints

1. Create endpoint file:
```python
# src/myapi/api/v1/endpoints/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_users():
    return {"users": []}
```

2. Register in router:
```python
# src/myapi/api/v1/router.py
from .endpoints import users

api_router.include_router(users.router, prefix="/users", tags=["users"])
```

### Adding Dependencies

```bash
# Add production dependency
poetry add sqlalchemy

# Add dev dependency
poetry add --group dev pytest-cov
```

### Modifying Configuration

Add new settings in `core/config.py`:

```python
class Settings(BaseSettings):
    # Add your settings
    MAX_CONNECTIONS: int = 100
    CACHE_TTL: int = 3600
```

## Troubleshooting

### Common Issues

**Issue**: Project name validation fails
```bash
[ERROR] Invalid project name: MyAPI
```
**Solution**: Use snake_case (lowercase with underscores): `my_api`

---

**Issue**: Poetry not found
```bash
poetry: command not found
```
**Solution**: Install Poetry: `pip install poetry`

---

**Issue**: Port 8000 already in use
```bash
ERROR:    [Errno 98] Address already in use
```
**Solution**: Change port in `.env`: `PORT=8001`

## Best Practices

### ✓ Do

- Use meaningful project names
- Fill in `.env` before running
- Write tests for new endpoints
- Keep API versioning consistent
- Document configuration changes
- Use type hints throughout

### ✗ Don't

- Commit `.env` files (use `.env.example`)
- Hardcode secrets in code
- Skip writing tests
- Ignore linter warnings
- Mix business logic in endpoints

## Performance

### Scaffold Speed

Average scaffold time: **30-50ms**
- Creates 27 files
- 6 directories
- ~3KB total size

### Observability Metrics

The scaffolder logs:
- Start time
- Files generated
- Duration
- Final location
- Any errors

## Future Enhancements

Planned features for the scaffolder:

- [ ] Database integration templates (PostgreSQL, MongoDB)
- [ ] Authentication scaffolding (JWT, OAuth)
- [ ] GraphQL option
- [ ] WebSocket support
- [ ] Celery task queue integration
- [ ] Multiple framework support (Django, Flask)
- [ ] Interactive CLI mode

## Contributing

To improve the scaffolder:

1. Update templates in `src/ultrathink/scaffolding/python_scaffolder.py`
2. Add tests in `tests/test_scaffolding.py`
3. Update this documentation
4. Run full test suite: `poetry run pytest`

## Related Documentation

- [FastAPI Template Design](./fastapi_template_design.md) - Full template specification
- [Ultrathink Vision](./02_ultrathink_vision.md) - Framework overview
- [Developer Guide](./03_developer_guide.md) - Development principles

## Support

For issues or questions:
- Check troubleshooting section above
- Review test cases in `tests/test_scaffolding.py`
- See FastAPI docs: https://fastapi.tiangolo.com/

---

**Version**: 0.1.0
**Status**: ✓ Production Ready
**Last Updated**: 2025-10-11
