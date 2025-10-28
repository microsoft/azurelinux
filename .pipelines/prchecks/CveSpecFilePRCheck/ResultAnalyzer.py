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
    
    def generate_html_report(self, analysis_result: 'MultiSpecAnalysisResult', pr_metadata: Optional[dict] = None) -> str:
        """
        Generate an interactive HTML report with dark theme and expandable sections.
        
        Args:
            analysis_result: MultiSpecAnalysisResult with all spec data
            pr_metadata: Optional dict with PR metadata (pr_number, pr_title, pr_author, etc.)
            
        Returns:
            HTML string with embedded CSS and JavaScript for interactivity
        """
        import html as html_module  # For escaping HTML attributes
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
"""
        
        # Add PR metadata section if provided
        if pr_metadata:
            pr_number = pr_metadata.get('pr_number', 'Unknown')
            pr_title = html_module.escape(pr_metadata.get('pr_title', 'Unknown'))
            pr_author = html_module.escape(pr_metadata.get('pr_author', 'Unknown'))
            source_branch = html_module.escape(pr_metadata.get('source_branch', 'unknown'))
            target_branch = html_module.escape(pr_metadata.get('target_branch', 'main'))
            source_commit = pr_metadata.get('source_commit_sha', '')[:8]
            
            html += f"""
    <div class="pr-info-card">
        <div class="pr-info-header">
            <div class="pr-info-icon">📋</div>
            <h3 class="pr-info-title">Pull Request Information</h3>
        </div>
        <div class="pr-info-grid">
            <span class="pr-info-label">PR Number</span>
            <span class="pr-info-value"><span class="pr-number-badge">#{pr_number}</span></span>
            
            <span class="pr-info-label">Title</span>
            <span class="pr-info-value">{pr_title}</span>
            
            <span class="pr-info-label">Author</span>
            <span class="pr-info-value"><span class="author-badge">@{pr_author}</span></span>
            
            <span class="pr-info-label">Branches</span>
            <span class="pr-info-value">
                <span class="branch-badge">{source_branch}</span> 
                <span style="color: var(--text-secondary); margin: 0 8px;">→</span> 
                <span class="branch-badge">{target_branch}</span>
            </span>
            
            <span class="pr-info-label">Commit</span>
            <span class="pr-info-value"><span class="commit-badge">{source_commit}</span></span>
        </div>
    </div>
"""
        
        html += f"""
    <div class="stats-grid">
        <!-- Total Specs Card -->
        <div class="stat-card" style="--stat-color: var(--accent-blue);">
            <div class="stat-icon stat-icon-blue">
                📊
            </div>
            <div class="stat-content">
                <div class="stat-value">{stats['total_specs']}</div>
                <div class="stat-label">Specs Analyzed</div>
            </div>
        </div>
        
        <!-- Errors Card -->
        <div class="stat-card" style="--stat-color: var(--accent-red);">
            <div class="stat-icon stat-icon-red">
                ⚠️
            </div>
            <div class="stat-content">
                <div class="stat-value">{stats['specs_with_errors']}</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
        
        <!-- Warnings Card -->
        <div class="stat-card" style="--stat-color: var(--accent-orange);">
            <div class="stat-icon stat-icon-orange">
                📋
            </div>
            <div class="stat-content">
                <div class="stat-value">{stats['specs_with_warnings']}</div>
                <div class="stat-label">Warnings</div>
            </div>
        </div>
        
        <!-- Total Issues Card with Bell Icon -->
        <div class="stat-card" style="--stat-color: var(--accent-purple);">
            <div class="stat-icon stat-icon-purple">
                <div class="bell-container">
                    <span class="bell-icon">🔔</span>
                    <span class="bell-badge" id="issues-badge">{analysis_result.total_issues}</span>
                </div>
            </div>
            <div class="stat-content">
                <div class="stat-value" id="total-issues-count">{analysis_result.total_issues}</div>
                <div class="stat-label">Total Issues</div>
            </div>
        </div>
    </div>
"""
        
        # Add package details
        for spec_result in sorted(analysis_result.spec_results, key=lambda x: x.package_name):
            pkg_color = self._get_severity_color(spec_result.severity)
            html += f"""
    <details class="spec-card" data-spec-name="{spec_result.package_name}">
        <summary style="color: {pkg_color};">
            {self._get_severity_emoji(spec_result.severity)} {spec_result.package_name}
            <span class="spec-summary" style="color: var(--text-secondary); font-weight: normal; font-size: 14px;">({spec_result.summary})</span>
        </summary>
        <div class="spec-card-content">
            <div style="margin-bottom: 16px;">
                <span style="color: var(--text-secondary); font-size: 13px;">Spec File:</span> 
                <code class="spec-file-badge">{spec_result.spec_path}</code>
            </div>
"""
            
            # Anti-patterns section
            if spec_result.anti_patterns:
                issues_by_type = spec_result.get_issues_by_type()
                html += """
            <details open class="antipattern-details">
                <summary>
                    🐛 Anti-Patterns Detected
                </summary>
                <div style="margin-top: 16px;">
"""
                for issue_type, patterns in issues_by_type.items():
                    html += f"""
                    <div class="issue-type-section">
                        <div class="issue-type-header">
                            <span class="issue-type-title">{issue_type}</span>
                            <span class="issue-count-badge">×{len(patterns)}</span>
                        </div>
                        <ul class="issue-list">
