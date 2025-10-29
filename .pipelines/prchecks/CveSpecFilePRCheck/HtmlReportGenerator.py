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
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; border-radius: 6px; border: 1px solid #30363d;">
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: {severity_color}; margin: 0;">
            {self.get_severity_emoji(analysis_result.overall_severity)} CVE Spec File Analysis Report
        </h2>
        <p style="color: #8b949e; margin: 5px 0; font-size: 12px;">
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
                <div class="stat-value">{stats['specs_with_errors']}</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
        
        <!-- Warnings Card -->
        <div class="stat-card filterable-stat" data-filter-severity="WARNING" style="--stat-color: var(--accent-orange); cursor: pointer;" title="Click to filter WARNING issues">
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
                                        <path d="M2.5 3.5a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0-1h-11zm2-2a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM0 13a1.5 1.5 0 0 0 1.5 1.5h13A1.5 1.5 0 0 0 16 13V6a1.5 1.5 0 0 0-1.5-1.5h-13A1.5 1.5 0 0 0 0 6v7zm1.5.5A.5.5 0 0 1 1 13V6a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-13z"/>
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
        javascript = self._get_javascript()
        
        # Generate cache-busting timestamp
        cache_buster = datetime.now().strftime('%Y%m%d%H%M%S')
        
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
    <!-- Favicon to prevent 404 errors -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🛡️%3C/text%3E%3C/svg%3E">
    <style>
{css}
    </style>
