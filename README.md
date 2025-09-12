# Hyblock Capital SDK

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue)](https://python-poetry.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)

SDK no oficial de Python para la API de Hyblock Capital, generado automáticamente desde la especificación OpenAPI/Swagger.

> **⚠️ Aviso**: Este es un SDK no oficial creado por la comunidad. No está afiliado, respaldado o mantenido oficialmente por Hyblock Capital.

## Características

- **Generación automática**: El SDK se genera automáticamente desde la especificación OpenAPI de Hyblock Capital
- **Completamente tipado**: Soporte completo para type hints y autocompletado en IDEs
- **Asíncrono**: Soporte para operaciones síncronas y asíncronas
- **Manejo de errores**: Excepciones personalizadas para diferentes tipos de errores de la API
- **Documentación integrada**: Documentación generada automáticamente con ejemplos
- **Testing incluido**: Suite de tests para validar la funcionalidad
- **Poetry compatible**: Gestión de dependencias moderna y reproducible

## Instalación

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
git clone https://github.com/hyblock-capital/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Configurar versión de Python con pyenv (recomendado)
pyenv local 3.11.12

# Instalar dependencias
poetry install
```

## Generar SDK desde OpenAPI

Este proyecto utiliza OpenAPI Generator para crear automáticamente el SDK desde la especificación Swagger de Hyblock Capital disponible en [https://media.hyblockcapital.com/document/swagger-dev.json](https://media.hyblockcapital.com/document/swagger-dev.json).

### Requisitos previos

- Python 3.8+ (recomendado 3.11.12 con pyenv)
- Poetry para gestión de dependencias
- Java 8+ (requerido por OpenAPI Generator)
- pyenv (recomendado para gestión de versiones de Python)

### Generación automática

**Opción 1: Script Bash (Recomendado)**

```bash
./generate_sdk.sh
```

**Opción 2: Manual**

```bash
# 1. Instalar OpenAPI Generator
poetry add --dev openapi-generator-cli

# 2. Generar SDK
openapi-generator-cli generate \
    -i https://media.hyblockcapital.com/document/swagger-dev.json \
    -g python \
    -o ./generated \
    -c openapi-generator-config.json

# 3. Mover archivos generados
mv ./generated/hyblock_capital_sdk ./hyblock_capital_sdk

# 4. Configurar Python local (opcional)
pyenv local 3.11.12

# 5. Instalar dependencias
poetry install
```

## Configuración

### Credenciales de API

Antes de usar el SDK, necesitas obtener tus credenciales de API desde el panel de Hyblock Capital:

1. Inicia sesión en [Hyblock Capital](https://hyblock.capital)
2. Ve a Configuración → API Keys
3. Crea una nueva API Key con los permisos necesarios
4. Guarda de forma segura tu `API Key` y `API Secret`

### Variables de entorno (Recomendado)

```bash
export HYBLOCK_API_KEY="tu_api_key_aqui"
export HYBLOCK_API_SECRET="tu_api_secret_aqui"
export HYBLOCK_API_URL="https://api1.dev.hyblockcapital.com/v1"  # Opcional
```

## Uso básico

### Configuración del cliente

```python
from hyblock_capital_sdk import ApiClient, Configuration
from hyblock_capital_sdk.api import AccountApi, TradingApi, MarketDataApi
import os

# Configuración usando variables de entorno
configuration = Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={
        'ApiKeyAuth': os.getenv('HYBLOCK_API_KEY')
    },
    api_key_prefix={
        'ApiKeyAuth': 'Bearer'
    }
)

# Crear cliente
api_client = ApiClient(configuration)

# Inicializar APIs
account_api = AccountApi(api_client)
trading_api = TradingApi(api_client)
market_api = MarketDataApi(api_client)
```

### Ejemplos de uso

#### Obtener información de la cuenta

```python
try:
    # Obtener balance de la cuenta
    account_info = account_api.get_account()
    print(f"ID de cuenta: {account_info.id}")
    print(f"Email: {account_info.email}")
    
    # Obtener balances
    balances = account_api.get_balances()
    for balance in balances:
        print(f"{balance.asset}: {balance.free} disponible, {balance.locked} bloqueado")
        
