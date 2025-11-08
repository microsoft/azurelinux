# CVE Spec File PR Check - Test Suite

## Overview

This test suite provides reusable test cases that modify **existing specs in SPECS/** to validate all 11 anti-pattern detection types. SPECS directory remains intact - apply these patches only in test branches.

## Test Strategy

Each test case is a **patch file** that adds anti-patterns to a carefully chosen spec file from SPECS/. The patches are designed to trigger specific anti-pattern detections while being realistic.

## Selected Specs and Rationale

| Spec File | Characteristics | Best For Testing |
|-----------|----------------|------------------|
| **azcopy** | Simple structure, already has CVE patches | Basic anti-patterns, duplicates |
| **curl** | Has CVE patches, simple macros | Missing files, changelog issues |
| **python-tomli** | Heavy macro usage (`%{pypi_name}`, `%{_description}`) | Macro expansion in CVE detection |
| **openssl** | Complex patches, many Patch numbers | Edge cases, format validation |

## Test Cases

### Test 1: Basic Anti-Patterns (`test-01-basic-antipatterns.patch`)

**Target**: `SPECS/curl/curl.spec`

**Modifications**:
- Add 3 more CVE patches (Patch3-5) but don't create the files → **missing-patch-file**
- Add Patch6 with future CVE-2035-11111 → **future-dated-cve**
- Duplicate existing Patch0 as Patch7 → **duplicate-cve-patch**
- Add Patch8: `security-fix.patch` (no CVE in name) → **patch-without-cve-ref**
- Add Patch9: `CVE-202X-INVALID.patch` → **invalid-cve-format**
- Add Patch10: `CVE-2025-99999.patch` but don't mention in changelog → **missing-cve-in-changelog**

**Expected Findings**: 7 ERROR, 3 WARNING

### Test 2: Macro Expansion (`test-02-macro-expansion.patch`)

**Target**: `SPECS/python-tomli/python-tomli.spec`

**Modifications**:
```spec
%global pypi_name tomli
%global cve_year 2025
%global cve_base CVE-
%global security_patch_num 12345

# Add these patches with macro references
Patch0: %{cve_base}%{cve_year}-%{security_patch_num}.patch
Patch1: CVE-%{cve_year}-54321.patch
Patch2: %{cve_base}2035-99999.patch  # Future year via macro
```

**Purpose**: Validate that PR check:
- Expands macros before CVE detection
- Detects `CVE-2025-12345` from `%{cve_base}%{cve_year}-%{security_patch_num}`
- Detects future-dated CVE even when year is in macro
- Handles conditional patches with `%if` blocks

**Expected Findings**: 3 ERROR (missing files, future-dated after expansion)

### Test 3: Unused Patch Files (`test-03-unused-patches.patch`)

**Target**: `SPECS/azcopy/azcopy.spec`

**Modifications**:
- Create `azcopy/orphaned-security-fix.patch` in SPECS directory
- Create `azcopy/CVE-2024-77777-unused.patch` in SPECS directory
- Don't reference them in .spec file

**Purpose**: Test **unused-patch-file** detection

**Expected Findings**: 2 WARNING

### Test 4: Changelog Validation (`test-04-changelog-issues.patch`)

**Target**: `SPECS/curl/curl.spec`

**Modifications**:
- Add `Patch11: CVE-2025-88888.patch`
- In changelog, add entry without proper dash prefix:
  ```
  Applied CVE-2025-88888 fix  # Missing '-' prefix
  ```
- Add malformed date:
  ```
  * Invalid Date Format - 1.0.0-1
  ```

**Purpose**: Test **invalid-changelog-format**

**Expected Findings**: 1 ERROR (missing file), 1 WARNING (invalid format)

### Test 5: Edge Cases (`test-05-edge-cases.patch`)

**Target**: `SPECS/openssl/openssl.spec`

**Modifications**:
- Add `Patch100: cve-2024-11111.patch` (lowercase 'cve')
- Add `Patch101: CVE-2024-00999.patch` (leading zeros)
- Add `Patch102: CVE-1999-00001.patch` (very old, first CVE year)
- Add `Patch103: CVE-2026-11111.patch` (current year + 1, boundary case)
- Add `Patch104: CVE-2024-11111-and-CVE-2024-22222-combined.patch` (multiple CVEs)

**Purpose**: Test format normalization, boundary conditions

**Expected Findings**: 5 ERROR (missing files), correct CVE extraction

## Directory Structure

```
.pipelines/prchecks/CveSpecFilePRCheck/tests/
├── TEST_SUITE.md (this file)
├── USAGE.md (how to apply tests)
├── test-patches/
│   ├── test-01-basic-antipatterns.patch
│   ├── test-02-macro-expansion.patch
│   ├── test-03-unused-patches/
│   │   ├── apply.sh
│   │   ├── orphaned-security-fix.patch
│   │   └── CVE-2024-77777-unused.patch
│   ├── test-04-changelog-issues.patch
│   └── test-05-edge-cases.patch
└── expected-findings/
    ├── test-01-expected.json
    ├── test-02-expected.json
    ├── test-03-expected.json
    ├── test-04-expected.json
    └── test-05-expected.json
```

## How to Use

### Quick Test (Single Category)

```bash
# 1. Create test branch
git checkout -b test/basic-antipatterns

# 2. Apply test patch
cd /path/to/azurelinux
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-01-basic-antipatterns.patch

# 3. Commit and push
git add SPECS/curl/
git commit -m "test: basic anti-pattern detection"
git push origin test/basic-antipatterns

# 4. Create PR
gh pr create --base abadawi/multi-spec-radar --head test/basic-antipatterns --title "Test: Basic Anti-Patterns"

# 5. Review HTML report and test OAuth
```

### Comprehensive Test (All Categories)

```bash
# Apply all test patches
for patch in .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-*.patch; do
    patch -p1 < "$patch"
done

# Apply unused patch files
bash .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-03-unused-patches/apply.sh

git add SPECS/
git commit -m "test: comprehensive anti-pattern detection validation"
git push origin test/comprehensive
gh pr create --base abadawi/multi-spec-radar --title "Test: Comprehensive PR Check Validation"
```

### Cleanup After Testing

```bash
# Revert all test changes
git checkout HEAD -- SPECS/

# Or reset branch
git reset --hard origin/abadawi/sim_7
```

## Expected HTML Report

When PR is created, the HTML report should show:

```
📊 Multi-Spec Analysis Summary
Total Specs Analyzed: 4
Total Findings: ~25-30
  ERROR: ~18-20
  WARNING: ~7-10

📄 curl.spec
  ❌ ERROR: Missing patch files: Patch3, Patch4, Patch5, Patch6, Patch9, Patch10
  ❌ ERROR: Future-dated CVE-2035-11111
  ❌ ERROR: Invalid CVE format: CVE-202X-INVALID
  ❌ ERROR: CVE-2025-99999 not in changelog
  ⚠️ WARNING: Duplicate CVE (Patch0 and Patch7)
  ⚠️ WARNING: Patch without CVE: security-fix.patch

📄 python-tomli.spec
  ❌ ERROR: Missing patch files (after macro expansion)
  ❌ ERROR: Future-dated CVE-2035-99999 (macro-expanded from %{cve_base}2035-99999)

📄 azcopy.spec
  ⚠️ WARNING: Unused patch: orphaned-security-fix.patch
  ⚠️ WARNING: Unused patch: CVE-2024-77777-unused.patch

📄 openssl.spec
  ❌ ERROR: Missing patch files: Patch100-104
  (CVEs correctly extracted and normalized from lowercase, leading zeros, etc.)
```

## Validation Checklist

After creating test PR:

- [ ] HTML report generated successfully
- [ ] All modified specs appear in report
- [ ] Findings match expected counts
- [ ] Macro-expanded CVEs show expanded form in report
- [ ] Future-dated CVEs detected correctly
- [ ] Duplicate CVEs identified
- [ ] Unused patch files reported
- [ ] Changelog issues detected
- [ ] OAuth sign-in works
- [ ] Challenge submission works for different finding types
- [ ] GitHub comment posted
- [ ] Label applied

## Anti-Pattern Coverage Matrix

| Anti-Pattern | Test 01 | Test 02 | Test 03 | Test 04 | Test 05 |
|--------------|---------|---------|---------|---------|---------|
| missing-patch-file | ✅ | ✅ | - | ✅ | ✅ |
| future-dated-cve | ✅ | ✅ | - | - | - |
| duplicate-cve-patch | ✅ | - | - | - | - |
| invalid-cve-format | ✅ | - | - | - | - |
| patch-without-cve-ref | ✅ | - | - | - | - |
| missing-cve-in-changelog | ✅ | - | - | - | - |
| unused-patch-file | - | - | ✅ | - | - |
| invalid-changelog-format | - | - | - | ✅ | - |
| Case normalization | - | - | - | - | ✅ |
| Leading zeros | - | - | - | - | ✅ |
| Boundary years | - | - | - | - | ✅ |
| Multiple CVEs in filename | - | - | - | - | ✅ |

All 11 anti-pattern types covered across 5 test cases!

---

**Last Updated**: October 21, 2024  
**Test Suite Version**: 2.0.0  
**Approach**: Patch-based modifications to existing SPECS
