#!/usr/bin/env python

from io import open
import os.path
from setuptools import setup

INSTALL_REQUIREMENTS = [
    "pyperclip==1.7.0"
]


def read_file(filename):
    full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    with open(full_path, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


setup(
    name="passwdgen",
    version="0.3.1",
    description="A password generation utility",
    long_description="".join(read_file("README.md")),
    long_description_content_type="text/markdown",
    author="Thane Thomson",
    author_email="connect@thanethomson.com",
    url="https://github.com/thanethomson/passwdgen",
    install_requires=INSTALL_REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "passwdgen = passwdgen.cmdline:main"
        ]
    },
    packages=["passwdgen"],
    package_data={
        "passwdgen": [
            "data/*.txt"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ]
)
