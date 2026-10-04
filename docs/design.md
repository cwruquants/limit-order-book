# Design

## Goals and non-goals

**Goals**

- Correct, deterministic matching with strict price-time priority.
- A small, stable `OrderBook` interface that multiple implementations can satisfy.
- Clear, testable invariants, verified with property-based tests.
- Measurable performance (Phase 3) without sacrificing clarity.

**Non-goals**

- Networking, FIX/ITCH protocols, or exchange connectivity.
- Multi-threaded or distributed matching.
- Floating-point prices. All prices are integer ticks.
- Wall-clock time inside the engine. Timestamps are caller-supplied sequence numbers.

## Core types

Defined in `src/lob/order.py`.

| Type        | Kind                          | Fields / members                                                                                                                |
|-------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `Side`      | `Enum`                        | `BUY`, `SELL`                                                                                                                   |
| `OrderType` | `Enum`                        | `LIMIT` (Phase 1); `MARKET`, `IOC`, `FOK`, `STOP`, `STOP_LIMIT`, `ICEBERG` (Phase 2)                                            |
| `Order`     | `dataclass(slots=True)`       | `order_id: int`, `side: Side`, `price: int \| None`, `quantity: int`, `timestamp: int`, `order_type: OrderType = LIMIT`, `remaining: int` |
| `Trade`     | `dataclass(frozen, slots)`    | `buy_order_id: int`, `sell_order_id: int`, `price: int`, `quantity: int`, `timestamp: int`                                     |

- `price` is in integer ticks; `None` only for market orders.
- `timestamp` is a monotonic sequence number, not wall-clock time.
- `remaining` is set to `quantity` in `__post_init__` and decremented as the order fills.

## OrderBook contract

Defined in `src/lob/book.py`.

| Method                                                    | Contract                                                                                                                     |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `add(order: Order) -> list[Trade]`                        | Match against the opposite side using strict price-time priority, rest any remainder, return trades in execution order.     |
| `cancel(order_id: int) -> bool`                           | O(1) lookup. Remove the resting order and return `True`; return `False` if not found.                                        |
| `best_bid() -> int \| None`                               | Highest resting bid price, or `None`.                                                                                        |
| `best_ask() -> int \| None`                               | Lowest resting ask price, or `None`.                                                                                         |
| `spread() -> int \| None`                                 | Concrete: `best_ask - best_bid`, or `None` if either side is empty.                                                          |
| `depth(levels: int = 5) -> dict[str, list[tuple[int, int]]]` | `{"bids": [(price, qty), ...], "asks": [...]}`, aggregated per level, best price first.                                    |

## Data-structure choice

`SortedDictOrderBook` uses:

- **Per side: `SortedDict[int, PriceLevel]`** (price → level). Sorted keys give O(log n) insert
  and delete of price levels, and best-price access via `peekitem(0)` / `peekitem(-1)`.
- **`dict[int, Order]`** (order_id → order) for O(1) cancel lookup.
- **`PriceLevel`**: a `collections.deque[Order]` per price, giving FIFO time priority with O(1)
  append and pop from the front.

## Matching semantics

- **Strict price-time priority.** Better prices match first; at equal prices, earlier
  `timestamp` matches first.
- **Trades execute at the resting order's price**, not the incoming order's price.
- **Partial fills** leave the remainder resting with its original time priority.
- **Quantity modifications:** reducing quantity keeps priority. Any other modification (price
  change or quantity increase) loses priority; treat it as cancel + new order.

## Invariants

These must hold after every public method returns, and should be checked with hypothesis
property tests:

1. The book is never crossed after `add` returns: `best_bid < best_ask` whenever both exist.
2. No zero-quantity orders rest on the book (`remaining > 0` for every resting order).
3. For each side, the sum of level `total_quantity` equals the sum of `remaining` over resting
   orders on that side.

## Open decisions

| Topic                   | Question                                                                                        | Status |
|-------------------------|-------------------------------------------------------------------------------------------------|--------|
| Iceberg refill priority | When the visible slice refills, does it keep its time priority or go to the back of the level? | TBD    |
| FOK liquidity check     | How is available liquidity checked before execution (full pre-scan vs. dry-run match)?          | TBD    |
| Stop trigger source     | Do stops trigger on last trade price or on mid price?                                           | TBD    |
| Self-trade prevention   | Is it supported, and if so which policy (cancel newest, cancel oldest, cancel both)?            | TBD    |
