"""
Módulo de autenticación para el SDK de Hyblock Capital.

Maneja la autenticación y autorización de requests hacia la API,
incluyendo la generación de signatures y manejo de API keys.
"""

import hashlib
import hmac
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode


class HyblockAuth:
    """
    Manejador de autenticación para la API de Hyblock Capital.

    Implementa el mecanismo de autenticación requerido por la API,
    incluyendo la generación de signatures HMAC y headers de autenticación.
    """

    def __init__(self, api_key: str, api_secret: str):
        """
        Inicializa el manejador de autenticación.

        Args:
            api_key: Clave de API proporcionada por Hyblock Capital
            api_secret: Secreto de API proporcionado por Hyblock Capital
        """
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")

    def generate_signature(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
        timestamp: Optional[int] = None,
    ) -> str:
        """
        Genera la signature HMAC-SHA256 requerida para autenticar requests.

        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Path del endpoint de la API
            params: Parámetros de query string
            body: Cuerpo del request (para POST/PUT)
            timestamp: Timestamp Unix (se genera automáticamente si no se proporciona)

        Returns:
            Signature hexadecimal
        """
        if timestamp is None:
            timestamp = int(time.time() * 1000)

        # Construir query string si hay parámetros
        query_string = ""
        if params:
            query_string = urlencode(sorted(params.items()))

        # Construir el payload para firmar
        payload_parts = [str(timestamp), method.upper(), path, query_string, body or ""]

        payload = "|".join(payload_parts)

        # Generar signature HMAC-SHA256
        signature = hmac.new(
            self.api_secret, payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return signature

    def get_auth_headers(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Genera los headers de autenticación para un request.

        Args:
            method: Método HTTP
            path: Path del endpoint
            params: Parámetros de query
            body: Cuerpo del request

        Returns:
            Diccionario con los headers de autenticación
        """
        timestamp = int(time.time() * 1000)
        signature = self.generate_signature(method, path, params, body, timestamp)

        return {
            "X-HBC-API-KEY": self.api_key,
            "X-HBC-TIMESTAMP": str(timestamp),
            "X-HBC-SIGNATURE": signature,
            "Content-Type": "application/json",
        }

    def validate_api_credentials(self) -> bool:
        """
        Valida que las credenciales de API estén en el formato correcto.

        Returns:
            True si las credenciales parecen válidas, False en caso contrario
        """
        if not self.api_key or not self.api_secret:
            return False

        # Verificar formato básico de API key (ejemplo: debe tener cierta longitud)
        if len(self.api_key) < 20 or len(self.api_secret) < 20:
            return False

        # Verificar que no contengan caracteres inválidos
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        if not all(c in allowed_chars for c in self.api_key):
            return False

        if not all(c in allowed_chars for c in self.api_secret.decode("utf-8")):
            return False

        return True
