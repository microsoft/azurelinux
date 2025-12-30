# Azure Function Configuration for RADAR Authentication

## Required App Settings

Once the Azure Function app is created, configure these settings:

```bash
# Navigate to function directory
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function

# Set GitHub OAuth credentials
az functionapp config appsettings set \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --settings \
    GITHUB_CLIENT_ID="Ov23lIafwvl8EP0Qzgcmb" \
    GITHUB_CLIENT_SECRET="<YOUR_SECRET_HERE>" \
    JWT_SECRET="$(openssl rand -hex 32)" \
  --output none

echo "✅ Settings configured"
```

## GitHub OAuth App Details

- **Application Name:** RADAR CVE Analysis Tool
- **Client ID:** `Ov23lIafwvl8EP0Qzgcmb`
- **Client Secret:** Stored securely (set in app settings above)
- **Callback URL:** `https://radar-func-v2.azurewebsites.net/api/auth/callback`
- **Homepage URL:** `https://github.com/microsoft/azurelinux`

## Deployment Steps

### 1. Upload Package to Blob Storage

```bash
# Upload the function package
az storage blob upload \
  --account-name radarstoragergac8b \
  --container-name app-package-radar-func-3747438 \
  --name radar-func-with-auth.zip \
  --file function-with-auth.zip \
  --auth-mode login \
  --overwrite

echo "✅ Package uploaded"
```

### 2. Generate SAS Token

```bash
# Generate 7-day SAS token
az storage blob generate-sas \
  --account-name radarstoragergac8b \
  --container-name app-package-radar-func-3747438 \
  --name radar-func-with-auth.zip \
  --permissions r \
  --expiry $(date -u -d '7 days' '+%Y-%m-%dT%H:%MZ') \
  --auth-mode login \
  --as-user \
  --full-uri

# Copy the output URL
```

### 3. Configure Run from Package

```bash
# Set WEBSITE_RUN_FROM_PACKAGE with SAS URL from step 2
az functionapp config appsettings set \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --settings WEBSITE_RUN_FROM_PACKAGE="<PASTE_SAS_URL_HERE>" \
  --output none

echo "✅ Run from Package configured"
```

### 4. Assign Managed Identity Permissions

```bash
# Get the function's managed identity principal ID
PRINCIPAL_ID=$(az functionapp identity show \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG \
  --query principalId \
  --output tsv)

echo "Managed Identity: $PRINCIPAL_ID"

# Grant Storage Blob Data Contributor role on radarblobstore
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"

echo "✅ Permissions granted"
```

### 5. Restart Function App

```bash
az functionapp restart \
  --name radar-func-v2 \
  --resource-group Radar-Storage-RG

echo "✅ Function app restarted"
echo "⏰ Wait 30-60 seconds for cold start..."
```

### 6. Test Endpoints

```bash
# Test health endpoint
curl https://radar-func-v2.azurewebsites.net/api/health

# Expected: {"status":"healthy","service":"RADAR Challenge Handler","timestamp":"..."}
```

## API Endpoints

### Authentication Endpoints

1. **GET /api/auth/callback**
   - GitHub OAuth callback
   - Receives: `code` and `state` query parameters
   - Returns: HTML redirect with JWT token in URL fragment

2. **POST /api/auth/verify**
   - Verify JWT token validity
   - Body: `{"token": "jwt_here"}`
   - Returns: User info if valid

3. **POST /api/challenge**
   - Submit challenge (requires JWT in Authorization header)
   - Body: `{"pr_number": ..., "antipattern_id": ..., "challenge_type": ..., "feedback_text": ...}`
   - Returns: Challenge confirmation

4. **GET /api/health**
   - Health check
   - Returns: Service status

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_CLIENT_ID` | OAuth App Client ID | `Ov23lIafwvl8EP0Qzgcmb` |
| `GITHUB_CLIENT_SECRET` | OAuth App Client Secret | `gho_xxx...` |
| `JWT_SECRET` | Secret for signing JWT tokens | Generate with `openssl rand -hex 32` |
| `WEBSITE_RUN_FROM_PACKAGE` | Blob URL with SAS token | `https://radarstoragergac8b.blob...` |

## Security Notes

- JWT tokens expire after 24 hours
- GitHub OAuth verifies collaborator status on `microsoft/azurelinux`
- Tokens are passed via URL fragments (not sent to server logs)
- CORS will be configured to allow blob storage origin
