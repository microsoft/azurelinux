# RADAR Label Workflow - Setup Instructions

## ✅ Completed Changes

### 1. Code Updates (Committed & Deployed)
- **GitHubClient.py**: Added `add_label()` method for consistent label management
- **CveSpecFilePRCheck.py**: Pipeline now adds `radar-issues-detected` label when posting PR check comments
- **function_app.py**: Azure Function now uses `GITHUB_TOKEN` (bot PAT) and adds `radar-acknowledged` label

### 2. Authentication Pattern
Following the same pattern as `GitHubClient`:
```python
# Both pipeline and Azure Function use GITHUB_TOKEN
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Use 'token' format for GitHub PATs (not 'Bearer')
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
```

### 3. Deployment Status
- ✅ Azure Function deployed successfully (radarfunc-labels.zip)
- ✅ Code committed to `abadawi/multi-spec-radar` branch
- ⏸️ Pending: Configure `GITHUB_TOKEN` environment variable

---

## 🔧 Required Configuration

### Step 1: Add GITHUB_TOKEN to Azure Function

The Azure Function needs the same bot PAT that the pipeline uses (`githubPrPat`).

**Option A: If you know the PAT value:**
```bash
az functionapp config appsettings set \
  --name radarfunc \
  --resource-group Radar-Storage-RG \
  --settings "GITHUB_TOKEN=<your_github_pat_here>"
```

**Option B: Retrieve from Azure DevOps Key Vault:**
The pipeline gets this from `$(githubPrPat)` variable. You may need to:
1. Check Azure DevOps variable groups for the PAT value
2. Or regenerate a new PAT from the CBL Mariner bot GitHub account

### Step 2: Create GitHub Labels

Create these 2 labels in the `microsoft/azurelinux` repository:

**Label 1: radar-issues-detected**
- Name: `radar-issues-detected`
- Description: `RADAR detected potential issues in this PR`
- Color: `#D73A4A` (red)

**Label 2: radar-acknowledged**
- Name: `radar-acknowledged`
- Description: `Feedback submitted for RADAR findings`
- Color: `#0E8A16` (green)

**How to create labels:**
1. Go to https://github.com/microsoft/azurelinux/labels
2. Click "New label"
3. Enter name, description, and color
4. Click "Create label"
5. Repeat for the second label

---

## 📋 Complete Workflow

### When Pipeline Detects Issues:
1. ✅ Pipeline runs CVE spec file check
2. ✅ If issues found (severity >= WARNING):
   - Posts comment to PR with findings
   - **Adds `radar-issues-detected` label**
3. ✅ Comment includes link to interactive HTML report (blob storage)

### When User Submits Challenge:
1. ✅ User opens HTML report, clicks "Challenge" button
2. ✅ User authenticates with GitHub OAuth
3. ✅ User fills out challenge form (False Alarm/Needs Context/Acknowledged)
4. ✅ Azure Function receives challenge:
   - Saves to analytics.json in blob storage
   - Posts comment to PR (using bot account with user attribution)
   - **Adds `radar-acknowledged` label**

### Label Benefits:
- **Filtering**: Easily find PRs with RADAR issues or feedback
- **Dashboards**: Track how many PRs have issues vs. acknowledged
- **Automation**: Could trigger additional workflows based on labels
- **Visibility**: Labels appear prominently in PR list and on the PR page

---

## 🧪 Testing Plan

### Test 1: Pipeline Label Addition
1. Push changes to `test/basic-antipatterns` branch
2. Pipeline should run and detect issues
3. Verify PR #14904 has:
   - Comment posted by CBL Mariner bot
   - `radar-issues-detected` label added

### Test 2: Challenge Label Addition
1. Open latest HTML report from blob storage
2. Submit a challenge for any finding
3. Verify PR #14904 has:
   - New comment posted by CBL Mariner bot (showing user attribution)
   - `radar-acknowledged` label added

### Test 3: End-to-End Workflow
1. Create fresh test PR with spec file changes
2. Pipeline runs → comment + `radar-issues-detected` label
3. Submit challenge → comment + `radar-acknowledged` label
4. Both labels visible on PR

---

## 📝 Next Steps

### Immediate (Required):
1. **Add GITHUB_TOKEN to Azure Function** (see Step 1 above)
2. **Create the 2 labels** in GitHub repository (see Step 2 above)
3. **Test the workflow** on PR #14904

### Future Enhancements:
- Add PR metadata to HTML reports (title, author, branches)
- Create dashboard to track challenge statistics
- Add webhook to notify team when challenges submitted
- Implement auto-close for PRs with all findings acknowledged

---

## 🔍 Troubleshooting

### If labels not added:
- Check function logs: `az functionapp logs tail --name radarfunc --resource-group Radar-Storage-RG`
- Verify `GITHUB_TOKEN` is configured: `az functionapp config appsettings list --name radarfunc --resource-group Radar-Storage-RG`
- Ensure labels exist in GitHub repository
- Check that bot PAT has `repo` scope permissions

### If comments not posted:
- Verify `GITHUB_TOKEN` has correct permissions
- Check bot account has write access to repository
- Review function logs for detailed error messages

---

## 📚 Files Changed

- `.pipelines/prchecks/CveSpecFilePRCheck/GitHubClient.py`
- `.pipelines/prchecks/CveSpecFilePRCheck/CveSpecFilePRCheck.py`
- `.pipelines/prchecks/CveSpecFilePRCheck/azure-function/function_app.py`

**Commit**: `d5ad71165` on `abadawi/multi-spec-radar` branch
**Deployment**: Successfully deployed to `radarfunc` Azure Function
