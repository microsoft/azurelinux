#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import unittest
from unittest.mock import patch, MagicMock
import check_entangled_specs

# Enable verbose output to make debugging easier
check_entangled_specs.verbose = True

class TestCheckSpecTags(unittest.TestCase):

    @patch('check_entangled_specs.read_spec_tag')
    def test_check_spec_tags_no_errors(self, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = [
            "v1", "r1", "v1", "r1",
            "v1.1", "r1.1", "v1.1", "r1.1",
        ]

        base_path = "/fake/path"
        tags = {"version": {}, "release": {}}
        groups = [
            frozenset(["spec1.spec", "spec2.spec"]),
            frozenset(["spec3.spec", "spec4.spec"]),
        ]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertFalse(result)

    @patch('check_entangled_specs.read_spec_tag')
    def test_check_spec_tags_with_errors(self, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = ["v2", "r2", "v2.1", "r2.1"]

        base_path = "/fake/path"
        tags = {"version": "", "release": ""}
        groups = [frozenset(["spec5.spec", "spec6.spec"])]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertTrue(result)

    @patch('check_entangled_specs.read_spec_tag')
    def test_check_spec_tags_with_expected_value(self, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = ["v3", "v3"]

        base_path = "/fake/path"
        tags = {"version": "v3"}
        groups = [frozenset(["spec7.spec", "spec8.spec"])]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertFalse(result)

    @patch('check_entangled_specs.read_spec_tag')
    def test_check_spec_tags_with_mismatched_expected_value(self, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = ["v4", "v4"]

        base_path = "/fake/path"
        tags = {"version": "v5"}
        groups = [frozenset(["spec1.spec", "spec2.spec"])]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertTrue(result)

class TestCheckMatches(unittest.TestCase):

    @patch('check_entangled_specs.read_spec_tag')
    @patch('check_entangled_specs.check_spec_tags')
    @patch('sys.exit')
    def test_check_matches_no_errors(self, mock_exit, mock_check_spec_tags, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = ["1.0", "1"]
        mock_check_spec_tags.side_effect = [False, False, False, False]

        base_path = "/fake/path"
        check_entangled_specs.check_matches(base_path)
        mock_exit.assert_not_called()

    @patch('check_entangled_specs.read_spec_tag')
    @patch('check_entangled_specs.check_spec_tags')
    @patch('sys.exit')
    def test_check_matches_with_errors(self, mock_exit, mock_check_spec_tags, mock_read_spec_tag):
        mock_read_spec_tag.side_effect = ["1.0", "1"]
        mock_check_spec_tags.side_effect = [False, False, True, False]

        base_path = "/fake/path"
        check_entangled_specs.check_matches(base_path)
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
