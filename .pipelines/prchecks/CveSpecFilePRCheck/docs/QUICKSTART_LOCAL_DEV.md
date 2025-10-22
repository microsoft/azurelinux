# Quick Start - Local Development Setup

## 🎯 TL;DR - Run These Commands Now

```bash
# 1. Grant yourself blob storage permissions (one-time setup)
az login
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"
USER_OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)
az role assignment create \
  --assignee $USER_OBJECT_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"

# 2. Install Python packages
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck
pip install -r requirements.txt

# 3. Test blob storage connection
python BlobStorageClient.py
```

## ✅ Expected Output

```
INFO - Initialized BlobStorageClient for https://radarblobstore.blob.core.windows.net/radarcontainer
INFO - Testing blob storage connection and permissions...
INFO - ✅ Successfully connected to container: radarcontainer
INFO - Uploading HTML report to blob: PR-99999/report-2025-10-15T...
INFO - ✅ HTML report uploaded successfully: https://radarblobstore.blob.core.windows.net/...
INFO - Uploading JSON data to blob: PR-99999/analysis-2025-10-15T...
INFO - ✅ JSON data uploaded successfully: https://radarblobstore.blob.core.windows.net/...
✅ Blob storage connection test passed!
```

## 🔍 What Just Happened?

1. **Granted yourself permissions** - Your Microsoft account now has blob storage access
2. **DefaultAzureCredential detected Azure CLI** - Used your `az login` credentials automatically
3. **Uploaded test blobs** - Created test HTML and JSON in blob storage
4. **Generated public URLs** - Blobs are publicly accessible

## 🚀 Next Steps

See `LOCAL_DEV_STRATEGY.md` for complete development workflow.

## ❓ Troubleshooting

### "ERROR: Access has been blocked by conditional access"
- Try: `az login --scope https://graph.microsoft.com//.default`
- Or: Use Azure Portal to grant permissions manually

### "ERROR: The specified resource does not exist"
- Check subscription: `az account show`
- Verify storage account exists: `az storage account show --name radarblobstore --resource-group Radar-Storage-RG`

### "ERROR: Permission denied"
- Wait 1-2 minutes for role assignment to propagate
- Verify: `az role assignment list --assignee $(az ad signed-in-user show --query id -o tsv) --scope /subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c`

## 📝 Important Notes

- ✅ **Same code works in pipeline** - DefaultAzureCredential will use UMI automatically
- ✅ **No secrets needed** - Uses your Azure login
- ✅ **Safe for development** - Your account already has subscription access
- ✅ **Can be revoked later** - Remove role assignment when done developing

---

**Ready to develop! 🎉**
