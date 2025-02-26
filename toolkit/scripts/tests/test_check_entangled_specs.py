#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import unittest
from unittest.mock import patch, MagicMock
import check_entangled_specs

# Enable verbose output to make debugging easier
check_entangled_specs.verbose = True

class TestCheckSpecTags(unittest.TestCase):

    @patch('check_entangled_specs.Spec.from_file')
    @patch('check_entangled_specs.get_tag_value')
    def test_check_spec_tags_no_errors(self, mock_get_tag_value, mock_from_file):
        mock_get_tag_value.side_effect = ["v1", "r1", "v1", "r1",
                                          "v1.1", "r1.1", "v1.1", "r1.1"]
        mock_from_file.return_value = MagicMock()

        base_path = "/fake/path"
        tags = ["version", "release"]
        groups = [frozenset(["spec1.spec", "spec2.spec"]),
                  frozenset(["spec3.spec", "spec4.spec"])]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertFalse(result)

    @patch('check_entangled_specs.Spec.from_file')
    @patch('check_entangled_specs.get_tag_value')
    def test_check_spec_tags_with_errors(self, mock_get_tag_value, mock_from_file):
        mock_get_tag_value.side_effect = ["v2", "r2", "v2.1", "r2.1"]
        mock_from_file.return_value = MagicMock()

        base_path = "/fake/path"
        tags = ["version", "release"]
        groups = [frozenset(["spec5.spec", "spec6.spec"])]

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups)
        self.assertTrue(result)

    @patch('check_entangled_specs.Spec.from_file')
    @patch('check_entangled_specs.get_tag_value')
    def test_check_spec_tags_with_expected_value(self, mock_get_tag_value, mock_from_file):
        mock_get_tag_value.side_effect = ["v3","v3"]
        mock_from_file.return_value = MagicMock()

        base_path = "/fake/path"
        tags = ["version"]
        groups = [frozenset(["spec7.spec", "spec8.spec"])]
        tag_expected_value = {"version":"v3"}

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups, tag_expected_value)
        self.assertFalse(result)

    @patch('check_entangled_specs.Spec.from_file')
    @patch('check_entangled_specs.get_tag_value')
    def test_check_spec_tags_with_mismatched_expected_value(self, mock_get_tag_value, mock_from_file):
        mock_get_tag_value.side_effect = ["v4","v4"]
        mock_from_file.return_value = MagicMock()

        base_path = "/fake/path"
        tags = ["version"]
        groups = [frozenset(["spec1.spec", "spec2.spec"])]
        tag_expected_value = {"version":"v5"}

        result = check_entangled_specs.check_spec_tags(base_path, tags, groups, tag_expected_value)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
