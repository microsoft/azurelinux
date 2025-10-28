#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
AnalyticsManager
----------------
Manages the analytics.json file in blob storage for tracking PR analysis history,
challenged issues, and issue lifecycle across commits.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from azure.core.exceptions import ResourceNotFoundError

logger = logging.getLogger("AnalyticsManager")


@dataclass
class IssueRecord:
    """Represents a detected issue in a commit"""
    issue_hash: str
    spec_file: str
    antipattern_type: str
    antipattern_name: str
    description: str
    severity: str
    line_number: Optional[int]
    first_detected_commit: str  # SHA of commit where first seen
    status: str  # active | challenged | resolved


@dataclass
class CommitAnalysis:
    """Represents analysis results for a single commit"""
    commit_sha: str
    timestamp: str
    report_url: str
    issues_detected: List[Dict]  # List of IssueRecord dicts
    issue_count: int


@dataclass
class Challenge:
    """Represents a user challenge to an issue"""
    challenge_id: str
    issue_hash: str
    commit_sha: str  # Commit where challenge was submitted
    spec_file: str
    antipattern_type: str
    details: str
    submitted_at: str
    submitted_by: Dict  # {username, email, is_collaborator}
    challenge_type: str  # false-positive | needs-clarification | other
    feedback_text: str
    status: str  # submitted | acknowledged | rejected


