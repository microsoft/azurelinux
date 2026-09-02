# Azure Linux Image Tests

Validation framework for built Azure Linux images (VM, container, and
WSL). Includes both static (offline filesystem) and runtime (live
container) tests, all driven by pytest.

## How it gets invoked

These tests are wired into `azldev` via the `[tests.*]` and
`[test-groups.*]` tables in `base/images/images.tests.toml`, and
referenced by each image's `tests.tests` in `base/images/images.toml`
(e.g. `tests.tests = [{ name = "static-image-checks" }, { group = "..." }]`).
The standard entry point is:

```bash
azldev image build vm-base
azldev image test  vm-base

azldev image build container-base
azldev image test  container-base

azldev image build wsl
azldev image test  wsl
```

Images with runtime package management ship `azurelinux-repos`, which defines
the repositories available in the resulting OS. These runtime repositories are
independent of the package sources used to build the image. Distroless
container images strip the package manager and do not ship a repository package.

`azldev` creates a per-suite Python venv, installs this directory's
`pyproject.toml`, and invokes pytest with the right `--image-path`,
`--image-name`, and `--capabilities` arguments.

## Test suites

| Test | Description | Runs for |
|------|-------------|----------|
| `static-image-checks` | Offline filesystem validation — mounts images read-only | All images |
| `runtime-container-tests` | Live container tests via `podman exec` | Container images |

## Direct (manual) invocation

```bash
cd base/images/tests

# Static tests — VM image
uv run pytest cases/static/ \
    --image-path /path/to/image.raw \
    --image-name vm-base \
    --capabilities machine-bootable,systemd,runtime-package-management

# Static tests — Container image
uv run pytest cases/static/ \
    --image-path /path/to/image.oci.tar.xz \
    --image-name container-base \
    --capabilities container,runtime-package-management

# Static tests — WSL image (plain rootfs tarball)
uv run pytest cases/static/ \
    --image-path /path/to/image.wsl \
    --image-name wsl \
    --capabilities systemd,runtime-package-management

# Runtime tests — Container image (requires podman)
uv run pytest cases/runtime/ \
    --image-path /path/to/image.oci.tar.xz \
    --image-name container-base \
    --capabilities container,runtime-package-management

# Runtime tests — from a registry reference
uv run pytest cases/runtime/ \
    --image-ref mcr.microsoft.com/azurelinux/base/core:4.0 \
    --image-name container-base \
    --capabilities container,runtime-package-management
```

