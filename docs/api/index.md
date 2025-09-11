# Hyblock Capital SDK

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue)](https://python-poetry.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)

SDK no oficial de Python para la API de Hyblock Capital, generado automáticamente desde la especificación OpenAPI/Swagger.

!!! warning "Aviso Importante"
    Este es un SDK **no oficial** creado por la comunidad. No está afiliado, respaldado o mantenido oficialmente por Hyblock Capital.

## Características

- **Generación automática**: El SDK se genera automáticamente desde la especificación OpenAPI de Hyblock Capital
- **Completamente tipado**: Soporte completo para type hints y autocompletado en IDEs
- **Asíncrono**: Soporte para operaciones síncronas y asíncronas
- **Manejo de errores**: Excepciones personalizadas para diferentes tipos de errores de la API
- **Documentación integrada**: Documentación generada automáticamente con ejemplos
- **Testing incluido**: Suite de tests para validar la funcionalidad
- **Poetry compatible**: Gestión de dependencias moderna y reproducible

## Instalación Rápida

=== "Poetry (Recomendado)"
    ```bash
    poetry add hyblock-capital-sdk
    ```

=== "pip"
    ```bash
    pip install hyblock-capital-sdk
    ```

=== "Desde repositorio"
    ```bash
    poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git
    ```

## Uso Básico

```python
import hyblock_capital_sdk as hc
import os

# Configuración
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)

# Cliente
api_client = hc.ApiClient(config)
liquidity_api = hc.LiquidityApi(api_client)

# Obtener pools de liquidez
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=20
)

print(f"Pools de liquidez: {len(pools)}")
```

## APIs Disponibles

### 📊 Liquidez y Liquidaciones
- **LiquidityApi**: Análisis de pools de liquidez y riesgo de liquidación
- **LiquidationApi**: Eventos históricos de liquidación

### 📈 Datos de Mercado
- **OrderbookApi**: Libros de órdenes en tiempo real
- **OrderflowApi**: Flujo de órdenes y análisis de mercado
- **OpenInterestApi**: Interés abierto y análisis de posiciones

### 💰 Trading y Posiciones
- **LongsAndShortsApi**: Análisis de posiciones largas y cortas
- **FundingRateApi**: Tasas de financiamiento

### 📋 Utilidades
- **CatalogApi**: Catálogo de monedas y exchanges disponibles
- **SentimentApi**: Análisis de sentimiento del mercado
- **OptionsApi**: Datos de opciones (si están disponibles)

## Ejemplos

### Análisis de Pools de Liquidez

```python
# Obtener niveles de liquidación acumulativos
cumulative_pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    sort="desc",
    limit=20
)

# Analizar el pool más grande
if cumulative_pools:
    largest_pool = max(cumulative_pools, key=lambda x: x.amount)
    print(f"Pool más grande: ${largest_pool.price} ({largest_pool.amount} BTC)")
```

### Heatmap de Liquidaciones

```python
# Obtener heatmap de liquidaciones
heatmap = liquidity_api.liquidation_heatmap_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=50
)

print(f"Heatmap con {len(heatmap)} puntos de datos")
```

## Recursos

- **Documentación completa**: Navega por las secciones de la izquierda
- **Ejemplos**: Ve a la sección [Examples](examples/basic-usage.md)
- **API Reference**: Consulta la [referencia completa de APIs](api/client.md)
- **GitHub**: [Repositorio del proyecto](https://github.com/ljofreflor/hyblock-capital-sdk)

## Soporte

- **Issues**: [GitHub Issues](https://github.com/ljofreflor/hyblock-capital-sdk/issues)
- **Contacto**: ljofre2146@gmail.com
- **Documentación API**: [docs.hyblock.capital](https://docs.hyblock.capital)

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](about/license.md).
