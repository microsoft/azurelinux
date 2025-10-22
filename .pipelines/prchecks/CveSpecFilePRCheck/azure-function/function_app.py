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

app = func.FunctionApp()

# Configuration
STORAGE_ACCOUNT_URL = "https://radarblobstore.blob.core.windows.net"
CONTAINER_NAME = "radarcontainer"

logger = logging.getLogger(__name__)


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
        "antipattern_id": "curl-ap-001",
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
        required_fields = ["pr_number", "antipattern_id", "challenge_type", "feedback_text"]
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
        antipattern_id = req_body["antipattern_id"]
        
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
            "antipattern_id": antipattern_id,
            "spec_file": req_body.get("spec_file", ""),
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "submitted_by": {
                "username": username,
                "email": email,
                "is_collaborator": is_collaborator
            },
            "challenge_type": req_body["challenge_type"],
            "feedback_text": req_body["feedback_text"],
            "status": "submitted"
        }
        
        logger.info(f"✏️  Creating challenge: {challenge_id} for antipattern: {antipattern_id} by {username}")
        
        # Add challenge to data
        if "challenges" not in current_data:
            current_data["challenges"] = []
        current_data["challenges"].append(challenge)
        
        # Update antipattern status
        antipattern_found = False
        for spec in current_data.get("specs", []):
            for ap in spec.get("antipatterns", []):
                if ap["id"] == antipattern_id:
                    ap["status"] = "challenged"
                    if req_body["challenge_type"] == "false-positive":
                        ap["marked_false_positive"] = True
                    antipattern_found = True
                    logger.info(f"✅ Updated antipattern status: {antipattern_id} -> challenged")
                    break
            if antipattern_found:
                break
        
        if not antipattern_found:
            logger.warning(f"⚠️  Antipattern not found in data: {antipattern_id}")
        
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
        
        # Post GitHub comment about the challenge
        try:
            logger.info(f"💬 Posting challenge notification to GitHub PR #{pr_number}")
            
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
            
            comment_body = f"""## {emoji} Challenge Submitted

**Finding**: {antipattern_id} in `{req_body.get("spec_file", "")}`  
**Challenge Type**: {type_text}  
**Submitted by**: @{username}  

**Feedback**:
> {req_body["feedback_text"]}

---
*Challenge ID: `{challenge_id}` • This challenge will be reviewed by the team.*
"""
            
            comment_url = f"https://api.github.com/repos/microsoft/azurelinux/issues/{pr_number}/comments"
            comment_headers = {
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            comment_response = requests.post(
                comment_url,
                headers=comment_headers,
                json={"body": comment_body},
                timeout=10
            )
            
            comment_posted = False
            if comment_response.status_code == 201:
                logger.info(f"✅ GitHub comment posted successfully")
                comment_posted = True
            else:
                logger.error(f"❌ Failed to post GitHub comment:")
                logger.error(f"   Status: {comment_response.status_code}")
                logger.error(f"   Response: {comment_response.text}")
                logger.error(f"   GitHub Token (first 10 chars): {github_token[:10] if github_token else 'None'}...")
                logger.error(f"   Comment URL: {comment_url}")
            
            # Add simple label to indicate PR has been acknowledged/reviewed
            logger.info(f"🏷️  Adding radar-acknowledged label to PR #{pr_number}")
            
            labels_url = f"https://api.github.com/repos/microsoft/azurelinux/issues/{pr_number}/labels"
            label_response = requests.post(
                labels_url,
                headers=comment_headers,
                json={"labels": ["radar-acknowledged"]},
                timeout=10
            )
            
            label_added = False
            if label_response.status_code == 200:
                logger.info(f"✅ Label 'radar-acknowledged' added successfully")
                label_added = True
            else:
                logger.error(f"❌ Failed to add label:")
                logger.error(f"   Status: {label_response.status_code}")
                logger.error(f"   Response: {label_response.text}")
                logger.info("   Note: Label might not exist in repo - create 'radar-acknowledged' label first")
        
        except Exception as comment_error:
            logger.error(f"❌ Exception during GitHub comment/label posting:")
            logger.error(f"   Error: {comment_error}")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            comment_posted = False
            label_added = False
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "challenge_id": challenge_id,
                "message": "Challenge submitted successfully",
                "github_comment_posted": comment_posted,
                "github_label_added": label_added
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
