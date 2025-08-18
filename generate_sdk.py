#!/usr/bin/env python3
"""
Script Python para generar el SDK de Hyblock Capital desde OpenAPI.

Este script automatiza todo el proceso de generación, desde la descarga
de la especificación hasta la configuración final del proyecto.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any
import urllib.request
from urllib.error import URLError

# Configuración
SWAGGER_URL = "https://api.hyblock.capital/swagger.json"
CONFIG_FILE = "openapi-generator-config.json" 
PROJECT_DIR = Path(__file__).parent
SDK_DIR = PROJECT_DIR / "hyblock_capital_sdk"

class Colors:
    """Códigos de color para output en terminal."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def print_colored(message: str, color: str = Colors.NC):
    """Imprime mensaje con color."""
    print(f"{color}{message}{Colors.NC}")

def check_java_installation() -> bool:
    """Verifica que Java esté instalado."""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_openapi_generator() -> bool:
    """Verifica que OpenAPI Generator esté disponible."""
    try:
        result = subprocess.run(
            ["openapi-generator-cli", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_openapi_generator():
    """Instala OpenAPI Generator CLI."""
    print_colored("⚠️  Instalando OpenAPI Generator CLI...", Colors.YELLOW)
    try:
        subprocess.run([
            "poetry", "run", "pip", "install", "openapi-generator-cli"
        ], check=True)
        print_colored("✅ OpenAPI Generator CLI instalado", Colors.GREEN)
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error instalando OpenAPI Generator: {e}", Colors.RED)
        sys.exit(1)

def download_swagger_spec(url: str, output_file: Path) -> bool:
    """Descarga la especificación OpenAPI."""
    print_colored(f"📥 Descargando especificación desde {url}...", Colors.BLUE)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        
        with open(output_file, 'wb') as f:
            f.write(data)
        
        # Verificar que sea JSON válido
        with open(output_file, 'r') as f:
            json.load(f)
        
        print_colored("✅ Especificación descargada y validada", Colors.GREEN)
        return True
        
    except URLError as e:
        print_colored(f"❌ Error descargando especificación: {e}", Colors.RED)
        return False
    except json.JSONDecodeError:
        print_colored("❌ Error: Archivo no es JSON válido", Colors.RED)
        return False

def generate_client(swagger_file: Path, output_dir: Path, config_file: Path) -> bool:
    """Genera el cliente usando OpenAPI Generator."""
    print_colored("⚙️  Generando cliente con OpenAPI Generator...", Colors.BLUE)
    
    try:
        cmd = [
            "openapi-generator-cli", "generate",
            "-i", str(swagger_file),
            "-g", "python",
            "-o", str(output_dir),
            "-c", str(config_file),
            "--additional-properties",
            "packageName=hyblock_capital_sdk,pythonPackageName=hyblock_capital_sdk"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print_colored("✅ Cliente generado exitosamente", Colors.GREEN)
        return True
        
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error generando cliente: {e}", Colors.RED)
        print_colored(f"Stdout: {e.stdout}", Colors.YELLOW)
        print_colored(f"Stderr: {e.stderr}", Colors.YELLOW)
        return False

def organize_generated_files(temp_dir: Path, target_dir: Path) -> bool:
    """Organiza los archivos generados en la estructura del proyecto."""
    print_colored("📦 Organizando archivos generados...", Colors.BLUE)
    
    try:
        generated_sdk = temp_dir / "hyblock_capital_sdk"
        
        if not generated_sdk.exists():
            print_colored("❌ Error: Directorio del SDK generado no encontrado", Colors.RED)
            return False
        
        # Respaldar directorio existente si existe
        if target_dir.exists():
            backup_name = f"{target_dir}.backup"
            if Path(backup_name).exists():
                shutil.rmtree(backup_name)
            shutil.move(str(target_dir), backup_name)
            print_colored(f"⚠️  Directorio existente respaldado como {backup_name}", Colors.YELLOW)
        
        # Mover el nuevo SDK
        shutil.move(str(generated_sdk), str(target_dir))
        print_colored(f"✅ SDK movido a {target_dir}", Colors.GREEN)
        
        # Copiar archivos útiles
        useful_files = ["setup.py", "requirements.txt", "README.md"]
        for file_name in useful_files:
            src_file = temp_dir / file_name
            if src_file.exists():
                dst_file = PROJECT_DIR / f"{file_name}.generated"
                shutil.copy2(str(src_file), str(dst_file))
                print_colored(f"✅ {file_name} copiado como referencia", Colors.GREEN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Error organizando archivos: {e}", Colors.RED)
        return False

def install_dependencies():
    """Instala dependencias del proyecto."""
    print_colored("📦 Instalando dependencias con Poetry...", Colors.BLUE)
    
    try:
        subprocess.run(["poetry", "install"], check=True, cwd=PROJECT_DIR)
        print_colored("✅ Dependencias instaladas", Colors.GREEN)
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error instalando dependencias: {e}", Colors.RED)

def verify_installation():
    """Verifica que el SDK se pueda importar."""
    print_colored("🧪 Verificando instalación...", Colors.BLUE)
    
    try:
        result = subprocess.run([
            "poetry", "run", "python", "-c", 
            "import hyblock_capital_sdk; print('✅ Importación exitosa')"
        ], check=True, capture_output=True, text=True, cwd=PROJECT_DIR)
        
        print_colored("✅ SDK verificado correctamente", Colors.GREEN)
        return True
        
    except subprocess.CalledProcessError as e:
        print_colored("❌ Error verificando SDK", Colors.RED)
        print_colored(f"Error: {e.stderr}", Colors.YELLOW)
        return False

def format_code():
    """Aplica formato al código generado."""
    print_colored("🎨 Aplicando formato con Black...", Colors.BLUE)
    
    try:
        # Verificar si Black está disponible
        subprocess.run(["poetry", "run", "black", "--version"], 
                     check=True, capture_output=True, cwd=PROJECT_DIR)
        
        # Aplicar formato
        subprocess.run([
            "poetry", "run", "black", str(SDK_DIR)
        ], check=True, cwd=PROJECT_DIR)
        
        print_colored("✅ Formato aplicado", Colors.GREEN)
        
    except subprocess.CalledProcessError:
        print_colored("⚠️  Black no disponible, saltando formato", Colors.YELLOW)

def main():
    """Función principal del script."""
    print_colored("🚀 Generando SDK de Hyblock Capital desde OpenAPI...", Colors.BLUE)
    
    # Verificar requisitos
    if not check_java_installation():
        print_colored("❌ Error: Java no está instalado", Colors.RED)
        print_colored("💡 Instala Java desde: https://adoptium.net/", Colors.YELLOW)
        sys.exit(1)
    
    if not check_openapi_generator():
        install_openapi_generator()
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        swagger_file = temp_path / "swagger.json"
        output_dir = temp_path / "generated"
        config_file = PROJECT_DIR / CONFIG_FILE
        
        # Verificar que existe el archivo de configuración
        if not config_file.exists():
            print_colored(f"❌ Error: Archivo de configuración no encontrado: {config_file}", Colors.RED)
            sys.exit(1)
        
        # Proceso de generación
        steps = [
            ("Descargar especificación", lambda: download_swagger_spec(SWAGGER_URL, swagger_file)),
            ("Generar cliente", lambda: generate_client(swagger_file, output_dir, config_file)),
            ("Organizar archivos", lambda: organize_generated_files(output_dir, SDK_DIR)),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print_colored(f"❌ Falló el paso: {step_name}", Colors.RED)
                sys.exit(1)
    
    # Pasos finales
    install_dependencies()
    
    if verify_installation():
        format_code()
        
        print_colored("🎉 ¡SDK generado exitosamente!", Colors.GREEN)
        print_colored(f"📖 Ubicación del SDK: {SDK_DIR}", Colors.BLUE)
        print_colored("📝 Para usar el SDK:", Colors.BLUE)
        print_colored("   poetry add ./hyblock-capital-sdk", Colors.YELLOW)
        print_colored("   from hyblock_capital_sdk import ApiClient", Colors.YELLOW)
        
        print_colored("📋 Próximos pasos recomendados:", Colors.BLUE)
        print_colored("   1. Revisar documentación generada", Colors.YELLOW)
        print_colored("   2. Ejecutar tests: poetry run pytest", Colors.YELLOW)
        print_colored("   3. Crear ejemplos de uso", Colors.YELLOW)
    else:
        print_colored("❌ La generación falló en la verificación", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
