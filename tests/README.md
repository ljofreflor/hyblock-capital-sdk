# Hyblock Capital SDK Tests

This documentation describes the unit and integration tests available for the Hyblock Capital SDK, focusing on liquidation pools.

## Test Summary

### **Unit Tests** (`test_liquidation_pools.py`)
- **13 tests** that validate specific liquidation pool functionality
- Use **mocks** to simulate API responses
- **Do not require** real credentials or internet connection
- Coverage of all main methods in `LiquidityApi`

### **Integration Tests** (`test_liquidation_integration.py`)
- **4 tests** that simulate complete analysis flows
- **End-to-end workflow** tests with multiple APIs
- Analysis of **correlations** and **patterns** in data
- Comparisons between **multiple exchanges**

## How to Run Tests

### **All liquidation tests:**
```bash
poetry run pytest tests/test_liquidation_pools.py tests/test_liquidation_integration.py -v
```

### **Unit tests only:**
```bash
poetry run pytest tests/test_liquidation_pools.py -v
```

### **Integration tests only:**
```bash
poetry run pytest tests/test_liquidation_integration.py -v
```

### **Tests with coverage:**
```bash
poetry run pytest tests/test_liquidation_pools.py tests/test_liquidation_integration.py --cov=hyblock_capital_sdk --cov-report=html
```

### **Parametrized tests (leverage categorization):**
```bash
poetry run pytest tests/test_liquidation_pools.py::TestLiquidationPools::test_leverage_categorization -v
```

## Specific Test Descriptions

### **Unit Tests**

#### 1. `test_liquidation_levels_get_success`
- **Objective**: Verify retrieval of specific liquidation levels
- **Mock data**: Pools with different leverages (5x, 10x, 25x)
- **Validations**: Data structure, leverage included, correct sizes

#### 2. `test_cumulative_liq_level_get_success`
- **Objective**: Test cumulative liquidation levels
- **Mock data**: Aggregations by timestamp with long/short counts
- **Validations**: Correct cumulative liquidation fields

#### 3. `test_anchored_liq_levels_count_get_long_short`
- **Objective**: Validate anchored counts separated by type
- **Mock data**: Different counts for long (42) and short (38)
- **Validations**: Correct counts and valid timestamps

#### 4. `test_liquidation_get_historical_events`
- **Objective**: Verify historical liquidation events
- **Mock data**: Events with long/short totals by period
- **Validations**: Correct aggregations, size buckets

#### 5. `test_liquidation_heatmap_get_success`
- **Objective**: Test liquidation heatmap
- **Mock data**: Price ranges with densities
- **Validations**: Correct price ranges, aggregated sizes

#### 6. `test_api_exception_handling`
- **Objective**: API exception handling
- **Simulates**: 401 Unauthorized error
- **Validations**: Exception caught correctly

#### 7. `test_invalid_parameters_validation`
- **Objective**: Invalid parameter validation
- **Simulates**: Unsupported currency
- **Validations**: 400 error for incorrect parameters

#### 8. `test_leverage_categorization` (Parametrized)
- **Objective**: Leverage level categorization
- **Parameters**: 5x→low, 10x→medium, 25x→high, 50x/100x→extreme
- **Validations**: Correct categorization according to risk level

#### 9. `test_time_range_filtering`
- **Objective**: Time range filtering
- **Mock data**: Pools with specific timestamps
- **Validations**: Temporal filters working

### **Integration Tests**

#### 1. `test_complete_liquidation_analysis_workflow`
- **Objective**: Complete liquidation analysis workflow
- **Simulates**: Catalog + levels + cumulative + counts + analysis
- **Validations**: 
  - Catalog with BTC available
  - Leverage analysis by categories
  - Inverse correlation: high leverage = shorter duration
  - Increasing cumulative data
  - Balanced long vs short counts

#### 2. `test_risk_analysis_by_leverage_categories`
- **Objective**: Risk analysis by leverage categories
- **Simulates**: Pools with different risk levels
- **Validations**:
  - Correct distribution by risk categories
  - Correlation: higher leverage = shorter duration
  - Size concentration in low risk

