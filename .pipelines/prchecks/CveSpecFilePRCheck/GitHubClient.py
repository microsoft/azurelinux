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
import re
from enum import Enum
from typing import Dict, List, Any, Optional
from AntiPatternDetector import Severity

# Configure logging
logging.basicConfig(level=logging.INFO)
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
        # Try multiple token environment variables in order of preference
        token_vars = [
            "GITHUB_TOKEN",  # Prioritize CBL-Mariner bot PAT from key vault
            "SYSTEM_ACCESSTOKEN",  # Fall back to Azure DevOps OAuth token
            "GITHUB_ACCESS_TOKEN",
            "AZDO_GITHUB_TOKEN"
        ]
        
        self.token = None
        for var in token_vars:
            if os.environ.get(var):
                self.token = os.environ.get(var)
                logger.info(f"Using {var} for GitHub authentication")
                break
                
        # Get repository details from environment variables
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "")  # Format: owner/repo
        
        # If GITHUB_REPOSITORY not set or empty, try to construct from BUILD_REPOSITORY_NAME
        if not self.repo_name or self.repo_name == "":
            self.repo_name = os.environ.get("BUILD_REPOSITORY_NAME", "")
            logger.info(f"Using BUILD_REPOSITORY_NAME: {self.repo_name}")
            
        # For Azure DevOps hosted repos, convert to GitHub format if needed
        if self.repo_name and "/" not in self.repo_name:
            if "microsoft" in self.repo_name.lower():
                self.repo_name = f"microsoft/{self.repo_name}"
                logger.info(f"Converted repo name to GitHub format: {self.repo_name}")
        
        # Get PR number from multiple possible environment variables
        pr_vars = [
            "GITHUB_PR_NUMBER",
            "SYSTEM_PULLREQUEST_PULLREQUESTNUMBER", 
            "SYSTEM_PULLREQUEST_PULLREQUESTID"
        ]
        
        self.pr_number = ""
        for var in pr_vars:
            if os.environ.get(var):
                self.pr_number = os.environ.get(var)
                logger.info(f"Using {var} for PR number: {self.pr_number}")
                break
                
        # If PR number still not found, try to extract from the source branch
        if not self.pr_number:
            source_branch = os.environ.get("BUILD_SOURCEBRANCH", "") or os.environ.get("SYSTEM_PULLREQUEST_SOURCEBRANCH", "")
            logger.info(f"Trying to extract PR number from branch: {source_branch}")
            
            match = re.match(r"refs/pull/(\d+)", source_branch)
            if match:
                self.pr_number = match.group(1)
                logger.info(f"Extracted PR number from branch: {self.pr_number}")
        
        # Validate and log configuration state
        if not self.token:
            logger.error("No GitHub token found in environment variables")
        else:
            # Safely log token prefix (first few chars only)
            token_prefix = self.token[:4] if self.token else ""
            logger.info(f"GitHub token prefix: {token_prefix}...")
            
        logger.info(f"GitHub repository: {self.repo_name}")
        logger.info(f"GitHub PR number: {self.pr_number}")
        
        # Set up base API URL and headers for GitHub API
        self.api_base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Azure-Linux-PR-Check"
        }
        
        # Add authorization header if token is available
        if self.token:
            # For Azure DevOps System.AccessToken, use Bearer format
            if os.environ.get("SYSTEM_ACCESSTOKEN") == self.token:
                self.headers["Authorization"] = f"Bearer {self.token}"
                logger.info("Using Bearer authentication format for Azure DevOps token")
            else:
                # GitHub PATs use the token format
                self.headers["Authorization"] = f"token {self.token}"
                logger.info("Using token authentication format for GitHub PAT")
    
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
            logger.error(f"Missing required params - token: {'✓' if self.token else '✗'}, repo: {self.repo_name}, pr: {self.pr_number}")
            return {}
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/{self.pr_number}/comments"
        logger.info(f"Posting comment to: {url}")
        
        payload = {
            "body": body
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            logger.info("✅ Successfully posted comment")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to post PR comment: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
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
    
    def add_label(self, label: str) -> Dict[str, Any]:
        """
        Add a label to the PR.
        
        Args:
            label: The label name to add
            
        Returns:
            Response from GitHub API
        """
        if not self.token or not self.repo_name or not self.pr_number:
            logger.error(f"Missing required params - token: {'✓' if self.token else '✗'}, repo: {self.repo_name}, pr: {self.pr_number}")
            return {}
            
        url = f"{self.api_base_url}/repos/{self.repo_name}/issues/{self.pr_number}/labels"
        logger.info(f"Adding label '{label}' to PR #{self.pr_number}")
        
        payload = {
            "labels": [label]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            logger.info(f"✅ Successfully added label '{label}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to add label '{label}': {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
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
        
        # Check if required environment variables are set
        if not self.token:
            logger.error("GitHub token not set - cannot post comments. Check GITHUB_TOKEN environment variable.")
            return {"error": "No GitHub token available"}
            
        if not self.repo_name:
            logger.error("GitHub repository not set - cannot post comments. Check GITHUB_REPOSITORY environment variable.")
            return {"error": "No GitHub repository specified"}
            
        if not self.pr_number:
            logger.error("GitHub PR number not set - cannot post comments. Check GITHUB_PR_NUMBER environment variable.")
            return {"error": "No GitHub PR number specified"}
            
        # Log authentication details (safely)
        auth_header = self.headers.get("Authorization", "None")
        auth_type = "Bearer" if auth_header.startswith("Bearer ") else "token" if auth_header.startswith("token ") else "Unknown"
        token_prefix = self.token[:4] if self.token else "None"
        
        logger.info(f"Attempting to post or update comment with marker: {marker}")
        logger.info(f"Repository: {self.repo_name}")
        logger.info(f"PR number: {self.pr_number}")
        logger.info(f"Auth type: {auth_type}, Token prefix: {token_prefix}...")
        
        # Get existing comments
        comments = self.get_pr_comments()
        
        # Look for our previous comment with the same marker
        for comment in comments:
            if f"<!-- {marker} -->" in comment.get("body", ""):
                # Found our comment, update it
                logger.info(f"Found existing comment with ID {comment['id']}, updating it")
                return self.update_pr_comment(comment["id"], marked_body)
        
        # Didn't find a comment with our marker, create a new one
        logger.info("No existing comment found with marker, creating new comment")
        return self.post_pr_comment(marked_body)
    
    def create_gist(self, filename: str, content: str, description: str = "") -> Optional[str]:
        """
        Create a secret GitHub Gist and return its URL.
        
        Args:
            filename: Name of the file in the gist
            content: Content of the file
            description: Description of the gist
            
        Returns:
            URL of the created gist, or None if failed
        """
        if not self.token:
            logger.warning("GitHub token not available, skipping gist creation")
            return None
            
        url = f"{self.api_base_url}/gists"
        
        payload = {
            "description": description,
            "public": False,  # Create secret gist
            "files": {
                filename: {
                    "content": content
                }
            }
        }
        
        try:
            logger.info(f"Creating secret gist: {filename}")
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            gist_data = response.json()
            gist_url = gist_data.get("html_url")
            logger.info(f"✅ Created gist: {gist_url}")
            return gist_url
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to create gist: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            return None

    
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
        # CRITICAL and ERROR result in failure status
        # WARNING and INFO result in success status (PR can still be merged)
        if severity == Severity.CRITICAL:
            state = "failure" 
            description = "Critical issues found - must be fixed"
        elif severity == Severity.ERROR:
            state = "failure"
            description = "Errors found - must be fixed"
        elif severity == Severity.WARNING:
            state = "success"  # WARNING allows PR to pass
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
        This provides a basic implementation for GitHub comment formatting.
        
        Args:
            severity: Highest severity level of detected issues
            issues: List of issue dictionaries with details
            ai_analysis: Optional AI-generated analysis to include
            
        Returns:
            Formatted markdown for a GitHub comment
        """
        # Basic implementation for GitHub comment formatting.
        # The main comment generation logic is now in ResultAnalyzer.generate_pr_comment_content()
        # which provides more sophisticated structured output handling.
        
        # Just return the header and issues list
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