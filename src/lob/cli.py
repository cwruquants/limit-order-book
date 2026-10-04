"""Interactive REPL for driving an order book by hand."""

import argparse
from dataclasses import dataclass, field

from lob.book import OrderBook, SortedDictOrderBook
from lob.order import Order, Side, Trade

HELP_TEXT = """\
Commands:
  add <buy|sell> <price> <qty>   submit a limit order (price in integer ticks)
  cancel <id>                    cancel a resting order
  book                           show top-of-book depth
  trades                         show trades executed this session
  help                           show this message
  quit                           exit"""

NOT_IMPLEMENTED = "not implemented yet"


@dataclass
class Session:
    """REPL state: the book, id/timestamp counters, and the session trade log."""

    book: OrderBook = field(default_factory=SortedDictOrderBook)
    trades: list[Trade] = field(default_factory=list)
    next_order_id: int = 1
    next_timestamp: int = 1

    def new_order(self, side: Side, price: int, quantity: int) -> Order:
        """Build a LIMIT order with the next order id and sequence timestamp."""
        order = Order(
            order_id=self.next_order_id,
            side=side,
            price=price,
            quantity=quantity,
            timestamp=self.next_timestamp,
        )
        self.next_order_id += 1
        self.next_timestamp += 1
        return order


def _parse_positive_int(token: str, name: str) -> int:
    value = int(token)
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _cmd_add(session: Session, args: list[str]) -> None:
    if len(args) != 3:
        print("usage: add <buy|sell> <price> <qty>")
        return
    side_token, price_token, qty_token = args
    try:
        side = Side[side_token.upper()]
    except KeyError:
        print("side must be 'buy' or 'sell'")
        return
    try:
        price = _parse_positive_int(price_token, "price")
        quantity = _parse_positive_int(qty_token, "qty")
    except ValueError as exc:
        print(f"invalid input: {exc}")
        return
    order = session.new_order(side, price, quantity)
    try:
        trades = session.book.add(order)
    except NotImplementedError:
        print(NOT_IMPLEMENTED)
        return
    session.trades.extend(trades)
    print(f"order {order.order_id} accepted")
    for trade in trades:
        print(f"  {trade}")


def _cmd_cancel(session: Session, args: list[str]) -> None:
    if len(args) != 1:
        print("usage: cancel <id>")
        return
    try:
        order_id = int(args[0])
    except ValueError:
        print("invalid input: id must be an integer")
        return
    try:
        cancelled = session.book.cancel(order_id)
    except NotImplementedError:
        print(NOT_IMPLEMENTED)
        return
    print(f"order {order_id} cancelled" if cancelled else f"order {order_id} not found")


def _cmd_book(session: Session, args: list[str]) -> None:
    try:
        depth = session.book.depth()
    except NotImplementedError:
        print(NOT_IMPLEMENTED)
        return
    print("asks:")
    for price, qty in reversed(depth["asks"]):
        print(f"  {price:>8} x {qty}")
    print("bids:")
    for price, qty in depth["bids"]:
        print(f"  {price:>8} x {qty}")


def _cmd_trades(session: Session, args: list[str]) -> None:
    if not session.trades:
        print("no trades")
        return
    for trade in session.trades:
        print(trade)


def handle_command(session: Session, line: str) -> bool:
    """Execute one REPL line. Returns False when the REPL should exit."""
    tokens = line.split()
    if not tokens:
        return True
    command, args = tokens[0].lower(), tokens[1:]
    if command in ("quit", "exit"):
        return False
    if command == "help":
        print(HELP_TEXT)
    elif command == "add":
        _cmd_add(session, args)
    elif command == "cancel":
        _cmd_cancel(session, args)
    elif command == "book":
        _cmd_book(session, args)
    elif command == "trades":
        _cmd_trades(session, args)
    else:
        print(f"unknown command: {command!r} (type 'help')")
    return True


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``lob`` console script."""
    parser = argparse.ArgumentParser(
        prog="lob",
        description="Interactive limit order book REPL.",
        epilog=HELP_TEXT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args(argv)

    session = Session()
    print("lob REPL. Type 'help' for commands.")
    while True:
        try:
            line = input("lob> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not handle_command(session, line):
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
