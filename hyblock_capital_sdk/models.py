"""
Modelos de datos para el SDK de Hyblock Capital.

Define las estructuras de datos utilizadas para representar la información
devuelta por la API de Hyblock Capital.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator, ConfigDict


class OrderStatus(str, Enum):
    """Estados posibles de una orden."""

    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class OrderType(str, Enum):
    """Tipos de órdenes disponibles."""

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TAKE_PROFIT = "take_profit"
    TAKE_PROFIT_LIMIT = "take_profit_limit"


class OrderSide(str, Enum):
    """Lado de la orden (compra o venta)."""

    BUY = "buy"
    SELL = "sell"


class PositionSide(str, Enum):
    """Lado de la posición (long o short)."""

    LONG = "long"
    SHORT = "short"


class TimeInForce(str, Enum):
    """Duración de la orden."""

    GTC = "gtc"  # Good Till Cancelled
    IOC = "ioc"  # Immediate Or Cancel
    FOK = "fok"  # Fill Or Kill
    GTD = "gtd"  # Good Till Date


class BaseHyblockModel(BaseModel):
    """Modelo base para todos los modelos del SDK."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
            Decimal: lambda d: str(d),
        },
    )


class Account(BaseHyblockModel):
    """
    Información de la cuenta del usuario.

    Attributes:
        id: Identificador único de la cuenta
        email: Email del usuario
        username: Nombre de usuario
        verification_level: Nivel de verificación (0-3)
        trading_enabled: Si el trading está habilitado
        margin_enabled: Si el trading con margen está habilitado
        futures_enabled: Si el trading de futuros está habilitado
        created_at: Fecha de creación de la cuenta
        updated_at: Fecha de última actualización
    """

    id: str
    email: str
    username: str
    verification_level: int = Field(ge=0, le=3)
    trading_enabled: bool = True
    margin_enabled: bool = False
    futures_enabled: bool = False
    created_at: datetime
    updated_at: datetime


class Balance(BaseHyblockModel):
    """
    Balance de un activo en la cuenta.

    Attributes:
        asset: Símbolo del activo (ej: BTC, ETH, USDT)
        free: Cantidad disponible para trading
        locked: Cantidad bloqueada en órdenes
        total: Cantidad total (free + locked)
        usd_value: Valor en USD del balance total
    """

    asset: str
    free: Decimal = Field(ge=0)
    locked: Decimal = Field(ge=0, default=Decimal("0"))
    total: Decimal = Field(ge=0)
    usd_value: Optional[Decimal] = Field(ge=0, default=None)

    @validator("total", always=True)
    def calculate_total(cls, v, values):
        """Calcula el total automáticamente si no se proporciona."""
        if v is None:
            return values.get("free", Decimal("0")) + values.get("locked", Decimal("0"))
        return v


class Order(BaseHyblockModel):
    """
    Información de una orden de trading.

    Attributes:
        id: Identificador único de la orden
        symbol: Par de trading (ej: BTC/USDT)
        side: Lado de la orden (buy/sell)
        type: Tipo de orden (market/limit/etc)
        amount: Cantidad a operar
        price: Precio de la orden (None para órdenes market)
        filled_amount: Cantidad ejecutada
        remaining_amount: Cantidad pendiente
        status: Estado actual de la orden
        time_in_force: Duración de la orden
        stop_price: Precio de stop (para órdenes stop)
        average_price: Precio promedio de ejecución
        fee: Comisión pagada
        fee_asset: Activo en que se pagó la comisión
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    id: str
    symbol: str
    side: OrderSide
    type: OrderType
    amount: Decimal = Field(gt=0)
    price: Optional[Decimal] = Field(gt=0, default=None)
    filled_amount: Decimal = Field(ge=0, default=Decimal("0"))
    remaining_amount: Decimal = Field(ge=0)
    status: OrderStatus
    time_in_force: TimeInForce = TimeInForce.GTC
    stop_price: Optional[Decimal] = Field(gt=0, default=None)
    average_price: Optional[Decimal] = Field(gt=0, default=None)
    fee: Optional[Decimal] = Field(ge=0, default=None)
    fee_asset: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @validator("remaining_amount", always=True)
    def calculate_remaining(cls, v, values):
        """Calcula la cantidad restante automáticamente."""
        if v is None:
            return values.get("amount", Decimal("0")) - values.get(
                "filled_amount", Decimal("0")
            )
        return v


class Position(BaseHyblockModel):
    """
    Información de una posición de trading.

    Attributes:
        id: Identificador único de la posición
        symbol: Par de trading
        side: Lado de la posición (long/short)
        size: Tamaño de la posición
        entry_price: Precio de entrada promedio
        mark_price: Precio de marca actual
        unrealized_pnl: PnL no realizado
        realized_pnl: PnL realizado
        margin: Margen utilizado
        leverage: Apalancamiento
        liquidation_price: Precio de liquidación
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    id: str
    symbol: str
    side: PositionSide
    size: Decimal = Field(ge=0)
    entry_price: Decimal = Field(gt=0)
    mark_price: Decimal = Field(gt=0)
    unrealized_pnl: Decimal = Field(default=Decimal("0"))
    realized_pnl: Decimal = Field(default=Decimal("0"))
    margin: Decimal = Field(ge=0)
    leverage: Decimal = Field(gt=0, le=100)
    liquidation_price: Optional[Decimal] = Field(gt=0, default=None)
    created_at: datetime
    updated_at: datetime


