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
    Creates a concise, focused comment for GitHub PR with clear severity indication,
    issues, analysis, and recommendations.
    
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
    
    # For ERROR and CRITICAL, explain that issues must be fixed
    if severity in [Severity.ERROR, Severity.CRITICAL]:
        comment += "These issues **must be fixed** before the PR can be merged.\n\n"
    
    # For WARNING and INFO, indicate they can still be merged
    if severity in [Severity.WARNING, Severity.INFO] and (warning_issues or info_issues):
        comment += "Issues don't block PR merge, but review is recommended.\n\n"
    
    # Start with CRITICAL issues
    if critical_issues:
        comment += "### 🚨 Critical Issues\n\n"
        for issue in critical_issues:
            comment += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            comment += f"  - **Fix**: {issue.get('recommendation', '')}\n"
        comment += "\n"
    
    # Then ERROR issues
    if error_issues:
        comment += "### ❌ Errors\n\n"
        for issue in error_issues:
            comment += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            comment += f"  - **Fix**: {issue.get('recommendation', '')}\n"
        comment += "\n"
    
    # Then WARNINGS
    if warning_issues:
        comment += "### ⚠️ Warnings\n\n"
        for issue in warning_issues:
            comment += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
            comment += f"  - **Recommendation**: {issue.get('recommendation', '')}\n"
        comment += "\n"
    
    # Then INFO items
    if info_issues:
        comment += "### ℹ️ Information\n\n"
        for issue in info_issues:
            comment += f"- **{issue.get('name', '')}**: {issue.get('description', '')}\n"
        comment += "\n"
    
    # Add a brief AI analysis summary - but make sure it's included
    if ai_analysis:
        comment += "### 🧠 Analysis\n\n"
        
        # Extract key sections from the analysis 
        # Look for sections about security implications, patch verification, or recommendations
        sections = []
        if "Security Implications" in ai_analysis:
            security_section = ai_analysis.split("Security Implications")[1].split("\n──────────")[0].strip()
            sections.append(security_section)
        
        if "Verification of CVE Patch" in ai_analysis:
            patch_section = ai_analysis.split("Verification of CVE Patch")[1].split("\n──────────")[0].strip()
            sections.append(patch_section)
        
        # If we couldn't find specific sections, use the first paragraph
        if not sections:
            ai_summary = ai_analysis.strip().split("\n\n")[0] if "\n\n" in ai_analysis else ai_analysis[:400]
            if len(ai_summary) > 400:
                ai_summary = ai_summary[:400] + "..."
            sections.append(ai_summary)
            
        # Add the selected sections
        for section in sections[:2]:  # Limit to 2 sections to keep it brief
            comment += f"{section}\n\n"
            
        comment += "*See ADO pipeline logs for complete analysis.*\n\n"
    
    # Add recommendations from conclusion (without the redundant "CONCLUSION" label)
    if conclusion:
        comment += "### 📝 Recommendations\n\n"
        
        # Extract the recommendation portion, removing any "CONCLUSION" prefix
        clean_conclusion = conclusion.replace("📝 CONCLUSION (extracted from recommendations)", "").strip()
        clean_conclusion = clean_conclusion.replace("📝 CONCLUSION", "").strip()
        
        # Extract key recommendations - look for bullet points or numbered items
        recommendation_parts = []
        
        # Try to find the "Recommendations" section
        if "Recommendations" in clean_conclusion:
            rec_section = clean_conclusion.split("Recommendations")[1].split("\n──────────")[0].strip()
            recommendation_parts.append(rec_section)
        
        # If we have specific "Remove or Replace" guidance, include it
        if "Remove or Replace" in clean_conclusion:
            replace_section = clean_conclusion.split("Remove or Replace")[1].split("\n──────────")[0].strip()
            if replace_section not in recommendation_parts:
                recommendation_parts.append(replace_section)
        
        # If we still don't have recommendations, just use the first section
        if not recommendation_parts:
            first_part = clean_conclusion.split("\n──────────")[0].strip()
            recommendation_parts.append(first_part)
            
        # Format and add recommendations
        for part in recommendation_parts[:2]:  # Limit to 2 sections to keep it brief
            # Remove redundant prefix indicators if present
            part = part.replace("Remove or Replace Patch4:", "").strip()
            comment += f"{part}\n\n"
    
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
