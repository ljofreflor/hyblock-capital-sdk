# Guía de Inicio Rápido - Hyblock Capital SDK

Esta guía te ayudará a configurar y usar el SDK de Hyblock Capital en menos de 5 minutos.

## Inicio Rápido

### 1. Prerrequisitos

Asegúrate de tener instalado:
- **Python 3.8.1+** (recomendado 3.11.12)
- **Poetry** (gestor de dependencias)
- **Java 8+** (requerido por OpenAPI Generator)
- **pyenv** (recomendado para gestión de versiones)

```bash
# Verificar versiones
python --version
poetry --version
java -version
```

### 2. Clonar y Configurar

```bash
# Clonar el repositorio
git clone https://github.com/hyblock-capital/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Configurar versión de Python (recomendado)
pyenv local 3.11.12

# Instalar dependencias
poetry install
```

### 3. Generar el SDK

El SDK se genera automáticamente desde la especificación OpenAPI de Hyblock Capital:

```bash
# Opción 1: Script Bash (recomendado)
./generate_sdk.sh

# Opción 2: Usar Makefile
make generate
```

### 4. Configurar Credenciales

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar con tus credenciales reales
nano .env
```

Configurar en `.env`:
```bash
HYBLOCK_API_KEY=tu_api_key_aqui
HYBLOCK_API_SECRET=tu_api_secret_aqui
HYBLOCK_API_URL=https://api1.dev.hyblockcapital.com/v1
```

### 5. Probar el SDK

```bash
# Ejecutar ejemplo básico
poetry run python examples/basic_usage.py

# Ejecutar tests
poetry run pytest

# Verificar con linting
make check
```

## Comandos Principales

### Generación del SDK
```bash
make generate          # Generar SDK desde OpenAPI
make clean-sdk         # Limpiar SDK generado (con backup)
make reinstall         # Reinstalar SDK completo
```

### Testing y Calidad
```bash
make test              # Ejecutar todos los tests
make test-cov          # Tests con reporte de cobertura
make lint              # Análisis de código
make format            # Formatear código
make check             # Verificaciones completas
```

### Desarrollo
```bash
make dev-setup         # Configurar entorno de desarrollo
make docs              # Generar documentación
make build             # Construir paquete
make clean             # Limpiar archivos temporales
```

## Uso Básico del SDK

### Configuración
```python
from hyblock_capital_sdk import ApiClient, Configuration
from hyblock_capital_sdk.api import AccountApi, TradingApi, MarketDataApi

# Configurar cliente
configuration = Configuration(
    host="https://api1.dev.hyblockcapital.com/v1",
    api_key={'ApiKeyAuth': 'tu_api_key'},
    api_key_prefix={'ApiKeyAuth': 'Bearer'}
)

client = ApiClient(configuration)
account_api = AccountApi(client)
```

### Obtener Datos de Cuenta
```python
# Información de cuenta
account = account_api.get_account()
print(f"ID: {account.id}, Email: {account.email}")

# Balances
balances = account_api.get_balances()
for balance in balances:
    print(f"{balance.asset}: {balance.free}")
```

### Datos de Mercado
```python
market_api = MarketDataApi(client)

# Ticker
ticker = market_api.get_ticker("BTC/USDT")
print(f"BTC/USDT: ${ticker.last_price}")

# Libro de órdenes
orderbook = market_api.get_orderbook("BTC/USDT")
print(f"Mejor bid: ${orderbook.bids[0].price}")
```

### Trading
```python
trading_api = TradingApi(client)

# Crear orden
order = trading_api.create_order({
    "symbol": "BTC/USDT",
    "side": "buy",
    "type": "limit", 
    "amount": 0.001,
    "price": 45000.00
})
```

## Regenerar SDK

Para actualizar el SDK con los últimos cambios de la API:

```bash
# Regenerar automáticamente
make generate

# O manualmente
./generate_sdk.sh
```

El script:
1. Descarga la especificación OpenAPI más reciente
2. Genera el nuevo código del SDK
3. Instala dependencias actualizadas
4. Ejecuta verificaciones básicas

## Seguridad

- **Nunca** hardcodees credenciales en el código
- Usa variables de entorno (`.env`)
- Configura permisos mínimos en API keys
- Mantén tus credenciales seguras
- Rota API keys regularmente

## Recursos Adicionales

- **Documentación completa**: [README.md](README.md)
- **Ejemplos avanzados**: [examples/](examples/)
- **Tests**: [tests/](tests/)
- **API Reference**: [docs.hyblock.capital](https://docs.hyblock.capital)

## Solución de Problemas

### Error de Java
```bash
# Instalar Java si no está disponible
brew install openjdk@11  # macOS
# o descargar desde https://adoptium.net/
```

### Error de OpenAPI Generator
```bash
# Instalar manualmente
pip install openapi-generator-cli
```

### Error de Importación del SDK
```bash
# Regenerar el SDK
make clean-sdk
make generate
```

### Error de Credenciales
- Verifica que tus API keys sean válidas
- Confirma que tengan los permisos necesarios
- Revisa que no hayan expirado

## ¡Listo para Usar!

Con esta configuración ya tienes:
- SDK generado automáticamente
- Entorno de desarrollo configurado
- Tests funcionando
- Ejemplos de uso disponibles
- CI/CD configurado
- Documentación completa

¡Comienza a desarrollar con el SDK de Hyblock Capital!