#### 3. `test_multi_exchange_comparison`
- **Objective**: Comparison between multiple exchanges
- **Simulates**: Data from Binance vs Bybit
- **Validations**:
  - Comparative analysis of total sizes
  - Long/short distribution by exchange
  - Average leverage metrics

#### 4. `test_time_based_analysis_with_mocked_time`
- **Objective**: Time-based analysis with controlled time
- **Simulates**: Fixed time using `@patch('time.time')`
- **Validations**:
  - Analysis of long/short dominance periods
  - Correct aggregated totals by period
  - Correct use of mocked time

## Use Cases Covered

### **Basic Functionality**
- Obtención de pools de liquidación
- Niveles acumulativos
- Conteos anclados
- Eventos históricos
- Heatmaps de liquidación

### **Error Handling**
- Excepciones de API (401, 400, 500)
- Parámetros inválidos
- Conexiones fallidas
- Timeouts

### **Advanced Analysis**
- Categorización por apalancamiento
- Análisis de riesgo
- Comparación entre exchanges
- Correlaciones temporales
- Agregaciones por período

### **Data Validations**
- Estructura de respuestas
- Tipos de datos correctos
- Rangos de valores válidos
- Consistencia entre endpoints

## Mock Configuration

Los tests usan mocks para simular:

### **Datos de Liquidación**
```python
mock_liquidation_levels = [
    hc.LiquidationLevels(
        timestamp=1661236020,
        size=125000.50,
        price=21450.25,
        leverage="10x",        # Leverage included
        side="long",
        open_duration=3600
    )
]
```

### **Datos Acumulativos**
```python
mock_cumulative_data = [
    hc.CumulativeLiqLevel(
        timestamp=1661236020,
        total_long_liquidation_size=300000.00,
        total_short_liquidation_size=200000.00,
        total_long_liquidation_count=15
    )
]
```

### **Conteos Anclados**
```python
mock_count = hc.AnchoredLiqLevelsCount(
    open_date=1661236020,
    total_count=42
)
```

## Coverage Metrics

Los tests actuales cubren:
- **LiquidityApi**: ~20% de cobertura de líneas
- **Modelos de datos**: ~55% de cobertura promedio
- **Manejo de errores**: Casos principales cubiertos
- **Flujos de integración**: Workflows end-to-end validados

## Advantages of Using Mocks

### **Speed**
- Tests ejecutan en **< 3 segundos**
- No dependen de conexión a internet
- No requieren credenciales reales

### **Reliability**
- Resultados **100% reproducibles**
- No afectados por estado de la API
- Control total sobre datos de prueba

### **Coverage**
- Prueba casos de **error** difíciles de reproducir
- Valida **edge cases** específicos  
- Simula **diferentes escenarios** fácilmente

### **Isolation**
- Cada test es **independiente**
- No hay **efectos secundarios**
- Fácil debugging de fallos

## Next Steps

Para expandir la cobertura de tests:

1. **Más endpoints**: Tests para otras APIs (Orderbook, Sentiment, etc.)
2. **Tests de performance**: Validar tiempos de respuesta
3. **Tests de stress**: Múltiples requests concurrentes
4. **Validación de datos reales**: Ocasionales tests con API real
5. **Tests de regresión**: Para cambios en el SDK generado

## Run Specific Tests

```bash
# Test específico por nombre
poetry run pytest tests/test_liquidation_pools.py::TestLiquidationPools::test_liquidation_levels_get_success -v

# Tests que contienen "leverage" en el nombre
poetry run pytest tests/ -k "leverage" -v

# Tests marcados como "slow" (si los hay)
poetry run pytest tests/ -m slow -v

# Tests con output detallado
poetry run pytest tests/test_liquidation_pools.py -v -s

# Tests con coverage detallado
poetry run pytest tests/test_liquidation_pools.py --cov=hyblock_capital_sdk.api.liquidity_api --cov-report=term-missing
```

---

**Remember**: These tests validate that leverage **is already included** in liquidation pools. You don't need to calculate it manually - Hyblock Capital provides it pre-processed in each pool.
