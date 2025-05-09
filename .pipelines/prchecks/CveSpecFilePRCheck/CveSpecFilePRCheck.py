#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
CveSpecFilePRCheck
-----------------
Main entry point for the CVE Spec File PR check pipeline.

This module integrates anti-pattern detection with Azure OpenAI analysis to
provide a comprehensive check of spec files in pull requests. It will fail
the pipeline explicitly when critical issues are detected, with detailed
output explaining the problems.
"""

import os
import sys
import logging
import json
import argparse
from pathlib import Path
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple

from GptModelConfigClass import GptModelConfig
from OpenAIClientClass import OpenAIClient
from PromptTemplatesClass import PromptTemplates
from AntiPatternDetector import AntiPatternDetector, AntiPattern, Severity
from ResultAnalyzer import ResultAnalyzer
from FixRecommender import FixRecommender
from GitHubClient import GitHubClient, CheckStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("cve-spec-check")

# Define exit codes
EXIT_SUCCESS = 0
EXIT_CRITICAL = 1
EXIT_ERROR = 2
EXIT_WARNING = 3
EXIT_FATAL = 10

def gather_diff() -> str:
    """
    Extracts the diff between source and target commits for a PR.
    Uses environment variables set by Azure DevOps pipeline.
    """
    logger.info("Gathering git diff between source and target commits...")
    
    try:
        # Get commit IDs from environment variables
        src_commit = os.environ.get("SYSTEM_PULLREQUEST_SOURCECOMMITID")
        tgt_commit = os.environ.get("SYSTEM_PULLREQUEST_TARGETCOMMITID")
        repo_path = os.environ.get("BUILD_SOURCESDIRECTORY")
        
        # Log the commit IDs we're using
        logger.info(f"Source commit: {src_commit}")
        logger.info(f"Target commit: {tgt_commit}")
        
        if not src_commit or not tgt_commit:
            raise ValueError("Source or target commit ID not found in environment variables")
        
        # First try to ensure we have the refs - a depth of 1 is sufficient
        try:
            logger.info("Fetching source+target commits with depth=1…")
            subprocess.check_call(
                [
                  "git", "fetch",
                  "--depth=1", "--no-tags", "origin",
                  src_commit, tgt_commit
                ],
                cwd=repo_path,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            logger.warning("Could not fetch one or both commits; proceeding anyway")
            
        # Try to get the diff directly using commit IDs (most reliable)
        logger.info("Generating diff between commits...")
        try:
            diff = subprocess.check_output(
                ["git", "diff", "--unified=3", tgt_commit, src_commit],
                cwd=repo_path,
                stderr=subprocess.PIPE  # Capture stderr to avoid polluting the logs
            )
            return diff.decode()
        except subprocess.CalledProcessError as e:
            logger.warning(f"Direct diff failed: {str(e)}")
            
            # Try alternative: find the merge base and diff from there
            logger.info("Trying alternative diff method using merge-base...")
            try:
                # Find the best common ancestor for the diff
                merge_base = subprocess.check_output(
                    ["git", "merge-base", src_commit, tgt_commit], 
                    cwd=repo_path
                ).decode().strip()
                
                logger.info(f"Found merge base: {merge_base}")
                
                # Get the diff from the merge base to our source commit
                diff = subprocess.check_output(
                    ["git", "diff", "--unified=3", merge_base, src_commit],
                    cwd=repo_path
                )
                return diff.decode()
            except subprocess.CalledProcessError as e:
                logger.error(f"Alternative diff method failed: {str(e)}")
                
                # Last resort: check if this is a new branch with just one commit
                logger.info("Checking if this is a new branch with a single commit...")
                try:
                    # If this is a new branch with just one commit, get that commit's changes
                    diff = subprocess.check_output(
                        ["git", "show", "--unified=3", src_commit],
                        cwd=repo_path
                    )
                    return diff.decode()
                except subprocess.CalledProcessError as e:
                    logger.error(f"All diff methods failed: {str(e)}")
                    raise ValueError("Could not generate a diff between the source and target commits")
                    
    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"Git diff command failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error gathering git diff: {e}")
        raise

def get_changed_spec_files(diff_text: str) -> List[str]:
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
    
    logger.info(f"Found {len(spec_files)} changed spec files")
    return spec_files

def get_spec_file_content(spec_path: str) -> Optional[str]:
    """
    Gets the full content of a spec file.
    
    Args:
        spec_path: Path to the spec file relative to repo root
    
    Returns:
        Content of the spec file as string, or None if file not found
    """
    full_path = os.path.join(os.environ["BUILD_SOURCESDIRECTORY"], spec_path)
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.warning(f"Could not read spec file {spec_path}: {str(e)}")
        return None

def get_package_directory_files(spec_path: str) -> List[str]:
    """
    Lists all files in the directory containing the spec file.
    
    Args:
        spec_path: Path to the spec file relative to repo root
    
    Returns:
        List of files in the package directory
    """
    dir_path = os.path.dirname(os.path.join(os.environ["BUILD_SOURCESDIRECTORY"], spec_path))
    try:
        return os.listdir(dir_path)
    except Exception as e:
        logger.warning(f"Could not list files in directory {dir_path}: {str(e)}")
        return []

def analyze_spec_files(diff_text: str, changed_spec_files: List[str]) -> Tuple[List[AntiPattern], str, bool]:
    """
    Analyzes spec files for anti-patterns and issues.
    
    Args:
        diff_text: Git diff output as text
        changed_spec_files: List of changed spec file paths
        
    Returns:
        Tuple containing:
        - List of detected anti-patterns
        - OpenAI analysis results
        - Boolean indicating if fatal errors occurred
    """
    repo_root = os.environ["BUILD_SOURCESDIRECTORY"]
    detector = AntiPatternDetector(repo_root)
    all_anti_patterns = []
    ai_analysis = ""
    
    try:
        # Initialize OpenAI client for analysis and recommendations
        openai_client = _initialize_openai_client()
        
        # Call OpenAI for analysis
        ai_analysis = call_openai(openai_client, diff_text, changed_spec_files)
        
        # Initialize FixRecommender with the OpenAI client for dynamic recommendations
        fix_recommender = FixRecommender(openai_client)
        
        # Early exit if no spec files changed
        if not changed_spec_files:
            return [], ai_analysis, False
            
        # Process each changed spec file for anti-patterns
        for spec_path in changed_spec_files:
            logger.info(f"Running anti-pattern detection on: {spec_path}")
            
            spec_content = get_spec_file_content(spec_path)
            if not spec_content:
                logger.warning(f"Could not read spec file content for {spec_path}, skipping detailed analysis")
                continue
                
            file_list = get_package_directory_files(spec_path)
            
            # Detect anti-patterns
            anti_patterns = detector.detect_all(spec_path, spec_content, file_list)
            
            # Enhance recommendations with the FixRecommender
            if anti_patterns:
                logger.info(f"Enhancing recommendations for {len(anti_patterns)} anti-patterns")
                anti_patterns = fix_recommender.enhance_recommendations(anti_patterns, spec_content, file_list)
            
            all_anti_patterns.extend(anti_patterns)
            
            # Log detected issues
            if anti_patterns:
                critical_count = sum(1 for p in anti_patterns if p.severity >= Severity.ERROR)
                warning_count = sum(1 for p in anti_patterns if p.severity == Severity.WARNING)
                
                logger.warning(f"Found {len(anti_patterns)} anti-patterns in {spec_path}:")
                logger.warning(f"   - {critical_count} critical/error issues")
                logger.warning(f"   - {warning_count} warnings")
            else:
                logger.info(f"No anti-patterns detected in {spec_path}")
        
        return all_anti_patterns, ai_analysis, False
        
    except Exception as e:
        logger.error(f"Error in analyze_spec_files: {str(e)}", exc_info=True)
        return all_anti_patterns, ai_analysis, True

def _initialize_openai_client() -> OpenAIClient:
    """
    Initializes and returns an OpenAI client for analysis and recommendations.
    
    Returns:
        Initialized OpenAIClient instance
    """
    # Read environment variables
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "o3-mini")  # Default to o3-mini if not specified

    # Validate environment variables
    if not all([api_base, deployment_name]):
        logger.error("Missing required environment variables")
        logger.error("Required: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME")
        raise ValueError("Missing required environment variables for Azure OpenAI")

    logger.info(f"API Endpoint: {api_base}")
    logger.info(f"Deployment: {deployment_name}")
    logger.info(f"Model: {model_name}")
    logger.info(f"API Version: {api_version}")

    # Create model configuration
    model_config = GptModelConfig(
        model_name=model_name,
        api_version=api_version,
        api_base=api_base,
        deployment_name=deployment_name
    )
    
    # Initialize client
    return OpenAIClient(model_config)

def call_openai(openai_client: OpenAIClient, diff_text: str, changed_spec_files: List[str]) -> str:
    """
    Calls Azure OpenAI to analyze the diff text and spec files.
    Uses PromptTemplates for comprehensive analysis.
    
    Args:
        openai_client: Initialized OpenAIClient for API calls
        diff_text: Git diff output as text
        changed_spec_files: List of changed spec file paths
        
    Returns:
        Analysis results from Azure OpenAI
    """
    try:
        # If no spec files have changed, do basic diff analysis
        if not changed_spec_files:
            logger.info("No spec files found in the diff, performing basic analysis...")
            response = openai_client.get_chat_completion(
                system_msg=PromptTemplates.get_system_prompt(),
                user_msg=f"Review this diff from a pull request that modifies .spec or .patch files:\n```diff\n{diff_text}\n```"
            )
            return response["content"]
            
        # Process each changed spec file with enhanced context
        results = []
        for spec_path in changed_spec_files:
            logger.info(f"Analyzing spec file: {spec_path}")
            
            # Gather comprehensive context for analysis
            spec_content = get_spec_file_content(spec_path)
            file_list = get_package_directory_files(spec_path)
            
            if not spec_content:
                logger.warning(f"Could not read spec file content for {spec_path}, skipping detailed analysis")
                continue
            
            # Get general spec analysis
            response = openai_client.get_chat_completion(
                system_msg=PromptTemplates.get_system_prompt(),
                user_msg=PromptTemplates.get_spec_analysis_prompt(
                    diff_text=diff_text,
                    file_list="\n".join(file_list),
                    spec_content=spec_content
                )
            )
            
            results.append(f"## Analysis for {spec_path}\n\n{response['content']}")
            
            # Extract patch references for patch verification
            patch_pattern = r'^Patch(\d+):\s+(.+?)$'
            patch_refs = {}
            for line in spec_content.splitlines():
                match = re.match(patch_pattern, line.strip())
                if match:
                    patch_num = match.group(1)
                    filename = match.group(2).strip()
                    patch_refs[patch_num] = filename
            
            # Extract CVE IDs for CVE validation
            cve_pattern = r'CVE-\d{4}-\d{4,}'
            cve_ids = sorted(list(set(re.findall(cve_pattern, spec_content, re.IGNORECASE))))
            
            # Get patch files
            patch_files = [f for f in file_list if f.endswith('.patch')]
            
            # If patch references exist, do patch verification
            if patch_refs:
                patch_refs_str = "\n".join([f"Patch{num}: {filename}" for num, filename in patch_refs.items()])
                
                logger.info(f"Performing patch verification for {len(patch_refs)} patch references...")
                patch_response = openai_client.get_chat_completion(
                    system_msg=PromptTemplates.get_system_prompt(),
                    user_msg=PromptTemplates.get_patch_verification_prompt(
                        spec_content=spec_content,
                        file_list="\n".join(file_list),
                        patch_references=patch_refs_str
                    )
                )
                results.append(f"## Patch Verification for {spec_path}\n\n{patch_response['content']}")
            
            # If CVE IDs exist, do CVE validation
            if cve_ids:
                logger.info(f"Performing CVE validation for {len(cve_ids)} CVE IDs...")
                cve_response = openai_client.get_chat_completion(
                    system_msg=PromptTemplates.get_system_prompt(),
                    user_msg=PromptTemplates.get_cve_validation_prompt(
                        diff_text=diff_text,
                        spec_content=spec_content,
                        cve_ids="\n".join(cve_ids),
                        patch_files="\n".join(patch_files)
                    )
                )
                results.append(f"## CVE Validation for {spec_path}\n\n{cve_response['content']}")
        
        # Join all results
        return "\n\n" + "\n\n---\n\n".join(results)
        
    except Exception as e:
        logger.error(f"Error calling Azure OpenAI: {str(e)}", exc_info=True)
        raise

def get_severity_exit_code(severity: Severity) -> int:
    """
    Map severity level to appropriate exit code.
    
    Args:
        severity: The highest severity level detected
        
    Returns:
        Exit code corresponding to the severity level
    """
    if severity == Severity.CRITICAL:
        return EXIT_CRITICAL
    elif severity == Severity.ERROR:
        return EXIT_ERROR
    elif severity == Severity.WARNING:
        return EXIT_WARNING
    else:  # INFO or no issues
        return EXIT_SUCCESS

def update_github_status(severity: Severity, anti_patterns: List[AntiPattern], ai_analysis: str, 
                        analyzer: ResultAnalyzer, post_comments: bool = True, use_checks_api: bool = True) -> None:
    """
    Updates GitHub with PR check status and optionally posts comments.
    
    Args:
        severity: Highest severity level detected
        anti_patterns: List of anti-patterns detected
        ai_analysis: AI-generated analysis text
        analyzer: ResultAnalyzer instance for generating reports
        post_comments: Whether to post comments on GitHub PR
        use_checks_api: Whether to use GitHub Checks API
    """
    # Skip GitHub updates if environment variables aren't set
    if not os.environ.get("GITHUB_ACCESS_TOKEN"):
        logger.warning("GITHUB_ACCESS_TOKEN not set, skipping GitHub updates")
        return
    
    # Get commit SHA from environment
    commit_sha = os.environ.get("SYSTEM_PULLREQUEST_SOURCECOMMITID")
    if not commit_sha:
        logger.warning("SYSTEM_PULLREQUEST_SOURCECOMMITID not set, skipping GitHub updates")
        return
    
    try:
        # Initialize GitHub client
        github_client = GitHubClient()
        
        # Convert anti-patterns to dictionaries for the comment formatter
        issues_dict = []
        for pattern in anti_patterns:
            issues_dict.append({
                "id": pattern.id if hasattr(pattern, 'id') else "",
                "name": pattern.name,
                "description": pattern.description,
                "severity": pattern.severity.name,
                "recommendation": pattern.recommendation,
                "file_path": pattern.file_path if hasattr(pattern, 'file_path') else "",
                "line_number": pattern.line_number if hasattr(pattern, 'line_number') else ""
            })
        
        # Post or update comment if enabled
        if post_comments:
            logger.info("Posting GitHub PR comment with analysis results...")
            comment_body = github_client.format_severity_comment(severity, issues_dict, ai_analysis)
            github_client.post_or_update_comment(comment_body, "azure-linux-spec-check")
            
            # Extract and post conclusion as a separate comment
            logger.info("Posting conclusion as a separate comment...")
            conclusion = analyzer.extract_conclusion()
            if conclusion:
                github_client.post_or_update_comment(conclusion, "azure-linux-spec-check-conclusion")
            else:
                logger.warning("No conclusion section found to post as a separate comment")
        
        # Create or update status using the Checks API if enabled
        if use_checks_api:
            logger.info("Updating GitHub PR status based on severity...")
            github_client.create_severity_status(severity, commit_sha)
        
        logger.info("GitHub updates completed successfully")
    
    except Exception as e:
        logger.error(f"Failed to update GitHub status: {str(e)}")
        # Continue execution - GitHub updates shouldn't cause pipeline failure

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="CVE Spec File PR Check")
    parser.add_argument('--fail-on-warnings', action='store_true', 
                      help='Fail the pipeline even when only warnings are detected')
    parser.add_argument('--exit-code-severity', action='store_true', 
                      help='Use different exit codes based on severity (0=success, 1=critical, 2=error, 3=warning)')
    parser.add_argument('--post-github-comments', action='store_true',
                      help='Post analysis results as comments on GitHub PR')
    parser.add_argument('--use-github-checks', action='store_true',
                      help='Use GitHub Checks API for multi-level notifications')
    args = parser.parse_args()
    
    try:
        # Gather git diff
        diff = gather_diff()
        
        if not diff.strip():
            logger.warning("No changes detected in the diff.")
            return EXIT_SUCCESS
        
        logger.info(f"Found diff of {len(diff.splitlines())} lines")
        
        # Extract changed spec files from diff
        changed_spec_files = get_changed_spec_files(diff)
        logger.info(f"Found {len(changed_spec_files)} changed spec files in the diff")
        
        # Run analysis on spec files
        anti_patterns, ai_analysis, fatal_error = analyze_spec_files(diff, changed_spec_files)
        
        # Process results
        analyzer = ResultAnalyzer(anti_patterns, ai_analysis)
        
        # Print summary to console
        print("\n" + analyzer.generate_console_summary())
        
        # Print detailed report
        detailed_report = analyzer.generate_detailed_report()
        print("\n" + detailed_report)
        
        # Save detailed report to file
        report_file = os.path.join(os.getcwd(), "spec_analysis_report.txt")
        with open(report_file, "w") as f:
            f.write(detailed_report)
        logger.info(f"Detailed analysis report saved to {report_file}")
        
        # Save JSON report
        json_file = os.path.join(os.getcwd(), "spec_analysis_report.json")
        with open(json_file, "w") as f:
            f.write(analyzer.to_json())
        logger.info(f"JSON analysis report saved to {json_file}")
        
        # Determine exit code
        if fatal_error:
            logger.error("Fatal error occurred during analysis")
            return EXIT_FATAL
            
        # Get highest severity
        highest_severity = analyzer.get_highest_severity()
        
        # Update GitHub status if requested
        update_github_status(
            highest_severity, 
            anti_patterns, 
            ai_analysis,
            analyzer,
            post_comments=args.post_github_comments,
            use_checks_api=args.use_github_checks
        )
        
        if args.exit_code_severity:
            # Return different exit codes based on severity
            exit_code = get_severity_exit_code(highest_severity)
            
            # Log exit details
            if exit_code == EXIT_SUCCESS:
                logger.info("Analysis completed successfully - no issues detected")
            else:
                severity_name = highest_severity.name
                logger.warning(f"Analysis completed with highest severity: {severity_name} (exit code {exit_code})")
                
            return exit_code
        else:
            # Traditional exit behavior (0 = success, 1 = failure)
            # Determine if we should fail based on severity and fail_on_warnings flag
            should_fail = False
            
            if highest_severity >= Severity.ERROR:
                # Always fail on ERROR or CRITICAL
                should_fail = True
            elif highest_severity == Severity.WARNING and args.fail_on_warnings:
                # Fail on WARNING only if fail_on_warnings is True
                should_fail = True
                
            if should_fail:
                error_message = analyzer.generate_error_message()
                print("\n" + error_message)
                return EXIT_CRITICAL  # Traditional error exit code
            else:
                logger.info("Analysis completed - no critical issues detected")
                return EXIT_SUCCESS
        
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return EXIT_FATAL

if __name__ == "__main__":
    sys.exit(main())