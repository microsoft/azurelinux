#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
GitHubClient
-----------
Handles interactions with GitHub API for reporting PR check results
with nuanced severity levels and posting detailed comments.
"""

import os
import requests
import logging
import json
from enum import Enum
from typing import Dict, List, Any, Optional
from AntiPatternDetector import Severity

# Configure logging
logger = logging.getLogger("github-client")

class CheckStatus(Enum):
    """GitHub Check API status values"""
    SUCCESS = "success"      # All good, everything passes
    NEUTRAL = "neutral"      # Informational, doesn't block merging
    FAILURE = "failure"      # Failed check, blocks merging
    CANCELLED = "cancelled"  # Check was cancelled
    SKIPPED = "skipped"      # Check was skipped
    TIMED_OUT = "timed_out"  # Check timed out
    IN_PROGRESS = "in_progress"  # Check is running

class GitHubClient:
    """Client for interacting with GitHub API for PR checks and comments"""
    
    def __init__(self):
        """Initialize the GitHub client using environment variables for auth"""
        # Get required environment variables
        self.token = os.environ.get("GITHUB_ACCESS_TOKEN")
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "")  # Format: owner/repo
        self.pr_number = os.environ.get("GITHUB_PR_NUMBER", "")
        
        # Validate required environment variables
        if not self.token:
            logger.warning("GITHUB_ACCESS_TOKEN not set, GitHub API interactions will be disabled")
        
        if not self.repo_name or not self.pr_number:
            logger.warning("GITHUB_REPOSITORY or GITHUB_PR_NUMBER not set, GitHub API interactions will be limited")
        
        # Set up base API URL and headers
        self.api_base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
    def create_check_run(self, name: str, head_sha: str, status: CheckStatus, 
                         conclusion: Optional[CheckStatus] = None,
                         output_title: Optional[str] = None, 
                         output_summary: Optional[str] = None,
                         output_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new check run with the specified status.
        
        Args:
            name: The name of the check
            head_sha: The SHA of the commit to check
            status: The current status of the check
            conclusion: The final conclusion (required if status is "completed")
            output_title: Title of the check output
            output_summary: Summary of the check output
            output_text: Detailed text of the check output
            
        Returns:
            Response from GitHub API
        """
        if not self.token:
            logger.warning("GitHub API token not available, skipping check run creation")
            return {}
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/check-runs"
        
        payload = {
            "name": name,
            "head_sha": head_sha,
            "status": status.value
        }
        
        if status == CheckStatus.COMPLETED and conclusion:
            payload["conclusion"] = conclusion.value
        
        if output_title and output_summary:
            payload["output"] = {
                "title": output_title,
                "summary": output_summary
            }
            
            if output_text:
                payload["output"]["text"] = output_text
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create check run: {str(e)}")
            return {}
    
    def post_pr_comment(self, body: str) -> Dict[str, Any]:
        """
        Post a comment on the PR.
        
        Args:
            body: The markdown content of the comment
            
        Returns:
            Response from GitHub API
        """
        if not self.token or not self.repo_name or not self.pr_number:
            logger.warning("Required GitHub params not available, skipping comment posting")
            return {}
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/{self.pr_number}/comments"
        
        payload = {
            "body": body
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to post PR comment: {str(e)}")
            return {}
    
    def get_pr_comments(self) -> List[Dict[str, Any]]:
        """
        Get existing comments on the PR.
        
        Returns:
            List of comment objects from GitHub API
        """
        if not self.token or not self.repo_name or not self.pr_number:
            logger.warning("Required GitHub params not available, skipping comment retrieval")
            return []
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/{self.pr_number}/comments"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get PR comments: {str(e)}")
            return []
    
    def delete_pr_comment(self, comment_id: int) -> bool:
        """
        Delete a comment on the PR.
        
        Args:
            comment_id: ID of the comment to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.token or not self.repo_name:
            logger.warning("Required GitHub params not available, skipping comment deletion")
            return False
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/comments/{comment_id}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete PR comment: {str(e)}")
            return False
    
    def update_pr_comment(self, comment_id: int, body: str) -> Dict[str, Any]:
        """
        Update an existing comment on the PR.
        
        Args:
            comment_id: ID of the comment to update
            body: New content for the comment
            
        Returns:
            Response from GitHub API
        """
        if not self.token or not self.repo_name:
            logger.warning("Required GitHub params not available, skipping comment update")
            return {}
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/comments/{comment_id}"
        
        payload = {
            "body": body
        }
        
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update PR comment: {str(e)}")
            return {}
    
    def post_or_update_comment(self, body: str, marker: str) -> Dict[str, Any]:
        """
        Post a new comment or update an existing one with the same marker.
        
        The marker is a unique string that identifies comments from this tool,
        allowing us to find and update our previous comments instead of creating duplicates.
        
        Args:
            body: Comment content
            marker: Unique marker to identify this type of comment
            
        Returns:
            Response from GitHub API
        """
        # Add the marker as a hidden HTML comment
        marked_body = f"<!-- {marker} -->\n{body}"
        
        # Get existing comments
        comments = self.get_pr_comments()
        
        # Look for our previous comment with the same marker
        for comment in comments:
            if f"<!-- {marker} -->" in comment.get("body", ""):
                # Found our comment, update it
                return self.update_pr_comment(comment["id"], marked_body)
        
        # Didn't find a comment with our marker, create a new one
        return self.post_pr_comment(marked_body)
    
    def create_severity_status(self, severity: Severity, commit_sha: str) -> Dict[str, Any]:
        """
        Create a status for the PR based on the severity level.
        
        Args:
            severity: Highest severity level of detected issues
            commit_sha: SHA of the commit to update status for
            
        Returns:
            Response from GitHub API
        """
        if not self.token or not self.repo_name:
            logger.warning("Required GitHub params not available, skipping status update")
            return {}
        
        url = f"{self.api_base_url}/repos/{self.repo_name}/statuses/{commit_sha}"
        
        # Map severity levels to status states and descriptions
        if severity == Severity.CRITICAL:
            state = "failure"
            description = "Critical issues found - must be fixed"
        elif severity == Severity.ERROR:
            state = "failure"
            description = "Errors found - must be fixed"
        elif severity == Severity.WARNING:
            state = "success"
            description = "Warnings found - review recommended"
        else:  # INFO or None
            state = "success"
            description = "All checks passed successfully"
        
        payload = {
            "state": state,
            "description": description,
            "context": "Azure Linux Spec Validator"  # This is what shows up in the GitHub UI
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create status: {str(e)}")
            return {}

    @staticmethod
    def format_severity_comment(severity: Severity, issues: List[Dict[str, Any]], 
                               ai_analysis: str = "") -> str:
        """
        Format a comment based on the severity of issues.
        
        Args:
            severity: Highest severity level of detected issues
            issues: List of issue dictionaries with details
            ai_analysis: Optional AI-generated analysis to include
            
        Returns:
            Formatted markdown for a GitHub comment
        """
        # Start with a header based on severity level
        if severity == Severity.CRITICAL:
            header = "## 🚨 CRITICAL ISSUES DETECTED\n\n"
            header += "These issues **must be fixed** before the PR can be merged.\n\n"
        elif severity == Severity.ERROR:
            header = "## ❌ ERRORS DETECTED\n\n"
            header += "These issues **must be fixed** before the PR can be merged.\n\n"
        elif severity == Severity.WARNING:
            header = "## ⚠️ WARNINGS DETECTED\n\n"
            header += "Review recommended, but PR can still be merged.\n\n"
        else:  # INFO or None
            header = "## ✅ VALIDATION SUCCESSFUL\n\n"
            if issues:
                header += "Some informational notes were detected, but they don't require action.\n\n"
            else:
                header += "No issues were detected in the spec files.\n\n"
        
        # Add issues by category
        comment = header
        
        # Group issues by severity
        critical_issues = [i for i in issues if i.get("severity") == "CRITICAL"]
        error_issues = [i for i in issues if i.get("severity") == "ERROR"]
        warning_issues = [i for i in issues if i.get("severity") == "WARNING"]
        info_issues = [i for i in issues if i.get("severity") == "INFO"]
        
        # Add critical issues
        if critical_issues:
            comment += "### 🚨 Critical Issues\n\n"
            for issue in critical_issues:
                comment += f"- **{issue.get('name')}**: {issue.get('description')}\n"
                if issue.get('recommendation'):
                    comment += f"  - **Fix**: {issue.get('recommendation')}\n"
            comment += "\n"
        
        # Add error issues
        if error_issues:
            comment += "### ❌ Errors\n\n"
            for issue in error_issues:
                comment += f"- **{issue.get('name')}**: {issue.get('description')}\n"
                if issue.get('recommendation'):
                    comment += f"  - **Fix**: {issue.get('recommendation')}\n"
            comment += "\n"
        
        # Add warning issues
        if warning_issues:
            comment += "### ⚠️ Warnings\n\n"
            for issue in warning_issues:
                comment += f"- **{issue.get('name')}**: {issue.get('description')}\n"
                if issue.get('recommendation'):
                    comment += f"  - **Fix**: {issue.get('recommendation')}\n"
            comment += "\n"
        
        # Add info issues
        if info_issues:
            comment += "### ℹ️ Informational\n\n"
            for issue in info_issues:
                comment += f"- **{issue.get('name')}**: {issue.get('description')}\n"
            comment += "\n"
        
        # Add AI analysis summary if provided
        if ai_analysis:
            # Truncate if too long for a comment
            max_length = 5000
            if len(ai_analysis) > max_length:
                ai_summary = ai_analysis[:max_length] + "...\n\n*(Analysis truncated. See full analysis in ADO logs)*"
            else:
                ai_summary = ai_analysis
                
            comment += "### 🧠 AI Analysis Summary\n\n"
            comment += ai_summary + "\n\n"
        
        # Add footer
        comment += "---\n"
        comment += "*This comment was automatically generated by the Azure Linux PR Check system. " 
        comment += "See ADO pipeline logs for full details.*"
        
        return comment