# Instalación

Esta página te guiará a través de la instalación del SDK de Hyblock Capital.

## Requisitos del Sistema

- **Python**: 3.8 o superior (recomendado 3.11.12)
- **Sistema operativo**: Windows, macOS, Linux
- **Gestor de dependencias**: pip o Poetry (recomendado)

## Opciones de Instalación

### Poetry (Recomendado)

Poetry es el gestor de dependencias recomendado para este proyecto.

=== "Desde PyPI"
    ```bash
    poetry add hyblock-capital-sdk
    ```

=== "Desde repositorio"
    ```bash
    poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git
    ```

=== "Para desarrollo"
    ```bash
    poetry add git+https://github.com/ljofreflor/hyblock-capital-sdk.git --editable
    ```

### pip

=== "Instalación básica"
    ```bash
    pip install hyblock-capital-sdk
    ```

=== "Con dependencias opcionales"
    ```bash
    pip install hyblock-capital-sdk[dev]
    ```

### Conda

```bash
conda install -c conda-forge hyblock-capital-sdk
```

## Instalación desde Fuentes

Si quieres instalar desde el código fuente:

```bash
# Clonar el repositorio
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk

# Instalar dependencias
poetry install --with dev

# O con pip
pip install -e .
```

## Configuración del Entorno

### Variables de Entorno

Configura las siguientes variables de entorno:

```bash
export HYBLOCK_API_KEY="tu_api_key_aqui"
export HYBLOCK_API_SECRET="tu_api_secret_aqui"
export HYBLOCK_API_URL="https://api1.dev.hyblockcapital.com/v1"
```

### Archivo .env

Crea un archivo `.env` en tu proyecto:

```env
HYBLOCK_API_KEY=tu_api_key_aqui
HYBLOCK_API_SECRET=tu_api_secret_aqui
HYBLOCK_API_URL=https://api1.dev.hyblockcapital.com/v1
```

### Verificar la Instalación

```python
import hyblock_capital_sdk as hc

# Verificar que la importación funciona
print(f"SDK versión: {hc.__version__}")

# Verificar configuración
config = hc.Configuration(host="https://api1.dev.hyblockcapital.com/v1")
print("✅ Configuración creada exitosamente")
```

## Solución de Problemas

### Error de importación

Si obtienes un error de importación:

```bash
# Verificar que Python puede encontrar el paquete
python -c "import hyblock_capital_sdk; print('OK')"
```

### Problemas con Poetry

Si Poetry no encuentra el paquete:

```bash
# Actualizar el índice de Poetry
poetry update

# Limpiar caché
poetry cache clear pypi --all
```

### Problemas con pip

Si pip no puede instalar el paquete:

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar con verbose para debug
pip install -v hyblock-capital-sdk
```

## Próximos Pasos

Una vez instalado:

1. **Configura tus credenciales** de API
2. **Lee el [Quick Start](quickstart.md)** para comenzar
3. **Explora los [ejemplos](examples/basic-usage.md)** disponibles
4. **Consulta la [referencia de APIs](api/client.md)** para funcionalidades avanzadas
