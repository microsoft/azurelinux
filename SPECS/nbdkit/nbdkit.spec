%bcond_with ruby
%bcond_with cdi
%bcond_with torrent
%bcond_with s3
%bcond_with blkio

Vendor:         Microsoft Corporation
Distribution:   Mariner
%undefine _package_note_flags
%global _hardened_build 1

%ifarch %{kernel_arches}
# ppc64le broken in rawhide:
# https://bugzilla.redhat.com/show_bug.cgi?id=2006709
# riscv64 tests fail with
# qemu-system-riscv64: invalid accelerator kvm
# qemu-system-riscv64: falling back to tcg
# qemu-system-riscv64: unable to find CPU model 'host'
# This seems to require changes in libguestfs and/or qemu to support
# -cpu max or -cpu virt.
# s390x builders can't run libguestfs
%ifnarch %{power64} riscv64 s390 s390x
%global have_libguestfs 1
%endif
%endif

# We can only compile the OCaml plugin on platforms which have native
# OCaml support (not bytecode).
%ifarch %{ocaml_native_compiler}
%global have_ocaml 1
%endif

# Architectures where we run the complete test suite including
# the libguestfs tests.
#
# On all other architectures, a simpler test suite must pass.  This
# omits any tests that run full qemu, since running qemu under TCG is
# often broken on non-x86_64 arches.
%global complete_test_arches x86_64

# If the test suite is broken on a particular architecture, document
# it as a bug and add it to this list.
%global broken_test_arches NONE


# If there are patches which touch autotools files, set this to 1.
%global patches_touch_autotools %{nil}

# The source directory.
%global source_directory 1.35-development

Name:           nbdkit
Version:        1.35.3
Release:        3%{?dist}
Summary:        NBD server

License:        BSD
URL:            https://gitlab.com/nbdkit/nbdkit

Source0:        http://libguestfs.org/download/nbdkit/%{source_directory}/%{name}-%{version}.tar.gz

BuildRequires: make
%if 0%{patches_touch_autotools}
BuildRequires:  autoconf, automake, libtool
%endif

BuildRequires:  gcc, gcc-c++
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  gnutls-devel
BuildRequires:  libselinux-devel
%if 0%{?have_libguestfs}
BuildRequires:  libguestfs-devel
%endif
BuildRequires:  libvirt-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  libzstd-devel
BuildRequires:  libcurl-devel
BuildRequires:  libnbd-devel >= 1.3.11
BuildRequires:  libssh-devel
BuildRequires:  e2fsprogs, e2fsprogs-devel
BuildRequires:  xorriso
%if %{with torrent}
BuildRequires:  rb_libtorrent-devel
%endif
%if %{with blkio}
BuildRequires:  libblkio-devel
%endif
BuildRequires:  bash-completion
BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  python3-devel
%if %{with s3}
BuildRequires:  python3-boto3
%endif
%if 0%{?have_ocaml}
BuildRequires:  ocaml >= 4.03
BuildRequires:  ocaml-ocamldoc
%endif
%if %{with ruby}
BuildRequires:  ruby-devel
%endif
BuildRequires:  tcl-devel
BuildRequires:  lua-devel

# Only for running the test suite:
BuildRequires:  %{_bindir}/bc
BuildRequires:  %{_bindir}/certtool
BuildRequires:  %{_bindir}/cut
BuildRequires:  expect
BuildRequires:  %{_bindir}/hexdump
BuildRequires:  /sbin/ip
BuildRequires:  jq
BuildRequires:  %{_bindir}/nbdcopy
BuildRequires:  %{_bindir}/nbdinfo
BuildRequires:  %{_bindir}/nbdsh
BuildRequires:  %{_bindir}/qemu-img
BuildRequires:  %{_bindir}/qemu-io
BuildRequires:  %{_bindir}/qemu-nbd
BuildRequires:  /sbin/sfdisk
BuildRequires:  %{_bindir}/socat
BuildRequires:  /sbin/ss
BuildRequires:  %{_bindir}/stat

# nbdkit is a metapackage pulling the server and a useful subset
# of the plugins and filters.
Requires:       nbdkit-server%{?_isa} = %{version}-%{release}
Requires:       nbdkit-basic-plugins%{?_isa} = %{version}-%{release}
Requires:       nbdkit-basic-filters%{?_isa} = %{version}-%{release}


%description
NBD is a protocol for accessing block devices (hard disks and
disk-like things) over the network.

nbdkit is a toolkit for creating NBD servers.

The key features are:

* Multithreaded NBD server written in C with good performance.

* Minimal dependencies for the basic server.

* Liberal license (BSD) allows nbdkit to be linked to proprietary
  libraries or included in proprietary code.

* Well-documented, simple plugin API with a stable ABI guarantee.
  Lets you to export "unconventional" block devices easily.

* You can write plugins in C or many other languages.

* Filters can be stacked in front of plugins to transform the output.

'%{name}' is a meta-package which pulls in the core server and a
useful subset of plugins and filters with minimal dependencies.

If you want just the server, install '%{name}-server'.

To develop plugins, install the '%{name}-devel' package and start by
reading the nbdkit(1) and nbdkit-plugin(3) manual pages.


%package server
Summary:        The %{name} server
License:        BSD

%description server
This package contains the %{name} server with only the null plugin
and no filters.  To install a basic set of plugins and filters you
need to install "nbdkit-basic-plugins", "nbdkit-basic-filters" or
the metapackage "nbdkit".


%package basic-plugins
Summary:        Basic plugins for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Provides:       %{name}-data-plugin = %{version}-%{release}
Provides:       %{name}-eval-plugin = %{version}-%{release}
Provides:       %{name}-file-plugin = %{version}-%{release}
Provides:       %{name}-floppy-plugin = %{version}-%{release}
Provides:       %{name}-full-plugin = %{version}-%{release}
Provides:       %{name}-info-plugin = %{version}-%{release}
Provides:       %{name}-memory-plugin = %{version}-%{release}
Provides:       %{name}-null-plugin = %{version}-%{release}
Provides:       %{name}-ondemand-plugin = %{version}-%{release}
Provides:       %{name}-ones-plugin = %{version}-%{release}
Provides:       %{name}-partitioning-plugin = %{version}-%{release}
Provides:       %{name}-pattern-plugin = %{version}-%{release}
Provides:       %{name}-random-plugin = %{version}-%{release}
Provides:       %{name}-sh-plugin = %{version}-%{release}
Provides:       %{name}-sparse-random-plugin = %{version}-%{release}
Provides:       %{name}-split-plugin = %{version}-%{release}
Provides:       %{name}-zero-plugin = %{version}-%{release}


%description basic-plugins
This package contains plugins for %{name} which only depend on simple
C libraries: glibc, gnutls, libzstd.  Other plugins for nbdkit with
more complex dependencies are packaged separately.

nbdkit-data-plugin          Serve small amounts of data from the command line.

nbdkit-eval-plugin          Write a shell script plugin on the command line.

nbdkit-file-plugin          The normal file plugin for serving files.

nbdkit-floppy-plugin        Create a virtual floppy disk from a directory.

nbdkit-full-plugin          A virtual disk that returns ENOSPC errors.

nbdkit-info-plugin          Serve client and server information.

nbdkit-memory-plugin        A virtual memory plugin.

nbdkit-ondemand-plugin      Create filesystems on demand.

nbdkit-ones-plugin          Fill disk with repeated 0xff or other bytes.

nbdkit-pattern-plugin       Fixed test pattern.

nbdkit-partitioning-plugin  Create virtual disks from partitions.

nbdkit-random-plugin        Random content plugin for testing.

nbdkit-sh-plugin            Write plugins as shell scripts or executables.

nbdkit-sparse-random-plugin Make sparse random disks.

nbdkit-split-plugin         Concatenate one or more files.

nbdkit-zero-plugin          Zero-length plugin for testing.


%package example-plugins
Summary:        Example plugins for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
# example4 is written in Perl.
Requires:       %{name}-perl-plugin

%description example-plugins
This package contains example plugins for %{name}.


# The plugins below have non-trivial dependencies are so are
# packaged separately.

%if %{with blkio}
%package blkio-plugin
Summary:        libblkio NVMe, vhost-user, vDPA, VFIO plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description blkio-plugin
This package contains libblkio (NVMe, vhost-user, vDPA, VFIO) support
for %{name}.
%endif


%package cc-plugin
Summary:        Write small inline C plugins and scripts for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       /bin/cat


%description cc-plugin
This package contains support for writing inline C plugins and scripts
for %{name}.  NOTE this is NOT the right package for writing plugins
in C, install %{name}-devel for that.


%if %{with cdi}
%package cdi-plugin
Summary:        Containerized Data Import plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       jq
Requires:       podman

%description cdi-plugin
This package contains Containerized Data Import support for %{name}.
%endif


%package curl-plugin
Summary:        HTTP/FTP (cURL) plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description curl-plugin
This package contains cURL (HTTP/FTP) support for %{name}.


