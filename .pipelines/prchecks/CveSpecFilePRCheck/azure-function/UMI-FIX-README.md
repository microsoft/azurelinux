# Azure Function UMI Configuration Fix

## Issue

Challenge submissions were failing with:
```
Azure storage error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

## Root Cause

The Azure Function (`radarfunc-eka5fmceg4b5fub0`) was using `DefaultAzureCredential()` without specifying which managed identity to use.

When the storage account has **key-based authentication disabled** (security best practice), `DefaultAzureCredential` must be configured with the UMI's client ID via the `AZURE_CLIENT_ID` environment variable.

## Solution

Set the `AZURE_CLIENT_ID` environment variable in the Azure Function app settings to point to the `cblmargh-identity` UMI.

### Quick Fix (Run this script)

```bash
cd .pipelines/prchecks/CveSpecFilePRCheck/azure-function
./configure-umi.sh
```

### Manual Fix

```bash
az functionapp config appsettings set \
  --name radarfunc-eka5fmceg4b5fub0 \
  --resource-group Radar-Storage-RG \
  --settings "AZURE_CLIENT_ID=7bf2e2c3-009a-460e-90d4-eff987a8d71d"
```

## Verification

After applying the fix:

1. **Check the setting is applied:**
   ```bash
   az functionapp config appsettings list \
     --name radarfunc-eka5fmceg4b5fub0 \
     --resource-group Radar-Storage-RG \
     --query "[?name=='AZURE_CLIENT_ID']"
   ```

2. **Test challenge submission:**
   - Open the HTML report from blob storage
   - Sign in with GitHub OAuth
   - Click "Challenge" on any finding
   - Select response type and add explanation
   - Click Submit
   - Should see "✅ Challenge submitted successfully!"

## Technical Details

### UMI Information
- **Name**: cblmargh-identity
- **Application/Client ID**: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
- **Object ID**: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
- **Permissions**: 
  - Contributor (subscription level)
  - Storage Blob Data Contributor (on radarblobstore)

### Related Fixes

This is the same fix applied to the pipeline in commit `e35117466`:
- Pipeline YAML also sets `AZURE_CLIENT_ID` environment variable
- Allows blob storage uploads from Azure DevOps pipeline
- Both pipeline and Azure Function now use the same UMI correctly

### Code References

**function_app.py** (line 177):
```python
credential = DefaultAzureCredential()  # Now will use AZURE_CLIENT_ID env var
blob_service_client = BlobServiceClient(
    account_url=STORAGE_ACCOUNT_URL,
    credential=credential
)
```

Without `AZURE_CLIENT_ID`, `DefaultAzureCredential` tries multiple authentication methods and fails because:
- EnvironmentCredential: No env vars set
- ManagedIdentityCredential: Multiple UMIs available, doesn't know which to use
- AzureCliCredential: Not available in Azure Function runtime
- etc.

With `AZURE_CLIENT_ID=7bf2e2c3-009a-460e-90d4-eff987a8d71d`, it directly uses the specified UMI.

## Status

- ✅ **Pipeline fixed** (commit e35117466)
- ⏳ **Azure Function needs fix** (run configure-umi.sh)
- ⏳ **CORS configuration** (also needed - see below)

## Additional Configuration Needed

The Azure Function also needs CORS configured to allow requests from blob storage URLs:

```bash
az functionapp cors add \
  --name radarfunc-eka5fmceg4b5fub0 \
  --resource-group Radar-Storage-RG \
  --allowed-origins "https://radarblobstore.blob.core.windows.net"
```

This allows the HTML reports served from blob storage to call the Azure Function endpoints.
