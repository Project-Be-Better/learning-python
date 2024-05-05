import unittest
from problem242 import is_anagram


class TestProblem242(unittest.TestCase):

    def test_is_anagram(self):
        s = "anagram"
        t = "angaram"
        self.assertTrue(is_anagram(s, t))

        s = "cat"
        t = "dog"
        self.assertFalse(is_anagram(s, t))
