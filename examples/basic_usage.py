#!/usr/bin/env python3
"""
Ejemplo básico de uso del SDK de Hyblock Capital.

Este ejemplo muestra cómo configurar el cliente y realizar operaciones básicas
como obtener información de cuenta y balances.

Antes de ejecutar este ejemplo:
1. Genera el SDK: ./generate_sdk.sh
2. Configura tus credenciales en .env
3. Instala dependencias: poetry install
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Función principal del ejemplo."""
    print("Ejemplo básico del SDK de Hyblock Capital")
    print("=" * 50)
    
    # Verificar que las variables de entorno estén configuradas
    api_key = os.getenv('HYBLOCK_API_KEY')
    api_secret = os.getenv('HYBLOCK_API_SECRET')
    api_url = os.getenv('HYBLOCK_API_URL', 'https://api1.dev.hyblockcapital.com/v1')
    
    if not api_key or not api_secret:
        print("Error: Credenciales de API no configuradas")
        print("Configura las variables de entorno:")
        print("   export HYBLOCK_API_KEY='tu_api_key'")
        print("   export HYBLOCK_API_SECRET='tu_api_secret'")
        print("   O copia env.example a .env y edítalo")
        return 1
    
    print(f"Credenciales configuradas")
    print(f"API URL: {api_url}")
    print(f"API Key: {api_key[:8]}...")
    
    try:
        # Intentar importar el SDK generado
        print("\n📦 Importando SDK...")
        
        try:
            # Estas importaciones funcionarán después de generar el SDK
            from hyblock_capital_sdk import ApiClient, Configuration
            from hyblock_capital_sdk.api import AccountApi, TradingApi, MarketDataApi
            print("✅ SDK importado correctamente")
        except ImportError as e:
            print(f"❌ Error importando SDK: {e}")
            print("💡 Asegúrate de haber generado el SDK primero:")
            print("   ./generate_sdk.sh")
            return 1
        
        # Configurar el cliente
        print("\n⚙️  Configurando cliente...")
        configuration = Configuration(
            host=api_url,
            api_key={
                'ApiKeyAuth': api_key
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
        
        print("✅ Cliente configurado correctamente")
        
        # Ejemplo 1: Obtener información de cuenta
        print("\n👤 Obteniendo información de cuenta...")
        try:
            account_info = account_api.get_account()
            print(f"✅ ID de cuenta: {account_info.id}")
            print(f"📧 Email: {account_info.email}")
            print(f"🎯 Trading habilitado: {account_info.trading_enabled}")
        except Exception as e:
            print(f"❌ Error obteniendo cuenta: {e}")
        
        # Ejemplo 2: Obtener balances
        print("\n💰 Obteniendo balances...")
        try:
            balances = account_api.get_balances()
            print("✅ Balances obtenidos:")
            for balance in balances[:5]:  # Mostrar solo los primeros 5
                print(f"   {balance.asset}: {balance.free} disponible, {balance.locked} bloqueado")
        except Exception as e:
            print(f"❌ Error obteniendo balances: {e}")
        
        # Ejemplo 3: Obtener ticker de mercado
        print("\n📈 Obteniendo datos de mercado...")
        try:
            ticker = market_api.get_ticker("BTC/USDT")
            print(f"✅ BTC/USDT:")
            print(f"   Precio actual: ${ticker.last_price}")
            print(f"   Cambio 24h: {ticker.price_change_percent_24h}%")
            print(f"   Volumen 24h: {ticker.volume_24h}")
        except Exception as e:
            print(f"❌ Error obteniendo ticker: {e}")
        
        # Ejemplo 4: Obtener órdenes abiertas
        print("\n📋 Obteniendo órdenes abiertas...")
        try:
            open_orders = trading_api.get_open_orders()
            print(f"✅ Órdenes abiertas: {len(open_orders)}")
            for order in open_orders[:3]:  # Mostrar solo las primeras 3
                print(f"   {order.id}: {order.side} {order.amount} {order.symbol} @ {order.price}")
        except Exception as e:
            print(f"❌ Error obteniendo órdenes: {e}")
        
        print("\n🎉 Ejemplo completado exitosamente!")
        print("\n📚 Próximos pasos:")
        print("   - Revisa otros ejemplos en el directorio examples/")
        print("   - Consulta la documentación: https://docs.hyblock.capital")
        print("   - Experimenta con diferentes endpoints de la API")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Verifica:")
        print("   1. Que el SDK esté generado correctamente")
        print("   2. Que las credenciales sean válidas")
        print("   3. Que tengas conexión a internet")
        return 1


if __name__ == "__main__":
    # Cargar variables de entorno desde .env si existe
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        print("📄 Cargando variables de entorno desde .env...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    sys.exit(main())