Test selection follows standard pytest positional arguments. Tests
under `cases/<image-family>/` are auto-skipped when `--image-name`
doesn't belong to that family — the `image` marker is applied
during collection by
`utils.pytest_plugin.pytest_collection_modifyitems` (see "Adding
tests" below for the convention). Tests marked
`@pytest.mark.require_capability("…")` skip when the named
capability isn't in `--capabilities`.

> Always pass `--image-name` when running manually if you want
> image-specific tests under `cases/<image-family>/` to run. Without
> it, every `@pytest.mark.image(...)`-tagged test is skipped.

## Prerequisites

System packages (not pip-installable):

- **`libguestfs`** — `guestmount`, `guestunmount` (VM images)
- **`guestfs-tools`** — `virt-inspector` (VM images)
- **`skopeo`** — OCI archive conversion (container images, static tests)
- **`umoci`** — OCI image unpacking (container images, static tests)
- **`buildah`** — cleanup of rootless umoci extracts (container images, static tests)
- **`podman`** — container runtime for live tests (container images, runtime tests)
- **`rpm`** — for `rpm --root` package queries
- **`uv`** — Python project/package manager

Runtime tests use `python-on-whales` to drive the Podman CLI directly;
the Podman REST API socket is not required.

`pytest_configure` does a preflight check and fails fast if any tool
needed for the current `--image-type` is missing.

## Layout

```
base/images/
├── images.toml                          # Image registry + tests.tests wiring
├── images.tests.toml                    # [tests.*] / [test-groups.*] catalog
└── tests/
    ├── pyproject.toml                   # uv project: pytest + python-on-whales deps
    ├── conftest.py                      # Session fixtures (static + runtime)
    ├── utils/                           # Helper package (not test-collected)
    │   ├── pytest_plugin.py             # CLI options, markers, tool preflight
    │   ├── container_runtime.py         # python-on-whales based container orchestration
    │   ├── extract.py                   # Image mounting / extraction
    │   ├── disk.py                      # virt-inspector → DiskInfo
    │   ├── parsers.py                   # File content parsers
    │   ├── types.py                     # Dataclasses
    │   └── tools.py                     # Native-tool registry
    └── cases/                           # Test cases
        ├── static/                      # Offline filesystem tests
        │   ├── test_os_release.py       # Shared: /etc/os-release
        │   ├── test_oci_config.py       # Shared (container): OCI Config.User unset
        │   ├── test_packages.py         # Shared: rpm-db checks (capability-gated)
        │   ├── vm-base/                 # VM-specific static tests
        │   │   ├── test_kernel.py
        │   │   └── test_partitions.py
        │   └── container-base/          # Container-specific static tests
        │       └── test_container.py
        └── runtime/                     # Live container tests (via podman exec)
            └── container-base/
                ├── test_basic.py        # Basic: shell access, DNS resolution
                └── test_nginx/          # Dockerfile test example
                    ├── test_nginx.py    # Test logic
                    ├── Dockerfile       # Custom image (ARG BASE_IMAGE)
                    └── nginx.conf       # Supporting files
```

## Available fixtures

| Fixture | Scope | Type | Description |
|---------|-------|------|-------------|
| `image_path` | session | `Path \| None` | From `--image-path` (None when `--image-ref` used) |
| `image_ref` | session | `str \| None` | From `--image-ref` (None when `--image-path` used) |
| `image_name` | session | `str \| None` | From `--image-name` |
| `image_type` | session | `str` | `"vm"` or `"container"` (explicit / capabilities / extension) |
| `capabilities` | session | `set[str]` | Parsed `--capabilities` |
| `workdir` | session | `Path` | Working directory for mounts/extractions |
| `rootfs` | session | `Path` | Mounted/extracted root filesystem |
| `oci_image_config` | session | `dict[str, object]` | Parsed `skopeo inspect --config` output (use with `@pytest.mark.require_capability("container")`) |
| `os_release` | session | `dict[str, str]` | Parsed `/etc/os-release` |
| `installed_packages` | session | `set[str]` | Installed RPM names (`rpm --root`) |
| `installed_package_sizes` | session | `dict[str, int]` | Installed RPM name → on-disk size in bytes (`rpm --root`, `%{SIZE}`) |
| `disk_info` | session | `DiskInfo \| None` | VM only |
| `partition_table` | session | `list[PartitionInfo]` | VM only — auto-skips on containers |
| `podman_client` | session | `DockerClient \| None` | python-on-whales Podman client; None for non-container images |
| `container_image_ref` | session | `str \| None` | Loaded image ID (cached); None for non-container |
| `running_container` | function | `ContainerInstance` | Fresh container per test — auto-skips on VMs |
| `container_exec_shell` | function | callable | `(cmd, shell="bash") → ContainerExecResult` |
| `container_exec` | function | callable | `(args) → ContainerExecResult` |
| `wait_for_http` | function | callable | `(url, *, retries=5, delay=1.0, connect_timeout=2.0, max_time=5.0) → ContainerExecResult` — polls an in-container HTTP endpoint with `curl`; raises after retries |
| `assert_http_server` | function | callable | `(start_command, url, expected, *, retries=5, delay=1.0) → ContainerExecResult` — starts a server, waits for `url`, asserts `expected` in body |
| `client_server_exec_shell` | function | tuple | Networked server and client containers for cross-container tests |

## Adding tests

- **Shared static (every image):** add a `cases/static/test_<topic>.py`. Use
    `@pytest.mark.require_capability("…")` if the test only applies to
    images with a given capability.
- **Image-specific static:** add `cases/static/<image-family>/test_<topic>.py`.
    Tests in such subdirectories are **automatically** restricted to that
    image family (the plugin applies `@pytest.mark.image("<dir>")`
    during collection — no boilerplate per file or per subdir). The
    directory name is treated as a *family*: an `--image-name` matches
    the family if it equals the family exactly or has the form
    `<family>-<variant>`.
- **Shared runtime (every container):** add a `cases/runtime/test_<topic>.py`.
    Use `container_exec_shell("...")` for normal runtime tests. Use
    `container_exec([...])` only when the test must avoid a shell, such as
    distroless or minimal images. Tests are auto-marked with
    `@pytest.mark.runtime`.
- **Image-specific runtime:** add `cases/runtime/<image-family>/test_<topic>.py`.

### Dockerfile-based runtime tests

When a runtime test needs packages or config beyond what the base image
ships, give it its own directory with a `Dockerfile`:

```
cases/runtime/container-base/test_nginx/
    test_nginx.py       # test logic
    Dockerfile          # builds on top of the image-under-test
    nginx.conf          # supporting files (COPY'd in Dockerfile)
```

The Dockerfile must use `ARG BASE_IMAGE` / `FROM ${BASE_IMAGE}` — the
framework injects the image-under-test automatically:

```dockerfile
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y nginx && dnf clean all
COPY nginx.conf /etc/nginx/nginx.conf
```

Mark tests with `@pytest.mark.dockerfile()` to trigger the build. The
marker optionally accepts a path relative to the test file's directory
(defaults to `Dockerfile` in the same directory):

```python
# Auto-discovers Dockerfile in the same directory
@pytest.mark.dockerfile()
def test_nginx_config(container_exec_shell):
    result = container_exec_shell("nginx -t")
    assert result.exit_code == 0

# Explicit path to a different Dockerfile
@pytest.mark.dockerfile("alt/Dockerfile.debug")
def test_debug_variant(container_exec_shell):
    ...
```

Built images are cached per session — multiple tests sharing the same
Dockerfile only trigger one build.

> **Note:** All containers (plain and Dockerfile-based) run with
> `sleep infinity` as PID 1 — the Dockerfile's `CMD`/`ENTRYPOINT` is
> overridden. Tests that need a service should start it explicitly via
> `container_exec_shell("nginx")`. This keeps behaviour predictable and
> ensures each test controls exactly what runs.

For service tests, poll readiness before asserting on responses; do not assume the
service binds synchronously — use `wait_until_service_ready(exec_shell, probe_cmd,
contains=...)` from `utils.container_runtime`. Foreground services should be
backgrounded explicitly, for example
`container_exec_shell("nohup my-service > /tmp/my-service.log 2>&1 &")`.

## Adding a native-tool dependency

Each `utils/*.py` module declares the CLI tools it shells out to as
module-level `NativeTool` constants and uses them at the call sites:

```python
# utils/extract.py
GUESTMOUNT = NativeTool(
    name="guestmount",
    package_hint="libguestfs",
    reason="FUSE-mount VM images",
    when="vm",            # "always" | "vm" | "container"
)

def mount_vm_image(...):
    subprocess.run([GUESTMOUNT.name, "--ro", ...])
```

Construction registers the tool, and `pytest_configure` does a
preflight check against `$PATH` for every tool whose `when` matches
the current image type. Missing tools fail fast with the
`package_hint`. Run `uv run python -m utils.tools` to see the full
status.
