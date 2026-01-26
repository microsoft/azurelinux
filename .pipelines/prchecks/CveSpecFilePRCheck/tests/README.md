# CVE Spec File PR Check - Test Suite

Comprehensive, reusable test cases for validating anti-pattern detection in the CVE spec file PR check system.

## 📁 Structure

```
tests/
├── README.md              # This file
├── TEST_SUITE.md          # Detailed test case descriptions
├── USAGE.md               # Step-by-step usage instructions
└── test-patches/          # Patch files to apply to SPECS
    ├── test-01-basic-antipatterns.patch
    ├── test-02-macro-expansion.patch
    ├── test-03-unused-patches/
    │   ├── apply.sh
    │   ├── orphaned-security-fix.patch
    │   └── CVE-2024-77777-unused.patch
    ├── test-04-changelog-issues.patch
    └── test-05-edge-cases.patch
```

## 🎯 What This Tests

All 11 anti-pattern detection types across 4 real spec files:

| Anti-Pattern | Severity | Tested By |
|--------------|----------|-----------|
| missing-patch-file | ERROR | Tests 1, 2, 4, 5 |
| future-dated-cve | ERROR | Tests 1, 2 |
| duplicate-cve-patch | WARNING | Test 1 |
| invalid-cve-format | ERROR | Test 1 |
| patch-without-cve-ref | WARNING | Test 1 |
| missing-cve-in-changelog | ERROR | Test 1 |
| unused-patch-file | WARNING | Test 3 |
| invalid-changelog-format | WARNING | Test 4 |
| **Macro expansion** | N/A | Test 2 |
| **Case normalization** | N/A | Test 5 |
| **Boundary conditions** | N/A | Test 5 |

## 📚 Documentation

- **TEST_SUITE.md**: Detailed test case specifications, expected findings, spec selection rationale
- **USAGE.md**: Step-by-step commands, troubleshooting guide, validation checklist

## 🎓 Example: Testing Macro Expansion

The PR check must expand RPM macros before detecting CVEs. Test 2 validates this:

```spec
# In python-tomli.spec
%global cve_base CVE-
%global cve_year 2025
Patch0: %{cve_base}%{cve_year}-12345.patch
```

**Expected**: Expands to `CVE-2025-12345.patch` and detects missing file.

## 🔗 Full Integration Test

After running tests and PR check completes:

1. ✅ Open HTML report from Azure Blob Storage
2. ✅ Sign in with GitHub OAuth
3. ✅ Verify role badge displays correctly
4. ✅ Submit challenge on findings
5. ✅ Verify GitHub comment posted
6. ✅ Verify `radar:findings-addressed` label applied

---

**See TEST_SUITE.md for detailed specifications and USAGE.md for step-by-step instructions.**

| unused-patch-file | WARNING | Test 3 |
| invalid-changelog-format | WARNING | Test 4 |
| **Macro expansion** | N/A | Test 2 |
| **Case normalization** | N/A | Test 5 |
| **Boundary conditions** | N/A | Test 5 |

## ⚡ Quick Start

```bash
# Test one category
git checkout -b test/basic
patch -p1 < .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-01-basic-antipatterns.patch
git add SPECS/curl/
git commit -m "test: basic anti-patterns"
git push origin test/basic
gh pr create --base abadawi/multi-spec-radar --title "Test: Basic Anti-Patterns"

# Test all categories
git checkout -b test/comprehensive
for patch in .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-*.patch; do
    patch -p1 < "$patch"
done
bash .pipelines/prchecks/CveSpecFilePRCheck/tests/test-patches/test-03-unused-patches/apply.sh
git add SPECS/
git commit -m "test: comprehensive validation"
git push origin test/comprehensive
gh pr create --base abadawi/multi-spec-radar --title "Test: Comprehensive"
```

From the CveSpecFilePRCheck directory:

```bash
# Run all tests
python tests/run_all_tests.py

# Or make it executable and run directly
chmod +x tests/run_all_tests.py
./tests/run_all_tests.py
```
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_antipattern_detector

# Run specific test class
python -m unittest tests.test_antipattern_detector.TestAntiPatternDetector

# Run specific test method
python -m unittest tests.test_antipattern_detector.TestAntiPatternDetector.test_missing_patch_file

# Run with verbose output
python -m unittest discover tests -v