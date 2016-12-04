# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import string

__all__ = [
    "PC_ALPHA_LOWER",
    "PC_ALPHA_UPPER",
    "PC_ALPHA",
    "PC_ALPHA_NUMERIC",
    "PC_NUMERIC",
    "PC_ALPHA_LOWER_SEP",
    "PC_ALPHA_UPPER_SEP",
    "PC_PRINTABLE",
    "PC_DICT",
    "PASSWORD_CHARSETS",
    "separators",
    "PASSWORD_CHARSET_NAMES",
    "DEFAULT_WORD_LIST"
]

PC_ALPHA_LOWER = "alpha-lower"
PC_ALPHA_UPPER = "alpha-upper"
PC_ALPHA = "alpha"
PC_ALPHA_NUMERIC = "alpha-numeric"
PC_NUMERIC = "numeric"
PC_ALPHA_LOWER_SEP = "alpha-lower-sep"
PC_ALPHA_UPPER_SEP = "alpha-upper-sep"
PC_PRINTABLE = "printable"
PC_DICT = "dict"

separators = "-_. ,"

PASSWORD_CHARSETS = {
    PC_ALPHA_LOWER: set(string.ascii_lowercase),
    PC_ALPHA_UPPER: set(string.ascii_uppercase),
    PC_ALPHA: set(string.ascii_letters),
    PC_ALPHA_NUMERIC: set(string.ascii_letters + string.digits),
    PC_ALPHA_LOWER_SEP: set(string.ascii_lowercase + separators),
    PC_ALPHA_UPPER_SEP: set(string.ascii_uppercase + separators),
    PC_PRINTABLE: set(string.printable)
}

PASSWORD_CHARSET_NAMES = (
    (PC_ALPHA_LOWER, "Alphabetical, lowercase (a-z)"),
    (PC_ALPHA_UPPER, "Alphabetical, uppercase (A-Z)"),
    (PC_ALPHA, "Alphabetical (a-z, A-Z)"),
    (PC_ALPHA_NUMERIC, "Alphabetical and numeric (a-z, A-Z, 0-9)"),
    (PC_NUMERIC, "Numeric (0-9)"),
    (PC_ALPHA_LOWER_SEP, "Alphabetical, lowercase, with separator (a-z, separator)"),
    (PC_ALPHA_UPPER_SEP, "Alphabetical, uppercase, with separator (A-Z, separator)"),
    (PC_PRINTABLE, "All printable characters (a-z, A-Z, 0-9, punctuation, whitespace)"),
    (PC_DICT, "Dictionary")
)

DEFAULT_WORD_LIST = "data/default-word-list.txt"
