from problem1 import twoSum
import unittest


class TestProblem1(unittest.TestCase):

    def test_two_sum(self):
        input = [2, 7, 11, 15]
        target = 9
        output = twoSum(input, target)
        self.assertEqual(output, [0, 1])

        input = [3, 2, 4]
        target = 6
        output = twoSum(input, target)
        self.assertEqual(output, [1, 2])

        input = [3, 3]
        target = 6
        output = twoSum(input, target)
        self.assertEqual(output, [0, 1])
