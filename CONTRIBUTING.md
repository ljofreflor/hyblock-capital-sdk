# Contribuyendo al Hyblock Capital SDK

¡Gracias por tu interés en contribuir al SDK oficial de Hyblock Capital! 🎉

## 🚀 Proceso de Contribución

### 1. Fork y Clone
```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/ljofreflor/hyblock-capital-sdk.git
cd hyblock-capital-sdk
```

### 2. Configurar Entorno de Desarrollo
```bash
# Instalar Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell
```

### 3. Desarrollo

#### Para cambios en la API:
```bash
# Regenerar SDK desde Swagger
./generate_sdk.sh

# Verificar cambios
make check
make test
```

#### Para cambios en tests o documentación:
```bash
# Formatear código
make format

# Ejecutar tests
make test

# Verificar cobertura
make coverage
```

### 4. Testing

#### Tests Obligatorios:
```bash
# Todos los tests deben pasar
make test

# Verificar calidad del código
make check

# Tests específicos de liquidación
poetry run pytest tests/test_liquidation_*.py -v
```

#### Crear Nuevos Tests:
- Seguir el patrón en `tests/test_liquidation_pools.py`
- Usar mocks para APIs externas
- Incluir docstrings explicativos
- Cubrir casos de éxito y error

### 5. Commit y Pull Request

#### Convención de Commits:
```bash
# Tipos permitidos:
feat: nueva funcionalidad
fix: corrección de bug  
docs: cambios en documentación
test: añadir o modificar tests
refactor: refactorización de código
chore: cambios en build/configuración

# Ejemplos:
git commit -m "feat: añadir soporte para nuevos endpoints de liquidación"
git commit -m "fix: corregir error en parsing de datos de apalancamiento"
git commit -m "docs: actualizar ejemplos de uso en README"
```

#### Pull Request:
1. Hacer push de tu branch
2. Crear Pull Request desde tu fork
3. Incluir descripción detallada
4. Referenciar issues relacionados

## 📋 Estándares de Código

### Python Code Style:
- **Black** para formateo automático
- **flake8** para linting
- **isort** para imports
- **mypy** para type checking

```bash
# Verificar todo automáticamente
make check
```

### Estructura de Tests:
```python
def test_funcionalidad_especifica():
    """
    Objetivo: Verificar que X funcionalidad Y comportamiento esperado.
    
    Casos cubiertos:
    - Entrada válida con resultado esperado
    - Entrada inválida con excepción esperada
    - Casos límite o edge cases
    """
    # Arrange
    mock_data = {...}
    
    # Act
    result = funcion_a_probar(mock_data)
    
    # Assert
    assert result.campo == valor_esperado
    mock_api.assert_called_with(parametros_esperados)
```

## 🔄 Flujo de Desarrollo

### Para Contribuidores Externos:
1. **Fork** del repositorio
2. **Branch** para tu feature: `git checkout -b feature/mi-funcionalidad`
3. **Desarrollo** con tests incluidos
4. **Pull Request** con descripción detallada

### Para Mantenedores:
1. **Review** de PRs
2. **Merge** después de aprobación
3. **Release** automático via GitHub Actions
4. **Publicación** en PyPI

## 🐛 Reportar Bugs

### Información Requerida:
- Versión del SDK
- Versión de Python
- Sistema operativo
- Código que reproduce el problema
- Error completo (traceback)

### Template de Bug Report:
Usa el template automático en GitHub Issues o incluye:

```python
# Código que reproduce el problema
import hyblock_capital_sdk as hc

config = hc.Configuration(...)
# ... resto del código
```

## 💡 Sugerir Funcionalidades

### Antes de Proponer:
1. Verificar que no existe ya un issue similar
2. Confirmar que está alineado con los objetivos del proyecto
3. Proporcionar casos de uso específicos

### Información Útil:
- Descripción del problema que resuelve
- Ejemplo de uso propuesto
- Implementaciones alternativas consideradas

## 📚 Documentación

### Actualizar Documentación:
- **README.md**: Información general y ejemplos básicos
- **QUICKSTART.md**: Guía de inicio rápido
- **examples/**: Ejemplos específicos de uso
- **Docstrings**: Documentación en el código

### Generar Documentación:
```bash
# TODO: Añadir generación automática de docs
# make docs
```

## 🚀 Release Process

### Para Mantenedores:

#### 1. Preparar Release:
```bash
# Actualizar versión
poetry version patch  # o minor/major

# Regenerar SDK si hay cambios en API
./generate_sdk.sh

# Verificar todo
make check
make test
```

#### 2. Crear Release:
```bash
# Tag del release
git tag v$(poetry version -s)
git push origin v$(poetry version -s)

# GitHub Actions se encarga del resto
```

#### 3. Publicar en PyPI:
```bash
# Automático via GitHub Actions
# O manual:
make upload-pypi
```

## ❓ Preguntas

### Dónde Pedir Ayuda:
- **GitHub Issues**: Para bugs y features
- **GitHub Discussions**: Para preguntas generales
- **Email**: ljofre2146@gmail.com para consultas privadas

### FAQ:

**Q: ¿Puedo contribuir sin conocimiento profundo de trading?**
A: ¡Sí! Contribuciones en documentación, tests, y mejoras generales son muy bienvenidas.

**Q: ¿El SDK se regenera automáticamente?**
A: Sí, el SDK se regenera desde el Swagger de Hyblock Capital, pero mejoras en configuración y tests son contribuciones valiosas.

**Q: ¿Qué pasa si rompo algo?**
A: Los tests y CI/CD están para detectar problemas. ¡No te preocupes y experimenta!

## 🎯 Roadmap

### Próximas Funcionalidades:
- [ ] Documentación automática con Sphinx
- [ ] Support para WebSockets
- [ ] CLI tool para operaciones comunes
- [ ] Más ejemplos de trading strategies

### Mejoras Técnicas:
- [ ] Async/await support
- [ ] Rate limiting automático
- [ ] Mejor manejo de errores
- [ ] Logging estructurado

---

¡Gracias por contribuir al ecosistema de Hyblock Capital! 🚀
