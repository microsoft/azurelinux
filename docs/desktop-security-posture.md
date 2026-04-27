# Desktop Security Posture — Technical Report

> **Historical Note (2026-04-27):** This report captures security analysis for a COSMIC-focused desktop path from an earlier project phase. KDE is now the canonical desktop target per `docs/decisions/ADR-0003-desktop-environment.md`.

**Project:** Azure Linux COSMIC Desktop (protagonist fork)
**Date:** April 23, 2026
**Scope:** Analysis of Azure Linux 3.0's hardened security baseline as it applies to a COSMIC Wayland desktop deployment. Each mitigation is evaluated for its mechanism, desktop-specific interaction, known gotchas, and concrete mitigation strategies.

---

## Table of Contents

1. [Compiler Hardening Layer](#1-compiler-hardening-layer)
   - 1.1 Position Independent Executables (`-fPIE -pie`)
   - 1.2 Stack Protector Strong (`-fstack-protector-strong`)
   - 1.3 Format String Protection (`-Wformat-security`)
   - 1.4 Fortify Source (`_FORTIFY_SOURCE=2`)
   - 1.5 Full RELRO (`--enable-bind-now`)
2. [Kernel Hardening Layer](#2-kernel-hardening-layer)
   - 2.1 Full ASLR (Including VDSO)
   - 2.2 `/dev/mem` and `/dev/kmem` Protection
   - 2.3 Strict Module RO/NX
   - 2.4 Kernel `.rodata` Write Protection
   - 2.5 `kptr_restrict`
   - 2.6 Symlink and Hardlink Restrictions
3. [Mandatory Access Control — SELinux](#3-mandatory-access-control--selinux)
   - 3.1 Mechanism
   - 3.2 Desktop Policy Gap (Critical)
   - 3.3 AVC Denial Taxonomy for COSMIC
   - 3.4 Policy Authoring Strategy
4. [Secure Boot and Module Signing](#4-secure-boot-and-module-signing)
5. [Supply Chain Integrity](#5-supply-chain-integrity)
6. [Threat Model Comparison: Server vs. Desktop](#6-threat-model-comparison-server-vs-desktop)
7. [Risk Register](#7-risk-register)
8. [Recommended Mitigation Roadmap](#8-recommended-mitigation-roadmap)

---

## 1. Compiler Hardening Layer

All Azure Linux packages are built through a centrally-controlled RPM macro set. Compiler hardening flags are injected at the `%{optflags}` macro level in `azurelinux-rpm-macros`, which means they apply to every package built from source in the repository — including all COSMIC components we add. This is architecturally stronger than distros that rely on package maintainers opting in.

### 1.1 Position Independent Executables (`-fPIE -pie`)

**Mechanism:** The compiler generates all code as position-independent, meaning no hard-coded absolute memory addresses. The linker marks the final executable as a PIE binary (`ET_DYN` ELF type). The kernel's ASLR then randomizes the base address of the executable at every execution.

**Desktop interaction:** COSMIC's components are Rust binaries. Rust compiles position-independent code by default (all Rust executables are PIE on Linux). This flag is therefore redundant for Rust targets but is still applied and causes no conflict.

For the C/C++ supporting stack (Mesa, GLib, GTK, libseat, libinput, libwl, libdrm), PIE applies and is the expected behavior. All modern desktop software is written and tested against PIE.

**Gotcha — GOT/PLT overhead in Mesa shader compilation:** Mesa's LLVM-based shader compiler (`radeonsi` backend) does a large amount of function-pointer-heavy dispatch during the first shader compilation of a session (cold cache). PIE means every function pointer goes through the PLT. The branch predictor handles this well by the second call. First-compile latency for complex shaders can be 5–15% higher than a non-PIE build. This is a cold-cache, one-time cost per shader variant, not a steady-state cost.

**Mitigation:** Mesa's shader disk cache (`MESA_SHADER_CACHE_DIR`, defaults to `~/.cache/mesa_shader_cache`) amortizes this across sessions. Ensure the disk cache is enabled and persisted in the COSMIC session environment. This is the default behavior and requires no configuration unless the user's home directory is tmpfs or on a network filesystem.

---

### 1.2 Stack Protector Strong (`-fstack-protector-strong`)

**Mechanism:** The compiler inserts a random "canary" value on the stack frame of any function that:
- Contains a local array of any type
- Takes the address of a local variable
- Contains a local `struct` or `union` that has an array member

The canary is loaded from `fs:0x28` (the thread-local storage slot) at function entry and checked before the function returns. A mismatch triggers `__stack_chk_fail()`, which calls `abort()`.

`-fstack-protector-strong` is a middle ground — `all` instruments every function, `strong` instruments the subset most likely to be exploitable. Approximately 20–40% of functions in a typical C codebase are instrumented.

**Desktop interaction:** The Wayland compositor's hot path (frame submission, input event dispatch, protocol message serialization) does not generally involve local arrays in tight loops. PipeWire's audio processing graph does involve fixed-size local buffers in its graph walker.

**Gotcha — false abort in legacy C code:** `_fstack-protector-strong` can cause a legitimate abort if a function uses a local array and then calls a function that, through some aliasing or macro expansion, writes past the local array before the canary check. This is rare in modern code but has been observed in:
- Old GStreamer plugins that use fixed-size stack buffers for media format negotiation
- Legacy `libpulse` compatibility shims
- Some `ibus` input method backend C code

**Mitigation:** Enable `ASAN` (AddressSanitizer) builds in CI for all C/C++ packages you add to the COSMIC layer. Stack canary aborts produce a stack trace via `backtrace()` that identifies the function. Any package that crashes under normal use with a canary failure has a real stack overflow bug that must be fixed upstream or patched locally. Do not disable the protector — fix the underlying code.

---

### 1.3 Format String Protection (`-Wformat-security`)

**Mechanism:** This flag promotes format string vulnerabilities to a compile-time error. Specifically, it errors when a non-literal string is passed as the format argument to `printf`-family functions:

```c
// Compile error under -Wformat-security:
char *user_input = get_user_input();
printf(user_input);  // ERROR: format not a string literal

// Correct:
printf("%s", user_input);
```

**Desktop interaction:** COSMIC's Rust components are immune — Rust's `format!` macro is type-safe and cannot produce format string vulnerabilities. This flag is relevant only to C/C++ dependencies.

**Gotcha — third-party C code that uses GLib's `g_message()`/`g_warning()` macros:** GLib's logging macros internally expand in ways that historically triggered `-Wformat-security` false positives on some older GLib versions. GLib 2.68+ resolved this. Azure Linux ships `glib2` 2.78.x, so this is not an issue for the packages in the tree.

The risk is in any **external C packages you port** for COSMIC that depend on older GLib-adjacent logging abstractions. Audit any package that fails to build under this flag — it either has a real vulnerability or a fixable pattern.

**Mitigation:** The mitigation is the flag itself. Packages that fail to compile are identified and patched before they ever run. No runtime mitigation is needed or applicable.

---

### 1.4 Fortify Source (`_FORTIFY_SOURCE=2`)

**Mechanism:** When `_FORTIFY_SOURCE=2` is defined, glibc replaces calls to unsafe memory/string functions with checked variants:

| Unsafe function | Fortified replacement |
|---|---|
| `memcpy(dst, src, n)` | Checks `n <= sizeof(dst)` if `sizeof(dst)` is known at compile time |
| `strcpy(dst, src)` | Checks destination size |
| `sprintf(buf, fmt, ...)` | Checks output buffer size |
| `gets(buf)` | Always errors at link time (unconditional) |

Level `2` (Azure Linux default) adds dynamic checks — if the size is not known at compile time, a runtime check is inserted. Level `1` only checks statically-known sizes.

**Desktop interaction — GTK/Cairo:** GTK and Cairo do significant buffer manipulation for widget rendering and surface compositing. Fortification catches off-by-one writes in surface copy operations. All modern GTK/Cairo versions are written to pass `_FORTIFY_SOURCE=2` cleanly.

**Gotcha — `_FORTIFY_SOURCE=2` with `memcpy` on overlapping regions:** Level 2 also enables the check that `memcpy` source and destination do not overlap (which is undefined behavior in C). Some older image/pixel manipulation code uses `memmove` semantics but calls `memcpy`. This triggers a runtime abort with `*** buffer overflow detected ***`.

This has been observed in:
- Older versions of `librsvg` (SVG renderer used by GTK icon themes)
- Some `gdk-pixbuf2` loaders for uncommon image formats (TGA, ICO)
- Legacy `ffmpeg` pixel format conversion code

**Mitigation:** Run the full COSMIC session in a VM with `MALLOC_CHECK_=3` (glibc heap debugging) and `_FORTIFY_SOURCE=2` during integration testing. Any legitimate abort surfaces a real bug. Replace `memcpy` with `memmove` where overlap is intentional, or patch the upstream package and track the fix.

---

### 1.5 Full RELRO (`--enable-bind-now`)

**Mechanism:** RELRO (RELocation Read-Only) is a two-level mitigation:

- **Partial RELRO:** The `.got` section (Global Offset Table entries for data) is placed before `.bss` and made read-only after relocation. The `.got.plt` section (function pointers resolved lazily) is still writable.
- **Full RELRO (`--enable-bind-now`):** Forces `LD_BIND_NOW=1` behavior — all dynamic symbols are resolved at program load time. After all relocations are complete, the entire `.got.plt` section is `mprotect()`'d to read-only. The linker achieves this via the `PT_GNU_RELRO` program header segment.

The security consequence: an attacker who achieves an arbitrary write primitive (via heap overflow, use-after-free, etc.) cannot overwrite a GOT entry to redirect the next call to `malloc()` or `free()` to attacker-controlled code.

**Desktop interaction:** Full RELRO is the most impactful mitigation against memory corruption exploits in a desktop context. `cosmic-comp` runs as the Wayland compositor, receiving and processing all window manager protocol messages from every application. It is a high-value target.

Without Full RELRO, a compromised Wayland client that can exploit a compositor protocol parser bug (a known attack surface — Wayland compositors have historically had protocol parsing vulnerabilities) could overwrite the compositor's GOT and redirect execution. With Full RELRO, this class of attack requires a more sophisticated technique (direct code injection, JIT spraying into executable regions, etc.).

**Gotcha — startup latency:** All symbols resolved at load time means `ld.so` walks every shared library's dynamic symbol table before `main()` is entered. For a binary like `cosmic-comp` that links against:

- `libwl-server.so` (~150 exported symbols)
- `libdrm.so` (~80 symbols)
- `libGL.so` / `libEGL.so` via libglvnd (~300 symbols)
- `libinput.so` (~120 symbols)
- `libxkbcommon.so` (~60 symbols)
- `libseat.so` (~20 symbols)
- Plus transitive dependencies of all of the above

...the total symbol resolution at startup is substantial. Estimated compositor cold-start overhead from Full RELRO: **50–150ms** depending on symbol count and storage I/O speed.

**Gotcha — `dlopen()` at runtime:** Some Mesa drivers use `dlopen()` to load backend modules (e.g., the DRI driver loader opening `iris_dri.so` or `radeonsi_dri.so`). These `dlopen()`'d libraries are also subject to Full RELRO when they are loaded, adding their symbol resolution to the `dlopen()` call latency. Mesa's first `eglInitialize()` call can be 20–80ms slower under Full RELRO than without it.

**Mitigation:** Two approaches:
1. **Prelink** (not recommended — conflicts with ASLR and is effectively abandoned)
2. **Systemd socket activation + pre-warm:** Start `cosmic-session` as early as possible in the systemd boot sequence so the RELRO startup cost is paid during boot, not at the user-visible login prompt. The startup cost is real but can be hidden in parallel boot activity.
3. **Mesa shader pre-compilation:** Use `VK_PIPELINE_CACHE` and `mesa_shader_cache` aggressively. The `dlopen()` overhead on first run is only paid once per Mesa driver version.

---

## 2. Kernel Hardening Layer

### 2.1 Full ASLR (Including VDSO)

**Mechanism:** Linux ASLR is controlled by `/proc/sys/kernel/randomize_va_space`. Azure Linux sets this to `2` (full randomization):

| Level | What's Randomized |
|---|---|
| `0` | Nothing |
| `1` | Stack, shared libraries, VDSO |
| `2` | Stack, shared libraries, VDSO, heap (`brk`), executable (requires PIE) |

At level `2`, the VDSO page (a kernel-mapped page containing `clock_gettime`, `gettimeofday`, `time`, and `getcpu` in fast-path userspace implementations) is also placed at a randomized address per-process.

**Desktop interaction:** The VDSO is used for monotonic clock reads, which are critical for:
- Frame timing in the compositor (VSync, adaptive sync, `clock_gettime(CLOCK_MONOTONIC)`)
- PipeWire graph timing (`clock_gettime(CLOCK_MONOTONIC_RAW)`)
- Animation interpolation in `libcosmic`'s animation system

**Gotcha — VDSO lookup cost under ASLR:** Without ASLR, glibc caches the VDSO mapping address in a static variable after the first lookup. With VDSO ASLR at level `2`, the address changes per-process but is fixed for the lifetime of a process. The cache still works; there is no repeated lookup cost per call. The overhead is:

- **One extra pointer dereference** per `clock_gettime` call (to the randomized VDSO address via the auxiliary vector `AT_SYSINFO_EHDR`)
- **Slightly higher TLB pressure** because the VDSO page lands at a different virtual address in each process, reducing TLB sharing between processes

The TLB pressure effect is measurable on systems running many processes simultaneously (a full COSMIC desktop session with compositor + panel + settings daemon + file manager + terminal + browser easily runs 15–30 processes).

**Mitigation:** This is not worth disabling — the security value (defeats VDSO as a fixed-address kernel code gadget for ROP chains) outweighs the TLB pressure. The correct response is to ensure COSMIC components are structured to minimize process count (use threads rather than processes for parallelism where possible). `cosmic-comp` is already a single-process compositor.

---

### 2.2 `/dev/mem` and `/dev/kmem` Protection

**Mechanism:** `CONFIG_STRICT_DEVMEM=y` and `CONFIG_DEVKMEM=n` in the kernel config. `/dev/mem` is restricted to non-kernel memory regions (cannot map kernel pages). `/dev/kmem` is compiled out entirely.

**Desktop interaction:** Modern GPU drivers (DRM/KMS) access hardware via memory-mapped I/O through the DRM subsystem, not through `/dev/mem`. `i915`, `amdgpu`, and `radeonsi` all use DRM device nodes (`/dev/dri/card0`, `/dev/dri/renderD128`). This protection does not affect normal desktop GPU operation.

**Gotcha — GPU diagnostic tools:** `gpu-top`, older versions of `radeontop`, and some vendor GPU diagnostic tools from circa 2015 or earlier used `/dev/mem` for MMIO register reads. Modern replacements (`intel_gpu_top`, `radeontop` ≥ 1.0, `nvtop`) all use DRM/debugfs. Ship only the modern tools.

**Mitigation:** None required for the primary stack. Document for contributors that GPU debugging must use DRM-based tools.

---

### 2.3 Strict Module RO/NX

**Mechanism:** `CONFIG_STRICT_MODULE_RWX=y`. After a kernel module is loaded and its `init` function completes, the kernel uses `set_memory_ro()` and `set_memory_nx()` to mark:
- Module `.text` section: executable, non-writable
- Module `.rodata` section: non-executable, non-writable
- Module `.data`/`.bss` sections: non-executable, writable

**Desktop interaction:** `i915` (Intel GPU), `amdgpu` (AMD GPU), `snd_hda_intel` (audio), `usbhid` (USB input), and `i2c_*` (display DDC/EDID) are all in-tree kernel modules compiled with this protection active.

**Gotcha — out-of-tree kernel modules:** Any module not in the kernel source tree (DKMS-based modules, external drivers) must be compiled and linked as a normal kernel module and will be subject to the same RO/NX enforcement. The issue arises if the DKMS module was written to self-patch its own code (extremely rare in legitimate drivers, common in rootkits).

For the COSMIC desktop, the only likely DKMS module is the proprietary NVIDIA driver (`nvidia.ko`). The legacy closed-source NVIDIA driver uses self-modifying code in its kernel module and **will not function** under `CONFIG_STRICT_MODULE_RWX=y`. The open-source `nvidia-open` kernel module (NVIDIA's OSS kernel module, available since driver version 515+) is compatible.

**Mitigation:** Ship `nvidia-open` kernel module support, not the legacy closed-source blob. NVIDIA declared the open module production-ready for Turing (RTX 20xx) and later architectures in driver version 560+. For pre-Turing NVIDIA hardware, there is no compatible path — the legacy blob is required, but those GPUs are effectively unsupported on this distro.

---

### 2.4 Kernel `.rodata` Write Protection

**Mechanism:** `CONFIG_DEBUG_RODATA=y` (implicit in `CONFIG_STRICT_KERNEL_RWX=y`). Kernel read-only data sections are mapped with the hardware write-protection bit set in page tables after boot. A kernel bug that tries to modify `.rodata` triggers a page fault and kernel oops/panic.

**Desktop interaction:** This is a kernel-internal protection with no direct userspace interaction. GPU drivers that update hardware-visible constant tables do so through writeable `.data` sections or explicitly-mapped DMA buffers, not through kernel `.rodata`.

**Gotcha:** None for normal desktop operation. This protection matters for kernel exploit mitigation, not application behavior.

---

### 2.5 `kptr_restrict`

**Mechanism:** `kernel.kptr_restrict = 2` (Azure Linux default). Controls exposure of kernel pointer values in `/proc/kallsyms`, `dmesg`, and `/proc/*` entries:

| Value | Behavior |
|---|---|
| `0` | All processes can read kernel pointers |
| `1` | Unprivileged processes see `0x0000000000000000` instead of real addresses |
| `2` | All processes (including root) see `0x0000000000000000` |

With value `2`, even root cannot read kernel symbol addresses from userspace interfaces. This defeats kernel ASLR bypass via `/proc/kallsyms` reading.

**Desktop interaction:** No effect on normal desktop operation. Kernel symbols are not needed at runtime by any desktop component.

**Gotcha — kernel performance profiling and tracing:** `perf record -a -g`, `bpftrace`, `SystemTap`, and `ftrace`-based tools require reading kernel symbol addresses for stack unwinding. With `kptr_restrict=2`:

- `perf report` will show `[unknown]` for kernel frames instead of symbol names
- `bpftrace` scripts that use `kaddr()` or `ksym()` will fail or return empty results
- `ftrace` function tracing by name still works (kernel-internal), but reading trace output with addresses will show `0x0` for kernel symbols

**Mitigation for developer/profiling use:** This can be lowered temporarily:

```bash
# Lower to allow root to read kernel pointers (for profiling session):
sudo sysctl kernel.kptr_restrict=1

# Restore after profiling:
sudo sysctl kernel.kptr_restrict=2
```

For developer images (as opposed to end-user images), consider shipping two image configs: one with `kptr_restrict=2` (production/end-user) and one with `kptr_restrict=1` (developer build). This is achievable via `PostInstallScripts` in the image config JSON.

---

### 2.6 Symlink and Hardlink Restrictions

**Mechanism:** `fs.protected_symlinks=1` and `fs.protected_hardlinks=1`. These implement two TOCTOU (time-of-check/time-of-use) race condition mitigations:

- **Protected symlinks:** Following a symlink in a world-writable sticky directory (e.g., `/tmp`) is blocked unless the symlink owner matches the process's effective UID or the directory owner.
- **Protected hardlinks:** Creating a hardlink to a file you do not own (or that has `setuid`/`setgid` bits) is blocked.

**Desktop interaction:** Well-written desktop software uses `mkstemp()` or `g_file_open_tmp()` for temporary files, which avoids these patterns. The restrictions are transparent to correct code.

**Gotcha — Java-based GUI applications:** Java's `java.io.File.createTempFile()` on some JVM implementations creates temp files in `/tmp` using a pattern that involves checking file existence before creation — a classic TOCTOU window. Under protected symlinks, a race during this window may fail with `EACCES` instead of completing. This affects Java-based applications such as:
- JetBrains IDEs (IntelliJ, CLion)
- NetBeans
- Some Eclipse plugins
- Older LibreOffice Java macro runtime

**Mitigation:** JVM applications should set `-Djava.io.tmpdir` to a user-writable non-sticky directory (e.g., `$XDG_RUNTIME_DIR/java-tmp`). This can be injected via a wrapper script in the application's `.desktop` entry or via a systemd user service environment file. The COSMIC app store (`cosmic-store`) should document this pattern for JVM app packaging.

**Gotcha — Electron apps:** Electron (Chromium-based) uses `/tmp` for socket files and IPC named pipes. Electron's socket naming is unique enough that it does not trigger the symlink restriction in practice. No mitigation required.

---

## 3. Mandatory Access Control — SELinux

### 3.1 Mechanism

SELinux implements type enforcement (TE) mandatory access control. Every kernel object — files, sockets, processes, message queues, shared memory segments, capabilities, device nodes — is labeled with a security context of the form:

```
user:role:type:level
e.g., system_u:system_r:cosmic_comp_t:s0
```

The SELinux policy is a compiled rule set that defines which `(source_type, target_type, object_class, permission)` 4-tuples are allowed. A process running as `cosmic_comp_t` attempting to `open` a file labeled `drm_device_t` will be allowed if and only if a rule exists:

```
allow cosmic_comp_t drm_device_t:chr_file { open read write ioctl };
```

If no such rule exists and SELinux is in enforcing mode, the `open()` syscall returns `EACCES` and an AVC (Access Vector Cache) denial is written to the audit log.

### 3.2 Desktop Policy Gap (Critical)

Azure Linux's SELinux policy (`selinux-policy` package, based on the `targeted` policy from the upstream `selinux-policy` project) is calibrated for **server workloads**:

- Web servers (`httpd_t`, `nginx_t`)
- Database servers (`mysqld_t`, `postgresql_t`)
- SSH daemons (`sshd_t`)
- Container runtimes (`container_t`, `container_runtime_t`)
- System services (`init_t`, `systemd_t`, `unconfined_service_t`)

There are **zero type definitions for any COSMIC component**. When `cosmic-comp` launches under a fresh SELinux policy, it runs in either:

- `unconfined_t` — if the user is in the `unconfined_u` SELinux user (default for admins). This means SELinux provides no confinement at all for the compositor, which defeats the purpose.
- `user_t` — if a stricter user mapping is applied. This type has a limited allow set and will generate hundreds of AVC denials when the compositor attempts to open DRM devices, create Wayland sockets, mmap shared memory, etc.

### 3.3 AVC Denial Taxonomy for COSMIC

The following are the expected categories of AVC denials when running COSMIC on a policy with no desktop context, ordered by frequency:

**Category 1 — DRM device access (compositor, greeter)**
```
avc: denied { open read write ioctl } for
  comm="cosmic-comp" path="/dev/dri/card0"
  scontext=user_u:user_r:user_t:s0
  tcontext=system_u:object_r:drm_device_t:s0
  tclass=chr_file
```
Every frame rendered requires `ioctl` on `/dev/dri/card0` (modesetting) and `/dev/dri/renderD128` (GPU command submission). Without allow rules, the compositor cannot render.

**Category 2 — Wayland socket creation**
```
avc: denied { create bind } for
  comm="cosmic-comp" path="/run/user/1000/wayland-0"
  scontext=user_u:user_r:user_t:s0
  tcontext=user_u:object_r:user_tmp_t:s0
  tclass=sock_file
```
The compositor creates a Unix domain socket that all Wayland clients connect to. The `bind()` call to create this socket under `/run/user/UID/` will be denied.

**Category 3 — Input device access**
```
avc: denied { open read } for
  comm="cosmic-comp" path="/dev/input/event0"
  scontext=user_u:user_r:user_t:s0
  tcontext=system_u:object_r:input_device_t:s0
  tclass=chr_file
```
The compositor must read raw input events from `evdev` nodes to handle keyboard and pointer input. `libinput` opens these on behalf of the compositor (or via `libseat`/`logind` device delegation).

**Category 4 — Shared memory for buffer passing**
```
avc: denied { create } for
  comm="cosmic-comp"
  scontext=user_u:user_r:user_t:s0
  tcontext=user_u:object_r:user_t:s0
  tclass=memfd
```
Wayland buffer sharing between the compositor and clients uses `memfd_create()` (anonymous memory-backed file descriptors). The compositor creates these and passes them to clients via Wayland's `wl_shm` or `zwp_linux_dmabuf_v1` protocols.

**Category 5 — D-Bus IPC between COSMIC components**
```
avc: denied { send_msg } for
  comm="cosmic-settings-daemon"
  scontext=user_u:user_r:user_t:s0
  tcontext=user_u:object_r:session_bus_type:s0
  tclass=dbus
```
`cosmic-settings-daemon`, `cosmic-notifications`, and `cosmic-panel` all communicate over the D-Bus session bus. Without explicit `dbus` send/receive rules, IPC between them is denied.

**Category 6 — GPU kernel module ioctl dispatch**
```
avc: denied { ioctl } for
  comm="cosmic-comp" path="/dev/dri/renderD128"
  ioctlcmd=0xXXXX
  scontext=user_u:user_r:user_t:s0
  tcontext=system_u:object_r:drm_device_t:s0
  tclass=chr_file
```
The DRM `ioctl` command numbers for `amdgpu` and `i915` differ. SELinux policy can restrict not just `ioctl` access but specific `ioctl` command values. Without `ioctl` allowlisting policy, all DRM ioctls are denied.

### 3.4 Policy Authoring Strategy

The approach used by Fedora for desktop SELinux policy (and the recommended approach here) is:

**Phase 1 — Permissive domain + audit collection (Weeks 1–8)**

Create a minimal policy module that declares the COSMIC types and places all COSMIC processes into a `permissive` domain (the rest of the system remains enforcing):

```te
# cosmic.te — initial skeleton
policy_module(cosmic, 0.1)

type cosmic_comp_t;
type cosmic_session_t;
type cosmic_greeter_t;
type cosmic_settings_daemon_t;

# Mark all COSMIC domains as permissive initially
permissive cosmic_comp_t;
permissive cosmic_session_t;
permissive cosmic_greeter_t;
permissive cosmic_settings_daemon_t;
```

Run the full COSMIC session normally. All AVC denials for COSMIC domains are logged but not enforced. Collect the audit log.

**Phase 2 — `audit2allow` + manual review (Weeks 8–16)**

Feed the collected audit log to `audit2allow` to generate an initial allow rule set:

```bash
ausearch -m avc -ts today | audit2allow -m cosmic_desktop > cosmic_desktop.te
```

**Do not** use `audit2allow` output directly without review. Common `audit2allow` anti-patterns to reject:
- `allow X self:capability sys_admin` — over-broad capability grant; find the specific capability needed
- `allow X drm_device_t:chr_file { ioctl }` without `ioctl` command number restriction — use `allowxperm` with specific ioctl numbers
- `allow X unlabeled_t:*` — indicates an unlabeled file that needs its own type definition

**Phase 3 — Enforcement per component (Weeks 16–24)**

Once a component's policy is reviewed and tested, remove its `permissive` declaration and run it in enforcing mode while leaving other components in permissive mode. Address regressions component by component.

**Phase 4 — Upstream contribution**

Contribute the COSMIC SELinux policy module to the upstream `selinux-policy` project (maintained at `https://github.com/SELinuxProject/selinux-policy`). This ensures policy updates flow back to Azure Linux via normal upstream channels.

**Estimated total policy lines:** A realistic COSMIC desktop SELinux policy module is approximately 800–1,500 lines of type enforcement (`.te`) + 200–400 lines of file context (`.fc`) specifications. This is comparable to a medium-complexity server application (e.g., `nginx`) and is a tractable engineering task, unlike the scope of a full desktop policy rewrite.

---

## 4. Secure Boot and Module Signing

**Mechanism:** Azure Linux implements a complete chain-of-trust:

```
UEFI Secure Boot (firmware)
  └── shim (Microsoft-signed)
       └── GRUB (signed by distro key enrolled in shim)
            └── kernel (signed by distro key)
                 └── kernel modules (signed by kernel build key)
```

All in-tree kernel modules are signed by the per-build kernel signing key during the RPM build of the `kernel` package. The public key is embedded in the kernel itself.

**Desktop interaction:** `i915`, `amdgpu`, and `snd_hda_intel` are all in-tree and signed. Normal hardware-accelerated desktop operation requires no additional signing workflow.

**Gotcha 1 — DKMS modules are unsigned:** Any out-of-tree module built via DKMS (`kernel-devel` + `dkms`) is not signed by the distro key. Under Secure Boot with `CONFIG_MODULE_SIG_FORCE=y` (which Azure Linux enables), unsigned modules are rejected at `insmod`/`modprobe`.

This affects:
- `nvidia-open` kernel modules (if installed from a binary package rather than compiled into the distro's kernel tree)
- VirtualBox guest additions
- Any custom kernel module a developer compiles against `kernel-devel`

**Mitigation — Machine Owner Key (MOK) enrollment:**

```bash
# Generate a MOK key pair:
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.key \
  -out MOK.crt -days 3650 -subj "/CN=Custom COSMIC MOK/"

# Sign the module:
/usr/src/linux-headers-$(uname -r)/scripts/sign-file \
  sha256 MOK.key MOK.crt nvidia.ko

# Enroll the key in shim's MOK database:
mokutil --import MOK.crt
# (requires reboot to confirm enrollment in shim's MOK manager UI)
```

This is the standard workflow on Ubuntu and Fedora for third-party modules. Ship `mokutil` and `shim-unsigned` (for MOK management) as first-class packages with user documentation. Include this in the COSMIC initial setup wizard (`cosmic-initial-setup`) as a guided flow when an unsigned module is detected.

**Gotcha 2 — Distro signing key rotation:** The kernel signing key is generated per-build of the `kernel` RPM. If the kernel is updated (new RPM), the new kernel's signing key differs from the previous one. Modules signed against the old kernel's key will not load on the new kernel. DKMS handles this by rebuilding the module against the new `kernel-devel`. This is standard behavior but must be documented.

---

## 5. Supply Chain Integrity

**Mechanism:** Azure Linux enforces supply chain integrity at two levels:

1. **Source verification:** Every `Source:` URL in an RPM spec has a companion `<package>.signatures.json` file:
   ```json
   {
     "Signatures": {
       "cosmic-comp-1.0.0.tar.gz": {
         "sha256": "abc123..."
       }
     }
   }
   ```
   The `srpmpacker` tool verifies the SHA-256 hash before accepting the source archive. A mismatched hash fails the build with a hard error.

2. **GPG-signed packages:** All built RPMs are GPG-signed. `tdnf` verifies signatures by default. `VALIDATE_IMAGE_GPG=y` on the image build enforces this during image composition.

**Desktop interaction — adding COSMIC source archives:**

Every new SPEC file added for a COSMIC component requires a corresponding `.signatures.json` file. This must be generated from the canonical upstream release tarball or cargo bundle:

```bash
sha256sum cosmic-comp-1.0.0.tar.gz
# output: <hash>  cosmic-comp-1.0.0.tar.gz
```

Then create `SPECS/cosmic-comp/cosmic-comp.signatures.json`:
```json
{
  "Signatures": {
    "cosmic-comp-1.0.0.tar.gz": {
      "sha256": "<hash>"
    }
  }
}
```

**Gotcha — Rust/Cargo vendored dependencies:** COSMIC components are Rust projects with potentially hundreds of `Cargo.toml` dependencies. The Azure Linux build system's hermetic chroot has no internet access. There are two approaches:

1. **Vendor the Cargo dependencies** into the source tarball: `cargo vendor` generates a `vendor/` directory. The vendored tarball is what goes into the SPEC as `Source1`, and its SHA-256 is what goes into `.signatures.json`. This is the approach used by Fedora for Rust packages.

2. **Use the Azure Linux Rust offline build pattern**: Azure Linux ships a `rust` spec and supports offline builds. The recommended approach is to follow Fedora's `rust-packaging` macros pattern (`%cargo_prep`, `%cargo_build`, `%cargo_install`) which handles vendored dependencies cleanly.

Every Cargo dependency version bump requires a new `.signatures.json` entry. Automate this in CI with a script that regenerates the hash file whenever `Cargo.lock` changes.

---

## 6. Threat Model Comparison: Server vs. Desktop

The fundamental tension in this project is that Azure Linux's security controls are calibrated for a different threat model than a desktop distribution faces.

| Threat Vector | Server Threat Model | Desktop Threat Model |
|---|---|---|
| **Primary attack surface** | Network-exposed daemons (SSH, HTTP, RPC) | User-facing applications (browser, email client, file manager) |
| **Attacker entry point** | Remote code execution via vulnerable service | Malicious document, URL, or binary executed by user |
| **Post-exploitation goal** | Lateral movement, data exfiltration, persistence | Keylogging, credential theft, privilege escalation to root |
| **Most valuable target** | Root access to the server | User session (browser history, SSH keys, `~/.gnupg`, Wayland clipboard) |
| **Confinement model needed** | Isolate services from each other and from root | Isolate applications from each other and from the session bus |
| **ASLR value** | High — RCE exploits need fixed addresses | High — same rationale applies |
| **SELinux value** | High — confines daemons, prevents service-to-service lateral movement | High — confines apps, but requires desktop-specific policy (the gap) |
| **Stack canaries value** | High for network-facing parsers | High for document format parsers (PDF, image codecs, fonts) |
| **RELRO value** | High for long-running daemons | High for compositor (highest-privilege desktop process) |

The compiler hardening features (PIE, canaries, FORTIFY, RELRO) are **equally valuable on a desktop** as on a server. They protect against the same class of memory corruption exploits regardless of whether the vulnerability is triggered via a network packet or a malicious PDF.

The SELinux policy is where the server/desktop gap is largest. The server policy provides no confinement for desktop processes. But this is a **policy gap, not an architectural flaw** — SELinux itself is the correct tool; it just needs desktop-specific policies written for it.

---

## 7. Risk Register

| ID | Risk | Severity | Probability | Mitigation |
|---|---|---|---|---|
| SEC-01 | SELinux has no COSMIC policy; running in `unconfined_t` provides no MAC | High | Certain (until policy is written) | Write COSMIC SELinux policy module; run in permissive domain during development |
| SEC-02 | Legacy closed-source NVIDIA driver incompatible with strict module RO/NX | Medium | High (if NVIDIA support is needed) | Ship `nvidia-open` only; document pre-Turing as unsupported |
| SEC-03 | `_FORTIFY_SOURCE=2` false positives in ported C packages | Low | Medium | Run integration tests with abort signal caught; fix underlying code |
| SEC-04 | Full RELRO startup latency degrades perceived login performance | Low | Certain | Hide cost in parallel boot sequence; measure and document baseline |
| SEC-05 | MOK enrollment UX is technical; desktop users may disable Secure Boot instead | Medium | Medium | Build guided MOK enrollment into `cosmic-initial-setup` |
| SEC-06 | Cargo vendoring for COSMIC Rust components adds per-release maintenance burden | Low | Certain | Automate `.signatures.json` generation in CI |
| SEC-07 | Java GUI apps fail under protected symlinks in `/tmp` | Low | Low (depends on app shipping decisions) | Use `$XDG_RUNTIME_DIR` for Java tmp; document in packaging guidelines |
| SEC-08 | `kptr_restrict=2` blocks kernel profiling for contributors | Low | Certain (for dev workflow) | Ship developer image config with `kptr_restrict=1` |

---

## 8. Recommended Mitigation Roadmap

### Phase 0 — Immediate (Pre-First-Boot)

1. Configure `cosmic-comp`, `cosmic-session`, and `cosmic-greeter` transient unit files to run in `permissive` SELinux domains from day one. Do not run them as `unconfined_t`.
2. Add `audit=1` to the kernel command line in the desktop image config to ensure all AVC denials are logged.
3. Validate that `mokutil` is present in the desktop package list.

### Phase 1 — Alpha (Months 1–3)

1. Collect AVC denial logs from all COSMIC processes running in permissive mode.
2. Write and ship initial COSMIC SELinux policy module (`cosmic.te`) covering the compositor, session, and greeter — the three highest-privilege components.
3. Enforce SELinux on compositor and greeter. Leave remaining COSMIC apps in permissive domains.
4. Automate Cargo vendor tarball generation and `.signatures.json` creation in the CI pipeline.

### Phase 2 — Beta (Months 3–6)

1. Extend SELinux policy to cover `cosmic-panel`, `cosmic-settings-daemon`, `cosmic-notifications`, and `cosmic-launcher`.
2. Enforce SELinux on all core COSMIC session components.
3. Build MOK enrollment UX into `cosmic-initial-setup`.
4. Measure and publish login time baseline; identify RELRO startup cost and confirm it is acceptable.

### Phase 3 — Release Candidate (Months 6–9)

1. Full SELinux enforcement on all COSMIC components (no permissive domains in production image).
2. Submit COSMIC SELinux policy upstream to `selinux-policy` project.
3. Publish developer image config with relaxed `kptr_restrict` and kernel profiling tools.
4. Complete integration testing with `_FORTIFY_SOURCE=2` abort signal trapping across all shipped C/C++ packages.
