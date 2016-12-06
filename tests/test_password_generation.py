# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.utils import iteritems
import unittest

from passwdgen.generator import *
from passwdgen.constants import *
from passwdgen.utils import *


class TestPasswordGeneration(unittest.TestCase):

    word_list = load_word_list()

    def test_failure_modes(self):
        try:
            chars("some-unrecognised-charset")
            self.fail("Unrecognised charsets should trigger a ValueError")
        except ValueError:
            pass

    def test_password_charset_intersection(self):
        for charset_id, charset in iteritems(PASSWORD_CHARSETS):
            pw = chars(charset_id)
            self.assertEqual(DEFAULT_CHAR_PASSWORD_LENGTH, len(pw))
            pw_chars = set(pw)
            self.assertTrue(pw_chars.issubset(charset))

    def test_character_length_based_password_generation(self):
        pw = chars(PC_SPECIAL, length=10)
        self.assertEqual(10, len(pw))

        pw = chars(PC_SPECIAL, length=20)
        self.assertEqual(20, len(pw))

    def test_character_entropy_based_password_generation(self):
        pw = chars(PC_SPECIAL, min_entropy=50)
        entropy = calculate_entropy(pw, PASSWORD_CHARSETS[PC_SPECIAL])
        self.assertTrue(entropy[PC_SPECIAL] >= 50.0)

        pw = chars(PC_SPECIAL, min_entropy=100)
        entropy = calculate_entropy(pw, PASSWORD_CHARSETS[PC_SPECIAL])
        self.assertTrue(entropy[PC_SPECIAL] >= 100.0)

    def test_dict_word_size_based_password_generation(self):
        pw = words(self.word_list, word_count=4)
        pw_words = pw.split(DEFAULT_WORD_SEPARATOR)
        self.assertEqual(4, len(pw_words))

        pw = words(self.word_list, separator=":", word_count=8)
        pw_words = pw.split(":")
        self.assertEqual(8, len(pw_words))

    def test_dict_entropy_based_password_generation(self):
        pw = words(self.word_list, min_entropy=50)
        entropy = calculate_entropy(pw, dict_set=self.word_list)
        self.assertTrue(entropy[PC_DICT] >= 50.0)

        pw = words(self.word_list, min_entropy=100)
        entropy = calculate_entropy(pw, dict_set=self.word_list)
        self.assertTrue(entropy[PC_DICT] >= 100.0)


if __name__ == "__main__":
    unittest.main()
