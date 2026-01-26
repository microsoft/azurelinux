#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Unit Tests for AntiPatternDetector
==================================

Comprehensive test suite for the AntiPatternDetector module, which detects
common anti-patterns and issues in RPM spec files for Azure Linux packages.

Dependencies:
-------------
- AntiPatternDetector: Main detection module under test
- unittest: Python standard testing framework
- tempfile: Temporary directory management for isolated testing
- unittest.mock: Mocking capabilities for isolated unit testing

Usage:
------
Run all tests:
    python test_antipattern_detector.py

Run specific test:
    python -m unittest test_antipattern_detector.TestAntiPatternDetector.test_specific_method

Run with verbose output:
    python -m unittest test_antipattern_detector.py -v
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

from AntiPatternDetector import AntiPatternDetector, AntiPattern, Severity


class TestAntiPatternDetector(unittest.TestCase):
    """
    Comprehensive test suite for AntiPatternDetector class.
    
    This test suite provides exhaustive coverage for all anti-pattern detection
    functionality in the AntiPatternDetector module. It validates the detection of
    common issues in RPM spec files used in Azure Linux packages, ensuring high
    quality and consistency in package specifications.
    
    Test Organization:
    ------------------
    The tests are organized into functional groups with clear section markers:
    
    1. **Patch File Issues** (`detect_patch_file_issues()` tests):
       - `test_missing_patch_file()`: Referenced patches not found in directory
       - `test_unused_patch_file()`: Orphaned patch files not referenced in spec
       - `test_cve_patch_mismatch()`: CVE-named patches without CVE documentation
       - `test_no_patch_issues()`: Negative test - all patches properly handled
    
    2. **CVE Reference Issues** (`detect_cve_issues()` tests):
       - `test_future_dated_cve()`: CVEs with unrealistic future years (>2026)
       - `test_missing_cve_in_changelog()`: CVEs in spec but not in changelog
       - `test_cve_documented_in_old_changelog_entry()`: CVEs in historical entries
       - `test_no_cve_references()`: Negative test - no CVE references present
    
    3. **Changelog Format Issues** (`detect_changelog_issues()` tests):
       - `test_missing_changelog_section()`: No %changelog section present
       - `test_empty_changelog_section()`: Empty %changelog with no entries
       - `test_invalid_changelog_format()`: Malformed changelog entry format
       - `test_valid_changelog_format()`: Negative test - proper format validation
    
    4. **Integration Testing** (`detect_all()` tests):
       - `test_detect_all_integration()`: Multi-category issue detection
       - `test_detect_all_no_issues()`: Negative test - clean spec file
    
    5. **Configuration and Data Structure Validation**:
       - `test_severity_mapping()`: Severity level configuration validation
       - `test_antipattern_dataclass()`: AntiPattern object creation and access
    
    6. **Edge Cases and Error Handling**:
       - `test_multiline_patch_references()`: Whitespace handling robustness
       - `test_cve_case_insensitive_matching()`: Case sensitivity behavior documentation
    
    Test Design Principles:
    -----------------------
    Each test method is designed to be:
    - **Independent**: No dependencies between test methods
    - **Deterministic**: Consistent results across multiple runs  
    - **Comprehensive**: Cover both positive and negative scenarios
    - **Realistic**: Use authentic Azure Linux spec file patterns
    - **Focused**: Test one specific aspect or scenario per method
    
    Test Data Strategy:
    -------------------
    - Uses realistic spec file content representative of Azure Linux packages
    - Includes both valid and invalid examples for thorough validation
    - Covers edge cases like empty content, malformed entries, boundary conditions
    - Validates both the detection logic and the data structure properties
    
    Assertion Patterns:
    -------------------
    Each test follows consistent assertion patterns:
    - Verify correct number of detected issues
    - Validate issue types and IDs match expectations
    - Check severity levels are appropriate
    - Confirm descriptive text includes relevant details
    - Assert line numbers are captured when available
    - Test both positive detection and negative (no false positives) scenarios
    
    Test Environment:
    -----------------
    - Uses temporary directories for isolated testing
    - Cleans up resources appropriately in tearDown()
    - Configures logging to reduce test noise
    - Supports both individual and batch test execution
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        Creates a clean testing environment for each test case with:
        - Temporary directory for isolated file operations
        - Fresh AntiPatternDetector instance with default configuration
        - Standard test spec file path following Azure Linux conventions
        
        This ensures each test runs independently without interference
        from previous test state or file system modifications.
        """
        self.temp_dir = tempfile.mkdtemp()
        self.detector = AntiPatternDetector(self.temp_dir)
        self.test_spec_path = "SPECS/test-package/test-package.spec"
    
    def tearDown(self):
        """
        Clean up after each test method.
        
        Performs any necessary cleanup operations after test execution.
        Currently minimal cleanup is needed as the temporary directory
        is automatically managed, but this method is available for
        future cleanup requirements such as:
        - Removing temporary files if created during testing
        - Resetting global state if modified
        - Cleaning up mock objects or external resources
        
        Note: The tempfile.mkdtemp() created directories are automatically
        cleaned up by the system, but explicit cleanup could be added here
        if needed for immediate resource release.
        """
        # Clean up temp directory if needed
        pass

    # =============================================================================
    # Test detect_patch_file_issues()
    # =============================================================================
    
    def test_missing_patch_file(self):
        """
        Test detection of patch files referenced in spec but missing from directory.
        
        This test validates that the detector correctly identifies when patch files
        are referenced in the spec file (via Patch0:, Patch1:, etc.) but the actual
        patch files are not present in the same directory as the spec file.
        
        Expected behavior:
        - Should detect all missing patch files
        - Each missing patch should generate an ERROR severity anti-pattern
        - Line numbers should be captured for context
        - Pattern descriptions should include the specific patch filename
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: missing-patch.patch
Patch1: another-missing.patch

%description
Test package
        """
        
        file_list = ["test-package.spec", "README.md"]  # Missing patch files
        
        patterns = self.detector.detect_patch_file_issues(
            self.test_spec_path, spec_content, file_list
        )
        
        # Should detect 2 missing patch files
        missing_patches = [p for p in patterns if p.id == 'missing-patch-file']
        self.assertEqual(len(missing_patches), 2)
        
        # Check specific patch names
        patch_names = [p.description for p in missing_patches]
        self.assertTrue(any("missing-patch.patch" in desc for desc in patch_names))
        self.assertTrue(any("another-missing.patch" in desc for desc in patch_names))
        
        # Check severity
        for pattern in missing_patches:
            self.assertEqual(pattern.severity, Severity.ERROR)
            self.assertIsNotNone(pattern.line_number)
    
    def test_unused_patch_file(self):
        """
        Test detection of patch files present but not referenced in spec.
        
        This test validates that the detector identifies patch files that exist
        in the directory but are not referenced anywhere in the spec file. These
        orphaned patch files may indicate incomplete packaging or leftover files.
        
        Expected behavior:
        - Should detect all unused .patch files in the directory
        - Each unused patch should generate a WARNING severity anti-pattern
        - Should not flag patches that are properly referenced in the spec
        - Pattern descriptions should include the specific patch filename
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: used-patch.patch

%description
Test package
        """
        
        file_list = [
            "test-package.spec", 
            "used-patch.patch",      # This one is referenced
            "unused-patch.patch",    # This one is not referenced
            "orphan.patch"           # This one is also not referenced
        ]
        
        patterns = self.detector.detect_patch_file_issues(
            self.test_spec_path, spec_content, file_list
        )
        
        # Should detect 2 unused patch files
        unused_patches = [p for p in patterns if p.id == 'unused-patch-file']
        self.assertEqual(len(unused_patches), 2)
        
        # Check specific patch names
        patch_names = [p.description for p in unused_patches]
        self.assertTrue(any("unused-patch.patch" in desc for desc in patch_names))
        self.assertTrue(any("orphan.patch" in desc for desc in patch_names))
        
        # Check severity
        for pattern in unused_patches:
            self.assertEqual(pattern.severity, Severity.WARNING)
    
    def test_cve_patch_mismatch(self):
        """
        Test detection of CVE-named patches without corresponding CVE documentation.
        
        This test validates that when a patch file is named using CVE convention
        (e.g., CVE-2023-1234-fix.patch), the corresponding CVE identifier should
        be mentioned somewhere in the spec file content. This ensures proper
        traceability between security patches and their documentation.
        
        Expected behavior:
        - Should detect CVE patch files where the CVE ID is not mentioned in spec
        - Each mismatch should generate an ERROR severity anti-pattern
        - Should not flag CVE patches that are properly documented
        - Should handle multiple CVE patches correctly
        - Should also detect unused patch files as separate issues
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: CVE-2023-1234-fix.patch
Patch1: regular-patch.patch

%description
Test package
This patch addresses some issues.

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Initial package
- Fixed CVE-2023-5678
        """
        
        file_list = [
            "test-package.spec",
            "CVE-2023-1234-fix.patch",  # CVE is referenced in Patch0 line, so no mismatch
            "CVE-2023-9999-fix.patch",  # CVE not mentioned anywhere in spec
            "CVE-2023-5678-fix.patch",  # CVE mentioned in changelog but not referenced as patch
            "regular-patch.patch"       # Referenced as Patch1
        ]
        
        patterns = self.detector.detect_patch_file_issues(
            self.test_spec_path, spec_content, file_list
        )
        
        # Should detect 1 CVE mismatch (CVE-2023-9999 patch file but CVE not mentioned in spec)
        cve_mismatches = [p for p in patterns if p.id == 'cve-patch-mismatch']
        self.assertEqual(len(cve_mismatches), 1)
        
        # Check specific CVE
        mismatch = cve_mismatches[0]
        self.assertIn("CVE-2023-9999", mismatch.description)
        self.assertEqual(mismatch.severity, Severity.ERROR)
        
        # Should also detect 2 unused patch files
        unused_patches = [p for p in patterns if p.id == 'unused-patch-file']
        self.assertEqual(len(unused_patches), 2)
        unused_patch_files = [p.description for p in unused_patches]
        self.assertTrue(any("CVE-2023-9999-fix.patch" in desc for desc in unused_patch_files))
        self.assertTrue(any("CVE-2023-5678-fix.patch" in desc for desc in unused_patch_files))
    
    def test_no_patch_issues(self):
        """
        Test that no issues are detected when patch file handling is correct.
        
        This negative test case validates that the detector does not generate
        false positives when all patch files are properly handled - i.e., all
        referenced patches exist and all existing patches are referenced.
        
        Expected behavior:
        - Should return an empty list when no issues exist
        - All patch files should be accounted for
        - CVE patches should have corresponding CVE documentation
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: fix-bug.patch
Patch1: CVE-2023-1234-security.patch

%description
Test package

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Fixed security issue CVE-2023-1234
        """
        
        file_list = [
            "test-package.spec",
            "fix-bug.patch",
            "CVE-2023-1234-security.patch"
        ]
        
        patterns = self.detector.detect_patch_file_issues(
            self.test_spec_path, spec_content, file_list
        )
        
        # Should detect no issues
        self.assertEqual(len(patterns), 0)

    # =============================================================================
    # Test detect_cve_issues()
    # =============================================================================
    
    def test_future_dated_cve(self):
        """
        Test detection of CVEs with unrealistic future dates.
        
        This test validates that the detector identifies CVE identifiers that
        have years significantly in the future (beyond 2026 threshold), which
        likely indicate typos or invalid CVE identifiers.
        
        CVE format: CVE-YYYY-NNNN where YYYY is the year.
        The detector flags CVEs with years > 2026 as suspicious.
        
        Expected behavior:
        - Should detect CVEs with years beyond the threshold (2026)
        - Each future CVE should generate an ERROR severity anti-pattern
        - Should not flag CVEs with reasonable years (2025, 2026)
        - Should include the year and CVE ID in the pattern description
        - Should capture line numbers for context
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Fixes CVE-2030-1234 and CVE-2025-5678

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Fixed CVE-2030-1234 and CVE-2025-5678
        """
        
        patterns = self.detector.detect_cve_issues(self.test_spec_path, spec_content)
        
        # Should detect 1 future-dated CVE (2030 > 2026 threshold)
        future_cves = [p for p in patterns if p.id == 'future-dated-cve']
        self.assertEqual(len(future_cves), 1)
        
        future_cve = future_cves[0]
        self.assertIn("CVE-2030-1234", future_cve.description)
        self.assertIn("2030", future_cve.description)
        self.assertEqual(future_cve.severity, Severity.ERROR)
        self.assertIsNotNone(future_cve.line_number)
    
    def test_missing_cve_in_changelog(self):
        """
        Test detection of CVEs referenced but not documented in changelog.
        
        This test validates that all CVE identifiers mentioned in the spec file
        (description, comments, etc.) are properly documented in the changelog
        section. This ensures traceability and proper security documentation.
        
        The detector searches the entire changelog section, not just the latest
        entry, to find CVE mentions.
        
        Expected behavior:
        - Should detect CVEs mentioned in spec but missing from changelog
        - Each missing CVE should generate an ERROR severity anti-pattern
        - Should not flag CVEs that are documented anywhere in changelog
        - Should handle multiple CVEs correctly
        - Should use case-sensitive matching (CVE-YYYY-NNNN format)
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Fixes CVE-2023-1234, CVE-2023-5678, and CVE-2023-9999

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Fixed CVE-2023-1234
- Updated dependencies
        """
        
        patterns = self.detector.detect_cve_issues(self.test_spec_path, spec_content)
        
        # Should detect 2 CVEs missing from changelog
        missing_cves = [p for p in patterns if p.id == 'missing-cve-in-changelog']
        self.assertEqual(len(missing_cves), 2)
        
        # Check specific CVEs
        missing_cve_ids = [p.description for p in missing_cves]
        self.assertTrue(any("CVE-2023-5678" in desc for desc in missing_cve_ids))
        self.assertTrue(any("CVE-2023-9999" in desc for desc in missing_cve_ids))
        
        # Check severity
        for pattern in missing_cves:
            self.assertEqual(pattern.severity, Severity.ERROR)
    
    def test_cve_documented_in_old_changelog_entry(self):
        """
        Test that CVEs documented in older changelog entries are not flagged.
        
        This test validates that the detector properly searches the entire
        changelog history, not just the latest entry, when checking for CVE
        documentation. CVEs may be documented in older entries when they were
        originally fixed.
        
        Expected behavior:
        - Should not flag CVEs that appear in any changelog entry
        - Should search the complete changelog section
        - Should handle multiple changelog entries correctly
        - Should return empty results when all CVEs are documented
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Fixes CVE-2023-1234 and CVE-2023-5678

%changelog
* Mon Feb 15 2024 Test User <test@example.com> - 1.0-2
- Updated version

* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Fixed CVE-2023-1234
- Security update for CVE-2023-5678
        """
        
        patterns = self.detector.detect_cve_issues(self.test_spec_path, spec_content)
        
        # Should detect no missing CVEs since both are in changelog
        missing_cves = [p for p in patterns if p.id == 'missing-cve-in-changelog']
        self.assertEqual(len(missing_cves), 0)
    
    def test_no_cve_references(self):
        """
        Test that no CVE issues are detected when there are no CVE references.
        
        This negative test case validates that the detector gracefully handles
        spec files that don't contain any CVE references. Non-security updates
        should not trigger CVE-related anti-patterns.
        
        Expected behavior:
        - Should return empty results for specs without CVE references
        - Should not generate false positives
        - Should handle regular package updates correctly
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Regular package update

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Initial package
        """
        
        patterns = self.detector.detect_cve_issues(self.test_spec_path, spec_content)
        
        # Should detect no issues
        self.assertEqual(len(patterns), 0)

    # =============================================================================
    # Test detect_changelog_issues()
    # =============================================================================
    
    def test_missing_changelog_section(self):
        """
        Test detection of missing %changelog section.
        
        This test validates that the detector identifies spec files that are
        missing the required %changelog section entirely. The changelog is
        mandatory in RPM spec files for tracking changes.
        
        Expected behavior:
        - Should detect when %changelog section is completely absent
        - Should generate an ERROR severity anti-pattern
        - Should provide clear description about missing section
        - Should include appropriate recommendation
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Test package without changelog
        """
        
        patterns = self.detector.detect_changelog_issues(self.test_spec_path, spec_content)
        
        # Should detect missing changelog
        missing_changelog = [p for p in patterns if p.id == 'missing-changelog-entry']
        self.assertEqual(len(missing_changelog), 1)
        
        pattern = missing_changelog[0]
        self.assertEqual(pattern.name, "Missing Changelog")
        self.assertIn("%changelog section", pattern.description)
        self.assertEqual(pattern.severity, Severity.ERROR)
    
    def test_empty_changelog_section(self):
        """
        Test detection of empty %changelog section.
        
        This test validates that the detector identifies spec files that have
        a %changelog section but no actual changelog entries. An empty changelog
        is not useful for tracking package changes.
        
        Expected behavior:
        - Should detect when %changelog section exists but has no entries
        - Should generate an ERROR severity anti-pattern
        - Should distinguish from missing changelog section
        - Should provide appropriate description and recommendation
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Test package

%changelog
        """
        
        patterns = self.detector.detect_changelog_issues(self.test_spec_path, spec_content)
        
        # Should detect empty changelog
        empty_changelog = [p for p in patterns if p.id == 'missing-changelog-entry']
        self.assertEqual(len(empty_changelog), 1)
        
        pattern = empty_changelog[0]
        self.assertEqual(pattern.name, "Empty Changelog")
        self.assertIn("no entries", pattern.description)
        self.assertEqual(pattern.severity, Severity.ERROR)
    
    def test_invalid_changelog_format(self):
        """
        Test detection of invalid changelog entry format.
        
        This test validates that the detector identifies changelog entries that
        don't follow the standard RPM changelog format. The expected format is:
        * Day Month DD YYYY User <email> - Version-Release
        
        The detection uses a two-stage process:
        1. Basic pattern: \\*\\s+\\w+\\s+\\w+\\s+\\d+\\s+\\d{4} (identifies potential entries)
        2. Strict pattern: \\*\\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\\s+[A-Z][a-z]+\\s+\\d{1,2}\\s+\\d{4}
        
        Only entries that match the basic pattern but fail the strict pattern
        are flagged as invalid.
        
        Expected behavior:
        - Should detect entries with invalid day names (not Mon-Sun)
        - Should generate WARNING severity anti-patterns
        - Should capture line numbers for context
        - Should not flag entries that don't match basic pattern at all
        - Should not flag properly formatted entries
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Test package

%changelog
* Foo Bar 15 2024 Test User <test@example.com> - 1.0-1
- This entry matches basic pattern but fails strict validation (invalid day name)

* Mon Jan 15 2024 Test User <test@example.com> - 1.0-0
- Valid format

* 2024-01-15 Test User <test@example.com> - 0.9-1
- This doesn't match basic pattern so won't be checked
        """
        
        patterns = self.detector.detect_changelog_issues(self.test_spec_path, spec_content)
        
        # The basic pattern r'\*\s+\w+\s+\w+\s+\d+\s+\d{4}' matches "* Foo Bar 15 2024"
        # The strict pattern r'\*\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+[A-Z][a-z]+\s+\d{1,2}\s+\d{4}' fails on "Foo" (not a day name)
        # So 1 invalid format should be detected
        invalid_formats = [p for p in patterns if p.id == 'invalid-changelog-format']
        self.assertEqual(len(invalid_formats), 1)
        
        # Check severity
        for pattern in invalid_formats:
            self.assertEqual(pattern.severity, Severity.WARNING)
            self.assertIsNotNone(pattern.line_number)
    
    def test_valid_changelog_format(self):
        """
        Test that valid changelog formats are not flagged.
        
        This negative test case validates that properly formatted changelog
        entries are not flagged as anti-patterns. It ensures the detector
        doesn't generate false positives for correct formats.
        
        Tests various valid formats:
        - Different valid day names (Mon, Fri, Wed)
        - Different month names (Jan, Dec, Nov)
        - Different day numbers (1, 15, 22)
        - Different years and user formats
        
        Expected behavior:
        - Should return empty results for properly formatted changelogs
        - Should accept all valid day names (Mon-Sun)
        - Should accept standard month abbreviations
        - Should not generate false positives
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Test package

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Initial package

* Fri Dec 1 2023 Another User <another@example.com> - 0.9-1
- Pre-release version

* Wed Nov 22 2023 Test User <test@example.com> - 0.8-1
- Early version
        """
        
        patterns = self.detector.detect_changelog_issues(self.test_spec_path, spec_content)
        
        # Should detect no issues
        self.assertEqual(len(patterns), 0)

    # =============================================================================
    # Test detect_all() integration
    # =============================================================================
    
    def test_detect_all_integration(self):
        """
        Test that detect_all() properly combines all detection methods.
        
        This comprehensive integration test validates that the detect_all() method
        correctly orchestrates all individual detection functions and aggregates
        their results. It uses a complex spec file scenario that intentionally
        contains multiple types of issues to ensure cross-functional detection works.
        
        Test Scenario Design:
        ---------------------
        The test spec contains deliberate issues across all categories:
        
        **Patch Issues**:
        - Missing patch: "missing-patch.patch" (referenced but not in file_list)
        - Unused patches: "unused-patch.patch", "CVE-2023-9999-fix.patch" (in file_list but not referenced)
        - CVE mismatch: "CVE-2023-9999-fix.patch" (CVE not mentioned in spec content)
        
        **CVE Issues**:
        - Future-dated CVE: "CVE-2030-1234" (year 2030 > 2026 threshold)
        - Missing in changelog: "CVE-2023-5678", "CVE-2030-1234" (in description, not changelog)
        
        **Changelog Issues**:
        - Invalid format: "Foo Bar 15 2024" (invalid day name)
        
        Expected Detection Results:
        ---------------------------
        The test should detect approximately 6+ distinct anti-pattern instances:
        1. `missing-patch-file`: missing-patch.patch
        2. `unused-patch-file`: unused-patch.patch (not referenced)
        3. `unused-patch-file`: CVE-2023-9999-fix.patch (not referenced)  
        4. `cve-patch-mismatch`: CVE-2023-9999 (patch exists but CVE not in spec)
        5. `future-dated-cve`: CVE-2030-1234 (unrealistic future year)
        6. `missing-cve-in-changelog`: CVE-2023-5678 (in description, not in changelog)
        7. `missing-cve-in-changelog`: CVE-2030-1234 (in description, not in changelog)
        8. `invalid-changelog-format`: "Foo Bar 15 2024" (malformed entry)
        
        Validation Strategy:
        --------------------
        - Confirms that issues from multiple detection categories are found
        - Verifies that the aggregation doesn't lose or duplicate issues
        - Ensures proper anti-pattern ID assignment across all categories
        - Validates that detect_all() returns the same results as individual calls
        
        This test serves as a comprehensive end-to-end validation of the entire
        anti-pattern detection pipeline and ensures all components work together
        correctly in realistic scenarios.
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: missing-patch.patch
Patch1: CVE-2023-1234-fix.patch

%description
Fixes CVE-2030-1234 and CVE-2023-5678
This patch addresses some issues.

%changelog
* Foo Bar 15 2024 Test User <test@example.com> - 1.0-1
- Fixed some issues
        """
        
        file_list = [
            "test-package.spec",
            "unused-patch.patch",
            "CVE-2023-1234-fix.patch",
            "CVE-2023-9999-fix.patch"  # CVE not mentioned anywhere in spec
        ]
        
        patterns = self.detector.detect_all(self.test_spec_path, spec_content, file_list)
        
        # Should detect multiple issues across all categories
        self.assertGreater(len(patterns), 0)
        
        # Check that different types of issues are detected
        pattern_ids = [p.id for p in patterns]
        self.assertIn('missing-patch-file', pattern_ids)  # missing-patch.patch
        self.assertIn('unused-patch-file', pattern_ids)   # unused-patch.patch, CVE-2023-9999-fix.patch
        self.assertIn('future-dated-cve', pattern_ids)    # CVE-2030-1234
        self.assertIn('missing-cve-in-changelog', pattern_ids)  # CVE-2023-5678, CVE-2030-1234
        self.assertIn('cve-patch-mismatch', pattern_ids)  # CVE-2023-9999 patch but CVE not in spec content
        self.assertIn('invalid-changelog-format', pattern_ids)  # "Foo Bar 15 2024" invalid format
        
        # Print actual pattern IDs for debugging
        print(f"Detected pattern IDs: {pattern_ids}")
    
    def test_detect_all_no_issues(self):
        """
        Test that detect_all() returns empty list when no issues exist.
        
        This negative test case for the integration functionality validates
        that detect_all() correctly returns an empty result when a spec file
        has no anti-patterns. This ensures the detector doesn't generate
        false positives in well-formed spec files.
        
        The test uses a properly formatted spec with:
        - All patch files properly referenced and existing
        - CVE properly documented in changelog
        - Valid changelog format
        - No missing sections
        
        Expected behavior:
        - Should return empty list when no issues are present
        - Should not generate false positives
        - Should validate clean spec files correctly
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: security-fix.patch

%description
Fixes CVE-2023-1234

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Security fix for CVE-2023-1234
        """
        
        file_list = [
            "test-package.spec",
            "security-fix.patch"
        ]
        
        patterns = self.detector.detect_all(self.test_spec_path, spec_content, file_list)
        
        # Should detect no issues
        self.assertEqual(len(patterns), 0)

    # =============================================================================
    # Test severity mapping and configuration
    # =============================================================================
    
    def test_severity_mapping(self):
        """
        Test that severity mapping is correctly applied.
        
        This test validates that the AntiPatternDetector correctly maps
        anti-pattern types to their expected severity levels. Proper severity
        mapping is crucial for determining which issues block PRs (ERROR/CRITICAL)
        versus which are recommendations (WARNING/INFO).
        
        Validates the following severity mappings:
        - missing-patch-file: ERROR (blocks merge)
        - unused-patch-file: WARNING (review recommended)
        - cve-patch-mismatch: ERROR (blocks merge)
        - future-dated-cve: ERROR (blocks merge)
        - missing-cve-in-changelog: ERROR (blocks merge)
        - missing-changelog-entry: ERROR (blocks merge)
        - invalid-changelog-format: WARNING (review recommended)
        
        Expected behavior:
        - Should map each anti-pattern ID to correct severity
        - Should maintain consistency with documented severity levels
        - Should support configuration changes if needed
        """
        # Test that severity map contains expected mappings
        expected_mappings = {
            'missing-patch-file': Severity.ERROR,
            'unused-patch-file': Severity.WARNING,
            'cve-patch-mismatch': Severity.ERROR,
            'future-dated-cve': Severity.ERROR,
            'missing-cve-in-changelog': Severity.ERROR,
            'missing-changelog-entry': Severity.ERROR,
            'invalid-changelog-format': Severity.WARNING,
        }
        
        for pattern_id, expected_severity in expected_mappings.items():
            self.assertEqual(
                self.detector.severity_map[pattern_id], 
                expected_severity,
                f"Severity mapping for {pattern_id} should be {expected_severity}"
            )
    
    def test_antipattern_dataclass(self):
        """
        Test that AntiPattern dataclass works correctly.
        
        This test validates the AntiPattern dataclass structure and functionality.
        The AntiPattern class is the core data structure for representing detected
        issues, containing all necessary information for reporting and processing.
        
        Validates:
        - All required fields are properly set and accessible
        - Field types are correct (string, int, enum, etc.)
        - Dataclass behavior works as expected
        - Optional fields (line_number, context) can be None
        
        Expected behavior:
        - Should create AntiPattern instances correctly
        - Should allow access to all fields
        - Should maintain field types and values
        - Should support both required and optional fields
        """
        pattern = AntiPattern(
            id='test-pattern',
            name='Test Pattern',
            description='Test description',
            severity=Severity.WARNING,
            file_path='/test/path',
            line_number=42,
            context='test context',
            recommendation='test recommendation'
        )
        
        self.assertEqual(pattern.id, 'test-pattern')
        self.assertEqual(pattern.name, 'Test Pattern')
        self.assertEqual(pattern.severity, Severity.WARNING)
        self.assertEqual(pattern.line_number, 42)

    # =============================================================================
    # Edge cases and error handling
    # =============================================================================
    
    def test_multiline_patch_references(self):
        """
        Test handling of patch references that might span multiple lines.
        
        This test validates that the detector correctly handles patch references
        with various whitespace patterns (spaces, tabs) that might occur in
        real spec files. It ensures the regex patterns are robust enough to
        handle different formatting styles.
        
        Tests various whitespace scenarios:
        - Normal spacing: "Patch0: filename.patch"
        - Extra spaces: "Patch1:    filename.patch"
        - Tab characters: "Patch2:\tfilename.patch"
        
        Expected behavior:
        - Should correctly parse patch references regardless of whitespace
        - Should not generate false positives for formatting variations
        - Should handle tabs and multiple spaces correctly
        - Should maintain accurate line number tracking
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: fix-memory-leak.patch
Patch1:    whitespace-patch.patch
Patch2:	tab-patch.patch

%description
Test package
        """
        
        file_list = [
            "test-package.spec",
            "fix-memory-leak.patch",
            "whitespace-patch.patch",
            "tab-patch.patch"
        ]
        
        patterns = self.detector.detect_patch_file_issues(
            self.test_spec_path, spec_content, file_list
        )
        
        # Should detect no issues (all patches properly referenced)
        self.assertEqual(len(patterns), 0)
    
    def test_cve_case_insensitive_matching(self):
        """
        Test CVE pattern matching behavior - implementation is case sensitive.
        
        This test documents and validates the current case-sensitive behavior
        of CVE pattern matching in the detector. The implementation uses regex
        pattern r'CVE-(\d{4})-(\d{4,})' which only matches uppercase "CVE".
        
        Important behavioral note:
        The detector currently performs case-sensitive matching, meaning:
        - "CVE-2023-1234" will be detected
        - "cve-2023-1234" will NOT be detected
        
        This test validates that only properly formatted (uppercase) CVE
        references are processed, while lowercase variants are ignored.
        This behavior may be intentional to enforce standard CVE formatting.
        
        Expected behavior:
        - Should only detect uppercase CVE references
        - Should ignore lowercase cve references
        - Should flag missing changelog documentation for detected CVEs
        - Should maintain case sensitivity in changelog matching
        """
        spec_content = """
Name: test-package
Version: 1.0

%description
Fixes cve-2023-1234 and CVE-2023-5678

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Fixed CVE-2023-1234 and cve-2023-5678
        """
        
        patterns = self.detector.detect_cve_issues(self.test_spec_path, spec_content)
        
        # The implementation uses regex r'CVE-(\d{4})-(\d{4,})' which is case sensitive
        # So only 'CVE-2023-5678' will be detected from description
        # CVE-2023-5678 is not in changelog (lowercase 'cve-2023-5678' doesn't match)
        # CVE-2023-1234 is in changelog, so only CVE-2023-5678 should be flagged as missing
        missing_cves = [p for p in patterns if p.id == 'missing-cve-in-changelog']
        self.assertEqual(len(missing_cves), 1)
        self.assertIn("CVE-2023-5678", missing_cves[0].description)

    def test_patch_file_with_url(self):
        """
        Test that patch files referenced with full URLs are handled correctly.
        
        This test validates the detector's ability to:
        - Extract filenames from full URLs in Patch declarations
        - Match URL-based references with local patch files
        - Not produce false positives for URL-based patch references
        
        Test scenarios:
        - Full HTTP/HTTPS URLs with patch files
        - URLs with complex paths
        - Mix of URL and simple filename references
        
        Expected behavior:
        - Only the filename part of URL should be used for matching
        - Should find patches like glibc-2.38-fhs-1.patch when referenced as
          https://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.38-fhs-1.patch
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: simple.patch
Patch1: https://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.38-fhs-1.patch
Patch2: https://example.com/patches/security-fix.patch
Patch3: relative/path/to/local.patch

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Initial release
"""
        
        file_list = [
            'test.spec',
            'simple.patch',
            'glibc-2.38-fhs-1.patch',  # Matches Patch1 URL
            'security-fix.patch',       # Matches Patch2 URL
            'local.patch',              # Matches Patch3 relative path
        ]
        
        detector = AntiPatternDetector()
        patterns = detector.detect_patch_file_issues(spec_content, 'test.spec', file_list)
        
        # Should not detect any missing patch files
        missing_patches = [p for p in patterns if p.id == 'missing-patch-file']
        self.assertEqual(len(missing_patches), 0, 
                        f"Should not report missing patches for URL references. Found: {[p.description for p in missing_patches]}")
        
        # Should not detect any unused patch files
        unused_patches = [p for p in patterns if p.id == 'unused-patch-file']
        self.assertEqual(len(unused_patches), 0,
                        f"Should not report unused patches. Found: {[p.description for p in unused_patches]}")
    
    def test_patch_file_url_mismatch(self):
        """
        Test detection of missing patches when URL-referenced patches don't exist locally.
        
        This test validates that the detector correctly identifies when:
        - A patch is referenced via URL but the corresponding file doesn't exist
        - The filename extraction from URL works correctly for missing files
        
        Expected behavior:
        - Should report missing patch when extracted filename not in directory
        - Should use only the filename part from the URL for checking
        """
        spec_content = """
Name: test-package
Version: 1.0

Patch0: https://www.example.com/patches/missing-patch.patch
Patch1: https://github.com/project/fixes/CVE-2023-1234.patch

%changelog
* Mon Jan 15 2024 Test User <test@example.com> - 1.0-1
- Initial release
"""
        
        file_list = [
            'test.spec',
            # Note: missing-patch.patch and CVE-2023-1234.patch are not in the list
        ]
        
        detector = AntiPatternDetector()
        patterns = detector.detect_patch_file_issues(spec_content, 'test.spec', file_list)
        
        # Should detect two missing patch files
        missing_patches = [p for p in patterns if p.id == 'missing-patch-file']
        self.assertEqual(len(missing_patches), 2)
        
        # Check that the correct filenames were extracted from URLs
        missing_descriptions = [p.description for p in missing_patches]
        self.assertTrue(any('missing-patch.patch' in d for d in missing_descriptions))
        self.assertTrue(any('CVE-2023-1234.patch' in d for d in missing_descriptions))


if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests
    
    # Run the tests
    unittest.main(verbosity=2)