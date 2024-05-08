import unittest
from problem74 import search_matrix


class TestProblem74(unittest.TestCase):

    def test_search_matrix(self):
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        target = 3
        rlt = search_matrix(matrix, target)
        self.assertTrue(rlt)

        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        target = 13
        rlt = search_matrix(matrix, target)
        self.assertFalse(rlt)
