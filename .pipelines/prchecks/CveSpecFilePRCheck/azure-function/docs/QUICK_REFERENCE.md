# RADAR Authentication - Quick Reference Card

## 🔑 OAuth App Credentials

```
Client ID:      Ov23lIafwvl8EP0Qzgcmb
Client Secret:  [Stored securely - do not commit]
Callback URL:   https://radar-func-v2.azurewebsites.net/api/auth/callback
```

## 📦 Deployment Package

```
File:     function-complete-auth.zip (5.3 KB)
Location: azure-function/function-complete-auth.zip
```

## 🚀 One-Command Deployment (After Function Created)

```bash
#!/bin/bash
# Quick deployment script
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function

FUNC_NAME="radar-func-v2"
RG="Radar-Storage-RG"
STORAGE="radarstoragergac8b"
CONTAINER="app-package-radar-func-3747438"
GITHUB_SECRET="<YOUR_GITHUB_OAUTH_SECRET>"

echo "1️⃣ Uploading package..."
az storage blob upload \
  --account-name $STORAGE \
  --container-name $CONTAINER \
  --name radar-func-complete-auth.zip \
  --file function-complete-auth.zip \
  --auth-mode login \
  --overwrite

echo "2️⃣ Generating SAS token..."
SAS_URL=$(az storage blob generate-sas \
  --account-name $STORAGE \
  --container-name $CONTAINER \
  --name radar-func-complete-auth.zip \
  --permissions r \
  --expiry $(date -u -d '7 days' '+%Y-%m-%dT%H:%MZ') \
  --auth-mode login \
  --as-user \
  --full-uri \
  --output tsv)

echo "3️⃣ Configuring app settings..."
JWT_SECRET=$(openssl rand -hex 32)

az functionapp config appsettings set \
  --name $FUNC_NAME \
  --resource-group $RG \
  --settings \
    GITHUB_CLIENT_ID="Ov23lIafwvl8EP0Qzgcmb" \
    GITHUB_CLIENT_SECRET="$GITHUB_SECRET" \
    JWT_SECRET="$JWT_SECRET" \
    WEBSITE_RUN_FROM_PACKAGE="$SAS_URL" \
  --output none

echo "4️⃣ Granting blob permissions..."
PRINCIPAL_ID=$(az functionapp identity show \
  --name $FUNC_NAME \
  --resource-group $RG \
  --query principalId \
  --output tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/$RG/providers/Microsoft.Storage/storageAccounts/radarblobstore" \
  2>/dev/null || echo "Permission may already exist"

echo "5️⃣ Enabling CORS..."
az functionapp cors add \
  --name $FUNC_NAME \
  --resource-group $RG \
  --allowed-origins "https://radarblobstore.blob.core.windows.net" \
  2>/dev/null || echo "CORS may already be configured"

echo "6️⃣ Restarting function..."
az functionapp restart --name $FUNC_NAME --resource-group $RG

echo ""
echo "✅ Deployment complete!"
echo "⏰ Wait 30-60 seconds for cold start, then test:"
echo ""
echo "   curl https://$FUNC_NAME.azurewebsites.net/api/health"
echo ""
```

## 🧪 Quick Test Commands

```bash
# Health check
curl https://radar-func-v2.azurewebsites.net/api/health

# Expected: {"status":"healthy",...}

# Test with invalid token
curl -X POST https://radar-func-v2.azurewebsites.net/api/challenge \
  -H "Authorization: Bearer invalid_token" \
  -H "Content-Type: application/json" \
  -d '{"pr_number":14877,"antipattern_id":"test","challenge_type":"false-positive","feedback_text":"test"}'

# Expected: {"error":"Invalid token",...}
```

## 📱 User Flow

```
1. User visits HTML report
   ↓
2. Clicks "Sign in with GitHub"
   ↓
3. GitHub OAuth authorization
   ↓
4. Redirect back with JWT token
   ↓
5. Token stored in localStorage
   ↓
6. UI shows user info + avatar
   ↓
7. User submits challenge
   ↓
8. JWT sent in Authorization header
   ↓
9. Backend validates + stores with user identity
```

## 🔍 Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| "Authentication required" | Token in localStorage? | Sign in again |
| "Token expired" | Token > 24 hours old? | Sign in again |
| "GitHub API error" | GitHub credentials set? | Check app settings |
| 503 Service Unavailable | Function running? | Restart function |
| CORS error | Origin allowed? | Add blob storage origin |

## 📊 Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/api/health` | None | Health check |
| GET | `/api/auth/callback` | None | OAuth callback |
| POST | `/api/auth/verify` | None | Verify token |
| POST | `/api/challenge` | **JWT** | Submit challenge |

## 📝 HTML Changes

**File:** `ResultAnalyzer.py`

**Added:**
- RADAR_AUTH JavaScript module
- Sign-in/sign-out UI
- User avatar display
- Collaborator badge
- Token management

**Location:** Lines 640-810 (in HTML template)

## 🎯 Success Criteria

- ✅ HTML shows sign-in button
- ✅ OAuth redirects to GitHub
- ✅ User authorizes app
- ✅ Redirects back with token
- ✅ UI shows user info
- ✅ Challenge submission includes JWT
- ✅ Backend validates JWT
- ✅ Data stored with user identity

## 📚 Documentation

- **Full details:** AUTH_IMPLEMENTATION_SUMMARY.md
- **Deployment guide:** DEPLOYMENT_WITH_AUTH.md
- **OAuth app:** https://github.com/settings/applications/3213384
