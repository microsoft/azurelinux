#!/usr/bin/env python3
"""Automate Azure Linux ISO install in QEMU over serial console.

This script boots an installer ISO, watches serial output, responds to known
prompts, waits for first boot, logs in, and verifies the installed system is up.

Example:
  python3 scripts/auto_iso_install_qemu.py \
      --iso /path/to/azl4-iso-installer.iso \
      --disk ./azl4-test.qcow2 \
      --log ./azl4-install.log
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional, Pattern


# --- Constants / compiled regexes ---

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
CPR_REPLY_RE = re.compile(r"(?:\x1B\[)?\d+;\d+R")
DSR_QUERY_RE = re.compile(r"\x1B\[[0-9;]*n")


# --- Data structures ---

@dataclass
class Responder:
    """One-shot pattern->reply rule."""
    pattern: Pattern[str]
    reply: str
    note: str
    max_hits: int = 1
    hits: int = 0

    def can_fire(self) -> bool:
        return self.hits < self.max_hits


@dataclass
class SequentialPrompts:
    """Track a sequence of prompts that must be answered in order."""
    prompts: list[tuple[Pattern[str], str, str]]  # (pattern, reply, cooldown_key)
    note_prefix: str
    entries: int = 0

    @property
    def done(self) -> bool:
        return self.entries >= len(self.prompts)

    @property
    def current(self) -> tuple[Pattern[str], str, str]:
        return self.prompts[self.entries]


@dataclass
class State:
    """Mutable automation state for the main loop."""
    installed: bool = False
    logged_in: bool = False
    login_verified: bool = False
    login_verification_sent: bool = False
    boot_analyze_done: bool = False
    boot_analyze_sent: bool = False
    spoke_selected: bool = False
    begin_attempts: int = 0
    root_spoke_choice: Optional[str] = None
    hub_begin_key: str = "b"
    root_spoke_lookup_notice_sent: bool = False
    awaiting_login_password: bool = False
    anaconda_started: bool = False
    install_started: bool = False
    post_install_enter_sent: bool = False
    poweroff_sent: bool = False
    login_password_sent: bool = False
    boot_luks_unlock_count: int = 0
    last_sent: dict[str, float] = field(default_factory=dict)


# --- Utility functions ---

def run_checked(cmd: List[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(shlex.quote(c) for c in cmd)}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def ensure_tools() -> None:
    machine = platform.machine()
    if machine not in ("x86_64", "AMD64"):
        raise RuntimeError(
            f"This script only supports x86_64 hosts (detected: {machine}). "
            f"aarch64 QEMU ISO boot is not currently supported."
        )
    for tool in ("qemu-system-x86_64", "qemu-img"):
        if subprocess.run(["bash", "-lc", f"command -v {tool}"], capture_output=True).returncode != 0:
            raise RuntimeError(f"Required tool not found: {tool}")


def ensure_disk(path: str, size: str) -> bool:
    """Create disk if missing. Returns True if disk already existed."""
    if os.path.exists(path):
        return True
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    run_checked(["qemu-img", "create", "-f", "qcow2", path, size])
    return False


def send_line(proc: subprocess.Popen, line: str) -> None:
    if proc.stdin is None:
        return
    proc.stdin.write((line + "\n").encode("utf-8"))
    proc.stdin.flush()


def maybe_send(
    proc: subprocess.Popen,
    buf: str,
    pattern: Pattern[str],
    reply: str,
    note: str,
    st: State,
    key: str,
    cooldown: float = 2.0,
) -> bool:
    """Send reply if pattern matches buf and cooldown has elapsed."""
    if not pattern.search(buf):
        return False
    now = time.time()
    if now - st.last_sent.get(key, 0.0) < cooldown:
        return False
    send_line(proc, reply)
    st.last_sent[key] = now
    print(f"\n[AUTO] {note}: sent {reply!r}")
    return True


def advance_seq(proc: subprocess.Popen, buf: str, seq: SequentialPrompts, st: State, cooldown: float = 2.0) -> bool:
    """Try to advance a sequential prompt sequence by one step."""
    if seq.done:
        return False
    pat, reply, key = seq.current
    if maybe_send(proc, buf, pat, reply, f"{seq.note_prefix} ({seq.entries + 1}/{len(seq.prompts)})", st, key, cooldown):
        seq.entries += 1
        return True
    return False


def sanitize(text: str) -> str:
    """Strip ANSI escapes and normalize line endings for regex matching."""
    clean = ANSI_ESCAPE_RE.sub("", text)
    clean = CPR_REPLY_RE.sub("", clean)
    return clean.replace("\r", "\n")


def strip_cpr_for_display(text: str, carry: str) -> tuple[str, str]:
    """Remove CPR/DSR noise from live output, handling chunk boundaries."""
    merged = carry + text
    stripped = DSR_QUERY_RE.sub("", merged)
    stripped = CPR_REPLY_RE.sub("", stripped)
    partial = re.search(r"\x1B\[[0-9;]*$", stripped)
    if partial:
        return stripped[:partial.start()], partial.group(0)
    return stripped, ""


def find_root_password_spoke_choice(screen_text: str) -> Optional[str]:
    """Return the numeric choice for the Root password spoke from hub text."""
    spoke_entry_re = re.compile(
        r"(?mi)(\d+)\)\s*\[[^\]]*\]\s*(.*?)"
        r"(?=(?:\s+\d+\)\s*\[[^\]]*\]\s*)|\n|$)",
    )
    for m in spoke_entry_re.finditer(screen_text):
        if re.search(r"\broot\s+password\b", m.group(2), re.IGNORECASE):
            return m.group(1)
    # Fallback: look left of "Root password" for nearest "N)".
    idx = screen_text.lower().find("root password")
    if idx != -1:
        nums = re.findall(r"(\d+)\)", screen_text[max(0, idx - 120):idx])
        if nums:
            return nums[-1]
    return None


def find_hub_begin_key(screen_text: str) -> str:
    m = re.search(r"(?mi)\['([^']+)'\s+to\s+begin\s+installation", screen_text)
    return m.group(1) if m else "b"


def hub_root_password_is_complete(screen_text: str) -> bool:
    return bool(
        re.search(r"(?mi)root\s+password\s+is\s+set", screen_text)
        or re.search(r"(?mi)\[x\]\s*Root\s+password\b", screen_text)
    )


# --- Patterns ---

P = {
    "post_install_enter": re.compile(
        r"Press\s+Enter\s+to\s+(?:reboot(?:\s+into\s+the\s+installed\s+system)?|quit)\s*: ?", re.IGNORECASE
    ),
    "login": re.compile(r"login:\s*$", re.IGNORECASE),
    "login_pw": re.compile(r"password:\s*$", re.IGNORECASE),
    "hub": re.compile(r"Please make (?:your choice from above|a selection from the above)", re.IGNORECASE),
    "root_pw": re.compile(r"(?m)^.*password\s*:\s*$", re.IGNORECASE),
    "root_pw_confirm": re.compile(r"(?mi)^.*((confirm|again).*(password|passphrase)|(password|passphrase).*(confirm|again)).*$"),
    "weak_pw": re.compile(r"(use (it|this) anyway|weak password)", re.IGNORECASE),
    "luks_pw": re.compile(r"(?mi)^\s*Passphrase\s*:\s*$"),
    "luks_pw_confirm": re.compile(r"(?mi)^\s*Passphrase\s*\(confirm\)\s*:\s*$"),
    "anaconda_started": re.compile(r"Starting installer", re.IGNORECASE),
    "boot_luks": re.compile(r"(?i)(?:please\s+)?enter\s+passphrase\s+for\s+(?:disk\s+)?\S+\s*:"),
}

SUCCESS_PATTERNS = [
    ("installed", re.compile(r"Installation complete\.\s*Press", re.IGNORECASE)),
    ("installed", re.compile(r"Created UEFI boot entry: Azure Linux", re.IGNORECASE)),
    ("logged_in", re.compile(r"\b(root|azurelinux)@[^\n]*[#\$]\s*$", re.IGNORECASE)),
    ("login_verified", re.compile(r"__AZL_INSTALL_SUCCESS__")),
    ("boot_analyze_done", re.compile(r"__AZL_ANALYZE_DONE__")),
]

FAILURE_PATTERNS = [
    re.compile(r"BootloaderInstallationError", re.IGNORECASE),
    re.compile(r"Traceback \(most recent call last\)", re.IGNORECASE),
    re.compile(r"kernel panic", re.IGNORECASE),
]

INSTALL_PROGRESS_PATTERNS = [
    re.compile(r"Running pre-installation", re.IGNORECASE),
    re.compile(r"Running installation", re.IGNORECASE),
    re.compile(r"Installing", re.IGNORECASE),
    re.compile(r"Creating efi", re.IGNORECASE),
]


# --- Main ---

def main() -> int:
    parser = argparse.ArgumentParser(description="Automate Azure Linux ISO installation in QEMU")
    parser.add_argument("-i", "--iso", required=True, help="Path to installer ISO")
    parser.add_argument("-d", "--disk", required=True, help="QCOW2 disk path")
    parser.add_argument("-s", "--disk-size", default="10G", help="Disk size if not exists")
    parser.add_argument("-m", "--memory", default="4096", help="RAM in MiB")
    parser.add_argument("-c", "--cpus", default="2", help="vCPU count")
    parser.add_argument("-t", "--timeout", type=int, default=600, help="Timeout in seconds")
    parser.add_argument("-u", "--username", default="root", help="Login username")
    parser.add_argument("-p", "--password", default="Azl4Install!234", help="Root/login password")
    parser.add_argument("-L", "--luks-passphrase", default=None, help="LUKS passphrase (defaults to --password)")
    parser.add_argument("-C", "--install-choice", choices=["1", "2"], default="1", help="Installer menu choice")
    parser.add_argument("-R", "--root-password-spoke", default=None, help="Explicit spoke number if hub parsing is ambiguous")
    parser.add_argument("-l", "--log", default="qemu-install.log", help="Serial log file")
    parser.add_argument("-r", "--raw-log", default=None, help="Raw serial log (defaults to <log>.raw)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress live QEMU serial output to stdout (logs still written to file)")
    parser.add_argument("--ovmf-code", default="/usr/share/edk2/ovmf/OVMF_CODE.fd", help="OVMF code path")
    parser.add_argument("--ovmf-vars", default="/usr/share/edk2/ovmf/OVMF_VARS.fd", help="OVMF vars template")
    args = parser.parse_args()

    luks_passphrase = args.luks_passphrase or args.password

    if not os.path.exists(args.iso):
        print(f"ISO not found: {args.iso}", file=sys.stderr)
        return 2

    ensure_tools()

    disk_existed = ensure_disk(args.disk, args.disk_size)
    if disk_existed:
        print(
            f"WARNING: Disk already exists: {args.disk}\n"
            f"  QEMU may boot from disk instead of ISO. "
            f"Delete the disk to force a fresh install.",
            file=sys.stderr,
        )

    vars_copy = os.path.abspath(os.path.splitext(args.disk)[0] + "-OVMF_VARS.fd")
    if not os.path.exists(vars_copy):
        os.makedirs(os.path.dirname(vars_copy) or ".", exist_ok=True)
        shutil.copy2(args.ovmf_vars, vars_copy)

    qemu_cmd = [
        "qemu-system-x86_64", "-enable-kvm", "-machine", "q35", "-cpu", "host",
        "-smp", str(args.cpus), "-m", str(args.memory),
        "-drive", f"if=pflash,format=raw,readonly=on,file={args.ovmf_code}",
        "-drive", f"if=pflash,format=raw,file={vars_copy}",
        "-drive", f"file={os.path.abspath(args.disk)},if=virtio,format=qcow2",
        "-cdrom", os.path.abspath(args.iso),
        "-boot", "once=d", "-serial", "stdio", "-monitor", "none", "-display", "none",
    ]

    responders = [
        Responder(re.compile(r"Select installation type"), args.install_choice, "Installer menu selection"),
        Responder(re.compile(r"grub>\s*$", re.IGNORECASE), "normal", "GRUB rescue fallback"),
    ]

    # Sequential prompt sequences.
    root_pw_seq = SequentialPrompts(
        prompts=[
            (P["root_pw"], args.password, "root_pw_first"),
            (P["root_pw_confirm"], args.password, "root_pw_second"),
        ],
        note_prefix="Root password",
    )
    luks_pw_seq = SequentialPrompts(
        prompts=[
            (P["luks_pw"], luks_passphrase, "luks_pw_first"),
            (P["luks_pw_confirm"], luks_passphrase, "luks_pw_second"),
        ],
        note_prefix="LUKS passphrase",
    )

    st = State()
    start = time.time()
    qemu: subprocess.Popen | None = None

    print("Launching QEMU:")
    print("  " + " ".join(shlex.quote(p) for p in qemu_cmd))

    raw_log_path = args.raw_log or f"{args.log}.raw"

    with open(args.log, "w", encoding="utf-8", buffering=1) as logf, \
         open(raw_log_path, "w", encoding="utf-8", buffering=1) as raw_logf:
        try:
            qemu = subprocess.Popen(
                qemu_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, bufsize=0,
            )
            assert qemu.stdout is not None
            os.set_blocking(qemu.stdout.fileno(), False)

            buf = ""
            display_carry = ""
            last_status = 0.0

            while True:
                if qemu.poll() is not None:
                    break
                if time.time() - start > args.timeout:
                    raise TimeoutError(f"Timed out after {args.timeout}s")

                try:
                    chunk = os.read(qemu.stdout.fileno(), 4096)
                except BlockingIOError:
                    chunk = b""

                if not chunk:
                    time.sleep(0.1)
                    if time.time() - last_status > 20:
                        sys.stdout.write(f"\n[STATUS] running... {int(time.time() - start)}s\n")
                        last_status = time.time()
                    continue

                text = chunk.decode("utf-8", errors="replace")
                raw_logf.write(text)
                display_text, display_carry = strip_cpr_for_display(text, display_carry)
                if not args.quiet:
                    sys.stdout.write(display_text)
                    sys.stdout.flush()
                logf.write(sanitize(text))
                buf = (buf + text)[-12000:]

                clean = sanitize(buf[-4000:])

                # Check for fatal errors.
                for pat in FAILURE_PATTERNS:
                    if pat.search(clean):
                        raise RuntimeError(f"Detected failure: {pat.pattern}")

                # Track state transitions.
                if not st.anaconda_started and P["anaconda_started"].search(buf[-2000:]):
                    st.anaconda_started = True

                if not st.install_started:
                    for pat in INSTALL_PROGRESS_PATTERNS:
                        if pat.search(clean):
                            st.install_started = True
                            print("\n[AUTO] Installation progress detected.")
                            break

                # Success detection. Gate logged_in shell prompt match to after the
                # login password was actually sent, so we don't match transient root
                # shells in the installer environment.
                for attr, pat in SUCCESS_PATTERNS:
                    if attr == "logged_in" and not st.login_password_sent:
                        continue
                    if pat.search(clean):
                        setattr(st, attr, True)

                # --- Pre-install automation ---
                if not st.installed:
                    hub_window = sanitize(buf[-2000:])

                    # Hub spoke selection.
                    if not st.spoke_selected and P["hub"].search(hub_window):
                        if st.root_spoke_choice is None:
                            st.root_spoke_choice = args.root_password_spoke or find_root_password_spoke_choice(hub_window)
                        st.hub_begin_key = find_hub_begin_key(hub_window)
                        if st.root_spoke_choice is not None:
                            if maybe_send(qemu, hub_window, P["hub"], st.root_spoke_choice,
                                          f"Hub: select Root password spoke ({st.root_spoke_choice})", st, "hub_select_spoke"):
                                st.spoke_selected = True
                        elif not st.root_spoke_lookup_notice_sent:
                            print("\n[AUTO] Hub detected, waiting to parse Root password spoke...")
                            st.root_spoke_lookup_notice_sent = True

                    # Root password entry (only after spoke selected).
                    if st.spoke_selected and not root_pw_seq.done:
                        advance_seq(qemu, buf[-1200:], root_pw_seq, st)

                    # LUKS passphrase during install (option 2, after anaconda starts).
                    if args.install_choice == "2" and st.anaconda_started and not luks_pw_seq.done:
                        advance_seq(qemu, buf[-1200:], luks_pw_seq, st)

                    # Weak password confirmation.
                    maybe_send(qemu, buf[-1200:], P["weak_pw"], "yes", "Weak password accept", st, "weak_pw_confirm")

                    # Begin installation once root password is set.
                    if root_pw_seq.done and not st.install_started and P["hub"].search(hub_window):
                        if hub_root_password_is_complete(hub_window):
                            if maybe_send(qemu, hub_window, P["hub"], st.hub_begin_key,
                                          f"Hub: begin installation ({st.hub_begin_key})", st, "hub_continue", cooldown=4.0):
                                st.begin_attempts += 1
                        elif st.begin_attempts == 0:
                            print("\n[AUTO] Hub: Root password incomplete; waiting...")

                # Generic responders (install menu, grub rescue).
                for r in responders:
                    if r.can_fire() and r.pattern.search(buf):
                        send_line(qemu, r.reply)
                        r.hits += 1
                        sys.stdout.write(f"\n[AUTO] {r.note}: sent {r.reply!r}\n")

                # --- Post-install automation ---
                if not st.post_install_enter_sent and P["post_install_enter"].search(sanitize(buf[-2000:])):
                    send_line(qemu, "")
                    st.post_install_enter_sent = True
                    print("\n[AUTO] Post-install prompt: sent Enter")

                # Boot LUKS unlock (first boot + after SELinux relabel reboot).
                if args.install_choice == "2" and st.installed and not st.login_verified:
                    if maybe_send(qemu, sanitize(buf[-1200:]), P["boot_luks"], luks_passphrase,
                                  f"Boot LUKS unlock (#{st.boot_luks_unlock_count + 1})", st,
                                  f"boot_luks_{st.boot_luks_unlock_count}", cooldown=5.0):
                        st.boot_luks_unlock_count += 1

                # Console login.
                if maybe_send(qemu, buf[-1200:], P["login"], args.username, "Login username", st, "login_username"):
                    st.awaiting_login_password = True
                if st.awaiting_login_password:
                    if maybe_send(qemu, buf[-1200:], P["login_pw"], args.password, "Login password", st, "login_password"):
                        st.awaiting_login_password = False
                        st.login_password_sent = True

                # Verification and shutdown.
                if st.logged_in and not st.login_verification_sent:
                    send_line(qemu, "echo __AZL_INSTALL_SUCCESS__")
                    st.login_verification_sent = True
                if st.login_verified and not st.boot_analyze_sent:
                    # Collect boot timing once the system is up.
                    send_line(
                        qemu,
                        "echo __AZL_ANALYZE_BEGIN__; systemd-analyze; "
                        "systemd-analyze blame | head -n 20; "
                        "echo __AZL_ANALYZE_DONE__",
                    )
                    st.boot_analyze_sent = True
                if st.boot_analyze_done and not st.poweroff_sent:
                    send_line(qemu, "poweroff")
                    st.poweroff_sent = True

                # Periodic status.
                if time.time() - last_status > 20:
                    sys.stdout.write(f"\n[STATUS] running... {int(time.time() - start)}s\n")
                    last_status = time.time()

            rc = qemu.returncode if qemu.returncode is not None else -1
            if rc not in (0, 1):
                raise RuntimeError(f"QEMU exited with unexpected code {rc}")
            if not st.installed:
                msg = "WARNING: install completion not detected; check log."
                if disk_existed:
                    msg += (
                        f"\n  The disk '{args.disk}' already existed before this run."
                        f"\n  QEMU likely booted from the existing disk instead of the ISO."
                        f"\n  Delete the disk and re-run to test a fresh ISO install."
                    )
                print(msg, file=sys.stderr)
                return 1
            if not st.login_verified:
                print("WARNING: login verification not detected; check log.", file=sys.stderr)
                return 1
            print(f"\nSUCCESS: automated install finished. Serial log: {args.log}")
            return 0

        except Exception as exc:
            print(f"\nERROR: {exc}", file=sys.stderr)
            if qemu and qemu.poll() is None:
                qemu.send_signal(signal.SIGTERM)
                try:
                    qemu.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    qemu.kill()
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
