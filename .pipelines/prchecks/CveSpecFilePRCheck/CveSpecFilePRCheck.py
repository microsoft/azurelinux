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

Functions Overview:
------------------



gather_diff():
    Extracts git diff between source and target commits for a PR using Azure DevOps environment variables.
    Handles multiple fallback strategies for diff generation and provides detailed commit context.

    * Git Commit Context:
        - Source Commit: The latest commit on the feature branch being proposed for merge
        - Target Commit: The latest commit on the destination branch (e.g., main) that the PR targets

get_changed_spec_files(diff_text):
    Parses git diff output to identify .spec files that have been modified in the PR.
    Returns list of spec file paths for focused analysis.

get_spec_file_content(spec_path):
    Reads and returns the complete content of a spec file from the filesystem.
    Handles file access errors gracefully with logging.

get_package_directory_files(spec_path):
    Lists all files in the directory containing a spec file (package directory).
    Used to identify patch files and other package artifacts for validation.

analyze_spec_files(diff_text, changed_spec_files):
    Main analysis orchestrator that combines anti-pattern detection with AI analysis.
    Returns detected anti-patterns, AI analysis results, and fatal error status.

_initialize_openai_client():
    Creates and configures Azure OpenAI client using environment variables.
    Sets up model configuration for GPT-based analysis.

call_openai(openai_client, diff_text, changed_spec_files):
    Calls Azure OpenAI for comprehensive spec file analysis including:
    - General spec analysis
    - Patch verification 
    - CVE validation
    Uses PromptTemplates for structured analysis.

get_severity_exit_code(severity):
    Maps anti-pattern severity levels to appropriate pipeline exit codes.
    Supports fine-grained exit code reporting based on issue severity.

update_github_status(severity, anti_patterns, ai_analysis, analyzer, post_comments, use_checks_api):
    Updates GitHub PR with analysis results via comments and/or Checks API.
    Integrates with GitHubClient for posting structured feedback on PRs.

_derive_github_context():
    Extracts GitHub repository and PR information from Azure DevOps environment variables.
    Handles multiple environment variable sources for GitHub integration.

main():
    Entry point that orchestrates the entire analysis pipeline:
    1. Gathers git diff
    2. Identifies changed spec files
    3. Runs anti-pattern detection and AI analysis
    4. Generates reports and saves results
    5. Updates GitHub status
    6. Returns appropriate exit codes

Exit Codes:
----------
0 (EXIT_SUCCESS): No issues or warnings only
1 (EXIT_CRITICAL): Critical issues detected
2 (EXIT_ERROR): Error-level issues detected  
3 (EXIT_WARNING): Warning-level issues detected
10 (EXIT_FATAL): Fatal errors during execution