%if 0%{?have_libguestfs}
%package guestfs-plugin
Summary:        libguestfs plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description guestfs-plugin
This package is a libguestfs plugin for %{name}.
%endif


%package iso-plugin
Summary:        Virtual ISO 9660 plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       xorriso

%description iso-plugin
This package is a virtual ISO 9660 (CD-ROM) plugin for %{name}.


%package libvirt-plugin
Summary:        Libvirt plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description libvirt-plugin
This package is a libvirt plugin for %{name}.  It lets you access
libvirt guest disks readonly.  It is implemented using the libvirt
virDomainBlockPeek API.


%package linuxdisk-plugin
Summary:        Virtual Linux disk plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
# for mke2fs
Requires:       e2fsprogs

%description linuxdisk-plugin
This package is a virtual Linux disk plugin for %{name}.


%package lua-plugin
Summary:        Lua plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description lua-plugin
This package lets you write Lua plugins for %{name}.


%package nbd-plugin
Summary:        NBD proxy / forward plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description nbd-plugin
This package lets you forward NBD connections from %{name}
to another NBD server.


%if 0%{?have_ocaml}
%package ocaml-plugin
Summary:        OCaml plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description ocaml-plugin
This package lets you run OCaml plugins for %{name}.

To compile OCaml plugins you will also need to install
%{name}-ocaml-plugin-devel.


%package ocaml-plugin-devel
Summary:        OCaml development environment for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       %{name}-ocaml-plugin%{?_isa} = %{version}-%{release}

%description ocaml-plugin-devel
This package lets you write OCaml plugins for %{name}.
%endif


%package perl-plugin
Summary:        Perl plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description perl-plugin
This package lets you write Perl plugins for %{name}.


%package python-plugin
Summary:        Python 3 plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description python-plugin
This package lets you write Python 3 plugins for %{name}.


%if %{with ruby}
%package ruby-plugin
Summary:        Ruby plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description ruby-plugin
This package lets you write Ruby plugins for %{name}.
%endif


%if %{with s3}
# In theory this is noarch, but because plugins are placed in _libdir
# which varies across architectures, RPM does not allow this.
%package S3-plugin
Summary:        Amazon S3 and Ceph plugin for %{name}
License:        BSD
Requires:       %{name}-python-plugin >= 1.22
# XXX Should not need to add this.
Requires:       python3-boto3

%description S3-plugin
This package lets you open disk images stored in Amazon S3
or Ceph using %{name}.
%endif


%package ssh-plugin
Summary:        SSH plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description ssh-plugin
This package contains SSH support for %{name}.


%package tcl-plugin
Summary:        Tcl plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description tcl-plugin
This package lets you write Tcl plugins for %{name}.


%package tmpdisk-plugin
Summary:        Remote temporary filesystem disk plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
# For mkfs and mke2fs (defaults).
Requires:       util-linux, e2fsprogs
# For other filesystems.
Suggests:       xfsprogs
Suggests:       ntfsprogs, dosfstools

%description tmpdisk-plugin
This package is a remote temporary filesystem disk plugin for %{name}.


%if %{with torrent}
%package torrent-plugin
Summary:        BitTorrent plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description torrent-plugin
This package is a BitTorrent plugin for %{name}.
%endif


%ifarch x86_64
%package vddk-plugin
Summary:        VMware VDDK plugin for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description vddk-plugin
This package is a plugin for %{name} which connects to
VMware VDDK for accessing VMware disks and servers.
%endif


%package basic-filters
Summary:        Basic filters for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Provides:       %{name}-blocksize-filter = %{version}-%{release}
Provides:       %{name}-blocksize-policy-filter = %{version}-%{release}
Provides:       %{name}-cacheextents-filter = %{version}-%{release}
Provides:       %{name}-cache-filter = %{version}-%{release}
Provides:       %{name}-checkwrite-filter = %{version}-%{release}
Provides:       %{name}-cow-filter = %{version}-%{release}
Provides:       %{name}-ddrescue-filter = %{version}-%{release}
Provides:       %{name}-delay-filter = %{version}-%{release}
Provides:       %{name}-error-filter = %{version}-%{release}
Provides:       %{name}-evil-filter = %{version}-%{release}
Provides:       %{name}-exitlast-filter = %{version}-%{release}
Provides:       %{name}-exitwhen-filter = %{version}-%{release}
Provides:       %{name}-exportname-filter = %{version}-%{release}
Provides:       %{name}-extentlist-filter = %{version}-%{release}
Provides:       %{name}-fua-filter = %{version}-%{release}
Provides:       %{name}-ip-filter = %{version}-%{release}
Provides:       %{name}-limit-filter = %{version}-%{release}
Provides:       %{name}-log-filter = %{version}-%{release}
Provides:       %{name}-luks-filter = %{version}-%{release}
Provides:       %{name}-multi-conn-filter = %{version}-%{release}
Provides:       %{name}-nocache-filter = %{version}-%{release}
Provides:       %{name}-noextents-filter = %{version}-%{release}
Provides:       %{name}-nofilter-filter = %{version}-%{release}
Provides:       %{name}-noparallel-filter = %{version}-%{release}
Provides:       %{name}-nozero-filter = %{version}-%{release}
Provides:       %{name}-offset-filter = %{version}-%{release}
Provides:       %{name}-partition-filter = %{version}-%{release}
Provides:       %{name}-pause-filter = %{version}-%{release}
Provides:       %{name}-protect-filter = %{version}-%{release}
Provides:       %{name}-rate-filter = %{version}-%{release}
Provides:       %{name}-readahead-filter = %{version}-%{release}
Provides:       %{name}-retry-filter = %{version}-%{release}
Provides:       %{name}-retry-request-filter = %{version}-%{release}
Provides:       %{name}-scan-filter = %{version}-%{release}
Provides:       %{name}-swab-filter = %{version}-%{release}
Provides:       %{name}-tls-fallback-filter = %{version}-%{release}
Provides:       %{name}-truncate-filter = %{version}-%{release}

%description basic-filters
This package contains filters for %{name} which only depend on simple
C libraries: glibc, gnutls.  Other filters for nbdkit with more
complex dependencies are packaged separately.

nbdkit-blocksize-filter    Adjust block size of requests sent to plugins.

nbdkit-blocksize-policy-filter  Set block size constraints and policy.

nbdkit-cache-filter        Server-side cache.

nbdkit-cacheextents-filter Cache extents.

nbdkit-checkwrite-filter   Check writes match contents of plugin.

nbdkit-cow-filter          Copy-on-write overlay for read-only plugins.

nbdkit-ddrescue-filter     Filter for serving from ddrescue dump.

nbdkit-delay-filter        Inject read and write delays.

nbdkit-error-filter        Inject errors.

nbdkit-evil-filter         Add random data corruption to reads.

nbdkit-exitlast-filter     Exit on last client connection.

nbdkit-exitwhen-filter     Exit gracefully when an event occurs.

nbdkit-exportname-filter   Adjust export names between client and plugin.

nbdkit-extentlist-filter   Place extent list over a plugin.

nbdkit-fua-filter          Modify flush behaviour in plugins.

nbdkit-ip-filter           Filter clients by IP address.

nbdkit-limit-filter        Limit nr clients that can connect concurrently.

nbdkit-log-filter          Log all transactions to a file.

nbdkit-luks-filter         Read and write LUKS-encrypted disks.

nbdkit-multi-conn-filter   Enable, emulate or disable multi-conn.

nbdkit-nocache-filter      Disable cache requests in the underlying plugin.

nbdkit-noextents-filter    Disable extents in the underlying plugin.

nbdkit-nofilter-filter     Passthrough filter.

nbdkit-noparallel-filter   Serialize requests to the underlying plugin.

nbdkit-nozero-filter       Adjust handling of zero requests by plugins.

nbdkit-offset-filter       Serve an offset and range.

nbdkit-partition-filter    Serve a single partition.

nbdkit-pause-filter        Pause NBD requests.

nbdkit-protect-filter      Write-protect parts of a plugin.

nbdkit-rate-filter         Limit bandwidth by connection or server.

nbdkit-readahead-filter    Prefetch data when reading sequentially.

nbdkit-retry-filter        Reopen connection on error.

nbdkit-retry-request-filter Retry single requests on error.

nbdkit-scan-filter         Prefetch data ahead of sequential reads.

nbdkit-swab-filter         Filter for swapping byte order.

nbdkit-tls-fallback-filter TLS protection filter.

nbdkit-truncate-filter     Truncate, expand, round up or round down size.


%package ext2-filter
Summary:        ext2, ext3 and ext4 filesystem support for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description ext2-filter
This package contains ext2, ext3 and ext4 filesystem support for
%{name}.


%package gzip-filter
Summary:        GZip filter for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description gzip-filter
This package is a gzip filter for %{name}.


