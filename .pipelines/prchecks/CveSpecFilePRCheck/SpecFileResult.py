#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
SpecFileResult
--------------
Data structure for organizing analysis results by spec file.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from AntiPatternDetector import AntiPattern, Severity

@dataclass
class SpecFileResult:
    """
    Container for all analysis results related to a single spec file.
    
    Attributes:
        spec_path: Path to the spec file
        package_name: Name of the package (extracted from spec)
        anti_patterns: List of detected anti-patterns for this spec
        ai_analysis: AI analysis results specific to this spec
        severity: Highest severity level found in this spec
        summary: Brief summary of issues found
    """
    spec_path: str
    package_name: str
    anti_patterns: List[AntiPattern] = field(default_factory=list)
    ai_analysis: str = ""
    severity: Severity = Severity.INFO
    summary: str = ""
    
    def __post_init__(self):
        """Calculate derived fields after initialization."""
        if self.anti_patterns:
            # Set severity to highest found
            severities = [p.severity for p in self.anti_patterns]
            self.severity = max(severities, key=lambda x: x.value)
            
            # Generate summary
            error_count = sum(1 for p in self.anti_patterns if p.severity == Severity.ERROR)
            warning_count = sum(1 for p in self.anti_patterns if p.severity == Severity.WARNING)
            self.summary = f"{error_count} errors, {warning_count} warnings"
    
    def get_issues_by_severity(self) -> Dict[Severity, List[AntiPattern]]:
        """Group anti-patterns by severity level."""
        grouped = {}
        for pattern in self.anti_patterns:
            if pattern.severity not in grouped:
                grouped[pattern.severity] = []
            grouped[pattern.severity].append(pattern)
        return grouped
    
    def get_issues_by_type(self) -> Dict[str, List[AntiPattern]]:
        """Group anti-patterns by type (id)."""
        grouped = {}
        for pattern in self.anti_patterns:
            if pattern.id not in grouped:
                grouped[pattern.id] = []
            grouped[pattern.id].append(pattern)
        return grouped

@dataclass
class MultiSpecAnalysisResult:
    """
    Container for analysis results across multiple spec files.
    
    Attributes:
        spec_results: List of individual spec file results
        overall_severity: Highest severity across all specs
        total_issues: Total count of all issues
        summary_statistics: Aggregated statistics
    """
    spec_results: List[SpecFileResult] = field(default_factory=list)
    overall_severity: Severity = Severity.INFO
    total_issues: int = 0
    summary_statistics: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate aggregate statistics."""
        if self.spec_results:
            # Overall severity
            self.overall_severity = max(
                (r.severity for r in self.spec_results),
                key=lambda x: x.value
            )
            
            # Summary statistics
            self.summary_statistics = {
                'total_specs': len(self.spec_results),
                'specs_with_errors': sum(
                    1 for r in self.spec_results 
                    if r.severity >= Severity.ERROR
                ),
                'specs_with_warnings': sum(
                    1 for r in self.spec_results 
                    if any(p.severity == Severity.WARNING for p in r.anti_patterns)
                ),
                'total_errors': sum(
                    sum(1 for p in r.anti_patterns if p.severity == Severity.ERROR)
                    for r in self.spec_results
                ),
                'total_warnings': sum(
                    sum(1 for p in r.anti_patterns if p.severity == Severity.WARNING)
                    for r in self.spec_results
                )
            }
            
            # Total issues (only ERROR + WARNING, not INFO)
            self.total_issues = (
                self.summary_statistics['total_errors'] + 
                self.summary_statistics['total_warnings']
            )
    
    def get_failed_specs(self) -> List[SpecFileResult]:
        """Get spec files with ERROR or higher severity."""
        return [
            r for r in self.spec_results 
            if r.severity >= Severity.ERROR
        ]
    
    def get_specs_by_package(self) -> Dict[str, SpecFileResult]:
        """Get spec results indexed by package name."""
        return {r.package_name: r for r in self.spec_results}