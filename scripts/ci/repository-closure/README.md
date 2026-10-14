# Candidate repository closure

`check_repo_closure.py` compares baseline and proposed base/base+SDK views,
failing only on new package/dependency failures. It requires RPM, createrepo_c,
and DNF 4 or 5 with repoclosure. Inputs are binary RPM directories already
routed into base and SDK.

Pass `--replaced-source-components-file` with a JSON array of affected source
package names. As in publication routing, component identifiers correspond to
RPM source names. The Control Tower preparation step includes source changes,
policy-only changes, and explicit deletions; acquisition adds any additional
successfully built components. The engine inventories baseline `SOURCERPM`
metadata and excludes every former binary output of those sources before
overlaying fresh RPMs. This removes stale subpackages and channel-moved outputs,
including in the base-only view. Deletion-only input is supported without RPMs;
empty input without an affected-source list remains an error.

Candidate selection allows equal-EVR baseline/candidate ties but rejects a
strictly newer baseline winner. Selection evidence retains all tied rows; the
solver configuration excludes the corresponding baseline names.

Use `--work-directory` for generated RPM repositories and `--output-directory`
for reports and logs. Same-filesystem inputs are hardlinked, with copies only
across filesystems. The pipeline keeps runtime RPMs under `Agent.TempDirectory`,
not in published artifacts.

The ADO entry point exposes queue-time `enableCandidateClosureCheck`,
`kojiFilesUrl`, and `kojiHubUrl` parameters. Closure steps run only for deployments
with `runCandidateClosureCheck: true` and package builds enabled. Disabling the
flag skips preparation/acquisition/solving and restores the original
added/changed-component scratch-build input. All closure steps honor the
deployment's `continueOnError` policy.

The wrapper configures x86_64 and aarch64 entries in `closureRepositories`,
each with matching base/builddeps baseline URLs. A single Control Tower
scratch build feeds both architecture checks. Acquisition, candidate RPMs,
DNF state, and reports are separated by architecture; noarch RPMs participate
in both views. A failure on one architecture does not suppress the other:
each solver requires successful tools setup and its own acquisition, or a
deletion-only transaction. Either architecture's failure fails the PROD check.
Deletion-only transactions also check both architectures without submitting
a scratch build.

Koji acquisition uses the official Python `koji.ClientSession` and `koji.PathInfo`,
not a custom XML-RPC transport or task-page HTML. The current
PROD hub was verified at `https://52.185.225.133/kojihub` (Koji 1.35.3).
`getTaskInfo` and `getTaskChildren` must describe a closed build with closed
`buildArch` children. Matching architecture/noarch tasks are preferred. Architecture
selection uses the decoded build request, not the task's scheduling architecture.
Ambiguous same-architecture children fail rather than guessing a retry winner.

Koji applies source RPM architecture restrictions before creating children.
When a closed root has no matching architecture/noarch task, acquisition
checks the other architecture tasks' complete inventories and retains only
their shared noarch outputs. Empty native output does not skip closure:
former outputs of the affected source are still removed from that architecture's
baseline, including when architecture support was dropped. Reports explicitly
record `hasMatchingArchitectureTask`. An empty root, incomplete inventory, or
explicit scratch architecture override excluding the requested view fails.
Duplicate noarch filenames within one closed root are selected once, after
Koji's finalization checks; duplicate component roots remain errors.

For each selected task, `getTaskResult().rpms` must exactly match the binary
RPM inventory from `listTaskOutput(..., all_volumes=True, strict=True)`,
including debug RPMs before filtering. Missing, unexpected, duplicate, unsafe,
or wrong-architecture results fail acquisition. Only the default Koji volume
is supported; other or ambiguous volumes fail explicitly. Source/debug RPMs
are excluded from candidate downloads. Every selected task must produce
publishable RPMs. API faults are errors; there is no HTML fallback. Reports retain
the client version, hub endpoint, discovery strategy, root task IDs, and selected
task IDs/requested architectures.

The official client handles anonymous metadata retries, configured for three
retries, a two-second retry interval, and a 60-second request timeout. Offline
retry is disabled. Artifact GETs reuse Koji's `request_with_retry` HTTP adapter
for connection/status retries, including HTTP 408/429/500/502/503/504. Standard
HTTP backoff and `Retry-After` handling belong to that adapter.

Koji's stock `downloadFile` does not accept a TLS policy or configured session,
so a small streaming download function uses a `requests.Session` with explicit
TLS verification and a 60-second request timeout. Both the hub and artifact
session honor `--insecure-koji-tls`; verification remains enabled by default.
Failed partial files are removed, and interrupted response bodies fail acquisition
rather than being resumed. Complete downloads are checked for RPM magic and
content length and hashed for the report. There is no custom transfer budget or
overall deadline. Report schema version 3 removes the former safety-limit and
per-RPM attempt/transfer-byte fields.

The Control Tower requirements pin the official client. Its GSSAPI dependency
requires native build tools; the pipeline installs GCC, Kerberos development
headers, and Python development headers before installing Python dependencies.

PROD's explicit insecure TLS exception remains: locally computed RPM hashes
record downloaded content, not authenticated provenance. A verifiable
hostname/CA pair or authenticated artifact digests are required to close that
infrastructure trust gap.
