#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
HtmlReportGenerator creates interactive HTML reports for CVE spec file analysis.

This module handles all HTML generation logic, including:
- Complete self-contained HTML pages with CSS and JavaScript
- Interactive dashboard components (stats cards, spec details, challenge system)
- Theme system (dark/light mode)
- Authentication UI integration
"""

import html as html_module
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from AntiPatternDetector import Severity

logger = logging.getLogger(__name__)


class HtmlReportGenerator:
    """Generates interactive HTML reports for CVE spec file analysis."""
    
    def __init__(self, severity_color_fn, severity_emoji_fn):
        """
        Initialize the HTML report generator.
        
        Args:
            severity_color_fn: Function to get color code for severity level
            severity_emoji_fn: Function to get emoji for severity level
        """
        self.get_severity_color = severity_color_fn
        self.get_severity_emoji = severity_emoji_fn
    
    def generate_report_body(self, analysis_result, pr_metadata: Optional[dict] = None) -> str:
        """
        Generate the HTML report body (content only, no page wrapper).
        
        Args:
            analysis_result: MultiSpecAnalysisResult with all spec data
            pr_metadata: Optional dict with PR metadata
            
        Returns:
            HTML string with report content
        """
        from AntiPatternDetector import Severity
        
        stats = analysis_result.summary_statistics
        severity_color = self.get_severity_color(analysis_result.overall_severity)
        
        html = f"""
<div style="font-family: 'Orbitron', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg-card); color: var(--text-primary); padding: 20px; border-radius: 12px; border: 1px solid var(--border-primary); box-shadow: var(--shadow-lg);">
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 class="matrix-title" style="color: {severity_color}; margin: 0; font-size: 2.5em; line-height: 1.2;">
            Code Review Analysis Report
        </h1>
        <p style="color: var(--text-secondary); margin: 10px 0 5px 0; font-size: 13px; font-style: italic;">
            Realtime Anti-pattern Detection with AI Reasoning
        </p>
        <p style="color: var(--text-tertiary); margin: 5px 0; font-size: 12px;">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        </p>
    </div>
"""
        
        # Add PR metadata section if provided
        if pr_metadata:
            html += self._generate_pr_info_section(pr_metadata)
        
        # Add stats grid
        html += self._generate_stats_grid(stats, analysis_result.total_issues)
        
        # Add package details
        html += self._generate_spec_cards(analysis_result.spec_results)
        
        html += """
</div>
"""
        return html
    
    def _generate_pr_info_section(self, pr_metadata: dict) -> str:
        """Generate PR information card."""
        pr_number = pr_metadata.get('pr_number', 'Unknown')
        pr_title = html_module.escape(pr_metadata.get('pr_title', 'Unknown'))
        pr_author = html_module.escape(pr_metadata.get('pr_author', 'Unknown'))
        source_branch = html_module.escape(pr_metadata.get('source_branch', 'unknown'))
        target_branch = html_module.escape(pr_metadata.get('target_branch', 'main'))
        source_commit = pr_metadata.get('source_commit_sha', '')[:8]
        
        return f"""
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
    
    def _generate_stats_grid(self, stats: dict, total_issues: int) -> str:
        """Generate statistics cards grid."""
        return f"""
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
        <div class="stat-card filterable-stat" data-filter-severity="ERROR" style="--stat-color: var(--accent-red); cursor: pointer;" title="Click to filter ERROR issues">
            <div class="stat-icon stat-icon-red">
                ⚠️
            </div>
            <div class="stat-content">
                <div class="stat-value">{stats['total_errors']}</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
        
        <!-- Warnings Card -->
        <div class="stat-card filterable-stat" data-filter-severity="WARNING" style="--stat-color: var(--accent-orange); cursor: pointer;" title="Click to filter WARNING issues">
            <div class="stat-icon stat-icon-orange">
                📋
            </div>
            <div class="stat-content">
                <div class="stat-value">{stats['total_warnings']}</div>
                <div class="stat-label">Warnings</div>
            </div>
        </div>
        
        <!-- Total Issues Card with Bell Icon -->
        <div class="stat-card" style="--stat-color: var(--accent-purple);">
            <div class="stat-icon stat-icon-purple">
                <div class="bell-container">
                    <span class="bell-icon">🔔</span>
                    <span class="bell-badge" id="issues-badge">{total_issues}</span>
                </div>
            </div>
            <div class="stat-content">
                <div class="stat-value" id="total-issues-count">{total_issues}</div>
                <div class="stat-label">Total Issues</div>
            </div>
        </div>
    </div>
"""
    
    def _generate_spec_cards(self, spec_results: list) -> str:
        """Generate expandable cards for each spec file."""
        from AntiPatternDetector import Severity
        
        html = ""
        for spec_result in sorted(spec_results, key=lambda x: x.package_name):
            pkg_color = self.get_severity_color(spec_result.severity)
            html += f"""
    <details class="spec-card" data-spec-name="{spec_result.package_name}">
        <summary style="color: {pkg_color};">
            {self.get_severity_emoji(spec_result.severity)} {spec_result.package_name}
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
                html += self._generate_antipattern_section(spec_result)
            
            # Recommended actions
            html += self._generate_recommendations_section(spec_result.anti_patterns)
            
            html += """
        </div>
    </details>
