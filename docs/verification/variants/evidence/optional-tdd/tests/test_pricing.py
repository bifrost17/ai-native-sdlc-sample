"""AC0: Existing subtotal behavior."""
import unittest
from pricing import payable, subtotal

class SubtotalTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(subtotal([]), 0)
    def test_multiple(self): self.assertEqual(subtotal([100, 250]), 350)
    def test_no_mutation(self):
        items=[100, 250]
        subtotal(items)
        self.assertEqual(items, [100, 250])

class PayableTests(unittest.TestCase):
    def test_floors_discount_before_subtracting(self):
        self.assertEqual(payable([1001], 10), 901)

    def test_zero_full_and_empty_boundaries(self):
        self.assertEqual(payable([100, 250], 0), 350)
        self.assertEqual(payable([100, 250], 100), 0)
        self.assertEqual(payable([], 37), 0)

    def test_rejects_percent_outside_inclusive_range(self):
        for percent in (-1, 101):
            with self.subTest(percent=percent):
                with self.assertRaises(ValueError):
                    payable([100], percent)

    def test_does_not_mutate_amounts(self):
        items = [1001, 250]
        payable(items, 10)
        self.assertEqual(items, [1001, 250])

if __name__ == "__main__": unittest.main()
