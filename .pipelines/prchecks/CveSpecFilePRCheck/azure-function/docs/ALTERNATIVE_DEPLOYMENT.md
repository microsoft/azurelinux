# Alternative Deployment Methods for radar-func

The function app appears to have network/deployment restrictions. Here are alternative methods:

## Method 1: App Service Editor (Portal - Easiest)

1. **Open App Service Editor**:
   - In Azure Portal, go to Function App `radar-func`
   - In left menu, go to **Development Tools** → **App Service Editor**
   - Click **"Go →"**
   
2. **Upload Files**:
   - You'll see a file explorer on the left
   - Extract the `function.zip` locally first:
     ```bash
     cd /tmp
     unzip /home/abadawix/git/azurelinux/.pipelines/prchecks/CveSpecFilePRCheck/azure-function/function.zip -d radar-func-deploy
     ```
   
3. **Copy Files**:
   - In App Service Editor, navigate to `/home/site/wwwroot/`
   - Upload these files from `/tmp/radar-func-deploy/`:
     - `function_app.py`
     - `host.json`
     - `requirements.txt`
   - The editor will auto-save

4. **Restart Function App**:
   - Go back to Function App overview
   - Click **"Restart"** at the top

## Method 2: Kudu Console (Most Reliable)

1. **Open Kudu**:
   - In Function App, go to **Development Tools** → **Advanced Tools**
   - Click **"Go"**
   - Opens: `https://radar-func-b5axhffvhgajbmhd.scm.azurewebsites.net`

2. **Use Debug Console**:
   - At top menu, click **Debug console** → **CMD**
   
3. **Navigate and Upload**:
   - In the console, type:
     ```
     cd site\wwwroot
     ```
   - Drag and drop these files into the file explorer pane:
     - `function_app.py`
     - `host.json`  
     - `requirements.txt`

4. **Install Dependencies**:
   - In the Kudu console, run:
     ```
     D:\home\python\python.exe -m pip install -r requirements.txt
     ```

5. **Restart**:
   - Function will auto-restart, or restart from portal

## Method 3: GitHub Actions (Best for CI/CD)

If you can commit the code to GitHub, we can set up automatic deployment:

1. **Create GitHub workflow file** at `.github/workflows/deploy-azure-function.yml`

2. **Get Publish Profile**:
   - In Function App, click **Get publish profile**
   - Copy the XML content
   - In GitHub repo, go to Settings → Secrets
   - Add secret: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`

3. **Push code and it will auto-deploy**

## Method 4: Request Access/Permissions

The 403 errors suggest:
- Network restrictions on the SCM site
- Or Conditional Access policies blocking deployments

**To fix**:
1. Go to Function App → **Configuration** → **General settings**
2. Find **SCM Basic Auth Publishing Credentials**
3. Set to **On**
4. Save and retry CLI deployment

Or ask your Azure admin to:
-Allow your IP for SCM site access
- Or temporarily disable Conditional Access for `*.scm.azurewebsites.net`

## 🎯 Recommended: Try Kudu Method (Method 2)

This bypasses most restrictions and usually works. Steps:

1. Navigate to: https://radar-func-b5axhffvhgajbmhd.scm.azurewebsites.net
2. Tools → Debug Console → CMD
3. `cd site\wwwroot`
4. Drag these 3 files from your local machine:
   - function_app.py
   - host.json
   - requirements.txt
5. Function will pick them up automatically

Let me know which method you'd like to try!
