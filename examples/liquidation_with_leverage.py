#!/usr/bin/env python3
"""
Ejemplo mostrando cómo los pools de liquidación YA INCLUYEN
el apalancamiento calculado automáticamente.
"""

import hyblock_capital_sdk as hc

def analyze_leverage_in_pools():
    """Analizar niveles de apalancamiento en los pools."""
    
    # Configurar cliente
    config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
    config.api_key["x-api-key"] = "tu-api-key"
    api_client = hc.ApiClient(config)
    
    liquidity_api = hc.LiquidityApi(api_client)
    
    try:
        # Obtener niveles específicos de liquidación
        print("🔍 Obteniendo niveles de liquidación con apalancamiento...")
        
        liquidation_levels = liquidity_api.liquidation_levels_get(
            coin="BTC",
            timeframe="1h",
            exchange="binance",
            sort="desc",
            limit=20
        )
        
        print("✅ Pools obtenidos! Analizando apalancamientos...")
        print("\n📊 ANÁLISIS DE APALANCAMIENTO EN POOLS:")
        print("=" * 60)
        
        # Procesar cada nivel de liquidación
        leverage_analysis = {}
        
        for i, level in enumerate(liquidation_levels[:10]):  # Primeros 10
            print(f"\n🏊‍♂️ Pool #{i+1}:")
            print(f"   💰 Tamaño: ${level.size:,.2f}")
            print(f"   💲 Precio liquidación: ${level.price:,.2f}")
            print(f"   ⚡ Apalancamiento: {level.leverage}")  # ¡YA INCLUIDO!
            print(f"   📈 Lado: {level.side}")
            print(f"   ⏰ Duración abierta: {level.open_duration/3600:.1f}h")
            
            # Agrupar por apalancamiento
            leverage = level.leverage
            if leverage not in leverage_analysis:
                leverage_analysis[leverage] = {
                    'count': 0,
                    'total_size': 0,
                    'long_pools': 0,
                    'short_pools': 0
                }
            
            leverage_analysis[leverage]['count'] += 1
            leverage_analysis[leverage]['total_size'] += level.size
            
            if level.side == 'long':
                leverage_analysis[leverage]['long_pools'] += 1
            else:
                leverage_analysis[leverage]['short_pools'] += 1
        
        # Resumen por apalancamiento
        print(f"\n📈 RESUMEN POR APALANCAMIENTO:")
        print("=" * 60)
        
        for leverage, data in leverage_analysis.items():
            print(f"\n⚡ Apalancamiento {leverage}:")
            print(f"   📊 Pools totales: {data['count']}")
            print(f"   💰 Tamaño total: ${data['total_size']:,.2f}")
            print(f"   📈 Pools Long: {data['long_pools']}")
            print(f"   📉 Pools Short: {data['short_pools']}")
            print(f"   💡 Promedio por pool: ${data['total_size']/data['count']:,.2f}")
        
        return leverage_analysis
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def analyze_aggregated_liquidations():
    """Analizar liquidaciones agregadas (sin apalancamiento específico)."""
    
    config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
    config.api_key["x-api-key"] = "tu-api-key"
    api_client = hc.ApiClient(config)
    
    liquidity_api = hc.LiquidityApi(api_client)
    
    try:
        print("\n🔥 LIQUIDACIONES AGREGADAS (eventos pasados):")
        print("=" * 60)
        
        # Liquidaciones históricas agregadas
        liquidations = liquidity_api.liquidation_get(
            coin="BTC",
            timeframe="1h",
            bucket="4,5,6",  # Liquidaciones grandes
            exchange="binance",
            limit=10
        )
        
        total_long = 0
        total_short = 0
        
        for liquidation in liquidations[:5]:
            print(f"\n📅 Fecha: {liquidation.open_date}")
            print(f"   📈 Liquidaciones Long: ${liquidation.long_liquidation:,.2f}")
            print(f"   📉 Liquidaciones Short: ${liquidation.short_liquidation:,.2f}")
            print(f"   ⚖️  Ratio L/S: {liquidation.long_liquidation/liquidation.short_liquidation:.2f}")
            
            total_long += liquidation.long_liquidation
            total_short += liquidation.short_liquidation
        
        print(f"\n💡 TOTALES AGREGADOS:")
        print(f"   📈 Total Long: ${total_long:,.2f}")
        print(f"   📉 Total Short: ${total_short:,.2f}")
        print(f"   🎯 Dominancia: {'Long' if total_long > total_short else 'Short'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal."""
    print("🎯 ANÁLISIS DE POOLS DE LIQUIDACIÓN")
    print("=" * 60)
    print("✅ Los pools YA INCLUYEN toda la información necesaria:")
    print("   • Apalancamiento específico por pool")
    print("   • Tamaños agregados por rango")
    print("   • Precios de liquidación calculados")
    print("   • Duración de posiciones abiertas")
    print("   • Clasificación Long/Short")
    
    # Analizar pools con apalancamiento específico
    leverage_data = analyze_leverage_in_pools()
    
    # Analizar liquidaciones agregadas
    analyze_aggregated_liquidations()
    
    print(f"\n💡 CONCLUSIÓN:")
    print("=" * 60)
    print("🚀 NO necesitas calcular apalancamiento manualmente")
    print("📊 Los pools vienen con TODO pre-calculado")
    print("⚡ Cada pool muestra su apalancamiento específico")
    print("💰 Los tamaños están agregados por rango USD")
    print("🎯 Solo filtras por moneda, exchange y timeframe")

if __name__ == "__main__":
    main()
    
    print(f"\n📋 PARÁMETROS QUE SÍ CONTROLAS:")
    print("   • coin: 'BTC', 'ETH', etc.")
    print("   • exchange: 'binance', 'bybit', etc.")
    print("   • timeframe: '1m', '5m', '1h', '4h', '1d'")
    print("   • bucket: rangos de tamaño (1-7)")
    print("   • level: 'long' o 'short' (para conteos)")
    print("   • anchor: '1h', '4h', '1d' (para anclajes)")
    
    print(f"\n🎯 NO NECESITAS ESPECIFICAR:")
    print("   ❌ Apalancamiento (ya calculado)")
    print("   ❌ Precios de liquidación (automáticos)")
    print("   ❌ Agregaciones (pre-procesadas)")
