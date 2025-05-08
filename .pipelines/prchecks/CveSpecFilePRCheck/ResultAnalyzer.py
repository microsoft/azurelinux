#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
ResultAnalyzer processes detection results and formats outputs for the pipeline.

This module analyzes results from both the programmatic anti-pattern detection
and AI-powered analysis, combining them into a comprehensive report that can be
used to determine whether to fail the pipeline.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from AntiPatternDetector import AntiPattern, Severity


class ResultAnalyzer:
    """
    Analyzes and formats results from anti-pattern detection and AI analysis.
    
    This class is responsible for:
    - Processing anti-pattern detection results
    - Formatting output reports for the console and logs
    - Determining whether to fail the pipeline based on severity
    """
    
    def __init__(self, anti_patterns: List[AntiPattern], ai_analysis: str):
        """
        Initialize with detection results and AI analysis.
        
        Args:
            anti_patterns: List of detected anti-patterns
            ai_analysis: Analysis string from Azure OpenAI
        """
        self.anti_patterns = anti_patterns
        self.ai_analysis = ai_analysis
        
        # Group anti-patterns by severity
        self.grouped_patterns = self._group_by_severity()
    
    def _group_by_severity(self) -> Dict[Severity, List[AntiPattern]]:
        """Group anti-patterns by severity level"""
        result = {}
        for pattern in self.anti_patterns:
            if pattern.severity not in result:
                result[pattern.severity] = []
            result[pattern.severity].append(pattern)
        return result
    
    def get_highest_severity(self) -> Severity:
        """Get the highest severity level among all detected anti-patterns"""
        if not self.anti_patterns:
            return Severity.INFO
        return max(pattern.severity for pattern in self.anti_patterns)
    
    def should_fail_pipeline(self) -> bool:
        """
        Determine if the pipeline should fail based on detected issues.
        
        Returns:
            True if issues with ERROR or CRITICAL severity are found
        """
        highest_severity = self.get_highest_severity()
        return highest_severity >= Severity.ERROR
    
    def generate_console_summary(self) -> str:
        """
        Generate a summary of detected issues for console output.
        
        Returns:
            Formatted summary string
        """
        if not self.anti_patterns:
            return "✅ No anti-patterns detected in spec files"
        
        # Count issues by severity
        counts = {}
        for pattern in self.anti_patterns:
            if pattern.severity not in counts:
                counts[pattern.severity] = 0
            counts[pattern.severity] += 1
        
        # Generate summary lines
        lines = ["📊 Anti-Pattern Detection Summary:"]
        
        emoji_map = {
            Severity.INFO: "ℹ️",
            Severity.WARNING: "⚠️",
            Severity.ERROR: "❌",
            Severity.CRITICAL: "🚨"
        }
        
        for severity in sorted(counts.keys(), reverse=True):
            lines.append(f"{emoji_map[severity]} {severity.name}: {counts[severity]} issue(s)")
        
        return "\n".join(lines)
    
    def generate_detailed_report(self) -> str:
        """
        Generate a detailed report of all detected issues.
        
        Returns:
            Formatted report string including anti-patterns and AI analysis
        """
        lines = []
        
        # Add border line with issue status
        if self.should_fail_pipeline():
            lines.append("=" * 80)
            lines.append("❌ CRITICAL ISSUES DETECTED - PR CHECK FAILED ❌")
            lines.append("=" * 80)
        else:
            lines.append("=" * 80)
            lines.append("⚠️ ISSUES DETECTED - PR CHECK PASSED WITH WARNINGS ⚠️")
            lines.append("=" * 80)
        
        # Add anti-pattern section if any were detected
        if self.anti_patterns:
            lines.append("\n🔍 DETECTED ANTI-PATTERNS:\n")
            
            # Group by severity for display
            for severity in sorted([s for s in self.grouped_patterns.keys()], reverse=True):
                patterns = self.grouped_patterns[severity]
                
                severity_emojis = {
                    Severity.INFO: "ℹ️",
                    Severity.WARNING: "⚠️",
                    Severity.ERROR: "❌",
                    Severity.CRITICAL: "🚨"
                }
                
                lines.append(f"{severity_emojis[severity]} {severity.name} ISSUES ({len(patterns)})")
                lines.append("-" * 80)
                
                for pattern in patterns:
                    lines.append(f"{pattern.name}: {pattern.description}")
                    
                    if pattern.affected_files:
                        file_list = ", ".join(pattern.affected_files)
                        lines.append(f"  Files: {file_list}")
                    
                    if pattern.recommendation:
                        lines.append(f"  Recommendation: {pattern.recommendation}")
                    
                    # Add specific details based on pattern type
                    if pattern.name == "MISSING_PATCH_FILES" and "missing_patches" in pattern.details:
                        lines.append("  Missing patch files:")
                        for patch in pattern.details["missing_patches"]:
                            lines.append(f"    - {patch}")
                    
                    elif pattern.name == "UNREFERENCED_PATCH_FILES" and "unreferenced_patches" in pattern.details:
                        lines.append("  Unreferenced patch files:")
                        for patch in pattern.details["unreferenced_patches"]:
                            lines.append(f"    - {patch}")
                    
                    elif pattern.name == "MISSING_PATCH_APPLICATION" and "missing_applications" in pattern.details:
                        lines.append("  Patches not applied:")
                        for app in pattern.details["missing_applications"]:
                            lines.append(f"    - Patch{app['patch_num']}: {app['filename']}")
                    
                    elif pattern.name == "DUPLICATE_PATCH_REFERENCES" and "duplicates" in pattern.details:
                        lines.append("  Duplicate patch references:")
                        for patch_num, line_nums in pattern.details["duplicates"].items():
                            lines.append(f"    - Patch{patch_num} defined at lines: {', '.join(map(str, line_nums))}")
                    
                    elif pattern.name == "MISSING_CVE_CHANGELOG_ENTRIES" and "missing_entries" in pattern.details:
                        lines.append("  CVEs missing from changelog:")
                        for cve in pattern.details["missing_entries"]:
                            lines.append(f"    - {cve}")
                    
                    lines.append("")
        
        # Add AI analysis section
        lines.extend([
            "\n💬 OPENAI ANALYSIS RESULTS:",
            "=" * 80,
            self.ai_analysis,
            "=" * 80
        ])
        
        return "\n".join(lines)
    
    def generate_error_message(self) -> str:
        """
        Generate a concise error message for pipeline failure.
        
        Returns:
            Error message string focusing on the most severe issues
        """
        if not self.should_fail_pipeline():
            return ""
        
        # Get all ERROR and CRITICAL issues
        severe_issues = []
        for severity in [Severity.ERROR, Severity.CRITICAL]:
            if severity in self.grouped_patterns:
                severe_issues.extend(self.grouped_patterns[severity])
        
        # Build error message
        lines = ["❌ PR Check Failed: The following issues must be fixed:"]
        
        for issue in severe_issues:
            lines.append(f"- {issue.name}: {issue.description}")
            if issue.recommendation:
                lines.append(f"  Fix: {issue.recommendation}")
        
        lines.append("\nSee the full analysis report in the pipeline logs for details.")
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """
        Convert analysis results to JSON format.
        
        Returns:
            JSON string with analysis results
        """
        result = {
            "failed": self.should_fail_pipeline(),
            "highest_severity": self.get_highest_severity().name,
            "anti_patterns": [pattern.to_dict() for pattern in self.anti_patterns],
            "ai_analysis": self.ai_analysis
        }
        
        return json.dumps(result, indent=2)