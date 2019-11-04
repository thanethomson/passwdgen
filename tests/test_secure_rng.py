# -*- coding: utf-8 -*-

import unittest
from passwdgen.utils import secure_random


class TestSecureRNG(unittest.TestCase):

    def test_upper_limiting_only(self):
        for i in range(1000):
            random_val = secure_random(100)
            self.assertTrue(0 <= random_val < 100)

    def test_upper_and_lower_limiting(self):
        for i in range(1000):
            random_val = secure_random(50, 100)
            self.assertTrue(50 <= random_val < 100)


if __name__ == "__main__":
    unittest.main()
