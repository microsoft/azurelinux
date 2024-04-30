
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

%bcond bzip2  1
%bcond gnutls 0
%bcond lz4    1
%bcond xz     1
%bcond zlib   1
%bcond zstd   1

# Bootstrap may be needed to break circular dependencies with cryptsetup,
# e.g. when re-building cryptsetup on a json-c SONAME-bump.
%bcond bootstrap 0
%bcond tests     1
%bcond lto       1

# Support for quick builds with rpmbuild --build-in-place.
# See README.build-in-place.
%bcond inplace 0

# Custom settings for Azure Linux
#  We don't need to support FIDO hardware for cryptenroll/cryptsetup
%bcond libfido2 0
#  This is needed only to include a splash image when building a UKI with ukify
%bcond pillow 0
#  We don't need to generate any QR codes
%bcond qrencode 0
#  This is only used for udev tracing
%bcond systemtap 0
#  We don't need to support Xen
%bcond xen 0

Name:           systemd
Url:            https://systemd.io
%if %{without inplace}
Version:        255
%else
# determine the build information from local checkout
Version:        %(tools/meson-vcs-tag.sh . error | sed -r 's/-([0-9])/.^\1/; s/-g/_g/')
%endif
Release:        12%{?dist}

# FIXME - hardcode to 'stable' for now as that's what we have in our blobstore
%global stable 1
# %%global stable %%(c="%%version"; [ "$c" = "${c#*.*}" ]; echo $?)

# For a breakdown of the licensing, see README
License:        LGPL-2.1-or-later AND MIT AND GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        System and Service Manager

%if %{undefined version_no_tilde}
# This is defined in 'macros.rust-srpm' which we may not have installed.
# However, we don't plan on using any RC releases, so we should be able to just define it directly to the version.
%define version_no_tilde %version
%endif

# download tarballs with "spectool -g systemd.spec"
%if %{defined commit}
Source0:        https://github.com/systemd/systemd%{?stable:-stable}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
%if 0%{?stable}
Source0:        https://github.com/systemd/systemd-stable/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz
%else
Source0:        https://github.com/systemd/systemd/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz
%endif
%endif
# This file must be available before %%prep.
# It is generated during systemd build and can be found in build/src/core/.
Source1:        triggers.systemd
Source2:        split-files.py

# Prevent accidental removal of the systemd package
Source4:        yum-protect-systemd.conf

Source6:        sysctl.conf.README
Source7:        systemd-journal-remote.xml
Source8:        systemd-journal-gatewayd.xml
Source9:        20-yama-ptrace.conf
Source10:       systemd-udev-trigger-no-reload.conf

Source14:       10-oomd-defaults.conf
Source15:       10-oomd-per-slice-defaults.conf
Source16:       10-timeout-abort.conf
Source17:       10-map-count.conf

Source21:       macros.sysusers
Source22:       sysusers.attr
Source23:       sysusers.prov
Source24:       sysusers.generate-pre.sh

Source25:       98-default-mac-none.link

%if 0
GIT_DIR=../../src/systemd/.git git format-patch-ab --no-signature -M -N v235..v235-stable
i=1; for j in 00*patch; do printf "Patch%04d:      %s\n" $i $j; i=$((i+1));done|xclip
GIT_DIR=../../src/systemd/.git git diffab -M v233..master@{2017-06-15} -- hwdb/[67]* hwdb/parse_hwdb.py >hwdb.patch
%endif

# Backports of patches from upstream (0000–0499)
#
# Any patches which are "in preparation" upstream should be listed here, rather
# than in the next section. Packit CI will drop any patches in this range before
# applying upstream pull requests.

# Work-around for dracut issue: run generators directly when we are in initrd
# https://bugzilla.redhat.com/show_bug.cgi?id=2164404
# Drop when dracut-060 is available.
Patch0001:      https://github.com/systemd/systemd/pull/26494.patch


# Those are downstream-only patches, but we don't want them in packit builds:
# https://bugzilla.redhat.com/show_bug.cgi?id=1738828
Patch0490:      use-bfq-scheduler.patch

# Adjust upstream config to use our shared stack
# NOTE: the patch was based on the fedora patch, but renamed to
# 'azurelinux-...' and modified for our 'system-*' pam files
Patch0491:      azurelinux-use-system-auth-in-pam-systemd-user.patch

# Patches for Azure Linux
Patch0900:      do-not-test-openssl-sm3.patch
Patch0901:      networkd-default-use-domains.patch

%ifarch %{ix86} x86_64 aarch64
%global want_bootloader 1
%endif

# additional BuildRequires for Azure Linux
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig(libcrypt)
BuildRequires:  p11-kit-devel
BuildRequires:  polkit-devel
# This is required for /etc/os-release, as the systemd uses this during src/boot/efi build
BuildRequires:  azurelinux-release
# This is required because...toolkit
BuildRequires:  systemd-bootstrap-rpm-macros

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  coreutils
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  pkgconfig(fdisk)
BuildRequires:  libpwquality-devel
BuildRequires:  pam-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-libs-devel
%if %{without bootstrap}
BuildRequires:  cryptsetup-devel
%endif
BuildRequires:  dbus-devel
BuildRequires:  /sbin/sfdisk
# /usr/bin/getfacl is needed by test-acl-util
BuildRequires:  /usr/bin/getfacl
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
%if %{with gnutls}
BuildRequires:  gnutls-devel
%endif
%if %{with qrencode}
BuildRequires:  qrencode-devel
%endif
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
%if %{with libfido2}
BuildRequires:  pkgconfig(libfido2)
%endif
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(tss2-rc)
BuildRequires:  pkgconfig(tss2-mu)
BuildRequires:  pkgconfig(libbpf)
%if %{with systemtap}
# This is required for udev tracing
BuildRequires:  systemtap-sdt-devel
%endif
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
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
%if %{with pillow}
BuildRequires:  python3dist(pillow)
%endif
BuildRequires:  python3dist(pytest-flakes)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(zstd)
%if 0%{?want_bootloader}
BuildRequires:  python3dist(pyelftools)
%endif
# gzip and lzma are provided by the stdlib
BuildRequires:  firewalld-filesystem
BuildRequires:  libseccomp-devel
BuildRequires:  meson >= 0.43
BuildRequires:  gettext
# We use RUNNING_ON_VALGRIND in tests, so the headers need to be available
BuildRequires:  valgrind-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  perl
BuildRequires:  perl(IPC::SysV)

%ifnarch %ix86
# bpftool is not built for i368
BuildRequires:  bpftool
%global have_bpf 1
%endif

%if %{with xen}
%ifarch x86_64 aarch64
%global have_xen 1
# That package is only built for those two architectures
BuildRequires:  xen-devel
%endif
%endif

Requires(post): coreutils
Requires(post): grep
# systemd-machine-id-setup requires libssl
Requires(post): openssl-libs
Requires:       dbus >= 1.9.18
Requires:       %{name}-pam%{_isa} = %{version}-%{release}
# FIXME - our toolkit can't handle logical deps like this
#Requires(meta): (%%{name}-rpm-macros = %%{version}-%%{release} if rpm-build)
Requires(meta): %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Recommends:     %{name}-networkd = %{version}-%{release}
Recommends:     %{name}-resolved = %{version}-%{release}
Recommends:     diffutils
# FIXME - our toolkit can't handle logical deps like this
#Requires:       (util-linux-core or util-linux)
Requires:       util-linux
Recommends:     libxkbcommon%{_isa}
Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       syslog
Provides:       systemd-units = %{version}-%{release}
Obsoletes:      systemd-bootstrap <= %{version}-%{release}
Obsoletes:      system-setup-keyboard < 0.9
Provides:       system-setup-keyboard = 0.9
# systemd-sysv-convert was removed in f20: https://fedorahosted.org/fpc/ticket/308
Obsoletes:      systemd-sysv < 206
# self-obsoletes so that dnf will install new subpackages on upgrade (#1260394)
Obsoletes:      %{name} < 249~~
Provides:       systemd-sysv = 206
Conflicts:      initscripts < 9.56.1
%if 0%{?fedora}
Conflicts:      fedora-release < 23-0.12
%endif
# Make sure that dracut supports systemd-executor and the renames done for v255
Conflicts:      dracut < 059

Obsoletes:      timedatex < 0.6-3
Provides:       timedatex = 0.6-3
Conflicts:      %{name}-standalone-repart < %{version}-%{release}^
Provides:       %{name}-repart = %{version}-%{release}
Conflicts:      %{name}-standalone-tmpfiles < %{version}-%{release}^
Provides:       %{name}-tmpfiles = %{version}-%{release}
Conflicts:      %{name}-standalone-sysusers < %{version}-%{release}^
Provides:       %{name}-sysusers = %{version}-%{release}
Conflicts:      %{name}-standalone-shutdown < %{version}-%{release}^
Provides:       %{name}-shutdown = %{version}-%{release}

# Recommends to replace normal Requires deps for stuff that is dlopen()ed
Recommends:     libpcre2-8.so.0%{?elf_suffix}
Recommends:     libpwquality.so.1%{?elf_suffix}
Recommends:     libpwquality.so.1(LIBPWQUALITY_1.0)%{?elf_bits}
%if %{with qrencode}
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
Obsoletes:      libudev < 183
Obsoletes:      systemd < 185-4
Conflicts:      systemd < 185-4
Obsoletes:      systemd-compat-libs < 230
Obsoletes:      nss-myhostname < 0.4
Provides:       nss-myhostname = 0.4
Provides:       nss-myhostname%{_isa} = 0.4
Obsoletes:      systemd-bootstrap-libs <= %{version}-%{release}

%description libs
Libraries for systemd and udev.

%package pam
Summary:        systemd PAM module
Requires:       %{name} = %{version}-%{release}

%description pam
Systemd PAM module registers the session with systemd-logind.

%package rpm-macros
Summary:        Macros that define paths and scriptlets related to systemd
BuildArch:      noarch
Obsoletes:      systemd-bootstrap-rpm-macros <= %{version}-%{release}

%description rpm-macros
Just the definitions of rpm macros.

See
https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd
for information how to use those macros.

%package devel
Summary:        Development headers for systemd
License:        LGPL-2.1-or-later AND MIT
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
# FIXME - our toolkit can't handle logical deps like this
#Requires(meta): (%%{name}-rpm-macros = %%{version}-%%{release} if rpm-build)
Requires(meta): %{name}-rpm-macros = %{version}-%{release}
Provides:       libudev-devel = %{version}
Provides:       libudev-devel%{_isa} = %{version}
Obsoletes:      libudev-devel < 183
Obsoletes:      systemd-bootstrap-devel <= %{version}-%{release}

%description devel
Development headers and auxiliary files for developing applications linking
to libudev or libsystemd.

%package udev
Summary: Rule-based device node and kernel event manager
License:        LGPL-2.1-or-later

Requires:       systemd%{_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post): grep
Requires:       kmod >= 18-4
# https://bodhi.fedoraproject.org/updates/FEDORA-2020-dd43dd05b1
Obsoletes:      systemd < 245.6-1
Provides:       udev = %{version}
Provides:       udev%{_isa} = %{version}
Obsoletes:      udev < 183
# FIXME - our toolkit can't handle logical deps like this
#Requires:       (grubby > 8.40-72 if grubby)
#Requires:       (sdubby > 1.0-3 if sdubby)

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
%if %{with libfido2}
Recommends:     libfido2.so.1%{?elf_suffix}
%endif
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

# self-obsoletes to install both packages after split of systemd-boot
Obsoletes:      systemd-udev < 252.2^

%description udev
This package contains systemd-udev and the rules and hardware database needed to
manage device nodes. This package is necessary on physical machines and in
virtual machines, but not in containers.

This package also provides systemd-timesyncd, a network time protocol daemon.

It also contains tools to manage encrypted home areas and secrets bound to the
machine, and to create or grow partitions and make file systems automatically.

%if 0%{?want_bootloader}
%package ukify
Summary:        Tool to build Unified Kernel Images
Requires:       %{name} = %{version}-%{release}

Requires:       python3dist(pefile)
Requires:       python3dist(zstd)
Requires:       python3dist(cryptography)
%if %{with pillow}
Recommends:     python3dist(pillow)
%endif

BuildArch:      noarch

%description ukify
This package provides ukify, a script that combines a kernel image, an initrd,
with a command line, and possibly PCR measurements and other metadata, into a
Unified Kernel Image (UKI).

%package boot-unsigned
Summary: UEFI boot manager (unsigned version)

Provides: systemd-boot-unsigned-%{efi_arch} = %version-%release
Provides: systemd-boot = %version-%release
Provides: systemd-boot%{_isa} = %version-%release
# A provides with just the version, no release or dist, used to build systemd-boot
Provides: version(systemd-boot-unsigned) = %version
Provides: version(systemd-boot-unsigned)%{_isa} = %version

# self-obsoletes to install both packages after split of systemd-boot
Obsoletes:      systemd-udev < 252.2^

%description boot-unsigned
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the unsigned version. Install systemd-boot instead to get
the version that works with Secure Boot.
%endif

%package container
# Name is the same as in Debian
Summary: Tools for containers and VMs
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
# obsolete parent package so that dnf will install new subpackage on upgrade (#1260394)
Obsoletes:      %{name} < 229-5
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
Requires:       %{name}%{_isa} = %{version}-%{release}
License:        LGPL-2.1-or-later
Requires:       firewalld-filesystem
Provides:       %{name}-journal-gateway = %{version}-%{release}
Provides:       %{name}-journal-gateway%{_isa} = %{version}-%{release}
Obsoletes:      %{name}-journal-gateway < 227-7
# Bias the system towards libcurl-minimal if nothing pulls in full libcurl (#1997040)
Suggests:       libcurl-minimal

%description journal-remote
Programs to forward journal entries over the network, using encrypted HTTP, and
to write journal files from serialized journal contents.

This package contains systemd-journal-gatewayd, systemd-journal-remote, and
systemd-journal-upload.

%package networkd
Summary:        System daemon that manages network configurations
Requires:       %{name}%{_isa} = %{version}-%{release}
License:        LGPL-2.1-or-later
# https://src.fedoraproject.org/rpms/systemd/pull-request/34
Obsoletes:      systemd < 246.6-2
Recommends:     libidn2.so.0%{?elf_suffix}
Recommends:     libidn2.so.0(IDN2_0.0.0)%{?elf_bits}

%description networkd
systemd-networkd is a system service that manages networks. It detects and
configures network devices as they appear, as well as creating virtual network
devices.

%package networkd-defaults
Summary:        Configure network interfaces with networkd by default
Requires:       %{name}-networkd = %{version}-%{release}
License:        MIT-0
BuildArch:      noarch

%description networkd-defaults
This package contains a set of config files for systemd-networkd that cause it
to configure network interfaces by default. Note that systemd-networkd needs to
enabled for this to have any effect.

%package resolved
Summary:        Network Name Resolution manager
Requires:       %{name}%{_isa} = %{version}-%{release}
Obsoletes:      %{name} < 249~~
Requires:       libidn2.so.0%{?elf_suffix}
Requires:       libidn2.so.0(IDN2_0.0.0)%{?elf_bits}
Requires(posttrans): grep

%description resolved
systemd-resolved is a system service that provides network name resolution to
local applications. It implements a caching and validating DNS/DNSSEC stub
resolver, as well as an LLMNR and MulticastDNS resolver and responder.

%package oomd-defaults
Summary:        Configuration files for systemd-oomd
Requires:       %{name}-udev = %{version}-%{release}
License:        LGPL-2.1-or-later
BuildArch:      noarch

%description oomd-defaults
A set of drop-in files for systemd units to enable action from systemd-oomd,
a userspace out-of-memory (OOM) killer.

%package tests
Summary:       Internal unit tests for systemd
Requires:      %{name}%{_isa} = %{version}-%{release}
# This dependency is provided transitively. Also add it explicitly to
# appease rpminspect, https://github.com/rpminspect/rpminspect/issues/1231:
Requires:      %{name}-libs%{_isa} = %{version}-%{release}

License:       LGPL-2.1-or-later

%description tests
"Installed tests" that are usually run as part of the build system. They can be
useful to test systemd internals.

%package standalone-repart
Summary:       Standalone systemd-repart binary for use on systems without systemd
Provides:      %{name}-repart = %{version}-%{release}
RemovePathPostfixes: .standalone

%description standalone-repart
Standalone systemd-repart binary with no dependencies on the systemd-shared library or
other libraries from systemd-libs. This package conflicts with the main systemd
package and is meant for use on systems without systemd.

%package standalone-tmpfiles
Summary:       Standalone systemd-tmpfiles binary for use on systems without systemd
Provides:      %{name}-tmpfiles = %{version}-%{release}
RemovePathPostfixes: .standalone

%description standalone-tmpfiles
Standalone systemd-tmpfiles binary with no dependencies on the systemd-shared library or
other libraries from systemd-libs. This package conflicts with the main systemd
package and is meant for use on systems without systemd.

%package standalone-sysusers
Summary:       Standalone systemd-sysusers binary for use on systems without systemd
Provides:      %{name}-sysusers = %{version}-%{release}
RemovePathPostfixes: .standalone

%description standalone-sysusers
Standalone systemd-sysusers binary with no dependencies on the systemd-shared library or
other libraries from systemd-libs. This package conflicts with the main systemd
package and is meant for use on systems without systemd.

%package standalone-shutdown
Summary:       Standalone systemd-shutdown binary for use on systems without systemd
Provides:      %{name}-shutdown = %{version}-%{release}
RemovePathPostfixes: .standalone

%description standalone-shutdown
Standalone systemd-shutdown binary with no dependencies on the systemd-shared library or
other libraries from systemd-libs. This package conflicts with the main systemd
package and is meant for use in exitrds.

%prep
%autosetup -n %{?commit:%{name}%[%stable?"-stable":""]-%{commit}}%{!?commit:%{name}%[%stable?"-stable":""]-%{version_no_tilde}} -p1

%build

