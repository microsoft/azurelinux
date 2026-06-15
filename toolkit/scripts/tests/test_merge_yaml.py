#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import unittest

# Ensure the scripts directory is on sys.path so we can import merge_yaml
CURRENT_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from merge_yaml import deep_merge


class TestDeepMerge(unittest.TestCase):
    def test_merge_scalars(self):
        self.assertEqual(deep_merge(1, 2), 2)
        self.assertEqual(deep_merge("a", "b"), "b")

    def test_merge_lists_append(self):
        self.assertEqual(deep_merge([1, 2], [3, 4]), [1, 2, 3, 4])
        self.assertEqual(deep_merge([], [1]), [1])

    def test_merge_dicts_recursive(self):
        base = {"a": 1, "b": {"x": 1, "y": 2}, "c": [1, 2]}
        delta = {"b": {"y": 3, "z": 4}, "c": [3], "d": 5}
        expected = {"a": 1, "b": {"x": 1, "y": 3, "z": 4}, "c": [1, 2, 3], "d": 5}
        self.assertEqual(deep_merge(base, delta), expected)

    def test_merge_mismatched_types(self):
        self.assertEqual(deep_merge({"a": 1}, [1, 2]), [1, 2])
        self.assertEqual(deep_merge([1, 2], {"a": 1}), {"a": 1})


if __name__ == "__main__":
    unittest.main()
