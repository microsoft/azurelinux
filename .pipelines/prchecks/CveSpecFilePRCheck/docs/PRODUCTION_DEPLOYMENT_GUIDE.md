# Production Deployment Guide - Blob Storage Integration

## Overview
This guide covers deploying the blob storage integration to the Azure DevOps pipeline. The code is **production-ready** and will automatically use User Managed Identity (UMI) authentication when running on the ADO agent pool.

---

## ✅ Code Changes Summary

### Files Modified:

1. **`CveSpecFilePRCheck.py`** (Main pipeline script)
   - Added `BlobStorageClient` import
   - Initialize `BlobStorageClient` in `main()` before posting GitHub comments
   - Pass `blob_storage_client` and `pr_number` to `generate_multi_spec_report()`
   - Graceful fallback: If blob client initialization fails, falls back to Gist

2. **`ResultAnalyzer.py`** (Report generation)
   - Updated `generate_multi_spec_report()` signature to accept `blob_storage_client` and `pr_number`
   - **Dual upload strategy**: 
     - Try blob storage first (preferred)
     - Fall back to Gist if blob fails or not available
   - Same HTML link formatting for both methods
   - Comprehensive logging for troubleshooting

3. **`BlobStorageClient.py`** (NEW - Azure Blob Storage client)
   - Uses `DefaultAzureCredential` for automatic authentication
   - **In ADO pipeline**: Automatically uses UMI (no code changes needed)
   - **Locally**: Would use Azure CLI credentials (blocked by CA policy in your case)
   - Uploads HTML to `PR-{number}/report-{timestamp}.html`
   - Returns public blob URLs

4. **`requirements.txt`**
   - Added `azure-storage-blob>=12.19.0`
   - Updated `azure-identity>=1.15.0`

---

## 🔐 Authentication Strategy

### How It Works (No Code Changes Needed):

```python
# In BlobStorageClient.__init__()
self.credential = DefaultAzureCredential()
```

**`DefaultAzureCredential` automatically tries (in order)**:
1. **Environment variables** (AZURE_CLIENT_ID, etc.) - Not used in our setup
2. **Managed Identity** - ✅ **This is what ADO pipeline will use**
3. **Azure CLI** - What local dev would use (blocked by CA policy for you)
4. **Interactive browser** - Not available in pipeline

**In your ADO pipeline**:
- The agent pool `mariner-dev-build-1es-mariner2-amd64` has UMI assigned
- UMI Client ID: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
- UMI Principal ID: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
- When code runs on the agent, `DefaultAzureCredential` automatically detects and uses the UMI
- **No configuration needed in the pipeline YAML**

---

## ⚠️ REQUIRED: Admin Prerequisites

**Before deploying to production, an admin must complete these steps:**

### Step 1: Grant UMI Permissions
The UMI needs "Storage Blob Data Contributor" role on `radarblobstore`.

**Option A: Azure Portal** (Recommended)
1. Go to https://portal.azure.com
2. Navigate to **Storage accounts** → `radarblobstore`
3. Select **Access Control (IAM)** in left menu
4. Click **+ Add** → **Add role assignment**
5. **Role tab**: Select `Storage Blob Data Contributor`, click **Next**
6. **Members tab**:
   - Select **Managed identity**
   - Click **+ Select members**
   - Filter: **User-assigned managed identity**
   - Search: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
   - Select it and click **Select**
7. Click **Review + assign**

**Option B: Azure CLI**
```bash
az login
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"

az role assignment create \
  --assignee 4cb669bf-1ae6-463a-801a-2d491da37b9d \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"
```

**Verify**:
```bash
az role assignment list \
  --assignee 4cb669bf-1ae6-463a-801a-2d491da37b9d \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore" \
  --role "Storage Blob Data Contributor" \
  -o table
```

### Step 2: Configure Public Blob Access
HTML reports need to be publicly accessible.

