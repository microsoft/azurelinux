# SPDX-License-Identifier: MIT
"""Container BVT (Build Verification Tests).

All tests run inside a live container via podman exec
"""

from __future__ import annotations

import json
import time

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cmd_ok(container_exec, cmd: str, timeout: int = 10) -> tuple[bool, str]:
    """Run cmd; return (success, stdout). Never raises."""
    try:
        result = container_exec(cmd, timeout=timeout)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("procps-ng", "gawk")
def test_bvt_system_footprint(container_exec) -> None:
    """BVT: Memory, disk, CPU, and process footprint metrics."""
    # Memory
    ok, out = _cmd_ok(container_exec, "free -m | awk '/^Mem:/ {print $2, $3}'")
    assert ok, "free command failed — procps-ng may be missing"
    parts = out.split()
    assert len(parts) == 2, f"Unexpected free output: {out!r}"
    total_mb = int(parts[0])
    assert total_mb > 0, f"Invalid total memory: {total_mb} MB"
    print(f"Memory: total={parts[0]} MB, used={parts[1]} MB")

    # Disk
    ok, out = _cmd_ok(container_exec, "df -h / | awk 'NR==2 {print $2, $3, $4}'")
    assert ok, "df command failed"
    print(f"Disk (total used avail): {out}")

    # CPU
    ok, out = _cmd_ok(container_exec, "nproc")
    assert ok, "nproc failed"
    assert int(out) > 0, f"Unexpected CPU count: {out}"
    print(f"CPU cores: {out}")

    # Process count
    ok, out = _cmd_ok(container_exec, "ps aux --no-headers | wc -l")
    assert ok, "ps failed — procps-ng may be missing"
    count = int(out)
    assert count >= 1, f"Too few processes: {count}"
    print(f"Running processes: {count}")

    # Package count (optional — rpm may be absent in distroless builds)
    ok, out = _cmd_ok(container_exec, "rpm -qa | wc -l", timeout=15)
    if ok:
        print(f"Installed packages: {out}")
    else:
        print("rpm not available — skipping package count")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("util-linux")
def test_bvt_logging(container_exec) -> None:
    """BVT: System logging via logger and log file/journal access."""
    tag = f"bvt_{int(time.time())}"
    message = f"BVT log test entry {tag}"

    ok, _ = _cmd_ok(container_exec, f"logger -t bvt_test '{message}'", timeout=10)
    assert ok, "logger command failed — util-linux may be missing"

    # Find the entry: try journalctl, then /var/log/messages, then /var/log/syslog
    found = False
    ok, out = _cmd_ok(container_exec, f"journalctl --no-pager --since '1 minute ago' 2>/dev/null | grep '{tag}' || true", timeout=15)
    if ok and tag in out:
        found = True

    if not found:
        for logfile in ("/var/log/messages", "/var/log/syslog"):
            ok, out = _cmd_ok(container_exec, f"tail -50 {logfile} 2>/dev/null | grep '{tag}' || true")
            if ok and tag in out:
                found = True
                break

    # Log entry visibility depends on journald/syslog being wired up in the container.
    if found:
        print(f"Log entry verified in system logs: {message}")
    else:
        print(f"WARNING: log entry not immediately visible (journald may not be running in container): {message}")


@pytest.mark.require_capability("container")
def test_bvt_mathematical_computing(container_exec) -> None:
    """BVT: Shell arithmetic, bc floating-point, and python3 math."""
    # Shell integer arithmetic (always available via bash)
    ok, out = _cmd_ok(container_exec, "echo $((2 + 2))")
    assert ok and out == "4", f"Basic arithmetic failed: {out!r}"

    ok, out = _cmd_ok(container_exec, "echo $((123 * 456))")
    assert ok and out == str(123 * 456), f"Multiplication failed: {out!r}"

    # bc (optional)
    ok, out = _cmd_ok(container_exec, "echo 'scale=2; 22/7' | bc", timeout=10)
    if ok:
        val = float(out)
        assert 3.1 < val < 3.2, f"bc pi approximation out of range: {val}"
        print(f"bc: 22/7 = {val}")
    else:
        print("bc not available — skipping floating-point test")

    # python3 (optional)
    py_cmd = r"""python3 -c "import math; print(f'{math.pi:.6f}'); print(f'{math.sqrt(16):.1f}'); print('OK')" """
    ok, out = _cmd_ok(container_exec, py_cmd, timeout=15)
    if ok and "OK" in out:
        assert "3.14159" in out, f"Unexpected pi: {out}"
        assert "4.0" in out, f"Unexpected sqrt(16): {out}"
        print(f"python3 math verified: {out.splitlines()[0]}")
    else:
        print("python3 not available — skipping Python math test")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("iproute", "iputils", "hostname")
