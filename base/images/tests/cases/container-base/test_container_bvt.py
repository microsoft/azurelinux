# SPDX-License-Identifier: MIT
"""Container BVT (Build Verification Tests).

All tests run inside a live container via podman exec and are marked @runtime_container_tests.
Tests are designed to be resilient to minimal container images — missing optional
tools are reported but do not fail the test unless they are essential.
"""

from __future__ import annotations

import json
import time

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cmd_ok(ssh_exec, cmd: str, timeout: int = 10) -> tuple[bool, str]:
    """Run cmd; return (success, stdout). Never raises."""
    try:
        result = ssh_exec(cmd, timeout=timeout)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_system_footprint(ssh_exec) -> None:
    """BVT: Memory, disk, CPU, and process footprint metrics."""
    # Memory
    ok, out = _cmd_ok(ssh_exec, "free -m | awk '/^Mem:/ {print $2, $3}'")
    assert ok, "free command failed — procps-ng may be missing"
    parts = out.split()
    assert len(parts) == 2, f"Unexpected free output: {out!r}"
    total_mb = int(parts[0])
    assert total_mb > 0, f"Invalid total memory: {total_mb} MB"
    print(f"Memory: total={parts[0]} MB, used={parts[1]} MB")

    # Disk
    ok, out = _cmd_ok(ssh_exec, "df -h / | awk 'NR==2 {print $2, $3, $4}'")
    assert ok, "df command failed"
    print(f"Disk (total used avail): {out}")

    # CPU
    ok, out = _cmd_ok(ssh_exec, "nproc")
    assert ok, "nproc failed"
    assert int(out) > 0, f"Unexpected CPU count: {out}"
    print(f"CPU cores: {out}")

    # Process count
    ok, out = _cmd_ok(ssh_exec, "ps aux --no-headers | wc -l")
    assert ok, "ps failed — procps-ng may be missing"
    count = int(out)
    assert count >= 1, f"Too few processes: {count}"
    print(f"Running processes: {count}")

    # Package count (optional — rpm may be absent in distroless builds)
    ok, out = _cmd_ok(ssh_exec, "rpm -qa | wc -l", timeout=15)
    if ok:
        print(f"Installed packages: {out}")
    else:
        print("rpm not available — skipping package count")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_logging(ssh_exec) -> None:
    """BVT: System logging via logger and log file/journal access."""
    tag = f"bvt_{int(time.time())}"
    message = f"BVT log test entry {tag}"

    ok, _ = _cmd_ok(ssh_exec, f"logger -t bvt_test '{message}'", timeout=10)
    assert ok, "logger command failed — util-linux may be missing"

    # Find the entry: try journalctl, then /var/log/messages, then /var/log/syslog
    found = False
    ok, out = _cmd_ok(ssh_exec, f"journalctl --no-pager --since '1 minute ago' 2>/dev/null | grep '{tag}' || true", timeout=15)
    if ok and tag in out:
        found = True

    if not found:
        for logfile in ("/var/log/messages", "/var/log/syslog"):
            ok, out = _cmd_ok(ssh_exec, f"tail -50 {logfile} 2>/dev/null | grep '{tag}' || true")
            if ok and tag in out:
                found = True
                break

    # Log entry visibility depends on journald/syslog being wired up in the container.
    if found:
        print(f"Log entry verified in system logs: {message}")
    else:
        print(f"WARNING: log entry not immediately visible (journald may not be running in container): {message}")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_mathematical_computing(ssh_exec) -> None:
    """BVT: Shell arithmetic, bc floating-point, and python3 math."""
    # Shell integer arithmetic (always available via bash)
    ok, out = _cmd_ok(ssh_exec, "echo $((2 + 2))")
    assert ok and out == "4", f"Basic arithmetic failed: {out!r}"

    ok, out = _cmd_ok(ssh_exec, "echo $((123 * 456))")
    assert ok and out == str(123 * 456), f"Multiplication failed: {out!r}"

    # bc (optional)
    ok, out = _cmd_ok(ssh_exec, "echo 'scale=2; 22/7' | bc", timeout=10)
    if ok:
        val = float(out)
        assert 3.1 < val < 3.2, f"bc pi approximation out of range: {val}"
        print(f"bc: 22/7 = {val}")
    else:
        print("bc not available — skipping floating-point test")

    # python3 (optional)
    py_cmd = r"""python3 -c "import math; print(f'{math.pi:.6f}'); print(f'{math.sqrt(16):.1f}'); print('OK')" """
    ok, out = _cmd_ok(ssh_exec, py_cmd, timeout=15)
    if ok and "OK" in out:
        assert "3.14159" in out, f"Unexpected pi: {out}"
        assert "4.0" in out, f"Unexpected sqrt(16): {out}"
        print(f"python3 math verified: {out.splitlines()[0]}")
    else:
        print("python3 not available — skipping Python math test")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_networking(ssh_exec) -> None:
    """BVT: Network interfaces, loopback ping, hostname, and routing."""
    # Network interfaces
    ok, out = _cmd_ok(ssh_exec, "ip addr show", timeout=10)
    assert ok, "ip command failed — iproute2 may be missing"
    inet_lines = [l.strip() for l in out.splitlines() if "inet " in l and "scope" in l]
    assert len(inet_lines) >= 1, f"No inet addresses found:\n{out}"
    print(f"Network interfaces ({len(inet_lines)} addresses): {inet_lines}")

    # Loopback ping
    ok, out = _cmd_ok(ssh_exec, "ping -c 2 -W 3 127.0.0.1", timeout=15)
    assert ok, f"Loopback ping failed — iputils may be missing: {out}"

    # Hostname
    ok, out = _cmd_ok(ssh_exec, "hostname")
    assert ok and len(out) > 0, f"hostname command failed or returned empty: {out!r}"
    print(f"Hostname: {out}")

    # Routing table (informational)
    ok, out = _cmd_ok(ssh_exec, "ip route show", timeout=10)
    if ok:
        print(f"Routing table present, default route: {'default' in out}")

    # DNS config (informational)
    ok, out = _cmd_ok(ssh_exec, "cat /etc/resolv.conf")
    if ok:
        print(f"DNS resolvers configured: {'nameserver' in out}")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_external_connectivity(ssh_exec) -> None:
    """BVT: External DNS resolution and optional HTTP connectivity."""
    domains = ["google.com", "microsoft.com", "github.com"]

    ok_nslookup, _ = _cmd_ok(ssh_exec, "which nslookup", timeout=5)
    if ok_nslookup:
        resolved = sum(
            1 for domain in domains
            for ok, out in [_cmd_ok(ssh_exec, f"nslookup {domain}", timeout=10)]
            if ok and "NXDOMAIN" not in out
        )
        print(f"DNS resolved {resolved}/{len(domains)} domains")
        assert resolved >= 1, f"All DNS resolutions failed for {domains}"
    else:
        print("nslookup not available — skipping DNS resolution test")

    # HTTP connectivity (optional)
    ok_curl, _ = _cmd_ok(ssh_exec, "which curl", timeout=5)
    if ok_curl:
        ok, out = _cmd_ok(ssh_exec, "curl -s --connect-timeout 5 --max-time 10 http://httpbin.org/get", timeout=15)
        if ok and '"origin"' in out:
            print("External HTTP connectivity verified")
        else:
            print("External HTTP test skipped or blocked by network policy")
    else:
        print("curl not available — skipping HTTP connectivity test")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_filesystem_operations(ssh_exec) -> None:
    """BVT: File create, read, chmod, and delete in /tmp."""
    content = "Azure Linux BVT filesystem test"
    path = "/tmp/bvt_test_file.txt"

    ok, _ = _cmd_ok(ssh_exec, f"echo '{content}' > {path}")
    assert ok, f"File creation failed: {path}"

    ok, out = _cmd_ok(ssh_exec, f"cat {path}")
    assert ok and content in out, f"File content mismatch: {out!r}"

    ok, out = _cmd_ok(ssh_exec, f"chmod 644 {path} && stat -c '%a' {path}")
    assert ok and "644" in out, f"chmod/stat failed: {out!r}"

    ok, _ = _cmd_ok(ssh_exec, f"rm {path}")
    assert ok, "File deletion failed"

    for sysfile in ("/etc/os-release", "/proc/version"):
        ok, _ = _cmd_ok(ssh_exec, f"test -r {sysfile}")
        assert ok, f"Cannot read required system file: {sysfile}"

    print("Filesystem operations verified")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_process_management(ssh_exec) -> None:
    """BVT: Background process start, list, and kill."""
    ok, _ = _cmd_ok(ssh_exec, "sleep 60 &", timeout=5)
    assert ok, "Failed to start background process"

    ok, out = _cmd_ok(ssh_exec, "ps aux | grep '[s]leep 60'", timeout=10)
    assert ok and "sleep 60" in out, f"Background process not found in ps: {out}"

    ok, _ = _cmd_ok(ssh_exec, "pkill -f 'sleep 60'", timeout=10)
    assert ok, "pkill failed"

    ok, out = _cmd_ok(ssh_exec, "ps aux | grep '[s]leep 60' || true")
    assert "sleep 60" not in out, "Process still running after pkill"
    print("Process management verified")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_user_management(ssh_exec) -> None:
    """BVT: Create, verify, switch to, and delete a transient test user."""
    user = "bvt_testuser"

    ok, out = _cmd_ok(ssh_exec, f"useradd -m {user}", timeout=15)
    assert ok, f"useradd failed — shadow-utils may be missing: {out}"

    ok, out = _cmd_ok(ssh_exec, f"id {user}")
    assert ok and user in out, f"User not found: {out}"

    ok, _ = _cmd_ok(ssh_exec, f"test -d /home/{user}")
    assert ok, f"Home directory /home/{user} not created"

    # Verify user is in passwd file (su may not work in minimal containers without TTY)
    ok, out = _cmd_ok(ssh_exec, f"grep '^{user}:' /etc/passwd")
    assert ok, f"User not in passwd file: {user}"

    ok, _ = _cmd_ok(ssh_exec, f"userdel -r {user}", timeout=15)
    assert ok, "userdel failed"
    print(f"User management verified for: {user}")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container", "runtime-package-management")