CONFIGURE_OPTS=(
        -Dmode=release
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers=
        -Ddns-servers=
        -Duser-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
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
        -Dcryptolib=openssl
        -Dp11kit=enabled
        -Dgcrypt=disabled
        -Daudit=enabled
        -Delfutils=enabled
        -Dlibcryptsetup=%[%{with bootstrap}?"disabled":"enabled"]
        -Delfutils=enabled
        -Dpwquality=enabled
        -Dqrencode=%[%{with qrencode}?"enabled":"disabled"]
        -Dgnutls=%[%{with gnutls}?"enabled":"disabled"]
        -Dmicrohttpd=enabled
        -Dvmspawn=enabled
        -Dlibidn2=enabled
        -Dlibiptc=disabled
        -Dlibcurl=enabled
        -Dlibfido2=%[%{with libfido2}?"enabled":"disabled"]
        -Dxenctrl=%[0%{?have_xen}?"enabled":"disabled"]
        -Defi=true
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
        -Dtty-gid=5
        -Dusers-gid=100
        -Dnobody-user=nobody
        -Dnobody-group=nobody
        -Dcompat-mutable-uid-boundaries=true
        -Dsplit-bin=true
        -Db_lto=%[%{with lto}?"true":"false"]
        -Db_ndebug=false
        -Dman=enabled
        -Dversion-tag=%{version}-%{release}
        # https://bugzilla.redhat.com/show_bug.cgi?id=1906010
        -Dshared-lib-tag=%{version_no_tilde}-%{release}
        -Dfallback-hostname="localhost"
        -Ddefault-dnssec=no
        -Ddefault-dns-over-tls=no
        # https://bugzilla.redhat.com/show_bug.cgi?id=1867830
        -Ddefault-mdns=no
        -Ddefault-llmnr=resolve
        # https://bugzilla.redhat.com/show_bug.cgi?id=2028169
        -Dstatus-unit-format-default=combined
        # https://fedoraproject.org/wiki/Changes/Shorter_Shutdown_Timer
        -Ddefault-timeout-sec=45
        -Ddefault-user-timeout-sec=45
        -Doomd=true
        -Dadm-gid=4
        -Daudio-gid=63
        -Dcdrom-gid=11
        -Ddialout-gid=18
        -Ddisk-gid=6
        -Dinput-gid=104
        -Dkmem-gid=9
        -Dkvm-gid=36
        -Dlp-gid=7
        -Drender-gid=105
        -Dsgx-gid=106
        -Dtape-gid=33
        -Dtty-gid=5
        -Dusers-gid=100
        -Dutmp-gid=22
        -Dvideo-gid=39
        -Dwheel-gid=10
        -Dsystemd-journal-gid=190
        -Dsystemd-network-uid=192
        -Dsystemd-resolve-uid=193
        # -Dsystemd-timesync-uid=, not set yet

        # For now, let's build the bootloader in the same places where we
        # built with gnu-efi. Later on, we might want to extend coverage, but
        # considering that that support is untested, let's not do this now.
        # Note, ukify requires bootloader, let's also explicitly enable/disable it
        # here for https://github.com/systemd/systemd/pull/24175.
        -Dbootloader=%[%{?want_bootloader}?"enabled":"disabled"]
        -Dukify=%[%{?want_bootloader}?"enabled":"disabled"]
)

%if %{without lto}
%global _lto_cflags %nil
%endif

# Do configuration. If doing an inplace build, try to do
# reconfiguration to pick up new options.
%if %{with inplace}
  command -v ccache 2>/dev/null && { CC="${CC:-ccache %__cc}"; CXX="${CXX:-ccache %__cxx}"; }

  [ -e %{_vpath_builddir}/build.ninja ] &&
  %__meson configure %{_vpath_builddir} "${CONFIGURE_OPTS[@]}" ||
%endif
{ %meson "${CONFIGURE_OPTS[@]}"; }

%meson_build

new_triggers=%{_vpath_builddir}/src/rpm/triggers.systemd.sh
if ! diff -u %{SOURCE1} ${new_triggers}; then
   echo -e "\n\n\nWARNING: triggers.systemd in Source1 is different!"
   echo -e "      cp $PWD/${new_triggers} %{SOURCE1}\n\n\n"
   sleep 5
fi

sed -r 's|/system/|/user/|g' %{SOURCE16} >10-timeout-abort.conf.user

%install
%meson_install

# udev links
mkdir -p %{buildroot}/%{_sbindir}
ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Compatiblity and documentation files
touch %{buildroot}/etc/crypttab
chmod 600 %{buildroot}/etc/crypttab

# /etc/sysctl.conf compat
install -Dm0644 %{SOURCE6} %{buildroot}/etc/sysctl.conf
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

# Install yum protection fragment
install -Dm0644 %{SOURCE4} %{buildroot}/etc/dnf/protected.d/systemd.conf

install -Dm0644 -t %{buildroot}/usr/lib/firewalld/services/ %{SOURCE7} %{SOURCE8}

# Install additional docs
# https://bugzilla.redhat.com/show_bug.cgi?id=1234951
install -Dm0644 -t %{buildroot}%{_pkgdocdir}/ %{SOURCE9}

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{system_unit_dir}/systemd-udev-trigger.service.d/ %{SOURCE10}

# systemd-oomd default configuration
install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/oomd.conf.d/ %{SOURCE14}
install -Dm0644 -t %{buildroot}%{system_unit_dir}/system.slice.d/ %{SOURCE15}
install -Dm0644 -t %{buildroot}%{user_unit_dir}/slice.d/ %{SOURCE15}
# https://fedoraproject.org/wiki/Changes/Shorter_Shutdown_Timer
install -Dm0644 -t %{buildroot}%{system_unit_dir}/service.d/ %{SOURCE16}
install -Dm0644 10-timeout-abort.conf.user %{buildroot}%{user_unit_dir}/service.d/10-timeout-abort.conf

# https://fedoraproject.org/wiki/Changes/IncreaseVmMaxMapCount
install -Dm0644 -t %{buildroot}%{_prefix}/lib/sysctl.d/ %{SOURCE17}

sed -i 's|#!/usr/bin/env python3|#!%{__python3}|' %{buildroot}/usr/lib/systemd/tests/run-unit-tests.py

install -m 0644 -D -t %{buildroot}%{_rpmconfigdir}/macros.d/ %{SOURCE21}
install -m 0644 -D -t %{buildroot}%{_rpmconfigdir}/fileattrs/ %{SOURCE22}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE23}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE24}

# https://bugzilla.redhat.com/show_bug.cgi?id=2107754
install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/network/ %{SOURCE25}

ln -s --relative %{buildroot}%{_bindir}/kernel-install %{buildroot}%{_sbindir}/installkernel

%find_lang %{name}

# Split files in build root into rpms
python3 %{SOURCE2} %buildroot %{!?want_bootloader:--no-bootloader}

%check
%if %{with tests}
meson test -C %{_vpath_builddir} -t 6 --print-errorlogs
%endif

#############################################################################################

%include %{SOURCE1}

%post
systemd-machine-id-setup &>/dev/null || :

# FIXME: move to %postun. We want to restart systemd *after* removing
# files from the old rpm. Right now we may still have bits the old
# setup if the files are not present in the new version. But before
# implement restarting of *other* services after the transaction, moving
# this would make things worse, increasing the number of warnings we get
# about needed daemon-reload.

systemctl daemon-reexec &>/dev/null || {
  # systemd v239 had bug #9553 in D-Bus authentication of the private socket,
  # which was later fixed in v240 by #9625.
  #
  # The end result is that a `systemctl daemon-reexec` call as root will fail
  # when upgrading from systemd v239, which means the system will not start
  # running the new version of systemd after this post install script runs.
  #
  # To work around this issue, let's fall back to using a `kill -TERM 1` to
  # re-execute the daemon when the `systemctl daemon-reexec` call fails.
  #
  # In order to prevent issues when the reason why the daemon-reexec failed is
  # not the aforementioned bug, let's only use this fallback when:
  #   - we're upgrading this RPM package; and
  #   - we confirm that systemd is running as PID1 on this system.
  if [ $1 -gt 1 ] && [ -d /run/systemd/system ] ; then
    kill -TERM 1 &>/dev/null || :
  fi
}

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

%postun
if [ $1 -eq 1 ]; then
   [ -w %{_localstatedir} ] && journalctl --update-catalog || :
   systemd-tmpfiles --create &>/dev/null || :
fi

%systemd_postun_with_restart systemd-timedated.service systemd-hostnamed.service systemd-journald.service systemd-localed.service systemd-userdbd.service

# FIXME: systemd-logind.service is excluded (https://github.com/systemd/systemd/pull/17558)

# This is the explanded form of %%systemd_user_daemon_reexec. We
# can't use the macro because we define it ourselves.
if [ $1 -ge 1 ] && [ -x "/usr/lib/systemd/systemd-update-helper" ]; then
    # Package upgrade, not uninstall
    /usr/lib/systemd/systemd-update-helper user-reexec || :
fi

%triggerun resolved -- systemd < 246.1-1
# This is for upgrades from previous versions before systemd-resolved became the default.
systemctl --no-reload preset systemd-resolved.service &>/dev/null || :

if systemctl -q is-enabled systemd-resolved.service &>/dev/null; then
  systemctl -q is-enabled NetworkManager.service 2>/dev/null && \
  ! test -L /etc/resolv.conf 2>/dev/null && \
  ! mountpoint /etc/resolv.conf &>/dev/null && \
  grep -q 'Generated by NetworkManager' /etc/resolv.conf 2>/dev/null && \
  echo -e '/etc/resolv.conf was generated by NetworkManager.\nRemoving it to let systemd-resolved manage this file.' && \
  mv -v /etc/resolv.conf /etc/resolv.conf.orig-with-nm && \
  ln -sv ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf 2>/dev/null || :

  systemctl start systemd-resolved.service &>/dev/null || :
fi

%triggerun -- systemd < 247.3-2
# This is for upgrades from previous versions before oomd-defaults is available.
systemctl --no-reload preset systemd-oomd.service &>/dev/null || :

%triggerpostun -- systemd < 253~rc1-2
# This is for upgrades from previous versions where systemd-journald-audit.socket
# had a static enablement symlink.
# We use %%triggerpostun here because rpm doesn't allow a second %%triggerun with
# a different package version.
systemctl --no-reload preset systemd-journald-audit.socket &>/dev/null || :

%global udev_services systemd-udev{d,-settle,-trigger}.service systemd-udevd-{control,kernel}.socket systemd-homed.service %{?want_bootloader:systemd-boot-update.service} systemd-oomd.service systemd-portabled.service systemd-pstore.service systemd-timesyncd.service remote-cryptsetup.target

%post udev
# Move old stuff around in /var/lib
mv %{_localstatedir}/lib/random-seed %{_localstatedir}/lib/systemd/random-seed &>/dev/null
mv %{_localstatedir}/lib/backlight %{_localstatedir}/lib/systemd/backlight &>/dev/null
if [ -L %{_localstatedir}/lib/systemd/timesync ]; then
    rm %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/private/systemd/timesync %{_localstatedir}/lib/systemd/timesync
fi
if [ -f %{_localstatedir}/lib/systemd/clock ] ; then
    mkdir -p %{_localstatedir}/lib/systemd/timesync
    mv %{_localstatedir}/lib/systemd/clock %{_localstatedir}/lib/systemd/timesync/.
fi

udevadm hwdb --update &>/dev/null

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

%postun udev
# Restart some services.
# Others are either oneshot services, or sockets, and restarting them causes issues (#1378974)
%systemd_postun_with_restart systemd-udevd.service systemd-timesyncd.service


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

%postun journal-remote
%systemd_postun_with_restart %journal_remote_units_restart
%firewalld_reload

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
    %systemd_post systemd-networkd.service systemd-networkd-wait-online.service
fi

%preun networkd
%systemd_preun systemd-networkd.service systemd-networkd-wait-online.service

%preun resolved
if [ $1 -eq 0 ] ; then
        systemctl disable --quiet \
                systemd-resolved.service \
                >/dev/null || :
        if [ -L /etc/resolv.conf ] && \
            realpath /etc/resolv.conf | grep ^/run/systemd/resolve/; then
                rm -f /etc/resolv.conf # no longer useful
                # if network manager is enabled, move to it instead
                [ -f /run/NetworkManager/resolv.conf ] && \
                systemctl -q is-enabled NetworkManager.service &>/dev/null && \
                    ln -fsv ../run/NetworkManager/resolv.conf /etc/resolv.conf
        fi
fi

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

%posttrans resolved
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

%files pam -f .file-list-pam

%files rpm-macros -f .file-list-rpm-macros

%files resolved -f .file-list-resolve

%files devel -f .file-list-devel

%files udev -f .file-list-udev

%if 0%{?want_bootloader}
%files ukify -f .file-list-ukify
%files boot-unsigned -f .file-list-boot
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
rm -rf $RPM_BUILD_ROOT
rm -f 10-timeout-abort.conf.user
rm -f .file-list-*
rm -f %{name}.lang

# While Fedora uses %autochangelog, we unfortunately cannot because
# our code is not stored in git per-project, instead everything is in
# a single git repo, which does not fit the design of %autospec and
# %autochangelog. So we need to continue manually maintaining the
# changelog here.
%changelog
* Thu Apr 18 2024 Dan Streetman <ddstreet@microsoft.com> - 255-12
- move libidn2 recommends from core package to systemd-networkd

* Wed Apr 24 2024 Dan Streetman <ddstreet@microsoft.com> - 255-11
- adjust pam.d/systemd-user file to include correct pam files

* Mon Apr 15 2024 Henry Li <lihl@microsoft.com> - 255-10
- Add patch to allow configurability of "UseDomains=" for networkd

* Wed Mar 20 2024 Dan Streetman <ddstreet@microsoft.com> - 255-9
- build dep the "bootstrap" macros because our maint scripts are broken without
  our rpm macros available during the build

* Mon Mar 11 2024 Daniel McIlvaney <damcilva@microsoft.com> - 255-8
- Obsolete the new systemd-bootstrap-libs subpacakge.

* Thu Feb 22 2024 Dan Streetman <ddstreet@microsoft.com> - 255-7
- remove use of %%azure (or %%azl) macro

* Wed Feb 28 2024 Dan Streetman <ddstreet@microsoft.com> - 255-6
- skip sm3 digest in test-openssl, we dont provide that digest

* Wed Feb 28 2024 Dan Streetman <ddstreet@microsoft.com> - 255-5
- update macro use in spec
- build with pytest-flakes

* Tue Feb 13 2024 Daniel McIlvaney <damcilva@microsoft.com> - 255-4
- Add Obsoletes: systemd-bootstrap* to allow systemd to replace the bootstrap version

* Wed Feb 07 2024 Dan Streetman <ddstreet@ieee.org> - 255-3
- remove conflicts dracut release number

* Thu Jan 04 2024 Dan Streetman <ddstreet@ieee.org> - 255-2
- Change upstream parent from Photon to Fedora.
- Following line is included only to avoid tooling failures, and does not indicate the actual license.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified.

* Wed Dec 06 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255-1
- Version 255
- Just a few bugfixes since 255-rc4: seccomp filters, logging,
  documentation, systemd-repart
- Includes a hardware database update.

* Sat Dec 02 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc4-1
- Version 255~rc4

* Fri Dec 01 2023 Adam Williamson <awilliam@redhat.com> - 255~rc3-4
- Backport PRs #30170 and #30266 to fix BPF denials (RHBZ #2250930)

* Wed Nov 29 2023 Adam Williamson <awilliam@redhat.com> - 255~rc3-3
- Backport #30197 to fix vconsole startup (RHBZ #2251394)

* Thu Nov 23 2023 Peter Robinson <pbrobinson@gmail.com> - 255~rc3-2
- de-dupe LICENSE.LGPL2.1 in licenses

* Wed Nov 22 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc3-1
- Version 255~rc3

* Wed Nov 22 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc2-2
- Add systemd-networkd-defaults subpackage

* Wed Nov 15 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc2-1
- Version 255~rc2
- See See https://raw.githubusercontent.com/systemd/systemd/v255-rc2/NEWS

* Wed Nov 08 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Add Conflicts with older dracut which doesn't have required patches

* Tue Nov 07 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc1-3
- Also build systemd-vmspawn

* Tue Nov 07 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc1-2
- Move oomd to systemd-udev

* Tue Nov 07 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 255~rc1-1
- Version 255~rc1
- See https://raw.githubusercontent.com/systemd/systemd/v255-rc1/NEWS
- All the files and services related to pcrs are moved to -udev subpackage.
  This includes the new systemd-pcrlock binary.

* Wed Sep 27 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.5-2
- Pull in more patches for keyboard layout matching

* Wed Sep 27 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.5-1
- Version 254.5
- Resolves rhbz#29216.

* Wed Sep 27 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-14
- Pull in patches to add PollLimit setting

