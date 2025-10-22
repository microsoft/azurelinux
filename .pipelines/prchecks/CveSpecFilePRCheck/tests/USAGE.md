# Test Suite Usage Guide

## Quick Start

### Test Individual Categories

```bash
cd /path/to/azurelinux

# Test 1: Basic Anti-Patterns
git checkout -b test/basic-antipatterns
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-01-basic-antipatterns.patch
git add SPECS/curl/
git commit -m "test: basic anti-pattern detection in curl.spec"
git push origin test/basic-antipatterns
gh pr create --base abadawi/multi-spec-radar --title "Test: Basic Anti-Patterns"

# Test 2: Macro Expansion
git checkout abadawi/sim_7
git checkout -b test/macro-expansion
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-02-macro-expansion.patch
git add SPECS/python-tomli/
git commit -m "test: macro expansion in CVE detection (python-tomli.spec)"
git push origin test/macro-expansion
gh pr create --base abadawi/multi-spec-radar --title "Test: Macro Expansion"

# Test 3: Unused Patch Files
git checkout abadawi/sim_7
git checkout -b test/unused-patches
bash .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-03-unused-patches/apply.sh
git add SPECS/azcopy/
git commit -m "test: unused patch file detection (azcopy)"
git push origin test/unused-patches
gh pr create --base abadawi/multi-spec-radar --title "Test: Unused Patches"

# Test 4: Changelog Issues
git checkout abadawi/sim_7
git checkout -b test/changelog-issues
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-04-changelog-issues.patch
git add SPECS/curl/
git commit -m "test: changelog format validation (curl.spec)"
git push origin test/changelog-issues
gh pr create --base abadawi/multi-spec-radar --title "Test: Changelog Issues"

# Test 5: Edge Cases
git checkout abadawi/sim_7
git checkout -b test/edge-cases
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-05-edge-cases.patch
git add SPECS/openssl/
git commit -m "test: edge case handling (openssl.spec)"
git push origin test/edge-cases
gh pr create --base abadawi/multi-spec-radar --title "Test: Edge Cases"
```

### Comprehensive Test (All Categories)

```bash
cd /path/to/azurelinux
git checkout -b test/comprehensive

# Apply all patches
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-01-basic-antipatterns.patch
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-02-macro-expansion.patch
bash .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-03-unused-patches/apply.sh
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-04-changelog-issues.patch
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-05-edge-cases.patch

# Commit all changes
git add SPECS/
git commit -m "test: comprehensive PR check validation (all anti-patterns)"
git push origin test/comprehensive

# Create PR
gh pr create --base abadawi/multi-spec-radar \
  --title "Test: Comprehensive Anti-Pattern Detection" \
  --body "Testing all 11 anti-pattern types across 4 spec files"
```

## What Happens Next

1. **Pipeline Triggers**: CveSpecFilePRCheck.yaml detects modified .spec files
2. **Analysis Runs**: Anti-pattern detector scans each modified spec
3. **Macros Expanded**: `%{cve_base}`, `%{cve_year}`, etc. are resolved
4. **Findings Generated**: All anti-patterns documented
5. **HTML Report**: Generated and uploaded to Azure Blob Storage
6. **GitHub Comment**: Posted to PR with blob URL

## Accessing HTML Report

```bash
# After PR creation, check GitHub comment for blob URL:
# https://radarblobstore.blob.core.windows.net/radarcontainer/PR-{number}/index.html

# Or construct URL manually:
PR_NUM=123  # Your PR number
echo "https://radarblobstore.blob.core.windows.net/radarcontainer/PR-${PR_NUM}/index.html"
```

## Testing OAuth Flow

1. **Open HTML report** in browser
2. **Click "Sign in with GitHub"**
3. **Authorize OAuth app** (first time only)
4. **Verify authentication**:
   - Username displayed
   - Role badge shown (PR Owner/Collaborator/Admin)
5. **Submit challenges**:
   - Click "Challenge" on any finding
   - Select response type (Agree/False alarm/Needs context)
   - Add explanation
   - Submit
6. **Verify GitHub integration**:
   - Check PR for new comment from bot
   - Verify label `radar:findings-addressed` applied
7. **Test multiple challenges**:
   - Challenge different finding types
   - Verify all posted to GitHub
   - Check analytics.json updated

## Cleanup

### After Testing Individual Category

```bash
# Revert changes to specific spec
git checkout HEAD -- SPECS/curl/curl.spec

# Or delete branch
git checkout abadawi/sim_7
git branch -D test/basic-antipatterns
git push origin --delete test/basic-antipatterns
```

