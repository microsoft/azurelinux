# Azure Function Manual Deployment Guide

## 🚀 Deploy via Azure Portal (Recommended - No CLI Issues)

### Step 1: Prepare Deployment Package ✅ DONE
The `function.zip` file is already created and ready in the `azure-function` folder.

### Step 2: Deploy via Azure Portal

1. **Open Azure Portal**:
   - Go to: https://portal.azure.com
   - Sign in with `ahmedbadawi@microsoft.com`

2. **Navigate to Function App**:
   - In the search bar at top, type: `radar-func`
   - Click on the Function App: `radar-func`

3. **Open Deployment Center**:
   - In the left menu, scroll down to **Deployment**
   - Click **Deployment Center**

4. **Choose ZIP Deploy Method**:
   - At the top, you'll see tabs
   - Look for **"Manual deployment (push)"** or **"ZIP Deploy"** option
   - Or click on the **"FTPS credentials"** tab to see ZIP deploy option

5. **Upload ZIP File**:
   - Click **"Browse"** or **"Choose file"**
   - Navigate to: `/home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function/`
   - Select: `function.zip`
   - Click **"Upload"** or **"Deploy"**

6. **Wait for Deployment**:
   - A notification will show deployment progress
   - Takes 1-3 minutes
   - You'll see "Deployment succeeded" when done

### Alternative: Use Advanced Tools (Kudu)

1. **Open Advanced Tools**:
   - In Function App, go to **Development Tools** → **Advanced Tools**
   - Click **"Go"** - this opens Kudu console
   - Or directly visit: `https://radar-func-b5axhffvhgajbmhd.scm.azurewebsites.net`

2. **Deploy via Kudu**:
   - In Kudu, click **Tools** → **ZIP Push Deploy**
   - Drag and drop `function.zip` onto the `/wwwroot` drop zone
   - Wait for extraction to complete

### Step 3: Verify Deployment

Once deployment completes:

1. **Check Functions**:
   - In Azure Portal, go to Function App → **Functions**
   - You should see:
     - ✅ `challenge` - HTTP Trigger
     - ✅ `health` - HTTP Trigger

2. **Test Health Endpoint**:
   - In Functions, click `health`
   - Click **"Get Function URL"**
   - Click **"Copy"**
   - Open in browser or use curl:
   ```bash
   curl https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health
   ```

### Step 4: Enable CORS

1. **In Function App**:
   - Go to **Settings** → **CORS**

2. **Add Allowed Origin**:
   - In the text box, enter: `https://radarblobstore.blob.core.windows.net`
   - Click **"Save"** at the top

3. **Verify CORS**:
   - Should see the blob storage URL in the allowed origins list

### Step 5: Test Complete Setup

Run the configuration script:
```bash
cd /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function
./configure-function.sh
```

Or test manually:
```bash
# Test health
curl https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/health

# Test challenge
curl -X POST \
  https://radar-func-b5axhffvhgajbmhd.canadacentral-01.azurewebsites.net/api/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "pr_number": 14877,
    "antipattern_id": "test-001",
    "challenge_type": "false-positive",
    "feedback_text": "Test",
    "user_email": "ahmedbadawi@microsoft.com"
  }'
```

## ✅ Success Criteria

After deployment, you should see:

1. **Health endpoint returns**:
```json
{
  "status": "healthy",
  "service": "RADAR Challenge Handler",
  "timestamp": "2025-10-16T..."
}
```

2. **Challenge endpoint returns**:
```json
{
  "success": true,
  "challenge_id": "ch-001",
  "message": "Challenge submitted successfully"
}
```

## 🐛 Troubleshooting

### Can't find ZIP Deploy option
- Try: Deployment → Deployment Center → Manual Deployment tab
- Or use Kudu (Advanced Tools method above)

### Deployment fails with error
- Check Application Insights logs
- Verify UMI is assigned (should be ✅)
- Check that Python runtime is set to 3.11

### Functions not visible after deployment
- Wait 1-2 minutes for app to restart
- Refresh the Functions page
- Check Deployment Center logs for errors

### CORS not saving
- Verify you're in the CORS settings (not API CORS)
- Remove any default localhost entries if needed
- Click Save and wait for confirmation

## 📝 Next Steps

After successful deployment:
1. ✅ Test both endpoints work
2. ✅ Confirm CORS is configured
3. ✅ Move on to implementing analytics data schema
4. ✅ Build interactive HTML dashboard
5. ✅ Integrate JavaScript to call challenge endpoint
