#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
post_github_comment.py
---------------------
Handles posting analysis results to GitHub PR comments.
This script is designed to be run as a separate step after the main analysis.
"""

import os
import sys
import json
import logging
import argparse
from typing import Dict, List, Any, Optional

from GitHubClient import GitHubClient
from AntiPatternDetector import Severity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("github-comment-poster")

def load_analysis_report(report_file_path: str) -> Dict[str, Any]:
    """
    Loads the analysis report from a JSON file.
    
    Args:
        report_file_path: Path to the JSON report file
        
    Returns:
        Dictionary containing the analysis results
    """
    logger.info(f"Loading analysis report from {report_file_path}")
    try:
        with open(report_file_path, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load analysis report: {str(e)}")
        return {}

def extract_severity_from_report(report: Dict[str, Any]) -> Severity:
    """
    Extracts the highest severity level from the report.
    
    Args:
        report: Analysis report dictionary
        
    Returns:
        Highest Severity level found
    """
    severity_str = report.get("highest_severity", "INFO")
    try:
        return Severity[severity_str]
    except KeyError:
        logger.warning(f"Unknown severity level: {severity_str}, defaulting to INFO")
        return Severity.INFO

def create_concise_comment(severity: Severity, anti_patterns: List[Dict], ai_analysis: str, conclusion: str) -> str:
    """
    Creates a very concise, focused comment for GitHub PR with only the most relevant details.
    
    Args:
        severity: Highest severity level detected
        anti_patterns: List of anti-patterns detected
        ai_analysis: AI-generated analysis text
        conclusion: Conclusion summary
        
    Returns:
        Formatted markdown for a GitHub comment
    """
    # Start with a header based on severity level
    if severity == Severity.CRITICAL:
        header = f"## 🚨 CRITICAL ISSUES DETECTED\n\n"
    elif severity == Severity.ERROR:
        header = f"## ❌ ERROR ISSUES DETECTED\n\n"
    elif severity == Severity.WARNING:
        header = f"## ⚠️ WARNING ISSUES DETECTED\n\n" 
    else:  # INFO or None
        header = f"## ✅ NO ISSUES DETECTED\n\n"
    
    # Group issues by severity
    critical_issues = [ap for ap in anti_patterns if ap.get("severity", "") == "CRITICAL"]
    error_issues = [ap for ap in anti_patterns if ap.get("severity", "") == "ERROR"]
    warning_issues = [ap for ap in anti_patterns if ap.get("severity", "") == "WARNING"]
    info_issues = [ap for ap in anti_patterns if ap.get("severity", "") == "INFO"]
    
    # Build comment body
    comment = header
    
    # Add relevant message based on severity
    if severity in [Severity.ERROR, Severity.CRITICAL]:
        comment += "These issues **must be fixed** before the PR can be merged.\n\n"
    elif severity in [Severity.WARNING, Severity.INFO] and (warning_issues or info_issues):
        comment += "Issues don't block PR merge, but review is recommended.\n\n"
    
    # Add issues by severity
    issue_sections = []
    
    if critical_issues:
        critical_section = "### 🚨 Critical Issues\n\n"
        for issue in critical_issues:
            critical_section += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            critical_section += f"  - **Fix**: {issue.get('recommendation', '')}\n"
        issue_sections.append(critical_section)
    
    if error_issues:
        error_section = "### ❌ Errors\n\n"
        for issue in error_issues:
            error_section += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            error_section += f"  - **Fix**: {issue.get('recommendation', '')}\n"
        issue_sections.append(error_section)
    
    if warning_issues:
        warning_section = "### ⚠️ Warnings\n\n"
        for issue in warning_issues:
            warning_section += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            warning_section += f"  - **Recommendation**: {issue.get('recommendation', '')}\n"
        issue_sections.append(warning_section)
    
    if info_issues:
        info_section = "### ℹ️ Information\n\n"
        for issue in info_issues:
            info_section += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
        issue_sections.append(info_section)
    
    # Add issue sections to comment
    for section in issue_sections:
        comment += section + "\n"
    
    # Find most relevant analysis focused on the detected issues
    if ai_analysis and (critical_issues or error_issues or warning_issues):
        # Create a focused analysis that's directly related to the detected issues
        comment += "### 🧠 Analysis\n\n"
        
        # Find the most specific analysis related to the issue types we detected
        issue_keywords = set()
        
        # Collect keywords from issues to find relevant analysis sections
        for issue in critical_issues + error_issues + warning_issues:
            name = issue.get('name', '').lower()
            if 'patch' in name:
                issue_keywords.add('patch')
            if 'cve' in name:
                issue_keywords.add('cve')
            if 'changelog' in name:
                issue_keywords.add('changelog')
        
        # Find the most relevant section based on the issue keywords
        relevant_text = ""
        
        if 'patch' in issue_keywords:
            # Search for sections specific to patch issues
            patch_terms = ['Missing Patch', 'placeholder patch', 'patch file', 'CVE-2024-xxxx', 'Patch4']
            for term in patch_terms:
                if term.lower() in ai_analysis.lower():
                    # Find a short paragraph containing this term
                    for paragraph in ai_analysis.split('\n\n'):
                        if term.lower() in paragraph.lower() and len(paragraph) < 300:
                            relevant_text = paragraph
                            break
                
                if relevant_text:
                    break
        
        # If we didn't find specific analysis, use a brief general summary
        if not relevant_text:
            lines = ai_analysis.strip().split('\n')
            for line in lines:
                if len(line) > 20 and len(line) < 300:  # Find a reasonably sized line
                    relevant_text = line
                    break
            
            if not relevant_text:
                relevant_text = ai_analysis[:200] + "..."
        
        comment += relevant_text.strip() + "\n\n"
    
    # Add very focused recommendations
    if conclusion:
        comment += "### 📝 Recommendations\n\n"
        
        # Clean up conclusion text
        clean_conclusion = conclusion.replace("📝 CONCLUSION (extracted from recommendations)", "").strip()
        clean_conclusion = clean_conclusion.replace("📝 CONCLUSION", "").strip()
        
        # For each issue type, find the most relevant recommendation
        recommendations = []
        
        # Focus on the most important recommendations based on detected errors
        if any('patch' in issue.get('name', '').lower() for issue in error_issues + critical_issues):
            if "Remove or correct Patch4" in clean_conclusion:
                rec = "• Remove or correct the incorrect patch entry (Patch4: CVE-2024-xxxx.patch).\n"
                rec += "• Either replace it with a valid CVE patch file or remove it from the spec file.\n"
                recommendations.append(rec)
        
        # If we didn't find any specific recommendations, use a summarized version
        if not recommendations:
            # Get the first bullet point or recommendation section
            for line in clean_conclusion.split("\n"):
                if line.strip().startswith("•") or line.strip().startswith("-") or line.strip().startswith("*"):
                    recommendations.append(line.strip())
                    
                    # Get the next line if it's part of the same bullet point
                    next_line_idx = clean_conclusion.split("\n").index(line) + 1
                    if next_line_idx < len(clean_conclusion.split("\n")):
                        next_line = clean_conclusion.split("\n")[next_line_idx]
                        if not (next_line.strip().startswith("•") or next_line.strip().startswith("-") or next_line.strip().startswith("*")):
                            recommendations.append(next_line.strip())
                    
                    break
                    
        # If we still don't have a recommendation, use a brief excerpt
        if not recommendations:
            first_100_chars = clean_conclusion[:100].strip()
            if first_100_chars:
                recommendations.append(first_100_chars + "...")
        
        # Add the recommendations
        for rec in recommendations:
            comment += rec + "\n\n"
    
    # Add footer
    comment += "---\n"
    comment += "*This comment was automatically generated by the Azure Linux PR Check. See ADO pipeline logs for full details.*"
    
    return comment

def post_github_comment(report: Dict[str, Any], use_checks_api: bool = False) -> int:
    """
    Posts the analysis results as a comment on the GitHub PR.
    
    Args:
        report: Analysis report dictionary
        use_checks_api: Whether to use GitHub Checks API
        
    Returns:
        Exit code: 0 for success, non-zero for failure
    """
    # Skip GitHub updates if no GitHub token is available
    if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("SYSTEM_ACCESSTOKEN")):
        logger.error("No GitHub token available (GITHUB_TOKEN or SYSTEM_ACCESSTOKEN), cannot post comments")
        return 1
    
    # Debug environment variables related to GitHub authentication and context
    logger.info("GitHub Environment Variables:")
    logger.info(f"  - GITHUB_TOKEN: {'Set' if os.environ.get('GITHUB_TOKEN') else 'Not Set'}")
    logger.info(f"  - SYSTEM_ACCESSTOKEN: {'Set' if os.environ.get('SYSTEM_ACCESSTOKEN') else 'Not Set'}")
    logger.info(f"  - GITHUB_REPOSITORY: {os.environ.get('GITHUB_REPOSITORY', 'Not Set')}")
    logger.info(f"  - GITHUB_PR_NUMBER: {os.environ.get('GITHUB_PR_NUMBER', 'Not Set')}")
    logger.info(f"  - BUILD_REPOSITORY_NAME: {os.environ.get('BUILD_REPOSITORY_NAME', 'Not Set')}")
    
    # Initialize GitHub client
    github_client = GitHubClient()
    
    # Verify GitHub client initialization
    if not github_client.repo_name or not github_client.pr_number:
        logger.error(f"GitHub client initialization failed: repo={github_client.repo_name}, PR={github_client.pr_number}")
        return 1
    
    # Extract information from report
    severity = extract_severity_from_report(report)
    anti_patterns = report.get("anti_patterns", [])
    ai_analysis = report.get("ai_analysis", "")
    conclusion = report.get("conclusion", "")
    
    # Create a concise, focused comment
    comment_body = create_concise_comment(severity, anti_patterns, ai_analysis, conclusion)
        
    # Log a preview of the comment
    logger.info(f"Comment preview: {comment_body[:100]}...")
    
    # Post or update comment
    result = github_client.post_or_update_comment(comment_body, "azure-linux-spec-check")
    logger.info(f"Comment post result: {result}")
    
    # Check for errors
    if isinstance(result, dict) and result.get("error"):
        logger.error(f"Error posting comment: {result.get('error')}")
        return 1
        
    # Update commit status if using Checks API
    if use_checks_api:
        # Get commit SHA from environment
        commit_sha = os.environ.get("SYSTEM_PULLREQUEST_SOURCECOMMITID")
        if not commit_sha:
            logger.warning("SYSTEM_PULLREQUEST_SOURCECOMMITID not set, skipping status update")
        else:
            logger.info(f"Updating GitHub status for commit {commit_sha}")
            status_result = github_client.create_severity_status(severity, commit_sha)
            logger.info(f"Status update result: {status_result}")
    
    return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Post analysis results to GitHub PR comments")
    parser.add_argument('--report-file', required=True,
                        help='Path to the JSON report file with analysis results')
    parser.add_argument('--use-github-checks', action='store_true',
                        help='Use GitHub Checks API for status updates')
    args = parser.parse_args()
    
    # Load analysis results
    report = load_analysis_report(args.report_file)
    if not report:
        logger.error("Failed to load valid analysis report, cannot post comment")
        return 1
        
    # Post comment with analysis results
    return post_github_comment(report, args.use_github_checks)

if __name__ == "__main__":
    sys.exit(main())
