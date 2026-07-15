"""Submit an official package build to Control Tower and confirm acceptance."""

from __future__ import annotations

import argparse
from pathlib import Path

import package_build

OFFICIAL_PACKAGE_PATH = "/api/Scenario/official/packages"


def build_request(environment: str, components: list[str]) -> package_build.ScenarioRequest:
    """Build the official package scenario request."""
    return package_build.ScenarioRequest(
        context="official-package-build",
        path=OFFICIAL_PACKAGE_PATH,
        payload={
            "environment": environment,
            "packages": components,
        },
    )


def validate_build_reason(build_reason: str) -> None:
    """Refuse official artifacts for unmerged pull-request code."""
    if build_reason != "PullRequest":
        return

    print(
        "##[error]Refusing to submit an official package build for a pull request -- "
        "unmerged code must never produce official artifacts."
    )
    raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit an official package-build job to the Control Tower service.",
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
        "--build-reason",
        required=True,
        help="ADO build reason. PullRequest builds are refused.",
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
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help="Maximum time to wait for an immediate terminal status (default: 600).",
    )
    return parser.parse_args()


def main() -> None:
    """Submit an official package build for the changed components."""
    args = _parse_args()

    validate_build_reason(args.build_reason)

    components = package_build.load_build_components(args.changed_components_file)
    if not components:
        print("No components need a rebuild -- skipping official package-build submission.")
        return

    package_build.submit_and_monitor(
        api_audience=args.api_audience,
        api_base_url=args.api_base_url,
        request=build_request(args.environment, components),
        poll_timeout_seconds=args.poll_timeout_seconds,
        wait_for_completion=False,
    )


if __name__ == "__main__":
    main()
