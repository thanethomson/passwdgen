# -*- coding: utf-8 -*-

import string

__all__ = [
    "PC_ALPHA_LOWER",
    "PC_ALPHA_UPPER",
    "PC_ALPHA",
    "PC_ALPHA_NUMERIC",
    "PC_NUMERIC",
    "PC_ALPHA_LOWER_SEP",
    "PC_ALPHA_UPPER_SEP",
    "PC_SPECIAL",
    "PC_DICT",
    "PASSWORD_CHARSETS",
    "separators",
    "SEP_NONE",
    "SEP_DASH",
    "SEP_UNDERSCORE",
    "SEP_PERIOD",
    "SEP_SPACE",
    "SEP_COMMA",
    "SEP_SEMICOLON",
    "SEP_COLON",
    "PASSWORD_SEPARATORS",
    "PASSWORD_SEPARATOR_IDS",
    "PASSWORD_CHARSET_NAMES",
    "PASSWORD_CHARSET_IDS",
    "LONGEST_CHARSET_NAME_LEN",
    "DEFAULT_WORD_LIST",
    "DEFAULT_CHAR_PASSWORD_LENGTH",
    "DEFAULT_WORD_PASSWORD_WORDS",
    "DEFAULT_MIN_WORD_LEN",
    "MIN_DICT_SIZE",
    "DEFAULT_WORD_SEPARATOR"
]

PC_ALPHA_LOWER = "alpha-lower"
PC_ALPHA_UPPER = "alpha-upper"
PC_ALPHA = "alpha"
PC_ALPHA_NUMERIC = "alpha-numeric"
PC_ALPHA_NUMERIC_SPACED = "alpha-numeric-spaced"
PC_NUMERIC = "numeric"
PC_ALPHA_LOWER_SEP = "alpha-lower-sep"
PC_ALPHA_UPPER_SEP = "alpha-upper-sep"
PC_SPECIAL = "special"
PC_DICT = "dict"

separators = "-_. ,;:"

# Use special characters from AWS password requirements:
# https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html
special_chars = "!@#$%^&*()_+-=[]{}|'"

SEP_NONE = "none"
SEP_DASH = "dash"
SEP_UNDERSCORE = "und"
SEP_PERIOD = "period"
SEP_SPACE = "space"
SEP_COMMA = "comma"
SEP_SEMICOLON = "semi"
SEP_COLON = "colon"

PASSWORD_SEPARATORS = {
    SEP_NONE: "",
    SEP_DASH: "-",
    SEP_UNDERSCORE: "_",
    SEP_PERIOD: ".",
    SEP_SPACE: " ",
    SEP_COMMA: ",",
    SEP_SEMICOLON: ";",
    SEP_COLON: ":"
}

PASSWORD_SEPARATOR_IDS = [
    SEP_NONE,
    SEP_DASH,
    SEP_UNDERSCORE,
    SEP_PERIOD,
    SEP_SPACE,
    SEP_COMMA,
    SEP_SEMICOLON,
    SEP_COLON
]

PASSWORD_CHARSETS = {
    PC_ALPHA_LOWER: set(string.ascii_lowercase),
    PC_ALPHA_UPPER: set(string.ascii_uppercase),
    PC_ALPHA: set(string.ascii_letters),
    PC_ALPHA_NUMERIC: set(string.ascii_letters + string.digits),
    PC_ALPHA_NUMERIC_SPACED: set(string.ascii_letters + string.digits + " "),
    PC_ALPHA_LOWER_SEP: set(string.ascii_lowercase + separators),
    PC_ALPHA_UPPER_SEP: set(string.ascii_uppercase + separators),
    PC_SPECIAL: set(string.ascii_letters + string.digits + special_chars),
    PC_NUMERIC: set(string.digits)
}

PASSWORD_CHARSET_NAMES = (
    (PC_ALPHA_LOWER, "Alphabetical, lowercase (a-z)"),
    (PC_ALPHA_UPPER, "Alphabetical, uppercase (A-Z)"),
    (PC_ALPHA, "Alphabetical (a-z, A-Z)"),
    (PC_ALPHA_NUMERIC, "Alphabetical and numeric (a-z, A-Z, 0-9)"),
    (PC_ALPHA_NUMERIC_SPACED, "Alphabetical, numeric, with spaces (a-z, A-Z, 0-9, space)"),
    (PC_NUMERIC, "Numeric (0-9)"),
    (PC_ALPHA_LOWER_SEP, "Alphabetical, lowercase, with separator (a-z, separator)"),
    (PC_ALPHA_UPPER_SEP, "Alphabetical, uppercase, with separator (A-Z, separator)"),
    (PC_SPECIAL, "Alphabetical, numeric and special characters (a-z, A-Z, 0-9, punctuation)"),
    (PC_DICT, "Dictionary")
)

PASSWORD_CHARSET_IDS = [id for id, _ in PASSWORD_CHARSET_NAMES]
LONGEST_CHARSET_NAME_LEN = max([len(name) for _, name in list(PASSWORD_CHARSET_NAMES)])

DEFAULT_CHARSET = PC_SPECIAL
DEFAULT_WORD_LIST = "data/default-word-list.txt"
DEFAULT_CHAR_PASSWORD_LENGTH = 12
DEFAULT_WORD_PASSWORD_WORDS = 4
DEFAULT_WORD_SEPARATOR = "-"
DEFAULT_MIN_WORD_LEN = 3

# minimum number of words in a dictionary
MIN_DICT_SIZE = 100
