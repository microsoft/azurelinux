# Copyright (c) 2026 Microsoft Corporation.
# Licensed under the MIT License.
"""Concurrency regression tests for the Fedora dist-git MCP server."""

from __future__ import annotations

import asyncio
import importlib.util
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import TYPE_CHECKING

import _mcp_utils
import pytest
from mcp import Client

if TYPE_CHECKING:
    from types import ModuleType

    from mcp.types import CallToolResult

_MCP_DIR = Path(__file__).resolve().parents[1]
_REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_distgit_module(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """Load the hyphenated MCP entrypoint without starting stdio."""
    monkeypatch.setattr(_mcp_utils, "load_env", lambda: None)
    script_path = _MCP_DIR / "fedora-distgit-mcp.py"
    spec = importlib.util.spec_from_file_location("_test_fedora_distgit_mcp", script_path)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {script_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_concurrent_search_clones_package_once(monkeypatch: pytest.MonkeyPatch) -> None:
    """Serialize concurrent searches that populate the same cache entry."""
    scratch_parent = _REPO_ROOT / "base" / "build" / "work" / "scratch"
    scratch_parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="distgit-concurrency-", dir=scratch_parent) as work_dir:
        distgit = _load_distgit_module(monkeypatch)
        monkeypatch.setattr(distgit, "_repos_dir", str(Path(work_dir) / "repos"))

        first_clone_started = threading.Event()
        second_clone_started = threading.Event()
        clone_count_lock = threading.Lock()
        clone_count = 0

        def fake_run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            nonlocal clone_count

            if len(command) > 1 and command[1] == "clone":
                with clone_count_lock:
                    clone_count += 1
                    current_clone = clone_count

                if current_clone == 1:
                    first_clone_started.set()
                    second_clone_started.wait(timeout=0.5)
                else:
                    second_clone_started.set()

                (Path(command[-1]) / ".git").mkdir(parents=True, exist_ok=True)
                return subprocess.CompletedProcess(command, 0, "", "")

            if "grep" in command:
                return subprocess.CompletedProcess(command, 1, "", "")

            return subprocess.CompletedProcess(command, 0, "", "")

        monkeypatch.setattr(distgit.subprocess, "run", fake_run)

        async def run_searches() -> list[CallToolResult]:
            async with Client(distgit.mcp, raise_exceptions=True) as client:
                arguments = {"package": "example", "query": "needle", "mode": "grep"}
                first = asyncio.create_task(client.call_tool("distgit_search", arguments))
                if not await asyncio.to_thread(first_clone_started.wait, 1):
                    pytest.fail("First search did not begin cloning")

                second = asyncio.create_task(client.call_tool("distgit_search", arguments))
                return list(await asyncio.wait_for(asyncio.gather(first, second), timeout=3))

        results = asyncio.run(run_searches())

        if clone_count != 1:
            pytest.fail(f"Expected one clone for concurrent searches, got {clone_count}")
        for result in results:
            if result.is_error:
                pytest.fail(f"Concurrent search failed: {result}")
