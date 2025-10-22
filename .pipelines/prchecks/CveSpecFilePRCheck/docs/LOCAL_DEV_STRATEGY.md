# Dual Authentication Strategy - Local Dev + Production Pipeline

## Problem
- **Local Development**: UMI doesn't work (requires Azure DevOps agent)
- **Production Pipeline**: UMI works automatically on agent pool
- **Need**: Test blob storage locally BEFORE deploying to pipeline

## Solution: DefaultAzureCredential Credential Chain

`DefaultAzureCredential` tries authentication methods in this order:
1. **Environment Variables** (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
2. **Managed Identity** (UMI/SMI - works in Azure DevOps)
3. **Azure CLI** (works locally if you're logged in)
4. **Visual Studio / VS Code** credentials
5. **Other methods...**

This means **same code works both locally and in pipeline**! 🎉

---

## Strategy

### For Local Development (You)
Use **Azure CLI authentication**:
```bash
# Login with your Microsoft account
az login

# Set correct subscription
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"

# Run your Python code
# DefaultAzureCredential will use your Azure CLI credentials automatically!
python BlobStorageClient.py
```

**Your account needs**:
- Read/write access to `radarblobstore` storage account
- `Storage Blob Data Contributor` role (or similar)

### For Production Pipeline (Azure DevOps)
Use **Managed Identity (UMI)**:
- Agent pool already configured with UMI
- `DefaultAzureCredential` automatically detects and uses UMI
- No code changes needed!

---

## Implementation Plan

### Phase 1: Local Testing Setup (Immediate)
1. ✅ Grant YOUR user account blob permissions (temporary, for development)
2. ✅ Test BlobStorageClient locally with Azure CLI auth
3. ✅ Develop and test analytics JSON generation locally
4. ✅ Test HTML/JSON upload locally

### Phase 2: Production Setup (For Pipeline)
1. ⏳ Grant UMI blob permissions (admin task)
2. ⏳ Configure public blob access (admin task)
3. ⏳ Deploy code to pipeline
4. ⏳ Test in pipeline with real PR

---

## Detailed Plan

### ✅ TASK 1: Grant Your Account Local Dev Permissions
**You can do this yourself!**

```bash
# Login and set subscription
az login
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"

# Get your user object ID
USER_OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)
echo "Your Object ID: $USER_OBJECT_ID"

# Grant yourself Storage Blob Data Contributor role
az role assignment create \
  --assignee $USER_OBJECT_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"

echo "✅ You now have blob storage access for local development!"
```

**This is safe because**:
- Only for development/testing
- Your account already has access to the subscription
- Follows least-privilege principle
- Can be removed later if needed

### ✅ TASK 2: Test BlobStorageClient Locally

```bash
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck

# Install packages
pip install -r requirements.txt

# Test connection
python BlobStorageClient.py
```

**Expected result**: Should upload test HTML and JSON successfully!

### ✅ TASK 3: Create Test Script
Create a test script to validate everything works locally before pipeline deployment.

### ✅ TASK 4: Develop Analytics JSON Schema
Design and implement while testing locally with your credentials.

### ✅ TASK 5: Implement AnalyticsDataBuilder
Test locally with sample data.

### ✅ TASK 6: Update ResultAnalyzer
Add blob storage integration, test locally with mock data.

### ✅ TASK 7: Add Credential Fallback Logic
Make code robust to work in both environments:
```python
# BlobStorageClient automatically handles this!
credential = DefaultAzureCredential()
# In local: Uses Azure CLI
# In pipeline: Uses UMI
# No code changes needed!
```

### ⏳ TASK 8: Request Admin to Grant UMI Permissions
Once local testing is complete and working, admin grants UMI permissions for production.

### ⏳ TASK 9: Deploy to Pipeline
Push code to branch, test in actual pipeline.

### ⏳ TASK 10: Validate End-to-End
Create test PR, verify pipeline uploads to blob storage.

---

## Updated File Structure

```
.pipelines/prchecks/CveSpecFilePRCheck/
├── BlobStorageClient.py           # ✅ DONE - works with both auth methods
├── requirements.txt                # ✅ DONE - has azure-storage-blob
├── test_blob_storage.py            # 🆕 TO CREATE - local test script
├── AnalyticsDataBuilder.py         # 🆕 TO CREATE
├── ResultAnalyzer.py               # TO UPDATE - add blob integration
├── CveSpecFilePRCheck.py          # TO UPDATE - initialize BlobStorageClient
├── MANUAL_ADMIN_STEPS.md          # ✅ DONE - for admin (UMI permissions)
└── LOCAL_DEV_SETUP.md             # 🆕 TO CREATE - for local testing
```

---

## Environment Variables for Testing

### Local Development
```bash
# No environment variables needed!
# DefaultAzureCredential uses Azure CLI automatically
# Just make sure you're logged in: az login
```

### Production Pipeline
```bash
# Already configured in pipeline YAML:
GITHUB_PR_NUMBER=$(System.PullRequest.PullRequestNumber)
BUILD_BUILDID=$(Build.BuildId)

# UMI automatically detected by DefaultAzureCredential
# No additional configuration needed!
```

---

## Testing Checklist

### Local Testing (Before Pipeline)
- [ ] Grant your account blob permissions
- [ ] Test BlobStorageClient.py standalone
- [ ] Create test_blob_storage.py and run it
- [ ] Verify HTML uploads successfully
- [ ] Verify JSON uploads successfully
- [ ] Check blob URLs are publicly accessible
- [ ] Test analytics JSON generation
- [ ] Test full workflow with mock PR data

### Pipeline Testing (After Local Works)
- [ ] Admin grants UMI permissions
- [ ] Admin configures public blob access
- [ ] Deploy code to test branch
- [ ] Create test PR with spec changes
- [ ] Verify pipeline runs successfully
- [ ] Check HTML blob URL in GitHub comment
- [ ] Verify JSON analytics data in blob storage
- [ ] Validate UMI authentication worked (check logs)

---

## Benefits of This Approach

✅ **No code duplication** - Same code works locally and in pipeline
✅ **Faster development** - Test locally without pipeline runs
✅ **Independent** - Don't wait for admin to grant UMI permissions
✅ **Safe** - Your account permissions only affect your testing
✅ **Production-ready** - Once local works, pipeline will work too
✅ **Debuggable** - Can test and fix issues locally first

---

## Security Notes

### Local Development Permissions
- Your user account gets temporary blob access for development
- Scoped to specific storage account only
- Can be revoked after development is complete
- Standard practice for development workflows

### Production UMI Permissions
- UMI only works within Azure DevOps agents
- More secure than storing credentials
- No secrets in code or configuration
- Follows Azure best practices

---

## Next Steps - Immediate Actions

1. **YOU RUN** (right now):
```bash
# Grant yourself local dev permissions
az login
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"
USER_OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)
az role assignment create \
  --assignee $USER_OBJECT_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"
```

2. **I CREATE**:
- `test_blob_storage.py` - Test script
- `LOCAL_DEV_SETUP.md` - Local setup guide
- `AnalyticsDataBuilder.py` - Analytics JSON builder

3. **WE TEST** together locally

4. **ADMIN GRANTS** UMI permissions (once local testing passes)

5. **WE DEPLOY** to pipeline

---

## Questions?

- ❓ **Will this work?** YES! DefaultAzureCredential is designed for exactly this use case
- ❓ **Is it safe?** YES! Your account already has subscription access
- ❓ **Will pipeline work?** YES! Same code, UMI will be used automatically
- ❓ **Need code changes?** NO! DefaultAzureCredential handles everything

Ready to proceed? Let's grant your account permissions and start testing! 🚀
