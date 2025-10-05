# Exceptions

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
    print("Invalid credentials")
except ForbiddenException:
    print("No permissions to access this endpoint")
except NotFoundException:
    print("Resource not found")
except RateLimitException as e:
    print(f"⏰ Rate limit excedido. Reintentar en {e.retry_after} segundos")
except BadRequestException as e:
    print(f"Invalid request: {e}")
except ServiceException as e:
    print(f"Server error: {e}")
except ApiException as e:
    print(f"API error: {e.status} - {e.reason}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Códigos de Estado HTTP

- **400**: Bad Request - Solicitud malformada
- **401**: Unauthorized - Credenciales inválidas
- **403**: Forbidden - Sin permisos
- **404**: Not Found - Recurso no encontrado
- **429**: Too Many Requests - Rate limit excedido
- **500**: Internal Server Error - Error del servidor