class AnalyticsManager:
    """Manages PR analytics data in blob storage"""
    
    def __init__(self, blob_storage_client):
        """
        Initialize the analytics manager.
        
        Args:
            blob_storage_client: BlobStorageClient instance for blob operations
        """
        self.blob_client = blob_storage_client
        logger.info("Initialized AnalyticsManager")
    
    def load_analytics(self, pr_number: int) -> Dict:
        """
        Load analytics.json for a PR from blob storage.
        
        Args:
            pr_number: GitHub PR number
            
        Returns:
            Analytics data dict, or new empty structure if not found
        """
        blob_name = f"PR-{pr_number}/analytics.json"
        
        try:
            logger.info(f"📦 Loading analytics from blob: {blob_name}")
            
            # Download from blob storage
            blob_client = self.blob_client.blob_service_client.get_blob_client(
                container=self.blob_client.container_name,
                blob=blob_name
            )
            
            blob_data = blob_client.download_blob()
            analytics_json = blob_data.readall().decode('utf-8')
            analytics = json.loads(analytics_json)
            
            logger.info(f"✅ Loaded analytics with {len(analytics.get('commits', []))} commits")
            return analytics
            
        except ResourceNotFoundError:
            logger.info(f"📝 Analytics not found, creating new structure for PR #{pr_number}")
            return self._create_new_analytics(pr_number)
        except Exception as e:
            logger.error(f"❌ Error loading analytics: {e}")
            # Return new structure on error
            return self._create_new_analytics(pr_number)
    
    def _create_new_analytics(self, pr_number: int) -> Dict:
        """Create new analytics structure for a PR"""
        return {
            "pr_number": pr_number,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "commits": [],
            "challenges": [],
            "issue_lifecycle": {},
            "summary_metrics": {
                "total_commits_analyzed": 0,
                "total_issues_ever_detected": 0,
                "currently_active_issues": 0,
                "challenged_issues": 0,
                "resolved_issues": 0
            }
        }
    
    def save_analytics(self, pr_number: int, analytics: Dict) -> bool:
        """
        Save analytics.json to blob storage.
        
        Args:
            pr_number: GitHub PR number
            analytics: Analytics data dict
            
        Returns:
            True if successful, False otherwise
        """
        blob_name = f"PR-{pr_number}/analytics.json"
        
        try:
            logger.info(f"💾 Saving analytics to blob: {blob_name}")
            
            # Update last_updated timestamp
            analytics["last_updated"] = datetime.utcnow().isoformat() + "Z"
            
            # Upload to blob storage
            blob_client = self.blob_client.blob_service_client.get_blob_client(
                container=self.blob_client.container_name,
                blob=blob_name
            )
            
            analytics_json = json.dumps(analytics, indent=2)
            blob_client.upload_blob(analytics_json, overwrite=True)
            
            logger.info(f"✅ Analytics saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving analytics: {e}")
            return False
    
    def add_commit_analysis(
        self,
        pr_number: int,
        commit_sha: str,
        report_url: str,
        issues: List
    ) -> Dict:
        """
        Record analysis for a new commit.
        
        Args:
            pr_number: GitHub PR number
            commit_sha: Git commit SHA
            report_url: URL to HTML report in blob storage
            issues: List of AntiPattern objects detected
            
        Returns:
            Updated analytics dict
        """
        analytics = self.load_analytics(pr_number)
        
        # Convert AntiPattern objects to dicts for storage
        issue_records = []
        for issue in issues:
            issue_record = {
                "issue_hash": issue.issue_hash,
                "spec_file": issue.file_path,
                "antipattern_type": issue.id,
                "antipattern_name": issue.name,
                "description": issue.description,
                "severity": issue.severity.name,
                "line_number": issue.line_number,
                "first_detected_commit": commit_sha,
                "status": "active"
            }
            issue_records.append(issue_record)
        
        # Add commit analysis
        commit_analysis = {
            "commit_sha": commit_sha,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "report_url": report_url,
            "issues_detected": issue_records,
            "issue_count": len(issues)
        }
        
        analytics["commits"].append(commit_analysis)
        analytics["summary_metrics"]["total_commits_analyzed"] = len(analytics["commits"])
        
        # Update issue lifecycle tracking
        for issue_record in issue_records:
            issue_hash = issue_record["issue_hash"]
            if issue_hash not in analytics["issue_lifecycle"]:
                analytics["issue_lifecycle"][issue_hash] = {
                    "first_detected": commit_sha,
                    "last_detected": commit_sha,
                    "challenge_id": None,
                    "status": "active",
                    "resolution": None
                }
            else:
                # Update last_detected for recurring issues
                analytics["issue_lifecycle"][issue_hash]["last_detected"] = commit_sha
        
        logger.info(f"📊 Added commit analysis for {commit_sha}: {len(issues)} issues")
        
        return analytics
    
    def get_challenged_issues(self, pr_number: int) -> Dict[str, Dict]:
        """
        Get all challenged issues for a PR.
        
        Args:
            pr_number: GitHub PR number
            
        Returns:
            Dict mapping issue_hash to challenge data
        """
        analytics = self.load_analytics(pr_number)
        
        challenged_issues = {}
        for challenge in analytics.get("challenges", []):
            issue_hash = challenge.get("issue_hash")
            if issue_hash:
                challenged_issues[issue_hash] = challenge
        
        logger.info(f"Found {len(challenged_issues)} challenged issues in PR #{pr_number}")
        return challenged_issues
    
    def categorize_issues(
        self,
        current_issues: List,
        analytics: Dict
    ) -> Dict[str, List]:
        """
        Categorize current commit's issues based on history and challenges.
        
        Args:
            current_issues: List of AntiPattern objects from current commit
            analytics: Current analytics data
            
        Returns:
            Dict with categorized issues:
            {
                "new_unchallenged": [...],
                "recurring_unchallenged": [...],
                "previously_challenged": [...],
                "all_challenged_hashes": set(...)
            }
        """
        # Get previous commit's issues (if exists)
        previous_hashes = set()
        if analytics.get("commits"):
            last_commit = analytics["commits"][-1]
            previous_hashes = {
                issue["issue_hash"] 
                for issue in last_commit.get("issues_detected", [])
            }
        
        # Get challenged issue hashes
        challenged_hashes = {
            challenge["issue_hash"] 
            for challenge in analytics.get("challenges", [])
        }
        
        # Categorize current issues
        new_unchallenged = []
        recurring_unchallenged = []
        previously_challenged = []
        
        for issue in current_issues:
            issue_hash = issue.issue_hash
            
            if issue_hash in challenged_hashes:
                # Issue was previously challenged
                previously_challenged.append(issue)
            elif issue_hash not in previous_hashes:
                # New issue (not in previous commit, not challenged)
                new_unchallenged.append(issue)
            else:
                # Recurring issue (was in previous, not challenged)
                recurring_unchallenged.append(issue)
        
        result = {
            "new_unchallenged": new_unchallenged,
            "recurring_unchallenged": recurring_unchallenged,
            "previously_challenged": previously_challenged,
            "all_challenged_hashes": challenged_hashes
        }
        
        logger.info(f"📊 Categorized issues: "
                   f"{len(new_unchallenged)} new, "
                   f"{len(recurring_unchallenged)} recurring unchallenged, "
                   f"{len(previously_challenged)} previously challenged")
        
        return result
    
    def update_summary_metrics(self, analytics: Dict) -> Dict:
        """
        Recalculate summary metrics based on current analytics data.
        
        Args:
            analytics: Current analytics data
            
        Returns:
            Updated analytics dict
        """
        # Count unique issues ever detected
        all_issue_hashes = set()
        for commit in analytics.get("commits", []):
            for issue in commit.get("issues_detected", []):
                all_issue_hashes.add(issue["issue_hash"])
        
        # Get latest commit's issues
        currently_active = set()
        if analytics.get("commits"):
            last_commit = analytics["commits"][-1]
            currently_active = {
                issue["issue_hash"] 
                for issue in last_commit.get("issues_detected", [])
            }
        
        # Count challenged issues
        challenged_count = len(analytics.get("challenges", []))
        
        # Count resolved issues (were in previous commits, not in latest)
        resolved_hashes = all_issue_hashes - currently_active
        
        analytics["summary_metrics"] = {
            "total_commits_analyzed": len(analytics.get("commits", [])),
            "total_issues_ever_detected": len(all_issue_hashes),
            "currently_active_issues": len(currently_active),
            "challenged_issues": challenged_count,
            "resolved_issues": len(resolved_hashes)
        }
        
        logger.info(f"📈 Updated metrics: {analytics['summary_metrics']}")
        
        return analytics
