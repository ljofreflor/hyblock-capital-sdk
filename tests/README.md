# Tests del SDK de Hyblock Capital

Esta documentación describe los tests unitarios y de integración disponibles para el SDK de Hyblock Capital, enfocándose en los pools de liquidación.

## 📋 Resumen de Tests

### **Tests Unitarios** (`test_liquidation_pools.py`)
- **13 tests** que validan funcionalidad específica de pools de liquidación
- Usan **mocks** para simular respuestas de la API
- **No requieren** credenciales reales ni conexión a internet
- Cobertura de todos los métodos principales de la `LiquidityApi`

### **Tests de Integración** (`test_liquidation_integration.py`)
- **4 tests** que simulan flujos completos de análisis 
- Pruebas de **workflows end-to-end** con múltiples APIs
- Análisis de **correlaciones** y **patrones** en los datos
- Comparaciones entre **múltiples exchanges**

## 🚀 Cómo Ejecutar los Tests

### **Todos los tests de liquidación:**
```bash
poetry run pytest tests/test_liquidation_pools.py tests/test_liquidation_integration.py -v
```

### **Solo tests unitarios:**
```bash
poetry run pytest tests/test_liquidation_pools.py -v
```

### **Solo tests de integración:**
```bash
poetry run pytest tests/test_liquidation_integration.py -v
```

### **Tests con coverage:**
```bash
poetry run pytest tests/test_liquidation_pools.py tests/test_liquidation_integration.py --cov=hyblock_capital_sdk --cov-report=html
```

### **Tests parametrizados (categorización de apalancamiento):**
```bash
poetry run pytest tests/test_liquidation_pools.py::TestLiquidationPools::test_leverage_categorization -v
```

## 🧪 Descripción de Tests Específicos

### **Tests Unitarios**

#### 1. `test_liquidation_levels_get_success`
- **Objetivo**: Verificar obtención de niveles específicos de liquidación
- **Datos mock**: Pools con diferentes apalancamientos (5x, 10x, 25x)
- **Validaciones**: Estructura de datos, apalancamiento incluido, tamaños correctos

#### 2. `test_cumulative_liq_level_get_success`
- **Objetivo**: Probar niveles acumulativos de liquidación
- **Datos mock**: Agregaciones por timestamp con conteos long/short
- **Validaciones**: Campos de liquidación acumulativa correctos

#### 3. `test_anchored_liq_levels_count_get_long_short`
- **Objetivo**: Validar conteos anclados separados por tipo
- **Datos mock**: Conteos diferentes para long (42) y short (38)
- **Validaciones**: Conteos correctos y timestamps válidos

#### 4. `test_liquidation_get_historical_events`
- **Objetivo**: Verificar eventos históricos de liquidación
- **Datos mock**: Eventos con totales long/short por período
- **Validaciones**: Agregaciones correctas, buckets de tamaño

#### 5. `test_liquidation_heatmap_get_success`
- **Objetivo**: Probar heatmap de liquidaciones
- **Datos mock**: Rangos de precios con densidades
- **Validaciones**: Rangos de precios correctos, tamaños agregados

#### 6. `test_api_exception_handling`
- **Objetivo**: Manejo de excepciones de API
- **Simula**: Error 401 Unauthorized
- **Validaciones**: Excepción capturada correctamente

#### 7. `test_invalid_parameters_validation`
- **Objetivo**: Validación de parámetros inválidos
- **Simula**: Moneda no soportada
- **Validaciones**: Error 400 para parámetros incorrectos

#### 8. `test_leverage_categorization` (Parametrizado)
- **Objetivo**: Categorización de niveles de apalancamiento
- **Parámetros**: 5x→low, 10x→medium, 25x→high, 50x/100x→extreme
- **Validaciones**: Categorización correcta según nivel de riesgo

#### 9. `test_time_range_filtering`
- **Objetivo**: Filtrado por rangos de tiempo
- **Datos mock**: Pools con timestamps específicos
- **Validaciones**: Filtros temporales funcionando

### **Tests de Integración**