%package stats-filter
Summary:        Statistics filter for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description stats-filter
Display statistics about operations.


%package tar-filter
Summary:        Tar archive filter for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       tar
Obsoletes:      %{name}-tar-plugin < 1.23.9-3

%description tar-filter
This package is a tar archive filter for %{name}.


%package xz-filter
Summary:        XZ filter for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}

%description xz-filter
This package is the xz filter for %{name}.


%package devel
Summary:        Development files and documentation for %{name}
License:        BSD
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files and documentation
for %{name}.  Install this package if you want to develop
plugins for %{name}.


%package bash-completion
Summary:       Bash tab-completion for %{name}
License:       BSD
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name}-server = %{version}-%{release}

%description bash-completion
Install this package if you want intelligent bash tab-completion
for %{name}.


%prep
%autosetup -p1
%if 0%{patches_touch_autotools}
autoreconf -i
%endif


%build
# Golang bindings are not enabled in the build since they don't
# need to be.  Most people would use them by copying the upstream
# package into their vendor/ directory.
export PYTHON=%{__python3}
%configure \
    --disable-static \
    --with-extra='%{name}-%{version}-%{release}' \
    --with-tls-priority=@NBDKIT,SYSTEM \
    --with-bash-completions \
    --with-curl \
    --with-gnutls \
    --with-liblzma \
    --with-libnbd \
    --with-manpages \
    --with-selinux \
    --with-ssh \
    --with-zlib \
    --enable-linuxdisk \
    --enable-python \
    --disable-golang \
    --disable-rust \
    --disable-valgrind \
%if 0%{?have_ocaml}
    --enable-ocaml \
%else
    --disable-ocaml \
%endif
    --enable-lua \
    --enable-perl \
%if %{with ruby}
    --enable-ruby \
%else
    --disable-ruby \
%endif
    --enable-tcl \
%if %{with torrent}
    --enable-torrent \
%else
    --disable-torrent \
%endif
%if %{with blkio}
    --with-libblkio \
%else
    --without-libblkio \
%endif
    --with-ext2 \
    --with-iso \
    --with-libvirt \
%ifarch x86_64
    --enable-vddk \
%else
    --disable-vddk \
%endif
%if 0%{?have_libguestfs}
    --with-libguestfs \
%else
    --without-libguestfs \
%endif
%ifarch 0%{?have_libguestfs} && %{complete_test_arches}
    --enable-libguestfs-tests \
%else
    --disable-libguestfs-tests \
%endif
    %{nil}

# Verify that it picked the correct version of Python
# to avoid RHBZ#1404631 happening again silently.
grep '^PYTHON_VERSION = 3' Makefile

%make_build


%install
%make_install

# Delete libtool crap.
find $RPM_BUILD_ROOT -name '*.la' -delete

# If cargo happens to be installed on the machine then the
# rust plugin is built.  Delete it if this happens.
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/nbdkit-rust-plugin.3*

# Remove some plugins we cannot --disable.
%if !%{with cdi}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/nbdkit-cdi-plugin.so
rm -f $RPM_BUILD_ROOT%{_mandir}/man?/nbdkit-cdi-plugin.*
%endif

%if !%{with s3}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/nbdkit-S3-plugin
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/nbdkit-S3-plugin.1*
%endif


%check
%ifnarch %{broken_test_arches}
function skip_test ()
{
    for f in "$@"; do
        rm -f "$f"
        echo 'exit 77' > "$f"
        chmod +x "$f"
    done
}

# Workaround for broken libvirt (RHBZ#1138604).
mkdir -p $HOME/.cache/libvirt

# tests/test-captive.sh is racy especially on s390x.  We need to
# rethink this test upstream.
skip_test tests/test-captive.sh

%ifarch s390x
# Temporarily kill tests/test-cache-max-size.sh since it fails
# sometimes on s390x for unclear reasons.
skip_test tests/test-cache-max-size.sh
%endif

# Temporarily kill test-nbd-tls.sh and test-nbd-tls-psk.sh
# https://www.redhat.com/archives/libguestfs/2020-March/msg00191.html
skip_test tests/test-nbd-tls.sh tests/test-nbd-tls-psk.sh

# Make sure we can see the debug messages (RHBZ#1230160).
export LIBGUESTFS_DEBUG=1
export LIBGUESTFS_TRACE=1

%make_build check
%endif


%if 0%{?have_ocaml}
%ldconfig_scriptlets plugin-ocaml
%endif


%files
# metapackage so empty


%files server
%doc README.md
%license LICENSE
%{_sbindir}/nbdkit
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/nbdkit-null-plugin.so
%dir %{_libdir}/%{name}/filters
%{_mandir}/man1/nbdkit.1*
%{_mandir}/man1/nbdkit-captive.1*
%{_mandir}/man1/nbdkit-client.1*
%{_mandir}/man1/nbdkit-loop.1*
%{_mandir}/man1/nbdkit-null-plugin.1*
%{_mandir}/man1/nbdkit-probing.1*
%{_mandir}/man1/nbdkit-protocol.1*
%{_mandir}/man1/nbdkit-service.1*
%{_mandir}/man1/nbdkit-security.1*
%{_mandir}/man1/nbdkit-tls.1*


%files basic-plugins
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-data-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-eval-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-file-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-floppy-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-full-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-info-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-memory-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-ondemand-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-ones-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-partitioning-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-pattern-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-random-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-sh-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-sparse-random-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-split-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-zero-plugin.so
%{_mandir}/man1/nbdkit-data-plugin.1*
%{_mandir}/man1/nbdkit-eval-plugin.1*
%{_mandir}/man1/nbdkit-file-plugin.1*
%{_mandir}/man1/nbdkit-floppy-plugin.1*
%{_mandir}/man1/nbdkit-full-plugin.1*
%{_mandir}/man1/nbdkit-info-plugin.1*
%{_mandir}/man1/nbdkit-memory-plugin.1*
%{_mandir}/man1/nbdkit-ondemand-plugin.1*
%{_mandir}/man1/nbdkit-ones-plugin.1*
%{_mandir}/man1/nbdkit-partitioning-plugin.1*
%{_mandir}/man1/nbdkit-pattern-plugin.1*
%{_mandir}/man1/nbdkit-random-plugin.1*
%{_mandir}/man3/nbdkit-sh-plugin.3*
%{_mandir}/man1/nbdkit-sparse-random-plugin.1*
%{_mandir}/man1/nbdkit-split-plugin.1*
%{_mandir}/man1/nbdkit-zero-plugin.1*


%files example-plugins
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-example*-plugin.so
%{_libdir}/%{name}/plugins/nbdkit-example4-plugin
%{_mandir}/man1/nbdkit-example*-plugin.1*


%if %{with blkio}
%files blkio-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-blkio-plugin.so
%{_mandir}/man1/nbdkit-blkio-plugin.1*
%endif


%files cc-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-cc-plugin.so
%{_mandir}/man3/nbdkit-cc-plugin.3*


%if %{with cdi}
%files cdi-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-cdi-plugin.so
%{_mandir}/man1/nbdkit-cdi-plugin.1*
%endif


%files curl-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-curl-plugin.so
%{_mandir}/man1/nbdkit-curl-plugin.1*


%if 0%{?have_libguestfs}
%files guestfs-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-guestfs-plugin.so
%{_mandir}/man1/nbdkit-guestfs-plugin.1*
%endif


%files iso-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-iso-plugin.so
%{_mandir}/man1/nbdkit-iso-plugin.1*


%files libvirt-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-libvirt-plugin.so
%{_mandir}/man1/nbdkit-libvirt-plugin.1*


%files linuxdisk-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-linuxdisk-plugin.so
%{_mandir}/man1/nbdkit-linuxdisk-plugin.1*


%files lua-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-lua-plugin.so
%{_mandir}/man3/nbdkit-lua-plugin.3*


%files nbd-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-nbd-plugin.so
%{_mandir}/man1/nbdkit-nbd-plugin.1*


%if 0%{?have_ocaml}
%files ocaml-plugin
%doc README.md
%license LICENSE
%{_libdir}/libnbdkitocaml.so.*

%files ocaml-plugin-devel
%{_libdir}/libnbdkitocaml.so
%{_libdir}/ocaml/NBDKit.*
%{_mandir}/man3/nbdkit-ocaml-plugin.3*
%{_mandir}/man3/NBDKit.3*
%endif


%files perl-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-perl-plugin.so
%{_mandir}/man3/nbdkit-perl-plugin.3*


%files python-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-python-plugin.so
%{_mandir}/man3/nbdkit-python-plugin.3*

%if %{with ruby}
%files ruby-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-ruby-plugin.so
%{_mandir}/man3/nbdkit-ruby-plugin.3*
%endif


%if %{with s3}
%files S3-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-S3-plugin
%{_mandir}/man1/nbdkit-S3-plugin.1*
%endif


