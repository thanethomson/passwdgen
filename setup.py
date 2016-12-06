#!/usr/bin/env python

from setuptools import setup

INSTALL_REQUIREMENTS = [
    "future==0.16.0",
    "pyperclip==1.5.27"
]

setup(
    name="passwdgen",
    version="0.2.2",
    description="A password generation utility",
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
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ]
)
