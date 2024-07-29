import unittest
from problem15 import three_sum


class TestProblem15(unittest.TestCase):

    def test_three_sum(self):
        input = [-1, 0, 1, 2, -1, -4]
        output = three_sum(input)
        result = [[-1, -1, 2], [-1, 0, 1]]
        self.assertEqual(output, result)

        input = [0, 0, 0]
        output = three_sum(input)
        result = [[0, 0, 0]]
        self.assertEqual(output, result)

        input = [0, 0, 0, 0]
        output = three_sum(input)
        result = [[0, 0, 0]]
        self.assertEqual(output, result)
