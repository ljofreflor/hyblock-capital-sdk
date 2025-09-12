# Longs and Shorts API

La `Longs_And_ShortsApi` proporciona acceso a longs and shorts api de Hyblock Capital.

## Configuración

```python
from hyblock_capital_sdk.api import Longs_And_ShortsApi
import hyblock_capital_sdk as hc

# Configurar cliente
config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
config.api_key["x-api-key"] = "tu_api_key"

api_client = hc.ApiClient(config)
longs_and_shorts_api = Longs_And_ShortsApi(api_client)
```

## Referencia de la API

::: hyblock_capital_sdk.api.longs_and_shorts_api
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
    result = longs_and_shorts_api.some_method()
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error: {e}")
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
    result = longs_and_shorts_api.some_method()
except UnauthorizedException:
    print("❌ Credenciales inválidas")
except RateLimitException as e:
    print(f"⏰ Rate limit excedido. Reintentar en {e.retry_after} segundos")
except ApiException as e:
    print(f"❌ Error de API: {e.status} - {e.reason}")
```

Para más información sobre métodos específicos, consulta la referencia de la API arriba.
