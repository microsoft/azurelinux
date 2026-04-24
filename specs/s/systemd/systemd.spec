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

# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

%global pkgdir %{_prefix}/lib/systemd
%global system_unit_dir %{pkgdir}/system
%global user_unit_dir %{pkgdir}/user

%if 0%{?__isa_bits} == 64
%global elf_bits (64bit)
%global elf_suffix ()%{elf_bits}
%endif

%bcond bzip2     1
%bcond gnutls    1
%bcond lz4       1
%bcond xz        1
%bcond zlib      1
%bcond zstd      1

# Bootstrap may be needed to break circular dependencies with cryptsetup,
# e.g. when re-building cryptsetup on a json-c SONAME-bump.
%bcond bootstrap 0
%bcond tests     1
%bcond lto       1
# Build docs on 64-bit architectures only
%bcond docs      %[%{?__isa_bits} >= 64]

# Build from git main
%bcond upstream  0

# Build with OBS-specific quirks
%bcond obs       0

# When bootstrap, libcryptsetup is disabled
# but auto-features causes many options to be turned on
# that depend on libcryptsetup (e.g. libcryptsetup-plugins, homed)
%if %{with bootstrap}
%global __meson_auto_features disabled
%endif

# Override %%autorelease. This is ugly, but rpmautospec doesn't implement
# autorelease correctly if the macro is conditionalized in the Release field.
%{?release_override:%global autorelease %{release_override}%{?dist}}

# In OBS, noarch packages are shared between all architectures and
# independent architectures can be rebuilt automatically without all
# the other architectures getting rebuilt. This can result in the noarch
# packages being newer than the archful packages for some architectures,
# which means our current strict deps from the noarch packages on the
# archful packages can't be satisfied.
#
# To address this problem, let's relax the dependencies from the noarch
# packages on the archful packages for OBS builds. Let's only do this for
# OBS builds because this isn't an issue on Fedora as it's impossible to
# build a package for only some of the architectures.
%if %{with obs}
%define noarch_requires_version %{version}
%else
%define noarch_requires_version %{version}-%{release}
%endif

Name:           systemd
Url:            https://systemd.io
# Allow users to specify the version and release when building the rpm by
# setting the %%version_override and %%release_override macros.
# But don't do that on OBS, otherwise the version subst fails, and will be
# like 257-123-gabcd257.1 instead of 257-123-gabcd
%if %{without obs}
Version:        %{?version_override}%{!?version_override:258.4}
%else
Version:        %{?version_override}%{!?version_override:%(cat meson.version)}
%endif
Release:        %autorelease

%global stable %(c="%version"; [ "$c" = "${c#*.*}" ]; echo $?)

# For a breakdown of the licensing, see README
License:        LGPL-2.1-or-later AND MIT AND GPL-2.0-or-later
Summary:        System and Service Manager

# download tarballs with "spectool -g systemd.spec"
# packit will always rewrite the first Source0 it finds, ignoring any conditionals so list
# the fallback source that's used if neither %%branch, %%commit or %%obs are defined first.
%if %{undefined branch} && %{undefined commit} && %{without obs}
Source0:        https://github.com/systemd/systemd/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz
%elif %{defined branch}
Source0:        https://github.com/systemd/systemd/archive/refs/heads/%{branch}.tar.gz
%elif %{defined commit}
Source0:        https://github.com/systemd/systemd/archive/%{commit}/%{name}-%{commit}.tar.gz
%elif %{with obs}
Source0:        https://github.com/systemd/systemd/archive/v%{version_no_tilde}/%{name}-%{version}.tar.xz
%endif
# This file must be available before %%prep.
# It is generated during systemd build and can be found at build/src/rpm/triggers.systemd.sh.
Source1:        triggers.systemd
Source2:        split-files.py
Source4:        test_sysusers_defined.py

Source6:        inittab
Source7:        sysctl.conf.README
Source8:        systemd-journal-remote.xml
Source9:        systemd-journal-gatewayd.xml
Source10:       20-yama-ptrace.conf
Source11:       systemd-udev-trigger-no-reload.conf
# https://fedoraproject.org/wiki/How_to_filter_libabigail_reports
Source13:       libabigail.abignore

Source14:       10-oomd-defaults.conf
Source15:       10-oomd-per-slice-defaults.conf
Source16:       10-timeout-abort.conf
Source17:       10-map-count.conf
Source18:       60-block-scheduler.rules

Source20:       macros.sysusers.compat
Source21:       macros.sysusers
Source22:       sysusers.attr
Source23:       sysusers.prov
Source24:       sysusers.generate-pre.sh

Source25:       98-default-mac-none.link

Source26:       systemd-user

%if 0%{?fedora} < 40 && 0%{?rhel} < 10
# Work-around for dracut issue: run generators directly when we are in initrd
# https://bugzilla.redhat.com/show_bug.cgi?id=2164404
# Drop when dracut-060 is available.
Patch:          https://github.com/systemd/systemd/pull/26494.patch
%endif

%if %{without upstream}
# Those are downstream-only patches, but we don't want them in packit builds.

# Temporarily drop use of PrivateTmp=disconnected. This is causing failures
# in various places:
# https://bugzilla.redhat.com/show_bug.cgi?id=2334015
# https://github.com/coreos/fedora-coreos-tracker/issues/1857
Patch:          0001-Revert-units-use-PrivateTmp-disconnected-instead-of-.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2251843
Patch:          https://github.com/systemd/systemd/pull/30846.patch

# Workaround for a kernel issue. Fixed in kernel-core-6.17.0-0.rc3.31.fc44.x86_64.
Patch:          https://github.com/systemd/systemd/pull/38724.patch

# Again create runlevelX.target. Dropping those files breaks upgrades.
# https://bugzilla.redhat.com/show_bug.cgi?id=2411195
Patch:          0001-Revert-units-drop-runlevel-0-6-.target.patch

# userdb: create userdb root directory with correct label
# We can drop this after SELinux policy is updated to handle the transition.
Patch:          https://github.com/systemd/systemd/pull/38769.patch

# userdb: omit empty parameters field in JSON messages
Patch:          https://github.com/systemd/systemd/pull/38922.patch
%endif

%ifarch %{ix86} x86_64 aarch64 riscv64
%global want_bootloader 1
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  coreutils
BuildRequires:  rpmdevtools
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  libfdisk-devel
BuildRequires:  libpwquality-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  pam-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-libs-devel
%if %{without bootstrap}
BuildRequires:  cryptsetup-devel
# Require (previous version) of our macros package.
# We use the %%systemd_{post,preun,…} macros for various services.
BuildRequires:  systemd-rpm-macros
%endif
BuildRequires:  dbus-devel
BuildRequires:  util-linux
# /usr/bin/getfacl is needed by test-acl-util
BuildRequires:  acl
BuildRequires:  libacl-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libblkid-devel
%if %{with xz}
BuildRequires:  xz-devel
BuildRequires:  xz
%endif
%if %{with lz4}
BuildRequires:  lz4-devel
BuildRequires:  lz4
%endif
%if %{with bzip2}
BuildRequires:  bzip2-devel
%endif
%if %{with zstd}
BuildRequires:  libzstd-devel
%endif
BuildRequires:  libidn2-devel
BuildRequires:  libcurl-devel
BuildRequires:  kmod-devel
BuildRequires:  elfutils-devel
BuildRequires:  openssl-devel
%if 0%{?fedora} >= 41
BuildRequires:  openssl-devel-engine
%endif
%if %{with gnutls}
BuildRequires:  gnutls-devel
%endif
%if 0%{?fedora}
BuildRequires:  qrencode-devel
%endif
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libfido2)
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(tss2-rc)
BuildRequires:  pkgconfig(tss2-mu)
BuildRequires:  pkgconfig(libbpf)
BuildRequires:  systemtap-sdt-devel
%if %{with docs}
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
%endif
BuildRequires:  pkgconfig
BuildRequires:  gperf
BuildRequires:  gawk
BuildRequires:  tree
BuildRequires:  hostname
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(lxml)
BuildRequires:  python3dist(pefile)
%if 0%{?fedora}
BuildRequires:  python3dist(pillow)
%endif
BuildRequires:  python3dist(pytest)
%if 0%{?want_bootloader}
BuildRequires:  python3dist(pyelftools)
%endif
# gzip and lzma are provided by the stdlib
BuildRequires:  firewalld-filesystem
BuildRequires:  libseccomp-devel
BuildRequires:  meson >= 0.43
BuildRequires:  gettext
# We use RUNNING_ON_VALGRIND in tests, so the headers need to be available
%ifarch %{valgrind_arches}
BuildRequires:  valgrind-devel
%endif
%if %{defined rhel} && 0%{?rhel} < 10
BuildRequires: rsync
%endif

