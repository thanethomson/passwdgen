# Changelog for `passwdgen`

## `v0.4.0` - 29 April 2023

* Packaging/build system rework, linting. Special thanks to @joelsgp for this!
  ([\#1](https://github.com/thanethomson/passwdgen/pull/1))

## `v0.3.1` - 04 November 2019

* Fix README for PyPI so it shows up

## `v0.3.0` - 04 November 2019

* Remove Python 2 support
* Restrict special characters to those [supported by
  AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)

## `v0.2.2` - 06 December 2016

* Another attempt to fix `builtins` import issue in Python 2.7.

## `v0.2.1` - 06 December 2016

* Fixing minor issue with setup in Python 2.7 (depending on the
  `builtins` library, which is not available by default in Python 2).


## `v0.2.0` - 06 December 2016

* Added feature to allow one to generate passwords based on


## `v0.1.2` - 06 December 2016

* Renamed password generation functions from `generate_password_chars`
  and `generate_password_words` to simply `chars` and `words`.
  Simplifies API.
* Added more documentation around password entropy selection.


## `v0.1.1` - 05 December 2016

* Fixing statistical calculation for `rng` command.


## `v0.1.0` - 05 December 2016

* First alpha release.
