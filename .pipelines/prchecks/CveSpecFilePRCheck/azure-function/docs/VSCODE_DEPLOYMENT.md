# VS Code Deployment Steps for Azure Function

## ✅ Pre-requisites
- Azure Functions extension installed: ✅ INSTALLED
- Signed into Azure with ahmedbadawi@microsoft.com

## 🚀 Deployment Steps

### Method 1: Using Azure Functions Panel

1. **Open Azure Panel**:
   - Click the Azure icon (A) in the left sidebar
   - Or press: `Ctrl+Shift+A` (Linux)

2. **Navigate to Function Apps**:
   - In the Azure panel, expand "RESOURCES"
   - Expand your subscription: "EdgeOS_IoT_CBL-Mariner_DevTest"
   - You should see "Function App" section
   - Look for "radar-func"

3. **Deploy**:
   - Right-click on the `azure-function` folder in your Explorer
   - Select "Deploy to Function App..."
   - OR use Command Palette: `Ctrl+Shift+P` → "Azure Functions: Deploy to Function App..."

4. **Select Deployment Target**:
   - Choose subscription: "EdgeOS_IoT_CBL-Mariner_DevTest"
   - Choose function app: "radar-func"
   - Confirm: "Deploy" when prompted

5. **Monitor Deployment**:
   - Watch the OUTPUT panel (Azure Functions view)
   - Deployment takes 1-3 minutes
   - Look for "Deployment successful" message

### Method 2: Using Command Palette (Alternative)

1. **Open Command Palette**: `Ctrl+Shift+P`

2. **Run**: "Azure Functions: Deploy to Function App..."

3. **Follow prompts**:
   - Select folder: `azure-function`
   - Select subscription: "EdgeOS_IoT_CBL-Mariner_DevTest"
   - Select function app: "radar-func"
   - Confirm deployment

### Method 3: Using Azure Functions Panel Right-Click

1. **In Azure Panel**:
   - Expand: RESOURCES → EdgeOS_IoT_CBL-Mariner_DevTest → Function App
   - Right-click on "radar-func"
   - Select "Deploy to Function App..."
   - Choose the `azure-function` folder when prompted

## ✅ After Deployment

### 1. Verify Deployment
Once deployment completes, you'll see output like:
```
Deployment successful.
Functions in radar-func:
  challenge - [httpTrigger]
  health - [httpTrigger]
```

### 2. Enable CORS
**Via VS Code**:
1. In Azure panel, expand "radar-func"
2. Expand "Application Settings"
3. Right-click "Application Settings" → "Add New Setting..."
4. Name: `CORS_ALLOWED_ORIGINS`
5. Value: `https://radarblobstore.blob.core.windows.net`

**OR Via Azure Portal**:
1. Go to https://portal.azure.com
2. Navigate to Function App "radar-func"
3. Settings → CORS
4. Add: `https://radarblobstore.blob.core.windows.net`
5. Click Save

### 3. Test Endpoints

**Test Health Endpoint**:
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

**Test Challenge Endpoint**:
```bash
curl -X POST \
  https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "pr_number": 14877,
    "antipattern_id": "test-001",
    "challenge_type": "false-positive",
    "feedback_text": "Test challenge submission",
    "user_email": "ahmedbadawi@microsoft.com"
  }'
```

Expected response:
```json
{
  "success": true,
  "challenge_id": "ch-001",
  "message": "Challenge submitted successfully"
}
```

### 4. View Logs (Optional)

**Via VS Code**:
1. In Azure panel, right-click "radar-func"
2. Select "Start Streaming Logs"
3. Make a test request to see logs in real-time

**Via Portal**:
1. Go to Function App → Functions → challenge
2. Click "Monitor"
3. View invocation logs

## 🐛 Troubleshooting

### "No workspace folder open"
- Make sure you have `/home/abadawix/git/azurelinux` open as workspace
- The `azure-function` folder should be visible in Explorer

### "Failed to get site config"
- Sign out and sign in again in Azure panel
- Verify you have permissions on radar-func

### "Deployment failed"
- Check OUTPUT panel for detailed error
- Verify function.json is valid
- Try deploying again (sometimes transient issues)

### CORS errors after deployment
- Verify CORS is configured with exact origin
- Test with `curl` first (bypasses CORS)
- Check browser console for specific CORS error

## 📝 Next Steps After Successful Deployment

1. ✅ Verify both endpoints work with curl
2. ✅ Confirm CORS is configured
3. ✅ Move to implementing the analytics data schema
4. ✅ Create AnalyticsDataBuilder class
5. ✅ Build interactive HTML dashboard
6. ✅ Integrate JavaScript to call challenge endpoint
