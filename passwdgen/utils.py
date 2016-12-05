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
import os
import struct

from constants import *


__all__ = [
    "clean_word_list",
    "permutations",
    "calculate_entropy",
    "load_word_list",
    "secure_random",
    "secure_random_quality"
]


def clean_word_list(input_path, output_path, encoding=None, min_word_len=None):
    """Cleans the given word list, ensuring no punctuation or capitalisation or duplicate words. Word lists
    must be plain text files, with one word per line, and sorted alphabetically.

    Args:
        input_path: The path to the input word list file.
        output_path: The path to where to write the output, filtered word list.
        encoding: The encoding to use when attempting to read the file (default: platform-dependent).
        min_word_len: The minimum length of words to include. Defaults to constants.DEFAULT_MIN_WORD_LEN.

    Returns:
        A dictionary containing statistics about the clean operation.
    """
    if min_word_len is None:
        min_word_len = DEFAULT_MIN_WORD_LEN
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

                if stripped_word and len(stripped_word) >= min_word_len:
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
            words = password.split(sep) if sep is not None else [password]
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

    if len(words) < MIN_DICT_SIZE:
        raise ValueError("Dictionary is too small. Valid dictionaries must contain at least %d unique words." % MIN_DICT_SIZE)

    return words


def secure_random(a, b=None):
    """Generates integers in the most secure manner possible provided by the operating system. On POSIX machines,
    this will use /dev/urandom. On Windows machines, this will use CryptGenRandom().

    Args:
        a: If b is supplied, this should be the minimum value of the randomly generated number (inclusive). If b
            is not supplied, this should be the maximum value of the randomly generated number (exclusive), and the
            minimum will be 0.
        b: If supplied, this must provide the maximum value of the randomly generated number (exclusive).

    Returns:
        A random integer i, with a <= i < b if b is supplied, otherwise 0 <= i < a.
    """
    if (a < 0) or ((b is not None) and (b < 0)):
        raise ValueError("Both a and b need to be integers >= 0 for secure random number generation")
    if (b is not None) and (b <= a):
        raise ValueError("For secure random number generation, b must be < a")

    (random_val, ) = struct.unpack("Q", os.urandom(8))
    return (random_val % int(a)) if b is None else (int(a) + (random_val % int(b - a)))


def secure_random_quality(sample_size=1000000):
    """Attempts to estimate the quality of the secure random number generator of the operating system.

    Args:
        sample_size: The number of random samples to generate and test.

    Returns:
        A dictionary containing some statistics about the random number generator.
    """
    start_time = time.time()

    total = 0
    counts = dict()
    for i in range(sample_size):
        rnd_val = secure_random(101)
        total += rnd_val
        counts[rnd_val] = (counts[rnd_val] + 1) if rnd_val in counts else 1

    mean = float(total) / float(sample_size)
    # calculate the variance
    variance = 0.0
    for val, count in iteritems(counts):
        variance += (val - mean) * count
    variance /= float(sample_size) - 1.0
    # ensure variance is positive (sometimes zeros can be negative with floating point numbers)
    if variance < 0.0:
        variance *= -1.0
    stddev = math.sqrt(variance)

    end_time = time.time()
    return {
        "mean": mean,
        "stddev": stddev,
        "variance": variance,
        "time": end_time - start_time
    }
