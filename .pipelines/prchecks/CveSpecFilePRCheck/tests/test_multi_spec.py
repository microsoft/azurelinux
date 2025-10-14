#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Test Suite for Multi-Spec File Organization
===========================================

Tests the new functionality for organizing results by spec file
when PRs contain changes to multiple packages.
"""

import unittest
import tempfile
import os
import sys
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SpecFileResult import SpecFileResult, MultiSpecAnalysisResult
from AntiPatternDetector import AntiPattern, Severity
from ResultAnalyzer import ResultAnalyzer
from GitHubClient import GitHubClient

class TestSpecFileResult(unittest.TestCase):
    """Test the SpecFileResult data structure."""
    
    def test_spec_file_result_creation(self):
        """Test creating a SpecFileResult with anti-patterns."""
        # Create some test anti-patterns
        patterns = [
            AntiPattern(
                id='missing-patch-file',
                name='Missing Patch File',
                description='Patch file not found',
                severity=Severity.ERROR,
                file_path='test.spec',
                line_number=10,
                context='Patch0: missing.patch',
                recommendation='Add the patch file'
            ),
            AntiPattern(
                id='unused-patch-file',
                name='Unused Patch File',
                description='Patch exists but not referenced',
                severity=Severity.WARNING,
                file_path='test.spec',
                line_number=None,
                context=None,
                recommendation='Remove or reference the patch'
            )
        ]
        
        # Create SpecFileResult
        result = SpecFileResult(
            spec_path='SPECS/package1/package1.spec',
            package_name='package1',
            anti_patterns=patterns,
            ai_analysis='Test AI analysis'
        )
        
        # Verify automatic severity calculation
        self.assertEqual(result.severity, Severity.ERROR)
        self.assertEqual(result.summary, '1 errors, 1 warnings')
        
    def test_issues_by_severity_grouping(self):
        """Test grouping issues by severity level."""
        patterns = [
            AntiPattern(
                id='error1', name='Error 1', description='desc',
                severity=Severity.ERROR, file_path='test.spec',
                line_number=1, context='', recommendation=''
            ),
            AntiPattern(
                id='error2', name='Error 2', description='desc',
                severity=Severity.ERROR, file_path='test.spec',
                line_number=2, context='', recommendation=''
            ),
            AntiPattern(
                id='warning1', name='Warning 1', description='desc',
                severity=Severity.WARNING, file_path='test.spec',
                line_number=3, context='', recommendation=''
            )
        ]
        
        result = SpecFileResult(
            spec_path='test.spec',
            package_name='test',
            anti_patterns=patterns
        )
        
        grouped = result.get_issues_by_severity()
        
        self.assertEqual(len(grouped[Severity.ERROR]), 2)
        self.assertEqual(len(grouped[Severity.WARNING]), 1)
        
    def test_issues_by_type_grouping(self):
        """Test grouping issues by type (id)."""
        patterns = [
            AntiPattern(
                id='missing-patch-file', name='Missing', description='desc1',
                severity=Severity.ERROR, file_path='test.spec',
                line_number=1, context='', recommendation=''
            ),
            AntiPattern(
                id='missing-patch-file', name='Missing', description='desc2',
                severity=Severity.ERROR, file_path='test.spec',
                line_number=2, context='', recommendation=''
            ),
            AntiPattern(
                id='cve-issue', name='CVE Issue', description='desc',
                severity=Severity.WARNING, file_path='test.spec',
                line_number=3, context='', recommendation=''
            )
        ]
        
        result = SpecFileResult(
            spec_path='test.spec',
            package_name='test',
            anti_patterns=patterns
        )
        
        grouped = result.get_issues_by_type()
        
        self.assertEqual(len(grouped['missing-patch-file']), 2)
        self.assertEqual(len(grouped['cve-issue']), 1)

class TestMultiSpecAnalysisResult(unittest.TestCase):
    """Test the MultiSpecAnalysisResult aggregation."""
    
    def test_multi_spec_aggregation(self):
        """Test aggregating results from multiple spec files."""
        # Create results for multiple packages
        spec1 = SpecFileResult(
            spec_path='SPECS/pkg1/pkg1.spec',
            package_name='pkg1',
            anti_patterns=[
                AntiPattern(
                    id='error', name='Error', description='desc',
                    severity=Severity.ERROR, file_path='pkg1.spec',
                    line_number=1, context='', recommendation=''
                )
            ]
        )
        
        spec2 = SpecFileResult(
            spec_path='SPECS/pkg2/pkg2.spec',
            package_name='pkg2',
            anti_patterns=[
                AntiPattern(
                    id='warning', name='Warning', description='desc',
                    severity=Severity.WARNING, file_path='pkg2.spec',
                    line_number=1, context='', recommendation=''
                )
            ]
        )
        
        spec3 = SpecFileResult(
            spec_path='SPECS/pkg3/pkg3.spec',
            package_name='pkg3',
            anti_patterns=[]  # Clean spec
        )
        
        # Create multi-spec result
        multi_result = MultiSpecAnalysisResult(
            spec_results=[spec1, spec2, spec3]
        )
        
        # Verify aggregation
        self.assertEqual(multi_result.overall_severity, Severity.ERROR)
        self.assertEqual(multi_result.total_issues, 2)
        self.assertEqual(multi_result.summary_statistics['total_specs'], 3)
        self.assertEqual(multi_result.summary_statistics['specs_with_errors'], 1)
        self.assertEqual(multi_result.summary_statistics['specs_with_warnings'], 1)
        self.assertEqual(multi_result.summary_statistics['total_errors'], 1)
        self.assertEqual(multi_result.summary_statistics['total_warnings'], 1)
        
    def test_get_failed_specs(self):
        """Test filtering specs with errors."""
        spec1 = SpecFileResult(
            spec_path='SPECS/fail/fail.spec',
            package_name='fail',
            anti_patterns=[
                AntiPattern(
                    id='error', name='Error', description='desc',
                    severity=Severity.ERROR, file_path='fail.spec',
                    line_number=1, context='', recommendation=''
                )
            ]
        )
        
        spec2 = SpecFileResult(
            spec_path='SPECS/pass/pass.spec',
            package_name='pass',
            anti_patterns=[]
        )
        
        multi_result = MultiSpecAnalysisResult(spec_results=[spec1, spec2])
        failed = multi_result.get_failed_specs()
        
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0].package_name, 'fail')
        
    def test_get_specs_by_package(self):
        """Test indexing specs by package name."""
        specs = [
            SpecFileResult(spec_path='SPECS/a/a.spec', package_name='package-a'),
            SpecFileResult(spec_path='SPECS/b/b.spec', package_name='package-b')
        ]
        
        multi_result = MultiSpecAnalysisResult(spec_results=specs)
        by_package = multi_result.get_specs_by_package()
        
        self.assertIn('package-a', by_package)
        self.assertIn('package-b', by_package)
        self.assertEqual(by_package['package-a'].spec_path, 'SPECS/a/a.spec')

class TestGitHubCommentFormatting(unittest.TestCase):
    """Test GitHub comment formatting for multi-spec results."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock environment variables that GitHubClient needs
        with patch.dict(os.environ, {
            'GITHUB_TOKEN': 'test-token',
            'GITHUB_REPOSITORY': 'test-org/test-repo'
        }):
            self.github_client = GitHubClient()
        
    def test_format_multi_spec_comment(self):
        """Test formatting a comment for multiple spec files."""
        # Create test data
        spec1 = SpecFileResult(
            spec_path='SPECS/glibc/glibc.spec',
            package_name='glibc',
            anti_patterns=[
                AntiPattern(
                    id='missing-patch-file',
                    name='Missing Patch File',
                    description='glibc-2.38-fhs-1.patch not found',
                    severity=Severity.ERROR,
                    file_path='glibc.spec',
                    line_number=45,
                    context='Patch5: https://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.38-fhs-1.patch',
                    recommendation='Add the missing patch file'
                )
            ],
            ai_analysis='Security patches need review for CVE compliance.'
        )
        
        spec2 = SpecFileResult(
            spec_path='SPECS/openssl/openssl.spec',
            package_name='openssl',
            anti_patterns=[
                AntiPattern(
                    id='cve-patch-mismatch',
                    name='CVE Patch Mismatch',
                    description='CVE-2024-1234.patch exists but CVE not documented',
                    severity=Severity.WARNING,
                    file_path='openssl.spec',
                    line_number=None,
                    context=None,
                    recommendation='Add CVE-2024-1234 to changelog'
                )
            ]
        )
        
        multi_result = MultiSpecAnalysisResult(spec_results=[spec1, spec2])
        
        # Format comment
        comment = self.github_client.format_multi_spec_comment(multi_result)
        
        # Verify comment structure
        self.assertIn('## 🔍 CVE Spec File Check Results', comment)
        self.assertIn('### ❌ Overall Status', comment)  # Should fail due to ERROR
        self.assertIn('### 📊 Summary by Package', comment)
        self.assertIn('glibc', comment)
        self.assertIn('openssl', comment)
        self.assertIn('### 📦 glibc Details', comment)
        self.assertIn('### 📦 openssl Details', comment)
        self.assertIn('glibc-2.38-fhs-1.patch not found', comment)
        self.assertIn('CVE-2024-1234', comment)
        self.assertIn('### ⚠️ Required Actions', comment)
        
    def test_format_comment_no_issues(self):
        """Test formatting when no issues are found."""
        spec1 = SpecFileResult(
            spec_path='SPECS/clean/clean.spec',
            package_name='clean-package',
            anti_patterns=[]
        )
        
        multi_result = MultiSpecAnalysisResult(spec_results=[spec1])
        comment = self.github_client.format_multi_spec_comment(multi_result)
        
        self.assertIn('### ✅ Overall Status', comment)
        self.assertIn('clean-package', comment)
        self.assertNotIn('### ⚠️ Required Actions', comment)