"""
        return html
    
    def _generate_antipattern_section(self, spec_result) -> str:
        """Generate anti-pattern detection results for a spec."""
        issues_by_type = spec_result.get_issues_by_type()
        
        html = """
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
                html += self._generate_issue_item(spec_result.package_name, issue_type, pattern, idx, spec_result.spec_path)
            
            html += """
                        </ul>
                    </div>
"""
        
        html += """
                </div>
            </details>
"""
        return html
    
    def _generate_issue_item(self, package_name: str, issue_type: str, pattern, idx: int, spec_path: str) -> str:
        """Generate a single issue item with challenge button."""
        # Use the issue_hash if available, otherwise fallback to generated ID
        issue_hash = pattern.issue_hash if hasattr(pattern, 'issue_hash') and pattern.issue_hash else f"{package_name}-{issue_type.replace(' ', '-').replace('_', '-')}-{idx}"
        finding_id = issue_hash  # For backwards compatibility in HTML
        
        # Get severity info for badge
        severity_color = self.get_severity_color(pattern.severity)
        severity_name = pattern.severity.name
        severity_emoji = self.get_severity_emoji(pattern.severity)
        
        # Properly escape the description for both HTML content and attributes
        escaped_desc = html_module.escape(pattern.description, quote=True)
        
        return f"""
                            <li class="antipattern-item issue-item" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-severity="{severity_name}">
                                <span class="severity-badge" style="background: {severity_color}20; color: {severity_color}; border: 1px solid {severity_color}40;">
                                    {severity_emoji} {severity_name}
                                </span>
                                <span class="issue-text">{escaped_desc}</span>
                                <button class="challenge-btn" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-spec="{spec_path}" data-issue-type="{issue_type}" data-description="{escaped_desc}">
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
    
    def _generate_recommendations_section(self, anti_patterns: list) -> str:
        """Generate recommended actions section."""
        from AntiPatternDetector import Severity
        
        recommendations = set()
        for pattern in anti_patterns:
            if pattern.severity >= Severity.ERROR:
                recommendations.add(pattern.recommendation)
        
        if not recommendations:
            return ""
        
        html = """
            <details open style="background: var(--bg-tertiary); border: 1px solid var(--border-primary); border-radius: 6px; margin: 10px 0; padding: 10px;">
                <summary style="cursor: pointer; font-weight: bold; color: var(--accent-green); user-select: none;">
                    ✅ Recommended Actions
                </summary>
                <ul style="margin: 10px 0; padding-left: 20px; list-style-type: none;">
"""
        for rec in recommendations:
            html += f"""
                    <li style="color: var(--text-primary); margin: 5px 0; font-size: 13px;">
                        <span style="color: var(--accent-green);">▸</span> {rec}
                    </li>
"""
        html += """
                </ul>
            </details>
