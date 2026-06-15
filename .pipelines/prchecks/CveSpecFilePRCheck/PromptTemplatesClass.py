#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
PromptTemplatesClass provides standardized prompt templates for Azure OpenAI
interactions related to spec file analysis and CVE checking.
"""

class PromptTemplates:
    """Collection of prompt templates for spec file analysis"""

    @staticmethod
    def get_system_prompt():
        """
        Returns the system prompt for the AI, setting up its role and expertise.
        """
        return """You are a security-focused software analyst specializing in Azure Linux package spec files and CVE patches. 
Your task is to review changes to .spec files and verify related patch files for security issues.

You have deep expertise in:
- RPM spec file format and best practices for Azure Linux
- CVE patching workflows in Azure Linux packages
- Linux package management and security
- Security vulnerability analysis and remediation

Analyze changes thoroughly, focusing on:
1. Security implications of version changes
2. Validation of CVE patch references in the format: Patch<N>: CVE-YYYY-XXXXX.patch
3. Common anti-patterns in spec file changes
4. Potential security regressions
5. Missing patches referenced in spec files
6. Proper changelog entries for CVE fixes (e.g., "- Fix CVE-YYYY-XXXXX with an upstream patch")
7. Proper application of patches with %patch or %autopatch directives

Provide clear, actionable feedback with specific recommendations."""

    @staticmethod
    def get_spec_analysis_prompt(diff_text, file_list, spec_content=None):
        """
        Returns a prompt for analyzing spec file changes with structured output for both 
        brief PR comments and detailed logging.
        
        Args:
            diff_text: The git diff showing changes
            file_list: List of files in the package directory
            spec_content: Full content of the spec file (if available)
        """
        spec_section = ""
        if spec_content:
            spec_section = f"""
### Full Spec File Content:
```
{spec_content}
```
"""

        return f"""## Task: Analyze the following .spec file changes and verify patch references

### Diff of Changes:
```diff
{diff_text}
```

### Files present in the package directory:
```
{", ".join(file_list) if isinstance(file_list, list) else file_list}
```
{spec_section}

**IMPORTANT: Structure your response into TWO distinct sections:**

## SECTION 1: BRIEF PR COMMENT SUMMARY
Provide a concise summary suitable for GitHub PR comments (keep under 200 words):

**Brief Analysis:** (1-2 sentences summarizing key findings)

**Critical Issues Found:** (List only ERROR/CRITICAL severity issues, if any)

**Recommended Actions:** (2-3 brief actionable bullet points for the most important fixes)

---

## SECTION 2: DETAILED ANALYSIS FOR LOGS
Provide comprehensive analysis for pipeline logs:

### Security Analysis:
1. What security implications do these changes have?
2. Are all CVE patch files referenced in the spec (Patch<N>: CVE-YYYY-XXXXX.patch) actually present in the file list?
3. Are there any version updates that should be flagged for security review?
4. Are all CVEs mentioned in the changelog matched with corresponding patch files?
5. Are patches being properly applied with %patch or %autopatch directives?
6. Is there proper changelog documentation for all CVE fixes?

### Anti-Pattern Detection:
Check for these common Azure Linux spec file issues:
- CVE patches referenced in spec but missing from the directory
- CVE fixes mentioned in changelog but without corresponding patch files
- Patches applied but not listed in Patch<N> directives
- Incorrect patch numbering (should be sequential Patch0, Patch1, etc.)
- Missing %patch or %autopatch directives to apply the patches
- Changelog entries for CVE fixes lacking CVE IDs or descriptions
- Inconsistent version numbers between Name, Version, and changelog
- BuildRequires and Requires missing security-related dependencies
- Patches not properly named according to CVE-YYYY-XXXXX.patch format
- Fix for a CVE without proper attribution or upstream reference

### Detailed Recommendations:
Provide specific, actionable recommendations for each issue found, including:
- Exact file names and line numbers where possible
- Specific commands or changes needed
- Security implications of not fixing the issues
- Best practices for Azure Linux packaging

