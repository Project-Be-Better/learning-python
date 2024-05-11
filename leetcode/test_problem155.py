import unittest
from problem155 import MinStack


class TestProblem155(unittest.TestCase):

    def test_push_pop_top_get_min(self):
        stack = MinStack()

        stack.push(-2)
        self.assertEqual(stack.top(), -2)
        self.assertEqual(stack.get_min(), -2)

        stack.push(0)
        self.assertEqual(stack.top(), 0)
        self.assertEqual(stack.get_min(), -2)

        stack.pop()
        self.assertEqual(stack.top(), -2)
        self.assertEqual(stack.get_min(), -2)

        stack.push(-3)
        self.assertEqual(stack.get_min(), -3)
