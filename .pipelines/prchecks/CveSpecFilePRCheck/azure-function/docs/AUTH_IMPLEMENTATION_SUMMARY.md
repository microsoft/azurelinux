# RADAR GitHub OAuth Authentication - Implementation Complete ✅

## Summary

GitHub OAuth authentication has been fully implemented for the RADAR CVE Analysis Tool. Users can now sign in to HTML reports hosted on blob storage, and their identity is captured and stored with challenge submissions.

---

## ✅ Completed Components

### 1. **GitHub OAuth App** 
- **Application Name:** RADAR CVE Analysis Tool
- **Owner:** @abadawi591 (personal account)
- **Client ID:** `Ov23lIafwvl8EP0Qzgcmb`
- **Client Secret:** Stored securely
- **Callback URL:** `https://radar-func-v2.azurewebsites.net/api/auth/callback`
- **Homepage:** `https://github.com/microsoft/azurelinux`
- **Scopes:** `read:user`, `read:org`

### 2. **Azure Function Backend** (`function_app.py`)

#### Authentication Endpoints:

**GET /api/auth/callback**
- Receives OAuth `code` from GitHub
- Exchanges code for GitHub access token
- Fetches user info from GitHub API
- Verifies collaborator status on `microsoft/azurelinux`
- Generates JWT token (24-hour expiration)
- Redirects back to HTML report with token in URL fragment

**POST /api/auth/verify**
- Validates JWT tokens
- Returns user info if valid
- Returns error for expired/invalid tokens

**POST /api/challenge** (UPDATED)
- Now requires `Authorization: Bearer <JWT>` header
- Validates JWT before accepting submission
- Extracts user info from token
- Stores challenge with authenticated user data:
  ```json
  {
    "submitted_by": {
      "username": "abadawi591",
      "email": "ahmedbadawi@microsoft.com",
      "is_collaborator": true
    }
  }
  ```

**GET /api/health**
- Health check endpoint (unchanged)

#### Dependencies Added:
- `PyJWT>=2.8.0` - JWT token handling
- `requests>=2.31.0` - GitHub API calls
- `cryptography>=41.0.0` - JWT cryptographic operations

### 3. **Client-Side JavaScript** (`ResultAnalyzer.py` HTML Template)

#### RADAR_AUTH Module Functions:

| Function | Description |
|----------|-------------|
| `signIn()` | Redirects to GitHub OAuth with current URL as state |
| `signOut()` | Clears localStorage and updates UI |
| `handleAuthCallback()` | Extracts JWT from URL fragment, stores in localStorage |
| `getCurrentUser()` | Returns user object from localStorage |
| `getAuthToken()` | Returns JWT token from localStorage |
| `isAuthenticated()` | Checks if user is signed in |
| `getAuthHeaders()` | Returns headers with Bearer token for API calls |
| `updateUI()` | Shows sign-in button or user menu based on auth state |

#### UI Components:

**Before Sign-In:**
```html
[Sign in with GitHub] button
```

**After Sign-In:**
```html
┌─────────────────────────────────┐
│ 👤 [Avatar]  John Doe           │
│              ✓ Collaborator     │
│                     [Sign Out]  │
└─────────────────────────────────┘
```

#### LocalStorage Keys:
- `radar_auth_token` - JWT token
- `radar_user_info` - User object (username, email, avatar, is_collaborator)

### 4. **Security Features**

✅ **JWT Tokens:**
- Signed with secret key
- 24-hour expiration
- Include user identity and collaborator status
- Passed via URL fragments (not sent to servers)

✅ **OAuth Flow:**
- GitHub handles authentication
- Only collaborators on `microsoft/azurelinux` verified
- State parameter prevents CSRF attacks

✅ **API Security:**
- Challenges require authentication
- Invalid/expired tokens rejected with 401
- User identity verified before storing data

---

## 📦 Deployment Package

**File:** `function-complete-auth.zip` (5.3 KB)
**Contents:**
- `function_app.py` (17.8 KB) - All auth endpoints implemented
- `host.json` - Azure Functions configuration
- `requirements.txt` - Python dependencies with auth packages

**Location:**
```
/home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function/function-complete-auth.zip
```

---

## 🚀 Deployment Steps (When Azure Function is Created)

### Step 1: Configure App Settings

```bash
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function

# Generate JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Set all environment variables
az functionapp config appsettings set \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --settings \
    GITHUB_CLIENT_ID="Ov23lIafwvl8EP0Qzgcmb" \
    GITHUB_CLIENT_SECRET="<YOUR_SECRET_HERE>" \
    JWT_SECRET="$JWT_SECRET" \
  --output none

echo "✅ OAuth credentials configured"
```

### Step 2: Upload Package to Blob Storage

```bash
# Upload function package
az storage blob upload \
  --account-name radarstoragergac8b \
  --container-name app-package-radar-func-3747438 \
  --name radar-func-complete-auth.zip \
  --file function-complete-auth.zip \
  --auth-mode login \
  --overwrite

echo "✅ Package uploaded"
```

### Step 3: Generate SAS Token

```bash
# Generate 7-day SAS token
SAS_URL=$(az storage blob generate-sas \
  --account-name radarstoragergac8b \
  --container-name app-package-radar-func-3747438 \
  --name radar-func-complete-auth.zip \
  --permissions r \
  --expiry $(date -u -d '7 days' '+%Y-%m-%dT%H:%MZ') \
  --auth-mode login \
  --as-user \
  --full-uri \
  --output tsv)

echo "SAS URL: $SAS_URL"
```

