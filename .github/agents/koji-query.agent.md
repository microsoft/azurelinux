---
name: koji-query
description: This agent can examine Koji builds, fetching task info and logs from the Koji Web UI, identifying failures, and providing insights on the root cause.
argument-hint: Provide a Koji task ID/URL (e.g., `1234`, `https://koji.example.com/koji/taskinfo?taskID=1234`), or a package name to search for (e.g., `kernel`).
user-invokable: true
---
# Koji Build Failure Analysis

## Koji Web UI

- **Base URL**: {GET FROM USER, or ENV: `KOJI_BASE_URL`}
  - If the env variable is not set, prompt the user to input the base URL of the Koji Web UI (e.g., `https://koji.example.com`), or tell them to set the `KOJI_BASE_URL` environment variable for future use.
- **MCP tools (preferred)**: Use the `koji` MCP server tools (`set_koji_url`, `koji_fetch`) to fetch pages and logs. These handle TLS verification automatically and write output to temp files under `base/build/work/scratch/koji/` to avoid bloating context. Use `read_file` and `grep_search` on the resulting files to inspect content.
  1. Call `set_koji_url` with the base URL first.
  2. Call `koji_fetch` with the path (e.g., `/koji/taskinfo?taskID=3307`). It returns the file path where content was saved.
  3. Use `read_file` or `grep_search` on the saved file to extract the information you need.
  4. Call `koji_cleanup` when done to remove fetched temp files and reclaim disk space (NOTE: This will clean up ALL scratch files, so only call it when you're completely done with the current files).
- **CLI fallback**: If MCP tools are unavailable, use `curl -sk` to skip TLS verification.

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

**MCP** (preferred): Call `set_koji_url` once, then `koji_fetch` with path `/koji/taskinfo?taskID=<TASK_ID>`. Use `grep_search` on the saved file to extract state, method, and child task IDs.

**CLI fallback**:
```
curl -sk "${KOJI_BASE_URL}/koji/taskinfo?taskID=<TASK_ID>"
```

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

**MCP** (preferred): Call `koji_fetch` with the path `/koji/getfile?taskID=<CHILD_TASK_ID>&volume=DEFAULT&name=<FILENAME>&offset=0`. The content is saved to a temp file — use `grep_search` or `read_file` to inspect it. For large logs, fetch with `&offset=-4000` first to get the tail.

**CLI fallback**:
```
curl -sk "${KOJI_BASE_URL}/koji/getfile?taskID=<CHILD_TASK_ID>&volume=DEFAULT&name=<FILENAME>&offset=0"
```

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

#### A. Plugin/callback failure (buildSRPMFromSCM only) -- check the **Result field in the task info HTML**
- `CallbackError: Error running postSCMCheckout callback` -- The `azldev` builder plugin failed during source preparation
- `azldev failed with return code 1` -- The Azure Linux source prep tool could not process the package
- These errors appear in the task page Result field, NOT in any log file
- Cause: Package spec/sources are malformed, or the azldev tool doesn't support the package layout

#### B. Mock infrastructure failure (mock exit status 30) -- check `mock_output.log` FIRST, then `root.log`
- `Failed to register machine: The name org.freedesktop.machine1 was not provided` -- systemd-nspawn/machined not available on builder (infrastructure issue, retry on different host)
- `could not init mock buildroot` -- Mock chroot setup failed before builds started
- These are builder infrastructure issues, not package issues. Retrying usually fixes them.

#### C. Dependency resolution failure (mock exit status 30) -- check `root.log`
- `No match for argument:` -- A `BuildRequires` package is not available in the build tag
- `Failed to resolve the transaction` -- dnf5 cannot satisfy dependencies
- Cause: Missing packages in the build tag, build order issues, or circular dependencies

#### D. Build/compilation/test failure (mock exit status 1) -- check `build.log`
- `error:` -- Compiler or build tool errors
- `FAIL ` / `ERROR ` -- Test suite failures in `%check` phase
- `Bad exit status from` -- RPM scriptlet failure (shows which phase: `%build`, `%check`, `%install`)
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

### MCP Tools (preferred)

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

> **Note:** Try to avoid fetching using `curl` directly, as it will require the user to approve every operation and will not save to a file automatically.

### Bash (CLI fallback)

```bash
# 1. Get parent task info
TASK_ID=3307
html=$(curl -sk "${KOJI_BASE_URL}/koji/taskinfo?taskID=${TASK_ID}")

# 2. Extract child task IDs
echo "$html" | grep -oP 'taskinfo\?taskID=\K\d+' | sort -un

# 3. For each child, check if it failed (look for "failed" in its task page)
CHILD_ID=6059
child_html=$(curl -sk "${KOJI_BASE_URL}/koji/taskinfo?taskID=${CHILD_ID}")
echo "$child_html" | grep -i 'failed'
# IMPORTANT: Check the Result field in the HTML for plugin/callback errors

# 4. Download and analyze the relevant log (check in order)
# 4a. mock_output.log for infrastructure errors
curl -sk "${KOJI_BASE_URL}/koji/getfile?taskID=${CHILD_ID}&volume=DEFAULT&name=mock_output.log&offset=-4000" \
  | grep -iE 'ERROR|Failed to register|could not init'

# 4b. root.log for dependency resolution errors
curl -sk "${KOJI_BASE_URL}/koji/getfile?taskID=${CHILD_ID}&volume=DEFAULT&name=root.log&offset=0" \
  | grep -iE 'No match for|Failed to resolve'

# 4c. build.log for build/test errors (check tail first, full if needed)
curl -sk "${KOJI_BASE_URL}/koji/getfile?taskID=${CHILD_ID}&volume=DEFAULT&name=build.log&offset=-4000" \
  | grep -iE 'FAIL |ERROR |Bad exit status|error:'
```

### PowerShell (CLI fallback)

```powershell
# 1. Get parent task info
$taskId = 3307
$html = (Invoke-WebRequest -Uri "${KOJI_BASE_URL}/koji/taskinfo?taskID=$taskId" -SkipCertificateCheck).Content

# 2. Extract child task IDs
[regex]::Matches($html, 'taskinfo\?taskID=(\d+)') |
  ForEach-Object { $_.Groups[1].Value } | Sort-Object {[int]$_} -Unique

# 3. For each child, check if it failed (look for "failed" in its task page)
$childId = 6059
$childHtml = (Invoke-WebRequest -Uri "${KOJI_BASE_URL}/koji/taskinfo?taskID=$childId" -SkipCertificateCheck).Content
# Parse state from HTML
# IMPORTANT: Check the Result field in the HTML for plugin/callback errors

# 4. Download and analyze the relevant log (check in order)
# 4a. mock_output.log for infrastructure errors
$mockLog = (Invoke-WebRequest -Uri "${KOJI_BASE_URL}/koji/getfile?taskID=$childId&volume=DEFAULT&name=mock_output.log&offset=-4000" -SkipCertificateCheck).Content
$mockLog -split "`n" | Select-String "ERROR|Failed to register|could not init"

# 4b. root.log for dependency resolution errors
$rootLog = (Invoke-WebRequest -Uri "${KOJI_BASE_URL}/koji/getfile?taskID=$childId&volume=DEFAULT&name=root.log&offset=0" -SkipCertificateCheck).Content
$rootLog -split "`n" | Select-String "No match for|Failed to resolve"

# 4c. build.log for build/test errors (check tail first, full if needed)
$buildLog = (Invoke-WebRequest -Uri "${KOJI_BASE_URL}/koji/getfile?taskID=$childId&volume=DEFAULT&name=build.log&offset=-4000" -SkipCertificateCheck).Content
$buildLog -split "`n" | Select-String "FAIL |ERROR |Bad exit status|error:"
```
