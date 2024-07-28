import unittest
from problem121 import max_profit


class TestProblem121(unittest.TestCase):

    def test_max_profit(self):
        prices = [7, 1, 5, 3, 6, 4]
        result = 5
        output = max_profit(prices)
        self.assertEqual(result, output)

        prices = [7, 6, 4, 3, 1]
        result = 0
        output = max_profit(prices)
        self.assertEqual(result, output)
