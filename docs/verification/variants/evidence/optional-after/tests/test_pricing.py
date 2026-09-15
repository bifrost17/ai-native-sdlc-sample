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

    def test_valid_percent_boundaries_and_empty_amounts(self):
        self.assertEqual(payable([100, 250], 0), 350)
        self.assertEqual(payable([100, 250], 100), 0)
        self.assertEqual(payable([], 25), 0)

    def test_percent_outside_range_raises_value_error(self):
        for discount_percent in (-1, 101):
            with self.subTest(discount_percent=discount_percent):
                with self.assertRaises(ValueError):
                    payable([100], discount_percent)

    def test_does_not_mutate_amounts(self):
        amounts = [1001, 250]
        payable(amounts, 10)
        self.assertEqual(amounts, [1001, 250])


if __name__ == "__main__": unittest.main()
