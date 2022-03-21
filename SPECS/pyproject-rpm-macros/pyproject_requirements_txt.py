"""Best-effort parser for requirements.txt files"""

import urllib.parse
from pathlib import Path
import sys
import os
import re

# `#` starts a comment only at end of line and after whitespace
COMMENT_RE = re.compile(r'(^|\s+)#.*$')

# Assume URLs start with a scheme; don't look for "egg=" URLs otherwise
URL_START_RE = re.compile(r'^[-_+a-zA-Z0-9]+://')

ENV_VAR_RE = re.compile(r'(?P<var>\$\{(?P<name>[A-Z0-9_]+)\})')
PKGNAME_RE = re.compile(r'^[-_a-zA-Z0-9]+')

# The requirements.txt format evolved rather organically; expect weirdness.

def convert_requirements_txt(lines, path:Path = None):
    """Convert lines of a requirements file to PEP 440-style requirement strs

    This does NOT handle all of requirements.txt features (only pip can do
    that), but tries its best.

    The resulting requirements might not actually be valid (either because
    they're wrong in the file, or because we missed a special case).

    path is the path to the requirements.txt file, used for options like `-r`.
    """
    requirements = []
    lines = combine_logical_lines(lines)
    lines = strip_comments(lines)
    lines = expand_env_vars(lines)
    if path:
        filename = path.name
    else:
        filename = '<requirements file>'
    for line in lines:
        if URL_START_RE.match(line):
            # Handle URLs with "egg=..." fragments
            # see https://pip.pypa.io/en/stable/cli/pip_install/#vcs-support
            parsed_url = urllib.parse.urlparse(line)
            parsed_fragment = urllib.parse.parse_qs(parsed_url.fragment)
            if 'egg' in parsed_fragment:
                # Prepend the package name to the URL.
                match = PKGNAME_RE.match(parsed_fragment['egg'][0])
                if match:
                    pkg_name = match[0]
                    requirements.append(f'{pkg_name}@{line}')
                    continue
            # If that didn't work, pass the line on;
            # the caller will deal with invalid requirements
            requirements.append(line)
        elif line.startswith('-r'):
            recursed_path = line[2:].strip()
            if path:
                recursed_path = path.parent / recursed_path
            recursed_path = Path(recursed_path)
            with recursed_path.open() as f:
                requirements.extend(convert_requirements_txt(f, recursed_path))
        elif line.startswith('-'):
            raise ValueError(f'{filename}: unsupported requirements file option: {line}')
        else:
            requirements.append(line)
    return requirements

def combine_logical_lines(lines):
    """Combine logical lines together (backslash line-continuation)"""
    pieces = []
    for line in lines:
        line = line.rstrip('\n')
        # Whole-line comments *only* are removed before line-contionuation
        if COMMENT_RE.match(line):
            continue
        if line.endswith('\\'):
            pieces.append(line[:-1])
        else:
            # trailing whitespace is only removed from full logical lines
            pieces.append(line.rstrip())
            yield ''.join(pieces)
            pieces = []
    yield ''.join(pieces)


def strip_comments(lines):
    for line in lines:
        line, *rest = COMMENT_RE.split(line, maxsplit=1)
        line = line.strip()
        if line:
            yield line


def expand_env_vars(lines):
    def repl(match):
        value = os.getenv(match['name'])
        if value is None:
            return match['var']
        return value
    for line in lines:
        if match := ENV_VAR_RE.search(line):
            var = match['var']
        yield ENV_VAR_RE.sub(repl, line)