%ifnarch %ix86
# bpftool is not built for i368
BuildRequires:  bpftool
BuildRequires:  kernel-devel
%global have_bpf 1
%endif

%if 0%{?fedora}
%ifarch x86_64 aarch64
%global have_xen 0
# That package is only built for those two architectures
%endif
%endif

%if %{with obs}
BuildRequires:  pesign-obs-integration
%endif

Requires(post): coreutils
Requires(post): grep
# systemd-machine-id-setup requires libssl
Requires(post): openssl-libs
Requires:       dbus >= 1.9.18
Requires:       systemd-pam%{_isa} = %{version}-%{release}
Requires(meta): (systemd-rpm-macros = %{version}-%{release} if rpm-build)
Requires:       systemd-libs%{_isa} = %{version}-%{release}
%{?fedora:Recommends:     systemd-networkd = %{version}-%{release}}
%{?fedora:Recommends:     systemd-resolved = %{version}-%{release}}
Requires:       systemd-shared%{_isa} = %{version}-%{release}
Requires:       /usr/bin/systemd-sysusers
# The standalone version doesn't Provide the _isa suffix,
# so this biases towards the common version.
Recommends:     systemd-sysusers%{_isa} = %{version}-%{release}
Recommends:     diffutils
Requires:       (util-linux-core or util-linux)
Requires:       (libbpf >= 2:1.4.7 if libbpf)
Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       syslog
Provides:       systemd-units = %{version}-%{release}
Obsoletes:      system-setup-keyboard < 0.9
Provides:       system-setup-keyboard = 0.9
# systemd-sysv-convert was removed in f20: https://fedorahosted.org/fpc/ticket/308
Obsoletes:      systemd-sysv < 206
Provides:       systemd-sysv = 206
Conflicts:      initscripts < 9.56.1
%if 0%{?fedora}
Conflicts:      fedora-release < 23-0.12
%endif
%if 0%{?fedora} >= 41
BuildRequires:  setup >= 2.15.0-1
BuildRequires:  python3
Conflicts:      setup < 2.15.0-1
Conflicts:      selinux-policy-any < 41.3
%endif

%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10
# Make sure that dracut supports systemd-executor and the renames done for v255,
# and dlopen libraries and read-only fs in initrd.
Conflicts:      dracut < 060-2
%elif 0%{?fedora} || %{without upstream}
# Make sure that dracut supports systemd-executor and the renames done for v255.
Conflicts:      dracut < 059-16
%endif

Conflicts:      systemd-standalone-tmpfiles
Provides:       systemd-tmpfiles = %{version}-%{release}
Conflicts:      systemd-standalone-shutdown
Provides:       systemd-shutdown = %{version}-%{release}

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/halt
Provides:       /usr/sbin/init
Provides:       /usr/sbin/poweroff
Provides:       /usr/sbin/reboot
Provides:       /usr/sbin/runlevel
Provides:       /usr/sbin/shutdown
Provides:       /usr/sbin/telinit
%endif

# Recommends to replace normal Requires deps for stuff that is dlopen()ed
Recommends:     libxkbcommon.so.0%{?elf_suffix}
Recommends:     libidn2.so.0%{?elf_suffix}
Recommends:     libidn2.so.0(IDN2_0.0.0)%{?elf_bits}
Recommends:     libpcre2-8.so.0%{?elf_suffix}
Recommends:     libpwquality.so.1%{?elf_suffix}
Recommends:     libpwquality.so.1(LIBPWQUALITY_1.0)%{?elf_bits}
%if 0%{?fedora}
Recommends:     libqrencode.so.4%{?elf_suffix}
%endif
Recommends:     libbpf.so.1%{?elf_suffix}
Recommends:     libbpf.so.1(LIBBPF_0.4.0)%{?elf_bits}

# used by systemd-coredump and systemd-analyze
Recommends:     libdw.so.1%{?elf_suffix}
Recommends:     libdw.so.1(ELFUTILS_0.186)%{?elf_bits}
Recommends:     libelf.so.1%{?elf_suffix}
Recommends:     libelf.so.1(ELFUTILS_1.7)%{?elf_bits}

# used by dissect, integritysetup, veritysetyp, growfs, repart, cryptenroll, home
Recommends:     libcryptsetup.so.12%{?elf_suffix}
Recommends:     libcryptsetup.so.12(CRYPTSETUP_2.4)%{?elf_bits}

# Libkmod is used to load modules.
Recommends:     libkmod.so.2%{?elf_suffix}
# kmod_list_next, kmod_load_resources, kmod_module_get_initstate,
# kmod_module_get_module, kmod_module_get_name, kmod_module_new_from_lookup,
# kmod_module_probe_insert_module, kmod_module_unref, kmod_module_unref_list,
# kmod_new, kmod_set_log_fn, kmod_unref, kmod_validate_resources
# are part of LIBKMOD_5.
Recommends:     libkmod.so.2(LIBKMOD_5)%{?elf_bits}

Recommends:     libarchive.so.13%{?elf_suffix}

%description
systemd is a system and service manager that runs as PID 1 and starts the rest
of the system. It provides aggressive parallelization capabilities, uses socket
and D-Bus activation for starting services, offers on-demand starting of
daemons, keeps track of processes using Linux control groups, maintains mount
and automount points, and implements an elaborate transactional dependency-based
service control logic. systemd supports SysV and LSB init scripts and works as a
replacement for sysvinit. Other parts of this package are a logging daemon,
utilities to control basic system configuration like the hostname, date, locale,
maintain a list of logged-in users, system accounts, runtime directories and
settings, and a logging daemons.
%if 0%{?stable}
This package was built from the %(c=%version; echo "v${c%.*}-stable") branch of systemd.
%endif

%package libs
Summary:        systemd libraries
License:        LGPL-2.1-or-later AND MIT
Provides:       nss-myhostname = 0.4
Provides:       nss-myhostname%{_isa} = 0.4
Conflicts:      systemd-shared < %{version}-%{release}

%description libs
Libraries for systemd and udev.

%package shared
Summary:        Internal systemd shared library
License:        LGPL-2.1-or-later AND MIT
# in 257.3-6 /usr/lib64/systemd/libsystemd-shared-257.2-14.fc42.so
# was moved from package systemd to systemd-shared.
# Add a conflit to allow downgrades across this change.
Conflicts:      systemd < 257.3-6
Conflicts:      systemd-libs < %{version}-%{release}

%description shared
Internal libraries used by various systemd binaries.

%package pam
Summary:        systemd PAM module
Requires:       systemd = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package rpm-macros
Summary:        Macros that define paths and scriptlets related to systemd
BuildArch:      noarch

%description rpm-macros
Just the definitions of rpm macros.

See
https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd
for information how to use those macros.

%package sysusers
Summary:        systemd-sysusers program
Requires:       systemd-shared%{_isa} = %{version}-%{release}
Conflicts:      systemd-standalone-sysusers
# in 257.3-6 /usr/bin/systemd-sysusers was moved from package systemd
# to systemd-sysusers. Add a conflit to allow downgrades across this change.
Conflicts:      systemd < 257.3-6

%description sysusers
This package contains the systemd-sysusers program.

%package devel
Summary:        Development headers for systemd
License:        LGPL-2.1-or-later AND MIT
Requires:       systemd-libs%{_isa} = %{version}-%{release}
Requires(meta): (systemd-rpm-macros = %{version}-%{release} if rpm-build)
Provides:       libudev-devel = %{version}
Provides:       libudev-devel%{_isa} = %{version}

