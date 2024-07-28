import unittest
from problem242 import is_anagram, is_anagram_longer


class TestProblem242(unittest.TestCase):

    def test_is_anagram(self):
        s = "anagram"
        t = "angaram"
        self.assertTrue(is_anagram(s, t))

        s = "cat"
        t = "dog"
        self.assertFalse(is_anagram(s, t))

    def test_is_anagram_longer(self):
        s = "anagram"
        t = "angaram"
        self.assertTrue(is_anagram_longer(s, t))

        s = "cat"
        t = "dog"
        self.assertFalse(is_anagram_longer(s, t))