%files ssh-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-ssh-plugin.so
%{_mandir}/man1/nbdkit-ssh-plugin.1*


%files tcl-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-tcl-plugin.so
%{_mandir}/man3/nbdkit-tcl-plugin.3*


%files tmpdisk-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-tmpdisk-plugin.so
%{_mandir}/man1/nbdkit-tmpdisk-plugin.1*


%if %{with torrent}
%files torrent-plugin
%doc README.md
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-torrent-plugin.so
%{_mandir}/man1/nbdkit-torrent-plugin.1*
%endif


%ifarch x86_64
%files vddk-plugin
%doc README.md plugins/vddk/README.VDDK
%license LICENSE
%{_libdir}/%{name}/plugins/nbdkit-vddk-plugin.so
%{_mandir}/man1/nbdkit-vddk-plugin.1*
%endif


%files basic-filters
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-blocksize-filter.so
%{_libdir}/%{name}/filters/nbdkit-blocksize-policy-filter.so
%{_libdir}/%{name}/filters/nbdkit-cache-filter.so
%{_libdir}/%{name}/filters/nbdkit-cacheextents-filter.so
%{_libdir}/%{name}/filters/nbdkit-checkwrite-filter.so
%{_libdir}/%{name}/filters/nbdkit-cow-filter.so
%{_libdir}/%{name}/filters/nbdkit-ddrescue-filter.so
%{_libdir}/%{name}/filters/nbdkit-delay-filter.so
%{_libdir}/%{name}/filters/nbdkit-error-filter.so
%{_libdir}/%{name}/filters/nbdkit-evil-filter.so
%{_libdir}/%{name}/filters/nbdkit-exitlast-filter.so
%{_libdir}/%{name}/filters/nbdkit-exitwhen-filter.so
%{_libdir}/%{name}/filters/nbdkit-exportname-filter.so
%{_libdir}/%{name}/filters/nbdkit-extentlist-filter.so
%{_libdir}/%{name}/filters/nbdkit-fua-filter.so
%{_libdir}/%{name}/filters/nbdkit-ip-filter.so
%{_libdir}/%{name}/filters/nbdkit-limit-filter.so
%{_libdir}/%{name}/filters/nbdkit-log-filter.so
%{_libdir}/%{name}/filters/nbdkit-luks-filter.so
%{_libdir}/%{name}/filters/nbdkit-multi-conn-filter.so
%{_libdir}/%{name}/filters/nbdkit-nocache-filter.so
%{_libdir}/%{name}/filters/nbdkit-noextents-filter.so
%{_libdir}/%{name}/filters/nbdkit-nofilter-filter.so
%{_libdir}/%{name}/filters/nbdkit-noparallel-filter.so
%{_libdir}/%{name}/filters/nbdkit-nozero-filter.so
%{_libdir}/%{name}/filters/nbdkit-offset-filter.so
%{_libdir}/%{name}/filters/nbdkit-partition-filter.so
%{_libdir}/%{name}/filters/nbdkit-pause-filter.so
%{_libdir}/%{name}/filters/nbdkit-protect-filter.so
%{_libdir}/%{name}/filters/nbdkit-rate-filter.so
%{_libdir}/%{name}/filters/nbdkit-readahead-filter.so
%{_libdir}/%{name}/filters/nbdkit-retry-filter.so
%{_libdir}/%{name}/filters/nbdkit-retry-request-filter.so
%{_libdir}/%{name}/filters/nbdkit-scan-filter.so
%{_libdir}/%{name}/filters/nbdkit-swab-filter.so
%{_libdir}/%{name}/filters/nbdkit-tls-fallback-filter.so
%{_libdir}/%{name}/filters/nbdkit-truncate-filter.so
%{_mandir}/man1/nbdkit-blocksize-filter.1*
%{_mandir}/man1/nbdkit-blocksize-policy-filter.1*
%{_mandir}/man1/nbdkit-cache-filter.1*
%{_mandir}/man1/nbdkit-cacheextents-filter.1*
%{_mandir}/man1/nbdkit-checkwrite-filter.1*
%{_mandir}/man1/nbdkit-cow-filter.1*
%{_mandir}/man1/nbdkit-ddrescue-filter.1*
%{_mandir}/man1/nbdkit-delay-filter.1*
%{_mandir}/man1/nbdkit-error-filter.1*
%{_mandir}/man1/nbdkit-evil-filter.1*
%{_mandir}/man1/nbdkit-exitlast-filter.1*
%{_mandir}/man1/nbdkit-exitwhen-filter.1*
%{_mandir}/man1/nbdkit-exportname-filter.1*
%{_mandir}/man1/nbdkit-extentlist-filter.1*
%{_mandir}/man1/nbdkit-fua-filter.1*
%{_mandir}/man1/nbdkit-ip-filter.1*
%{_mandir}/man1/nbdkit-limit-filter.1*
%{_mandir}/man1/nbdkit-log-filter.1*
%{_mandir}/man1/nbdkit-luks-filter.1*
%{_mandir}/man1/nbdkit-multi-conn-filter.1*
%{_mandir}/man1/nbdkit-nocache-filter.1*
%{_mandir}/man1/nbdkit-noextents-filter.1*
%{_mandir}/man1/nbdkit-nofilter-filter.1*
%{_mandir}/man1/nbdkit-noparallel-filter.1*
%{_mandir}/man1/nbdkit-nozero-filter.1*
%{_mandir}/man1/nbdkit-offset-filter.1*
%{_mandir}/man1/nbdkit-partition-filter.1*
%{_mandir}/man1/nbdkit-pause-filter.1*
%{_mandir}/man1/nbdkit-protect-filter.1*
%{_mandir}/man1/nbdkit-rate-filter.1*
%{_mandir}/man1/nbdkit-readahead-filter.1*
%{_mandir}/man1/nbdkit-retry-filter.1*
%{_mandir}/man1/nbdkit-retry-request-filter.1*
%{_mandir}/man1/nbdkit-scan-filter.1*
%{_mandir}/man1/nbdkit-swab-filter.1*
%{_mandir}/man1/nbdkit-tls-fallback-filter.1*
%{_mandir}/man1/nbdkit-truncate-filter.1*


%files ext2-filter
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-ext2-filter.so
%{_mandir}/man1/nbdkit-ext2-filter.1*


%files gzip-filter
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-gzip-filter.so
%{_mandir}/man1/nbdkit-gzip-filter.1*


%files stats-filter
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-stats-filter.so
%{_mandir}/man1/nbdkit-stats-filter.1*


%files tar-filter
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-tar-filter.so
%{_mandir}/man1/nbdkit-tar-filter.1*


%files xz-filter
%doc README.md
%license LICENSE
%{_libdir}/%{name}/filters/nbdkit-xz-filter.so
%{_mandir}/man1/nbdkit-xz-filter.1*


