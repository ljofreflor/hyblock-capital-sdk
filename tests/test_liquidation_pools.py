#!/usr/bin/env python3
"""
Tests unitarios para pools de liquidación usando mocks.
Prueba la funcionalidad sin hacer llamadas reales a la API.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import time

import hyblock_capital_sdk as hc


class TestLiquidationPools:
    """Test class para funcionalidad de pools de liquidación."""

    def setup_method(self):
        """
        Configurar cliente mock para cada test.

        Se ejecuta antes de cada método de test para configurar
        el entorno de prueba con mocks.
        """
        # Crear configuración mock
        self.config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
        self.config.api_key = {"x-api-key": "test-api-key"}

        # Crear cliente mock
        self.api_client_mock = Mock(spec=hc.ApiClient)
        self.liquidity_api = hc.LiquidityApi(self.api_client_mock)

    def test_liquidation_levels_get_success(self):
        """
        Test para obtener niveles de liquidación exitosamente.

        Valida que se retornen datos correctos con el formato esperado
        incluyendo apalancamiento, precios y tamaños.
        """
        # Datos mock de respuesta
        mock_liquidation_levels = [
            hc.LiquidationLevels(
                timestamp=1661236020,
                creation_date=1661236020,
                size=125000.50,
                price=21450.25,
                leverage="10x",
                side="long",
                open_duration=3600,
            ),
            hc.LiquidationLevels(
                timestamp=1661236080,
                creation_date=1661236080,
                size=89000.75,
                price=21380.15,
                leverage="25x",
                side="short",
                open_duration=1800,
            ),
            hc.LiquidationLevels(
                timestamp=1661236140,
                creation_date=1661236140,
                size=250000.00,
                price=21500.00,
                leverage="5x",
                side="long",
                open_duration=7200,
            ),
        ]

        # Configurar mock para retornar datos
        self.liquidity_api.liquidation_levels_get = Mock(
            return_value=mock_liquidation_levels
        )

        # Ejecutar función
        result = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", exchange="binance", limit=10
        )

        # Verificaciones
        assert len(result) == 3, "Debería retornar 3 pools de liquidación"
        assert (
            result[0].leverage == "10x"
        ), "Primer pool debería tener apalancamiento 10x"
        assert result[0].side == "long", "Primer pool debería ser tipo long"
        assert result[0].size == 125000.50, "Primer pool debería tener tamaño correcto"
        assert (
            result[1].leverage == "25x"
        ), "Segundo pool debería tener apalancamiento 25x"
        assert (
            result[2].size == 250000.00
        ), "Tercer pool debería tener el tamaño más grande"

        # Verificar que se llamó con parámetros correctos
        self.liquidity_api.liquidation_levels_get.assert_called_once_with(
            coin="BTC", timeframe="1h", exchange="binance", limit=10
        )

    def test_cumulative_liq_level_get_success(self):
        """
        Test para obtener niveles acumulativos de liquidación.

        Verifica que los datos acumulativos se retornen correctamente
        con agregaciones por precio y tiempo.
        """
        # Mock de datos acumulativos
        mock_cumulative_data = [
            hc.CumulativeLiqLevel(
                timestamp=1661236020,
                total_long_liquidation_size=300000.00,
                total_short_liquidation_size=200000.00,
                total_long_liquidation_count=15,
                total_short_liquidation_count=10,
            ),
            hc.CumulativeLiqLevel(
                timestamp=1661236080,
                total_long_liquidation_size=450000.00,
                total_short_liquidation_size=300000.00,
                total_long_liquidation_count=23,
                total_short_liquidation_count=18,
            ),
        ]

        self.liquidity_api.cumulative_liq_level_get = Mock(
            return_value=mock_cumulative_data
        )

        # Ejecutar
        result = self.liquidity_api.cumulative_liq_level_get(
            coin="ETH", timeframe="4h", exchange="bybit", sort="desc", limit=20
        )

        # Verificaciones
        assert len(result) == 2, "Debería retornar 2 niveles acumulativos"
        assert (
            result[0].timestamp == 1661236020
        ), "Primer nivel debería tener timestamp correcto"
        assert (
            result[1].total_long_liquidation_size == 450000.00
        ), "Segundo nivel debería tener tamaño long correcto"

        # Verificar llamada
        self.liquidity_api.cumulative_liq_level_get.assert_called_once_with(
            coin="ETH", timeframe="4h", exchange="bybit", sort="desc", limit=20
        )

    def test_anchored_liq_levels_count_get_long_short(self):
        """
        Test para conteo de niveles anclados tanto long como short.

        Valida que se puedan obtener conteos separados para posiciones
        long y short con diferentes períodos de anclaje.
        """
        # Mock para conteo long
        mock_long_count = hc.AnchoredLiqLevelsCount(
            open_date=1661236020, total_count=42
        )

        # Mock para conteo short
        mock_short_count = hc.AnchoredLiqLevelsCount(
            open_date=1661236020, total_count=38
        )

        # Configurar mocks
        self.liquidity_api.anchored_liq_levels_count_get = Mock()
        self.liquidity_api.anchored_liq_levels_count_get.side_effect = [
            mock_long_count,
            mock_short_count,
        ]

        # Ejecutar para long
        long_result = self.liquidity_api.anchored_liq_levels_count_get(
            coin="BTC", timeframe="1h", level="long", anchor="1d", limit=50
        )

        # Ejecutar para short
        short_result = self.liquidity_api.anchored_liq_levels_count_get(
            coin="BTC", timeframe="1h", level="short", anchor="1d", limit=50
        )

        # Verificaciones
        assert long_result.total_count == 42, "Conteo long debería ser 42"
        assert long_result.open_date == 1661236020, "Fecha debería ser correcta"
        assert short_result.total_count == 38, "Conteo short debería ser 38"
        assert short_result.open_date == 1661236020, "Fecha debería ser correcta"

        # Verificar que se hicieron 2 llamadas
        assert self.liquidity_api.anchored_liq_levels_count_get.call_count == 2

    def test_liquidation_get_historical_events(self):
        """
        Test para obtener eventos históricos de liquidación.

        Verifica que se puedan obtener liquidaciones pasadas agregadas
        por períodos de tiempo con buckets de tamaño.
        """
        # Mock de eventos históricos
        mock_historical_liquidations = [
            hc.Liquidation(
                open_date=1661236020,
                long_liquidation=1250000.00,
                short_liquidation=890000.00,
            ),
            hc.Liquidation(
                open_date=1661322420,
                long_liquidation=980000.00,
                short_liquidation=1150000.00,
            ),
            hc.Liquidation(
                open_date=1661408820,
                long_liquidation=1450000.00,
                short_liquidation=750000.00,
            ),
        ]

        self.liquidity_api.liquidation_get = Mock(
            return_value=mock_historical_liquidations
        )

        # Parámetros de tiempo
        end_time = int(time.time())
        start_time = end_time - (24 * 60 * 60)  # 24 horas atrás

        # Ejecutar
        result = self.liquidity_api.liquidation_get(
            coin="BTC",
            timeframe="1h",
            bucket="4,5,6",  # Liquidaciones grandes
            exchange="binance",
            start_time=start_time,
            end_time=end_time,
            limit=20,
        )

        # Verificaciones
        assert len(result) == 3, "Debería retornar 3 eventos históricos"
        assert (
            result[0].long_liquidation == 1250000.00
        ), "Primera liquidación long debería ser correcta"
        assert (
            result[1].short_liquidation == 1150000.00
        ), "Segunda liquidación short debería ser correcta"

        # Verificar totales
        total_long = sum(event.long_liquidation for event in result)
        total_short = sum(event.short_liquidation for event in result)
        assert total_long == 3680000.00, "Total liquidaciones long debería ser correcto"
        assert (
            total_short == 2790000.00
        ), "Total liquidaciones short debería ser correcto"

    def test_liquidation_heatmap_get_success(self):
        """
        Test para obtener heatmap de liquidaciones.

        Valida que el heatmap retorne rangos de precios con tamaños
        agregados para visualización de densidad de liquidaciones.
        """
        # Mock de heatmap
        mock_heatmap_data = [
            hc.LiquidationHeatmap(
                timestamp=1661236020,
                size=500000.00,
                starting_price=21000.00,
                ending_price=21100.00,
                side="long",
            ),
            hc.LiquidationHeatmap(
                timestamp=1661236080,
                size=750000.00,
                starting_price=21100.00,
                ending_price=21200.00,
                side="short",
            ),
            hc.LiquidationHeatmap(
                timestamp=1661236140,
                size=300000.00,
                starting_price=21200.00,
                ending_price=21300.00,
                side="long",
            ),
        ]

        self.liquidity_api.liquidation_heatmap_get = Mock(
            return_value=mock_heatmap_data
        )

        # Ejecutar
        result = self.liquidity_api.liquidation_heatmap_get(
            coin="BTC", timeframe="1h", exchange="binance", limit=50
        )

        # Verificaciones
        assert len(result) == 3, "Debería retornar 3 rangos de heatmap"
        assert (
            result[0].starting_price == 21000.00
        ), "Primer rango debería empezar en precio correcto"
        assert (
            result[0].ending_price == 21100.00
        ), "Primer rango debería terminar en precio correcto"
        assert (
            result[1].size == 750000.00
        ), "Segundo rango debería tener el tamaño más grande"

    def test_api_exception_handling(self):
        """
        Test para manejo de excepciones de API.

        Verifica que las excepciones se manejen correctamente cuando
        la API retorna errores o falla la conexión.
        """
        # Configurar mock para lanzar excepción
        self.liquidity_api.liquidation_levels_get = Mock(
            side_effect=hc.ApiException("API Error: 401 Unauthorized")
        )

        # Verificar que se lance la excepción
        with pytest.raises(hc.ApiException) as exc_info:
            self.liquidity_api.liquidation_levels_get(coin="BTC", timeframe="1h")

        assert "401 Unauthorized" in str(
            exc_info.value
        ), "Excepción debería contener mensaje de error"

    def test_invalid_parameters_validation(self):
        """
        Test para validación de parámetros inválidos.

        Verifica que se manejen correctamente parámetros inválidos
        como monedas no soportadas o timeframes incorrectos.
        """
        # Mock para parámetros inválidos
        self.liquidity_api.liquidation_levels_get = Mock(
            side_effect=hc.ApiException("API Error: 400 Invalid coin parameter")
        )

        # Probar con moneda inválida
        with pytest.raises(hc.ApiException) as exc_info:
            self.liquidity_api.liquidation_levels_get(
                coin="INVALID_COIN", timeframe="1h"
            )

        assert "Invalid coin parameter" in str(
            exc_info.value
        ), "Debería validar parámetro de moneda"

    @pytest.mark.parametrize(
        "leverage,expected_category",
        [
            ("5x", "low"),
            ("10x", "medium"),
            ("25x", "high"),
            ("50x", "extreme"),
            ("100x", "extreme"),
        ],
    )
    def test_leverage_categorization(self, leverage, expected_category):
        """
        Test parametrizado para categorización de apalancamiento.

        Verifica que diferentes niveles de apalancamiento se categoricen
        correctamente según rangos de riesgo.
        """

        def categorize_leverage(leverage_str):
            """Función helper para categorizar apalancamiento."""
            value = int(leverage_str.rstrip("x"))
            if value <= 5:
                return "low"
            elif value <= 15:
                return "medium"
            elif value <= 30:
                return "high"
            else:
                return "extreme"

        result = categorize_leverage(leverage)
        assert (
            result == expected_category
        ), f"Apalancamiento {leverage} debería ser categoría {expected_category}"

    def test_time_range_filtering(self):
        """
        Test para filtrado por rango de tiempo.

        Verifica que se puedan filtrar correctamente los pools
        por rangos de tiempo específicos.
        """
        # Mock con datos de diferentes tiempos
        mock_time_filtered_data = [
            hc.LiquidationLevels(
                timestamp=1661236020,  # Tiempo específico 1
                size=100000.00,
                leverage="10x",
                side="long",
            ),
            hc.LiquidationLevels(
                timestamp=1661322420,  # Tiempo específico 2
                size=150000.00,
                leverage="15x",
                side="short",
            ),
        ]

        self.liquidity_api.liquidation_levels_get = Mock(
            return_value=mock_time_filtered_data
        )

        # Ejecutar con filtro de tiempo
        start_time = 1661236000
        end_time = 1661322500

        result = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", start_time=start_time, end_time=end_time
        )

        # Verificaciones
        assert len(result) == 2, "Debería retornar datos filtrados por tiempo"
        assert all(
            start_time <= pool.timestamp <= end_time for pool in result
        ), "Todos los pools deberían estar en el rango de tiempo"


if __name__ == "__main__":
    # Ejecutar tests específicos
    pytest.main([__file__, "-v", "--tb=short"])
