#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
GitHub Integration Module for CVE Spec File PR Check
====================================================

This module handles all GitHub-related operations for the CVE spec file PR check,
including fetching PR details, posting comments, and managing check statuses.

Key Features:
- Fetches PR metadata (files changed, diff content)
- Posts formatted analysis results as PR comments
- Updates PR check status based on analysis results
- Handles multi-spec file results with organized formatting

Usage:
    github_client = GitHubClient()
    pr_files = github_client.get_pr_files(pr_number)
    github_client.post_comment(pr_number, comment_body)
"""

import os
import sys
import json
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AntiPatternDetector import AntiPattern, Severity
from SpecFileResult import MultiSpecAnalysisResult

class GitHubClient:
    """
    GitHub API client for PR operations.
    
    This class encapsulates all GitHub API interactions needed for the
    CVE spec file PR check process.
    """
    
    def __init__(self):
        """Initialize the GitHub client with authentication."""
        self.token = os.environ.get('GITHUB_TOKEN')
        self.repo = os.environ.get('GITHUB_REPOSITORY', 'microsoft/azurelinux')
        self.api_base = 'https://api.github.com'
        
        if not self.token:
            print("Warning: GITHUB_TOKEN not set. GitHub operations will be limited.")
        
        self.headers = {
            'Authorization': f'token {self.token}' if self.token else '',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Get the list of files changed in a PR.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            List of file information dictionaries
        """
        url = f"{self.api_base}/repos/{self.repo}/pulls/{pr_number}/files"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching PR files: {e}")
            return []
    
    def get_pr_diff(self, pr_number: int) -> str:
        """
        Get the full diff of a PR.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            PR diff as a string
        """
        url = f"{self.api_base}/repos/{self.repo}/pulls/{pr_number}"
        headers = {**self.headers, 'Accept': 'application/vnd.github.v3.diff'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching PR diff: {e}")
            return ""
    
    def post_comment(self, pr_number: int, comment: str) -> bool:
        """
        Post a comment to a PR.
        
        Args:
            pr_number: Pull request number
            comment: Comment text (markdown supported)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.token:
            print("Cannot post comment: GITHUB_TOKEN not set")
            print("Comment that would be posted:")
            print(comment)
            return False
        
        url = f"{self.api_base}/repos/{self.repo}/issues/{pr_number}/comments"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json={'body': comment}
            )
            response.raise_for_status()
            print(f"Successfully posted comment to PR #{pr_number}")
            return True
        except requests.RequestException as e:
            print(f"Error posting comment: {e}")
            return False
    
    def format_comment(self, anti_patterns: List[AntiPattern], ai_analysis: List[str]) -> str:
        """
        Format the analysis results as a GitHub comment.
        
        Args:
            anti_patterns: List of detected anti-patterns
            ai_analysis: List of AI analysis results
            
        Returns:
            Formatted markdown comment
        """
        comment = "## 🔍 CVE Spec File Check Results\n\n"
        
        # Determine overall status
        has_errors = any(p.severity == Severity.ERROR for p in anti_patterns)
        has_warnings = any(p.severity == Severity.WARNING for p in anti_patterns)
        
        if has_errors:
            comment += "### ❌ Status: **FAILED**\n"
            comment += "Critical issues found that must be addressed before merging.\n\n"
        elif has_warnings:
            comment += "### ⚠️ Status: **WARNING**\n"
            comment += "Non-critical issues found. Please review.\n\n"
        else:
            comment += "### ✅ Status: **PASSED**\n"
            comment += "No issues detected.\n\n"
        
        # Summary statistics
        comment += "### 📊 Summary\n"
        comment += f"- Total issues found: {len(anti_patterns)}\n"
        
        # Group issues by severity
        errors = [p for p in anti_patterns if p.severity == Severity.ERROR]
        warnings = [p for p in anti_patterns if p.severity == Severity.WARNING]
        info = [p for p in anti_patterns if p.severity == Severity.INFO]
        
        comment += f"- Critical (must fix): {len(errors)}\n"
        comment += f"- Warnings (should review): {len(warnings)}\n"
        comment += f"- Info: {len(info)}\n\n"
        
        # Critical issues section
        if errors:
            comment += "### 🔴 Critical Issues Found:\n"
            for pattern in errors:
                comment += f"• **{pattern.name}**: {pattern.description}\n"
                if pattern.file_path and pattern.line_number:
                    comment += f"  📍 Location: `{pattern.file_path}:{pattern.line_number}`\n"
                if pattern.recommendation:
                    comment += f"  💡 Recommendation: {pattern.recommendation}\n"
        else:
            comment += "### ✅ Critical Issues:\n"
            comment += "• No critical security issues or missing CVE patch files were identified.\n"
        
        comment += "\n"
        
        # Warning issues section
        if warnings:
            comment += "### ⚠️ Warnings:\n"
            for pattern in warnings:
                comment += f"• **{pattern.name}**: {pattern.description}\n"
                if pattern.file_path and pattern.line_number:
                    comment += f"  📍 Location: `{pattern.file_path}:{pattern.line_number}`\n"
                if pattern.recommendation:
                    comment += f"  💡 Recommendation: {pattern.recommendation}\n"
            comment += "\n"
        
        # AI Analysis section
        if ai_analysis and any(ai_analysis):
            comment += "### 🤖 AI Analysis:\n"
            for analysis in ai_analysis:
                if analysis:  # Skip empty analyses
                    comment += f"{analysis}\n\n"
        
        # Required actions
        if has_errors:
            comment += "### ⚠️ Required Actions\n"
            comment += "Please address all critical issues before this PR can be merged.\n\n"
        
        # Footer
        comment += "---\n"
        comment += f"*Generated by CVE Spec File Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
        
        return comment
    
    def format_multi_spec_comment(self, multi_result: 'MultiSpecAnalysisResult') -> str:
        """
        Format analysis results for multiple spec files as a GitHub comment.
        
        Args:
            multi_result: MultiSpecAnalysisResult containing all spec file results
            
        Returns:
            Formatted markdown comment for GitHub
        """
        comment = "## 🔍 CVE Spec File Check Results\n\n"
        
        # Overall status
        if multi_result.overall_severity == Severity.ERROR:
            comment += "### ❌ Overall Status: **FAILED**\n"
            comment += f"Found critical issues that must be addressed before merging.\n\n"
        elif multi_result.overall_severity == Severity.WARNING:
            comment += "### ⚠️ Overall Status: **WARNING**\n"
            comment += f"Found issues that should be reviewed.\n\n"
        else:
            comment += "### ✅ Overall Status: **PASSED**\n"
            comment += f"No critical issues found.\n\n"
        
        # Summary statistics
        stats = multi_result.summary_statistics
        comment += "### 📊 Summary by Package\n\n"
        comment += f"- **Total Packages Analyzed:** {stats['total_specs']}\n"
        comment += f"- **Packages with Errors:** {stats['specs_with_errors']}\n"
        comment += f"- **Packages with Warnings:** {stats['specs_with_warnings']}\n"
        comment += f"- **Total Issues:** {multi_result.total_issues} "
        comment += f"({stats['total_errors']} errors, {stats['total_warnings']} warnings)\n\n"
        
        # Table of packages
        comment += "| Package | Status | Issues |\n"
        comment += "|---------|--------|--------|\n"
        
        for spec_result in multi_result.spec_results:
            status_emoji = "❌" if spec_result.severity == Severity.ERROR else (
                "⚠️" if spec_result.severity == Severity.WARNING else "✅"
            )
            comment += f"| {spec_result.package_name} | {status_emoji} | {spec_result.summary} |\n"
        
        comment += "\n"
        
        # Detailed issues by package (only for packages with issues)
        failed_specs = [s for s in multi_result.spec_results if s.anti_patterns]
        
        if failed_specs:
            comment += "### 📋 Detailed Issues\n\n"
            
            for spec_result in failed_specs:
                comment += f"#### 📦 {spec_result.package_name} Details\n\n"
                comment += f"**Spec File:** `{spec_result.spec_path}`\n\n"
                
                # Group by severity
                errors = [p for p in spec_result.anti_patterns if p.severity == Severity.ERROR]
                warnings = [p for p in spec_result.anti_patterns if p.severity == Severity.WARNING]
                
                # Only show Critical Issues section if there are errors
                if errors:
                    comment += "**🔴 Critical Issues Found:**\n"
                    for pattern in errors:
                        comment += f"• **{pattern.name}**: {pattern.description}\n"
                        if pattern.file_path and pattern.line_number:
                            comment += f"  📍 Location: `{pattern.file_path}:{pattern.line_number}`\n"
                        if pattern.recommendation:
                            comment += f"  💡 Recommendation: {pattern.recommendation}\n"
                    comment += "\n"
                
                # Warning issues
                if warnings:
                    comment += "**⚠️ Warnings:**\n"
                    for pattern in warnings:
                        comment += f"• **{pattern.name}**: {pattern.description}\n"
                        if pattern.file_path and pattern.line_number:
                            comment += f"  📍 Location: `{pattern.file_path}:{pattern.line_number}`\n"
                        if pattern.recommendation:
                            comment += f"  💡 Recommendation: {pattern.recommendation}\n"
                    comment += "\n"
                
                # AI Analysis
                if spec_result.ai_analysis:
                    comment += "**🤖 AI Analysis:**\n"
                    comment += f"{spec_result.ai_analysis}\n\n"
        else:
            # No issues found in any package
            comment += "### ✅ No Issues Found\n\n"
            comment += "All analyzed spec files passed the CVE security checks.\n\n"
        
        # Required actions
        if multi_result.overall_severity == Severity.ERROR:
            comment += "### ⚠️ Required Actions\n\n"
            comment += "Please address all critical issues (❌) before this PR can be merged.\n"
        
        # Footer
        comment += "\n---\n"
        comment += "*Generated by CVE Spec File Check - "
        comment += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
        
        return comment
    
    def update_check_status(self, sha: str, status: str, description: str) -> bool:
        """
        Update the status check for a commit.
        
        Args:
            sha: Git commit SHA
            status: Status ('pending', 'success', 'failure', 'error')
            description: Short description of the status
            
        Returns:
            True if successful, False otherwise
        """
        if not self.token:
            print(f"Would update status to: {status} - {description}")
            return False
        
        url = f"{self.api_base}/repos/{self.repo}/statuses/{sha}"
        
        data = {
            'state': status,
            'description': description,
            'context': 'CVE Spec File Check'
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            print(f"Successfully updated check status to: {status}")
            return True
        except requests.RequestException as e:
            print(f"Error updating check status: {e}")
            return False


def main():
    """Test the GitHub client functionality."""
    client = GitHubClient()
    
    # Test with a sample PR number (would need a real PR number to test)
    pr_number = int(os.environ.get('PR_NUMBER', '1'))
    
    print(f"Testing GitHub client with PR #{pr_number}")
    
    # Test getting PR files
    files = client.get_pr_files(pr_number)
    print(f"Found {len(files)} changed files")
    
    # Create a sample comment
    sample_patterns = [
        AntiPattern(
            id='test-error',
            name='Test Error',
            description='This is a test error',
            severity=Severity.ERROR,
            file_path='test.spec',
            line_number=10,
            context='Test context',
            recommendation='Fix this test issue'
        )
    ]
    
    comment = client.format_comment(sample_patterns, ['Test AI analysis'])
    print("\nFormatted comment:")
    print(comment)


if __name__ == '__main__':
    main()