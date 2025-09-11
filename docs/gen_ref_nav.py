"""Script para generar automáticamente la navegación de documentación de APIs."""

import os
from pathlib import Path

def generate_api_docs():
    """Genera archivos de documentación para todas las APIs."""
    
    # Directorio base del SDK
    sdk_dir = Path("../hyblock_capital_sdk")
    docs_dir = Path(".")
    
    # APIs disponibles
    apis = {
        "catalog": "Catalog API",
        "funding_rate": "Funding Rate API", 
        "liquidity": "Liquidity API",
        "longs_and_shorts": "Longs and Shorts API",
        "open_interest": "Open Interest API",
        "options": "Options API",
        "orderbook": "Orderbook API",
        "orderflow": "Orderflow API",
        "profile_tool": "Profile Tool API",
        "sentiment": "Sentiment API"
    }
    
    # Crear archivos de documentación para cada API
    for api_file, api_title in apis.items():
        doc_file = docs_dir / f"{api_file}.md"
        
        # Verificar si el archivo de API existe
        api_path = sdk_dir / "api" / f"{api_file}_api.py"
        if not api_path.exists():
            continue
            
        # Crear contenido de documentación
        content = f"""# {api_title}

La `{api_file.title()}Api` proporciona acceso a {api_title.lower()} de Hyblock Capital.

## Configuración

```python
from hyblock_capital_sdk.api import {api_file.title()}Api
import hyblock_capital_sdk as hc

# Configurar cliente
config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
config.api_key["x-api-key"] = "tu_api_key"

api_client = hc.ApiClient(config)
{api_file}_api = {api_file.title()}Api(api_client)
```

## Referencia de la API

::: hyblock_capital_sdk.api.{api_file}_api
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: true
      separate_signature: true
      merge_init_into_class: false
      show_bases: true
      show_root_full_path: false
      filters: ["!^_"]

## Ejemplos de Uso

```python
# Ejemplo básico de uso
try:
    # Reemplazar con el método apropiado de la API
    result = {api_file}_api.some_method()
    print(f"Resultado: {{result}}")
except Exception as e:
    print(f"Error: {{e}}")
```

## Manejo de Errores

```python
from hyblock_capital_sdk.exceptions import (
    ApiException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    RateLimitException
)

try:
    result = {api_file}_api.some_method()
except UnauthorizedException:
    print("❌ Credenciales inválidas")
except RateLimitException as e:
    print(f"⏰ Rate limit excedido. Reintentar en {{e.retry_after}} segundos")
except ApiException as e:
    print(f"❌ Error de API: {{e.status}} - {{e.reason}}")
```

Para más información sobre métodos específicos, consulta la referencia de la API arriba.
"""
        
        # Escribir archivo
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generado: {doc_file}")

def generate_models_docs():
    """Genera documentación para los modelos."""
    
    docs_dir = Path(".")
    models_file = docs_dir / "models.md"
    
    content = """# Models

Los modelos representan las estructuras de datos utilizadas por el SDK de Hyblock Capital.

## Modelos Principales

::: hyblock_capital_sdk.models
    options:
      show_source: false
      show_root_heading: true
      show_root_toc_entry: true
      separate_signature: true
      merge_init_into_class: false
      show_bases: true
      show_root_full_path: false
      filters: ["!^_"]

## Ejemplos de Uso

```python
from hyblock_capital_sdk.models import (
    # Importar modelos específicos según sea necesario
    # Ejemplo: CumulativeLiquidationLevel, LiquidationEvent, etc.
)

# Los modelos se crean automáticamente por las APIs
# No es necesario crear instancias manualmente en la mayoría de casos
```

## Estructura de Datos

Los modelos siguen la estructura definida por la especificación OpenAPI de Hyblock Capital y se generan automáticamente.
"""
    
    with open(models_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generado: {models_file}")

def generate_exceptions_docs():
    """Genera documentación para las excepciones."""
    
    docs_dir = Path(".")
    exceptions_file = docs_dir / "exceptions.md"
    
    content = """# Exceptions

El SDK incluye excepciones personalizadas para manejar diferentes tipos de errores de la API.

## Excepciones Disponibles

::: hyblock_capital_sdk.exceptions
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: true
      separate_signature: true
      merge_init_into_class: false
      show_bases: true
      show_root_full_path: false
      filters: ["!^_"]

## Manejo de Errores

```python
from hyblock_capital_sdk.exceptions import (
    ApiException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ServiceException,
    RateLimitException
)

try:
    # Tu código de API aquí
    result = api.some_method()
except UnauthorizedException:
    print("❌ Credenciales inválidas")
except ForbiddenException:
    print("❌ Sin permisos para acceder a este endpoint")
except NotFoundException:
    print("❌ Recurso no encontrado")
except RateLimitException as e:
    print(f"⏰ Rate limit excedido. Reintentar en {e.retry_after} segundos")
except BadRequestException as e:
    print(f"❌ Solicitud inválida: {e}")
except ServiceException as e:
    print(f"❌ Error del servidor: {e}")
except ApiException as e:
    print(f"❌ Error de API: {e.status} - {e.reason}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
```

## Códigos de Estado HTTP

- **400**: Bad Request - Solicitud malformada
- **401**: Unauthorized - Credenciales inválidas
- **403**: Forbidden - Sin permisos
- **404**: Not Found - Recurso no encontrado
- **429**: Too Many Requests - Rate limit excedido
- **500**: Internal Server Error - Error del servidor
"""
    
    with open(exceptions_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generado: {exceptions_file}")

if __name__ == "__main__":
    print("🔧 Generando documentación automática...")
    
    # Cambiar al directorio de docs
    os.chdir(Path(__file__).parent)
    
    # Generar documentación
    generate_api_docs()
    generate_models_docs()
    generate_exceptions_docs()
    
    print("✅ Documentación generada exitosamente!")