except Exception as e:
    print(f"Error: {e}")
```

#### Obtener datos de mercado

```python
try:
    # Obtener ticker de un símbolo
    ticker = market_api.get_ticker("BTC/USDT")
    print(f"BTC/USDT - Precio: ${ticker.last_price}")
    print(f"Cambio 24h: {ticker.price_change_percent_24h}%")
    
    # Obtener libro de órdenes
    orderbook = market_api.get_orderbook("BTC/USDT", limit=10)
    print(f"Mejor bid: ${orderbook.bids[0].price}")
    print(f"Mejor ask: ${orderbook.asks[0].price}")
    
except Exception as e:
    print(f"Error: {e}")
```

#### Realizar trading

```python
from hyblock_capital_sdk.models import OrderRequest, OrderSide, OrderType

try:
    # Crear orden de compra limit
    order_request = OrderRequest(
        symbol="BTC/USDT",
        side=OrderSide.BUY,
        type=OrderType.LIMIT,
        amount=0.001,
        price=45000.00
    )
    
    order = trading_api.create_order(order_request)
    print(f"Orden creada: {order.id}")
    print(f"Estado: {order.status}")
    
    # Consultar orden
    order_status = trading_api.get_order(order.id)
    print(f"Cantidad ejecutada: {order_status.filled_amount}")
    
    # Cancelar orden si está pendiente
    if order_status.status == "open":
        cancelled_order = trading_api.cancel_order(order.id)
        print(f"Orden cancelada: {cancelled_order.id}")
        
except Exception as e:
    print(f"Error: {e}")
```

#### Analizar pools de liquidez

```python
from hyblock_capital_sdk.api import LiquidityApi

# Inicializar API de liquidez
liquidity_api = LiquidityApi(api_client)

try:
    # 1. Obtener niveles acumulativos de liquidación
    cumulative_pools = liquidity_api.cumulative_liq_level_get(
        coin="BTC",
        timeframe="1h",
        exchange="binance",
        sort="desc",
        limit=20
    )
    
    print("Pools de liquidación acumulativos:")
    for pool in cumulative_pools:
        print(f"  Precio: ${pool.price} | Cantidad: {pool.amount} BTC")
    
    # 2. Conteo de liquidaciones Long ancladas
    long_liquidations = liquidity_api.anchored_liq_levels_count_get(
        coin="BTC",
        timeframe="1h",
        level="long",
        anchor="1d",
        exchange="binance",
        limit=10
    )
    
    print(f"\nLiquidaciones Long detectadas: {len(long_liquidations)}")
    
    # 3. Tamaño de pools de liquidez
    pool_sizes = liquidity_api.anchored_liq_levels_size_get(
        coin="BTC",
        timeframe="1h",
        level="long",
        anchor="4h",
        exchange="binance",
        limit=10
    )
    
    print(f"Tamaños de pools analizados: {len(pool_sizes)}")
    
    # 4. Heatmap de liquidaciones
    heatmap = liquidity_api.liquidation_heatmap_get(
        coin="BTC",
        timeframe="1h",
        exchange="binance",
        limit=50
    )
    
    print(f"Heatmap de liquidaciones: {len(heatmap)} puntos")
    
    # 5. Eventos históricos de liquidación
    import time
    end_time = int(time.time())
    start_time = end_time - (24 * 60 * 60)  # Últimas 24 horas
    
    historical_events = liquidity_api.liquidation_get(
        coin="BTC",
        timeframe="1h",
        bucket="4,5,6",  # Liquidaciones grandes: 10k-100k, 100k-1m, 1m-10m
        exchange="binance",
        start_time=start_time,
        end_time=end_time,
        limit=20
    )
    
    print(f"Eventos históricos (24h): {len(historical_events)}")
    
except Exception as e:
    print(f"Error analizando pools: {e}")
```

#### Análisis avanzado de liquidaciones

```python
# Configuración para múltiples exchanges
exchanges = ["binance", "bybit", "okx"]
coins = ["BTC", "ETH", "SOL"]