%description devel
Development headers and auxiliary files for developing applications linking
to libudev or libsystemd.

%package udev
Summary: Rule-based device node and kernel event manager
License:        LGPL-2.1-or-later

Requires:       systemd%{_isa} = %{version}-%{release}
Requires(post):   systemd%{_isa} = %{version}-%{release}
Requires(preun):  systemd%{_isa} = %{version}-%{release}
Requires(postun): systemd%{_isa} = %{version}-%{release}
Requires(post): grep
Requires:       kmod >= 18-4
Provides:       udev = %{version}
Provides:       udev%{_isa} = %{version}
%if 0%{?fedora} || 0%{?rhel} >= 10
Requires:       (grubby > 8.40-72 if grubby)
%endif
%if 0%{?fedora}
Requires:       (sdubby > 1.0-3 if sdubby)
%endif
# A backport of systemd-timesyncd is shipped as a separate package in EPEL so
# let's make sure we properly handle that.
%if 0%{?rhel}
Conflicts:      systemd-timesyncd < %{version}-%{release}
Obsoletes:      systemd-timesyncd < %{version}-%{release}
Provides:       systemd-timesyncd = %{version}-%{release}
%endif
Conflicts:      systemd-networkd < %{version}-%{release}

# Libkmod is used to load modules. Assume that if we need udevd, we certainly
# want to load modules, so make this into a hard dependency here.
Requires:       libkmod.so.2%{?elf_suffix}
Requires:       libkmod.so.2(LIBKMOD_5)%{?elf_bits}

# Recommends to replace normal Requires deps for stuff that is dlopen()ed
# used by dissect, integritysetup, veritysetyp, growfs, repart, cryptenroll, home
Recommends:     libcryptsetup.so.12%{?elf_suffix}
Recommends:     libcryptsetup.so.12(CRYPTSETUP_2.4)%{?elf_bits}

# used by systemd-coredump and systemd-analyze
Recommends:     libdw.so.1%{?elf_suffix}
Recommends:     libdw.so.1(ELFUTILS_0.186)%{?elf_bits}
Recommends:     libelf.so.1%{?elf_suffix}
Recommends:     libelf.so.1(ELFUTILS_1.7)%{?elf_bits}

# used by home, cryptsetup, cryptenroll, logind
Recommends:     libfido2.so.1%{?elf_suffix}
Recommends:     libp11-kit.so.0%{?elf_suffix}
Recommends:     libtss2-esys.so.0%{?elf_suffix}
Recommends:     libtss2-mu.so.0%{?elf_suffix}
Recommends:     libtss2-rc.so.0%{?elf_suffix}

# https://bugzilla.redhat.com/show_bug.cgi?id=1377733#c9
Suggests:       systemd-bootchart
# https://bugzilla.redhat.com/show_bug.cgi?id=1408878
Requires:       kbd

# https://bugzilla.redhat.com/show_bug.cgi?id=1753381
Provides:       u2f-hidraw-policy = 1.0.2-40
Obsoletes:      u2f-hidraw-policy < 1.0.2-40

Conflicts:      systemd-standalone-repart
Provides:       systemd-repart = %{version}-%{release}

# Newer versions of those are required to support X11 keycode remapping
Conflicts:      xorg-x11-drv-evdev < 2.11.0
Conflicts:      xorg-x11-drv-libinput < 1.5.0

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/udevadm
%endif

%description udev
This package contains systemd-udev and the rules and hardware database needed to
manage device nodes. This package is necessary on physical machines and in
virtual machines, but not in containers.

This package also provides systemd-timesyncd, a network time protocol daemon.

It also contains tools to manage encrypted home areas and secrets bound to the
machine, and to create or grow partitions and make file systems automatically.

%package ukify
Summary:        Tool to build Unified Kernel Images
Requires:       systemd = %{noarch_requires_version}

Requires:       (systemd-boot if %{shrink:(
        filesystem(x86-32) or
        filesystem(x86-64) or
        filesystem(aarch64) or
        filesystem(riscv64)
)})
Requires:       python3dist(pefile)
Requires:       python3dist(zstandard)
Requires:       python3dist(cryptography)
%if 0%{?fedora}
Recommends:     python3dist(pillow)
%endif

# for tests
%ifarch riscv64
# 2.42 received support for riscv64 + efi targets
%global binutils_version_req >= 2.42
%endif
BuildRequires:  binutils %{?binutils_version_req}

BuildArch:      noarch

%description ukify
This package provides ukify, a script that combines a kernel image, an initrd,
with a command line, and possibly PCR measurements and other metadata, into a
Unified Kernel Image (UKI).

%if 0%{?want_bootloader}
%if %{without obs}
%package boot-unsigned
Summary: UEFI boot manager (unsigned version)

Provides: systemd-boot-unsigned-%{efi_arch} = %version-%release
Provides: systemd-boot = %version-%release
Provides: systemd-boot%{_isa} = %version-%release
# A provides with just the version, no release or dist, used to build systemd-boot
Provides: version(systemd-boot-unsigned) = %version
Provides: version(systemd-boot-unsigned)%{_isa} = %version

%description boot-unsigned
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the unsigned version. Install systemd-boot instead to get
the version that works with Secure Boot.
%else
%package boot
Summary: UEFI boot manager (signed version)

Provides: systemd-boot-signed-%{efi_arch} = %version-%release
Provides: systemd-boot = %version-%release
Provides: systemd-boot%{_isa} = %version-%release
# A provides with just the version, no release or dist, used to build systemd-boot
Provides: version(systemd-boot-signed) = %version
Provides: version(systemd-boot-signed)%{_isa} = %version

%description boot
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the signed version.
%endif
%endif

%package container
# Name is the same as in Debian
Summary: Tools for containers and VMs
Requires:       systemd%{_isa} = %{version}-%{release}
Requires(post):   systemd%{_isa} = %{version}-%{release}
Requires(preun):  systemd%{_isa} = %{version}-%{release}
Requires(postun): systemd%{_isa} = %{version}-%{release}
# For systemd-vmspawn which uses qemu:
Recommends:     qemu-kvm-core
%if 0%{?fedora}
Recommends:     qemu-device-display-virtio-gpu
Recommends:     qemu-device-display-virtio-vga
%endif
# Bias the system towards libcurl-minimal if nothing pulls in full libcurl (#1997040)
Suggests:       libcurl-minimal
License:        LGPL-2.1-or-later

%description container
Systemd tools to spawn and manage containers and virtual machines.

This package contains systemd-nspawn, systemd-vmspawn, machinectl,
systemd-machined, and systemd-importd.

%package journal-remote
# Name is the same as in Debian
Summary:        Tools to send journal events over the network
Requires:       systemd%{_isa} = %{version}-%{release}
License:        LGPL-2.1-or-later
Requires:       firewalld-filesystem
Provides:       systemd-journal-gateway = %{version}-%{release}
Provides:       systemd-journal-gateway%{_isa} = %{version}-%{release}
# Bias the system towards libcurl-minimal if nothing pulls in full libcurl (#1997040)
Suggests:       libcurl-minimal

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP, and
to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd, systemd-journal-remote, and
systemd-journal-upload.

%package networkd
Summary:        System daemon that manages network configurations
Requires:       systemd%{_isa} = %{version}-%{release}
%{?fedora:Recommends:     systemd-udev = %{version}-%{release}}
Conflicts:      systemd-udev < %{version}-%{release}
License:        LGPL-2.1-or-later

%description networkd
systemd-networkd is a system service that manages networks. It detects and
configures network devices as they appear, as well as creating virtual network
devices.

%package networkd-defaults
Summary:        Configure network interfaces with networkd by default
Requires:       systemd-networkd = %{noarch_requires_version}
License:        MIT-0
BuildArch:      noarch

%description networkd-defaults
This package contains a set of config files for systemd-networkd that cause it
to configure network interfaces by default. Note that systemd-networkd needs to
enabled for this to have any effect.

%package resolved
Summary:        Network Name Resolution manager
Requires:       systemd%{_isa} = %{version}-%{release}
Requires:       libidn2.so.0%{?elf_suffix}
Requires:       libidn2.so.0(IDN2_0.0.0)%{?elf_bits}
Requires(posttrans): grep

