#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
FixRecommender
-------------
Generates specific, actionable fix recommendations for detected anti-patterns.

This module enhances the basic recommendations in AntiPattern instances
with more specific, content-aware recommendations that can be directly
applied to fix the detected issues.
"""

import os
import re
import logging
import datetime
from typing import Dict, List, Optional, Any
from AntiPatternDetector import AntiPattern, Severity

# Configure logging
logger = logging.getLogger("fix-recommender")

class FixRecommender:
    """Generates specific fix recommendations for anti-patterns"""
    
    def __init__(self, openai_client=None):
        """
        Initialize the fix recommender

        Args:
            openai_client: Optional OpenAIClient for dynamic recommendations
        """
        logger.info("Initialized FixRecommender")
        self.openai_client = openai_client
        
    def enhance_recommendations(self, anti_patterns: List[AntiPattern], 
                               spec_content: str, file_list: List[str]) -> List[AntiPattern]:
        """
        Enhance recommendations for anti-patterns with more specific, actionable fixes.
        
        Args:
            anti_patterns: List of detected anti-patterns
            spec_content: Content of the spec file
            file_list: List of files in the same directory
            
        Returns:
            List of anti-patterns with enhanced recommendations
        """
        if not anti_patterns:
            return []
            
        # Process each anti-pattern to enhance its recommendation
        enhanced_patterns = []
        for pattern in anti_patterns:
            # Create a copy to avoid modifying the original
            enhanced_pattern = pattern
            
            # Generate specific recommendation based on pattern type
            if pattern.id == 'missing-patch-file':
                enhanced_pattern.recommendation = self._recommend_missing_patch(pattern, spec_content, file_list)
            elif pattern.id == 'unused-patch-file':
                enhanced_pattern.recommendation = self._recommend_unused_patch(pattern, spec_content, file_list)
            elif pattern.id == 'cve-patch-mismatch':
                enhanced_pattern.recommendation = self._recommend_cve_patch_mismatch(pattern, spec_content)
            elif pattern.id == 'missing-cve-in-changelog':
                enhanced_pattern.recommendation = self._recommend_missing_cve_changelog(pattern, spec_content)
            elif pattern.id == 'missing-changelog-entry':
                enhanced_pattern.recommendation = self._recommend_missing_changelog(pattern)
            elif pattern.id == 'invalid-changelog-format':
                enhanced_pattern.recommendation = self._recommend_invalid_changelog_format(pattern, spec_content)
            elif pattern.id == 'future-dated-cve':
                enhanced_pattern.recommendation = self._recommend_future_dated_cve(pattern)
            else:
                # For any pattern not explicitly handled, use AI reasoning
                enhanced_pattern.recommendation = self._recommend_with_model(pattern, spec_content, file_list)
                
            enhanced_patterns.append(enhanced_pattern)
            
        return enhanced_patterns
        
    def _recommend_missing_patch(self, pattern: AntiPattern, spec_content: str, 
                                file_list: List[str]) -> str:
        """Generate recommendation for missing patch file"""
        # Extract patch filename from description
        patch_file = re.search(r"'([^']+)'", pattern.description)
        if not patch_file:
            return pattern.recommendation
        
        patch_file = patch_file.group(1)
        
        # Check if there's a similarly named file that might be a replacement
        similar_files = [f for f in file_list if f.endswith('.patch') and self._similarity(f, patch_file) > 0.7]
        
        if similar_files:
            similar_file = similar_files[0]
            # Extract patch number from context
            patch_num = re.search(r"Patch(\d+):", pattern.context)
            if patch_num:
                patch_num = patch_num.group(1)
                # Construct specific recommendation with code example
                return f"""The patch file '{patch_file}' is missing. Consider using '{similar_file}' instead.

To fix this issue, update the Patch line in your spec file:
```
Patch{patch_num}: {similar_file}
```

Alternatively, add the missing patch file to the package directory."""
        
        # If no similar file found, recommend creating the patch
        return f"""The patch file '{patch_file}' is referenced in the spec but not found in the directory.

You have two options:
1. Create the missing patch file '{patch_file}' in the package directory
2. Update the spec file to reference an existing patch file instead

