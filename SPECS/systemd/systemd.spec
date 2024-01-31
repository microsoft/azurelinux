#global commit c4b843473a75fb38ed5bf54e9d3cfb1cb3719efa
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

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
%bcond gnutls 1
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

Name:           systemd
Url:            https://systemd.io
%if %{without inplace}
Version:        255
%else
# determine the build information from local checkout
Version:        %(tools/meson-vcs-tag.sh . error | sed -r 's/-([0-9])/.^\1/; s/-g/_g/')
%endif
Release:        %autorelease

%global stable %(c="%version"; [ "$c" = "${c#*.*}" ]; echo $?)

# For a breakdown of the licensing, see README
License:        LGPL-2.1-or-later AND MIT AND GPL-2.0-or-later
Summary:        System and Service Manager

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
Source3:        purge-nobody-user

# Prevent accidental removal of the systemd package
Source4:        yum-protect-systemd.conf

Source5:        inittab
Source6:        sysctl.conf.README
Source7:        systemd-journal-remote.xml
Source8:        systemd-journal-gatewayd.xml
Source9:        20-yama-ptrace.conf
Source10:       systemd-udev-trigger-no-reload.conf
# https://fedoraproject.org/wiki/How_to_filter_libabigail_reports
Source13:       .abignore

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
Patch0491:      fedora-use-system-auth-in-pam-systemd-user.patch

%ifarch %{ix86} x86_64 aarch64
%global want_bootloader 1
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  coreutils
BuildRequires:  libcap-devel
BuildRequires:  libmount-devel
BuildRequires:  libfdisk-devel
BuildRequires:  libpwquality-devel
BuildRequires:  pam-devel
BuildRequires:  libselinux-devel
BuildRequires:  audit-libs-devel
%if %{without bootstrap}
BuildRequires:  cryptsetup-devel
%endif
BuildRequires:  dbus-devel
BuildRequires:  /usr/sbin/sfdisk
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
%if %{undefined rhel}
BuildRequires:  qrencode-devel
%endif
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  iptables-devel
BuildRequires:  pkgconfig(libfido2)
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(tss2-rc)
BuildRequires:  pkgconfig(tss2-mu)
BuildRequires:  pkgconfig(libbpf)
BuildRequires:  systemtap-sdt-devel
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
%if %{undefined rhel}
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(pytest-flakes)
%endif
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

%if 0%{?fedora}
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
Requires(meta): (%{name}-rpm-macros = %{version}-%{release} if rpm-build)
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
%{?fedora:Recommends:     %{name}-networkd = %{version}-%{release}}
%{?fedora:Recommends:     %{name}-resolved = %{version}-%{release}}
Recommends:     diffutils
Requires:       (util-linux-core or util-linux)
Recommends:     libxkbcommon%{_isa}
Provides:       /bin/systemctl
Provides:       /sbin/shutdown
Provides:       syslog
Provides:       systemd-units = %{version}-%{release}
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
Conflicts:      dracut < 059-16

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
Recommends:     libidn2.so.0%{?elf_suffix}
Recommends:     libidn2.so.0(IDN2_0.0.0)%{?elf_bits}
Recommends:     libpcre2-8.so.0%{?elf_suffix}
Recommends:     libpwquality.so.1%{?elf_suffix}
Recommends:     libpwquality.so.1(LIBPWQUALITY_1.0)%{?elf_bits}
%if %{undefined rhel}
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

%description rpm-macros
Just the definitions of rpm macros.

See
https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd
for information how to use those macros.

%package devel
Summary:        Development headers for systemd
License:        LGPL-2.1-or-later AND MIT
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires(meta): (%{name}-rpm-macros = %{version}-%{release} if rpm-build)
Provides:       libudev-devel = %{version}
Provides:       libudev-devel%{_isa} = %{version}
Obsoletes:      libudev-devel < 183

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
Requires:       (grubby > 8.40-72 if grubby)
Requires:       (sdubby > 1.0-3 if sdubby)

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
Recommends:     python3dist(pillow)

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
%global ntpvendor %(source /etc/os-release; echo ${ID})
%{!?ntpvendor: echo 'NTP vendor zone is not set!'; exit 1}

CONFIGURE_OPTS=(
        -Dmode=release
        -Dsysvinit-path=/etc/rc.d/init.d
        -Drc-local=/etc/rc.d/rc.local
        -Dntp-servers='0.%{ntpvendor}.pool.ntp.org 1.%{ntpvendor}.pool.ntp.org 2.%{ntpvendor}.pool.ntp.org 3.%{ntpvendor}.pool.ntp.org'
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

# /etc/initab
install -Dm0644 -t %{buildroot}/etc/ %{SOURCE5}

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

install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/ %{SOURCE13}

install -D -t %{buildroot}/usr/lib/systemd/ %{SOURCE3}

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
# Use rpm's own sysusers provides where available
%if ! (0%{?fedora} >= 39 || 0%{?rhel} >= 10)
install -m 0644 -D -t %{buildroot}%{_rpmconfigdir}/fileattrs/ %{SOURCE22}
install -m 0755 -D -t %{buildroot}%{_rpmconfigdir}/ %{SOURCE23}
%endif
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

%changelog
%autochangelog
