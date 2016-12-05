# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest

from passwdgen.utils import permutations


class TestPermutationCount(unittest.TestCase):

    def test_failure_modes(self):
        # should return 0 if k > n
        self.assertEqual(0, permutations(10, 20))
        # should return 0 if k < 0
        self.assertEqual(0, permutations(10, -1))

    def test_basic_permutations(self):
        # test some pre-calculated permutation counts
        self.assertEqual(90, permutations(10, 2))
        self.assertEqual(720, permutations(10, 3))
        self.assertEqual(5040, permutations(10, 4))
        self.assertEqual(30240, permutations(10, 5))
        self.assertEqual(151200, permutations(10, 6))
        self.assertEqual(604800, permutations(10, 7))
        self.assertEqual(1814400, permutations(10, 8))
        self.assertEqual(3628800, permutations(10, 9))
        self.assertEqual(3628800, permutations(10, 10))


if __name__ == "__main__":
    unittest.main()
