# Ejemplos de uso del SDK de Hyblock Capital

Este directorio contiene ejemplos prácticos de cómo usar el SDK de Hyblock Capital para diferentes casos de uso.

## Estructura de ejemplos

- `basic_usage.py` - Ejemplo básico de configuración y uso del SDK
- `trading_example.py` - Ejemplos de operaciones de trading
- `market_data_example.py` - Obtención y procesamiento de datos de mercado
- `websocket_example.py` - Uso de WebSockets para datos en tiempo real
- `advanced_features.py` - Características avanzadas del SDK

## Requisitos previos

1. **Credenciales de API**: Obtén tus credenciales desde [Hyblock Capital](https://hyblock.capital/api)
2. **Variables de entorno**: Configura tu archivo `.env` basado en `env.example`
3. **SDK instalado**: Asegúrate de que el SDK esté instalado y generado

```bash
# Generar el SDK
python generate_sdk.py

# Instalar dependencias
poetry install

# Configurar variables de entorno
cp env.example .env
# Edita .env con tus credenciales reales
```

## Ejecutar ejemplos

```bash
# Ejemplo básico
poetry run python examples/basic_usage.py

# Ejemplo de trading
poetry run python examples/trading_example.py

# Datos de mercado
poetry run python examples/market_data_example.py
```

## Configuración de seguridad

⚠️ **IMPORTANTE**: 
- Nunca hardcodees credenciales en el código
- Usa variables de entorno o un gestor de secretos
- Revisa los permisos de tus API keys
- Usa credenciales de prueba para desarrollo

## Soporte

Si encuentras problemas con los ejemplos:
1. Verifica que tus credenciales sean válidas
2. Confirma que el SDK esté correctamente generado
3. Revisa los logs para errores específicos
4. Consulta la documentación en [docs.hyblock.capital](https://docs.hyblock.capital)
