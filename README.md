# passwdgen

## Overview
`passwdgen` is a simple password generation utility with a couple of
powerful extra features (including password entropy calculation and
entropy-based password generation).


## Installation
To use `passwdgen`, you will need to install either Python 2.7+ or
Python 3.5+.

```bash
> pip install passwdgen
```


## Entropy
Entropy, in the context of information theory, provides a convenient
way to quantify the amount of information in a particular set of
data. With regard to password strength, the higher the entropy of
a password, the more difficult it is for an attacker to guess.

From the perspective of the generator, the password strength is measured
by way of the information source. From the perspective of an attacker,
the more information is known about the information source that
generated the password (e.g. the kind of random number generator used,
the character set to which the password belongs), the lower the entropy
of that password.

### Secure random number generation
Entropy calculations are based on the assumption that the random number
source is of *good quality* (see [CSPRNG](https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator))
and generates [uniformly distributed](https://en.wikipedia.org/wiki/Discrete_uniform_distribution)
random numbers. The random number generator (RNG) used in `passwd`
is provided by the `os.urandom()` function, which uses `/dev/urandom`
on POSIX systems and `CryptGenRandom()` on Windows systems.

### Character-based calculation
This password generator uses the following definition for entropy: a
single character `c` from a character set of size `n` characters has
an entropy of `log2(n)` bits (per character). Entropy adds up as the
length of the password increases, i.e. two characters from the character
set of size `n` will have a combined overall entropy of `2 x log2(n)`.

For example, if the lowercase alphabet `a..z` is used as the character
set, it has `n=26`. Each character would have an entropy of
`log2(26) = 4.700439718141093` bits per character. A password string,
therefore, such as `mysuperweakpassword` of length 19 characters, will
have a total entropy of `19 x log2(26) = 89.31` bits.

As the size of the character set increases, so does the entropy of the
password of a certain length, as an attacker attempting a brute force
attack would have to search a much larger set of possibilities to
find the password.

### Dictionary-based calculation
The dictionary-based method of entropy calculation assumes that an
attacker has prior knowledge that the password was generated using a
dictionary of words, and even knows which dictionary was used. This
would obviously be the case if you personally used `passwdgen` to
generate a dictionary-based password, as all the code and the dictionary
are out in the open.

In this case, instead of assuming a character set (which would mean
a far higher entropy in passwords with 2 or more words), a
dictionary-based attack could be performed much quicker.

For example, the password `dog-far-nightly-can` is 19 characters long
and makes use of the lowercase alphabet and hyphens (resulting in a
character set of 27 possible characters). This means that a
brute force attacker using the full lowercase alphabet and hyphens
would be faced with a potential password entropy of
`19 x log2(27) = 90.34` bits.

If, however, the attacker knows that the password is dictionary-based
and that the words are separated by hyphens, the attacker would only
have to guess the 4 words from the dictionary making up the password.
This results in a potential entropy from the perspective of the
attacker of `4 x log2(275,185) = 72.28` bits (assuming dictionary
size of 275,185 words). This is still a pretty strong password, but
it is still easier to crack than a password where the attacker does not
know that it is dictionary-based.


## Dictionary
The included dictionary is a "cleaned out" (see the `wordlist clean`
command provided by `passwdgen`) version of a dictionary created
through [SCOWL (And Friends)](http://wordlist.aspell.net/), using their
[word list generator](http://app.aspell.net/create).

At present, the embedded dictionary contains **71,188** words, ensuring
an entropy of `log2(71,188) = 16.119` bits per word.

### Legal
Copyright 2000-2014 by Kevin Atkinson

> Permission to use, copy, modify, distribute and sell these word
> lists, the associated scripts, the output created from the scripts,
> and its documentation for any purpose is hereby granted without fee,
> provided that the above copyright notice appears in all copies and
> that both that copyright notice and this permission notice appear in
> supporting documentation. Kevin Atkinson makes no representations
> about the suitability of this array for any purpose. It is provided
> "as is" without express or implied warranty.

Copyright (c) J Ross Beresford 1993-1999. All Rights Reserved.

> The following restriction is placed on the use of this publication:
> if The UK Advanced Cryptics Dictionary is used in a software package
> or redistributed in any form, the copyright notice must be
> prominently displayed and the text of this document must be included
> verbatim.
>
> There are no other restrictions: I would like to see the list
> distributed as widely as possible.

Many sources were used in the creation of SCOWL, most of them were in
the public domain or used indirectly.  For a full list please see the
SCOWL readme.

[http://wordlist.aspell.net/](http://wordlist.aspell.net/)


## References
The following sources were consulted in building the password generator:

* [Entropy (information theory) ~ Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))
* [How should I calculate the entropy of a password? ~ Cryptography StackExchange](http://crypto.stackexchange.com/questions/374/how-should-i-calculate-the-entropy-of-a-password)
* [How to calculate password entropy](https://ritcyberselfdefense.wordpress.com/2011/09/24/how-to-calculate-password-entropy/)
* [Permutation ~ Wikipedia](https://en.wikipedia.org/wiki/Permutation)


## License
**The MIT License (MIT)**

Copyright (c) 2016 Thane Thomson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
