#!/usr/bin/env python3
"""
Ejemplo completo para obtener y analizar pools de liquidación
usando el SDK de Hyblock Capital.
"""

import hyblock_capital_sdk as hc
from datetime import datetime, timedelta
import time

def main():
    """Ejemplo principal para analizar pools de liquidación."""
    
    # 1. Configurar cliente
    print("🔧 Configurando cliente...")
    config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
    
    # Configurar autenticación (reemplaza con tu API key real)
    config.api_key["x-api-key"] = "tu-api-key-aqui"
    
    api_client = hc.ApiClient(config)
    liquidity_api = hc.LiquidityApi(api_client)
    
    # 2. Obtener catálogo de monedas disponibles
    catalog_api = hc.CatalogApi(api_client)
    try:
        print("📋 Obteniendo catálogo...")
        catalog = catalog_api.catalog_get()
        print(f"✅ Catálogo obtenido: {list(catalog.keys())[:5]}... exchanges disponibles")
    except Exception as e:
        print(f"⚠️  Error obteniendo catálogo: {e}")
        print("💡 Usando valores por defecto...")
    
    # 3. Analizar pools de liquidación para BTC
    coin = "BTC"
    timeframe = "1h"
    exchange = "binance"
    
    print(f"\n🏊‍♂️ Analizando pools de liquidación para {coin}...")
    
    try:
        # 3.1 Niveles acumulativos
        print("📊 Obteniendo niveles acumulativos...")
        cumulative_pools = liquidity_api.cumulative_liq_level_get(
            coin=coin,
            timeframe=timeframe,
            exchange=exchange,
            sort="desc",
            limit=20
        )
        print(f"✅ Pools acumulativos obtenidos: {len(cumulative_pools) if hasattr(cumulative_pools, '__len__') else 'N/A'} registros")
        
        # 3.2 Conteo de niveles anclados (Long)
        print("📈 Obteniendo conteo de liquidaciones Long...")
        long_count = liquidity_api.anchored_liq_levels_count_get(
            coin=coin,
            timeframe=timeframe,
            level="long",
            anchor="1d",
            exchange=exchange,
            limit=10
        )
        print(f"✅ Conteo Long obtenido")
        
        # 3.3 Conteo de niveles anclados (Short)
        print("📉 Obteniendo conteo de liquidaciones Short...")
        short_count = liquidity_api.anchored_liq_levels_count_get(
            coin=coin,
            timeframe=timeframe,
            level="short",
            anchor="1d",
            exchange=exchange,
            limit=10
        )
        print(f"✅ Conteo Short obtenido")
        
        # 3.4 Tamaño de niveles anclados
        print("💰 Obteniendo tamaño de pools...")
        pool_sizes = liquidity_api.anchored_liq_levels_size_get(
            coin=coin,
            timeframe=timeframe,
            level="long",
            anchor="4h",
            exchange=exchange,
            limit=10
        )
        print(f"✅ Tamaños de pools obtenidos")
        
        # 3.5 Liquidaciones específicas por rangos
        print("🎯 Obteniendo niveles específicos...")
        specific_levels = liquidity_api.liquidation_levels_get(
            coin=coin,
            timeframe="4h",
            exchange=exchange,
            limit=15
        )
        print(f"✅ Niveles específicos obtenidos")
        
        # 3.6 Eventos de liquidación históricos (último día)
        print("📜 Obteniendo eventos históricos...")
        end_time = int(time.time())
        start_time = end_time - (24 * 60 * 60)  # 24 horas atrás
        
        historical_events = liquidity_api.liquidation_get(
            coin=coin,
            timeframe="1h",
            bucket="4,5,6",  # Liquidaciones grandes: 10k-100k, 100k-1m, 1m-10m
            exchange=exchange,
            start_time=start_time,
            end_time=end_time,
            limit=20
        )
        print(f"✅ Eventos históricos obtenidos")
        
        # 4. Resumen de análisis
        print(f"\n📋 RESUMEN DEL ANÁLISIS PARA {coin}:")
        print(f"   💱 Exchange: {exchange}")
        print(f"   ⏱️  Timeframe: {timeframe}")
        print(f"   📊 Datos obtenidos exitosamente:")
        print(f"      • Pools acumulativos ✅")
        print(f"      • Conteo Long/Short ✅")
        print(f"      • Tamaños de pools ✅")
        print(f"      • Niveles específicos ✅")
        print(f"      • Eventos históricos ✅")
        
    except Exception as e:
        print(f"❌ Error analizando pools: {e}")
        print("💡 Verifica:")
        print("   • Tu API key es válida")
        print("   • Los parámetros son correctos")
        print("   • Tienes permisos para estos endpoints")

def analyze_liquidation_heatmap():
    """Ejemplo adicional para obtener heatmap de liquidaciones."""
    print("\n🔥 Análisis de Heatmap de Liquidaciones...")
    
    config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
    config.api_key["x-api-key"] = "tu-api-key-aqui"
    
    api_client = hc.ApiClient(config)
    liquidity_api = hc.LiquidityApi(api_client)
    
    try:
        # Heatmap de liquidaciones
        heatmap = liquidity_api.liquidation_heatmap_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            limit=50
        )
        print("✅ Heatmap de liquidaciones obtenido")
        
    except Exception as e:
        print(f"❌ Error obteniendo heatmap: {e}")

if __name__ == "__main__":
    main()
    analyze_liquidation_heatmap()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Reemplaza 'tu-api-key-aqui' con tu API key real")
    print("2. Ajusta los parámetros según tus necesidades")
    print("3. Procesa los datos recibidos según tu estrategia")
    print("4. Considera implementar alertas basadas en los pools")
