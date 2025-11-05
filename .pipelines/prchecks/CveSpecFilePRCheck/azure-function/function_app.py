#!/usr/bin/env python3
"""
Azure Function: RADAR Challenge Handler
Handles challenge submissions for CVE spec file analysis findings.
"""

import azure.functions as func
import json
import logging
import os
import jwt
import requests
from datetime import datetime
from urllib.parse import urlencode
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError, ResourceNotFoundError
from azure.keyvault.secrets import SecretClient

# Import HTML generator from same directory
from HtmlReportGenerator import HtmlReportGenerator
from AntiPatternDetector import Severity

app = func.FunctionApp()

# Configuration
STORAGE_ACCOUNT_URL = "https://radarblobstore.blob.core.windows.net"
CONTAINER_NAME = "radarcontainer"
KEY_VAULT_URL = "https://mariner-pipelines-kv.vault.azure.net"
GITHUB_TOKEN_SECRET_NAME = "cblmarghGithubPRPat"

logger = logging.getLogger(__name__)

# Global variable to cache the GitHub token
_cached_github_token = None

def get_github_token():
    """
    Fetch GitHub PAT token from Azure Key Vault using Managed Identity.
    Token is cached after first retrieval for performance.
    """
    global _cached_github_token
    
    if _cached_github_token:
        return _cached_github_token
    
    try:
        # Use DefaultAzureCredential (works with Managed Identity in Azure Function)
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
        
        logger.info(f"🔐 Fetching GitHub token from Key Vault: {KEY_VAULT_URL}")
        secret = secret_client.get_secret(GITHUB_TOKEN_SECRET_NAME)
        _cached_github_token = secret.value
        
        logger.info(f"✅ GitHub token fetched successfully from Key Vault")
        logger.info(f"🔑 Token prefix: {_cached_github_token[:10]}...")
        logger.info(f"🔑 Token length: {len(_cached_github_token)}")
        
        return _cached_github_token
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch GitHub token from Key Vault: {e}")
        # Fallback to environment variable if Key Vault fails
        fallback_token = os.environ.get("GITHUB_TOKEN", "")
        if fallback_token:
            logger.warning(f"⚠️  Using fallback GITHUB_TOKEN from environment variable")
            return fallback_token
        else:
            logger.error(f"❌ No fallback token available")
            return None


