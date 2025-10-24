# Azure Function Deployment Guide

## Quick Deploy

### 1. Package the Function

```bash
cd .pipelines/prchecks/CveSpecFilePRCheck/azure-function
zip -r function-app.zip . -x "*.git*" -x "__pycache__/*" -x "*.pyc"
```

### 2. Deploy to Azure Function App

```bash
az functionapp deployment source config-zip \
  --resource-group <your-resource-group> \
  --name radarfunc \
  --src function-app.zip
```

**Or using Azure Portal:**

1. Go to Azure Portal → Function Apps → `radarfunc`
2. Click **Deployment Center** (left sidebar)
3. Click **Manual Deployment** → **Zip Deploy**
4. Upload `function-app.zip`
5. Click **Deploy**

### 3. Verify Deployment

Check the function logs:

```bash
az functionapp logs tail \
  --resource-group <your-resource-group> \
  --name radarfunc
```

Or in Azure Portal:
- Function Apps → radarfunc → Log stream

### 4. Test the Function

The function will now automatically fetch the GitHub token from Key Vault using Managed Identity.

**Check logs for confirmation:**
```
🔐 Fetching GitHub token from Key Vault: https://mariner-pipelines-kv.vault.azure.net
✅ GitHub token fetched successfully from Key Vault
🔑 Token prefix: ghp_vY8EUh...
```

## Configuration

### Managed Identity Permissions

The Function App's Managed Identity must have **Get** and **List** permissions on the Key Vault:

1. Go to Azure Portal → Key Vaults → `mariner-pipelines-kv`
2. Click **Access policies**
3. Verify `radarfunc` (or its managed identity) has:
   - **Secret permissions**: Get, List

### Key Vault Configuration

- **Key Vault URL**: `https://mariner-pipelines-kv.vault.azure.net`
- **Secret Name**: `cblmarghGithubPRPat`
- **Secret Value**: GitHub PAT token (starts with `ghp_`)

## Benefits of This Approach

✅ **No manual environment variable updates needed**
✅ **Token automatically stays current** - just update Key Vault
✅ **Centralized token management**
✅ **Secure access via Managed Identity**
✅ **Token caching for performance**

## Troubleshooting

### Function fails to fetch token

**Error**: "Failed to fetch GitHub token from Key Vault"

**Solutions:**
1. Verify Managed Identity has Key Vault permissions
2. Check Key Vault firewall settings
3. Verify secret name is exactly `cblmarghGithubPRPat`
4. Check Function App logs for detailed error

### Fallback behavior

If Key Vault fetch fails, the function will:
1. Log an error
2. Attempt to use `GITHUB_TOKEN` environment variable as fallback
3. If no fallback available, return error to client
