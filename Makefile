# Makefile para el SDK de Hyblock Capital

.PHONY: help install generate generate-commit generate-push clean test lint format docs build publish dev-setup

# Variables
PYTHON := poetry run python
PIP := poetry run pip
PYTEST := poetry run pytest
BLACK := poetry run black
FLAKE8 := poetry run flake8
MYPY := poetry run mypy

# Directorios
SDK_DIR := hyblock_capital_sdk
TESTS_DIR := tests
DOCS_DIR := docs

# Ayuda por defecto
help: ## Mostrar este mensaje de ayuda
	@echo "Comandos disponibles:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Configuración de desarrollo
dev-setup: ## Configurar entorno de desarrollo
	@echo "Configurando entorno de desarrollo..."
	@echo "Verificando versión de Python..."
	@if command -v pyenv > /dev/null; then \
		echo "Configurando Python 3.11.12 con pyenv..."; \
		pyenv local 3.11.12; \
	else \
		echo "pyenv no encontrado, usando Python del sistema"; \
	fi
	poetry env use python
	poetry install --with dev
	poetry run pre-commit install
	@echo "Entorno configurado"

install: ## Instalar dependencias del proyecto
	@echo " Instalando dependencias..."
	poetry install
	@echo " Dependencias instaladas"

# Generación del SDK
generate: ## Generar SDK desde OpenAPI
	@echo " Generando SDK desde especificación OpenAPI..."
	./generate_sdk.sh
	@echo " SDK generado exitosamente"

generate-commit: generate ## Generar SDK y crear commit [generate-sdk]
	@echo " Creando commit con cambios del SDK..."
	@if git diff --quiet -- hyblock_capital_sdk; then \
		echo " No hay cambios en SDK, nada para commitear"; \
	else \
		git add hyblock_capital_sdk; \
		git commit -m "chore(generate): update SDK from OpenAPI [generate-sdk]"; \
		echo " Commit creado"; \
	fi

generate-push: ## Generar, commitear y pushear SDK
	@$(MAKE) generate-commit
	@last_msg=$$(git log -1 --pretty=%B 2>/dev/null || true); \
	if echo "$$last_msg" | grep -q "chore(generate): update SDK from OpenAPI"; then \
		echo " Pusheando cambios..."; \
		git push origin $$(git rev-parse --abbrev-ref HEAD); \
	else \
		echo " No hay commit nuevo para pushear"; \
	fi

# Testing
test: ## Ejecutar todos los tests
	@echo " Ejecutando tests..."
	$(PYTEST) $(TESTS_DIR) -v

test-cov: ## Ejecutar tests con reporte de cobertura
	@echo " Ejecutando tests con cobertura..."
	$(PYTEST) $(TESTS_DIR) --cov=$(SDK_DIR) --cov-report=html --cov-report=term-missing

test-unit: ## Ejecutar solo tests unitarios
	@echo " Ejecutando tests unitarios..."
	$(PYTEST) $(TESTS_DIR)/unit -v

test-integration: ## Ejecutar tests de integración
	@echo " Ejecutando tests de integración..."
	$(PYTEST) $(TESTS_DIR)/integration -v

# Linting y formato
lint: ## Ejecutar análisis de código (excluye código generado)
	@echo " Ejecutando análisis de código..."
	$(FLAKE8) --exclude $(SDK_DIR)/api,$(SDK_DIR)/models $(SDK_DIR) $(TESTS_DIR)
	$(MYPY) $(SDK_DIR)

format: ## Formatear código con Black (sin tocar lo generado)
	@echo " Formateando código..."
	$(BLACK) --exclude 'hyblock_capital_sdk/(api|models)/' $(SDK_DIR) $(TESTS_DIR)

format-check: ## Verificar formato sin aplicar cambios (sin tocar lo generado)
	@echo " Verificando formato..."
	$(BLACK) --exclude 'hyblock_capital_sdk/(api|models)/' --check $(SDK_DIR) $(TESTS_DIR)

