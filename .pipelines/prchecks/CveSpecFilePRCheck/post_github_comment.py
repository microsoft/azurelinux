"""
Post GitHub comment script for CVE Spec File PR Check.

This script creates concise GitHub PR comments based on the analysis results
from the CVE spec file check. It reads the generated JSON report and posts
a brief summary to the GitHub PR.

Usage:
    python post_github_comment.py <repo_owner> <repo_name> <pr_number> <report_file>

Note: This script is maintained for backward compatibility with existing pipelines.
The main CveSpecFilePRCheck.py now includes integrated GitHub comment posting.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add the current directory to sys.path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

from GitHubClient import GitHubClient


def setup_logging() -> None:
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_analysis_report(report_file: str) -> Optional[Dict[str, Any]]:
    """
    Load the analysis report from a JSON file.
    
    Args:
        report_file: Path to the JSON report file
        
    Returns:
        Dictionary containing the analysis report or None if loading fails
    """
    try:
        report_path = Path(report_file)
        if not report_path.exists():
            logging.error(f"Report file not found: {report_file}")
            return None
            
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
            
        logging.info(f"Successfully loaded report from {report_file}")
        return report
        
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in report file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading report file: {e}")
        return None


def create_concise_comment(report: Dict[str, Any]) -> str:
    """
    Create a concise GitHub comment from the analysis report.
    
    Args:
        report: Analysis report dictionary
        
    Returns:
        Formatted comment string for GitHub PR
    """
    try:
        # Try to get brief summary first (from new structured approach)
        if 'brief_summary' in report:
            brief_content = report['brief_summary']
            if brief_content and brief_content.strip():
                return f"## CVE Spec File Analysis\n\n{brief_content}"
        
        # Fallback to creating summary from full report
        status = report.get('status', 'unknown')
        total_issues = report.get('total_issues', 0)
        
        if status == 'passed' and total_issues == 0:
            return "## CVE Spec File Analysis\n\n✅ **No issues found** - Spec file analysis passed successfully."
        
        # Build comment for issues found
        comment_parts = ["## CVE Spec File Analysis\n"]
        
        if total_issues > 0:
            comment_parts.append(f"🔍 **Found {total_issues} issue(s)** that need attention:\n")
            
            # Add critical/high severity issues if available
            high_priority_issues = []
            for file_name, file_data in report.get('files', {}).items():
                if isinstance(file_data, dict) and 'issues' in file_data:
                    for issue in file_data['issues']:
                        severity = issue.get('severity', '').lower()
                        if severity in ['critical', 'high']:
                            high_priority_issues.append({
                                'file': file_name,
                                'type': issue.get('type', 'Unknown'),
                                'severity': severity,
                                'description': issue.get('description', ''),
                                'recommendation': issue.get('recommendation', '')
                            })
            
            # Show high priority issues
            if high_priority_issues:
                comment_parts.append("### High Priority Issues:\n")
                for issue in high_priority_issues[:3]:  # Limit to 3 for brevity
                    comment_parts.append(f"- **{issue['type']}** in `{issue['file']}` ({issue['severity']})")
                    if issue['description']:
                        comment_parts.append(f"  - {issue['description']}")
                    if issue['recommendation']:
                        comment_parts.append(f"  - Recommendation: {issue['recommendation']}")
                    comment_parts.append("")
                
                if len(high_priority_issues) > 3:
                    comment_parts.append(f"... and {len(high_priority_issues) - 3} more issues.\n")
            
            comment_parts.append("📋 **Full details** are available in the Azure DevOps pipeline logs.")
        
        return "\n".join(comment_parts)
        
    except Exception as e:
        logging.error(f"Error creating comment: {e}")
        return f"## CVE Spec File Analysis\n\n⚠️ Analysis completed but encountered an error generating the summary. Check pipeline logs for details."


def main():
    """Main function to post GitHub comment."""
    setup_logging()
    
    if len(sys.argv) != 5:
        print("Usage: python post_github_comment.py <repo_owner> <repo_name> <pr_number> <report_file>")
        sys.exit(1)
    
    repo_owner = sys.argv[1]
    repo_name = sys.argv[2]
    pr_number = sys.argv[3]
    report_file = sys.argv[4]
    
    logging.info(f"Posting comment for PR #{pr_number} in {repo_owner}/{repo_name}")
    logging.info(f"Using report file: {report_file}")
    
    # Load the analysis report
    report = load_analysis_report(report_file)
    if not report:
        logging.error("Failed to load analysis report")
        sys.exit(1)
    
    # Create the comment content
    comment_content = create_concise_comment(report)
    logging.info("Generated comment content")
    
    try:
        # Initialize GitHub client and post comment
        github_client = GitHubClient()
        success = github_client.post_pr_comment(
            repo_owner=repo_owner,
            repo_name=repo_name,
            pr_number=int(pr_number),
            comment=comment_content
        )
        
        if success:
            logging.info("Successfully posted GitHub comment")
            print("GitHub comment posted successfully")
        else:
            logging.error("Failed to post GitHub comment")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Error posting GitHub comment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
