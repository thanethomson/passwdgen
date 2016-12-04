# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
from getpass import getpass
import argparse
from utils import clean_word_list


def main():
    """Main routine for handling command line functionality for passwdgen."""

    parser = argparse.ArgumentParser(description="A password generation utility.")
    subparsers = parser.add_subparsers(help="The command to execute.", dest="command")

    parser_info = subparsers.add_parser(
        "info",
        help=(
            "Compute information about one or more passwords. If no password file is specified, it attempts to " +
            "read a password from stdin."
        )
    )
    parser_info.add_argument(
        "--password_file",
        default=None,
        help=(
            "Read passwords from a file instead of the command line (assumes a text file, one password per line, " +
            "skips newlines)."
        )
    )
    parser_info.add_argument(
        "--encoding",
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
        dest="generate_clipboard",
        help="Copy the generated password to the clipboard (only for when generating a single password)."
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
        "--encoding",
        default=None,
        help=(
            "The encoding to use when read/writing input/output files. " +
            "(See https://docs.python.org/2/library/codecs.html#standard-encodings)"
        )
    )

    args = parser.parse_args()

    if args.command == "info":
        if args.password_file is None:
            if sys.stdin.isatty():
                passwd = getpass("Please enter the password to check: ")
            else:
                # if the input's been piped in
                passwd = sys.stdin.read().strip()

    elif args.command == "generate":
        print("Should generate password(s) here")

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