**Option A: Azure Portal** (Recommended)
1. Go to https://portal.azure.com
2. Navigate to **Storage accounts** → `radarblobstore`
3. Select **Containers** in left menu
4. Find `radarcontainer` (create if doesn't exist)
5. Click on the container
6. Click **Change access level**
7. Select: **Blob (anonymous read access for blobs only)**
8. Click **OK**

**Option B: Azure CLI**
```bash
# Check if container exists
az storage container exists \
  --name radarcontainer \
  --account-name radarblobstore \
  --auth-mode login

# Create with public access (if doesn't exist)
az storage container create \
  --name radarcontainer \
  --account-name radarblobstore \
  --public-access blob \
  --auth-mode login

# Or update existing
az storage container set-permission \
  --name radarcontainer \
  --account-name radarblobstore \
  --public-access blob \
  --auth-mode login
```

---

## 🚀 Deployment Steps

### 1. Ensure Admin Prerequisites Are Complete
- [ ] UMI has "Storage Blob Data Contributor" role
- [ ] Container `radarcontainer` has blob-level public access

### 2. Verify Requirements Are Installed
The pipeline should already install packages from `requirements.txt`, but verify:

```bash
pip install -r requirements.txt
```

Should include:
- `azure-storage-blob>=12.19.0`
- `azure-identity>=1.15.0`

### 3. Deploy Code to Branch
```bash
# Commit the changes
git add CveSpecFilePRCheck.py ResultAnalyzer.py BlobStorageClient.py requirements.txt
git commit -m "Add Azure Blob Storage integration for HTML reports with UMI auth"

# Push to your branch
git push origin <your-branch-name>
```

### 4. Create Test PR
1. Create a test PR that modifies a spec file
2. Watch the pipeline run
3. Check pipeline logs for blob storage messages

### 5. Verify in Pipeline Logs
Look for these log messages:

**Success Path**:
```
INFO: Initialized BlobStorageClient for https://radarblobstore.blob.core.windows.net/radarcontainer
INFO: BlobStorageClient initialized successfully (will use UMI in pipeline)
INFO: Attempting to upload HTML report to Azure Blob Storage...
INFO: Uploading HTML report to blob: PR-12345/report-2025-10-15T203450Z.html
INFO: ✅ HTML report uploaded to blob storage: https://radarblobstore.blob.core.windows.net/radarcontainer/PR-12345/report-2025-10-15T203450Z.html
INFO: Added HTML report link to comment: https://radarblobstore.blob.core.windows.net/...
```

**Fallback Path (if blob fails)**:
```
WARNING: Failed to initialize BlobStorageClient, will fall back to Gist: <error>
INFO: Using Gist for HTML report (blob storage not available or failed)
INFO: ✅ HTML report uploaded to Gist: https://gist.github.com/...
```

### 6. Verify GitHub Comment
The PR comment should have:

```markdown
## 📊 Interactive HTML Report

### 🔗 **[CLICK HERE to open the Interactive HTML Report](https://radarblobstore.blob.core.windows.net/radarcontainer/PR-12345/report-2025-10-15T203450Z.html)**

*Opens in a new tab with full analysis details and interactive features*
```

### 7. Verify HTML Report is Publicly Accessible
- Click the link in the GitHub comment
- Should open the HTML report directly in browser
- No authentication should be required
- Report should display with dark theme and interactive features

---

## 🔧 Troubleshooting

### Issue: "Failed to initialize BlobStorageClient"

**Check**:
1. Are the required packages installed? (`azure-storage-blob`, `azure-identity`)
2. Is the storage account name correct? (`radarblobstore`)
3. Is the container name correct? (`radarcontainer`)

**Look for**:
```
ERROR: BlobStorageClient initialization failed: <specific error>
```

### Issue: "Access denied" or "401/403" errors

**Check**:
1. Did admin grant UMI the "Storage Blob Data Contributor" role?
2. Is the UMI assigned to the agent pool?
3. Is the subscription correct?

**Verify UMI assignment**:
```bash
az role assignment list \
  --assignee 4cb669bf-1ae6-463a-801a-2d491da37b9d \
  --all \
  -o table
```

### Issue: HTML URL not publicly accessible

**Check**:
1. Is blob-level public access enabled on `radarcontainer`?
2. Open Azure Portal → radarblobstore → radarcontainer → Properties
3. Should show "Public access level: Blob"

**Verify**:
```bash
az storage container show \
  --name radarcontainer \
  --account-name radarblobstore \
  --auth-mode login \
  --query publicAccess
```

Should return: `"blob"`

### Issue: "ManagedIdentityCredential authentication unavailable"

**This means**: UMI is not being detected

**Check**:
1. Is the pipeline running on the correct agent pool? (`mariner-dev-build-1es-mariner2-amd64`)
2. Is the UMI actually assigned to that agent pool?
3. Contact Azure DevOps admin to verify UMI configuration

### Issue: Falls back to Gist every time

**If blob storage consistently fails**, check:
1. Pipeline logs for specific error messages
2. Storage account firewall rules (should allow Azure services)
3. Network connectivity from agent pool to storage account

---

## 📊 Expected Blob Storage Structure

After successful runs, you should see this hierarchy in `radarcontainer`:

```
radarcontainer/
├── PR-12345/
│   ├── report-2025-10-15T120000Z.html
│   ├── report-2025-10-15T140000Z.html
│   └── report-2025-10-15T160000Z.html
├── PR-12346/
│   └── report-2025-10-15T130000Z.html
└── PR-12347/
    └── report-2025-10-15T150000Z.html
```

Each PR gets its own folder. Multiple runs create timestamped files.

**Public URL format**:
```
https://radarblobstore.blob.core.windows.net/radarcontainer/PR-{number}/report-{timestamp}.html
```

---

## 🎯 Success Criteria

Your deployment is successful when:

- ✅ Pipeline runs without errors
- ✅ Pipeline logs show "HTML report uploaded to blob storage"
- ✅ GitHub comment includes blob storage URL (not Gist URL)
- ✅ Clicking the link opens the HTML report
- ✅ HTML report is publicly accessible (no login required)
- ✅ Report displays correctly with dark theme
- ✅ Blob appears in Azure Portal under radarcontainer

---

## 🔄 Rollback Plan

If blob storage causes issues:

### Option 1: Disable Blob Storage (Keep Gist)
Comment out the blob storage initialization:

```python
# blob_storage_client = BlobStorageClient(...)
blob_storage_client = None
```

This will automatically fall back to Gist.

### Option 2: Revert Changes
```bash
git revert <commit-hash>
git push origin <branch-name>
```

The Gist integration remains functional as a fallback.

---

## 📝 Next Steps (Future Enhancements)

After successful HTML blob storage deployment:

1. **Analytics JSON Upload** (Phase 3B)
   - Design Power BI-optimized JSON schema
   - Upload analytics data to same PR folder
   - Structure: `PR-{number}/analysis-{timestamp}.json`

2. **Data Retention Policy**
   - Configure blob lifecycle management
   - Archive old reports to cool storage
   - Delete reports older than X days

3. **Power BI Dashboard**
   - Connect Power BI to blob storage
   - Query analytics JSON files
   - Build dashboards for trends

---

## 📞 Support

**For permission issues**: Contact Azure admin or subscription owner
**For UMI issues**: Contact Azure DevOps team managing the agent pool
**For code issues**: Check pipeline logs and file GitHub issue

---

## 📚 Related Documentation

- `MANUAL_ADMIN_STEPS.md` - Detailed admin instructions
- `LOCAL_DEV_STRATEGY.md` - Dual authentication explanation
- `PHASE3_PLAN.md` - Overall Phase 3 plan
- `BlobStorageClient.py` - Implementation details
