# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
from getpass import getpass
import argparse
import pyperclip

from . import __version__
from .generator import *
from .utils import *
from .constants import *


def show_password_entropy(passwd, word_list):
    """Displays the password entropy calculation results."""
    entropy = calculate_entropy(passwd, dict_set=word_list)
    print("\nPassword length: %d characters" % len(passwd))
    print("\nEntropy")
    print("-------")
    for charset, charset_name in list(PASSWORD_CHARSET_NAMES):
        print(("{:<%d}" % LONGEST_CHARSET_NAME_LEN).format(charset_name) + " : " +
              (("%.6f" % entropy[charset]) if charset in entropy else "not in character set"))
    print("")


def main():
    """Main routine for handling command line functionality for passwdgen."""

    parser = argparse.ArgumentParser(description="A password generation utility (v%s)." % __version__)
    subparsers = parser.add_subparsers(help="The command to execute.", dest="command")

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Display the version of passwdgen."
    )

    parser_info = subparsers.add_parser(
        "info",
        help=(
            "Compute information about a password. If passwdgen has input piped into it via stdin, that " +
            "will be interpreted as the password."
        )
    )
    parser_info.add_argument(
        "-d", "--dictionary",
        default=None,
        help="Path to the dictionary file to use. This must be a plain text file with one word per line."
    )
    parser_info.add_argument(
        "-e", "--encoding",
        default=None,
        help=(
            "The encoding to use when read/writing input/output files. " +
            "(See https://docs.python.org/2/library/codecs.html#standard-encodings)"
        )
    )

    parser_generate = subparsers.add_parser(
        "generate",
        help="Generate password(s)."
    )
    parser_generate.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help=(
            "Copy the generated password to the clipboard (only for when generating a single password) instead of "+
            "writing the password to stdout"
        )
    )
    parser_generate.add_argument(
        "-d", "--dictionary",
        default=None,
        help="Path to the dictionary file to use. This must be a plain text file with one word per line."
    )
    parser_generate.add_argument(
        "-e", "--encoding",
        default=None,
        help=(
            "The encoding to use when read/writing input/output files. " +
            "(See https://docs.python.org/2/library/codecs.html#standard-encodings)"
        )
    )
    parser_generate.add_argument(
        "-i", "--info",
        action="store_true",
        help="Additionally display information about the generated password, including password entropy."
    )
    parser_generate.add_argument(
        "-l", "--length",
        type=int,
        default=None,
        help=(
            "The default number of characters or words to generate, depending on which kind of password " +
            "is being generated (a character- or dictionary-based one). Defaults: %d characters or %d words."
        ) % (DEFAULT_CHAR_PASSWORD_LENGTH, DEFAULT_WORD_PASSWORD_WORDS)
    )
    parser_generate.add_argument(
        "-m", "--min-entropy",
        default=None,
        type=int,
        help="The minimum entropy of the required password (optional). If length is specified, this will be ignored."
    )
    parser_generate.add_argument(
        "-s", "--separator",
        choices=PASSWORD_SEPARATOR_IDS,
        default=SEP_DASH,
        help=(
            "The separator to use when generating passwords from dictionaries (default=%s)."
        ) % SEP_DASH
    )
    parser_generate.add_argument(
        "--starting-letters",
        default=None,
        help=(
            "The letters to use as initials for the generated words."
        )
    )
    parser_generate.add_argument(
        "-t", "--charset",
        choices=PASSWORD_CHARSET_IDS,
        default=PC_DICT,
        help=(
                 "Which character set/approach to use when generating the password (default=\"%s\"). See the " +
                 "README.md file at https://github.com/thanethomson/passwdgen for more details."
             ) % PC_DICT
    )

    parser_rng = subparsers.add_parser(
        "rng",
        help="Test the quality of the operating system's random number generator."
    )
    parser_rng.add_argument(
        "-s", "--sample-size",
        type=int,
        default=1000000,
        help="Define the sample size to test with (default = 1,000,000)."
    )

    parser_wordlist = subparsers.add_parser(
        "wordlist",
        help="Utilities relating to word list manipulation."
    )
    subparsers_wordlist = parser_wordlist.add_subparsers(dest="wordlist_subcommand")

    parser_wordlist_clean = subparsers_wordlist.add_parser(
        "clean",
        help="Cleans up a given word list, stripping punctuation, digits and whitespace."
    )
    parser_wordlist_clean.add_argument(
        "input_file",
        help="The input text file, one word per line, to be cleaned."
    )
    parser_wordlist_clean.add_argument(
        "output_file",
        help="The output file into which to write the cleaned word list."
    )
    parser_wordlist_clean.add_argument(
        "-e", "--encoding",
        default=None,
        help=(
            "The encoding to use when read/writing input/output files. " +
            "(See https://docs.python.org/2/library/codecs.html#standard-encodings)"
        )
    )

    args = parser.parse_args()

    if args.version:
        print("passwdgen v%s" % __version__)

    elif args.command == "info":
        if sys.stdin.isatty():
            passwd = getpass("Please enter the password to check: ")
        else:
            # if the input's been piped in
            passwd = sys.stdin.read()
            # strip off the single trailing newline
            if passwd.endswith("\n"):
                passwd = passwd[:-1]

        word_list = load_word_list(filename=args.dictionary, encoding=args.encoding)
        show_password_entropy(passwd, word_list)

    elif args.command == "rng":
        print("Testing OS RNG. Attempting to generate %d samples between 0 and 100 (inclusive). Please wait..." % args.sample_size)
        result = secure_random_quality(args.sample_size)
        print("\nStatistics")
        print("----------")
        print("Mean               : %.6f (should approach %.3f as the sample size increases; %.3f%% difference)" % (
            result['mean'],
            result['expected_mean'],
            result['mean_diff']
        ))
        print("Standard deviation : %.6f (should be as close to %.6f as possible; %.3f%% difference)" % (
            result['stddev'],
            result['expected_stddev'],
            result['stddev_diff']
        ))
        print("Time taken         : %.3f seconds\n" % result['time'])

    elif args.command == "generate":
        try:
            word_list = load_word_list(filename=args.dictionary, encoding=args.encoding)

            # dictionary-based password generation
            if args.charset == PC_DICT:
                # load our dictionary
                passwd = words(
                    word_list,
                    separator=PASSWORD_SEPARATORS[args.separator],
                    word_count=args.length,
                    min_entropy=args.min_entropy,
                    starting_letters=args.starting_letters
                )
            else:
                passwd = chars(
                    args.charset,
                    length=args.length,
                    min_entropy=args.min_entropy
                )

            if args.clipboard:
                pyperclip.copy(passwd)
                print("Password copied to clipboard.")
            else:
                print(passwd)

            if args.info:
                show_password_entropy(passwd, word_list)

        except ValueError as e:
            print("Error: %s" % e)

    elif args.command == "wordlist":
        if args.wordlist_subcommand == "clean":
            print("Attempting to clean word list: %s" % args.input_file)
            result = clean_word_list(
                args.input_file,
                args.output_file,
                encoding=args.encoding
            )
            print("Cleaned file in %.3f seconds. Read %d words, wrote %d." % (
                result["time"],
                result["words_read"],
                result["words_written"]
            ))
