# Monte Carlo Simulation Project

A lightweight Python project that demonstrates Monte Carlo methods with two practical simulations:

1. **Estimating \(\pi\)** using random point sampling.
2. **European call option pricing** under a geometric Brownian motion model.

## Features

- Deterministic runs with optional random seed
- CLI interface for running simulations quickly
- Reusable Python API
- Basic unit tests

## Project Structure

```text
.
├── README.md
├── pyproject.toml
├── src
│   └── montecarlo
│       ├── __init__.py
│       ├── cli.py
│       └── simulations.py
└── tests
    └── test_simulations.py
```

## Quick Start

### 1) Run with Python module mode

Estimate pi:

```bash
python -m montecarlo.cli pi --trials 200000 --seed 7
```

Price an option:

```bash
python -m montecarlo.cli option \
  --spot 100 --strike 105 --rate 0.03 --volatility 0.2 --maturity 1.0 \
  --trials 500000 --seed 21
```

### 2) Install editable package (optional)

```bash
pip install -e .
```

Then run:

```bash
montecarlo pi --trials 100000
```

## API Example

```python
from montecarlo.simulations import estimate_pi, price_european_call

pi_result = estimate_pi(trials=100_000, seed=42)
print(pi_result.estimate, pi_result.standard_error)

option_result = price_european_call(
    spot=100,
    strike=100,
    rate=0.05,
    volatility=0.2,
    maturity=1.0,
    trials=200_000,
    seed=42,
)
print(option_result.price, option_result.standard_error)
```

## Testing

```bash
python -m unittest discover -s tests
```

## Notes

- Monte Carlo error decreases with \(\mathcal{O}(1 / \sqrt{N})\), so larger trial counts improve precision.
- This project uses only the Python standard library.
