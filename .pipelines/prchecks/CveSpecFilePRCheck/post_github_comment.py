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
    
    # Format a comment based on severity and issues
    comment_body = github_client.format_severity_comment(severity, anti_patterns, ai_analysis)
    
    # Include conclusion in the main comment
    if conclusion:
        comment_body += "\n\n" + conclusion
        
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
