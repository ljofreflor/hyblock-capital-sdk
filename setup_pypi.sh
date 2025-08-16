#!/bin/bash

# Script de configuración automatizada para PyPI
# Uso: ./setup_pypi.sh

set -e  # Salir si hay errores

echo "🚀 CONFIGURACIÓN AUTOMATIZADA PARA PyPI"
echo "======================================="
echo

# Verificar si estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: No se encontró pyproject.toml"
    echo "   Ejecuta este script desde la raíz del proyecto"
    exit 1
fi

# Función para pedir confirmación
confirm() {
    while true; do
        read -p "$1 (y/N): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            "" ) return 1;;
            * ) echo "Por favor responde 'y' o 'n'.";;
        esac
    done
}

# Función para configurar .pypirc
setup_pypirc() {
    echo "🔑 Configurando archivo .pypirc..."
    
    PYPIRC_FILE="$HOME/.pypirc"
    
    if [ -f "$PYPIRC_FILE" ]; then
        if confirm "El archivo .pypirc ya existe. ¿Sobrescribir?"; then
            echo "   Respaldando .pypirc existente..."
            cp "$PYPIRC_FILE" "$PYPIRC_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        else
            echo "   Saltando configuración de .pypirc"
            return 0
        fi
    fi
    
    echo "   Necesitas tus tokens de API de PyPI:"
    echo "   - PyPI Test: https://test.pypi.org/manage/account/token/"
    echo "   - PyPI Oficial: https://pypi.org/manage/account/token/"
    echo
    
    read -p "   Token de PyPI Test (pypi-...): " TEST_TOKEN
    read -p "   Token de PyPI Oficial (pypi-...): " PROD_TOKEN
    
    if [ -z "$TEST_TOKEN" ] || [ -z "$PROD_TOKEN" ]; then
        echo "❌ Error: Necesitas ambos tokens"
        exit 1
    fi
    
    # Crear archivo .pypirc
    cat > "$PYPIRC_FILE" << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = $PROD_TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $TEST_TOKEN
EOF
    
    # Asegurar permisos correctos
    chmod 600 "$PYPIRC_FILE"
    
    echo "✅ Archivo .pypirc configurado correctamente"
}

# Función para verificar herramientas
check_tools() {
    echo "🔧 Verificando herramientas necesarias..."
    
    # Verificar Poetry
    if ! command -v poetry &> /dev/null; then
        echo "❌ Poetry no está instalado"
        echo "   Instala Poetry: https://python-poetry.org/docs/#installation"
        exit 1
    fi
    echo "✅ Poetry encontrado: $(poetry --version)"
    
    # Verificar que twine esté instalado
    if ! poetry run python -c "import twine" &> /dev/null; then
        echo "   Instalando twine..."
        poetry run pip install twine
    fi
    echo "✅ Twine disponible"
    
    # Verificar Python
    PYTHON_VERSION=$(poetry run python --version)
    echo "✅ Python: $PYTHON_VERSION"
}

# Función para preparar el paquete
prepare_package() {
    echo "📦 Preparando el paquete..."
    
    # Verificar tests
    echo "   Ejecutando tests..."
    if ! make test > /dev/null 2>&1; then
        echo "⚠️  Algunos tests fallaron. ¿Continuar?"
        if ! confirm "   ¿Proceder de todas formas?"; then
            echo "❌ Preparación cancelada"
            exit 1
        fi
    fi
    echo "✅ Tests ejecutados"
    
    # Formatear código
    echo "   Formateando código..."
    make format > /dev/null 2>&1
    echo "✅ Código formateado"
    
    # Construir distribución
    echo "   Construyendo distribución..."
    make build-dist > /dev/null 2>&1
    echo "✅ Distribución construida"
    
    # Verificar distribución
    echo "   Verificando distribución..."
    make check-dist > /dev/null 2>&1
    echo "✅ Distribución verificada"
}

# Función principal de subida
upload_package() {
    echo "🚀 Proceso de subida..."
    
    # Subir a Test PyPI primero
    echo "   Subiendo a PyPI Test..."
    if confirm "   ¿Subir a PyPI Test primero?"; then
        poetry run python -m twine upload --repository testpypi dist/*
        echo "✅ Subido a PyPI Test"
        echo
        echo "🧪 PRUEBA LA INSTALACIÓN DESDE TEST:"
        echo "   pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk"
        echo "   python -c \"import hyblock_capital_sdk; print('OK')\""
        echo
        
        if confirm "   ¿La instalación desde test funcionó correctamente?"; then
            echo "✅ Test confirmado, procediendo a PyPI oficial"
        else
            echo "❌ Corrige los problemas antes de subir a PyPI oficial"
            exit 1
        fi
    fi
    
    # Subir a PyPI oficial
    echo
    echo "🚨 SUBIENDO A PyPI OFICIAL 🚨"
    echo "   Esta acción publicará el paquete públicamente"
    
    if confirm "   ¿Estás seguro de subir a PyPI oficial?"; then
        poetry run python -m twine upload dist/*
        echo "✅ ¡Paquete publicado en PyPI oficial!"
        echo
        echo "🎉 ¡ÉXITO! El SDK está ahora disponible públicamente:"
        echo "   pip install hyblock-capital-sdk"
        echo "   https://pypi.org/project/hyblock-capital-sdk/"
    else
        echo "❌ Subida a PyPI oficial cancelada"
    fi
}

# Script principal
main() {
    echo "Este script te ayudará a configurar y subir el SDK a PyPI."
    echo
    
    if confirm "¿Continuar con la configuración automática?"; then
        check_tools
        setup_pypirc
        prepare_package
        upload_package
    else
        echo "❌ Configuración cancelada"
        echo "   Puedes usar los comandos manuales:"
        echo "   make pypi-help"
        exit 1
    fi
}

# Ejecutar script principal
main