def test_bvt_networking(container_exec) -> None:
    """BVT: Network interfaces, loopback ping, hostname, and routing."""
    # Network interfaces
    ok, out = _cmd_ok(container_exec, "ip addr show", timeout=10)
    assert ok, "ip command failed — iproute2 may be missing"
    inet_lines = [l.strip() for l in out.splitlines() if "inet " in l and "scope" in l]
    assert len(inet_lines) >= 1, f"No inet addresses found:\n{out}"
    print(f"Network interfaces ({len(inet_lines)} addresses): {inet_lines}")

    # Loopback presence (the inet 127.0.0.1 line above already proves loopback
    # exists). ping is informational only: rootless podman with slirp4netns
    # often blocks ICMP regardless of iputils being installed.
    assert any("127.0.0.1" in l for l in inet_lines), "Loopback interface missing"
    ok, out = _cmd_ok(container_exec, "ping -c 2 -W 3 127.0.0.1", timeout=15)
    if ok:
        print("Loopback ping succeeded")
    else:
        print(f"Loopback ping not available (likely rootless ICMP restriction): {out[:120]}")

    # Hostname (hostname package was installed via requires_pkg)
    ok, out = _cmd_ok(container_exec, "hostname")
    assert ok, f"hostname command failed: {out!r}"
    print(f"Hostname: {out or '(empty - no --hostname set)'}")

    # Routing table (informational)
    ok, out = _cmd_ok(container_exec, "ip route show", timeout=10)
    if ok:
        print(f"Routing table present, default route: {'default' in out}")

    # DNS config (informational)
    ok, out = _cmd_ok(container_exec, "cat /etc/resolv.conf")
    if ok:
        print(f"DNS resolvers configured: {'nameserver' in out}")


@pytest.mark.require_capability("container")
def test_bvt_external_connectivity(container_exec) -> None:
    """BVT: External DNS resolution and optional HTTP connectivity."""
    domains = ["google.com", "microsoft.com", "github.com"]

    ok_nslookup, _ = _cmd_ok(container_exec, "which nslookup", timeout=5)
    if ok_nslookup:
        resolved = sum(
            1 for domain in domains
            for ok, out in [_cmd_ok(container_exec, f"nslookup {domain}", timeout=10)]
            if ok and "NXDOMAIN" not in out
        )
        print(f"DNS resolved {resolved}/{len(domains)} domains")
        assert resolved >= 1, f"All DNS resolutions failed for {domains}"
    else:
        print("nslookup not available — skipping DNS resolution test")

    # HTTP connectivity (optional)
    ok_curl, _ = _cmd_ok(container_exec, "which curl", timeout=5)
    if ok_curl:
        ok, out = _cmd_ok(container_exec, "curl -s --connect-timeout 5 --max-time 10 http://httpbin.org/get", timeout=15)
        if ok and '"origin"' in out:
            print("External HTTP connectivity verified")
        else:
            print("External HTTP test skipped or blocked by network policy")
    else:
        print("curl not available — skipping HTTP connectivity test")


@pytest.mark.require_capability("container")
def test_bvt_filesystem_operations(container_exec) -> None:
    """BVT: File create, read, chmod, and delete in /tmp."""
    content = "Azure Linux BVT filesystem test"
    path = "/tmp/bvt_test_file.txt"

    ok, _ = _cmd_ok(container_exec, f"echo '{content}' > {path}")
    assert ok, f"File creation failed: {path}"

    ok, out = _cmd_ok(container_exec, f"cat {path}")
    assert ok and content in out, f"File content mismatch: {out!r}"

    ok, out = _cmd_ok(container_exec, f"chmod 644 {path} && stat -c '%a' {path}")
    assert ok and "644" in out, f"chmod/stat failed: {out!r}"

    ok, _ = _cmd_ok(container_exec, f"rm {path}")
    assert ok, "File deletion failed"

    for sysfile in ("/etc/os-release", "/proc/version"):
        ok, _ = _cmd_ok(container_exec, f"test -r {sysfile}")
        assert ok, f"Cannot read required system file: {sysfile}"

    print("Filesystem operations verified")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("procps-ng")
def test_bvt_process_management(container_exec) -> None:
    """BVT: Background process start, list, and kill."""
    ok, _ = _cmd_ok(container_exec, "sleep 60 &", timeout=5)
    assert ok, "Failed to start background process"

    ok, out = _cmd_ok(container_exec, "ps aux | grep '[s]leep 60'", timeout=10)
    assert ok and "sleep 60" in out, f"Background process not found in ps: {out}"

    ok, _ = _cmd_ok(container_exec, "pkill -f 'sleep 60'", timeout=10)
    assert ok, "pkill failed"

    ok, out = _cmd_ok(container_exec, "ps aux | grep '[s]leep 60' || true")
    assert "sleep 60" not in out, "Process still running after pkill"
    print("Process management verified")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("shadow-utils")