@app.route(route="challenge", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def submit_challenge(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handle authenticated challenge submissions and update blob JSON.
    
    Expected Headers:
        Authorization: Bearer <JWT_TOKEN>
    
    Expected POST body:
    {
        "pr_number": 14877,
        "spec_file": "SPECS/curl/curl.spec",
        "issue_hash": "curl-CVE-2024-12345-missing-cve-in-changelog",
        "antipattern_id": "curl-ap-001",  # Legacy field, kept for backwards compatibility
        "challenge_type": "false-positive",
        "feedback_text": "This is intentional because..."
    }
    
    Returns:
        JSON response with success status and challenge_id
    """
    logger.info("🎯 RADAR Challenge Handler - Processing authenticated request")
    
    try:
        # Step 1: Verify JWT authentication
        auth_header = req.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            logger.error("❌ Missing or invalid Authorization header")
            return func.HttpResponse(
                json.dumps({
                    "error": "Authentication required",
                    "message": "Please sign in to submit challenges"
                }),
                mimetype="application/json",
                status_code=401
            )
        
        token = auth_header.replace('Bearer ', '')
        
        # Verify JWT token
        try:
            user_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            username = user_payload.get('username')
            email = user_payload.get('email')
            is_collaborator = user_payload.get('is_collaborator', False)
            is_admin = user_payload.get('is_admin', False)
            github_token = user_payload.get('github_token')
            
            logger.info(f"✅ Authenticated user: {username} (collaborator: {is_collaborator}, admin: {is_admin})")
        except jwt.ExpiredSignatureError:
            logger.error("❌ JWT token expired")
            return func.HttpResponse(
                json.dumps({
                    "error": "Token expired",
                    "message": "Please sign in again"
                }),
                mimetype="application/json",
                status_code=401
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"❌ Invalid JWT token: {e}")
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid token",
                    "message": "Authentication failed"
                }),
                mimetype="application/json",
                status_code=401
            )
        
        # Step 2: Parse request body
        try:
            req_body = req.get_json()
            logger.info(f"📥 Received challenge from {username}: {json.dumps(req_body, indent=2)}")
        except ValueError as e:
            logger.error(f"❌ Invalid JSON in request body: {e}")
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                mimetype="application/json",
                status_code=400
            )
        
        # Validate required fields
        required_fields = ["pr_number", "issue_hash", "challenge_type", "feedback_text"]
        missing_fields = [field for field in required_fields if field not in req_body]
        
        if missing_fields:
            logger.error(f"❌ Missing required fields: {missing_fields}")
            return func.HttpResponse(
                json.dumps({"error": f"Missing required fields: {', '.join(missing_fields)}"}),
                mimetype="application/json",
                status_code=400
            )
        
        # Validate challenge_type
        valid_challenge_types = ["false-positive", "needs-context", "disagree-with-severity"]
        if req_body["challenge_type"] not in valid_challenge_types:
            logger.error(f"❌ Invalid challenge_type: {req_body['challenge_type']}")
            return func.HttpResponse(
                json.dumps({
                    "error": f"Invalid challenge_type. Must be one of: {', '.join(valid_challenge_types)}"
                }),
                mimetype="application/json",
                status_code=400
            )
        
        pr_number = req_body["pr_number"]
        issue_hash = req_body["issue_hash"]
        # Keep antipattern_id for backwards compatibility (optional)
        antipattern_id = req_body.get("antipattern_id", issue_hash)
        
        logger.info(f"📝 Processing challenge for issue_hash: {issue_hash}")
        
        # Step 3: Verify user has permission to submit challenge
        # Allow: PR owner, repository collaborators, or repository admins
        is_pr_owner = False
        
        if not (is_collaborator or is_admin):
            # Check if user is the PR owner
            logger.info(f"🔍 Checking if {username} is PR owner for PR #{pr_number}...")
            pr_url = f"https://api.github.com/repos/microsoft/azurelinux/pulls/{pr_number}"
            pr_headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/json"}
            
            try:
                pr_response = requests.get(pr_url, headers=pr_headers)
                if pr_response.status_code == 200:
                    pr_data = pr_response.json()
                    pr_owner_username = pr_data.get("user", {}).get("login", "")
                    is_pr_owner = (pr_owner_username == username)
                    logger.info(f"{'✅' if is_pr_owner else '❌'} PR owner: {pr_owner_username}, User: {username}")
                else:
                    logger.warning(f"⚠️ Could not fetch PR #{pr_number}: {pr_response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ Error checking PR ownership: {e}")
        
        # Verify user has permission
        has_permission = is_pr_owner or is_collaborator or is_admin
        
        if not has_permission:
            logger.error(f"❌ User {username} does not have permission to submit challenges for PR #{pr_number}")
            return func.HttpResponse(
                json.dumps({
                    "error": "Permission denied",
                    "message": "You must be the PR owner, a repository collaborator, or an admin to submit challenges"
                }),
                mimetype="application/json",
                status_code=403
            )
        
        permission_type = "admin" if is_admin else ("collaborator" if is_collaborator else "PR owner")
        logger.info(f"✅ Permission verified: {username} is {permission_type}")
        
        # Initialize blob client with UMI
        logger.info("🔐 Authenticating with Managed Identity...")
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=STORAGE_ACCOUNT_URL,
            credential=credential
        )
        
        # Get the analytics JSON blob
        blob_name = f"PR-{pr_number}/analytics.json"
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME,
            blob=blob_name
        )
        
        logger.info(f"📦 Fetching analytics blob: {blob_name}")
        
        try:
            # Download current JSON
            blob_data = blob_client.download_blob()
            current_data = json.loads(blob_data.readall())
            logger.info(f"✅ Successfully loaded analytics data")
        except ResourceNotFoundError:
            logger.warning(f"⚠️  Analytics blob not found: {blob_name}")
            logger.info("📝 Creating new analytics.json file for this PR")
            # Create new analytics file on first challenge
            current_data = {
                "pr_number": pr_number,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "challenges": []
            }
        
        # Generate challenge ID
        existing_challenges = current_data.get("challenges", [])
        challenge_id = f"ch-{len(existing_challenges) + 1:03d}"
        
        # Create challenge entry with authenticated user info
        challenge = {
            "challenge_id": challenge_id,
            "issue_hash": issue_hash,  # Primary identifier for tracking across commits
            "antipattern_id": antipattern_id,  # Legacy field for backwards compatibility
            "spec_file": req_body.get("spec_file", ""),
            "commit_sha": req_body.get("commit_sha", "unknown"),  # Commit where issue was challenged
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "timestamp": datetime.utcnow().isoformat() + "Z",  # For HTML display compatibility
            "submitted_by": {
                "username": username,
                "email": email,
                "is_collaborator": is_collaborator
            },
            "user": username,  # For HTML display compatibility
            "challenge_type": req_body["challenge_type"],
            "feedback_text": req_body["feedback_text"],  # Keep for backwards compatibility
            "feedback": req_body["feedback_text"],  # For HTML display compatibility
            "status": "submitted"
        }
        
        logger.info(f"✏️  Creating challenge: {challenge_id} for issue_hash: {issue_hash} by {username}")
        
        # Add challenge to data
        if "challenges" not in current_data:
            current_data["challenges"] = []
        current_data["challenges"].append(challenge)
        
        # Update issue_lifecycle to mark this issue as challenged
        # CRITICAL: Only update if issue already exists (was detected by PR check)
        # Do NOT create new entries - this prevents counting challenged-only issues
        # toward "all issues resolved" calculation
        if "issue_lifecycle" not in current_data:
            current_data["issue_lifecycle"] = {}
        
        if issue_hash in current_data["issue_lifecycle"]:
            # Issue was detected by PR check - update its status
            current_data["issue_lifecycle"][issue_hash]["status"] = "challenged"
            current_data["issue_lifecycle"][issue_hash]["challenge_id"] = challenge_id
            logger.info(f"✅ Updated issue_lifecycle for {issue_hash}: status=challenged, challenge_id={challenge_id}")
        else:
            # Issue not in lifecycle (PR check hasn't run yet or issue is not real)
            # Do NOT add to issue_lifecycle to avoid false "all resolved" calculation
            logger.warning(f"⚠️  Issue {issue_hash} not found in issue_lifecycle")
            logger.warning(f"   This issue was not detected by PR check yet")
            logger.warning(f"   Challenge recorded but issue_lifecycle not modified")
            logger.warning(f"   Issue will appear in lifecycle after next PR check run")
        
        # Legacy: Also update antipattern status in specs array (if it exists)
        antipattern_found = False
        for spec in current_data.get("specs", []):
            for ap in spec.get("antipatterns", []):
                # Match by issue_hash if available, fallback to antipattern_id
                ap_hash = ap.get("issue_hash", ap.get("id"))
                if ap_hash == issue_hash or ap.get("id") == antipattern_id:
                    ap["status"] = "challenged"
                    if req_body["challenge_type"] == "false-positive":
                        ap["marked_false_positive"] = True
                    antipattern_found = True
                    logger.info(f"✅ Updated legacy antipattern status: {ap.get('id')} -> challenged")
                    break
            if antipattern_found:
                break
        
        if not antipattern_found:
            logger.info(f"ℹ️  No legacy antipattern entry found for {issue_hash} (analytics.json might be from new schema)")
        
        # Recalculate summary metrics
        total_findings = sum(len(s.get("antipatterns", [])) for s in current_data.get("specs", []))
        challenged_count = len([c for c in current_data["challenges"] if c["status"] == "submitted"])
        false_positive_count = len([c for c in current_data["challenges"] if c["challenge_type"] == "false-positive"])
        
        current_data["summary_metrics"] = current_data.get("summary_metrics", {})
        current_data["summary_metrics"].update({
            "challenged_findings": challenged_count,
            "false_positives": false_positive_count,
            "challenge_rate": round((challenged_count / total_findings * 100) if total_findings > 0 else 0, 2),
            "false_positive_rate": round((false_positive_count / total_findings * 100) if total_findings > 0 else 0, 2)
        })
        
        logger.info(f"📊 Updated metrics - Challenged: {challenged_count}, False Positives: {false_positive_count}")
        
        # Upload updated JSON (atomic operation)
        logger.info(f"⬆️  Uploading updated analytics data...")
        blob_client.upload_blob(
            json.dumps(current_data, indent=2),
            overwrite=True
        )
        
        logger.info(f"✅✅✅ Challenge submitted successfully: {challenge_id}")
        
        # Update existing HTML report with challenge marker
        # This is much simpler than regenerating - just download, modify checkbox, re-upload
        logger.info(f"📄 Updating existing HTML report with challenge marker...")
        report_url = None
        
        try:
            # Find the latest HTML report in blob storage
            latest_html_blob = None
            list_blobs = blob_service_client.get_container_client(CONTAINER_NAME).list_blobs(
                name_starts_with=f"PR-{pr_number}/report-"
            )
            
            # Find the most recent report
            blobs = sorted(list_blobs, key=lambda b: b.last_modified, reverse=True)
            if blobs:
                latest_html_blob = blobs[0].name
                logger.info(f"📥 Found latest HTML report: {latest_html_blob}")
            else:
                logger.warning(f"⚠️  No HTML report found for PR-{pr_number}")
                report_url = None
                
            if latest_html_blob:
                # Download existing HTML
                html_blob_client = blob_service_client.get_blob_client(
                    container=CONTAINER_NAME,
                    blob=latest_html_blob
                )
                
                blob_data = html_blob_client.download_blob()
                original_html = blob_data.readall().decode('utf-8')
                logger.info(f"✅ Downloaded HTML report ({len(original_html)} bytes)")
                
                # Update the button for this issue_hash
                # Find: <button class="btn btn-sm challenge-btn" data-issue-hash="HASH"...>Challenge</button>
                # Replace with: <button class="btn btn-sm challenge-btn challenged" data-issue-hash="HASH"...>Challenged</button>
                import re
                
                # Pattern to match button with this specific issue_hash
                # Capture: (1) full button opening tag, (2) closing </button>
                pattern = f'(<button[^>]*data-issue-hash="{re.escape(issue_hash)}"[^>]*>)Challenge(</button>)'
                
                def update_button(match):
                    button_tag = match.group(1)  # Full opening <button...> tag
                    button_close = match.group(2)  # </button>
                    
                    # Add 'challenged' class if not already present
                    if 'challenged' not in button_tag:
                        # Find the class attribute and add 'challenged' to it
                        button_tag = re.sub(
                            r'(class="[^"]*challenge-btn)([^"]*")',
                            r'\1 challenged\2',
                            button_tag
                        )
                    
                    # Replace 'Challenge' text with 'Challenged ✓'
                    return button_tag + 'Challenged ✓' + button_close
                
                updated_html = re.sub(pattern, update_button, original_html)
                
                if updated_html != original_html:
                    logger.info(f"✅ Updated challenge checkbox for issue {issue_hash}")
                    
                    # Upload updated HTML with new timestamp
                    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H%M%SZ')
                    new_html_blob_name = f"PR-{pr_number}/report-{timestamp}.html"
                    logger.info(f"📤 Uploading updated HTML to: {new_html_blob_name}")
                    
                    new_html_blob_client = blob_service_client.get_blob_client(
                        container=CONTAINER_NAME,
                        blob=new_html_blob_name
                    )
                    
                    new_html_blob_client.upload_blob(updated_html, overwrite=True)
                    logger.info(f"✅ Updated HTML uploaded successfully")
                    
                    # Return the new URL
                    report_url = f"{STORAGE_ACCOUNT_URL}/{CONTAINER_NAME}/{new_html_blob_name}"
                    logger.info(f"✅✅✅ Updated HTML report URL: {report_url}")
                else:
                    logger.warning(f"⚠️  Checkbox already checked or issue_hash not found in HTML")
                    # Still return the original URL
                    report_url = f"{STORAGE_ACCOUNT_URL}/{CONTAINER_NAME}/{latest_html_blob}"
                    
        except Exception as html_error:
            logger.error(f"❌ Failed to update HTML report!")
            logger.error(f"   Error type: {type(html_error).__name__}")
            logger.error(f"   Error message: {str(html_error)}")
            import traceback
            logger.error(f"   Full traceback:")
            logger.error(traceback.format_exc())
            report_url = None
            logger.warning(f"⚠️  report_url set to None due to error")
        
        # Post GitHub comment about the challenge
        try:
            logger.info(f"💬 Posting challenge notification to GitHub PR #{pr_number}")
            
            # Fetch BOT token from Key Vault for posting comment and managing labels
            bot_token = get_github_token()
            
            if not bot_token:
                logger.warning("⚠️  Bot token not available from Key Vault, comment and labels cannot be managed")
                comment_posted = False
                label_added = False
            else:
                challenge_type_emoji = {
                    "false-positive": "🟢",
                    "needs-context": "🟡", 
                    "agree": "🔴"
                }
                emoji = challenge_type_emoji.get(req_body["challenge_type"], "💬")
                
                challenge_type_text = {
                    "false-positive": "False Alarm",
                    "needs-context": "Needs Context",
                    "agree": "Acknowledged"
                }
                type_text = challenge_type_text.get(req_body["challenge_type"], req_body["challenge_type"])
                
                # Determine role badge for user
                role_badge = ""
                if is_admin:
                    role_badge = " 🔴 **Admin**"
                elif is_collaborator:
                    role_badge = " 🟢 **Collaborator**"
                elif is_pr_owner:
                    role_badge = " 🟠 **PR Owner**"
                
                # Format comment with prominent user attribution
                comment_body = f"""## {emoji} Challenge Submitted by @{username}{role_badge}

> **👤 Submitted by: @{username}{role_badge}**  
> This challenge was submitted by the user above through the RADAR system.

**Issue**: `{issue_hash}`  
**File**: `{req_body.get("spec_file", "")}`  
**Challenge Type**: {type_text}  

**Feedback from @{username}**:
> {req_body["feedback_text"]}

---
*Challenge ID: `{challenge_id}` • Submitted on {datetime.utcnow().strftime('%Y-%m-%d at %H:%M UTC')}*  
*This challenge will be reviewed by the team.*
"""
                
                comment_url = f"https://api.github.com/repos/microsoft/azurelinux/issues/{pr_number}/comments"
                
                # Use the BOT token from Key Vault to post the comment
                logger.info(f"💬 Posting challenge comment using BOT token (on behalf of @{username})")
                bot_comment_headers = {
                    "Authorization": f"token {bot_token}",  # Bot PAT from Key Vault
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json"
                }
                comment_response = requests.post(
                    comment_url,
                    headers=bot_comment_headers,
                    json={"body": comment_body},
                    timeout=10
                )
                
                comment_posted = False
                if comment_response.status_code == 201:
                    logger.info(f"✅ GitHub comment posted successfully on behalf of @{username}")
                    comment_posted = True
                else:
                    logger.error(f"❌ Failed to post GitHub comment:")
                    logger.error(f"   Status: {comment_response.status_code}")
                    logger.error(f"   Response: {comment_response.text}")
                    logger.error(f"   User: @{username}")
                    logger.error(f"   Comment URL: {comment_url}")
            
                # Smart label management: Check if ALL issues are now challenged
                logger.info(f"🏷️  Managing labels based on challenge state...")
                
                bot_comment_headers = {
                    "Authorization": f"token {bot_token}",  # Bot PAT uses 'token' prefix
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json"
                }
                
                labels_url = f"https://api.github.com/repos/microsoft/azurelinux/issues/{pr_number}/labels"
                
                # Calculate unchallenged vs challenged issue counts from issue_lifecycle
                issue_lifecycle = current_data.get("issue_lifecycle", {})
                total_issues = len(issue_lifecycle)
                challenged_issues = sum(1 for issue in issue_lifecycle.values() if issue.get("status") == "challenged")
                unchallenged_issues = total_issues - challenged_issues
                
                logger.info(f"   📊 Issue status: {total_issues} total, {challenged_issues} challenged, {unchallenged_issues} unchallenged")
                logger.info(f"   📋 Issue lifecycle keys: {list(issue_lifecycle.keys())[:10]}")  # Log first 10 issue hashes
                
                # CRITICAL: Only manage labels if we have commit history (analytics.json was populated by PR check)
                # This prevents premature label removal when analytics.json is created on first challenge
                has_commit_history = len(current_data.get("commits", [])) > 0
                
                if not has_commit_history:
                    logger.warning(f"   ⚠️  No commit history in analytics.json - skipping label management")
                    logger.warning(f"   This analytics.json was likely created by a challenge before PR check ran")
                    logger.warning(f"   Labels will be managed correctly after next PR check run")
                    label_added = False
                else:
                    label_added = False
                    
                    if total_issues > 0 and unchallenged_issues == 0:
                        # ALL issues have been challenged - update labels
                        logger.info(f"   ✅ All {total_issues} issues challenged! Updating labels...")
                        
                        # Remove radar-issues-detected
                        try:
                            delete_url = f"{labels_url}/radar-issues-detected"
                            delete_response = requests.delete(delete_url, headers=bot_comment_headers, timeout=10)
                            if delete_response.status_code in [200, 404]:
                                logger.info(f"   ✓ Removed 'radar-issues-detected' label (or it wasn't present)")
                            else:
                                logger.warning(f"   Failed to remove 'radar-issues-detected': {delete_response.status_code}")
                        except Exception as e:
                            logger.warning(f"   Error removing 'radar-issues-detected': {e}")
                        
                        # Add radar-acknowledged
                        label_response = requests.post(
                            labels_url,
                            headers=bot_comment_headers,
                            json={"labels": ["radar-acknowledged"]},
                            timeout=10
                        )
                        
                        if label_response.status_code == 200:
                            logger.info(f"   ✅ Label 'radar-acknowledged' added successfully")
                            label_added = True
                        else:
                            logger.error(f"   ❌ Failed to add 'radar-acknowledged': {label_response.status_code}")
                            logger.error(f"   Response: {label_response.text}")
                    else:
                        # Still have unchallenged issues - keep radar-issues-detected label
                        logger.info(f"   ⚠️  Still {unchallenged_issues} unchallenged issue(s) - keeping 'radar-issues-detected' label")
                        label_added = False
        
        except Exception as comment_error:
            logger.error(f"❌ Exception during GitHub comment/label posting:")
            logger.error(f"   Error: {comment_error}")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            comment_posted = False
            label_added = False
        
        # Add diagnostic info to response
        diagnostic_info = {}
        if not comment_posted and 'comment_response' in locals():
            diagnostic_info['comment_error'] = {
                'status_code': comment_response.status_code,
                'message': comment_response.text[:200]  # First 200 chars
            }
        if not label_added and 'label_response' in locals():
            diagnostic_info['label_error'] = {
                'status_code': label_response.status_code,
                'message': label_response.text[:200]
            }
        
        kv_token = get_github_token()
        diagnostic_info['using_bot_token'] = bool(kv_token)
        diagnostic_info['bot_token_length'] = len(kv_token) if kv_token else 0
        diagnostic_info['bot_token_prefix'] = kv_token[:10] if kv_token else 'empty'
        diagnostic_info['report_regenerated'] = bool(report_url)
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "challenge_id": challenge_id,
                "message": "Challenge submitted successfully",
                "github_comment_posted": comment_posted,
                "github_label_added": label_added,
                "report_url": report_url,
                "diagnostics": diagnostic_info
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except AzureError as e:
        logger.error(f"❌ Azure error: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"Azure storage error: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.exception(e)
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )


@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint."""
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "RADAR Challenge Handler",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }),
        mimetype="application/json",
        status_code=200
    )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

