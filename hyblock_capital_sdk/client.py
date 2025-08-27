"""
Cliente principal del SDK de Hyblock Capital.

Proporciona la interfaz principal para interactuar con la API de Hyblock Capital,
incluyendo métodos para trading, consulta de datos de mercado y gestión de cuenta.
"""

import json
import time
from decimal import Decimal
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import HyblockAuth
from .exceptions import (
    HyblockAPIError,
    HyblockAuthenticationError,
    HyblockConnectionError,
    HyblockRateLimitError,
    HyblockValidationError,
    HyblockInsufficientFundsError,
    HyblockOrderError,
    HyblockMarketDataError,
)
from .models import (
    Account,
    Balance,
    Order,
    Position,
    Trade,
    Ticker,
    OrderBook,
    Candle,
    MarketInfo,
    OrderSide,
    OrderType,
    TimeInForce,
)


class HyblockClient:
    """
    Cliente principal para la API de Hyblock Capital.

    Proporciona métodos para realizar operaciones de trading, consultar datos
    de mercado y gestionar la cuenta del usuario.

    Example:
        client = HyblockClient(
            api_key="tu_api_key",
            api_secret="tu_api_secret"
        )

        # Obtener balance
        balances = client.get_balances()

        # Crear orden
        order = client.create_order(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            amount=Decimal("0.001"),
            price=Decimal("45000")
        )
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.hyblock.capital",
        timeout: int = 30,
        max_retries: int = 3,
        testnet: bool = False,
    ):
        """
        Inicializa el cliente de Hyblock Capital.

        Args:
            api_key: Clave de API
            api_secret: Secreto de API
            base_url: URL base de la API
            timeout: Timeout para requests en segundos
            max_retries: Número máximo de reintentos
            testnet: Si usar la red de pruebas
        """
        self.auth = HyblockAuth(api_key, api_secret)

        if testnet:
            self.base_url = "https://testnet-api.hyblock.capital"
        else:
            self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        # Configurar sesión HTTP con reintentos
        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Validar credenciales
        if not self.auth.validate_api_credentials():
            raise HyblockAuthenticationError("Credenciales de API inválidas")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> Dict[str, Any]:
        """
        Realiza un request HTTP a la API.

        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint de la API (sin base URL)
            params: Parámetros de query string
            data: Datos del cuerpo del request
            auth_required: Si se requiere autenticación

        Returns:
            Respuesta JSON de la API

        Raises:
            HyblockAPIError: Error general de la API
            HyblockAuthenticationError: Error de autenticación
            HyblockConnectionError: Error de conexión
            HyblockRateLimitError: Límite de velocidad excedido
        """
        url = f"{self.base_url}{endpoint}"
        headers = {}
        body = None

        if data:
            body = json.dumps(data, default=str)

        if auth_required:
            headers.update(self.auth.get_auth_headers(method, endpoint, params, body))
        else:
            headers["Content-Type"] = "application/json"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=body,
                timeout=self.timeout,
            )

            # Verificar rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise HyblockRateLimitError(
                    "Límite de velocidad excedido",
                    retry_after=retry_after,
                    status_code=response.status_code,
                )

            # Verificar errores de autenticación
            if response.status_code == 401:
                raise HyblockAuthenticationError(
                    "Credenciales de API inválidas o expiradas",
                    status_code=response.status_code,
                )

            # Verificar errores de validación
            if response.status_code == 400:
                error_data = response.json() if response.content else {}
                raise HyblockValidationError(
                    error_data.get("message", "Error de validación"),
                    status_code=response.status_code,
                    details=error_data,
                )

            # Verificar otros errores HTTP
            if not response.ok:
                error_data = response.json() if response.content else {}
                error_message = error_data.get(
                    "message", f"Error HTTP {response.status_code}"
                )

                raise HyblockAPIError(
                    error_message,
                    status_code=response.status_code,
                    error_code=error_data.get("code"),
                    details=error_data,
                )

            return response.json()

        except requests.exceptions.Timeout:
            raise HyblockConnectionError(f"Timeout después de {self.timeout} segundos")

        except requests.exceptions.ConnectionError as e:
            raise HyblockConnectionError(f"Error de conexión: {str(e)}")

        except requests.exceptions.RequestException as e:
            raise HyblockConnectionError(f"Error de request: {str(e)}")

    # Métodos de Account Management

    def get_account(self) -> Account:
        """
        Obtiene información de la cuenta del usuario.

        Returns:
            Información de la cuenta
        """
        data = self._make_request("GET", "/api/v1/account")
        return Account(**data)

    def get_balances(self) -> List[Balance]:
        """
        Obtiene todos los balances de la cuenta.

        Returns:
            Lista de balances por activo
        """
        data = self._make_request("GET", "/api/v1/account/balances")
        return [Balance(**item) for item in data]

    def get_balance(self, asset: str) -> Optional[Balance]:
        """
        Obtiene el balance de un activo específico.

        Args:
            asset: Símbolo del activo (ej: BTC, ETH, USDT)

        Returns:
            Balance del activo o None si no se encuentra
        """
        balances = self.get_balances()
        for balance in balances:
            if balance.asset.upper() == asset.upper():
                return balance
        return None

    # Métodos de Trading

    def create_order(
        self,
        symbol: str,
        side: OrderSide,
        type: OrderType,
        amount: Union[Decimal, float, str],
        price: Optional[Union[Decimal, float, str]] = None,
        stop_price: Optional[Union[Decimal, float, str]] = None,
        time_in_force: TimeInForce = TimeInForce.GTC,
        client_order_id: Optional[str] = None,
    ) -> Order:
        """
        Crea una nueva orden de trading.

        Args:
            symbol: Par de trading (ej: BTC/USDT)
            side: Lado de la orden (buy/sell)
            type: Tipo de orden
            amount: Cantidad a operar
            price: Precio (requerido para órdenes limit)
            stop_price: Precio de stop (para órdenes stop)
            time_in_force: Duración de la orden
            client_order_id: ID personalizado para la orden

        Returns:
            Información de la orden creada

        Raises:
            HyblockOrderError: Error específico de la orden
            HyblockInsufficientFundsError: Fondos insuficientes
        """
        data = {
            "symbol": symbol,
            "side": side.value,
            "type": type.value,
            "amount": str(amount),
            "timeInForce": time_in_force.value,
        }

        if price is not None:
            data["price"] = str(price)

        if stop_price is not None:
            data["stopPrice"] = str(stop_price)

        if client_order_id:
            data["clientOrderId"] = client_order_id

        try:
            response = self._make_request("POST", "/api/v1/orders", data=data)
            return Order(**response)

        except HyblockAPIError as e:
            if e.error_code == "INSUFFICIENT_FUNDS":
                raise HyblockInsufficientFundsError(
                    "Fondos insuficientes para crear la orden", details=e.details
                )
            elif "order" in str(e).lower():
                raise HyblockOrderError(str(e), details=e.details)
            else:
                raise

    def get_orders(
        self,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Order]:
        """
        Obtiene las órdenes del usuario.

        Args:
            symbol: Filtrar por símbolo específico
            status: Filtrar por estado específico
            limit: Número máximo de órdenes a retornar

        Returns:
            Lista de órdenes
        """
        params = {"limit": limit}

        if symbol:
            params["symbol"] = symbol

        if status:
            params["status"] = status

        data = self._make_request("GET", "/api/v1/orders", params=params)
        return [Order(**item) for item in data]

    def get_order(self, order_id: str) -> Order:
        """
        Obtiene información de una orden específica.

        Args:
            order_id: ID de la orden

        Returns:
            Información de la orden
        """
        data = self._make_request("GET", f"/api/v1/orders/{order_id}")
        return Order(**data)

    def cancel_order(self, order_id: str) -> Order:
        """
        Cancela una orden específica.

        Args:
            order_id: ID de la orden a cancelar

        Returns:
            Información de la orden cancelada
        """
        data = self._make_request("DELETE", f"/api/v1/orders/{order_id}")
        return Order(**data)

    def cancel_all_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """
        Cancela todas las órdenes abiertas.

        Args:
            symbol: Cancelar solo órdenes de un símbolo específico

        Returns:
            Lista de órdenes canceladas
        """
        params = {}
        if symbol:
            params["symbol"] = symbol

        data = self._make_request("DELETE", "/api/v1/orders", params=params)
        return [Order(**item) for item in data]

    def get_trades(
        self,
        symbol: Optional[str] = None,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[Trade]:
        """
        Obtiene el historial de trades del usuario.

        Args:
            symbol: Filtrar por símbolo específico
            limit: Número máximo de trades a retornar
            start_time: Fecha de inicio
            end_time: Fecha de fin

        Returns:
            Lista de trades
        """
        params = {"limit": limit}

        if symbol:
            params["symbol"] = symbol

        if start_time:
            params["startTime"] = int(start_time.timestamp() * 1000)

        if end_time:
            params["endTime"] = int(end_time.timestamp() * 1000)

        data = self._make_request("GET", "/api/v1/trades", params=params)
        return [Trade(**item) for item in data]

    # Métodos de Market Data

    def get_ticker(self, symbol: str) -> Ticker:
        """
        Obtiene información de ticker para un símbolo.

        Args:
            symbol: Par de trading

        Returns:
            Información del ticker
        """
        try:
            data = self._make_request(
                "GET", f"/api/v1/ticker/{symbol}", auth_required=False
            )
            return Ticker(**data)
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e), symbol=symbol)

    def get_tickers(self) -> List[Ticker]:
        """
        Obtiene información de ticker para todos los símbolos.

        Returns:
            Lista de tickers
        """
        try:
            data = self._make_request("GET", "/api/v1/ticker", auth_required=False)
            return [Ticker(**item) for item in data]
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e))

    def get_orderbook(self, symbol: str, limit: int = 100) -> OrderBook:
        """
        Obtiene el libro de órdenes para un símbolo.

        Args:
            symbol: Par de trading
            limit: Número de niveles a retornar

        Returns:
            Libro de órdenes
        """
        try:
            params = {"limit": limit}
            data = self._make_request(
                "GET", f"/api/v1/orderbook/{symbol}", params=params, auth_required=False
            )
            return OrderBook(**data)
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e), symbol=symbol)

    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[Candle]:
        """
        Obtiene velas de precio para análisis técnico.

        Args:
            symbol: Par de trading
            interval: Intervalo de tiempo (1m, 5m, 1h, 1d, etc.)
            limit: Número máximo de velas
            start_time: Fecha de inicio
            end_time: Fecha de fin

        Returns:
            Lista de velas
        """
        try:
            params = {"interval": interval, "limit": limit}

            if start_time:
                params["startTime"] = int(start_time.timestamp() * 1000)

            if end_time:
                params["endTime"] = int(end_time.timestamp() * 1000)

            data = self._make_request(
                "GET", f"/api/v1/candles/{symbol}", params=params, auth_required=False
            )
            return [Candle(**item) for item in data]
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e), symbol=symbol)

    def get_markets(self) -> List[MarketInfo]:
        """
        Obtiene información de todos los mercados disponibles.

        Returns:
            Lista de información de mercados
        """
        try:
            data = self._make_request("GET", "/api/v1/markets", auth_required=False)
            return [MarketInfo(**item) for item in data]
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e))

    def get_market(self, symbol: str) -> MarketInfo:
        """
        Obtiene información de un mercado específico.

        Args:
            symbol: Par de trading

        Returns:
            Información del mercado
        """
        try:
            data = self._make_request(
                "GET", f"/api/v1/markets/{symbol}", auth_required=False
            )
            return MarketInfo(**data)
        except HyblockAPIError as e:
            raise HyblockMarketDataError(str(e), symbol=symbol)

    # Métodos de utilidad

    def ping(self) -> bool:
        """
        Verifica la conectividad con la API.

        Returns:
            True si la API responde correctamente
        """
        try:
            self._make_request("GET", "/api/v1/ping", auth_required=False)
            return True
        except HyblockAPIError:
            return False

    def get_server_time(self) -> datetime:
        """
        Obtiene la hora del servidor.

        Returns:
            Hora del servidor
        """
        data = self._make_request("GET", "/api/v1/time", auth_required=False)
        return datetime.fromtimestamp(data["serverTime"] / 1000)
