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
import re
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
        # Use the severity.value for comparison instead of comparing the enum objects directly
        return max((pattern.severity for pattern in self.anti_patterns), key=lambda x: x.value)
    
    def should_fail_pipeline(self) -> bool:
        """
        Determine if the pipeline should fail based on detected issues.
        
        Returns:
            True if issues with ERROR or CRITICAL severity are found
        """
        highest_severity = self.get_highest_severity()
        # Convert to values for comparison
        return highest_severity.value >= Severity.ERROR.value
    
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
        
        # Sort by severity value, not the enum object itself
        for severity in sorted(counts.keys(), key=lambda x: x.value, reverse=True):
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
            lines.append("\n## 🔍 DETECTED ANTI-PATTERNS\n")
            
            # Group by severity for display
            # Sort by severity value, not the enum object itself
            for severity in sorted([s for s in self.grouped_patterns.keys()], key=lambda x: x.value, reverse=True):
                patterns = self.grouped_patterns[severity]
                
                severity_emojis = {
                    Severity.INFO: "ℹ️",
                    Severity.WARNING: "⚠️",
                    Severity.ERROR: "❌",
                    Severity.CRITICAL: "🚨"
                }
                
                lines.append(f"### {severity_emojis[severity]} {severity.name} ISSUES ({len(patterns)})")
                lines.append("-" * 80)
                
                # Number the patterns for easier reference
                for i, pattern in enumerate(patterns, 1):
                    lines.append(f"**{i}. {pattern.name}**: {pattern.description}")
                    
                    if hasattr(pattern, 'file_path') and pattern.file_path:
                        lines.append(f"   📄 **File**: `{pattern.file_path}`")
                    
                    if pattern.recommendation:
                        lines.append(f"   💡 **Recommendation**: {pattern.recommendation}")
                    
                    # Add specific details based on pattern type
                    if pattern.name == "MISSING_PATCH_FILES" and "missing_patches" in pattern.details:
                        lines.append("   🔍 **Missing patch files**:")
                        for j, patch in enumerate(pattern.details["missing_patches"], 1):
                            lines.append(f"     {j}. `{patch}`")
                    
                    elif pattern.name == "UNREFERENCED_PATCH_FILES" and "unreferenced_patches" in pattern.details:
                        lines.append("   🔍 **Unreferenced patch files**:")
                        for j, patch in enumerate(pattern.details["unreferenced_patches"], 1):
                            lines.append(f"     {j}. `{patch}`")
                    
                    elif pattern.name == "MISSING_PATCH_APPLICATION" and "missing_applications" in pattern.details:
                        lines.append("   🔍 **Patches not applied**:")
                        for j, app in enumerate(pattern.details["missing_applications"], 1):
                            lines.append(f"     {j}. Patch{app['patch_num']}: `{app['filename']}`")
                    
                    elif pattern.name == "DUPLICATE_PATCH_REFERENCES" and "duplicates" in pattern.details:
                        lines.append("   🔍 **Duplicate patch references**:")
                        for j, (patch_num, line_nums) in enumerate(pattern.details["duplicates"].items(), 1):
                            lines.append(f"     {j}. Patch{patch_num} defined at lines: {', '.join(map(str, line_nums))}")
                    
                    elif pattern.name == "MISSING_CVE_CHANGELOG_ENTRIES" and "missing_entries" in pattern.details:
                        lines.append("   🔍 **CVEs missing from changelog**:")
                        for j, cve in enumerate(pattern.details["missing_entries"], 1):
                            lines.append(f"     {j}. `{cve}`")
                    
                    lines.append("")
        
        # Add AI analysis section with better formatting
        lines.extend([
            "\n## 💬 OPENAI ANALYSIS RESULTS\n",
            "=" * 80
        ])
        
        # Format AI analysis for better readability
        formatted_analysis = []
        for line in self.ai_analysis.split('\n'):
            # Preserve existing markdown headers
            if line.startswith('##'):
                formatted_analysis.append(f"\n{line}")
            # Format section headers that look like headers but aren't properly marked
            elif re.match(r'^(Summary|Conclusion|Analysis|Recommendations?)(\s*:)?$', line, re.IGNORECASE):
                formatted_analysis.append(f"\n### 📊 {line}")
            # Enhance bullet points
            elif line.strip().startswith('•'):
                formatted_analysis.append(line.replace('•', '🔹'))
            # Enhance numbered lists
            elif re.match(r'^\d+\.', line.strip()):
                formatted_analysis.append(line)
            # Highlight CVE IDs
            elif 'CVE-' in line:
                formatted_line = re.sub(r'(CVE-\d{4}-\d{4,})', r'`\1`', line)
                formatted_analysis.append(formatted_line)
            # Highlight recommendations
            elif 'recommend' in line.lower():
                if not line.strip().startswith('🔸'):
                    formatted_analysis.append(f"🔸 {line}")
                else:
                    formatted_analysis.append(line)
            else:
                formatted_analysis.append(line)
        
        lines.append('\n'.join(formatted_analysis))
        lines.append("\n" + "=" * 80)
        
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
        # Create a serializable dictionary for each AntiPattern
        anti_pattern_dicts = []
        for pattern in self.anti_patterns:
            # Convert AntiPattern to a dictionary with all serializable attributes
            pattern_dict = {
                "name": pattern.name,
                "description": pattern.description,
                "severity": pattern.severity.name,
                "recommendation": pattern.recommendation
            }
            
            # Add optional attributes if they exist
            if hasattr(pattern, 'file_path') and pattern.file_path:
                pattern_dict["file_path"] = pattern.file_path
            
            if hasattr(pattern, 'line_number') and pattern.line_number:
                pattern_dict["line_number"] = pattern.line_number
                
            if hasattr(pattern, 'details') and pattern.details:
                pattern_dict["details"] = pattern.details
                
            if hasattr(pattern, 'id') and pattern.id:
                pattern_dict["id"] = pattern.id
                
            anti_pattern_dicts.append(pattern_dict)
        
        result = {
            "failed": self.should_fail_pipeline(),
            "highest_severity": self.get_highest_severity().name,
            "anti_patterns": anti_pattern_dicts,
            "ai_analysis": self.ai_analysis
        }
        
        return json.dumps(result, indent=2)
    
    def extract_conclusion(self) -> str:
        """
        Extract the conclusion section from the AI analysis.
        
        Returns:
            The conclusion section as a formatted string with emojis
        """
        conclusion = ""
        in_conclusion = False
        conclusion_header = False
        
        # Try to find a conclusion section in the AI analysis
        for line in self.ai_analysis.splitlines():
            # Check for various ways "Conclusion" might be formatted in the text
            if re.match(r'^#{1,3}\s+Conclusion', line, re.IGNORECASE) or line.strip() == "Conclusion:" or line.strip() == "CONCLUSION":
                in_conclusion = True
                conclusion_header = True
                conclusion = "## 📝 CONCLUSION\n\n"
                continue
            
            # If we're past the conclusion and hit another section header, stop collecting
            if in_conclusion and line.startswith('#') and not conclusion_header:
                break
                
            # Reset conclusion_header flag after processing the header
            conclusion_header = False
            
            # Add the line to our conclusion if we're in the conclusion section
            if in_conclusion:
                # Enhance bullet points with emojis
                if line.strip().startswith('•'):
                    line = line.replace('•', '🔹')
                elif line.strip().startswith('-'):
                    line = line.replace('-', '🔸')
                    
                # Highlight CVE IDs
                if 'CVE-' in line:
                    line = re.sub(r'(CVE-\d{4}-\d{4,})', r'`\1`', line)
                
                conclusion += line + "\n"
        
        # If no formal conclusion section was found, try to extract recommendations
        if not conclusion:
            recommendations = []
            in_recommendations = False
            
            for line in self.ai_analysis.splitlines():
                if "recommendation" in line.lower() or "summary" in line.lower():
                    in_recommendations = True
                    recommendations.append("## 📝 CONCLUSION (extracted from recommendations)\n")
                    continue
                
                if in_recommendations and line.strip():
                    recommendations.append(line)
            
            if recommendations:
                conclusion = "\n".join(recommendations)
        
        # If we still don't have a conclusion, create a generic one
        if not conclusion:
            conclusion = "## 📝 CONCLUSION\n\nPlease review the detailed analysis above for information about the CVE patches and spec file."
            
            # Try to identify the most important issues from anti-patterns
            critical_issues = [p for p in self.anti_patterns if p.severity >= Severity.ERROR]
            if critical_issues:
                conclusion += "\n\n### ❌ Critical Issues Detected:\n\n"
                for i, issue in enumerate(critical_issues, 1):
                    conclusion += f"**{i}. {issue.name}**: {issue.description}\n"
                    if issue.recommendation:
                        conclusion += f"   💡 **Recommendation**: {issue.recommendation}\n"
                    conclusion += "\n"
        
        return conclusion