isort: ## Ordenar imports (excluye código generado)
	@echo "📑 Ordenando imports..."
	poetry run isort --skip-glob 'hyblock_capital_sdk/api/*' --skip-glob 'hyblock_capital_sdk/models/*' $(SDK_DIR) $(TESTS_DIR)

# Verificaciones completas
check: format-check lint test ## Ejecutar todas las verificaciones
	@echo " Todas las verificaciones pasaron"

# Documentación
docs: ## Generar documentación
	@echo " Generando documentación..."
	@mkdir -p $(DOCS_DIR)
	poetry run sphinx-build -b html $(DOCS_DIR) $(DOCS_DIR)/_build

docs-serve: ## Servir documentación localmente
	@echo " Sirviendo documentación en http://localhost:8000"
	$(PYTHON) -m http.server 8000 -d $(DOCS_DIR)/_build

# Build y publicación
build: clean ## Construir paquete para distribución
	@echo " Construyendo paquete..."
	poetry build
	@echo " Paquete construido en dist/"

publish-test: build ## Publicar en PyPI test
	@echo " Publicando en PyPI test..."
	poetry publish --repository testpypi

publish: build ## Publicar en PyPI
	@echo " Publicando en PyPI..."
	poetry publish

# Limpieza
clean: ## Limpiar archivos temporales y de build
	@echo " Limpiando archivos temporales..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf $(DOCS_DIR)/_build/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -name "*.backup.*" -delete
	rm -f swagger.json openapi.json
	@echo " Limpieza completada"

clean-sdk: ## Limpiar SDK generado (mantener respaldo)
	@echo " Limpiando SDK generado..."
	@if [ -d "$(SDK_DIR)" ]; then \
		mv $(SDK_DIR) $(SDK_DIR).backup.$$(date +%Y%m%d_%H%M%S); \
		echo " SDK respaldado y removido"; \
	else \
		echo "ℹ️  No hay SDK para limpiar"; \
	fi

# Utilidades de desarrollo
swagger-download: ## Descargar especificación Swagger
	@echo " Descargando especificación Swagger..."
	curl -f -s -o swagger.json https://media.hyblockcapital.com/document/swagger-dev.json
	@echo " Especificación descargada: swagger.json"

swagger-validate: ## Validar especificación Swagger descargada
	@echo " Validando especificación Swagger..."
	$(PYTHON) -m json.tool swagger.json > /dev/null
	@echo " Especificación válida"

# Información del proyecto
info: ## Mostrar información del proyecto
	@echo " Información del proyecto:"
	@echo "  Nombre: hyblock-capital-sdk"
	@echo "  Versión: $$(poetry version -s)"
	@echo "  Python: $$(poetry run python --version)"
	@echo "  Poetry: $$(poetry --version)"
	@echo "  Directorio SDK: $(SDK_DIR)"
	@echo "  Tests: $(TESTS_DIR)"

# Verificar dependencias
deps-check: ## Verificar dependencias
	@echo " Verificando dependencias..."
	poetry check
	poetry show --outdated

deps-update: ## Actualizar dependencias
	@echo " Actualizando dependencias..."
	poetry update

# Configuración de pre-commit
pre-commit-install: ## Instalar hooks de pre-commit
	@echo "🔧 Instalando hooks de pre-commit..."
	poetry run pre-commit install

pre-commit-run: ## Ejecutar pre-commit en todos los archivos
	@echo " Ejecutando pre-commit..."
	poetry run pre-commit run --all-files

# Operaciones avanzadas
reinstall: clean-sdk generate install ## Reinstalar SDK completo
	@echo " Reinstalación completa terminada"

verify: generate test ## Generar y verificar SDK
	@echo " SDK generado y verificado"

# Release workflow
release-patch: ## Incrementar versión patch y generar release
	poetry version patch
	$(MAKE) clean generate test build
	@echo " Release patch listo"

release-minor: ## Incrementar versión minor y generar release
	poetry version minor
	$(MAKE) clean generate test build
	@echo " Release minor listo"

release-major: ## Incrementar versión major y generar release
	poetry version major
	$(MAKE) clean generate test build
	@echo " Release major listo"

