#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
HtmlReportGenerator creates interactive HTML reports for CVE spec file analysis.

This module handles all HTML generation logic, including:
- Complete self-contained HTML pages with CSS and JavaScript
- Interactive dashboard components (stats cards, spec details, challenge system)
- Professional theme system (dark/light mode)
- Authentication UI integration
- Bell icon spec expansion functionality
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
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: var(--bg-card); color: var(--text-primary); padding: 24px; border-radius: 8px; border: 1px solid var(--border-primary); box-shadow: var(--shadow-lg);">
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 class="main-title" style="margin: 0; font-size: 2em; line-height: 1.2;">
            Code Review Analysis Report
        </h1>
        <p style="color: var(--text-secondary); margin: 12px 0 5px 0; font-size: 14px;">
            Automated Anti-pattern Detection System
        </p>
        <p style="color: var(--text-tertiary); margin: 5px 0; font-size: 13px;">
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
            <h3 class="pr-info-title">Pull Request Details</h3>
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
                <span class="arrow-separator">→</span> 
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
        <div class="stat-card" style="--stat-accent: var(--accent-blue);">
            <div class="stat-header">
                <span class="stat-label">Specs Analyzed</span>
            </div>
            <div class="stat-value">{stats['total_specs']}</div>
        </div>
        
        <!-- Errors Card -->
        <div class="stat-card filterable-stat" data-filter-severity="ERROR" style="--stat-accent: var(--error-color);">
            <div class="stat-header">
                <span class="stat-label">Critical Issues</span>
            </div>
            <div class="stat-value">{stats['total_errors']}</div>
        </div>
        
        <!-- Warnings Card -->
        <div class="stat-card filterable-stat" data-filter-severity="WARNING" style="--stat-accent: var(--warning-color);">
            <div class="stat-header">
                <span class="stat-label">Warnings</span>
            </div>
            <div class="stat-value">{stats['total_warnings']}</div>
        </div>
        
        <!-- Total Issues Card -->
        <div class="stat-card reset-filter-stat" style="--stat-accent: var(--primary-color);">
            <div class="stat-header">
                <span class="stat-label">Total Issues</span>
                <span class="notification-dot" id="issues-badge">{total_issues}</span>
            </div>
            <div class="stat-value" id="total-issues-count">{total_issues}</div>
        </div>
    </div>
"""
    
    def _generate_spec_cards(self, spec_results: list) -> str:
        """Generate expandable cards for each spec file."""
        from AntiPatternDetector import Severity
        
        html = ""
        for spec_result in sorted(spec_results, key=lambda x: x.package_name):
            severity_indicator = "high" if spec_result.severity >= Severity.ERROR else "medium" if spec_result.severity >= Severity.WARNING else "low"
            html += f"""
    <details class="spec-card" data-spec-name="{spec_result.package_name}" data-severity="{severity_indicator}">
        <summary>
            <span class="spec-name">{spec_result.package_name}</span>
            <span class="spec-summary">{spec_result.summary}</span>
        </summary>
        <div class="spec-card-content">
            <div class="spec-file-info">
                <span class="spec-file-label">File:</span> 
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
            <div class="antipattern-container">
                <h4 class="section-title">Detected Issues</h4>
"""
        
        for issue_type, patterns in issues_by_type.items():
            html += f"""
                    <div class="issue-type-section">
                        <div class="issue-type-header">
                            <span class="issue-type-title">{issue_type}</span>
                            <span class="issue-count-badge">{len(patterns)}</span>
                        </div>
                        <div class="issue-list">
"""
            for idx, pattern in enumerate(patterns):
                html += self._generate_issue_item(spec_result.package_name, issue_type, pattern, idx, spec_result.spec_path)
            
            html += """
                        </div>
                    </div>
"""
        
        html += """
            </div>
