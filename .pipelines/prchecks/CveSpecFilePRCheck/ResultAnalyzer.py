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
import os
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional, Tuple
from AntiPatternDetector import AntiPattern, Severity
from datetime import datetime

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
    
    def __init__(self, anti_patterns: List[AntiPattern] = None, ai_analysis: str = None):
        """
        Initialize with detection results and AI analysis.
        
        Args:
            anti_patterns: List of detected anti-patterns (optional)
            ai_analysis: Analysis string from Azure OpenAI (optional)
        """
        self.anti_patterns = anti_patterns or []
        self.ai_analysis = ai_analysis or ""
        
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
    
    def _get_severity_emoji(self, severity: Severity) -> str:
        """Get emoji for severity level."""
        emoji_map = {
            Severity.INFO: "✅",
            Severity.WARNING: "⚠️",
            Severity.ERROR: "🔴",
            Severity.CRITICAL: "🔥"
        }
        return emoji_map.get(severity, "ℹ️")
    
    def generate_html_report(self, analysis_result: 'MultiSpecAnalysisResult') -> str:
        """
        Generate an interactive HTML report with dark theme and expandable sections.
        
        Args:
            analysis_result: MultiSpecAnalysisResult with all spec data
            
        Returns:
            HTML string with embedded CSS and JavaScript for interactivity
        """
        stats = analysis_result.summary_statistics
        severity_color = self._get_severity_color(analysis_result.overall_severity)
        
        html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; border-radius: 6px; border: 1px solid #30363d;">
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: {severity_color}; margin: 0;">
            {self._get_severity_emoji(analysis_result.overall_severity)} CVE Spec File Analysis Report
        </h2>
        <p style="color: #8b949e; margin: 5px 0; font-size: 12px;">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        </p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px;">
        <div style="background: #161b22; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #30363d;">
            <div style="font-size: 24px; font-weight: bold; color: #58a6ff;">{stats['total_specs']}</div>
            <div style="font-size: 12px; color: #8b949e;">Specs Analyzed</div>
        </div>
        <div style="background: #161b22; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #30363d;">
            <div style="font-size: 24px; font-weight: bold; color: #f85149;">{stats['specs_with_errors']}</div>
            <div style="font-size: 12px; color: #8b949e;">Errors</div>
        </div>
        <div style="background: #161b22; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #30363d;">
            <div style="font-size: 24px; font-weight: bold; color: #d29922;">{stats['specs_with_warnings']}</div>
            <div style="font-size: 12px; color: #8b949e;">Warnings</div>
        </div>
        <div style="background: #161b22; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #30363d;">
            <div style="font-size: 24px; font-weight: bold; color: #c9d1d9;">{analysis_result.total_issues}</div>
            <div style="font-size: 12px; color: #8b949e;">Total Issues</div>
        </div>
    </div>
"""
        
        # Add package details
        for spec_result in sorted(analysis_result.spec_results, key=lambda x: x.package_name):
            pkg_color = self._get_severity_color(spec_result.severity)
            html += f"""
    <details style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; margin-bottom: 10px; padding: 10px;">
        <summary style="cursor: pointer; font-weight: bold; color: {pkg_color}; font-size: 16px; user-select: none;">
            {self._get_severity_emoji(spec_result.severity)} {spec_result.package_name}
            <span style="color: #8b949e; font-weight: normal; font-size: 14px;">({spec_result.summary})</span>
        </summary>
        <div style="margin-top: 15px; padding-left: 20px;">
            <div style="margin-bottom: 10px;">
                <span style="color: #8b949e;">Spec File:</span> <code style="background: #0d1117; padding: 2px 6px; border-radius: 3px; font-size: 12px;">{spec_result.spec_path}</code>
            </div>
