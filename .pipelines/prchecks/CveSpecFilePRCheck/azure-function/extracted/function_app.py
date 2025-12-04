#!/usr/bin/env python3
"""
Azure Function: RADAR Challenge Handler
Handles challenge submissions for CVE spec file analysis findings.
"""

import azure.functions as func
import json
import logging
from datetime import datetime
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
    Handle challenge submissions and update blob JSON.
    
    Expected POST body:
    {
        "pr_number": 14877,
        "spec_file": "SPECS/curl/curl.spec",
        "antipattern_id": "curl-ap-001",
        "challenge_type": "false-positive",
        "feedback_text": "This is intentional because...",
        "user_email": "ahmedbadawi@microsoft.com"
    }
    
    Returns:
        JSON response with success status and challenge_id
    """
    logger.info("🎯 RADAR Challenge Handler - Processing request")
    
    try:
        # Parse request body
        try:
            req_body = req.get_json()
            logger.info(f"📥 Received challenge request: {json.dumps(req_body, indent=2)}")
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
            logger.error(f"❌ Analytics blob not found: {blob_name}")
            return func.HttpResponse(
                json.dumps({"error": f"Analytics data not found for PR #{pr_number}"}),
                mimetype="application/json",
                status_code=404
            )
        
        # Generate challenge ID
        existing_challenges = current_data.get("challenges", [])
        challenge_id = f"ch-{len(existing_challenges) + 1:03d}"
        
        # Create challenge entry
        challenge = {
            "challenge_id": challenge_id,
            "antipattern_id": antipattern_id,
            "spec_file": req_body.get("spec_file", ""),
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "submitted_by": req_body.get("user_email", "anonymous"),
            "challenge_type": req_body["challenge_type"],
            "feedback_text": req_body["feedback_text"],
            "status": "submitted"
        }
        
        logger.info(f"✏️  Creating challenge: {challenge_id} for antipattern: {antipattern_id}")
        
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
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "challenge_id": challenge_id,
                "message": "Challenge submitted successfully"
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
