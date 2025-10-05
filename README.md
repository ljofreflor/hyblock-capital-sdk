# Hyblock Capital SDK (Unofficial)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue)](https://python-poetry.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)
[![Unofficial](https://img.shields.io/badge/status-unofficial-orange.svg)](https://github.com/ljofreflor/hyblock-capital-sdk)

**⚠️ UNOFFICIAL SDK** - Python SDK for Hyblock Capital API, automatically generated from OpenAPI/Swagger specification.

> **🚨 IMPORTANT DISCLAIMER**: This is an **UNOFFICIAL SDK** created by @leonardojofre. It is **NOT affiliated with, endorsed by, or officially maintained** by Hyblock Capital. Use at your own risk.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Inicio Rápido](#inicio-rápido)
- [Uso Básico](#uso-básico)
- [Ejemplos](#ejemplos)
- [Desarrollo](#desarrollo)
- [CI/CD y Publicación](#cicd-y-publicación)
- [Testing y Validación](#testing-y-validación)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## ✨ Características

- **Generación automática**: El SDK se genera automáticamente desde la especificación OpenAPI de Hyblock Capital
- **Completamente tipado**: Soporte completo para type hints y autocompletado en IDEs
- **Asíncrono**: Soporte para operaciones síncronas y asíncronas
- **Manejo de errores**: Excepciones personalizadas para diferentes tipos de errores de la API
- **Documentación integrada**: Documentación generada automáticamente con ejemplos
- **Testing incluido**: Suite de tests para validar la funcionalidad
- **Poetry compatible**: Gestión de dependencias moderna y reproducible

## 🚀 Instalación

### Desde PyPI

```bash
pip install hyblock-capital-sdk
```

### Con Poetry (Recomendado)

**Opción 1: Desde PyPI**
```bash
poetry add hyblock-capital-sdk
```

**Opción 2: Desde el repositorio**
```bash
poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git
```

**Opción 3: Para desarrollo**
```bash
poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git --editable
```

### Desarrollo local

```bash
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk
poetry install --with dev
```

## ⚡ Inicio Rápido

### Prerrequisitos

Asegúrate de tener instalado:
- **Python 3.8.1+** (recomendado 3.11.12)
- **Poetry** (gestor de dependencias)
- **Java 8+** (requerido por OpenAPI Generator)
- **pyenv** (recomendado para gestión de versiones)

```bash
# Verificar versiones
python --version
poetry --version
java -version
```

### Configuración rápida

```bash
# Clonar el repositorio
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Configurar versión de Python (recomendado)
pyenv local 3.11.12

# Instalar dependencias
poetry install --with dev

# Verificar instalación
poetry run python -c "import hyblock_capital_sdk; print('✅ SDK instalado correctamente')"
```

## 💻 Uso Básico

### Configuración básica

```python
from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi

# Configurar el cliente
config = Configuration()
client = ApiClient(config)

# Crear instancia de la API
catalog_api = CatalogApi(client)

# Usar la API
try:
    # Ejemplo: obtener información del catálogo
    response = catalog_api.get_catalog()
    print(f"Respuesta: {response}")
except Exception as e:
    print(f"Error: {e}")
```

### Uso asíncrono

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

## 📚 Ejemplos

### Ejemplo básico

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

## 🔧 Desarrollo

### Generación del SDK

El SDK se genera automáticamente desde la especificación OpenAPI de Hyblock Capital:

```bash
# Generar SDK localmente
./generate_sdk.sh

# Verificar cambios
git status
git diff

# Committear cambios
git add .
git commit -m "chore: regenerate SDK from OpenAPI"
```

### Estructura del proyecto

```
hyblock-capital-sdk/
├── README.md                    # Este archivo
├── pyproject.toml              # Configuración Poetry
├── openapi-generator-config.json # Config OpenAPI Generator
├── generate_sdk.sh             # Script de generación
├── Makefile                    # Automatización de comandos
├── .gitignore                  # Exclusiones de Git
├── env.example                 # Ejemplo de variables de entorno
├── hyblock_capital_sdk/        # SDK generado
│   ├── __init__.py
│   ├── api/                    # APIs generadas
│   ├── models/                 # Modelos de datos
│   ├── api_client.py
│   ├── configuration.py
│   └── exceptions.py
├── tests/                      # Tests del SDK
├── examples/                   # Ejemplos de uso
└── docs/                       # Documentación
```

### Comandos de desarrollo

```bash
# Instalar dependencias
poetry install --with dev

# Ejecutar tests
poetry run pytest

# Linting
poetry run flake8 hyblock_capital_sdk/

# Formatear código
poetry run black hyblock_capital_sdk/

# Generar SDK
./generate_sdk.sh

# Build del paquete
poetry build

# Publicar en PyPI
poetry publish
```

## 🚀 CI/CD y Publicación

### Configuración de GitHub Secrets

Para automatizar la publicación en PyPI, configura estos secrets en GitHub:

1. **Ve a tu repositorio** → Settings → Secrets and variables → Actions
2. **Crea estos secrets:**
   - `PYPI_TOKEN`: Token de PyPI (producción)
   - `TEST_PYPI_TOKEN`: Token de TestPyPI (testing)

### Obtener tokens de PyPI

#### Para PyPI (Producción):
1. Ve a [PyPI.org](https://pypi.org) → Account settings → API tokens
2. Crea un token con nombre `hyblock-capital-sdk-ci`
3. **Copia el token generado** (formato: `pypi-...`) - **NO lo compartas**

#### Para TestPyPI (Testing):
1. Ve a [TestPyPI.org](https://test.pypi.org) → Account settings → API tokens
2. Crea un token con nombre `hyblock-capital-sdk-test-ci`
3. **Copia el token generado** (formato: `pypi-...`) - **NO lo compartas**

### Flujo de publicación

1. **Push a main/develop** → Ejecuta tests y linting
2. **Crear tag** → Ejecuta publicación automática a PyPI
3. **Pull Request** → Ejecuta tests y publicación a TestPyPI

### Comandos para publicar

```bash
# Incrementar versión
poetry version patch  # 0.1.0 → 0.1.1
poetry version minor  # 0.1.0 → 0.2.0
poetry version major  # 0.1.0 → 1.0.0

# Crear tag y push
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git tag v$(poetry version -s)
git push origin main
git push origin v$(poetry version -s)
```

## 🧪 Testing y Validación

### Validación Automática de PyPI

El proyecto incluye workflows de CI/CD que validan automáticamente:

#### **1. Test de Instalación desde PyPI**
- Se ejecuta en cada push a `main` y `develop`
- Verifica que el SDK se puede instalar desde PyPI
- Prueba tanto con `pip` como con `Poetry`
- Valida que los componentes principales funcionan

#### **2. Test Post-Publicación**
- Se ejecuta automáticamente después de crear un tag de versión
- Verifica que la versión específica se publicó correctamente
- Confirma que la instalación funciona con la nueva versión
- Valida que aparece en el listado de PyPI

#### **3. Monitoreo de Versiones**
- Se ejecuta cada 6 horas
- Detecta diferencias entre versión del proyecto y PyPI
- Crea issues automáticamente si hay inconsistencias
- Verifica que la última versión en PyPI funciona

### Ejecutar Tests Localmente

```bash
# Tests unitarios
poetry run pytest tests/ -v

# Tests con cobertura
poetry run pytest tests/ --cov=hyblock_capital_sdk --cov-report=html

# Verificar instalación desde PyPI
pip install hyblock-capital-sdk
python -c "import hyblock_capital_sdk; print('✅ Instalación exitosa')"
```

### Workflows de GitHub Actions

- **`ci.yml`**: Pipeline principal con tests, linting y validación de PyPI
- **`pypi-test.yml`**: Test específico de instalación desde PyPI
- **`post-publish-test.yml`**: Validación post-publicación
- **`pypi-monitor.yml`**: Monitoreo continuo de versiones

## 🤝 Contribuir

### Flujo de contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -m 'feat: agregar nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **Abre** un Pull Request

### Estándares de código

- **Python 3.8+** compatible
- **Type hints** obligatorios
- **Docstrings** para todas las funciones públicas
- **Tests** para nueva funcionalidad
- **Linting** con flake8 y black

### Comandos de contribución

```bash
# Instalar dependencias de desarrollo
poetry install --with dev

# Ejecutar tests
poetry run pytest

# Linting
poetry run flake8 hyblock_capital_sdk/
poetry run black hyblock_capital_sdk/
poetry run isort hyblock_capital_sdk/

# Verificar tipos
poetry run mypy hyblock_capital_sdk/
```

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🧹 Limpieza Automática de Ramas

El proyecto incluye un sistema automático de limpieza de ramas:

- **Eliminación automática**: Las ramas `feature/*`, `fix/*`, `hotfix/*` se eliminan automáticamente después del merge
- **Protección**: Las ramas `main` y `develop` nunca se eliminan
- **Workflow**: `.github/workflows/cleanup-branches.yml` maneja la limpieza automática

## 🔗 Enlaces Útiles

- **Repositorio**: [GitHub](https://github.com/ljofreflor/hyblock-capital-sdk)
- **PyPI**: [hyblock-capital-sdk](https://pypi.org/project/hyblock-capital-sdk/)
- **Documentación**: [MkDocs](https://ljofreflor.github.io/hyblock-capital-sdk/)
- **API de Hyblock Capital**: [Documentación](https://media.hyblockcapital.com/document/swagger-dev.json)

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. **Revisa** la documentación
2. **Busca** en los issues existentes
3. **Crea** un nuevo issue si es necesario
4. **Contacta** al mantenedor: ljofre2146@gmail.com

---

**Desarrollado con ❤️ para la comunidad de Hyblock Capital**