</head>
<body data-report-version="{cache_buster}">
    <!-- Top Navigation Bar -->
    <div id="top-bar">
        <div id="top-bar-left">
            <div id="top-bar-logo">
                <span>🛡️</span>
                <span>CVE Spec Analysis</span>
            </div>
            <div style="font-size: 10px; color: var(--text-tertiary); margin-left: 12px; font-family: monospace;">
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
                    <button class="challenge-option" data-type="false_alarm">
                        🔴 False Alarm
                    </button>
                    <button class="challenge-option" data-type="agree">
                        🟢 Agree with Finding
                    </button>
                    <button class="challenge-option" data-type="needs_context">
                        🟡 Needs More Context
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
        # This would contain the full CSS - for now, returning a placeholder
        # In production, you'd import this from a separate file or template
        return """        /* CSS VARIABLES - THEME SYSTEM */
        :root {
            /* Modern Dark Theme (Default) - Deep Black Shades */
            --bg-primary: #000000;
            --bg-secondary: #0a0a0a;
            --bg-tertiary: #0f0f0f;
            --bg-card: #171717;
            --bg-card-hover: #1f1f1f;
            --bg-hover: rgba(31, 31, 31, 0.8);
            
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
        }
        
        /* Light Theme Override */
        [data-theme="light"] {
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --bg-card: #ffffff;
            --bg-card-hover: #f9fafb;
            --bg-hover: rgba(249, 250, 251, 0.9);
            
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
        }
        
        * {
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }
        
        body {
            margin: 0;
            padding: 20px;
            padding-top: 80px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            min-height: 100vh;
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
            box-shadow: var(--shadow-sm);
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
            gap: 8px;
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
        }
        
        #top-bell-container .bell-icon {
            font-size: 20px;
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
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            min-width: 180px;
            z-index: 1001;
            overflow: hidden;
        }
        
        .dropdown-menu.show {
            display: block;
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
            background: var(--bg-card-hover);
        }
        
        .dropdown-item svg {
            flex-shrink: 0;
        }
        
        #user-menu-container {
            position: relative;
        }
        
        #sign-out-btn:hover {
            color: var(--accent-red);
        }
        
        /* PR Info Card */
        .pr-info-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
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
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .author-badge {
            background: var(--accent-purple-bg);
            color: var(--accent-purple);
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .branch-badge {
            background: var(--accent-green-bg);
            color: var(--accent-green);
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        
        .commit-badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 2px 8px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(88, 166, 255, 0.1);
            border-color: rgba(88, 166, 255, 0.3);
        }
        
        .stat-card.filter-active {
            background: rgba(88, 166, 255, 0.15);
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
            transform: scale(1.05);
        }
        
        .stat-card.filter-active:hover {
            transform: scale(1.05) translateY(-2px);
        }
        
        .issue-item.filtered-out {
            opacity: 0.3;
            filter: blur(1px);
            pointer-events: none;
        }
        
        .issue-item.filtered-in {
            animation: highlightIssue 0.5s ease-out;
            border-left-color: rgba(88, 166, 255, 0.8) !important;
            background: rgba(88, 166, 255, 0.1);
        }
        
        @keyframes highlightIssue {
            0% {
                background: rgba(88, 166, 255, 0.3);
                transform: translateX(10px);
            }
            100% {
                background: rgba(88, 166, 255, 0.1);
                transform: translateX(0);
            }
        }
        
        .stat-icon {
            font-size: 36px;
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
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
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 14px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
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
        }
        
        /* Spec Cards */
        .spec-card {
            background: rgba(23, 23, 23, 0.6);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            margin-bottom: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .spec-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(88, 166, 255, 0.1);
            border-color: rgba(88, 166, 255, 0.3);
        }
        
        .spec-card summary {
            cursor: pointer;
            padding: 16px 20px;
            font-weight: 600;
            font-size: 16px;
            user-select: none;
            background: rgba(88, 166, 255, 0.08);
            border: 1px solid rgba(88, 166, 255, 0.2);
            border-radius: 8px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .spec-card summary:hover {
            background: rgba(88, 166, 255, 0.15);
            border-color: rgba(88, 166, 255, 0.3);
            transform: translateY(-1px);
        }
        
        .spec-card summary::marker {
            content: '';
        }
        
        .spec-card summary::before {
            content: '▶';
            font-size: 12px;
            transition: transform 0.2s ease;
            color: var(--accent-blue);
        }
        
        .spec-card[open] summary::before {
            transform: rotate(90deg);
        }
        
        .spec-card-content {
            padding: 0 20px 20px 20px;
            background: rgba(13, 13, 13, 0.4);
        }
        
        .spec-file-badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        
        /* Anti-pattern Details */
        .antipattern-details {
            background: rgba(13, 13, 13, 0.3);
            border: 1px solid var(--border-primary);
            border-left: 3px solid var(--accent-purple);
            border-radius: 10px;
            margin: 10px 0;
            padding: 10px;
        }
        
        .antipattern-details summary {
            cursor: pointer;
            font-weight: bold;
            color: var(--text-primary);
            user-select: none;
            padding: 10px 12px;
            border-radius: 6px;
            background: rgba(163, 113, 247, 0.08);
            border: 1px solid rgba(163, 113, 247, 0.2);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .antipattern-details summary:hover {
            background: rgba(163, 113, 247, 0.15);
            border-color: rgba(163, 113, 247, 0.3);
            transform: translateX(2px);
        }
        
        .antipattern-details summary::marker {
            content: '';
        }
        
        .antipattern-details summary::before {
            content: '▶';
            font-size: 10px;
            transition: transform 0.2s ease;
            color: var(--accent-purple);
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
            background: rgba(163, 113, 247, 0.15);
            color: var(--accent-purple);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        /* Issue List Items */
        .issue-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .issue-item {
            background: transparent;
            border: 1px solid transparent;
            border-left: 2px solid transparent;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .issue-item:hover {
            background: var(--bg-hover);
            border-left-color: rgba(88, 166, 255, 0.6);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        .issue-item::before {
            display: none;
        }
        
        .severity-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        .issue-text {
            flex: 1;
            color: var(--text-primary);
            font-size: 14px;
            line-height: 1.5;
        }
        
        .challenge-btn {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        
        .challenge-btn:hover {
            background: var(--accent-blue-bg);
            border-color: var(--accent-blue);
            color: var(--accent-blue);
        }
        
        .challenge-btn svg {
            width: 14px;
            height: 14px;
        }
        
        .challenge-details {
            display: none;
            margin-top: 12px;
            padding: 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 6px;
        }
        
        .challenge-details.visible {
            display: block;
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
            background: rgba(0, 0, 0, 0.8);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.visible {
            display: flex;
        }
        
        .modal-content {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid var(--border-primary);
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
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .modal-close:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }
        
        .modal-body {
            padding: 20px;
        }
        
        #modal-finding-text {
            background: var(--bg-tertiary);
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid var(--accent-blue);
            margin-bottom: 20px;
            color: var(--text-primary);
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
            padding: 12px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }
        
        .challenge-option:hover {
            border-color: var(--accent-blue);
            background: var(--bg-card-hover);
        }
        
        .challenge-option.selected {
            background: var(--accent-blue-bg);
            border-color: var(--accent-blue);
            color: var(--accent-blue);
        }
        
        #challenge-feedback {
            width: 100%;
            min-height: 100px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            color: var(--text-primary);
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            margin-bottom: 16px;
        }
        
        #challenge-feedback:focus {
            outline: none;
            border-color: var(--accent-blue);
        }
        
        #submit-challenge-btn {
            background: var(--accent-blue);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s ease;
        }
        
        #submit-challenge-btn:hover {
            background: var(--accent-blue-dark);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        #submit-challenge-btn:disabled {
            background: var(--bg-tertiary);
            color: var(--text-tertiary);
            cursor: not-allowed;
            transform: none;
        }"""
    
    def _get_javascript(self) -> str:
        """Get all JavaScript code for the HTML page."""
        # This would contain the full JavaScript - returning a placeholder
        # In production, you'd import this from a separate file or template
        return """        // Wrap all code in DOMContentLoaded to ensure DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
        
        // Theme Management
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const themeText = document.getElementById('theme-text');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            if (theme === 'light') {
                themeIcon.textContent = '☀️';
                themeText.textContent = 'Light';
            } else {
                themeIcon.textContent = '🌙';
                themeText.textContent = 'Dark';
            }
        }
        
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
        
        // Sign out function
        function signOut() {
            console.log('User signed out');
            // In production, this would clear auth tokens and redirect
            document.getElementById('user-menu-container').style.display = 'none';
            document.getElementById('sign-in-btn').style.display = 'flex';
            localStorage.removeItem('github_token');
            localStorage.removeItem('github_username');
            localStorage.removeItem('github_avatar');
            localStorage.removeItem('github_role');
            
            // Close dropdown
            const dropdown = document.getElementById('user-dropdown');
            if (dropdown) {
                dropdown.classList.remove('show');
            }
            
            alert('Signed out successfully');
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
        
        // Attach sign out button event listener
        const signOutBtn = document.getElementById('sign-out-btn');
        if (signOutBtn) {
            signOutBtn.addEventListener('click', signOut);
        }
        
        // Function to populate user profile and determine role
        function populateUserProfile() {
            // In production, this would fetch from GitHub API and check repo permissions
            // For now, using mock data - replace with actual API call
            const userData = {
                username: localStorage.getItem('github_username') || 'GitHub User',
                avatar: localStorage.getItem('github_avatar') || 'https://avatars.githubusercontent.com/u/6154722?v=4',
                role: localStorage.getItem('github_role') || 'PR_OWNER' // PR_OWNER, COLLABORATOR, ADMIN
            };
            
            // Populate user avatar
            const avatarEl = document.getElementById('user-avatar');
            if (avatarEl) {
                avatarEl.src = userData.avatar;
            }
            
            // Populate username
            const nameEl = document.getElementById('user-name');
            if (nameEl) {
                nameEl.textContent = userData.username;
            }
            
            // Populate role badge
            const roleBadge = document.getElementById('collaborator-badge');
            if (!roleBadge) return;
            
            let roleIcon = '';
            let roleText = '';
            let roleColor = '';
            
            switch(userData.role) {
                case 'ADMIN':
                    roleIcon = '🔴';
                    roleText = 'Admin';
                    roleColor = '#ef4444';
                    break;
                case 'COLLABORATOR':
                    roleIcon = '🟢';
                    roleText = 'Collaborator';
                    roleColor = '#22c55e';
                    break;
                case 'PR_OWNER':
                default:
                    roleIcon = '🟠';
                    roleText = 'PR Owner';
                    roleColor = '#fb8500';
            }
            
            roleBadge.textContent = `${roleIcon} ${roleText}`;
            roleBadge.style.color = roleColor;
            roleBadge.style.background = `${roleColor}20`;
        }
        
        // Always populate user profile on page load
        populateUserProfile();
        
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
        
        // Submit challenge (placeholder - would integrate with Azure Function)
        async function submitChallenge() {
            const selectedOption = document.querySelector('.challenge-option.selected');
            if (!selectedOption) {
                alert('Please select a feedback type');
                return;
            }
            
            const challengeType = selectedOption.getAttribute('data-type');
            const feedback = document.getElementById('challenge-feedback').value;
            
            // Placeholder for API call
            console.log('Challenge submitted:', {
                findingId: currentFindingId,
                issueHash: currentIssueHash,
                spec: currentSpec,
                issueType: currentIssueType,
                description: currentDescription,
                challengeType,
                feedback
            });
            
            // Show success and close modal
            alert('Feedback submitted successfully!');
            closeChallengeModal();
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
            const totalIssues = document.getElementById('total-issues-count').textContent;
            document.getElementById('issues-badge').textContent = totalIssues;
            document.getElementById('top-bell-badge').textContent = totalIssues;
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
        
        }); // End DOMContentLoaded"""