%description resolved
systemd-resolved is a system service that provides network name resolution to
local applications. It implements a caching and validating DNS/DNSSEC stub
resolver, as well as an LLMNR and MulticastDNS resolver and responder.

%package oomd-defaults
Summary:        Configuration files for systemd-oomd
Requires:       systemd-udev = %{noarch_requires_version}
License:        LGPL-2.1-or-later
BuildArch:      noarch

%description oomd-defaults
A set of drop-in files for systemd units to enable action from systemd-oomd,
a userspace out-of-memory (OOM) killer.

%package tests
Summary:       Internal unit tests for systemd
Requires:      systemd%{_isa} = %{version}-%{release}
# This dependency is provided transitively. Also add it explicitly to
# appease rpminspect, https://github.com/rpminspect/rpminspect/issues/1231:
Requires:      systemd-libs%{_isa} = %{version}-%{release}
Requires:      python3dist(psutil)

License:       LGPL-2.1-or-later

%description tests
Systemd unit tests used to test the internal implementation after a build.
Different binaries test different parts of the codebase.

%package standalone-repart
Summary:       Standalone systemd-repart binary for use on systems without systemd
Provides:      systemd-repart = %{version}-%{release}
Conflicts:     systemd-udev
Suggests:      coreutils-single
RemovePathPostfixes: .standalone

%description standalone-repart
Standalone systemd-repart binary with no dependencies on the systemd-shared
library or other libraries from systemd-libs. This package conflicts with the
main systemd package and is meant for use on systems without systemd.

%package standalone-tmpfiles
Summary:       Standalone systemd-tmpfiles binary for use on systems without systemd
Provides:      systemd-tmpfiles = %{version}-%{release}
Conflicts:     systemd
Suggests:      coreutils-single
RemovePathPostfixes: .standalone

%description standalone-tmpfiles
Standalone systemd-tmpfiles binary with no dependencies on the systemd-shared
library or other libraries from systemd-libs. This package conflicts with the
main systemd package and is meant for use on systems without systemd.

%package standalone-sysusers
Summary:       Standalone systemd-sysusers binary for use on systems without systemd
Provides:      systemd-sysusers = %{version}-%{release}
Suggests:      coreutils-single
RemovePathPostfixes: .standalone

%description standalone-sysusers
Standalone systemd-sysusers binary with no dependencies on the systemd-shared
library or other libraries from systemd-libs. This package conflicts with the
main systemd package and is meant for use on systems without systemd.

%package standalone-shutdown
Summary:       Standalone systemd-shutdown binary for use in exitrds
Provides:      systemd-shutdown = %{version}-%{release}
Conflicts:     systemd
Suggests:      coreutils-single
RemovePathPostfixes: .standalone

%description standalone-shutdown
Standalone systemd-shutdown binary with no dependencies on the systemd-shared
library or other libraries from systemd-libs. This package conflicts with the
main systemd package and is meant for use in exitrds.

%prep
%if %{with obs}
# Recipe files in the OBS build are in a distro-specific dir, as they conflict (e.g. with SUSE ones)
mv %{_sourcedir}/%{name}.fedora/* %{_sourcedir}
%endif

%autosetup -C -p1

# Disable user lockdown until rpm implements it natively.
# https://github.com/rpm-software-management/rpm/issues/3450
sed -r -i 's/^u!/u/' sysusers.d/*.conf*

%build
%global ntpvendor %(source /etc/os-release; echo ${ID})
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

VMLINUX_H_PATH=''

%if 0%{?have_bpf}

%global find_vmlinux_h %{expand:
import functools, glob, subprocess
def cmp(a, b):
  c = subprocess.call(["rpmdev-vercmp", a, b], stdout=subprocess.DEVNULL)
  return {0:0, 11:+1, 12:-1}[c]
choices = list(glob.glob("/usr/src/kernels/*/vmlinux.h"))
assert choices
print(max(choices, key=functools.cmp_to_key(cmp)))
}

# The build fails on ppc64le with
# "GCC error "Must specify a BPF target arch via __TARGET_ARCH_xxx".
# TODO: Remove this when libbpf checks for __powerpc64__ macro.
%ifnarch ppc64le
VMLINUX_H_PATH=$(%python3 -c '%find_vmlinux_h')
%endif
%endif

CONFIGURE_OPTS=(
        -Dmode=release
        -Dslow-tests=true
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
        -Ddns-servers=
        -Dservice-watchdog=
        -Ddev-kvm-mode=0666
        -Dkmod=enabled
        -Dxkbcommon=enabled
        -Dblkid=enabled
        -Dfdisk=enabled
        -Dseccomp=enabled
        -Dima=true
        -Dselinux=enabled
        -Dbpf-framework=%[0%{?have_bpf}?"enabled":"disabled"]
        -Dvmlinux-h=%[0%{?have_bpf}?"auto":"disabled"]
        -Dvmlinux-h-path="$VMLINUX_H_PATH"
        -Dapparmor=disabled
        -Dpolkit=enabled
        -Dxz=%[%{with xz}?"enabled":"disabled"]
        -Dzlib=%[%{with zlib}?"enabled":"disabled"]
        -Dbzip2=%[%{with bzip2}?"enabled":"disabled"]
        -Dlz4=%[%{with lz4}?"enabled":"disabled"]
        -Dzstd=%[%{with zstd}?"enabled":"disabled"]
        -Dpam=enabled
        -Dacl=enabled
        -Dsmack=true
        -Dopenssl=enabled
        -Dp11kit=enabled
        -Dgcrypt=disabled
        -Daudit=enabled
        -Delfutils=enabled
        -Dlibcryptsetup=%[%{with bootstrap}?"disabled":"enabled"]
        -Delfutils=enabled
        -Drepart=enabled
        -Dpwquality=enabled
        -Dqrencode=%[%{defined rhel}?"disabled":"enabled"]
        -Dgnutls=%[%{with gnutls}?"enabled":"disabled"]
        -Dmicrohttpd=enabled
        -Dvmspawn=enabled
        -Dlibidn2=enabled
        -Dlibiptc=disabled
        -Dlibcurl=enabled
        -Dlibfido2=enabled
        -Dxenctrl=%[0%{?have_xen}?"enabled":"disabled"]
        -Defi=true
        -Dsysupdate=enabled
        -Dsysupdated=enabled
        -Dtpm=true
        -Dtpm2=enabled
        -Dhwdb=true
        -Dsysusers=true
        -Dstandalone-binaries=true
        -Ddefault-kill-user-processes=false
        -Dfirst-boot-full-preset=true
        -Ddefault-network=true
        -Dtests=unsafe
        -Dinstall-tests=true
        -Dnobody-user=nobody
        -Dnobody-group=nobody
        -Dcompat-mutable-uid-boundaries=true
        -Dsplit-bin=true
        -Db_ndebug=false
        -Dman=%[%{with docs}?"enabled":"disabled"]
        -Dversion-tag=%{version}%[%{without upstream}?"-%{release}":""]
        # https://bugzilla.redhat.com/show_bug.cgi?id=1906010
        -Dshared-lib-tag=%{version_no_tilde}%[%{without upstream}?"-%{release}":""]
        -Dlink-executor-shared=false
        -Dfallback-hostname="localhost"
        -Ddefault-dnssec=no
        -Ddefault-dns-over-tls=no
        # https://bugzilla.redhat.com/show_bug.cgi?id=1867830
        -Ddefault-mdns=no
        -Ddefault-llmnr=resolve
        # https://bugzilla.redhat.com/show_bug.cgi?id=2028169
        -Dstatus-unit-format-default=combined
%if 0%{?fedora}
        # https://fedoraproject.org/wiki/Changes/Shorter_Shutdown_Timer
        -Ddefault-timeout-sec=45
        -Ddefault-user-timeout-sec=45
%endif
        -Dconfigfiledir=/usr/lib
        -Doomd=true

        -Dadm-gid=4
        -Dtty-gid=5
        -Ddisk-gid=6
        -Dlp-gid=7
        -Dkmem-gid=9
        -Dwheel-gid=10
        -Dcdrom-gid=11
        -Ddialout-gid=18
        -Dutmp-gid=22
        -Dtape-gid=33
        -Dkvm-gid=36
        -Dvideo-gid=39
        -Daudio-gid=63
        -Dusers-gid=100
        -Dinput-gid=104
        -Drender-gid=105
        -Dsgx-gid=106
        -Dsystemd-journal-gid=190
        -Dsystemd-network-uid=192
        -Dsystemd-resolve-uid=193
        # -Dsystemd-timesync-uid=, not set yet

        # Make sure we use the original paths to maintain compatibility
        # with unmerged systems
        -Dquotaon-path=/usr/sbin/quotaon
        -Dquotacheck-path=/usr/sbin/quotacheck
        -Dkmod-path=/usr/bin/kmod
        -Dkexec-path=/usr/sbin/kexec
        -Dsulogin-path=/usr/sbin/sulogin
        -Dmount-path=/usr/bin/mount
        -Dumount-path=/usr/bin/umount
        -Dloadkeys-path=/usr/bin/loadkeys
        -Dsetfont-path=/usr/bin/setfont
        -Dnologin-path=/usr/sbin/nologin

        # For now, let's build the bootloader in the same places where we
        # built with gnu-efi. Later on, we might want to extend coverage, but
        # considering that that support is untested, let's not do this now.
        -Dbootloader=%[%{?want_bootloader}?"enabled":"disabled"]
        -Dukify=enabled
%if 0%{?want_bootloader} && %{with obs}
        -Dsbat-distro-url=https://github.com/systemd/systemd
        -Dsbat-distro=upstream
        -Dsbat-distro-summary='Upstream build from git'
%endif
)