"""
        return html
    
    def _generate_issue_item(self, package_name: str, issue_type: str, pattern, idx: int, spec_path: str) -> str:
        """Generate a single issue item with challenge button."""
        issue_hash = pattern.issue_hash if hasattr(pattern, 'issue_hash') and pattern.issue_hash else f"{package_name}-{issue_type.replace(' ', '-').replace('_', '-')}-{idx}"
        finding_id = issue_hash
        
        severity_name = pattern.severity.name
        severity_class = "severity-high" if severity_name == "ERROR" else "severity-medium" if severity_name == "WARNING" else "severity-low"
        
        escaped_desc = html_module.escape(pattern.description, quote=True)
        
        return f"""
                            <div class="issue-item {severity_class}" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-severity="{severity_name}">
                                <div class="issue-content">
                                    <span class="severity-indicator"></span>
                                    <span class="issue-text">{escaped_desc}</span>
                                </div>
                                <button class="challenge-btn" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-spec="{spec_path}" data-issue-type="{issue_type}" data-description="{escaped_desc}">
                                    Challenge
                                </button>
                            </div>
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
            <div class="recommendations-section">
                <h4 class="section-title">Recommended Actions</h4>
                <ul class="recommendations-list">
"""
        for rec in recommendations:
            html += f"""
                    <li>{rec}</li>
"""
        html += """
                </ul>
            </div>
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
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="report-version" content="{cache_buster}">
    <title>Code Review Report - PR #{pr_number}</title>
    <!-- Professional fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%232563eb'/%3E%3Ctext x='50' y='50' text-anchor='middle' dominant-baseline='central' font-size='50' fill='white' font-weight='bold'%3ER%3C/text%3E%3C/svg%3E">
    <style>
{css}
    </style>
