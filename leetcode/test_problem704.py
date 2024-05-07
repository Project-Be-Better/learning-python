import unittest
from problem704 import search


class TestSearch(unittest.TestCase):

    def test_search(self):
        nums = [-1, 0, 3, 5, 9, 12]
        target = 9
        rlt = search(nums, target)
        self.assertEqual(rlt, 4)

        nums = [-1, 0, 3, 5, 9, 12]
        target = 2
        rlt = search(nums, target)
        self.assertEqual(rlt, -1)

        nums = [-1, 0, 3, 3, 5, 9, 12]
        target = 3
        rlt = search(nums, target)
        self.assertNotEqual(rlt, 2)
