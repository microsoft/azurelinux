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

Koji acquisition uses the hub's XML-RPC API, not task-page HTML. The current
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
publishable RPMs. Requests have bounded response sizes and timeouts, and API
faults are errors; there is no HTML fallback. Reports retain the hub endpoint,
discovery strategy, root task IDs, and selected task IDs/requested architectures.

The four explicitly allowlisted read-only XML-RPC methods and RPM GETs retry
typed transient network failures and HTTP 408/429/500/502/503/504 responses.
Arbitrary XML-RPC POSTs are not replayed. Each operation allows four attempts
within a 600-second retry window, with a 60-second socket timeout clamped to
the remaining window. The window is checked between bounded stream reads;
it is not an OS-level hard cancellation deadline. Exponential backoff starts
at two seconds with up to one second of jitter. `Retry-After` delta/date values
are honored up to 30 seconds; longer requested delays fail rather than retry
early. Certificate/TLS, authorization, XML-RPC fault, malformed-content, and
safety-limit failures are not retried.

Every download attempt starts with a fresh file and digest; failed partial
files are removed. Bytes received by failed attempts still consume the
aggregate download budget, including across RPMs. Reports record the retry
policy plus each RPM's attempt count and cumulative transferred bytes.

PROD's explicit insecure TLS exception remains: locally computed RPM hashes
record downloaded content, not authenticated provenance. A verifiable
hostname/CA pair or authenticated artifact digests are required to close that
infrastructure trust gap.
