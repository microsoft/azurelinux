#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
AntiPatternDetector
------------------
Detects anti-patterns in spec files and related artifacts.

This module provides systematic detection of common problems in spec files,
with configurable severity levels and detailed reporting.

Functions:
----------
detect_all():
    Main entry point that runs all anti-pattern detection methods on a spec file.
    Combines results from patch file, CVE, and changelog issue detection.

detect_patch_file_issues():
    Detects patch file related problems:
    - Missing patch files referenced in spec but not found in directory
    - Unused patch files present in directory but not referenced in spec  
    - CVE patch naming mismatches (CVE-named patches without corresponding CVE documentation)

detect_cve_issues():
    Detects CVE reference related problems:
    - Future-dated CVEs (CVE years beyond current expected range)
    - Missing CVE documentation in changelog (CVEs referenced in spec but not in changelog)
    - Validates CVE format and cross-references with changelog entries

detect_changelog_issues():
    Detects changelog format and content problems:
    - Missing %changelog section entirely
    - Empty changelog sections with no entries
    - Invalid changelog entry format (non-standard RPM changelog format)
    - Validates standard format: * Day Month DD YYYY User <email> - Version

Severity Levels:
---------------
- CRITICAL: Must be fixed before merge
- ERROR: Should be fixed before merge  
- WARNING: Review recommended but doesn't block merge
- INFO: Informational only
"""

import os
import re
import logging
from enum import Enum, auto
from typing import List, Dict, Optional, Any, Set, Tuple
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger("anti-pattern-detector")

class Severity(Enum):
    """Severity levels for anti-patterns"""
    INFO = auto()       # Informational only
    WARNING = auto()    # Warning that should be reviewed
    ERROR = auto()      # Error that should be fixed
    CRITICAL = auto()   # Critical issue that must be fixed

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

@dataclass
class AntiPattern:
    """Represents a detected anti-pattern in a spec file"""
    id: str                     # Unique identifier for this type of anti-pattern
    name: str                   # Human-readable name/title
    description: str            # Detailed description of the problem
    severity: Severity          # Severity level
    file_path: str              # Path to the file with the issue
    line_number: Optional[int]  # Line number (if applicable)
    context: Optional[str]      # Surrounding context from the file
    recommendation: str         # Suggested fix or improvement

class AntiPatternDetector:
    """Detects common anti-patterns in spec files"""
    
    def __init__(self, repo_root: str):
        """
        Initialize the anti-pattern detector.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        logger.info("Initialized AntiPatternDetector")
        
        # Define severity mapping for anti-patterns
        # This allows for easy configuration of severity levels
        self.severity_map = {
            # Patch related issues
            'missing-patch-file': Severity.ERROR,
            'cve-patch-mismatch': Severity.ERROR,
            'unused-patch-file': Severity.WARNING,
            'patch-without-cve-ref': Severity.WARNING,
            
            # CVE related issues
            'missing-cve-reference': Severity.ERROR,
            'invalid-cve-format': Severity.ERROR,
            'future-dated-cve': Severity.ERROR,
            'duplicate-cve-patch': Severity.WARNING,
            
            # Changelog related issues
            'missing-changelog-entry': Severity.ERROR,
            'invalid-changelog-format': Severity.WARNING,
            'missing-cve-in-changelog': Severity.ERROR,
        }

    def detect_all(self, file_path: str, file_content: str, 
                   file_list: List[str]) -> List[AntiPattern]:
        """
        Run all anti-pattern detection methods on a spec file.
        
        Args:
            file_path: Path to the spec file relative to repo root
            file_content: Content of the spec file
            file_list: List of files in the same directory
            
        Returns:
            List of detected anti-patterns
        """
        logger.info(f"Running all anti-pattern detections on {file_path}")
        
        # Combined list of all detected anti-patterns
        all_patterns = []
        
        # Run each detection method and collect results
        all_patterns.extend(self.detect_patch_file_issues(file_content, file_path, file_list))
        all_patterns.extend(self.detect_cve_issues(file_path, file_content))
        all_patterns.extend(self.detect_changelog_issues(file_path, file_content))
        
        # Return combined results
        logger.info(f"Found {len(all_patterns)} anti-patterns in {file_path}")
        return all_patterns

    def _extract_spec_macros(self, spec_content: str) -> dict:
        """
        Extract macro definitions from spec file content.
        
        Parses the spec file to extract macro values defined via:
        - Name: package_name
        - Version: version_number  
        - Release: release_number
        - %global macro_name value
        - %define macro_name value
        
        Args:
            spec_content: Full text content of the spec file
            
        Returns:
            Dictionary mapping macro names to their values
        """
        macros = {}
        
        for line in spec_content.split('\n'):
            line = line.strip()
            
            # Extract Name, Version, Release
            if line.startswith('Name:'):
                macros['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('Version:'):
                macros['version'] = line.split(':', 1)[1].strip()
            elif line.startswith('Release:'):
                # Remove %{?dist} and similar from release
                release = line.split(':', 1)[1].strip()
                release = re.sub(r'%\{[^}]+\}', '', release)  # Remove macros
                macros['release'] = release.strip()
            elif line.startswith('Epoch:'):
                macros['epoch'] = line.split(':', 1)[1].strip()
            
            # Extract %global and %define macros
            global_match = re.match(r'%global\s+(\w+)\s+(.+)', line)
            if global_match:
                macros[global_match.group(1)] = global_match.group(2).strip()
            
            define_match = re.match(r'%define\s+(\w+)\s+(.+)', line)
            if define_match:
                macros[define_match.group(1)] = define_match.group(2).strip()
        
        return macros
    
    def _expand_macros(self, text: str, macros: dict) -> str:
        """
        Expand RPM macros in text using provided macro dictionary.
        
        Handles both %{macro_name} and %macro_name formats.
        Performs recursive expansion (macros can reference other macros).
        
        Args:
            text: Text containing macros to expand
            macros: Dictionary of macro name -> value mappings
            
        Returns:
            Text with macros expanded
        """
        if not text:
            return text
        
        # Maximum iterations to prevent infinite loops
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            original_text = text
            
            # Expand %{macro_name} format
            for macro_name, macro_value in macros.items():
                text = text.replace(f'%{{{macro_name}}}', str(macro_value))
                text = text.replace(f'%{macro_name}', str(macro_value))
            
            # If no changes were made, we're done
            if text == original_text:
                break
                
            iteration += 1
        
        return text

    def detect_patch_file_issues(self, spec_content: str, file_path: str, file_list: List[str]) -> List[AntiPattern]:
        """
        Detect issues related to patch files in spec files.
        
        This function validates patch file references in spec files against the actual
        files present in the package directory. It performs bidirectional validation
        to ensure consistency between spec declarations and filesystem state.
        
        Issues detected:
        ----------------
        1. Missing patch files (ERROR):
           - Patches referenced in spec but not found in directory
           - Example: Patch0: security.patch (but file doesn't exist)
        
        2. Unused patch files (WARNING):
           - .patch files in directory but not referenced in spec
           - Example: old-fix.patch exists but no Patch line references it
        
        3. CVE patch mismatches (ERROR):
           - CVE-named patches without corresponding CVE documentation in spec
           - Example: CVE-2023-1234.patch exists but CVE-2023-1234 not in changelog
        
        Args:
            spec_content: Full text content of the spec file
            file_path: Path to the spec file being analyzed
            file_list: List of all files in the package directory
            
        Returns:
            List of AntiPattern objects representing detected issues
        """
        patterns = []
        
        # Extract macros from spec file
        macros = self._extract_spec_macros(spec_content)
        logger.debug(f"Extracted macros: {macros}")
        
        # Extract patch references from spec file with line numbers
        # Updated regex to handle both simple filenames and full URLs
        patch_regex = r'^Patch(\d+):\s+(.+?)$'
        patch_refs = {}
        
        for line_num, line in enumerate(spec_content.split('\n'), 1):
            match = re.match(patch_regex, line.strip())
            if match:
                patch_file = match.group(2).strip()
                
                # Expand macros in patch filename BEFORE processing
                patch_file_expanded = self._expand_macros(patch_file, macros)
                
                # Extract just the filename from URL if it's a full path
                # Handle URLs like https://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.38-fhs-1.patch
                if '://' in patch_file_expanded:
                    # Extract filename from URL (last part after the final /)
                    patch_file_expanded = patch_file_expanded.split('/')[-1]
                elif '/' in patch_file_expanded:
                    # Handle relative paths like patches/fix.patch
                    patch_file_expanded = patch_file_expanded.split('/')[-1]
                
                # Store both original and expanded for better error messages
                patch_refs[patch_file_expanded] = {
                    'line_num': line_num,
                    'line_content': line.strip(),
                    'original': patch_file,
                    'expanded': patch_file_expanded
                }
        
        # Check for missing patch files (referenced in spec but not in directory)
        for patch_file_expanded, patch_info in patch_refs.items():
            if patch_file_expanded not in file_list:
                # Show both original and expanded in description if they differ
                if patch_info['original'] != patch_info['expanded']:
                    description = (f"Patch file '{patch_info['original']}' "
                                 f"(expands to '{patch_file_expanded}') "
                                 f"referenced in spec but not found in directory")
                else:
                    description = f"Patch file '{patch_file_expanded}' referenced in spec but not found in directory"
                
                patterns.append(AntiPattern(
                    id='missing-patch-file',
                    name="Missing Patch File",
                    description=description,
                    severity=self.severity_map.get('missing-patch-file', Severity.ERROR),
                    file_path=file_path,
                    line_number=patch_info['line_num'],
                    context=patch_info['line_content'],
                    recommendation="Add the missing patch file or update the Patch reference"
                ))
        
        # Check for CVE patch naming conventions
        for patch_file in file_list:
            if patch_file.endswith('.patch'):
                # Check if patch exists in spec file
                if patch_file not in patch_refs:
                    patterns.append(AntiPattern(
                        id='unused-patch-file',
                        name="Unused Patch File",
                        description=f"Patch file '{patch_file}' exists in directory but is not referenced in spec",
                        severity=self.severity_map.get('unused-patch-file', Severity.WARNING),
                        file_path=file_path,
                        line_number=None,
                        context=None,
                        recommendation="Add a reference to the patch file or remove it if not needed"
                    ))
                
                # Check for CVE-named patches
                if patch_file.startswith('CVE-'):
                    cve_match = re.search(r'(CVE-\d{4}-\d+)', patch_file)
                    if cve_match:
                        cve_id = cve_match.group(1)
                        if cve_id not in spec_content:
                            patterns.append(AntiPattern(
                                id='cve-patch-mismatch',
                                name="CVE Patch Mismatch",
                                description=f"Patch file '{patch_file}' contains CVE reference but {cve_id} is not mentioned in spec",
                                severity=self.severity_map.get('cve-patch-mismatch', Severity.ERROR),
                                file_path=file_path,
                                line_number=None,
                                context=None,
                                recommendation=f"Add {cve_id} to the spec file changelog entry"
                            ))
        
        return patterns
    
    def detect_cve_issues(self, file_path: str, file_content: str) -> List[AntiPattern]:
        """
        Detect issues related to CVE references.
        
        Args:
            file_path: Path to the spec file relative to repo root
            file_content: Content of the spec file
            
        Returns:
            List of detected CVE-related anti-patterns
        """
        patterns = []
        
        # Extract all CVE references
        cve_pattern = r'CVE-(\d{4})-(\d{4,})'
        cve_matches = list(re.finditer(cve_pattern, file_content))
        
        # Skip if no CVE references (may not be a security update)
        if not cve_matches:
            return patterns
        
        # Check for duplicate CVEs
        seen_cves = set()
        for match in cve_matches:
            cve_id = match.group(0)
            if cve_id in seen_cves:
                continue
                
            seen_cves.add(cve_id)
            
            # Get line number for context
            line_num = file_content[:match.start()].count('\n') + 1
            line = file_content.splitlines()[line_num - 1]
            
            # Check future-dated CVEs
            year = int(match.group(1))
            if year > 2026:  # Adjust this date as needed
                patterns.append(AntiPattern(
                    id='future-dated-cve',
                    name="Future-Dated CVE",
                    description=f"CVE {cve_id} appears to be from the future (year {year})",
                    severity=self.severity_map.get('future-dated-cve', Severity.ERROR),
                    file_path=file_path,
                    line_number=line_num,
                    context=line.strip(),
                    recommendation="Check if the CVE year is correct"
                ))
        
        # Check changelog for CVE references
        changelog_pattern = r'%changelog(.*?)$'
        changelog_match = re.search(changelog_pattern, file_content, re.DOTALL)
        
        if changelog_match:
            changelog_text = changelog_match.group(1)
            
            # Check entire changelog for CVE mentions, not just latest entry
            # We consider any CVE mentioned anywhere in the changelog to be properly documented
            missing_cves = set()
            for cve_id in seen_cves:
                if cve_id not in changelog_text:
                    # This CVE is not mentioned in any changelog entry
                    missing_cves.add(cve_id)
            
            # Report only CVEs that are truly missing from the entire changelog
            for cve_id in missing_cves:
                patterns.append(AntiPattern(
                    id='missing-cve-in-changelog',
                    name="Missing CVE in Changelog",
                    description=f"{cve_id} is referenced in the spec file but not mentioned in any changelog entry",
                    severity=self.severity_map.get('missing-cve-in-changelog', Severity.ERROR),
                    file_path=file_path,
                    line_number=None,
                    context=None,
                    recommendation=f"Add {cve_id} to a changelog entry"
                ))
        
        return patterns
    
    def detect_changelog_issues(self, file_path: str, file_content: str) -> List[AntiPattern]:
        """
        Detect issues related to the changelog.
        
        Args:
            file_path: Path to the spec file relative to repo root
            file_content: Content of the spec file
            
        Returns:
            List of detected changelog-related anti-patterns
        """
        patterns = []
        
        # Check if changelog exists
        if '%changelog' not in file_content:
            patterns.append(AntiPattern(
                id='missing-changelog-entry',
                name="Missing Changelog",
                description="Spec file does not contain a %changelog section",
                severity=self.severity_map.get('missing-changelog-entry', Severity.ERROR),
                file_path=file_path,
                line_number=None,
                context=None,
                recommendation="Add a %changelog section to the spec file"
            ))
            return patterns  # Can't do further changelog checks
            
        # Extract changelog
        changelog_pattern = r'%changelog(.*?)$'
        changelog_match = re.search(changelog_pattern, file_content, re.DOTALL)
        
        if changelog_match:
            changelog_text = changelog_match.group(1).strip()
            
            # Check if changelog follows expected format
            entry_pattern = r'\*\s+\w+\s+\w+\s+\d+\s+\d{4}'
            entries = re.finditer(entry_pattern, changelog_text)
            
            entry_found = False
            for entry_match in entries:
                entry_found = True
                entry_text = entry_match.group(0)
                line_num = file_content[:entry_match.start()].count('\n') + 1
                
                # Check if entry has standard format
                if not re.match(r'\*\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+[A-Z][a-z]+\s+\d{1,2}\s+\d{4}', entry_text):
                    patterns.append(AntiPattern(
                        id='invalid-changelog-format',
                        name="Invalid Changelog Format",
                        description=f"Changelog entry '{entry_text}' does not follow standard format",
                        severity=self.severity_map.get('invalid-changelog-format', Severity.WARNING),
                        file_path=file_path,
                        line_number=line_num,
                        context=entry_text,
                        recommendation="Use standard format: * Day Month DD YYYY User <email> - Version"
                    ))
                
            if not entry_found:
                patterns.append(AntiPattern(
                    id='missing-changelog-entry',
                    name="Empty Changelog",
                    description="Spec file has a %changelog section but no entries",
                    severity=self.severity_map.get('missing-changelog-entry', Severity.ERROR),
                    file_path=file_path,
                    line_number=None,
                    context=None,
                    recommendation="Add changelog entries for all changes"
                ))
        
        return patterns