### Step 4: Configure Run from Package

```bash
# Set WEBSITE_RUN_FROM_PACKAGE
az functionapp config appsettings set \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --settings WEBSITE_RUN_FROM_PACKAGE="$SAS_URL" \
  --output none

echo "✅ Run from Package configured"
```

### Step 5: Assign Managed Identity Permissions

```bash
# Get function's managed identity
PRINCIPAL_ID=$(az functionapp identity show \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --query principalId \
  --output tsv)

# Grant blob storage permissions
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"

echo "✅ Permissions granted to $PRINCIPAL_ID"
```

### Step 6: Enable CORS

```bash
# Allow HTML reports to call function API
az functionapp cors add \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --allowed-origins "https://radarblobstore.blob.core.windows.net"

echo "✅ CORS configured"
```

### Step 7: Restart and Test

```bash
# Restart function app
az functionapp restart \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG

echo "⏰ Waiting for cold start (30 seconds)..."
sleep 30

# Test health endpoint
curl https://radar-func-v2.azurewebsites.net/api/health

# Expected: {"status":"healthy","service":"RADAR Challenge Handler","timestamp":"..."}
```

---

## 🧪 Testing the Authentication Flow

### Test Plan:

1. **Generate New HTML Report:**
   ```bash
   # Trigger pipeline or run locally to generate HTML with auth UI
   # HTML will now include sign-in button and RADAR_AUTH module
   ```

2. **Visit HTML Report:**
   - Open report URL: `https://radarblobstore.blob.core.windows.net/radarcontainer/pr-XXXXX/report.html`
   - Should see "Sign in with GitHub" button in top-right corner

3. **Sign In:**
   - Click "Sign in with GitHub"
   - Redirects to GitHub OAuth authorization page
   - Authorize "RADAR CVE Analysis Tool"
   - Redirects back to HTML report

4. **Verify Authentication:**
   - Should see user avatar and name in top-right
   - If collaborator, should see "✓ Collaborator" badge
   - Token stored in browser's localStorage

5. **Submit Challenge:**
   - Click on an anti-pattern finding
   - Fill in challenge form
   - Submit challenge
   - Backend validates JWT and stores with user identity

6. **Verify Data:**
   ```bash
   # Download analytics JSON
   az storage blob download \
     --account-name radarblobstore \
     --container-name radarcontainer \
     --name pr-XXXXX/analytics.json \
     --file analytics.json \
     --auth-mode login
   
   # Check challenge has user info
   cat analytics.json | grep -A 5 "submitted_by"
   ```

7. **Test Token Expiration:**
   - Wait 24+ hours or manually clear token
   - Try to submit challenge
   - Should prompt to sign in again

---

## 📊 Data Schema Update

### Challenge Object (Before):
```json
{
  "challenge_id": "ch-001",
  "antipattern_id": "curl-ap-001",
  "submitted_at": "2025-10-20T21:00:00Z",
  "submitted_by": "anonymous",
  "challenge_type": "false-positive",
  "feedback_text": "...",
  "status": "submitted"
}
```

### Challenge Object (After):
```json
{
  "challenge_id": "ch-001",
  "antipattern_id": "curl-ap-001",
  "submitted_at": "2025-10-20T21:00:00Z",
  "submitted_by": {
    "username": "abadawi591",
    "email": "ahmedbadawi@microsoft.com",
    "is_collaborator": true
  },
  "challenge_type": "false-positive",
  "feedback_text": "...",
  "status": "submitted"
}
```

---

## 🔒 Security Considerations

| Aspect | Implementation |
|--------|----------------|
| **Token Storage** | LocalStorage (client-side only) |
| **Token Transmission** | URL fragments (not sent to servers) |
| **Token Expiration** | 24 hours |
| **Token Validation** | Server-side JWT verification |
| **Collaborator Verification** | GitHub API check during OAuth |
| **HTTPS Only** | All endpoints use HTTPS |
| **CORS** | Restricted to blob storage origin |

---

## 🔄 Migration Notes

If/when migrating from personal OAuth app to organization OAuth app:

1. Create new OAuth app in Microsoft org
2. Get new Client ID and Client Secret
3. Update Azure Function app settings:
   ```bash
   az functionapp config appsettings set \
     --name radar-func-v2 \
     --resource-group Radar-Storage-RG \
     --settings \
       GITHUB_CLIENT_ID="<NEW_ORG_CLIENT_ID>" \
       GITHUB_CLIENT_SECRET="<NEW_ORG_CLIENT_SECRET>"
   ```
4. Update HTML template constant in ResultAnalyzer.py:
   ```javascript
   const GITHUB_CLIENT_ID = '<NEW_ORG_CLIENT_ID>';
   ```
5. Restart function app
6. **No other code changes needed!**

---

## 📝 Next Steps

1. ⏳ **Wait for admin to create Azure Function app**
2. 🚀 **Deploy function-complete-auth.zip** using steps above
3. 🧪 **Test authentication flow** end-to-end
4. 📊 **Verify data storage** with user attribution
5. 🔄 **Consider org OAuth migration** for production

---

## 📞 Support

For questions or issues:
- Check DEPLOYMENT_WITH_AUTH.md for detailed deployment instructions
- Review function logs: `az functionapp log tail --name radar-func-v2 --resource-group Radar-Storage-RG`
- Test endpoints manually with curl
- Verify OAuth app settings at https://github.com/settings/applications/3213384

---

**Implementation Status:** ✅ **COMPLETE - Ready for Deployment**

*Waiting on: Admin to create Azure Function app*
