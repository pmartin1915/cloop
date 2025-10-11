"""
Tests for the Python FastAPI scaffolder
"""
import pytest
from pathlib import Path
import shutil

from ultrathink.scaffolding import PythonScaffolder


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for test output"""
    output_dir = tmp_path / "test_projects"
    output_dir.mkdir()
    yield output_dir
    # Cleanup after test
    if output_dir.exists():
        shutil.rmtree(output_dir)


@pytest.fixture
def scaffolder():
    """Create a PythonScaffolder instance"""
    return PythonScaffolder()


def test_scaffold_basic_project(scaffolder, temp_output_dir):
    """Test basic project scaffolding"""
    project_name = "myapi"

    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir),
        author_name="Test Author",
        author_email="test@example.com",
        description="Test API"
    )

    # Assert project directory was created
    assert project_path.exists()
    assert project_path.is_dir()
    assert project_path.name == project_name


def test_scaffold_creates_all_directories(scaffolder, temp_output_dir):
    """Test that all expected directories are created"""
    project_name = "testapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Check main directories
    assert (project_path / "src").exists()
    assert (project_path / "tests").exists()
    assert (project_path / ".github" / "workflows").exists()

    # Check source structure
    assert (project_path / "src" / project_name).exists()
    assert (project_path / "src" / project_name / "api").exists()
    assert (project_path / "src" / project_name / "api" / "v1").exists()
    assert (project_path / "src" / project_name / "api" / "v1" / "endpoints").exists()
    assert (project_path / "src" / project_name / "core").exists()
    assert (project_path / "src" / project_name / "models").exists()
    assert (project_path / "src" / project_name / "services").exists()

    # Check test structure
    assert (project_path / "tests" / "api").exists()
    assert (project_path / "tests" / "services").exists()


def test_scaffold_creates_all_files(scaffolder, temp_output_dir):
    """Test that all expected files are created"""
    project_name = "fileapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Root files
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()

    # CI/CD
    assert (project_path / ".github" / "workflows" / "ci.yml").exists()

    # Main application files
    assert (project_path / "src" / project_name / "__init__.py").exists()
    assert (project_path / "src" / project_name / "main.py").exists()

    # Core files
    assert (project_path / "src" / project_name / "core" / "config.py").exists()
    assert (project_path / "src" / project_name / "core" / "logging.py").exists()

    # API files
    assert (project_path / "src" / project_name / "api" / "dependencies.py").exists()
    assert (project_path / "src" / project_name / "api" / "v1" / "router.py").exists()
    assert (project_path / "src" / project_name / "api" / "v1" / "endpoints" / "health.py").exists()

    # Models
    assert (project_path / "src" / project_name / "models" / "schemas.py").exists()

    # Services
    assert (project_path / "src" / project_name / "services" / "example_service.py").exists()

    # Tests
    assert (project_path / "tests" / "conftest.py").exists()
    assert (project_path / "tests" / "api" / "test_health.py").exists()


def test_scaffold_file_content_substitution(scaffolder, temp_output_dir):
    """Test that template variables are correctly substituted"""
    project_name = "contentapi"
    author_name = "John Doe"
    author_email = "john@example.com"
    description = "My awesome API"

    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir),
        author_name=author_name,
        author_email=author_email,
        description=description
    )

    # Check pyproject.toml
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert f'name = "{project_name}"' in pyproject_content
    assert f'name = "{author_name}"' in pyproject_content
    assert f'email = "{author_email}"' in pyproject_content
    assert f'description = "{description}"' in pyproject_content

    # Check README.md
    readme_content = (project_path / "README.md").read_text(encoding="utf-8")
    assert f"# {project_name}" in readme_content
    assert description in readme_content

    # Check main.py
    main_content = (project_path / "src" / project_name / "main.py").read_text(encoding="utf-8")
    assert f'"{project_name}' in main_content or f"'{project_name}" in main_content
    assert description in main_content


def test_scaffold_invalid_project_name_uppercase(scaffolder, temp_output_dir):
    """Test that uppercase project names are rejected"""
    with pytest.raises(ValueError, match="Invalid project name"):
        scaffolder.scaffold(
            project_name="MyAPI",
            output_dir=str(temp_output_dir)
        )


def test_scaffold_invalid_project_name_hyphen(scaffolder, temp_output_dir):
    """Test that project names with hyphens are rejected"""
    with pytest.raises(ValueError, match="Invalid project name"):
        scaffolder.scaffold(
            project_name="my-api",
            output_dir=str(temp_output_dir)
        )


def test_scaffold_invalid_project_name_starts_with_number(scaffolder, temp_output_dir):
    """Test that project names starting with numbers are rejected"""
    with pytest.raises(ValueError, match="Invalid project name"):
        scaffolder.scaffold(
            project_name="1api",
            output_dir=str(temp_output_dir)
        )


def test_scaffold_project_already_exists(scaffolder, temp_output_dir):
    """Test that scaffolding fails if project directory already exists"""
    project_name = "existingapi"

    # Create project first time
    scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Try to create again - should fail
    with pytest.raises(FileExistsError, match="Project directory already exists"):
        scaffolder.scaffold(
            project_name=project_name,
            output_dir=str(temp_output_dir)
        )


def test_scaffold_pyproject_toml_structure(scaffolder, temp_output_dir):
    """Test that pyproject.toml has correct structure"""
    project_name = "structapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    pyproject_content = (project_path / "pyproject.toml").read_text()

    # Check for essential sections
    assert "[project]" in pyproject_content
    assert "[project.scripts]" in pyproject_content
    assert "[tool.poetry]" in pyproject_content
    assert "[build-system]" in pyproject_content
    assert "[dependency-groups]" in pyproject_content
    assert "[tool.ruff]" in pyproject_content
    assert "[tool.pytest.ini_options]" in pyproject_content

    # Check for essential dependencies
    assert "fastapi" in pyproject_content
    assert "uvicorn" in pyproject_content
    assert "pydantic" in pyproject_content
    assert "pytest" in pyproject_content


def test_scaffold_main_py_structure(scaffolder, temp_output_dir):
    """Test that main.py has correct structure"""
    project_name = "mainapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    main_content = (project_path / "src" / project_name / "main.py").read_text()

    # Check for essential imports
    assert "from fastapi import FastAPI" in main_content
    assert "from fastapi.middleware.cors import CORSMiddleware" in main_content

    # Check for app initialization
    assert "app = FastAPI(" in main_content

    # Check for lifespan
    assert "@asynccontextmanager" in main_content
    assert "async def lifespan" in main_content

    # Check for CORS
    assert "add_middleware" in main_content
    assert "CORSMiddleware" in main_content

    # Check for root endpoint
    assert '@app.get("/")' in main_content
    assert "async def root()" in main_content

    # Check for main function
    assert "def main():" in main_content
    assert "uvicorn.run" in main_content


def test_scaffold_health_endpoint(scaffolder, temp_output_dir):
    """Test that health endpoint is correctly created"""
    project_name = "healthapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    health_content = (
        project_path / "src" / project_name / "api" / "v1" / "endpoints" / "health.py"
    ).read_text()

    # Check structure
    assert "from fastapi import APIRouter" in health_content
    assert "router = APIRouter()" in health_content
    assert '@router.get("' in health_content  # Check for decorator start
    assert "async def health_check()" in health_content
    assert "HealthResponse" in health_content


def test_scaffold_test_structure(scaffolder, temp_output_dir):
    """Test that test files are correctly structured"""
    project_name = "teststructapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Check conftest.py
    conftest_content = (project_path / "tests" / "conftest.py").read_text()
    assert "import pytest" in conftest_content
    assert "from fastapi.testclient import TestClient" in conftest_content
    assert "@pytest.fixture" in conftest_content
    assert "def client():" in conftest_content

    # Check test_health.py
    test_health_content = (project_path / "tests" / "api" / "test_health.py").read_text()
    assert "def test_health_check(client):" in test_health_content
    assert "def test_root_endpoint(client):" in test_health_content
    assert 'client.get("/api/v1/health")' in test_health_content
    assert "assert response.status_code == 200" in test_health_content


def test_scaffold_docker_files(scaffolder, temp_output_dir):
    """Test that Docker files are correctly created"""
    project_name = "dockerapi"
    project_path = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Check Dockerfile
    dockerfile_content = (project_path / "Dockerfile").read_text()
    assert "FROM python:3.11-slim" in dockerfile_content
    assert "RUN pip install poetry" in dockerfile_content
    assert "EXPOSE 8000" in dockerfile_content

    # Check docker-compose.yml
    compose_content = (project_path / "docker-compose.yml").read_text()
    assert "version:" in compose_content
    assert "services:" in compose_content
    assert "api:" in compose_content
    assert "ports:" in compose_content
    assert '"8000:8000"' in compose_content


def test_scaffold_returns_project_path(scaffolder, temp_output_dir):
    """Test that scaffold returns the correct project path"""
    project_name = "returnapi"

    result = scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    assert isinstance(result, Path)
    assert result.name == project_name
    assert result.parent == temp_output_dir
    assert result.exists()


def test_scaffold_logging(scaffolder, temp_output_dir, caplog):
    """Test that scaffolding produces appropriate log messages"""
    import logging

    caplog.set_level(logging.INFO)

    project_name = "logapi"
    scaffolder.scaffold(
        project_name=project_name,
        output_dir=str(temp_output_dir)
    )

    # Check that appropriate log messages were generated
    assert "Starting scaffolding" in caplog.text
    assert "Project scaffolded successfully" in caplog.text
    assert project_name in caplog.text