class TestResultAnalyzer(unittest.TestCase):
    """Test ResultAnalyzer report generation for multi-spec results."""
    
    def setUp(self):
        """Set up test environment."""
        self.analyzer = ResultAnalyzer(anti_patterns=[], ai_analysis=[])
        
    def test_generate_multi_spec_report(self):
        """Test generating a comprehensive report for multiple specs."""
        # Create test data with various issues
        spec1 = SpecFileResult(
            spec_path='SPECS/critical/critical.spec',
            package_name='critical-pkg',
            anti_patterns=[
                AntiPattern(
                    id='future-dated-cve',
                    name='Future Dated CVE',
                    description='CVE-2030-9999 has invalid future date',
                    severity=Severity.ERROR,
                    file_path='critical.spec',
                    line_number=100,
                    context='CVE-2030-9999',
                    recommendation='Fix CVE year'
                )
            ]
        )
        
        spec2 = SpecFileResult(
            spec_path='SPECS/warning/warning.spec',
            package_name='warning-pkg',
            anti_patterns=[
                AntiPattern(
                    id='unused-patch-file',
                    name='Unused Patch File',
                    description='old-fix.patch not referenced',
                    severity=Severity.WARNING,
                    file_path='warning.spec',
                    line_number=None,
                    context=None,
                    recommendation='Remove or reference the patch'
                )
            ]
        )
        
        multi_result = MultiSpecAnalysisResult(spec_results=[spec1, spec2])
        
        # Generate report
        report = self.analyzer.generate_multi_spec_report(multi_result)
        
        # Verify report content
        self.assertIn('CVE SPEC FILE CHECK - ANALYSIS REPORT', report)
        self.assertIn('EXECUTIVE SUMMARY', report)
        self.assertIn('Total Spec Files Analyzed: 2', report)
        self.assertIn('Specs with Errors: 1', report)
        self.assertIn('Specs with Warnings: 1', report)
        self.assertIn('PACKAGE ANALYSIS DETAILS', report)
        self.assertIn('critical-pkg', report)
        self.assertIn('warning-pkg', report)
        self.assertIn('RECOMMENDED ACTIONS', report)
        
    def test_save_json_results(self):
        """Test saving results in JSON format."""
        spec1 = SpecFileResult(
            spec_path='SPECS/test/test.spec',
            package_name='test-pkg',
            anti_patterns=[
                AntiPattern(
                    id='test-issue',
                    name='Test Issue',
                    description='Test description',
                    severity=Severity.INFO,
                    file_path='test.spec',
                    line_number=1,
                    context='context',
                    recommendation='recommendation'
                )
            ],
            ai_analysis='AI test analysis'
        )
        
        multi_result = MultiSpecAnalysisResult(spec_results=[spec1])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            self.analyzer.save_json_results(multi_result, temp_path)
            
            # Read and verify JSON
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            self.assertIn('timestamp', data)
            self.assertEqual(data['overall_severity'], 'INFO')
            self.assertEqual(data['total_issues'], 1)
            self.assertEqual(len(data['spec_results']), 1)
            
            spec_data = data['spec_results'][0]
            self.assertEqual(spec_data['package_name'], 'test-pkg')
            self.assertEqual(len(spec_data['anti_patterns']), 1)
            self.assertEqual(spec_data['ai_analysis'], 'AI test analysis')
            
        finally:
            os.unlink(temp_path)

def run_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSpecFileResult))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiSpecAnalysisResult))
    suite.addTests(loader.loadTestsFromTestCase(TestGitHubCommentFormatting))
    suite.addTests(loader.loadTestsFromTestCase(TestResultAnalyzer))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)