### After Comprehensive Test

```bash
# Revert all SPECS changes
git checkout HEAD -- SPECS/

# Or reset entire branch
git checkout abadawi/sim_7
git branch -D test/comprehensive
git push origin --delete test/comprehensive
```

## Troubleshooting

### Patch Doesn't Apply

```bash
# Check if you're on correct branch
git branch --show-current  # Should be a test branch

# Check if SPECS files match expected state
git status

# Try manual edit if patch fails
# Edit the spec file directly following the patch instructions
```

### Pipeline Doesn't Trigger

- Ensure .spec files in SPECS/ directory were modified
- Check that PR targets correct branch (multi-spec-radar)
- Verify pipeline file exists: `.pipelines/prchecks/CveSpecFilePRCheck.yaml`

### No Findings in Report

- Check spec file actually has the anti-patterns
- Verify macros expanded correctly (check logs)
- Ensure patch files created/missing as expected

### OAuth Doesn't Work

- Check GitHub OAuth App settings
- Verify Azure Function is running
- Check browser console for errors
- Ensure GITHUB_CLIENT_ID in HTML matches OAuth app

## Expected Results by Test

### Test 1: Basic Anti-Patterns (curl.spec)

**Expected Findings**: 10 total
- ❌ ERROR (7): Missing patch files Patch3-5, Patch6, Patch9, Patch10
- ❌ ERROR (1): Future-dated CVE-2035-11111
- ❌ ERROR (1): Invalid CVE format CVE-202X-INVALID
- ❌ ERROR (1): CVE-2025-99999 not in changelog
- ⚠️ WARNING (1): Duplicate CVE-2025-0665 (Patch0 and Patch7)
- ⚠️ WARNING (1): Patch without CVE reference: security-hardening-fix.patch

### Test 2: Macro Expansion (python-tomli.spec)

**Expected Findings**: 4 total
- ❌ ERROR (3): Missing patch files (all 3 patches)
- ❌ ERROR (1): Future-dated CVE-2035-99999 (from macro `%{future_year}`)
- ✅ Correctly expanded: `CVE-2025-12345` from `%{cve_base}%{cve_year}-%{security_patch_num}`

### Test 3: Unused Patches (azcopy.spec)

**Expected Findings**: 2 total
- ⚠️ WARNING (1): Unused orphaned-security-fix.patch
- ⚠️ WARNING (1): Unused CVE-2024-77777-unused.patch

### Test 4: Changelog Issues (curl.spec)

**Expected Findings**: 2 total
- ❌ ERROR (1): Missing Patch11 file
- ⚠️ WARNING (1): Invalid changelog format ("Applied CVE-2025-88888 fix" - missing dash)

### Test 5: Edge Cases (openssl.spec)

**Expected Findings**: 5 total
- ❌ ERROR (5): Missing patch files Patch100-104
- ✅ Correctly normalized: `cve-2024-11111.patch` → `CVE-2024-11111`
- ✅ Correctly handled: Leading zeros in CVE-2024-00999
- ✅ Correctly accepted: CVE-1999-00001 (valid old CVE)
- ✅ Correctly extracted: Multiple CVEs from Patch104

## Files Modified by Each Test

| Test | Modified Specs | New Files Created | Unchanged |
|------|---------------|-------------------|-----------|
| Test 1 | curl.spec | None | All other specs |
| Test 2 | python-tomli.spec | None | All other specs |
| Test 3 | None | azcopy/*.patch (2 files) | All specs |
| Test 4 | curl.spec | None | All other specs |
| Test 5 | openssl.spec | None | All other specs |
| Comprehensive | curl, python-tomli, openssl | azcopy/*.patch | All others |

## Validation Checklist

After running tests, verify:

- [ ] All expected specs appear in HTML report
- [ ] Finding counts match expected results
- [ ] Macros show expanded form (not `%{...}` in report)
- [ ] CVE IDs normalized to uppercase
- [ ] Future-dated CVEs flagged
- [ ] Duplicate CVEs detected
- [ ] Unused patches reported
- [ ] Changelog format issues caught
- [ ] OAuth sign-in successful
- [ ] Role badge displays correctly
- [ ] Challenge submission works
- [ ] GitHub comment posted
- [ ] Label applied to PR
- [ ] analytics.json updated

---

**Pro Tip**: Start with Test 1 (basic) to validate the core functionality, then proceed to Test 2 (macros) to verify expansion logic works correctly.
