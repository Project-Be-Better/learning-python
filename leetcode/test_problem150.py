import unittest
from problem150 import Solution


class TestProblem150(unittest.TestCase):

    def test_eval_rpn(self):
        input = ["2", "1", "+", "3", "*"]
        solution = Solution()
        output = solution.evalRPN(input)
        self.assertEqual(output, 9)

        input = ["4", "13", "5", "/", "+"]
        output = solution.evalRPN(input)
        self.assertEqual(output, 6)

        input = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
        output = solution.evalRPN(input)
        self.assertEqual(output, 22)