%files devel
%doc BENCHMARKING OTHER_PLUGINS README.md SECURITY TODO
%license LICENSE
# Include the source of the example plugins in the documentation.
%doc plugins/example*/*.c
%doc plugins/example4/nbdkit-example4-plugin
%doc plugins/lua/example.lua
%if 0%{?have_ocaml}
%doc plugins/ocaml/example.ml
%endif
%doc plugins/perl/example.pl
%doc plugins/python/examples/*.py
%doc plugins/ruby/example.rb
%doc plugins/sh/example.sh
%doc plugins/tcl/example.tcl
%{_includedir}/nbdkit-common.h
%{_includedir}/nbdkit-filter.h
%{_includedir}/nbdkit-plugin.h
%{_includedir}/nbdkit-version.h
%{_includedir}/nbd-protocol.h
%{_mandir}/man3/nbdkit-filter.3*
%{_mandir}/man3/nbdkit-plugin.3*
%{_mandir}/man1/nbdkit-release-notes-1.*.1*
%{_libdir}/pkgconfig/nbdkit.pc


%files bash-completion
%license LICENSE
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/nbdkit


%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.35.3-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue May 23 2023 Vince Perri <viperri@microsoft.com> - 1.34.1-2
- License verified.
- Removing libxcrypt-compat requirement from vddk plugin.
- Disabling torrent, S3, cdi, and blkio plugins.
- Removing torrent .so with --disable-torrent instead of rm -rf.
- Removing nbdkit-srpm-macros package after adding desired 'Provides'.
- Avoid non-zero exit from `%check` section
- Disabling plug-in for Ruby due to building issues.
- Removing in-spec verification of source tarballs.
- Making binaries paths compatible with CBL-Mariner's paths.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).

* Thu May 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.35.3-1
- New upstream development version 1.35.3
- New plugin: ones
- New filter: evil

* Wed May 10 2023 Richard W.M. Jones <rjones@redhat.com> - 1.35.2-1
- New upstream development version 1.35.2

* Sat Apr 29 2023 Richard W.M. Jones <rjones@redhat.com> - 1.35.1-1
- New upstream development version 1.35.1

* Tue Apr 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.34.1-1
- New upstream stable version 1.34.1

* Fri Apr 14 2023 Richard W.M. Jones <rjones@redhat.com> - 1.34.0-1
- New upstream stable version 1.34.0

* Thu Apr 13 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.12-1
- New upstream development version 1.33.12

* Thu Mar 09 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.11-1
- New upstream development version 1.33.11

* Tue Feb 28 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.10-1
- New upstream development version 1.33.10

* Sat Feb 25 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.9-1
- New upstream development version 1.33.9

* Tue Feb 07 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.8-1
- New upstream development version 1.33.8

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.7-3
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 14 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.7-1
- New upstream development version 1.33.7

* Wed Jan 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.6-1
- New upstream development version 1.33.6
- New plugin: nbdkit-blkio-plugin

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.33.5-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Tue Jan 03 2023 Richard W.M. Jones <rjones@redhat.com> - 1.33.5-1
- New upstream development version 1.33.5

* Sat Dec 03 2022 Richard W.M. Jones <rjones@redhat.com> - 1.33.4-1
- New upstream development version 1.33.4

* Fri Nov 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.33.3-1
- New upstream development version 1.33.3

* Tue Oct 11 2022 Richard W.M. Jones <rjones@redhat.com> - 1.33.2-1
- New upstream development version 1.33.2

* Thu Aug 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.33.1-1
- New upstream development version 1.33.1

* Thu Aug 11 2022 Richard W.M. Jones <rjones@redhat.com> - 1.32.1-1
- New upstream stable version 1.32.1

* Mon Aug 01 2022 Richard W.M. Jones <rjones@redhat.com> - 1.32.0-1
- New upstream stable version 1.32.0

* Fri Jul 29 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.15-1
- New upstream development version 1.31.15

* Sun Jul 24 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.14-1
- New upstream development version 1.31.14

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.13-1
- New upstream development version 1.31.13

* Sun Jul 17 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.12-1
- New upstream development version 1.31.12

* Sun Jul 10 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.11-1
- New upstream development version 1.31.11

* Mon Jun 27 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.10-1
- New upstream development version 1.31.10

* Mon Jun 20 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.9-3
- OCaml 4.14.0 rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.31.9-2
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.9-1
- New upstream development version 1.31.9

* Thu Jun 09 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.8-1
- New upstream development version 1.31.8
- Rename README file.

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31.7-2
- Perl 5.36 rebuild

* Thu May 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.7-1
- New upstream development version 1.31.7

* Sat May 14 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.6-1
- New upstream development version 1.31.6
- New filter: scan

* Mon May 09 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.5-1
- New upstream development version 1.31.5

* Mon May 09 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.4-1
- New upstream development version 1.31.4
- Add new luks filter.

* Sat May 07 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.3-1
- New upstream development version 1.31.3
- Stats filter is now written in C++, move to a new subpackage.

* Tue Apr 26 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.2-1
- New upstream development version 1.31.2

* Wed Apr 20 2022 Richard W.M. Jones <rjones@redhat.com> - 1.31.1-1
- New upstream development version 1.31.1

* Sat Apr 16 2022 Richard W.M. Jones <rjones@redhat.com> - 1.30.3-1
- New stable version 1.30.3
- Remove dependency on ssh-keygen which was never really used.

* Sat Apr 02 2022 Richard W.M. Jones <rjones@redhat.com> - 1.30.2-1
- New stable version 1.30.2

* Tue Mar 15 2022 Richard W.M. Jones <rjones@redhat.com> - 1.30.1-1
- New stable version 1.30.1

* Mon Feb 28 2022 Richard W.M. Jones <rjones@redhat.com> - 1.30.0-3
- Add nbdkit-srpm-macros

* Thu Feb 24 2022 Richard W.M. Jones <rjones@redhat.com> - 1.30.0-1
- New stable version 1.30.0

* Sat Feb 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.29.16-1
- New upstream development version 1.29.16
- New nbdkit-blocksize-policy-filter.

* Tue Feb 15 2022 Richard W.M. Jones <rjones@redhat.com> - 1.29.15-1
- New upstream development version 1.29.15

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.29.14-2
- F-36: rebuild against ruby31

* Thu Jan 20 2022 Richard W.M. Jones <rjones@redhat.com> - 1.29.14-1
- New upstream development version 1.29.14

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 15 2022 Richard W.M. Jones <rjones@redhat.com> - 1.29.13-1
- New upstream development version 1.29.13

* Tue Jan 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.29.12-1
- New upstream development version 1.29.12

* Sat Dec 18 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.11-1
- New upstream development version 1.29.11
- Use new --disable-libguestfs-tests on non-guestfs arches.

* Tue Dec 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.9-1
- New upstream development version 1.29.9

* Sat Dec 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.8-1
- New upstream development version 1.29.8
- Add nbdkit-protect-filter.

* Thu Nov 25 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.7-2
- Bump release and rebuild

* Tue Nov 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.7-1
- New upstream development version 1.29.7

* Fri Nov 19 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.6-1
- New upstream development version 1.29.6

* Tue Nov 09 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.5-1
- New upstream development version 1.29.5
- New minimum OCaml is 4.03

* Thu Nov 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.4-1
- New upstream development version 1.29.4
- Remove references to nbdkit-streaming-plugin (now removed upstream)
- Move nbdkit-null-plugin to the nbdkit-server package

* Tue Nov 02 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.3-2
- Switch to xorriso (instead of genisoimage)

* Thu Oct 28 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.3-1
- New upstream development version 1.29.3

* Mon Oct 25 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.2-1
- New upstream development version 1.29.2

* Tue Oct 19 2021 Richard W.M. Jones <rjones@redhat.com> - 1.29.1-1
- New upstream development version 1.29.1
- New filter: nbdkit-retry-request-filter

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.28.0-2
- OCaml 4.13.1 build

* Thu Sep 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.28.0-1
- New upstream stable branch version 1.28.0

* Tue Sep 21 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.10-1
- New upstream development version 1.27.10.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.27.9-2
- Rebuilt with OpenSSL 3.0.0

* Sat Sep  4 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.9-1
- New upstream development version 1.27.9.
- Remove patches which are upstream.

* Wed Sep  1 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.8-3
- Re-enable tests on armv7.

* Tue Aug 31 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.8-2
- Fix for qemu 6.1.

* Mon Aug 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.8-1
- New upstream development version 1.27.8.
- Remove patch which is included upstream.

* Thu Aug 19 2021 Eric Blake <eblake@redhat.com> - 1.27.7-2
- Include followup patch related to CVE-2021-3716.

* Thu Aug 19 2021 Eric Blake <eblake@redhat.com> - 1.27.7-1
- New upstream development version 1.27.7; addresses CVE-2021-3716.

* Fri Aug 13 2021 Eric Blake <eblake@redhat.com> - 1.27.5-1
- New upstream development version 1.27.5.

* Thu Aug 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.4-1
- New upstream development version 1.27.4.

* Fri Jul 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.3-1
- New upstream development version 1.27.3.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.2-1
- New upstream development version 1.27.2.

* Fri Jun 11 2021 Richard W.M. Jones <rjones@redhat.com> - 1.27.1-1
- New upstream development version 1.27.1.

* Mon Jun 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.26.0-1
- New upstream version 1.26.0.

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.25.9-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.9-1
- New upstream version 1.25.9.

* Tue May 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.25.8-2
- Perl 5.34 re-rebuild of updated packages

* Tue May 25 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.8-1
- New upstream version 1.25.8.

* Tue May 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.25.7-4
- Perl 5.34 re-rebuild updated packages

* Tue May 25 2021 Leigh Scott <leigh123linux@gmail.com> - 1.25.7-3
- Rebuild for new libtorrent

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.25.7-2
- Perl 5.34 rebuild

* Wed May 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.7-1
- New upstream version 1.25.7.
- Disable libguestfs tests on riscv64.

* Sat Apr 10 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.6-1
- New upstream version 1.25.6.

* Sat Apr 03 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.5-1
- New upstream version 1.25.5.

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.4-2
- Fix upstream URL.
- Enable non-guestfs tests on all arches.

* Wed Mar 10 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.4-1
- New upstream development version 1.25.4.
- New filter: multi-conn

* Tue Mar  9 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.3-3
- Make nbdkit-vddk-plugin depend on libxcrypt-compat (RHBZ#1931818).

* Thu Mar  4 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.3-2
- Remove socat dependency in RHEL 9.

* Tue Mar  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.3-1
- New upstream development version 1.25.3.

* Tue Mar  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-2
- OCaml 4.12.0 build (RHBZ#1934138).

* Wed Feb 03 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-1
- New upstream development version 1.25.2.
- Remove all remaining traces of nbdkit-gzip-plugin and nbdkit-tar-plugin.
- Remove nbdkit-streaming-plugin (deprecated upstream).
- Remove obsoletes of old nbdkit-ext2-plugin.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Richard W.M. Jones <rjones@redhat.com> - 1.25.1-1
- New upstream development version 1.25.1.

* Tue Jan 19 2021 Richard W.M. Jones <rjones@redhat.com> - 1.24.0-3
- Obsolete nbdkit-tar-plugin to provide smooth upgrades to F33+.

* Fri Jan 08 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.24.0-2
- F-34: rebuild against ruby 3.0

* Thu Jan 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.24.0-1
- New upstream version 1.24.0.

* Thu Jan 07 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.23.13-2
- F-34: rebuild against ruby 3.0

* Tue Dec 29 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.13-1
- New upstream development version 1.23.13.
- Add configure --with-extra.

* Tue Dec 22 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.11-1
- New upstream development version 1.23.11.
- New nbdkit-checkwrite-filter.

* Thu Dec 10 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.10-2
- Avoid boto3 dependency on RHEL.

* Tue Dec 08 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.10-1
- New upstream development version 1.23.10.
- New nbdkit-sparse-random-plugin.

* Thu Dec 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.9-2
- Move gzip and tar filters with other filters.
- Remove nbdkit-tar-plugin (replaced with nbdkit-tar-filter), except RHEL 8.
- Do not ship nbdkit-S3-plugin on RHEL.

* Thu Nov 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.9-1
- New upstream development version 1.23.9.
- Add nbdkit-S3-plugin.

* Mon Nov 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.8-1
- New upstream development version 1.23.8.
- Add nbdkit-exitwhen-filter.

* Mon Oct 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.7-1
- New upstream development version 1.23.7.
- Add new NBDKit(3) man page for the OCaml plugin.

* Tue Sep 22 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.6-1
- New upstream development version 1.23.6.
- New exportname filter.
- Add patch to fix tests.

* Wed Sep 16 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.5-1
- New upstream development version 1.23.5.

* Tue Sep 08 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.4-1
- New upstream development version 1.23.4.

* Sat Sep 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.3-1
- New upstream development version 1.23.3.

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.2-2
- OCaml 4.11.1 rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.23.2-1
- New upstream development version 1.23.2.

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.22.0-2
- Reenable sfdisk test because util-linux contains fix.

* Thu Aug 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.22.0-1
- New stable version 1.22.0.

* Mon Aug 24 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.26-2
- OCaml 4.11.0 rebuild

* Thu Aug 20 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.26-1
- New upstream version 1.21.26.

* Sun Aug 16 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.25-1
- New upstream version 1.21.25.
- New nbdkit-ondemand-plugin.
- New nbdkit-client(1) man page.

* Tue Aug 11 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.24-1
- New upstream version 1.21.24.
- Add nbdkit-tls-fallback-filter.

* Mon Aug 10 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.21.23-1
- Enable libguestfs tests only on %%{kernel_arches}

* Sat Aug  8 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.23-1
- New upstream version 1.21.23.

* Thu Aug  6 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.22-1
- New upstream version 1.21.22.
- Note this requires updated libnbd 1.3.11 because of bugs in 1.3.10.

* Tue Aug  4 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.21-1
- New upstream version 1.21.21.
- Remove patches, all upstream.

* Sat Aug  1 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.20-6
- Add upstream patches to try to track down test failure in Koji.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.20-1
- New upstream development version 1.21.20.
- Disable test-partition1.sh because of sfdisk bug.

* Tue Jul 21 2020 Tom Stellard <tstellar@redhat.com> - 1.21.19-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sat Jul 18 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.19-1
- New upstream development version 1.21.19.
- New nbdkit-cdi-plugin.

* Mon Jul 13 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.18-1
- New upstream development version 1.21.18.
- Fixes nbdkit-gzip-filter.

* Sat Jul 11 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.17-1
- New upstream development version 1.21.17.
- New nbdkit-gzip-filter.
- Remove deprecated nbdkit-gzip-plugin.

* Thu Jul  9 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.16-1
- New upstream development version 1.21.16.
- New nbdkit-tar-filter.
- nbdkit-ext2-plugin has been removed, no need to delete it.

* Mon Jul  6 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.15-1
- New upstream development version 1.21.15.
- New nbdkit-swab-filter.

* Fri Jul  3 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.14-1
- New upstream development version 1.21.14.
- New nbdkit-pause-filter.

* Mon Jun 29 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.13-1
- New upstream development version 1.21.13.
- Tar plugin rewritten again in C.
- New nbdkit-torrent-plugin.
- Remove various upgrade paths which are no longer needed in F33.

* Sat Jun 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.21.12-3
- Perl 5.32 re-rebuild updated packages

* Thu Jun 25 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.12-2
- Fix dependencies of nbdkit-tar-plugin since rewritten in Python.

* Tue Jun 23 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.12-1
- New upstream development version 1.21.12.
- Use new --disable-rust configure option.

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.21.11-2
- Perl 5.32 rebuild

* Fri Jun 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.11-1
- New upstream development version 1.21.11.

* Mon Jun 15 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.10-1
- New upstream development version 1.21.10.
- This makes nbdkit-basic-plugins depend on zstd.

* Sun Jun 14 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.9-1
- New upstream development version 1.21.9.

* Tue Jun  9 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.8-1
- New upstream development version 1.21.8.
- Remove upstream patches.

* Thu Jun  4 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.7-1
- New upstream development version 1.21.7.
- New nbdkit-cc-plugin subpackage.

* Tue Jun  2 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-1
- New upstream development version 1.21.6.

* Sat May 30 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.5-1
- New upstream development version 1.21.5.
- New ddrescue filter.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.21.4-3
- Rebuilt for Python 3.9

* Wed May 20 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.4-2
- Add upstream patch to make tests/test-truncate4.sh more stable on s390x.

* Tue May 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.4-1
- New upstream development version 1.21.4.

* Sun May 10 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.3-1
- New upstream development version 1.21.3.

* Thu May 07 2020 Richard W.M. Jones <rjones@redhat.com> - 1.21.2-1
- New upstream development version 1.21.2.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.20.1-2
- Bump and rebuild for OCaml 4.11.0+dev2-2020-04-22 rebuild.

* Mon May  4 2020 Richard W.M. Jones <rjones@redhat.com> - 1.20.1-2
- New upstream version 1.20.1.

* Sat May  2 2020 Richard W.M. Jones <rjones@redhat.com> - 1.20.0-2
- New upstream version 1.20.0.

* Thu Apr 30 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.12-1
- New upstream version 1.19.12.

* Tue Apr 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.11-1
- New upstream version 1.19.11.

* Fri Apr 24 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.10-1
- New upstream version 1.19.10.

* Thu Apr 23 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.9-1
- New upstream version 1.19.9.

* Thu Apr 16 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.8-1
- New upstream version 1.19.8.

* Wed Apr  8 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.7-1
- New upstream version 1.19.7.
- Disable VDDK on i386, support for VDDK 5.1.1 was removed upstream.

* Tue Mar 31 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.6-1
- New upstream version 1.19.6.

* Sat Mar 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.5-1
- New upstream version 1.19.5.

* Fri Mar 20 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.4-1
- New upstream version 1.19.4.

* Thu Mar 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.3-2
- Kill some upstream tests which are problematic.
- Restore test-shutdown.sh (it was renamed to test-delay-shutdown.sh)

* Tue Mar 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.3-1
- New upstream version 1.19.3.
- New plugin and subpackage: tmpdisk.

* Sat Mar 07 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.2-1
- New upstream version 1.19.2.
- New filters: exitlast, limit.

* Fri Mar 06 2020 Richard W.M. Jones <rjones@redhat.com> - 1.19.1-1
- New upstream version 1.19.1.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.18.0-1
- New upstream stable branch version 1.18.0.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.11-2
- OCaml 4.10.0 final.

* Tue Feb 25 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.11-1
- New upstream development version 1.17.11.

* Wed Feb 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.10-1
- New upstream development version 1.17.10.

* Tue Feb 18 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.9-1
- New upstream development version 1.17.9.

* Wed Feb 12 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.8-1
- New upstream development version 1.17.8.
- New filter: ext2.
- Deprecate and remove ext2 plugin.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.7-1
- New upstream development version 1.17.7.
- New filter: extentlist.

* Tue Jan 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.17.6-1
- New upstream development version 1.17.6.

* Sun Dec 15 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.5-1
- New upstream development version 1.17.5.
- Remove upstream patches.

* Sat Dec 14 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.4-2
- Improve test times.

* Fri Dec 13 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.4-1
- New upstream development version 1.17.4.
- New filter: nofilter.
- Remove upstream patches.

* Tue Dec 10 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.3-2
- New upstream development version 1.17.3.
- Add upstream patch to fix IPv6 support in tests.

* Sat Dec  7 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.2-2
- Reenable OCaml plugin on riscv64 again, should now work with 4.09.

* Tue Dec  3 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.2-1
- New upstream development version 1.17.2.
- Enable armv7 again.

* Sun Dec  1 2019 Richard W.M. Jones <rjones@redhat.com> - 1.17.1-1
- New upstream development version 1.17.1.
- Add nbdkit-eval-plugin.
- Add nbdkit-ip-filter.

* Wed Nov 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.16.0-6
- Use gpgverify macro instead of explicit gpgv2 command.

* Fri Nov 15 2019 Richard W.M. Jones <rjones@redhat.com> - 1.16.0-5
- Enable libvirt plugin on all architectures.
- Disable OCaml plugin on riscv64 temporarily.

* Thu Nov 14 2019 Richard W.M. Jones <rjones@redhat.com> - 1.16.0-1
- New stable release 1.16.0.

* Sat Nov 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.8-1
- New upstream version 1.15.8.
- Add new nbdkit-release-notes-* man pages.

* Wed Nov 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.7-1
- New upstream version 1.15.7.

* Fri Oct 25 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.6-1
- New upstream version 1.15.6.

* Sat Oct 19 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.5-1
- New upstream release 1.15.5.

* Tue Oct  1 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.4-1
- New upstream release 1.15.4.
- New nbdkit-security(1) man page.
- Rename nbdkit-reflection-plugin to nbdkit-info-plugin.

* Wed Sep 25 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.3-1
- New upstream release 1.15.3.
- Add new header file nbd-protocol.h to devel subpackage.

* Fri Sep 20 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.2-1
- New upstream version 1.15.2.
- Fixes second Denial of Service attack:
  https://www.redhat.com/archives/libguestfs/2019-September/msg00272.html
- Add new nbdkit-reflection-plugin.
- Add new nbdkit-retry-filter.

* Thu Sep 12 2019 Richard W.M. Jones <rjones@redhat.com> - 1.15.1-1
- New upstream version 1.15.1.
- Fixes Denial of Service / Amplication Attack:
  https://www.redhat.com/archives/libguestfs/2019-September/msg00084.html
- Add nbdsh BR for tests.
- Package <nbdkit-version.h>.

* Thu Aug 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.14.0-2
- Split out nbdkit-nbd-plugin subpackage.

* Wed Aug 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1.14.0-1
- New upstream version 1.14.0.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.9-3
- Temporarily kill tests/test-shutdown.sh

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 1.13.9-2
- Rebuilt for Python 3.8

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.9-1
- New upstream version 1.13.9.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.8-7
- Add provides for all basic plugins and filters.

* Tue Aug 20 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.8-5
- BR libnbd 0.9.8.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.13.8-4
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.8-3
- Fix for libnbd 0.9.8.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.13.8-2
- Rebuilt for Python 3.8

* Fri Aug  2 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.8-1
- New upstream version 1.13.8.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.7-2
- Add upstream patch to deal with qemu-img 4.1 output change.

* Tue Jul 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.7-1
- New upstream version 1.13.7.

* Fri Jul 26 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.6-1
- New upstream version 1.13.6.
- Add BR libnbd-devel.
- New filter: cacheextents.
- Disable guestfs plugin on i686.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.5-2
- Further fix for Python 3.8 embed brokenness.

* Sun Jun 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.5-1
- New upstream version 1.13.5.

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.13.4-2
- Perl 5.30 rebuild

* Tue May 21 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.4-1
- New upstream version 1.13.4.
- Add new filters: nocache, noparallel.

* Sat Apr 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.3-1
- New upstream version 1.13.3.
- Add OCaml example to devel subpackage.

* Wed Apr 24 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.2-1
- New upstream version 1.13.2.

* Tue Apr 23 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.1-1
- New upstream version 1.13.1.
- Distribute BENCHMARKING and SECURITY files.
- Includes a fix for possible remote memory heap leak with user plugins.

* Sat Apr 13 2019 Richard W.M. Jones <rjones@redhat.com> - 1.13.0-1
- New upstream version 1.13.0.
- Add stats filter.

* Wed Apr 10 2019 Richard W.M. Jones <rjones@redhat.com> - 1.12.0-1
- New upstream version 1.12.0.
- Add noextents filter.

* Mon Apr 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.15-1
- New upstream version 1.11.15.

* Sat Apr 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.14-1
- New upstream version 1.11.14.
- Remove deprecated nbdkit-xz-plugin (replaced by nbdkit-xz-filter).

* Tue Apr 02 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.13-1
- New upstream version 1.11.13.

* Tue Apr 02 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.12-1
- New upstream version 1.11.12.
- New nbdkit-readahead-filter.

* Fri Mar 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.11-1
- New upstream version 1.11.11.

* Thu Mar 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.10-1
- New upstream version 1.11.10.

* Sat Mar 23 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.9-1
- New upstream version 1.11.9.

* Tue Mar 12 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.8-1
- New upstream version 1.11.8.

* Thu Mar 07 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.7-3
- Remove Python 2 plugin completely.
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Mar 07 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.7-2
- Remove Provides/Obsoletes in Fedora 31.
- Remove workaround for QEMU bug which is fixed in Fedora 30+.
- Make the tests run in parallel, otherwise they are too slow.

* Thu Mar 07 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.7-1
- New upstream version 1.11.7.
- Add nbdkit ssh plugin.
- Remove patches already upstream.

* Tue Mar 05 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.6-2
- Add nbdkit rate filter.

* Fri Mar 01 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.6-1
- New upstream version 1.11.6.
- Add linuxdisk plugin.
- Remove rust plugin if compiled.

* Tue Feb 05 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.5-1
- New upstream version 1.11.5.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.4-1
- New upstream version 1.11.4.

* Mon Jan 28 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.3-1
- New upstream version 1.11.3.

* Thu Jan 24 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.2-2
- F-30: rebuild against ruby26

* Thu Jan 24 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.2-1
- New upstream version 1.11.2.
- Drop patches included in upstream tarball.

* Thu Jan 24 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.1-2
- F-30: rebuild again against ruby26

* Tue Jan 22 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.1-1
- New upstream version 1.11.1.

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.0-2
- F-30: rebuild against ruby26

* Fri Jan 18 2019 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-1
- New upstream version 1.10.0.

* Tue Jan 15 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.10-1
- New upstream version 1.9.10.

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.9.9-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Jan  7 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.9-1
- New upstream version 1.9.9.

* Tue Jan  1 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.8-1
- New upstream version 1.9.8.

* Mon Dec 17 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.7-2
- Remove misguided LDFLAGS hack which removed server hardening.
  https://bugzilla.redhat.com/show_bug.cgi?id=1624149#c6

* Sat Dec 15 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.7-1
- New upstream version 1.9.7.

* Thu Dec 13 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-1
- New upstream version 1.9.6.
- Add nbdkit-full-plugin.

* Mon Dec 10 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.5-1
- New upstream version 1.9.5.

* Tue Dec 04 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.4-1
- New upstream version 1.9.4.
- Fix low priority security issue with TLS:
  https://www.redhat.com/archives/libguestfs/2018-December/msg00047.html
- New man page nbdkit-loop(1).

* Thu Nov 29 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.3-1
- New upstream version 1.9.3.

* Thu Nov 22 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-1
- New upstream version 1.9.2.
- Add new filter subpackage: nbdkit-xz-filter.
- Deprecate (but do not remove) nbdkit-xz-plugin.

* Sun Nov 18 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-1
- New upstream version 1.9.1.

* Wed Nov 14 2018 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-1
- New upstream version 1.9.0.
- New development branch.

* Mon Nov 12 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-1
- New stable branch version 1.8.0.

* Fri Nov 09 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.10-1
- New upstream version 1.7.10, possibly final before 1.8.

* Tue Nov 06 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.9-2
- nbdkit metapackage should depend on versioned -server subpackage etc.

* Tue Nov 06 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.9-1
- New upstream version 1.7.9.

* Tue Oct 30 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.8-1
- New upstream version 1.7.8.

* Mon Oct 29 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.7-1
- New upstream version 1.7.7.
- New nbdkit-floppy-plugin subpackage.

* Wed Oct 17 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.6-1
- New upstream version 1.7.6.
- New nbdkit-iso-plugin subpackage.

* Tue Oct 16 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-1
- New upstream version 1.7.5.

* Tue Oct  2 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-1
- New upstream version 1.7.4.

* Tue Sep 18 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-1
- New upstream version 1.7.3.
- Add partitioning plugin.

* Thu Sep 13 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.2-1
- New upstream version 1.7.2.

* Mon Sep 10 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-1
- New upstream version 1.7.1.

* Sat Sep 08 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-1
- New upstream version 1.7.0, development branch.
- Add nbdkit-sh-plugin.

* Tue Aug 28 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.0-1
- New upstream version 1.6.0, stable branch.

* Mon Aug 27 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.10-3
- New upstream version 1.5.10.
- Add upstream patches after 1.5.10.

* Sun Aug 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.9-2
- New upstream version 1.5.9.
- Add upstream patches since 1.5.9 was released.

* Tue Aug 21 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.8-1
- New upstream version 1.5.8.

* Sat Aug 18 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.7-1
- New upstream version 1.5.7.

* Sat Aug 18 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.6-2
- Disable libvirt on riscv64.
- Other simplifications to %%configure line.

* Thu Aug 16 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.6-1
- New upstream version 1.5.6.

* Tue Aug 14 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-2
- Make nbdkit a metapackage.
- Package server in nbdkit-server subpackage.
- Rename all nbdkit-plugin-FOO to nbdkit-FOO-plugin to match upstream.

* Mon Aug 13 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-1
- New upstream version 1.5.5.
- New plugin: data.

* Mon Aug  6 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.4-1
- New upstream version 1.5.4.
- Add topic man pages.

* Mon Aug  6 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.3-1
- New upstream version 1.5.3.
- New filter: error.

* Wed Aug  1 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-1
- New upstream version 1.5.2.
- Remove patches which are all upstream.
- New filter: truncate.

* Tue Jul 24 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- Enable VDDK plugin on x86-64 only.

* Fri Jul 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- Remove patches, all upstream in this version.
- Small refactorings in the spec file.

* Sun Jul 15 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-3
- Add all upstream patches since 1.5.0.
- New pattern plugin.
- Add fixes for 32 bit platforms i686 and armv7.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul  7 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-1
- New upstream version 1.5.0.
- Add Lua plugin and nbdkit-plugin-lua subpackage.
- Make python-unversioned-command dependent on Fedora >= 29.

* Fri Jul  6 2018 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-1
- New upstream version 1.4.0.
- Add nbdkit-plugin-tcl subpackage.
- +BR python-unversioned-command

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1.3.4-4
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.4-3
- Rebuilt for Python 3.7

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.3.4-2
- Perl 5.28 rebuild

* Sat Jun 23 2018 Richard W.M. Jones <rjones@redhat.com> - 1.3.4-1
- New upstream version 1.3.4.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.3-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- New plugins: nbdkit-zero-plugin, nbdkit-random-plugin.
- Remove upstream patches.

* Sat Jun  9 2018 Richard W.M. Jones <rjones@redhat.com> - 1.3.2-2
- New upstream version 1.3.2.
- Remove patches now upstream.
- New ext2 plugin and subpackage, requires e2fsprogs-devel to build.
- Enable tarball signatures.
- Add upstream patch to fix tests when guestfish not available.
- Enable bash tab completion.

* Wed Jun  6 2018 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- Add patch to work around libvirt problem with relative socket paths.
- Add patch to fix the xz plugin test with recent guestfish.

* Fri Apr  6 2018 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-1
- Move to development branch version 1.3.0.
- New filters: blocksize, fua, log, nozero.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.28-5
- Escape macros in changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.28-3
- Switch to %%ldconfig_scriptlets

* Fri Jan 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1.1.28-2
- Run a simplified test suite on all arches.

* Mon Jan 22 2018 Richard W.M. Jones <rjones@redhat.com> - 1.1.28-1
- New upstream version 1.1.28.
- Add two new filters to nbdkit-basic-filters.

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.1.27-2
- Rebuilt for switch to libxcrypt

* Sat Jan 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.1.27-1
- New upstream version 1.1.27.
- Add new subpackage nbdkit-basic-filters containing new filters.

* Thu Jan 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.1.26-2
- Rebuild against updated Ruby.

* Sat Dec 23 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.26-1
- New upstream version 1.1.26.
- Add new pkg-config file and dependency.

* Wed Dec 06 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.25-1
- New upstream version 1.1.25.

* Tue Dec 05 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-1
- New upstream version 1.1.24.
- Add tar plugin (new subpackage nbdkit-plugin-tar).

* Tue Dec 05 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.23-1
- New upstream version 1.1.23.
- Add example4 plugin.
- Python3 tests require libguestfs so disable on s390x.

* Sun Dec 03 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.22-1
- New upstream version 1.1.22.
- Enable tests on Fedora.

* Sat Dec 02 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.20-1
- New upstream version 1.1.20.
- Add nbdkit-split-plugin to basic plugins.

* Sat Dec 02 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.19-2
- OCaml 4.06.0 rebuild.

* Thu Nov 30 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.19-1
- New upstream version 1.1.19.
- Combine all the simple plugins in %%{name}-basic-plugins.
- Add memory and null plugins.
- Rename the example plugins subpackage.
- Use %%license instead of %%doc for license file.
- Remove patches now upstream.

* Wed Nov 29 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.18-4
- Fix Python 3 builds / RHEL macros (RHBZ#1404631).

* Tue Nov 21 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.18-3
- New upstream version 1.1.18.
- Add NBD forwarding plugin.
- Add libselinux-devel so that SELinux support is enabled in the daemon.
- Apply all patches from upstream since 1.1.18.

* Fri Oct 20 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.16-2
- New upstream version 1.1.16.
- Disable python3 plugin on RHEL/EPEL <= 7.
- Only ship on x86_64 in RHEL/EPEL <= 7.

* Wed Sep 27 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.15-1
- New upstream version 1.1.15.
- Enable TLS support.

* Fri Sep 01 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.14-1
- New upstream version 1.1.14.

* Fri Aug 25 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.13-1
- New upstream version 1.1.13.
- Remove patches which are all upstream.
- Remove grubby hack, should not be needed with modern supermin.

* Sat Aug 19 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-13
- Rebuild for OCaml 4.05.0.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-10
- Rebuild for OCaml 4.04.2.

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.12-9
- Perl 5.26 rebuild

* Mon May 15 2017 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-8
- Rebuild for OCaml 4.04.1.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Vít Ondruch <vondruch@redhat.com> - 1.1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Fri Dec 23 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-5
- Rebuild for Python 3.6 update.

* Wed Dec 14 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-4
- Fix python3 subpackage so it really uses python3 (RHBZ#1404631).

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-3
- Rebuild for OCaml 4.04.0.

* Mon Oct 03 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-2
- Compile Python 2 and Python 3 versions of the plugin.

* Wed Jun 08 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.12-1
- New upstream version 1.1.12
- Enable Ruby plugin.
- Disable tests on Rawhide because libvirt is broken again (RHBZ#1344016).

* Wed May 25 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-10
- Add another upstream patch since 1.1.11.

* Mon May 23 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-9
- Add all patches upstream since 1.1.11 (fixes RHBZ#1336758).

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.11-7
- Perl 5.24 rebuild

* Wed Mar 09 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-6
- When tests fail, dump out test-suite.log so we can debug it.

* Fri Feb 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-5
- Don't run tests on x86, because kernel is broken there
  (https://bugzilla.redhat.com/show_bug.cgi?id=1302071)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-3
- Add support for newstyle NBD protocol (RHBZ#1297100).

* Sat Oct 31 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.11-1
- New upstream version 1.1.11.

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.10-3
- OCaml 4.02.3 rebuild.

* Sat Jun 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.10-2
- Enable libguestfs plugin on aarch64.

* Fri Jun 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.10-1
- New upstream version.
- Enable now working OCaml plugin (requires OCaml >= 4.02.2).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.9-5
- Perl 5.22 rebuild

* Wed Jun 10 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.9-4
- Enable debugging messages when running make check.

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.9-3
- Perl 5.22 rebuild

* Tue Oct 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.9-2
- New upstream version 1.1.9.
- Add the streaming plugin.
- Include fix for streaming plugin in 1.1.9.

* Wed Sep 10 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.8-4
- Rebuild for updated Perl in Rawhide.
- Workaround for broken libvirt (RHBZ#1138604).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.8-1
- New upstream version 1.1.8.
- Add support for cURL, and new nbdkit-plugin-curl package.

* Fri Jun 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- New upstream version 1.1.7.
- Remove patches which are now all upstream.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 06 2014 Dan Horák <dan[at]danny.cz> - 1.1.6-4
- libguestfs is available only on selected arches

* Fri Feb 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-3
- Backport some upstream patches, fixing a minor bug and adding more tests.
- Enable the tests since kernel bug is fixed.

* Sun Feb 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- New upstream version 1.1.6.

* Sat Feb 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-2
- New upstream version 1.1.5.
- Enable the new Python plugin.
- Perl plugin man page moved to section 3.
- Perl now requires ExtUtils::Embed.

* Mon Feb 10 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.4-1
- New upstream version 1.1.4.
- Enable the new Perl plugin.

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-1
- New upstream version 1.1.3 which fixes some test problems.
- Disable tests because Rawhide kernel is broken (RHBZ#991808).
- Remove a single quote from description which confused emacs.
- Remove patch, now upstream.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Fix segfault when IPv6 client is used (RHBZ#986601).

* Tue Jul 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- New development version 1.1.2.
- Disable the tests on Fedora <= 18.

* Tue Jun 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-1
- New development version 1.1.1.
- Add libguestfs plugin.
- Run the test suite.

* Mon Jun 24 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-4
- Initial release.
