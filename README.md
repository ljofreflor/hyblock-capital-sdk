# Hyblock Capital SDK (Unofficial)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue)](https://python-poetry.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)
[![Unofficial](https://img.shields.io/badge/status-unofficial-orange.svg)](https://github.com/ljofreflor/hyblock-capital-sdk)

**UNOFFICIAL SDK** - Python SDK for Hyblock Capital API, automatically generated from OpenAPI/Swagger specification.

> **IMPORTANT DISCLAIMER**: This is an **UNOFFICIAL SDK** created by @leonardojofre. It is **NOT affiliated with, endorsed by, or officially maintained** by Hyblock Capital. Use at your own risk.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Examples](#examples)
- [Development](#development)
- [CI/CD and Publishing](#cicd-and-publishing)
- [Testing and Validation](#testing-and-validation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automatic generation**: SDK is automatically generated from Hyblock Capital's OpenAPI specification
- **Fully typed**: Complete support for type hints and IDE autocompletion
- **Asynchronous**: Support for both synchronous and asynchronous operations
- **Error handling**: Custom exceptions for different types of API errors
- **Integrated documentation**: Automatically generated documentation with examples
- **Testing included**: Test suite to validate functionality
- **Poetry compatible**: Modern and reproducible dependency management

## Installation

### From PyPI

```bash
pip install hyblock-capital-sdk
```

### With Poetry (Recommended)

**Option 1: From PyPI**
```bash
poetry add hyblock-capital-sdk
```

**Option 2: From repository**
```bash
poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git
```

**Option 3: For development**
```bash
poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git --editable
```

### Local development

```bash
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk
poetry install --with dev
```

## Quick Start

### Prerequisites

Make sure you have installed:
- **Python 3.8.1+** (recommended 3.11.12)
- **Poetry** (dependency manager)
- **Java 8+** (required by OpenAPI Generator)
- **pyenv** (recommended for version management)

```bash
# Check versions
python --version
poetry --version
java -version
```

### Quick setup

```bash
# Clone the repository
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Configure Python version (recommended)
pyenv local 3.11.12

# Install dependencies
poetry install --with dev

# Verify installation
poetry run python -c "import hyblock_capital_sdk; print('SDK installed correctly')"
```

## Basic Usage

### Basic configuration

```python
from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi

# Configure the client
config = Configuration()
client = ApiClient(config)

# Create API instance
catalog_api = CatalogApi(client)

# Use the API
try:
    # Example: get catalog information
    response = catalog_api.get_catalog()
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
```

### Asynchronous usage

```python
import asyncio
from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi

async def main():
    config = Configuration()
    client = ApiClient(config)
    catalog_api = CatalogApi(client)
    
    try:
        response = await catalog_api.get_catalog()
        print(f"Respuesta: {response}")
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
asyncio.run(main())
```

## Examples

### Basic example

```python
from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi

def main():
    # Configurar cliente
    config = Configuration()
    client = ApiClient(config)
    
    # Crear instancia de API
    catalog_api = CatalogApi(client)
    
    try:
        # Obtener catálogo
        catalog = catalog_api.get_catalog()
        print("Catálogo obtenido:", catalog)
        
    except Exception as e:
        print(f"Error al obtener catálogo: {e}")

if __name__ == "__main__":
    main()
```

### Ejemplo con manejo de errores

```python
from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi
from hyblock_capital_sdk.exceptions import ApiException

def main():
    config = Configuration()
    client = ApiClient(config)
    catalog_api = CatalogApi(client)
    
    try:
        catalog = catalog_api.get_catalog()
        print("Éxito:", catalog)
        
    except ApiException as e:
        print(f"Error de API: {e.status} - {e.reason}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
```

## Development

### SDK Generation

The SDK is automatically generated from Hyblock Capital's OpenAPI specification:

```bash
# Generate SDK locally
./generate_sdk.sh

# Check changes
git status
git diff

# Commit changes
git add .
git commit -m "chore: regenerate SDK from OpenAPI"
```

### Project structure

```
hyblock-capital-sdk/
├── README.md                    # This file
├── pyproject.toml              # Poetry configuration
├── openapi-generator-config.json # OpenAPI Generator config
├── generate_sdk.sh             # Generation script
├── Makefile                    # Command automation
├── .gitignore                  # Git exclusions
├── env.example                 # Environment variables example
├── hyblock_capital_sdk/        # Generated SDK
│   ├── __init__.py
│   ├── api/                    # Generated APIs
│   ├── models/                 # Data models
│   ├── api_client.py
│   ├── configuration.py
│   └── exceptions.py
├── tests/                      # SDK tests
├── examples/                   # Usage examples
└── docs/                       # Documentation
```

### Development commands

```bash
# Install dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Linting
poetry run flake8 hyblock_capital_sdk/

# Format code
poetry run black hyblock_capital_sdk/

# Generate SDK
./generate_sdk.sh

# Build package
poetry build

# Publish to PyPI
poetry publish
```

## CI/CD and Publishing

### GitHub Secrets Configuration

To automate publishing to PyPI, configure these secrets in GitHub:

1. **Go to your repository** → Settings → Secrets and variables → Actions
2. **Create these secrets:**
   - `PYPI_TOKEN`: PyPI token (production)
   - `TEST_PYPI_TOKEN`: TestPyPI token (testing)

### Get PyPI Tokens

#### For PyPI (Production):
1. Go to [PyPI.org](https://pypi.org) → Account settings → API tokens
2. Create a token named `hyblock-capital-sdk-ci`
3. **Copy the generated token** (format: `pypi-...`) - **DO NOT share it**

#### For TestPyPI (Testing):
1. Go to [TestPyPI.org](https://test.pypi.org) → Account settings → API tokens
2. Create a token named `hyblock-capital-sdk-test-ci`
3. **Copy the generated token** (format: `pypi-...`) - **DO NOT share it**

### Publishing workflow

1. **Push to main/develop** → Runs tests and linting
2. **Create tag** → Executes automatic publication to PyPI
3. **Pull Request** → Runs tests and publishes to TestPyPI

### Publishing commands

```bash
# Increment version
poetry version patch  # 0.1.0 → 0.1.1
poetry version minor  # 0.1.0 → 0.2.0
poetry version major  # 0.1.0 → 1.0.0

# Create tag and push
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git tag v$(poetry version -s)
git push origin main
git push origin v$(poetry version -s)
```

## Testing and Validation

### Automatic PyPI Validation

The project includes CI/CD workflows that automatically validate:

#### **1. PyPI Installation Test**
- Runs on every push to `main` and `develop`
- Verifies that the SDK can be installed from PyPI
- Tests with both `pip` and `Poetry`
- Validates that main components work

#### **2. Post-Publication Test**
- Runs automatically after creating a version tag
- Verifies that the specific version was published correctly
- Confirms that installation works with the new version
- Validates that it appears in the PyPI listing

#### **3. Version Monitoring**
- Runs every 6 hours
- Detects differences between project version and PyPI
- Creates issues automatically if there are inconsistencies
- Verifies that the latest version on PyPI works

### Run Tests Locally

```bash
# Unit tests
poetry run pytest tests/ -v

# Tests with coverage
poetry run pytest tests/ --cov=hyblock_capital_sdk --cov-report=html

# Verify installation from PyPI
pip install hyblock-capital-sdk
python -c "import hyblock_capital_sdk; print('Installation successful')"
```

### GitHub Actions Workflows

- **`ci.yml`**: Main pipeline with tests, linting and PyPI validation
- **`pypi-test.yml`**: Specific PyPI installation test
- **`post-publish-test.yml`**: Post-publication validation
- **`pypi-monitor.yml`**: Continuous version monitoring

## Contributing

### Contribution workflow

1. **Fork** the repository
2. **Create** a branch for your feature: `git checkout -b feature/new-functionality`
3. **Commit** your changes: `git commit -m 'feat: add new functionality'`
4. **Push** to the branch: `git push origin feature/new-functionality`
5. **Open** a Pull Request

### Code standards

- **Python 3.8+** compatible
- **Type hints** required
- **Docstrings** for all public functions
- **Tests** for new functionality
- **Linting** with flake8 and black

### Contribution commands

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Linting
poetry run flake8 hyblock_capital_sdk/
poetry run black hyblock_capital_sdk/
poetry run isort hyblock_capital_sdk/

# Type checking
poetry run mypy hyblock_capital_sdk/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Automatic Branch Cleanup

The project includes an automatic branch cleanup system:

- **Automatic deletion**: `feature/*`, `fix/*`, `hotfix/*` branches are automatically deleted after merge
- **Protection**: `main` and `develop` branches are never deleted
- **Workflow**: `.github/workflows/cleanup-branches.yml` handles automatic cleanup

## Useful Links

- **Repository**: [GitHub](https://github.com/ljofreflor/hyblock-capital-sdk)
- **PyPI**: [hyblock-capital-sdk](https://pypi.org/project/hyblock-capital-sdk/)
- **Documentation**: [MkDocs](https://ljofreflor.github.io/hyblock-capital-sdk/)
- **Hyblock Capital API**: [Documentation](https://media.hyblockcapital.com/document/swagger-dev.json)

## Support

If you encounter any issues or have questions:

1. **Check** the documentation
2. **Search** existing issues
3. **Create** a new issue if needed
4. **Contact** the maintainer: ljofre2146@gmail.com

---

**Developed for the Hyblock Capital community**