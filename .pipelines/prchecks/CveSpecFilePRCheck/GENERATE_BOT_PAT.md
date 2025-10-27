# Generate New GitHub PAT for CBL-Mariner-Bot

## Background
The current GitHub Personal Access Token (PAT) for the CBL-Mariner-Bot account has expired. This token is used by:
1. **Azure DevOps Pipeline** - To post initial antipattern detection comments on PRs
2. **Azure Function** - To add labels and post challenge-related updates

## Impact of Expired Token
- PR checks fail with `401 Bad credentials` errors
- No automated comments on PRs for antipattern detection
- RADAR system cannot post detection reports or labels

## Steps to Generate New PAT

### 1. Log into CBL-Mariner-Bot Account
- Go to https://github.com/login
- Sign in with CBL-Mariner-Bot credentials
- **Contact:** Team admin or whoever manages the bot account credentials

### 2. Navigate to PAT Settings
- Click on your profile picture (top-right corner)
- Go to **Settings** → **Developer settings** (bottom of left sidebar)
- Click **Personal access tokens** → **Tokens (classic)**
  - URL: https://github.com/settings/tokens

### 3. Generate New Token
Click **"Generate new token"** → **"Generate new token (classic)"**

### 4. Configure Token Settings

**Token Name:** (Recommended)
```
Azure DevOps Pipeline - PR Checks & RADAR
```

**Expiration:** (Choose one)
- ✅ **Recommended:** `No expiration` (for production stability)
- Alternative: `1 year` (requires annual renewal)

**Scopes:** (Select these checkboxes)
- ✅ **repo** (Full control of private repositories)
  - This includes:
    - `repo:status` - Commit status
    - `repo_deployment` - Deployment status
    - `public_repo` - Public repositories
    - `repo:invite` - Repository invitations
- ✅ **workflow** (Update GitHub Action workflows)

**Other scopes:** Leave unchecked

### 5. Generate and Copy Token
- Scroll to bottom and click **"Generate token"**
- ⚠️ **CRITICAL:** Copy the token immediately - you won't see it again!
- Token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (40 characters)

### 6. Verify Token (Optional but Recommended)
Test the token works:
```bash
curl -H "Authorization: token YOUR_NEW_TOKEN_HERE" https://api.github.com/user
```

Expected output:
```json
{
  "login": "CBL-Mariner-Bot",
  "type": "User",
  ...
}
```

If you see `"message": "Bad credentials"`, the token is invalid.

---

## Updating the Token in Azure

After generating the new token, it must be updated in **TWO** locations:

### Location 1: Azure Key Vault (for Azure Function)
**Key Vault Name:** `mariner-pipelines-kv`  
**Secret Name:** `cblmarghGithubPRPat`

**Update via Azure CLI:**
```bash
az keyvault secret set \
  --vault-name mariner-pipelines-kv \
  --name cblmarghGithubPRPat \
  --value "ghp_YOUR_NEW_TOKEN_HERE"
```

**Update via Azure Portal:**
1. Go to https://portal.azure.com
2. Search for `mariner-pipelines-kv`
3. Go to **Secrets** (left sidebar)
4. Click on `cblmarghGithubPRPat`
5. Click **"+ New Version"**
6. Paste new token value
7. Click **"Create"**

### Location 2: Azure DevOps Pipeline Variables (for PR Check Pipeline)

You need to update **BOTH** of these variables (they should have the same value):
- `cblmarghGithubPRPat`
- `githubPrPat`

**Update via Azure DevOps UI:**
1. Go to your Azure DevOps project
2. Navigate to **Pipelines** → **Library**
3. Find the variable group OR go to the specific pipeline settings
4. Update both variable values with the new token
5. ✅ Check "Keep this value secret" (lock icon)
6. Click **Save**

**Alternative: Update via Pipeline YAML (Not Recommended for Secrets)**
- Better to use UI to keep tokens encrypted

---

## Verification Steps

### 1. Verify Key Vault Update
```bash
az keyvault secret show \
  --vault-name mariner-pipelines-kv \
  --name cblmarghGithubPRPat \
  --query "value" -o tsv | head -c 10
```
Expected: `ghp_XXXXXX` (first 10 chars of new token)

### 2. Verify Azure Function
- Go to Azure Portal → Function App `radarfunc`
- The function will automatically pick up the new token from Key Vault
- No restart needed (uses DefaultAzureCredential)

### 3. Verify Pipeline
- Trigger a test PR check pipeline run
- Check logs for: `✅ GITHUB_TOKEN is set (prefix: ghp_XXXXXX...)`
- Verify the prefix matches your NEW token (not `ghp_4qL6t6...`)

### 4. End-to-End Test
- Create a test PR with an antipattern (e.g., far-future CVE year)
- Verify bot posts initial comment ✅
- Verify labels are added ✅
- Verify no 401 errors ❌

---

## Troubleshooting

### Issue: "Bad credentials" Error
**Cause:** Token may not be authorized for Microsoft organization

**Solution:**
1. Go to https://github.com/settings/tokens
2. Find your new token in the list
3. Click **"Configure SSO"** next to it
4. Click **"Authorize"** next to `microsoft` organization
5. Confirm authorization

### Issue: "Resource not found" Error
**Cause:** Missing required scopes

**Solution:**
- Regenerate token with `repo` and `workflow` scopes
- Delete old token to avoid confusion

### Issue: Pipeline still uses old token
**Cause:** Variable not updated in correct location

**Solution:**
- Check BOTH pipeline variables: `cblmarghGithubPRPat` AND `githubPrPat`
- Verify both have the NEW token value
- Check pipeline YAML uses correct variable name (line 120)

---

## Security Best Practices

✅ **DO:**
- Use "No expiration" for production stability
- Enable SSO authorization for Microsoft org
- Store in Key Vault (encrypted at rest)
- Mark as secret in Azure DevOps
- Document token purpose and location
- Test token before deploying

❌ **DON'T:**
- Commit token to git repository
- Share token in chat/email
- Use personal account token for bot operations
- Store in plain text files
- Reuse tokens across multiple systems

---

## Contact Information

**If you need help:**
- Primary contact: [Your team lead or admin name]
- Bot account owner: [Whoever manages CBL-Mariner-Bot credentials]
- Azure subscription owner: [Person with Key Vault access]

**Current Status (as of October 24, 2025):**
- ❌ Old token: `ghp_4qL6t6...` - EXPIRED
- ⏳ New token: Waiting for generation
- 🔄 Temporary workaround: Using personal token (not recommended for production)

---

## After Token Update

Once the new token is generated and deployed:

1. ✅ Test with a PR check run
2. ✅ Update this document with generation date
3. ✅ Set calendar reminder for renewal (if not "no expiration")
4. ✅ Delete old token from GitHub settings
5. ✅ Notify team that system is operational

**Generated by:** [Your name]  
**Date:** October 24, 2025  
**Last Updated:** October 24, 2025