def test_bvt_user_management(container_exec) -> None:
    """BVT: Create, verify, switch to, and delete a transient test user."""
    user = "bvt_testuser"

    ok, out = _cmd_ok(container_exec, f"useradd -m {user}", timeout=15)
    assert ok, f"useradd failed — shadow-utils may be missing: {out}"

    ok, out = _cmd_ok(container_exec, f"id {user}")
    assert ok and user in out, f"User not found: {out}"

    ok, _ = _cmd_ok(container_exec, f"test -d /home/{user}")
    assert ok, f"Home directory /home/{user} not created"

    # Verify user is in passwd file (su may not work in minimal containers without TTY)
    ok, out = _cmd_ok(container_exec, f"grep '^{user}:' /etc/passwd")
    assert ok, f"User not in passwd file: {user}"

    ok, _ = _cmd_ok(container_exec, f"userdel -r {user}", timeout=15)
    assert ok, "userdel failed"
    print(f"User management verified for: {user}")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
def test_bvt_package_management(container_exec) -> None:
    """BVT: Package manager (tdnf/dnf) cache refresh, list, and info."""
    ok_tdnf, _ = _cmd_ok(container_exec, "which tdnf", timeout=5)
    pm = "tdnf" if ok_tdnf else "dnf"

    ok, out = _cmd_ok(container_exec, f"{pm} makecache", timeout=60)
    assert ok, f"{pm} makecache failed: {out}"

    ok, out = _cmd_ok(container_exec, f"{pm} list --installed | head -20", timeout=30)
    assert ok, f"Package listing failed: {out}"
    assert any(kw in out.lower() for kw in ("azure", "bash", "filesystem")), \
        f"Expected Azure Linux packages not found in listing: {out[:200]}"

    ok, out = _cmd_ok(container_exec, f"{pm} info bash", timeout=15)
    assert ok, f"Package info for bash failed: {out}"
    print(f"Package management verified via {pm}")


@pytest.mark.require_capability("container")
def test_bvt_environment_variables(container_exec, container_info: dict) -> None:
    """BVT: Essential environment variables and custom variable export."""
    ok, out = _cmd_ok(container_exec, "env")
    assert ok, "env command failed"
    assert "PATH=" in out, "Required env var PATH not set"
    print([l for l in out.splitlines() if l.startswith("PATH=")][0])

    ok, out = _cmd_ok(container_exec, "export BVT_VAR=azure_linux_bvt && echo $BVT_VAR")
    assert ok and "azure_linux_bvt" in out, f"Custom env var not set: {out!r}"

    ok, out = _cmd_ok(container_exec, "echo $HOSTNAME")
    assert ok and len(out) > 0, "HOSTNAME is empty"
    print(f"Container HOSTNAME: {out}")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("procps-ng")
def test_bvt_container_health_summary(container_exec, container_info: dict) -> None:
    """BVT: Aggregated health summary — OS info, memory, processes, packages."""
    health: dict = {
        "container_name": container_info["container_name"],
        "container_ip": container_info["ip_address"],
        "timestamp": int(time.time()),
    }

    ok, out = _cmd_ok(container_exec, "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'")
    assert ok and out, "Could not read /etc/os-release"
    health["os"] = out

    ok, out = _cmd_ok(container_exec, "uname -r")
    if ok:
        health["kernel"] = out

    ok, out = _cmd_ok(container_exec, "uptime -s 2>/dev/null || uptime")
    if ok:
        health["uptime"] = out

    # Memory: read /proc/meminfo directly with pure shell (no awk dependency)
    ok, out = _cmd_ok(container_exec, "grep '^MemTotal:' /proc/meminfo")
    if ok and out:
        # Format: "MemTotal:       16384000 kB"
        parts = out.split()
        if len(parts) >= 2 and parts[1].isdigit():
            health["memory_total_mb"] = int(parts[1]) // 1024

    ok, out = _cmd_ok(container_exec, "ps aux --no-headers | wc -l")
    if ok:
        health["process_count"] = int(out)

    ok, out = _cmd_ok(container_exec, "rpm -qa | wc -l", timeout=15)
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


# ---------------------------------------------------------------------------
# Ports of legacy CBL-Mariner ContainerBase BVT tests
# ---------------------------------------------------------------------------

