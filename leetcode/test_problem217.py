from problem217 import contains_duplicate
import unittest


class TestDuplicate(unittest.TestCase):

    def test_contains_duplicate(self):
        nums = [1, 2, 3, 1]
        result = contains_duplicate(nums)
        self.assertTrue(result)

        nums = [1, 2, 3]
        result = contains_duplicate(nums)
        self.assertFalse(result)

        nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
        result = contains_duplicate(nums)
        self.assertTrue(result)