"""
            
            # Anti-patterns section
            if spec_result.anti_patterns:
                issues_by_type = spec_result.get_issues_by_type()
                html += """
            <details open style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; margin: 10px 0; padding: 10px;">
                <summary style="cursor: pointer; font-weight: bold; color: #f85149; user-select: none;">
                    🐛 Anti-Patterns Detected
                </summary>
                <div style="margin-top: 10px;">
"""
                for issue_type, patterns in issues_by_type.items():
                    html += f"""
                    <div style="margin-bottom: 15px;">
                        <div style="font-weight: bold; color: #d29922; margin-bottom: 5px;">
                            {issue_type} <span style="background: #0d1117; padding: 2px 8px; border-radius: 10px; font-size: 11px; color: #8b949e;">×{len(patterns)}</span>
                        </div>
                        <ul style="margin: 5px 0; padding-left: 20px; list-style-type: disc;">
"""
                    for idx, pattern in enumerate(patterns):
                        # Create unique ID for this finding
                        finding_id = f"{spec_result.package_name}-{issue_type.replace(' ', '-').replace('_', '-')}-{idx}"
                        html += f"""
                            <li style="color: #c9d1d9; margin: 10px 0; font-size: 13px; position: relative;">
                                {pattern.description}
                                <button class="challenge-btn" data-finding-id="{finding_id}" data-spec="{spec_result.spec_path}" data-issue-type="{issue_type}" data-description="{pattern.description.replace('"', '&quot;')}" style="margin-left: 10px; padding: 4px 8px; font-size: 11px; background: #21262d; color: #58a6ff; border: 1px solid #30363d; border-radius: 4px; cursor: pointer;">
                                    💬 Challenge
                                </button>
                            </li>
"""
                    html += """
                        </ul>
                    </div>
"""
                html += """
                </div>
            </details>
"""
            
            # Recommended actions
            recommendations = set()
            for pattern in spec_result.anti_patterns:
                if pattern.severity >= Severity.ERROR:
                    recommendations.add(pattern.recommendation)
            
            if recommendations:
                html += """
            <details open style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; margin: 10px 0; padding: 10px;">
                <summary style="cursor: pointer; font-weight: bold; color: #3fb950; user-select: none;">
                    ✅ Recommended Actions
                </summary>
                <ul style="margin: 10px 0; padding-left: 20px; list-style-type: none;">
"""
                for rec in recommendations:
                    html += f"""
                    <li style="color: #c9d1d9; margin: 5px 0; font-size: 13px;">
                        <span style="color: #3fb950;">▸</span> {rec}
                    </li>
"""
                html += """
                </ul>
            </details>
"""
            
            html += """
        </div>
    </details>
"""
        
        html += """