class Trade(BaseHyblockModel):
    """
    Información de una operación ejecutada.

    Attributes:
        id: Identificador único del trade
        order_id: ID de la orden que generó el trade
        symbol: Par de trading
        side: Lado del trade (buy/sell)
        amount: Cantidad operada
        price: Precio de ejecución
        fee: Comisión pagada
        fee_asset: Activo en que se pagó la comisión
        is_maker: Si fue una operación maker
        timestamp: Momento de ejecución
    """

    id: str
    order_id: str
    symbol: str
    side: OrderSide
    amount: Decimal = Field(gt=0)
    price: Decimal = Field(gt=0)
    fee: Decimal = Field(ge=0)
    fee_asset: str
    is_maker: bool
    timestamp: datetime


class Ticker(BaseHyblockModel):
    """
    Información de ticker de un símbolo.

    Attributes:
        symbol: Par de trading
        last_price: Último precio
        bid_price: Mejor precio de compra
        ask_price: Mejor precio de venta
        high_24h: Precio más alto en 24h
        low_24h: Precio más bajo en 24h
        volume_24h: Volumen en 24h
        price_change_24h: Cambio de precio en 24h
        price_change_percent_24h: Cambio porcentual en 24h
        timestamp: Momento de la información
    """

    symbol: str
    last_price: Decimal = Field(gt=0)
    bid_price: Decimal = Field(gt=0)
    ask_price: Decimal = Field(gt=0)
    high_24h: Decimal = Field(gt=0)
    low_24h: Decimal = Field(gt=0)
    volume_24h: Decimal = Field(ge=0)
    price_change_24h: Decimal
    price_change_percent_24h: Decimal
    timestamp: datetime


class OrderBookEntry(BaseHyblockModel):
    """Entrada en el libro de órdenes."""

    price: Decimal = Field(gt=0)
    amount: Decimal = Field(gt=0)


class OrderBook(BaseHyblockModel):
    """
    Libro de órdenes de un símbolo.

    Attributes:
        symbol: Par de trading
        bids: Lista de órdenes de compra (precio, cantidad)
        asks: Lista de órdenes de venta (precio, cantidad)
        timestamp: Momento de la información
    """

    symbol: str
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    timestamp: datetime


class Candle(BaseHyblockModel):
    """
    Vela de precio para análisis técnico.

    Attributes:
        symbol: Par de trading
        interval: Intervalo de tiempo (1m, 5m, 1h, etc)
        open_time: Tiempo de apertura
        close_time: Tiempo de cierre
        open_price: Precio de apertura
        high_price: Precio máximo
        low_price: Precio mínimo
        close_price: Precio de cierre
        volume: Volumen operado
        trades_count: Número de operaciones
    """

    symbol: str
    interval: str
    open_time: datetime
    close_time: datetime
    open_price: Decimal = Field(gt=0)
    high_price: Decimal = Field(gt=0)
    low_price: Decimal = Field(gt=0)
    close_price: Decimal = Field(gt=0)
    volume: Decimal = Field(ge=0)
    trades_count: int = Field(ge=0)


class MarketInfo(BaseHyblockModel):
    """
    Información de un mercado/símbolo.

    Attributes:
        symbol: Par de trading
        base_asset: Activo base
        quote_asset: Activo de cotización
        status: Estado del mercado (active/inactive)
        min_order_size: Tamaño mínimo de orden
        max_order_size: Tamaño máximo de orden
        price_precision: Precisión del precio
        amount_precision: Precisión de la cantidad
        maker_fee: Comisión maker
        taker_fee: Comisión taker
    """

    symbol: str
    base_asset: str
    quote_asset: str
    status: str
    min_order_size: Decimal = Field(gt=0)
    max_order_size: Decimal = Field(gt=0)
    price_precision: int = Field(ge=0)
    amount_precision: int = Field(ge=0)
    maker_fee: Decimal = Field(ge=0)
    taker_fee: Decimal = Field(ge=0)
