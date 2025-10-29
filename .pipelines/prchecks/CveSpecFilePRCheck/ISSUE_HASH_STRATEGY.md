# Issue Hash Strategy: Hybrid Approach

## Executive Summary

**Recommendation**: Use **Hybrid Context-Based + Content Fingerprint** approach.

- **Primary Key**: Human-readable context hash (e.g., `nginx-CVE-2025-11111-missing-patch-file`)
- **Verification**: Content fingerprint to detect actual fixes
- **Benefits**: Best of both worlds - readable + accurate

---

## Problem Analysis

### Current Issue (Fixed)
Hash collisions when multiple items share identifiers:
- `CVE-2025-11111.patch` → `nginx-CVE-2025-11111-missing-patch-file`
- `CVE-2025-11111-and-CVE-2025-22222.patch` → `nginx-CVE-2025-11111-missing-patch-file` (collision)

**Status**: ✅ Fixed by prioritizing full patch filename

### User's Proposal
Use spec file content + patch file state to generate hash.

**Goal**: Create perfectly unique hashes that reflect actual code state.

---

## Approach Comparison

### A. Pure Content-Based Hash

**Implementation**:
```python
def generate_content_hash(antipattern):
    # Hash the relevant content
    content_parts = [
        antipattern.file_path,
        antipattern.description,
        antipattern.context or "",  # Surrounding code
        str(antipattern.line_number) if antipattern.line_number else ""
    ]
    
    content_str = "|".join(content_parts)
    hash_digest = hashlib.sha256(content_str.encode()).hexdigest()[:12]
    
    return f"{package}-{antipattern.id}-{hash_digest}"
    # Example: nginx-missing-patch-file-a7b3c9d2e5f1
```

**Pros**:
- ✅ Zero collision risk
- ✅ Automatic uniqueness
- ✅ Captures full context

**Cons**:
- ❌ Loses human readability (`a7b3c9d2e5f1` vs `CVE-2025-11111`)
- ❌ Hash changes on unrelated edits (blank lines, formatting)
- ❌ Challenge history lost when spec modified
- ❌ Can't track "same issue across commits" if content changes
- ❌ False positives: Issue looks "new" after minor spec edits

**Use Cases**:
- Good for: Detecting exact duplicate issues
- Bad for: Long-lived issue tracking across spec changes

---

### B. Enhanced Context-Based Hash (Current, Fixed)

**Implementation**:
```python
def generate_issue_hash(antipattern):
    package = extract_package_name(antipattern.file_path)
    identifier = extract_key_identifier(antipattern)  # CVE, patch name, etc.
    
    return f"{package}-{identifier}-{antipattern.id}"
    # Example: nginx-CVE-2025-11111-missing-patch-file
```

**Pros**:
- ✅ Human-readable and debuggable
- ✅ Stable across minor spec edits
- ✅ Preserves challenge history across commits
- ✅ Easy to correlate with GitHub comments/logs

**Cons**:
- ⚠️ Requires careful identifier extraction (regex patterns)
- ⚠️ Possible collisions if extraction logic flawed
- ❌ Doesn't detect when issue actually fixed (if CVE still mentioned)

**Use Cases**:
- Good for: Long-term issue tracking, challenge persistence
- Bad for: Detecting subtle issue resolution

---

### C. Hybrid: Context Hash + Content Fingerprint (RECOMMENDED)