If this is a CVE patch, ensure it follows naming conventions (e.g., CVE-YYYY-XXXXX.patch)."""

    def _recommend_unused_patch(self, pattern: AntiPattern, spec_content: str, 
                               file_list: List[str]) -> str:
        """Generate recommendation for unused patch file"""
        # Extract patch filename from description
        patch_file = re.search(r"'([^']+)'", pattern.description)
        if not patch_file:
            return pattern.recommendation
        
        patch_file = patch_file.group(1)
        
        # Find next available patch number
        patch_numbers = []
        for line in spec_content.splitlines():
            patch_match = re.match(r'^Patch(\d+):', line.strip())
            if patch_match:
                patch_numbers.append(int(patch_match.group(1)))
                
        next_patch_num = 0 if not patch_numbers else max(patch_numbers) + 1
        
        # Construct specific recommendation with code example
        return f"""The patch file '{patch_file}' exists in the directory but is not referenced in the spec.

To fix this issue, add a reference to the spec file:
```
Patch{next_patch_num}: {patch_file}
```

Then make sure to apply it using the appropriate directive:
```
%patch{next_patch_num} -p1
```

If the patch is not needed, consider removing it from the package directory."""

    def _recommend_cve_patch_mismatch(self, pattern: AntiPattern, spec_content: str) -> str:
        """Generate recommendation for CVE patch mismatch"""
        # Extract CVE ID from description
        cve_id = re.search(r"(CVE-\d{4}-\d+)", pattern.description)
        if not cve_id:
            return pattern.recommendation
        
        cve_id = cve_id.group(1)
        
        # Find changelog section
        changelog_match = re.search(r'%changelog(.*?)$', spec_content, re.DOTALL)
        if not changelog_match:
            return f"""Add {cve_id} to the spec file by adding a changelog entry.
            
Add a %changelog section with an entry for the CVE fix:
```
%changelog
* {self._get_current_date()} Your Name <your.email@example.com> - current_version-release
- Fix {cve_id}
```"""
        
        # Find most recent changelog entry
        changelog_text = changelog_match.group(1)
        entries = re.split(r'\*\s+\w+\s+\w+\s+\d+\s+\d{4}', changelog_text)
        
        if len(entries) > 1:
            # Construct specific recommendation with code example
            return f"""Add {cve_id} reference to the latest changelog entry:
```
- Fix {cve_id}
```

Make sure the CVE is properly documented in the changelog and the patch is applied in the %build or %install section."""
        else:
            # If no entries found, recommend adding one
            return f"""Add a changelog entry for the CVE fix:
```
* {self._get_current_date()} Your Name <your.email@example.com> - current_version-release
- Fix {cve_id}
```"""

    def _recommend_missing_cve_changelog(self, pattern: AntiPattern, spec_content: str) -> str:
        """Generate recommendation for missing CVE in changelog"""
        # Extract CVE ID from description
        cve_id = re.search(r"(CVE-\d{4}-\d+)", pattern.description)
        if not cve_id:
            return pattern.recommendation
        
        cve_id = cve_id.group(1)
        
        # Find most recent changelog entry
        changelog_match = re.search(r'%changelog(.*?)$', spec_content, re.DOTALL)
        if not changelog_match:
            return f"""Add {cve_id} to the spec file by adding a proper changelog entry.
            
Add a %changelog section with an entry for the CVE fix:
```
%changelog
* {self._get_current_date()} Your Name <your.email@example.com> - current_version-release
- Fix {cve_id}
```"""
        
        # Find the first changelog entry line
        changelog_text = changelog_match.group(1)
        entry_match = re.search(r'\*\s+\w+\s+\w+\s+\d+\s+\d{4}', changelog_text)
        
        if entry_match:
            # Get position where we should insert our new line
            entry_text = entry_match.group(0)
            entry_end = changelog_text.find(entry_text) + len(entry_text)
            
            # Construct specific recommendation with code example
            return f"""Add {cve_id} reference to the latest changelog entry by adding this line after '{entry_text}':
```
- Fix {cve_id}
```

This ensures the CVE fix is properly documented in the changelog."""
        else:
            # If no entries found, recommend adding one
            return f"""Add a changelog entry for the CVE fix:
```
* {self._get_current_date()} Your Name <your.email@example.com> - current_version-release
- Fix {cve_id}
```"""

    def _recommend_missing_changelog(self, pattern: AntiPattern) -> str:
        """Generate recommendation for missing changelog"""
        return f"""Add a %changelog section at the end of your spec file:
```
%changelog
* {self._get_current_date()} Your Name <your.email@example.com> - initial-version
- Initial package version
```

Replace with appropriate version information and details about your changes."""

    def _recommend_invalid_changelog_format(self, pattern: AntiPattern, 
                                           spec_content: str) -> str:
        """Generate recommendation for invalid changelog format"""
        # Extract invalid entry from context
        if not pattern.context:
            return pattern.recommendation
        
        invalid_entry = pattern.context
        
        # Create a properly formatted entry
        proper_format = f"* {self._get_current_date()} Your Name <your.email@example.com> - version-release"
        
        return f"""The changelog entry format '{invalid_entry}' is invalid.
        
