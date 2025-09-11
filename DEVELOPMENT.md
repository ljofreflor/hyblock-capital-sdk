# Guía de Desarrollo - Hyblock Capital SDK

## 🔄 Flujo de Trabajo de Desarrollo

### **Generación Local del SDK**

El SDK se genera **localmente** y se committea al repositorio. **No se regenera automáticamente en CI/CD**.

#### **1. Generar SDK Localmente**

```bash
# Clonar el repositorio
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Instalar dependencias
poetry install --with dev

# Generar el SDK desde la especificación OpenAPI
./generate_sdk.sh
```

#### **2. Committear Cambios**

```bash
# Revisar cambios generados
git status
git diff

# Committear el SDK actualizado
git add .
git commit -m "feat: actualizar SDK con últimos cambios de la API"
git push origin main
```

#### **3. Regenerar SDK (Cuando Sea Necesario)**

**⚠️ Solo regenerar cuando:**
- La API de Hyblock Capital tenga cambios
- Se necesiten nuevos endpoints
- Haya cambios en la especificación OpenAPI

```bash
# Limpiar SDK actual
rm -rf hyblock_capital_sdk/

# Regenerar completamente
./generate_sdk.sh

# Revisar cambios y committear
git add .
git commit -m "feat: regenerar SDK con especificación OpenAPI actualizada"
```

## 🚀 CI/CD Simplificado

### **Qué Hace el CI/CD Ahora:**

✅ **Tests**: Ejecuta todos los tests en múltiples versiones de Python
✅ **Linting**: Verifica calidad de código
✅ **Build**: Construye el paquete para PyPI
✅ **Security**: Análisis de vulnerabilidades
✅ **Deploy**: Publica en PyPI (con tags)

❌ **No Regenera SDK**: El código ya está en el repositorio

### **Jobs del Pipeline:**

1. **`lint-and-test`**: Tests y calidad de código
2. **`build-and-test`**: Construcción del paquete
3. **`security-scan`**: Análisis de seguridad
4. **`generate-sdk`**: Solo manual o con `[generate-sdk]` en commit
5. **`publish-test`**: Publica en Test PyPI (branch develop)
6. **`publish`**: Publica en PyPI oficial (tags)

## 🛠️ Comandos de Desarrollo

### **Testing**
```bash
# Tests completos
make test

# Tests específicos
poetry run pytest tests/test_liquidation_pools.py -v

# Coverage
poetry run pytest --cov=hyblock_capital_sdk
```

### **Calidad de Código**
```bash
# Verificar todo
make check

# Solo linting
make lint

# Formatear código
make format
```

### **Construcción**
```bash
# Limpiar dist anterior
make clean-dist

# Construir paquete
make build-dist

# Verificar paquete
make check-dist
```

## 🔧 Regeneración Manual de SDK

### **Opción 1: Localmente (Recomendado)**
```bash
./generate_sdk.sh
git add .
git commit -m "feat: actualizar SDK"
git push
```

### **Opción 2: GitHub Actions Manual**
```bash
# Commit con mensaje especial
git commit -m "feat: nueva funcionalidad [generate-sdk]"
git push

# O ejecutar workflow manualmente desde GitHub Actions UI
```

### **Opción 3: GitHub Actions UI**
1. Ir a Actions tab en GitHub
2. Seleccionar "CI/CD Pipeline"
3. Click "Run workflow"
4. Ejecutar manualmente

## 📋 Checklist de Release

### **Antes de Release:**

- [ ] ✅ SDK generado con última especificación
- [ ] ✅ Tests pasando (`make test`)
- [ ] ✅ Linting correcto (`make check`)
- [ ] ✅ Versión actualizada en `pyproject.toml`
- [ ] ✅ CHANGELOG.md actualizado
- [ ] ✅ Commit y push de cambios

### **Para Release:**

```bash
# Actualizar versión
poetry version patch  # o minor/major

# Crear tag
git tag v$(poetry version -s)
git push origin v$(poetry version -s)

# GitHub Actions publicará automáticamente en PyPI
```

## 🐛 Solución de Problemas

### **Error: "SDK no encontrado"**
```bash
# El SDK no está en el repositorio
./generate_sdk.sh
git add hyblock_capital_sdk/
git commit -m "fix: agregar SDK generado"
```

### **Error: "Timeout al descargar OpenAPI spec"**
```bash
# Verificar conexión
curl -s https://media.hyblockcapital.com/document/swagger-dev.json

# El script tiene retry automático, verificar logs
```

### **Tests fallando después de regenerar SDK**
```bash
# Actualizar tests si hay cambios en la API
poetry run pytest tests/ -v

# Revisar si hay breaking changes en la API
```

## 📚 Recursos

- **Documentación OpenAPI Generator**: https://openapi-generator.tech
- **API de Hyblock Capital**: https://docs.hyblock.capital
- **Poetry Documentation**: https://python-poetry.org/docs/

---

**Ventajas del Nuevo Flujo:**
- ⚡ CI/CD más rápido (no descarga externa)
- 🔒 Más confiable (no depende de API externa)
- 🎯 Control total sobre cuándo regenerar
- 🔍 Fácil review de cambios en el SDK