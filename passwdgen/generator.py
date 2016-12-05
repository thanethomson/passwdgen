# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import math
from builtins import range

from .utils import secure_random
from .constants import *


__all__ = [
    "generate_password_chars",
    "generate_password_words"
]


def generate_password_chars(charset, length=None, min_entropy=None):
    """Generates a character-based password. If the length parameter is supplied, the min_entropy parameter
    is ignored (i.e. either a length or a minimum entropy is required, but not both). If no length or
    min_entropy parameters are supplied, a default password length is chosen (see
    constants.DEFAULT_CHAR_PASSWORD_LENGTH).

    Args:
        charset: The character set to use from which to source characters.
        length: The desired length of the password.
        min_entropy: The desired minimum entropy of the password, based on the given charset.

    Returns:
        A string containing the generated password.
    """
    if charset not in PASSWORD_CHARSETS:
        raise ValueError("Unrecognised charset: %s" % charset)
    else:
        charset_chars = list(PASSWORD_CHARSETS[charset])
        charset_size = len(charset_chars)

    password = ""

    if length is None and min_entropy is None:
        length = DEFAULT_CHAR_PASSWORD_LENGTH

    if length is not None:
        for i in range(length):
            password += charset_chars[secure_random(charset_size)]

    else:
        # work backwards from the entropy
        entropy_per_char = math.log(charset_size, 2.0)
        # round up on the number of characters
        min_chars = int(math.ceil(min_entropy / entropy_per_char))
        for i in range(min_chars):
            password += charset_chars[secure_random(charset_size)]

    return password


def generate_password_words(dict_set, separator=None, word_count=None, min_entropy=None):
    """Generates a word-based password from the given dictionary. If the word_count parameter is supplied,
    the min_entropy parameter is ignored (i.e. either a word count or minimum entropy is required, but not
    both). If no length or min_entropy parameters are supplied, a default word count is chosen (see
    constants.DEFAULT_WORD_PASSWORD_WORDS).

    Args:
        dict_set: The word list/dictionary from which to generate a password.
        separator:
        word_count: The number of words to use to build the password.
        min_entropy: The desired minimum entropy of the password, based on the given dictionary.

    Returns:
        A string containing the generated password.
    """
    word_list = list(dict_set)
    word_list_size = len(word_list)
    password_words = []

    if word_count is None and min_entropy is None:
        word_count = DEFAULT_WORD_PASSWORD_WORDS

    if separator is None:
        separator = DEFAULT_WORD_SEPARATOR

    if word_count is not None:
        for i in range(word_count):
            password_words.append(word_list[secure_random(word_list_size)])

    else:
        entropy_per_word = math.log(word_list_size, 2.0)
        min_words = int(math.ceil(min_entropy / entropy_per_word))
        for i in range(min_words):
            password_words.append(word_list[secure_random(word_list_size)])

    return separator.join(password_words)