* Wed Sep 27 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-13
- Change versioned Conflicts to rich Requires (rhbz#2240828)

* Tue Sep 19 2023 Adam Williamson <awilliam@redhat.com> - 254.2-12
- Backport PR #29215 to improve keyboard layout matching

* Mon Sep 18 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-7
- Fix creation of installkernel symlink

* Fri Sep 15 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-6
- Provide /usr/sbin/installkernel (rhbz#2239008).

* Thu Sep 07 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-2
- Make inter-subpackage dependencies archful

* Thu Sep 07 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.2-1
- Version 254.2
- A bunch of fixes in various areas: manager, coredump, sysupdate,
  hibernation, journal.
- Should fix rhbz#2234653.

* Wed Sep 06 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.1-8
- Actually reload user managers and backport unit reload macros

* Sat Sep 02 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 254.1-7
- ukify: Drop obsolete dependency on objcopy

* Sat Sep 02 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 254.1-6
- Add missing ukify dependency on python-cryptography

* Sun Aug 20 2023 Yu Watanabe <watanabe.yu+github@gmail.com> - 254.1-5
- spec: also explicitly enable/disable ukify support

* Sun Aug 13 2023 Yu Watanabe <watanabe.yu+github@gmail.com> - 254.1-4
- spec: explicitly enable/disable xen support

* Wed Aug 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254.1-1
- Version 254.1 (rhbz#2228089, possibly partial fix for rhbz#2229524)

* Wed Aug 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254-5
- Do daemon-reexec of user managers after package upgrade

* Mon Aug 07 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 254-4
- Revert "Supress errors on selinux systems"

* Thu Aug 03 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 254-3
- Add a custom %%clean implementation

* Thu Aug 03 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 254-2
- Update libbpf soname

* Fri Jul 28 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254-1
- Version 254 (just a bunch of bugfixes, mostly for unusual architectures,
  since rc3)
- rhbz#2226908
- See https://raw.githubusercontent.com/systemd/systemd/v254-rc1/NEWS for
  the full changeset.

* Mon Jul 24 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254~rc3-1
- Version 254~rc3
- A bunch of fixes, e.g. rhbz#2223795. Also a bunch of reverts of commits
  which were found to cause problems.

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 254~rc2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254~rc2-4
- Fix scriptlets for various services and remote-cryptsetup.target
  (rhbz#2217997)

* Sun Jul 16 2023 Stewart Smith <stewart@flamingspork.com> - 254~rc2-3
- Convert existing bcond_with[out] to plain bcond

* Sun Jul 16 2023 Stewart Smith <trawets@amazon.com> - 254~rc2-2
- Move gnutls, zlib, bzip2, lz4, xz, and zstd to bconds

* Sat Jul 15 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254~rc2-1
- Version 254~rc2
- Various bug fixes, in particular kernel-install should again work without
  /proc.

* Thu Jul 13 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 254~rc1-1
- Version 254~rc1
- Way too many changes to list. See
  https://raw.githubusercontent.com/systemd/systemd/v254-rc1/NEWS
- Fix regression in socket activation of services (rhbz#2213660).

* Mon Jun 26 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 253.5-7
- Use rpm sysuser provide generation on RHEL >= 10

* Thu Jun 22 2023 Panu Matilainen <pmatilai@redhat.com> - 253.5-6
- Use rpm's sysuser provide generation on Fedora >= 39

* Wed Jun 21 2023 Anita Zhang <the.anitazha@gmail.com> - 253.5-5
- fix typos in standalone package provides

* Mon Jun 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 253.5-4
- Avoid pillow and pyflakes in RHEL builds

* Mon Jun 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 253.5-3
- Avoid qrencode dependency in RHEL builds

* Fri Jun 02 2023 Alessandro Astone <ales.astone@gmail.com> - 253.5-2
- Increase vm.max_map_count

* Thu Jun 01 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.5-1
- Version 253.5

* Thu May 11 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.4-1
- Version 253.4

* Thu May 11 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 253.2-6
- Raise ManagedOOMMemoryPressureLimit from 50%% to 80%%

* Tue May 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.2-5
- Add forgotten Provides and Conflicts for standalones

* Wed Apr 26 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.2-4
- sysusers.generate-pre.sh: properly escape quotes in description strings
  (rhbz#2104141)

* Wed Apr 26 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.2-3
- sysusers.generate-pre.sh: fix indentation in generated scripts

* Wed Mar 29 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.2-1
- Version 253.2

* Wed Mar 29 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.1-7
- oomd: stop monitoring user-*.slice slices (rhbz#2177722)

* Thu Mar 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.1-6
- Move /usr/lib/systemd/boot/ to systemd-boot-unsigned subpackage

* Fri Mar 03 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.1-2
- Fix build with gnu-efi-3.0.11-13

* Fri Mar 03 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253.1-1
- Version 253.1
- Fixes rhbz#2148464

* Wed Mar 01 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253-7
- Move man pages for sd-boot into systemd-boot-unsigned

* Wed Feb 22 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253-6
- Set TimeoutStopFailureMode=abort for services (see
  https://fedoraproject.org/wiki/Changes/Shorter_Shutdown_Timer)

* Tue Feb 21 2023 Dusty Mabe <dusty@dustymabe.com> - 253-5
- remove group write permission from 98-default-mac-none.link

* Tue Feb 21 2023 Dusty Mabe <dusty@dustymabe.com> - 253-4
- fix comment instructions for 98-default-mac-none.link

* Tue Feb 21 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253-3
- Backport patch for container compatibility (rhbz#2165004)

* Tue Feb 21 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253-2
- Add workaround patch for dracut generator issue (rhbz#2164404)

* Mon Feb 20 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253-1
- Version 253 (mostly some documentation fixes since -rc3).

* Fri Feb 10 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc3-1
- Version 253-rc3
- A bunch of bugfixes for regressions, some documentation and bug fixes
  too.
- Really fix rhbz#2165692 (previous build carried an unapplied patch).

* Thu Feb 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc2-7
- Revert patch switch causes problems for 'systemctl isolate'
  (rhbz#2165692)

* Wed Feb 08 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc2-6
- Disable systemd-boot-update.service in presets

* Wed Feb 08 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc2-4
- Update License to SPDX

* Mon Feb 06 2023 Thomas Haller <thaller@redhat.com> - 253~rc2-3
- add "98-default-mac-none.link" to keep default MAC address of
  bridge/bond/team

* Thu Feb 02 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 253~rc2-2
- Shorten shutdown timeout to 45 s

* Thu Feb 02 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc2-1
- Version 253~rc2
- Sysusers fixup (rhbz#2156900) + other small changes

* Thu Feb 02 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 253~rc1-5
- Build with xen only on Fedora

* Thu Jan 26 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc1-3
- Reenable systemd-journald-audit.socket after upgrades (rhbz#2164594)

* Wed Jan 25 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc1-2
- Add Requires on Python modules to systemd-ukify and Recommends for
  libp11-kit

* Tue Jan 24 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 253~rc1-1
- Version 253~rc1
- See https://raw.githubusercontent.com/systemd/systemd/v253-rc1/NEWS
- New subpackages: systemd-repart-standalone, systemd-shutdown-standalone,
  and systemd-ukify.

* Sun Jan 22 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.4-4
- Backport patches to fix issues gcc-13 and -D_FORTIFY_SOURCE=3

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 252.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Daan De Meyer <daan.j.demeyer@gmail.com> - 252.4-2
- Add python3 to BuildRequires

* Tue Dec 20 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.4-1
- Version 252.4
- Fixes a few different issues (systemd-timesyncd connectivity problems,
  broken emoji output on the console, crashes in pid1 unit dependency
  logic)
- CVE-2022-4415: systemd: coredump not respecting fs.suid_dumpable kernel
  setting

* Sat Dec 17 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.3-4
- boot: add Provides:systemd-boot(isa)

* Wed Dec 14 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.3-2
- Use upstream pam systemd-auth file with a patch, add pam_keyinit

* Thu Dec 08 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.3-1
- Version 252.3 (rhbz#2136916, rhbz#2083900)

* Fri Dec 02 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.2-2
- Split out systemd-boot-unsigned package

* Thu Nov 24 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.2-1
- Version 252.2
- Latest batch of bugfixes (rhbz#2137631)

* Thu Nov 24 2022 Martin Osvald <mosvald@redhat.com> - 252.1-3
- Support user:group notation by sysusers.generate-pre.sh script

* Tue Nov 08 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252.1-1
- Version 252.1 (just some small fixes).

* Mon Oct 31 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252-1
- Version 252

* Tue Oct 25 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc3-1
- Version 252-rc3 (#2135778)

* Tue Oct 18 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc2-28
- Version 252-rc2 (#2134741, #2133792)

* Fri Oct 14 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc1-31
- Fix upgrade detection in %%posttrans scriptlet (rhbz#2115094)

* Sun Oct 09 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc1-30
- Fix indentation in %%sysusers_create_compat macro (rhbz#2132835)

* Sun Oct 09 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc1-29
- Correctly move systemd-measure to systemd-udev subpackage

* Fri Oct 07 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 252~rc1-28
- Version 252-rc1 (for details see
  https://raw.githubusercontent.com/systemd/systemd/v252-rc1/NEWS)

* Sat Oct 01 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.5-29
- Fix permissions on %%ghost files (rhbz#2122889)

* Sat Oct 01 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.5-28
- Version 251.5 (rhbz#2129343, rhbz#2121106, rhbz#2130188)

* Fri Sep 30 2022 Yu Watanabe <watanabe.yu+github@gmail.com> - 251.4-41
- Replace patch for test-mountpoint-util

* Fri Sep 30 2022 Yu Watanabe <watanabe.yu+github@gmail.com> - 251.4-40
- patch: fix regression in bfq patch

* Fri Sep 30 2022 Luca BRUNO <lucab@lucabruno.net> - 251.4-39
- sysusers/generate: bridge 'm' entries to usermod

* Fri Sep 30 2022 Anita Zhang <the.anitazha@gmail.com> - 251.4-38
- Update systemd-oomd defaults to friendlier values
- Remove swap policy. Default amount of swap (8GB?) is a lot lower than
  what we use internally with the swap policy. Which frequently leads to
  GNOME getting killed (e.g.
  https://bugzilla.redhat.com/show_bug.cgi?id=1941170, and other BZs not
  linked here). Internally we use 0.5x-1x size of physical memory for swap
  via swapfiles (this will be documented in systemd upstream). In simple
  cases of using more memory than is available (but without memory
  pressure), the Kernel OOM killer can handle killing the offending
  process.

* Thu Sep 29 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.4-37
- Make systemd-devel conditionally pull in systemd-rpm-macros

* Fri Aug 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 251.4-53
- Set compile-time fallback hostname to "localhost"
  https://fedoraproject.org/wiki/Changes/FallbackHostname

* Thu Aug 18 2022 Kalev Lember <klember@redhat.com> - 251.4-52
- Avoid requiring systemd-pam from -devel subpackage

* Tue Aug 09 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.4-51
- Manually bump release version for rpmautospec

* Tue Aug 09 2022 Luca BRUNO <lucab@lucabruno.net> - 251.4-26
- Align sysusers-generated shell value with upstream systemd default

* Tue Aug 09 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.4-2
- Backport patches and do a full preset on first boot (#2114065,
  https://fedoraproject.org/wiki/Changes/Preset_All_Systemd_Units_on_First_Boot)

* Mon Aug 08 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.4-1
- Version 251.4 (fixes rhbz#2112551)
- A bunch of fixes to documentation, crashes in systemd-resolved,
  systemd-networkd, systemd itself, and other smaller fixes.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 251.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.3-1
- Update to latest bugfix release
- Drop forgotten "temporary" workaround for #1663040

* Wed Jun 29 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.2-2
- Drop forward-secure-sealing code from sd-journal and tools

* Thu Jun  2 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.2-1
- A bunch of man page fixes, a few memory-access correctness fixes,
  remove excessive messages to utmp sessions, suppress messages about
  bpf setup in the user manager (#2084955)

* Wed May 25 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.1-2
- Supress errors from useradd/groupadd (#2090129)
- Drop "v" from the version tag, add tilde back
- The tag for shared-libraries is reintroduced (#1906010)

* Tue May 24 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251.1-1
- First bugfix release for 250
- Two fixes for kernel-install and a revert for #2087225, #2088788.

* Sat May 21 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251-1
- Latest upstream release, for details see
  https://raw.githubusercontent.com/systemd/systemd/v251/NEWS.
- Fixes for #2071034, #2084955, #2086166.

* Mon May 16 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251~rc3-1
- Update to latest upstream prerelease (just various bugfixes)
- Udev rule processing should be now fixed (#2076459)
- Run sysusers and hwdb and catalog updates also if systemd is not running
  (#2085481)

* Wed May 11 2022 Adam Williamson <awilliam@redhat.com> - 251~rc2-2
- Backport #23352 to fix RHBZ #2083374

* Thu May  5 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251~rc2-1
- New upstream prerelease, for details see
  https://raw.githubusercontent.com/systemd/systemd/v251-rc2/NEWS.

* Tue Apr 12 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251~rc1-3
- Do not touch /etc/resolv.conf on upgrades (#2074122)
- Add bugfix patch and revert one patch which might be causing
  problems with the compose

* Mon Apr  4 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251~rc1-2
- Merge libsystemd-core back into individual binaries and drop the
  private shared library suffix (this should server as a work-around
  for rhbz#2071069)

* Tue Mar 29 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 251~rc1-1
- First release candidate in the new cycle
- Fixes rhbz#1449751, rhbz#1906010

* Fri Mar 18 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.4-2
- Fix the wrong file assignment done in previous version

* Thu Mar 17 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.4-1
- Move libcryptsetup plugins to -udev (#2031873)
- Move systemd-cryptenroll to -udev (David Tardon)
- Disable default DNS over TLS (#1889901) (Michael Catanzaro)

* Thu Feb 24 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-6
- Avoid trying to create the symlink if there's a dangling symlink already in
  place (#2058388)

* Wed Feb 23 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-5
- Move part of %%post scriptlet for resolved to %%posttrans (#2018913)
- Specify owner of utmp/wtmp/btmp/lastlog as root in the rpm listing

* Wed Feb 16 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-4
- Drop scriptlet for handling nobody user upgrades from Fedora <28
- Specify owner of /var/log/journal as root in the rpm listing (#2018913)

* Thu Feb 10 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-4
- Add pam_namespace to systemd-user pam config (rhbz#2053098)
- Drop 20-grubby.install plugin for kernel-install (rhbz#2033646)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 250.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-2
- Take ghost ownership of /var/log/lastlog (#1798685)

* Tue Jan 18 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.3-1
- Third stable release after v250: fixes for sd-boot on fringe hardware (e.g. VirtualBox),
  various man page updates, sd-journal file verification is now stricter,
  systemd-networkd by default will not add routes for wireguard AllowedIPs=
  systemd nss modules shouldn't try to read kernel command line
- Don't do sd-boot updates when not installed (#2038289)
- xdg-autostart-service will ignore ExecCondition= when the helper binary is missing
- kernel-install does cleanup better (#2016630)

* Fri Jan  7 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.2-1
- Second stable release after v250: various bugfixes
  (systemd-resolved, systemd-journald, userdbctl, homed).
- The manager should now gracefully handle the case where BPF LSM
  cannot be initialized (#2036145). The BPF filters are enabled again
  on all architectures, so *other* filter should also work on the
  affected architectures.
- kernel-install now checks paths used by grub2 before sd-boot paths again
  (#2036199)
- fstab-generator now ignores root-on-nfs/cifs/iscsi and live (#2037233)
- CVE-2021-3997, #2024639: systemd-tmpfiles would exhaust the stack and crash
  during excessive recursion on a very deeply nested directory structure.

* Tue Jan  4 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250.1-1
- First stable version after v250: various bugfixes, in particular for
  sd-boot, systemd-networkd, and various build issues.
- Fixes #2036517, #2035608, #2036217.

* Thu Dec 30 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250-3
- Disable bpf filters on arm64 (#2036145)

* Sat Dec 25 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250-2
- Fix warning about systemd-boot-update.service not existing on
  non-uefi architectures
- Enable all bpf features (#2035608)

* Thu Dec 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250-1
- Version 250, only some very small changes since -rc3.
- Switch unit status name format to 'combined' (#2028169)

* Mon Dec 20 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250~rc3-1
- Latest prerelease, see
  https://raw.githubusercontent.com/systemd/systemd/v250-rc3/NEWS for
  details.
- Fixes rhbz#2006761, rhbz#2027627, rhbz#1926323, rhbz#1919538.

* Sun Dec 12 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250~rc1-4
- Move systemd-boot-update.service to -udev subpackage
  and add it the the installation scriptlets (#2031400)
- Move libcryptsetup-token-systemd plugins to -udev (#2031873)
- Create /etc/resolv.conf symlink if nothing is present yet (#2032085)

* Fri Dec 10 2021 Pavel Březina <pbrezina@redhat.com> - 250~rc1-3
- Remove nsswitch.conf scriptlets (#2023743)

* Thu Dec  9 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 250~rc1-1
- Version 250-rc1,
  see https://raw.githubusercontent.com/systemd/systemd/v250-rc1/NEWS for
  details.

* Fri Nov 19 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 249.7-3
- Disable legacy iptables support

* Mon Nov 15 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.7-2
- Supress errors from update-helper when selinux is enabled (see #2023332)

* Sun Nov 14 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.7-1
- Latest bugfix release (better erofs detection, sd-event memory
  corruption bugfix, logind, documentation)
- Really fix helper to restart user units with older systemd (#2020415)

* Sun Nov 14 2021 Petr Menšík <pemensik@redhat.com> - 249.7-1
- Switch /etc/resolv.conf over to NM when systemd-resolved is uninstalled

* Wed Nov 10 2021 Kir Kolyshkin <kolyshkin@gmail.com> - 249.7-1
- Fix scope activation from a user instance (#2022041)

* Mon Nov  8 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.6-3
- Fix helper to restart user units with older systemd (#2020415)

* Thu Nov  4 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.6-2
- Latest bugfix release (networkd, coredumpctl, varlink, udev,
  systemctl, systemd itself, better detection of Hyper-V and
  Virtualbox virtualization, documentation updates)
- Fix helper to restart user units

* Fri Oct 29 2021 Adam Williamson <awilliam@redhat.com> - 249.5-2
- Backport PR #133 to fix boot

* Tue Oct 12 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.5-1
- Latest bugfix release (various fixes in systemd-networkd,
  -timesyncd, -journald, -udev, homed, -resolved, -repart, -oomd,
  -coredump, systemd itself, seccomp filters, TPM2 handling,
  -documentation, sd-event, sd-journal, journalctl, and nss-systemd).
- Fixes #1976445.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 249.4-2
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 24 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.4-1
- Latest bugfix release: various fixes for systemd-networkd,
  systemd-resolved, systemd, systemd-boot.
- Backport of macros to restart systemd user units (#1993244)

* Fri Aug  6 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.3-1
- Latest bugfix release: improved compatibility with latest glibc,
  various small documentation fixes, and fixes for systemd-networkd bridging,
  other minor fixes.
- systemctl set-property accepts glob patterns now (#1986258)

* Fri Jul 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.2-1
- Latest bugfix release (a minor hwdb regression bugfix, and correction
  to kernel commandline handling when reexecuting PID 1 in a container)

* Fri Jul 23 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 249.2-1
- Build with -Ddefault-dns-over-tls=opportunistic
  (https://fedoraproject.org/wiki/Changes/DNS_Over_TLS, #1889901)

* Tue Jul 20 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249.1-1
- Various minor documentation and correctness fixes.
- CVE-2021-33910, #1984020: an unchecked stack allocation could be used to
  crash systemd and cause the system to reboot by creating a very long
  fuse mountpoint path.

* Wed Jul  7 2021 Neal Gompa <ngompa13@gmail.com> - 249-2
- Use correct NEWS URLs for systemd 249 releases in changelog entries

* Wed Jul  7 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249-1
- Latest upstream release with minor bugfixes, see
  https://github.com/systemd/systemd/blob/v249/NEWS.
- systemd-oomd cpu usage is reduced (#1944646)

* Thu Jul  1 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249~rc3-1
- Latest upstream prerelease with various bugfixes, see
  https://github.com/systemd/systemd/blob/v249-rc3/NEWS.

* Fri Jun 25 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249~rc2-1
- Latest upstream prerelease with various bugfixes, see
  https://github.com/systemd/systemd/blob/v249-rc2/NEWS.
- Ignore FORCERENEW DHCP packets (TALOS-2020-1142, CVE-2020-13529, #1959398)

* Thu Jun 17 2021 Adam Williamson <awilliam@redhat.com> - 249~rc1-2
- Stop systemd providing systemd-resolved, now the subpackage exists (#1973462)

* Wed Jun 16 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 249~rc1-1
- Latest upstream prerelease, see
  https://github.com/systemd/systemd/blob/v249-rc1/NEWS.
  Fixes #1963428.
- Use systemd-sysusers to create users (#1965815)
- Move systemd-resolved into systemd-resolved subpackage (#1923727)
  [patch from Petr Menšík]

* Sat May 15 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248.3-1
- A fix for resolved crashes (#1946386, #1960227, #1950241)
- Some minor fixes for documentation, systemd-networkd, systemd-run, bootctl.

* Fri May  7 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248.2-1
- Pull in some more patches from upstream (#1944646, #1885090, #1941340)
- Adjust modes of some %%ghost files (#1956059)

* Thu May  6 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248.1-1
- Latest stable version: a long list of minor correctness fixes all around
  (#1955475, #911766, #1958167, #1952919)
- Enable tpm2-tss dependency (#1949505)

* Tue Apr 06 2021 Adam Williamson <awilliam@redhat.com> - 248-2
- Re-enable resolved caching, we hope all major bugs are resolved now

* Wed Mar 31 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248-1
- Latest upstream release, see
  https://github.com/systemd/systemd/blob/v248/NEWS.
- The changes since -rc4 are rather small, various fixes all over the place.
  A fix to how systemd-oomd selects a candidate to kill, and more debug logging
  to make this more transparent.

* Tue Mar 30 2021 Anita Zhang <the.anitazha@gmail.com> - 248~rc4-6
- Increase oomd user memory pressure limit to 50% (#1941170)

* Fri Mar 26 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc4-5
- Do not preset systemd-networkd.service and systemd-networkd-wait-online.service
  on upgrades from before systemd-networkd was split out (#1943263)
- In nsswitch.conf, move nss-myhostname to the front, before nss-mdns4 (#1943199)

* Wed Mar 24 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc4-4
- Revert patch that seems to cause problems with dns resolution
  (see comments on https://bodhi.fedoraproject.org/updates/FEDORA-2021-1c1a870ceb)

* Mon Mar 22 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc4-3
- Fix hang when processing timers during DST switch in Europe/Dublin timezone (#1941335)
- Fix returning combined IPv4/IPv6 responses from systemd-resolved cache (#1940715)
  (But note that the disablement of caching added previously is
  retained until we can do more testing.)
- Minor fix to interface naming by udev
- Fix for systemd-repart --size

* Fri Mar 19 2021 Adam Williamson <awilliam@redhat.com> - 248~rc4-2
- Disable resolved cache via config snippet (#1940715)

* Thu Mar 18 2021 Yu Watanabe <yuwatana@redhat.com> - 248~rc4-1
- Latest upstream prerelease, see
  https://github.com/systemd/systemd/blob/v248-rc4/NEWS.
- A bunch of documentation updates, and correctness fixes.

* Tue Mar 16 2021 Adam Williamson <awilliam@redhat.com> - 248~rc3-2
- Backport PR #19009 to fix CNAME redirect resolving some more (#1933433)

* Thu Mar 11 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc3-1
- Latest upstream prerelease, see
  https://github.com/systemd/systemd/blob/v248-rc3/NEWS.
- A bunch of documentation updates, correctness fixes, and systemd-networkd
  features.
- Resolves #1933137, #1935084, #1933873, #1931181, #1933335, #1935062, #1927148.

* Thu Mar 11 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc2-5
- Fix crash in pid1 during daemon-reexec (#1931034)

* Fri Mar 05 2021 Adam Williamson <awilliam@redhat.com> - 248~rc2-3
- Fix stub resolver CNAME chain resolving (#1933433)

* Mon Mar 01 2021 Josh Boyer <jwboyer@fedoraproject.org> - 248~rc2-2
- Don't set the fallback hostname to Fedora on non-Fedora OSes

* Tue Feb 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc2-1
- Latest upstream prelease, just a bunch of small fixes.
- Fixes #1931957.

* Tue Feb 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc1-2
- Rebuild with the newest scriptlets

* Tue Feb 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 248~rc1-1
- Latest upstream prerelease, see
  https://github.com/systemd/systemd/blob/v248-rc1/NEWS.
- Fixes #1614751 by only restarting services at the end of transcation.
  Various packages need to be rebuilt to have the updated macros.
- Fixes #1879028, though probably not completely.
- Fixes #1925805, #1928235.

* Wed Feb 17 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 247.3-3
- Increase oomd user memory pressure limit to 10% (#1929856)

* Fri Feb  5 2021 Anita Zhang <the.anitazha@gmail.com> - 247.3-2
- Changes for https://fedoraproject.org/wiki/Changes/EnableSystemdOomd.
- Backports consist primarily of PR #18361, #18444, and #18401 (plus some
  additional ones to handle merge conflicts).
- Create systemd-oomd-defaults subpackage to install unit drop-ins that will
  configure systemd-oomd to monitor and act.

* Tue Feb  2 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247.3-1
- Minor stable release
- Fixes #1895937, #1813219, #1903106.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 247.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247.2-2
- Fix bfq patch again (#1813219)

* Wed Dec 23 2020 Jonathan Underwood <jonathan.underwood@gmail.com> - 247.2-2
- Add patch to enable crypttab to support disabling of luks read and
  write workqueues (corresponding to
  https://github.com/systemd/systemd/pull/18062/).

* Wed Dec 16 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247.2-1
- Minor stable release
- Fixes #1908071.

* Tue Dec  8 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247.1-3
- Rebuild with fallback hostname change reverted.

* Fri Dec 04 2020 Bastien Nocera <bnocera@redhat.com> - 247.1-2
- Unset fallback-hostname as plenty of applications expected localhost
  to mean "default hostname" without ever standardising it (#1892235)

* Tue Dec  1 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247.1-1
- Latest stable release
- Fixes #1902819.
- Files to configure networking with systemd-networkd in a VM or container are
  moved to systemd-networkd subpackage. (They were previously in the -container
  subpackage, which is for container/VM management.)

* Thu Nov 26 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247-1
- Update to the latest version
- #1900878 should be fixed

* Tue Oct 20 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 247~rc2
- New upstream pre-release. See
  https://github.com/systemd/systemd/blob/v247-rc1/NEWS.
  Many smaller and bigger improvements and features are introduced.
  (#1885101, #1890632, #1879216)

  A backwards-incompatible change affects PCI network devices which
  are connected through a bridge which is itself associated with a
  slot. When more than one device was associated with the same slot,
  one of the devices would pseudo-randomly get named after the slot.
  That name is now not generated at all. This changed behaviour is
  causes the net naming scheme to be changed to "v247". To restore
  previous behaviour, specify net.naming-scheme=v245.

  systemd-oomd is built, but should not be considered "production
  ready" at this point. Testing and bug reports are welcome.

* Wed Sep 30 2020 Dusty Mabe <dusty@dustymabe.com> - 246.6-3
- Try to make files in subpackages (especially the networkd subpackage)
  more appropriate.

* Thu Sep 24 2020 Filipe Brandenburger <filbranden@gmail.com> - 246.6-2
- Build a package with standalone binaries for non-systemd systems.
  For now, only systemd-sysusers is included.

* Thu Sep 24 2020 Christian Glombek <lorbus@fedoraproject.org> - 246.6-2
- Split out networkd sub-package and add to main package as recommended dependency

* Sun Sep 20 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.6-1
- Update to latest stable release (various minor fixes: manager,
  networking, bootct, kernel-install, systemd-dissect, systemd-homed,
  fstab-generator, documentation) (#1876905)
- Do not fail in test because of kernel bug (#1803070)

* Sun Sep 13 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.5-1
- Update to latest stable release (a bunch of small network-related
  fixes in systemd-networkd and socket handling, documentation updates,
  a bunch of fixes for error handling).
- Also remove existing file when creating /etc/resolv.conf symlink
  upon installation (#1873856 again)

* Wed Sep  2 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.4-1
- Update to latest stable version: a rework of how the unit cache mtime works
  (hopefully #1872068, #1871327, #1867930), plus various fixes to
  systemd-resolved, systemd-dissect, systemd-analyze, systemd-ask-password-agent,
  systemd-networkd, systemd-homed, systemd-machine-id-setup, presets for
  instantiated units, documentation and shell completions.
- Create /etc/resolv.conf symlink upon installation (#1873856)
- Move nss-mdns before nss-resolve in /etc/nsswitch.conf and disable
  mdns by default in systemd-resolved (#1867830)

* Wed Aug 26 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.3-1
- Update to bugfix version (some networkd fixes, minor documentation
  fixes, relax handling of various error conditions, other fixlets for
  bugs without bugzilla numbers).

* Mon Aug 17 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.2-1
- A few minor bugfixes
- Adjust seccomp filter for kernel 5.8 and glibc 2.32 (#1869030)
- Create /etc/resolv.conf symlink on upgrade (#1867865)

* Fri Aug  7 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246.1-1
- A few minor bugfixes
- Remove /etc/resolv.conf on upgrades (if managed by NetworkManager), so
  that systemd-resolved can take over the management of the symlink.

* Thu Jul 30 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246-1
- Update to released version. Only some minor bugfixes since the pre-release.

* Sun Jul 26 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246~rc2-2
- Make /tmp be 50% of RAM again (#1856514)
- Re-run 'systemctl preset systemd-resolved' on upgrades.
  /etc/resolv.conf is not modified, by a hint is emitted if it is
  managed by NetworkManager.

* Fri Jul 24 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246~rc2-1
- New pre-release with incremental fixes
  (#1856037, #1858845, #1856122, #1857783)
- Enable systemd-resolved (with DNSSEC disabled by default, and LLMNR
  and mDNS support in resolve-only mode by default).
  See https://fedoraproject.org/wiki/Changes/systemd-resolved.

* Thu Jul  9 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 246~rc1-1
- New upstream release, see
  https://raw.githubusercontent.com/systemd/systemd/v246-rc1/NEWS.

  This release includes many new unit settings, related inter alia to
  cgroupsv2 freezer support and cpu affinity, encryption and verification.
  systemd-networkd has a ton of new functionality and many other tools gained
  smaller enhancements. systemd-homed gained FIDO2 support.

  Documentation has been significantly improved: sd-bus and sd-hwdb
  libraries are now fully documented; man pages have been added for
  the D-BUS APIs of systemd daemons and various new interfaces.

  Closes #1392925, #1790972, #1197886, #1525593.

* Wed Jun 24 2020 Bastien Nocera <bnocera@redhat.com> - 245.6-3
- Set fallback-hostname to fedora so that unset hostnames are still
  recognisable (#1392925)

* Tue Jun  2 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.6-2
- Add self-obsoletes to fix upgrades from F31

* Sun May 31 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.6-1
- Update to latest stable version (some documentation updates, minor
  memory correctness issues) (#1815605, #1827467, #1842067)

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 245.5-2
- Add explicit BuildRequires: acl
- Bootstrapping for json-c SONAME bump

* Fri Apr 17 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.5-1
- Update to latest stable version (#1819313, #1815412, #1800875)

* Thu Apr 16 2020 Björn Esser <besser82@fedoraproject.org> - 245.4-2
- Add bootstrap option to break circular deps on cryptsetup

* Wed Apr  1 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.4-1
- Update to latest stable version (#1814454)

* Thu Mar 26 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.3-1
- Update to latest stable version (no issue that got reported in bugzilla)

* Wed Mar 18 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245.2-1
- Update to latest stable version (a few bug fixes for random things) (#1798776)

* Fri Mar  6 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245-1
- Update to latest version (#1807485)

* Wed Feb 26 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245~rc2-1
- Modify the downstream udev rule to use bfq to only apply to disks (#1803500)
- "Upgrade" dependency on kbd package from Recommends to Requires (#1408878)
- Move systemd-bless-boot.service and systemd-boot-system-token.service to
  systemd-udev subpackage (#1807462)
- Move a bunch of other services to systemd-udev:
  systemd-pstore.service, all fsck-related functionality,
  systemd-volatile-root.service, systemd-verity-setup.service, and a few
  other related files.
- Fix daemon-reload rule to not kill non-systemd pid1 (#1803240)
- Fix namespace-related failure when starting systemd-homed (#1807465) and
  group lookup failure in nss_systemd (#1809147)
- Drop autogenerated BOOT_IMAGE= parameter from stored kernel command lines
  (#1716164)
- Don't require /proc to be mounted for systemd-sysusers to work (#1807768)

* Fri Feb 21 2020 Filipe Brandenburger <filbranden@gmail.com> - 245~rc1-4
- Update daemon-reexec fallback to check whether the system is booted with
  systemd as PID 1 and check whether we're upgrading before using kill -TERM
  on PID 1 (#1803240)

* Tue Feb 18 2020 Adam Williamson <awilliam@redhat.com> - 245~rc1-3
- Revert 097537f0 to fix plymouth etc. running when they shouldn't (#1803293)

* Fri Feb  7 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245~rc1-2
- Add default 'disable *' preset for user units (#1792474, #1468501),
  see https://fedoraproject.org/wiki/Changes/Systemd_presets_for_user_units.
- Add macro to generate "compat" scriptlets based off sysusers.d format
  and autogenerate user() and group() virtual provides (#1792462),
  see https://fedoraproject.org/wiki/Changes/Adopting_sysusers.d_format.
- Revert patch to udev rules causing regression with usb hubs (#1800820).

* Wed Feb  5 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 245~rc1-1
- New upstream release, see
  https://raw.githubusercontent.com/systemd/systemd/v245-rc1/NEWS.

  This release includes completely new functionality: systemd-repart,
  systemd-homed, user reconds in json, and multi-instantiable
  journald, and a partial rework of internal communcation to use
  varlink, and bunch of more incremental changes.

  The "predictable" interface name naming scheme is changed,
  net.naming-scheme= can be used to undo the change. The change applies
  to container interface names on the host.

- Fixes #1774242, #1787089, #1798414/CVE-2020-1712.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 244.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 21 2019  <zbyszek@nano-f31> - 244.1-2
- Disable service watchdogs (for systemd units)

* Sun Dec 15 2019  <zbyszek@nano-f31> - 244.1-1
- Update to latest stable batch (systemd-networkd fixups, better
  support for seccomp on s390x, minor cleanups to documentation).
- Drop patch to revert addition of NoNewPrivileges to systemd units

* Fri Nov 29 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 244-1
- Update to latest version. Just minor bugs fixed since the pre-release.

* Fri Nov 22 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 244~rc1-1
- Update to latest pre-release version,
  see https://github.com/systemd/systemd/blob/master/NEWS#L3.
  Biggest items: cgroups v2 cpuset controller, fido_id builtin in udev,
  systemd-networkd does not create a default route for link local addressing,
  systemd-networkd supports dynamic reconfiguration and a bunch of new settings.
  Network files support matching on WLAN SSID and BSSID.
- Better error messages when preset/enable/disable are used with a glob (#1763488)
- u2f-hidraw-policy package is obsoleted (#1753381)

* Tue Nov 19 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243.4
- Latest bugfix release. Systemd-stable snapshots will now be numbered.
- Fix broken PrivateDevices filter on big-endian, s390x in particular (#1769148)
- systemd-modules-load.service should only warn, not fail, on error (#1254340)
- Fix incorrect certificate validation with DNS over TLS (#1771725, #1771726,
  CVE-2018-21029)
- Fix regression with crypttab keys with colons
- Various memleaks and minor memory access issues, warning adjustments

* Fri Oct 18 2019 Adam Williamson <awilliam@redhat.com> - 243-4.gitef67743
- Backport PR #13792 to fix nomodeset+BIOS CanGraphical bug (#1728240)

* Thu Oct 10 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243-3.gitef67743
- Various minor documentation and error message cleanups
- Do not use cgroup v1 hierarchy in nspawn on groups v2 (#1756143)

* Sat Sep 21 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243-2.gitfab6f01
- Backport a bunch of patches (memory access issues, improvements to error
  reporting and handling in networkd, some misleading man page contents #1751363)
- Fix permissions on static nodes (#1740664)
- Make systemd-networks follow the RFC for DHPCv6 and radv timeouts
- Fix one crash in systemd-resolved (#1703598)
- Make journal catalog creation reproducible (avoid unordered hashmap use)
- Mark the accelerometer in HP laptops as part of the laptop base
- Fix relabeling of directories with relabel-extra.d/
- Fix potential stuck noop jobs in pid1
- Obsolete timedatex package (#1735584)

* Tue Sep  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243-1
- Update to latest release
- Emission of Session property-changed notifications from logind is fixed
  (this was breaking the switching of sessions to and from gnome).
- Security issue: unprivileged users were allowed to change DNS
  servers configured in systemd-resolved. Now proper polkit authorization
  is required.

* Mon Aug 26 2019 Adam Williamson <awilliam@redhat.com> - 243~rc2-2
- Backport PR #13406 to solve PATH ordering issue (#1744059)

* Thu Aug 22 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243~rc2-1
- Update to latest pre-release. Fixes #1740113, #1717712.
- The default scheduler for disks is set to BFQ (1738828)
- The default cgroup hierarchy is set to unified (cgroups v2) (#1732114).
  Use systemd.unified-cgroup-hierarchy=0 on the kernel command line to revert.
  See https://fedoraproject.org/wiki/Changes/CGroupsV2.

* Wed Aug 07 2019 Adam Williamson <awilliam@redhat.com> - 243~rc1-2
- Backport PR #1737362 so we own /etc/systemd/system again (#1737362)

* Tue Jul 30 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 243~rc1-1
- Update to latest version (#1715699, #1696373, #1711065, #1718192)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 242-7.git9d34e79
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242-6.git9d34e79
- Ignore bad rdrand output on AMD CPUs (#1729268)
- A bunch of backported patches from upstream: documentation, memory
  access fixups, command output tweaks (#1708996)

* Tue Jun 25 2019 Björn Esser <besser82@fedoraproject.org>- 242-5.git7a6d834
- Rebuilt (libqrencode.so.4)

* Tue Jun 25 2019 Miro Hrončok <mhroncok@redhat.com>- 242-4.git7a6d834
- Rebuilt for iptables update (libip4tc.so.2)

* Fri Apr 26 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242-3.git7a6d834
- Add symbol to mark vtable format changes (anything using sd_add_object_vtable
  or sd_add_fallback_vtable needs to be rebuilt)
- Fix wireguard ListenPort handling in systemd-networkd
- Fix hang in flush_accept (#1702358)
- Fix handling of RUN keys in udevd
- Some documentation and shell completion updates and minor fixes

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 242-2
- Rebuild with Meson fix for #1699099

* Thu Apr 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242-1
- Update to latest release
- Make scriptlet failure non-fatal

* Tue Apr  9 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242~rc4-1
- Update to latest prerelease

* Thu Apr  4 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242~rc3-1
- Update to latest prerelease

* Wed Apr  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 242~rc2-1
- Update to the latest prerelease.
- The bug reported on latest update that systemd-resolved and systemd-networkd are
  re-enabled after upgrade is fixed.

* Fri Mar 29 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241-4.gitcbf14c9
- Backport various patches from the v241..v242 range:
  kernel-install will not create the boot loader entry automatically (#1648907),
  various bash completion improvements (#1183769),
  memory leaks and such (#1685286).

* Thu Mar 14 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241-3.gitc1f8ff8
- Declare hyperv and framebuffer devices master-of-seat again (#1683197)

* Wed Feb 20 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241-2.gita09c170
- Prevent buffer overread in systemd-udevd
- Properly validate dbus paths received over dbus (#1678394, CVE-2019-6454)

* Sat Feb  9 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc2-2
- Turn LTO back on

* Tue Feb  5 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc2-1
- Update to latest release -rc2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 241~rc1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Yu Watanabe <watanabe.yu@gmail.com> - 241~rc1-2
- Backport a patch for kernel-install

* Sat Jan 26 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 241~rc1-1
- Update to latest release -rc1

* Tue Jan 15 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-6.gitf02b547
- Add a work-around for #1663040

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 240-5.gitf02b547
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jan 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-4.gitf02b547
- Add a work-around for selinux issue on live images (#1663040)

* Fri Jan 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-3.gitf02b547
- systemd-journald and systemd-journal-remote reject entries which
  contain too many fields (CVE-2018-16865, #1664973) and set limits on the
  process' command line length (CVE-2018-16864, #1664972)
- $DBUS_SESSION_BUS_ADDRESS is again exported by pam_systemd (#1662857)
- A fix for systemd-udevd crash (#1662303)

* Sat Dec 22 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-2
- Add two more patches that revert recent udev changes

* Fri Dec 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 240-1
- Update to latest release
  See https://github.com/systemd/systemd/blob/master/NEWS for the list of changes.

* Mon Dec 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-10.git9f3aed1
- Hibernation checks for resume= are rescinded (#1645870)
- Various patches:
  - memory issues in logind, networkd, journald (#1653068), sd-device, etc.
  - Adaptations for newer meson, lz4, kernel
  - Fixes for misleading bugs in documentation
- net.ipv4.conf.all.rp_filter is changed from 1 to 2

* Thu Nov 29 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Adjust scriptlets to modify /etc/authselect/user-nsswitch.conf
  (see https://github.com/pbrezina/authselect/issues/77)
- Drop old scriptlets for nsswitch.conf modifications for nss-mymachines and nss-resolve

* Sun Nov 18 2018 Alejandro Domínguez Muñoz <adomu@net-c.com>
- Remove link creation for rsyslog.service

* Thu Nov  8 2018 Adam Williamson <awilliam@redhat.com> - 239-9.git9f3aed1
- Go back to using systemctl preset-all in %%post (#1647172, #1118740)

* Mon Nov  5 2018 Adam Williamson <awilliam@redhat.com> - 239-8.git9f3aed1
- Requires(post) openssl-libs to fix live image build machine-id issue
  See: https://pagure.io/dusty/failed-composes/issue/960

* Mon Nov  5 2018 Yu Watanabe <watanabe.yu@gmail.com>
- Set proper attributes to private directories

* Fri Nov  2 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-7.git9f3aed1
- Split out the rpm macros into systemd-rpm-macros subpackage (#1645298)

* Sun Oct 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-6.git9f3aed1
- Fix a local vulnerability from a race condition in chown-recursive (CVE-2018-15687, #1639076)
- Fix a local vulnerability from invalid handling of long lines in state deserialization (CVE-2018-15686, #1639071)
- Fix a remote vulnerability in DHCPv6 in systemd-networkd (CVE-2018-15688, #1639067)
- The DHCP server is started only when link is UP
- DHCPv6 prefix delegation is improved
- Downgrade logging of various messages and add loging in other places
- Many many fixes in error handling and minor memory leaks and such
- Fix typos and omissions in documentation
- Typo in %%_environmnentdir rpm macro is fixed (with backwards compatiblity preserved)
- Matching by MACAddress= in systemd-networkd is fixed
- Creation of user runtime directories is improved, and the user
  manager is only stopped after 10 s after the user logs out (#1642460 and other bugs)
- systemd units systemd-timesyncd, systemd-resolved, systemd-networkd are switched back to use DynamicUser=0
- Aliases are now resolved when loading modules from pid1. This is a (redundant) fix for a brief kernel regression.
- "systemctl --wait start" exits immediately if no valid units are named
- zram devices are not considered as candidates for hibernation
- ECN is not requested for both in- and out-going connections (the sysctl overide for net.ipv4.tcp_ecn is removed)
- Various smaller improvements to unit ordering and dependencies
- generators are now called with the manager's environment
- Handling of invalid (intentionally corrupt) dbus messages is improved, fixing potential local DOS avenues
- The target of symlinks links in .wants/ and .requires/ is now ignored. This fixes an issue where
  the unit file would sometimes be loaded from such a symlink, leading to non-deterministic unit contents.
- Filtering of kernel threads is improved. This fixes an issues with newer kernels where hybrid kernel/user
  threads are used by bpfilter.
- "noresume" can be used on the kernel command line to force normal boot even if a hibernation images is present
- Hibernation is not advertised if resume= is not present on the kernenl command line
- Hibernation/Suspend/... modes can be disabled using AllowSuspend=,
  AllowHibernation=, AllowSuspendThenHibernate=, AllowHybridSleep=
- LOGO= and DOCUMENTATION_URL= are documented for the os-release file
- The hashmap mempool is now only used internally in systemd, and is disabled for external users of the systemd libraries
- Additional state is serialized/deserialized when logind is restarted, fixing the handling of user objects
- Catalog entries for the journal are improved (#1639482)
- If suspend fails, the post-suspend hooks are still called.
- Various build issues on less-common architectures are fixed

* Wed Oct  3 2018 Jan Synáček <jsynacek@redhat.com> - 239-5
- Fix meson using -Ddebug, which results in FTBFS
- Fix line_begins() to accept word matching full string (#1631840)

* Mon Sep 10 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-4
- Move /etc/yum/protected.d/systemd.conf to /etc/dnf/ (#1626969)

* Wed Jul 18 2018 Terje Rosten <terje.rosten@ntnu.no> - 239-3
- Ignore return value from systemd-binfmt in scriptlet (#1565425)

* Sun Jul 15 2018 Filipe Brandenburger <filbranden@gmail.com> - 239-3
- Override systemd-user PAM config in install and not prep

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 239-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-2
- Rebuild for Python 3.7 again

* Fri Jun 22 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 239-1
- Update to latest version, mostly bug fixes and new functionality,
  very little breaking changes. See
  https://github.com/systemd/systemd/blob/v239/NEWS for details.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 238-9.git0e0aa59
- Rebuilt for Python 3.7

* Fri May 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-8.git0e0aa59
- Backport a number of patches (documentation, hwdb updates)
- Fixes for tmpfiles 'e' entries
- systemd-networkd crashes
- XEN virtualization detection on hyper-v
- Avoid relabelling /sys/fs/cgroup if not needed (#1576240)

* Wed Apr 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-7.fc28.1
- Allow fake Delegate= setting on slices (#1568594)

* Wed Mar 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-7
- Move udev transfiletriggers to the right package, fix quoting

* Tue Mar 27 2018 Colin Walters <walters@verbum.org> - 238-6
- Use shell for triggers; see https://github.com/systemd/systemd/pull/8550
  This fixes compatibility with rpm-ostree.

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-5
- Backport patch to revert inadvertent change of "predictable" interface name (#1558027)

* Fri Mar 16 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-4
- Do not close dbus connection during dbus reload call (#1554578)

* Wed Mar  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-3
- Revert the patches for GRUB BootLoaderSpec support
- Add patch for /etc/machine-id creation (#1552843)

* Tue Mar  6 2018 Yu Watanabe <watanabe.yu@gmail.com> - 238-2
- Fix transfiletrigger script (#1551793)

* Mon Mar  5 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238-1
- Update to latest version
- This fixes a hard-to-trigger potential vulnerability (CVE-2018-6954)
- New transfiletriggers are installed for udev hwdb and rules, the journal
  catalog, sysctl.d, binfmt.d, sysusers.d, tmpfiles.d.

* Tue Feb 27 2018 Javier Martinez Canillas <javierm@redhat.com> - 237-7.git84c8da5
- Add patch to install kernel images for GRUB BootLoaderSpec support

* Sat Feb 24 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-6.git84c8da5
- Create /etc/systemd in %%post libs if necessary (#1548607)

* Fri Feb 23 2018 Adam Williamson <awilliam@redhat.com> - 237-5.git84c8da5
- Use : not touch to create file in -libs %%post

* Thu Feb 22 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 237-4.git84c8da5
- Add coreutils dep for systemd-libs %%post
- Add patch to typecast USB IDs to avoid compile failure

* Wed Feb 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-3.git84c8da5
- Update some patches for test skipping that were updated upstream
  before merging
- Add /usr/lib/systemd/purge-nobody-user — a script to check if nobody is defined
  correctly and possibly replace existing mappings

* Tue Feb 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-2.gitdff4849
- Backport a bunch of patches, most notably for the journal and various
  memory issues. Some minor build fixes.
- Switch to new ldconfig macros that do nothing in F28+
- /etc/systemd/dont-synthesize-nobody is created in %%post if nfsnobody
  or nobody users are defined (#1537262)

* Fri Feb  9 2018 Zbigniew Jędrzejeweski-Szmek <zbyszek@in.waw.pl> - 237-1.git78bd769
- Update to first stable snapshot (various minor memory leaks and misaccesses,
  some documentation bugs, build fixes).

* Sun Jan 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 237-1
- Update to latest version

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 236-4.git3e14c4c
- Add patch to include <crypt.h> if needed

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 236-3.git3e14c4c
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-2.git23e14c4
- Backport a bunch of bugfixes from upstream (#1531502, #1531381, #1526621
  various memory corruptions in systemd-networkd)
- /dev/kvm is marked as a static node which fixes permissions on s390x
  and ppc64 (#1532382)

* Fri Dec 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 236-1
- Update to latest version

* Mon Dec 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-5.git4a0e928
- Update to latest git snapshot, do not build for realz
- Switch to libidn2 again (#1449145)

* Tue Nov 07 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-4
- Rebuild for cryptsetup-2.0.0-0.2.fc28

* Wed Oct 25 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-3
- Backport a bunch of patches, including LP#172535

* Wed Oct 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-2
- Patches for cryptsetup _netdev

* Fri Oct  6 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 235-1
- Update to latest version

* Tue Sep 26 2017 Nathaniel McCallum <npmccallum@redhat.com> - 234-8
- Backport /etc/crypttab _netdev feature from upstream

* Thu Sep 21 2017 Michal Sekletar <msekleta@redhat.com> - 234-7
- Make sure to remove all device units sharing the same sysfs path (#1475570)

* Mon Sep 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-6
- Bump xslt recursion limit for libxslt-1.30

* Mon Jul 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-5
- Backport more patches (#1476005, hopefully #1462378)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 234-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-3
- Fix x-systemd.timeout=0 in /etc/fstab (#1462378)
- Minor patches (memleaks, --help fixes, seccomp on arm64)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-2
- Create kvm group (#1431876)

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-1
- Latest release

* Sat Jul  1 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-7.git74d8f1c
- Update to snapshot
- Build with meson again

* Tue Jun 27 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-6
- Fix an out-of-bounds write in systemd-resolved (CVE-2017-9445)

* Fri Jun 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-5.gitec36d05
- Update to snapshot version, build with meson

* Thu Jun 15 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-4
- Backport a bunch of small fixes (memleaks, wrong format strings,
  man page clarifications, shell completion)
- Fix systemd-resolved crash on crafted DNS packet (CVE-2017-9217, #1455493)
- Fix systemd-vconsole-setup.service error on systems with no VGA console (#1272686)
- Drop soft-static uid for systemd-journal-gateway
- Use ID from /etc/os-release as ntpvendor

* Thu Mar 16 2017 Michal Sekletar <msekleta@redhat.com> - 233-3
- Backport bugfixes from upstream
- Don't return error when machinectl couldn't figure out container IP addresses (#1419501)

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-2
- Fix installation conflict with polkit

* Thu Mar  2 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 233-1
- New upstream release (#1416201, #1405439, #1420753, many others)
- New systemd-tests subpackage with "installed tests"

* Thu Feb 16 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-15
- Add %%ghost %%dir entries for .wants dirs of our targets (#1422894)

* Tue Feb 14 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-14
- Ignore the hwdb parser test

* Tue Feb 14 2017 Jan Synáček <jsynacek@redhat.com> - 232-14
- machinectl fails when virtual machine is running (#1419501)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 232-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-12
- Backport patch for initrd-switch-root.service getting killed (#1414904)
- Fix sd-journal-gatewayd -D, --trust, and COREDUMP_CONTAINER_CMDLINE
  extraction by sd-coredump.

* Sun Jan 29 2017 zbyszek <zbyszek@in.waw.pl> - 232-11
- Backport a number of patches (#1411299, #1413075, #1415745,
                                ##1415358, #1416588, #1408884)
- Fix various memleaks and unitialized variable access
- Shell completion enhancements
- Enable TPM logging by default (#1411156)
- Update hwdb (#1270124)

* Thu Jan 19 2017 Adam Williamson <awilliam@redhat.com> - 232-10
- Backport fix for boot failure in initrd-switch-root (#1414904)

* Wed Jan 18 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-9
- Add fake dependency on systemd-pam to systemd-devel to ensure systemd-pam
  is available as multilib (#1414153)

* Tue Jan 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-8
- Fix buildsystem to check for lz4 correctly (#1404406)

* Wed Jan 11 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-7
- Various small tweaks to scriplets

* Sat Jan 07 2017 Kevin Fenzi <kevin@scrye.com> - 232-6
- Fix scriptlets to never fail in libs post

* Fri Jan 06 2017 Kevin Fenzi <kevin@scrye.com> - 232-5
- Add patch from Michal Schmidt to avoid process substitution (#1392236)

* Sun Nov  6 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-4
- Rebuild (#1392236)

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-3
- Make /etc/dbus-1/system.d directory non-%%ghost

* Fri Nov  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-2
- Fix kernel-install (#1391829)
- Restore previous systemd-user PAM config (#1391836)
- Move journal-upload.conf.5 from systemd main to journal-remote subpackage (#1391833)
- Fix permissions on /var/lib/systemd/journal-upload (#1262665)

* Thu Nov  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-1
- Update to latest version (#998615, #1181922, #1374371, #1390704, #1384150, #1287161)
- Add %%{_isa} to Provides on arch-full packages (#1387912)
- Create systemd-coredump user in %%pre (#1309574)
- Replace grubby patch with a short-circuiting install.d "plugin"
- Enable nss-systemd in the passwd, group lines in nsswith.conf
- Add [!UNAVAIL=return] fallback after nss-resolve in hosts line in nsswith.conf
- Move systemd-nspawn man pages to the right subpackage (#1391703)

* Tue Oct 18 2016 Jan Synáček <jsynacek@redhat.com> - 231-11
- SPC - Cannot restart host operating from container (#1384523)

* Sun Oct  9 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-10
- Do not recreate /var/log/journal on upgrades (#1383066)
- Move nss-myhostname provides to systemd-libs (#1383271)

* Fri Oct  7 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-9
- Fix systemctl set-default (#1374371)
- Prevent systemd-udev-trigger.service from restarting (follow-up for #1378974)

* Tue Oct  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-8
- Apply fix for #1378974

* Mon Oct  3 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-7
- Apply patches properly

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-6
- Better fix for (#1380286)

* Thu Sep 29 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-5
- Denial-of-service bug against pid1 (#1380286)

* Thu Aug 25 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-4
- Fix preset-all (#1363858)
- Fix issue with daemon-reload messing up graphics (#1367766)
- A few other bugfixes

* Wed Aug 03 2016 Adam Williamson <awilliam@redhat.com> - 231-3
- Revert preset-all change, it broke stuff (#1363858)

* Wed Jul 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-2
- Call preset-all on initial installation (#1118740)
- Fix botched Recommends for libxkbcommon

* Tue Jul 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-1
- Update to latest version

* Wed Jun  8 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 230-3
- Update to latest git snapshot (fixes for systemctl set-default,
  polkit lingering policy, reversal of the framebuffer rules,
  unaligned access fixes, fix for StartupBlockIOWeight-over-dbus).
  Those changes are interspersed with other changes and new features
  (mostly in lldp, networkd, and nspawn). Some of those new features
  might not work, but I think that existing functionality should not
  be broken, so it seems worthwile to update to the snapshot.

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-2
- Remove systemd-compat-libs on upgrade

* Sat May 21 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 230-1
- New version
- Drop compat-libs
- Require libxkbcommon explictly, since the automatic dependency will
  not be generated anymore

* Tue Apr 26 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 229-15
- Remove duplicated entries in -container %%files (#1330395)

* Fri Apr 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-14
- Move installation of udev services to udev subpackage (#1329023)

* Mon Apr 18 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-13
- Split out systemd-pam subpackage (#1327402)

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-12
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-11
- move more binaries and services from the main package to subpackages

* Mon Apr 18 2016 Harald Hoyer <harald@redhat.com> - 229-10
- move device dependant stuff to the udev subpackage

* Tue Mar 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-9
- Add myhostname to /etc/nsswitch.conf (#1318303)

* Mon Mar 21 2016 Harald Hoyer <harald@redhat.com> - 229-8
- fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019

* Thu Mar 17 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-7
- Moar patches (#1316964, #1317928)
- Move vconsole-setup and tmpfiles-setup-dev bits to systemd-udev
- Protect systemd-udev from deinstallation

* Fri Mar 11 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-6
- Create /etc/resolv.conf symlink from systemd-resolved (#1313085)

* Fri Mar  4 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 229-5
- Split out systemd-container subpackage (#1163412)
- Split out system-udev subpackage
- Add various bugfix patches, incl. a tentative fix for #1308771

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 229-4
- Power64 and s390(x) now have libseccomp support
- aarch64 has gnu-efi

* Tue Feb 23 2016 Jan Synáček <jsynacek@redhat.com> - 229-3
- Fix build failures on ppc64 (#1310800)

* Tue Feb 16 2016 Dennis Gilmore <dennis@ausil.us> - 229-2
- revert: fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019
- this causes the dtb files to not get installed at all and the fdtdir
- line in extlinux.conf to not get updated correctly

* Thu Feb 11 2016 Michal Sekletar <msekleta@redhat.com> - 229-1
- New upstream release

* Thu Feb 11 2016 Harald Hoyer <harald@redhat.com> - 228-10.gite35a787
- fixed kernel-install for copying files for grubby
Resolves: rhbz#1299019

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 228-9.gite35a787
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 228-8.gite35a787
- Rebuild for binutils on aarch64 fix

* Fri Jan 08 2016 Dan Horák <dan[at]danny.cz> - 228-7.gite35a787
- apply the conflict with fedora-release only in Fedora

* Thu Dec 10 2015 Jan Synáček <jsynacek@redhat.com> - 228-6.gite35a787
- Fix rawhide build failures on ppc64 (#1286249)

* Sun Nov 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-6.gite35a787
- Create /etc/systemd/network (#1286397)

* Thu Nov 26 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-5.gite35a787
- Do not install nss modules by default

* Tue Nov 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-4.gite35a787
- Update to latest upstream git: there is a bunch of fixes
  (nss-mymachines overflow bug, networkd fixes, more completions are
  properly installed), mixed with some new resolved features.
- Rework file triggers so that they always run before daemons are restarted

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-3
- Enable rpm file triggers for daemon-reload

* Thu Nov 19 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 228-2
- Fix version number in obsoleted package name (#1283452)

* Wed Nov 18 2015 Kay Sievers <kay@redhat.com> - 228-1
- New upstream release

* Thu Nov 12 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-7
- Rename journal-gateway subpackage to journal-remote
- Ignore the access mode on /var/log/journal (#1048424)
- Do not assume fstab is present (#1281606)

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 227-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 227-5
- Rebuild for libmicrohttpd soname bump

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 227-4
- Rebuilt for Python3.5 rebuild

* Wed Nov  4 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 227-3
- Fix syntax in kernel-install (#1277264)

* Tue Nov 03 2015 Michal Schmidt <mschmidt@redhat.com> - 227-2
- Rebuild for libmicrohttpd soname bump.

* Wed Oct  7 2015 Kay Sievers <kay@redhat.com> - 227-1
- New upstream release

* Fri Sep 18 2015 Jan Synáček <jsynacek@redhat.com> - 226-3
- user systemd-journal-upload should be in systemd-journal group (#1262743)

* Fri Sep 18 2015 Kay Sievers <kay@redhat.com> - 226-2
- Add selinux to  system-user PAM config

* Tue Sep  8 2015 Kay Sievers <kay@redhat.com> - 226-1
- New upstream release

* Thu Aug 27 2015 Kay Sievers <kay@redhat.com> - 225-1
- New upstream release

* Fri Jul 31 2015 Kay Sievers <kay@redhat.com> - 224-1
- New upstream release

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-2
- update to git snapshot

* Wed Jul 29 2015 Kay Sievers <kay@redhat.com> - 223-1
- New upstream release

* Thu Jul  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 222-2
- Remove python subpackages (python-systemd in now standalone)

* Tue Jul  7 2015 Kay Sievers <kay@redhat.com> - 222-1
- New upstream release

* Mon Jul  6 2015 Kay Sievers <kay@redhat.com> - 221-5.git619b80a
- update to git snapshot

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 221-4.git604f02a
- Add example file with yama config (#1234951)

* Sun Jul 5 2015 Kay Sievers <kay@redhat.com> - 221-3.git604f02a
- update to git snapshot

* Mon Jun 22 2015 Kay Sievers <kay@redhat.com> - 221-2
- build systemd-boot EFI tools

* Fri Jun 19 2015 Lennart Poettering <lpoetter@redhat.com> - 221-1
- New upstream release
- Undoes botched translation check, should be reinstated later?

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 220-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-9
- The gold linker is now fixed on aarch64

* Tue Jun  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-8
- Remove gudev which is now provided as separate package (libgudev)
- Fix for spurious selinux denials (#1224211)
- Udev change events (#1225905)
- Patches for some potential crashes
- ProtectSystem=yes does not touch /home
- Man page fixes, hwdb updates, shell completion updates
- Restored persistent device symlinks for bcache, xen block devices
- Tag all DRM cards as master-of-seat

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-7
- fix udev block device watch

* Tue Jun 09 2015 Harald Hoyer <harald@redhat.com> 220-6
- add support for network disk encryption

* Sun Jun  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 220-5
- Disable gold on aarch64 until it's fixed (tracked in rhbz #1225156)

* Sat May 30 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 220-4
- systemd-devel should require systemd-libs, not the main package (#1226301)
- Check for botched translations (#1226566)
- Make /etc/udev/hwdb.d part of the rpm (#1226379)

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 220-3
- Add patch to fix udev --daemon not cleaning child processes
  (upstream commit 86c3bece38bcf5).

* Wed May 27 2015 Richard W.M. Jones <rjones@redhat.com> - 220-2
- Add patch to fix udev --daemon crash (upstream commit 040e689654ef08).

* Thu May 21 2015 Lennart Poettering <lpoetter@redhat.com> - 220-1
- New upstream release
- Drop /etc/mtab hack, as that's apparently fixed in mock now (#1116158)
- Remove ghosting for /etc/systemd/system/runlevel*.target, these
  targets are not configurable anymore in systemd upstream
- Drop work-around for #1002806, since this is solved upstream now

* Wed May 20 2015 Dennis Gilmore <dennis@ausil.us> - 219-15
- fix up the conflicts version for fedora-release

* Wed May 20 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-14
- Remove presets (#1221340)
- Fix (potential) crash and memory leak in timedated, locking failure
  in systemd-nspawn, crash in resolved.
- journalctl --list-boots should be faster
- zsh completions are improved
- various ommissions in docs are corrected (#1147651)
- VARIANT and VARIANT_ID fields in os-release are documented
- systemd-fsck-root.service is generated in the initramfs (#1201979, #1107818)
- systemd-tmpfiles should behave better on read-only file systems (#1207083)

* Wed Apr 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-13
- Patches for some outstanding annoyances
- Small keyboard hwdb updates

* Wed Apr  8 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-12
- Tighten requirements between subpackages (#1207381).

* Sun Mar 22 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-11
- Move all parts systemd-journal-{remote,upload} to
  systemd-journal-gatewayd subpackage (#1193143).
- Create /var/lib/systemd/journal-upload directory (#1193145).
- Cut out lots of stupid messages at debug level which were obscuring more
  important stuff.
- Apply "tentative" state for devices only when they are added, not removed.
- Ignore invalid swap pri= settings (#1204336)
- Fix SELinux check for timedated operations to enable/disable ntp (#1014315)
- Fix comparing of filesystem paths (#1184016)

* Sat Mar 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-10
- Fixes for bugs 1186018, 1195294, 1185604, 1196452.
- Hardware database update.
- Documentation fixes.
- A fix for journalctl performance regression.
- Fix detection of inability to open files in journalctl.
- Detect SuperH architecture properly.
- The first of duplicate lines in tmpfiles wins again.
- Do vconsole setup after loading vconsole driver, not fbcon.
- Fix problem where some units were restarted during systemd reexec.
- Fix race in udevadm settle tripping up NetworkManager.
- Downgrade various log messages.
- Fix issue where journal-remote would process some messages with a delay.
- GPT /srv partition autodiscovery is fixed.
- Reconfigure old Finnish keymaps in post (#1151958)

* Tue Mar 10 2015 Jan Synáček <jsynacek@redhat.com> - 219-9
- Buttons on Lenovo X6* tablets broken (#1198939)

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 219-8
- Reworked device handling (#1195761)
- ACL handling fixes (with a script in %%post)
- Various log messages downgraded (#1184712)
- Allow PIE on s390 again (#1197721)

* Wed Feb 25 2015 Michal Schmidt <mschmidt@redhat.com> - 219-7
- arm: reenable lto. gcc-5.0.0-0.16 fixed the crash (#1193212)

* Tue Feb 24 2015 Colin Walters <walters@redhat.com> - 219-6
- Revert patch that breaks Atomic/OSTree (#1195761)

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-5
- Undo the resolv.conf workaround, Aim for a proper fix in Rawhide.

* Fri Feb 20 2015 Michal Schmidt <mschmidt@redhat.com> - 219-4
- Revive fedora-disable-resolv.conf-symlink.patch to unbreak composes.

* Wed Feb 18 2015 Michal Schmidt <mschmidt@redhat.com> - 219-3
- arm: disabling gold did not help; disable lto instead (#1193212)

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 219-2
- Update 90-default.present for dbxtool.

* Mon Feb 16 2015 Lennart Poettering <lpoetter@redhat.com> - 219-1
- New upstream release
- This removes the sysctl/bridge hack, a different solution needs to be found for this (see #634736)
- This removes the /etc/resolv.conf hack, anaconda needs to fix their handling of /etc/resolv.conf as symlink
- This enables "%%check"
- disable gold on arm, as that is broken (see #1193212)

* Mon Feb 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 218-6
- aarch64 now has seccomp support

* Thu Feb 05 2015 Michal Schmidt <mschmidt@redhat.com> - 218-5
- Don't overwrite systemd.macros with unrelated Source file.

* Thu Feb  5 2015 Jan Synáček <jsynacek@redhat.com> - 218-4
- Add a touchpad hwdb (#1189319)

* Thu Jan 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-4
- Enable xkbcommon dependency to allow checking of keymaps
- Fix permissions of /var/log/journal (#1048424)
- Enable timedatex in presets (#1187072)
- Disable rpcbind in presets (#1099595)

* Wed Jan  7 2015 Jan Synáček <jsynacek@redhat.com> - 218-3
- RFE: journal: automatically rotate the file if it is unlinked (#1171719)

* Mon Jan 05 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 218-3
- Add firewall description files (#1176626)

* Thu Dec 18 2014 Jan Synáček <jsynacek@redhat.com> - 218-2
- systemd-nspawn doesn't work on s390/s390x (#1175394)

* Wed Dec 10 2014 Lennart Poettering <lpoetter@redhat.com> - 218-1
- New upstream release
- Enable "nss-mymachines" in /etc/nsswitch.conf

* Thu Nov 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 217-4
- Change libgudev1 to only require systemd-libs (#727499), there's
  no need to require full systemd stack.
- Fixes for bugs #1159448, #1152220, #1158035.
- Bash completions updates to allow propose more units for start/restart,
  and completions for set-default,get-default.
- Again allow systemctl enable of instances.
- Hardware database update and fixes.
- Udev crash on invalid options and kernel commandline timeout parsing are fixed.
- Add "embedded" chassis type.
- Sync before 'reboot -f'.
- Fix restarting of timer units.

* Wed Nov 05 2014 Michal Schmidt <mschmidt@redhat.com> - 217-3
- Fix hanging journal flush (#1159641)

* Fri Oct 31 2014 Michal Schmidt <mschmidt@redhat.com> - 217-2
- Fix ordering cycles involving systemd-journal-flush.service and
  remote-fs.target (#1159117)

* Tue Oct 28 2014 Lennart Poettering <lpoetter@redhat.com> - 217-1
- New upstream release

* Fri Oct 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-12
- Drop PackageKit.service from presets (#1154126)

* Mon Oct 13 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-11
- Conflict with old versions of initscripts (#1152183)
- Remove obsolete Finnish keymap (#1151958)

* Fri Oct 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-10
- Fix a problem with voluntary daemon exits and some other bugs
  (#1150477, #1095962, #1150289)

* Fri Oct 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-9
- Update to latest git, but without the readahead removal patch
  (#1114786, #634736)

* Wed Oct 01 2014 Kay Sievers <kay@redhat.com> - 216-8
- revert "don't reset selinux context during CHANGE events"

* Wed Oct 01 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 216-7
- add temporary workaround for #1147910
- don't reset selinux context during CHANGE events

* Wed Sep 10 2014 Michal Schmidt <mschmidt@redhat.com> - 216-6
- Update timesyncd with patches to avoid hitting NTP pool too often.

* Tue Sep 09 2014 Michal Schmidt <mschmidt@redhat.com> - 216-5
- Use common CONFIGURE_OPTS for build2 and build3.
- Configure timesyncd with NTP servers from Fedora/RHEL vendor zone.

* Wed Sep 03 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-4
- Move config files for sd-j-remote/upload to sd-journal-gateway subpackage (#1136580)

* Thu Aug 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 216-3
- Drop no LTO build option for aarch64/s390 now it's fixed in binutils (RHBZ 1091611)

* Thu Aug 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 216-2
- Re-add patch to disable resolve.conf symlink (#1043119)

* Wed Aug 20 2014 Lennart Poettering <lpoetter@redhat.com> - 216-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 215-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Dan Horák <dan[at]danny.cz> 215-11
- disable LTO also on s390(x)

* Sat Aug 09 2014 Harald Hoyer <harald@redhat.com> 215-10
- fixed PPC64LE

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 215-9
- fix license handling

* Wed Jul 30 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-8
- Create systemd-journal-remote and systemd-journal-upload users (#1118907)

* Thu Jul 24 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-7
- Split out systemd-compat-libs subpackage

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 215-6
- Rebuilt for gobject-introspection 1.41.4

* Mon Jul 21 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-5
- Fix SELinux context of /etc/passwd-, /etc/group-, /etc/.updated (#1121806)
- Add missing BR so gnutls and elfutils are used

* Sat Jul 19 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-4
- Various man page updates
- Static device node logic is conditionalized on CAP_SYS_MODULES instead of CAP_MKNOD
  for better behaviour in containers
- Some small networkd link handling fixes
- vconsole-setup runs setfont before loadkeys (https://bugs.freedesktop.org/show_bug.cgi?id=80685)
- New systemd-escape tool
- XZ compression settings are tweaked to greatly improve journald performance
- "watch" is accepted as chassis type
- Various sysusers fixes, most importantly correct selinux labels
- systemd-timesyncd bug fix (https://bugs.freedesktop.org/show_bug.cgi?id=80932)
- Shell completion improvements
- New udev tag ID_SOFTWARE_RADIO can be used to instruct logind to allow user access
- XEN and s390 virtualization is properly detected

* Mon Jul 07 2014 Colin Walters <walters@redhat.com> - 215-3
- Add patch to disable resolve.conf symlink (#1043119)

* Sun Jul 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 215-2
- Move systemd-journal-remote to systemd-journal-gateway package (#1114688)
- Disable /etc/mtab handling temporarily (#1116158)

* Thu Jul 03 2014 Lennart Poettering <lpoetter@redhat.com> - 215-1
- New upstream release
- Enable coredump logic (which abrt would normally override)

* Sun Jun 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 214-5
- On aarch64 disable LTO as it still has issues on that arch

* Thu Jun 26 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-4
- Bugfixes (#996133, #1112908)

* Mon Jun 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-3
- Actually create input group (#1054549)

* Sun Jun 22 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 214-2
- Do not restart systemd-logind on upgrades (#1110697)
- Add some patches (#1081429, #1054549, #1108568, #928962)

* Wed Jun 11 2014 Lennart Poettering <lpoetter@redhat.com> - 214-1
- New upstream release
- Get rid of "floppy" group, since udev uses "disk" now
- Reenable LTO

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 213-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-3
- fix systemd-timesync user creation

* Wed May 28 2014 Michal Sekletar <msekleta@redhat.com> - 213-2
- Create temporary files after installation (#1101983)
- Add sysstat-collect.timer, sysstat-summary.timer to preset policy (#1101621)

* Wed May 28 2014 Kay Sievers <kay@redhat.com> - 213-1
- New upstream release

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 212-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 23 2014 Adam Williamson <awilliam@redhat.com> - 212-5
- revert change from 212-4, causes boot fail on single CPU boxes (RHBZ 1095891)

* Wed May 07 2014 Kay Sievers <kay@redhat.com> - 212-4
- add netns udev workaround

* Wed May 07 2014 Michal Sekletar <msekleta@redhat.com> - 212-3
- enable uuidd.socket by default (#1095353)

* Sat Apr 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 212-2
- Disable building with -flto for the moment due to gcc 4.9 issues (RHBZ 1091611)

* Tue Mar 25 2014 Lennart Poettering <lpoetter@redhat.com> - 212-1
- New upstream release

* Mon Mar 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 211-2
- Explicitly define which upstream platforms support libseccomp

* Tue Mar 11 2014 Lennart Poettering <lpoetter@redhat.com> - 211-1
- New upstream release

* Mon Mar 10 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-8
- Fix logind unpriviledged reboot issue and a few other minor fixes
- Limit generator execution time
- Recognize buttonless joystick types

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-7
- ppc64le needs link warnings disabled, too

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 210-6
- move ifarch ppc64le to correct place (libseccomp req)

* Fri Mar 07 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-5
- Bugfixes: #1047568, #1047039, #1071128, #1073402
- Bash completions for more systemd tools
- Bluetooth database update
- Manpage fixes

* Thu Mar 06 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-4
- Apply work-around for ppc64le too (#1073647).

* Sat Mar 01 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Backport a few patches, add completion for systemd-nspawn.

* Fri Feb 28 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 210-3
- Apply work-arounds for ppc/ppc64 for bugs 1071278 and 1071284

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-2
- Check more services against preset list and enable by default

* Mon Feb 24 2014 Lennart Poettering <lpoetter@redhat.com> - 210-1
- new upstream release

* Sun Feb 23 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 209-2.gitf01de96
- Enable dnssec-triggerd.service by default (#1060754)

* Sun Feb 23 2014 Kay Sievers <kay@redhat.com> - 209-2.gitf01de96
- git snapshot to sort out ARM build issues

* Thu Feb 20 2014 Lennart Poettering <lpoetter@redhat.com> - 209-1
- new upstream release

* Tue Feb 18 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-15
- Make gpsd lazily activated (#1066421)

* Mon Feb 17 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-14
- Back out patch which causes user manager to be destroyed when unneeded
  and spams logs (#1053315)

* Sun Feb 16 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-13
- A different fix for #1023820 taken from Mageia
- Backported fix for #997031
- Hardward database updates, man pages improvements, a few small memory
  leaks, utf-8 correctness and completion fixes
- Support for key-slot option in crypttab

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 208-12
- Own the %%{_prefix}/lib/kernel(/*) and %%{_datadir}/zsh(/*) dirs.

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-11
- Backport a few fixes, relevant documentation updates, and HWDB changes
  (#1051797, #1051768, #1047335, #1047304, #1047186, #1045849, #1043304,
   #1043212, #1039351, #1031325, #1023820, #1017509, #953077)
- Flip journalctl to --full by default (#984758)

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-9
- Apply two patches for #1026860

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-8
- Bump release to stay ahead of f20

* Tue Dec 03 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-7
- Backport patches (#1023041, #1036845, #1006386?)
- HWDB update
- Some small new features: nspawn --drop-capability=, running PID 1 under
  valgrind, "yearly" and "annually" in calendar specifications
- Some small documentation and logging updates

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-6
- Bump release to stay ahead of f20

* Tue Nov 19 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-5
- Use unit name in PrivateTmp= directories (#957439)
- Update manual pages, completion scripts, and hardware database
- Configurable Timeouts/Restarts default values
- Support printing of timestamps on the console
- Fix some corner cases in detecting when writing to the console is safe
- Python API: convert keyword values to string, fix sd_is_booted() wrapper
- Do not tread missing /sbin/fsck.btrfs as an error (#1015467)
- Allow masking of fsck units
- Advertise hibernation to swap files
- Fix SO_REUSEPORT settings
- Prefer converted xkb keymaps to legacy keymaps (#981805, #1026872)
- Make use of newer kmod
- Assorted bugfixes: #1017161, #967521, #988883, #1027478, #821723, #1014303

* Tue Oct 22 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-4
- Add temporary fix for #1002806

* Mon Oct 21 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 208-3
- Backport a bunch of fixes and hwdb updates

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-2
- Move old random seed and backlight files into the right place

* Wed Oct 2 2013 Lennart Poettering <lpoetter@redhat.com> - 208-1
- New upstream release

* Thu Sep 26 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-5
- Do not create /var/var/... dirs

* Wed Sep 18 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 207-4
- Fix policykit authentication
- Resolves: rhbz#1006680

* Tue Sep 17 2013 Harald Hoyer <harald@redhat.com> 207-3
- fixed login
- Resolves: rhbz#1005233

* Mon Sep 16 2013 Harald Hoyer <harald@redhat.com> 207-2
- add some upstream fixes for 207
- fixed swap activation
- Resolves: rhbz#1008604

* Fri Sep 13 2013 Lennart Poettering <lpoetter@redhat.com> - 207-1
- New upstream release

* Fri Sep 06 2013 Harald Hoyer <harald@redhat.com> 206-11
- support "debug" kernel command line parameter
- journald: fix fd leak in journal_file_empty
- journald: fix vacuuming of archived journals
- libudev: enumerate - do not try to match against an empty subsystem
- cgtop: fixup the online help
- libudev: fix memleak when enumerating childs

* Wed Sep 04 2013 Harald Hoyer <harald@redhat.com> 206-10
- Do not require grubby, lorax now takes care of grubby
- cherry-picked a lot of patches from upstream

* Tue Aug 27 2013 Dennis Gilmore <dennis@ausil.us> - 206-9
- Require grubby, Fedora installs require grubby,
- kernel-install took over from new-kernel-pkg
- without the Requires we are unable to compose Fedora
- everyone else says that since kernel-install took over
- it is responsible for ensuring that grubby is in place
- this is really what we want for Fedora

* Tue Aug 27 2013 Kay Sievers <kay@redhat.com> - 206-8
- Revert "Require grubby its needed by kernel-install"

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> 206-7
- Require grubby its needed by kernel-install

* Thu Aug 22 2013 Harald Hoyer <harald@redhat.com> 206-6
- kernel-install now understands kernel flavors like PAE

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 206-5
- add sddm.service to preset file (#998978)

* Fri Aug 16 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 206-4
- Filter out provides for private python modules.
- Add requires on kmod >= 14 (#990994).

* Sun Aug 11 2013 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 206-3
- New systemd-python3 package (#976427).
- Add ownership of a few directories that we create (#894202).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Kay Sievers <kay@redhat.com> - 206-1
- New upstream release
  Resolves (#984152)

* Wed Jul  3 2013 Lennart Poettering <lpoetter@redhat.com> - 205-1
- New upstream release

* Wed Jun 26 2013 Michal Schmidt <mschmidt@redhat.com> 204-10
- Split systemd-journal-gateway subpackage (#908081).

* Mon Jun 24 2013 Michal Schmidt <mschmidt@redhat.com> 204-9
- Rename nm_dispatcher to NetworkManager-dispatcher in default preset (#977433)

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-8
- fix, which helps to sucessfully browse journals with
  duplicated seqnums

* Fri Jun 14 2013 Harald Hoyer <harald@redhat.com> 204-7
- fix duplicate message ID bug
Resolves: rhbz#974132

* Thu Jun 06 2013 Harald Hoyer <harald@redhat.com> 204-6
- introduce 99-default-disable.preset

* Thu Jun  6 2013 Lennart Poettering <lpoetter@redhat.com> - 204-5
- Rename 90-display-manager.preset to 85-display-manager.preset so that it actually takes precedence over 90-default.preset's "disable *" line (#903690)

* Tue May 28 2013 Harald Hoyer <harald@redhat.com> 204-4
- Fix kernel-install (#965897)

* Wed May 22 2013 Kay Sievers <kay@redhat.com> - 204-3
- Fix kernel-install (#965897)

* Thu May  9 2013 Lennart Poettering <lpoetter@redhat.com> - 204-2
- New upstream release
- disable isdn by default (#959793)

* Tue May 07 2013 Harald Hoyer <harald@redhat.com> 203-2
- forward port kernel-install-grubby.patch

* Tue May  7 2013 Lennart Poettering <lpoetter@redhat.com> - 203-1
- New upstream release

* Wed Apr 24 2013 Harald Hoyer <harald@redhat.com> 202-3
- fix ENOENT for getaddrinfo
- Resolves: rhbz#954012 rhbz#956035
- crypt-setup-generator: correctly check return of strdup
- logind-dbus: initialize result variable
- prevent library underlinking

* Fri Apr 19 2013 Harald Hoyer <harald@redhat.com> 202-2
- nspawn create empty /etc/resolv.conf if necessary
- python wrapper: add sd_journal_add_conjunction()
- fix s390 booting
- Resolves: rhbz#953217

* Thu Apr 18 2013 Lennart Poettering <lpoetter@redhat.com> - 202-1
- New upstream release

* Tue Apr 09 2013 Michal Schmidt <mschmidt@redhat.com> - 201-2
- Automatically discover whether to run autoreconf and add autotools and git
  BuildRequires based on the presence of patches to be applied.
- Use find -delete.

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 201-1
- New upstream release

* Mon Apr  8 2013 Lennart Poettering <lpoetter@redhat.com> - 200-4
- Update preset file

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-3
- Remove NetworkManager-wait-online.service from presets file again, it should default to off

* Fri Mar 29 2013 Lennart Poettering <lpoetter@redhat.com> - 200-2
- New upstream release

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-2
- Add NetworkManager-wait-online.service to the presets file

* Tue Mar 26 2013 Lennart Poettering <lpoetter@redhat.com> - 199-1
- New upstream release

* Mon Mar 18 2013 Michal Schmidt <mschmidt@redhat.com> 198-7
- Drop /usr/s?bin/ prefixes.

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-6
- run autogen to pickup all changes

* Fri Mar 15 2013 Harald Hoyer <harald@redhat.com> 198-5
- do not mount anything, when not running as pid 1
- add initrd.target for systemd in the initrd

* Wed Mar 13 2013 Harald Hoyer <harald@redhat.com> 198-4
- fix switch-root and local-fs.target problem
- patch kernel-install to use grubby, if available

* Fri Mar 08 2013 Harald Hoyer <harald@redhat.com> 198-3
- add Conflict with dracut < 026 because of the new switch-root isolate

* Thu Mar  7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-2
- Create required users

* Thu Mar 7 2013 Lennart Poettering <lpoetter@redhat.com> - 198-1
- New release
- Enable journal persistancy by default

* Sun Feb 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 197-3
- Bump for ARM

* Fri Jan 18 2013 Michal Schmidt <mschmidt@redhat.com> - 197-2
- Added qemu-guest-agent.service to presets (Lennart, #885406).
- Add missing pygobject3-base to systemd-analyze deps (Lennart).
- Do not require hwdata, it is all in the hwdb now (Kay).
- Drop dependency on dbus-python.

* Tue Jan  8 2013 Lennart Poettering <lpoetter@redhat.com> - 197-1
- New upstream release

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-4
- Enable rngd.service by default (#857765).

* Mon Dec 10 2012 Michal Schmidt <mschmidt@redhat.com> - 196-3
- Disable hardening on s390(x) because PIE is broken there and produces
  text relocations with __thread (#868839).

* Wed Dec 05 2012 Michal Schmidt <mschmidt@redhat.com> - 196-2
- added spice-vdagentd.service to presets (Lennart, #876237)
- BR cryptsetup-devel instead of the legacy cryptsetup-luks-devel provide name
  (requested by Milan Brož).
- verbose make to see the actual build flags

* Wed Nov 21 2012 Lennart Poettering <lpoetter@redhat.com> - 196-1
- New upstream release

* Tue Nov 20 2012 Lennart Poettering <lpoetter@redhat.com> - 195-8
- https://bugzilla.redhat.com/show_bug.cgi?id=873459
- https://bugzilla.redhat.com/show_bug.cgi?id=878093

* Thu Nov 15 2012 Michal Schmidt <mschmidt@redhat.com> - 195-7
- Revert udev killing cgroup patch for F18 Beta.
- https://bugzilla.redhat.com/show_bug.cgi?id=873576

* Fri Nov 09 2012 Michal Schmidt <mschmidt@redhat.com> - 195-6
- Fix cyclical dep between systemd and systemd-libs.
- Avoid broken build of test-journal-syslog.
- https://bugzilla.redhat.com/show_bug.cgi?id=873387
- https://bugzilla.redhat.com/show_bug.cgi?id=872638

* Thu Oct 25 2012 Kay Sievers <kay@redhat.com> - 195-5
- require 'sed', limit HOSTNAME= match

* Wed Oct 24 2012 Michal Schmidt <mschmidt@redhat.com> - 195-4
- add dmraid-activation.service to the default preset
- add yum protected.d fragment
- https://bugzilla.redhat.com/show_bug.cgi?id=869619
- https://bugzilla.redhat.com/show_bug.cgi?id=869717

* Wed Oct 24 2012 Kay Sievers <kay@redhat.com> - 195-3
- Migrate /etc/sysconfig/ i18n, keyboard, network files/variables to
  systemd native files

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-2
- Provide syslog because the journal is fine as a syslog implementation

* Tue Oct 23 2012 Lennart Poettering <lpoetter@redhat.com> - 195-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=831665
- https://bugzilla.redhat.com/show_bug.cgi?id=847720
- https://bugzilla.redhat.com/show_bug.cgi?id=858693
- https://bugzilla.redhat.com/show_bug.cgi?id=863481
- https://bugzilla.redhat.com/show_bug.cgi?id=864629
- https://bugzilla.redhat.com/show_bug.cgi?id=864672
- https://bugzilla.redhat.com/show_bug.cgi?id=864674
- https://bugzilla.redhat.com/show_bug.cgi?id=865128
- https://bugzilla.redhat.com/show_bug.cgi?id=866346
- https://bugzilla.redhat.com/show_bug.cgi?id=867407
- https://bugzilla.redhat.com/show_bug.cgi?id=868603

* Wed Oct 10 2012 Michal Schmidt <mschmidt@redhat.com> - 194-2
- Add scriptlets for migration away from systemd-timedated-ntp.target

* Wed Oct  3 2012 Lennart Poettering <lpoetter@redhat.com> - 194-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=859614
- https://bugzilla.redhat.com/show_bug.cgi?id=859655

* Fri Sep 28 2012 Lennart Poettering <lpoetter@redhat.com> - 193-1
- New upstream release

* Tue Sep 25 2012 Lennart Poettering <lpoetter@redhat.com> - 192-1
- New upstream release

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-2
- Fix journal mmap header prototype definition to fix compilation on 32bit

* Fri Sep 21 2012 Lennart Poettering <lpoetter@redhat.com> - 191-1
- New upstream release
- Enable all display managers by default, as discussed with Adam Williamson

* Thu Sep 20 2012 Lennart Poettering <lpoetter@redhat.com> - 190-1
- New upstream release
- Take possession of /etc/localtime, and remove /etc/sysconfig/clock
- https://bugzilla.redhat.com/show_bug.cgi?id=858780
- https://bugzilla.redhat.com/show_bug.cgi?id=858787
- https://bugzilla.redhat.com/show_bug.cgi?id=858771
- https://bugzilla.redhat.com/show_bug.cgi?id=858754
- https://bugzilla.redhat.com/show_bug.cgi?id=858746
- https://bugzilla.redhat.com/show_bug.cgi?id=858266
- https://bugzilla.redhat.com/show_bug.cgi?id=858224
- https://bugzilla.redhat.com/show_bug.cgi?id=857670
- https://bugzilla.redhat.com/show_bug.cgi?id=856975
- https://bugzilla.redhat.com/show_bug.cgi?id=855863
- https://bugzilla.redhat.com/show_bug.cgi?id=851970
- https://bugzilla.redhat.com/show_bug.cgi?id=851275
- https://bugzilla.redhat.com/show_bug.cgi?id=851131
- https://bugzilla.redhat.com/show_bug.cgi?id=847472
- https://bugzilla.redhat.com/show_bug.cgi?id=847207
- https://bugzilla.redhat.com/show_bug.cgi?id=846483
- https://bugzilla.redhat.com/show_bug.cgi?id=846085
- https://bugzilla.redhat.com/show_bug.cgi?id=845973
- https://bugzilla.redhat.com/show_bug.cgi?id=845194
- https://bugzilla.redhat.com/show_bug.cgi?id=845028
- https://bugzilla.redhat.com/show_bug.cgi?id=844630
- https://bugzilla.redhat.com/show_bug.cgi?id=839736
- https://bugzilla.redhat.com/show_bug.cgi?id=835848
- https://bugzilla.redhat.com/show_bug.cgi?id=831740
- https://bugzilla.redhat.com/show_bug.cgi?id=823485
- https://bugzilla.redhat.com/show_bug.cgi?id=821813
- https://bugzilla.redhat.com/show_bug.cgi?id=807886
- https://bugzilla.redhat.com/show_bug.cgi?id=802198
- https://bugzilla.redhat.com/show_bug.cgi?id=767795
- https://bugzilla.redhat.com/show_bug.cgi?id=767561
- https://bugzilla.redhat.com/show_bug.cgi?id=752774
- https://bugzilla.redhat.com/show_bug.cgi?id=732874
- https://bugzilla.redhat.com/show_bug.cgi?id=858735

* Thu Sep 13 2012 Lennart Poettering <lpoetter@redhat.com> - 189-4
- Don't pull in pkg-config as dep
- https://bugzilla.redhat.com/show_bug.cgi?id=852828

* Wed Sep 12 2012 Lennart Poettering <lpoetter@redhat.com> - 189-3
- Update preset policy
- Rename preset policy file from 99-default.preset to 90-default.preset so that people can order their own stuff after the Fedora default policy if they wish

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-2
- Update preset policy
- https://bugzilla.redhat.com/show_bug.cgi?id=850814

* Thu Aug 23 2012 Lennart Poettering <lpoetter@redhat.com> - 189-1
- New upstream release

* Thu Aug 16 2012 Ray Strode <rstrode@redhat.com> 188-4
- more scriptlet fixes
  (move dm migration logic to %%posttrans so the service
   files it's looking for are available at the time
   the logic is run)

* Sat Aug 11 2012 Lennart Poettering <lpoetter@redhat.com> - 188-3
- Remount file systems MS_PRIVATE before switching roots
- https://bugzilla.redhat.com/show_bug.cgi?id=847418

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 188-2
- fix scriptlets

* Wed Aug  8 2012 Lennart Poettering <lpoetter@redhat.com> - 188-1
- New upstream release
- Enable gdm and avahi by default via the preset file
- Convert /etc/sysconfig/desktop to display-manager.service symlink
- Enable hardened build

* Mon Jul 30 2012 Kay Sievers <kay@redhat.com> - 187-3
- Obsolete: system-setup-keyboard

* Wed Jul 25 2012 Kalev Lember <kalevlember@gmail.com> - 187-2
- Run ldconfig for the new -libs subpackage

* Thu Jul 19 2012 Lennart Poettering <lpoetter@redhat.com> - 187-1
- New upstream release

* Mon Jul 09 2012 Harald Hoyer <harald@redhat.com> 186-2
- fixed dracut conflict version

* Tue Jul  3 2012 Lennart Poettering <lpoetter@redhat.com> - 186-1
- New upstream release

* Fri Jun 22 2012 Nils Philippsen <nils@redhat.com> - 185-7.gite7aee75
- add obsoletes/conflicts so multilib systemd -> systemd-libs updates work

* Thu Jun 14 2012 Michal Schmidt <mschmidt@redhat.com> - 185-6.gite7aee75
- Update to current git

* Wed Jun 06 2012 Kay Sievers - 185-5.gita2368a3
- disable plymouth in configure, to drop the .wants/ symlinks

* Wed Jun 06 2012 Michal Schmidt <mschmidt@redhat.com> - 185-4.gita2368a3
- Update to current git snapshot
  - Add systemd-readahead-analyze
  - Drop upstream patch
- Split systemd-libs
- Drop duplicate doc files
- Fixed License headers of subpackages

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> - 185-3
- Drop plymouth files
- Conflict with old plymouth

* Tue Jun 05 2012 Kay Sievers - 185-2
- selinux udev labeling fix
- conflict with older dracut versions for new udev file names

* Mon Jun 04 2012 Kay Sievers - 185-1
- New upstream release
  - udev selinux labeling fixes
  - new man pages
  - systemctl help <unit name>

* Thu May 31 2012 Lennart Poettering <lpoetter@redhat.com> - 184-1
- New upstream release

* Thu May 24 2012 Kay Sievers <kay@redhat.com> - 183-1
- New upstream release including udev merge.

* Wed Mar 28 2012 Michal Schmidt <mschmidt@redhat.com> - 44-4
- Add triggers from Bill Nottingham to correct the damage done by
  the obsoleted systemd-units's preun scriptlet (#807457).

* Mon Mar 26 2012 Dennis Gilmore <dennis@ausil.us> - 44-3
- apply patch from upstream so we can build systemd on arm and ppc
- and likely the rest of the secondary arches

* Tue Mar 20 2012 Michal Schmidt <mschmidt@redhat.com> - 44-2
- Don't build the gtk parts anymore. They're moving into systemd-ui.
- Remove a dead patch file.

* Fri Mar 16 2012 Lennart Poettering <lpoetter@redhat.com> - 44-1
- New upstream release
- Closes #798760, #784921, #783134, #768523, #781735

* Mon Feb 27 2012 Dennis Gilmore <dennis@ausil.us> - 43-2
- don't conflict with fedora-release systemd never actually provided
- /etc/os-release so there is no actual conflict

* Wed Feb 15 2012 Lennart Poettering <lpoetter@redhat.com> - 43-1
- New upstream release
- Closes #789758, #790260, #790522

* Sat Feb 11 2012 Lennart Poettering <lpoetter@redhat.com> - 42-1
- New upstream release
- Save a bit of entropy during system installation (#789407)
- Don't own /etc/os-release anymore, leave that to fedora-release

* Thu Feb  9 2012 Adam Williamson <awilliam@redhat.com> - 41-2
- rebuild for fixed binutils

* Thu Feb  9 2012 Lennart Poettering <lpoetter@redhat.com> - 41-1
- New upstream release

* Tue Feb  7 2012 Lennart Poettering <lpoetter@redhat.com> - 40-1
- New upstream release

* Thu Jan 26 2012 Kay Sievers <kay@redhat.com> - 39-3
- provide /sbin/shutdown

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 39-2
- increment release

* Wed Jan 25 2012 Kay Sievers <kay@redhat.com> - 39-1.1
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Wed Jan 25 2012 Lennart Poettering <lpoetter@redhat.com> - 39-1
- New upstream release

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-6.git9fa2f41
- Update to a current git snapshot.
- Resolves: #781657

* Sun Jan 22 2012 Michal Schmidt <mschmidt@redhat.com> - 38-5
- Build against libgee06. Reenable gtk tools.
- Delete unused patches.
- Add easy building of git snapshots.
- Remove legacy spec file elements.
- Don't mention implicit BuildRequires.
- Configure with --disable-static.
- Merge -units into the main package.
- Move section 3 manpages to -devel.
- Fix unowned directory.
- Run ldconfig in scriptlets.
- Split systemd-analyze to a subpackage.

* Sat Jan 21 2012 Dan Horák <dan[at]danny.cz> - 38-4
- fix build on big-endians

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-3
- Disable building of gtk tools for now

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-2
- Fix a few (build) dependencies

* Wed Jan 11 2012 Lennart Poettering <lpoetter@redhat.com> - 38-1
- New upstream release

* Tue Nov 15 2011 Michal Schmidt <mschmidt@redhat.com> - 37-4
- Run authconfig if /etc/pam.d/system-auth is not a symlink.
- Resolves: #753160

* Wed Nov 02 2011 Michal Schmidt <mschmidt@redhat.com> - 37-3
- Fix remote-fs-pre.target and its ordering.
- Resolves: #749940

* Wed Oct 19 2011 Michal Schmidt <mschmidt@redhat.com> - 37-2
- A couple of fixes from upstream:
- Fix a regression in bash-completion reported in Bodhi.
- Fix a crash in isolating.
- Resolves: #717325

* Tue Oct 11 2011 Lennart Poettering <lpoetter@redhat.com> - 37-1
- New upstream release
- Resolves: #744726, #718464, #713567, #713707, #736756

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-5
- Undo the workaround. Kay says it does not belong in systemd.
- Unresolves: #741655

* Thu Sep 29 2011 Michal Schmidt <mschmidt@redhat.com> - 36-4
- Workaround for the crypto-on-lvm-on-crypto disk layout
- Resolves: #741655

* Sun Sep 25 2011 Michal Schmidt <mschmidt@redhat.com> - 36-3
- Revert an upstream patch that caused ordering cycles
- Resolves: #741078

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-2
- Add /etc/timezone to ghosted files

* Fri Sep 23 2011 Lennart Poettering <lpoetter@redhat.com> - 36-1
- New upstream release
- Resolves: #735013, #736360, #737047, #737509, #710487, #713384

* Thu Sep  1 2011 Lennart Poettering <lpoetter@redhat.com> - 35-1
- New upstream release
- Update post scripts
- Resolves: #726683, #713384, #698198, #722803, #727315, #729997, #733706, #734611

* Thu Aug 25 2011 Lennart Poettering <lpoetter@redhat.com> - 34-1
- New upstream release

* Fri Aug 19 2011 Harald Hoyer <harald@redhat.com> 33-2
- fix ABRT on service file reloading
- Resolves: rhbz#732020

* Wed Aug  3 2011 Lennart Poettering <lpoetter@redhat.com> - 33-1
- New upstream release

* Fri Jul 29 2011 Lennart Poettering <lpoetter@redhat.com> - 32-1
- New upstream release

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-2
- Fix access mode of modprobe file, restart logind after upgrade

* Wed Jul 27 2011 Lennart Poettering <lpoetter@redhat.com> - 31-1
- New upstream release

* Wed Jul 13 2011 Lennart Poettering <lpoetter@redhat.com> - 30-1
- New upstream release

* Thu Jun 16 2011 Lennart Poettering <lpoetter@redhat.com> - 29-1
- New upstream release

* Mon Jun 13 2011 Michal Schmidt <mschmidt@redhat.com> - 28-4
- Apply patches from current upstream.
- Fixes memory size detection on 32-bit with >4GB RAM (BZ712341)

* Wed Jun 08 2011 Michal Schmidt <mschmidt@redhat.com> - 28-3
- Apply patches from current upstream
- https://bugzilla.redhat.com/show_bug.cgi?id=709909
- https://bugzilla.redhat.com/show_bug.cgi?id=710839
- https://bugzilla.redhat.com/show_bug.cgi?id=711015

* Sat May 28 2011 Lennart Poettering <lpoetter@redhat.com> - 28-2
- Pull in nss-myhostname

* Thu May 26 2011 Lennart Poettering <lpoetter@redhat.com> - 28-1
- New upstream release

* Wed May 25 2011 Lennart Poettering <lpoetter@redhat.com> - 26-2
- Bugfix release
- https://bugzilla.redhat.com/show_bug.cgi?id=707507
- https://bugzilla.redhat.com/show_bug.cgi?id=707483
- https://bugzilla.redhat.com/show_bug.cgi?id=705427
- https://bugzilla.redhat.com/show_bug.cgi?id=707577

* Sat Apr 30 2011 Lennart Poettering <lpoetter@redhat.com> - 26-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=699394
- https://bugzilla.redhat.com/show_bug.cgi?id=698198
- https://bugzilla.redhat.com/show_bug.cgi?id=698674
- https://bugzilla.redhat.com/show_bug.cgi?id=699114
- https://bugzilla.redhat.com/show_bug.cgi?id=699128

* Thu Apr 21 2011 Lennart Poettering <lpoetter@redhat.com> - 25-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694788
- https://bugzilla.redhat.com/show_bug.cgi?id=694321
- https://bugzilla.redhat.com/show_bug.cgi?id=690253
- https://bugzilla.redhat.com/show_bug.cgi?id=688661
- https://bugzilla.redhat.com/show_bug.cgi?id=682662
- https://bugzilla.redhat.com/show_bug.cgi?id=678555
- https://bugzilla.redhat.com/show_bug.cgi?id=628004

* Wed Apr  6 2011 Lennart Poettering <lpoetter@redhat.com> - 24-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=694079
- https://bugzilla.redhat.com/show_bug.cgi?id=693289
- https://bugzilla.redhat.com/show_bug.cgi?id=693274
- https://bugzilla.redhat.com/show_bug.cgi?id=693161

* Tue Apr  5 2011 Lennart Poettering <lpoetter@redhat.com> - 23-1
- New upstream release
- Include systemd-sysv-convert

* Fri Apr  1 2011 Lennart Poettering <lpoetter@redhat.com> - 22-1
- New upstream release

* Wed Mar 30 2011 Lennart Poettering <lpoetter@redhat.com> - 21-2
- The quota services are now pulled in by mount points, hence no need to enable them explicitly

* Tue Mar 29 2011 Lennart Poettering <lpoetter@redhat.com> - 21-1
- New upstream release

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 20-2
- Apply upstream patch to not send untranslated messages to plymouth

* Tue Mar  8 2011 Lennart Poettering <lpoetter@redhat.com> - 20-1
- New upstream release

* Tue Mar  1 2011 Lennart Poettering <lpoetter@redhat.com> - 19-1
- New upstream release

* Wed Feb 16 2011 Lennart Poettering <lpoetter@redhat.com> - 18-1
- New upstream release

* Mon Feb 14 2011 Bill Nottingham <notting@redhat.com> - 17-6
- bump upstart obsoletes (#676815)

* Wed Feb  9 2011 Tom Callaway <spot@fedoraproject.org> - 17-5
- add macros.systemd file for %%{_unitdir}

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  9 2011 Lennart Poettering <lpoetter@redhat.com> - 17-3
- Fix popen() of systemctl, #674916

* Mon Feb  7 2011 Bill Nottingham <notting@redhat.com> - 17-2
- add epoch to readahead obsolete

* Sat Jan 22 2011 Lennart Poettering <lpoetter@redhat.com> - 17-1
- New upstream release

* Tue Jan 18 2011 Lennart Poettering <lpoetter@redhat.com> - 16-2
- Drop console.conf again, since it is not shipped in pamtmp.conf

* Sat Jan  8 2011 Lennart Poettering <lpoetter@redhat.com> - 16-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 15-1
- New upstream release

* Thu Nov 25 2010 Lennart Poettering <lpoetter@redhat.com> - 14-1
- Upstream update
- Enable hwclock-load by default
- Obsolete readahead
- Enable /var/run and /var/lock on tmpfs

* Fri Nov 19 2010 Lennart Poettering <lpoetter@redhat.com> - 13-1
- new upstream release

* Wed Nov 17 2010 Bill Nottingham <notting@redhat.com> 12-3
- Fix clash

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-2
- Don't clash with initscripts for now, so that we don't break the builders

* Wed Nov 17 2010 Lennart Poettering <lpoetter@redhat.com> - 12-1
- New upstream release

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> - 11-2
- Rebuild with newer vala, libnotify

* Thu Oct  7 2010 Lennart Poettering <lpoetter@redhat.com> - 11-1
- New upstream release

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 10-6
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Bill Nottingham <notting@redhat.com> - 10-5
- merge -sysvinit into main package

* Mon Sep 20 2010 Bill Nottingham <notting@redhat.com> - 10-4
- obsolete upstart-sysvinit too

* Fri Sep 17 2010 Bill Nottingham <notting@redhat.com> - 10-3
- Drop upstart requires

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-2
- Enable audit
- https://bugzilla.redhat.com/show_bug.cgi?id=633771

* Tue Sep 14 2010 Lennart Poettering <lpoetter@redhat.com> - 10-1
- New upstream release
- https://bugzilla.redhat.com/show_bug.cgi?id=630401
- https://bugzilla.redhat.com/show_bug.cgi?id=630225
- https://bugzilla.redhat.com/show_bug.cgi?id=626966
- https://bugzilla.redhat.com/show_bug.cgi?id=623456

* Fri Sep  3 2010 Bill Nottingham <notting@redhat.com> - 9-3
- move fedora-specific units to initscripts; require newer version thereof

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-2
- Add missing tarball

* Fri Sep  3 2010 Lennart Poettering <lpoetter@redhat.com> - 9-1
- New upstream version
- Closes 501720, 614619, 621290, 626443, 626477, 627014, 627785, 628913

* Fri Aug 27 2010 Lennart Poettering <lpoetter@redhat.com> - 8-3
- Reexecute after installation, take ownership of /var/run/user
- https://bugzilla.redhat.com/show_bug.cgi?id=627457
- https://bugzilla.redhat.com/show_bug.cgi?id=627634

* Thu Aug 26 2010 Lennart Poettering <lpoetter@redhat.com> - 8-2
- Properly create default.target link

* Wed Aug 25 2010 Lennart Poettering <lpoetter@redhat.com> - 8-1
- New upstream release

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-3
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623561

* Thu Aug 12 2010 Lennart Poettering <lpoetter@redhat.com> - 7-2
- Fix https://bugzilla.redhat.com/show_bug.cgi?id=623430

* Tue Aug 10 2010 Lennart Poettering <lpoetter@redhat.com> - 7-1
- New upstream release

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-2
- properly hide output on package installation
- pull in coreutils during package installtion

* Fri Aug  6 2010 Lennart Poettering <lpoetter@redhat.com> - 6-1
- New upstream release
- Fixes #621200

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-2
- Add tarball

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 5-1
- Prepare release 5

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 4-4
- Add 'sysvinit-userspace' provide to -sysvinit package to fix upgrade/install (#618537)

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-3
- Add libselinux to build dependencies

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-2
- Use the right tarball

* Sat Jul 24 2010 Lennart Poettering <lpoetter@redhat.com> - 4-1
- New upstream release, and make default

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-3
- Used wrong tarball

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-2
- Own /cgroup jointly with libcgroup, since we don't dpend on it anymore

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 3-1
- New upstream release

* Fri Jul 9 2010 Lennart Poettering <lpoetter@redhat.com> - 2-0
- New upstream release

* Wed Jul 7 2010 Lennart Poettering <lpoetter@redhat.com> - 1-0
- First upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.7.20100629git4176e5
- New snapshot
- Split off -units package where other packages can depend on without pulling in the whole of systemd

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.6.20100622gita3723b
- Add missing libtool dependency.

* Tue Jun 22 2010 Lennart Poettering <lpoetter@redhat.com> - 0-0.5.20100622gita3723b
- Update snapshot

* Mon Jun 14 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.4.20100614git393024
- Pull the latest snapshot that fixes a segfault. Resolves rhbz#603231

* Fri Jun 11 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.3.20100610git2f198e
- More minor fixes as per review

* Thu Jun 10 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.2.20100610git2f198e
- Spec improvements from David Hollis

* Wed Jun 09 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.1.20090609git2f198e
- Address review comments

* Tue Jun 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0-0.0.git2010-06-02
- Initial spec (adopted from Kay Sievers)
