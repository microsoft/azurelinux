# Phase 3 Setup - Quick Reference

## 🎯 Current Status

### Configuration (CONFIRMED)
- ✅ **UMI Client ID**: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
- ✅ **Storage Account**: `radarblobstore`
- ✅ **Container**: `radarcontainer`
- ✅ **Resource Group**: `Radar-Storage-RG`
- ✅ **Data Retention**: Indefinite
- ✅ **Analytics**: Power BI (agnostic design)

---

## 📝 Your Action Items

### Step 1: Verify UMI Permissions
```bash
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck
./verify-umi-permissions.sh
```

**This script will:**
- Look up the UMI
- Check if it has `Storage Blob Data Contributor` role
- Offer to grant permissions if missing
- Provide Azure Portal instructions

### Step 2: Configure Public Access
```bash
./configure-public-access.sh
```

**This script will:**
- Check if `radarcontainer` exists (create if needed)
- Enable blob-level public read access
- Confirm HTML reports will be publicly accessible

---

## 📊 Expected Outcomes

After running both scripts successfully:

✅ **UMI has permissions** to read/write blobs  
✅ **Container exists** with public read access  
✅ **HTML reports** will be accessible via URLs like:
```
https://radarblobstore.blob.core.windows.net/radarcontainer/PR-12345/report-2025-10-15T203450Z.html
```

---

## 🚀 Next Phase (After Scripts Succeed)

I will implement:
1. **BlobStorageClient.py** - UMI authentication, upload/download
2. **Analytics JSON Schema** - Power BI compatible structure
3. **AnalyticsDataBuilder** - Transform analysis results
4. **Integration** - Replace Gist with blob storage
5. **Testing** - Verify read/write functionality

---

## 🆘 Troubleshooting

### If verify-umi-permissions.sh fails:
- Check you're logged into correct Azure subscription: `az account show`
- Verify UMI exists: `az identity list | grep 7bf2e2c3`
- Check you have permissions to assign roles

### If configure-public-access.sh fails:
- Verify storage account exists: `az storage account show --name radarblobstore --resource-group Radar-Storage-RG`
- Check you have permissions on the storage account
- Try authenticating: `az login`

---

## 📞 What to Report Back

After running the scripts, please tell me:
1. ✅ "Both scripts succeeded" → I'll start implementation
2. ❌ "Script X failed with error Y" → I'll help troubleshoot

That's it! Run the scripts and let me know the results. 🎯
