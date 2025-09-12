# 🔐 Configuración de Credenciales PyPI para CI/CD

## 📋 **Resumen**

Este documento explica cómo configurar las credenciales de PyPI en GitHub Actions para automatizar la publicación del SDK.

## 🚀 **Configuración de GitHub Secrets**

### **Paso 1: Acceder a la configuración del repositorio**

1. Ve a tu repositorio en GitHub: `https://github.com/ljofreflor/hyblock-capital-sdk`
2. Haz clic en **Settings** (pestaña superior)
3. En el menú lateral izquierdo, haz clic en **Secrets and variables** → **Actions**

### **Paso 2: Crear los secrets necesarios**

Haz clic en **New repository secret** y crea los siguientes secrets:

#### **Para PyPI (Producción):**
- **Name**: `PYPI_TOKEN`
- **Value**: `[TU_TOKEN_REAL_DE_PYPI]` (formato: `pypi-...`)

#### **Para TestPyPI (Testing):**
- **Name**: `TEST_PYPI_TOKEN`
- **Value**: `[TU_TOKEN_REAL_DE_TESTPYPI]` (formato: `pypi-...`)

## 🔑 **Cómo obtener los tokens de PyPI**

### **Para PyPI (Producción):**

1. Ve a [PyPI.org](https://pypi.org) y haz login
2. Ve a **Account settings** → **API tokens**
3. Haz clic en **Add API token**
4. **Token name**: `hyblock-capital-sdk-ci`
5. **Scope**: `Entire account (all projects)` o `Specific project: hyblock-capital-sdk`
6. **Copia el token generado** (formato: `pypi-...`) - **NO lo compartas**

### **Para TestPyPI (Testing):**

1. Ve a [TestPyPI.org](https://test.pypi.org) y haz login
2. Ve a **Account settings** → **API tokens**
3. Haz clic en **Add API token**
4. **Token name**: `hyblock-capital-sdk-test-ci`
5. **Scope**: `Entire account (all projects)` o `Specific project: hyblock-capital-sdk`
6. **Copia el token generado** (formato: `pypi-...`) - **NO lo compartas**

## 🔄 **Cómo funciona el CI/CD**

### **Flujo de publicación:**

1. **Push a main/develop** → Ejecuta tests y linting
2. **Crear tag** → Ejecuta publicación automática a PyPI
3. **Pull Request** → Ejecuta tests y publicación a TestPyPI

### **Comandos para crear tags:**

```bash
# Incrementar versión
poetry version patch  # 0.1.0 → 0.1.1
poetry version minor  # 0.1.0 → 0.2.0
poetry version major  # 0.1.0 → 1.0.0

# Crear tag y push
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git tag v$(poetry version -s)
git push origin main
git push origin v$(poetry version -s)
```

## 🛡️ **Seguridad**

### **Buenas prácticas:**

- ✅ **Nunca** commitees tokens en el código
- ✅ **Usa** GitHub Secrets para credenciales
- ✅ **Rota** los tokens periódicamente
- ✅ **Usa** tokens con scope limitado cuando sea posible
- ✅ **Monitorea** el uso de los tokens

### **Verificación de seguridad:**

```bash
# Verificar que no hay tokens en el código
grep -r "pypi-" . --exclude-dir=.git
grep -r "PYPI_TOKEN" . --exclude-dir=.git
```

## 🧪 **Testing del CI/CD**

### **Probar TestPyPI:**

1. Haz un push a cualquier branch
2. Ve a **Actions** en GitHub
3. Verifica que el job `publish-testpypi` se ejecute
4. Revisa los logs para confirmar publicación exitosa

### **Probar PyPI:**

1. Crea un tag: `git tag v0.1.1 && git push origin v0.1.1`
2. Ve a **Actions** en GitHub
3. Verifica que el job `publish` se ejecute
4. Revisa los logs para confirmar publicación exitosa

## 📊 **Monitoreo**

### **Verificar publicación exitosa:**

```bash
# Verificar en PyPI
pip install hyblock-capital-sdk --no-cache-dir
python -c "import hyblock_capital_sdk; print('✅ SDK disponible en PyPI')"

# Verificar en TestPyPI
pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk --no-cache-dir
python -c "import hyblock_capital_sdk; print('✅ SDK disponible en TestPyPI')"
```

## 🚨 **Troubleshooting**

### **Error: "Invalid credentials"**
- Verifica que el token esté correctamente configurado en GitHub Secrets
- Asegúrate de que el token no haya expirado
- Verifica que el token tenga los permisos correctos

### **Error: "Version already exists"**
- Incrementa la versión en `pyproject.toml`
- Crea un nuevo tag con la nueva versión

### **Error: "Package not found"**
- Verifica que el nombre del paquete en `pyproject.toml` sea correcto
- Asegúrate de que el paquete esté construido correctamente

## 📚 **Referencias**

- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [PyPI API Tokens](https://pypi.org/help/#apitoken)
- [Poetry Publishing](https://python-poetry.org/docs/cli/#publish)
- [GitHub Actions](https://docs.github.com/en/actions)
