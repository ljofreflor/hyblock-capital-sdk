# Quick Start

This guide will help you get started with the **UNOFFICIAL** Hyblock Capital SDK in less than 5 minutes.

> **DISCLAIMER**: This is an **UNOFFICIAL SDK** created by @leonardojofre. It is **NOT affiliated with, endorsed by, or officially maintained** by Hyblock Capital. Use at your own risk.

## 1. Installation

```bash
# With Poetry (recommended)
poetry add hyblock-capital-sdk

# Or with pip
pip install hyblock-capital-sdk
```

## 2. Configuration

### Getting API Credentials

1. Visit [Hyblock Capital](https://hyblock.capital)
2. Go to **Settings → API Keys**
3. Create a new API Key
4. Save your `API Key` and `API Secret`

### Configuring the Client

```python
import hyblock_capital_sdk as hc
import os

# Basic configuration
config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": "your_api_key_here"}
)

# Create client
api_client = hc.ApiClient(config)
```

### Environment Variables (Recommended)

```python
import os

config = hc.Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY")}
)
```

## 3. First Steps

### Getting Currency Catalog

```python
from hyblock_capital_sdk.api import CatalogApi

catalog_api = CatalogApi(api_client)

try:
    catalog = catalog_api.catalog_get()
    print(f"Available currencies: {list(catalog.keys())}")
except Exception as e:
    print(f"Error: {e}")
```

### Analyzing Liquidity Pools

```python
from hyblock_capital_sdk.api import LiquidityApi

liquidity_api = LiquidityApi(api_client)

# Get liquidation pools for BTC
pools = liquidity_api.cumulative_liq_level_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=10
)

print(f"Liquidity pools found: {len(pools)}")
for pool in pools[:3]:  # Show first 3
    print(f"  Price: ${pool.price} | Amount: {pool.amount} BTC")
```

## 4. Common Examples

### Long/Short Liquidation Analysis

```python
# Long Liquidations
long_liquidations = liquidity_api.anchored_liq_levels_count_get(
    coin="BTC",
    timeframe="1h",
    level="long",
    anchor="1d",
    exchange="binance",
    limit=10
)

# Short Liquidations
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

### Liquidation Heatmap

```python
# Get heatmap
heatmap = liquidity_api.liquidation_heatmap_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=50
)

print(f"Heatmap with {len(heatmap)} data points")
```

### Open Interest Data

```python
from hyblock_capital_sdk.api import OpenInterestApi

oi_api = OpenInterestApi(api_client)

# Get open interest
oi_data = oi_api.open_interest_get(
    coin="BTC",
    timeframe="1h",
    exchange="binance",
    limit=20
)

print(f"Open interest data: {len(oi_data)} records")
```

## 5. Error Handling

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
    print("Invalid credentials")
except RateLimitException as e:
    print(f"Rate limit exceeded. Retry in {e.retry_after} seconds")
except ApiException as e:
    print(f"API error: {e.status} - {e.reason}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 6. Complete Example Script

```python
#!/usr/bin/env python3
"""
Complete example script for Hyblock Capital SDK
"""

import hyblock_capital_sdk as hc
import os
from hyblock_capital_sdk.api import LiquidityApi, CatalogApi

def main():
    # Configuration
    config = hc.Configuration(
        host="https://api1.dev.hyblockcapital.com/v1",
        api_key={"x-api-key": os.getenv("HYBLOCK_API_KEY", "your_api_key_here")}
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
            print(f"  {i}. Price: ${pool.price} | Amount: {pool.amount} BTC")
        
        # 3. Liquidation heatmap
        print("\nGetting heatmap...")
        heatmap = liquidity_api.liquidation_heatmap_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            limit=20
        )
        print(f"Heatmap: {len(heatmap)} points")
        
        print("\nScript executed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Check your API key and internet connection")

if __name__ == "__main__":
    main()
```

## 7. Next Steps

Now that you have the SDK working:

1. **Explore the [API reference](api/client.md)** to see all available functionality
2. **Check out [advanced examples](examples/liquidation-pools.md)** for more complex use cases
3. **Review the [development documentation](development/contributing.md)** if you want to contribute to the project

## 8. Additional Resources

- **Official Hyblock Capital documentation**: [docs.hyblock.capital](https://docs.hyblock.capital)
- **Project GitHub**: [hyblock-capital-sdk](https://github.com/ljofreflor/hyblock-capital-sdk)
- **Report issues**: [GitHub Issues](https://github.com/ljofreflor/hyblock-capital-sdk/issues)
