"""Contract tests for the Control Tower PR-check entry point."""

from __future__ import annotations

from argparse import Namespace
from unittest.mock import Mock

import pytest
import run_prcheck


def test_main_uses_pipeline_service_connection(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use the identity authenticated by the enclosing AzureCLI task."""
    credential = object()
    make_credential = Mock(return_value=credential)

    args = Namespace(
        api_audience="api://control-tower",
        api_base_url="https://control-tower.example",
        build_reason="PullRequest",
        changed_components_file=None,
        components=["lolcat"],
        poll_timeout_seconds=60,
        repo_uri="https://github.com/microsoft/azurelinux",
        source_branch=None,
        source_commit="source-commit",
        target_branch=None,
        target_commit=None,
    )

    monkeypatch.setattr(run_prcheck, "_parse_args", Mock(return_value=args))
    monkeypatch.setattr(run_prcheck.ct, "make_credential", make_credential, raising=False)
    monkeypatch.setattr(run_prcheck.ct, "get_token", Mock(return_value="token"))
    monkeypatch.setattr(run_prcheck.ct, "make_session", Mock(return_value=object()))
    monkeypatch.setattr(run_prcheck.ct, "post_scenario", Mock(return_value={"jobId": "job-id"}))
    monkeypatch.setattr(
        run_prcheck.ct,
        "poll_until_terminal",
        Mock(return_value=({"status": run_prcheck.ct.SUCCESS_STATUS}, False)),
    )
    monkeypatch.setattr(run_prcheck.ct, "print_final_status", Mock())
    monkeypatch.setattr(run_prcheck.ct, "report_failure", Mock())

    run_prcheck.main()

    make_credential.assert_called_once_with()
