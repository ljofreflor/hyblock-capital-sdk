# API Client

El `ApiClient` es el componente central del SDK que maneja las comunicaciones con la API de Hyblock Capital.

## Configuración Básica

```python
import hyblock_capital_sdk as hc

# Configuración mínima
config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
api_client = hc.ApiClient(config)
```

## Configuración con Autenticación

```python
import os

config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)

api_client = hc.ApiClient(config)
```

## Configuración Avanzada

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": "tu_api_key"},
    api_key_prefix={"x-api-key": "Bearer"},
    username="usuario_opcional",
    password="contraseña_opcional",
    discard_unknown_keys=True,
    disabled_client_side_validations="",
    server_index=None,
    server_variables={},
    server_operation_index={},
    server_operation_variables={},
    ssl_ca_cert=None,
    cert_file=None,
    key_file=None,
    assert_hostname=None,
    tls_server_name=None,
    key_password=None,
    connection_pool_maxsize=None,
    proxy=None,
    proxy_headers=None,
    safe_chars_for_path_param="",
    retries=None,
    socket_options=None,
    client_side_validation=True,
    auth_settings=None,
    user_agent=None,
    read_timeout=60,
    connect_timeout=60,
    timeout=60,
    pool_timeout=60,
    pool_connections=10,
    pool_maxsize=10,
    pool_block=False,
    pool_pre_ping=False,
    pool_recycle=-1,
    pool_retry_on_error=3,
    maxsize=10,
    block=False,
    pre_ping=False,
    recycle=-1,
    retry_on_error=3
)
```

## Métodos Principales

### call_api

Realiza una llamada a la API con los parámetros especificados.

```python
# Ejemplo de uso interno (generalmente no se usa directamente)
response = api_client.call_api(
    resource_path="/v1/liquidity/cumulative-liq-level",
    method="GET",
    path_params={},
    query_params={"coin": "BTC", "timeframe": "1h"},
    header_params={},
    body=None,
    post_params={},
    files={},
    response_type="object",
    auth_settings=["ApiKeyAuth"],
    async_req=False,
    _return_http_data_only=True,
    _preload_content=True,
    _request_timeout=None,
    collection_formats={},
    _host=None,
    _request_auth=None
)
```

### request

Método de conveniencia para realizar requests HTTP.

```python
# GET request
response = api_client.request(
    method="GET",
    url="/v1/catalog",
    headers={"x-api-key": "tu_api_key"},
    query_params={"limit": 10}
)

# POST request
response = api_client.request(
    method="POST",
    url="/v1/some-endpoint",
    headers={"Content-Type": "application/json"},
    body={"key": "value"}
)
```

### sanitize_for_serialization

Convierte objetos Python a formato JSON serializable.

```python
data = {"price": 45000.0, "amount": 1.5}
serialized = api_client.sanitize_for_serialization(data)
```

### deserialize

Deserializa respuestas JSON a objetos Python.

```python
json_data = '{"price": 45000.0, "amount": 1.5}'
deserialized = api_client.deserialize(
    response=json_data,
    response_type="dict",
    _check_type=True
)
```

## Configuración de Timeouts

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    read_timeout=30,      # Timeout para lectura
    connect_timeout=10,   # Timeout para conexión
    pool_timeout=5,       # Timeout para pool de conexiones
)
```

## Configuración de Pool de Conexiones

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    pool_connections=20,  # Número de conexiones en el pool
    pool_maxsize=20,      # Tamaño máximo del pool
    pool_block=True,      # Bloquear cuando el pool esté lleno
)
```

## Configuración de Retry

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    retries=3,            # Número de reintentos
    pool_retry_on_error=3 # Reintentos para errores de pool
)
```

## Configuración SSL/TLS

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    ssl_ca_cert="/path/to/ca_cert.pem",
    cert_file="/path/to/client.crt",
    key_file="/path/to/client.key",
    key_password="password_for_key"
)
```

## Configuración de Proxy

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    proxy="http://proxy.example.com:8080",
    proxy_headers={"User-Agent": "MyApp/1.0"}
)
```

## Configuración de User Agent

```python
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    user_agent="MyApp/1.0 (Python SDK)"
)
```

## Ejemplo Completo

```python
import hyblock_capital_sdk as hc
import os
from hyblock_capital_sdk.api import LiquidityApi

def create_configured_client():
    """Crear un cliente API configurado con todas las opciones."""
    
    config = hc.Configuration(
        host="https://api1.dev.hyblockcapital.com/v1",
        api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")},
        read_timeout=30,
        connect_timeout=10,
        pool_connections=10,
        pool_maxsize=10,
        retries=3,
        user_agent="MyTradingApp/1.0 (HyblockCapital SDK)"
    )
    
    return hc.ApiClient(config)

# Uso
api_client = create_configured_client()
liquidity_api = LiquidityApi(api_client)

# Ahora puedes usar todas las APIs
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance"
)
```

## Mejores Prácticas

1. **Reutilizar el cliente**: Crea un solo `ApiClient` y reutilízalo para todas las operaciones
2. **Configurar timeouts apropiados**: Ajusta los timeouts según tu caso de uso
3. **Usar pool de conexiones**: Para aplicaciones de alto volumen, configura un pool de conexiones
4. **Manejar errores**: Siempre envuelve las llamadas a la API en try-catch
5. **Configurar User-Agent**: Identifica tu aplicación con un User-Agent personalizado

## Troubleshooting

### Error de conexión

```python
try:
    pools = liquidity_api.cumulative_liq_level_get(coin="BTC")
except ConnectionError as e:
    print(f"Error de conexión: {e}")
    # Verificar conectividad a internet
    # Verificar URL del host
```

### Error de timeout

```python
try:
    pools = liquidity_api.cumulative_liq_level_get(coin="BTC")
except TimeoutError as e:
    print(f"Timeout: {e}")
    # Aumentar timeout en la configuración
    # Verificar velocidad de conexión
```

### Error de autenticación

```python
try:
    pools = liquidity_api.cumulative_liq_level_get(coin="BTC")
except UnauthorizedException as e:
    print(f"No autorizado: {e}")
    # Verificar API key
    # Verificar permisos de la API key
```