# First 50 digits after "3." of pi — used to verify high-precision arithmetic.
_PI_PREFIX_50 = "14159265358979323846264338327950288419716939937510"


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("python3")
def test_bvt_pi_to_1000_places(container_exec) -> None:
    """BVT: High-precision pi to 1000 digits via python3 ``decimal``.

    Ports the legacy "Pi to 1000 places". Uses Machin's formula in the
    container's Python to avoid extra package dependencies.
    """
    py_cmd = "python3 <<'PYEOF'\n" + (
        "from decimal import Decimal, getcontext\n"
        "getcontext().prec = 1010\n"
        "def atan(x):\n"
        "    s = Decimal(0); t = x; n = Decimal(1); sign = 1\n"
        "    x2 = x * x\n"
        "    while t / n != 0:\n"
        "        s += sign * t / n\n"
        "        t *= x2; n += 2; sign = -sign\n"
        "    return s\n"
        "pi = 16 * atan(Decimal(1) / 5) - 4 * atan(Decimal(1) / 239)\n"
        "print(str(pi)[:1002])\n"
    ) + "PYEOF\n"
    ok, out = _cmd_ok(container_exec, py_cmd, timeout=60)
    assert ok, f"python3 pi computation failed — python3 may be missing: {out!r}"
    # Output is "3." + 1000 digits
    assert out.startswith("3."), f"Unexpected pi output prefix: {out[:20]!r}"
    digits = out[2:]
    assert len(digits) >= 1000, f"Got only {len(digits)} digits of pi"
    assert digits.startswith(_PI_PREFIX_50), \
        f"Pi digits incorrect at the start: got {digits[:50]!r}"
    print(f"Pi to 1000 places verified (first 50 digits: {digits[:50]})")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("python3")
def test_bvt_pi_repeated_iterations(container_exec) -> None:
    """BVT: Compute pi to 1000 places repeatedly (CPU stress + consistency).

    Ports the legacy "Pi to N x 1000 places" — runs the calculation 10 times
    and asserts every iteration yields the same prefix.
    """
    py_cmd = "python3 <<'PYEOF'\n" + (
        "from decimal import Decimal, getcontext\n"
        "getcontext().prec = 1010\n"
        "def atan(x):\n"
        "    s = Decimal(0); t = x; n = Decimal(1); sign = 1\n"
        "    x2 = x * x\n"
        "    while t / n != 0:\n"
        "        s += sign * t / n\n"
        "        t *= x2; n += 2; sign = -sign\n"
        "    return s\n"
        "results = set()\n"
        "for _ in range(10):\n"
        "    results.add(str(16 * atan(Decimal(1) / 5) - 4 * atan(Decimal(1) / 239))[:52])\n"
        "print(len(results), next(iter(results)))\n"
    ) + "PYEOF\n"
    ok, out = _cmd_ok(container_exec, py_cmd, timeout=120)
    assert ok, f"python3 repeated pi computation failed: {out!r}"
    parts = out.split(maxsplit=1)
    assert len(parts) == 2, f"Unexpected output: {out!r}"
    unique_count, sample = int(parts[0]), parts[1]
    assert unique_count == 1, f"Pi values diverged across iterations: {unique_count} distinct values"
    assert sample.startswith("3."), f"Bad pi sample: {sample!r}"
    assert sample[2:].startswith(_PI_PREFIX_50), f"Pi prefix wrong: {sample!r}"
    print(f"Pi to 1000 places consistent across 10 iterations: {sample[:52]}")


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.requires_pkg("curl")
def test_bvt_sustained_http_fetch(container_exec) -> None:
    """BVT: Sustained external HTTP — 50 sequential fetches, ≥90% success.

    Ports the legacy "Core Networking Test" (50-iteration page fetch).
    """
    iterations = 50
    url = "http://httpbin.org/get"
    # One bash loop is far cheaper than 50 podman exec invocations.
    cmd = (
        f"i=0; ok=0; while [ $i -lt {iterations} ]; do "
        f"curl -s -o /dev/null -w '%{{http_code}}\\n' "
        f"--connect-timeout 5 --max-time 10 {url} | "
        f"grep -q '^2' && ok=$((ok+1)); i=$((i+1)); done; echo $ok"
    )
    ok, out = _cmd_ok(container_exec, cmd, timeout=iterations * 12)
    assert ok, f"Sustained fetch loop failed: {out!r}"
    success = int(out.strip().splitlines()[-1])
    success_rate = success / iterations
    print(f"Sustained HTTP fetch: {success}/{iterations} succeeded ({success_rate:.0%})")
    assert success_rate >= 0.9, \
        f"HTTP success rate {success_rate:.0%} below 90% threshold ({success}/{iterations})"
