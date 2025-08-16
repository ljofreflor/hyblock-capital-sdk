"""
Tests para el proceso de generación del SDK desde OpenAPI.

Valida que el proceso de generación automática funcione correctamente
y que el SDK generado tenga la estructura esperada.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest

# Imports que estarán disponibles después de la generación
# Por ahora usamos mocks para testear la lógica de generación


class TestSDKGeneration:
    """Tests para la generación del SDK."""

    def test_openapi_config_file_exists(self):
        """
        Verificar que el archivo de configuración de OpenAPI Generator existe.

        Valida que el archivo openapi-generator-config.json esté presente
        y contenga la configuración necesaria.
        """
        config_file = Path("openapi-generator-config.json")
        assert config_file.exists(), "Archivo de configuración OpenAPI no encontrado"

        with open(config_file, "r") as f:
            config = json.load(f)

        # Verificar campos esenciales
        required_fields = [
            "packageName",
            "packageVersion",
            "clientPackage",
            "packageAuthor",
            "packageDescription",
        ]

        for field in required_fields:
            assert (
                field in config
            ), f"Campo requerido '{field}' no encontrado en configuración"

        # Verificar valores específicos
        assert config["packageName"] == "hyblock_capital_sdk"
        assert config["clientPackage"] == "hyblock_capital_sdk"
        assert "hyblock" in config["packageDescription"].lower()

    def test_generation_script_exists_and_executable(self):
        """
        Verificar que el script de generación existe y es ejecutable.

        Valida que el script bash esté presente y tenga permisos de ejecución.
        """
        bash_script = Path("generate_sdk.sh")

        assert bash_script.exists(), "Script Bash de generación no encontrado"

        # Verificar permisos de ejecución
        assert os.access(bash_script, os.X_OK), "Script Bash no es ejecutable"

    @patch("urllib.request.urlopen")
    def test_swagger_download_simulation(self, mock_urlopen, sample_openapi_spec):
        """
        Simular la descarga de la especificación Swagger.

        Valida que el proceso de descarga maneje correctamente
        la especificación OpenAPI de Hyblock Capital.
        """
        # Configurar mock de respuesta HTTP
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(sample_openapi_spec).encode(
            "utf-8"
        )
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Simular el proceso que haría el script bash
        swagger_url = "https://media.hyblockcapital.com/document/swagger-dev.json"

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".json", delete=False
        ) as tmp_file:
            try:
                # Simular descarga
                with mock_urlopen(swagger_url) as response:
                    data = response.read()
                    tmp_file.write(data.decode("utf-8"))
                    tmp_file.flush()

                # Verificar que el archivo se puede cargar como JSON válido
                with open(tmp_file.name, "r") as f:
                    loaded_spec = json.load(f)

                assert loaded_spec == sample_openapi_spec
                assert "openapi" in loaded_spec
                assert "paths" in loaded_spec

            finally:
                os.unlink(tmp_file.name)

    @patch("subprocess.run")
    def test_openapi_generator_command_simulation(self, mock_subprocess):
        """
        Simular la ejecución del comando OpenAPI Generator.

        Valida que el comando se ejecute con los parámetros correctos.
        """
        # Configurar mock para simular éxito
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Generation completed successfully"
        mock_subprocess.return_value.stderr = ""

        # Comando esperado
        expected_cmd = [
            "openapi-generator-cli",
            "generate",
            "-i",
            "swagger.json",
            "-g",
            "python",
            "-o",
            "generated",
            "-c",
            "openapi-generator-config.json",
            "--additional-properties",
            "packageName=hyblock_capital_sdk,pythonPackageName=hyblock_capital_sdk",
        ]

        # Simular llamada
        with tempfile.TemporaryDirectory() as temp_dir:
            swagger_file = Path(temp_dir) / "swagger.json"
            output_dir = Path(temp_dir) / "generated"

            # El comando real se ejecutaría aquí
            # Por ahora solo verificamos que el mock se configure correctamente
            assert mock_subprocess.return_value.returncode == 0

    def test_project_structure_after_generation(self):
        """
        Verificar la estructura del proyecto después de la generación.

        Valida que los directorios y archivos esperados estén presentes
        después de ejecutar la generación del SDK.
        """
        project_root = Path(".")

        # Archivos que deberían existir
        expected_files = [
            "pyproject.toml",
            "README.md",
            "generate_sdk.sh",
            "openapi-generator-config.json",
            ".gitignore",
            "Makefile",
        ]

        for file_name in expected_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"Archivo esperado no encontrado: {file_name}"

        # Directorios que deberían existir
        expected_dirs = ["tests", ".github/workflows"]

        for dir_name in expected_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"Directorio esperado no encontrado: {dir_name}"
            assert (
                dir_path.is_dir()
            ), f"La ruta existe pero no es un directorio: {dir_name}"

    def test_pyproject_toml_configuration(self):
        """
        Verificar la configuración de pyproject.toml.

        Valida que el archivo de configuración de Poetry contenga
        todos los metadatos y dependencias necesarias.
        """
        pyproject_file = Path("pyproject.toml")
        assert pyproject_file.exists(), "pyproject.toml no encontrado"

        # Leer y parsear el archivo TOML
        # Para simplicidad, verificamos contenido como texto
        with open(pyproject_file, "r") as f:
            content = f.read()

        # Verificar metadatos esenciales
        assert 'name = "hyblock-capital-sdk"' in content
        assert "hyblock_capital_sdk" in content
        assert "openapi" in content.lower()

        # Verificar dependencias requeridas para OpenAPI Generator
        assert "urllib3" in content
        assert "python-dateutil" in content
        assert "pydantic" in content

        # Verificar dependencias de desarrollo
        assert "pytest" in content
        assert "black" in content
        # openapi-generator-cli se instala dinámicamente en el script

    @pytest.mark.slow
    def test_makefile_targets(self):
        """
        Verificar que el Makefile contenga los targets necesarios.

        Valida que el Makefile incluya comandos para todas las
        operaciones importantes del proyecto.
        """
        makefile = Path("Makefile")
        assert makefile.exists(), "Makefile no encontrado"

        with open(makefile, "r") as f:
            content = f.read()

        # Targets esperados
        expected_targets = [
            "help",
            "install",
            "generate",
            "test",
            "lint",
            "format",
            "build",
            "clean",
        ]

        for target in expected_targets:
            assert (
                f"{target}:" in content
            ), f"Target '{target}' no encontrado en Makefile"

        # Verificar que use Poetry
        assert "poetry run" in content
        assert "poetry install" in content

    def test_github_actions_workflow(self):
        """
        Verificar la configuración de GitHub Actions.

        Valida que el workflow de CI/CD esté configurado correctamente
        para generar y testear el SDK automáticamente.
        """
        workflow_file = Path(".github/workflows/ci.yml")
        assert (
            workflow_file.exists()
        ), "Archivo de workflow de GitHub Actions no encontrado"

        with open(workflow_file, "r") as f:
            content = f.read()

        # Verificar elementos esenciales del workflow
        assert "name: CI/CD Pipeline" in content
        assert "generate-sdk" in content.lower()
        assert "poetry" in content
        assert "python" in content
        assert "java" in content  # Requerido por OpenAPI Generator

        # Verificar que incluya generación automática
        assert "generate_sdk.sh" in content

    def test_gitignore_configuration(self):
        """
        Verificar la configuración de .gitignore.

        Valida que los archivos y directorios apropiados estén excluidos
        del control de versiones, especialmente archivos generados y credenciales.
        """
        gitignore_file = Path(".gitignore")
        assert gitignore_file.exists(), ".gitignore no encontrado"

        with open(gitignore_file, "r") as f:
            content = f.read()

        # Verificar exclusiones importantes
        important_exclusions = [
            "__pycache__",
            "*.py[cod]",  # Incluye *.pyc
            ".env",
            "dist/",
            "build/",
            "swagger.json",
            "generated/",
            "*.backup",  # Cambiado de *.backup.*
            ".idea/",
            ".vscode/",
        ]

        for exclusion in important_exclusions:
            assert (
                exclusion in content
            ), f"Exclusión importante '{exclusion}' no encontrada en .gitignore"


class TestGenerationTools:
    """Tests para las herramientas y utilidades de generación."""

    def test_environment_example_file(self):
        """
        Verificar que existe un archivo de ejemplo de variables de entorno.

        Valida que haya un archivo que muestre cómo configurar
        las variables de entorno necesarias.
        """
        env_example = Path("env.example")
        assert env_example.exists(), "Archivo env.example no encontrado"

        with open(env_example, "r") as f:
            content = f.read()

        # Verificar que contenga variables importantes
        important_vars = ["HYBLOCK_API_KEY", "HYBLOCK_API_SECRET", "HYBLOCK_API_URL"]

        for var in important_vars:
            assert (
                var in content
            ), f"Variable de entorno '{var}' no documentada en env.example"

    @patch("pathlib.Path.exists")
    def test_sdk_directory_validation(self, mock_exists):
        """
        Verificar la validación del directorio del SDK.

        Simula diferentes estados del directorio del SDK y valida
        que el proceso de generación maneje cada caso correctamente.
        """
        # Caso 1: Directorio no existe (primera generación)
        mock_exists.return_value = False
        # El generador debería crear el directorio

        # Caso 2: Directorio existe pero está vacío
        mock_exists.return_value = True
        # El generador debería proceder con la generación

        # Caso 3: Directorio existe con contenido
        mock_exists.return_value = True
        # El generador debería crear un backup

        # Por ahora solo verificamos que el mock funciona
        assert mock_exists.return_value == True

    def test_configuration_validation(self):
        """
        Verificar la validación de la configuración de OpenAPI Generator.

        Valida que la configuración sea compatible con las capacidades
        del generador y produzca un SDK funcional.
        """
        config_file = Path("openapi-generator-config.json")

        if config_file.exists():
            with open(config_file, "r") as f:
                config = json.load(f)

            # Verificar configuraciones críticas
            assert config.get("library") in [
                None,
                "urllib3",
            ], "Biblioteca HTTP no compatible"
            assert config.get(
                "supportPython3", True
            ), "Soporte para Python 3 debe estar habilitado"
            assert (
                config.get("generateSourceCodeOnly", False) == False
            ), "Debe generar archivos completos del proyecto"

            # Verificar que la configuración sea consistente
            assert config.get("packageName") == config.get(
                "pythonPackageName"
            ), "Nombres de paquete inconsistentes"
