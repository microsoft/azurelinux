#!/usr/bin/env python3
import json
import os
import shutil
import subprocess

from _mcp_utils import (
    FastMCP,
    StatusDict,
    load_env,
    write_output,
)

mcp = FastMCP("control-tower")

# TOBIASB: Gves us the control tower endpoint and scope.
load_env()
# _BASE_CT_ENDPOINT = "https://controltower-dev-jwisitgpr74k6-gjb0fchvgkbnamgp.b01.azurefd.net"
# _CT_SCOPE = "api://0cc68201-58e0-48a6-a589-24c39b9d2745/access_as_user"

_scratch_dir: str = os.path.join(
    os.environ.get("AZLDEV_WORK_DIR", "base/build/work"), "scratch", "control-tower"
)

def _run_pri_fly(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run pri-fly with the given arguments and return the CompletedProcess."""
    return subprocess.run(
        ["pri-fly"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def _get_koji_target_for_job(job_id: str) -> str | None:
    """Fetch the first koji target name for a job, or None on failure."""
    result = _run_pri_fly(["results", "jobs", "koji", "get", "--job-id", job_id])
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
        for task in data.get("buildTasks", []):
            target = task.get("kojiInfo", {}).get("kojiTarget", "")
            if target:
                return target
    except (json.JSONDecodeError, KeyError):
        pass
    return None


@mcp.tool()
def results_jobs_koji_get(job_id: str) -> StatusDict:
    """Get Koji results for a control tower job."""
    result = _run_pri_fly(["results", "jobs", "koji", "get", "--job-id", job_id])

    output = write_output(result.stdout, output_dir=_scratch_dir, prefix="control-tower-")

    status: StatusDict = {
        "returncode": result.returncode,
        "output": output,
    }

    return status


@mcp.tool()
def list_builds(
    target_type: str = "",
    plan_type: str = "",
    status: str = "",
    requested_by: str = "",
    limit: int = 10,
) -> StatusDict:
    """List recent Control Tower builds with optional filters.

    Returns a compact summary of matching workflow jobs sorted by creation
    date (most recent first).

    Args:
        target_type: Filter by koji target substring (e.g. "bootstrap" matches
            "azl4-bootstrap-rpms-target", "rpms-target" matches stage-2 builds).
            Requires an extra API call per candidate job so keep limit small.
        plan_type: Filter by workflow plan type. Common values:
            FullRepository, PackageOnly, ImageBuild, Target, Publish,
            KojiStatusUpdate, ImageFundamentals, Custom.
        status: Filter by job status (Completed, Failed, Running, TimedOut, Unknown).
        requested_by: Filter by requestor (substring match, e.g. "ScheduledJob"
            or an email address).
        limit: Max number of results to return (default 10, max 50).
    """
    limit = max(1, min(limit, 50))

    # Fetch all workflow jobs with plan metadata.
    result = _run_pri_fly(["workflow", "jobs", "get", "--include-workflow-plan"])
    if result.returncode != 0:
        return {"returncode": result.returncode, "output": result.stdout}

    try:
        jobs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"returncode": 1, "output": "Failed to parse workflow jobs JSON"}

    # Apply filters that don't require extra API calls first.
    filtered = []
    for job in jobs:
        plan = job.get("workflowPlan") or {}
        if plan_type and plan.get("planType", "").lower() != plan_type.lower():
            continue
        if status and job.get("status", "").lower() != status.lower():
            continue
        if requested_by and requested_by.lower() not in job.get("requestedBy", "").lower():
            continue
        filtered.append(job)

    # If target_type filter is set, resolve koji targets (expensive).
    if target_type:
        target_matched = []
        for job in filtered:
            if len(target_matched) >= limit:
                break
            koji_target = _get_koji_target_for_job(job["id"])
            if koji_target and target_type.lower() in koji_target.lower():
                job["_kojiTarget"] = koji_target
                target_matched.append(job)
        filtered = target_matched

    # Truncate to limit.
    filtered = filtered[:limit]

    # Build compact summary.
    summary_rows = []
    for job in filtered:
        plan = job.get("workflowPlan") or {}
        row = {
            "jobId": job["id"],
            "status": job.get("status"),
            "createdAt": job.get("createdAt"),
            "completedAt": job.get("completedAt"),
            "requestedBy": job.get("requestedBy"),
            "errorMessage": job.get("errorMessage"),
            "planType": plan.get("planType"),
            "isProd": plan.get("isProd"),
            "isScratchBuild": plan.get("isScratchBuild"),
        }
        if "_kojiTarget" in job:
            row["kojiTarget"] = job["_kojiTarget"]
        summary_rows.append(row)

    output_text = json.dumps(summary_rows, indent=2)
    output = write_output(
        output_text, output_dir=_scratch_dir, prefix="control-tower-"
    )
    return {"returncode": 0, "output": output}


@mcp.tool()
def call_pri_fly(input: list[str]) -> StatusDict:
    """Run `pri-fly` with arbitrary arguments. This can include `--help` to gather more information about usage."""
    result = _run_pri_fly(input)

    output = write_output(result.stdout, output_dir=_scratch_dir, prefix="control-tower-")

    status: StatusDict = {
        "returncode": result.returncode,
        "output": output,
    }

    return status

if __name__ == "__main__":
    # If the tool "pri-fly" is not available, this MCP will not function correctly. Ensure that "pri-fly" is installed and accessible in the system's PATH.
    if not shutil.which("pri-fly"):
        print("Error: 'pri-fly' is not installed or not found in PATH. Please install 'pri-fly' to use this MCP.")
        exit(0)

    mcp.run()