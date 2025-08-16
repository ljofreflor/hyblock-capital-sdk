"""
Configuración global de pytest para los tests del SDK de Hyblock Capital.

Define fixtures, configuraciones y utilidades compartidas entre todos los tests.
"""

import os
import pytest
from typing import Dict, Any
from unittest.mock import Mock, patch

# Configurar variables de entorno para tests
os.environ["HYBLOCK_API_KEY"] = "test_api_key"
os.environ["HYBLOCK_API_SECRET"] = "test_api_secret"
os.environ["HYBLOCK_API_URL"] = "https://api.test.hyblock.capital"


@pytest.fixture
def mock_api_credentials() -> Dict[str, str]:
    """
    Fixture que proporciona credenciales de API mock para tests.

    Returns:
        Diccionario con credenciales de prueba
    """
    return {
        "api_key": "test_api_key_12345",
        "api_secret": "test_api_secret_67890",
        "api_url": "https://api.test.hyblock.capital",
    }


@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """
    Fixture que proporciona una respuesta de API mock genérica.

    Returns:
        Diccionario con respuesta de API de prueba
    """
    return {
        "status": "success",
        "data": {"id": "test_id_123", "timestamp": "2024-01-01T00:00:00Z"},
        "message": "Operation completed successfully",
    }


@pytest.fixture
def mock_account_info() -> Dict[str, Any]:
    """
    Fixture que proporciona información de cuenta mock.

    Returns:
        Diccionario con información de cuenta de prueba
    """
    return {
        "id": "acc_123456",
        "email": "test@example.com",
        "username": "testuser",
        "verification_level": 2,
        "trading_enabled": True,
        "margin_enabled": False,
        "futures_enabled": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z",
    }


@pytest.fixture
def mock_balance_data() -> Dict[str, Any]:
    """
    Fixture que proporciona datos de balance mock.

    Returns:
        Diccionario con datos de balance de prueba
    """
    return {
        "asset": "BTC",
        "free": "1.50000000",
        "locked": "0.10000000",
        "total": "1.60000000",
        "usd_value": "48000.00",
    }


@pytest.fixture
def mock_order_data() -> Dict[str, Any]:
    """
    Fixture que proporciona datos de orden mock.

    Returns:
        Diccionario con datos de orden de prueba
    """
    return {
        "id": "order_123456",
        "symbol": "BTC/USDT",
        "side": "buy",
        "type": "limit",
        "amount": "0.001",
        "price": "45000.00",
        "filled_amount": "0.000",
        "remaining_amount": "0.001",
        "status": "open",
        "time_in_force": "gtc",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_ticker_data() -> Dict[str, Any]:
    """
    Fixture que proporciona datos de ticker mock.

    Returns:
        Diccionario con datos de ticker de prueba
    """
    return {
        "symbol": "BTC/USDT",
        "last_price": "45000.00",
        "bid_price": "44950.00",
        "ask_price": "45050.00",
        "high_24h": "46000.00",
        "low_24h": "44000.00",
        "volume_24h": "1234.56789",
        "price_change_24h": "1000.00",
        "price_change_percent_24h": "2.27",
        "timestamp": "2024-01-01T12:00:00Z",
    }


@pytest.fixture
def mock_http_client():
    """
    Fixture que proporciona un cliente HTTP mock.

    Returns:
        Mock del cliente HTTP
    """
    with patch("urllib3.PoolManager") as mock_pool_manager:
        mock_client = Mock()
        mock_pool_manager.return_value = mock_client

        # Configurar respuesta mock por defecto
        mock_response = Mock()
        mock_response.status = 200
        mock_response.data = b'{"status": "success", "data": {}}'
        mock_client.request.return_value = mock_response

        yield mock_client


@pytest.fixture
def mock_websocket_client():
    """
    Fixture que proporciona un cliente WebSocket mock.

    Returns:
        Mock del cliente WebSocket
    """
    with patch("websockets.connect") as mock_connect:
        mock_ws = Mock()
        mock_connect.return_value.__aenter__.return_value = mock_ws
        yield mock_ws


@pytest.fixture(autouse=True)
def reset_environment():
    """
    Fixture que se ejecuta automáticamente para limpiar el entorno entre tests.

    Resetea variables de entorno y estado global que podrían afectar otros tests.
    """
    # Limpiar variables de entorno específicas del SDK
    test_env_vars = [
        "HYBLOCK_API_KEY",
        "HYBLOCK_API_SECRET",
        "HYBLOCK_API_URL",
        "HYBLOCK_REQUEST_TIMEOUT",
        "LOG_LEVEL",
    ]

    original_values = {}
    for var in test_env_vars:
        original_values[var] = os.environ.get(var)

    yield

    # Restaurar valores originales
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value
        elif var in os.environ:
            del os.environ[var]


# Configuración de pytest
def pytest_configure(config):
    """Configuración global de pytest."""
    # Configurar marcadores personalizados
    config.addinivalue_line("markers", "unit: marca un test como test unitario")
    config.addinivalue_line(
        "markers", "integration: marca un test como test de integración"
    )
    config.addinivalue_line("markers", "e2e: marca un test como test end-to-end")
    config.addinivalue_line(
        "markers", "slow: marca un test como lento (requiere tiempo adicional)"
    )
    config.addinivalue_line(
        "markers",
        "requires_credentials: marca un test que requiere credenciales reales",
    )


def pytest_collection_modifyitems(config, items):
    """Modifica la colección de tests para agregar marcadores automáticos."""
    for item in items:
        # Agregar marcador 'unit' a tests en el directorio unit/
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)

        # Agregar marcador 'integration' a tests en el directorio integration/
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Agregar marcador 'e2e' a tests en el directorio e2e/
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# Fixtures para tests específicos de OpenAPI Generator
@pytest.fixture
def sample_openapi_spec() -> Dict[str, Any]:
    """
    Fixture que proporciona una especificación OpenAPI de ejemplo.

    Returns:
        Diccionario con especificación OpenAPI simplificada
    """
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Hyblock Capital API",
            "version": "1.0.0",
            "description": "API de trading de criptomonedas",
        },
        "servers": [{"url": "https://api1.dev.hyblockcapital.com/v1"}],
        "paths": {
            "/account": {
                "get": {
                    "summary": "Obtener información de cuenta",
                    "responses": {
                        "200": {
                            "description": "Información de cuenta",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Account"}
                                }
                            },
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Account": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "email": {"type": "string"},
                        "trading_enabled": {"type": "boolean"},
                    },
                }
            }
        },
    }
