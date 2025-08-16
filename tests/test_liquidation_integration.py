#!/usr/bin/env python3
"""
Tests de integración para análisis completo de pools de liquidación
usando mocks avanzados para simular escenarios reales.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time
from datetime import datetime, timedelta

import hyblock_capital_sdk as hc


class TestLiquidationPoolsIntegration:
    """Tests de integración para análisis completo de pools."""

    def setup_method(self):
        """Configurar entorno de test para cada método."""
        self.config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
        self.config.api_key = {"x-api-key": "test-api-key"}

        # Crear mocks para todas las APIs necesarias
        self.api_client_mock = Mock(spec=hc.ApiClient)
        self.liquidity_api = hc.LiquidityApi(self.api_client_mock)
        self.catalog_api = hc.CatalogApi(self.api_client_mock)

    def test_complete_liquidation_analysis_workflow(self):
        """
        Test de flujo completo de análisis de liquidación.

        Simula un análisis completo obteniendo:
        1. Catálogo de monedas disponibles
        2. Niveles específicos de liquidación
        3. Datos acumulativos
        4. Conteos anclados
        5. Análisis de apalancamiento
        """
        # 1. Mock del catálogo (usando diccionario simple)
        mock_catalog = {
            "binance": ["BTC", "ETH", "ADA", "DOT"],
            "bybit": ["BTC", "ETH", "SOL"],
            "okx": ["BTC", "ETH", "AVAX"],
        }
        self.catalog_api.catalog_get = Mock(return_value=mock_catalog)

        # 2. Mock de niveles específicos con diferentes apalancamientos
        mock_liquidation_levels = [
            hc.LiquidationLevels(
                timestamp=1661236020,
                size=125000.00,
                price=21450.25,
                leverage="10x",
                side="long",
                open_duration=3600,
            ),
            hc.LiquidationLevels(
                timestamp=1661236080,
                size=89000.75,
                price=21380.15,
                leverage="25x",
                side="short",
                open_duration=1800,
            ),
            hc.LiquidationLevels(
                timestamp=1661236140,
                size=250000.00,
                price=21500.00,
                leverage="5x",
                side="long",
                open_duration=7200,
            ),
            hc.LiquidationLevels(
                timestamp=1661236200,
                size=75000.00,
                price=21320.00,
                leverage="50x",
                side="short",
                open_duration=900,
            ),
        ]
        self.liquidity_api.liquidation_levels_get = Mock(
            return_value=mock_liquidation_levels
        )

        # 3. Mock de datos acumulativos
        mock_cumulative = [
            hc.CumulativeLiqLevel(
                timestamp=1661236020,
                total_long_liquidation_size=300000.00,
                total_short_liquidation_size=200000.00,
                total_long_liquidation_count=15,
            ),
            hc.CumulativeLiqLevel(
                timestamp=1661236080,
                total_long_liquidation_size=450000.00,
                total_short_liquidation_size=300000.00,
                total_long_liquidation_count=23,
            ),
        ]
        self.liquidity_api.cumulative_liq_level_get = Mock(return_value=mock_cumulative)

        # 4. Mock de conteos anclados
        mock_long_count = hc.AnchoredLiqLevelsCount(
            open_date=1661236020, total_count=42
        )
        mock_short_count = hc.AnchoredLiqLevelsCount(
            open_date=1661236020, total_count=38
        )

        # Configurar side_effect para diferentes llamadas
        self.liquidity_api.anchored_liq_levels_count_get = Mock()
        self.liquidity_api.anchored_liq_levels_count_get.side_effect = [
            mock_long_count,
            mock_short_count,
        ]

        # EJECUTAR ANÁLISIS COMPLETO

        # Paso 1: Obtener catálogo
        catalog = self.catalog_api.catalog_get()

        # Paso 2: Verificar que BTC esté disponible
        available_exchanges = []
        if "binance" in catalog and "BTC" in catalog["binance"]:
            available_exchanges.append("binance")
        if "bybit" in catalog and "BTC" in catalog["bybit"]:
            available_exchanges.append("bybit")

        assert (
            len(available_exchanges) >= 1
        ), "BTC debería estar disponible en al menos un exchange"

        # Paso 3: Obtener niveles de liquidación
        liquidation_levels = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", exchange="binance", limit=20
        )

        # Paso 4: Análisis de apalancamiento
        leverage_analysis = {}
        total_size = 0

        for level in liquidation_levels:
            leverage = level.leverage
            if leverage not in leverage_analysis:
                leverage_analysis[leverage] = {
                    "count": 0,
                    "total_size": 0,
                    "avg_duration": 0,
                }

            leverage_analysis[leverage]["count"] += 1
            leverage_analysis[leverage]["total_size"] += level.size
            leverage_analysis[leverage]["avg_duration"] += level.open_duration
            total_size += level.size

        # Calcular promedios
        for leverage_data in leverage_analysis.values():
            leverage_data["avg_duration"] /= leverage_data["count"]

        # Paso 5: Obtener datos acumulativos
        cumulative_data = self.liquidity_api.cumulative_liq_level_get(
            coin="BTC", timeframe="1h", exchange="binance", sort="desc", limit=10
        )

        # Paso 6: Obtener conteos long/short
        long_count = self.liquidity_api.anchored_liq_levels_count_get(
            coin="BTC", timeframe="1h", level="long", anchor="1d"
        )

        short_count = self.liquidity_api.anchored_liq_levels_count_get(
            coin="BTC", timeframe="1h", level="short", anchor="1d"
        )

        # VERIFICACIONES DEL ANÁLISIS COMPLETO

        # Verificar catálogo
        assert "BTC" in catalog["binance"], "BTC debería estar en Binance"
        assert len(available_exchanges) >= 1, "Debería haber exchanges disponibles"

        # Verificar niveles de liquidación
        assert len(liquidation_levels) == 4, "Debería haber 4 niveles de liquidación"
        assert total_size == 539000.75, "Tamaño total debería ser correcto"

        # Verificar análisis de apalancamiento
        assert "10x" in leverage_analysis, "Debería incluir apalancamiento 10x"
        assert "25x" in leverage_analysis, "Debería incluir apalancamiento 25x"
        assert "5x" in leverage_analysis, "Debería incluir apalancamiento 5x"
        assert "50x" in leverage_analysis, "Debería incluir apalancamiento 50x"

        # Verificar que 50x tiene menor duración (más riesgoso)
        assert (
            leverage_analysis["50x"]["avg_duration"]
            < leverage_analysis["5x"]["avg_duration"]
        ), "Apalancamiento alto debería tener menor duración promedio"

        # Verificar datos acumulativos
        assert len(cumulative_data) == 2, "Debería haber 2 niveles acumulativos"
        assert (
            cumulative_data[1].total_long_liquidation_size
            > cumulative_data[0].total_long_liquidation_size
        ), "Segundo nivel debería tener mayor tamaño long acumulativo"

        # Verificar conteos
        assert long_count.total_count == 42, "Conteo long debería ser 42"
        assert short_count.total_count == 38, "Conteo short debería ser 38"

        # Verificar que se hicieron todas las llamadas esperadas
        self.catalog_api.catalog_get.assert_called_once()
        self.liquidity_api.liquidation_levels_get.assert_called_once()
        self.liquidity_api.cumulative_liq_level_get.assert_called_once()
        assert self.liquidity_api.anchored_liq_levels_count_get.call_count == 2

    def test_risk_analysis_by_leverage_categories(self):
        """
        Test para análisis de riesgo por categorías de apalancamiento.

        Simula análisis de riesgo clasificando pools por niveles
        de apalancamiento y calculando métricas de riesgo.
        """
        # Mock con datos variados de riesgo
        mock_risk_data = [
            # Bajo riesgo
            hc.LiquidationLevels(
                size=300000, leverage="2x", side="long", open_duration=86400
            ),
            hc.LiquidationLevels(
                size=250000, leverage="3x", side="long", open_duration=72000
            ),
            hc.LiquidationLevels(
                size=200000, leverage="5x", side="short", open_duration=43200
            ),
            # Medio riesgo
            hc.LiquidationLevels(
                size=150000, leverage="10x", side="long", open_duration=21600
            ),
            hc.LiquidationLevels(
                size=120000, leverage="15x", side="short", open_duration=14400
            ),
            # Alto riesgo
            hc.LiquidationLevels(
                size=80000, leverage="25x", side="long", open_duration=7200
            ),
            hc.LiquidationLevels(
                size=60000, leverage="30x", side="short", open_duration=5400
            ),
            # Extremo riesgo
            hc.LiquidationLevels(
                size=40000, leverage="50x", side="long", open_duration=1800
            ),
            hc.LiquidationLevels(
                size=25000, leverage="100x", side="short", open_duration=900
            ),
        ]

        self.liquidity_api.liquidation_levels_get = Mock(return_value=mock_risk_data)

        # Ejecutar obtención de datos
        pools = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", exchange="binance"
        )

        # Función de categorización de riesgo
        def categorize_risk(leverage_str):
            value = int(leverage_str.rstrip("x"))
            if value <= 5:
                return "low"
            elif value <= 15:
                return "medium"
            elif value <= 30:
                return "high"
            else:
                return "extreme"

        # Análisis de riesgo
        risk_analysis = {
            "low": {"count": 0, "total_size": 0, "avg_duration": 0},
            "medium": {"count": 0, "total_size": 0, "avg_duration": 0},
            "high": {"count": 0, "total_size": 0, "avg_duration": 0},
            "extreme": {"count": 0, "total_size": 0, "avg_duration": 0},
        }

        for pool in pools:
            risk_category = categorize_risk(pool.leverage)
            risk_analysis[risk_category]["count"] += 1
            risk_analysis[risk_category]["total_size"] += pool.size
            risk_analysis[risk_category]["avg_duration"] += pool.open_duration

        # Calcular promedios
        for category in risk_analysis.values():
            if category["count"] > 0:
                category["avg_duration"] /= category["count"]

        # Verificaciones de análisis de riesgo
        assert (
            risk_analysis["low"]["count"] == 3
        ), "Debería haber 3 pools de bajo riesgo"
        assert (
            risk_analysis["medium"]["count"] == 2
        ), "Debería haber 2 pools de riesgo medio"
        assert (
            risk_analysis["high"]["count"] == 2
        ), "Debería haber 2 pools de alto riesgo"
        assert (
            risk_analysis["extreme"]["count"] == 2
        ), "Debería haber 2 pools de riesgo extremo"

        # Verificar correlación inversa: mayor apalancamiento = menor duración
        assert (
            risk_analysis["low"]["avg_duration"]
            > risk_analysis["medium"]["avg_duration"]
        ), "Bajo riesgo debería tener mayor duración promedio"
        assert (
            risk_analysis["medium"]["avg_duration"]
            > risk_analysis["high"]["avg_duration"]
        ), "Riesgo medio debería tener mayor duración que alto riesgo"
        assert (
            risk_analysis["high"]["avg_duration"]
            > risk_analysis["extreme"]["avg_duration"]
        ), "Alto riesgo debería tener mayor duración que riesgo extremo"

        # Verificar concentración de tamaño por riesgo
        low_risk_size = risk_analysis["low"]["total_size"]
        extreme_risk_size = risk_analysis["extreme"]["total_size"]
        assert (
            low_risk_size > extreme_risk_size
        ), "Pools de bajo riesgo deberían tener mayor tamaño total"

    def test_multi_exchange_comparison(self):
        """
        Test para comparación entre múltiples exchanges.

        Simula obtención de datos de diferentes exchanges
        para análisis comparativo de pools de liquidación.
        """
        # Mock para Binance
        mock_binance_data = [
            hc.LiquidationLevels(size=200000, leverage="10x", side="long"),
            hc.LiquidationLevels(size=150000, leverage="20x", side="short"),
            hc.LiquidationLevels(size=300000, leverage="5x", side="long"),
        ]

        # Mock para Bybit
        mock_bybit_data = [
            hc.LiquidationLevels(size=180000, leverage="15x", side="long"),
            hc.LiquidationLevels(size=120000, leverage="25x", side="short"),
            hc.LiquidationLevels(size=250000, leverage="8x", side="long"),
        ]

        # Configurar mocks para diferentes exchanges
        def side_effect_function(*args, **kwargs):
            exchange = kwargs.get("exchange")
            if exchange == "binance":
                return mock_binance_data
            elif exchange == "bybit":
                return mock_bybit_data
            else:
                return []

        self.liquidity_api.liquidation_levels_get = Mock(
            side_effect=side_effect_function
        )

        # Obtener datos de ambos exchanges
        binance_pools = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", exchange="binance"
        )

        bybit_pools = self.liquidity_api.liquidation_levels_get(
            coin="BTC", timeframe="1h", exchange="bybit"
        )

        # Análisis comparativo
        def analyze_exchange_data(pools, exchange_name):
            return {
                "exchange": exchange_name,
                "total_pools": len(pools),
                "total_size": sum(pool.size for pool in pools),
                "avg_leverage": sum(int(pool.leverage.rstrip("x")) for pool in pools)
                / len(pools),
                "long_pools": len([p for p in pools if p.side == "long"]),
                "short_pools": len([p for p in pools if p.side == "short"]),
            }

        binance_analysis = analyze_exchange_data(binance_pools, "binance")
        bybit_analysis = analyze_exchange_data(bybit_pools, "bybit")

        # Verificaciones
        assert binance_analysis["total_pools"] == 3, "Binance debería tener 3 pools"
        assert bybit_analysis["total_pools"] == 3, "Bybit debería tener 3 pools"

        assert binance_analysis["total_size"] == 650000, "Tamaño total Binance correcto"
        assert bybit_analysis["total_size"] == 550000, "Tamaño total Bybit correcto"

        # Verificar que se llamó a cada exchange
        assert self.liquidity_api.liquidation_levels_get.call_count == 2

        # Verificar distribución long/short en cada exchange
        assert binance_analysis["long_pools"] == 2, "Binance debería tener 2 pools long"
        assert (
            binance_analysis["short_pools"] == 1
        ), "Binance debería tener 1 pool short"
        assert bybit_analysis["long_pools"] == 2, "Bybit debería tener 2 pools long"
        assert bybit_analysis["short_pools"] == 1, "Bybit debería tener 1 pool short"

    @patch("time.time")
    def test_time_based_analysis_with_mocked_time(self, mock_time):
        """
        Test para análisis basado en tiempo usando tiempo mockeado.

        Simula análisis temporal controlando el tiempo del sistema
        para pruebas reproducibles.
        """
        # Configurar tiempo mockeado
        base_time = 1661236020  # Tiempo base fijo
        mock_time.return_value = base_time

        # Mock de datos históricos con diferentes timestamps
        mock_historical_data = [
            hc.Liquidation(
                open_date=base_time - 3600,  # 1 hora atrás
                long_liquidation=500000,
                short_liquidation=300000,
            ),
            hc.Liquidation(
                open_date=base_time - 7200,  # 2 horas atrás
                long_liquidation=750000,
                short_liquidation=450000,
            ),
            hc.Liquidation(
                open_date=base_time - 10800,  # 3 horas atrás
                long_liquidation=600000,
                short_liquidation=800000,
            ),
        ]

        self.liquidity_api.liquidation_get = Mock(return_value=mock_historical_data)

        # Calcular rango de tiempo
        current_time = int(time.time())
        start_time = current_time - (4 * 3600)  # 4 horas atrás

        # Ejecutar análisis temporal
        historical_liquidations = self.liquidity_api.liquidation_get(
            coin="BTC",
            timeframe="1h",
            start_time=start_time,
            end_time=current_time,
            bucket="3,4,5",
        )

        # Análisis temporal
        temporal_analysis = {
            "total_periods": len(historical_liquidations),
            "total_long": sum(liq.long_liquidation for liq in historical_liquidations),
            "total_short": sum(
                liq.short_liquidation for liq in historical_liquidations
            ),
            "long_dominance_periods": len(
                [
                    liq
                    for liq in historical_liquidations
                    if liq.long_liquidation > liq.short_liquidation
                ]
            ),
            "short_dominance_periods": len(
                [
                    liq
                    for liq in historical_liquidations
                    if liq.short_liquidation > liq.long_liquidation
                ]
            ),
        }

        # Verificaciones temporales
        assert (
            temporal_analysis["total_periods"] == 3
        ), "Debería haber 3 períodos históricos"
        assert (
            temporal_analysis["total_long"] == 1850000
        ), "Total liquidaciones long correcto"
        assert (
            temporal_analysis["total_short"] == 1550000
        ), "Total liquidaciones short correcto"
        assert (
            temporal_analysis["long_dominance_periods"] == 2
        ), "2 períodos con dominancia long"
        assert (
            temporal_analysis["short_dominance_periods"] == 1
        ), "1 período con dominancia short"

        # Verificar que se usó el tiempo mockeado
        mock_time.assert_called()


if __name__ == "__main__":
    # Ejecutar todos los tests de integración
    pytest.main([__file__, "-v", "--tb=short"])
