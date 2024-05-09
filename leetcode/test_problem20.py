import unittest
from problem20 import valid_parentheses


class TestProblem20(unittest.TestCase):

    def test_valid_parentheses(self):
        s = "()"
        rlt = valid_parentheses(s)
        self.assertTrue(rlt)

        s = "()[]{}"
        rlt = valid_parentheses(s)
        self.assertTrue(rlt)

        s = "(]"
        rlt = valid_parentheses(s)
        self.assertFalse(rlt)

        s = "([)]"
        rlt = valid_parentheses(s)
        self.assertFalse(rlt)
