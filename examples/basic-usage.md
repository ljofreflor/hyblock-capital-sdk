# Basic Usage

Esta página contiene ejemplos básicos de uso del SDK de Hyblock Capital.

## Configuración Inicial

```python
import hyblock_capital_sdk as hc
import os

# Configuración básica
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)

api_client = hc.ApiClient(config)
```

## Ejemplo 1: Obtener Catálogo

```python
from hyblock_capital_sdk.api import CatalogApi

catalog_api = CatalogApi(api_client)

try:
    catalog = catalog_api.catalog_get()
    print(f"Monedas disponibles: {list(catalog.keys())}")
except Exception as e:
    print(f"Error: {e}")
```

## Ejemplo 2: Análisis de Pools de Liquidez

```python
from hyblock_capital_sdk.api import LiquidityApi

liquidity_api = LiquidityApi(api_client)

# Obtener pools acumulativos
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=10
)

print(f"Pools encontrados: {len(pools)}")
for pool in pools:
    print(f"Precio: ${pool.price} | Cantidad: {pool.amount} BTC")
```

## Ejemplo 3: Heatmap de Liquidaciones

```python
# Obtener heatmap
heatmap = liquidity_api.liquidation_heatmap_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=50
)

print(f"Heatmap con {len(heatmap)} puntos")
```

## Ejemplo 4: Manejo de Errores

```python
from hyblock_capital_sdk.exceptions import (
    ApiException,
    UnauthorizedException,
    RateLimitException
)

try:
    pools = liquidity_api.cumulative_liq_level_get(
        coin="BTC",
        timeframe="1h",
        exchange="binance"
    )
except UnauthorizedException:
    print("❌ Credenciales inválidas")
except RateLimitException as e:
    print(f"⏰ Rate limit excedido. Reintentar en {e.retry_after} segundos")
except ApiException as e:
    print(f"❌ Error de API: {e.status} - {e.reason}")
```

## Ejemplo Completo

```python
#!/usr/bin/env python3
"""
Ejemplo completo del SDK de Hyblock Capital
"""

import hyblock_capital_sdk as hc
import os
from hyblock_capital_sdk.api import LiquidityApi, CatalogApi

def main():
    # Configuración
    config = hc.Configuration(
        host="https://api1.dev.hyblockcapital.com/v1",
        api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY", "tu_api_key_aqui")}
    )
    
    api_client = hc.ApiClient(config)
    
    # APIs
    catalog_api = CatalogApi(api_client)
    liquidity_api = LiquidityApi(api_client)
    
    try:
        # 1. Obtener catálogo
        print("📋 Obteniendo catálogo...")
        catalog = catalog_api.catalog_get()
        print(f"✅ Monedas disponibles: {len(catalog)}")
        
        # 2. Analizar pools de liquidez para BTC
        print("\n🏊‍♂️ Analizando pools de liquidez para BTC...")
        pools = liquidity_api.cumulative_liq_level_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            limit=5
        )
        
        print(f"✅ Pools encontrados: {len(pools)}")
        for i, pool in enumerate(pools, 1):
            print(f"  {i}. Precio: ${pool.price} | Cantidad: {pool.amount} BTC")
        
        print("\n🎉 ¡Ejemplo ejecutado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Próximos Pasos

- Revisa [Liquidation Pools](liquidation-pools.md) para ejemplos más avanzados
- Consulta la [referencia de APIs](../api/liquidity.md) para funcionalidades completas
- Explora [Quick Start](../quickstart.md) para una guía paso a paso
