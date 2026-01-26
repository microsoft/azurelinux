# RADAR Label Management Specification

## Overview

The RADAR system uses GitHub labels to track the lifecycle of detected antipatterns in Pull Requests. Labels are automatically managed by both the **Pipeline** (on new commits) and the **Azure Function** (when users submit challenges).

## Label Types

### `radar-issues-detected` 🔴
**Meaning**: PR has unchallenged antipattern issues that require attention.

**When Applied**:
- Pipeline detects antipatterns in the PR
- At least one issue remains unchallenged

**When Removed**:
- All detected issues have been challenged by the PR author
- A new commit resolves all antipattern issues

---

### `radar-acknowledged` 🟡  
**Meaning**: All detected issues have been acknowledged/challenged by the PR author.

**When Applied**:
- All issues in `issue_lifecycle` have `status: "challenged"`
- Can be applied by either Pipeline or Azure Function

**When Removed**:
- A new commit introduces new unchallenged issues
- A new commit with no issues (transitions to `radar-issues-resolved`)

---

### `radar-issues-resolved` 🟢
**Meaning**: All previously detected issues have been fixed/removed.

**When Applied**:
- A new commit is pushed with NO antipattern issues detected
- Only applied if there were previously detected issues

**When Removed**:
- A new commit reintroduces antipattern issues

---

## Label State Machine

```
[Initial PR] 
    ↓ (issues detected)
[radar-issues-detected]
    ↓ (all issues challenged)
[radar-acknowledged]
    ↓ (new commit fixes all issues)
[radar-issues-resolved]
    ↓ (new commit adds issues)
[radar-issues-detected]
```

### Detailed State Transitions

#### State 1: `radar-issues-detected`
**Condition**: `unchallenged_issues > 0`

**Actions**:
- Pipeline: Remove all other radar labels, add `radar-issues-detected`
- Azure Function: Keep `radar-issues-detected` unless all issues challenged

**Transitions**:
- → `radar-acknowledged` when user challenges all issues
- → `radar-issues-resolved` when new commit has 0 issues

---

#### State 2: `radar-acknowledged`  
**Condition**: `total_issues > 0 AND unchallenged_issues == 0`

**Actions**:
- Pipeline: Remove all other radar labels, add `radar-acknowledged`  
- Azure Function: Remove `radar-issues-detected`, add `radar-acknowledged`

**Transitions**:
- → `radar-issues-detected` when new commit adds unchallenged issues
- → `radar-issues-resolved` when new commit has 0 issues
- → Stays `radar-acknowledged` when new commit only has previously challenged issues

---

#### State 3: `radar-issues-resolved`
**Condition**: `total_issues == 0 AND previously_had_issues == true`

**Actions**:
- Pipeline: Remove all other radar labels, add `radar-issues-resolved`

**Transitions**:
- → `radar-issues-detected` when new commit introduces issues

---

## Implementation Details

### Data Source: `issue_lifecycle`

Both Pipeline and Azure Function MUST use the **same data source** for consistency:

```json
{
  "issue_lifecycle": {
    "nginx-CVE-2025-11111-missing-patch-file": {
      "first_detected": "abc123",
      "last_detected": "def456",
      "status": "active",          // or "challenged"
      "challenge_id": "ch-001"      // null if not challenged
    }
  }
}
```

### Counting Logic

**Total Issues**:
```python
total_issues = len(issue_lifecycle)
```

**Challenged Issues**:
```python
challenged_issues = sum(1 for issue in issue_lifecycle.values() 
                        if issue.get("status") == "challenged")
```

**Unchallenged Issues**:
```python
unchallenged_issues = total_issues - challenged_issues
```

---

## Actor Responsibilities

### Pipeline (on new commit)

**Responsibilities**:
1. Analyze changed spec files for antipatterns
2. Update `issue_lifecycle` with newly detected issues
3. Mark resolved issues (not detected in current commit)
4. Calculate label state from **entire `issue_lifecycle`**, not just current commit
5. Remove all radar labels and apply appropriate one

**Critical**: Pipeline MUST count ALL issues in `issue_lifecycle`, including:
- Issues from current commit
- Issues from previous commits still present
- Previously challenged issues still in codebase

**Algorithm**:
```python
# Load analytics.json
issue_lifecycle = analytics["issue_lifecycle"]

# Count from issue_lifecycle (ALL issues ever detected)
total_issues = len(issue_lifecycle)
challenged_count = sum(1 for i in issue_lifecycle.values() if i["status"] == "challenged")
unchallenged_count = total_issues - challenged_count

# Apply label
if total_issues == 0:
    add_label("radar-issues-resolved")  # Only if previously had issues
elif unchallenged_count == 0:
    add_label("radar-acknowledged")
else:
    add_label("radar-issues-detected")
```

---

### Azure Function (on challenge submission)

**Responsibilities**:
1. Record challenge in `analytics.json`
2. Update `issue_lifecycle[issue_hash]["status"]` to "challenged"
3. Check if ALL issues now challenged
4. Update labels if appropriate

**Algorithm**:
```python
# After recording challenge
issue_lifecycle = analytics["issue_lifecycle"]
total_issues = len(issue_lifecycle)
challenged_count = sum(1 for i in issue_lifecycle.values() if i["status"] == "challenged")
unchallenged_count = total_issues - challenged_count

# Only update labels if all issues challenged
if unchallenged_count == 0 and total_issues > 0:
    remove_label("radar-issues-detected")
    add_label("radar-acknowledged")
else:
    # Keep radar-issues-detected
    pass
```

---

## Edge Cases

### Case 1: Spec File Removed in New Commit
**Scenario**: PR originally modified `nginx.spec` (10 issues), then new commit removes all changes to `nginx.spec`.

