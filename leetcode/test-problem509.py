import unittest
from problem509 import fibonacci, fibonacci_recursion


class TestProblem509(unittest.TestCase):

    def test_fibonacci(self):
        result = 1
        output = fibonacci(2)
        self.assertEqual(result, output)

        result = 2
        output = fibonacci(3)
        self.assertEqual(result, output)

        result = 3
        output = fibonacci(4)
        self.assertEqual(result, output)

        result = 1
        output = fibonacci_recursion(2)
        self.assertEqual(result, output)

        result = 2
        output = fibonacci_recursion(3)
        self.assertEqual(result, output)

        result = 3
        output = fibonacci_recursion(4)
        self.assertEqual(result, output)
