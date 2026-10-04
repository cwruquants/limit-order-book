"""Smoke tests for the Phase 0 skeleton."""

import dataclasses

import pytest

import lob
from lob import Order, OrderBook, OrderType, Side, Trade
from lob.book import SortedDictOrderBook


def test_package_exports() -> None:
    for name in ("Order", "Trade", "Side", "OrderType", "OrderBook"):
        assert hasattr(lob, name)


def test_order_remaining_defaults_to_quantity() -> None:
    order = Order(order_id=1, side=Side.BUY, price=100, quantity=10, timestamp=1)
    assert order.remaining == order.quantity == 10
    assert order.order_type is OrderType.LIMIT


def test_trade_is_frozen() -> None:
    trade = Trade(buy_order_id=1, sell_order_id=2, price=100, quantity=5, timestamp=3)
    with pytest.raises(dataclasses.FrozenInstanceError):
        trade.quantity = 6  # type: ignore[misc]


def test_sorted_dict_order_book_is_order_book() -> None:
    assert isinstance(SortedDictOrderBook(), OrderBook)


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="Phase 1: best_bid/best_ask")
def test_spread_is_none_on_empty_book() -> None:
    assert SortedDictOrderBook().spread() is None


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="Phase 1: matching engine")
def test_simple_cross() -> None:
    """Resting sell 100x10 + incoming buy 101x4 -> one trade at 100 for 4, 6 left resting."""
    book = SortedDictOrderBook()
    sell = Order(order_id=1, side=Side.SELL, price=100, quantity=10, timestamp=1)
    buy = Order(order_id=2, side=Side.BUY, price=101, quantity=4, timestamp=2)

    assert book.add(sell) == []
    trades = book.add(buy)

    assert len(trades) == 1
    trade = trades[0]
    assert trade.buy_order_id == 2
    assert trade.sell_order_id == 1
    assert trade.price == 100
    assert trade.quantity == 4
    assert sell.remaining == 6
    assert book.depth() == {"bids": [], "asks": [(100, 6)]}
    assert book.best_bid() is None
    assert book.best_ask() == 100
