
+"""Command line interface for Monte Carlo simulations."""
+
+from __future__ import annotations
+
+import argparse
+
+from .simulations import estimate_pi, price_european_call
+
+
+def build_parser() -> argparse.ArgumentParser:
+    parser = argparse.ArgumentParser(description="Monte Carlo simulation toolkit")
+    subparsers = parser.add_subparsers(dest="command", required=True)
+
+    pi_parser = subparsers.add_parser("pi", help="Estimate pi")
+    pi_parser.add_argument("--trials", type=int, default=100_000)
+    pi_parser.add_argument("--seed", type=int, default=None)
+
+    option_parser = subparsers.add_parser("option", help="Price a European call")
+    option_parser.add_argument("--spot", type=float, required=True)
+    option_parser.add_argument("--strike", type=float, required=True)
+    option_parser.add_argument("--rate", type=float, required=True)
+    option_parser.add_argument("--volatility", type=float, required=True)
+    option_parser.add_argument("--maturity", type=float, required=True)
+    option_parser.add_argument("--trials", type=int, default=100_000)
+    option_parser.add_argument("--seed", type=int, default=None)
+
+    return parser
+
+
+def main() -> None:
+    parser = build_parser()
+    args = parser.parse_args()
+
+    if args.command == "pi":
+        result = estimate_pi(trials=args.trials, seed=args.seed)
+        print(f"pi_estimate={result.estimate:.8f}")
+        print(f"standard_error={result.standard_error:.8f}")
+        print(f"trials={result.trials}")
+    elif args.command == "option":
+        result = price_european_call(
+            spot=args.spot,
+            strike=args.strike,
+            rate=args.rate,
+            volatility=args.volatility,
+            maturity=args.maturity,
+            trials=args.trials,
+            seed=args.seed,
+        )
+        print(f"call_price={result.price:.8f}")
+        print(f"standard_error={result.standard_error:.8f}")
+        print(f"trials={result.trials}")
+
+
+if __name__ == "__main__":
+    main()
