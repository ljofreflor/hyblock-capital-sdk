# Quick Start

Esta guía te ayudará a comenzar con el SDK de Hyblock Capital en menos de 5 minutos.

## 1. Instalación

```bash
# Con Poetry (recomendado)
poetry add hyblock-capital-sdk

# O con pip
pip install hyblock-capital-sdk
```

## 2. Configuración

### Obtener Credenciales de API

1. Visita [Hyblock Capital](https://hyblock.capital)
2. Ve a **Configuración → API Keys**
3. Crea una nueva API Key
4. Guarda tu `API Key` y `API Secret`

### Configurar el Cliente

```python
import hyblock_capital_sdk as hc
import os

# Configuración básica
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": "tu_api_key_aqui"}
)

# Crear cliente
api_client = hc.ApiClient(config)
```

### Variables de Entorno (Recomendado)

```python
import os

config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)
```

## 3. Primeros Pasos

### Obtener Catálogo de Monedas

```python
from hyblock_capital_sdk.api import CatalogApi

catalog_api = CatalogApi(api_client)

try:
    catalog = catalog_api.catalog_get()
    print(f"Monedas disponibles: {list(catalog.keys())}")
except Exception as e:
    print(f"Error: {e}")
```

### Analizar Pools de Liquidez

```python
from hyblock_capital_sdk.api import LiquidityApi

liquidity_api = LiquidityApi(api_client)

# Obtener pools de liquidación para BTC
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=10
)

print(f"Pools de liquidez encontrados: {len(pools)}")
for pool in pools[:3]:  # Mostrar los primeros 3
    print(f"  Precio: ${pool.price} | Cantidad: {pool.amount} BTC")
```

## 4. Ejemplos Comunes

### Análisis de Liquidaciones Long/Short

```python
# Liquidaciones Long
long_liquidations = liquidity_api.anchored_liq_levels_count_get(
    coin="BTC",
    timeframe="1h",
    level="long",
    anchor="1d",
    exchange="binance",
    limit=10
)

# Liquidaciones Short
short_liquidations = liquidity_api.anchored_liq_levels_count_get(
    coin="BTC",
    timeframe="1h",
    level="short",
    anchor="1d",
    exchange="binance",
    limit=10
)

print(f"Long liquidations: {len(long_liquidations)}")
print(f"Short liquidations: {len(short_liquidations)}")
```

### Heatmap de Liquidaciones

```python
# Obtener heatmap
heatmap = liquidity_api.liquidation_heatmap_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=50
)

print(f"Heatmap con {len(heatmap)} puntos de datos")
```

### Datos de Interés Abierto

```python
from hyblock_capital_sdk.api import OpenInterestApi

oi_api = OpenInterestApi(api_client)

# Obtener interés abierto
oi_data = oi_api.open_interest_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=20
)

print(f"Datos de interés abierto: {len(oi_data)} registros")
```

## 5. Manejo de Errores

```python
from hyblock_capital_sdk.exceptions import (
    ApiException,
    UnauthorizedException,
    ForbiddenException,
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
except Exception as e:
    print(f"❌ Error inesperado: {e}")
```

## 6. Script Completo de Ejemplo

```python
#!/usr/bin/env python3
"""
Script de ejemplo completo para Hyblock Capital SDK
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
        
        # 3. Heatmap de liquidaciones
        print("\n🔥 Obteniendo heatmap...")
        heatmap = liquidity_api.liquidation_heatmap_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            limit=20
        )
        print(f"✅ Heatmap: {len(heatmap)} puntos")
        
        print("\n🎉 ¡Script ejecutado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica tu API key y conexión a internet")

if __name__ == "__main__":
    main()
```

## 7. Próximos Pasos

Ahora que tienes el SDK funcionando:

1. **Explora la [referencia de APIs](api/client.md)** para ver todas las funcionalidades disponibles
2. **Revisa los [ejemplos avanzados](examples/liquidation-pools.md)** para casos de uso más complejos
3. **Consulta la [documentación de desarrollo](development/contributing.md)** si quieres contribuir al proyecto

## 8. Recursos Adicionales

- **Documentación oficial de Hyblock Capital**: [docs.hyblock.capital](https://docs.hyblock.capital)
- **GitHub del proyecto**: [hyblock-capital-sdk](https://github.com/ljofreflor/hyblock-capital-sdk)
- **Reportar problemas**: [GitHub Issues](https://github.com/ljofreflor/hyblock-capital-sdk/issues)
