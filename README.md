# limit-order-book

Python limit order book and matching engine with price-time priority, multiple order types, and performance benchmarking.

## Overview

`lob` is a single-process limit order book built by CWRU Quants. Orders are matched with strict
price-time priority; prices are always integer ticks. The engine exposes a small, stable
interface (`OrderBook` in `src/lob/book.py`) so that alternative implementations can be
benchmarked against each other. See [`docs/design.md`](docs/design.md) for the full contract.

## Quickstart

Recommended: [uv](https://docs.astral.sh/uv/) installs the pinned Python (`.python-version`)
automatically.

```bash
git clone https://github.com/cwruquants/limit-order-book.git
cd limit-order-book
uv sync --extra dev
uv run pytest
uv run lob
```

Alternatively, with plain pip (Python 3.12+):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
lob
```

## Project structure

```text
limit-order-book/
├── src/lob/
│   ├── __init__.py       # public exports
│   ├── order.py          # Side, OrderType, Order, Trade
│   ├── price_level.py    # PriceLevel: FIFO queue at one price
│   ├── book.py           # OrderBook ABC + SortedDictOrderBook
│   └── cli.py            # `lob` interactive REPL
├── tests/                # pytest + hypothesis
├── docs/design.md        # design and matching semantics
└── .github/              # CI, templates, CODEOWNERS
```

## Roadmap

| Phase | Name                       | Scope                                                        |
|-------|----------------------------|--------------------------------------------------------------|
| 0+1   | MVP Matching               | Skeleton, LIMIT orders, price-time matching, cancel, depth   |
| 2     | Order Types                | MARKET, IOC, FOK, STOP, STOP_LIMIT, ICEBERG                  |
| 3     | Performance                | pytest-benchmark suite, profiling, alternative book backends |
| 4     | Multi-Symbol & Persistence | Multiple instruments, event log, snapshot/replay             |
| 5     | Analytics & Viz            | Depth charts, trade tape, market-quality metrics             |
| 6     | Stretch                    | TBD                                                          |

## Team tracks

| Track     | Owns                                                              |
|-----------|-------------------------------------------------------------------|
| Engine    | Matching logic, `OrderBook` implementations, `PriceLevel`         |
| Markets   | Order type semantics, market-structure rules, realistic scenarios |
| Infra     | CI, tooling, benchmarks, CLI, persistence                         |
| Tech Lead | Interfaces, design doc, reviews, roadmap                          |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © CWRU Quants