Use the standard format instead:
```
{proper_format}
```

Each changelog entry should start with an asterisk followed by day, month, date, year,
name, email address, and then package version information."""

    def _recommend_future_dated_cve(self, pattern: AntiPattern) -> str:
        """Generate recommendation for future-dated CVE"""
        # Extract CVE ID from description
        cve_id = re.search(r"CVE (CVE-\d{4}-\d+)", pattern.description)
        if not cve_id:
            return pattern.recommendation
        
        cve_id = cve_id.group(1)
        
        # Extract incorrect year from description
        year_match = re.search(r"year (\d{4})", pattern.description)
        if not year_match:
            return pattern.recommendation
        
        incorrect_year = year_match.group(1)
        current_year = str(datetime.datetime.now().year)
        
        # Suggest corrected CVE ID
        corrected_cve = cve_id.replace(incorrect_year, current_year)
        
        return f"""The CVE ID {cve_id} appears to have an incorrect year ({incorrect_year}).
        
Check the MITRE CVE database and update to the correct CVE ID. If you meant the current year's CVE, use:
```
{corrected_cve}
```

Verify the CVE ID exists in the official CVE database."""

    def _recommend_with_model(self, pattern: AntiPattern, spec_content: str, 
                             file_list: List[str]) -> str:
        """
        Generate recommendation for an anti-pattern using AI reasoning.
        This is used as a fallback for patterns not explicitly handled.
        
        Args:
            pattern: The anti-pattern to generate a recommendation for
            spec_content: Content of the spec file
            file_list: List of files in the same directory
            
        Returns:
            AI-generated recommendation string
        """
        # If no OpenAI client is available, return the original recommendation
        if not self.openai_client:
            logger.warning(f"No OpenAI client available for dynamic recommendation generation")
            return pattern.recommendation
        
        try:
            logger.info(f"Generating dynamic recommendation for {pattern.id}")
            
            # Context to provide to the model
            file_context = "\n".join(file_list) if file_list else "No files in directory"
            pattern_context = pattern.context if pattern.context else "No context available"
            
            # Create a prompt for the model that explains the issue and asks for a recommendation
            prompt = f"""I need to fix an issue in a spec file for Azure Linux. Please provide a detailed, specific recommendation.

## Issue Details:
- Type: {pattern.id}
- Name: {pattern.name}
- Description: {pattern.description}
- Severity: {pattern.severity.name}
- File: {pattern.file_path}
- Line number: {pattern.line_number if pattern.line_number else "N/A"}
- Context: {pattern_context}

## Spec File Content:
```
{spec_content[:2000]}  # Truncate to avoid token limits
...
```

## Files in Package Directory:
```
{file_context}
```

## Request:
Please provide a specific, actionable recommendation to fix this issue. Include:
1. A clear explanation of what needs to be changed
2. Code examples where appropriate
3. Reference to specific lines or files that need modification
4. The reasoning behind the recommendation
5. Any alternative approaches if applicable

Your recommendation should follow Azure Linux packaging guidelines and RPM spec best practices."""

            # Call the OpenAI client to get a recommendation
            response = self.openai_client.get_chat_completion(
                system_msg="You are an Azure Linux packaging expert specializing in RPM spec files. Your task is to provide specific, actionable recommendations to fix issues in spec files.",
                user_msg=prompt
            )
            
            # Extract the recommendation from the response
            recommendation = response.get("content", "")
            
            if recommendation:
                return recommendation
            else:
                logger.warning(f"Received empty recommendation from OpenAI")
                return pattern.recommendation
                
        except Exception as e:
            logger.error(f"Error generating recommendation with model: {str(e)}")
            return pattern.recommendation

    def _get_current_date(self) -> str:
        """Get current date in changelog format: Day Month DD YYYY"""
        today = datetime.datetime.now()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        return f"{days[today.weekday()]} {months[today.month-1]} {today.day:02d} {today.year}"
        
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings"""
        # Simple implementation of string similarity
        # For a more sophisticated approach, consider using difflib or Levenshtein distance
        s1, s2 = str1.lower(), str2.lower()
        
        # Handle empty strings
        if not s1 or not s2:
            return 0.0
            
        # Check if one is substring of the other
        if s1 in s2:
            return len(s1) / len(s2)
        if s2 in s1:
            return len(s2) / len(s1)
            
        # Count matching characters
        matches = sum(c1 == c2 for c1, c2 in zip(s1, s2))
        return matches / max(len(s1), len(s2))