Environment Variables Required:
------------------------------
- SYSTEM_PULLREQUEST_SOURCECOMMITID: Source commit for PR diff
- SYSTEM_PULLREQUEST_TARGETCOMMITID: Target commit for PR diff  
- BUILD_SOURCESDIRECTORY: Repository root directory
- AZURE_OPENAI_ENDPOINT: Azure OpenAI API endpoint
- AZURE_OPENAI_DEPLOYMENT_NAME: OpenAI model deployment name
- GITHUB_TOKEN or SYSTEM_ACCESSTOKEN: For GitHub integration
- GITHUB_REPOSITORY: Repository in owner/repo format
- GITHUB_PR_NUMBER: Pull request number
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
    
    Source Commit (SYSTEM_PULLREQUEST_SOURCECOMMITID):
        What it is: The latest commit on the feature branch that contains the changes being proposed
        Example: If you're working on a feature branch called fix-cve-2023-1234 and you've made 
                several commits, the source commit is the HEAD (most recent commit) of that branch
        Purpose: This represents the "new" state - what you want to merge into the target
    
    Target Commit (SYSTEM_PULLREQUEST_TARGETCOMMITID):
        What it is: The latest commit on the destination branch that the PR wants to merge into
        Example: The HEAD commit of the main branch at the time the PR was created or last updated
        Purpose: This represents the "current" state - what exists before your changes
    
    The diff generated shows: "What changes do I need to apply to the target commit to get to the source commit?"
    This allows the pipeline to analyze only the delta/changes rather than the entire codebase.
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
        
        # Dynamic recommendations have been consolidated into AI analysis; deprecated FixRecommender
        
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
                        analyzer: ResultAnalyzer, post_comments: bool = False, use_checks_api: bool = False) -> None:
    """
    Posts GitHub PR comments with brief analysis and updates status checks.
    
    This replaces the deprecated separate GitHub comment posting approach with
    integrated functionality that uses structured AI output for concise PR comments.
    
    Args:
        severity: Highest severity level detected
        anti_patterns: List of anti-patterns detected
        ai_analysis: AI-generated analysis text (contains structured sections)
        analyzer: ResultAnalyzer instance for generating reports
        post_comments: Whether to post comments on GitHub PR
        use_checks_api: Whether to use GitHub Checks API for status updates
    """
    if not (post_comments or use_checks_api):
        logger.info("GitHub integration disabled. Skipping GitHub updates.")
        return
    
    try:
        github_client = GitHubClient()
        
        # Determine status based on severity
        if severity >= Severity.ERROR:
            status = CheckStatus.FAILURE
            status_title = "CVE Spec File Check Failed"
        elif severity == Severity.WARNING:
            status = CheckStatus.NEUTRAL  # Warnings don't block merging
            status_title = "CVE Spec File Check Passed with Warnings"
        else:
            status = CheckStatus.SUCCESS
            status_title = "CVE Spec File Check Passed"
        
        # Post PR comment with brief analysis if requested
        if post_comments:
            logger.info("Posting brief analysis as GitHub PR comment...")
            comment_content = analyzer.generate_pr_comment_content()
            
            try:
                # Check if we've already posted a comment from this check
                existing_comments = github_client.get_pr_comments()
                bot_comment_id = None
                
                # Look for existing comment from this bot/check
                for comment in existing_comments:
                    if "🚨 PR Check Failed" in comment.get("body", "") or "✅ PR Check Passed" in comment.get("body", ""):
                        bot_comment_id = comment.get("id")
                        break
                
                if bot_comment_id:
                    # Update existing comment
                    logger.info(f"Updating existing PR comment (ID: {bot_comment_id})")
                    github_client.update_pr_comment(bot_comment_id, comment_content)
                else:
                    # Post new comment
                    logger.info("Posting new PR comment")
                    github_client.post_pr_comment(comment_content)
                    
            except Exception as e:
                logger.error(f"Failed to post/update GitHub PR comment: {e}")
        
        # Update GitHub Checks API if requested
        if use_checks_api:
            logger.info("Updating GitHub PR status via Checks API...")
            try:
                # Get commit SHA for the check
                head_sha = os.environ.get("SYSTEM_PULLREQUEST_SOURCECOMMITID", "")
                if not head_sha:
                    logger.warning("Could not determine HEAD SHA for GitHub check")
                    return
                
                # Create check run summary using structured content
                summary = analyzer.generate_console_summary()
                detailed_output = analyzer.extract_brief_summary_for_pr()  # Use brief summary for check output
                
                github_client.create_check_run(
                    name="CVE Spec File Analysis",
                    head_sha=head_sha,
                    status=CheckStatus.IN_PROGRESS,  # First set to in_progress
                    conclusion=status,  # Then set conclusion
                    output_title=status_title,
                    output_summary=summary,
                    output_text=detailed_output
                )
                
            except Exception as e:
                logger.error(f"Failed to update GitHub check status: {e}")
                
    except Exception as e:
        logger.error(f"Failed to initialize GitHub client: {e}")
        logger.info("Continuing without GitHub integration...")