</div>
"""
        return html
    
    def _get_severity_color(self, severity: Severity) -> str:
        """Get color code for severity level (dark theme)."""
        color_map = {
            Severity.INFO: "#3fb950",      # Green
            Severity.WARNING: "#d29922",   # Yellow
            Severity.ERROR: "#f85149",     # Red
            Severity.CRITICAL: "#ff6b6b"   # Bright red
        }
        return color_map.get(severity, "#8b949e")
    
    def generate_multi_spec_report(self, analysis_result: 'MultiSpecAnalysisResult', include_html: bool = True, 
                                   github_client = None, blob_storage_client = None, pr_number: int = None,
                                   pr_metadata: dict = None) -> str:
        """
        Generate a comprehensive report for multi-spec analysis results with enhanced formatting.
        
        Args:
            analysis_result: MultiSpecAnalysisResult with all spec data
            include_html: Whether to include interactive HTML report at the top
            github_client: Optional GitHubClient instance for creating Gist with HTML report (fallback)
            blob_storage_client: Optional BlobStorageClient for uploading to Azure Blob Storage (preferred)
            pr_number: PR number for blob storage upload (required if blob_storage_client provided)
            pr_metadata: Optional dict with PR metadata (title, author, branches, sha, timestamp)
            
        Returns:
            Formatted GitHub markdown report with optional HTML section
        """
        report_lines = []
        
        # Use provided metadata or create default
        if not pr_metadata:
            pr_metadata = {
                "pr_number": pr_number or 0,
                "pr_title": f"PR #{pr_number}" if pr_number else "Unknown PR",
                "pr_author": "Unknown",
                "source_branch": os.environ.get("SYSTEM_PULLREQUEST_SOURCEBRANCH", "unknown"),
                "target_branch": os.environ.get("SYSTEM_PULLREQUEST_TARGETBRANCH", "main"),
                "source_commit_sha": os.environ.get("SYSTEM_PULLREQUEST_SOURCECOMMITID", "")[:8],
                "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
        
        # Add HTML report - try blob storage first, fall back to Gist
        # Note: Blob storage preferred for production, Gist as fallback
        if include_html and (blob_storage_client or github_client):
            html_report = self.generate_html_report(analysis_result)
            
            # Create a self-contained HTML page with authentication
            html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CVE Spec File Check Report - PR #{pr_number}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        }}
        
        /* Auth UI Styles */
        #auth-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        
        #sign-in-btn {{
            background: #238636;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        #sign-in-btn:hover {{
            background: #2ea043;
        }}
        
        #user-menu {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        #user-avatar {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
        }}
        
        #user-info {{
            display: flex;
            flex-direction: column;
        }}
        
        #user-name {{
            font-size: 14px;
            font-weight: 600;
            color: #c9d1d9;
        }}
        
        #collaborator-badge {{
            font-size: 11px;
            color: #58a6ff;
            background: #1f6feb20;
            padding: 2px 6px;
            border-radius: 12px;
        }}
        
        #sign-out-btn {{
            background: transparent;
            color: #8b949e;
            border: 1px solid #30363d;
            padding: 4px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }}
        
        #sign-out-btn:hover {{
            background: #21262d;
            color: #c9d1d9;
        }}
        
        .challenge-btn:hover {{
            background: #30363d;
            border-color: #58a6ff;
        }}
        
        .challenge-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        /* Challenge Modal */
        #challenge-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }}
        
        #challenge-modal.active {{
            display: flex;
        }}
        
        .modal-content {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 24px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        }}
        
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #30363d;
        }}
        
        .modal-header h3 {{
            margin: 0;
            color: #c9d1d9;
            font-size: 18px;
        }}
        
        .modal-close {{
            background: transparent;
            border: none;
            color: #8b949e;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            line-height: 24px;
        }}
        
        .modal-close:hover {{
            color: #c9d1d9;
        }}
        
        .finding-info {{
            background: #0d1117;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 16px;
            border: 1px solid #30363d;
        }}
        
        .finding-info p {{
            margin: 4px 0;
            color: #8b949e;
            font-size: 13px;
        }}
        
        .finding-info strong {{
            color: #c9d1d9;
        }}
        
        .challenge-options {{
            margin: 16px 0;
        }}
        
        .challenge-options label {{
            display: block;
            padding: 12px;
            margin: 8px 0;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            cursor: pointer;
            color: #c9d1d9;
        }}
        
        .challenge-options label:hover {{
            border-color: #58a6ff;
            background: #161b22;
        }}
        
        .challenge-options input[type="radio"] {{
            margin-right: 8px;
        }}
        
        .challenge-options input[type="radio"]:checked + label {{
            border-color: #58a6ff;
            background: #1f6feb20;
        }}
        
        .feedback-textarea {{
            width: 100%;
            min-height: 100px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 12px;
            color: #c9d1d9;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
        }}
        
        .feedback-textarea:focus {{
            outline: none;
            border-color: #58a6ff;
        }}
        
        .modal-actions {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
            justify-content: flex-end;
        }}
        
        .btn {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border: none;
        }}
        
        .btn-primary {{
            background: #238636;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #2ea043;
        }}
        
        .btn-primary:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .btn-secondary {{
            background: transparent;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }}
        
        .btn-secondary:hover {{
            background: #21262d;
        }}
    </style>
    <script>
        // ============================================================================
        // RADAR Authentication Module
        // ============================================================================
        
        const RADAR_AUTH = (() => {{
            const GITHUB_CLIENT_ID = 'Ov23limFwlBEPDQzgGmb';
            const AUTH_CALLBACK_URL = 'https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/auth/callback';
            const STORAGE_KEY = 'radar_auth_token';
            const USER_KEY = 'radar_user_info';
            
            // Get current user from localStorage
            function getCurrentUser() {{
                const userJson = localStorage.getItem(USER_KEY);
                return userJson ? JSON.parse(userJson) : null;
            }}
            
            // Get auth token from localStorage
            function getAuthToken() {{
                return localStorage.getItem(STORAGE_KEY);
            }}
            
            // Check if user is authenticated
            function isAuthenticated() {{
                return !!getAuthToken();
            }}
            
            // Initiate GitHub OAuth login
            function signIn() {{
                const currentUrl = window.location.href.split('#')[0]; // Remove any existing fragment
                const state = encodeURIComponent(currentUrl);
                const authUrl = `https://github.com/login/oauth/authorize?client_id=${{GITHUB_CLIENT_ID}}&redirect_uri=${{encodeURIComponent(AUTH_CALLBACK_URL)}}&scope=read:user%20read:org&state=${{state}}`;
                
                console.log('🔐 Redirecting to GitHub OAuth...');
                window.location.href = authUrl;
            }}
            
            // Sign out
            function signOut() {{
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem(USER_KEY);
                console.log('👋 Signed out');
                updateUI();
            }}
            
            // Handle auth callback (extract token from URL fragment)
            function handleAuthCallback() {{
                const fragment = window.location.hash.substring(1);
                const params = new URLSearchParams(fragment);
                const token = params.get('token');
                
                if (token) {{
                    console.log('🎫 Token received from OAuth callback');
                    localStorage.setItem(STORAGE_KEY, token);
                    
                    // Decode JWT to get user info (simple base64 decode, not verification)
                    try {{
                        const payload = JSON.parse(atob(token.split('.')[1]));
                        localStorage.setItem(USER_KEY, JSON.stringify({{
                            username: payload.username,
                            email: payload.email,
                            name: payload.name,
                            avatar_url: payload.avatar_url,
                            is_collaborator: payload.is_collaborator
                        }}));
                        console.log('✅ User authenticated:', payload.username);
                    }} catch (e) {{
                        console.error('Failed to decode token:', e);
                    }}
                    
                    // Clean up URL
                    window.history.replaceState({{}}, document.title, window.location.pathname + window.location.search);
                    updateUI();
                }}
            }}
            
            // Update UI based on auth state
            function updateUI() {{
                const authContainer = document.getElementById('auth-container');
                const user = getCurrentUser();
                
                if (user) {{
                    // Determine role badge
                    let roleBadge = '';
                    let roleColor = '';
                    let roleIcon = '';
                    
                    if (user.is_admin) {{
                        roleIcon = '👑';
                        roleBadge = 'Admin';
                        roleColor = '#ffd60a';
                    }} else if (user.is_collaborator) {{
                        roleIcon = '🔵';
                        roleBadge = 'Collaborator';
                        roleColor = '#0077b6';
                    }} else {{
                        roleIcon = '🟠';
                        roleBadge = 'PR Owner';
                        roleColor = '#fb8500';
                    }}
                    
                    // Show user menu with role badge
                    authContainer.innerHTML = `
                        <div id="user-menu">
                            <img id="user-avatar" src="${{user.avatar_url}}" alt="${{user.username}}">
                            <div id="user-info">
                                <div id="user-name">${{user.name || user.username}}</div>
                                <span id="collaborator-badge" style="color: ${{roleColor}};">${{roleIcon}} ${{roleBadge}}</span>
                            </div>
                            <button id="sign-out-btn" onclick="RADAR_AUTH.signOut()">Sign Out</button>
                        </div>
                    `;
                }} else {{
                    // Show sign-in button
                    authContainer.innerHTML = `
                        <button id="sign-in-btn" onclick="RADAR_AUTH.signIn()">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                            </svg>
                            Sign in with GitHub
                        </button>
                    `;
                }}
            }}
            
            // Get auth headers for API requests
            function getAuthHeaders() {{
                const token = getAuthToken();
                return token ? {{
                    'Authorization': `Bearer ${{token}}`,
                    'Content-Type': 'application/json'
                }} : {{
                    'Content-Type': 'application/json'
                }};
            }}
            
            // Initialize on page load
            function init() {{
                console.log('🚀 RADAR Auth initialized');
                handleAuthCallback();
                updateUI();
            }}
            
            // Public API
            return {{
                init,
                signIn,
                signOut,
                isAuthenticated,
                getCurrentUser,
                getAuthToken,
                getAuthHeaders
            }};
        }})();
        
        // Initialize auth when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {{
            RADAR_AUTH.init();
            initializeChallengeButtons();
        }});
        
        // ============================================================================
        // Challenge/Feedback Module
        // ============================================================================
        
        function initializeChallengeButtons() {{
            const challengeButtons = document.querySelectorAll('.challenge-btn');
            challengeButtons.forEach(btn => {{
                btn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const findingId = btn.dataset.findingId;
                    const spec = btn.dataset.spec;
                    const issueType = btn.dataset.issueType;
                    const description = btn.dataset.description;
                    
                    openChallengeModal({{
                        findingId,
                        spec,
                        issueType,
                        description
                    }});
                }});
            }});
        }}
        
        function openChallengeModal(finding) {{
            // Check if user is authenticated
            if (!RADAR_AUTH.isAuthenticated()) {{
                alert('Please sign in to submit challenges');
                RADAR_AUTH.signIn();
                return;
            }}
            
            const modal = document.getElementById('challenge-modal');
            document.getElementById('finding-spec').textContent = finding.spec;
            document.getElementById('finding-type').textContent = finding.issueType;
            document.getElementById('finding-desc').textContent = finding.description;
            
            // Store finding data for submission
            modal.dataset.findingId = finding.findingId;
            modal.dataset.spec = finding.spec;
            modal.dataset.issueType = finding.issueType;
            modal.dataset.description = finding.description;
            
            modal.classList.add('active');
        }}
        
        function closeChallengeModal() {{
            const modal = document.getElementById('challenge-modal');
            modal.classList.remove('active');
            document.getElementById('challenge-form').reset();
        }}
        
        async function submitChallenge() {{
            const modal = document.getElementById('challenge-modal');
            const challengeType = document.querySelector('input[name="challenge-type"]:checked');
            const feedbackText = document.getElementById('feedback-text').value.trim();
            const submitBtn = document.getElementById('submit-challenge-btn');
            
            if (!challengeType) {{
                alert('Please select a response type');
                return;
            }}
            
            if (!feedbackText) {{
                alert('Please provide an explanation');
                return;
            }}
            
            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {{
                const pr_number = {pr_number or 0};  // Will be filled by Python
                
                const response = await fetch('https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/challenge', {{
                    method: 'POST',
                    headers: RADAR_AUTH.getAuthHeaders(),
                    body: JSON.stringify({{
                        pr_number: pr_number,
                        spec_file: modal.dataset.spec,
                        antipattern_id: modal.dataset.findingId,
                        challenge_type: challengeType.value,
                        feedback_text: feedbackText
                    }})
                }});
                
                const result = await response.json();
                
                if (response.ok) {{
                    alert('✅ Challenge submitted successfully! A comment has been posted to the PR.');
                    closeChallengeModal();
                    
                    // Mark button as submitted
                    const btn = document.querySelector(`[data-finding-id="${{modal.dataset.findingId}}"]`);
                    if (btn) {{
                        btn.textContent = '✅ Challenged';
                        btn.disabled = true;
                    }}
                }} else {{
                    alert(`❌ Failed to submit challenge: ${{result.error || 'Unknown error'}}`);
                }}
            }} catch (error) {{
                console.error('Challenge submission error:', error);
                alert(`❌ Network error: ${{error.message}}`);
            }} finally {{
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Challenge';
            }}
        }}
    </script>
</head>
<body>
    <!-- Auth UI Container -->
    <div id="auth-container"></div>
    
    <!-- Challenge Modal -->
    <div id="challenge-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>💬 Challenge Finding</h3>
                <button class="modal-close" onclick="closeChallengeModal()">×</button>
            </div>
            
            <div class="finding-info">
                <p><strong>Spec File:</strong> <span id="finding-spec"></span></p>
                <p><strong>Issue Type:</strong> <span id="finding-type"></span></p>
                <p><strong>Description:</strong> <span id="finding-desc"></span></p>
            </div>
            
            <form id="challenge-form" onsubmit="event.preventDefault(); submitChallenge();">
                <div class="challenge-options">
                    <label style="cursor: pointer;">
                        <input type="radio" name="challenge-type" value="false-positive">
                        <span>🟢 <strong>False Alarm</strong> - This finding is incorrect</span>
                    </label>
                    <label style="cursor: pointer;">
                        <input type="radio" name="challenge-type" value="needs-context">
                        <span>🟡 <strong>Needs Context</strong> - This requires additional explanation</span>
                    </label>
                    <label style="cursor: pointer;">
                        <input type="radio" name="challenge-type" value="disagree-with-severity">
                        <span>🔴 <strong>Agree</strong> - I acknowledge this finding</span>
                    </label>
                </div>
                
                <div style="margin: 16px 0;">
                    <label style="color: #8b949e; font-size: 13px; display: block; margin-bottom: 8px;">
                        Explanation (required):
                    </label>
                    <textarea id="feedback-text" class="feedback-textarea" placeholder="Provide details about your response..." required></textarea>
                </div>
                
                <div class="modal-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeChallengeModal()">Cancel</button>
                    <button type="submit" id="submit-challenge-btn" class="btn btn-primary">Submit Challenge</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Main Report Content -->
{html_report}
</body>
</html>"""
            
            html_url = None
            
            # Try blob storage first (preferred for production with UMI)
            if blob_storage_client and pr_number:
                try:
                    logger.info("Attempting to upload HTML report to Azure Blob Storage...")
                    html_url = blob_storage_client.upload_html(
                        pr_number=pr_number,
                        html_content=html_page
                    )
                    if html_url:
                        logger.info(f"✅ HTML report uploaded to blob storage: {html_url}")
                except Exception as e:
                    logger.warning(f"Blob storage upload failed, will try Gist fallback: {e}")
                    html_url = None
            
            # Fall back to Gist if blob storage failed or not available
            if not html_url and github_client:
                logger.info("Using Gist for HTML report (blob storage not available or failed)")
                html_url = github_client.create_gist(
                    filename="cve-spec-check-report.html",
                    content=html_page,
                    description=f"CVE Spec File Check Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                if html_url:
                    logger.info(f"✅ HTML report uploaded to Gist: {html_url}")
            
            if html_url:
                # Add prominent HTML report link section
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")
                report_lines.append("## 📊 Interactive HTML Report")
                report_lines.append("")
                report_lines.append(f"### 🔗 **[CLICK HERE to open the Interactive HTML Report]({html_url})**")
                report_lines.append("")
                report_lines.append("*Opens in a new tab with full analysis details and interactive features*")
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")
                logger.info(f"Added HTML report link to comment: {html_url}")
            else:
                logger.warning("Both blob storage and Gist failed - skipping HTML report section")
                # No HTML report section added if both methods fail
        
        # Get severity emoji
        severity_emoji = self._get_severity_emoji(analysis_result.overall_severity)
        severity_name = analysis_result.overall_severity.name
        
        # Header with emoji and severity
        if analysis_result.overall_severity >= Severity.ERROR:
            report_lines.append(f"# {severity_emoji} CVE Spec File Check - **FAILED**")
        elif analysis_result.overall_severity == Severity.WARNING:
            report_lines.append(f"# {severity_emoji} CVE Spec File Check - **PASSED WITH WARNINGS**")
        else:
            report_lines.append(f"# {severity_emoji} CVE Spec File Check - **PASSED**")
        
        report_lines.append("")
        report_lines.append(f"**Overall Severity:** {severity_emoji} **{severity_name}**")
        report_lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## 📋 Executive Summary")
        report_lines.append("")
        stats = analysis_result.summary_statistics
        report_lines.append(f"| Metric | Count |")
        report_lines.append(f"|--------|-------|")
        report_lines.append(f"| **Total Spec Files Analyzed** | {stats['total_specs']} |")
        report_lines.append(f"| **Specs with Errors** | 🔴 {stats['specs_with_errors']} |")
        report_lines.append(f"| **Specs with Warnings** | ⚠️ {stats['specs_with_warnings']} |")
        report_lines.append(f"| **Total Issues Found** | {analysis_result.total_issues} |")
        report_lines.append("")
        
        # Package-by-package breakdown
        report_lines.append("## 📦 Package Analysis Details")
        report_lines.append("")
        
        sorted_specs = sorted(analysis_result.spec_results, key=lambda x: x.package_name)
        for idx, spec_result in enumerate(sorted_specs):
            pkg_emoji = self._get_severity_emoji(spec_result.severity)
            
            # Wrap entire spec section in collapsible details (open by default)
            report_lines.append("<details open>")
            report_lines.append(f"<summary><h3>{pkg_emoji} <b>{spec_result.package_name}</b> - {spec_result.severity.name}</h3></summary>")
            report_lines.append("")
            
            # Spec metadata
            report_lines.append(f"- **Spec File:** `{spec_result.spec_path}`")
            report_lines.append(f"- **Status:** {pkg_emoji} **{spec_result.severity.name}**")
            report_lines.append(f"- **Issues:** {spec_result.summary}")
            report_lines.append("")
            
            # Finer delimiter before anti-patterns
            if spec_result.anti_patterns or spec_result.ai_analysis or spec_result.severity >= Severity.ERROR:
                report_lines.append("***")
                report_lines.append("")
            
            # Anti-patterns section
            if spec_result.anti_patterns:
                report_lines.append("<details open>")
                report_lines.append("<summary>🐛 <b>Anti-Patterns Detected</b> (Click to collapse)</summary>")
                report_lines.append("")
                
                # Group by type
                issues_by_type = spec_result.get_issues_by_type()
                for issue_type, patterns in issues_by_type.items():
                    # Get severity from first pattern of this type (they should all be same severity)
                    pattern_severity = patterns[0].severity if patterns else Severity.INFO
                    severity_emoji_local = self._get_severity_emoji(pattern_severity)
                    severity_name = pattern_severity.name
                    
                    report_lines.append(f"#### {severity_emoji_local} `{issue_type}` **({severity_name})** - {len(patterns)} occurrence(s)")
                    report_lines.append("")
                    for i, pattern in enumerate(patterns, 1):
                        # Truncate long descriptions
                        desc = pattern.description if len(pattern.description) <= 100 else pattern.description[:97] + "..."
                        report_lines.append(f"{i}. {desc}")
                    report_lines.append("")
                
                report_lines.append("</details>")
                report_lines.append("")
                
                # Delimiter after anti-patterns if more content follows
                if spec_result.ai_analysis or spec_result.severity >= Severity.ERROR:
                    report_lines.append("***")
                    report_lines.append("")
            
            # AI Analysis section
            if spec_result.ai_analysis:
                report_lines.append("<details open>")
                report_lines.append("<summary>🤖 <b>AI Analysis Summary</b> (Click to collapse)</summary>")
                report_lines.append("")
                # Take first 5 lines of AI analysis
                ai_lines = spec_result.ai_analysis.split('\n')[:5]
                for line in ai_lines:
                    if line.strip():
                        report_lines.append(line)
                report_lines.append("")
                report_lines.append("</details>")
                report_lines.append("")
                
                # Delimiter after AI analysis if recommended actions follow
                if spec_result.severity >= Severity.ERROR:
                    report_lines.append("***")
                    report_lines.append("")
            
            # Per-spec Recommended Actions
            if spec_result.severity >= Severity.ERROR:
                report_lines.append("<details open>")
                report_lines.append(f"<summary>✅ <b>Recommended Actions for {spec_result.package_name}</b> (Click to collapse)</summary>")
                report_lines.append("")
                
                # Get unique recommendations
                recommendations = set()
                for pattern in spec_result.anti_patterns:
                    if pattern.severity >= Severity.ERROR:
                        recommendations.add(pattern.recommendation)
                
                if recommendations:
                    for rec in sorted(recommendations):
                        report_lines.append(f"- [ ] {rec}")
                    report_lines.append("")
                
                report_lines.append("</details>")
                report_lines.append("")
            
            # Close spec-level details
            report_lines.append("</details>")
            report_lines.append("")
            
            # Add subtle delimiter between specs (but not after the last one)
            if idx < len(sorted_specs) - 1:
                report_lines.append("---")
                report_lines.append("")
        
        # Overall Recommendations (keep at bottom)
        if analysis_result.get_failed_specs():
            report_lines.append("---")
            report_lines.append("")
            report_lines.append("## ✅ All Recommended Actions")
            report_lines.append("")
            report_lines.append("*Complete checklist of all actions needed across all packages*")
            report_lines.append("")
            
            for spec_result in analysis_result.get_failed_specs():
                report_lines.append(f"### **{spec_result.package_name}**")
                report_lines.append("")
                
                # Get unique recommendations
                recommendations = set()
                for pattern in spec_result.anti_patterns:
                    if pattern.severity >= Severity.ERROR:
                        recommendations.add(pattern.recommendation)
                
                for rec in sorted(recommendations):
                    report_lines.append(f"- [ ] {rec}")
                report_lines.append("")
        
        # Footer
        report_lines.append("---")
        report_lines.append("*🤖 Automated CVE Spec File Check | Azure Linux PR Pipeline*")
        
        return '\n'.join(report_lines)

    def save_json_results(self, analysis_result: 'MultiSpecAnalysisResult', filepath: str):
        """
        Save analysis results in structured JSON format.
        
        Args:
            analysis_result: MultiSpecAnalysisResult to save
            filepath: Path to save JSON file
        """
        import json
        from dataclasses import asdict
        
        # Convert to JSON-serializable format
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'overall_severity': analysis_result.overall_severity.name,
            'total_issues': analysis_result.total_issues,
            'summary_statistics': analysis_result.summary_statistics,
            'spec_results': []
        }
        
        for spec_result in analysis_result.spec_results:
            spec_data = {
                'spec_path': spec_result.spec_path,
                'package_name': spec_result.package_name,
                'severity': spec_result.severity.name,
                'summary': spec_result.summary,
                'anti_patterns': [
                    {
                        'id': p.id,
                        'name': p.name,
                        'description': p.description,
                        'severity': p.severity.name,
                        'line_number': p.line_number,
                        'recommendation': p.recommendation
                    }
                    for p in spec_result.anti_patterns
                ],
                'ai_analysis': spec_result.ai_analysis
            }
            json_data['spec_results'].append(spec_data)
        
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        logger.info(f"Saved JSON results to {filepath}")