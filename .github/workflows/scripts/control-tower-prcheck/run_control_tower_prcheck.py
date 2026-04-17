"""Call the Control Tower prcheck API.

Sends a POSTs to CT's 'prcheck' endpoint with a payload containing the PR context.

Authentication:
    Requires an active Azure CLI session (e.g. via an AzureCLI@2 pipeline
    task with a Workload Identity Federation service connection).
    ``DefaultAzureCredential`` discovers the session automatically.
"""

import argparse
import json
import sys

import requests
from azure.identity import DefaultAzureCredential


def _parse_components(value: str) -> list[str]:
    """Parse a comma-separated string into a list of stripped, non-empty names."""
    return [c.strip() for c in value.split(",") if c.strip()]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Control Tower prcheck API.",
    )
    parser.add_argument(
        "--api-audience",
        required=True,
        help="Entra ID audience URI (e.g. api://<client-id>)",
    )
    parser.add_argument(
        "--api-base-url", required=True, help="Base URL of the Control Tower service"
    )
    parser.add_argument(
        "--build-reason",
        required=True,
        help="ADO build reason (PullRequest, IndividualCI, …)",
    )
    parser.add_argument(
        "--components",
        required=True,
        type=_parse_components,
        help="Comma-separated list of affected component names",
    )
    parser.add_argument("--source-commit", required=True, help="Source commit SHA")
    parser.add_argument(
        "--source-branch",
        default=None,
        help="Source branch name (alternative to --source-commit)",
    )
    parser.add_argument("--target-commit", default=None, help="Target commit SHA")
    parser.add_argument(
        "--target-branch",
        default=None,
        help="Target branch name (alternative to --target-commit)",
    )
    parser.add_argument("--repo-uri", required=True, help="Upstream repository URI")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    # ── Build payload ────────────────────────────────────────────────
    payload: dict = {
        "components": args.components,
        "buildReason": args.build_reason,
        "repoUri": args.repo_uri,
        "sourceCommitSha": args.source_commit,
    }
    if args.source_branch is not None:
        payload["sourceBranch"] = args.source_branch
    if args.target_commit is not None:
        payload["targetCommitSha"] = args.target_commit
    if args.target_branch is not None:
        payload["targetBranch"] = args.target_branch

    print("Calling Control Tower 'prcheck' endpoint...")
    print("Payload:")
    print(json.dumps(payload, indent=2))

    if args.build_reason == "PullRequest":
        print(
            "Skipping Control Tower call - pull request triggers are not supported, yet."
        )
        return

    # ── Acquire bearer token ─────────────────────────────────────────
    credential = DefaultAzureCredential()
    token = credential.get_token(f"{args.api_audience}/.default").token

    # ── Call prcheck API ─────────────────────────────────────────────
    url = f"{args.api_base_url}/api/Scenario/prcheck"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=(10, 60),
    )

    # ── Handle response ──────────────────────────────────────────────
    print("Service response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.JSONDecodeError:
        print(response.text)

    print(f"HTTP status: {response.status_code}")

    if not response.ok:
        print(f"##[error]Control Tower returned HTTP {response.status_code}")
        sys.exit(1)


if __name__ == "__main__":
    main()