# GitHub OAuth Configuration
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


@app.route(route="auth/callback", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def auth_callback(req: func.HttpRequest) -> func.HttpResponse:
    """
    GitHub OAuth callback endpoint.
    
    Flow:
    1. Receives 'code' from GitHub OAuth
    2. Exchanges code for access token
    3. Gets user info from GitHub API
    4. Verifies user is collaborator on microsoft/azurelinux
    5. Generates JWT token
    6. Redirects to HTML report with token
    """
    logger.info("🔐 GitHub OAuth callback received")
    
    try:
        # Get authorization code from query params
        code = req.params.get('code')
        state = req.params.get('state')  # Contains original report URL
        
        if not code:
            logger.error("❌ No authorization code provided")
            return func.HttpResponse(
                "Missing authorization code",
                status_code=400
            )
        
        logger.info(f"📝 Authorization code received, state: {state}")
        
        # Step 1: Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        }
        token_headers = {"Accept": "application/json"}
        
        logger.info("🔄 Exchanging code for access token...")
        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        token_json = token_response.json()
        
        if "access_token" not in token_json:
            logger.error(f"❌ Failed to get access token: {token_json}")
            return func.HttpResponse(
                f"Failed to authenticate with GitHub: {token_json.get('error_description', 'Unknown error')}",
                status_code=401
            )
        
        access_token = token_json["access_token"]
        logger.info("✅ Access token obtained")
        
        # Step 2: Get user info from GitHub
        user_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        logger.info("👤 Fetching user information...")
        user_response = requests.get("https://api.github.com/user", headers=user_headers)
        user_data = user_response.json()
        
        username = user_data.get("login")
        email = user_data.get("email") or f"{username}@users.noreply.github.com"
        avatar_url = user_data.get("avatar_url")
        name = user_data.get("name") or username
        
        logger.info(f"✅ User authenticated: {username}")
        
        # Step 3: Check repository permissions
        logger.info("🔍 Verifying repository permissions...")
        
        # Check if user is a collaborator
        collab_url = f"https://api.github.com/repos/microsoft/azurelinux/collaborators/{username}"
        collab_response = requests.get(collab_url, headers=user_headers)
        is_collaborator = collab_response.status_code == 204
        
        # Check if user is an admin (has push permission)
        permission_url = f"https://api.github.com/repos/microsoft/azurelinux/collaborators/{username}/permission"
        perm_response = requests.get(permission_url, headers=user_headers)
        is_admin = False
        if perm_response.status_code == 200:
            perm_data = perm_response.json()
            permission = perm_data.get("permission", "")
            is_admin = permission in ["admin", "maintain"]
        
        logger.info(f"{'✅' if is_collaborator else '⚠️'} Collaborator: {is_collaborator}, Admin: {is_admin}")
        
        # Step 4: Generate JWT token with permissions
        # Note: PR ownership is verified per-challenge since PR number isn't known at auth time
        jwt_payload = {
            "username": username,
            "email": email,
            "name": name,
            "avatar_url": avatar_url,
            "is_collaborator": is_collaborator,
            "is_admin": is_admin,
            "github_token": access_token,  # Store for later PR ownership checks
            "exp": datetime.utcnow().timestamp() + (JWT_EXPIRATION_HOURS * 3600),
            "iat": datetime.utcnow().timestamp()
        }
        
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logger.info(f"🎫 JWT token generated for {username}")
        
        # Step 5: Redirect back to HTML report with token
        # The 'state' parameter contains the original report URL
        redirect_url = state or "https://radarblobstore.blob.core.windows.net/radarcontainer/"
        
        # Add token to URL fragment (client-side only, not sent to server)
        redirect_url_with_token = f"{redirect_url}#token={jwt_token}"
        
        logger.info(f"🔄 Redirecting to: {redirect_url}")
        
        # Return HTML with auto-redirect (safer than 302 redirect for fragments)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Success</title>
            <script>
                // Store token in URL fragment and redirect
                window.location.href = "{redirect_url}#token={jwt_token}";
            </script>
        </head>
        <body>
            <p>Authentication successful! Redirecting...</p>
            <p>If not redirected automatically, <a href="{redirect_url}#token={jwt_token}">click here</a>.</p>
        </body>
        </html>
        """
        
        return func.HttpResponse(
            html_content,
            mimetype="text/html",
            status_code=200
        )
        
    except requests.RequestException as e:
        logger.error(f"❌ GitHub API error: {e}")
        return func.HttpResponse(
            f"GitHub API error: {str(e)}",
            status_code=500
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error in auth callback: {e}", exc_info=True)
        return func.HttpResponse(
            f"Authentication error: {str(e)}",
            status_code=500
        )


@app.route(route="auth/verify", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def verify_token(req: func.HttpRequest) -> func.HttpResponse:
    """
    Verify JWT token and return user info.
    
    Expected POST body:
    {
        "token": "jwt_token_here"
    }
    
    Returns user info if token is valid.
    """
    logger.info("🔍 Token verification requested")
    
    try:
        # Parse request body
        req_body = req.get_json()
        token = req_body.get("token")
        
        if not token:
            return func.HttpResponse(
                json.dumps({"error": "Missing token"}),
                mimetype="application/json",
                status_code=400
            )
        
        # Verify and decode JWT
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            logger.info(f"✅ Token valid for user: {payload.get('username')}")
            
            return func.HttpResponse(
                json.dumps({
                    "valid": True,
                    "user": {
                        "username": payload.get("username"),
                        "email": payload.get("email"),
                        "name": payload.get("name"),
                        "avatar_url": payload.get("avatar_url"),
                        "is_collaborator": payload.get("is_collaborator")
                    }
                }),
                mimetype="application/json",
                status_code=200
            )
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ Token expired")
            return func.HttpResponse(
                json.dumps({"valid": False, "error": "Token expired"}),
                mimetype="application/json",
                status_code=401
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"⚠️ Invalid token: {e}")
            return func.HttpResponse(
                json.dumps({"valid": False, "error": "Invalid token"}),
                mimetype="application/json",
                status_code=401
            )
            
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logger.error(f"❌ Error verifying token: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            mimetype="application/json",
            status_code=500
        )
