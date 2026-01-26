# Azure Function - RADAR Challenge Handler

This Azure Function handles challenge submissions for CVE spec file analysis findings.

## Endpoints

### POST /api/challenge
Submit a challenge for an anti-pattern finding.

**Request Body:**
```json
{
  "pr_number": 14877,
  "spec_file": "SPECS/curl/curl.spec",
  "antipattern_id": "curl-ap-001",
  "challenge_type": "false-positive",
  "feedback_text": "This is intentional because...",
  "user_email": "ahmedbadawi@microsoft.com"
}
```

**Challenge Types:**
- `false-positive`: Finding is not actually an issue
- `needs-context`: Issue exists but is intentional for specific reason
- `disagree-with-severity`: Issue exists but severity is too high

**Response (Success):**
```json
{
  "success": true,
  "challenge_id": "ch-001",
  "message": "Challenge submitted successfully"
}
```

**Response (Error):**
```json
{
  "error": "Error description"
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "RADAR Challenge Handler",
  "timestamp": "2025-10-16T21:00:00Z"
}
```

## Authentication

Uses User Managed Identity (UMI) to access Azure Blob Storage with read/write permissions.

## Deployment

Deploy to Azure Function App `radar-func` using Azure CLI:

```bash
cd azure-function
func azure functionapp publish radar-func
```

Or using VS Code Azure Functions extension.

## Configuration

- **Storage Account**: radarblobstore
- **Container**: radarcontainer
- **UMI Client ID**: 7bf2e2c3-009a-460e-90d4-eff987a8d71d