"""
        return html
    
    def generate_complete_page(self, report_body: str, pr_number: int) -> str:
        """
        Generate a complete self-contained HTML page with CSS and JavaScript.
        
        Args:
            report_body: The HTML report body content
            pr_number: PR number for the page title
            
        Returns:
            Complete HTML page as string
        """
        css = self._get_css_styles()
        javascript = self._get_javascript(pr_number)
        
        # Generate cache-busting timestamp
        cache_buster = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # NOTE: Replace this data URL with your actual humanoid image converted to base64
        # You can use: https://www.base64-image.de/ to convert your image
        humanoid_image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="report-version" content="{cache_buster}">
    <title>CVE Spec File Check Report - PR #{pr_number}</title>
    <!-- Matrix/Code Style Font -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <!-- Favicon to prevent 404 errors -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🛡️%3C/text%3E%3C/svg%3E">
    <style>
        /* Store humanoid image as CSS variable */
        :root {{
            --humanoid-image: url('{humanoid_image_data}');
        }}
{css}
    </style>
</head>
<body data-report-version="{cache_buster}">
    <!-- Top Navigation Bar -->
    <div id="top-bar">
        <div id="top-bar-left">
            <div id="top-bar-logo">
                <div class="radar-humanoid-container">
                    <div class="radar-humanoid-bg"></div>
                    <span class="radar-title" data-tooltip="Realtime Anti-pattern Detection with AI Reasoning">RADAR</span>
                </div>
            </div>
            <div style="font-size: 10px; color: var(--text-tertiary); margin-left: 12px; font-family: 'Share Tech Mono', monospace;">
                v{cache_buster}
            </div>
        </div>
        <div id="top-bar-right">
            <!-- Bell notification icon -->
            <div id="top-bell-container">
                <span class="bell-icon">🔔</span>
                <span id="top-bell-badge" class="bell-badge">0</span>
            </div>
            
            <!-- Theme Toggle -->
            <button id="theme-toggle" aria-label="Toggle theme">
                <span id="theme-icon">🌙</span>
                <span id="theme-text">Dark</span>
            </button>
            
            <!-- Auth Container -->
            <div id="auth-container">
                <button id="sign-in-btn" style="display: none;">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                    </svg>
                    Sign in with GitHub
                </button>
                <div id="user-menu-container">
                    <div id="user-menu">
                        <img id="user-avatar" src="" alt="User">
                        <div id="user-info">
                            <div id="user-name"></div>
                            <span id="collaborator-badge"></span>
                        </div>
                        <button id="user-menu-toggle" aria-label="User menu">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                            </svg>
                        </button>
                    </div>
                    <div id="user-dropdown" class="dropdown-menu">
                        <button id="sign-out-btn" class="dropdown-item">
                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
                                <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
                            </svg>
                            Sign Out
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Main Content -->
    <div id="main-container">
{report_body}
    </div>
    
    <!-- Challenge Modal -->
    <div id="challenge-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Challenge Finding</h2>
                <button class="modal-close" id="modal-close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <p id="modal-finding-text"></p>
                <div id="challenge-options">
                    <button class="challenge-option" data-type="false-positive">
                        ❌ False Positive
                    </button>
                    <button class="challenge-option" data-type="needs-context">
                        ⚠️ Needs More Context
                    </button>
                    <button class="challenge-option" data-type="disagree-with-severity">
                        ⚡ Disagree with Severity
                    </button>
                </div>
                <textarea id="challenge-feedback" placeholder="Additional feedback (optional)"></textarea>
                <div id="challenge-auth-required" style="display: none;">
                    <p style="color: var(--accent-orange); margin: 10px 0;">
                        ⚠️ Please sign in with GitHub to submit feedback.
                    </p>
                </div>
                <button id="submit-challenge-btn">Submit Feedback</button>
            </div>
        </div>
    </div>
    
    <script>
{javascript}
    </script>
</body>
</html>
"""
    
    def _get_css_styles(self) -> str:
        """Get all CSS styles for the HTML page."""
        return """        /* CSS VARIABLES - THEME SYSTEM */
        :root {
            /* Modern Dark Theme (Default) - Enhanced */
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
            --bg-tertiary: #1a1a1a;
            --bg-card: #161616;
            --bg-card-hover: #202020;
            --bg-hover: rgba(255, 255, 255, 0.05);
            --bg-modal-overlay: rgba(0, 0, 0, 0.85);
            
            --border-primary: #2a2a2a;
            --border-secondary: #333333;
            --border-accent: #404040;
            
            --text-primary: #f0f0f0;
            --text-secondary: #b0b0b0;
            --text-tertiary: #808080;
            
            --accent-blue: #4a9eff;
            --accent-blue-dark: #2563eb;
            --accent-blue-light: #60a5fa;
            --accent-blue-bg: rgba(74, 158, 255, 0.1);
            
            --accent-green: #22c55e;
            --accent-green-bg: rgba(34, 197, 94, 0.1);
            
            --accent-orange: #ff9500;
            --accent-orange-bg: rgba(255, 149, 0, 0.1);
            
            --accent-red: #ff453a;
            --accent-red-bg: rgba(255, 69, 58, 0.1);
            
            --accent-purple: #af52de;
            --accent-purple-bg: rgba(175, 82, 222, 0.1);
            
            --accent-gold: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            
            --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.8);
            --shadow-md: 0 4px 8px -1px rgba(0, 0, 0, 0.8), 0 2px 4px -1px rgba(0, 0, 0, 0.6);
            --shadow-lg: 0 10px 25px -3px rgba(0, 0, 0, 0.8), 0 4px 10px -2px rgba(0, 0, 0, 0.6);
            --shadow-xl: 0 20px 40px -5px rgba(0, 0, 0, 0.9), 0 10px 20px -5px rgba(0, 0, 0, 0.7);
            --shadow-glow: 0 0 20px rgba(74, 158, 255, 0.3);
            
            --humanoid-filter: brightness(1) contrast(1.2);
        }
        
        /* Professional Light Theme with Blue/Purple Accents */
        [data-theme="light"] {
            --bg-primary: #f5f7ff;
            --bg-secondary: #ffffff;
            --bg-tertiary: #e8ecff;
            --bg-card: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
            --bg-card-hover: linear-gradient(135deg, #f8faff 0%, #e8ecff 100%);
            --bg-hover: rgba(99, 102, 241, 0.05);
            --bg-modal-overlay: rgba(0, 0, 0, 0.5);
            
            --border-primary: #d4d8ff;
            --border-secondary: #c1c7ff;
            --border-accent: #a5adff;
            
            --text-primary: #1a1d3a;
            --text-secondary: #4a5178;
            --text-tertiary: #6b7299;
            
            --accent-blue: #4f46e5;
            --accent-blue-dark: #4338ca;
            --accent-blue-light: #6366f1;
            --accent-blue-bg: rgba(99, 102, 241, 0.1);
            
            --accent-green: #059669;
            --accent-green-bg: rgba(5, 150, 105, 0.1);
            
            --accent-orange: #ea580c;
            --accent-orange-bg: rgba(234, 88, 12, 0.1);
            
            --accent-red: #dc2626;
            --accent-red-bg: rgba(220, 38, 38, 0.1);
            
            --accent-purple: #9333ea;
            --accent-purple-bg: rgba(147, 51, 234, 0.1);
            
            --accent-gold: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            
            --shadow-sm: 0 1px 3px 0 rgba(99, 102, 241, 0.08), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px -1px rgba(99, 102, 241, 0.12), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(99, 102, 241, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(99, 102, 241, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.25);
            
            --humanoid-filter: invert(1) hue-rotate(180deg) brightness(1.2);
        }
        
        /* Light theme specific card backgrounds */
        [data-theme="light"] .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%);
        }
        
        [data-theme="light"] .pr-info-card {
            background: linear-gradient(135deg, #fafbff 0%, #e8ecff 100%);
        }
        
        [data-theme="light"] .spec-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 50%, #e8ecff 100%);
        }
        
        [data-theme="light"] .antipattern-details {
            background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
        }
        
        [data-theme="light"] .issue-item {
            background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            margin: 0;
            padding: 20px;
            padding-top: 80px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            min-height: 100vh;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        
        /* Smooth transitions for theme switching */
        body * {
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
        }
        
        /* Matrix-style title font */
        .matrix-title {
            font-family: 'Orbitron', monospace !important;
            font-weight: 900 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase;
            background: linear-gradient(45deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: matrix-glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes matrix-glow {
            from {
                filter: drop-shadow(0 0 10px rgba(74, 158, 255, 0.5));
            }
            to {
                filter: drop-shadow(0 0 20px rgba(175, 82, 222, 0.8));
            }
        }
        
        /* Top Bar Styles */
        #top-bar {
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
            box-shadow: var(--shadow-md);
            backdrop-filter: blur(10px);
            background: rgba(22, 22, 22, 0.95);
        }
        
        [data-theme="light"] #top-bar {
            background: rgba(255, 255, 255, 0.95);
        }
        
        #top-bar-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        #top-bar-logo {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Humanoid Background Container */
        .radar-humanoid-container {
            position: relative;
            display: flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 12px;
            overflow: hidden;
            background: rgba(0, 0, 0, 0.3);
        }
        
        [data-theme="light"] .radar-humanoid-container {
            background: rgba(99, 102, 241, 0.05);
        }
        
        .radar-humanoid-bg {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: var(--humanoid-image);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.15;
            filter: var(--humanoid-filter);
            z-index: 0;
        }
        
        .radar-humanoid-container:hover .radar-humanoid-bg {
            opacity: 0.25;
            animation: pulse-bg 2s ease-in-out infinite;
        }
        
        @keyframes pulse-bg {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        #top-bar-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        #theme-toggle {
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
        }
        
        #theme-toggle:hover {
            background: var(--bg-card-hover);
            border-color: var(--accent-blue);
            color: var(--text-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }
        
        #theme-icon {
            font-size: 18px;
            display: flex;
            align-items: center;
        }
        
        /* Bell Notification */
        #top-bell-container {
            position: relative;
            cursor: pointer;
            margin-right: 16px;
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 10px;
            transition: all 0.2s ease;
        }
        
        #top-bell-container:hover {
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        #top-bell-container .bell-icon {
            font-size: 20px;
            animation: bell-ring 2s ease-in-out infinite;
        }
        
        @keyframes bell-ring {
            0%, 100% { transform: rotate(0); }
            10%, 30% { transform: rotate(-10deg); }
            20%, 40% { transform: rotate(10deg); }
        }
        
        #top-bell-badge {
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
        }
        
        /* Auth UI */
        #auth-container {
            display: flex;
            align-items: center;
        }
        
        #sign-in-btn {
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
        }
        
        #sign-in-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            filter: brightness(1.1);
        }
        
        #user-menu-container {
            position: relative;
        }
        
        #user-menu {
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 8px 12px;
            position: relative;
        }
        
        #user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 2px solid var(--accent-blue);
            object-fit: cover;
        }
        
        #user-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        #user-name {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        #collaborator-badge {
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        #user-menu-toggle {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 6px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        #user-menu-toggle:hover {
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }
        
        .dropdown-menu {
            display: none;
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            box-shadow: var(--shadow-xl);
            min-width: 180px;
            z-index: 1001;
            overflow: hidden;
        }
        
        .dropdown-menu.show {
            display: block;
            animation: slideDown 0.2s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .dropdown-item {
            width: 100%;
            background: transparent;
            border: none;
            padding: 10px 16px;
            text-align: left;
            cursor: pointer;
            color: var(--text-primary);
            font-size: 13px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }
        
        .dropdown-item:hover {
            background: var(--bg-hover);
        }
        
        .dropdown-item svg {
            flex-shrink: 0;
        }
        
        #sign-out-btn:hover {
            color: var(--accent-red);
        }
        
        /* Main Container */
        #main-container {
            max-width: 1400px;
            margin: 0 auto;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* PR Info Card */
        .pr-info-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
        }
        
        .pr-info-card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
        
        .pr-info-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-primary);
        }
        
        .pr-info-icon {
            font-size: 24px;
        }
        
        .pr-info-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }
        
        .pr-info-grid {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 12px 20px;
            align-items: center;
        }
        
        .pr-info-label {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
        }
        
        .pr-info-value {
            font-size: 14px;
            color: var(--text-primary);
        }
        
        .pr-number-badge {
            background: var(--accent-blue-bg);
            color: var(--accent-blue);
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            border: 1px solid var(--accent-blue);
        }
        
        .author-badge {
            background: var(--accent-purple-bg);
            color: var(--accent-purple);
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            border: 1px solid var(--accent-purple);
        }
        
        .branch-badge {
            background: var(--accent-green-bg);
            color: var(--accent-green);
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 600;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            display: inline-block;
            border: 1px solid var(--accent-green);
        }
        
        .commit-badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 4px 10px;
            border-radius: 6px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            display: inline-block;
            border: 1px solid var(--border-primary);
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            align-items: center;
            gap: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--stat-color, var(--accent-blue));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover::before {
            transform: scaleX(1);
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--stat-color, var(--accent-blue));
        }
        
        .stat-card.filter-active {
            background: var(--stat-color, var(--accent-blue));
            background: linear-gradient(135deg, var(--stat-color, var(--accent-blue)), transparent);
            border-color: var(--stat-color, var(--accent-blue));
            box-shadow: 0 0 20px rgba(74, 158, 255, 0.3);
            transform: scale(1.05);
        }
        
        .stat-card.filter-active:hover {
            transform: scale(1.05) translateY(-2px);
        }
        
        .issue-item.filtered-out {
            opacity: 0.2;
            filter: blur(2px);
            pointer-events: none;
            transform: scale(0.95);
        }
        
        .issue-item.filtered-in {
            animation: highlightIssue 0.5s ease-out;
            border-left-color: var(--accent-blue) !important;
            background: linear-gradient(90deg, var(--accent-blue-bg), transparent);
        }
        
        @keyframes highlightIssue {
            0% {
                background: var(--accent-blue-bg);
                transform: translateX(20px);
            }
            100% {
                background: linear-gradient(90deg, var(--accent-blue-bg), transparent);
                transform: translateX(0);
            }
        }
        
        .stat-icon {
            font-size: 36px;
            width: 64px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            background: var(--stat-color, var(--accent-blue-bg));
        }
        
        .stat-icon-blue {
            background: var(--accent-blue-bg);
        }
        
        .stat-icon-red {
            background: var(--accent-red-bg);
        }
        
        .stat-icon-orange {
            background: var(--accent-orange-bg);
        }
        
        .stat-icon-purple {
            background: var(--accent-purple-bg);
        }
        
        .stat-content {
            flex: 1;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: 4px;
            background: var(--accent-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            font-size: 14px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        
        /* Bell Icon in Stats */
        .bell-container {
            position: relative;
            display: inline-flex;
        }
        
        .bell-icon {
            font-size: 36px;
        }
        
        .bell-badge {
            position: absolute;
            top: -4px;
            right: -4px;
            background: var(--accent-red);
            color: white;
            font-size: 12px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 10px;
            min-width: 20px;
            text-align: center;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        /* Spec Cards */
        .spec-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            margin-bottom: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }
        
        .spec-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent-blue);
        }
        
        .spec-card summary {
            cursor: pointer;
            padding: 20px;
            font-weight: 600;
            font-size: 16px;
            user-select: none;
            background: linear-gradient(135deg, var(--bg-card), var(--bg-tertiary));
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .spec-card summary:hover {
            background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-card));
        }
        
        .spec-card summary::marker {
            content: '';
        }
        
        .spec-card summary::before {
            content: '▶';
            font-size: 12px;
            transition: transform 0.2s ease;
            color: var(--accent-blue);
            display: inline-block;
        }
        
        .spec-card[open] summary::before {
            transform: rotate(90deg);
        }
        
        .spec-summary {
            color: var(--text-secondary);
            font-weight: normal;
            font-size: 14px;
            margin-left: auto;
        }
        
        .spec-card-content {
            padding: 0 20px 20px 20px;
            background: var(--bg-secondary);
        }
        
        .spec-file-badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 6px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            display: inline-block;
            border: 1px solid var(--border-primary);
        }
        
        /* Anti-pattern Details */
        .antipattern-details {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-left: 3px solid var(--accent-purple);
            border-radius: 10px;
            margin: 16px 0;
            padding: 12px;
        }
        
        .antipattern-details summary {
            cursor: pointer;
            font-weight: bold;
            color: var(--text-primary);
            user-select: none;
            padding: 12px 16px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--accent-purple-bg), transparent);
            border: 1px solid var(--accent-purple);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .antipattern-details summary:hover {
            background: var(--accent-purple-bg);
            transform: translateX(4px);
        }
        
        .antipattern-details summary::marker {
            content: '';
        }
        
        .antipattern-details summary::before {
            content: '▶';
            font-size: 10px;
            transition: transform 0.2s ease;
            color: var(--accent-purple);
            display: inline-block;
        }
        
        .antipattern-details[open] summary::before {
            transform: rotate(90deg);
        }
        
        /* Issue Type Sections */
        .issue-type-section {
            margin: 16px 0;
            background: transparent;
            border-radius: 8px;
        }
        
        .issue-type-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-primary);
            margin-bottom: 12px;
        }
        
        .issue-type-title {
            font-weight: 600;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .issue-count-badge {
            background: var(--accent-purple-bg);
            color: var(--accent-purple);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid var(--accent-purple);
        }
        
        /* Issue List Items */
        .issue-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .issue-item {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-left: 3px solid var(--accent-blue);
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .issue-item:hover {
            background: var(--bg-card-hover);
            border-left-width: 5px;
            transform: translateX(4px);
            box-shadow: var(--shadow-md);
        }
        
        .issue-item::before {
            display: none;
        }
        
        .severity-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            flex-shrink: 0;
            box-shadow: var(--shadow-sm);
        }
        
        .issue-text {
            flex: 1;
            color: var(--text-primary);
            font-size: 14px;
            line-height: 1.6;
        }
        
        .challenge-btn {
            background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-card));
            border: 1px solid var(--border-primary);
            color: var(--text-secondary);
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        
        .challenge-btn:hover {
            background: linear-gradient(135deg, var(--accent-blue-bg), var(--accent-blue));
            border-color: var(--accent-blue);
            color: white;
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .challenge-btn svg {
            width: 14px;
            height: 14px;
        }
        
        .challenge-btn.challenged {
            background: var(--accent-green-bg);
            border-color: var(--accent-green);
            color: var(--accent-green);
            cursor: not-allowed;
        }
        
        .challenge-details {
            display: none;
            margin-top: 12px;
            padding: 12px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            box-shadow: inset var(--shadow-sm);
        }
        
        .challenge-details.visible {
            display: block;
            animation: slideDown 0.3s ease;
        }
        
        .challenge-details-grid {
            display: grid;
            gap: 8px;
        }
        
        .challenge-detail-row {
            display: grid;
            grid-template-columns: 140px 1fr;
            gap: 12px;
        }
        
        .challenge-detail-label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
        }
        
        .challenge-detail-value {
            font-size: 12px;
            color: var(--text-primary);
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-modal-overlay);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
        }
        
        .modal.visible {
            display: flex;
            animation: fadeIn 0.2s ease;
        }
        
        .modal-content {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 16px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: var(--shadow-xl);
            animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px;
            border-bottom: 1px solid var(--border-primary);
            background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-card));
        }
        
        .modal-header h2 {
            margin: 0;
            font-size: 20px;
            color: var(--text-primary);
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 28px;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 0;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        
        .modal-close:hover {
            background: var(--bg-hover);
            color: var(--accent-red);
            transform: rotate(90deg);
        }
        
        .modal-body {
            padding: 24px;
        }
        
        #modal-finding-text {
            background: var(--bg-tertiary);
            padding: 16px;
            border-radius: 8px;
            border-left: 3px solid var(--accent-blue);
            margin-bottom: 20px;
            color: var(--text-primary);
            font-size: 14px;
            line-height: 1.6;
        }
        
        #challenge-options {
            display: grid;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .challenge-option {
            background: var(--bg-tertiary);
            border: 2px solid var(--border-primary);
            color: var(--text-primary);
            padding: 14px 18px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s ease;
        }
        
        .challenge-option:hover {
            border-color: var(--accent-blue);
            background: var(--bg-card-hover);
            transform: translateX(4px);
        }
        
        .challenge-option.selected {
            background: var(--accent-blue-bg);
            border-color: var(--accent-blue);
            color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
        }
        
        #challenge-feedback {
            width: 100%;
            min-height: 120px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            color: var(--text-primary);
            padding: 14px;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            margin-bottom: 16px;
            transition: all 0.2s ease;
        }
        
        #challenge-feedback:focus {
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
        }
        
        #submit-challenge-btn {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-blue-dark));
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        #submit-challenge-btn:hover:not(:disabled) {
            background: linear-gradient(135deg, var(--accent-blue-light), var(--accent-blue));
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        #submit-challenge-btn:disabled {
            background: var(--bg-tertiary);
            color: var(--text-tertiary);
            cursor: not-allowed;
            transform: none;
        }
        
        /* RADAR Branding */
        .radar-title {
            font-weight: 900;
            font-style: italic;
            font-size: 1.5em;
            letter-spacing: 0.05em;
            background: var(--accent-gold);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            cursor: help;
            display: inline-block;
            transition: all 0.3s ease;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            z-index: 1;
        }
        
        .radar-title:hover {
            transform: scale(1.05);
            filter: brightness(1.2);
        }
        
        .radar-title::after {
            content: attr(data-tooltip);
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%) translateY(8px);
            background: var(--bg-card);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.7em;
            font-weight: 600;
            font-style: normal;
            letter-spacing: normal;
            white-space: nowrap;
            max-width: 300px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-xl);
            border: 1px solid var(--accent-gold);
            z-index: 10000;
        }
        
        .radar-title:hover::after {
            opacity: 1;
            transform: translateX(-50%) translateY(12px);
        }
        
        /* Smooth scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-tertiary);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border-accent);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-blue);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .pr-info-grid {
                grid-template-columns: 1fr;
            }
            
            #top-bar {
                padding: 0 12px;
            }
            
            .radar-title {
                font-size: 1.2em;
            }
            
            .radar-humanoid-container {
                padding: 4px 8px;
            }
        }"""
    
    def _get_javascript(self, pr_number: int) -> str:
        """Get all JavaScript code for the HTML page."""
        js_code = """        // ============================================================================
        // RADAR Authentication Module
        // ============================================================================
        
        const RADAR_AUTH = (() => {
            const GITHUB_CLIENT_ID = 'Ov23limFwlBEPDQzgGmb';
            const AUTH_CALLBACK_URL = 'https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/auth/callback';
            const STORAGE_KEY = 'radar_auth_token';
            const USER_KEY = 'radar_user_info';
            
            // Get current user from localStorage
            function getCurrentUser() {
                const userJson = localStorage.getItem(USER_KEY);
                return userJson ? JSON.parse(userJson) : null;
            }
            
            // Get auth token from localStorage
            function getAuthToken() {
                return localStorage.getItem(STORAGE_KEY);
            }
            
            // Check if user is authenticated
            function isAuthenticated() {
                return !!getAuthToken();
            }
            
            // Initiate GitHub OAuth login
            function signIn() {
                const currentUrl = window.location.href.split('#')[0];
                const state = encodeURIComponent(currentUrl);
                const authUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(AUTH_CALLBACK_URL)}&scope=read:user%20read:org&state=${state}`;
                
                console.log('🔐 Redirecting to GitHub OAuth...');
                window.location.href = authUrl;
            }
            
            // Sign out
            function signOut() {
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem(USER_KEY);
                console.log('👋 Signed out');
                updateUI();
            }
            
            // Handle auth callback (extract token from URL fragment)
            function handleAuthCallback() {
                const fragment = window.location.hash.substring(1);
                const params = new URLSearchParams(fragment);
                const token = params.get('token');
                
                if (token) {
                    console.log('🎫 Token received from OAuth callback');
                    localStorage.setItem(STORAGE_KEY, token);
                    
                    // Decode JWT to get user info (simple base64 decode, not verification)
                    try {
                        const payload = JSON.parse(atob(token.split('.')[1]));
                        localStorage.setItem(USER_KEY, JSON.stringify({
                            username: payload.username,
                            email: payload.email,
                            name: payload.name,
                            avatar_url: payload.avatar_url,
                            is_collaborator: payload.is_collaborator,
                            is_admin: payload.is_admin
                        }));
                        console.log('✅ User authenticated:', payload.username);
                    } catch (e) {
                        console.error('Failed to decode token:', e);
                    }
                    
                    // Clean up URL
                    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
                    updateUI();
                }
            }
            
            // Update UI based on auth state
            function updateUI() {
                const user = getCurrentUser();
                const userMenuContainer = document.getElementById('user-menu-container');
                const signInBtn = document.getElementById('sign-in-btn');
                
                if (!userMenuContainer || !signInBtn) return;
                
                if (user) {
                    // Show user menu
                    userMenuContainer.style.display = 'block';
                    signInBtn.style.display = 'none';
                    
                    // Populate user data
                    const avatarEl = document.getElementById('user-avatar');
                    const nameEl = document.getElementById('user-name');
                    const badgeEl = document.getElementById('collaborator-badge');
                    
                    if (avatarEl) avatarEl.src = user.avatar_url;
                    if (nameEl) nameEl.textContent = user.name || user.username;
                    
                    if (badgeEl) {
                        let roleIcon = '';
                        let roleText = '';
                        let roleColor = '';
                        
                        if (user.is_admin) {
                            roleIcon = '🔴';
                            roleText = 'Admin';
                            roleColor = '#ef4444';
                        } else if (user.is_collaborator) {
                            roleIcon = '🟢';
                            roleText = 'Collaborator';
                            roleColor = '#22c55e';
                        } else {
                            roleIcon = '🟠';
                            roleText = 'PR Owner';
                            roleColor = '#fb8500';
                        }
                        
                        badgeEl.textContent = `${roleIcon} ${roleText}`;
                        badgeEl.style.color = roleColor;
                        badgeEl.style.background = `${roleColor}20`;
                    }
                } else {
                    // Show sign-in button
                    userMenuContainer.style.display = 'none';
                    signInBtn.style.display = 'flex';
                }
            }
            
            // Get auth headers for API requests
            function getAuthHeaders() {
                const token = getAuthToken();
                return token ? {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                } : {
                    'Content-Type': 'application/json'
                };
            }
            
            // Initialize on page load
            function init() {
                console.log('🚀 RADAR Auth initialized');
                handleAuthCallback();
                updateUI();
            }
            
            // Public API
            return {
                init,
                signIn,
                signOut,
                isAuthenticated,
                getCurrentUser,
                getAuthToken,
                getAuthHeaders
            };
        })();
        
        // Wrap all code in DOMContentLoaded to ensure DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
        
        // Initialize RADAR Auth
        RADAR_AUTH.init();
        
        // Theme Management
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const themeText = document.getElementById('theme-text');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            // Update button to show what mode you can switch TO
            if (theme === 'dark') {
                themeIcon.textContent = '☀️';
                themeText.textContent = 'Light';
            } else {
                themeIcon.textContent = '🌙';
                themeText.textContent = 'Dark';
            }
        }
        
        // Load saved theme or default to dark
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
        
        // Attach Sign In button event listener
        const signInBtn = document.getElementById('sign-in-btn');
        if (signInBtn) {
            signInBtn.addEventListener('click', () => RADAR_AUTH.signIn());
        }
        
        // Dropdown toggle functionality
        const userMenuToggle = document.getElementById('user-menu-toggle');
        const userDropdown = document.getElementById('user-dropdown');
        
        if (userMenuToggle && userDropdown) {
            userMenuToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                userDropdown.classList.toggle('show');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!userMenuToggle.contains(e.target) && !userDropdown.contains(e.target)) {
                    userDropdown.classList.remove('show');
                }
            });
        }
        
        // Attach Sign Out button event listener
        const signOutBtn = document.getElementById('sign-out-btn');
        if (signOutBtn) {
            signOutBtn.addEventListener('click', () => {
                userDropdown.classList.remove('show');
                RADAR_AUTH.signOut();
            });
        }
        
        // Challenge Modal Management
        let currentFindingId = null;
        let currentIssueHash = null;
        let currentSpec = null;
        let currentIssueType = null;
        let currentDescription = null;
        
        function openChallengeModal(findingId, issueHash, spec, issueType, description) {
            currentFindingId = findingId;
            currentIssueHash = issueHash;
            currentSpec = spec;
            currentIssueType = issueType;
            currentDescription = description;
            
            document.getElementById('modal-finding-text').textContent = description;
            document.getElementById('challenge-modal').classList.add('visible');
            
            // Reset form
            document.querySelectorAll('.challenge-option').forEach(btn => btn.classList.remove('selected'));
            document.getElementById('challenge-feedback').value = '';
        }
        
        function closeChallengeModal() {
            document.getElementById('challenge-modal').classList.remove('visible');
        }
        
        // Attach close button event listener
        document.getElementById('modal-close-btn').addEventListener('click', closeChallengeModal);
        
        // Challenge option selection
        document.querySelectorAll('.challenge-option').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.challenge-option').forEach(b => b.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
        
        // Submit challenge to Azure Function
        async function submitChallenge() {
            // Check authentication first
            if (!RADAR_AUTH.isAuthenticated()) {
                alert('Please sign in to submit challenges');
                RADAR_AUTH.signIn();
                return;
            }
            
            const selectedOption = document.querySelector('.challenge-option.selected');
            if (!selectedOption) {
                alert('Please select a feedback type');
                return;
            }
            
            const challengeType = selectedOption.getAttribute('data-type');
            const feedback = document.getElementById('challenge-feedback').value.trim();
            
            if (!feedback) {
                alert('Please provide an explanation');
                return;
            }
            
            const submitBtn = document.getElementById('submit-challenge-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {
                const pr_number = {pr_number};
                const headers = RADAR_AUTH.getAuthHeaders();
                
                console.log('📤 Submitting challenge to Azure Function...');
                
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 15000);
                
                const response = await fetch('https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/challenge', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({
                        pr_number: pr_number,
                        spec_file: currentSpec,
                        issue_hash: currentIssueHash,
                        antipattern_id: currentFindingId,
                        challenge_type: challengeType,
                        feedback_text: feedback
                    }),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                const result = await response.json();
                
                if (response.ok) {
                    console.log('✅ Challenge submitted successfully');
                    
                    let message = '✅ Challenge submitted successfully!\\n\\n';
                    message += `Challenge ID: ${result.challenge_id}\\n`;
                    
                    if (result.github_comment_posted) {
                        message += '✅ Comment posted to PR\\n';
                    }
                    if (result.github_label_added) {
                        message += '✅ Label added to PR\\n';
                    }
                    
                    alert(message);
                    
                    // Update button UI
                    const btn = document.querySelector(`button.challenge-btn[data-finding-id="${currentFindingId}"]`);
                    if (btn) {
                        btn.textContent = '✅ Challenged';
                        btn.disabled = true;
                        btn.classList.add('challenged');
                    }
                    
                    // Update issue counters dynamically
                    const totalIssuesEl = document.getElementById('total-issues-count');
                    const bellBadge = document.getElementById('top-bell-badge');
                    const issuesBadge = document.getElementById('issues-badge');
                    
                    if (totalIssuesEl) {
                        const currentCount = parseInt(totalIssuesEl.textContent) || 0;
                        const newCount = Math.max(0, currentCount - 1);
                        totalIssuesEl.textContent = newCount;
                        console.log(`📊 Updated total issues: ${currentCount} → ${newCount}`);
                    }
                    
                    if (bellBadge) {
                        const currentCount = parseInt(bellBadge.textContent) || 0;
                        const newCount = Math.max(0, currentCount - 1);
                        bellBadge.textContent = newCount;
                    }
                    
                    if (issuesBadge) {
                        const currentCount = parseInt(issuesBadge.textContent) || 0;
                        const newCount = Math.max(0, currentCount - 1);
                        issuesBadge.textContent = newCount;
                    }
                    
                    closeChallengeModal();
                } else {
                    console.error('❌ Server error:', result);
                    
                    if (response.status === 401) {
                        alert('🔐 Your session has expired!\\n\\nPlease sign in again.');
                        RADAR_AUTH.signOut();
                        return;
                    }
                    
                    alert(`❌ Failed to submit challenge: ${result.error || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('❌ Challenge submission error:', error);
                
                if (error.name === 'AbortError') {
                    alert('❌ Request timeout: Server took too long to respond.');
                } else {
                    alert(`❌ Error: ${error.message}`);
                }
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Feedback';
            }
        }
        
        // Attach submit button event listener
        document.getElementById('submit-challenge-btn').addEventListener('click', submitChallenge);
        
        // Attach challenge buttons
        document.querySelectorAll('.challenge-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const findingId = this.getAttribute('data-finding-id');
                const issueHash = this.getAttribute('data-issue-hash');
                const spec = this.getAttribute('data-spec');
                const issueType = this.getAttribute('data-issue-type');
                const description = this.getAttribute('data-description');
                openChallengeModal(findingId, issueHash, spec, issueType, description);
            });
        });
        
        // Bell notification update
        function updateCounters() {
            const totalIssuesEl = document.getElementById('total-issues-count');
            const topBellBadge = document.getElementById('top-bell-badge');
            const issuesBadge = document.getElementById('issues-badge');
            
            if (totalIssuesEl) {
                const totalIssues = totalIssuesEl.textContent;
                if (issuesBadge) issuesBadge.textContent = totalIssues;
                if (topBellBadge) topBellBadge.textContent = totalIssues;
            }
        }
        
        updateCounters();
        
        // Severity filtering functionality
        let activeSeverityFilter = null;
        
        document.querySelectorAll('.filterable-stat').forEach(card => {
            card.addEventListener('click', function() {
                const severity = this.getAttribute('data-filter-severity');
                
                // Toggle filter
                if (activeSeverityFilter === severity) {
                    // Clear filter
                    activeSeverityFilter = null;
                    this.classList.remove('filter-active');
                    document.querySelectorAll('.issue-item').forEach(item => {
                        item.classList.remove('filtered-out', 'filtered-in');
                    });
                } else {
                    // Apply new filter
                    activeSeverityFilter = severity;
                    
                    // Update active stat card
                    document.querySelectorAll('.filterable-stat').forEach(c => c.classList.remove('filter-active'));
                    this.classList.add('filter-active');
                    
                    // Filter and highlight issues
                    let firstMatchingIssue = null;
                    document.querySelectorAll('.issue-item').forEach(item => {
                        const itemSeverity = item.getAttribute('data-severity');
                        if (itemSeverity === severity) {
                            item.classList.remove('filtered-out');
                            item.classList.add('filtered-in');
                            if (!firstMatchingIssue) {
                                firstMatchingIssue = item;
                            }
                        } else {
                            item.classList.add('filtered-out');
                            item.classList.remove('filtered-in');
                        }
                    });
                    
                    // Scroll to first matching issue with smooth animation
                    if (firstMatchingIssue) {
                        setTimeout(() => {
                            firstMatchingIssue.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'center' 
                            });
                        }, 100);
                    }
                }
            });
        });
        
        // Close modal on outside click
        document.getElementById('challenge-modal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeChallengeModal();
            }
        });
        
        // Add smooth scroll behavior for all internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Add keyboard shortcut support
        document.addEventListener('keydown', function(e) {
            // Escape to close modal
            if (e.key === 'Escape') {
                const modal = document.getElementById('challenge-modal');
                if (modal && modal.classList.contains('visible')) {
                    closeChallengeModal();
                }
            }
            
            // Ctrl/Cmd + K to toggle theme
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                themeToggle.click();
            }
        });
        
        }); // End DOMContentLoaded"""
        
        # Replace the pr_number placeholder with actual value
        return js_code.replace('{pr_number}', str(pr_number))