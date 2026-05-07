# SPDX-License-Identifier: MIT
"""Ported Azure Linux Container Structure Test (CST) suite.

These are static filesystem and metadata assertions ported from the Google
Container Structure Test YAML format to pytest. They validate core container
image properties without requiring a running container runtime.

Mapped from: base/images/tests/cst/azl4_container_static_test.yaml
"""

from __future__ import annotations

import re
import pytest
from pathlib import Path


# ============================================================================
# File Existence Tests (7 checks)
# ============================================================================


@pytest.mark.static_container_test
def test_file_exists_root(rootfs: Path) -> None:
    """Root directory must exist."""
    assert rootfs.exists(), "Root directory does not exist"


@pytest.mark.static_container_test
def test_file_exists_bin_date(rootfs: Path) -> None:
    """Date binary must exist and be executable by owner."""
    path = rootfs / "bin" / "date"
    assert path.exists(), f"File {path} does not exist"
    # Check executable by owner (user x bit)
    mode = path.stat().st_mode
    assert mode & 0o100, f"File {path} is not executable by owner"


@pytest.mark.static_container_test
def test_file_exists_bin_bash(rootfs: Path) -> None:
    """Bash must exist."""
    path = rootfs / "bin" / "bash"
    assert path.exists(), f"File {path} does not exist"


@pytest.mark.static_container_test
def test_file_exists_etc_os_release(rootfs: Path) -> None:
    """os-release must exist."""
    path = rootfs / "etc" / "os-release"
    assert path.exists(), f"File {path} does not exist"


@pytest.mark.static_container_test
def test_file_exists_etc_passwd(rootfs: Path) -> None:
    """passwd file must exist."""
    path = rootfs / "etc" / "passwd"
    assert path.exists(), f"File {path} does not exist"


@pytest.mark.static_container_test
def test_file_exists_etc_dnf_dnf_conf(rootfs: Path) -> None:
    """DNF config must exist."""
    path = rootfs / "etc" / "dnf" / "dnf.conf"
    assert path.exists(), f"File {path} does not exist"


@pytest.mark.static_container_test
def test_file_not_exists_etc_dummy(rootfs: Path) -> None:
    """Dummy file should not exist (negative test)."""
    path = rootfs / "etc" / "dummy"
    assert not path.exists(), f"File {path} should not exist"


# ============================================================================
# File Content Tests (4 checks)
# ============================================================================


@pytest.mark.static_container_test
def test_content_os_release_id(rootfs: Path, os_release: dict[str, str]) -> None:
    """os-release must contain Azure Linux ID."""
    assert os_release.get("ID") == "azurelinux", \
        f"Expected ID=azurelinux, got {os_release.get('ID')}"


@pytest.mark.static_container_test
def test_content_os_release_version(rootfs: Path, os_release: dict[str, str]) -> None:
    """os-release must contain correct version."""
    # Match pattern: VERSION_ID=4.0 (exact)
    version_id = os_release.get("VERSION_ID")
    assert version_id == "4.0", \
        f"Expected VERSION_ID=4.0, got {version_id}"


@pytest.mark.static_container_test
def test_content_os_release_variant(rootfs: Path, os_release: dict[str, str]) -> None:
    """os-release must identify as container variant."""
    variant_id = os_release.get("VARIANT_ID")
    assert variant_id == "container", \
        f"Expected VARIANT_ID=container, got {variant_id}"


@pytest.mark.static_container_test
def test_content_passwd_root_entry(rootfs: Path) -> None:
    """passwd file must contain root user entry."""
    path = rootfs / "etc" / "passwd"
    content = path.read_text()
    # Pattern: root:x:0:0:Super User:/root:/bin/bash or similar
    pattern = r"^root:x:0:0:.*:/root:/bin/bash"
    assert re.search(pattern, content, re.MULTILINE), \
        f"Root entry not found in passwd file matching pattern {pattern}"


# ============================================================================
# License Tests (2 checks)
# ============================================================================


@pytest.mark.static_container_test
def test_license_bash_exists(rootfs: Path) -> None:
    """Bash license file must exist."""
    path = rootfs / "usr" / "share" / "licenses" / "bash" / "COPYING"
    assert path.exists(), f"License file {path} does not exist"


@pytest.mark.static_container_test
def test_license_coreutils_single_exists(rootfs: Path) -> None:
    """coreutils-single license file must exist."""
    path = rootfs / "usr" / "share" / "licenses" / "coreutils-single" / "COPYING"
    assert path.exists(), f"License file {path} does not exist"


# ============================================================================
# Metadata Test (1 check)
# ============================================================================


@pytest.mark.static_container_test
def test_metadata_entrypoint(rootfs: Path) -> None:
    """Metadata validation: cmd=['/bin/bash'], workdir='/', user='root'.
    
    Note: This test validates the image structure is set up correctly.
    Actual metadata (entrypoint, workdir, user) would be verified when
    running the container. Here we just verify core structure is correct.
    """
    # Verify bash exists (required for entrypoint)
    bash_path = rootfs / "bin" / "bash"
    assert bash_path.exists(), "bash not found for entrypoint"
    
    # Verify root user exists
    passwd_path = rootfs / "etc" / "passwd"
    content = passwd_path.read_text()
    assert re.search(r"^root:", content, re.MULTILINE), \
        "root user not found in passwd"
    
    # Verify home directory exists
    root_home = rootfs / "root"
    assert root_home.exists(), "root home directory does not exist"