**Implementation**:
```python
@dataclass
class AntiPattern:
    # ... existing fields ...
    issue_hash: str = ""           # Context-based (human-readable)
    content_fingerprint: str = ""  # NEW: Content-based verification

def generate_hybrid_hash(antipattern, spec_content, patch_files):
    # 1. Generate human-readable context hash (primary key)
    package = extract_package_name(antipattern.file_path)
    identifier = extract_key_identifier(antipattern)
    issue_hash = f"{package}-{identifier}-{antipattern.id}"
    
    # 2. Generate content fingerprint (for verification)
    fingerprint = calculate_content_fingerprint(
        antipattern, spec_content, patch_files
    )
    
    return issue_hash, fingerprint

def calculate_content_fingerprint(antipattern, spec_content, patch_files):
    """
    Create fingerprint from relevant content to detect actual fixes.
    
    Includes:
    - Spec file content around the issue (±5 lines)
    - Referenced patch file existence
    - Line number (for position-sensitive issues)
    """
    context_lines = extract_context_lines(
        spec_content, 
        antipattern.line_number, 
        radius=5
    )
    
    # For missing-patch-file: Include list of .patch files
    if antipattern.id == "missing-patch-file":
        patch_name = extract_patch_name(antipattern.description)
        patch_exists = patch_name in patch_files
        
        fingerprint_data = {
            "type": antipattern.id,
            "context": context_lines,
            "patch_exists": patch_exists,
            "patch_name": patch_name
        }
    
    # For CVE-in-changelog: Include changelog entries
    elif antipattern.id == "missing-cve-in-changelog":
        cve_id = extract_cve(antipattern.description)
        changelog_section = extract_changelog_section(spec_content)
        
        fingerprint_data = {
            "type": antipattern.id,
            "context": context_lines,
            "cve": cve_id,
            "changelog": changelog_section
        }
    
    # Generic: Use surrounding context
    else:
        fingerprint_data = {
            "type": antipattern.id,
            "context": context_lines,
            "line": antipattern.line_number
        }
    
    # Hash the fingerprint data
    data_str = json.dumps(fingerprint_data, sort_keys=True)
    fingerprint = hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    return f"fp:{fingerprint}"
```

**Storage in issue_lifecycle**:
```json
{
  "issue_lifecycle": {
    "nginx-CVE-2025-11111-missing-patch-file": {
      "issue_hash": "nginx-CVE-2025-11111-missing-patch-file",
      "content_fingerprint": "fp:a7b3c9d2e5f18263",
      "first_detected": "abc123",
      "last_detected": "def456",
      "status": "active",
      "challenge_id": null,
      "fingerprint_changed": false
    }
  }
}
```

**Detection Logic**:
```python
def update_issue_lifecycle(analytics, current_issues):
    """
    Smart issue tracking with content verification.
    """
    for issue in current_issues:
        hash_key = issue.issue_hash
        new_fingerprint = issue.content_fingerprint
        
        if hash_key in analytics["issue_lifecycle"]:
            # Issue hash exists - check if content changed
            old_fingerprint = analytics["issue_lifecycle"][hash_key].get("content_fingerprint")
            
            if old_fingerprint != new_fingerprint:
                # Content changed! Issue was modified
                analytics["issue_lifecycle"][hash_key]["fingerprint_changed"] = True
                analytics["issue_lifecycle"][hash_key]["content_fingerprint"] = new_fingerprint
                analytics["issue_lifecycle"][hash_key]["last_detected"] = commit_sha
                
                # Log for debugging
                logger.info(f"📝 Issue {hash_key}: Content changed (potential fix attempt)")
            else:
                # Exact same issue, just update last_detected
                analytics["issue_lifecycle"][hash_key]["last_detected"] = commit_sha
        else:
            # New issue
            analytics["issue_lifecycle"][hash_key] = {
                "issue_hash": hash_key,
                "content_fingerprint": new_fingerprint,
                "first_detected": commit_sha,
                "last_detected": commit_sha,
                "status": "active",
                "challenge_id": null,
                "fingerprint_changed": False
            }
```

**Pros**:
- ✅ Human-readable primary key (`nginx-CVE-2025-11111-missing-patch-file`)
- ✅ Detects actual fixes (fingerprint changes)
- ✅ Challenge history preserved (uses context hash as key)
- ✅ Can detect "same issue, different context"
- ✅ Backwards compatible (fingerprint is optional addition)

**Cons**:
- ⚠️ Slightly more complex implementation
- ⚠️ Need to pass spec_content and patch_files to detector

**Use Cases**:
- ✅ Perfect for: Everything! Best of both worlds

---

## Recommendation: Implement Hybrid Approach

### Phase 1: Add Content Fingerprint Field

1. **Update AntiPattern dataclass**:
   ```python
   @dataclass
   class AntiPattern:
       # ... existing ...
       issue_hash: str = ""
       content_fingerprint: str = ""  # NEW
   ```

2. **Update AntiPatternDetector**:
   - Add `calculate_content_fingerprint()` method
   - Call it after generating `issue_hash`
   - Pass spec content and patch file list

3. **Update issue_lifecycle storage**:
   - Add `content_fingerprint` field
   - Add `fingerprint_changed` boolean

### Phase 2: Use Fingerprint for Smart Detection

1. **Resolution Detection**:
   - If fingerprint changes → Log "Issue modified"
   - If issue missing AND fingerprint changed before → "Potentially fixed"
   - If issue missing AND fingerprint same before → "Temporarily missing"