Focus particularly on security implications and whether all referenced CVE patches are actually present in the directory."""

    @staticmethod
    def get_cve_validation_prompt(diff_text, spec_content, cve_ids, patch_files):
        """
        Returns a prompt specifically focused on validating CVE patches with structured output.
        
        Args:
            diff_text: The git diff showing changes
            spec_content: Full content of the spec file
            cve_ids: List of CVE IDs mentioned in the spec
            patch_files: List of patch files found in the directory
        """
        return f"""## Task: Validate CVE patch integration in Azure Linux spec file

### Diff of Changes:
```diff
{diff_text}
```

### Full Spec File Content:
```
{spec_content}
```

### CVE IDs mentioned in spec or changelog:
```
{cve_ids}
```

### Actual patch files found in package directory:
```
{patch_files}
```

**IMPORTANT: Structure your response into TWO distinct sections:**

## SECTION 1: BRIEF PR COMMENT SUMMARY
**CVE Validation Summary:** (1-2 sentences on CVE patch status)

**Critical CVE Issues:** (List missing or mismatched CVE patches)

**Recommended CVE Actions:** (2-3 actionable fixes for CVE issues)

---

## SECTION 2: DETAILED CVE VALIDATION FOR LOGS
### Comprehensive CVE Analysis:
1. Are all the CVE IDs mentioned in the spec covered by actual patch files in the format CVE-YYYY-XXXXX.patch?
2. Are all CVEs mentioned in the changelog matched with corresponding patch files?
3. Are the patches properly referenced with Patch<N> directives and applied with %patch or %autopatch directives?
4. Are there any patches that should have CVE IDs but don't?
5. Does the changelog properly document all CVE fixes with adequate descriptions?
6. Are the patches correctly numbered and sequenced (Patch0, Patch1, etc.)?

### Detailed CVE Issues Check:
- Missing patch files for referenced CVEs
- Inconsistent naming between CVE references and patch filenames
- Incomplete changelog entries for CVE fixes
- Patches not being applied properly
- Duplicate CVE patches or references
- Outdated CVE patches that have been superseded

### Specific CVE Recommendations:
Provide detailed validation report highlighting any mismatches or concerns, with specific recommendations for fixing any issues including exact file names and required changes."""

    @staticmethod
    def get_patch_verification_prompt(spec_content, file_list, patch_references):
        """
        Returns a prompt for verifying if all patches referenced in the spec
        are present in the package directory, with structured output.
        
        Args:
            spec_content: Full content of the spec file
            file_list: List of files in the package directory
            patch_references: Extracted patch references from spec file
        """
        return f"""## Task: Verify patch references in spec file against actual files

### Spec File Content:
```
{spec_content}
```

### Files in Package Directory:
```
{file_list}
```

### Patch References from Spec (Patch<N> lines):
```
{patch_references}
```

**IMPORTANT: Structure your response into TWO distinct sections:**

## SECTION 1: BRIEF PR COMMENT SUMMARY
**Patch Verification Summary:** (1-2 sentences on patch status)

**Critical Patch Issues:** (List missing or unreferenced patches)

**Recommended Patch Actions:** (2-3 actionable fixes)

---

## SECTION 2: DETAILED PATCH VERIFICATION FOR LOGS
### Comprehensive Patch Analysis:
1. Are all patches referenced in the spec file (via Patch<N>) actually present in the directory?
2. Are there any patch files in the directory that aren't referenced in the spec?
3. Are the patch numbers sequential and properly ordered?
4. For CVE patches, do the filenames match the CVE IDs referenced in the spec?

### Detailed Verification Report:
Check each Patch<N> reference against the actual files in the directory and identify any missing or incorrectly referenced patches. Pay special attention to CVE patches, which should follow the naming convention CVE-YYYY-XXXXX.patch.

### Specific Patch Recommendations:
Provide detailed verification report with specific issues and recommendations including exact file names and required changes."""