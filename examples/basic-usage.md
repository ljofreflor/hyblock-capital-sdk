# Basic Usage

This page contains basic usage examples for the Hyblock Capital SDK.

## Initial Configuration

```python
import hyblock_capital_sdk as hc
import os

# Basic configuration
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)

api_client = hc.ApiClient(config)
```

## Example 1: Get Catalog

```python
from hyblock_capital_sdk.api import CatalogApi

catalog_api = CatalogApi(api_client)

try:
    catalog = catalog_api.catalog_get()
    print(f"Available currencies: {list(catalog.keys())}")
except Exception as e:
    print(f"Error: {e}")
```

## Example 2: Liquidity Pool Analysis

```python
from hyblock_capital_sdk.api import LiquidityApi

liquidity_api = LiquidityApi(api_client)

# Get cumulative pools
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=10
)

print(f"Pools found: {len(pools)}")
for pool in pools:
    print(f"Price: ${pool.price} | Amount: {pool.amount} BTC")
```

## Example 3: Liquidation Heatmap

```python
# Get heatmap
heatmap = liquidity_api.liquidation_heatmap_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=50
)

print(f"Heatmap with {len(heatmap)} points")
```

## Example 4: Error Handling

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
    print("Invalid credentials")
except RateLimitException as e:
    print(f"Rate limit exceeded. Retry in {e.retry_after} seconds")
except ApiException as e:
    print(f"API error: {e.status} - {e.reason}")
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
        # 1. Get catalog
        print("Getting catalog...")
        catalog = catalog_api.catalog_get()
        print(f"Available currencies: {len(catalog)}")
        
        # 2. Analyze liquidity pools for BTC
        print("\nAnalyzing liquidity pools for BTC...")
        pools = liquidity_api.cumulative_liq_level_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            limit=5
        )
        
        print(f"Pools found: {len(pools)}")
        for i, pool in enumerate(pools, 1):
            print(f"  {i}. Precio: ${pool.price} | Cantidad: {pool.amount} BTC")
        
        print("\nExample executed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Próximos Pasos

- Revisa [Liquidation Pools](liquidation-pools.md) para ejemplos más avanzados
- Consulta la [referencia de APIs](../api/liquidity.md) para funcionalidades completas
- Explora [Quick Start](../quickstart.md) para una guía paso a paso