</head>
<body data-report-version="{cache_buster}">
    <!-- Top Navigation Bar -->
    <nav id="top-bar">
        <div id="top-bar-left">
            <div id="logo">
                <span class="logo-text">RADAR</span>
                <span class="logo-subtitle">Analysis Report</span>
            </div>
        </div>
        <div id="top-bar-right">
            <!-- Notification Bell -->
            <button id="top-bell-container" class="icon-btn" aria-label="Expand all sections">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                </svg>
                <span id="top-bell-badge" class="badge">0</span>
            </button>
            
            <!-- Theme Toggle -->
            <button id="theme-toggle" class="icon-btn" aria-label="Toggle theme">
                <svg id="theme-icon-light" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="5"/>
                    <line x1="12" y1="1" x2="12" y2="3"/>
                    <line x1="12" y1="21" x2="12" y2="23"/>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                    <line x1="1" y1="12" x2="3" y2="12"/>
                    <line x1="21" y1="12" x2="23" y2="12"/>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
                <svg id="theme-icon-dark" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
            </button>
            
            <!-- Auth Container -->
            <div id="auth-container">
                <button id="sign-in-btn" class="primary-btn" style="display: none;">
                    Sign in with GitHub
                </button>
                <div id="user-menu-container">
                    <button id="user-menu" class="user-menu-btn">
                        <img id="user-avatar" src="" alt="User">
                        <div id="user-info">
                            <span id="user-name"></span>
                            <span id="collaborator-badge"></span>
                        </div>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="6 9 12 15 18 9"/>
                        </svg>
                    </button>
                    <div id="user-dropdown" class="dropdown-menu">
                        <button id="sign-out-btn" class="dropdown-item">
                            Sign Out
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <main id="main-container">
{report_body}
    </main>
    
    <!-- Challenge Modal -->
    <div id="challenge-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Challenge Finding</h2>
                <button class="modal-close" id="modal-close-btn" aria-label="Close">&times;</button>
            </div>
            <div class="modal-body">
                <div id="modal-finding-text" class="finding-display"></div>
                <div id="challenge-options">
                    <label class="challenge-option">
                        <input type="radio" name="challenge-type" value="false-positive">
                        <span>False Positive</span>
                    </label>
                    <label class="challenge-option">
                        <input type="radio" name="challenge-type" value="needs-context">
                        <span>Needs More Context</span>
                    </label>
                    <label class="challenge-option">
                        <input type="radio" name="challenge-type" value="disagree-with-severity">
                        <span>Disagree with Severity</span>
                    </label>
                </div>
                <textarea id="challenge-feedback" placeholder="Please provide additional details about why you're challenging this finding..." rows="4"></textarea>
                <button id="submit-challenge-btn" class="primary-btn">Submit Feedback</button>
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
        """Get all CSS styles for the HTML page with professional design."""
        return """        /* CSS VARIABLES - Professional Theme System */
        :root {
            /* Professional Dark Theme */
            --bg-primary: #0f0f10;
            --bg-secondary: #18181b;
            --bg-tertiary: #1f1f23;
            --bg-card: #18181b;
            --bg-card-hover: #202024;
            --bg-hover: rgba(255, 255, 255, 0.04);
            --bg-modal-overlay: rgba(0, 0, 0, 0.8);
            
            --border-primary: #27272a;
            --border-secondary: #3f3f46;
            --border-accent: #52525b;
            
            --text-primary: #fafafa;
            --text-secondary: #a1a1aa;
            --text-tertiary: #71717a;
            
            --primary-color: #3b82f6;
            --primary-hover: #2563eb;
            --accent-blue: #3b82f6;
            --error-color: #ef4444;
            --warning-color: #f59e0b;
            --success-color: #10b981;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            
            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 8px;
        }
        
        /* Professional Light Theme */
        [data-theme="light"] {
            --bg-primary: #ffffff;
            --bg-secondary: #fafafa;
            --bg-tertiary: #f4f4f5;
            --bg-card: #ffffff;
            --bg-card-hover: #f9fafb;
            --bg-hover: rgba(0, 0, 0, 0.02);
            --bg-modal-overlay: rgba(0, 0, 0, 0.5);
            
            --border-primary: #e4e4e7;
            --border-secondary: #d4d4d8;
            --border-accent: #a1a1aa;
            
            --text-primary: #09090b;
            --text-secondary: #52525b;
            --text-tertiary: #71717a;
            
            --primary-color: #2563eb;
            --primary-hover: #1d4ed8;
            --accent-blue: #2563eb;
            --error-color: #dc2626;
            --warning-color: #ea580c;
            --success-color: #059669;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            transition: background-color 0.2s, color 0.2s;
        }
        
        code, pre {
            font-family: 'JetBrains Mono', 'Monaco', 'Consolas', monospace;
        }
        
        /* Typography */
        h1, h2, h3, h4 {
            font-weight: 600;
            line-height: 1.3;
        }
        
        .main-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }
        
        /* Top Navigation Bar */
        #top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 56px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-primary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 1000;
            backdrop-filter: blur(8px);
            background: rgba(24, 24, 27, 0.8);
        }
        
        [data-theme="light"] #top-bar {
            background: rgba(255, 255, 255, 0.8);
        }
        
        #top-bar-left {
            display: flex;
            align-items: center;
            gap: 24px;
        }
        
        #logo {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }
        
        .logo-text {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }
        
        .logo-subtitle {
            font-size: 14px;
            color: var(--text-tertiary);
            font-weight: 400;
        }
        
        #top-bar-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Icon Buttons */
        .icon-btn {
            position: relative;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .icon-btn:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
            border-color: var(--border-secondary);
        }
        
        .icon-btn:active {
            transform: scale(0.96);
        }
        
        .badge {
            position: absolute;
            top: -4px;
            right: -4px;
            background: var(--error-color);
            color: white;
            font-size: 11px;
            font-weight: 600;
            padding: 1px 5px;
            border-radius: 10px;
            min-width: 18px;
            text-align: center;
        }
        
        /* Buttons */
        .primary-btn {
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: var(--radius-md);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .primary-btn:hover {
            background: var(--primary-hover);
        }
        
        .primary-btn:active {
            transform: scale(0.98);
        }
        
        .primary-btn:disabled {
            background: var(--bg-tertiary);
            color: var(--text-tertiary);
            cursor: not-allowed;
            transform: none;
        }
        
        /* User Menu */
        #user-menu-container {
            position: relative;
            display: none;
        }
        
        .user-menu-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            background: transparent;
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            padding: 4px 12px 4px 4px;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-primary);
        }
        
        .user-menu-btn:hover {
            background: var(--bg-hover);
            border-color: var(--border-secondary);
        }
        
        #user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        #user-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
        }
        
        #user-name {
            font-size: 14px;
            font-weight: 500;
        }
        
        #collaborator-badge {
            font-size: 11px;
            color: var(--text-tertiary);
        }
        
        .dropdown-menu {
            display: none;
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            min-width: 160px;
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
            font-size: 14px;
            transition: background 0.2s;
        }
        
        .dropdown-item:hover {
            background: var(--bg-hover);
        }
        
        /* Main Container */
        #main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 24px 24px;
        }
        
        /* PR Info Card */
        .pr-info-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 24px;
        }
        
        .pr-info-header {
            margin-bottom: 20px;
        }
        
        .pr-info-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .pr-info-grid {
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 16px;
            align-items: center;
        }
        
        .pr-info-label {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }
        
        .pr-info-value {
            font-size: 14px;
            color: var(--text-primary);
        }
        
        .pr-number-badge,
        .author-badge,
        .branch-badge,
        .commit-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            border: 1px solid var(--border-primary);
        }
        
        .arrow-separator {
            color: var(--text-tertiary);
            margin: 0 8px;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-lg);
            padding: 20px;
            position: relative;
            transition: all 0.2s;
            cursor: pointer;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 3px;
            height: 100%;
            background: var(--stat-accent, transparent);
            border-radius: var(--radius-lg) 0 0 var(--radius-lg);
            transition: width 0.2s;
        }
        
        .stat-card:hover {
            background: var(--bg-card-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .stat-card:hover::before {
            width: 4px;
        }
        
        .filterable-stat:hover,
        .reset-filter-stat:hover {
            border-color: var(--stat-accent);
        }
        
        .stat-card.filter-active {
            background: var(--bg-card-hover);
            border-color: var(--stat-accent);
            box-shadow: 0 0 0 1px var(--stat-accent);
        }
        
        .stat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .stat-label {
            font-size: 13px;
            color: var(--text-tertiary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
        }
        
        .notification-dot {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            background: var(--error-color);
            color: white;
            font-size: 11px;
            font-weight: 600;
            border-radius: 50%;
        }
        
        /* Spec Cards */
        .spec-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-lg);
            margin-bottom: 16px;
            overflow: hidden;
        }
        
        .spec-card[data-severity="high"] {
            border-left: 3px solid var(--error-color);
        }
        
        .spec-card[data-severity="medium"] {
            border-left: 3px solid var(--warning-color);
        }
        
        .spec-card[data-severity="low"] {
            border-left: 3px solid var(--success-color);
        }
        
        .spec-card summary {
            cursor: pointer;
            padding: 20px;
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }
        
        .spec-card summary::-webkit-details-marker {
            display: none;
        }
        
        .spec-card summary:hover {
            background: var(--bg-hover);
        }
        
        .spec-card summary::before {
            content: '';
            display: inline-block;
            width: 0;
            height: 0;
            border-left: 5px solid var(--text-tertiary);
            border-top: 5px solid transparent;
            border-bottom: 5px solid transparent;
            margin-right: 12px;
            transition: transform 0.2s;
        }
        
        .spec-card[open] summary::before {
            transform: rotate(90deg);
        }
        
        .spec-name {
            font-weight: 600;
            font-size: 15px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
        }
        
        .spec-summary {
            font-size: 13px;
            color: var(--text-tertiary);
        }
        
        .spec-card-content {
            padding: 0 20px 20px;
            border-top: 1px solid var(--border-primary);
        }
        
        .spec-file-info {
            margin: 20px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .spec-file-label {
            font-size: 13px;
            color: var(--text-tertiary);
            font-weight: 500;
        }
        
        .spec-file-badge {
            padding: 4px 8px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        /* Issues Section */
        .antipattern-container {
            margin-top: 24px;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }
        
        .issue-type-section {
            margin-bottom: 20px;
        }
        
        .issue-type-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 8px;
            margin-bottom: 12px;
            border-bottom: 1px solid var(--border-primary);
        }
        
        .issue-type-title {
            font-size: 14px;
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .issue-count-badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .issue-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .issue-item {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            transition: all 0.2s;
        }
        
        .issue-item:hover {
            background: var(--bg-hover);
            transform: translateX(4px);
        }
        
        .issue-item.filtered-out {
            opacity: 0.3;
            pointer-events: none;
        }
        
        .issue-item.filtered-in {
            box-shadow: 0 0 0 2px var(--primary-color);
        }
        
        .issue-content {
            display: flex;
            gap: 12px;
            flex: 1;
            align-items: flex-start;
        }
        
        .severity-indicator {
            width: 3px;
            height: 100%;
            min-height: 20px;
            border-radius: 2px;
            flex-shrink: 0;
        }
        
        .severity-high .severity-indicator {
            background: var(--error-color);
        }
        
        .severity-medium .severity-indicator {
            background: var(--warning-color);
        }
        
        .severity-low .severity-indicator {
            background: var(--success-color);
        }
        
        .issue-text {
            font-size: 14px;
            color: var(--text-primary);
            line-height: 1.5;
        }
        
        .challenge-btn {
            padding: 6px 12px;
            background: transparent;
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .challenge-btn:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
            background: var(--bg-hover);
        }
        
        .challenge-btn.challenged {
            background: var(--success-color);
            color: white;
            border-color: var(--success-color);
            cursor: not-allowed;
        }
        
        /* Recommendations */
        .recommendations-section {
            margin-top: 24px;
            padding: 16px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-md);
        }
        
        .recommendations-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .recommendations-list li {
            font-size: 14px;
            color: var(--text-primary);
            padding-left: 20px;
            position: relative;
        }
        
        .recommendations-list li::before {
            content: '•';
            position: absolute;
            left: 0;
            color: var(--success-color);
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
            backdrop-filter: blur(4px);
        }
        
        .modal.visible {
            display: flex;
        }
        
        .modal-content {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-lg);
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: var(--shadow-xl);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-primary);
        }
        
        .modal-header h2 {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 24px;
            color: var(--text-tertiary);
            cursor: pointer;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
            transition: all 0.2s;
        }
        
        .modal-close:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        .modal-body {
            padding: 24px;
        }
        
        .finding-display {
            padding: 12px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-md);
            margin-bottom: 20px;
            font-size: 14px;
            color: var(--text-primary);
            line-height: 1.5;
        }
        
        #challenge-options {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .challenge-option {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .challenge-option:hover {
            background: var(--bg-hover);
            border-color: var(--border-secondary);
        }
        
        .challenge-option input[type="radio"] {
            margin: 0;
        }
        
        .challenge-option input[type="radio"]:checked + span {
            color: var(--primary-color);
            font-weight: 500;
        }
        
        #challenge-feedback {
            width: 100%;
            padding: 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            margin-bottom: 20px;
        }
        
        #challenge-feedback:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 0 2px var(--primary-color); }
            50% { box-shadow: 0 0 10px 2px var(--primary-color); }
        }
        
        #top-bell-container.glowing {
            animation: glow 1s ease-in-out;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .pr-info-grid {
                grid-template-columns: 1fr;
                gap: 8px;
            }
            
            #top-bar {
                padding: 0 16px;
            }
            
            .logo-subtitle {
                display: none;
            }
        }
        
        /* Utility Classes */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }"""
    
    def _get_javascript(self, pr_number: int) -> str:
        """Get all JavaScript code for the HTML page with professional interactions."""
        js_code = """        // ============================================================================
        // RADAR Authentication Module
        // ============================================================================
        
        const RADAR_AUTH = (() => {
            const GITHUB_CLIENT_ID = 'Ov23limFwlBEPDQzgGmb';
            const AUTH_CALLBACK_URL = 'https://radarfunc-eka5fmceg4b5fub0.canadacentral-01.azurewebsites.net/api/auth/callback';
            const STORAGE_KEY = 'radar_auth_token';
            const USER_KEY = 'radar_user_info';
            
            function getCurrentUser() {
                const userJson = localStorage.getItem(USER_KEY);
                return userJson ? JSON.parse(userJson) : null;
            }
            
            function getAuthToken() {
                return localStorage.getItem(STORAGE_KEY);
            }
            
            function isAuthenticated() {
                return !!getAuthToken();
            }
            
            function signIn() {
                const currentUrl = window.location.href.split('#')[0];
                const state = encodeURIComponent(currentUrl);
                const authUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(AUTH_CALLBACK_URL)}&scope=read:user%20read:org&state=${state}`;
                window.location.href = authUrl;
            }
            
            function signOut() {
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem(USER_KEY);
                updateUI();
            }
            
            function handleAuthCallback() {
                const fragment = window.location.hash.substring(1);
                const params = new URLSearchParams(fragment);
                const token = params.get('token');
                
                if (token) {
                    localStorage.setItem(STORAGE_KEY, token);
                    
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
                    } catch (e) {
                        console.error('Failed to decode token:', e);
                    }
                    
                    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
                    updateUI();
                }
            }
            
            function updateUI() {
                const user = getCurrentUser();
                const userMenuContainer = document.getElementById('user-menu-container');
                const signInBtn = document.getElementById('sign-in-btn');
                
                if (!userMenuContainer || !signInBtn) return;
                
                if (user) {
                    userMenuContainer.style.display = 'block';
                    signInBtn.style.display = 'none';
                    
                    const avatarEl = document.getElementById('user-avatar');
                    const nameEl = document.getElementById('user-name');
                    const badgeEl = document.getElementById('collaborator-badge');
                    
                    if (avatarEl) avatarEl.src = user.avatar_url;
                    if (nameEl) nameEl.textContent = user.name || user.username;
                    
                    if (badgeEl) {
                        if (user.is_admin) {
                            badgeEl.textContent = 'Admin';
                        } else if (user.is_collaborator) {
                            badgeEl.textContent = 'Collaborator';
                        } else {
                            badgeEl.textContent = 'PR Owner';
                        }
                    }
                } else {
                    userMenuContainer.style.display = 'none';
                    signInBtn.style.display = 'block';
                }
            }
            
            function getAuthHeaders() {
                const token = getAuthToken();
                return token ? {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                } : {
                    'Content-Type': 'application/json'
                };
            }
            
            function init() {
                handleAuthCallback();
                updateUI();
            }
            
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
        
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
        
        // Initialize Auth
        RADAR_AUTH.init();
        
        // Theme Management
        const themeToggle = document.getElementById('theme-toggle');
        const lightIcon = document.getElementById('theme-icon-light');
        const darkIcon = document.getElementById('theme-icon-dark');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            if (theme === 'dark') {
                lightIcon.style.display = 'block';
                darkIcon.style.display = 'none';
            } else {
                lightIcon.style.display = 'none';
                darkIcon.style.display = 'block';
            }
        }
        
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
        
        // Auth UI Events
        const signInBtn = document.getElementById('sign-in-btn');
        if (signInBtn) {
            signInBtn.addEventListener('click', () => RADAR_AUTH.signIn());
        }
        
        // User Menu Dropdown
        const userMenu = document.getElementById('user-menu');
        const userDropdown = document.getElementById('user-dropdown');
        
        if (userMenu && userDropdown) {
            userMenu.addEventListener('click', (e) => {
                e.stopPropagation();
                userDropdown.classList.toggle('show');
            });
            
            document.addEventListener('click', (e) => {
                if (!userMenu.contains(e.target) && !userDropdown.contains(e.target)) {
                    userDropdown.classList.remove('show');
                }
            });
        }
        
        const signOutBtn = document.getElementById('sign-out-btn');
        if (signOutBtn) {
            signOutBtn.addEventListener('click', () => {
                userDropdown.classList.remove('show');
                RADAR_AUTH.signOut();
            });
        }
        
        // Bell Icon - Expand All Specs
        const topBellContainer = document.getElementById('top-bell-container');
        
        if (topBellContainer) {
            topBellContainer.addEventListener('click', function(e) {
                e.preventDefault();
                
                const specCards = document.querySelectorAll('.spec-card');
                let allExpanded = true;
                
                specCards.forEach(card => {
                    if (!card.hasAttribute('open')) {
                        allExpanded = false;
                    }
                });
                
                if (allExpanded) {
                    this.classList.add('glowing');
                    setTimeout(() => {
                        this.classList.remove('glowing');
                    }, 1000);
                    
                    if (specCards.length > 0) {
                        specCards[0].scrollIntoView({
                            behavior: 'smooth',
                            block: 'center'
                        });
                    }
                } else {
                    specCards.forEach((card, index) => {
                        setTimeout(() => {
                            card.setAttribute('open', '');
                        }, index * 30);
                    });
                    
                    if (specCards.length > 0) {
                        setTimeout(() => {
                            specCards[0].scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }, 200);
                    }
                }
            });
        }
        
        // Challenge Modal
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
            document.querySelectorAll('input[name="challenge-type"]').forEach(radio => {
                radio.checked = false;
            });
            document.getElementById('challenge-feedback').value = '';
        }
        
        function closeChallengeModal() {
            document.getElementById('challenge-modal').classList.remove('visible');
        }
        
        document.getElementById('modal-close-btn').addEventListener('click', closeChallengeModal);
        
        // Submit Challenge
        async function submitChallenge() {
            if (!RADAR_AUTH.isAuthenticated()) {
                alert('Please sign in to submit challenges');
                RADAR_AUTH.signIn();
                return;
            }
            
            const selectedOption = document.querySelector('input[name="challenge-type"]:checked');
            if (!selectedOption) {
                alert('Please select a feedback type');
                return;
            }
            
            const challengeType = selectedOption.value;
            const feedback = document.getElementById('challenge-feedback').value.trim();
            
            if (!feedback) {
                alert('Please provide additional details');
                return;
            }
            
            const submitBtn = document.getElementById('submit-challenge-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {
                const pr_number = {pr_number};
                const headers = RADAR_AUTH.getAuthHeaders();
                
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
                    alert('Challenge submitted successfully!');
                    
                    // Update button
                    const btn = document.querySelector(`button.challenge-btn[data-finding-id="${currentFindingId}"]`);
                    if (btn) {
                        btn.textContent = 'Challenged';
                        btn.classList.add('challenged');
                        btn.disabled = true;
                    }
                    
                    // Update counters
                    updateIssueCounts(-1);
                    closeChallengeModal();
                } else {
                    if (response.status === 401) {
                        alert('Your session has expired. Please sign in again.');
                        RADAR_AUTH.signOut();
                        return;
                    }
                    alert(`Failed to submit challenge: ${result.error || 'Unknown error'}`);
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    alert('Request timeout: Server took too long to respond.');
                } else {
                    alert(`Error: ${error.message}`);
                }
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Feedback';
            }
        }
        
        document.getElementById('submit-challenge-btn').addEventListener('click', submitChallenge);
        
        // Attach challenge button events
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
        
        // Update issue counters
        function updateIssueCounts(delta) {
            const totalIssuesEl = document.getElementById('total-issues-count');
            const topBellBadge = document.getElementById('top-bell-badge');
            
            if (totalIssuesEl) {
                const currentCount = parseInt(totalIssuesEl.textContent) || 0;
                const newCount = Math.max(0, currentCount + delta);
                totalIssuesEl.textContent = newCount;
            }
            
            if (topBellBadge) {
                const currentCount = parseInt(topBellBadge.textContent) || 0;
                const newCount = Math.max(0, currentCount + delta);
                topBellBadge.textContent = newCount;
            }
        }
        
        // Initialize counters
        function initializeCounters() {
            const totalIssuesEl = document.getElementById('total-issues-count');
            const topBellBadge = document.getElementById('top-bell-badge');
            
            if (totalIssuesEl && topBellBadge) {
                topBellBadge.textContent = totalIssuesEl.textContent;
            }
        }
        
        initializeCounters();
        
        // Severity filtering
        let activeSeverityFilter = null;
        
        function expandAllSpecCards() {
            document.querySelectorAll('.spec-card').forEach(card => {
                card.setAttribute('open', '');
            });
        }
        
        function resetAllFilters() {
            activeSeverityFilter = null;
            document.querySelectorAll('.filterable-stat').forEach(card => {
                card.classList.remove('filter-active');
            });
            document.querySelectorAll('.issue-item').forEach(item => {
                item.classList.remove('filtered-out', 'filtered-in');
            });
        }
        
        document.querySelector('.reset-filter-stat')?.addEventListener('click', function() {
            resetAllFilters();
        });
        
        document.querySelectorAll('.filterable-stat').forEach(card => {
            card.addEventListener('click', function() {
                const severity = this.getAttribute('data-filter-severity');
                
                if (activeSeverityFilter === severity) {
                    resetAllFilters();
                } else {
                    activeSeverityFilter = severity;
                    expandAllSpecCards();
                    
                    document.querySelectorAll('.filterable-stat').forEach(c => c.classList.remove('filter-active'));
                    this.classList.add('filter-active');
                    
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
                    
                    if (firstMatchingIssue) {
                        setTimeout(() => {
                            firstMatchingIssue.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'center' 
                            });
                        }, 300);
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
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const modal = document.getElementById('challenge-modal');
                if (modal && modal.classList.contains('visible')) {
                    closeChallengeModal();
                }
            }
            
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                themeToggle.click();
            }
        });
        
        }); // End DOMContentLoaded"""
        
        return js_code.replace('{pr_number}', str(pr_number))