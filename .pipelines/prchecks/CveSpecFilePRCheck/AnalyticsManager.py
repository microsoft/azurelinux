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
    
    def __init__(self, blob_storage_client, pr_number: int):
        """
        Initialize the analytics manager.
        
        Args:
            blob_storage_client: BlobStorageClient instance for blob operations
            pr_number: GitHub PR number
        """
        self.blob_client = blob_storage_client
        self.pr_number = pr_number
        self.analytics = None  # Cache for current analytics data
        logger.info(f"Initialized AnalyticsManager for PR #{pr_number}")
    
    def load_analytics(self) -> Dict:
        """
        Load analytics.json for the PR from blob storage.
        
        Returns:
            Analytics data dict, or new empty structure if not found
        """
        blob_name = f"PR-{self.pr_number}/analytics.json"
        
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
            self.analytics = analytics  # Cache the loaded analytics
            return analytics
            
        except ResourceNotFoundError:
            logger.info(f"📝 Analytics not found, creating new structure for PR #{self.pr_number}")
            analytics = self._create_new_analytics()
            self.analytics = analytics
            return analytics
        except Exception as e:
            logger.error(f"❌ Error loading analytics: {e}")
            # Return new structure on error
            analytics = self._create_new_analytics()
            self.analytics = analytics
            return analytics
    
    def _create_new_analytics(self) -> Dict:
        """Create new analytics structure for the PR"""
        return {
            "pr_number": self.pr_number,
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
    
    def save_analytics(self) -> bool:
        """
        Save analytics.json to blob storage.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.analytics:
            logger.warning("No analytics data to save")
            return False
            
        blob_name = f"PR-{self.pr_number}/analytics.json"
        
        try:
            logger.info(f"💾 Saving analytics to blob: {blob_name}")
            
            # Update last_updated timestamp
            self.analytics["last_updated"] = datetime.utcnow().isoformat() + "Z"
            
            # Upload to blob storage
            blob_client = self.blob_client.blob_service_client.get_blob_client(
                container=self.blob_client.container_name,
                blob=blob_name
            )
            
            analytics_json = json.dumps(self.analytics, indent=2)
            blob_client.upload_blob(analytics_json, overwrite=True)
            
            logger.info(f"✅ Analytics saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving analytics: {e}")
            return False
    
    def add_commit_analysis(
        self,
        commit_sha: str,
        report_url: str,
        issues: List
    ) -> None:
        """
        Record analysis for a new commit.
        
        Args:
            commit_sha: Git commit SHA
            report_url: URL to HTML report in blob storage
            issues: List of AntiPattern objects detected
        """
        if not self.analytics:
            logger.error("Analytics not loaded, call load_analytics() first")
            return
        
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
        
        self.analytics["commits"].append(commit_analysis)
        self.analytics["summary_metrics"]["total_commits_analyzed"] = len(self.analytics["commits"])
        
        # Update issue lifecycle tracking
        for issue_record in issue_records:
            issue_hash = issue_record["issue_hash"]
            if issue_hash not in self.analytics["issue_lifecycle"]:
                self.analytics["issue_lifecycle"][issue_hash] = {
                    "first_detected": commit_sha,
                    "last_detected": commit_sha,
                    "challenge_id": None,
                    "status": "active",
                    "resolution": None
                }
            else:
                # Update last_detected for recurring issues
                self.analytics["issue_lifecycle"][issue_hash]["last_detected"] = commit_sha
        
        logger.info(f"📊 Added commit analysis for {commit_sha}: {len(issues)} issues")
    
    def get_challenged_issues(self) -> Dict[str, Dict]:
        """
        Get all challenged issues for the PR.
        
        Returns:
            Dict mapping issue_hash to challenge data
        """
        if not self.analytics:
            logger.warning("Analytics not loaded")
            return {}
        
        challenged_issues = {}
        for challenge in self.analytics.get("challenges", []):
            issue_hash = challenge.get("issue_hash")
            if issue_hash:
                challenged_issues[issue_hash] = challenge
        
        logger.info(f"Found {len(challenged_issues)} challenged issues in PR #{self.pr_number}")
        return challenged_issues
    
    def categorize_issues(
        self,
        current_issues: List
    ) -> Dict[str, List]:
        """
        Categorize current commit's issues based on history and challenges.
        
        Args:
            current_issues: List of AntiPattern objects from current commit
            
        Returns:
            Dict with categorized issues:
            {
                "new_issues": [...],           # Renamed from new_unchallenged
                "recurring_unchallenged": [...],
                "challenged_issues": [...],    # Renamed from previously_challenged
                "resolved_issues": []          # Issues from previous commits not in current
            }
        """
        if not self.analytics:
            logger.warning("Analytics not loaded")
            return {
                "new_issues": current_issues,
                "recurring_unchallenged": [],
                "challenged_issues": [],
                "resolved_issues": []
            }
        
        # Get previous commit's issues (if exists)
        previous_hashes = set()
        if self.analytics.get("commits") and len(self.analytics["commits"]) > 1:
            # Get second-to-last commit (before current one we just added)
            last_commit = self.analytics["commits"][-2]
            previous_hashes = {
                issue["issue_hash"] 
                for issue in last_commit.get("issues_detected", [])
            }
        
        # Get challenged issue hashes
        challenged_hashes = {
            challenge["issue_hash"] 
            for challenge in self.analytics.get("challenges", [])
        }
        
        # Get current issue hashes
        current_hashes = {issue.issue_hash for issue in current_issues}
        
        # Calculate resolved issues (in previous, not in current, not challenged)
        resolved_hashes = previous_hashes - current_hashes - challenged_hashes
        
        # Categorize current issues
        new_issues = []
        recurring_unchallenged = []
        challenged_issues = []
        
        for issue in current_issues:
            issue_hash = issue.issue_hash
            
            if issue_hash in challenged_hashes:
                # Issue was previously challenged
                challenged_issues.append(issue)
            elif issue_hash not in previous_hashes:
                # New issue (not in previous commit, not challenged)
                new_issues.append(issue)
            else:
                # Recurring issue (was in previous, not challenged)
                recurring_unchallenged.append(issue)
        
        result = {
            "new_issues": new_issues,
            "recurring_unchallenged": recurring_unchallenged,
            "challenged_issues": challenged_issues,
            "resolved_issues": list(resolved_hashes)  # Just hashes for resolved
        }
        
        logger.info(f"📊 Categorized issues: "
                   f"{len(new_issues)} new, "
                   f"{len(recurring_unchallenged)} recurring unchallenged, "
                   f"{len(challenged_issues)} previously challenged, "
                   f"{len(resolved_hashes)} resolved")
        
        return result
    
    def update_summary_metrics(self) -> None:
        """
        Recalculate summary metrics based on current analytics data.
        """
        if not self.analytics:
            logger.warning("Analytics not loaded")
            return
        
        # Count unique issues ever detected
        all_issue_hashes = set()
        for commit in self.analytics.get("commits", []):
            for issue in commit.get("issues_detected", []):
                all_issue_hashes.add(issue["issue_hash"])
        
        # Get latest commit's issues
        currently_active = set()
        if self.analytics.get("commits"):
            last_commit = self.analytics["commits"][-1]
            currently_active = {
                issue["issue_hash"] 
                for issue in last_commit.get("issues_detected", [])
            }
        
        # Count challenged issues
        challenged_count = len(self.analytics.get("challenges", []))
        
        # Count resolved issues (were in previous commits, not in latest)
        resolved_hashes = all_issue_hashes - currently_active
        
        self.analytics["summary_metrics"] = {
            "total_commits_analyzed": len(self.analytics.get("commits", [])),
            "total_issues_ever_detected": len(all_issue_hashes),
            "currently_active_issues": len(currently_active),
            "challenged_issues": challenged_count,
            "resolved_issues": len(resolved_hashes)
        }
        
        logger.info(f"📈 Updated metrics: {self.analytics['summary_metrics']}")