#### 1. `test_complete_liquidation_analysis_workflow`
- **Objetivo**: Flujo completo de análisis de liquidación
- **Simula**: Catálogo + niveles + acumulativos + conteos + análisis
- **Validaciones**: 
  - Catálogo con BTC disponible
  - Análisis de apalancamiento por categorías
  - Correlación inversá: alto apalancamiento = menor duración
  - Datos acumulativos crecientes
  - Conteos long vs short balanceados

#### 2. `test_risk_analysis_by_leverage_categories`
- **Objetivo**: Análisis de riesgo por categorías de apalancamiento
- **Simula**: Pools con diferentes niveles de riesgo
- **Validaciones**:
  - Distribución correcta por categorías de riesgo
  - Correlación: mayor apalancamiento = menor duración
  - Concentración de tamaño en bajo riesgo

#### 3. `test_multi_exchange_comparison`
- **Objetivo**: Comparación entre múltiples exchanges
- **Simula**: Datos de Binance vs Bybit
- **Validaciones**:
  - Análisis comparativo de tamaños totales
  - Distribución long/short por exchange
  - Métricas de apalancamiento promedio

#### 4. `test_time_based_analysis_with_mocked_time`
- **Objetivo**: Análisis temporal con tiempo controlado
- **Simula**: Tiempo fijo usando `@patch('time.time')`
- **Validaciones**:
  - Análisis de períodos de dominancia long/short
  - Totales agregados correctos por período
  - Uso correcto del tiempo mockeado

## 🎯 Casos de Uso Cubiertos

### **✅ Funcionalidad Básica**
- Obtención de pools de liquidación
- Niveles acumulativos
- Conteos anclados
- Eventos históricos
- Heatmaps de liquidación

### **✅ Manejo de Errores**
- Excepciones de API (401, 400, 500)
- Parámetros inválidos
- Conexiones fallidas
- Timeouts

### **✅ Análisis Avanzado**
- Categorización por apalancamiento
- Análisis de riesgo
- Comparación entre exchanges
- Correlaciones temporales
- Agregaciones por período

### **✅ Validaciones de Datos**
- Estructura de respuestas
- Tipos de datos correctos
- Rangos de valores válidos
- Consistencia entre endpoints

## 🔧 Configuración de Mocks

Los tests usan mocks para simular:

### **Datos de Liquidación**
```python
mock_liquidation_levels = [
    hc.LiquidationLevels(
        timestamp=1661236020,
        size=125000.50,
        price=21450.25,
        leverage="10x",        # ✅ Apalancamiento incluido
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

## 📊 Métricas de Cobertura

Los tests actuales cubren:
- **LiquidityApi**: ~20% de cobertura de líneas
- **Modelos de datos**: ~55% de cobertura promedio
- **Manejo de errores**: Casos principales cubiertos
- **Flujos de integración**: Workflows end-to-end validados

## 🎭 Ventajas de Usar Mocks

### **✅ Velocidad**
- Tests ejecutan en **< 3 segundos**
- No dependen de conexión a internet
- No requieren credenciales reales

### **✅ Confiabilidad**
- Resultados **100% reproducibles**
- No afectados por estado de la API
- Control total sobre datos de prueba

### **✅ Cobertura**
- Prueba casos de **error** difíciles de reproducir
- Valida **edge cases** específicos  
- Simula **diferentes escenarios** fácilmente

### **✅ Aislamiento**
- Cada test es **independiente**
- No hay **efectos secundarios**
- Fácil debugging de fallos

## 🚀 Próximos Pasos

Para expandir la cobertura de tests:

1. **Más endpoints**: Tests para otras APIs (Orderbook, Sentiment, etc.)
2. **Tests de performance**: Validar tiempos de respuesta
3. **Tests de stress**: Múltiples requests concurrentes
4. **Validación de datos reales**: Ocasionales tests con API real
5. **Tests de regresión**: Para cambios en el SDK generado

## 💡 Ejecutar Tests Específicos

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

**🎯 Recuerda**: Estos tests validan que el apalancamiento **YA está incluido** en los pools de liquidación. No necesitas calcularlo manualmente - Hyblock Capital lo proporciona pre-procesado en cada pool.
