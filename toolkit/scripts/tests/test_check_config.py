#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import unittest
from io import StringIO
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch

from kernel_config_checker.check_config import (
    check_kernel_config,
    parse_kernel_config,
)
from kernel_config_checker.schema.schema import (
    ArchConfigPair,
    Architecture,
    IntentionalKernelConfigSchema,
    KernelConfig,
    KernelConfigValue,
    KernelObject,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _make_schema(default_configs=None, overrides=None):
    """Build an IntentionalKernelConfigSchema from simple lists."""
    return IntentionalKernelConfigSchema(
        default=KernelObject(
            name="default",
            kernel_configs=default_configs or [],
        ),
        overrides=overrides or [],
    )


def _kc(name, arch, value, justification="test"):
    """Shorthand to create a single-arch KernelConfig."""
    return KernelConfig(
        name=name,
        values=[ArchConfigPair(architecture=arch, value=value)],
        justification=justification,
    )


# ---------------------------------------------------------------------------
# parse_kernel_config
# ---------------------------------------------------------------------------

class TestParseKernelConfig(unittest.TestCase):

    def _parse(self, text):
        """Write *text* to a temp file and parse it."""
        tmp = Path("/tmp/_test_kernel_config")
        tmp.write_text(dedent(text))
        try:
            return parse_kernel_config(tmp)
        finally:
            tmp.unlink()

    def test_is_not_set(self):
        """'# CONFIG_FOO is not set' lines are parsed as CONFIG_FOO='n'."""
        cfg = self._parse("# CONFIG_FOO is not set\n")
        self.assertEqual(cfg, {"CONFIG_FOO": "n"})

    def test_enabled(self):
        """'CONFIG_BAR=y' is parsed as enabled."""
        cfg = self._parse("CONFIG_BAR=y\n")
        self.assertEqual(cfg, {"CONFIG_BAR": "y"})

    def test_module(self):
        """'CONFIG_BAZ=m' is parsed as module-enabled."""
        cfg = self._parse("CONFIG_BAZ=m\n")
        self.assertEqual(cfg, {"CONFIG_BAZ": "m"})

    def test_numeric_value(self):
        """Numeric values like '256' are kept as strings."""
        cfg = self._parse("CONFIG_NR_CPUS=256\n")
        self.assertEqual(cfg, {"CONFIG_NR_CPUS": "256"})

    def test_string_value(self):
        """Quoted string values preserve the surrounding quotes."""
        cfg = self._parse('CONFIG_DEFAULT_HOSTNAME="(none)"\n')
        self.assertEqual(cfg, {"CONFIG_DEFAULT_HOSTNAME": '"(none)"'})

    def test_comments_and_blanks_ignored(self):
        """Plain comments and blank lines are skipped."""
        text = """\
            #
            # General setup
            #

            CONFIG_A=y
        """
        cfg = self._parse(text)
        self.assertEqual(cfg, {"CONFIG_A": "y"})

    def test_mixed_entries(self):
        """A file mixing 'is not set', =m, and numeric lines parses correctly."""
        text = """\
            # CONFIG_X is not set
            CONFIG_Y=m
            CONFIG_Z=1024
        """
        cfg = self._parse(text)
        self.assertEqual(cfg, {"CONFIG_X": "n", "CONFIG_Y": "m", "CONFIG_Z": "1024"})

    def test_empty_file(self):
        """An empty .config file returns an empty dict."""
        cfg = self._parse("")
        self.assertEqual(cfg, {})

    def test_value_with_equals_sign(self):
        """Values containing '=' are not split incorrectly (split on first '=' only)."""
        cfg = self._parse('CONFIG_CMDLINE="root=/dev/sda1 ro"\n')
        self.assertEqual(cfg, {"CONFIG_CMDLINE": '"root=/dev/sda1 ro"'})


# ---------------------------------------------------------------------------
# check_kernel_config
# ---------------------------------------------------------------------------

class TestCheckKernelConfig(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_all_correct_returns_true(self, _stdout):
        """Returns True when all actual values match the schema defaults."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.ENABLED),
            _kc("CONFIG_B", Architecture.X86_64, KernelConfigValue.MODULE),
        ])
        actual = {"CONFIG_A": "y", "CONFIG_B": "m"}
        self.assertTrue(
            check_kernel_config(actual, schema, "kernel", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_mismatch_returns_false(self, _stdout):
        """Returns False when an actual value differs from the expected one."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.ENABLED),
        ])
        actual = {"CONFIG_A": "n"}
        self.assertFalse(
            check_kernel_config(actual, schema, "kernel", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_missing_config_treated_as_disabled(self, _stdout):
        """A config absent from the .config file defaults to 'n'."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_MISSING", Architecture.X86_64, KernelConfigValue.ENABLED),
        ])
        self.assertFalse(
            check_kernel_config({}, schema, "kernel", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_missing_config_expected_disabled_passes(self, _stdout):
        """Missing config expected to be 'n' should pass."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_GONE", Architecture.X86_64, KernelConfigValue.DISABLED),
        ])
        self.assertTrue(
            check_kernel_config({}, schema, "kernel", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_override_replaces_default(self, _stdout):
        """A kernel-specific override replaces the default expectation."""
        schema = _make_schema(
            default_configs=[
                _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.ENABLED),
            ],
            overrides=[
                KernelObject(
                    name="kernel-hvm",
                    kernel_configs=[
                        _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.DISABLED),
                    ],
                )
            ],
        )
        actual = {"CONFIG_A": "n"}
        self.assertTrue(
            check_kernel_config(actual, schema, "kernel-hvm", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_override_without_match_uses_default(self, _stdout):
        """When the kernel name doesn't match any override, defaults apply."""
        schema = _make_schema(
            default_configs=[
                _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.ENABLED),
            ],
            overrides=[
                KernelObject(
                    name="other-kernel",
                    kernel_configs=[
                        _kc("CONFIG_A", Architecture.X86_64, KernelConfigValue.DISABLED),
                    ],
                )
            ],
        )
        actual = {"CONFIG_A": "y"}
        self.assertTrue(
            check_kernel_config(actual, schema, "kernel", "x86_64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_numeric_expected_value(self, _stdout):
        """Custom string values (e.g. '256') are compared correctly."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_NR_CPUS", Architecture.ARM64, "256"),
        ])
        actual = {"CONFIG_NR_CPUS": "256"}
        self.assertTrue(
            check_kernel_config(actual, schema, "kernel", "arm64")
        )

    @patch("sys.stdout", new_callable=StringIO)
    def test_error_output_contains_config_name(self, stdout):
        """Failure output includes the name of the misconfigured option."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_BAD", Architecture.X86_64, KernelConfigValue.ENABLED),
        ])
        check_kernel_config({"CONFIG_BAD": "n"}, schema, "kernel", "x86_64")
        self.assertIn("CONFIG_BAD", stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_different_arch_configs_independent(self, _stdout):
        """Only configs matching the target architecture are checked."""
        schema = _make_schema(default_configs=[
            _kc("CONFIG_ARM_ONLY", Architecture.ARM64, KernelConfigValue.ENABLED),
        ])
        # x86_64 check should have nothing to verify, so it passes
        self.assertTrue(
            check_kernel_config({}, schema, "kernel", "x86_64")
        )


if __name__ == "__main__":
    unittest.main()
