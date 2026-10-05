"""Unit tests for pyproject_getopt.lua option parsing.

Most tests are written in Lua (test_pyproject_getopt.lua) and run via
parametrized test_lua. Tests that need to inspect stderr for error
messages or define real RPM parametric macros stay in Python.
"""

import os
import subprocess
import textwrap
from pathlib import Path

import pytest

BASEDIR = Path(__file__).parent


def rpmlua(script):
    """Run a Lua script via rpm --eval, return (stdout, stderr, returncode)."""
    full_script = textwrap.dedent(f"""\
        package.path = "{BASEDIR}/?.lua"
    """) + textwrap.dedent(script)
    r = subprocess.run(
        # ["rpmlua", "-e", full_script] when we no longer support c9s
        ["rpm", "--eval", "%{lua:" + full_script + "}"],
        capture_output=True, text=True,
        env={**os.environ, "LANG": "C.UTF-8"},
    )
    return r.stdout, r.stderr, r.returncode


def _get_lua_test_names():
    stdout, stderr, rc = rpmlua("""\
        local t = require("test_pyproject_getopt")
        for _, name in ipairs(t.list()) do
            io.write(name .. "\\n")
        end
    """)
    assert rc == 0, f"Failed to list Lua tests:\n{stderr}"
    names = stdout.strip().splitlines()
    assert names, "No Lua tests found"
    return names


@pytest.mark.parametrize("lua_test_name", _get_lua_test_names())
def test_lua(lua_test_name):
    stdout, stderr, rc = rpmlua(f"""\
        local t = require("test_pyproject_getopt")
        t.{lua_test_name}()
    """)
    if rc != 0:
        raise AssertionError(stderr)
    if stdout.startswith("SKIP: "):
        pytest.skip(stdout.removeprefix("SKIP: ").strip())


class TestErrorMessages:
    """Verify that error messages contain expected text (via stderr).

    These call raw_* functions from the Lua test module which invoke
    getopt() without pcall, so the RPM error propagates to stderr.
    """

    def _run_raw(self, name):
        _, stderr, rc = rpmlua(f"require('test_pyproject_getopt').{name}()")
        assert rc != 0, "expected an error"
        return stderr

    def test_unknown_option_message(self):
        stderr = self._run_raw("raw_unknown_short_option")
        assert "unknown option: -z" in stderr

    def test_unknown_long_option_message(self):
        stderr = self._run_raw("raw_unknown_long_option")
        assert "unknown option: --bogus" in stderr

    def test_missing_value_message(self):
        stderr = self._run_raw("raw_missing_value_short")
        assert "requires a value" in stderr

    def test_flag_given_value_message(self):
        stderr = self._run_raw("raw_flag_given_value")
        assert "does not take a value" in stderr

    def test_mutual_exclusion_message(self):
        stderr = self._run_raw("raw_R_and_x")
        assert "mutually exclusive" in stderr
        assert "--no-runtime" in stderr
        assert "--extras" in stderr

    def test_repeated_without_separator_message(self):
        stderr = self._run_raw("raw_repeated_without_separator")
        assert "cannot be repeated" in stderr

    def test_macro_rejects_unknown_option_message(self):
        stderr = self._run_raw("raw_macro_rejects_unknown_option")
        assert "%_test_macro" in stderr
        assert "unknown option: --bogus" in stderr
