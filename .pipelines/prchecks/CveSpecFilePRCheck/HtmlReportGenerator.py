#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
HtmlReportGenerator creates interactive HTML reports for CVE spec file analysis.

This module handles all HTML generation logic, including:
- Complete self-contained HTML pages with CSS and JavaScript
- Interactive dashboard components (stats cards, spec details, challenge system)
- GitHub-inspired theme system (dark/light mode)
- Authentication UI integration
- Bell icon spec expansion functionality
"""

import html as html_module
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import logging
import base64
import os

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
    
    def _load_logo_as_data_uri(self, logo_path: str) -> str:
        """
        Load a logo file and convert it to a base64 data URI.
        
        Args:
            logo_path: Path to the logo file
            
        Returns:
            Data URI string for embedding in HTML
        """
        try:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = base64.b64encode(f.read()).decode('utf-8')
                    return f"data:image/png;base64,{logo_data}"
        except Exception as e:
            logger.warning(f"Failed to load logo {logo_path}: {e}")
        
        # Fallback to placeholder SVG
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='14' fill='%230969da'/%3E%3Ctext x='16' y='21' text-anchor='middle' font-size='18' fill='white' font-weight='bold'%3ER%3C/text%3E%3C/svg%3E"
    
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
<div class="container-lg px-3 py-4">
    <div class="Box">
        <div class="Box-header">
            <h2 class="Box-title">
                Code Review Analysis Report
            </h2>
        </div>
        <div class="Box-body">
            <p class="text-secondary mb-0">
                By RADAR | Realtime Anti-pattern Detection with AI Reasoning • Generated {datetime.now().strftime('%b %d, %Y at %H:%M UTC')}
            </p>
        </div>
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
    <div class="Box mt-3">
        <div class="Box-header">
            <h3 class="Box-title">Pull Request Information</h3>
        </div>
        <div class="Box-body">
            <dl class="form-group">
                <dt class="input-label">PR</dt>
                <dd>
                    <a href="#" class="Link--primary">#{pr_number}</a>
                </dd>
                
                <dt class="input-label">Title</dt>
                <dd>{pr_title}</dd>
                
                <dt class="input-label">Author</dt>
                <dd>
                    <svg class="octicon octicon-person mr-1" viewBox="0 0 16 16" width="16" height="16" style="color: var(--color-fg-muted);">
                        <path fill-rule="evenodd" d="M10.5 5a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm.061 3.073a4 4 0 10-5.123 0 6.004 6.004 0 00-3.431 5.142.75.75 0 001.498.07 4.5 4.5 0 018.99 0 .75.75 0 101.498-.07 6.005 6.005 0 00-3.432-5.142z"/>
                    </svg>
                    <a href="#" class="Link--primary">@{pr_author}</a>
                </dd>
                
                <dt class="input-label">Branches</dt>
                <dd>
                    <span class="branch-name">{source_branch}</span>
                    <span class="text-secondary mx-1">←</span>
                    <span class="branch-name">{target_branch}</span>
                </dd>
                
                <dt class="input-label">Commit</dt>
                <dd><code class="commit-sha">{source_commit}</code></dd>
            </dl>
        </div>
    </div>
"""
    
    def _generate_stats_grid(self, stats: dict, total_issues: int) -> str:
        """Generate statistics cards grid."""
        return f"""
    <div class="d-flex flex-wrap mt-3" style="gap: 12px;">
        <div class="Box flex-1 stats-card">
            <div class="Box-body d-flex flex-column">
                <span class="text-secondary text-small">Specs Analyzed</span>
                <span class="f1 text-bold">{stats['total_specs']}</span>
            </div>
        </div>
        
        <div class="Box flex-1 stats-card filterable-stat" data-filter-severity="ERROR" style="cursor: pointer;">
            <div class="Box-body d-flex flex-column">
                <span class="text-secondary text-small">Critical Issues</span>
                <span class="f1 text-bold color-fg-danger">{stats['total_errors']}</span>
            </div>
        </div>
        
        <div class="Box flex-1 stats-card filterable-stat" data-filter-severity="WARNING" style="cursor: pointer;">
            <div class="Box-body d-flex flex-column">
                <span class="text-secondary text-small">Warnings</span>
                <span class="f1 text-bold color-fg-attention">{stats['total_warnings']}</span>
            </div>
        </div>
        
        <div class="Box flex-1 stats-card reset-filter-stat" style="cursor: pointer;">
            <div class="Box-body d-flex flex-column">
                <span class="text-secondary text-small">Total Issues</span>
                <span class="f1 text-bold" id="total-issues-count">{total_issues}</span>
            </div>
        </div>
    </div>
"""
    
    def _generate_spec_cards(self, spec_results: list) -> str:
        """Generate expandable cards for each spec file."""
        from AntiPatternDetector import Severity
        
        html = ""
        for spec_result in sorted(spec_results, key=lambda x: x.package_name):
            severity_class = "color-border-danger-emphasis" if spec_result.severity >= Severity.ERROR else "color-border-attention-emphasis" if spec_result.severity >= Severity.WARNING else "color-border-success-emphasis"
            
            # Count issues by type for summary
            errors = sum(1 for p in spec_result.anti_patterns if p.severity >= Severity.ERROR)
            warnings = sum(1 for p in spec_result.anti_patterns if p.severity >= Severity.WARNING and p.severity < Severity.ERROR)
            
            html += f"""
    <details class="Box mt-3 Details {severity_class}">
        <summary class="Box-header Details-summary">
            <svg class="octicon octicon-chevron mr-2" viewBox="0 0 16 16" width="16" height="16">
                <path fill-rule="evenodd" d="M6.22 3.22a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.75.75 0 01-1.06-1.06L9.94 8 6.22 4.28a.75.75 0 010-1.06z"/>
            </svg>
            <span class="text-bold mr-2">{spec_result.package_name}</span>
            <span class="text-secondary text-small">({errors} errors, {warnings} warnings)</span>
        </summary>
        <div class="Box-body">
            <div class="mb-3">
                <span class="text-secondary text-small">Spec File:</span> 
                <code class="text-mono text-small px-1 py-1">{spec_result.spec_path}</code>
            </div>
"""
            
            # Anti-patterns section with better grouping
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
            <details open class="Details mb-3">
                <summary class="Details-summary">
                    <svg class="octicon octicon-bug mr-1" viewBox="0 0 16 16" width="16" height="16">
                        <path fill-rule="evenodd" d="M4.72.22a.75.75 0 011.06 0l1 .999a3.492 3.492 0 012.441 0l1-.999a.75.75 0 111.06 1.06l-.35.35a3.499 3.499 0 01.9 1.622L12.78 3.3a.75.75 0 010 1.5l-1.95.046A3.5 3.5 0 018 7.843v1.657h2.5a2.5 2.5 0 012.5 2.5v.5a.75.75 0 01-1.5 0V12a1 1 0 00-1-1H8v2.75a.75.75 0 01-1.5 0V11H4a1 1 0 00-1 1v.5a.75.75 0 01-1.5 0V12A2.5 2.5 0 014 9.5h2.5V7.843A3.5 3.5 0 013.67 4.846L1.72 4.8a.75.75 0 010-1.5l1.95-.047a3.499 3.499 0 01.9-1.622l-.35-.35A.75.75 0 014.72.22zM8 1.5a2 2 0 00-2 2V5h4V3.5a2 2 0 00-2-2z"/>
                    </svg>
                    Detected Issues
                </summary>
                <div class="mt-3">
