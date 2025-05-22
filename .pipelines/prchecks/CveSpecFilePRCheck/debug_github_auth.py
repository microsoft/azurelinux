#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Debug script to test GitHub authentication and PR commenting functionality
"""

import os
import sys
import logging
import requests
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("github-auth-debug")

def debug_github_auth():
    """Debug GitHub authentication and environment variables"""
    
    # Check environment variables
    logger.info("GitHub Environment Variables:")
    logger.info(f"  - GITHUB_TOKEN: {'Set (length: ' + str(len(os.environ.get('GITHUB_TOKEN', ''))) + ')' if os.environ.get('GITHUB_TOKEN') else 'Not Set'}")
    logger.info(f"  - SYSTEM_ACCESSTOKEN: {'Set' if os.environ.get('SYSTEM_ACCESSTOKEN') else 'Not Set'}")
    logger.info(f"  - GITHUB_REPOSITORY: {os.environ.get('GITHUB_REPOSITORY', 'Not Set')}")
    logger.info(f"  - BUILD_REPOSITORY_NAME: {os.environ.get('BUILD_REPOSITORY_NAME', 'Not Set')}")
    logger.info(f"  - GITHUB_PR_NUMBER: {os.environ.get('GITHUB_PR_NUMBER', 'Not Set')}")
    logger.info(f"  - SYSTEM_PULLREQUEST_PULLREQUESTNUMBER: {os.environ.get('SYSTEM_PULLREQUEST_PULLREQUESTNUMBER', 'Not Set')}")
    
    # Construct repository name and PR number
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo_name or repo_name == "":
        repo_name = os.environ.get("BUILD_REPOSITORY_NAME", "")
        logger.info(f"Using BUILD_REPOSITORY_NAME: {repo_name}")
    
    if repo_name and "/" not in repo_name:
        repo_name = f"microsoft/{repo_name}"
        logger.info(f"Converted repo name to GitHub format: {repo_name}")
    
    pr_number = os.environ.get("GITHUB_PR_NUMBER", "") or os.environ.get("SYSTEM_PULLREQUEST_PULLREQUESTNUMBER", "")
    
    logger.info(f"Final repository: {repo_name}")
    logger.info(f"Final PR number: {pr_number}")
    
    # Test token availability
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        logger.error("No GITHUB_TOKEN available!")
        return False
    
    # Create headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Azure-Linux-PR-Check-Debug",
        "Authorization": f"token {token}"
    }
    
    # Test API access - get authenticated user info
    try:
        logger.info("Testing GitHub API access...")
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"Authentication successful! Logged in as: {user_data.get('login', 'Unknown')}")
        else:
            logger.error(f"Authentication failed! Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error testing GitHub API: {e}")
        return False
    
    # Test PR commenting if repo and PR number are available
    if repo_name and pr_number:
        try:
            logger.info(f"Testing PR comment access for {repo_name} PR #{pr_number}...")
            url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
            
            # Just test fetching existing comments first
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                comments = response.json()
                logger.info(f"Successfully retrieved {len(comments)} comments from PR")
                return True
            else:
                logger.error(f"Failed to access PR comments! Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error testing PR comment access: {e}")
            return False
    else:
        logger.warning("Can't test PR comment access - missing repo name or PR number")
        return False
    
    return True

def post_test_comment():
    """Post a test comment to the PR"""
    
    # Get required variables
    token = os.environ.get("GITHUB_TOKEN", "")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "") or os.environ.get("BUILD_REPOSITORY_NAME", "")
    if repo_name and "/" not in repo_name:
        repo_name = f"microsoft/{repo_name}"
    
    pr_number = os.environ.get("GITHUB_PR_NUMBER", "") or os.environ.get("SYSTEM_PULLREQUEST_PULLREQUESTNUMBER", "")
    
    if not token or not repo_name or not pr_number:
        logger.error("Missing required variables to post comment")
        return False
    
    # Create headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Azure-Linux-PR-Check-Debug",
        "Authorization": f"token {token}"
    }
    
    # Create comment payload
    comment_body = "## 🧪 Test Comment from CVE Spec File PR Check\n\n"
    comment_body += "This is a test comment to verify GitHub PR commenting functionality.\n\n"
    comment_body += "If you can see this comment, GitHub PR commenting is working! 🎉\n\n"
    comment_body += f"- Repository: `{repo_name}`\n"
    comment_body += f"- PR number: `{pr_number}`\n"
    comment_body += f"- Time: `{os.popen('date -u').read().strip()}`\n"
    
    payload = {
        "body": f"<!-- debug-test-comment -->\n{comment_body}"
    }
    
    # Post the comment
    try:
        logger.info(f"Posting test comment to {repo_name} PR #{pr_number}...")
        url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [201, 200]:
            result = response.json()
            logger.info(f"Successfully posted comment! ID: {result.get('id')}, URL: {result.get('html_url')}")
            return True
        else:
            logger.error(f"Failed to post comment! Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error posting test comment: {e}")
        return False

if __name__ == "__main__":
    print("\n=== GitHub Authentication Debug Tool ===\n")
    
    if debug_github_auth():
        print("\n✅ GitHub authentication successful!")
        
        if len(sys.argv) > 1 and sys.argv[1] == "--post-comment":
            if post_test_comment():
                print("✅ Test comment posted successfully!")
            else:
                print("❌ Failed to post test comment")
    else:
        print("\n❌ GitHub authentication failed!")
        
    print("\n=======================================\n")
