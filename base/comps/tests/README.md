# Azure Linux Component Tests

Generic pytest-based validation for RPM artifacts built from Azure Linux
components. This suite is component rather than image oriented: it accepts RPM
files produced by a component build and delegates validation to native RPM
tooling. It contains no package-specific expectations and is intended for
orchestration by `azldev`.

## Checks

- `rpm --checksig --verbose` validates the RPM signature area and payload
  digests.
- RPM header, file-manifest, dependency, provide, and scriptlet queries verify
  that each artifact is readable by `rpm`.
- `rpmlint` runs the Azure Linux policy packaged in the validation container
  across the complete candidate RPM set.
- A container smoke test publishes the candidate set as a temporary repository
  and installs it into a fresh Azure Linux validation container.
- `rmdepcheck` compares the temporary candidate repository with one or more
  Azure Linux baseline repositories for reverse-dependency regressions.
- `rpmdeplint` checks the candidate RPMs themselves: that their declared
  dependencies are satisfiable, that they do not introduce undeclared file
  conflicts with other packages, and that they are not an accidental
  downgrade, all against one or more given repos.

## Run locally

Build the base image first with `azldev image build container-base`. The public
bootstrap image is not sufficient because it omits RPM configuration required
to install validation tools. The runner installs `rpmlint`, `rpminspect`,
`rpminspect-data-azurelinux`, `rmdepcheck`, and `rpmdeplint` by name from the
Azure Linux repos already configured in that base image — no locally built
validation-tool RPMs are required. Then provide one or more RPM files, or one
or more directories. Directory inputs are searched recursively for `*.rpm`
files.

```bash
cd base/comps/tests
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-dir ../../out/rpms/rpm-base
```

To validate explicit artifacts instead:

```bash
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-path /path/to/package.rpm \
  --rpm-path /path/to/package-devel.rpm
```

Use pytest's container option for validation. It builds a local runner from an
AZL4 container image and re-executes the selected test set there:

```bash
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-dir ../../out/rpms/rpm-base
```

`rpminspect` compares each candidate RPM with a baseline RPM having the same
`NAME.ARCH`. This is the local-RPM equivalent of Fedora CI's Koji task versus
previous-build comparison. The runner uses its installed Azure Linux policy.

```bash
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-dir /path/to/candidate-rpms \
  --baseline-rpm-dir /path/to/baseline-rpms
```

When a component dist-git source tree supplies `rpminspect.yaml`, pass it with
`--rpminspect-local-config`. The suite runs rpminspect from that file's parent
directory, allowing rpminspect to merge the component exceptions with the Azure
Linux vendor policy. `azldev component test --source-dir <prepared-source>`
discovers and forwards this file automatically.

The runner image supplies `rpm`, `rpmlint`, `rpminspect`,
`rpminspect-data-azurelinux`, `rmdepcheck`, `rpmdeplint`, `dnf5`, and
`createrepo_c`. The host only needs Podman and an AZL4 base image.

## Reverse dependencies

`rmdepcheck` is the AZL equivalent of Fedora CI's `rdc-repos` check: it uses a
released AZL repository as the baseline and the candidate RPM set as a local
repository. It has no Koji or compose dependency. Pass each baseline repository
explicitly, allowing CI to select the correct AZL release, architecture, and
channel.

```bash
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-dir /path/to/candidate-rpms \
  --base-repo https://packages.microsoft.com/azurelinux/4/prod/base/x86_64
```

## Dependency validation (rpmdeplint)

`rpmdeplint` is the AZL equivalent of Fedora CI's `rpmdeplint` dependency gate:
it checks the candidate RPMs directly, without installing them, for three
classes of defect:

- **Unsatisfiable dependencies** (`check-sat`) — a `Requires:` that nothing in
  the given repos can provide, often introduced by a missed `BuildRequires`
  or a renamed/removed upstream dependency.
- **Undeclared file conflicts** (`check-conflicts`) — two packages installing
  the same path without a corresponding `Conflicts:` relationship.
- **Accidental downgrades** (`check-upgrade`) — a candidate build that is
  older (by RPM version comparison) than a package of the same name already
  present in the given repos.

Pass one or more repos with `--rpmdeplint-repo NAME[,URL_OR_PATH]` (same
syntax as rpmdeplint's own `-r/--repo`):

```bash
uv run pytest cases/ \
  --container-image microsoft/azurelinux/base/core:4.0 \
  --rpm-dir /path/to/candidate-rpms \
  --rpmdeplint-repo azurelinux-base,https://packages.microsoft.com/azurelinux/4/prod/base/x86_64
```

## Policy

The container installs the reviewed, versioned Azure Linux `rpmlint` and
`rpminspect-data-azurelinux` packages. This keeps policy selection independent
of the host distribution.
