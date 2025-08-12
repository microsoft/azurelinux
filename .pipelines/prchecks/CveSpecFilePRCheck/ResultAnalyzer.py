#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
ResultAnalyzer processes detection results and formats outputs for the pipeline.

This module analyzes results from both the programmatic anti-pattern detection
and AI-powered analysis, combining them into a comprehensive report that can be
used to determine whether to fail the pipeline.

Key Features:
- Parses structured AI output (brief summary vs detailed analysis)
- Generates concise PR comments focusing on critical issues
- Creates comprehensive logs for Azure DevOps pipeline
- Handles anti-pattern detection results with severity-based reporting
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from AntiPatternDetector import AntiPattern, Severity

# Configure logging
logger = logging.getLogger(__name__)


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
            "\n## 💬 COMPREHENSIVE AI ANALYSIS RESULTS\n",
            "=" * 80
        ])
        
        # Use the detailed analysis section from structured AI output
        detailed_ai_analysis = self.extract_detailed_analysis_for_logs()
        
        # Format AI analysis for better readability
        formatted_analysis = []
        for line in detailed_ai_analysis.split('\n'):
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
        Convert analysis results to JSON format with structured content.
        
        Returns:
            JSON string with analysis results, including separated brief and detailed content
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
            "pipeline_status": {
                "failed": self.should_fail_pipeline(),
                "highest_severity": self.get_highest_severity().name,
                "total_issues": len(self.anti_patterns),
                "critical_errors": len([p for p in self.anti_patterns if p.severity in (Severity.CRITICAL, Severity.ERROR)]),
                "warnings": len([p for p in self.anti_patterns if p.severity == Severity.WARNING])
            },
            "anti_patterns": anti_pattern_dicts,
            "ai_analysis": {
                "raw_response": self.ai_analysis,
                "brief_summary": self.extract_brief_summary_for_pr(),
                "detailed_analysis": self.extract_detailed_analysis_for_logs()
            },
            "reports": {
                "console_summary": self.generate_console_summary(),
                "detailed_report": self.generate_detailed_report(),
                "pr_comment_content": self.generate_pr_comment_content()
            }
        }
        
        return json.dumps(result, indent=2)
    
    def extract_conclusion(self) -> str:
        """
        Extract the conclusion section from the AI analysis.
        DEPRECATED: Use extract_brief_summary_for_pr() for PR comments instead.
        
        Returns:
            The conclusion section as a formatted string with emojis
        """
        logger.warning("extract_conclusion() is deprecated. Use extract_brief_summary_for_pr() for PR comments.")
        return self.extract_brief_summary_for_pr()

    def extract_brief_summary_for_pr(self) -> str:
        """
        Extracts the brief summary section from structured AI analysis for GitHub PR comments.
        
        Returns:
            Brief summary formatted for PR comments, or fallback content if parsing fails
        """
        if "SECTION 1: BRIEF PR COMMENT SUMMARY" in self.ai_analysis:
            try:
                # Extract Section 1 content
                section1_start = self.ai_analysis.find("SECTION 1: BRIEF PR COMMENT SUMMARY")
                section2_start = self.ai_analysis.find("SECTION 2: DETAILED ANALYSIS FOR LOGS")
                
                if section2_start == -1:
                    # If no Section 2 found, take everything after Section 1
                    brief_content = self.ai_analysis[section1_start:]
                else:
                    brief_content = self.ai_analysis[section1_start:section2_start]
                
                # Clean up the content
                brief_content = brief_content.replace("SECTION 1: BRIEF PR COMMENT SUMMARY", "").strip()
                brief_content = brief_content.replace("---", "").strip()
                
                return brief_content
                
            except Exception as e:
                logger.warning(f"Failed to parse brief summary from AI response: {e}")
                return self._generate_fallback_brief_summary()
        else:
            logger.info("AI response does not contain structured sections. Generating fallback summary.")
            return self._generate_fallback_brief_summary()

    def extract_detailed_analysis_for_logs(self) -> str:
        """
        Extracts the detailed analysis section from structured AI analysis for pipeline logs.
        
        Returns:
            Detailed analysis content, or full AI analysis if parsing fails
        """
        if "SECTION 2: DETAILED ANALYSIS FOR LOGS" in self.ai_analysis:
            try:
                section2_start = self.ai_analysis.find("SECTION 2: DETAILED ANALYSIS FOR LOGS")
                detailed_content = self.ai_analysis[section2_start:]
                
                # Clean up the content
                detailed_content = detailed_content.replace("SECTION 2: DETAILED ANALYSIS FOR LOGS", "").strip()
                
                return detailed_content
                
            except Exception as e:
                logger.warning(f"Failed to parse detailed analysis from AI response: {e}")
                return self.ai_analysis
        else:
            logger.info("AI response does not contain structured sections. Using full AI analysis.")
            return self.ai_analysis

    def _generate_fallback_brief_summary(self) -> str:
        """
        Generates a fallback brief summary when structured parsing fails.
        
        Returns:
            Brief summary based on anti-patterns and available AI content
        """
        summary_parts = []
        
        # Count critical issues from anti-patterns
        critical_patterns = [p for p in self.anti_patterns if p.severity in (Severity.CRITICAL, Severity.ERROR)]
        warning_patterns = [p for p in self.anti_patterns if p.severity == Severity.WARNING]
        
        if critical_patterns:
            summary_parts.append(f"**🚨 {len(critical_patterns)} Critical/Error Issue(s) Detected**")
            for pattern in critical_patterns[:3]:  # Show max 3 critical issues
                summary_parts.append(f"- **{pattern.name}**: {pattern.description}")
            if len(critical_patterns) > 3:
                summary_parts.append(f"- ...and {len(critical_patterns) - 3} more critical issue(s)")
        
        elif warning_patterns:
            summary_parts.append(f"**⚠️ {len(warning_patterns)} Warning(s) Found**")
            for pattern in warning_patterns[:2]:  # Show max 2 warnings
                summary_parts.append(f"- **{pattern.name}**: {pattern.description}")
        
        else:
            summary_parts.append("**✅ No Critical Issues Detected**")
        
        # Try to extract key points from AI analysis
        if self.ai_analysis:
            # Look for lines that seem like recommendations or important points
            ai_lines = self.ai_analysis.split('\n')
            important_lines = []
            for line in ai_lines[:10]:  # Check first 10 lines for key points
                if any(keyword in line.lower() for keyword in ['recommend', 'critical', 'error', 'missing', 'issue']):
                    important_lines.append(line.strip())
                    if len(important_lines) >= 2:  # Max 2 AI points
                        break
            
            if important_lines:
                summary_parts.append("\n**AI Key Points:**")
                summary_parts.extend(important_lines)
        
        return "\n".join(summary_parts) if summary_parts else "Analysis completed. See detailed logs for full results."

    def generate_pr_comment_content(self) -> str:
        """
        Generates content specifically formatted for GitHub PR comments.
        Focuses on critical issues and brief recommendations.
        
        Returns:
            Formatted content suitable for posting as a GitHub PR comment
        """
        content_parts = []
        
        # Header with overall status
        critical_errors = [p for p in self.anti_patterns if p.severity in (Severity.CRITICAL, Severity.ERROR)]
        warnings = [p for p in self.anti_patterns if p.severity == Severity.WARNING]
        
        if critical_errors:
            content_parts.append("## 🚨 PR Check Failed - Critical Issues Found")
            content_parts.append(f"Found {len(critical_errors)} critical/error issue(s) that must be fixed.")
        elif warnings:
            content_parts.append("## ⚠️ PR Check Passed with Warnings")
            content_parts.append(f"Found {len(warnings)} warning(s) that should be reviewed.")
        else:
            content_parts.append("## ✅ PR Check Passed")
            content_parts.append("No critical issues detected in spec file changes.")
        
        # Add critical anti-pattern issues
        if critical_errors:
            content_parts.append("\n### 🔍 Critical Issues Detected:")
            for i, pattern in enumerate(critical_errors, 1):
                content_parts.append(f"{i}. **{pattern.name}** ({pattern.severity.name})")
                content_parts.append(f"   - {pattern.description}")
                if pattern.recommendation:
                    content_parts.append(f"   - 💡 **Fix:** {pattern.recommendation}")
        
        # Add brief AI analysis
        brief_ai_summary = self.extract_brief_summary_for_pr()
        if brief_ai_summary and brief_ai_summary != "Analysis completed. See detailed logs for full results.":
            content_parts.append("\n### 🤖 AI Analysis Summary:")
            content_parts.append(brief_ai_summary)
        
        # Add footer
        content_parts.append("\n---")
        content_parts.append("📋 **For detailed analysis and recommendations, check the Azure DevOps pipeline logs.**")
        
        return "\n".join(content_parts)