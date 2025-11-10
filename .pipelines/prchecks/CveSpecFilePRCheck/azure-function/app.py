#!/usr/bin/env python3
"""
Flask API: RADAR Challenge Handler
Handles challenge submissions for CVE spec file analysis findings.
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError, ResourceNotFoundError

app = Flask(__name__)

# Configuration
STORAGE_ACCOUNT_URL = "https://radarblobstore.blob.core.windows.net"
CONTAINER_NAME = "radarcontainer"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_blob_client(blob_name):
    """Get blob client using managed identity."""
    try:
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=STORAGE_ACCOUNT_URL,
            credential=credential
        )
        return blob_service_client.get_blob_client(
            container=CONTAINER_NAME,
            blob=blob_name
        )
    except Exception as e:
        logger.error(f"Failed to create blob client: {e}")
        raise


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "RADAR Challenge Handler",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route('/api/challenge', methods=['POST'])
def submit_challenge():
    """
    Handle challenge submissions and update blob JSON.
    
    Expected POST body:
    {
        "pr_number": 14877,
        "antipattern_id": "finding-001",
        "challenge_type": "false-positive" | "needs-clarification" | "incorrect-severity",
        "feedback_text": "User feedback text",
        "user_email": "user@example.com"
    }
    """
    try:
        # Parse request body
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['pr_number', 'antipattern_id', 'challenge_type', 'feedback_text']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        pr_number = data['pr_number']
        antipattern_id = data['antipattern_id']
        challenge_type = data['challenge_type']
        feedback_text = data['feedback_text']
        user_email = data.get('user_email', 'anonymous@example.com')
        
        # Validate challenge type
        valid_types = ['false-positive', 'needs-clarification', 'incorrect-severity']
        if challenge_type not in valid_types:
            return jsonify({
                "success": False,
                "error": f"Invalid challenge_type. Must be one of: {', '.join(valid_types)}"
            }), 400
        
        logger.info(f"Processing challenge for PR {pr_number}, finding {antipattern_id}")
        
        # Get the analytics JSON blob
        blob_name = f"pr-{pr_number}/analytics.json"
        blob_client = get_blob_client(blob_name)
        
        # Download existing JSON
        try:
            blob_data = blob_client.download_blob().readall()
            analytics_data = json.loads(blob_data)
            logger.info(f"Downloaded existing analytics data for PR {pr_number}")
        except ResourceNotFoundError:
            # Create new analytics structure if doesn't exist
            analytics_data = {
                "pr_number": pr_number,
                "findings": {},
                "challenges": [],
                "metrics": {
                    "total_findings": 0,
                    "challenged_findings": 0,
                    "false_positive_rate": 0.0
                }
            }
            logger.info(f"Creating new analytics data for PR {pr_number}")
        
        # Create challenge record
        challenge_id = f"ch-{len(analytics_data.get('challenges', []))}-{int(datetime.utcnow().timestamp())}"
        challenge = {
            "challenge_id": challenge_id,
            "antipattern_id": antipattern_id,
            "challenge_type": challenge_type,
            "feedback_text": feedback_text,
            "user_email": user_email,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Update analytics data
        if 'challenges' not in analytics_data:
            analytics_data['challenges'] = []
        analytics_data['challenges'].append(challenge)
        
        # Update metrics
        if 'metrics' not in analytics_data:
            analytics_data['metrics'] = {}
        
        challenged_findings = len(set(c['antipattern_id'] for c in analytics_data['challenges']))
        total_findings = analytics_data.get('metrics', {}).get('total_findings', 0)
        
        analytics_data['metrics']['challenged_findings'] = challenged_findings
        if total_findings > 0:
            analytics_data['metrics']['false_positive_rate'] = challenged_findings / total_findings
        
        # Upload updated JSON
        updated_json = json.dumps(analytics_data, indent=2)
        blob_client.upload_blob(updated_json, overwrite=True)
        
        logger.info(f"Successfully processed challenge {challenge_id}")
        
        return jsonify({
            "success": True,
            "challenge_id": challenge_id,
            "message": "Challenge submitted successfully",
            "timestamp": challenge['timestamp']
        }), 200
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {e}")
        return jsonify({
            "success": False,
            "error": "Invalid JSON in request body"
        }), 400
        
    except AzureError as e:
        logger.error(f"Azure storage error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to update analytics data"
        }), 500
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        "service": "RADAR Challenge Handler API",
        "version": "1.0.0",
        "endpoints": {
            "/api/health": "Health check",
            "/api/challenge": "Submit challenge (POST)"
        }
    }), 200


if __name__ == '__main__':
    # Run on port 8080 for container deployment
    app.run(host='0.0.0.0', port=8080, debug=False)
