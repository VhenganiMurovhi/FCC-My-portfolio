
+import math
+import unittest
+
+from montecarlo.simulations import estimate_pi, price_european_call
+
+
+class TestPiSimulation(unittest.TestCase):
+    def test_estimate_pi_is_reasonable(self):
+        result = estimate_pi(trials=200_000, seed=123)
+        self.assertTrue(abs(result.estimate - math.pi) < 0.02)
+        self.assertGreater(result.standard_error, 0)
+
+    def test_invalid_trials_raises(self):
+        with self.assertRaises(ValueError):
+            estimate_pi(trials=0)
+
+
+class TestOptionSimulation(unittest.TestCase):
+    def test_price_is_positive(self):
+        result = price_european_call(
+            spot=100,
+            strike=100,
+            rate=0.05,
+            volatility=0.2,
+            maturity=1.0,
+            trials=200_000,
+            seed=123,
+        )
+        self.assertGreater(result.price, 0)
+        self.assertGreaterEqual(result.standard_error, 0)
+
+    def test_invalid_parameters_raise(self):
+        with self.assertRaises(ValueError):
+            price_european_call(
+                spot=-1,
+                strike=100,
+                rate=0.05,
+                volatility=0.2,
+                maturity=1.0,
+                trials=1_000,
+            )
+
+
+if __name__ == "__main__":
+    unittest.main()
