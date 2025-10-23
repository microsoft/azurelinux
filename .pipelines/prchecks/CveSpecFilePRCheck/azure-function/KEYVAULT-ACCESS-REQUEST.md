# Key Vault Access Request for Azure Function

## Summary
The `radarfunc` Azure Function needs to read the GitHub PAT from Key Vault to post PR comments securely.

## Current Configuration
✅ **Azure Function**: `radarfunc` (Radar-Storage-RG)
✅ **User-Assigned Managed Identity**: `cblmargh-identity` 
   - Client ID: `7bf2e2c3-009a-460e-90d4-eff987a8d71d`
   - Principal ID: `4cb669bf-1ae6-463a-801a-2d491da37b9d`
✅ **Key Vault Reference Configured**: 
   ```
   GITHUB_TOKEN=@Microsoft.KeyVault(SecretUri=https://mariner-pipelines-kv.vault.azure.net/secrets/cblmarghGithubPRPat/)
   ```

## Required Action
⏳ **Grant RBAC Permission** to allow the UMI to read secrets from Key Vault.

### Command to Run:
```bash
az role assignment create \
  --assignee 7bf2e2c3-009a-460e-90d4-eff987a8d71d \
  --role "Key Vault Secrets User" \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/MarinerPipelines_RG/providers/Microsoft.KeyVault/vaults/mariner-pipelines-kv"
```

### Who Can Run This:
- User with **Owner** or **User Access Administrator** role on:
  - The `mariner-pipelines-kv` Key Vault, OR
  - The `MarinerPipelines_RG` resource group, OR
  - The subscription

### Why This Is Needed:
1. The Azure Function posts GitHub comments when users submit challenge feedback
2. It needs the GitHub PAT to authenticate with GitHub API
3. Storing PAT in Key Vault (vs app settings) is more secure:
   - No plaintext secrets in configuration
   - Automatic rotation support
   - Centralized secret management
   - Audit trail of secret access

### Verification After Granting Access:
Check if the permission was granted:
```bash
az role assignment list \
  --assignee 7bf2e2c3-009a-460e-90d4-eff987a8d71d \
  --scope "/subscriptions/0012ca50-c773-43b2-80e2-f24b6377145c/resourceGroups/MarinerPipelines_RG/providers/Microsoft.KeyVault/vaults/mariner-pipelines-kv"
```

Test if the function can resolve the Key Vault reference:
```bash
# Restart the function to pick up the permission
az functionapp restart --name radarfunc --resource-group Radar-Storage-RG

# Check function logs for any Key Vault access errors
az functionapp log tail --name radarfunc --resource-group Radar-Storage-RG
```

---

## Context
- **Pipeline**: Already uses this same UMI and Key Vault secret successfully
- **Function**: Shares the same infrastructure pattern for consistency
- **Security**: Follows Azure best practices for secret management
