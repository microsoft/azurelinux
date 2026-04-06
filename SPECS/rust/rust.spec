## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           rust
Version:        1.94.0
Release:        %autorelease
Summary:        The Rust Programming Language
License:        (Apache-2.0 OR MIT) AND (Artistic-2.0 AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0 AND Unicode-3.0)
# ^ written as: (rust itself) and (bundled libraries)
URL:            https://www.rust-lang.org

# Only x86_64, i686, and aarch64 are Tier 1 platforms at this time.
# https://doc.rust-lang.org/nightly/rustc/platform-support.html
%global rust_arches x86_64 i686 armv7hl aarch64 ppc64le s390x riscv64
ExclusiveArch:  %{rust_arches}

# To bootstrap from scratch, set the channel and date from src/stage0
# e.g. 1.89.0 wants rustc: 1.88.0-2025-06-26
# or nightly wants some beta-YYYY-MM-DD
%global bootstrap_version 1.93.0
%global bootstrap_channel 1.93.0
%global bootstrap_date 2026-01-22

# Only the specified arches will use bootstrap binaries.
# NOTE: Those binaries used to be uploaded with every new release, but that was
# a waste of lookaside cache space when they're most often unused.
# Run "spectool -g rust.spec" after changing this and then "fedpkg upload" to
# add them to sources. Remember to remove them again after the bootstrap build!
#global bootstrap_arches %%{rust_arches}

# We need CRT files for *-wasi targets, at least as new as the commit in
# src/ci/docker/host-x86_64/dist-various-2/build-wasi-toolchain.sh
%global wasi_libc_url https://github.com/WebAssembly/wasi-libc
%global wasi_libc_ref wasi-sdk-29
%global wasi_libc_name wasi-libc-%{wasi_libc_ref}
%global wasi_libc_source %{wasi_libc_url}/archive/%{wasi_libc_ref}/%{wasi_libc_name}.tar.gz
%global wasi_libc_dir %{_builddir}/%{wasi_libc_name}
%if 0%{?fedora}
%bcond_with bundled_wasi_libc
%else
%bcond_without bundled_wasi_libc
%endif

# Using llvm-static may be helpful as an opt-in, e.g. to aid LLVM rebases.
%bcond_with llvm_static

# We can also choose to just use Rust's bundled LLVM, in case the system LLVM
# is insufficient. Rust currently requires LLVM 19.0+.
# See src/bootstrap/src/core/build_steps/llvm.rs, fn check_llvm_version
# See src/llvm-project/cmake/Modules/LLVMVersion.cmake for bundled version.
%global min_llvm_version 20.0.0
%global bundled_llvm_version 21.1.8
#global llvm_compat_version 19
%global llvm llvm%{?llvm_compat_version}
%bcond_with bundled_llvm

# Requires stable libgit2 1.9, and not the next minor soname change.
# This needs to be consistent with the bindings in vendor/libgit2-sys.
%global min_libgit2_version 1.9.2
%global next_libgit2_version 1.10.0~
%global bundled_libgit2_version 1.9.2
%if 0%{?fedora} >= 41
%bcond_with bundled_libgit2
%else
%bcond_without bundled_libgit2
%endif

# Cargo uses UPSERTs with omitted conflict targets
%global min_sqlite3_version 3.35
%global bundled_sqlite3_version 3.51.1
%if 0%{?rhel} && 0%{?rhel} < 10
%bcond_without bundled_sqlite3
%else
%bcond_with bundled_sqlite3
%endif

%if 0%{?rhel}
# Disable cargo->libgit2->libssh2 on RHEL, as it's not approved for FIPS (rhbz1732949)
%bcond_without disabled_libssh2
%else
%bcond_with disabled_libssh2
%endif

# Reduce rustc's own debuginfo and optimizations to conserve 32-bit memory.
# e.g. https://github.com/rust-lang/rust/issues/45854
%global reduced_debuginfo 0
%if 0%{?__isa_bits} == 32
%global reduced_debuginfo 1
%endif
# Also on current riscv64 hardware, although future hardware will be
# able to handle it.
# e.g. http://fedora.riscv.rocks/koji/buildinfo?buildID=249870
%ifarch riscv64
%global reduced_debuginfo 1
%endif

%if 0%{?reduced_debuginfo}
%global enable_debuginfo --debuginfo-level=0 --debuginfo-level-std=2
%global enable_rust_opts --set rust.codegen-units-std=1
%bcond_with rustc_pgo
%else
# Build rustc with full debuginfo, CGU=1, ThinLTO, and PGO.
%global enable_debuginfo --debuginfo-level=2
%global enable_rust_opts --set rust.codegen-units=1 --set rust.lto=thin
%bcond_without rustc_pgo
%endif

# Detect non-stable channels from the version, like 1.74.0~beta.1
%{lua: do
  local version = rpm.expand("%{version}")
  local version_channel, subs = version:gsub("^.*~(%w+).*$", "%1", 1)
  rpm.define("channel " .. (subs ~= 0 and version_channel or "stable"))
  rpm.define("rustc_package rustc-" .. version_channel .. "-src")
end}
Source0:        https://static.rust-lang.org/dist/%{rustc_package}.tar.xz
Source1:        https://static.rust-lang.org/dist/%{rustc_package}.tar.xz.asc
Source2:        https://static.rust-lang.org/rust-key.gpg.ascii

Source10:        %{wasi_libc_source}

# Sources for bootstrap_arches are inserted by lua below

# By default, rust tries to use "rust-lld" as a linker for some targets.
Patch1:         0001-Use-lld-provided-by-system.patch

# Set a substitute-path in rust-gdb for standard library sources.
Patch2:         rustc-1.70.0-rust-gdb-substitute-path.patch

# Override default target CPUs to match distro settings
# TODO: upstream this ability into the actual build configuration
Patch3:         0001-Let-environment-variables-override-some-default-CPUs.patch

# Override the default self-contained system libraries
# TODO: the first can probably be upstreamed, but the second is hard-coded,
# and we're only applying that if not with bundled_wasi_libc.
Patch4:         0001-bootstrap-allow-disabling-target-self-contained.patch
Patch5:         0002-set-an-external-library-path-for-wasm32-wasi.patch

# We don't want to use the bundled library in libsqlite3-sys
Patch6:         rustc-1.94.0-unbundle-sqlite.patch

# stage0 tries to copy all of /usr/lib, sometimes unsuccessfully, see #143735
Patch7:         0001-only-copy-rustlib-into-stage0-sysroot.patch

# bootstrap: always propagate `CARGO_TARGET_{host}_LINKER`
# https://github.com/rust-lang/rust/pull/152077
Patch8:         0001-bootstrap-always-propagate-CARGO_TARGET_-host-_LINKE.patch

# Fixes for LLVM 22 compatibility
# https://github.com/rust-lang/rust/pull/151410
Patch9:         0001-Update-amdgpu-data-layout.patch
Patch10:        0002-Avoid-passing-addrspacecast-to-lifetime-intrinsics.patch
Patch11:        0003-Don-t-use-evex512-with-LLVM-22.patch

### RHEL-specific patches below ###

# Simple rpm macros for rust-toolset (as opposed to full rust-packaging)
Source100:      macros.rust-toolset
Source101:      macros.rust-srpm
Source102:      cargo_vendor.attr
Source103:      cargo_vendor.prov

# Disable cargo->libgit2->libssh2 on RHEL, as it's not approved for FIPS (rhbz1732949)
Patch100:       rustc-1.94.0-disable-libssh2.patch

# When building wasi, prevent linking a compiler-rt builtins library we don't have.
Patch1000:	wasi-no-link-builtins.patch

# Get the Rust triple for any architecture and ABI.
%{lua: function rust_triple(arch, abi)
  abi = abi or "gnu"
  if arch == "armv7hl" then
    arch = "armv7"
    abi = abi.."eabihf"
  elseif arch == "ppc64le" then
    arch = "powerpc64le"
  elseif arch == "riscv64" then
    arch = "riscv64gc"
  end
  return arch.."-unknown-linux-"..abi
end}

%define rust_triple() %{lua: print(rust_triple(
  rpm.expand("%{?1}%{!?1:%{_target_cpu}}"),
  rpm.expand("%{?2}%{!?2:gnu}")
))}

# Get the environment variable form of the Rust triple.
%define rust_triple_env() %{lua:
  print(rpm.expand("%{rust_triple %*}"):gsub("-", "_"):upper())
}

# Define a space-separated list of targets to ship rust-std-static-$triple for
# cross-compilation. The packages are noarch, but they're not fully
# reproducible between hosts, so only x86_64 actually builds it.
%ifarch x86_64
%if 0%{?fedora}
%global mingw_targets i686-pc-windows-gnu x86_64-pc-windows-gnu
%endif
%global wasm_targets wasm32-unknown-unknown wasm32-wasip1
%if 0%{?fedora}
%global extra_targets x86_64-unknown-none x86_64-unknown-uefi
%endif
%if 0%{?rhel} >= 10
%global extra_targets x86_64-unknown-none
%endif
%endif
%ifarch aarch64
%if 0%{?fedora}
%global extra_targets aarch64-unknown-none-softfloat aarch64-unknown-uefi
%endif
%if 0%{?rhel} >= 10
%global extra_targets aarch64-unknown-none-softfloat
%endif
%endif
%global all_targets %{?mingw_targets} %{?wasm_targets} %{?extra_targets}
%define target_enabled() %{lua:
  print(rpm.expand(" %{all_targets} "):find(rpm.expand(" %1 "), 1, true) or 0)
}

%if %defined bootstrap_arches
# For each bootstrap arch, add an additional binary Source.
# Also define bootstrap_source just for the current target.
%{lua: do
  local bootstrap_arches = {}
  for arch in rpm.expand("%{bootstrap_arches}"):gmatch("%S+") do
    table.insert(bootstrap_arches, arch)
  end
  local base = rpm.expand("https://static.rust-lang.org/dist/%{bootstrap_date}")
  local channel = rpm.expand("%{bootstrap_channel}")
  local target_arch = rpm.expand("%{_target_cpu}")
  for i, arch in ipairs(bootstrap_arches) do
    i = 1000 + i * 6
    local suffix = channel.."-"..rust_triple(arch)
    print(string.format("Source%d: %s/cargo-%s.tar.xz\n", i, base, suffix))
    print(string.format("Source%d: %s/cargo-%s.tar.xz.asc\n", i+1, base, suffix))
    print(string.format("Source%d: %s/rustc-%s.tar.xz\n", i+2, base, suffix))
    print(string.format("Source%d: %s/rustc-%s.tar.xz.asc\n", i+3, base, suffix))
    print(string.format("Source%d: %s/rust-std-%s.tar.xz\n", i+4, base, suffix))
    print(string.format("Source%d: %s/rust-std-%s.tar.xz.asc\n", i+5, base, suffix))
    if arch == target_arch then
      rpm.define("bootstrap_source_cargo "..i)
      rpm.define("bootstrap_sig_cargo "..i+1)
      rpm.define("bootstrap_source_rustc "..i+2)
      rpm.define("bootstrap_sig_rustc "..i+3)
      rpm.define("bootstrap_source_std "..i+4)
      rpm.define("bootstrap_sig_std "..i+5)
      rpm.define("bootstrap_suffix "..suffix)
    end
  end
end}
%endif

