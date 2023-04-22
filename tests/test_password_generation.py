# -*- coding: utf-8 -*-

import unittest

from passwdgen.generator import *
from passwdgen.constants import *
from passwdgen.utils import *


class TestPasswordGeneration(unittest.TestCase):
    word_list = load_word_list()

    def test_unrecognised_charset(self):
        try:
            chars("some-unrecognised-charset")
            self.fail("Unrecognised charsets should trigger a ValueError")
        except ValueError:
            pass

    def test_not_enough_starting_letters(self):
        try:
            words(self.word_list, word_count=5, starting_letters="abc")
            self.fail(
                "Fewer starting letters than required word count should trigger a ValueError"
            )
        except ValueError:
            pass

        try:
            words(self.word_list, min_entropy=80, starting_letters="abc")
            self.fail(
                "Fewer starting letters than required word count should trigger a ValueError"
            )
        except ValueError:
            pass

    def test_password_charset_intersection(self):
        for charset_id, charset in PASSWORD_CHARSETS.items():
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

    def test_starting_letters(self):
        starting_letters = "hello"
        pw = words(self.word_list, starting_letters=starting_letters)
        pw_words = pw.split("-")
        self.assertEqual(len(starting_letters), len(pw_words))
        for i in range(len(pw_words)):
            self.assertTrue(pw_words[i].startswith(starting_letters[i]))


if __name__ == "__main__":
    unittest.main()
