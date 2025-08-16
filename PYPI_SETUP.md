# 🚀 Guía de Configuración para PyPI

Esta guía te ayudará a configurar la autenticación y subir el SDK de Hyblock Capital a PyPI.

## 📋 Requisitos Previos

### 1. Crear Cuentas
- **PyPI Test**: https://test.pypi.org/account/register/
- **PyPI Oficial**: https://pypi.org/account/register/

### 2. Verificar Email
- Confirma tu email en ambas plataformas

### 3. Habilitar 2FA (Recomendado)
- Configura autenticación de dos factores para mayor seguridad

## 🔑 Configuración de Tokens de API

### Paso 1: Crear Tokens

#### Para PyPI Test:
1. Ve a https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Nombre: `hyblock-capital-sdk-test`
4. Scope: `Entire account` (para el primer upload)
5. Copia el token (comienza con `pypi-`)

#### Para PyPI Oficial:
1. Ve a https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Nombre: `hyblock-capital-sdk`
4. Scope: `Entire account` (para el primer upload)
5. Copia el token (comienza con `pypi-`)

### Paso 2: Configurar Autenticación

#### Opción A: Archivo `.pypirc` (Recomendado)

Crea el archivo `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-TU_TOKEN_OFICIAL_AQUI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-TU_TOKEN_TEST_AQUI
```

#### Opción B: Variables de Entorno

```bash
# Para PyPI Test
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-TU_TOKEN_TEST_AQUI
export TWINE_REPOSITORY=testpypi

# Para PyPI Oficial
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-TU_TOKEN_OFICIAL_AQUI
```

## 🔄 Proceso de Publicación

### 1. Preparación
```bash
# Verificar todo está correcto
make check
make test

# Limpiar distribuciones anteriores
make clean-dist
```

### 2. Construir Distribución
```bash
# Construir el paquete
make build-dist

# Verificar la distribución
make check-dist
```

### 3. Subir a PyPI Test (SIEMPRE PRIMERO)
```bash
# Subir a entorno de pruebas
make upload-test
```

### 4. Probar Instalación desde Test
```bash
# En un entorno limpio/diferente:
pip install --index-url https://test.pypi.org/simple/ hyblock-capital-sdk

# Probar importación
python -c "import hyblock_capital_sdk; print('OK')"
```

### 5. Subir a PyPI Oficial
```bash
# Solo después de probar en test
make upload-pypi
```

## 📦 Verificación Post-Publicación

### Verificar en PyPI
- PyPI Test: https://test.pypi.org/project/hyblock-capital-sdk/
- PyPI Oficial: https://pypi.org/project/hyblock-capital-sdk/

### Probar Instalación
```bash
# Instalación normal
pip install hyblock-capital-sdk

# Verificar funcionamiento
python -c "
import hyblock_capital_sdk as hc
config = hc.Configuration(host='https://api1.dev.hyblockcapital.com/v1')
print('SDK instalado correctamente!')
print(f'Versión: {hc.__version__}')
"
```

## 🔧 Comandos Útiles

```bash
# Mostrar ayuda de PyPI
make pypi-help

# Ver estado de la distribución
ls -la dist/

# Verificar metadatos del paquete
poetry run python -m twine check dist/*

# Ver información del paquete instalado
pip show hyblock-capital-sdk

# Desinstalar para testing
pip uninstall hyblock-capital-sdk
```

## 🚨 Solución de Problemas

### Error: "Repository does not allow updating..."
- **Causa**: Intentando subir la misma versión dos veces
- **Solución**: Incrementar versión en `pyproject.toml`

### Error: "Invalid or non-existent authentication"
- **Causa**: Token incorrecto o malformado
- **Solución**: Verificar token en `.pypirc` o variables de entorno

### Error: "Package name too similar to existing package"
- **Causa**: Nombre muy similar a otro paquete
- **Solución**: Cambiar nombre en `pyproject.toml`

### Error: "File already exists"
- **Causa**: Archivo ya existe en PyPI
- **Solución**: Incrementar versión o usar `--skip-existing`

## 📈 Versionado

### Esquema de Versiones
- `0.1.0` - Primera release
- `0.1.1` - Bug fixes
- `0.2.0` - Nuevas features
- `1.0.0` - Release estable

### Actualizar Versión
```bash
# Editar pyproject.toml
version = "0.1.1"

# O usar poetry
poetry version patch    # 0.1.0 -> 0.1.1
poetry version minor    # 0.1.0 -> 0.2.0
poetry version major    # 0.1.0 -> 1.0.0
```

## 🎯 Checklist de Publicación

- [ ] ✅ Cuentas creadas en PyPI y PyPI Test
- [ ] ✅ Tokens de API configurados
- [ ] ✅ Archivo `.pypirc` configurado
- [ ] ✅ `make check` pasa sin errores
- [ ] ✅ `make test` pasa todos los tests
- [ ] ✅ `make build-dist` construye correctamente
- [ ] ✅ `make check-dist` verifica OK
- [ ] ✅ `make upload-test` sube a test PyPI
- [ ] ✅ Instalación desde test PyPI funciona
- [ ] ✅ SDK importa y funciona correctamente
- [ ] ✅ `make upload-pypi` sube a PyPI oficial
- [ ] ✅ Verificación final en PyPI oficial

## 🔗 Enlaces Útiles

- **PyPI**: https://pypi.org/
- **PyPI Test**: https://test.pypi.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **Poetry Docs**: https://python-poetry.org/docs/
- **Python Packaging Guide**: https://packaging.python.org/

## 💡 Mejores Prácticas

1. **Siempre usar PyPI Test primero**
2. **Incrementar versión para cada release**
3. **Usar tokens de API, no contraseñas**
4. **Verificar metadatos antes de subir**
5. **Probar instalación en entorno limpio**
6. **Mantener tokens seguros y privados**
7. **Usar scope específico para tokens cuando sea posible**

---

¡Con esta configuración, el SDK estará listo para que los clientes lo instalen fácilmente con `pip install hyblock-capital-sdk`! 🎉