%ifarch %{bootstrap_arches}
%global local_rust_root %{_builddir}/rust-%{bootstrap_suffix}
Provides:       bundled(%{name}-bootstrap) = %{bootstrap_version}
%else
BuildRequires:  (cargo >= %{bootstrap_version} with cargo <= %{version})
BuildRequires:  (%{name} >= %{bootstrap_version} with %{name} <= %{version})
%global local_rust_root %{_prefix}
%endif

%if 0%{?rhel} && 0%{?rhel} < 11
BuildRequires:  gnupg2
%else
BuildRequires:  gpgverify
%endif

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
# explicit curl-devel to avoid httpd24-curl (rhbz1540167)
BuildRequires:  curl-devel
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)

%if %{without bundled_libgit2}
BuildRequires:  (pkgconfig(libgit2) >= %{min_libgit2_version} with pkgconfig(libgit2) < %{next_libgit2_version})
%endif

%if %{without bundled_sqlite3}
BuildRequires:  pkgconfig(sqlite3) >= %{min_sqlite3_version}
%endif

%if %{without disabled_libssh2}
BuildRequires:  pkgconfig(libssh2)
%endif

%if 0%{?rhel} == 8
BuildRequires:  platform-python
%else
BuildRequires:  python3
%endif
BuildRequires:  python3-rpm-macros

%if %with bundled_llvm
BuildRequires:  cmake >= 3.20.0
BuildRequires:  ninja-build
Provides:       bundled(llvm) = %{bundled_llvm_version}
%else
BuildRequires:  cmake >= 3.5.1
%if %defined llvm_compat_version
%global llvm_root %{_libdir}/%{llvm}
%global llvm_path %{llvm_root}/bin
%else
%global llvm_root %{_prefix}
%endif
BuildRequires:  %{llvm}-devel >= %{min_llvm_version}
%if %with llvm_static
BuildRequires:  %{llvm}-static
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
%endif
%endif

# make check needs "ps" for src/test/ui/wait-forked-but-failed-child.rs
BuildRequires:  procps-ng

# debuginfo-gdb tests need gdb
BuildRequires:  gdb
# Work around https://bugzilla.redhat.com/show_bug.cgi?id=2275274:
# gdb currently prints a "Unable to load 'rpm' module. Please install the python3-rpm package."
# message that breaks version detection.
BuildRequires:  python3-rpm

# For src/test/run-make/static-pie
BuildRequires:  glibc-static

# Virtual provides for folks who attempt "dnf install rustc"
Provides:       rustc = %{version}-%{release}
Provides:       rustc%{?_isa} = %{version}-%{release}

# Always require our exact standard library
Requires:       %{name}-std-static%{?_isa} = %{version}-%{release}

# The C compiler is needed at runtime just for linking. Someday rustc might
# invoke the linker directly, and then we'll only need binutils.
# https://github.com/rust-lang/rust/issues/11937
Requires:       /usr/bin/cc

%global __ranlib %{_bindir}/ranlib

