"""Core order and trade types.

Prices are ALWAYS integer ticks, never floats. Converting to and from human-readable
prices (e.g. dollars) is the caller's responsibility and must happen outside the engine.
Timestamps are monotonic sequence numbers assigned by the caller, never wall-clock times.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


class Side(Enum):
    """Side of an order."""

    BUY = auto()
    SELL = auto()


class OrderType(Enum):
    """Order type. Only LIMIT is used in Phase 1."""

    LIMIT = auto()
    # Phase 2: the order types below are not supported until Phase 2.
    MARKET = auto()
    IOC = auto()
    FOK = auto()
    STOP = auto()
    STOP_LIMIT = auto()
    ICEBERG = auto()


@dataclass(slots=True)
class Order:
    """An order submitted to the book.

    Attributes:
        order_id: Unique identifier for the order.
        side: BUY or SELL.
        price: Limit price in integer ticks; None for market orders.
        quantity: Original quantity.
        timestamp: Monotonic sequence number (not wall-clock) used for time priority.
        order_type: Order type; defaults to LIMIT.
        remaining: Unfilled quantity; initialised to ``quantity``.
    """

    order_id: int
    side: Side
    price: int | None
    quantity: int
    timestamp: int
    order_type: OrderType = OrderType.LIMIT
    remaining: int = field(init=False)

    def __post_init__(self) -> None:
        self.remaining = self.quantity


@dataclass(frozen=True, slots=True)
class Trade:
    """An immutable record of a single execution between a buy and a sell order."""

    buy_order_id: int
    sell_order_id: int
    price: int
    quantity: int
    timestamp: int