**Expected**:
- Pipeline detects 0 issues in current commit
- `issue_lifecycle` still has 10 issues (marked as "resolved" because last_detected != current_commit)
- BUT: Those issues are no longer relevant since spec changes were removed
- Label should transition to `radar-issues-resolved`

**Current Behavior**: ✅ Correct (if counting current commit issues = 0)

---

### Case 2: New Commit Doesn't Touch Spec File
**Scenario**: PR has `nginx.spec` with 10 issues. User challenges 1 issue. Then pushes commit to `README.md` (unrelated file).

**Expected**:
- Pipeline runs but finds no spec file changes
- `issue_lifecycle` still has 10 issues (1 challenged, 9 unchallenged)
- Label should REMAIN `radar-issues-detected` (9 unchallenged)

**Current Behavior**: ❌ **BUG** - Pipeline only analyzes changed files, so `categorize_issues()` returns empty, making `total_issues = 0`, incorrectly changing label to `radar-issues-resolved`

**Fix Required**: Pipeline must count from `issue_lifecycle`, not from current commit's detected issues.

---

### Case 3: Same Issue in Multiple Commits
**Scenario**: Issue detected in commit A, still present in commit B.

**Expected**:
- `issue_lifecycle[hash]["last_detected"]` updated to commit B
- Issue counted once (not duplicated)
- Label remains based on challenge status

**Current Behavior**: ✅ Correct (issue_hash used as unique key)

---

## Current Bugs

### 🐛 Bug #1: Pipeline Counts Only Current Commit Issues

**Location**: `CveSpecFilePRCheck.py` lines 872-874

**Problem**:
```python
unchallenged_count = len(categorized_issues['new_issues']) + len(categorized_issues['recurring_unchallenged'])
challenged_count = len(categorized_issues['challenged_issues'])
total_issues = unchallenged_count + challenged_count
```

This counts ONLY issues detected in the current commit, not the entire `issue_lifecycle`.

**Impact**:
- If new commit doesn't touch spec files → `total_issues = 0` → Wrong label
- If spec file removed → `total_issues = 0` → Wrong label  
- Inconsistent with Azure Function (which uses `issue_lifecycle`)

**Fix**: Count from `issue_lifecycle` like Azure Function does:
```python
issue_lifecycle = analytics_mgr.analytics.get("issue_lifecycle", {})
total_issues = len(issue_lifecycle)
challenged_count = sum(1 for i in issue_lifecycle.values() if i.get("status") == "challenged")
unchallenged_count = total_issues - challenged_count
```

---

### 🐛 Bug #2: No Detection of "Previously Had Issues"

**Problem**: `radar-issues-resolved` should only be applied if there were previously detected issues. Currently applies even on first commit with 0 issues.

**Fix**: Check if `len(analytics["commits"]) > 1` or if `issue_lifecycle` has entries with `status != "active"`.

---

## Recommended Fixes

### Fix #1: Use issue_lifecycle for Label Decisions in Pipeline

```python
# In CveSpecFilePRCheck.py around line 867
if categorized_issues:
    # Remove all existing radar labels first
    logger.info("🏷️  Managing radar labels based on challenge state...")
    for label in ["radar-issues-detected", "radar-acknowledged", "radar-issues-resolved"]:
        github_client.remove_label(label)
    
    # Count from issue_lifecycle (same as Azure Function)
    issue_lifecycle = analytics_mgr.analytics.get("issue_lifecycle", {})
    total_issues = len(issue_lifecycle)
    challenged_count = sum(1 for issue in issue_lifecycle.values() 
                          if issue.get("status") == "challenged")
    unchallenged_count = total_issues - challenged_count
    
    logger.info(f"   📊 Issue lifecycle: {total_issues} total, {challenged_count} challenged, {unchallenged_count} unchallenged")
    
    # Add appropriate label based on state
    if total_issues == 0:
        # No issues detected (or all resolved)
        if len(analytics_mgr.analytics.get("commits", [])) > 1:
            # Had issues before, now resolved
            logger.info("   ✅ All issues resolved - adding 'radar-issues-resolved'")
            github_client.add_label("radar-issues-resolved")
        # else: First commit with no issues, no label needed
    elif unchallenged_count == 0:
        # All issues have been challenged
        logger.info(f"   ✅ All {total_issues} issues challenged - adding 'radar-acknowledged'")
        github_client.add_label("radar-acknowledged")
    else:
        # Has unchallenged issues
        logger.info(f"   ⚠️  {unchallenged_count}/{total_issues} unchallenged issues - adding 'radar-issues-detected'")
        github_client.add_label("radar-issues-detected")
```

---

## Testing Checklist

- [ ] First commit with issues → `radar-issues-detected`
- [ ] Challenge all issues → `radar-acknowledged`  
- [ ] New commit with same issues (all challenged) → `radar-acknowledged` (stays)
- [ ] New commit with new unchallenged issue → `radar-issues-detected`
- [ ] New commit fixes all issues → `radar-issues-resolved`
- [ ] New commit to unrelated file (no spec changes) → Label unchanged
- [ ] Spec file removed from PR → `radar-issues-resolved`
- [ ] Challenge 1 of 10 issues → `radar-issues-detected` (9 remain)
- [ ] Pipeline and Azure Function agree on label state

---

## Summary

**Key Principle**: Both Pipeline and Azure Function must use `issue_lifecycle` as the source of truth for label decisions. This ensures consistency regardless of which files are modified in a commit.

**Data Flow**:
1. Pipeline detects issues → Updates `issue_lifecycle`
2. User challenges issue → Azure Function updates `issue_lifecycle`  
3. Both check `issue_lifecycle` → Apply same label logic → Consistent state
