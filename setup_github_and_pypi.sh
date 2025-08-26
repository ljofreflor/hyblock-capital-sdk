#!/bin/bash

# Script completo para configurar GitHub y PyPI
# Uso: ./setup_github_and_pypi.sh

set -e

echo "🚀 CONFIGURACIÓN COMPLETA: GITHUB + PyPI"
echo "========================================"
echo

# Función para verificar si el comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para confirmar acciones
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

# Verificar estado de git
check_git_status() {
    echo "📋 VERIFICANDO ESTADO DE GIT..."
    
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ No es un repositorio git"
        exit 1
    fi
    
    if [ -z "$(git remote get-url origin 2>/dev/null)" ]; then
        echo "⚠️  No hay remoto configurado"
        NEED_REMOTE=true
    else
        echo "✅ Remoto ya configurado: $(git remote get-url origin)"
        NEED_REMOTE=false
    fi
    
    # Verificar si hay commits
    if ! git rev-parse HEAD >/dev/null 2>&1; then
        echo "⚠️  No hay commits. Haciendo commit inicial..."
        git add .
        git commit -m "feat: initial release of Hyblock Capital SDK"
    fi
    
    echo "✅ Estado de git verificado"
}

# Configurar remoto de GitHub
setup_github_remote() {
    if [ "$NEED_REMOTE" = true ]; then
        echo
        echo "🔗 CONFIGURANDO GITHUB..."
        echo
        echo "Primero necesitas crear el repositorio en GitHub:"
        echo "1. Ve a: https://github.com/new"
        echo "2. Repository name: hyblock-capital-sdk"
        echo "3. Description: SDK no oficial para la API de Hyblock Capital"
        echo "4. Público (necesario para PyPI)"
        echo "5. NO inicializar con README, .gitignore o LICENSE (ya los tenemos)"
        echo "6. Click 'Create repository'"
        echo
        
        if confirm "¿Ya creaste el repositorio en GitHub?"; then
            echo "   Configurando remoto..."
            git remote add origin https://github.com/ljofreflor/hyblock-capital-sdk.git
            git branch -M main
            echo "✅ Remoto configurado"
        else
            echo "❌ Configura GitHub primero"
            exit 1
        fi
    fi
}

# Subir código a GitHub
push_to_github() {
    echo
    echo "📤 SUBIENDO CÓDIGO A GITHUB..."
    
    if confirm "¿Subir código a GitHub?"; then
        git push -u origin main
        echo "✅ Código subido a GitHub"
        echo "📍 Repositorio disponible en: https://github.com/ljofreflor/hyblock-capital-sdk"
    else
        echo "⚠️  Código no subido a GitHub"
        return 1
    fi
}

# Configurar PyPI
setup_pypi() {
    echo
    echo "🐍 CONFIGURANDO PyPI..."
    
    if confirm "¿Configurar PyPI ahora?"; then
        # Verificar si twine está instalado
        if ! poetry run python -c "import twine" >/dev/null 2>&1; then
            echo "   Instalando twine..."
            poetry run pip install twine
        fi
        
        # Verificar .pypirc
        if [ ! -f "$HOME/.pypirc" ]; then
            echo "   Necesitas configurar tokens de PyPI"
            echo "   PyPI Test: https://test.pypi.org/manage/account/token/"
            echo "   PyPI Oficial: https://pypi.org/manage/account/token/"
            echo
            
            read -p "   Token de PyPI Test (pypi-...): " TEST_TOKEN
            read -p "   Token de PyPI Oficial (pypi-...): " PROD_TOKEN
            
            if [ -n "$TEST_TOKEN" ] && [ -n "$PROD_TOKEN" ]; then
                cat > "$HOME/.pypirc" << EOF
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
                chmod 600 "$HOME/.pypirc"
                echo "✅ .pypirc configurado"
            else
                echo "⚠️  Tokens no proporcionados. Puedes configurarlos después con:"
                echo "      ./setup_pypi.sh"
                return 1
            fi
        else
            echo "✅ .pypirc ya existe"
        fi
        
        # Construir distribución
        echo "   Construyendo distribución..."
        make build-dist >/dev/null 2>&1
        make check-dist >/dev/null 2>&1
        echo "✅ Distribución construida y verificada"
        
        return 0
    else
        echo "⚠️  PyPI no configurado. Puedes hacerlo después con:"
        echo "      ./setup_pypi.sh"
        return 1
    fi
}