"""
                    for idx, pattern in enumerate(patterns):
                        # Use the issue_hash if available, otherwise fallback to generated ID
                        issue_hash = pattern.issue_hash if hasattr(pattern, 'issue_hash') and pattern.issue_hash else f"{spec_result.package_name}-{issue_type.replace(' ', '-').replace('_', '-')}-{idx}"
                        finding_id = issue_hash  # For backwards compatibility in HTML
                        # Properly escape the description for both HTML content and attributes
                        escaped_desc = html_module.escape(pattern.description, quote=True)
                        html += f"""
                            <li class="antipattern-item issue-item" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}">
                                <span class="issue-text">{escaped_desc}</span>
                                <button class="challenge-btn" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-spec="{spec_result.spec_path}" data-issue-type="{issue_type}" data-description="{escaped_desc}">
                                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M2.5 3.5a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-11zm2-2a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM0 13a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 16 13V6a1.5 1.5 0 0 0-1.5-1.5h-13A1.5 1.5 0 0 0 0 6v7zm1.5.5A.5.5 0 0 1 1 13V6a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-13z"/>
                                    </svg>
                                    Challenge
                                </button>
                                <div class="challenge-details" data-finding-id="{finding_id}">
                                    <div class="challenge-details-grid">
                                        <div class="challenge-detail-row">
                                            <span class="challenge-detail-label">Challenge Type:</span>
                                            <span class="challenge-detail-value challenge-type"></span>
                                        </div>
                                        <div class="challenge-detail-row">
                                            <span class="challenge-detail-label">Feedback:</span>
                                            <span class="challenge-detail-value challenge-feedback"></span>
                                        </div>
                                        <div class="challenge-detail-row">
                                            <span class="challenge-detail-label">Submitted:</span>
                                            <span class="challenge-detail-value challenge-timestamp"></span>
                                        </div>
                                    </div>
                                </div>
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
                                   pr_metadata: dict = None, categorized_issues: dict = None) -> str:
        """
        Generate a comprehensive report for multi-spec analysis results with enhanced formatting.
        
        Args:
            analysis_result: MultiSpecAnalysisResult with all spec data
            include_html: Whether to include interactive HTML report at the top
            github_client: Optional GitHubClient instance for creating Gist with HTML report (fallback)
            blob_storage_client: Optional BlobStorageClient for uploading to Azure Blob Storage (preferred)
            pr_number: PR number for blob storage upload (required if blob_storage_client provided)
            pr_metadata: Optional dict with PR metadata (title, author, branches, sha, timestamp)
            categorized_issues: Optional dict with categorized issues from AnalyticsManager
            
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
            html_report = self.generate_html_report(analysis_result, pr_metadata=pr_metadata)
            
            # Create a self-contained HTML page with authentication
            html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CVE Spec File Check Report - PR #{pr_number}</title>
    <!-- Favicon to prevent 404 errors -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🛡️%3C/text%3E%3C/svg%3E">
    <style>
        /* ============================================
           CSS VARIABLES - THEME SYSTEM
           ============================================ */
        :root {{
            /* Modern Dark Theme (Default) - Deep Black Shades */
            --bg-primary: #000000;
            --bg-secondary: #0a0a0a;
            --bg-tertiary: #0f0f0f;
            --bg-card: #171717;
            --bg-card-hover: #1f1f1f;
            
            --border-primary: #262626;
            --border-secondary: #333333;
            --border-accent: #404040;
            
            --text-primary: #e5e5e5;
            --text-secondary: #a3a3a3;
            --text-tertiary: #737373;
            
            --accent-blue: #3b82f6;
            --accent-blue-dark: #2563eb;
            --accent-blue-light: #60a5fa;
            --accent-blue-bg: #1e3a8a;
            
            --accent-green: #10b981;
            --accent-green-bg: #064e3b;
            
            --accent-orange: #f59e0b;
            --accent-orange-bg: #78350f;
            
            --accent-red: #ef4444;
            --accent-red-bg: #7f1d1d;
            
            --accent-purple: #8b5cf6;
            --accent-purple-bg: #4c1d95;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
        }}
        
        /* Light Theme Override */
        [data-theme="light"] {{
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --bg-card: #ffffff;
            --bg-card-hover: #f9fafb;
            
            --border-primary: #e5e7eb;
            --border-secondary: #d1d5db;
            --border-accent: #9ca3af;
            
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --text-tertiary: #6b7280;
            
            --accent-blue: #2563eb;
            --accent-blue-dark: #1d4ed8;
            --accent-blue-light: #3b82f6;
            --accent-blue-bg: #dbeafe;
            
            --accent-green: #059669;
            --accent-green-bg: #d1fae5;
            
            --accent-orange: #d97706;
            --accent-orange-bg: #fed7aa;
            
            --accent-red: #dc2626;
            --accent-red-bg: #fee2e2;
            
            --accent-purple: #7c3aed;
            --accent-purple-bg: #ede9fe;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}
        
        * {{
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            min-height: 100vh;
        }}
        
        /* ============================================
           THEME TOGGLE & TOP BAR
           ============================================ */
        #top-bar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-primary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 1000;
            box-shadow: var(--shadow-sm);
        }}
        
        #top-bar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        #top-bar-logo {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        #top-bar-right {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        #theme-toggle {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            color: var(--text-secondary);
            transition: all 0.2s ease;
        }}
        
        #theme-toggle:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-blue);
            color: var(--text-primary);
            transform: translateY(-1px);
        }}
        
        #theme-icon {{
            font-size: 18px;
            display: flex;
            align-items: center;
        }}
        
        /* Adjust body padding for fixed top bar */
        body {{
            padding-top: 80px;
        }}
        
        /* Top Bell Notification */
        #top-bell-container {{
            position: relative;
            cursor: pointer;
            margin-right: 16px;
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 10px;
            transition: all 0.2s ease;
        }}
        
        #top-bell-container:hover {{
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            transform: translateY(-2px);
        }}
        
        #top-bell-container .bell-icon {{
            font-size: 20px;
        }}
        
        #top-bell-badge {{
            position: absolute;
            top: 2px;
            right: 2px;
            background: var(--accent-red);
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 10px;
            min-width: 18px;
            text-align: center;
        }}
        
        /* Auth UI Styles */
        #auth-container {{
            display: flex;
            align-items: center;
        }}
        
        #sign-in-btn {{
            background: linear-gradient(180deg, var(--accent-blue) 0%, var(--accent-blue-dark) 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: var(--shadow-md);
            transition: all 0.2s ease;
        }}
        
        #sign-in-btn:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}
        
        #user-menu {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 6px 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: var(--shadow-sm);
            position: relative;
        }}
        
        #user-avatar {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 2px solid var(--accent-blue);
        }}
        
        #user-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        
        #user-name {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }}
        
        #collaborator-badge {{
            font-size: 10px;
            color: var(--accent-blue);
            background: var(--accent-blue-bg);
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        #sign-out-btn {{
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border-primary);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        #sign-out-btn:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
            border-color: var(--accent-red);
        }}
        
        /* ============================================
           STATS CARDS - Modern Dashboard Style
           ============================================ */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--stat-color), transparent);
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--stat-color);
        }}
        
        .stat-icon {{
            width: 56px;
            height: 56px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
            position: relative;
        }}
        
        .stat-icon-blue {{
            background: var(--accent-blue-bg);
            color: var(--accent-blue);
        }}
        
        .stat-icon-red {{
            background: var(--accent-red-bg);
            color: var(--accent-red);
        }}
        
        .stat-icon-orange {{
            background: var(--accent-orange-bg);
            color: var(--accent-orange);
        }}
        
        .stat-icon-purple {{
            background: var(--accent-purple-bg);
            color: var(--accent-purple);
        }}
        
        .stat-content {{
            flex: 1;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .stat-label {{
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Bell Icon with Animated Badge */
        .bell-container {{
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}
        
        .bell-icon {{
            font-size: 28px;
            animation: bellRing 0.5s ease;
        }}
        
        .bell-badge {{
            position: absolute;
            top: -4px;
            right: -4px;
            background: var(--accent-red);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 12px;
            min-width: 20px;
            text-align: center;
            box-shadow: 0 0 0 2px var(--bg-card);
            animation: badgePop 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
        }}
        
        @keyframes bellRing {{
            0%, 100% {{ transform: rotate(0deg); }}
            25% {{ transform: rotate(15deg); }}
            50% {{ transform: rotate(-15deg); }}
            75% {{ transform: rotate(10deg); }}
        }}
        
        @keyframes badgePop {{
            0% {{ transform: scale(0); }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); }}
        }}
        
        /* ============================================================================
           Spec Details Cards - Modern Design
           ============================================================================ */
        
        .spec-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 16px;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .spec-card:hover {{
            border-color: var(--border-hover);
            background: var(--bg-hover);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }}
        
        .spec-card summary {{
            cursor: pointer;
            padding: 16px 20px;
            font-weight: 600;
            font-size: 16px;
            user-select: none;
            background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-primary) 100%);
            transition: background 0.2s ease;
        }}
        
        .spec-card summary:hover {{
            background: linear-gradient(180deg, var(--bg-hover) 0%, var(--bg-card) 100%);
        }}
        
        .spec-card-content {{
            padding: 20px;
        }}
        
        .spec-file-badge {{
            display: inline-block;
            background: var(--bg-primary);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: var(--accent-blue);
            border: 1px solid var(--border-color);
        }}
        
        /* Issue Type Sections */
        .issue-type-section {{
            margin-bottom: 20px;
            padding: 12px;
            background: var(--bg-primary);
            border-left: 3px solid var(--accent-orange);
            border-radius: 6px;
        }}
        
        .issue-type-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}
        
        .issue-type-title {{
            font-weight: 600;
            color: var(--accent-orange);
            font-size: 14px;
        }}
        
        .issue-count-badge {{
            background: var(--bg-card);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            color: var(--text-secondary);
            font-weight: 600;
            border: 1px solid var(--border-color);
        }}
        
        /* Issue List Items */
        .issue-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .issue-item {{
            padding: 12px;
            margin: 8px 0;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            transition: all 0.2s ease;
            position: relative;
        }}
        
        .issue-item:hover {{
            border-color: var(--border-hover);
            background: var(--bg-hover);
        }}
        
        .issue-item::before {{
            content: "▸";
            position: absolute;
            left: -8px;
            top: 12px;
            color: var(--accent-orange);
            font-weight: bold;
        }}
        
        .issue-text {{
            color: var(--text-primary);
            font-size: 13px;
            line-height: 1.6;
            margin-right: 8px;
        }}
        
        /* Antipattern Details Section */
        .antipattern-details {{
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px;
            margin: 12px 0;
        }}
        
        .antipattern-details summary {{
            cursor: pointer;
            font-weight: 600;
            color: var(--accent-red);
            user-select: none;
            padding: 8px;
            border-radius: 4px;
            transition: background 0.2s ease;
        }}
        
        .antipattern-details summary:hover {{
            background: var(--bg-card);
        }}
        
        /* ============================================================================
           PR Information Card - Modern Design
           ============================================================================ */
        
        .pr-info-card {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-primary) 100%);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}
        
        .pr-info-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .pr-info-icon {{
            font-size: 24px;
            background: var(--accent-blue-bg);
            padding: 10px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .pr-info-title {{
            font-size: 18px;
            font-weight: 600;
            color: var(--accent-blue);
            margin: 0;
        }}
        
        .pr-info-grid {{
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 12px 20px;
            font-size: 14px;
        }}
        
        .pr-info-label {{
            color: var(--text-secondary);
            font-weight: 500;
        }}
        
        .pr-info-value {{
            color: var(--text-primary);
            font-weight: 400;
        }}
        
        .pr-number-badge {{
            display: inline-block;
            background: var(--accent-blue-bg);
            color: var(--accent-blue);
            padding: 4px 12px;
            border-radius: 16px;
            font-weight: 700;
            font-size: 14px;
        }}
        
        .branch-badge {{
            display: inline-block;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: var(--accent-blue);
            font-weight: 500;
        }}
        
        .commit-badge {{
            display: inline-block;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        
        .author-badge {{
            color: var(--accent-blue);
            font-weight: 600;
        }}
        
        .challenge-btn:hover {{
            background: #30363d;
            border-color: #58a6ff;
        }}
        
        /* Modern Challenge Button */
        .challenge-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 500;
            background: linear-gradient(180deg, #21262d 0%, #161b22 100%);
            color: #58a6ff;
            border: 1px solid #30363d;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-left: 10px;
            vertical-align: middle;
        }}
        
        .challenge-btn:hover {{
            background: linear-gradient(180deg, #30363d 0%, #21262d 100%);
            border-color: #58a6ff;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
            transform: translateY(-1px);
        }}
        
        .challenge-btn:active {{
            transform: translateY(0);
        }}
        
        .challenge-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}
        
        .challenge-btn.challenged {{
            background: linear-gradient(180deg, #1f6feb20 0%, #1f6feb10 100%);
            color: #3fb950;
            border-color: #3fb950;
        }}
        
        /* Challenged Item Styling */
        .challenged-item {{
            position: relative;
            opacity: 0.6;
            background: #0d111780 !important;
            border-left: 3px solid #58a6ff !important;
            padding-left: 12px;
            margin: 8px 0;
            border-radius: 6px;
            transition: all 0.3s ease;
        }}
        
        .challenged-item:hover {{
            opacity: 0.8;
            background: #161b2280 !important;
        }}
        
        .challenged-item .issue-text {{
            text-decoration: line-through;
            color: #6e7681 !important;
        }}
        
        .challenged-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background: #1f6feb30;
            color: #58a6ff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
            vertical-align: middle;
        }}
        
        /* Expandable Challenge Details */
        .challenge-details {{
            display: none;
            margin-top: 12px;
            padding: 12px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            font-size: 12px;
            animation: slideDown 0.2s ease;
        }}
        
        .challenge-details.expanded {{
            display: block;
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .challenge-details-grid {{
            display: grid;
            gap: 8px;
        }}
        
        .challenge-detail-row {{
            display: flex;
            gap: 8px;
        }}
        
        .challenge-detail-label {{
            color: #8b949e;
            font-weight: 600;
            min-width: 100px;
        }}
        
        .challenge-detail-value {{
            color: #c9d1d9;
        }}
        
        .challenge-type-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .challenge-type-false-positive {{
            background: #1f883d20;
            color: #3fb950;
        }}
        
        .challenge-type-needs-context {{
            background: #d2992220;
            color: #d29922;
        }}
        
        .challenge-type-acknowledge {{
            background: #f8514920;
            color: #f85149;
        }}
        
        .expand-toggle {{
            cursor: pointer;
            user-select: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: #58a6ff;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
        }}
        
        .expand-toggle:hover {{
            text-decoration: underline;
        }}
        
        .expand-icon {{
            transition: transform 0.2s ease;
        }}
        
        .expand-icon.expanded {{
            transform: rotate(90deg);
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
        
        // ============================================================================
        // Challenge Details Management
        // ============================================================================
        
        function toggleChallengeDetails(findingId) {{
            const detailsDiv = document.querySelector(`.challenge-details[data-finding-id="${{findingId}}"]`);
            const expandIcon = document.querySelector(`li[data-finding-id="${{findingId}}"] .expand-icon`);
            
            if (detailsDiv) {{
                detailsDiv.classList.toggle('expanded');
                if (expandIcon) {{
                    expandIcon.classList.toggle('expanded');
                }}
            }}
        }}
        
        function populateChallengeDetails(findingId, challengeType, feedback) {{
            const detailsDiv = document.querySelector(`.challenge-details[data-finding-id="${{findingId}}"]`);
            
            if (detailsDiv) {{
                const typeLabel = challengeType === 'false-positive' ? 'False Positive' :
                                challengeType === 'needs-context' ? 'Needs Context' : 'Acknowledged';
                const typeClass = `challenge-type-${{challengeType.replace('_', '-')}}`;
                
                detailsDiv.querySelector('.challenge-type').innerHTML = `<span class="challenge-type-badge ${{typeClass}}">${{typeLabel}}</span>`;
                detailsDiv.querySelector('.challenge-feedback').textContent = feedback;
                detailsDiv.querySelector('.challenge-timestamp').textContent = new Date().toLocaleString();
            }}
        }}
        
        function storeChallengeDetails(issueHash, details) {{
            const key = 'radar_challenged_details_pr_{pr_number or 0}';
            const stored = localStorage.getItem(key);
            const allDetails = stored ? JSON.parse(stored) : {{}};
            
            allDetails[issueHash] = details;
            localStorage.setItem(key, JSON.stringify(allDetails));
        }}
        
        function getChallengeDetails(issueHash) {{
            const key = 'radar_challenged_details_pr_{pr_number or 0}';
            const stored = localStorage.getItem(key);
            if (!stored) return null;
            
            const allDetails = JSON.parse(stored);
            return allDetails[issueHash] || null;
        }}
        
        function updateCounters(listItem, delta) {{
            console.log(`📊 Updating counters with delta: ${{delta}}`);
            
            // 1. Update Total Issues counter in stat card and BOTH bell badges
            const totalIssuesCount = document.getElementById('total-issues-count');
            const issuesBadge = document.getElementById('issues-badge');
            const topBellBadge = document.getElementById('top-bell-badge');
            
            if (totalIssuesCount) {{
                const currentTotal = parseInt(totalIssuesCount.textContent) || 0;
                const newTotal = Math.max(0, currentTotal + delta);
                totalIssuesCount.textContent = newTotal;
                console.log(`   ✅ Updated Total Issues: ${{currentTotal}} → ${{newTotal}}`);
                
                // Update both bell badges
                if (issuesBadge) {{
                    issuesBadge.textContent = newTotal;
                }}
                if (topBellBadge) {{
                    topBellBadge.textContent = newTotal;
                }}
                // Trigger bell animation
                animateBellBadge();
            }}
            
            // 2. Update spec-level issue type counter (×count badge)
            // Find the issue type div that contains this list item
            let currentEl = listItem;
            while (currentEl && !currentEl.querySelector('span[style*="border-radius: 10px"]')) {{
                currentEl = currentEl.parentElement;
            }}
            
            if (currentEl) {{
                const counterSpan = currentEl.querySelector('span[style*="border-radius: 10px"]');
                if (counterSpan) {{
                    const match = counterSpan.textContent.match(/×(\d+)/);
                    if (match) {{
                        const currentCount = parseInt(match[1]) || 0;
                        const newCount = Math.max(0, currentCount + delta);
                        counterSpan.textContent = `×${{newCount}}`;
                        console.log(`   ✅ Updated spec-level counter: ×${{currentCount}} → ×${{newCount}}`);
                    }}
                }}
            }}
            
            // 3. Update spec summary text (e.g., "4 errors, 1 warnings")
            // Find the details element containing this spec
            let specDetails = listItem.closest('details[data-spec-name]');
            if (specDetails) {{
                const summarySpan = specDetails.querySelector('.spec-summary');
                if (summarySpan) {{
                    // Parse current summary text like "(4 errors, 1 warnings)"
                    const summaryText = summarySpan.textContent;
                    const errorMatch = summaryText.match(/(\d+)\s+errors?/i);
                    const warningMatch = summaryText.match(/(\d+)\s+warnings?/i);
                    
                    // Determine if this is an error or warning based on the issue type
                    const issueTypeDiv = listItem.closest('div[style*="margin-bottom: 15px"]');
                    const isError = issueTypeDiv && issueTypeDiv.textContent.toLowerCase().includes('error');
                    
                    let newSummary = '';
                    if (errorMatch) {{
                        let errorCount = parseInt(errorMatch[1]) || 0;
                        if (isError) {{
                            errorCount = Math.max(0, errorCount + delta);
                        }}
                        newSummary += `${{errorCount}} error${{errorCount !== 1 ? 's' : ''}}`;
                    }}
                    
                    if (warningMatch) {{
                        let warningCount = parseInt(warningMatch[1]) || 0;
                        if (!isError) {{
                            warningCount = Math.max(0, warningCount + delta);
                        }}
                        if (newSummary) newSummary += ', ';
                        newSummary += `${{warningCount}} warning${{warningCount !== 1 ? 's' : ''}}`;
                    }}
                    
                    summarySpan.textContent = `(${{newSummary}})`;
                    console.log(`   ✅ Updated spec summary: ${{summaryText}} → (${{newSummary}})`);
                }}
            }}
            
            console.log('✅ Counter update complete');
        }}
        
        function restoreChallengedState() {{
            console.log('🔄 Restoring challenged items from localStorage...');
            
            const key = 'radar_challenged_details_pr_{pr_number or 0}';
            const stored = localStorage.getItem(key);
            
            if (!stored) {{
                console.log('   No challenged items to restore');
                return;
            }}
            
            const allDetails = JSON.parse(stored);
            const itemsArray = Object.entries(allDetails);
            
            if (itemsArray.length === 0) {{
                console.log('   No challenged items to restore');
                return;
            }}
            
            console.log(`   Restoring ${{itemsArray.length}} challenged items`);
            
            // Apply challenged state to each item
            itemsArray.forEach(([hash, details]) => {{
                const listItem = document.querySelector(`li.antipattern-item[data-issue-hash="${{hash}}"]`);
                const btn = document.querySelector(`button.challenge-btn[data-issue-hash="${{hash}}"]`);
                
                if (listItem && btn) {{
                    const findingId = listItem.dataset.findingId;
                    
                    // Add challenged class
                    listItem.classList.add('challenged-item');
                    
                    // Update button
                    btn.innerHTML = `
                        <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
                        </svg>
                        Challenged
                    `;
                    btn.classList.add('challenged');
                    btn.disabled = true;
                    
                    // Add badge and expand toggle if not already there
                    const textSpan = listItem.querySelector('.issue-text');
                    if (textSpan && !listItem.querySelector('.challenged-badge')) {{
                        const badge = document.createElement('span');
                        badge.className = 'challenged-badge';
                        badge.innerHTML = '💬 Challenged';
                        textSpan.after(badge);
                        
                        const expandToggle = document.createElement('span');
                        expandToggle.className = 'expand-toggle';
                        expandToggle.innerHTML = '<span class="expand-icon">▶</span> View Details';
                        expandToggle.onclick = () => toggleChallengeDetails(findingId);
                        badge.after(expandToggle);
                    }}
                    
                    // Populate details
                    populateChallengeDetails(findingId, details.type, details.feedback);
                    
                    // Update counters for this challenged item
                    updateCounters(listItem, -1);
                    
                    console.log(`   ✅ Restored challenged state for: ${{hash}}`);
                }}
            }});
            
            console.log('✅ Challenged state restoration complete');
        }}
        
        function initializeChallengeButtons() {{
            const challengeButtons = document.querySelectorAll('.challenge-btn');
            challengeButtons.forEach(btn => {{
                btn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const findingId = btn.dataset.findingId;
                    const issueHash = btn.dataset.issueHash || btn.dataset.findingId;  // Use issue_hash if available
                    const spec = btn.dataset.spec;
                    const issueType = btn.dataset.issueType;
                    const description = btn.dataset.description;
                    
                    openChallengeModal({{
                        findingId,
                        issueHash,
                        spec,
                        issueType,
                        description
                    }});
                }});
            }});
        }}
        
        function openChallengeModal(finding) {{
            console.log('🔍 Opening challenge modal for:', finding);
            
            // Check if user is authenticated
            if (!RADAR_AUTH.isAuthenticated()) {{
                alert('Please sign in to submit challenges');
                RADAR_AUTH.signIn();
                return;
            }}
            
            // Get modal container first
            const modal = document.getElementById('challenge-modal');
            
            // CRITICAL: Check if modal has been corrupted
            if (modal && modal.innerHTML && modal.innerHTML.trim() === '✅ Challenged') {{
                console.error('❌ CRITICAL BUG DETECTED: Modal innerHTML has been corrupted!');
                console.error('   Modal innerHTML should contain form structure, but contains:', modal.innerHTML);
                console.error('   This happens when the challenge button selector accidentally selects the modal.');
                console.error('   You must REFRESH THE PAGE to restore modal functionality.');
                alert('❌ Modal has been corrupted (likely a bug in button selection).\\n\\nPlease REFRESH the page to continue.');
                return;
            }}
            
            console.log('🔍 Modal element details:', {{
                found: !!modal,
                tagName: modal ? modal.tagName : 'N/A',
                id: modal ? modal.id : 'N/A',
                className: modal ? modal.className : 'N/A',
                childCount: modal ? modal.children.length : 0,
                innerHTML_length: modal ? modal.innerHTML.length : 0
            }});
            
            if (!modal) {{
                console.error('❌ CRITICAL: Modal element #challenge-modal not found in DOM!');
                alert('Error: Modal dialog not found. Please refresh the page and try again.');
                return;
            }}
            
            // Log first 500 chars of innerHTML to see what's actually there
            if (modal.innerHTML) {{
                console.log('📄 Modal innerHTML (first 500 chars):', modal.innerHTML.substring(0, 500));
            }} else {{
                console.error('❌ Modal innerHTML is empty or undefined!');
            }}
            
            // Get child elements - try both methods (getElementById and querySelector)
            let specEl = document.getElementById('finding-spec');
            let typeEl = document.getElementById('finding-type');
            let descEl = document.getElementById('finding-desc');
            
            console.log('🔍 Direct getElementById results:', {{
                specEl: !!specEl,
                typeEl: !!typeEl,
                descEl: !!descEl
            }});
            
            // Fallback to querySelector within modal if getElementById fails
            if (!specEl) specEl = modal.querySelector('#finding-spec');
            if (!typeEl) typeEl = modal.querySelector('#finding-type');
            if (!descEl) descEl = modal.querySelector('#finding-desc');
            
            console.log('� After querySelector fallback:', {{
                specEl: !!specEl,
                typeEl: !!typeEl,
                descEl: !!descEl
            }});
            
            // Robust error handling
            if (!specEl || !typeEl || !descEl) {{
                console.error('❌ CRITICAL: Modal child elements missing after both methods!');
                console.error('   Trying alternative query methods...');
                
                // Try finding by class or tag within modal
                const allSpans = modal.getElementsByTagName('span');
                console.log('   Found', allSpans.length, 'span elements in modal');
                
                // Try querySelectorAll
                const spansByQuery = modal.querySelectorAll('span');
                console.log('   querySelectorAll found', spansByQuery.length, 'spans');
                
                alert('Error: Modal is corrupted. Please refresh the page and try again.');
                return;
            }}
            
            // Populate modal with finding data
            console.log('✅ Populating modal with finding data');
            specEl.textContent = finding.spec;
            typeEl.textContent = finding.issueType;
            descEl.textContent = finding.description;
            
            // Store finding data for submission
            modal.dataset.findingId = finding.findingId;
            modal.dataset.issueHash = finding.issueHash || finding.findingId;  // Store issue_hash
            modal.dataset.spec = finding.spec;
            modal.dataset.issueType = finding.issueType;
            modal.dataset.description = finding.description;
            
            console.log('✅ Opening modal with issue_hash:', modal.dataset.issueHash);
            modal.classList.add('active');
        }}
        
        function closeChallengeModal() {{
            console.log('🔒 Closing challenge modal');
            const modal = document.getElementById('challenge-modal');
            const form = document.getElementById('challenge-form');
            
            if (!modal) {{
                console.error('❌ Modal not found when trying to close');
                return;
            }}
            
            // Remove active class to hide modal
            modal.classList.remove('active');
            
            // Reset form if it exists
            if (form) {{
                form.reset();
                console.log('✅ Form reset successfully');
            }} else {{
                console.warn('⚠️  Challenge form not found during close');
            }}
            
            // Clear modal data attributes for next use
            if (modal.dataset) {{
                modal.dataset.findingId = '';
                modal.dataset.issueHash = '';
                modal.dataset.spec = '';
                modal.dataset.issueType = '';
                modal.dataset.description = '';
            }}
            
            console.log('✅ Modal closed successfully');
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
                const headers = RADAR_AUTH.getAuthHeaders();
                
                console.log('📤 Submitting challenge to Azure Function...');
                console.log('   PR Number:', pr_number);
                console.log('   Challenge Type:', challengeType.value);
                console.log('   Has Auth Token:', !!headers.Authorization);
                
                // Create abort controller for timeout
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
                
                const response = await fetch('https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/challenge', {{
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({{
                        pr_number: pr_number,
                        spec_file: modal.dataset.spec,
                        issue_hash: modal.dataset.issueHash,  // Primary identifier
                        antipattern_id: modal.dataset.findingId,  // Legacy field for backwards compatibility
                        challenge_type: challengeType.value,
                        feedback_text: feedbackText
                    }}),
                    signal: controller.signal
                }});
                
                clearTimeout(timeoutId);
                
                console.log('📥 Response received:', response.status, response.statusText);
                
                const result = await response.json();
                
                if (response.ok) {{
                    console.log('✅ Challenge submitted successfully');
                    console.log('   GitHub comment posted:', result.github_comment_posted);
                    console.log('   GitHub label added:', result.github_label_added);
                    if (result.diagnostics) {{
                        console.log('   Diagnostics:', result.diagnostics);
                        console.log('   Bot token loaded:', result.diagnostics.using_bot_token);
                        console.log('   Bot token length:', result.diagnostics.bot_token_length);
                        console.log('   Bot token prefix:', result.diagnostics.bot_token_prefix);
                    }}
                    
                    let message = '✅ Challenge submitted successfully!\\n\\n';
                    message += `Challenge ID: ${{result.challenge_id}}\\n`;
                    
                    if (result.github_comment_posted) {{
                        message += '✅ Comment posted to PR\\n';
                    }} else {{
                        message += '⚠️  Comment posting failed\\n';
                        if (result.diagnostics && result.diagnostics.comment_error) {{
                            message += `   Error: ${{result.diagnostics.comment_error.status_code}} - ${{result.diagnostics.comment_error.message.substring(0, 50)}}...\\n`;
                        }}
                    }}
                    
                    if (result.github_label_added) {{
                        message += '✅ Label added to PR\\n';
                    }} else {{
                        message += '⚠️  Label not added\\n';
                        if (result.diagnostics && result.diagnostics.label_error) {{
                            message += `   Error: ${{result.diagnostics.label_error.status_code}} - ${{result.diagnostics.label_error.message.substring(0, 50)}}...\\n`;
                        }} else {{
                            message += '   Note: Make sure radar-acknowledged label exists in repo\\n';
                        }}
                    }}
                    
                    alert(message);
                    
                    // Apply challenged styling and populate details
                    const findingId = modal.dataset.findingId;
                    const issueHash = modal.dataset.issueHash;
                    
                    console.log('🎨 Applying challenged styling to:', findingId);
                    
                    // Find the list item
                    const listItem = document.querySelector(`li.antipattern-item[data-finding-id="${{findingId}}"]`);
                    const btn = document.querySelector(`button.challenge-btn[data-finding-id="${{findingId}}"]`);
                    
                    if (listItem && btn) {{
                        // Add challenged class
                        listItem.classList.add('challenged-item');
                        
                        // Update button
                        btn.innerHTML = `
                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
                            </svg>
                            Challenged
                        `;
                        btn.classList.add('challenged');
                        btn.disabled = true;
                        
                        // Add expand toggle badge
                        const textSpan = listItem.querySelector('.issue-text');
                        if (textSpan && !listItem.querySelector('.challenged-badge')) {{
                            const badge = document.createElement('span');
                            badge.className = 'challenged-badge';
                            badge.innerHTML = '💬 Challenged';
                            textSpan.after(badge);
                            
                            // Add expand toggle
                            const expandToggle = document.createElement('span');
                            expandToggle.className = 'expand-toggle';
                            expandToggle.innerHTML = '<span class="expand-icon">▶</span> View Details';
                            expandToggle.onclick = () => toggleChallengeDetails(findingId);
                            badge.after(expandToggle);
                        }}
                        
                        // Store challenge data
                        storeChallengeDetails(issueHash, {{
                            type: challengeType.value,
                            feedback: feedbackText,
                            timestamp: new Date().toISOString()
                        }});
                        
                        // Populate details section
                        populateChallengeDetails(findingId, challengeType.value, feedbackText);
                        
                        // Update counters for this newly challenged item
                        updateCounters(listItem, -1);
                        
                        console.log('✅ Challenged styling applied');
                    }} else {{
                        console.warn('⚠️  Could not find list item or button');
                    }}
                    
                    closeChallengeModal();
                }} else {{
                    console.error('❌ Server error:', result);
                    
                    // Handle token expiration specifically
                    if (response.status === 401 || (result.error && result.error.includes('Token expired'))) {{
                        alert('🔐 Your session has expired!\\n\\nPlease sign in again to submit challenges.');
                        closeChallengeModal();
                        RADAR_AUTH.signOut(); // Clear expired token
                        return;
                    }}
                    
                    alert(`❌ Failed to submit challenge: ${{result.error || 'Unknown error'}}`);
                }}
            }} catch (error) {{
                console.error('❌ Challenge submission error:', error);
                
                if (error.name === 'AbortError') {{
                    alert('❌ Request timeout: The server took too long to respond. Please try again.');
                }} else if (error.message.includes('Failed to fetch')) {{
                    alert('❌ Network error: Could not reach the server. Please check:\\n' +
                          '1. Your internet connection\\n' +
                          '2. CORS is configured on the Azure Function\\n' +
                          '3. The Azure Function is running');
                }} else {{
                    alert(`❌ Error: ${{error.message}}`);
                }}
            }} finally {{
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Challenge';
            }}
        }}
        
        // ============================================================================
        // THEME TOGGLE SYSTEM
        // ============================================================================
        
        function initializeTheme() {{
            // Check localStorage for saved theme, default to dark
            const savedTheme = localStorage.getItem('radar_theme') || 'dark';
            applyTheme(savedTheme);
        }}
        
        function toggleTheme() {{
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('radar_theme', newTheme);
        }}
        
        function applyTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            const themeIcon = document.getElementById('theme-icon');
            const themeLabel = document.getElementById('theme-label');
            
            if (theme === 'light') {{
                themeIcon.textContent = '☀️';
                themeLabel.textContent = 'Light';
            }} else {{
                themeIcon.textContent = '🌙';
                themeLabel.textContent = 'Dark';
            }}
        }}
        
        // ============================================================================
        // COUNTER ANIMATIONS
        // ============================================================================
        
        function animateBellBadge() {{
            const badge = document.getElementById('issues-badge');
            const topBadge = document.getElementById('top-bell-badge');
            const bellIcon = document.querySelector('.bell-icon');
            const topBellIcon = document.querySelector('#top-bell-container .bell-icon');
            
            // Animate stats card badge
            if (badge) {{
                badge.style.animation = 'none';
                setTimeout(() => {{
                    badge.style.animation = 'badgePop 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55)';
                }}, 10);
            }}
            
            // Animate top bar badge
            if (topBadge) {{
                topBadge.style.animation = 'none';
                setTimeout(() => {{
                    topBadge.style.animation = 'badgePop 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55)';
                }}, 10);
            }}
            
            // Animate stats card bell icon
            if (bellIcon) {{
                bellIcon.style.animation = 'none';
                setTimeout(() => {{
                    bellIcon.style.animation = 'bellRing 0.5s ease';
                }}, 10);
            }}
            
            // Animate top bar bell icon
            if (topBellIcon) {{
                topBellIcon.style.animation = 'none';
                setTimeout(() => {{
                    topBellIcon.style.animation = 'bellRing 0.5s ease';
                }}, 10);
            }}
        }}
        
        // Initialize modal verification on DOM load
        document.addEventListener('DOMContentLoaded', function() {{
            // Initialize theme on page load
            initializeTheme();
            
            console.log('🔍 Verifying modal structure on page load...');
            
            const modal = document.getElementById('challenge-modal');
            
            if (!modal) {{
                console.error('❌ CRITICAL: Modal container not found!');
                return;
            }}
            
            // Check using querySelector within the modal (works even when display:none)
            const specEl = modal.querySelector('#finding-spec');
            const typeEl = modal.querySelector('#finding-type');
            const descEl = modal.querySelector('#finding-desc');
            const form = modal.querySelector('#challenge-form');
            
            const modalCheck = {{
                modal: !!modal,
                specEl: !!specEl,
                typeEl: !!typeEl,
                descEl: !!descEl,
                form: !!form
            }};
            
            console.log('📋 Modal DOM elements:', modalCheck);
            
            if (Object.values(modalCheck).every(v => v === true)) {{
                console.log('✅ All modal elements loaded successfully');
            }} else {{
                console.error('❌ WARNING: Some modal elements are missing!', modalCheck);
                console.error('   This will prevent challenge submissions from working.');
                console.error('   Modal HTML:', modal.innerHTML.substring(0, 200));
            }}
        }});
    </script>
</head>
<body>
    <!-- Top Navigation Bar -->
    <div id="top-bar">
        <div id="top-bar-left">
            <div id="top-bar-logo">
                🛡️ RADAR Analysis
            </div>
        </div>
        <div id="top-bar-right">
            <!-- Theme Toggle -->
            <button id="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
                <span id="theme-icon">🌙</span>
                <span id="theme-label">Dark</span>
            </button>
            <!-- Bell Notification Icon -->
            <div id="top-bell-container" class="bell-container" title="Total Issues">
                <span class="bell-icon">🔔</span>
                <span id="top-bell-badge" class="bell-badge">0</span>
            </div>
            <!-- Auth UI Container -->
            <div id="auth-container"></div>
        </div>
    </div>
    
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
                report_lines.append(f"### 🔗 <a href=\"{html_url}\" target=\"_blank\" rel=\"noopener noreferrer\">CLICK HERE to open the Interactive HTML Report</a>")
                report_lines.append("")
                report_lines.append("**The report will open in a new tab automatically**")
                report_lines.append("")
                report_lines.append("**Features:**")
                report_lines.append("- 🎯 Interactive anti-pattern detection results")
                report_lines.append("- 🔐 GitHub OAuth sign-in for authenticated challenges")
                report_lines.append("- 💬 Submit feedback and challenges directly from the report")
                report_lines.append("- 📊 Comprehensive analysis with severity indicators")
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
        
        # Add categorized issues breakdown if available
        if categorized_issues:
            report_lines.append("## 🏷️ Issue Status Tracking")
            report_lines.append("")
            report_lines.append("This commit's issues have been categorized based on challenge history:")
            report_lines.append("")
            
            new_count = len(categorized_issues['new_issues'])
            recurring_count = len(categorized_issues['recurring_unchallenged'])
            challenged_count = len(categorized_issues['challenged_issues'])
            resolved_count = len(categorized_issues['resolved_issues'])
            
            report_lines.append(f"| Status | Count | Description |")
            report_lines.append(f"|--------|-------|-------------|")
            report_lines.append(f"| 🆕 **New Issues** | {new_count} | First time detected in this PR |")
            report_lines.append(f"| 🔄 **Recurring Unchallenged** | {recurring_count} | Previously detected but not yet challenged |")
            report_lines.append(f"| ✅ **Previously Challenged** | {challenged_count} | Issues already acknowledged by reviewers |")
            report_lines.append(f"| ✔️ **Resolved** | {resolved_count} | Issues fixed since last commit |")
            report_lines.append("")
            
            # Show actionable issues requiring attention
            unchallenged_total = new_count + recurring_count
            if unchallenged_total > 0:
                report_lines.append(f"⚠️ **{unchallenged_total} issue(s)** require attention (new or recurring unchallenged)")
                report_lines.append("")
            elif challenged_count > 0:
                report_lines.append(f"✅ All {challenged_count} issue(s) have been acknowledged by reviewers")
                report_lines.append("")
            else:
                report_lines.append("🎉 No issues detected in this commit!")
                report_lines.append("")
            
            # Add helpful note
            if challenged_count > 0:
                report_lines.append("> **Note:** Previously challenged issues are not re-flagged. They remain visible for tracking purposes.")
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