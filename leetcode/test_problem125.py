import unittest
from problem125 import is_palindrome


class TestProblem125(unittest.TestCase):

    def test_is_palindrome(self):

        input = "A man, a plan, a canal: Panama"
        output = is_palindrome(input)
        self.assertTrue(output)

        input = "race a car"
        output = is_palindrome(input)
        self.assertFalse(output)

        input = " "
        output = is_palindrome(input)
        self.assertTrue(output)
