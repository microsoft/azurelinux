libkkc - Japanese Kana Kanji conversion library
======
[![Build Status](https://travis-ci.org/ueno/libkkc.svg?branch=master)](https://travis-ci.org/ueno/libkkc) [![Coverage Status](https://img.shields.io/coveralls/ueno/libkkc.svg)](https://coveralls.io/r/ueno/libkkc)

What's this?
------

libkkc provides a converter from Kana-string to
Kana-Kanji-mixed-string.  It was named after kkc.el in GNU Emacs, a
simple Kana Kanji converter, while libkkc tries to convert sentences
in a bit more complex way using N-gram language models.

Install
------

1. compile and install [marisa-trie](https://code.google.com/p/marisa-trie/)

2. compile and install

```
$ ./autogen.sh
$ make
$ make install
```

3. run kkc program

```
$ kkc
Type kana sentence in the following form:
SENTENCE [N-BEST [SEGMENT-BOUNDARY...]]

>> わたしのなまえはなかのです
0: <わたし/わたし><の/の><名前/なまえ><は/は><中野/なかの><で/で><す/す>

# get 3 matches instead of 1
>> わたしのなまえはなかのです 3
0: <わたし/わたし><の/の><名前/なまえ><は/は><中野/なかの><で/で><す/す>
1: <私/わたし><の/の><名前/なまえ><は/は><中野/なかの><で/で><す/す>
2: <わたし/わたし><の/の><名前/なまえ><は/は><中野/なかの><デス/です>

# enlarge the second segment (の -> のな)
>> わたしのなまえはなかのです 1 3 5
0: <わたし/わたし><のな/のな><前/まえ><は/は><中野/なかの><で/で><す/す>

# shrink the fourth segment (なかの -> なか)
>> わたしのなまえはなかのです 1 3 4 7 8 10
0: <わたし/わたし><の/の><名前/なまえ><は/は><中/なか><の/の><で/で><す/す>
```

License
------
```
GPLv3+

Copyright (C) 2011-2014 Daiki Ueno <ueno@gnu.org>
Copyright (C) 2011-2014 Red Hat, Inc.

This file is free software; as a special exception the author gives
unlimited permission to copy and/or distribute it, with or without
modifications, as long as this notice is preserved.

This file is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```