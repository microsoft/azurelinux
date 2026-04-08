#!/usr/bin/python3
#
# This script turns localedata/SUPPORTED (whose path is passed as the
# first argument) into a normalized list of LANGUAGE "_" REGION pairs.
# (If there is no REGION defined, only LANGUAGE is used.)  The list
# is written to standard output, with one element per line.

import sys

supported, = sys.argv[1:]

# Pairs seen so far.  Used to suppress duplicates.
seen = set()
with open(supported) as inp:
    for line in inp:
        if line.startswith("#") or line == "SUPPORTED-LOCALES=\\\n":
            # Comment or prefix.
            continue
        if not line.endswith(" \\\n"):
            raise IOError("line without continuation: " + repr(line))
        try:
            slash = line.index("/")
        except ValueError:
            raise IOError("line without slash: " + repr(line))
        spec = line[:slash]
        for separator in ".@":
            try:
                # Strip charset, variant specifiers.
                spec = spec[:spec.index(separator)]
            except ValueError:
                pass
        seen.add(spec)

# The C locale does not correspond to a language.
seen.remove("C")

# The glibc source file is not sorted.
for spec in sorted(seen):
    print(spec)
print() # The Lua generator produces a trailing newline.