def _derive_github_context():
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    if not repo:
        repo = os.getenv("BUILD_REPOSITORY_NAME", "").strip()
    
    pr_num = os.getenv("GITHUB_PR_NUMBER", "").strip()
    if not pr_num:
        branch = os.getenv("BUILD_SOURCEBRANCH", "") or os.getenv("SYSTEM_PULLREQUEST_SOURCEBRANCH", "")
        match = re.match(r"refs/pull/(\d+)", branch)
        if match:
            pr_num = match.group(1)
    
    if repo:
        os.environ["GITHUB_REPOSITORY"] = repo
    if pr_num:
        os.environ["GITHUB_PR_NUMBER"] = pr_num

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
    
    # Derive GitHub context from environment variables
    _derive_github_context()
    
    # Debug environment variables related to GitHub authentication and context
    logger.info("GitHub Environment Variables:")
    logger.info(f"  - GITHUB_TOKEN: {'Set' if os.environ.get('GITHUB_TOKEN') else 'Not Set'}")
    logger.info(f"  - SYSTEM_ACCESSTOKEN: {'Set' if os.environ.get('SYSTEM_ACCESSTOKEN') else 'Not Set'}")
    logger.info(f"  - GITHUB_REPOSITORY: {os.environ.get('GITHUB_REPOSITORY', 'Not Set')}")
    logger.info(f"  - GITHUB_PR_NUMBER: {os.environ.get('GITHUB_PR_NUMBER', 'Not Set')}")
    logger.info(f"  - BUILD_REPOSITORY_NAME: {os.environ.get('BUILD_REPOSITORY_NAME', 'Not Set')}")
    logger.info(f"  - SYSTEM_PULLREQUEST_PULLREQUESTNUMBER: {os.environ.get('SYSTEM_PULLREQUEST_PULLREQUESTNUMBER', 'Not Set')}")
    
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
        
        # Process results with structured analysis
        analyzer = ResultAnalyzer(anti_patterns, ai_analysis)
        
        # Print console summary (contains brief overview)
        console_summary = analyzer.generate_console_summary()
        print(f"\n{console_summary}")
        
        # Log detailed analysis to Azure DevOps pipeline logs
        detailed_analysis = analyzer.extract_detailed_analysis_for_logs()
        if detailed_analysis:
            logger.info("=== DETAILED ANALYSIS FOR PIPELINE LOGS ===")
            for line in detailed_analysis.split('\n'):
                if line.strip():
                    logger.info(line)
            logger.info("=== END DETAILED ANALYSIS ===")
        
        # Generate and save comprehensive report files
        detailed_report = analyzer.generate_detailed_report()
        report_file = os.path.join(os.getcwd(), "spec_analysis_report.txt")
        with open(report_file, "w") as f:
            f.write(detailed_report)
        logger.info(f"Detailed analysis report saved to {report_file}")
        
        # Save enhanced JSON report with structured content for pipeline and GitHub integration
        json_file = os.path.join(os.getcwd(), "spec_analysis_report.json")
        json_report = analyzer.to_json()
        with open(json_file, "w") as f:
            f.write(json_report)
        logger.info(f"Enhanced JSON analysis report saved to {json_file}")
        
        # Log brief summary for quick reference
        brief_summary = analyzer.extract_brief_summary_for_pr()
        if brief_summary:
            logger.info("=== BRIEF SUMMARY FOR PR ===")
            logger.info(brief_summary)
            logger.info("=== END BRIEF SUMMARY ===")
        
        # Determine exit code
        if fatal_error:
            logger.error("Fatal error occurred during analysis")
            return EXIT_FATAL
            
        # Get highest severity
        highest_severity = analyzer.get_highest_severity()
        
        # Update GitHub status with integrated comment posting using structured content
        update_github_status(
            highest_severity, 
            anti_patterns, 
            ai_analysis,
            analyzer,
            post_comments=args.post_github_comments,
            use_checks_api=args.use_github_checks
        )
        
        if args.exit_code_severity:
            # Return exit codes based on severity, but do not fail on warnings unless requested
            if highest_severity.value >= Severity.ERROR.value:
                exit_code = get_severity_exit_code(highest_severity)
            elif highest_severity == Severity.WARNING:
                exit_code = EXIT_WARNING if args.fail_on_warnings else EXIT_SUCCESS
            else:
                exit_code = EXIT_SUCCESS
            
            # Log exit details
            if exit_code == EXIT_SUCCESS:
                logger.info("Analysis completed successfully - no issues detected or warnings only.")
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
                # Generate structured error message for failure case
                error_message = analyzer.generate_error_message()
                print(f"\n{error_message}")
                return EXIT_CRITICAL  # Traditional error exit code
            else:
                logger.info("Analysis completed - no critical issues detected")
                return EXIT_SUCCESS
        
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return EXIT_FATAL

if __name__ == "__main__":
    sys.exit(main())