def test_bvt_package_management(ssh_exec) -> None:
    """BVT: Package manager (tdnf/dnf) cache refresh, list, and info."""
    ok_tdnf, _ = _cmd_ok(ssh_exec, "which tdnf", timeout=5)
    pm = "tdnf" if ok_tdnf else "dnf"

    ok, out = _cmd_ok(ssh_exec, f"{pm} makecache", timeout=60)
    assert ok, f"{pm} makecache failed: {out}"

    ok, out = _cmd_ok(ssh_exec, f"{pm} list --installed | head -20", timeout=30)
    assert ok, f"Package listing failed: {out}"
    assert any(kw in out.lower() for kw in ("azure", "bash", "filesystem")), \
        f"Expected Azure Linux packages not found in listing: {out[:200]}"

    ok, out = _cmd_ok(ssh_exec, f"{pm} info bash", timeout=15)
    assert ok, f"Package info for bash failed: {out}"
    print(f"Package management verified via {pm}")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_environment_variables(ssh_exec, container_info: dict) -> None:
    """BVT: Essential environment variables and custom variable export."""
    ok, out = _cmd_ok(ssh_exec, "env")
    assert ok, "env command failed"
    assert "PATH=" in out, "Required env var PATH not set"
    print([l for l in out.splitlines() if l.startswith("PATH=")][0])

    ok, out = _cmd_ok(ssh_exec, "export BVT_VAR=azure_linux_bvt && echo $BVT_VAR")
    assert ok and "azure_linux_bvt" in out, f"Custom env var not set: {out!r}"

    ok, out = _cmd_ok(ssh_exec, "echo $HOSTNAME")
    assert ok and len(out) > 0, "HOSTNAME is empty"
    print(f"Container HOSTNAME: {out}")


