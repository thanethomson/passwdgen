# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.utils import iteritems
from builtins import range
from functools import reduce
from operator import mul
from string import ascii_lowercase
from io import open
import time
import math
import pkg_resources

from constants import *


def clean_word_list(input_path, output_path, encoding=None):
    """Cleans the given word list, ensuring no punctuation or capitalisation or duplicate words. Word lists
    must be plain text files, with one word per line, and sorted alphabetically.

    Args:
        input_path: The path to the input word list file.
        output_path: The path to where to write the output, filtered word list.
        encoding: The encoding to use when attempting to read the file (default: platform-dependent).

    Returns:
        A dictionary containing statistics about the clean operation.
    """
    word_list = set()
    start_time = time.time()
    words_read = 0
    with open(input_path, "rt", encoding=encoding) as input_file:
        for line in input_file:
            word = line.strip().lower()
            if len(word) > 0:
                words_read += 1

                # strip possessives
                if word.endswith("'s"):
                    word = word[:-2]

                # strip non-alphabetical characters
                stripped_word = ""
                for c in word:
                    if c in ascii_lowercase:
                        stripped_word += c

                if stripped_word:
                    word_list.add(stripped_word)

    with open(output_path, "wt", encoding=encoding) as output_file:
        for word in sorted(list(word_list)):
            output_file.write("%s\n" % word)

    end_time = time.time()
    return {
        "time": end_time - start_time,
        "words_read": words_read,
        "words_written": len(word_list)
    }


def permutations(n, k):
    """Calculates the number of ordered k-permutations of n.

    Args:
        n: The total size of the set.
        k: The size of each sub-set.

    Returns:
        The number of possible uniquely ordered subsets of length k that can be generated from the set of size n.
    """
    return reduce(mul, range(n - k + 1, n + 1)) if 0 <= k <= n else 0


def calculate_entropy(password, dict_set=None):
    """Utility to calculate the entropy of a password (in bits) based on the detected charset (as from the
    perspective of a prospective attacker).

    Args:
        password: The source password to use in calculation.
        dict_set: The set of words in our dictionary/word list.

    Returns:
        A dictionary containing the entropies of the password based on different attacker dictionaries.
    """
    password_letters = set(password)
    password_len = len(password)
    entropy = dict()

    # find the charsets in which we'll find this password
    for charset_name, charset in iteritems(PASSWORD_CHARSETS):
        if password_letters.issubset(charset):
            entropy[charset_name] = math.log(1.0*len(charset), 2.0) * password_len

    if dict_set is not None:
        # we assume our dictionary words are all lowercase, and that our separator is used
        if password_letters.issubset(PASSWORD_CHARSETS[PC_ALPHA_LOWER_SEP]):
            # detect the separator
            sep = None
            for c in password_letters:
                if c in separators:
                    sep = c
                    break

            # split the words by separator
            if sep is not None:
                words = password.split(sep)
                # only if the words are unique to each other
                if len(words) == len(set(words)):
                    all_words_found = True
                    for word in words:
                        if word not in dict_set:
                            all_words_found = False

                    # only if all of the words in the password are in our specific dictionary
                    if all_words_found:
                        entropy[PC_DICT] = math.log(permutations(len(dict_set), len(words)), 2.0)

    return entropy


def load_word_list(filename=None, resource=None, encoding=None):
    """Loads a word list from the given filename or resource.

    Args:
        filename: If specified, loads the word list from this file system path.
        resource: If no filename is specified, this is loaded relative to the passwdgen package path. If no resource
            is specified, the default word list is used.
        encoding: The encoding to use when reading the file (default: OS-dependent).

    Returns:
        A set containing the entire list of non-zero-length words in the word list.
    """
    words = set()

    if filename is None:
        filename = pkg_resources.resource_filename("passwdgen", resource or DEFAULT_WORD_LIST)

    with open(filename, "rt", encoding=encoding) as input_file:
        for line in input_file:
            word = line.strip()
            if len(word) > 0:
                words.add(word)

    return words