# ALL Rust libraries are private, because they don't keep an ABI.
%global _privatelibs lib(.*-[[:xdigit:]]{16}*|rustc.*)[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
%global __provides_exclude_from ^(%{_docdir}|%{rustlibdir}/src)/.*$
%global __requires_exclude_from ^(%{_docdir}|%{rustlibdir}/src)/.*$

# While we don't want to encourage dynamic linking to Rust shared libraries, as
# there's no stable ABI, we still need the unallocated metadata (.rustc) to
# support custom-derive plugins like #[proc_macro_derive(Foo)].
%global _find_debuginfo_opts --keep-section .rustc

# The standard library rlibs are essentially static archives, but we don't want
# to strip them because that impairs the debuginfo of all Rust programs.
# It also had a tendency to break the cross-compiled libraries:
# - wasm targets lost the archive index, which we were repairing with llvm-ranlib
# - uefi targets couldn't link builtins like memcpy, possibly due to lost COMDAT flags
%global __brp_strip_static_archive %{nil}
%global __brp_strip_lto %{nil}

# We're going to override --libdir when configuring to get rustlib into a
# common path, but we'll fix the shared libraries during install.
%global common_libdir %{_prefix}/lib
%global rustlibdir %{common_libdir}/rustlib

%if %defined mingw_targets
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-crt
BuildRequires:  mingw64-crt
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-winpthreads-static
BuildRequires:  mingw64-winpthreads-static
%endif

%if %defined wasm_targets
%if %with bundled_wasi_libc
BuildRequires:  clang%{?llvm_compat_version}
%else
BuildRequires:  wasi-libc-static
%endif
BuildRequires:  lld%{?llvm_compat_version}
%endif

# For profiler_builtins
BuildRequires:  compiler-rt%{?llvm_compat_version}

# This component was removed as of Rust 1.69.0.
# https://github.com/rust-lang/rust/pull/101841
Obsoletes:      %{name}-analysis < 1.69.0~

# Experimenting with a fine-grained version of %%cargo_vendor_manifest,
# so we can have different bundled provides for each tool subpackage.
%define cargo_tree_manifest(n:m:f:t:) (       \
  %{!-n:%{error:must specify a tool name}}    \
  set -euo pipefail                           \
  mkdir -p build/manifests/%{-n*}             \
  %{shrink:                                   \
    env RUSTC_BOOTSTRAP=1                     \
      RUSTC=%{local_rust_root}/bin/rustc      \
      %{local_rust_root}/bin/cargo tree       \
      --offline --edges normal,build          \
      --prefix none --format "{p}"            \
      %{-m:--manifest-path %{-m*}/Cargo.toml} \
      %{-f:--features %{-f*}}                 \
      %{-t:--target %{-t*}}                   \
      %*                                      \
    | sed '/([*/]/d; s/ (proc-macro)$//'      \
    | sort -u                                 \
    >build/manifests/%{-n*}/cargo-vendor.txt  \
  }                                           \
)
%ifnarch %{bootstrap_arches}
%{?fedora:BuildRequires: cargo-rpm-macros}
%{?rhel:BuildRequires: rust-toolset}
%endif

%description
Rust is a systems programming language that runs blazingly fast, prevents
segfaults, and guarantees thread safety.

This package includes the Rust compiler and documentation generator.


%package std-static
Summary:        Standard library for Rust
Provides:       %{name}-std-static-%{rust_triple} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       glibc-devel%{?_isa} >= 2.17

%description std-static
This package includes the standard libraries for building applications
written in Rust.

%global target_package()                        \
%package std-static-%1                          \
Summary:        Standard library for Rust %1    \
Requires:       %{name} = %{version}-%{release}

%global target_description()                                            \
%description std-static-%1                                              \
This package includes the standard libraries for building applications  \
written in Rust for the %2 target %1.

%if %target_enabled i686-pc-windows-gnu
%target_package i686-pc-windows-gnu
Requires:       mingw32-crt
Requires:       mingw32-gcc
Requires:       mingw32-winpthreads-static
Provides:       mingw32-rust = %{version}-%{release}
Provides:       mingw32-rustc = %{version}-%{release}
BuildArch:      noarch
%target_description i686-pc-windows-gnu MinGW
%endif

%if %target_enabled x86_64-pc-windows-gnu
%target_package x86_64-pc-windows-gnu
Requires:       mingw64-crt
Requires:       mingw64-gcc
Requires:       mingw64-winpthreads-static
Provides:       mingw64-rust = %{version}-%{release}
Provides:       mingw64-rustc = %{version}-%{release}
BuildArch:      noarch
%target_description x86_64-pc-windows-gnu MinGW
%endif

%if %target_enabled wasm32-unknown-unknown
%target_package wasm32-unknown-unknown
Requires:       lld >= 8.0
BuildArch:      noarch
%target_description wasm32-unknown-unknown WebAssembly
%endif

%if %target_enabled wasm32-wasip1
%target_package wasm32-wasip1
Requires:       lld >= 8.0
%if %with bundled_wasi_libc
Provides:       bundled(wasi-libc)
%else
Requires:       wasi-libc-static
%endif
BuildArch:      noarch
# https://blog.rust-lang.org/2024/04/09/updates-to-rusts-wasi-targets.html
Obsoletes:      %{name}-std-static-wasm32-wasi < 1.84.0~
%target_description wasm32-wasip1 WebAssembly
%endif

%if %target_enabled x86_64-unknown-none
%target_package x86_64-unknown-none
Requires:       lld
%target_description x86_64-unknown-none embedded
%endif

%if %target_enabled aarch64-unknown-uefi
%target_package aarch64-unknown-uefi
Requires:       lld
%target_description aarch64-unknown-uefi embedded
%endif

%if %target_enabled x86_64-unknown-uefi
%target_package x86_64-unknown-uefi
Requires:       lld
%target_description x86_64-unknown-uefi embedded
%endif

%if %target_enabled aarch64-unknown-none-softfloat
%target_package aarch64-unknown-none-softfloat
Requires:       lld
%target_description aarch64-unknown-none-softfloat embedded
%endif


%package debugger-common
Summary:        Common debugger pretty printers for Rust
BuildArch:      noarch

%description debugger-common
This package includes the common functionality for %{name}-gdb and %{name}-lldb.


%package gdb
Summary:        GDB pretty printers for Rust
BuildArch:      noarch
Requires:       gdb
Requires:       %{name}-debugger-common = %{version}-%{release}
# rust-gdb uses rustc to find the sysroot
Requires:       %{name} = %{version}-%{release}

%description gdb
This package includes the rust-gdb script, which allows easier debugging of Rust
programs.


%package lldb
Summary:        LLDB pretty printers for Rust
BuildArch:      noarch
Requires:       lldb
Requires:       python3-lldb
Requires:       %{name}-debugger-common = %{version}-%{release}
# rust-lldb uses rustc to find the sysroot
Requires:       %{name} = %{version}-%{release}

%description lldb
This package includes the rust-lldb script, which allows easier debugging of Rust
programs.


%package doc
Summary:        Documentation for Rust
# NOT BuildArch:      noarch
# Note, while docs are mostly noarch, some things do vary by target_arch.
# Koji will fail the build in rpmdiff if two architectures build a noarch
# subpackage differently, so instead we have to keep its arch.

# Cargo no longer builds its own documentation
# https://github.com/rust-lang/cargo/pull/4904
# We used to keep a shim cargo-doc package, but now that's merged too.
Obsoletes:      cargo-doc < 1.65.0~
Provides:       cargo-doc = %{version}-%{release}

%description doc
This package includes HTML documentation for the Rust programming language and
its standard library.


%package -n cargo
Summary:        Rust's package manager and build tool
%if %with bundled_libgit2
Provides:       bundled(libgit2) = %{bundled_libgit2_version}
%endif
%if %with bundled_sqlite3
Provides:       bundled(sqlite) = %{bundled_sqlite3_version}
%endif
# For tests:
BuildRequires:  git-core
# Cargo is not much use without Rust, and it's worth keeping the versions
# in sync since some feature development depends on them together.
Requires:       %{name} = %{version}-%{release}

# "cargo vendor" is a builtin command starting with 1.37. The Obsoletes and
# Provides are mostly relevant to RHEL, but harmless to have on Fedora/etc. too
Obsoletes:      cargo-vendor <= 0.1.23
Provides:       cargo-vendor = %{version}-%{release}

%description -n cargo
Cargo is a tool that allows Rust projects to declare their various dependencies
and ensure that you'll always get a repeatable build.


%package -n rustfmt
Summary:        Tool to find and fix Rust formatting issues
Requires:       cargo

# /usr/bin/rustfmt is dynamically linked against internal rustc libs
Requires:       %{name}%{?_isa} = %{version}-%{release}

# The component/package was rustfmt-preview until Rust 1.31.
Obsoletes:      rustfmt-preview < 1.0.0
Provides:       rustfmt-preview = %{version}-%{release}

%description -n rustfmt
A tool for formatting Rust code according to style guidelines.


%package analyzer
Summary:        Rust implementation of the Language Server Protocol

# /usr/bin/rust-analyzer is dynamically linked against internal rustc libs
Requires:       %{name}%{?_isa} = %{version}-%{release}

# The standard library sources are needed for most functionality.
Recommends:     %{name}-src

# RLS is no longer available as of Rust 1.65, but we're including the stub
# binary that implements LSP just enough to recommend rust-analyzer.
Obsoletes:      rls < 1.65.0~
# The component/package was rls-preview until Rust 1.31.
Obsoletes:      rls-preview < 1.31.6

%description analyzer
rust-analyzer is an implementation of Language Server Protocol for the Rust
programming language. It provides features like completion and goto definition
for many code editors, including VS Code, Emacs and Vim.


%package -n clippy
Summary:        Lints to catch common mistakes and improve your Rust code
Requires:       cargo
# /usr/bin/clippy-driver is dynamically linked against internal rustc libs
Requires:       %{name}%{?_isa} = %{version}-%{release}

# The component/package was clippy-preview until Rust 1.31.
Obsoletes:      clippy-preview <= 0.0.212
Provides:       clippy-preview = %{version}-%{release}

%description -n clippy
A collection of lints to catch common mistakes and improve your Rust code.


%package src
Summary:        Sources for the Rust standard library
BuildArch:      noarch
Recommends:     %{name}-std-static = %{version}-%{release}

%description src
This package includes source files for the Rust standard library. It may be
useful as a reference for code completion tools in various editors.


%if 0%{?rhel}

%package toolset-srpm-macros
Summary:        RPM macros for building Rust source packages
BuildArch:      noarch

# This used to be from its own source package, versioned like rust2rpm.
Obsoletes:      rust-srpm-macros < 18~
Provides:       rust-srpm-macros = 25.2

%description toolset-srpm-macros
RPM macros for building source packages for Rust projects.


%package toolset
Summary:        Rust Toolset
BuildArch:      noarch
Requires:       rust = %{version}-%{release}
Requires:       cargo = %{version}-%{release}
Requires:       rust-toolset-srpm-macros = %{version}-%{release}
Conflicts:      cargo-rpm-macros

%description toolset
This is the metapackage for Rust Toolset, bringing in the Rust compiler,
the Cargo package manager, and a few convenience macros for rpm builds.

%endif


%prep
%gpgverify -k 2 -s 1 -d 0

%ifarch %{bootstrap_arches}
%gpgverify -k 2 -s %{bootstrap_sig_cargo} -d %{bootstrap_source_cargo}
%gpgverify -k 2 -s %{bootstrap_sig_rustc} -d %{bootstrap_source_rustc}
%gpgverify -k 2 -s %{bootstrap_sig_std} -d %{bootstrap_source_std}
rm -rf %{local_rust_root}
%setup -q -n cargo-%{bootstrap_suffix} -T -b %{bootstrap_source_cargo}
./install.sh --prefix=%{local_rust_root} --disable-ldconfig
%setup -q -n rustc-%{bootstrap_suffix} -T -b %{bootstrap_source_rustc}
./install.sh --prefix=%{local_rust_root} --disable-ldconfig
%setup -q -n rust-std-%{bootstrap_suffix} -T -b %{bootstrap_source_std}
./install.sh --prefix=%{local_rust_root} --disable-ldconfig
test -f '%{local_rust_root}/bin/cargo'
test -f '%{local_rust_root}/bin/rustc'
%endif

%if %{defined wasm_targets} && %{with bundled_wasi_libc}
%setup -q -n %{wasi_libc_name} -T -b 10
rm -rf %{wasi_libc_dir}/dlmalloc/

%patch -P1000 -p1
%endif

%setup -q -n %{rustc_package}

%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%if %without bundled_wasi_libc
%patch -P5 -p1
%endif
%if %without bundled_sqlite3
%patch -P6 -p1
%endif
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1

%if %with disabled_libssh2
%patch -P100 -p1
%endif

# Use our explicit python3 first
sed -i.try-python -e '/^try python3 /i try "%{__python3}" "$@"' ./configure

# Set a substitute-path in rust-gdb for standard library sources.
sed -i.rust-src -e "s#@BUILDDIR@#$PWD#" ./src/etc/rust-gdb

%if %without bundled_llvm
rm -rf src/llvm-project/
mkdir -p src/llvm-project/libunwind/
%endif

# Remove submodules we don't need.
rm -rf src/gcc
rm -rf src/tools/enzyme
rm -rf src/tools/rustc-perf/collector/*-benchmarks/

# Remove other unused vendored libraries. This leaves the directory in place,
# because some build scripts watch them, e.g. "cargo:rerun-if-changed=curl".
%define clear_dir() find ./%1 -mindepth 1 -delete
%clear_dir vendor/curl-sys*/curl/
%clear_dir vendor/*jemalloc-sys*/jemalloc/
%clear_dir vendor/libffi-sys*/libffi/
%clear_dir vendor/libmimalloc-sys*/c_src/mimalloc/
%clear_dir vendor/libsqlite3-sys*/sqlcipher/
%clear_dir vendor/libssh2-sys*/libssh2/
%clear_dir vendor/libz-sys*/src/zlib{,-ng}/
%clear_dir vendor/lzma-sys*/xz-*/
%clear_dir vendor/openssl-src*/openssl/
%clear_dir vendor/capstone-sys-*/capstone/

%if %without bundled_libgit2
%clear_dir vendor/libgit2-sys*/libgit2/
%endif

%if %without bundled_sqlite3
%clear_dir vendor/libsqlite3-sys*/sqlite3/
%endif

%if %with disabled_libssh2
rm -rf vendor/libssh2-sys*/
%endif

# This only affects the transient rust-installer, but let it use our dynamic xz-libs
sed -i.lzma -e '/LZMA_API_STATIC/d' src/bootstrap/src/core/build_steps/tool.rs

%if %{without bundled_llvm} && %{with llvm_static}
# Static linking to distro LLVM needs to add -lffi
# https://github.com/rust-lang/rust/issues/34486
sed -i.ffi -e '$a #[link(name = "ffi")] extern "C" {}' \
  compiler/rustc_llvm/src/lib.rs
%endif

# The configure macro will modify some autoconf-related files, which upsets
# cargo when it tries to verify checksums in those files. If we just truncate
# that file list, cargo won't have anything to complain about.
find vendor -name .cargo-checksum.json \
  -exec sed -i.uncheck -e 's/"files":{[^}]*}/"files":{ }/' '{}' '+'

# Sometimes Rust sources start with #![...] attributes, and "smart" editors think
# it's a shebang and make them executable. Then brp-mangle-shebangs gets upset...
find -name '*.rs' -type f -perm /111 -exec chmod -v -x '{}' '+'

# The distro flags are only appropriate for the host, not our cross-targets,
# and they're not as fine-grained as the settings we choose for std vs rustc.
%if %defined build_rustflags
%global build_rustflags %{nil}
%endif

# These are similar to __cflags_arch_* in /usr/lib/rpm/redhat/macros
%global rustc_target_cpus %{lua: do
  local fedora = tonumber(rpm.expand("0%{?fedora}"))
  local rhel = tonumber(rpm.expand("0%{?rhel}"))
  local env =
    " RUSTC_TARGET_CPU_X86_64=x86-64" .. ((rhel >= 10) and "-v3" or (rhel == 9) and "-v2" or "")
    .. " RUSTC_TARGET_CPU_PPC64LE=" .. ((rhel >= 9) and "pwr9" or "pwr8")
    .. " RUSTC_TARGET_CPU_S390X=" ..
        ((rhel >= 9) and "z14" or (rhel == 8 or fedora >= 38) and "z13" or
         (fedora >= 26) and "zEC12" or (rhel == 7) and "z196" or "z10")
  print(env)
end}

# Set up shared environment variables for build/install/check.
# *_USE_PKG_CONFIG=1 convinces *-sys crates to use the system library.
%global rust_env %{shrink:
  %{?rustflags:RUSTFLAGS="%{rustflags}"}
  %{rustc_target_cpus}
  %{!?with_bundled_sqlite3:LIBSQLITE3_SYS_USE_PKG_CONFIG=1}
  %{!?with_disabled_libssh2:LIBSSH2_SYS_USE_PKG_CONFIG=1}
  %{?llvm_path:PATH="%{llvm_path}:$PATH"}
}
%global export_rust_env export %{rust_env}

%build
%{export_rust_env}

# Some builders have relatively little memory for their CPU count.
# At least 4GB per CPU is a good rule of thumb for building rustc.
%if %undefined constrain_build
%define constrain_build(m:) %{lua:
  for l in io.lines('/proc/meminfo') do
    if l:sub(1, 9) == "MemTotal:" then
      local opt_m = math.tointeger(rpm.expand("%{-m*}"))
      local mem_total = math.tointeger(string.match(l, "MemTotal:%s+(%d+)"))
      local cpu_limit = math.max(1, mem_total // (opt_m * 1024))
      if cpu_limit < math.tointeger(rpm.expand("%_smp_build_ncpus")) then
        rpm.define("_smp_build_ncpus " .. cpu_limit)
      end
      break
    end
  end
}
%endif
%constrain_build -m 4096

%if %defined mingw_targets
%define mingw_target_config %{shrink:
  --set target.i686-pc-windows-gnu.linker=%{mingw32_cc}
  --set target.i686-pc-windows-gnu.cc=%{mingw32_cc}
  --set target.i686-pc-windows-gnu.ar=%{mingw32_ar}
  --set target.i686-pc-windows-gnu.ranlib=%{mingw32_ranlib}
  --set target.i686-pc-windows-gnu.self-contained=false
  --set target.x86_64-pc-windows-gnu.linker=%{mingw64_cc}
  --set target.x86_64-pc-windows-gnu.cc=%{mingw64_cc}
  --set target.x86_64-pc-windows-gnu.ar=%{mingw64_ar}
  --set target.x86_64-pc-windows-gnu.ranlib=%{mingw64_ranlib}
  --set target.x86_64-pc-windows-gnu.self-contained=false
}
%endif

%if %defined wasm_targets
%if %with bundled_wasi_libc
%define wasi_libc_flags MALLOC_IMPL=emmalloc CC=clang AR=llvm-ar NM=llvm-nm
%make_build --quiet -C %{wasi_libc_dir} %{wasi_libc_flags} TARGET_TRIPLE=wasm32-wasip1
%define wasm_target_config %{shrink:
  --set target.wasm32-wasip1.wasi-root=%{wasi_libc_dir}/sysroot
}
%else
%define wasm_target_config %{shrink:
  --set target.wasm32-wasip1.wasi-root=%{_prefix}/wasm32-wasi
  --set target.wasm32-wasip1.self-contained=false
}
%endif
%endif

# Find the compiler-rt library for the Rust profiler_builtins and optimized-builtins crates.
%define clang_lib %{expand:%%clang%{?llvm_compat_version}_resource_dir}/lib
%define profiler %{clang_lib}/%{_arch}-redhat-linux-gnu/libclang_rt.profile.a
test -r "%{profiler}"

# llvm < 21 does not provide a builtins library for s390x.
%if "%{_arch}" != "s390x" || 0%{?clang_major_version} >= 21
%define optimized_builtins %{clang_lib}/%{_arch}-redhat-linux-gnu/libclang_rt.builtins.a
test -r "%{optimized_builtins}"
%else
%define optimized_builtins false
%endif


%configure --disable-option-checking \
  --docdir=%{_pkgdocdir} \
  --libdir=%{common_libdir} \
  --build=%{rust_triple} --host=%{rust_triple} --target=%{rust_triple} \
  --set target.%{rust_triple}.linker=%{__cc} \
  --set target.%{rust_triple}.cc=%{__cc} \
  --set target.%{rust_triple}.cxx=%{__cxx} \
  --set target.%{rust_triple}.ar=%{__ar} \
  --set target.%{rust_triple}.ranlib=%{__ranlib} \
  --set target.%{rust_triple}.profiler="%{profiler}" \
  --set target.%{rust_triple}.optimized-compiler-builtins="%{optimized_builtins}" \
  %{?mingw_target_config} \
  %{?wasm_target_config} \
  --python=%{__python3} \
  --local-rust-root=%{local_rust_root} \
  --set build.rustfmt=/bin/true \
  %{!?with_bundled_llvm: --llvm-root=%{llvm_root} \
    %{!?with_llvm_static: --enable-llvm-link-shared } } \
  --disable-llvm-static-stdcpp \
  --disable-llvm-bitcode-linker \
  --disable-lld \
  --disable-rpath \
  %{enable_debuginfo} \
  %{enable_rust_opts} \
  --set build.jobs=%_smp_build_ncpus \
  --set build.build-stage=2 \
  --set build.doc-stage=2 \
  --set build.install-stage=2 \
  --set build.test-stage=2 \
  --set build.optimized-compiler-builtins=false \
  --set rust.llvm-tools=false \
  --set rust.verify-llvm-ir=true \
  --enable-extended \
  --tools=cargo,clippy,rust-analyzer,rustdoc,rustfmt,src \
  --enable-vendor \
  --enable-verbose-tests \
  --release-channel=%{channel} \
  --release-description="%{?fedora:Fedora }%{?rhel:Red Hat }%{version}-%{release}"

%global __x %{__python3} ./x.py

%if %{with rustc_pgo}
# Build the compiler with profile instrumentation
%define profraw $PWD/build/profiles
%define profdata $PWD/build/rustc.profdata
mkdir -p "%{profraw}"
%{__x} build sysroot --rust-profile-generate="%{profraw}"
# Build cargo as a workload to generate compiler profiles
# We normally use `x.py`, but in this case we invoke the stage 2 compiler and libs
# directly to ensure we use the instrumented compiler.
env LLVM_PROFILE_FILE="%{profraw}/default_%%m_%%p.profraw" \
  LD_LIBRARY_PATH=$PWD/build/host/stage2/lib \
  RUSTC=$PWD/build/host/stage2/bin/rustc \
  cargo build --manifest-path=src/tools/cargo/Cargo.toml
# Finalize the profile data and clean up the raw files
llvm-profdata merge -o "%{profdata}" "%{profraw}"
rm -r "%{profraw}" build/%{rust_triple}/stage2*/
# Redefine the macro to use that profile data from now on
%global __x %{__x} --rust-profile-use="%{profdata}"
%endif

# Build the compiler normally (with or without PGO)
%{__x} build sysroot

# Build everything else normally
%{__x} build
%{__x} doc

for triple in %{?all_targets} ; do
  %{__x} build --target=$triple std
done

# Collect cargo-vendor.txt for each tool and std
%{cargo_tree_manifest -n rustc -- -p rustc-main -p rustdoc}
%{cargo_tree_manifest -n cargo -m src/tools/cargo}
%{cargo_tree_manifest -n clippy -m src/tools/clippy}
%{cargo_tree_manifest -n rust-analyzer -m src/tools/rust-analyzer}
%{cargo_tree_manifest -n rustfmt -m src/tools/rustfmt}

%{cargo_tree_manifest -n std -m library -f backtrace}
for triple in %{?all_targets} ; do
  case $triple in
    *-none*) %{cargo_tree_manifest -n std-$triple -m library/alloc -t $triple} ;;
    *) %{cargo_tree_manifest -n std-$triple -m library -f backtrace -t $triple} ;;
  esac
