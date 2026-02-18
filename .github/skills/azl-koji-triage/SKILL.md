---
name: azl-koji-triage
description: "Examine Koji builds, fetch task info and logs from the Koji Web UI, identify failures, and provide root cause analysis. Use when triaging Koji build failures, investigating failed tasks, downloading build logs, or searching for broken packages. Triggers: koji failure, koji build failed, koji task, koji log, koji triage, build failure analysis."
---

# Koji Build Failure Triage

## Koji Web UI

- **Base URL**: Get from the user, or from env variable `KOJI_BASE_URL`.
  - If the env variable is not set, prompt the user to input the base URL of the Koji Web UI (e.g., `https://koji.example.com`), or tell them to set the `KOJI_BASE_URL` environment variable for future use.
- **MCP tools (preferred)**: Use the `koji` MCP server tools (`set_koji_url`, `koji_fetch`) to fetch pages and logs. These write output to temp files under `base/build/work/scratch/koji/` to avoid bloating context. Use `read_file` and `grep_search` on the resulting files to inspect content.
  1. Call `set_koji_url` with the base URL first.
  2. Call `koji_fetch` with the path (e.g., `/koji/taskinfo?taskID=3307`). It returns the file path where content was saved.
     - If the fetch fails with an SSL certificate error (e.g., self-signed cert), ask the user if they want to skip SSL verification, then call `koji_allow_insecure` to proceed. Do **NOT** proceed without explicit user approval for the **specific** URL.
  3. Use `read_file` or `grep_search` on the saved file to extract the information you need.
  4. Call `koji_cleanup` when done to remove fetched temp files and reclaim disk space (NOTE: This will clean up ALL scratch files, so only call it when you're completely done with the current files).
- **MCP is required.** If MCP tools are not working, ask the user to fix their MCP configuration rather than falling back to CLI tools.
- **Network issues**: Koji is typically only accessible via VPN or corporate network. If you encounter connection errors or timeouts, assume it is a network permissions issue — ask the user to confirm they are connected to the appropriate network before retrying. Do NOT keep retrying on your own.

## Discovery: Finding Builds by Package Name

When the user provides a **package name** instead of a task ID, use **both** discovery paths below to find all recent failures. Neither path alone is sufficient.

> **Why two paths?** The package info page only lists builds where Koji created a build record. If a task fails early (e.g., `buildSRPMFromSCM` fails), no build record exists and the failure is invisible on the package page. The failed tasks list catches these, but doesn't filter by package — you must grep for the name. Always run both.

### Path A: Package info page (finds builds with records)

1. **Search for the package:**

```
/koji/search?match=glob&type=package&terms=<PACKAGE_NAME>
```

- If the exact name doesn't match, try a glob: `terms=<NAME>*`
- Extract the `packageID` from the results (look for `packageinfo?packageID=` links)
- If the search returns only one match, Koji redirects directly to the package info page (skip step 2).

2. **Get recent builds from the package info page:**

```
/koji/packageinfo?packageID=<PACKAGE_ID>
```

- Look for `buildinfo?buildID=` links with state `failed`
- Note the build NVRs (Name-Version-Release) for context

3. **Get the build's parent task ID:**

```
/koji/buildinfo?buildID=<BUILD_ID>
```

- Extract the `taskinfo?taskID=` link — this is the parent `build` task
- The parent task's Descendants section lists the actual failed child tasks (`buildArch`, `buildSRPMFromSCM`)

### Path B: Failed tasks list (catches failures with no build record)

Search the global failed tasks list for the package name:

```
/koji/tasks?owner=&state=failed&view=flat&method=build&order=-id
```

- This lists all recent failed `build` tasks, newest first
- **Grep the results for the package name** to find relevant task IDs
- This catches early failures (e.g., `buildSRPMFromSCM` errors, plugin/callback errors) that never create a build record and would be invisible on the package info page

### Combine results

Collect the parent task IDs from both paths, deduplicate, then for each parent task:
1. Fetch `taskinfo?taskID=<PARENT_ID>` to see the Descendants tree
2. Identify which child task(s) failed (`buildSRPMFromSCM` or `buildArch`)
3. Proceed to the Investigation Workflow below for each failed child

### Quick-reference: Discovery URLs

| Goal | URL Path |
|------|----------|
| Search packages by name | `/koji/search?match=glob&type=package&terms=<NAME>` |
| Package info (recent builds) | `/koji/packageinfo?packageID=<ID>` |
| Build details → parent task | `/koji/buildinfo?buildID=<ID>` |
| All recent failed build tasks | `/koji/tasks?owner=&state=failed&view=flat&method=build&order=-id` |
| Search builds by NVR | `/koji/search?match=glob&type=build&terms=<NAME>*` |

### Example: "Why is the kernel broken?"

```
# Path A: Package info page
# 1. Search for the kernel package
koji_fetch(path="/koji/search?match=glob&type=package&terms=kernel")
# → grep for 'packageinfo?packageID=' → e.g., packageID=6
# → (if single match, Koji redirects directly to package info page)

# 2. Get package info to see recent builds
koji_fetch(path="/koji/packageinfo?packageID=6")
# → grep for 'failed' and 'buildinfo?buildID=' → e.g., buildID=1482

# 3. Get the parent task ID from the build info page
koji_fetch(path="/koji/buildinfo?buildID=1482")
# → grep for 'taskinfo?taskID=' → e.g., parent task 32608

# Path B: Failed tasks list (run in parallel with Path A)
# 4. Search all recent failed build tasks for "kernel"
koji_fetch(path="/koji/tasks?owner=&state=failed&view=flat&method=build&order=-id")
# → grep for 'kernel' → may find additional tasks (e.g., task 87474)
#    that failed before creating a build record

# Combine: parent tasks = {32608, 87474}
# 5. For each parent, fetch task info and find the failed child
koji_fetch(path="/koji/taskinfo?taskID=32608")
# → Descendants: buildArch x86_64 (task 39696) = failed
koji_fetch(path="/koji/taskinfo?taskID=87474")
# → Descendants: buildSRPMFromSCM (task 87475) = failed

# 6. Investigate each failed child using the workflow below
```

## Investigation Workflow

### 1. Get Task Info

Fetch the task page and extract key details (state, method, children).

Call `set_koji_url` once, then `koji_fetch` with path `/koji/taskinfo?taskID=<TASK_ID>`. Use `grep_search` on the saved file to extract state, method, and child task IDs.

Parse the HTML to find:
- **State**: `failed`, `closed` (success), `canceled`, `free`, `open`
- **Method**: `build` (parent), `buildSRPMFromSCM`, `buildArch`
- **Child task IDs**: Look for `taskinfo?taskID=` links in the Descendants section

A `build` task always has children: one `buildSRPMFromSCM` (SRPM creation) and one or more `buildArch` tasks (per architecture). The parent fails if any child fails.

### 2. Find the Failed Child

Extract all `taskinfo?taskID=<ID>` links from the parent task page. Then fetch each child task page and check its state. Typically:
- `buildSRPMFromSCM` succeeds
- One of the `buildArch` tasks fails (look for `state.*failed` in the HTML)

**Important**: Also check the **Result** field in the task info HTML. For some failures (especially `buildSRPMFromSCM`), the error message is embedded directly in the page under "Result" and is NOT in any downloadable log file.

### 3. Download Logs

Download logs from the failed child task.

Call `koji_fetch` with the path `/koji/getfile?taskID=<CHILD_TASK_ID>&volume=DEFAULT&name=<FILENAME>&offset=0`. The content is saved to a temp file — use `grep_search` or `read_file` to inspect it. For large logs, fetch with `&offset=-4000` first to get the tail.

Available log files (listed on the child task page):
| File | Contains |
|------|----------|
| `root.log` | Mock chroot setup, dependency resolution, RPM build commands |
| `build.log` | RPM build output (`%prep`, `%build`, `%install`, `%check`) |
| `mock_output.log` | Mock orchestration output, systemd-nspawn errors |
| `checkout.log` | Git clone/fetch output (buildSRPMFromSCM tasks only) |
| `dnf5.log` | Package manager operations |
| `state.log` | Mock state transitions |
| `hw_info.log` | Builder hardware info |
| `mock_config.log` | Mock configuration |

Use `offset=-4000` instead of `offset=0` to get just the tail (last 4KB) for a quick peek.

### 4. Identify the Failure

There are four main failure categories. Check them in this order:

#### A. Plugin/callback failure (buildSRPMFromSCM only) — check the **Result field in the task info HTML**
- `CallbackError: Error running postSCMCheckout callback` — The `azldev` builder plugin failed during source preparation
- `azldev failed with return code 1` — The Azure Linux source prep tool could not process the package
- These errors appear in the task page Result field, NOT in any log file
- Cause: Package spec/sources are malformed, or the azldev tool doesn't support the package layout

#### B. Mock infrastructure failure (mock exit status 30) — check `mock_output.log` FIRST, then `root.log`
- `Failed to register machine: The name org.freedesktop.machine1 was not provided` — systemd-nspawn/machined not available on builder (infrastructure issue, retry on different host)
- `could not init mock buildroot` — Mock chroot setup failed before builds started
- These are builder infrastructure issues, not package issues. Retrying usually fixes them.

#### C. Dependency resolution failure (mock exit status 30) — check `root.log`
- `No match for argument:` — A `BuildRequires` package is not available in the build tag
- `Failed to resolve the transaction` — dnf5 cannot satisfy dependencies
- Cause: Missing packages in the build tag, build order issues, or circular dependencies

#### D. Build/compilation/test failure (mock exit status 1) — check `build.log`
- `error:` — Compiler or build tool errors
- `FAIL ` / `ERROR ` — Test suite failures in `%check` phase
- `Bad exit status from` — RPM scriptlet failure (shows which phase: `%build`, `%check`, `%install`)
- Look for the **Testsuite summary** block to see PASS/FAIL/ERROR/SKIP counts

**Common root causes**:
| Pattern | Cause | Log / Location |
|---------|-------|----------------|
| `CallbackError...azldev` | Source prep plugin failure | Task info HTML Result field |
| `azldev failed with return code 1` | Package spec/source issue | Task info HTML Result field |
| `Failed to register machine` | Builder missing systemd-machined | `mock_output.log` |
| `could not init mock buildroot` | Mock infrastructure failure | `mock_output.log` |
| `No match for argument: <pkg>` | Missing BuildRequires in build tag | `root.log` |
| `Failed to resolve the transaction` | Dependency resolution failure | `root.log` |
| `FAIL tests/...` with test summary | Test failure in `%check` | `build.log` |
| `Bad exit status from` (%check) | Test suite failed | `build.log` |
| `Bad exit status from` (%build) | Compilation failed | `build.log` |
| `error: unpacking of archive failed` | Corrupt source/SRPM | `build.log` |
| `no inotify_add_watch` | Container inotify limitation | `build.log` |
| `mock exited with status 30` | Dependency OR infrastructure | `root.log` or `mock_output.log` |
| `mock exited with status 1` | Build or test failure | `build.log` |

## Example: Full Investigation

```
# 1. Set the Koji base URL (once per session)
set_koji_url(base_url="https://koji.example.com")

# 2. Fetch parent task info → saved to temp file
koji_fetch(path="/koji/taskinfo?taskID=3307")
# → "Wrote 12345 bytes (200 lines) to base/build/work/scratch/koji/task_3307_taskinfo.html.xxxxx"

# 3. Use grep_search on the saved file to find child task IDs and state
#    grep for 'taskinfo?taskID=' to find children
#    grep for 'failed' to find which child failed

# 4. Fetch the failed child's task info (check Result field for plugin errors)
koji_fetch(path="/koji/taskinfo?taskID=6059")

# 5. Fetch logs in order of priority:
# 5a. mock_output.log (infrastructure errors)
koji_fetch(path="/koji/getfile?taskID=6059&volume=DEFAULT&name=mock_output.log&offset=-4000")
# → grep saved file for: ERROR, Failed to register, could not init

# 5b. root.log (dependency resolution errors)
koji_fetch(path="/koji/getfile?taskID=6059&volume=DEFAULT&name=root.log")
# → grep saved file for: No match for, Failed to resolve

# 5c. build.log (build/test errors)
koji_fetch(path="/koji/getfile?taskID=6059&volume=DEFAULT&name=build.log")
# → grep saved file for: FAIL, ERROR, Bad exit status, error:

# 5d. For exceptionally large files, consider using 'fold' on the saved file.
```

## If Koji tools are not working

The MCP server is the only supported method for fetching Koji information: it handles URL construction, SSL issues, output file creation and cleanup, etc.

If MCP tools are not working, guide the user to help them fix their MCP configuration. A (non exhaustive) list of some things to check:
- If they are in VSCode or Copilot CLI, ensure they are running in a reasonable workspace (ie not a parent folder that doesn't have the right mcp.json file, or adhoc files that don't have a root dir)
- If they REALLY don't want to be in a workspace, guide them through adding a global mcp configuration
  - Copilot CLI: `~/.copilot/mcp-config.json` (https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli#add-an-mcp-server)
  - VSCode: user profile: (https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_add-an-mcp-server)
- Check that the MCP server can start - it might be missing the `mcp` python package dependency
- Something else...