2. **Label Management Enhancement**:
   - Count only issues where fingerprint unchanged OR recently challenged
   - Issues with changed fingerprints could be "pending verification"

3. **Challenge Validation**:
   - If user challenges issue, store fingerprint at challenge time
   - On next commit, check if fingerprint changed
   - If changed → Auto-close challenge as "fixed"
   - If same → Keep challenge active

---

## Implementation Details

### For missing-patch-file Antipatterns

**Fingerprint includes**:
```python
{
    "type": "missing-patch-file",
    "patch_name": "CVE-2025-11111.patch",
    "patch_exists": false,  # Check filesystem
    "spec_context": "Patch0: CVE-2025-11111.patch\nPatch1: CVE-2025-22222.patch",
    "line_range": [145, 155]  # ±5 lines around Patch reference
}
```

**When patch is added**:
- Fingerprint changes: `patch_exists: false` → `true`
- System detects: "Issue likely fixed"
- Can auto-resolve or mark for review

### For missing-cve-in-changelog Antipatterns

**Fingerprint includes**:
```python
{
    "type": "missing-cve-in-changelog",
    "cve_id": "CVE-2025-11111",
    "changelog_content": "* Fri Oct 27 2025...\n- Updated to version 1.2.3\n...",
    "cve_in_changelog": false  # Grep CVE in changelog
}
```

**When changelog updated**:
- Fingerprint changes: `cve_in_changelog: false` → `true`
- System detects: "CVE added to changelog"
- Can auto-resolve

---

## Edge Cases Handled

### Case 1: Spec Reformatting
**Scenario**: User runs formatter, adds blank lines

**Context Hash**: `nginx-CVE-2025-11111-missing-patch-file` (unchanged ✅)
**Fingerprint**: Changes slightly due to context lines

**Result**: Issue tracked under same hash, fingerprint change logged but not treated as new issue

---

### Case 2: Issue Fixed Then Reappears
**Scenario**: 
1. Patch added (issue fixed)
2. Patch removed in later commit (issue returns)

**Context Hash**: `nginx-CVE-2025-11111-missing-patch-file` (same)
**Fingerprint Timeline**:
- Commit 1: `fp:abc123` (patch missing)
- Commit 2: `fp:def456` (patch exists) 
- Commit 3: `fp:abc123` (patch missing again)

**Result**: Can detect regression! "Issue reappeared with original fingerprint"

---

### Case 3: Same CVE, Different Context
**Scenario**: CVE-2025-11111 mentioned in multiple places

**Context Hash**: 
- `nginx-CVE-2025-11111-missing-patch-file` (patch)
- `nginx-CVE-2025-11111-missing-cve-in-changelog` (changelog)

**Fingerprints**: Completely different (different file sections)

**Result**: Tracked as separate issues correctly ✅

---

## Migration Strategy

### For Existing PRs

**Problem**: Existing `issue_lifecycle` entries don't have fingerprints

**Solution**:
```python
if "content_fingerprint" not in issue_data:
    # Legacy issue without fingerprint
    issue_data["content_fingerprint"] = None
    issue_data["fingerprint_changed"] = False
    
    # On next detection, populate fingerprint
```

**Backwards Compatible**: System works without fingerprints, they're additive

---

## Performance Considerations

**Fingerprint Calculation Cost**:
- Read spec file: Already done for detection
- Extract context lines: O(1) with line index
- Hash calculation: ~1ms per issue
- **Total**: Negligible (< 10ms for 100 issues)

**Storage Cost**:
- Fingerprint: 16 chars = 16 bytes
- Per PR with 50 issues: 800 bytes
- **Impact**: Minimal

---

## Conclusion

**Implement Hybrid Approach**:

1. **Keep current context-based hash** (human-readable)
2. **Add content fingerprint** (accuracy)
3. **Use fingerprint for verification** (detect actual fixes)

**Benefits**:
- ✅ No breaking changes
- ✅ Human-readable tracking
- ✅ Accurate fix detection
- ✅ Challenge history preserved
- ✅ Regression detection
- ✅ Auto-resolution potential

**Next Steps**:
1. Extend `AntiPattern` with `content_fingerprint` field
2. Implement `calculate_content_fingerprint()` 
3. Update `issue_lifecycle` schema
4. Add fingerprint-based smart detection
5. Test with real PRs

Would you like me to implement this hybrid approach?