"""
        
        for issue_type, patterns in issues_by_type.items():
            # Create a collapsible section for each issue type
            html += f"""
                    <details open class="Details mb-2">
                        <summary class="Details-summary py-2 px-2 bg-subtle">
                            <span class="text-bold text-small">{issue_type}</span>
                            <span class="Counter ml-2">{len(patterns)}</span>
                        </summary>
                        <div class="mt-2">
"""
            for idx, pattern in enumerate(patterns):
                html += self._generate_issue_item(spec_result.package_name, issue_type, pattern, idx, spec_result.spec_path)
            
            html += """
                        </div>
                    </details>
"""
        
        html += """
                </div>
            </details>
"""
        return html
    
    def _generate_issue_item(self, package_name: str, issue_type: str, pattern, idx: int, spec_path: str) -> str:
        """Generate a single issue item with challenge button."""
        issue_hash = pattern.issue_hash if hasattr(pattern, 'issue_hash') and pattern.issue_hash else f"{package_name}-{issue_type.replace(' ', '-').replace('_', '-')}-{idx}"
        finding_id = issue_hash
        
        severity_name = pattern.severity.name
        severity_label_class = "Label--danger" if severity_name == "ERROR" else "Label--attention" if severity_name == "WARNING" else "Label--success"
        severity_display = "ERROR" if severity_name == "ERROR" else "WARNING" if severity_name == "WARNING" else "INFO"
        
        # Add GitHub-style octicons for severity
        severity_icon = """<svg class="octicon octicon-issue-opened mr-1" viewBox="0 0 16 16" width="16" height="16">
            <path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/>
            <path fill-rule="evenodd" d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>
        </svg>""" if severity_name == "ERROR" else """<svg class="octicon octicon-alert mr-1" viewBox="0 0 16 16" width="16" height="16">
            <path fill-rule="evenodd" d="M8.22 1.754a.25.25 0 00-.44 0L1.698 13.132a.25.25 0 00.22.368h12.164a.25.25 0 00.22-.368L8.22 1.754zm-1.763-.707c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0114.082 15H1.918a1.75 1.75 0 01-1.543-2.575L6.457 1.047zM9 11a1 1 0 11-2 0 1 1 0 012 0zm-.25-5.25a.75.75 0 00-1.5 0v2.5a.75.75 0 001.5 0v-2.5z"/>
        </svg>""" if severity_name == "WARNING" else ""
        
        escaped_desc = html_module.escape(pattern.description, quote=True)
        
        return f"""
                            <div class="Box-row issue-item" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-severity="{severity_name}">
                                <div class="d-flex flex-justify-between flex-items-start">
                                    <div class="flex-1 mr-3">
                                        <div class="d-flex flex-items-start">
                                            {severity_icon}
                                            <div class="flex-1">
                                                <span class="Label {severity_label_class} mr-2">{severity_display}</span>
                                                <span class="text-normal">{escaped_desc}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <button class="btn btn-sm challenge-btn" type="button" data-finding-id="{finding_id}" data-issue-hash="{issue_hash}" data-spec="{spec_path}" data-issue-type="{issue_type}" data-description="{escaped_desc}">
                                        Challenge
                                    </button>
                                </div>
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
            <details open class="Details">
                <summary class="Details-summary">
                    <svg class="octicon octicon-check-circle mr-1" viewBox="0 0 16 16" width="16" height="16" style="color: var(--color-success-fg);">
                        <path fill-rule="evenodd" d="M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM8 0a8 8 0 100 16A8 8 0 008 0zm3.28 5.78a.75.75 0 00-1.06-1.06L7 7.94 5.78 6.72a.75.75 0 00-1.06 1.06l1.75 1.75a.75.75 0 001.06 0l3.75-3.75z"/>
                    </svg>
                    Recommended Actions
                </summary>
                <div class="flash flash-success mt-3">
"""
        for rec in recommendations:
            html += f"""
                    <div class="mb-1">• {rec}</div>