%if %{without lto}
%global _lto_cflags %nil
%endif

{ %meson "${CONFIGURE_OPTS[@]}" %{?meson_extra_configure_options} ; }

%meson_build

# If dynamic spec generation is available, directly pick up the triggers
# from the build directory for upstream builds.
%if %{with upstream} && (0%{?fedora} >= 41 || 0%{?rhel} >= 11)
# Include the triggers
cp %{_vpath_builddir}/src/rpm/triggers.systemd.sh %{specpartsdir}/triggers.specpart
%else
new_triggers=%{_vpath_builddir}/src/rpm/triggers.systemd.sh
if ! diff -u %{SOURCE1} ${new_triggers}; then
   echo -e "\n\n\nWARNING: triggers.systemd in Source1 is different!"
   echo -e "      cp $PWD/${new_triggers} %{SOURCE1}\n\n\n"
   sleep 5
fi
%endif

sed -r 's|/system/|/user/|g' %{SOURCE16} >10-timeout-abort.conf.user

%install
%meson_install

# udev links
%if "%{_sbindir}" != "%{_bindir}"
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm
%endif

# Compatiblity and documentation files
touch %{buildroot}/etc/crypttab
chmod 600 %{buildroot}/etc/crypttab

# Config files that were moved under /usr.
# We need to %ghost them so that they are not removed on upgrades.
touch %{buildroot}/etc/systemd/coredump.conf \
      %{buildroot}/etc/systemd/homed.conf \
      %{buildroot}/etc/systemd/journald.conf \
      %{buildroot}/etc/systemd/journal-remote.conf \
      %{buildroot}/etc/systemd/journal-upload.conf \
      %{buildroot}/etc/systemd/logind.conf \
      %{buildroot}/etc/systemd/networkd.conf \
      %{buildroot}/etc/systemd/oomd.conf \
      %{buildroot}/etc/systemd/pstore.conf \
      %{buildroot}/etc/systemd/resolved.conf \
      %{buildroot}/etc/systemd/sleep.conf \
      %{buildroot}/etc/systemd/system.conf \
      %{buildroot}/etc/systemd/timesyncd.conf \
      %{buildroot}/etc/systemd/user.conf \
      %{buildroot}/etc/udev/udev.conf \
      %{buildroot}/etc/udev/iocost.conf

# /etc/initab
install -Dm0644 -t %{buildroot}/etc/ %{SOURCE6}

# /etc/sysctl.conf compat
install -Dm0644 %{SOURCE7} %{buildroot}/etc/sysctl.conf
ln -s ../sysctl.conf %{buildroot}/etc/sysctl.d/99-sysctl.conf

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{system_unit_dir}/basic.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/default.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/dbus.target.wants
mkdir -p %{buildroot}%{system_unit_dir}/syslog.target.wants
mkdir -p %{buildroot}/run
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/lastlog
chmod 0664 %{buildroot}%{_localstatedir}/log/lastlog
touch %{buildroot}/run/utmp
touch %{buildroot}%{_localstatedir}/log/{w,b}tmp

# Make sure the user generators dir exists too
mkdir -p %{buildroot}%{pkgdir}/system-generators
mkdir -p %{buildroot}%{pkgdir}/user-generators

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/localtime
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
install -d -m 0700 %{buildroot}%{_sysconfdir}/userdb

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{pkgdir}/system-shutdown/
mkdir -p %{buildroot}%{pkgdir}/system-sleep/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/backlight
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/rfkill
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/linger
mkdir -p %{buildroot}%{_localstatedir}/lib/private
mkdir -p %{buildroot}%{_localstatedir}/log/private
mkdir -p %{buildroot}%{_localstatedir}/cache/private
mkdir -p %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/timesync
ln -s ../private/systemd/journal-upload %{buildroot}%{_localstatedir}/lib/systemd/journal-upload
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed
touch %{buildroot}%{_localstatedir}/lib/systemd/timesync/clock
touch %{buildroot}%{_localstatedir}/lib/private/systemd/journal-upload/state

# Install yum protection config. Old location in /etc.
mkdir -p %{buildroot}/etc/dnf/protected.d/
cat >%{buildroot}/etc/dnf/protected.d/systemd.conf <<EOF
systemd
systemd-udev
EOF
# Install dnf5 protection config. New location under /usr.
mkdir -p %{buildroot}/usr/share/dnf5/libdnf.conf.d/
cat >%{buildroot}/usr/share/dnf5/libdnf.conf.d/protect-systemd.conf <<EOF
[main]
protected_packages = systemd, systemd-udev
EOF

install -Dm0644 -t %{buildroot}/usr/lib/firewalld/services/ %{SOURCE8} %{SOURCE9}

# Install additional docs
# https://bugzilla.redhat.com/show_bug.cgi?id=1234951
install -Dm0644 -t %{buildroot}%{_pkgdocdir}/ %{SOURCE10}

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/ %{SOURCE11}

install -Dm0644 %{SOURCE13} %{buildroot}%{_prefix}/lib/systemd/.abignore

# systemd-oomd default configuration
install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/oomd.conf.d/ %{SOURCE14}
install -Dm0644 -t %{buildroot}%{system_unit_dir}/system.slice.d/ %{SOURCE15}
install -Dm0644 -t %{buildroot}%{user_unit_dir}/slice.d/ %{SOURCE15}
%if 0%{?fedora}
# https://fedoraproject.org/wiki/Changes/Shorter_Shutdown_Timer
install -Dm0644 -t %{buildroot}%{system_unit_dir}/service.d/ %{SOURCE16}
install -Dm0644 10-timeout-abort.conf.user %{buildroot}%{user_unit_dir}/service.d/10-timeout-abort.conf
%endif

# https://fedoraproject.org/wiki/Changes/IncreaseVmMaxMapCount
install -Dm0644 -t %{buildroot}%{_prefix}/lib/sysctl.d/ %{SOURCE17}

# As requested in https://bugzilla.redhat.com/show_bug.cgi?id=1738828.
# Test results are that bfq seems to behave better and more consistently on
# typical hardware. The kernel does not have a configuration option to set the
# default scheduler, and it currently needs to be set by userspace.
install -Dm0644 -t %{buildroot}%{_prefix}/lib/udev/rules.d/ %{SOURCE18}

sed -i 's|#!/usr/bin/env python3|#!%{__python3}|' %{buildroot}/usr/lib/systemd/tests/run-unit-tests.py