done

%install
%if 0%{?rhel} && 0%{?rhel} <= 9
%{?set_build_flags}
%endif
%{export_rust_env}

DESTDIR=%{buildroot} %{__x} install

for triple in %{?all_targets} ; do
  DESTDIR=%{buildroot} %{__x} install --target=$triple std
done

# These are transient files used by x.py dist and install
rm -rf ./build/dist/ ./build/tmp/

# Some of the components duplicate-install binaries, leaving backups we don't want
rm -f %{buildroot}%{_bindir}/*.old

# Make sure the compiler's shared libraries are in the proper libdir
%if "%{_libdir}" != "%{common_libdir}"
mkdir -p %{buildroot}%{_libdir}
find %{buildroot}%{common_libdir} -maxdepth 1 -type f -name '*.so' \
  -exec mv -v -t %{buildroot}%{_libdir} '{}' '+'
%endif

# The shared libraries should be executable for debuginfo extraction.
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' \
  -exec chmod -v +x '{}' '+'

# The shared standard library is excluded from Provides, because it has no
# stable ABI. However, we still ship it alongside the static target libraries
# to enable some niche local use-cases, like the `evcxr` REPL.
# Make sure those libraries are also executable for debuginfo extraction.
find %{buildroot}%{rustlibdir} -type f -name '*.so' \
  -exec chmod -v +x '{}' '+'

# Remove installer artifacts (manifests, uninstall scripts, etc.)
find %{buildroot}%{rustlibdir} -maxdepth 1 -type f -exec rm -v '{}' '+'

# Remove backup files from %%configure munging
find %{buildroot}%{rustlibdir} -type f -name '*.orig' -exec rm -v '{}' '+'

# https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error
# We don't actually need to ship any of those python scripts in rust-src anyway.
find %{buildroot}%{rustlibdir}/src -type f -name '*.py' -exec rm -v '{}' '+'

# Remove unwanted documentation files (we already package them)
rm -f %{buildroot}%{_pkgdocdir}/README.md
rm -f %{buildroot}%{_pkgdocdir}/COPYRIGHT
rm -f %{buildroot}%{_pkgdocdir}/LICENSE
rm -f %{buildroot}%{_pkgdocdir}/LICENSE-APACHE
rm -f %{buildroot}%{_pkgdocdir}/LICENSE-MIT
rm -f %{buildroot}%{_pkgdocdir}/LICENSE-THIRD-PARTY
rm -f %{buildroot}%{_pkgdocdir}/*.old

# Sanitize the HTML documentation
find %{buildroot}%{_pkgdocdir}/html -empty -delete
find %{buildroot}%{_pkgdocdir}/html -type f -exec chmod -x '{}' '+'

# Create the path for crate-devel packages
mkdir -p %{buildroot}%{_datadir}/cargo/registry

# Cargo no longer builds its own documentation
# https://github.com/rust-lang/cargo/pull/4904
mkdir -p %{buildroot}%{_docdir}/cargo
ln -sT ../rust/html/cargo/ %{buildroot}%{_docdir}/cargo/html

# We don't want Rust copies of LLVM tools (rust-lld, rust-llvm-dwp)
rm -f %{buildroot}%{rustlibdir}/%{rust_triple}/bin/rust-ll*

%if 0%{?rhel}
# This allows users to build packages using Rust Toolset.
%{__install} -D -m 644 %{S:100} %{buildroot}%{rpmmacrodir}/macros.rust-toolset
%{__install} -D -m 644 %{S:101} %{buildroot}%{rpmmacrodir}/macros.rust-srpm
%{__install} -D -m 644 %{S:102} %{buildroot}%{_fileattrsdir}/cargo_vendor.attr
%{__install} -D -m 755 %{S:103} %{buildroot}%{_rpmconfigdir}/cargo_vendor.prov
%endif


%check
%if 0%{?rhel} && 0%{?rhel} <= 9
%{?set_build_flags}
%endif
%{export_rust_env}

# Sanity-check the installed binaries, debuginfo-stripped and all.
TMP_HELLO=$(mktemp -d)
(
  cd "$TMP_HELLO"
  export RUSTC=%{buildroot}%{_bindir}/rustc \
    LD_LIBRARY_PATH="%{buildroot}%{_libdir}:$LD_LIBRARY_PATH"
  %{buildroot}%{_bindir}/cargo init --name hello-world
  %{buildroot}%{_bindir}/cargo run --verbose

  # Sanity-check that code-coverage builds and runs
  env RUSTFLAGS="-Cinstrument-coverage" %{buildroot}%{_bindir}/cargo run --verbose
  test -r default_*.profraw

  # Try a build sanity-check for other std-enabled targets
  for triple in %{?mingw_targets} %{?wasm_targets}; do
    %{buildroot}%{_bindir}/cargo build --verbose --target=$triple
  done
)
rm -rf "$TMP_HELLO"

# The results are not stable on koji, so mask errors and just log it.
# Some of the larger test artifacts are manually cleaned to save space.

# - Bootstrap is excluded because it's not something we ship, and a lot of its
#   tests are geared toward the upstream CI environment.
# - Crashes are excluded because they are less reliable, especially stuff like
#   SIGSEGV across different arches -- UB can do all kinds of weird things.
#   They're only meant to notice "accidental" fixes anyway, not *should* crash.
%{__x} test --no-fail-fast --skip={src/bootstrap,tests/crashes} || :
rm -rf "./build/%{rust_triple}/test/"

# Cargo tests skip list
# Every test skipped here must have a documented reason to be skipped.
# Duplicates are safe to add.

# This test relies on the DNS to fail to resolve the host. DNS is not enabled
# in mock in koji so the DNS resolution doesn't take place to begin with.
# We test this after packaging
%global cargo_test_skip_list net_err_suggests_fetch_with_cli

%ifarch aarch64
# https://github.com/rust-lang/rust/issues/123733
%global cargo_test_skip_list %{cargo_test_skip_list} panic_abort_doc_tests
%endif
%if %with disabled_libssh2
# These tests need ssh - guaranteed to fail when libssh2 is disabled.
%global cargo_test_skip_list %{shrink:
  %{cargo_test_skip_list}
  net_err_suggests_fetch_with_cli
  ssh_something_happens
}
%endif
%if "%{cargo_test_skip_list}" != ""
%define cargo_test_skip --test-args "%(printf -- '--skip %%s ' %{cargo_test_skip_list})"
%endif
%{__x} test --no-fail-fast cargo %{?cargo_test_skip} || :
rm -rf "./build/%{rust_triple}/stage2-tools/%{rust_triple}/cit/"

%{__x} test --no-fail-fast clippy || :

%{__x} test --no-fail-fast rust-analyzer || :

%{__x} test --no-fail-fast rustfmt || :

%ldconfig_scriptlets


%files
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%doc README.md
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_libdir}/librustc_driver-*.so
%{_libexecdir}/rust-analyzer-proc-macro-srv
%{_mandir}/man1/rustc.1*
%{_mandir}/man1/rustdoc.1*
%license build/manifests/rustc/cargo-vendor.txt
%license %{_pkgdocdir}/COPYRIGHT.html
%license %{_pkgdocdir}/licenses/
%exclude %{_sysconfdir}/target-spec-json-schema.json


%files std-static
%dir %{rustlibdir}
%dir %{rustlibdir}/%{rust_triple}
%dir %{rustlibdir}/%{rust_triple}/lib
%{rustlibdir}/%{rust_triple}/lib/*.rlib
%{rustlibdir}/%{rust_triple}/lib/*.rmeta
%{rustlibdir}/%{rust_triple}/lib/*.so
%license build/manifests/std/cargo-vendor.txt
%license %{_pkgdocdir}/COPYRIGHT-library.html

%global target_files()        \
%files std-static-%1          \
%dir %{rustlibdir}            \
%dir %{rustlibdir}/%1         \
%dir %{rustlibdir}/%1/lib     \
%{rustlibdir}/%1/lib/*.rlib   \
%{rustlibdir}/%1/lib/*.rmeta  \
%license build/manifests/std-%1/cargo-vendor.txt

%if %target_enabled i686-pc-windows-gnu
%target_files i686-pc-windows-gnu
%{rustlibdir}/i686-pc-windows-gnu/lib/rs*.o
%exclude %{rustlibdir}/i686-pc-windows-gnu/lib/*.dll
%exclude %{rustlibdir}/i686-pc-windows-gnu/lib/*.dll.a
%endif

%if %target_enabled x86_64-pc-windows-gnu
%target_files x86_64-pc-windows-gnu
%{rustlibdir}/x86_64-pc-windows-gnu/lib/rs*.o
%exclude %{rustlibdir}/x86_64-pc-windows-gnu/lib/*.dll
%exclude %{rustlibdir}/x86_64-pc-windows-gnu/lib/*.dll.a
%endif

%if %target_enabled wasm32-unknown-unknown
%target_files wasm32-unknown-unknown
%endif

%if %target_enabled wasm32-wasip1
%target_files wasm32-wasip1
%if %with bundled_wasi_libc
%dir %{rustlibdir}/wasm32-wasip1/lib/self-contained
%{rustlibdir}/wasm32-wasip1/lib/self-contained/crt*.o
%{rustlibdir}/wasm32-wasip1/lib/self-contained/libc.a
%endif
%endif

%if %target_enabled x86_64-unknown-none
%target_files x86_64-unknown-none
%endif

%if %target_enabled aarch64-unknown-uefi
%target_files aarch64-unknown-uefi
%endif

%if %target_enabled x86_64-unknown-uefi
%target_files x86_64-unknown-uefi
%endif

%if %target_enabled aarch64-unknown-none-softfloat
%target_files aarch64-unknown-none-softfloat
%endif


%files debugger-common
%dir %{rustlibdir}
%dir %{rustlibdir}/etc
%{rustlibdir}/etc/rust_*.py*


%files gdb
%{_bindir}/rust-gdb
%{rustlibdir}/etc/gdb_*
%exclude %{_bindir}/rust-gdbgui


%files lldb
%{_bindir}/rust-lldb
%{rustlibdir}/etc/lldb_*


%files doc
%docdir %{_pkgdocdir}
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
# former cargo-doc
%docdir %{_docdir}/cargo
%dir %{_docdir}/cargo
%{_docdir}/cargo/html


%files -n cargo
%license src/tools/cargo/LICENSE-{APACHE,MIT,THIRD-PARTY}
%doc src/tools/cargo/README.md
%{_bindir}/cargo
%{_mandir}/man1/cargo*.1*
%{_sysconfdir}/bash_completion.d/cargo
%{_datadir}/zsh/site-functions/_cargo
%dir %{_datadir}/cargo
%dir %{_datadir}/cargo/registry
%license build/manifests/cargo/cargo-vendor.txt


%files -n rustfmt
%{_bindir}/rustfmt
%{_bindir}/cargo-fmt
%doc src/tools/rustfmt/{README,CHANGELOG,Configurations}.md
%license src/tools/rustfmt/LICENSE-{APACHE,MIT}
%license build/manifests/rustfmt/cargo-vendor.txt


%files analyzer
%{_bindir}/rust-analyzer
%doc src/tools/rust-analyzer/README.md
%license src/tools/rust-analyzer/LICENSE-{APACHE,MIT}
%license build/manifests/rust-analyzer/cargo-vendor.txt


%files -n clippy
%{_bindir}/cargo-clippy
%{_bindir}/clippy-driver
%doc src/tools/clippy/{README.md,CHANGELOG.md}
%license src/tools/clippy/LICENSE-{APACHE,MIT}
%license build/manifests/clippy/cargo-vendor.txt


%files src
%dir %{rustlibdir}
%{rustlibdir}/src


%if 0%{?rhel}
%files toolset-srpm-macros
%{rpmmacrodir}/macros.rust-srpm

%files toolset
%{rpmmacrodir}/macros.rust-toolset
%{_fileattrsdir}/cargo_vendor.attr
%{_rpmconfigdir}/cargo_vendor.prov
%endif


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.94.0-2
- Latest state for rust

* Thu Mar 05 2026 Josh Stone <jistone@redhat.com> - 1.94.0-1
- Update to Rust 1.94.0

* Thu Feb 12 2026 Josh Stone <jistone@redhat.com> - 1.93.1-1
- Update to Rust 1.93.1

* Wed Feb 04 2026 Josh Stone <jistone@redhat.com> - 1.93.0-3
- Fix unnecessary rebuilds (rust#152077)

* Tue Jan 27 2026 Josh Stone <jistone@redhat.com> - 1.93.0-2
- Add source file verification

* Thu Jan 22 2026 Paul Murphy <murp@redhat.com> - 1.93.0-1
- Update to Rust 1.93.0

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.92.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 15 2025 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.92.0-3
- Update rpminspect.yaml

* Mon Dec 15 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.92.0-2
- Update disable-libssh2 patch for 1.92.0

* Thu Dec 11 2025 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.92.0-1
- Update to Rust 1.92.0

* Mon Nov 10 2025 Paul Murphy <murp@redhat.com> - 1.91.1-1
- Update to Rust 1.91.1

* Thu Oct 30 2025 Josh Stone <jistone@redhat.com> - 1.91.0-1
- Update to Rust 1.91.0

* Thu Sep 18 2025 Josh Stone <jistone@redhat.com> - 1.90.0-1
- Update to Rust 1.90.0

* Fri Aug 15 2025 Josh Stone <jistone@redhat.com> - 1.89.0-4
- Re-enable PGO for ppc64le

* Thu Aug 14 2025 Paul Murphy <paumurph@redhat.com> - 1.89.0-3
- Enable optimized-compiler-builtins on the native compiler

* Thu Aug 07 2025 Jakub Jelen <jjelen@fedoraproject.org> - 1.89.0-2
- Rust-gdb and lldb require rustc to find a sysroot

* Thu Aug 07 2025 Paul Murphy <paumurph@redhat.com> - 1.89.0-1
- Update to Rust 1.89.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.88.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Josh Stone <jistone@redhat.com> - 1.88.0-1
- Update to Rust 1.88.0

* Tue May 27 2025 Josh Stone <jistone@redhat.com> - 1.87.0-2
- Skip PGO on all ppc64le builds for now

* Thu May 15 2025 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.87.0-1
- Update to Rust 1.87.0

* Thu Apr 24 2025 Josh Stone <jistone@redhat.com> - 1.86.0-2
- Temporarily skip PGO on RHEL ppc64le

* Thu Apr 03 2025 Josh Stone <jistone@redhat.com> - 1.86.0-1
- Update to Rust 1.86.0

* Tue Mar 18 2025 Josh Stone <jistone@redhat.com> - 1.85.1-1
- Update to Rust 1.85.1

* Mon Mar 10 2025 Josh Stone <jistone@redhat.com> - 1.85.0-5
- Clean up LLVM-compat and enable it on ELN

* Sat Mar 08 2025 Josh Stone <jistone@redhat.com> - 1.85.0-4
- Lock cargo to the matching rust version

* Sat Mar 08 2025 Josh Stone <jistone@redhat.com> - 1.85.0-3
- Add `Provides: bundled(crate(_))` for vendored dependencies

* Wed Feb 26 2025 Josh Stone <jistone@redhat.com> - 1.85.0-2
- ld.gold isn't needed for tests anymore

* Thu Feb 20 2025 Josh Stone <jistone@redhat.com> - 1.85.0-1
- Update to Rust 1.85.0

* Thu Jan 30 2025 Josh Stone <jistone@redhat.com> - 1.84.1-1
- Update to Rust 1.84.1

* Mon Jan 27 2025 Josh Stone <jistone@redhat.com> - 1.84.0-7
- Restore libstd.so for uses like evcxr

* Mon Jan 20 2025 Josh Stone <jistone@redhat.com> - 1.84.0-6
- Use system oniguruma for building rust-docs

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.84.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Josh Stone <jistone@redhat.com> - 1.84.0-4
- Fully remove the shared standard library

* Fri Jan 10 2025 Josh Stone <jistone@redhat.com> - 1.84.0-3
- Revert use of clang/lld; patch cc-rs#1354 instead

* Thu Jan 09 2025 Josh Stone <jistone@redhat.com> - 1.84.0-2
- Use lld when building the compiler

* Thu Jan 09 2025 Josh Stone <jistone@redhat.com> - 1.84.0-1
- Update to Rust 1.84.0

* Wed Dec 18 2024 Josh Stone <jistone@redhat.com> - 1.83.0-6
- prep: Remove submodules we don't need.

* Wed Dec 18 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.83.0-5
- Update rpminspect unicode exceptions

* Mon Dec 16 2024 David Michael <fedora.dm0@gmail.com> - 1.83.0-4
- Put an upper bound on the cargo requirement as well

* Tue Dec 03 2024 Josh Stone <jistone@redhat.com> - 1.83.0-2
- Exclude target shared libraries

* Thu Nov 28 2024 Josh Stone <jistone@redhat.com> - 1.83.0-1
- Update to Rust 1.83.0

* Tue Nov 12 2024 Josh Stone <jistone@redhat.com> - 1.82.0-4
- [eln] update to wasi-libc-24

* Wed Oct 30 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.82.0-3
- Add unicode exception rules for rpminpect

* Tue Oct 29 2024 Josh Stone <jistone@redhat.com> - 1.82.0-2
- Set build.jobs for everything

* Thu Oct 17 2024 Josh Stone <jistone@redhat.com> - 1.82.0-1
- Update to Rust 1.82.0

* Sat Oct 12 2024 Davide Cavalca <dcavalca@centosproject.org> - 1.81.0-7
- Reenable the aarch64-unknown-none-softfloat target on RHEL

* Tue Oct 08 2024 Josh Stone <jistone@redhat.com> - 1.81.0-6
- Require rust libraries for rust-analyzer; Fixes RHBZ#2316529

* Wed Oct 02 2024 Josh Stone <jistone@redhat.com> - 1.81.0-5
- [eln] Upgrade wasi-libc for clang-19

* Mon Sep 30 2024 Josh Stone <jistone@redhat.com> - 1.81.0-3
- Apply patches for LLVM 19

* Mon Sep 30 2024 Josh Stone <jistone@redhat.com> - 1.81.0-2
- Only add an automatic SONAME for Rust dylibs

* Thu Sep 05 2024 Josh Stone <jistone@redhat.com> - 1.81.0-1
- Update to Rust 1.81.0

* Mon Aug 12 2024 Nikita Popov <npopov@redhat.com> - 1.80.1-1
- Update to Rust 1.80.1

* Sun Jul 28 2024 Songsong Zhang <u2fsdgvkx1@gmail.com> - 1.80.0-2
- do not install gold in riscv64

* Thu Jul 25 2024 Josh Stone <jistone@redhat.com> - 1.80.0-1
- Update to Rust 1.80.0

* Thu Jul 25 2024 Gerd Hoffmann <kraxel@redhat.com> - 1.79.0-8
- lld fixup for aarch64-unknown-uefi

* Thu Jul 25 2024 Gerd Hoffmann <kraxel@redhat.com> - 1.79.0-7
- enable aarch64-unknown-uefi

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.79.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.79.0-5
- Import gating tests from tests/rust

* Thu Jun 20 2024 Josh Stone <jistone@redhat.com> - 1.79.0-4
- Update bundled wasi-libc for distinct target triples

* Thu Jun 13 2024 Nikita Popov <npopov@redhat.com> - 1.79.0-1
- Update to 1.79.0

* Tue May 28 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.78.0-3
- rust-toolset Requires: rust-toolset-srpm-macros

* Thu May 02 2024 Josh Stone <jistone@redhat.com> - 1.78.0-1
- Update to 1.78.0

* Tue Apr 30 2024 Josh Stone <jistone@redhat.com> - 1.77.2-7
- Use bundled sqlite3 when the system version is too old.

* Thu Apr 25 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.77.2-6
- test: Move librsvg2 and stratisd rebuild tests into rpm-rebuild test

* Thu Apr 25 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 1.77.2-5
- tests: Add rpmbuild tests

* Wed Apr 24 2024 Josh Stone <jistone@redhat.com> - 1.77.2-4
- Disable brp-strip-static-archive

* Wed Apr 17 2024 Josh Stone <jistone@redhat.com> - 1.77.2-3
- Add fixes for several test cases

* Tue Apr 16 2024 Josh Stone <jistone@redhat.com> - 1.77.2-2
- [rhel] Rename rust-srpm-macros to rust-toolset-srpm-macros

* Tue Apr 09 2024 Josh Stone <jistone@redhat.com> - 1.77.2-1
- Update to 1.77.2; Fixes RHBZ#2274248 CVE-2024-24576

* Fri Apr 05 2024 Josh Stone <jistone@redhat.com> - 1.77.0-3
- Ensure more consistency in PGO flags -- fixes Cargo tests

* Thu Mar 21 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 1.77.0-2
- Add build target for aarch64-unknown-none-softfloat

* Thu Mar 21 2024 Nikita Popov <npopov@redhat.com> - 1.77.0-1
- Update to 1.77.0

* Thu Feb 08 2024 Josh Stone <jistone@redhat.com> - 1.76.0-1
- Update to 1.76.0.

* Tue Jan 30 2024 Josh Stone <jistone@redhat.com> - 1.75.0-3
- Consolidate 32-bit build compromises.
- Update rust-toolset and add rust-srpm-macros for ELN.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.75.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 31 2023 Josh Stone <jistone@redhat.com> - 1.75.0-1
- Update to 1.75.0.

* Thu Dec 07 2023 Josh Stone <jistone@redhat.com> - 1.74.1-1
- Update to 1.74.1.

* Thu Nov 16 2023 Josh Stone <jistone@redhat.com> - 1.74.0-1
- Update to 1.74.0.

* Thu Oct 26 2023 Josh Stone <jistone@redhat.com> - 1.73.0-2
- Use thin-LTO and PGO for rustc itself.

* Thu Oct 05 2023 Josh Stone <jistone@redhat.com> - 1.73.0-1
- Update to 1.73.0.
- Drop el7 conditionals from the spec.

* Fri Sep 29 2023 Josh Stone <jistone@redhat.com> - 1.72.1-3
- Fix the profiler runtime with compiler-rt-17
- Switch to unbundled wasi-libc on Fedora
- Use emmalloc instead of CC0 dlmalloc when bundling wasi-libc

* Mon Sep 25 2023 Josh Stone <jistone@redhat.com> - 1.72.1-2
- Fix LLVM dependency for ELN
- Add build target for x86_64-unknown-none
- Add build target for x86_64-unknown-uefi

* Tue Sep 19 2023 Josh Stone <jistone@redhat.com> - 1.72.1-1
- Update to 1.72.1.
- Migrated to SPDX license

* Thu Aug 24 2023 Josh Stone <jistone@redhat.com> - 1.72.0-1
- Update to 1.72.0.

* Mon Aug 07 2023 Josh Stone <jistone@redhat.com> - 1.71.1-1
- Update to 1.71.1.
- Security fix for CVE-2023-38497

* Tue Jul 25 2023 Josh Stone <jistone@redhat.com> - 1.71.0-3
- Relax the suspicious_double_ref_op lint
- Enable the profiler runtime for native hosts

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.71.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Josh Stone <jistone@redhat.com> - 1.71.0-1
- Update to 1.71.0.

* Fri Jun 23 2023 Josh Stone <jistone@redhat.com> - 1.70.0-2
- Override default target CPUs to match distro settings

* Thu Jun 01 2023 Josh Stone <jistone@redhat.com> - 1.70.0-1
- Update to 1.70.0.

* Fri May 05 2023 Josh Stone <jistone@redhat.com> - 1.69.0-3
- Fix debuginfo with LLVM 16

* Mon May 01 2023 Josh Stone <jistone@redhat.com> - 1.69.0-2
- Build with LLVM 15 on Fedora 38+

* Thu Apr 20 2023 Josh Stone <jistone@redhat.com> - 1.69.0-1
- Update to 1.69.0.
- Obsolete rust-analysis.

* Tue Mar 28 2023 Josh Stone <jistone@redhat.com> - 1.68.2-1
- Update to 1.68.2.

* Thu Mar 23 2023 Josh Stone <jistone@redhat.com> - 1.68.1-1
- Update to 1.68.1.

* Thu Mar 09 2023 Josh Stone <jistone@redhat.com> - 1.68.0-1
- Update to 1.68.0.

* Tue Mar 07 2023 David Michael <fedora.dm0@gmail.com> - 1.67.1-3
- Add a virtual Provides to rust-std-static containing the target triple.

* Mon Feb 20 2023 Orion Poplawski <orion@nwra.com> - 1.67.1-2
- Ship rust-toolset for EPEL7

* Thu Feb 09 2023 Josh Stone <jistone@redhat.com> - 1.67.1-1
- Update to 1.67.1.

* Fri Feb 03 2023 Josh Stone <jistone@redhat.com> - 1.67.0-3
- Unbundle libgit2 on Fedora 38.

* Fri Jan 27 2023 Adam Williamson <awilliam@redhat.com> - 1.67.0-2
- Backport PR #107360 to fix build of mesa
- Backport 675fa0b3 to fix bootstrapping failure

* Thu Jan 26 2023 Josh Stone <jistone@redhat.com> - 1.67.0-1
- Update to 1.67.0.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.66.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Josh Stone <jistone@redhat.com> - 1.66.1-1
- Update to 1.66.1.
- Security fix for CVE-2022-46176

* Thu Dec 15 2022 Josh Stone <jistone@redhat.com> - 1.66.0-1
- Update to 1.66.0.

* Thu Nov 03 2022 Josh Stone <jistone@redhat.com> - 1.65.0-1
- Update to 1.65.0.
- rust-analyzer now obsoletes rls.

* Thu Sep 22 2022 Josh Stone <jistone@redhat.com> - 1.64.0-1
- Update to 1.64.0.
- Add rust-analyzer.

* Thu Aug 11 2022 Josh Stone <jistone@redhat.com> - 1.63.0-1
- Update to 1.63.0.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.62.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Josh Stone <jistone@redhat.com> - 1.62.1-1
- Update to 1.62.1.

* Wed Jul 13 2022 Josh Stone <jistone@redhat.com> - 1.62.0-2
- Prevent unsound coercions from functions with opaque return types.

* Thu Jun 30 2022 Josh Stone <jistone@redhat.com> - 1.62.0-1
- Update to 1.62.0.

* Mon May 23 2022 Josh Stone <jistone@redhat.com> - 1.61.0-2
- Add missing target_feature to the list of well known cfg names

* Thu May 19 2022 Josh Stone <jistone@redhat.com> - 1.61.0-1
- Update to 1.61.0.
- Add rust-toolset for ELN.

* Thu Apr 07 2022 Josh Stone <jistone@redhat.com> - 1.60.0-1
- Update to 1.60.0.

* Fri Mar 25 2022 Josh Stone <jistone@redhat.com> - 1.59.0-4
- Fix the archive index for wasm32-wasi's libc.a

* Fri Mar 04 2022 Stephen Gallagher <sgallagh@redhat.com> - 1.59.0-3
- Rebuild against the bootstrapped build

* Fri Mar 04 2022 Stephen Gallagher <sgallagh@redhat.com> - 1.59.0-2.1
- Bootstrapping for Fedora ELN

* Tue Mar 01 2022 Josh Stone <jistone@redhat.com> - 1.59.0-2
- Fix s390x hangs, rhbz#2058803

* Thu Feb 24 2022 Josh Stone <jistone@redhat.com> - 1.59.0-1
- Update to 1.59.0.
- Revert to libgit2 1.3.x

* Sun Feb 20 2022 Igor Raits <igor.raits@gmail.com> - 1.58.1-2
- Rebuild for libgit2 1.4.x

* Thu Jan 20 2022 Josh Stone <jistone@redhat.com> - 1.58.1-1
- Update to 1.58.1.

* Thu Jan 13 2022 Josh Stone <jistone@redhat.com> - 1.58.0-1
- Update to 1.58.0.

* Wed Jan 05 2022 Josh Stone <jistone@redhat.com> - 1.57.0-2
- Add rust-std-static-i686-pc-windows-gnu
- Add rust-std-static-x86_64-pc-windows-gnu

* Thu Dec 02 2021 Josh Stone <jistone@redhat.com> - 1.57.0-1
- Update to 1.57.0, fixes rhbz#2028675.
- Backport rust#91070, fixes rhbz#1990657
- Add rust-std-static-wasm32-wasi

* Sun Nov 28 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.56.1-3
- De-bootstrap (libgit2)

* Sun Nov 28 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.56.1-2
- Rebuild for libgit2 1.3.x

* Mon Nov 01 2021 Josh Stone <jistone@redhat.com> - 1.56.1-1
- Update to 1.56.1.

* Thu Oct 21 2021 Josh Stone <jistone@redhat.com> - 1.56.0-1
- Update to 1.56.0.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.55.0-2
- Rebuilt with OpenSSL 3.0.0

* Thu Sep 09 2021 Josh Stone <jistone@redhat.com> - 1.55.0-1
- Update to 1.55.0.
- Use llvm-ranlib for wasm rlibs; Fixes rhbz#2002612

* Tue Aug 24 2021 Josh Stone <jistone@redhat.com> - 1.54.0-2
- Build with LLVM 12 on Fedora 35+

* Thu Jul 29 2021 Josh Stone <jistone@redhat.com> - 1.54.0-1
- Update to 1.54.0.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.53.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Josh Stone <jistone@redhat.com> - 1.53.0-2
- Exclude wasm on s390x for lack of lld

* Thu Jun 17 2021 Josh Stone <jistone@redhat.com> - 1.53.0-1
- Update to 1.53.0.

* Wed Jun 02 2021 Josh Stone <jistone@redhat.com> - 1.52.1-2
- Set rust.codegen-units-std=1 for all targets again.
- Add rust-std-static-wasm32-unknown-unknown.
- Rebuild f34 with LLVM 12.

* Mon May 10 2021 Josh Stone <jistone@redhat.com> - 1.52.1-1
- Update to 1.52.1.

* Thu May 06 2021 Josh Stone <jistone@redhat.com> - 1.52.0-1
- Update to 1.52.0.

* Fri Apr 16 2021 Josh Stone <jistone@redhat.com> - 1.51.0-3
- Security fixes for CVE-2020-36323, CVE-2021-31162

* Wed Apr 14 2021 Josh Stone <jistone@redhat.com> - 1.51.0-2
- Security fixes for CVE-2021-28876, CVE-2021-28878, CVE-2021-28879
- Fix bootstrap for stage0 rust 1.51

* Thu Mar 25 2021 Josh Stone <jistone@redhat.com> - 1.51.0-1
- Update to 1.51.0.

* Thu Feb 11 2021 Josh Stone <jistone@redhat.com> - 1.50.0-1
- Update to 1.50.0.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Josh Stone <jistone@redhat.com> - 1.49.0-1
- Update to 1.49.0.

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.48.0-3
- De-bootstrap

* Mon Dec 28 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.48.0-2
- Rebuild for libgit2 1.1.x

* Thu Nov 19 2020 Josh Stone <jistone@redhat.com> - 1.48.0-1
- Update to 1.48.0.

* Sat Oct 10 2020 Jeff Law <law@redhat.com> - 1.47.0-2
- Re-enable LTO

* Thu Oct 08 2020 Josh Stone <jistone@redhat.com> - 1.47.0-1
- Update to 1.47.0.

* Fri Aug 28 2020 Fabio Valentini <decathorpe@gmail.com> - 1.46.0-2
- Fix LTO with doctests (backported cargo PR#8657).

* Thu Aug 27 2020 Josh Stone <jistone@redhat.com> - 1.46.0-1
- Update to 1.46.0.

* Mon Aug 03 2020 Josh Stone <jistone@redhat.com> - 1.45.2-1
- Update to 1.45.2.

* Thu Jul 30 2020 Josh Stone <jistone@redhat.com> - 1.45.1-1
- Update to 1.45.1.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Josh Stone <jistone@redhat.com> - 1.45.0-1
- Update to 1.45.0.

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 1.44.1-2
- Disable LTO

* Thu Jun 18 2020 Josh Stone <jistone@redhat.com> - 1.44.1-1
- Update to 1.44.1.

* Thu Jun 04 2020 Josh Stone <jistone@redhat.com> - 1.44.0-1
- Update to 1.44.0.

* Thu May 07 2020 Josh Stone <jistone@redhat.com> - 1.43.1-1
- Update to 1.43.1.

* Thu Apr 23 2020 Josh Stone <jistone@redhat.com> - 1.43.0-1
- Update to 1.43.0.

* Thu Mar 12 2020 Josh Stone <jistone@redhat.com> - 1.42.0-1
- Update to 1.42.0.

* Thu Feb 27 2020 Josh Stone <jistone@redhat.com> - 1.41.1-1
- Update to 1.41.1.

* Thu Feb 20 2020 Josh Stone <jistone@redhat.com> - 1.41.0-2
- Rebuild with llvm9.0

* Thu Jan 30 2020 Josh Stone <jistone@redhat.com> - 1.41.0-1
- Update to 1.41.0.

* Thu Jan 16 2020 Josh Stone <jistone@redhat.com> - 1.40.0-3
- Build compiletest with in-tree libtest

* Tue Jan 07 2020 Josh Stone <jistone@redhat.com> - 1.40.0-2
- Fix compiletest with newer (local-rebuild) libtest
- Fix ARM EHABI unwinding

* Thu Dec 19 2019 Josh Stone <jistone@redhat.com> - 1.40.0-1
- Update to 1.40.0.

* Tue Nov 12 2019 Josh Stone <jistone@redhat.com> - 1.39.0-2
- Fix a couple build and test issues with rustdoc.

* Thu Nov 07 2019 Josh Stone <jistone@redhat.com> - 1.39.0-1
- Update to 1.39.0.

* Fri Sep 27 2019 Josh Stone <jistone@redhat.com> - 1.38.0-2
- Filter the libraries included in rust-std (rhbz1756487)

* Thu Sep 26 2019 Josh Stone <jistone@redhat.com> - 1.38.0-1
- Update to 1.38.0.

* Thu Aug 15 2019 Josh Stone <jistone@redhat.com> - 1.37.0-1
- Update to 1.37.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Josh Stone <jistone@redhat.com> - 1.36.0-1
- Update to 1.36.0.

* Wed May 29 2019 Josh Stone <jistone@redhat.com> - 1.35.0-2
- Fix compiletest for rebuild testing.

* Thu May 23 2019 Josh Stone <jistone@redhat.com> - 1.35.0-1
- Update to 1.35.0.

* Tue May 14 2019 Josh Stone <jistone@redhat.com> - 1.34.2-1
- Update to 1.34.2 -- fixes CVE-2019-12083.

* Tue Apr 30 2019 Josh Stone <jistone@redhat.com> - 1.34.1-3
- Set rust.codegen-units-std=1

* Fri Apr 26 2019 Josh Stone <jistone@redhat.com> - 1.34.1-2
- Remove the ThinLTO workaround.

* Thu Apr 25 2019 Josh Stone <jistone@redhat.com> - 1.34.1-1
- Update to 1.34.1.
- Add a ThinLTO fix for rhbz1701339.

* Thu Apr 11 2019 Josh Stone <jistone@redhat.com> - 1.34.0-1
- Update to 1.34.0.

* Fri Mar 01 2019 Josh Stone <jistone@redhat.com> - 1.33.0-2
- Fix deprecations for self-rebuild

* Thu Feb 28 2019 Josh Stone <jistone@redhat.com> - 1.33.0-1
- Update to 1.33.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Josh Stone <jistone@redhat.com> - 1.32.0-1
- Update to 1.32.0.

* Mon Jan 07 2019 Josh Stone <jistone@redhat.com> - 1.31.1-9
- Update to 1.31.1 for RLS fixes.

* Thu Dec 06 2018 Josh Stone <jistone@redhat.com> - 1.31.0-8
- Update to 1.31.0 -- Rust 2018!
- clippy/rls/rustfmt are no longer -preview

* Thu Nov 08 2018 Josh Stone <jistone@redhat.com> - 1.30.1-7
- Update to 1.30.1.

* Thu Oct 25 2018 Josh Stone <jistone@redhat.com> - 1.30.0-6
- Update to 1.30.0.

* Mon Oct 22 2018 Josh Stone <jistone@redhat.com> - 1.29.2-5
- Rebuild without bootstrap binaries.

* Sat Oct 20 2018 Josh Stone <jistone@redhat.com> - 1.29.2-4
- Re-bootstrap armv7hl due to rhbz#1639485

* Fri Oct 12 2018 Josh Stone <jistone@redhat.com> - 1.29.2-3
- Update to 1.29.2.

* Tue Sep 25 2018 Josh Stone <jistone@redhat.com> - 1.29.1-2
- Update to 1.29.1.
- Security fix for str::repeat (pending CVE).

* Thu Sep 13 2018 Josh Stone <jistone@redhat.com> - 1.29.0-1
- Update to 1.29.0.
- Add a clippy-preview subpackage

* Mon Aug 13 2018 Josh Stone <jistone@redhat.com> - 1.28.0-3
- Use llvm6.0 instead of llvm-7 for now

* Tue Aug 07 2018 Josh Stone <jistone@redhat.com> - 1.28.0-2
- Rebuild for LLVM ppc64/s390x fixes

* Thu Aug 02 2018 Josh Stone <jistone@redhat.com> - 1.28.0-1
- Update to 1.28.0.

* Tue Jul 24 2018 Josh Stone <jistone@redhat.com> - 1.27.2-4
- Update to 1.27.2.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Josh Stone <jistone@redhat.com> - 1.27.1-2
- Update to 1.27.1.
- Security fix for CVE-2018-1000622

* Thu Jun 21 2018 Josh Stone <jistone@redhat.com> - 1.27.0-1
- Update to 1.27.0.

* Tue Jun 05 2018 Josh Stone <jistone@redhat.com> - 1.26.2-4
- Rebuild without bootstrap binaries.

* Tue Jun 05 2018 Josh Stone <jistone@redhat.com> - 1.26.2-3
- Update to 1.26.2.
- Re-bootstrap to deal with LLVM symbol changes.

* Tue May 29 2018 Josh Stone <jistone@redhat.com> - 1.26.1-2
- Update to 1.26.1.

* Thu May 10 2018 Josh Stone <jistone@redhat.com> - 1.26.0-1
- Update to 1.26.0.

* Mon Apr 16 2018 Dan Callaghan <dcallagh@redhat.com> - 1.25.0-3
- Add cargo, rls, and analysis

* Tue Apr 10 2018 Josh Stone <jistone@redhat.com> - 1.25.0-2
- Filter codegen-backends from Provides too.

* Thu Mar 29 2018 Josh Stone <jistone@redhat.com> - 1.25.0-1
- Update to 1.25.0.

* Thu Mar 01 2018 Josh Stone <jistone@redhat.com> - 1.24.1-1
- Update to 1.24.1.

* Wed Feb 21 2018 Josh Stone <jistone@redhat.com> - 1.24.0-3
- Backport a rebuild fix for rust#48308.

* Mon Feb 19 2018 Josh Stone <jistone@redhat.com> - 1.24.0-2
- rhbz1546541: drop full-bootstrap; cmp libs before symlinking.
- Backport pr46592 to fix local_rebuild bootstrapping.
- Backport pr48362 to fix relative/absolute libdir.

* Thu Feb 15 2018 Josh Stone <jistone@redhat.com> - 1.24.0-1
- Update to 1.24.0.

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.23.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 06 2018 Josh Stone <jistone@redhat.com> - 1.23.0-3
- Use full-bootstrap to work around a rebuild issue.
- Patch binaryen for GCC 8

* Thu Feb 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.23.0-2
- Switch to %%ldconfig_scriptlets

* Mon Jan 08 2018 Josh Stone <jistone@redhat.com> - 1.23.0-1
- Update to 1.23.0.

* Thu Nov 23 2017 Josh Stone <jistone@redhat.com> - 1.22.1-1
- Update to 1.22.1.

* Thu Oct 12 2017 Josh Stone <jistone@redhat.com> - 1.21.0-1
- Update to 1.21.0.

* Mon Sep 11 2017 Josh Stone <jistone@redhat.com> - 1.20.0-2
- ABI fixes for ppc64 and s390x.

* Thu Aug 31 2017 Josh Stone <jistone@redhat.com> - 1.20.0-1
- Update to 1.20.0.
- Add a rust-src subpackage.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Josh Stone <jistone@redhat.com> - 1.19.0-2
- Use find-debuginfo.sh --keep-section .rustc

* Thu Jul 20 2017 Josh Stone <jistone@redhat.com> - 1.19.0-1
- Update to 1.19.0.

* Thu Jun 08 2017 Josh Stone <jistone@redhat.com> - 1.18.0-1
- Update to 1.18.0.

* Mon May 08 2017 Josh Stone <jistone@redhat.com> - 1.17.0-2
- Move shared libraries back to libdir and symlink in rustlib

* Thu Apr 27 2017 Josh Stone <jistone@redhat.com> - 1.17.0-1
- Update to 1.17.0.

* Mon Mar 20 2017 Josh Stone <jistone@redhat.com> - 1.16.0-3
- Make rust-lldb arch-specific to deal with lldb deps

* Fri Mar 17 2017 Josh Stone <jistone@redhat.com> - 1.16.0-2
- Limit rust-lldb arches

* Thu Mar 16 2017 Josh Stone <jistone@redhat.com> - 1.16.0-1
- Update to 1.16.0.
- Use rustbuild instead of the old makefiles.
- Update bootstrapping to include rust-std and cargo.
- Add a rust-lldb subpackage.

* Thu Feb 09 2017 Josh Stone <jistone@redhat.com> - 1.15.1-1
- Update to 1.15.1.
- Require rust-rpm-macros for new crate packaging.
- Keep shared libraries under rustlib/, only debug-stripped.
- Merge and clean up conditionals for epel7.

* Fri Dec 23 2016 Josh Stone <jistone@redhat.com> - 1.14.0-2
- Rebuild without bootstrap binaries.

* Thu Dec 22 2016 Josh Stone <jistone@redhat.com> - 1.14.0-1
- Update to 1.14.0.
- Rewrite bootstrap logic to target specific arches.
- Bootstrap ppc64, ppc64le, s390x. (thanks to Sinny Kumari for testing!)

* Thu Nov 10 2016 Josh Stone <jistone@redhat.com> - 1.13.0-1
- Update to 1.13.0.
- Use hardening flags for linking.
- Split the standard library into its own package
- Centralize rustlib/ under /usr/lib/ for multilib integration.

* Thu Oct 20 2016 Josh Stone <jistone@redhat.com> - 1.12.1-1
- Update to 1.12.1.

* Fri Oct 14 2016 Josh Stone <jistone@redhat.com> - 1.12.0-7
- Rebuild with LLVM 3.9.
- Add ncurses-devel for llvm-config's -ltinfo.

* Thu Oct 13 2016 Josh Stone <jistone@redhat.com> - 1.12.0-6
- Rebuild with llvm-static, preparing for 3.9

* Fri Oct 07 2016 Josh Stone <jistone@redhat.com> - 1.12.0-5
- Rebuild with fixed eu-strip (rhbz1380961)

* Fri Oct 07 2016 Josh Stone <jistone@redhat.com> - 1.12.0-4
- Rebuild without bootstrap binaries.

* Thu Oct 06 2016 Josh Stone <jistone@redhat.com> - 1.12.0-3
- Bootstrap aarch64.
- Use jemalloc's MALLOC_CONF to work around #36944.
- Apply pr36933 to really disable armv7hl NEON.

* Sat Oct 01 2016 Josh Stone <jistone@redhat.com> - 1.12.0-2
- Protect .rustc from rpm stripping.

* Fri Sep 30 2016 Josh Stone <jistone@redhat.com> - 1.12.0-1
- Update to 1.12.0.
- Always use --local-rust-root, even for bootstrap binaries.
- Remove the rebuild conditional - the build system now figures it out.
- Let minidebuginfo do its thing, since metadata is no longer a note.
- Let rust build its own compiler-rt builtins again.

* Sat Sep 03 2016 Josh Stone <jistone@redhat.com> - 1.11.0-3
- Rebuild without bootstrap binaries.

* Fri Sep 02 2016 Josh Stone <jistone@redhat.com> - 1.11.0-2
- Bootstrap armv7hl, with backported no-neon patch.

* Wed Aug 24 2016 Josh Stone <jistone@redhat.com> - 1.11.0-1
- Update to 1.11.0.
- Drop the backported patches.
- Patch get-stage0.py to trust existing bootstrap binaries.
- Use libclang_rt.builtins from compiler-rt, dodging llvm-static issues.
- Use --local-rust-root to make sure the right bootstrap is used.

* Sat Aug 13 2016 Josh Stone <jistone@redhat.com> 1.10.0-4
- Rebuild without bootstrap binaries.

* Fri Aug 12 2016 Josh Stone <jistone@redhat.com> - 1.10.0-3
- Initial import into Fedora (#1356907), bootstrapped
- Format license text as suggested in review.
- Note how the tests already run in parallel.
- Undefine _include_minidebuginfo, because it duplicates ".note.rustc".
- Don't let checks fail the whole build.
- Note that -doc can't be noarch, as rpmdiff doesn't allow variations.

* Tue Jul 26 2016 Josh Stone <jistone@redhat.com> - 1.10.0-2
- Update -doc directory ownership, and mark its licenses.
- Package and declare licenses for libbacktrace and hoedown.
- Set bootstrap_base as a global.
- Explicitly require python2.

* Thu Jul 14 2016 Josh Stone <jistone@fedoraproject.org> - 1.10.0-1
- Initial package, bootstrapped

## END: Generated by rpmautospec
