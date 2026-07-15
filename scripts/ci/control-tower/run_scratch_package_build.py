"""Submit a scratch package build to Control Tower and wait as requested."""

from __future__ import annotations

import argparse
from pathlib import Path

import package_build

SCRATCH_PACKAGE_PATH = "/api/Scenario/packages"


def build_request(
    environment: str,
    components: list[str],
    *,
    branch: str | None = None,
    commit_sha: str | None = None,
) -> package_build.ScenarioRequest:
    """Build the scratch package scenario request."""
    if branch is not None and commit_sha is not None:
        msg = "branch and commit_sha are mutually exclusive"
        raise ValueError(msg)

    payload: package_build.ScenarioPayload = {
        "environment": environment,
        "packages": components,
    }
    if branch is not None:
        payload["branch"] = branch
    if commit_sha is not None:
        payload["commitSha"] = commit_sha

    return package_build.ScenarioRequest(
        context="scratch-package-build",
        path=SCRATCH_PACKAGE_PATH,
        payload=payload,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a scratch package-build job to the Control Tower service.",
    )
    parser.add_argument(
        "--api-audience",
        required=True,
        help="Entra ID audience URI (e.g. api://<client-id>)",
    )
    parser.add_argument(
        "--api-base-url",
        required=True,
        help="Base URL of the Control Tower service",
    )
    parser.add_argument(
        "--changed-components-file",
        required=True,
        type=Path,
        help="Path to the raw JSON output of 'azldev component changed -a -O json'.",
    )
    parser.add_argument(
        "--environment",
        required=True,
        help="Distro-config RPM build-environment name (e.g. '4.0').",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--branch",
        default=None,
        help="Source branch override. The environment branch is used when omitted.",
    )
    source.add_argument(
        "--commit-sha",
        default=None,
        help="Source commit override. The environment branch is used when omitted.",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help="Maximum time to wait for the job to reach a terminal status (default: 600).",
    )
    parser.add_argument(
        "--wait-for-completion",
        action="store_true",
        default=False,
        help="Require the build to reach a successful terminal state before returning.",
    )
    return parser.parse_args()


def main() -> None:
    """Submit a scratch package build for the changed components."""
    args = _parse_args()
    components = package_build.load_build_components(args.changed_components_file)
    if not components:
        print("No components need a rebuild -- skipping scratch package-build submission.")
        return

    package_build.submit_and_monitor(
        api_audience=args.api_audience,
        api_base_url=args.api_base_url,
        request=build_request(
            args.environment,
            components,
            branch=args.branch,
            commit_sha=args.commit_sha,
        ),
        poll_timeout_seconds=args.poll_timeout_seconds,
        wait_for_completion=args.wait_for_completion,
    )


if __name__ == "__main__":
    main()
