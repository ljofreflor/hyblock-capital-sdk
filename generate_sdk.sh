#!/bin/bash

# Script para generar el SDK de Hyblock Capital desde la especificación OpenAPI
# Este script automatiza el proceso de generación del cliente Python

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
SWAGGER_URL="https://media.hyblockcapital.com/document/swagger-dev.json"
SWAGGER_FILE="swagger.json"
OUTPUT_DIR="./generated"
FINAL_DIR="./hyblock_capital_sdk"
CONFIG_FILE="openapi-generator-config.json"

echo -e "${BLUE}Generando SDK de Hyblock Capital desde OpenAPI...${NC}"

# Verificar que Java esté instalado
if ! command -v java &> /dev/null; then
    echo -e "${RED}Error: Java no está instalado. OpenAPI Generator requiere Java.${NC}"
    echo -e "${YELLOW}Instala Java desde: https://adoptium.net/${NC}"
    exit 1
fi

# Verificar que OpenAPI Generator esté disponible
if ! command -v openapi-generator-cli &> /dev/null; then
    echo -e "${YELLOW}  OpenAPI Generator CLI no encontrado. Instalando...${NC}"
    poetry run pip install openapi-generator-cli
fi

# Paso 1: Descargar la especificación OpenAPI de Hyblock Capital
echo -e "${BLUE}Descargando especificación OpenAPI desde ${SWAGGER_URL}...${NC}"
# Intentar descarga con retry logic
download_success=false
for attempt in {1..3}; do
    echo -e "${YELLOW}Intento $attempt de 3...${NC}"
    if curl -f -s --connect-timeout 15 --max-time 30 -o "$SWAGGER_FILE" "$SWAGGER_URL"; then
        echo -e "${GREEN}✅ Especificación descargada exitosamente${NC}"
        download_success=true
        break
    else
        echo -e "${RED}⚠️ Intento $attempt falló${NC}"
        if [ $attempt -lt 3 ]; then
            echo -e "${YELLOW}Reintentando en 5 segundos...${NC}"
            sleep 5
        fi
    fi
done

if [ "$download_success" = false ]; then
    echo -e "${RED}❌ Error: No se pudo descargar la especificación OpenAPI después de 3 intentos${NC}"
    echo -e "${YELLOW}Verifica que la URL sea correcta: $SWAGGER_URL${NC}"
    echo -e "${YELLOW}Verifica tu conexión a internet${NC}"
    exit 1
fi

# Verificar que el archivo Swagger sea válido JSON
if ! poetry run python -m json.tool "$SWAGGER_FILE" > /dev/null 2>&1; then
    echo -e "${RED} Error: El archivo Swagger no es un JSON válido${NC}"
    exit 1
fi

# Paso 2: Crear directorio de salida temporal
echo -e "${BLUE}Preparando directorios...${NC}"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Paso 3: Generar el cliente usando OpenAPI Generator
echo -e "${BLUE}Generando cliente Python con OpenAPI Generator...${NC}"
poetry run openapi-generator-cli generate \
    -i "$SWAGGER_FILE" \
    -g python \
    -o "$OUTPUT_DIR" \
    -c "$CONFIG_FILE" \
    --additional-properties=packageName=hyblock_capital_sdk,pythonPackageName=hyblock_capital_sdk,generateSourceCodeOnly=false

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Cliente generado exitosamente${NC}"
else
    echo -e "${RED}Error durante la generación del cliente${NC}"
    exit 1
fi

# Paso 4: Mover archivos generados al directorio correcto (preservando wrappers y archivos personalizados)
echo -e "${BLUE}Organizando archivos generados...${NC}"

GEN_DIR="$OUTPUT_DIR/hyblock_capital_sdk"

if [ ! -d "$GEN_DIR" ]; then
    echo -e "${RED}Error: No se encontró el directorio del paquete generado${NC}"
    exit 1
fi

# Asegurar directorio final
mkdir -p "$FINAL_DIR"

# Reemplazar solo rutas generadas conocidas, preservando wrappers (auth.py, client.py, __init__.py personalizado, etc.)
declare -a GEN_SUBDIRS=("api" "models")
declare -a GEN_FILES=("api_client.py" "api_response.py" "configuration.py" "exceptions.py" "rest.py")

# Copiar subdirectorios generados
for d in "${GEN_SUBDIRS[@]}"; do
  if [ -d "$GEN_DIR/$d" ]; then
    echo -e "${YELLOW}  Actualizando directorio generado: ${d}${NC}"
    rm -rf "$FINAL_DIR/$d"
    cp -R "$GEN_DIR/$d" "$FINAL_DIR/$d"
  fi
done

# Copiar archivos generados
for f in "${GEN_FILES[@]}"; do
  if [ -f "$GEN_DIR/$f" ]; then
    echo -e "${YELLOW}  Actualizando archivo generado: ${f}${NC}"
    cp -f "$GEN_DIR/$f" "$FINAL_DIR/$f"
  fi
done

# Reemplazar siempre __init__.py con el generado para mantener exports consistentes
if [ -f "$GEN_DIR/__init__.py" ]; then
  cp -f "$GEN_DIR/__init__.py" "$FINAL_DIR/__init__.py"
  echo -e "${GREEN}  __init__.py generado copiado${NC}"
fi

# Paso 5: Copiar archivos de configuración útiles si se generaron
if [ -f "$OUTPUT_DIR/setup.py" ]; then
    cp "$OUTPUT_DIR/setup.py" "./setup.py.generated"
    echo -e "${GREEN}setup.py copiado como referencia${NC}"
fi

if [ -f "$OUTPUT_DIR/requirements.txt" ]; then
    cp "$OUTPUT_DIR/requirements.txt" "./requirements.generated.txt"
    echo -e "${GREEN}requirements.txt copiado como referencia${NC}"
fi

# Paso 6: Limpiar archivos temporales
echo -e "${BLUE}Limpiando archivos temporales...${NC}"
rm -rf "$OUTPUT_DIR"
rm -f "$SWAGGER_FILE"

# Paso 7: Instalar dependencias con Poetry
echo -e "${BLUE}Instalando dependencias con Poetry...${NC}"
poetry install

# Paso 8: Ejecutar verificaciones básicas
echo -e "${BLUE}Ejecutando verificaciones básicas...${NC}"

# Verificar que el paquete se pueda importar
if poetry run python -c "import hyblock_capital_sdk; print('Importación exitosa')"; then
    echo -e "${GREEN}El SDK se puede importar correctamente${NC}"
else
    echo -e "${RED}Error: No se puede importar el SDK generado${NC}"
    exit 1
fi

# Nota: No se aplica formateo automático al código generado para preservar la salida del generador

echo -e "${GREEN}SDK generado exitosamente!${NC}"
echo -e "${BLUE}Ubicación del SDK: $FINAL_DIR${NC}"
echo -e "${BLUE}Para usar el SDK:${NC}"
echo -e "${YELLOW}   poetry add ./hyblock-capital-sdk${NC}"
echo -e "${YELLOW}   from hyblock_capital_sdk import ApiClient, Configuration${NC}"

echo -e "${BLUE}Próximos pasos recomendados:${NC}"
echo -e "${YELLOW}   1. Revisar la documentación generada en docs/README.md${NC}"
echo -e "${YELLOW}   2. Ejecutar tests: poetry run pytest${NC}"
echo -e "${YELLOW}   3. Personalizar configuración según necesidades${NC}"
echo -e "${YELLOW}   4. Crear ejemplos de uso en examples/${NC}"
