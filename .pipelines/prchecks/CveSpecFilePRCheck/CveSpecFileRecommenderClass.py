#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
CveSpecFileRecommenderClass analyzes git diffs from PR changes
and provides recommendations using Azure OpenAI, with comprehensive
context including file listings and spec content analysis.
"""

import os
import sys
import re
import subprocess
import glob
from pathlib import Path
from GptModelConfigClass import GptModelConfig
from OpenAIClientClass import OpenAIClient
from PromptTemplatesClass import PromptTemplates

def gather_diff():
    """
    Extracts the diff between source and target commits for a PR.
    Uses environment variables set by Azure DevOps pipeline.
    """
    src = os.environ["SYSTEM_PULLREQUEST_SOURCECOMMITID"]
    tgt = os.environ["SYSTEM_PULLREQUEST_TARGETCOMMITID"]
    diff = subprocess.check_output(
        ["git", "diff", "--unified=3", tgt, src],
        cwd=os.environ["BUILD_SOURCESDIRECTORY"]
    )
    return diff.decode()

def get_changed_spec_files(diff_text):
    """
    Extracts the paths of changed .spec files from the diff.
    
    Args:
        diff_text: Git diff output as text
    
    Returns:
        List of changed spec file paths
    """
    spec_files = []
    lines = diff_text.splitlines()
    
    for line in lines:
        if line.startswith('+++ b/') and line.endswith('.spec'):
            path = line[6:]  # Remove '+++ b/' prefix
            spec_files.append(path)
    
    return spec_files

def get_spec_file_content(spec_path):
    """
    Gets the full content of a spec file.
    
    Args:
        spec_path: Path to the spec file
    
    Returns:
        Content of the spec file as string
    """
    full_path = os.path.join(os.environ["BUILD_SOURCESDIRECTORY"], spec_path)
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ Warning: Could not read spec file {spec_path}: {str(e)}")
        return None

def get_package_directory_files(spec_path):
    """
    Lists all files in the directory containing the spec file.
    
    Args:
        spec_path: Path to the spec file
    
    Returns:
        List of files in the package directory
    """
    dir_path = os.path.dirname(os.path.join(os.environ["BUILD_SOURCESDIRECTORY"], spec_path))
    try:
        files = os.listdir(dir_path)
        return files
    except Exception as e:
        print(f"⚠️ Warning: Could not list files in directory {dir_path}: {str(e)}")
        return []

def extract_cve_ids(spec_content):
    """
    Extracts CVE IDs mentioned in the spec file.
    
    Args:
        spec_content: Content of the spec file
    
    Returns:
        List of CVE IDs
    """
    if not spec_content:
        return []
    
    # Match CVE-YYYY-NNNNN patterns
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    cve_ids = re.findall(cve_pattern, spec_content, re.IGNORECASE)
    
    # Deduplicate and sort
    return sorted(list(set(cve_ids)))

def extract_patch_references(spec_content):
    """
    Extracts patch references from the spec file (Patch0, Patch1, etc.)
    
    Args:
        spec_content: Content of the spec file
    
    Returns:
        Dictionary of patch numbers to filenames
    """
    if not spec_content:
        return {}
    
    # Match Patch<N>: filename patterns
    patch_pattern = r'^Patch(\d+):\s+(.+?)$'
    patches = {}
    
    for line in spec_content.splitlines():
        match = re.match(patch_pattern, line.strip())
        if match:
            patch_num = int(match.group(1))
            filename = match.group(2).strip()
            patches[patch_num] = filename
    
    return patches

def extract_changelog_cves(spec_content):
    """
    Extracts CVE IDs mentioned in the changelog section.
    
    Args:
        spec_content: Content of the spec file
    
    Returns:
        List of CVE IDs from changelog
    """
    if not spec_content:
        return []
    
    # Extract %changelog section
    changelog_section = None
    lines = spec_content.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == '%changelog':
            changelog_section = '\n'.join(lines[i:])
            break
    
    if not changelog_section:
        return []
    
    # Match CVE-YYYY-NNNNN patterns in changelog
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    cve_ids = re.findall(cve_pattern, changelog_section, re.IGNORECASE)
    
    # Deduplicate and sort
    return sorted(list(set(cve_ids)))

def get_patch_files(file_list):
    """
    Filters the file list to only include patch files.
    
    Args:
        file_list: List of files
    
    Returns:
        List of patch files
    """
    return [f for f in file_list if f.endswith('.patch')]

def check_patch_references(patch_refs, patch_files):
    """
    Compares patch references in spec with actual patch files.
    
    Args:
        patch_refs: Dictionary of patch numbers to filenames
        patch_files: List of patch files in directory
    
    Returns:
        Dictionary with analysis of missing and unreferenced patches
    """
    missing_patches = []
    for _, filename in patch_refs.items():
        if filename not in patch_files:
            missing_patches.append(filename)
    
    unreferenced_patches = []
    for filename in patch_files:
        if filename not in patch_refs.values():
            unreferenced_patches.append(filename)
    
    return {
        'missing_patches': missing_patches,
        'unreferenced_patches': unreferenced_patches
    }

def validate_cve_patches(cve_ids, patch_files, patch_refs):
    """
    Validates that CVE IDs have corresponding patch files.
    
    Args:
        cve_ids: List of CVE IDs from spec file
        patch_files: List of patch files in directory
        patch_refs: Dictionary of patch references
    
    Returns:
        Dictionary with validation results
    """
    cve_patches = {}
    missing_cves = []
    
    # Map CVEs to patch files
    for cve_id in cve_ids:
        cve_patch_found = False
        for patch_file in patch_files:
            if cve_id.lower() in patch_file.lower():
                cve_patches[cve_id] = patch_file
                cve_patch_found = True
                break
        
        if not cve_patch_found:
            missing_cves.append(cve_id)
    
    # Check patch references for CVEs
    unreferenced_cve_patches = []
    for patch_file in patch_files:
        if re.search(r'cve-\d{4}-\d{4,7}', patch_file.lower()):
            if patch_file not in patch_refs.values():
                unreferenced_cve_patches.append(patch_file)
    
    return {
        'cve_patches': cve_patches,
        'missing_cves': missing_cves,
        'unreferenced_cve_patches': unreferenced_cve_patches
    }

def call_openai(diff_text, changed_spec_files):
    """
    Calls Azure OpenAI to analyze the diff text and spec files.
    Uses PromptTemplates for comprehensive analysis.
    """
    # Read environment variables (set by run-pr-check.sh)
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "o3-mini")  # Default to o3-mini if not specified

    # Validate environment variables
    if not all([api_base, deployment_name]):
        print("❌ Missing required environment variables")
        print("Required: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME")
        sys.exit(1)

    print(f"🔗 API Endpoint: {api_base}")
    print(f"🚀 Deployment: {deployment_name}")
    print(f"🤖 Model: {model_name}")
    print(f"📄 API Version: {api_version}")

    try:
        # Create model configuration
        model_config = GptModelConfig(
            model_name=model_name,
            api_version=api_version,
            api_base=api_base,
            deployment_name=deployment_name
        )
        
        # Initialize client
        client = OpenAIClient(model_config)
        
        # If no spec files have changed, do basic diff analysis
        if not changed_spec_files:
            print("📋 No spec files found in the diff, performing basic analysis...")
            response = client.get_chat_completion(
                system_msg=PromptTemplates.get_system_prompt(),
                user_msg=f"Review this diff from a pull request that modifies .spec or .patch files:\n```diff\n{diff_text}\n```"
            )
            return response["content"]
            
        # Process each changed spec file with enhanced context
        results = []
        for spec_path in changed_spec_files:
            print(f"🔍 Analyzing spec file: {spec_path}")
            
            # Gather comprehensive context for analysis
            spec_content = get_spec_file_content(spec_path)
            file_list = get_package_directory_files(spec_path)
            
            if not spec_content:
                print(f"⚠️ Could not read spec file content for {spec_path}, skipping detailed analysis")
                continue
            
            # Extract references, IDs, and patches for validation
            patch_files = get_patch_files(file_list)
            patch_refs = extract_patch_references(spec_content)
            cve_ids = extract_cve_ids(spec_content)
            changelog_cves = extract_changelog_cves(spec_content)
            
            # Merge all CVE IDs for analysis
            all_cves = sorted(list(set(cve_ids + changelog_cves)))
            
            print(f"📊 Found {len(all_cves)} CVE IDs, {len(patch_files)} patch files, and {len(patch_refs)} patch references")
            
            # Perform validation checks
            patch_check = check_patch_references(patch_refs, patch_files)
            cve_validation = validate_cve_patches(all_cves, patch_files, patch_refs)
            
            # Pre-analysis summary for debugging
            if patch_check['missing_patches']:
                print(f"⚠️ Warning: {len(patch_check['missing_patches'])} patch files referenced in spec but missing in directory")
            
            if patch_check['unreferenced_patches']:
                print(f"⚠️ Warning: {len(patch_check['unreferenced_patches'])} patch files in directory but not referenced in spec")
            
            if cve_validation['missing_cves']:
                print(f"⚠️ Warning: {len(cve_validation['missing_cves'])} CVE IDs mentioned without corresponding patch files")
            
            # Build patch references string for prompt
            patch_refs_str = "\n".join([f"Patch{num}: {filename}" for num, filename in patch_refs.items()])
            
            # Get general spec analysis
            response = client.get_chat_completion(
                system_msg=PromptTemplates.get_system_prompt(),
                user_msg=PromptTemplates.get_spec_analysis_prompt(
                    diff_text=diff_text,
                    file_list="\n".join(file_list),
                    spec_content=spec_content
                )
            )
            
            results.append(f"## Analysis for {spec_path}\n\n{response['content']}")
            
            # If CVE IDs or patch references exist, do specific validations
            if all_cves or patch_refs:
                # Patch verification
                if patch_refs:
                    print(f"🔍 Performing patch verification for {len(patch_refs)} patch references...")
                    patch_response = client.get_chat_completion(
                        system_msg=PromptTemplates.get_system_prompt(),
                        user_msg=PromptTemplates.get_patch_verification_prompt(
                            spec_content=spec_content,
                            file_list="\n".join(file_list),
                            patch_references=patch_refs_str
                        )
                    )
                    results.append(f"## Patch Verification for {spec_path}\n\n{patch_response['content']}")
                
                # CVE validation if CVEs are present
                if all_cves:
                    print(f"🛡️ Performing CVE validation for {len(all_cves)} CVE IDs...")
                    cve_response = client.get_chat_completion(
                        system_msg=PromptTemplates.get_system_prompt(),
                        user_msg=PromptTemplates.get_cve_validation_prompt(
                            diff_text=diff_text,
                            spec_content=spec_content,
                            cve_ids="\n".join(all_cves),
                            patch_files="\n".join(patch_files)
                        )
                    )
                    results.append(f"## CVE Validation for {spec_path}\n\n{cve_response['content']}")
        
        # Join all results
        return "\n\n" + "\n\n---\n\n".join(results)
        
    except Exception as e:
        print(f"❌ Error calling Azure OpenAI: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the script"""
    print("🔍 Gathering git diff between source and target commits...")
    diff = gather_diff()
    
    if not diff.strip():
        print("⚠️ No changes detected in the diff.")
        sys.exit(0)
    
    print(f"📄 Found diff of {len(diff.splitlines())} lines")
    
    # Extract changed spec files from diff
    changed_spec_files = get_changed_spec_files(diff)
    print(f"🔍 Found {len(changed_spec_files)} changed spec files in the diff")
    
    print("🧠 Sending to Azure OpenAI for comprehensive analysis...")
    
    review = call_openai(diff, changed_spec_files)
    
    print("\n💬 LLM REVIEW RESULTS:")
    print("=" * 80)
    print(review)
    print("=" * 80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
