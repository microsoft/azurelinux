# Azure Function Setup Guide

## 📋 Function App Information

- **Function App Name**: `radar-func`
- **Hostname**: `radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net`
- **Location**: Canada Central
- **Resource Group**: Radar-Storage-RG
- **Subscription**: EdgeOS_IoT_CBL-Mariner_DevTest
- **Runtime**: Python 3.11 on Linux

## 🔐 Configuration Required

### 1. Assign User Managed Identity (✅ DONE via Portal)
- UMI Client ID: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
- UMI Principal ID: `4cb669bf-1ae6-463a-801a-2d491da37b9d`

### 2. Enable CORS (Required for HTML to call function)

Via Azure Portal:
1. Go to Function App `radar-func`
2. Settings → CORS
3. Add allowed origin: `https://radarblobstore.blob.core.windows.net`
4. Click Save

Via Azure CLI:
```bash
az functionapp cors add \
  --name radar-func \
  --resource-group Radar-Storage-RG \
  --allowed-origins "https://radarblobstore.blob.core.windows.net"
```

### 3. Configure Application Settings (Optional but Recommended)

Via Azure Portal:
1. Go to Function App `radar-func`
2. Settings → Configuration → Application settings
3. Add new setting:
   - Name: `AZURE_CLIENT_ID`
   - Value: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
4. Click Save

Via Azure CLI:
```bash
az functionapp config appsettings set \
  --name radar-func \
  --resource-group Radar-Storage-RG \
  --settings AZURE_CLIENT_ID=7bf2e2c3-009a-460e-90d4-eff987a8d71d
```

## 🚀 Deployment Options

### Option 1: Deploy via VS Code (Recommended)

1. **Install VS Code Extension**:
   - Install "Azure Functions" extension in VS Code

2. **Sign in to Azure**:
   - Open VS Code Command Palette (Ctrl+Shift+P)
   - Run: `Azure: Sign In`

3. **Deploy**:
   - Right-click the `azure-function` folder
   - Select "Deploy to Function App..."
   - Choose subscription: `EdgeOS_IoT_CBL-Mariner_DevTest`
   - Choose function app: `radar-func`
   - Confirm deployment

### Option 2: Deploy via Azure Portal

1. **Prepare Deployment Package**:
   ```bash
   cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function
   zip -r function.zip . -x "*.git*" -x "__pycache__/*" -x ".venv/*"
   ```

2. **Upload via Portal**:
   - Go to https://portal.azure.com
   - Navigate to Function App `radar-func`
   - Deployment → Deployment Center
   - Choose deployment method: "ZIP Deploy" or "Local Git"
   - Upload `function.zip`

### Option 3: Deploy via Azure CLI with Basic Auth

If you have contributor permissions:

```bash
# Set basic auth credentials (if needed)
az functionapp deployment list-publishing-credentials \
  --name radar-func \
  --resource-group Radar-Storage-RG

# Deploy
cd azure-function
az functionapp deployment source config-zip \
  --resource-group Radar-Storage-RG \
  --name radar-func \
  --src function.zip
```

If you get 403 error, you may need to enable basic auth:
```bash
az resource update \
  --resource-group Radar-Storage-RG \
  --name scm \
  --resource-type basicPublishingCredentialsPolicies \
  --parent sites/radar-func \
  --set properties.allow=true
```

### Option 4: GitHub Actions (For CI/CD)

Create `.github/workflows/deploy-function.yml`:
```yaml
name: Deploy Azure Function

on:
  push:
    branches:
      - main
    paths:
      - '.pipelines/prchecks/CveSpecFilePRCheck/azure-function/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Deploy to Azure Function
        uses: Azure/functions-action@v1
        with:
          app-name: 'radar-func'
          package: '.pipelines/prchecks/CveSpecFilePRCheck/azure-function'
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

## ✅ Verify Deployment

### Test Health Endpoint
```bash
curl https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "RADAR Challenge Handler",
  "timestamp": "2025-10-16T21:00:00Z"
}
```

### Test Challenge Endpoint
```bash
curl -X POST \
  https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "pr_number": 14877,
    "antipattern_id": "test-ap-001",
    "challenge_type": "false-positive",
    "feedback_text": "Test challenge",
    "user_email": "test@example.com"
  }'
```

## 🔍 Monitoring & Logs

### View Logs via Portal
1. Go to Function App `radar-func`
2. Functions → `challenge` → Monitor
3. View Invocations and Logs

### Stream Logs via CLI
```bash
az webapp log tail \
  --name radar-func \
  --resource-group Radar-Storage-RG
```

### Application Insights
Logs are automatically sent to Application Insights (if enabled).

## 🌐 API Endpoint URLs

Once deployed, your endpoints will be:

- **Health Check**: `https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health`
- **Challenge Submission**: `https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge`

Use these URLs in your HTML JavaScript code.

## 📝 Next Steps

1. ✅ Deploy function code (choose deployment method above)
2. ✅ Configure CORS for blob storage origin
3. ✅ Test health endpoint
4. ✅ Test challenge endpoint with sample data
5. ✅ Integrate endpoint URL into HTML dashboard JavaScript
6. ✅ Test end-to-end from HTML page

## ⚠️ Troubleshooting

### 403 Forbidden on Deployment
- Enable basic authentication in portal: Settings → Configuration → General settings → SCM Basic Auth → On
- Or use VS Code deployment method

### Function not authenticating to blob storage
- Verify UMI is assigned to function app
- Verify UMI has "Storage Blob Data Contributor" role on storage account
- Check Application Insights logs for authentication errors

### CORS errors in browser
- Add blob storage origin to CORS allowed origins
- Ensure origin matches exactly (including https://)

### Function cold starts
- Consider using Premium plan for instant warm-up
- Or accept 5-10 second delay on first request after idle period