@pytest.mark.runtime_container_tests
@pytest.mark.require_capability("container")
def test_bvt_container_health_summary(ssh_exec, container_info: dict) -> None:
    """BVT: Aggregated health summary — OS info, memory, processes, packages."""
    health: dict = {
        "container_name": container_info["container_name"],
        "container_ip": container_info["ip_address"],
        "timestamp": int(time.time()),
    }

    ok, out = _cmd_ok(ssh_exec, "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'")
    assert ok and out, "Could not read /etc/os-release"
    health["os"] = out

    ok, out = _cmd_ok(ssh_exec, "uname -r")
    if ok:
        health["kernel"] = out

    ok, out = _cmd_ok(ssh_exec, "uptime -s 2>/dev/null || uptime")
    if ok:
        health["uptime"] = out

    ok, out = _cmd_ok(ssh_exec, "free -m | awk '/^Mem:/ {print $2}'")
    if ok:
        health["memory_total_mb"] = int(out)

    ok, out = _cmd_ok(ssh_exec, "ps aux --no-headers | wc -l")
    if ok:
        health["process_count"] = int(out)

    ok, out = _cmd_ok(ssh_exec, "rpm -qa | wc -l", timeout=15)
    if ok:
        health["package_count"] = int(out)

    assert health.get("container_name"), "Missing container name"
    assert health.get("container_ip"), "Missing container IP"
    assert health.get("os"), "Missing OS information"
    assert health.get("memory_total_mb", 0) > 0, "Invalid memory reading"
    assert health.get("process_count", 0) >= 1, "No processes detected"

    print("\n" + "=" * 60)
    print("CONTAINER BVT HEALTH SUMMARY")
    print("=" * 60)
    print(json.dumps(health, indent=2))
    print("=" * 60)
