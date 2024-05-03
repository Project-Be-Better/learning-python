import unittest
from problem88 import merge


class TestProblem88(unittest.TestCase):

    def test_merge(self):
        # Test case 1
        nums1 = [1, 2, 3, 0, 0, 0]
        m = 3
        nums2 = [2, 5, 6]
        n = 3
        merge(nums1, nums2, m, n)
        self.assertEqual(nums1, [1, 2, 2, 3, 5, 6])

        # Test case 2
        nums1 = [1]
        m = 1
        nums2 = []
        n = 0
        # merge(nums1, m, nums2, n)
        merge(nums1, nums2, m, n)

        self.assertEqual(nums1, [1])

        # Test case 3
        nums1 = [0]
        m = 0
        nums2 = [1]
        n = 1
        # merge(nums1, m, nums2, n)
        merge(nums1, nums2, m, n)

        self.assertEqual(nums1, [1])