# Subir a PyPI Test
upload_to_test_pypi() {
    echo
    echo "🧪 SUBIENDO A PyPI TEST..."
    
    if confirm "¿Subir a PyPI Test primero?"; then
        poetry run python -m twine upload --repository testpypi dist/*
        echo "✅ Subido a PyPI Test"
        echo "🧪 Prueba la instalación:"
        echo "   pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk"
        echo
        
        if confirm "   ¿La instalación desde test funcionó?"; then
            return 0
        else
            echo "❌ Corrige problemas antes de subir a PyPI oficial"
            return 1
        fi
    else
        echo "⚠️  No subido a PyPI Test"
        return 1
    fi
}

# Subir a PyPI oficial
upload_to_pypi() {
    echo
    echo "🚨 SUBIENDO A PyPI OFICIAL 🚨"
    echo "   Esta acción publicará el paquete públicamente"
    
    if confirm "   ¿Subir a PyPI oficial?"; then
        poetry run python -m twine upload dist/*
        echo "✅ ¡PUBLICADO EN PyPI OFICIAL!"
        echo "📦 Los usuarios pueden instalarlo con:"
        echo "   pip install hyblock-capital-sdk"
        echo "🌐 Disponible en: https://pypi.org/project/hyblock-capital-sdk/"
        return 0
    else
        echo "❌ No subido a PyPI oficial"
        return 1
    fi
}

# Script principal
main() {
    echo "Este script configura GitHub y PyPI automáticamente."
    echo
    
    if confirm "¿Continuar con la configuración completa?"; then
        
        # Verificar git
        check_git_status
        
        # Configurar GitHub
        setup_github_remote
        
        # Subir a GitHub
        if push_to_github; then
            GITHUB_OK=true
        else
            GITHUB_OK=false
        fi
        
        # Configurar PyPI
        if setup_pypi; then
            PYPI_OK=true
        else
            PYPI_OK=false
        fi
        
        # Si PyPI está configurado, continuar con uploads
        if [ "$PYPI_OK" = true ]; then
            if upload_to_test_pypi; then
                upload_to_pypi
            fi
        fi
        
        # Resumen final
        echo
        echo "🎉 CONFIGURACIÓN COMPLETADA"
        echo "=========================="
        
        if [ "$GITHUB_OK" = true ]; then
            echo "✅ GitHub: https://github.com/ljofreflor/hyblock-capital-sdk"
        else
            echo "⚠️  GitHub: Pendiente"
        fi
        
        if [ "$PYPI_OK" = true ]; then
            echo "✅ PyPI: Configurado (verifica en https://pypi.org/project/hyblock-capital-sdk/)"
        else
            echo "⚠️  PyPI: Pendiente (usa ./setup_pypi.sh)"
        fi
        
        echo
        echo "📚 Próximos pasos:"
        echo "- Los clientes pueden instalar: pip install hyblock-capital-sdk"
        echo "- Para updates: actualiza versión y ejecuta make upload-pypi"
        echo "- Para regenerar SDK: ./generate_sdk.sh"
        
    else
        echo "❌ Configuración cancelada"
        echo
        echo "📝 Comandos manuales disponibles:"
        echo "   ./setup_pypi.sh          # Solo PyPI"
        echo "   git remote add origin ... # Solo GitHub"
        echo "   make pypi-help           # Ayuda PyPI"
    fi
}

# Ejecutar
main