"""
        html += """
                </div>
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
        
        # Load actual logo files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, 'assets')
        radar_logo_light = self._load_logo_as_data_uri(os.path.join(assets_dir, 'radar_light.png'))
        radar_logo_dark = self._load_logo_as_data_uri(os.path.join(assets_dir, 'radar_dark.png'))
        
        return f"""<!DOCTYPE html>
<html lang="en" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="report-version" content="{cache_buster}">
    <title>PR #{pr_number} · Code Review Report</title>
    <!-- GitHub-like fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%230969da' d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/%3E%3C/svg%3E">
    <style>
{css}
    </style>
</head>
<body>
    <!-- GitHub-like Header -->
    <div class="Header">
        <div class="Header-item">
            <a href="#" class="Header-link f4 d-flex flex-items-center">
                <img class="radar-logo mr-2" id="radar-logo" src="{radar_logo_light}" alt="RADAR" width="32" height="32">
                <span class="Header-title">
                    <span class="text-bold">RADAR</span>
                    <span class="text-secondary mx-1">/</span>
                    <span>Analysis</span>
                </span>
            </a>
        </div>
        <div class="Header-item Header-item--full">
            <nav class="Header-nav">
                <span class="Header-navItem">
                    <span class="text-secondary">PR</span>
                    <a href="#" class="Label Label--primary ml-1">#{pr_number}</a>
                </span>
            </nav>
        </div>
        <div class="Header-item mr-2">
            <button id="notification-indicator" class="btn-octicon notification-indicator position-relative" type="button" aria-label="Expand all sections">
                <svg class="octicon octicon-bell" viewBox="0 0 16 16" width="16" height="16">
                    <path d="M8 16a2 2 0 001.985-1.75c.017-.137-.097-.25-.235-.25h-3.5c-.138 0-.252.113-.235.25A2 2 0 008 16z"/>
                    <path fill-rule="evenodd" d="M8 1.5A3.5 3.5 0 004.5 5v2.947c0 .346-.102.683-.294.97l-1.703 2.556a.018.018 0 00-.003.01l.001.006c0 .002.002.004.004.006a.017.017 0 00.006.004l.007.001h10.964l.007-.001a.016.016 0 00.006-.004.016.016 0 00.004-.006l.001-.007a.017.017 0 00-.003-.01l-1.703-2.554a1.75 1.75 0 01-.294-.97V5A3.5 3.5 0 008 1.5zM3 5a5 5 0 0110 0v2.947c0 .05.015.098.042.139l1.703 2.555A1.518 1.518 0 0113.482 13H2.518a1.518 1.518 0 01-1.263-2.36l1.703-2.554A.25.25 0 003 7.947V5z"/>
                </svg>
                <span class="notification-badge" id="notification-badge">0</span>
            </button>
        </div>
        <div class="Header-item">
            <button id="theme-toggle" class="btn-octicon" type="button" aria-label="Toggle theme">
                <svg class="octicon octicon-sun" id="theme-icon-light" viewBox="0 0 16 16" width="16" height="16">
                    <path fill-rule="evenodd" d="M8 10.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM8 12a4 4 0 100-8 4 4 0 000 8zM8 0a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0V.75A.75.75 0 018 0zm0 13a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 018 13zM2.343 2.343a.75.75 0 011.061 0l1.06 1.061a.75.75 0 01-1.06 1.06l-1.06-1.06a.75.75 0 010-1.06v-.001zm9.193 9.193a.75.75 0 011.06 0l1.061 1.06a.75.75 0 01-1.06 1.061l-1.061-1.06a.75.75 0 010-1.061zM16 8a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 0116 8zM3 8a.75.75 0 01-.75.75H.75a.75.75 0 010-1.5h1.5A.75.75 0 013 8zm10.657-5.657a.75.75 0 010 1.061l-1.061 1.06a.75.75 0 11-1.06-1.06l1.06-1.06a.75.75 0 011.06 0h.001zm-9.193 9.193a.75.75 0 010 1.06l-1.06 1.061a.75.75 0 11-1.061-1.06l1.06-1.061a.75.75 0 011.061 0z"/>
                </svg>
                <svg class="octicon octicon-moon" id="theme-icon-dark" style="display: none;" viewBox="0 0 16 16" width="16" height="16">
                    <path fill-rule="evenodd" d="M9.598 1.591a.75.75 0 01.785-.175 7 7 0 11-8.967 8.967.75.75 0 01.961-.96 5.5 5.5 0 007.046-7.046.75.75 0 01.175-.786zm1.616 1.945a7 7 0 01-7.678 7.678 5.5 5.5 0 107.678-7.678z"/>
                </svg>
            </button>
        </div>
        <div class="Header-item">
            <div id="auth-container">
                <button id="sign-in-btn" class="btn btn-sm btn-primary" style="display: none;">
                    Sign in with GitHub
                </button>
                <details class="details-reset details-overlay" id="user-menu-container" style="display: none;">
                    <summary class="Header-link d-flex flex-items-center" aria-label="View profile and more">
                        <img id="user-avatar" class="avatar avatar-small circle mr-2" src="" alt="@user" width="20" height="20">
                        <span id="user-name" class="text-bold mr-1"></span>
                        <span id="collaborator-badge" class="Label Label--accent"></span>
                        <span class="dropdown-caret ml-1"></span>
                    </summary>
                    <details-menu class="dropdown-menu dropdown-menu-sw">
                        <div class="dropdown-header">
                            <strong id="dropdown-user-name"></strong>
                            <div class="text-secondary text-small" id="dropdown-user-role"></div>
                        </div>
                        <div class="dropdown-divider"></div>
                        <button id="sign-out-btn" class="dropdown-item" type="button">Sign out</button>
                    </details-menu>
                </details>
            </div>
        </div>
    </div>
    
    <!-- Main Content -->
    <main>
{report_body}
    </main>
    
    <!-- GitHub-like Challenge Modal -->
    <div id="challenge-modal" class="Overlay Overlay--hidden">
        <div class="Overlay-backdrop"></div>
        <div class="Overlay-content">
            <div class="Box">
                <div class="Box-header">
                    <h3 class="Box-title">Challenge Finding</h3>
                    <button id="modal-close-btn" class="btn-octicon" type="button" aria-label="Close">
                        <svg class="octicon octicon-x" viewBox="0 0 16 16" width="16" height="16">
                            <path fill-rule="evenodd" d="M3.72 3.72a.75.75 0 011.06 0L8 6.94l3.22-3.22a.75.75 0 111.06 1.06L9.06 8l3.22 3.22a.75.75 0 11-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 01-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 010-1.06z"/>
                        </svg>
                    </button>
                </div>
                <div class="Box-body">
                    <div class="flash mb-3">
                        <div id="modal-finding-text"></div>
                    </div>
                    
                    <div class="form-group">
                        <div class="form-group-header">
                            <label>Feedback Type</label>
                        </div>
                        <div class="form-checkbox">
                            <label>
                                <input type="radio" name="challenge-type" value="false-positive">
                                False Positive
                            </label>
                        </div>
                        <div class="form-checkbox">
                            <label>
                                <input type="radio" name="challenge-type" value="needs-context">
                                Needs More Context
                            </label>
                        </div>
                        <div class="form-checkbox">
                            <label>
                                <input type="radio" name="challenge-type" value="disagree-with-severity">
                                Disagree with Severity
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <div class="form-group-header">
                            <label for="challenge-feedback">Additional Details</label>
                        </div>
                        <textarea id="challenge-feedback" class="form-control" rows="4" placeholder="Explain why you're challenging this finding..."></textarea>
                    </div>
                    
                    <div class="form-actions">
                        <button id="submit-challenge-btn" class="btn btn-primary" type="button">Submit feedback</button>
                        <button class="btn" type="button" onclick="document.getElementById('challenge-modal').classList.add('Overlay--hidden')">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Store logo URLs
        const RADAR_LOGO_LIGHT = "{radar_logo_light}";
        const RADAR_LOGO_DARK = "{radar_logo_dark}";
{javascript}
    </script>
</body>
</html>
"""
    
    def _get_css_styles(self) -> str:
        """Get all CSS styles for the HTML page with GitHub-inspired design."""
        return """        /* GitHub-inspired CSS Variables and Base Styles */
        :root {
            --color-canvas-default: #ffffff;
            --color-canvas-subtle: #f6f8fa;
            --color-canvas-inset: #f0f3f6;
            --color-fg-default: #1F2328;
            --color-fg-muted: #656d76;
            --color-fg-subtle: #6e7781;
            --color-border-default: #d0d7de;
            --color-border-muted: #d8dee4;
            --color-border-subtle: rgba(27, 31, 36, 0.15);
            --color-shadow-small: 0 1px 0 rgba(27, 31, 36, 0.04);
            --color-shadow-medium: 0 3px 6px rgba(140, 149, 159, 0.15);
            --color-shadow-large: 0 8px 24px rgba(140, 149, 159, 0.2);
            --color-neutral-emphasis-plus: #24292f;
            --color-accent-fg: #0969da;
            --color-accent-emphasis: #0969da;
            --color-accent-muted: rgba(84, 174, 255, 0.4);
            --color-accent-subtle: #ddf4ff;
            --color-success-fg: #1a7f37;
            --color-success-emphasis: #2da44e;
            --color-attention-fg: #9a6700;
            --color-attention-emphasis: #bf8700;
            --color-danger-fg: #cf222e;
            --color-danger-emphasis: #da3633;
            --color-done-fg: #8250df;
            --color-done-emphasis: #8250df;
        }
        
        [data-color-mode="dark"] {
            --color-canvas-default: #0d1117;
            --color-canvas-subtle: #161b22;
            --color-canvas-inset: #010409;
            --color-fg-default: #e6edf3;
            --color-fg-muted: #7d8590;
            --color-fg-subtle: #6e7681;
            --color-border-default: #30363d;
            --color-border-muted: #21262d;
            --color-border-subtle: rgba(240, 246, 252, 0.1);
            --color-shadow-small: 0 0 transparent;
            --color-shadow-medium: 0 3px 6px #010409;
            --color-shadow-large: 0 8px 24px #010409;
            --color-neutral-emphasis-plus: #f0f6fc;
            --color-accent-fg: #58a6ff;
            --color-accent-emphasis: #1f6feb;
            --color-accent-muted: rgba(56, 139, 253, 0.4);
            --color-accent-subtle: rgba(56, 139, 253, 0.1);
            --color-success-fg: #3fb950;
            --color-success-emphasis: #238636;
            --color-attention-fg: #d29922;
            --color-attention-emphasis: #9e6a03;
            --color-danger-fg: #f85149;
            --color-danger-emphasis: #da3633;
            --color-done-fg: #a371f7;
            --color-done-emphasis: #8957e5;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: var(--color-fg-default);
            background-color: var(--color-canvas-default);
        }
        
        a {
            color: var(--color-accent-fg);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* GitHub Header */
        .Header {
            display: flex;
            padding: 16px;
            font-size: 14px;
            line-height: 1.5;
            color: var(--color-fg-default);
            background-color: var(--color-canvas-subtle);
            border-bottom: 1px solid var(--color-border-muted);
        }
        
        .Header-item {
            display: flex;
            margin-right: 16px;
            align-self: stretch;
            align-items: center;
            flex-wrap: nowrap;
        }
        
        .Header-item--full {
            flex: auto;
        }
        
        .Header-link {
            font-weight: 600;
            color: var(--color-fg-default);
            white-space: nowrap;
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        
        .Header-link:hover {
            color: var(--color-fg-muted);
            text-decoration: none;
        }
        
        .Header-title {
            display: flex;
            align-items: center;
        }
        
        .Header-navItem {
            padding: 0 8px;
        }
        
        /* Octicons */
        .octicon {
            vertical-align: text-bottom;
            fill: currentColor;
        }
        
        /* RADAR Logo */
        .radar-logo {
            border-radius: 6px;
        }
        
        /* GitHub Box Component */
        .Box {
            background-color: var(--color-canvas-default);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
        }
        
        .Box-header {
            padding: 16px;
            margin: -1px -1px 0 -1px;
            background-color: var(--color-canvas-subtle);
            border-color: var(--color-border-default);
            border-style: solid;
            border-width: 1px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        
        .Box-title {
            font-size: 14px;
            font-weight: 600;
            margin: 0;
        }
        
        .Box-body {
            padding: 16px;
        }
        
        .Box-row {
            padding: 16px;
            margin-top: -1px;
            list-style-type: none;
            border-top: 1px solid var(--color-border-muted);
        }
        
        .Box-row:first-of-type {
            border-top-color: transparent;
        }
        
        /* GitHub Buttons */
        .btn {
            position: relative;
            display: inline-block;
            padding: 5px 16px;
            font-size: 14px;
            font-weight: 500;
            line-height: 20px;
            white-space: nowrap;
            vertical-align: middle;
            cursor: pointer;
            user-select: none;
            border: 1px solid;
            border-radius: 6px;
            appearance: none;
            color: var(--color-btn-text);
            background-color: var(--color-btn-bg);
            border-color: var(--color-btn-border);
            box-shadow: var(--color-btn-shadow), var(--color-btn-inset-shadow);
            transition: 80ms cubic-bezier(0.33, 1, 0.68, 1);
            transition-property: color, background-color, border-color;
        }
        
        .btn {
            --color-btn-text: var(--color-fg-default);
            --color-btn-bg: var(--color-canvas-subtle);
            --color-btn-border: rgba(27, 31, 36, 0.15);
            --color-btn-shadow: 0 1px 0 rgba(27, 31, 36, 0.04);
            --color-btn-inset-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25);
        }
        
        [data-color-mode="dark"] .btn {
            --color-btn-text: var(--color-fg-default);
            --color-btn-bg: #21262d;
            --color-btn-border: rgba(240, 246, 252, 0.1);
            --color-btn-shadow: 0 0 transparent;
            --color-btn-inset-shadow: 0 0 transparent;
        }
        
        .btn:hover {
            background-color: var(--color-btn-hover-bg);
            border-color: var(--color-btn-hover-border);
        }
        
        .btn {
            --color-btn-hover-bg: #f3f4f6;
            --color-btn-hover-border: rgba(27, 31, 36, 0.15);
        }
        
        [data-color-mode="dark"] .btn {
            --color-btn-hover-bg: #30363d;
            --color-btn-hover-border: #8b949e;
        }
        
        .btn-primary {
            --color-btn-text: #fff;
            --color-btn-bg: #2da44e;
            --color-btn-border: rgba(27, 31, 36, 0.15);
            --color-btn-shadow: 0 1px 0 rgba(27, 31, 36, 0.1);
            --color-btn-inset-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
            --color-btn-hover-bg: #2c974b;
            --color-btn-hover-border: rgba(27, 31, 36, 0.15);
        }
        
        [data-color-mode="dark"] .btn-primary {
            --color-btn-text: #fff;
            --color-btn-bg: #238636;
            --color-btn-border: rgba(240, 246, 252, 0.1);
            --color-btn-hover-bg: #2ea043;
        }
        
        .btn-sm {
            padding: 3px 12px;
            font-size: 12px;
            line-height: 20px;
        }
        
        .btn-octicon {
            display: inline-block;
            padding: 5px;
            margin-left: 4px;
            line-height: 1;
            color: var(--color-fg-muted);
            vertical-align: middle;
            background: transparent;
            border: 0;
            cursor: pointer;
        }
        
        .btn-octicon:hover {
            color: var(--color-accent-fg);
        }
        
        /* Challenge button specific styling */
        .challenge-btn {
            background-color: var(--color-btn-bg);
            border-color: var(--color-btn-border);
        }
        
        .challenge-btn:hover {
            background-color: var(--color-btn-hover-bg);
            border-color: var(--color-accent-emphasis);
        }
        
        .challenge-btn.challenged {
            color: var(--color-success-fg);
            background-color: rgba(46, 160, 67, 0.1);
            border-color: var(--color-success-emphasis);
            cursor: not-allowed;
        }
        
        .challenge-btn.challenged::before {
            content: "✓ ";
        }
        
        /* Container */
        .container-lg {
            max-width: 1012px;
            margin-right: auto;
            margin-left: auto;
        }
        
        /* Padding utilities */
        .px-1 { padding-right: 4px !important; padding-left: 4px !important; }
        .px-2 { padding-right: 8px !important; padding-left: 8px !important; }
        .px-3 { padding-right: 16px !important; padding-left: 16px !important; }
        .py-1 { padding-top: 4px !important; padding-bottom: 4px !important; }
        .py-2 { padding-top: 8px !important; padding-bottom: 8px !important; }
        .py-4 { padding-top: 24px !important; padding-bottom: 24px !important; }
        .mt-2 { margin-top: 8px !important; }
        .mt-3 { margin-top: 16px !important; }
        .mb-0 { margin-bottom: 0 !important; }
        .mb-1 { margin-bottom: 4px !important; }
        .mb-2 { margin-bottom: 8px !important; }
        .mb-3 { margin-bottom: 16px !important; }
        .ml-1 { margin-left: 4px !important; }
        .ml-2 { margin-left: 8px !important; }
        .mr-1 { margin-right: 4px !important; }
        .mr-2 { margin-right: 8px !important; }
        .mr-3 { margin-right: 16px !important; }
        .mx-1 { margin-right: 4px !important; margin-left: 4px !important; }
        
        /* Display utilities */
        .d-flex { display: flex !important; }
        .d-none { display: none !important; }
        .flex-column { flex-direction: column !important; }
        .flex-wrap { flex-wrap: wrap !important; }
        .flex-items-center { align-items: center !important; }
        .flex-items-start { align-items: flex-start !important; }
        .flex-justify-between { justify-content: space-between !important; }
        .flex-1 { flex: 1 !important; min-width: 0; }
        .width-full { width: 100% !important; }
        .position-relative { position: relative !important; }
        
        /* Text utilities */
        .text-secondary { color: var(--color-fg-muted) !important; }
        .text-small { font-size: 12px !important; }
        .text-normal { font-weight: 400 !important; }
        .text-bold { font-weight: 600 !important; }
        .text-mono { font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, Liberation Mono, Menlo, monospace !important; }
        .f1 { font-size: 26px !important; }
        .f4 { font-size: 16px !important; }
        
        /* Background utilities */
        .bg-subtle { background-color: var(--color-canvas-subtle) !important; }
        
        /* Color utilities */
        .color-fg-danger { color: var(--color-danger-fg) !important; }
        .color-fg-attention { color: var(--color-attention-fg) !important; }
        .color-fg-success { color: var(--color-success-fg) !important; }
        .color-border-danger-emphasis { border-color: var(--color-danger-emphasis) !important; border-left-width: 3px !important; }
        .color-border-attention-emphasis { border-color: var(--color-attention-emphasis) !important; border-left-width: 3px !important; }
        .color-border-success-emphasis { border-color: var(--color-success-emphasis) !important; border-left-width: 3px !important; }
        
        /* Labels */
        .Label {
            display: inline-block;
            padding: 0 7px;
            font-size: 12px;
            font-weight: 500;
            line-height: 18px;
            border-radius: 2em;
            white-space: nowrap;
            border: 1px solid transparent;
        }
        
        .Label--primary {
            color: #ffffff;
            background-color: #0969da;
            border-color: transparent;
        }
        
        [data-color-mode="dark"] .Label--primary {
            background-color: #1f6feb;
        }
        
        .Label--success {
            color: #ffffff;
            background-color: #2da44e;
            border-color: transparent;
        }
        
        [data-color-mode="dark"] .Label--success {
            background-color: #238636;
        }
        
        .Label--attention {
            color: #000000;
            background-color: #fff8c5;
            border-color: rgba(212, 167, 44, 0.4);
        }
        
        [data-color-mode="dark"] .Label--attention {
            color: #f0f6fc;
            background-color: rgba(187, 128, 9, 0.15);
            border-color: rgba(187, 128, 9, 0.4);
        }
        
        .Label--danger {
            color: #ffffff;
            background-color: #d1242f;
            border-color: transparent;
        }
        
        [data-color-mode="dark"] .Label--danger {
            background-color: #da3633;
        }
        
        .Label--accent {
            color: var(--color-fg-default);
            background-color: var(--color-accent-subtle);
            border-color: var(--color-accent-muted);
            font-size: 11px;
        }
        
        /* Counter */
        .Counter {
            display: inline-block;
            padding: 2px 6px;
            font-size: 12px;
            font-weight: 500;
            line-height: 1;
            color: var(--color-fg-default);
            background-color: var(--color-neutral-muted);
            border: 1px solid transparent;
            border-radius: 20px;
        }
        
        [data-color-mode="dark"] .Counter {
            background-color: rgba(110, 118, 129, 0.2);
        }
        
        /* Branch name */
        .branch-name {
            display: inline-block;
            padding: 2px 6px;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, Liberation Mono, Menlo, monospace;
            font-size: 12px;
            color: var(--color-accent-fg);
            background-color: var(--color-accent-subtle);
            border-radius: 6px;
        }
        
        /* Commit SHA */
        .commit-sha {
            font-family: ui-monospace, SFMono-Regular, SF Mono, Consolas, Liberation Mono, Menlo, monospace;
            font-size: 12px;
        }
        
        /* Form elements */
        .form-control {
            padding: 5px 12px;
            font-size: 14px;
            line-height: 20px;
            color: var(--color-fg-default);
            vertical-align: middle;
            background-color: var(--color-canvas-default);
            background-repeat: no-repeat;
            background-position: right 8px center;
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            box-shadow: var(--color-primer-shadow-inset);
            transition: 80ms cubic-bezier(0.33, 1, 0.68, 1);
            transition-property: color, background-color, box-shadow, border-color;
            width: 100%;
        }
        
        .form-control:focus {
            background-color: var(--color-canvas-default);
            border-color: var(--color-accent-emphasis);
            outline: none;
            box-shadow: inset 0 0 0 1px var(--color-accent-emphasis);
        }
        
        .form-group {
            margin: 15px 0;
        }
        
        .form-group-header {
            margin: 0 0 6px;
        }
        
        .form-group-header label {
            font-weight: 600;
            font-size: 14px;
        }
        
        .form-checkbox {
            padding-left: 20px;
            margin: 8px 0;
        }
        
        .form-checkbox label {
            font-weight: normal;
            cursor: pointer;
        }
        
        .form-checkbox input[type="radio"] {
            float: left;
            margin: 2px 0 0 -20px;
            vertical-align: middle;
        }
        
        .form-actions {
            padding-top: 15px;
        }
        
        /* Details/Summary (GitHub dropdown style) */
        .Details {
            display: block;
        }
        
        .Details-summary {
            display: list-item;
            cursor: pointer;
            list-style: none;
        }
        
        .Details-summary::-webkit-details-marker {
            display: none;
        }
        
        .Details-summary .octicon-chevron {
            transition: transform 0.2s;
        }
        
        [open] > .Details-summary .octicon-chevron {
            transform: rotate(90deg);
        }
        
        /* Stats cards */
        .stats-card {
            transition: all 0.2s;
        }
        
        .stats-card:hover {
            box-shadow: var(--color-shadow-medium);
            transform: translateY(-2px);
        }
        
        .filterable-stat {
            cursor: pointer;
        }
        
        .filterable-stat.filter-active {
            background-color: var(--color-accent-subtle) !important;
            border-color: var(--color-accent-emphasis) !important;
        }
        
        /* Issue items */
        .issue-item {
            transition: all 0.2s;
        }
        
        .issue-item:hover {
            background-color: var(--color-canvas-subtle);
        }
        
        .issue-item .octicon {
            color: var(--color-fg-muted);
            flex-shrink: 0;
            margin-top: 2px;
        }
        
        .issue-item .octicon-issue-opened {
            color: var(--color-danger-fg);
        }
        
        .issue-item .octicon-alert {
            color: var(--color-attention-fg);
        }
        
        .issue-item.filtered-out {
            opacity: 0.3;
            pointer-events: none;
        }
        
        .issue-item.filtered-in {
            background-color: var(--color-accent-subtle);
            border-left: 3px solid var(--color-accent-emphasis);
            padding-left: 13px;
        }
        
        /* Flash messages */
        .flash {
            position: relative;
            padding: 16px;
            color: var(--color-fg-default);
            background-color: var(--color-canvas-subtle);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
        }
        
        .flash-success {
            color: var(--color-success-fg);
            background-color: rgba(46, 160, 67, 0.1);
            border-color: var(--color-success-emphasis);
        }
        
        [data-color-mode="dark"] .flash-success {
            background-color: rgba(46, 160, 67, 0.1);
        }
        
        /* Notification Badge */
        .notification-badge {
            position: absolute;
            top: -4px;
            right: -4px;
            min-width: 16px;
            height: 16px;
            padding: 0 4px;
            font-size: 10px;
            font-weight: 600;
            line-height: 16px;
            color: #fff;
            text-align: center;
            background-color: var(--color-danger-emphasis);
            border-radius: 8px;
            display: none;
        }
        
        .notification-badge.active {
            display: block;
        }
        
        /* Dropdown */
        .details-overlay {
            position: relative;
        }
        
        .dropdown-menu {
            position: absolute;
            top: 100%;
            right: 0;
            left: auto;
            z-index: 100;
            width: 180px;
            padding-top: 4px;
            padding-bottom: 4px;
            margin-top: 2px;
            background-color: var(--color-canvas-default);
            background-clip: padding-box;
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            box-shadow: var(--color-shadow-large);
        }
        
        .dropdown-menu-sw {
            right: 0;
            left: auto;
        }
        
        .dropdown-header {
            padding: 8px 16px;
            font-size: 12px;
            color: var(--color-fg-muted);
        }
        
        .dropdown-divider {
            height: 0;
            margin: 8px 0;
            border-top: 1px solid var(--color-border-muted);
        }
        
        .dropdown-item {
            display: block;
            width: 100%;
            padding: 4px 16px;
            color: var(--color-fg-default);
            text-align: left;
            background-color: transparent;
            border: 0;
            cursor: pointer;
        }
        
        .dropdown-item:hover {
            color: var(--color-fg-default);
            text-decoration: none;
            background-color: var(--color-accent-subtle);
        }
        
        .dropdown-caret {
            display: inline-block;
            width: 0;
            height: 0;
            vertical-align: middle;
            content: "";
            border-style: solid;
            border-width: 4px 4px 0;
            border-right-color: transparent;
            border-bottom-color: transparent;
            border-left-color: transparent;
            margin-left: 4px;
        }
        
        /* Avatar */
        .avatar {
            display: inline-block;
            overflow: hidden;
            line-height: 1;
            vertical-align: middle;
            border-radius: 6px;
            flex-shrink: 0;
        }
        
        .avatar-small {
            border-radius: 3px;
        }
        
        .circle {
            border-radius: 50% !important;
        }
        
        /* Link styles */
        .Link--primary {
            color: var(--color-accent-fg) !important;
            font-weight: 600;
        }
        
        .Link--primary:hover {
            text-decoration: underline;
        }
        
        /* Modal/Overlay */
        .Overlay {
            display: flex !important;
            position: fixed;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 99;
            align-items: center;
            justify-content: center;
        }
        
        .Overlay--hidden {
            display: none !important;
        }
        
        .Overlay-backdrop {
            position: fixed;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 99;
            background-color: rgba(27, 31, 36, 0.5);
        }
        
        [data-color-mode="dark"] .Overlay-backdrop {
            background-color: rgba(1, 4, 9, 0.8);
        }
        
        .Overlay-content {
            position: relative;
            z-index: 100;
            max-width: 640px;
            max-height: 80vh;
            overflow: auto;
            margin: auto;
        }
        
        /* Form data list */
        dl.form-group dt {
            margin: 0 0 6px;
            font-style: normal;
            font-weight: 600;
            font-size: 14px;
        }
        
        dl.form-group dd {
            margin-left: 0;
            margin-bottom: 16px;
        }
        
        .input-label {
            font-weight: 600;
            font-size: 14px;
            color: var(--color-fg-default);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .Header {
                flex-wrap: wrap;
            }
            
            .Header-item--full {
                order: 1;
                width: 100%;
                margin-top: 12px;
            }
        }"""
    
    def _get_javascript(self, pr_number: int) -> str:
        """Get all JavaScript code for the HTML page with GitHub-like interactions."""
        js_code = """        // ============================================================================
        // GitHub-inspired RADAR Report JavaScript
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
                    const dropdownNameEl = document.getElementById('dropdown-user-name');
                    const dropdownRoleEl = document.getElementById('dropdown-user-role');
                    
                    if (avatarEl) avatarEl.src = user.avatar_url || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"%3E%3Cpath fill="%23959da5" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/%3E%3C/svg%3E';
                    if (nameEl) nameEl.textContent = user.name || user.username;
                    if (dropdownNameEl) dropdownNameEl.textContent = user.name || user.username;
                    
                    let roleText = 'Member';
                    if (user.is_admin) {
                        roleText = 'Admin';
                        if (badgeEl) badgeEl.style.backgroundColor = 'var(--color-danger-subtle)';
                    } else if (user.is_collaborator) {
                        roleText = 'Collaborator';
                        if (badgeEl) badgeEl.style.backgroundColor = 'var(--color-success-subtle)';
                    } else {
                        roleText = 'PR Owner';
                        if (badgeEl) badgeEl.style.backgroundColor = 'var(--color-attention-subtle)';
                    }
                    
                    if (badgeEl) {
                        badgeEl.textContent = roleText;
                        badgeEl.style.display = 'inline-block';
                    }
                    if (dropdownRoleEl) {
                        dropdownRoleEl.textContent = roleText;
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
        
        // Theme Management (GitHub style)
        const themeToggle = document.getElementById('theme-toggle');
        const lightIcon = document.getElementById('theme-icon-light');
        const darkIcon = document.getElementById('theme-icon-dark');
        const htmlElement = document.documentElement;
        const radarLogo = document.getElementById('radar-logo');
        
        function setTheme(mode) {
            htmlElement.setAttribute('data-color-mode', mode);
            localStorage.setItem('theme', mode);
            
            if (mode === 'dark') {
                lightIcon.style.display = 'block';
                darkIcon.style.display = 'none';
                if (radarLogo) radarLogo.src = RADAR_LOGO_DARK;
            } else {
                lightIcon.style.display = 'none';
                darkIcon.style.display = 'block';
                if (radarLogo) radarLogo.src = RADAR_LOGO_LIGHT;
            }
        }
        
        // Check for saved theme or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-color-mode') || 'light';
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
        
        // Auth UI Events
        const signInBtn = document.getElementById('sign-in-btn');
        if (signInBtn) {
            signInBtn.addEventListener('click', () => RADAR_AUTH.signIn());
        }
        
        // User Menu Dropdown (GitHub details/summary style)
        const signOutBtn = document.getElementById('sign-out-btn');
        if (signOutBtn) {
            signOutBtn.addEventListener('click', () => {
                RADAR_AUTH.signOut();
            });
        }
        
        // Update notification badge
        function updateNotificationBadge() {
            const totalIssuesEl = document.getElementById('total-issues-count');
            const notificationBadge = document.getElementById('notification-badge');
            
            if (totalIssuesEl && notificationBadge) {
                const count = parseInt(totalIssuesEl.textContent) || 0;
                notificationBadge.textContent = count;
                if (count > 0) {
                    notificationBadge.classList.add('active');
                } else {
                    notificationBadge.classList.remove('active');
                }
            }
        }
        
        updateNotificationBadge();
        
        // Notification Bell - Expand All Specs
        const notificationIndicator = document.getElementById('notification-indicator');
        
        if (notificationIndicator) {
            notificationIndicator.addEventListener('click', function(e) {
                e.preventDefault();
                
                const specCards = document.querySelectorAll('.Details');
                let allExpanded = true;
                
                specCards.forEach(card => {
                    if (!card.hasAttribute('open')) {
                        allExpanded = false;
                    }
                });
                
                if (allExpanded) {
                    // Animate notification bell
                    this.style.animation = 'pulse 0.5s';
                    setTimeout(() => {
                        this.style.animation = '';
                    }, 500);
                    
                    if (specCards.length > 0) {
                        specCards[0].scrollIntoView({
                            behavior: 'smooth',
                            block: 'center'
                        });
                    }
                } else {
                    // Expand all
                    specCards.forEach((card) => {
                        card.setAttribute('open', '');
                    });
                    
                    if (specCards.length > 0) {
                        setTimeout(() => {
                            specCards[0].scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }, 100);
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
            document.getElementById('challenge-modal').classList.remove('Overlay--hidden');
            
            // Reset form
            document.querySelectorAll('input[name="challenge-type"]').forEach(radio => {
                radio.checked = false;
            });
            document.getElementById('challenge-feedback').value = '';
        }
        
        function closeChallengeModal() {
            document.getElementById('challenge-modal').classList.add('Overlay--hidden');
        }
        
        document.getElementById('modal-close-btn').addEventListener('click', closeChallengeModal);
        
        // Close modal on backdrop click
        document.querySelector('.Overlay-backdrop')?.addEventListener('click', closeChallengeModal);
        
        // Submit Challenge
        async function submitChallenge() {
            if (!RADAR_AUTH.isAuthenticated()) {
                alert('Please sign in with GitHub to submit feedback');
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
                alert('Please provide additional details about your feedback');
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
                    // Update button
                    const btn = document.querySelector(`.challenge-btn[data-finding-id="${currentFindingId}"]`);
                    if (btn) {
                        btn.textContent = 'Challenged';
                        btn.classList.add('challenged');
                        btn.disabled = true;
                    }
                    
                    // Update notification badge
                    const notificationBadge = document.getElementById('notification-badge');
                    if (notificationBadge) {
                        const currentCount = parseInt(notificationBadge.textContent) || 0;
                        const newCount = Math.max(0, currentCount - 1);
                        notificationBadge.textContent = newCount;
                        if (newCount === 0) {
                            notificationBadge.classList.remove('active');
                        }
                    }
                    
                    // Update total issues count
                    const totalIssuesEl = document.getElementById('total-issues-count');
                    if (totalIssuesEl) {
                        const currentCount = parseInt(totalIssuesEl.textContent) || 0;
                        const newCount = Math.max(0, currentCount - 1);
                        totalIssuesEl.textContent = newCount;
                    }
                    
                    closeChallengeModal();
                    alert('Thank you for your feedback! It has been submitted successfully.');
                } else {
                    if (response.status === 401) {
                        alert('Your session has expired. Please sign in again.');
                        RADAR_AUTH.signOut();
                        return;
                    }
                    alert(`Failed to submit feedback: ${result.error || 'Unknown error'}`);
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    alert('Request timeout: Server took too long to respond.');
                } else {
                    alert(`Error: ${error.message}`);
                }
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit feedback';
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
        
        // Severity filtering
        let activeSeverityFilter = null;
        
        function expandAllSpecCards() {
            document.querySelectorAll('.Details').forEach(card => {
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
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Escape to close modal
            if (e.key === 'Escape') {
                const modal = document.getElementById('challenge-modal');
                if (modal && !modal.classList.contains('Overlay--hidden')) {
                    closeChallengeModal();
                }
            }
            
            // Cmd/Ctrl + K for theme toggle
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                themeToggle.click();
            }
        });
        
        // Add pulse animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
        
        }); // End DOMContentLoaded"""
        
        return js_code.replace('{pr_number}', str(pr_number))