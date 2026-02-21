
+"""Core Monte Carlo simulation routines."""
+
+from __future__ import annotations
+
+from dataclasses import dataclass
+import math
+import random
+
+
+@dataclass(frozen=True)
+class PiEstimationResult:
+    estimate: float
+    inside_ratio: float
+    standard_error: float
+    trials: int
+
+
+@dataclass(frozen=True)
+class OptionPricingResult:
+    price: float
+    standard_error: float
+    discounted_payoff_mean: float
+    trials: int
+
+
+def _validate_trials(trials: int) -> None:
+    if trials <= 0:
+        raise ValueError("trials must be a positive integer")
+
+
+def estimate_pi(trials: int, seed: int | None = None) -> PiEstimationResult:
+    """Estimate pi via Monte Carlo random sampling in the unit square."""
+    _validate_trials(trials)
+    rng = random.Random(seed)
+
+    inside = 0
+    for _ in range(trials):
+        x = rng.random()
+        y = rng.random()
+        if x * x + y * y <= 1.0:
+            inside += 1
+
+    p_hat = inside / trials
+    estimate = 4.0 * p_hat
+    standard_error = 4.0 * math.sqrt(max(p_hat * (1.0 - p_hat), 0.0) / trials)
+
+    return PiEstimationResult(
+        estimate=estimate,
+        inside_ratio=p_hat,
+        standard_error=standard_error,
+        trials=trials,
+    )
+
+
+def price_european_call(
+    *,
+    spot: float,
+    strike: float,
+    rate: float,
+    volatility: float,
+    maturity: float,
+    trials: int,
+    seed: int | None = None,
+) -> OptionPricingResult:
+    """Price a European call option via risk-neutral Monte Carlo."""
+    _validate_trials(trials)
+    if spot <= 0 or strike <= 0:
+        raise ValueError("spot and strike must be positive")
+    if volatility < 0:
+        raise ValueError("volatility must be non-negative")
+    if maturity <= 0:
+        raise ValueError("maturity must be positive")
+
+    rng = random.Random(seed)
+    drift = (rate - 0.5 * volatility * volatility) * maturity
+    diffusion_scale = volatility * math.sqrt(maturity)
+    discount = math.exp(-rate * maturity)
+
+    discounted_payoffs: list[float] = []
+    for _ in range(trials):
+        z = rng.gauss(0.0, 1.0)
+        terminal_price = spot * math.exp(drift + diffusion_scale * z)
+        payoff = max(terminal_price - strike, 0.0)
+        discounted_payoffs.append(discount * payoff)
+
+    mean = sum(discounted_payoffs) / trials
+    if trials > 1:
+        variance = sum((x - mean) ** 2 for x in discounted_payoffs) / (trials - 1)
+        standard_error = math.sqrt(variance / trials)
+    else:
+        standard_error = 0.0
+
+    return OptionPricingResult(
+        price=mean,
+        standard_error=standard_error,
+        discounted_payoff_mean=mean,
+        trials=trials,
+    )
