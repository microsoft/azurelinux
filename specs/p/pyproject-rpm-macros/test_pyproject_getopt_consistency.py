"""Assert that short/long option mappings are consistent across
macros.pyproject, Python argparse scripts, and README.md."""

import argparse
import importlib
import re
from pathlib import Path

import pytest

BASEDIR = Path(__file__).parent

# Macros with corresponding Python scripts
MACROS_PYTHON = (
    "pyproject_buildrequires",
    "pyproject_save_files",
    "pyproject_wheel",
)

# Macros that appear in the README reference table
MACROS_README = (
    "pyproject_buildrequires",
    "pyproject_check_import",
    "pyproject_extras_subpkg",
    "pyproject_save_files",
    "pyproject_wheel",
    "tox",
)


def parse_macros_file():
    """Extract {macro_name: set((short, long), ...)} from macros.pyproject."""
    text = (BASEDIR / "macros.pyproject").read_text()
    result = {}

    # Match .getopt({ specs })
    # The macro name comes from the %macro_name(-) definition line above the call
    prev_end = 0
    for m in re.finditer(r"\.getopt\(", text):
        start = m.end()
        # Find the macro name from the nearest preceding %name(-) line
        preceding = text[prev_end:m.start()]
        macro_name = re.findall(r"^%(\w+)\(-\)", preceding, re.MULTILINE)[-1]
        prev_end = m.end()
        # Find the opt_spec table (first argument)
        brace_start = text.index("{", start)
        depth = 0
        pos = brace_start
        while pos < len(text):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    break
            pos += 1
        spec_text = text[brace_start : pos + 1]
        opts = set()
        for opt_m in re.finditer(
            r'short\s*=\s*"([^"]+)"\s*,\s*long\s*=\s*"([^"]+)"', spec_text
        ):
            opts.add((opt_m.group(1), opt_m.group(2)))
        result[macro_name] = opts

    return result


def parse_python_script(module_name):
    """Extract set((short, long), ...) from a module's argparser().

    Only returns options that have both a short (-X) and long (--Y) form,
    which are the user-facing options.
    """
    module = importlib.import_module(module_name)
    parser = module.argparser()
    opts = set()
    for action in parser._actions:  # this is quite stable private API
        if isinstance(action, argparse._HelpAction):
            continue
        strings = action.option_strings
        if len(strings) == 2 and strings[0].startswith("-") and not strings[0].startswith("--"):
            short = strings[0][1:]  # strip the -
            long = strings[1][2:]  # strip the --
            opts.add((short, long))
    return opts


def parse_readme():
    """Extract {macro_name: set((short, long), ...)} from README tables."""
    text = (BASEDIR / "README.md").read_text()
    result = {}

    current_macro = None
    in_table = False

    for line in text.splitlines():
        # Detect ### `%macro_name` headings
        if heading_m := re.match(r"^### `%(\w+)`", line):
            current_macro = heading_m.group(1)
            in_table = False
            continue

        if current_macro is None:
            continue

        # Detect table rows (skip header and separator)
        if re.match(r"^\|[-\s|]+\|$", line):
            in_table = True
            continue

        if not line.startswith("|"):
            if in_table:
                # Left the table
                current_macro = None
                in_table = False
            continue

        if not in_table:
            # This is the header row
            if "Short" in line and "Long" in line:
                in_table = False  # next line will be separator
            continue

        # Parse table data row: | `-x EXTRAS` | `--extras EXTRAS` | ... |
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 4:
            continue

        short_col = cols[1]  # e.g. "`-x EXTRAS`"
        long_col = cols[2]  # e.g. "`--extras EXTRAS`"

        short_m = re.match(r"`-(\w)", short_col)
        long_m = re.match(r"`--([\w-]+)", long_col)

        if short_m and long_m:
            short = short_m.group(1)
            long = long_m.group(1)
            if current_macro not in result:
                result[current_macro] = set()
            result[current_macro].add((short, long))

    return result


@pytest.fixture(scope="module")
def macro_opts():
    return parse_macros_file()


@pytest.fixture(scope="module")
def readme_opts():
    return parse_readme()


@pytest.mark.parametrize("macro_name", MACROS_PYTHON)
def test_macro_options_match_python(macro_opts, macro_name):
    python_opts = parse_python_script(macro_name)
    macro_set = macro_opts[macro_name]
    assert macro_set
    assert macro_set == python_opts


@pytest.mark.parametrize("macro_name", MACROS_README)
def test_macro_options_match_readme(macro_opts, readme_opts, macro_name):
    macro_set = macro_opts[macro_name]
    readme_set = readme_opts.get(macro_name, set())
    assert macro_set
    assert macro_set == readme_set
