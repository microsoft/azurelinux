# Manual Admin Steps Required - Azure Configuration

## Context
Local environment cannot complete UMI permission verification due to:
- Conditional Access Policy requiring interactive browser authentication
- Microsoft Graph API permissions not available in dev environment
- UMI is used by **Azure DevOps pipeline agents**, not local machines

## Required Manual Steps (Azure Admin)

### ✅ Subscription Confirmed
- **Subscription**: `EdgeOS_IoT_CBL-Mariner_DevTest`
- **Subscription ID**: `0012ca50-c773-43b2-80e2-f24b6377145c`

### ✅ UMI Confirmed
- **Client ID**: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
- **Principal ID**: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
- **Status**: UMI exists and is accessible

### ✅ Storage Account Confirmed
- **Storage Account**: `radarblobstore`
- **Resource Group**: `Radar-Storage-RG`
- **Resource ID**: `/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore`
- **Status**: Storage account exists

---

## ⚠️ STEP 1: Grant UMI Permissions (Azure Admin Required)

### Option A: Azure Portal (Recommended)
1. Go to: https://portal.azure.com
2. Navigate to **Storage accounts** → `radarblobstore`
3. In left menu, select **Access Control (IAM)**
4. Click **+ Add** → **Add role assignment**
5. **Role tab**: Select `Storage Blob Data Contributor`
6. Click **Next**
7. **Members tab**:
   - Select **Managed identity**
   - Click **+ Select members**
   - Filter: **User-assigned managed identity**
   - Search for Principal ID: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
   - Select it
   - Click **Select**
8. Click **Next** → **Review + assign**

### Option B: Azure CLI (Requires Admin Rights)
```bash
# Login as admin with appropriate permissions
az login

# Set subscription
az account set --subscription "EdgeOS_IoT_CBL-Mariner_DevTest"

# Grant permission
az role assignment create \
  --assignee 4cb669bf-1ae6-463a-801a-2d491da37b9d \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore"
```

### Verification
After granting permissions, verify with:
```bash
az role assignment list \
  --assignee 4cb669bf-1ae6-463a-801a-2d491da37b9d \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/Radar-Storage-RG/providers/Microsoft.Storage/storageAccounts/radarblobstore" \
  --role "Storage Blob Data Contributor" \
  -o table
```

---

## ⚠️ STEP 2: Configure Public Blob Access (Azure Admin Required)

### Option A: Azure Portal (Recommended)
1. Go to: https://portal.azure.com
2. Navigate to **Storage accounts** → `radarblobstore`
3. In left menu, select **Containers**
4. Find or create container: `radarcontainer`
5. If creating new:
   - Click **+ Container**
   - Name: `radarcontainer`
   - Public access level: **Blob (anonymous read access for blobs only)**
   - Click **Create**
6. If container exists:
   - Select `radarcontainer`
   - Click **Change access level**
   - Select: **Blob (anonymous read access for blobs only)**
   - Click **OK**

### Option B: Azure CLI (Requires Admin Rights)
```bash
# Check if container exists
az storage container exists \
  --name radarcontainer \
  --account-name radarblobstore \
  --auth-mode login

# Create container with public access (if doesn't exist)
az storage container create \
  --name radarcontainer \
  --account-name radarblobstore \
  --public-access blob \
  --auth-mode login

# Or update existing container
az storage container set-permission \
  --name radarcontainer \
  --account-name radarblobstore \
  --public-access blob \
  --auth-mode login
```

### Verification
HTML reports should be publicly accessible at URLs like:
```
https://radarblobstore.blob.core.windows.net/radarcontainer/PR-12345/report-2025-10-15T203450Z.html
```

---

## 📝 Status

- ✅ **Subscription**: Identified (`EdgeOS_IoT_CBL-Mariner_DevTest`)
- ✅ **UMI**: Found (Principal ID: `4cb669bf-1ae6-463a-801a-2d491da37b9d`)
- ✅ **Storage Account**: Exists (`radarblobstore`)
- ⏸️ **UMI Permissions**: Requires admin to grant
- ⏸️ **Public Access**: Requires admin to configure

---

## 🚀 Next Steps

### For Azure Admin:
1. Complete STEP 1: Grant UMI permissions
2. Complete STEP 2: Configure public blob access
3. Notify developer when complete

### For Developer (After Admin Completes Steps):
1. Implement `BlobStorageClient.py`
2. Create analytics JSON schema
3. Integrate with pipeline
4. Test end-to-end in pipeline (UMI auth will work automatically)

---

## ⚡ Important Notes

- **UMI authentication only works in Azure DevOps pipeline**, not locally
- `DefaultAzureCredential` will automatically use UMI when code runs on agent pool
- Local testing of blob storage requires different credentials (e.g., Azure CLI login)
- Once permissions are granted, no code changes needed - it just works™

---

## 📞 Who to Contact

For permission grants, contact your Azure subscription admin or:
- Azure DevOps team managing the `mariner-dev-build-1es-mariner2-amd64` agent pool
- Azure resource group owner for `Radar-Storage-RG`