# Debugging
debug-env: ## Mostrar información del entorno
	@echo " Información del entorno:"
	@echo "  PWD: $$(pwd)"
	@echo "  PATH: $$PATH"
	@echo "  Python executable: $$(which python)"
	@echo "  Poetry executable: $$(which poetry)"
	@echo "  Java version: $$(java -version 2>&1 | head -n 1 || echo 'Java no encontrado')"
	@echo "  OpenAPI Generator: $$(openapi-generator-cli version 2>/dev/null || echo 'No encontrado')"

# Ejemplo de uso rápido
example: ## Ejecutar ejemplo básico del SDK
	@echo " Ejecutando ejemplo básico..."
	@if [ -f "examples/basic_usage.py" ]; then \
		$(PYTHON) examples/basic_usage.py; \
	else \
		echo "⚠️  Archivo de ejemplo no encontrado. Genera el SDK primero."; \
	fi

# ======================================================================
# PUBLICACIÓN EN PyPI
# ======================================================================

.PHONY: build-dist upload-test upload-pypi clean-dist

build-dist: clean-dist ## Construir distribución para PyPI
	@echo " Construyendo distribución del paquete..."
	poetry build
	@echo " Distribución creada en dist/"

clean-dist: ## Limpiar archivos de distribución
	@echo " Limpiando archivos de distribución..."
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo " Archivos de distribución eliminados"

check-dist: build-dist ## Verificar la distribución antes de subir
	@echo " Verificando distribución..."
	poetry run python -m twine check dist/*
	@echo " Verificación completada"

upload-test: build-dist ## Subir a PyPI Test
	@echo " Subiendo a PyPI Test (testpypi)..."
	@echo "⚠️  Necesitarás tu token de PyPI Test"
	poetry run python -m twine upload --repository testpypi dist/*
	@echo " Paquete subido a PyPI Test"
	@echo " Instalar desde test: pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk"

upload-pypi: build-dist ## Subir a PyPI oficial
	@echo "🚨 SUBIENDO A PyPI OFICIAL 🚨"
	@echo "⚠️  Esta acción publicará el paquete públicamente"
	@read -p "¿Estás seguro? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo " Subiendo a PyPI oficial..."; \
		poetry run python -m twine upload dist/*; \
		echo " Paquete publicado en PyPI"; \
		echo " Instalar: pip install hyblock-capital-sdk"; \
	else \
		echo "❌ Publicación cancelada"; \
	fi

install-publishing-tools: ## Instalar herramientas de publicación
	@echo " Instalando herramientas de publicación..."
	poetry add --group dev twine
	@echo " Herramientas instaladas"

pypi-help: ## Mostrar ayuda para publicación en PyPI
	@echo ""
	@echo "🚀 GUÍA DE PUBLICACIÓN EN PyPI:"
	@echo "================================"
	@echo ""
	@echo "1. Preparar el paquete:"
	@echo "   make check          # Verificar calidad del código"
	@echo "   make test           # Ejecutar todos los tests"
	@echo "   make clean-dist     # Limpiar distribuciones anteriores"
	@echo ""
	@echo "2. Construir y verificar:"
	@echo "   make build-dist     # Construir distribución"
	@echo "   make check-dist     # Verificar distribución"
	@echo ""
	@echo "3. Subir a PyPI Test primero:"
	@echo "   make upload-test    # Probar en testpypi"
	@echo ""
	@echo "4. Probar instalación desde test:"
	@echo "   pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk"
	@echo ""
	@echo "5. Si todo funciona, subir a PyPI oficial:"
	@echo "   make upload-pypi    # Publicar oficialmente"
	@echo ""
	@echo "📋 REQUISITOS PREVIOS:"
	@echo "- Cuenta en PyPI y PyPI Test"
	@echo "- Tokens de autenticación configurados"
	@echo "- make install-publishing-tools"
	@echo ""
	@echo "🔗 Enlaces útiles:"
	@echo "- PyPI: https://pypi.org/"
	@echo "- PyPI Test: https://test.pypi.org/"
	@echo "- Twine docs: https://twine.readthedocs.io/"
	@echo ""