%if 0%{?fedora} >= 42
install -m 0644 -D %{SOURCE21} %{buildroot}%{_rpmconfigdir}/macros.d/macros.sysusers
%else
install -m 0644 -D %{SOURCE20} %{buildroot}%{_rpmconfigdir}/macros.d/macros.sysusers
# Use rpm's own sysusers provides where available
%if ! (0%{?fedora} >= 39 || 0%{?rhel} >= 10)
install -m 0644 -D -t %{buildroot}%{_rpmconfigdir}/fileattrs/ %{SOURCE22}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE23}
%endif
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE24}
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=2107754
install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/network/ %{SOURCE25}

%if 0%{?fedora} || 0%{?rhel} >= 10
ln -s --relative %{buildroot}%{_bindir}/kernel-install %{buildroot}%{_sbindir}/installkernel
%endif

%if "%{_sbindir}" == "%{_bindir}"
# Systemd has the split-sbin option which is also used to select the directory
# for alias symlinks. We need to keep split-sbin=true for now, to support
# unmerged systems. Move the symlinks here instead.
mv -v %{buildroot}/usr/sbin/* %{buildroot}%{_bindir}/
%endif

%if 0%{?fedora} >= 41
%if %{without upstream}
# This requires https://pagure.io/setup/pull-request/50
# and https://src.fedoraproject.org/rpms/setup/pull-request/10.
# We skip this on upstream builds so that new users and groups
# can be added without breaking the build.
%if 0%{?fedora} >= 43
%{python3} %{SOURCE4} /usr/lib/sysusers.d/setup.conf %{buildroot}/usr/lib/sysusers.d/basic.conf
%else
%{python3} %{SOURCE4} /usr/lib/sysusers.d/20-setup-{users,groups}.conf %{buildroot}/usr/lib/sysusers.d/basic.conf
%endif
%endif
rm %{buildroot}/usr/lib/sysusers.d/basic.conf
%endif

# Disable sshd_config.d/20-systemd-userdb.conf for now.
# This option may override an existing AuthorizedKeysCommand setting
# (or be ineffective, depending on the order of configuration).
# See https://github.com/systemd/systemd/issues/33648.
rm %{buildroot}/etc/ssh/sshd_config.d/20-systemd-userdb.conf
mv %{buildroot}/usr/lib/tmpfiles.d/20-systemd-userdb.conf{,.example}

install -m 0644 -t %{buildroot}%{_prefix}/lib/pam.d/ %{SOURCE26}

%find_lang %{name}

# Split files in build root into rpms
python3 %{SOURCE2} %buildroot %{!?want_bootloader:--no-bootloader}

# Stage sd-boot binaries for signing
%if %{with obs} && 0%{?want_bootloader}
BRP_PESIGN_FILES=/usr/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi BRP_PESIGN_PACKAGES=systemd-boot /usr/lib/rpm/brp-suse.d/brp-99-pesign
%endif

%check
%if %{with tests}
meson test -C %{_vpath_builddir} -t 6 --print-errorlogs
%endif

%if %{with lto}
# Make sure that LTO is effective at removing unused code. When compiled
# without LTO, we end up with all of libbasic_static.a in libsystemd.so.
# For example, all the configuration stuff is not needed for libsystemd.so.
# Make sure it is gone.
(! strings %{buildroot}%{_libdir}/libsystemd.so | grep Config)
%endif

#############################################################################################

%if %{without upstream} || (0%{?fedora} < 41 && 0%{?rhel} < 11)
%include %{SOURCE1}
%endif

# This macro is newly added upstream so we can't rely on it being always being available
# in the systemd-rpm-macros yet so we define it ourselves.
%global systemd_posttrans_with_restart() \
%{expand:%%{?__systemd_someargs_%#:%%__systemd_someargs_%# systemd_posttrans_with_restart}} \
if [ $1 -ge 2 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then \
    # Package upgrade, not install \
    /usr/lib/systemd/systemd-update-helper mark-restart-system-units %* || : \
fi \
%{nil}

%post
systemd-machine-id-setup &>/dev/null || :

[ $1 -eq 1 ] || exit 0

# create /var/log/journal only on initial installation,
# and only if it's writable (it won't be in rpm-ostree).
[ -w %{_localstatedir} ] && mkdir -p %{_localstatedir}/log/journal

[ -w %{_localstatedir} ] && journalctl --update-catalog || :
systemd-sysusers || :
systemd-tmpfiles --create &>/dev/null || :

# We reset the enablement of all services upon initial installation
# https://bugzilla.redhat.com/show_bug.cgi?id=1118740#c23
# This will fix up enablement of any preset services that got installed
# before systemd due to rpm ordering problems:
# https://bugzilla.redhat.com/show_bug.cgi?id=1647172.
# We also do this for user units, see
# https://fedoraproject.org/wiki/Changes/Systemd_presets_for_user_units.
systemctl preset-all &>/dev/null || :
systemctl --global preset-all &>/dev/null || :

%posttrans
if [ $1 -ge 2 ]; then
  [ -w %{_localstatedir} ] && journalctl --update-catalog || :

  systemctl daemon-reexec || :

  systemd-tmpfiles --create &>/dev/null || :
fi

%systemd_posttrans_with_restart systemd-timedated.service systemd-hostnamed.service systemd-journald.service systemd-localed.service systemd-userdbd.service

# FIXME: systemd-logind.service is excluded (https://github.com/systemd/systemd/pull/17558)

# This is the expanded form of %%systemd_user_daemon_reexec. We
# can't use the macro because we define it ourselves.
if [ $1 -ge 2 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then
    # Package upgrade, not uninstall
    /usr/lib/systemd/systemd-update-helper user-reexec || :
fi

%triggerun -- systemd < 256
# This is for upgrades from previous versions before systemd restart was moved to %%postun
systemctl daemon-reexec || :

%triggerpostun -- systemd < 253~rc1-2
# This is for upgrades from previous versions where systemd-journald-audit.socket
# had a static enablement symlink.
# We use %%triggerpostun here because rpm doesn't allow a second %%triggerun with
# a different package version.
systemctl --no-reload preset systemd-journald-audit.socket &>/dev/null || :

%global udev_services %{shrink:
                        cryptsetup-pre.target
                        cryptsetup.target
                        hibernate.target
                        hybrid-sleep.target
                        initrd-cleanup.service
                        initrd-fs.target
                        initrd-parse-etc.service
                        initrd-root-device.target
                        initrd-root-fs.target
                        initrd-switch-root.service
                        initrd-switch-root.target
                        initrd-udevadm-cleanup-db.service
                        initrd-usr-fs.target
                        initrd.target
                        integritysetup-pre.target
                        integritysetup.target
                        kmod-static-nodes.service
                        proc-sys-fs-binfmt_misc.automount
                        proc-sys-fs-binfmt_misc.mount
                        quotaon-root.service
                        quotaon@.service
                        remote-cryptsetup.target
                        remote-veritysetup.target
                        sleep.target
                        suspend-then-hibernate.target
                        suspend.target
                        system-systemd\\x2dcryptsetup.slice
                        system-systemd\\x2dveritysetup.slice
                        systemd-backlight@.service
                        systemd-binfmt.service
                        systemd-bless-boot.service
                        systemd-bsod.service
                        systemd-coredump.socket
                        systemd-coredump@.service
                        systemd-fsck-root.service
                        systemd-fsck@.service
                        systemd-growfs-root.service
                        systemd-growfs@.service
                        systemd-hibernate-clear.service
                        systemd-hibernate-resume.service
                        systemd-hibernate.service
                        systemd-homed-activate.service
                        systemd-homed-firstboot.service
                        systemd-homed.service
                        systemd-hwdb-update.service
                        systemd-hybrid-sleep.service
                        systemd-modules-load.service
                        systemd-network-generator.service
                        systemd-oomd.service
                        systemd-oomd.socket
                        systemd-pcrextend.socket
                        systemd-pcrextend@.service
                        systemd-pcrfs-root.service
                        systemd-pcrfs@.service
                        systemd-pcrlock-file-system.service
                        systemd-pcrlock-firmware-code.service
                        systemd-pcrlock-firmware-config.service
                        systemd-pcrlock-machine-id.service
                        systemd-pcrlock-make-policy.service
                        systemd-pcrlock-secureboot-authority.service
                        systemd-pcrlock-secureboot-policy.service
                        systemd-pcrlock.socket
                        systemd-pcrlock@.service
                        systemd-pcrmachine.service
                        systemd-pcrphase-initrd.service
                        systemd-pcrphase-sysinit.service
                        systemd-pcrphase.service
                        systemd-portabled.service
                        systemd-pstore.service
                        systemd-quotacheck-root.service
                        systemd-quotacheck@.service
                        systemd-random-seed.service
                        systemd-remount-fs.service
                        systemd-repart.service
                        systemd-rfkill.service
                        systemd-rfkill.socket
                        systemd-suspend-then-hibernate.service
                        systemd-suspend.service
                        systemd-sysctl.service
                        systemd-timesyncd.service
                        systemd-tmpfiles-setup-dev-early.service
                        systemd-tmpfiles-setup-dev.service
                        systemd-udev-load-credentials.service
                        systemd-udev-settle.service
                        systemd-udev-trigger.service
                        systemd-udevd-control.socket
                        systemd-udevd-kernel.socket
                        systemd-udevd.service
                        systemd-vconsole-setup.service
                        systemd-volatile-root.service
                        veritysetup-pre.target
                        veritysetup.target
                        %{?want_bootloader:
                          systemd-boot-random-seed.service
                          systemd-boot-update.service
                          systemd-bootctl.socket
                          systemd-bootctl@.service
                         }
                       }

%post udev
# Move old stuff around in /var/lib
mv %{_localstatedir}/lib/random-seed %{_localstatedir}/lib/systemd/random-seed &>/dev/null
mv %{_localstatedir}/lib/backlight %{_localstatedir}/lib/systemd/backlight &>/dev/null
if [ -L %{_localstatedir}/lib/systemd/timesync ]; then
    rm %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/private/systemd/timesync %{_localstatedir}/lib/systemd/timesync
fi
if [ -f %{_localstatedir}/lib/systemd/clock ]; then
    mkdir -p %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/systemd/clock %{_localstatedir}/lib/systemd/timesync/.
fi

systemd-hwdb update &>/dev/null

%systemd_post %udev_services

# Try to save the random seed, but don't complain if /dev/urandom is unavailable
/usr/lib/systemd/systemd-random-seed save 2>&1 | \
    grep -v 'Failed to open /dev/urandom' || :

# Replace obsolete keymaps
# https://bugzilla.redhat.com/show_bug.cgi?id=1151958
grep -q -E '^KEYMAP="?fi-latin[19]"?' /etc/vconsole.conf 2>/dev/null &&
    sed -i.rpm.bak -r 's/^KEYMAP="?fi-latin[19]"?/KEYMAP="fi"/' /etc/vconsole.conf || :

%preun udev
%systemd_preun %udev_services

%posttrans udev
# Restart some services.
# Others are either oneshot services, or sockets, and restarting them causes issues (#1378974)
%systemd_posttrans_with_restart systemd-udevd.service systemd-timesyncd.service systemd-homed.service systemd-oomd.service systemd-portabled.service

%global journal_remote_units_restart systemd-journal-gatewayd.service systemd-journal-remote.service systemd-journal-upload.service
%global journal_remote_units_norestart systemd-journal-gatewayd.socket systemd-journal-remote.socket
%post journal-remote
%systemd_post %journal_remote_units_restart %journal_remote_units_norestart
%firewalld_reload

%preun journal-remote
%systemd_preun %journal_remote_units_restart %journal_remote_units_norestart
if [ $1 -eq 1 ] ; then
    if [ -f %{_localstatedir}/lib/systemd/journal-upload/state -a ! -L %{_localstatedir}/lib/systemd/journal-upload ] ; then
        mkdir -p %{_localstatedir}/lib/private/systemd/journal-upload
        mv %{_localstatedir}/lib/systemd/journal-upload/state %{_localstatedir}/lib/private/systemd/journal-upload/.
        rmdir %{_localstatedir}/lib/systemd/journal-upload || :
    fi
fi

%posttrans journal-remote
%systemd_posttrans_with_restart %journal_remote_units_restart
%firewalld_reload

%global networkd_services %{shrink:
                            systemd-networkd.service
                            systemd-networkd.socket
                            systemd-networkd-varlink.socket
                            systemd-networkd-wait-online.service
                            systemd-network-generator.service
                            systemd-networkd-persistent-storage.service
                           }

%post networkd
# systemd-networkd was split out in systemd-246.6-2.
# Ideally, we would have a trigger scriptlet to record enablement
# state when upgrading from systemd <= systemd-246.6-1. But, AFAICS,
# rpm doesn't allow us to trigger on another package, short of
# querying the rpm database ourselves, which seems risky. For rpm,
# systemd and systemd-networkd are completely unrelated.  So let's use
# a hack to detect if an old systemd version is currently present in
# the file system.
# https://bugzilla.redhat.com/show_bug.cgi?id=1943263
if [ $1 -eq 1 ] && ls /usr/lib/systemd/libsystemd-shared-24[0-6].so &>/dev/null; then
    echo "Skipping presets for systemd-networkd.service, seems we are upgrading from old systemd."
else
    %systemd_post %networkd_services
fi

%preun networkd
%systemd_preun %networkd_services

%posttrans networkd
%systemd_posttrans_with_restart systemd-networkd.service

%post resolved
[ $1 -eq 1 ] || exit 0
# Initial installation

touch %{_localstatedir}/lib/rpm-state/systemd-resolved.initial-installation

# Related to https://bugzilla.redhat.com/show_bug.cgi?id=1943263
if ls /usr/lib/systemd/libsystemd-shared-24[0-8].so &>/dev/null; then
    echo "Skipping presets for systemd-resolved.service, seems we are upgrading from old systemd."
    exit 0
fi

%systemd_post systemd-resolved.service

%preun resolved
%systemd_preun systemd-resolved.service
if [ $1 -eq 0 ] ; then
        if [ -L /etc/resolv.conf ] && \
            realpath /etc/resolv.conf | grep ^/run/systemd/resolve/; then
                rm -f /etc/resolv.conf # no longer useful
                # if network manager is enabled, move to it instead
                [ -f /run/NetworkManager/resolv.conf ] && \
                systemctl -q is-enabled NetworkManager.service &>/dev/null && \
                    ln -fsv ../run/NetworkManager/resolv.conf /etc/resolv.conf
        fi
fi

%posttrans resolved
%systemd_posttrans_with_restart systemd-resolved.service
[ -e %{_localstatedir}/lib/rpm-state/systemd-resolved.initial-installation ] || exit 0
rm %{_localstatedir}/lib/rpm-state/systemd-resolved.initial-installation
# Initial installation

# Create /etc/resolv.conf symlink.
# (https://bugzilla.redhat.com/show_bug.cgi?id=1873856)
#
# We would also create it using tmpfiles, but let's do this here too
# before NetworkManager gets a chance. (systemd-tmpfiles invocation
# above does not do this, because the line is marked with ! and
# tmpfiles is invoked without --boot in the scriptlet.)
#
# *Create* the symlink if nothing is present yet.
# (https://bugzilla.redhat.com/show_bug.cgi?id=2032085)
#
# *Override* the symlink if systemd is running. Don't do it if systemd
# is not running, because that will immediately break DNS resolution,
# since systemd-resolved is also not running
# (https://bugzilla.redhat.com/show_bug.cgi?id=1891847).
#
# Also don't create the symlink to the stub when the stub is disabled (#1891847 again).
if systemctl -q is-enabled systemd-resolved.service &>/dev/null &&
   ! systemd-analyze cat-config systemd/resolved.conf 2>/dev/null |
        grep -iqE '^DNSStubListener\s*=\s*(no?|false|0|off)\s*$'; then

  if ! test -e /etc/resolv.conf && ! test -L /etc/resolv.conf; then
    ln -sv ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf || :
  elif test -d /run/systemd/system/ &&
     ! mountpoint /etc/resolv.conf &>/dev/null; then
    ln -fsv ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf || :
  fi
fi

%global _docdir_fmt %{name}

%files -f %{name}.lang -f .file-list-main
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/LICENSE*
# Only the licenses texts for the licenses in License line are included.
%license LICENSE.GPL2
%license LICENSES/MIT.txt
%ghost %dir %attr(0755,-,-) /etc/systemd/system/basic.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/bluetooth.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/default.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/getty.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/graphical.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/local-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/machines.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/multi-user.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/network-online.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/printer.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/remote-fs.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sockets.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/sysinit.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/system-update.target.wants
%ghost %dir %attr(0755,-,-) /etc/systemd/system/timers.target.wants
%ghost %dir %attr(0700,-,-) /var/lib/portables
%ghost %dir %attr(0755,-,-) /var/lib/rpm-state/systemd

%files libs -f .file-list-libs
%license LICENSE.LGPL2.1

%files shared -f .file-list-shared
%license LICENSE.LGPL2.1
%license LICENSES/MIT.txt

%files pam -f .file-list-pam

%files rpm-macros -f .file-list-rpm-macros

%files sysusers -f .file-list-sysusers

%files resolved -f .file-list-resolve

%files devel -f .file-list-devel

%files udev -f .file-list-udev

%files ukify -f .file-list-ukify
%if 0%{?want_bootloader}
%if %{without obs}
%files boot-unsigned -f .file-list-boot
%else
%files boot -f .file-list-boot
%endif
%endif

%files container -f .file-list-container
%ghost %dir %attr(0700,-,-) /var/lib/machines

%files journal-remote -f .file-list-remote

%files networkd -f .file-list-networkd

%files networkd-defaults -f .file-list-networkd-defaults

%files oomd-defaults -f .file-list-oomd-defaults

%files tests -f .file-list-tests

%files standalone-repart -f .file-list-standalone-repart

%files standalone-tmpfiles -f .file-list-standalone-tmpfiles

%files standalone-sysusers -f .file-list-standalone-sysusers

%files standalone-shutdown -f .file-list-standalone-shutdown

%clean
rm -rf \
    $RPM_BUILD_ROOT \
    10-timeout-abort.conf.user \
    .file-list-* \
    %{name}.lang \
    debugfiles.list \
    debuglinks.list \
    debugsourcefiles.list \
    debugsources.list \
    elfbins.list

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 258.4-2
- Latest state for systemd

* Sat Feb 07 2026 Zbigniew Jędrzejewski-Szmek <zbyszek@amutable.com> - 258.4-1
- Version 258.4

* Mon Jan 05 2026 Andreas Schneider <asn@redhat.com> - 258.3-3
- userdb: Omit empty parameters field in JSON messages

* Wed Dec 17 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.3-2
- Add patches for ssh-generator vsock issue

* Sat Dec 13 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.3-1
- Version 258.3
- 148 patches, for all kinds of small issues.
- Includes a hwdb update.

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.2-1
- Version 258.2
- A bunch of fixes in many components.
- Stop creating user namespace for system services (rhbz#2391343)
- Systemd trigger scriptlets are updated

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-12
- Restore runlevelX.target units (rhbz#2411195)

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-11
- Use %%autosetup -C

* Mon Nov 10 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 258.1-10
- Remove hack to stop systemd-networkd-resolve-hook.socket

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-9
- Automatically figure out the name of the top-level tar dir

* Mon Nov 10 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 258.1-8
- Make sure fallback source is listed first

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-7
- Enable sysupdate and sysupdated

* Mon Nov 10 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 258.1-6
- Add missing networkd socket units

* Mon Nov 10 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 258.1-5
- Drop backwards compat logic from integration tests script

* Mon Nov 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-4
- Require systemd-rpm-macros for build

* Mon Nov 10 2025 Lukáš Zaoral <lzaoral@redhat.com> - 258.1-3
- Require python3-zstandard in ELN

* Wed Oct 15 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-2
- Require systemd-libs and systemd-shared to be in the same version
  (rhbz#2404143)

* Mon Oct 13 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258.1-1
- Version 258.1
- This is the first (large) batch of fixes after v258:
- fixes for boot loader and early boot code
- fixes for systemd itself, systemd-udevd, systemd-logind, systemd-
  machined, and library code
- unprivileged operation in systemd-machined is disabled for now
- lots of documentation and shell-completion fixes
- includes an hwdb update

* Sat Sep 27 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258-2
- Require systemd-networkd and systemd-udev to be in the same version
  (rhbz#2397579)

* Wed Sep 17 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258-1
- Version 258 💝
- See https://raw.githubusercontent.com/systemd/systemd/v258/NEWS for the
  final list of changes.

* Fri Sep 12 2025 Andreas Schneider <asn@redhat.com> - 258~rc4-2
- Pre-create /etc/userdb directory

* Fri Sep 05 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc4-1
- Version 258~rc4

* Thu Sep 04 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc3-4
- Add to patch to create userdb root directory with correct label

* Wed Sep 03 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc3-3
- Fix unit name in scriptlet

* Tue Aug 26 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc3-2
- Add workaround patch to hopefully pass podman CI tests

* Wed Aug 20 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc3-1
- Version 258~rc3
- A large number of fixes in various components
- Hardware database and syscall numbers are updated

* Wed Aug 06 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc2-1
- Version 258~rc2

* Wed Jul 23 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 258~rc1-1
- Version 258~rc1
- See https://raw.githubusercontent.com/systemd/systemd/v258-rc1/NEWS. Too
  many changes to list or discuss here.

* Tue Jul 08 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.7-3
- Add "test" that LTO effectively removes unused code from shared lib

* Sat Jul 05 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.7-2
- Build docs on 64-bit architectures only

* Thu Jun 26 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.7-1
- Version 257.7
- Fixes for systemd itself, systemd-repart, systemd-resolved, systemd-
  vmspawn, systemd-networkd, resolvectl, bootctl, the shared library code,
  man pages, shell completions, and tests.
- Hardware database is updated.

* Thu Jun 05 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.6-3
- Do not mark symlinks as %%ghost

* Wed Jun 04 2025 Matteo Croce <teknoraver@meta.com> - 257.6-2
- Let systemd-{sysusers,shared} conflict with older systemd

* Thu May 29 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.6-1
- Version 257.6
- Fix for local information disclosure in systemd-coredump (CVE-2025-4598)
- Fixes for systemd itself, run0, systemd-networkd, "secure" pager, man
  pages, shell completions, sd-boot, sd-varlink
- Hardware database update

* Tue May 20 2025 David Tardon <dtardon@redhat.com> - 257.5-6
- Package pcrlock files together with systemd-pcrlock (rhbz#2366948)

* Thu May 08 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.5-5
- Move mount.ddi symlinks to -container subpackage

* Fri May 02 2025 LuK1337 <priv.luk@gmail.com> - 257.5-4
- Revert "Disable freezing of user sessions"

* Thu Apr 17 2025 LuK1337 <priv.luk@gmail.com> - 257.5-3
- Backport adb/fastboot udev rules (BZ#2356537)

* Thu Apr 10 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.5-2
- Backport CI fix

* Wed Apr 09 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.5-1
- Version 257.5
- A lot of small fixes in various components

* Thu Apr 03 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-19
- fmf: Check out mkosi to some directory in /var/tmp

* Thu Apr 03 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-17
- fmf: Use mkosi/mkosi.local.conf if the mkosi/ directory exists

* Tue Mar 25 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-15
- Relax dependencies from noarch packages on archful packages for OBS
  builds

* Sun Mar 23 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-14
- Remove purge-nobody-user script

* Sun Mar 23 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.4-13
- Add more services to %%post for udev and networkd

* Sun Mar 23 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 257.4-12
- Fix paths for /usr/sbin/nologin and related progs

* Fri Mar 21 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-11
- Make the source tarball glob in the test script more generic

* Fri Mar 21 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-10
- Support specifying extra mkosi repositories to the test script

* Fri Mar 21 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-9
- Use old setup sysusers files on Fedora < 43

* Fri Mar 21 2025 Daan De Meyer <daan.j.demeyer@gmail.com> - 257.4-8
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
