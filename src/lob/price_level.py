"""A single price level: a FIFO queue of resting orders at one price."""

from collections import deque

from lob.order import Order


class PriceLevel:
    """FIFO queue of resting orders at a single price, backed by ``collections.deque``."""

    __slots__ = ("price", "_orders")

    def __init__(self, price: int) -> None:
        self.price: int = price
        self._orders: deque[Order] = deque()

    def append(self, order: Order) -> None:
        """Add ``order`` to the back of the queue (lowest time priority at this level)."""
        # TODO(Phase 1)
        raise NotImplementedError

    def pop_front(self) -> Order:
        """Remove and return the order with the highest time priority.

        Raises:
            IndexError: If the level is empty.
        """
        # TODO(Phase 1)
        raise NotImplementedError

    def remove(self, order_id: int) -> bool:
        """Remove the order with ``order_id`` from this level.

        Returns:
            True if the order was found and removed, False otherwise.
        """
        # TODO(Phase 1)
        raise NotImplementedError

    def peek(self) -> Order | None:
        """Return the order with the highest time priority without removing it, or None."""
        # TODO(Phase 1)
        raise NotImplementedError

    @property
    def total_quantity(self) -> int:
        """Sum of ``remaining`` across all orders at this level."""
        # TODO(Phase 1)
        raise NotImplementedError

    def __len__(self) -> int:
        """Number of orders resting at this level."""
        # TODO(Phase 1)
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True if no orders rest at this level."""
        # TODO(Phase 1)
        raise NotImplementedError
