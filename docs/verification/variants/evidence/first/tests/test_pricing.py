"""AC0: Existing subtotal behavior."""
import unittest
import pricing

subtotal = pricing.subtotal

class SubtotalTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(subtotal([]), 0)
    def test_multiple(self): self.assertEqual(subtotal([100, 250]), 350)
    def test_no_mutation(self):
        items=[100, 250]
        subtotal(items)
        self.assertEqual(items, [100, 250])


class PayableTests(unittest.TestCase):
    def test_calculation_examples(self):
        cases = [
            ([1001], 10, 901),
            ([100, 250], 0, 350),
            ([100, 250], 100, 0),
            ([], 25, 0),
        ]
        for amounts, discount_percent, expected in cases:
            with self.subTest(amounts=amounts, discount_percent=discount_percent):
                self.assertEqual(
                    pricing.payable(amounts, discount_percent), expected
                )

    def test_rejects_percent_below_zero(self):
        with self.assertRaises(ValueError):
            pricing.payable([100], -1)

    def test_rejects_percent_above_one_hundred(self):
        with self.assertRaises(ValueError):
            pricing.payable([100], 101)

    def test_does_not_mutate_amounts(self):
        amounts = [1001, 250]
        pricing.payable(amounts, 10)
        self.assertEqual(amounts, [1001, 250])

if __name__ == "__main__": unittest.main()