for coin in coins:
    print(f"\n🔍 Analizando {coin} en múltiples exchanges...")
    
    for exchange in exchanges:
        try:
            # Obtener niveles de liquidación
            levels = liquidity_api.liquidation_levels_get(
                coin=coin,
                timeframe="4h",
                exchange=exchange,
                limit=15
            )
            
            print(f"  {exchange}: {len(levels)} niveles de liquidación")
            
            # Analizar el pool más grande
            if levels:
                largest_pool = max(levels, key=lambda x: x.amount)
                print(f"    Pool más grande: ${largest_pool.price} ({largest_pool.amount} {coin})")
                
        except Exception as e:
            print(f"  {exchange}: Error - {e}")
```

## Regenerar SDK

Para actualizar el SDK con los últimos cambios de la API:

```bash
# Regenerar desde la especificación más reciente
./generate_sdk.sh
```

El script automáticamente:
1. Descarga la especificación OpenAPI más reciente
2. Genera el nuevo código del SDK
3. Instala las dependencias
4. Ejecuta verificaciones básicas

## Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Con coverage
poetry run pytest --cov=hyblock_capital_sdk

# Tests específicos
poetry run pytest tests/test_account_api.py
```

## Documentación

- [Documentación de la API](https://docs.hyblock.capital/api)
- [Documentación del SDK](./docs/)
- [Ejemplos](./examples/)
- [Referencia de modelos](./docs/models.md)

## Análisis de Pools de Liquidez

El SDK proporciona acceso completo a los datos de pools de liquidez de Hyblock Capital, permitiendo análisis avanzados de riesgo de liquidación.

### Tipos de análisis disponibles

#### 1. **Pools Acumulativos** (`cumulative_liq_level_get`)
- Muestra la distribución acumulada de liquidaciones
- Útil para identificar zonas de alta concentración de liquidez
- Parámetros: `coin`, `timeframe`, `exchange`, `sort`, `limit`

#### 2. **Conteo de Liquidaciones Ancladas** (`anchored_liq_levels_count_get`)
- Cuenta liquidaciones por nivel (long/short) en un período específico
- Ayuda a identificar patrones de liquidación recurrentes
- Parámetros: `coin`, `timeframe`, `level`, `anchor`, `exchange`, `limit`

#### 3. **Tamaño de Pools** (`anchored_liq_levels_size_get`)
- Analiza el volumen de liquidez en cada nivel de precio
- Identifica los pools más grandes que pueden causar movimientos significativos
- Parámetros: `coin`, `timeframe`, `level`, `anchor`, `exchange`, `limit`

#### 4. **Heatmap de Liquidaciones** (`liquidation_heatmap_get`)
- Visualización de la densidad de liquidaciones por precio y tiempo
- Útil para identificar clusters de riesgo
- Parámetros: `coin`, `timeframe`, `exchange`, `limit`

#### 5. **Eventos Históricos** (`liquidation_get`)
- Liquidaciones específicas que han ocurrido en el pasado
- Permite análisis de correlación y patrones temporales
- Parámetros: `coin`, `timeframe`, `bucket`, `exchange`, `start_time`, `end_time`, `limit`

### Parámetros comunes

- **coin**: Símbolo de la criptomoneda (BTC, ETH, SOL, etc.)
- **timeframe**: Período de tiempo (1h, 4h, 1d, 1w)
- **exchange**: Exchange (binance, bybit, okx, etc.)
- **level**: Tipo de liquidación (long, short)
- **anchor**: Período de anclaje (1h, 4h, 1d, 1w)
- **bucket**: Rangos de tamaño (1-10k, 4-100k, 5-1m, 6-10m, etc.)

### Casos de uso

1. **Identificación de soporte/resistencia**: Los pools grandes pueden actuar como niveles clave
2. **Análisis de riesgo**: Concentraciones altas indican mayor riesgo de liquidación
3. **Estrategias de trading**: Evitar áreas con alta probabilidad de liquidación
4. **Alertas automáticas**: Monitoreo de pools que se acercan a niveles críticos
5. **Backtesting**: Análisis histórico de correlación entre liquidaciones y movimientos de precio

## Manejo de errores

El SDK incluye excepciones personalizadas para diferentes tipos de errores:

```python
from hyblock_capital_sdk.exceptions import (
    ApiException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    RateLimitException
)

try:
    account_info = account_api.get_account()
except UnauthorizedException:
    print("Credenciales inválidas")
except RateLimitException as e:
    print(f"Límite de velocidad excedido. Reintentar en {e.retry_after} segundos")
except ApiException as e:
    print(f"Error de API: {e.status} - {e.reason}")
```

## Seguridad

- **Nunca** hardcodees tus credenciales en el código
- Usa variables de entorno o un sistema de gestión de secretos
- Configura permisos mínimos necesarios en tus API keys
- Revisa regularmente el uso de tus API keys
- Rota tus credenciales periódicamente

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Desarrollo

```bash
# Configurar entorno de desarrollo
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Configurar Python (recomendado usar pyenv)
pyenv local 3.11.12

# Instalar dependencias de desarrollo
poetry install --with dev

# Instalar pre-commit hooks
poetry run pre-commit install

# Ejecutar verificaciones
poetry run black tests/  # Formatear código
poetry run flake8 tests/ # Linting
poetry run mypy hyblock_capital_sdk/ --exclude hyblock_capital_sdk/api --exclude hyblock_capital_sdk/models
poetry run pytest  # Tests
```

### Comandos útiles con Poetry

```bash
# Generar SDK desde OpenAPI
poetry run ./generate_sdk.sh

# Ejecutar tests con coverage
poetry run pytest --cov=hyblock_capital_sdk

# Build del paquete
poetry build

# Publicar en PyPI Test
poetry publish --repository testpypi

# Ver información del proyecto
poetry show
poetry check
```

## Licencias y Atribuciones

### Licencia del SDK
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

### Dependencias de Terceros
Para información detallada sobre las licencias de las dependencias utilizadas, consulta [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

### Atribuciones
Consulta el archivo [NOTICE](NOTICE) para información sobre el código generado automáticamente y atribuciones.

## Términos de Uso

**IMPORTANTE**: Este SDK interactúa con la API de Hyblock Capital. El uso de esta API está sujeto a los términos de servicio de Hyblock Capital. Al usar este SDK, aceptas cumplir con dichos términos.

- Este SDK no está afiliado oficialmente con Hyblock Capital
- Los usuarios son responsables de cumplir con los términos de servicio de la API
- El uso de la API puede estar sujeto a límites de tasa y otras restricciones
- Los usuarios deben obtener las credenciales API apropiadas de Hyblock Capital

Para más información sobre los términos de servicio de la API, visita el sitio oficial de Hyblock Capital.

## Soporte

- **Issues del SDK**: [GitHub Issues](https://github.com/ljofreflor/hyblock-capital-sdk/issues)
- **Documentación de la API**: [docs.hyblock.capital](https://docs.hyblock.capital)
- **Contacto**: ljofre2146@gmail.com

## Roadmap

- [ ] Soporte para WebSockets en tiempo real
- [ ] Cliente asíncrono optimizado
- [ ] Herramientas de backtesting integradas
- [ ] Indicadores técnicos incluidos
- [ ] CLI para operaciones rápidas
- [ ] Plugins para frameworks populares

## Performance

El SDK está optimizado para:
- Conexiones persistentes para múltiples requests
- Pooling de conexiones HTTP
- Serialización/deserialización eficiente
- Cache inteligente para datos de mercado
- Manejo automático de rate limiting

## Troubleshooting

### Problemas comunes

**Error de autenticación**
```
ApiException: 401 Unauthorized
```
- Verifica que tu API Key y Secret sean correctos
- Asegúrate de que la API Key tenga los permisos necesarios
- Verifica que la API Key no haya expirado

**Error de rate limiting**
```
ApiException: 429 Too Many Requests
```
- Reduce la frecuencia de tus requests
- Implementa backoff exponencial
- Considera usar WebSockets para datos en tiempo real

**Error de conexión**
```
ConnectionError: Unable to connect to host
```
- Verifica tu conexión a internet
- Confirma que la URL de la API sea correcta
- Revisa si hay firewalls bloqueando la conexión

Para más ayuda, consulta nuestra [documentación de troubleshooting](./docs/troubleshooting.md) o abre un issue en GitHub.
