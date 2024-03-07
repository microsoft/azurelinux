%define majmin %(echo %{version} | cut -d. -f1-2)

# Architectures on which golang works.
#% global golang_arches aarch64 % {arm} % {ix86} x86_64
# In theory the above, in practice golang is so often broken that
# I now disable it:
%global golang_arches NONE

# Architectures that we run the basic sanity-check test.
#
# Currently the basic sanity check is *broken* on:
#
# aarch64: "MSI is not supported by interrupt controller" (RHBZ#1414081)
%global test_arches x86_64

# If there are patches which touch autotools files, set this to 1.
%global patches_touch_autotools 1

%bcond_without appliances

%bcond_with php
%bcond_with inspect-icons
%bcond_with man-pages

Summary:        Access and modify virtual machine disk images
Name:           libguestfs
Version:        1.44.0
Release:        18%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Source and patches.
URL:            https://libguestfs.org/
Source0:        https://libguestfs.org/download/%{majmin}-stable/%{name}-%{version}.tar.gz
# Replacement README file.
Source4:        README-replacement.in
# Guestfish colour prompts.
Source5:        guestfish.sh
# Used to build the supermin appliance in Koji.
Source6:        yum.conf.in
# Maintainer script which helps with handling patches.
Source8:        copy-patches.sh
# Build cache RPMS configuration for tdnf downloading
# This is a copy of toolkit/resources/manifests/package/local.repo
Source9:        tdnf-build-cache.repo
# Upstream patches not present in 1.44.0
Patch0:         libguestfs-ocaml413compat.patch
Patch1:         libguestfs-config-rpm.patch
Patch2:         libguestfs-file-5.40.patch

BuildRequires:  %{_bindir}/ping
BuildRequires:  %{_bindir}/pod2text
BuildRequires:  %{_bindir}/wget
# Build requirements for the appliance.
#
# Get the initial list by doing:
#   for f in $(cat appliance/packagelist); do echo $f; done | sort -u
# However you have to edit the list down to packages which exist in
# current Mariner, since supermin ignores non-existent packages.
BuildRequires:  acl
BuildRequires:  attr
BuildRequires:  augeas-devel >= 1.7.0
BuildRequires:  augeas-libs
BuildRequires:  bash
BuildRequires:  bash-completion
BuildRequires:  binutils
BuildRequires:  bison
BuildRequires:  btrfs-progs
BuildRequires:  bzip2
BuildRequires:  coreutils
BuildRequires:  cpio
BuildRequires:  createrepo_c
BuildRequires:  cryptsetup
BuildRequires:  curl
BuildRequires:  dhclient
BuildRequires:  diffutils
BuildRequires:  dosfstools
BuildRequires:  e2fsprogs
BuildRequires:  file
BuildRequires:  file-devel
BuildRequires:  findutils
BuildRequires:  flex
BuildRequires:  fuse
BuildRequires:  fuse-devel
BuildRequires:  gawk
# Basic build requirements for the library and virt tools.
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gdisk
BuildRequires:  genisoimage
BuildRequires:  gfs2-utils
BuildRequires:  glibc-static >= 2.35-6%{?dist}
BuildRequires:  gobject-introspection-devel
BuildRequires:  gperf
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  hivex
BuildRequires:  hivex-devel >= 1.3.10
BuildRequires:  iproute
BuildRequires:  iputils
BuildRequires:  jansson-devel
BuildRequires:  kernel
BuildRequires:  kmod
BuildRequires:  kpartx
BuildRequires:  less
BuildRequires:  libacl-devel
BuildRequires:  libcap
BuildRequires:  libcap-devel
BuildRequires:  libconfig-devel
BuildRequires:  libdb-utils
BuildRequires:  libldm
BuildRequires:  libldm-devel
BuildRequires:  libselinux
BuildRequires:  libselinux-devel
BuildRequires:  libselinux-utils
BuildRequires:  libtirpc-devel
BuildRequires:  libvirt-daemon-kvm >= 5.3.0
BuildRequires:  libvirt-devel
BuildRequires:  libxml2
BuildRequires:  libxml2-devel
BuildRequires:  lsof
BuildRequires:  lsscsi
BuildRequires:  lua
BuildRequires:  lua-devel
BuildRequires:  lvm2
BuildRequires:  lzop
BuildRequires:  make
BuildRequires:  mdadm
BuildRequires:  ntfs-3g
BuildRequires:  ntfs-3g-system-compression
BuildRequires:  ntfsprogs
# For language bindings.
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-gettext-devel
BuildRequires:  ocaml-hivex-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-ounit-devel
BuildRequires:  openssh-clients
BuildRequires:  parted
BuildRequires:  pciutils
BuildRequires:  pcre
BuildRequires:  pcre-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-libintl-perl
BuildRequires:  perl-macros
BuildRequires:  policycoreutils
BuildRequires:  procps
BuildRequires:  psmisc
BuildRequires:  python3-devel
BuildRequires:  python3-libvirt
BuildRequires:  qemu-img
BuildRequires:  qemu-kvm
BuildRequires:  readline-devel
BuildRequires:  rpcgen
BuildRequires:  rsync
BuildRequires:  ruby-devel
BuildRequires:  rubygem-rake
BuildRequires:  scrub
BuildRequires:  sed
BuildRequires:  sleuthkit
BuildRequires:  squashfs-tools
BuildRequires:  strace
BuildRequires:  supermin-devel >= 5.1.18
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  systemd-units
BuildRequires:  tar
BuildRequires:  tdnf
BuildRequires:  udev
BuildRequires:  unzip
BuildRequires:  util-linux
BuildRequires:  vala
BuildRequires:  vim
BuildRequires:  which
BuildRequires:  xfsprogs
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  yajl
BuildRequires:  zerofree
BuildRequires:  zip
BuildRequires:  perl(Expect)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Sys::Virt)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(Win::Hivex)
BuildRequires:  perl(Win::Hivex::Regedit)
BuildRequires:  rubygem(irb)
# json is not pulled in automatically, see RHBZ#1325022
BuildRequires:  rubygem(json)
BuildRequires:  rubygem(rdoc)
BuildRequires:  rubygem(test-unit)

%if 0%{patches_touch_autotools}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libtool
%endif

%if %{with_check}
BuildRequires:  git
%endif

%if %{with man-pages}
BuildRequires:  po4a
%endif

%if %{with inspect-icons}
BuildRequires:  icoutils
BuildRequires:  netpbm-progs
%endif

%if %{with php}
BuildRequires:  php-devel
%endif

%ifarch %{golang_arches}
BuildRequires:  golang
%endif

%ifarch x86_64
BuildRequires:  syslinux
BuildRequires:  syslinux-devel
%endif

%ifnarch aarch64
BuildRequires:  zfs-fuse
%endif

# For core disk-create API.
Requires:       qemu-img
# The daemon dependencies are not included automatically, because it
# is buried inside the appliance, so list them here.
Requires:       augeas-libs >= 1.7.0
# For core mount-local (FUSE) API.
Requires:       fuse
Requires:       hivex >= 1.3.10
Requires:       libacl
Requires:       libcap
# For core inspection API.
Requires:       libdb-utils
Requires:       libselinux
Requires:       libvirt-daemon-driver-qemu
Requires:       libvirt-daemon-driver-secret
Requires:       libvirt-daemon-kvm >= 5.3.0
Requires:       pcre
# For qemu direct and libvirt backends.
Requires:       qemu-kvm-core
# For building the appliance.
Requires:       supermin >= 5.1.18
Requires:       systemd-libs
Requires:       yajl

%ifarch aarch64
#Requires:       edk2-aarch64
%endif

Recommends:     libvirt-daemon-config-network
Recommends:     libvirt-daemon-driver-storage-core
Recommends:     selinux-policy

Suggests:       qemu-block-curl
Suggests:       qemu-block-gluster
Suggests:       qemu-block-iscsi
Suggests:       qemu-block-rbd
Suggests:       qemu-block-ssh

Provides:       bundled(gnulib)

# Filter perl provides.
%{?perl_default_filter}

# Unbreak the linker.
%undefine _strict_symbol_defs_build

%description
Libguestfs is a library for accessing and modifying virtual machine
disk images.  http://libguestfs.org

It can be used to make batch configuration changes to guests, get disk
used/free statistics (virt-df), perform backups and guest clones,
change registry/UUID/hostname info, build guests from scratch
(virt-builder) and much more.

Libguestfs uses Linux kernel and qemu code, and can access any type of
guest filesystem that Linux and qemu can, including but not limited
to: ext2/3/4, btrfs, FAT and NTFS, LVM, many different disk partition
schemes, qcow, qcow2, vmdk.

Libguestfs is split into several subpackages.  The basic subpackages are:

               libguestfs  C library
         libguestfs-tools  virt-* tools, guestfish and guestmount (FUSE)
       libguestfs-tools-c  only the subset of virt tools written in C
                             (for reduced dependencies)
                 virt-dib  safe and secure diskimage-builder replacement

For enhanced features, install:

     libguestfs-forensics  adds filesystem forensics support
          libguestfs-gfs2  adds Global Filesystem (GFS2) support
 libguestfs-inspect-icons  adds support for inspecting guest icons
        libguestfs-rescue  enhances virt-rescue shell with more tools
         libguestfs-rsync  rsync to/from guest filesystems
           libguestfs-xfs  adds XFS support
           libguestfs-zfs  adds ZFS support

For developers:

         libguestfs-devel  C/C++ header files and library

Language bindings:

 libguestfs-gobject-devel  GObject bindings and GObject Introspection
%ifarch %{golang_arches}
           golang-guestfs  Go language bindings
%endif
              lua-guestfs  Lua bindings
   ocaml-libguestfs-devel  OCaml bindings
         perl-Sys-Guestfs  Perl bindings
%if %{with php}
           php-libguestfs  PHP bindings
%endif
       python3-libguestfs  Python 3 bindings
          ruby-libguestfs  Ruby bindings
          libguestfs-vala  Vala language bindings

%package devel
Summary:        Development tools and libraries for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-tools-c = %{version}-%{release}
Requires:       pkg-config
# For libguestfs-make-fixed-appliance.
Requires:       xz

%description devel
%{name}-devel contains development tools and libraries
for %{name}.

%package forensics
Summary:        Filesystem forensics support for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description forensics
This adds filesystem forensics support to %{name}.  Install it if you
want to forensically analyze disk images using The Sleuth Kit.

%package gfs2
Summary:        GFS2 support for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gfs2
This adds GFS2 support to %{name}.  Install it if you want to process
disk images containing GFS2.Exiting due to strict setting

%package rescue
Summary:        Additional tools for virt-rescue
License:        LGPLv2+

Requires:       %{name}-tools-c = %{version}-%{release}

%description rescue
This adds additional tools to use inside the virt-rescue shell,
such as ssh, network utilities, editors and debugging utilities.

%package rsync
Summary:        rsync support for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description rsync
This adds rsync support to %{name}.  Install it if you want to use
rsync to upload or download files into disk images.

%package xfs
Summary:        XFS support for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description xfs
This adds XFS support to %{name}.  Install it if you want to process
disk images containing XFS.

%ifnarch aarch64
%package zfs
Summary:        ZFS support for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description zfs
This adds ZFS support to %{name}.  Install it if you want to process
disk images containing ZFS.
%endif


%if %{with inspect-icons}
%package inspect-icons
Summary:        Additional dependencies for inspecting guest icons
License:        LGPLv2+

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Requires:       icoutils
Requires:       netpbm-progs

%description inspect-icons
%{name}-inspect-icons is a metapackage that pulls in additional
dependencies required by libguestfs to pull icons out of non-Linux
guests.  Install this package if you want libguestfs to be able to
inspect non-Linux guests and display icons from them.

The only reason this is a separate package is to avoid core libguestfs
having to depend on Perl.  See https://bugzilla.redhat.com/1194158
%endif


%package tools-c
Summary:        System administration tools for virtual machines
License:        GPLv2+

Requires:       %{_bindir}/hexedit
Requires:       %{_bindir}/less
Requires:       %{_bindir}/man
Requires:       %{_bindir}/vi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       curl
# For virt-builder:
Requires:       gnupg2
Requires:       xz

Recommends:     libguestfs-xfs

# For virt-builder-repository:
Suggests:       osinfo-db
# For virt-edit and virt-customize:
Suggests:       perl

%description tools-c
This package contains miscellaneous system administrator command line
tools for virtual machines.

Note that you should install %{name}-tools (which pulls in
this package).  This package is only used directly when you want
to avoid dependencies on Perl.

%package tools
Summary:        System administration tools for virtual machines
License:        GPLv2+

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-tools-c = %{version}-%{release}

%description tools
This package contains miscellaneous system administrator command line
tools for virtual machines.

Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.

The guestmount command lets you mount guest filesystems on the host
using FUSE and %{name}.

Virt-alignment-scan scans virtual machines looking for partition
alignment problems.

Virt-builder is a command line tool for rapidly making disk images
of popular free operating systems.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-copy-in and virt-copy-out are command line tools for uploading
and downloading files and directories to and from virtual machines.

Virt-customize is a command line tool for customizing virtual machine
disk images.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-diff shows the differences between virtual machines.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-filesystems is a command line tool to display the filesystems,
partitions, block devices, LVs, VGs and PVs found in a disk image
or virtual machine.  It replaces the deprecated programs
virt-list-filesystems and virt-list-partitions with a much more
capable tool.

Virt-format is a command line tool to erase and make blank disks.

Virt-get-kernel extracts a kernel/initrd from a disk image.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-log is a command line tool to display the log files from a
virtual machine.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-make-fs is a command line tool to build a filesystem out of
a collection of files or a tarball.

Virt-rescue provides a rescue shell for making interactive,
unstructured fixes to virtual machines.

Virt-resize can resize existing virtual machine disk images.

Virt-sparsify makes virtual machine disk images sparse (thin-provisioned).

Virt-sysprep lets you reset or unconfigure virtual machines in
preparation for cloning them.

Virt-tail follows (tails) a log file within a guest, like 'tail -f'.

Virt-tar-in and virt-tar-out are archive, backup and upload tools
for virtual machines.  These replace the deprecated program virt-tar.

Virt-win-reg lets you look at and modify the Windows Registry of
Windows virtual machines.

%package -n virt-dib
Summary:        Safe and secure diskimage-builder replacement
License:        GPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n virt-dib
Virt-dib is a safe and secure alternative to the OpenStack
diskimage-builder command.  It is compatible with most
diskimage-builder elements.

%package bash-completion
Summary:        Bash tab-completion scripts for %{name} tools
License:        LGPLv2+

BuildArch:      noarch

Requires:       %{name}-tools-c = %{version}-%{release}
Requires:       bash-completion >= 2.0

%description bash-completion
Install this package if you want intelligent bash tab-completion
for guestfish, guestmount and various virt-* tools.

%package -n ocaml-%{name}
Summary:        OCaml bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.

%package -n ocaml-%{name}-devel
Summary:        OCaml bindings for %{name}
License:        LGPLv2+

Requires:       ocaml-%{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.

%package -n perl-Sys-Guestfs
Summary:        Perl bindings for %{name} (Sys::Guestfs)
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description -n perl-Sys-Guestfs
perl-Sys-Guestfs contains Perl bindings for %{name} (Sys::Guestfs).

%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary:        Python 3 bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
python3-%{name} contains Python 3 bindings for %{name}.

%package -n ruby-%{name}
Summary:        Ruby bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ruby
Requires:       ruby(release)

Provides:       ruby(guestfs) = %{version}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.

%if %{with php}
%package -n php-%{name}
Summary:        PHP bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       php(api) = %{php_core_api}
Requires:       php(zend-abi) = %{php_zend_api}

%description -n php-%{name}
php-%{name} contains PHP bindings for %{name}.
%endif

%package -n lua-guestfs
Summary:        Lua bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       lua

%description -n lua-guestfs
lua-guestfs contains Lua bindings for %{name}.

%package gobject
Summary:        GObject bindings for %{name}
License:        LGPLv2+

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gobject
%{name}-gobject contains GObject bindings for %{name}.

To develop software against these bindings, you need to install
%{name}-gobject-devel.

%package gobject-devel
Summary:        GObject bindings for %{name}
License:        LGPLv2+

Requires:       %{name}-gobject = %{version}-%{release}

%description gobject-devel
%{name}-gobject contains GObject bindings for %{name}.

This package is needed if you want to write software using the
GObject bindings.  It also contains GObject Introspection information.

%package vala
Summary:        Vala for %{name}
License:        LGPLv2+

Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       vala

%description vala
%{name}-vala contains GObject bindings for %{name}.

%ifarch %{golang_arches}
%package -n golang-guestfs
Summary:        Golang bindings for %{name}
License:        LGPLv2+

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}
Requires:       golang

Provides:       golang(libguestfs.org) = %{version}-%{release}

%description -n golang-guestfs
golang-%{name} contains Go language bindings for %{name}.
%endif

%if %{with man-pages}
%package man-pages-ja
Summary:        Japanese (ja) man pages for %{name}
License:        LGPLv2+

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description man-pages-ja
%{name}-man-pages-ja contains Japanese (ja) man pages
for %{name}.

%package man-pages-uk
Summary:        Ukrainian (uk) man pages for %{name}
License:        LGPLv2+

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description man-pages-uk
%{name}-man-pages-uk contains Ukrainian (uk) man pages
for %{name}.
%endif

%prep
%autosetup -p1

%if 0%{patches_touch_autotools}
autoreconf -i
%endif

# For sVirt to work, the local temporary directory we use in the tests
# must be labelled the same way as /tmp.  This doesn't work if either
# the directory is on NFS (no SELinux labels) or if SELinux is
# disabled, hence the tests.
if [ "$(stat -f -L -c %T .)" != "nfs" ] && \
   [ "$(getenforce | tr '[A-Z]' '[a-z]')" != "disabled" ]; then
    chcon --reference=/tmp tmp
fi

# Replace developer-centric README that ships with libguestfs, with
# our replacement file.
mv README README.orig
sed 's/@VERSION@/%{version}/g' < %{SOURCE4} > README

# Re-enable upstream cache and local repos
mkdir -pv %{_sysconfdir}/yum.repos.d
cp %{SOURCE9} %{_sysconfdir}/yum.repos.d/allrepos.repo

# Download appliance, since our chroot TDNF config does not have `keepcache=1`
# Must keep in sync with BRs under "Build requirements for the appliance"
# Download to
mkdir -pv %{_var}/cache/tdnf
tdnf install --downloadonly -y --disablerepo=* \
  --enablerepo=local-repo \
  --enablerepo=upstream-cache-repo \
  --enablerepo=toolchain-repo \
  --alldeps --downloaddir %{_var}/cache/tdnf \
    acl \
    attr \
    augeas-libs \
    bash \
    binutils \
    btrfs-progs \
    bzip2 \
    coreutils \
    cpio \
    cryptsetup \
    curl \
    dhclient \
    diffutils \
    dosfstools \
    e2fsprogs \
    file \
    findutils \
    gawk \
    gdisk \
    genisoimage \
    gfs2-utils \
    grep \
    gzip \
    hivex \
    iproute \
    iputils \
    kernel \
    kmod \
    kpartx \
    less \
    libcap \
    libldm \
    libselinux \
    libxml2 \
    lsof \
    lsscsi \
    lvm2 \
    lzop \
    mdadm \
    ntfs-3g ntfsprogs \
    ntfs-3g-system-compression \
    openssh-clients \
    parted \
    pciutils \
    pcre \
    policycoreutils \
    procps \
    psmisc \
    qemu-img \
    rsync \
    scrub \
    sed \
    sleuthkit \
    squashfs-tools \
    strace \
%ifarch x86_64
    syslinux \
    syslinux-devel \
%endif
    systemd \
    tar \
    udev \
    util-linux \
    vim \
    which \
    xfsprogs \
    xz \
    yajl \
    zerofree \
%ifnarch aarch64
    zfs-fuse \
%endif


mkdir cachedir repo
find %{_var}/cache/tdnf -type f -name '*.rpm' -print0 | \
  xargs -0 -n 1 cp -t repo
createrepo_c repo
sed -e "s|@PWD@|$(pwd)|" %{SOURCE6} > yum.conf

%build
# "--with-distro=REDHAT" is used to indicate Mariner is "Fedora-like" in package naming
%configure \
  PYTHON=python3 \
  --with-default-backend=libvirt \
  --with-distro=REDHAT \
  --with-extra="release=%{release},libvirt" \
  --with-qemu="qemu-system-%{_build_arch} qemu" \
  --with-supermin-packager-config=$(pwd)/yum.conf \
%if %{without php}
  --disable-php \
%endif
%ifnarch %{golang_arches}
  --disable-golang \
%endif
  --without-java \
%if %{without appliances}
  --enable-appliance=no \
%endif
  --disable-erlang

# Building index-parse.c by hand works around a race condition in the
# autotools cruft, where two or more copies of yacc race with each
# other, resulting in a corrupted file.
#
# 'INSTALLDIRS' ensures that Perl and Ruby libs are installed in the
# vendor dir, not the site dir.
make -j1 -C builder index-parse.c
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}

%ifarch %{test_arches}
%check
export LIBGUESTFS_DEBUG=1
export LIBGUESTFS_TRACE=1
export LIBVIRT_DEBUG=1

if ! make quickcheck QUICKCHECK_TEST_TOOL_ARGS="-t 1200"; then
    cat $HOME/.cache/libvirt/qemu/log/* && false
fi
%endif

%install
# This file is creeping over 1 MB uncompressed, and since it is
# included in the -devel subpackage, compress it to reduce
# installation size.
gzip -9 ChangeLog

# supermin prepare does not detect configuration files for Mariner, so create
# our own base tarball out of the root filesystem RPM
mkdir -pv mariner-filesystem
pushd mariner-filesystem
rpm2cpio %{_var}/cache/tdnf/filesystem*.rpm | cpio -id
popd
tar -czvf base.tar.gz mariner-filesystem
mv base.tar.gz appliance/supermin.d/

# 'INSTALLDIRS' ensures that Perl and Ruby libs are installed in the
# vendor dir, not the site dir.
make DESTDIR=%{buildroot} INSTALLDIRS=vendor install

# Delete static libraries.
rm $( find %{buildroot} -name '*.a' | grep -v /ocaml/ )

# Delete libtool files.
find %{buildroot} -type f -name "*.la" -delete -print

# Delete some bogus Perl files.
find %{buildroot} -name perllocal.pod -delete
find %{buildroot} -name .packlist -delete
find %{buildroot} -name '*.bs' -delete
find %{buildroot} -name 'bindtests.pl' -delete

%if %{with appliances}
# Remove obsolete binaries (RHBZ#1213298).
rm %{buildroot}%{_bindir}/virt-list-filesystems
rm %{buildroot}%{_bindir}/virt-list-partitions
rm %{buildroot}%{_bindir}/virt-tar
rm %{buildroot}%{_mandir}/man1/virt-list-filesystems.1*
rm %{buildroot}%{_mandir}/man1/virt-list-partitions.1*
rm %{buildroot}%{_mandir}/man1/virt-tar.1*
%endif

# golang: Ignore what libguestfs upstream installs, and just copy the
# source files to %%{_datadir}/gocode/src.
%ifarch %{golang_arches}
rm -r %{buildroot}%{_libdir}/golang
mkdir -p %{buildroot}%{_datadir}/gocode/src
cp -a golang/src/libguestfs.org %{buildroot}%{_datadir}/gocode/src
%endif

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv %{buildroot}%{_docdir}/libguestfs installed-docs
gzip --best installed-docs/*.xml

%if %{with appliances}
# Split up the monolithic packages file in the supermin appliance so
# we can install dependencies in subpackages.
pushd %{buildroot}%{_libdir}/guestfs/supermin.d

function move_to
{
    if ! grep -Esq "^$1$" packages; then
        echo "move_to $1: package name not found in packages file"
        exit 1
    fi
    grep -Ev "^$1$" < packages > packages-t
    mv packages-t packages
    echo "$1" >> "$2"
}

move_to curl            zz-packages-dib
move_to kpartx          zz-packages-dib
move_to qemu-img        zz-packages-dib
move_to which           zz-packages-dib
move_to sleuthkit       zz-packages-forensics
move_to gfs2-utils      zz-packages-gfs2
move_to iputils         zz-packages-rescue
move_to lsof            zz-packages-rescue
move_to openssh-clients zz-packages-rescue
move_to pciutils        zz-packages-rescue
move_to strace          zz-packages-rescue
move_to vim             zz-packages-rescue
move_to rsync           zz-packages-rsync
move_to xfsprogs        zz-packages-xfs
%ifnarch aarch64
move_to zfs-fuse        zz-packages-zfs
%endif

popd
%endif

%if %{with appliances}
# If there is a bogus dependency on kernel-*, rename it to 'kernel'
# instead.  This can happen for various reasons:
# - DNF picks kernel-debug instead of kernel.
# - Version of kernel-rt in brew > version of kernel.
# On all known architectures, depending on 'kernel' should
# mean "we need a kernel".
pushd %{buildroot}%{_libdir}/guestfs/supermin.d
sed -i 's/^kernel-.*/kernel/' packages
popd
%endif

# Guestfish colour prompts.
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile.d

# Remove the .gitignore file from ocaml/html which will be copied to docdir.
rm ocaml/html/.gitignore

# Find locale files.
%find_lang %{name}

%files -f %{name}.lang
%license COPYING COPYING.LIB
%doc README
%{_bindir}/libguestfs-test-tool
%if %{with appliances}
%{_libdir}/guestfs/
%exclude %{_libdir}/guestfs/supermin.d/zz-packages-*
%endif
%{_libdir}/libguestfs.so.*
%{_mandir}/man1/guestfs-faq.1*
%{_mandir}/man1/guestfs-performance.1*
%{_mandir}/man1/guestfs-recipes.1*
%{_mandir}/man1/guestfs-release-notes-1*.1*
%{_mandir}/man1/guestfs-release-notes-historical.1*
%{_mandir}/man1/guestfs-security.1*
%{_mandir}/man1/libguestfs-test-tool.1*

%files devel
%doc AUTHORS BUGS ChangeLog.gz HACKING TODO README
%doc examples/*.c
%doc installed-docs/*
%{_libdir}/libguestfs.so
%if %{with appliances}
%{_sbindir}/libguestfs-make-fixed-appliance
%{_mandir}/man1/libguestfs-make-fixed-appliance.1*
%endif
%{_mandir}/man1/guestfs-building.1*
%{_mandir}/man1/guestfs-hacking.1*
%{_mandir}/man1/guestfs-internals.1*
%{_mandir}/man1/guestfs-testing.1*
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/libguestfs.3*
%{_includedir}/guestfs.h
%{_libdir}/pkgconfig/libguestfs.pc

%if %{with appliances}
%files forensics
%{_libdir}/guestfs/supermin.d/zz-packages-forensics

%files gfs2
%{_libdir}/guestfs/supermin.d/zz-packages-gfs2

%files rsync
%{_libdir}/guestfs/supermin.d/zz-packages-rsync

%files rescue
%{_libdir}/guestfs/supermin.d/zz-packages-rescue

%files xfs
%{_libdir}/guestfs/supermin.d/zz-packages-xfs

%ifnarch aarch64
%files zfs
%{_libdir}/guestfs/supermin.d/zz-packages-zfs
%endif

%endif

%if %{with inspect-icons}
%files inspect-icons
# no files
%endif

%files tools-c
%doc README
%config(noreplace) %{_sysconfdir}/libguestfs-tools.conf
%{_sysconfdir}/virt-builder
%dir %{_sysconfdir}/xdg/virt-builder
%dir %{_sysconfdir}/xdg/virt-builder/repos.d
%config %{_sysconfdir}/xdg/virt-builder/repos.d/*
%config %{_sysconfdir}/profile.d/guestfish.sh
%{_mandir}/man5/libguestfs-tools.conf.5*
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*
%{_bindir}/guestmount
%{_mandir}/man1/guestmount.1*
%{_bindir}/guestunmount
%{_mandir}/man1/guestunmount.1*
%{_bindir}/virt-alignment-scan
%{_mandir}/man1/virt-alignment-scan.1*
%{_bindir}/virt-builder
%{_mandir}/man1/virt-builder.1*
%{_bindir}/virt-builder-repository
%{_mandir}/man1/virt-builder-repository.1*
%{_bindir}/virt-cat
%{_mandir}/man1/virt-cat.1*
%{_bindir}/virt-copy-in
%{_mandir}/man1/virt-copy-in.1*
%{_bindir}/virt-copy-out
%{_mandir}/man1/virt-copy-out.1*
%{_bindir}/virt-customize
%{_mandir}/man1/virt-customize.1*
%{_bindir}/virt-df
%{_mandir}/man1/virt-df.1*
%{_bindir}/virt-diff
%{_mandir}/man1/virt-diff.1*
%{_bindir}/virt-edit
%{_mandir}/man1/virt-edit.1*
%{_bindir}/virt-filesystems
%{_mandir}/man1/virt-filesystems.1*
%{_bindir}/virt-format
%{_mandir}/man1/virt-format.1*
%{_bindir}/virt-get-kernel
%{_mandir}/man1/virt-get-kernel.1*
%{_bindir}/virt-index-validate
%{_mandir}/man1/virt-index-validate.1*
%{_bindir}/virt-inspector
%{_mandir}/man1/virt-inspector.1*
%{_bindir}/virt-log
%{_mandir}/man1/virt-log.1*
%{_bindir}/virt-ls
%{_mandir}/man1/virt-ls.1*
%{_bindir}/virt-make-fs
%{_mandir}/man1/virt-make-fs.1*
%{_bindir}/virt-rescue
%{_mandir}/man1/virt-rescue.1*
%{_bindir}/virt-resize
%{_mandir}/man1/virt-resize.1*
%{_bindir}/virt-sparsify
%{_mandir}/man1/virt-sparsify.1*
%{_bindir}/virt-sysprep
%{_mandir}/man1/virt-sysprep.1*
%{_bindir}/virt-tail
%{_mandir}/man1/virt-tail.1*
%{_bindir}/virt-tar-in
%{_mandir}/man1/virt-tar-in.1*
%{_bindir}/virt-tar-out
%{_mandir}/man1/virt-tar-out.1*

%if %{with appliances}
%files tools
%doc README
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*
%endif

%files -n virt-dib
%doc README
%{_bindir}/virt-dib
%{_mandir}/man1/virt-dib.1*
%if %{with appliances}
%{_libdir}/guestfs/supermin.d/zz-packages-dib
%endif

%files bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/guestfish
%{_datadir}/bash-completion/completions/guestmount
%{_datadir}/bash-completion/completions/guestunmount
%{_datadir}/bash-completion/completions/libguestfs-test-tool
%{_datadir}/bash-completion/completions/virt-*

%files -n ocaml-%{name}
%{_libdir}/ocaml/guestfs
%exclude %{_libdir}/ocaml/guestfs/*.a
%exclude %{_libdir}/ocaml/guestfs/*.cmxa
%exclude %{_libdir}/ocaml/guestfs/*.cmx
%exclude %{_libdir}/ocaml/guestfs/*.mli
%{_libdir}/ocaml/stublibs/dllmlguestfs.so
%{_libdir}/ocaml/stublibs/dllmlguestfs.so.owner

%files -n ocaml-%{name}-devel
%doc ocaml/examples/*.ml ocaml/html
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli
%{_mandir}/man3/guestfs-ocaml.3*

%files -n perl-Sys-Guestfs
%doc perl/examples/*.pl
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/guestfs-perl.3*

%files -n python3-%{name}
%doc python/examples/*.py
%{python3_sitearch}/libguestfsmod*.so
%{python3_sitearch}/guestfs.py
%{python3_sitearch}/__pycache__/guestfs*.py*
%{_mandir}/man3/guestfs-python.3*

%files -n ruby-%{name}
%doc ruby/examples/*.rb
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/guestfs.rb
%{ruby_vendorarchdir}/_guestfs.so
%{_mandir}/man3/guestfs-ruby.3*

%if %{with php}
%files -n php-%{name}
%doc php/README-PHP
%dir %{_sysconfdir}/php.d
%{_sysconfdir}/php.d/guestfs_php.ini
%{_libdir}/php/modules/guestfs_php.so
%endif

%files -n lua-guestfs
%doc lua/examples/*.lua
%license lua/examples/LICENSE
%{_libdir}/lua/*/guestfs.so
%{_mandir}/man3/guestfs-lua.3*

%files gobject
%{_libdir}/libguestfs-gobject-1.0.so.0*
%{_libdir}/girepository-1.0/Guestfs-1.0.typelib

%files gobject-devel
%{_libdir}/libguestfs-gobject-1.0.so
%{_includedir}/guestfs-gobject.h
%dir %{_includedir}/guestfs-gobject
%{_includedir}/guestfs-gobject/*.h
%{_datadir}/gir-1.0/Guestfs-1.0.gir
%{_libdir}/pkgconfig/libguestfs-gobject-1.0.pc
%{_mandir}/man3/guestfs-gobject.3*

%files vala
%{_datadir}/vala/vapi/libguestfs-gobject-1.0.deps
%{_datadir}/vala/vapi/libguestfs-gobject-1.0.vapi

%ifarch %{golang_arches}
%files -n golang-guestfs
%doc golang/examples/*.go
%license golang/examples/LICENSE
%{_datadir}/gocode/src/libguestfs.org
%{_mandir}/man3/guestfs-golang.3*
%endif

%if %{with man-pages}
%files man-pages-ja
%lang(ja) %{_mandir}/ja/man1/*.1*
%lang(ja) %{_mandir}/ja/man3/*.3*
%lang(ja) %{_mandir}/ja/man5/*.5*

%files man-pages-uk
%lang(uk) %{_mandir}/uk/man1/*.1*
%lang(uk) %{_mandir}/uk/man3/*.3*
%lang(uk) %{_mandir}/uk/man5/*.5*
%endif

%changelog
* Wed Oct 11 2023 Minghe Ren <mingheren@microsoft.com> - 1.44.0-18
- Bump release to rebuild against glibc 2.35-6

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.44.0-17
- Bump release to rebuild with updated version of Go.

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.44.0-16
- Bump release to rebuild against glibc 2.35-5

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.44.0-15
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 15 2023 Andrew Phelps <anphel@microsoft.com> - 1.44.0-14
- Enable toolchain-repo with tdnf download command to fix build break

* Wed Jul 05 2023 Andrew Phelps <anphel@microsoft.com> - 1.44.0-13
- Bump release to rebuild against glibc 2.35-4

* Wed Apr 12 2023 Sam Meluch <sammeluch@microsoft.com> - 1.44.0-12
- Update tdnf download to tdnf install --downloadonly

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.44.0-11
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.44.0-10
- Bump release to rebuild with go 1.18.8

* Tue Sep 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 1.44.0-9
- Rebuilt for glibc-static 2.35-3

* Thu Sep 01 2022 Andrew Phelps <anphel@microsoft.com> - 1.44.0-8
- Remove duplicate BR on qemu-img
- Change runtime requires from qemu-img binary to qemu-img package

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.44.0-7
- Bump release to rebuild against Go 1.18.5

* Tue Apr 05 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44.0-6
- License verified.
- Making BR on "po4a" conditional.
- Spec clean-up.

* Sat Feb 05 2022 Thomas Crain <thcrain@microsoft.com> - 1.44.0-5
- Add patch to fix UUID parsing with file >= 5.40
- Downgrade selinux-policy requirement to a recommendation without a version constraint
- Bump release number to 5

* Thu Jan 20 2022 Thomas Crain <thcrain@microsoft.com> - 1.44.0-3
- Remove Fedora-specific comments/macros
- Use TDNF to get build-cached RPMs
- Remove link to highjacked upstream bug tracker
- Conditionally include PHP deps (off by default)
- Patch ocaml support, RPM config support
- Disable inspect-icons support by default (we don't have ghostscript)
- Remove reiserfs, nilfs, jfs, hfsplus, ufs completely
- Replace perl(Locale::TextDomain) BR with actual provider perl-libintl-perl
- License verified

* Thu Sep 30 2021 Thomas Crain <thcrain@microsoft.com> - 1.44.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Remove epoch
- Temporarily disable appliance building
- Remove RHEL-specifics

* Wed Jan 06 2021 Richard W.M. Jones <rjones@redhat.com> - 1:1.44.0-1
- New upstream stable version 1.44.0.

* Sat Sep 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.2-2
- Rebuild for OCaml 4.11.1 in Fedora 33.

* Mon Sep 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.2-1
- New upstream version 1.43.2.
- Replace libvirt-daemon-qemu with libvirt-daemon-kvm.

* Wed Sep 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.1-7.1
- Bump release and rebuild.

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.1-7
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.1-6
- OCaml 4.11.0 rebuild

* Mon Aug 10 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.43.1-5
- Use ExclusiveArch: %%{kernel_arches}

* Fri Jul 31 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.1-4
- Disable then reenable LTO.
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/ULGH5JYL7MHKDKTINJLOEN2QG6LOHWH7/

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.43.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul  6 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.43.1-1
- New development branch 1.43.
- Remove upstream patches.

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.42.0-8
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:1.42.0-7
- Rebuilt for Python 3.9

* Wed May 06 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.0-6
- Fix path to libguestfs appliance.

* Thu Apr 16 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.0-3
- Bump and rebuild to fix broken OCaml deps.

* Thu Mar 12 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.1-1
- Enable NTFS-3g system compression.

* Mon Mar 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.42.0-1
- New upstream stable version 1.42.0.
- Drop the benchmarking subpackage: moved to a new package upstream.
- Enable Vala bindings.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.8-9
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.41.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Vít Ondruch <vondruch@redhat.com> - 1:1.41.8-7
- Another rebuild against Ruby 2.7.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.8-5
- OCaml 4.10.0+beta1 rebuild.

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:1.41.8-4
- F-32: rebuild against ruby27

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.8-3
- OCaml 4.09.0 (final) rebuild.

* Wed Nov 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.8-2
- Use gpgverify macro instead of explicit gpgv2 command.

* Tue Nov 19 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.8-1
- New upstream version 1.41.8.
- virt-v2v is now in a separate project.
- Drop erlang bindings.

* Fri Oct 11 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.5-1
- New upstream version 1.41.5.

* Fri Oct 04 2019 Remi Collet <remi@remirepo.net> - 1:1.41.4-2
- rebuild for https://fedoraproject.org/wiki/Changes/php74

* Tue Sep 17 2019 Pino Toscano <ptoscano@redhat.com> - 1:1.41.4-2
- Drop virt-p2v (virt-p2v-maker subpackage), which is now built from
  its own source.

* Mon Sep 02 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.41.4-1
- New upstream version 1.41.4.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.40.2-10
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-9
- OCaml 4.08.1 (final) rebuild.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-8
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.40.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
- Disable the package entirely on i686 because there is no kernel
  https://fedoraproject.org/wiki/Changes/Stop_Building_i686_Kernels

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.40.2-6
- Perl 5.30 rebuild

* Fri May 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-5
- Add proposed patch for Python 3.8 (RHBZ#1705482).

* Mon Mar 18 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-4
- Remove Java bindings.
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/CW4XMOIKMNRRPAZ4H2ER7VPBY6YV2ODL/#YHTZ7IGVTKPWCBOY5C6UW7BMX7F35R5Q

* Thu Mar 07 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-3
- Remove Python 2 bindings completely.
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.40.2-2
- Rebuild for readline 8.0

* Fri Feb 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.2-1
- New upstream version 1.40.2.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.40.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:1.40.1-4
- F-30: rebuild against ruby26

* Mon Jan 21 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> - 1:1.40.1-3
- Disable ZFS for RISC-V (riscv64)

* Thu Jan 17 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.1-2
- nbdkit Python3 plugin is called "python3" in Fedora, adjust configure line.

* Thu Jan 17 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.40.1-1
- New upstream version 1.40.1.
- Remove patch which is now upstream.
- Add new virt-v2v man pages.

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:1.39.11-4
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Jan 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.11-3
- Small fix for qemu behaviour (RHBZ#1664318).

* Fri Oct 12 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.11-2
- lib: Add Recommends for libvirt-daemon-config-network so that networking
  works out of the box.

* Sat Sep 22 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.11-1
- New upstream version 1.39.11.

* Fri Sep 21 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.10-1
- New upstream version 1.39.10.

* Fri Aug 31 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.9-1
- New upstream version 1.39.9.

* Fri Jul 27 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.8-1
- New upstream version 1.39.8.

* Thu Jul 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.7-3
- v2v: Recommends nbdkit-plugin-vddk for -it vddk mode.

* Tue Jul 24 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.7-2
- Rebuild for unannounced soname bump in libconfig.

* Sat Jul 14 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.7-1
- New upstream version 1.39.7.
- v2v/TODO was removed upstream.

* Fri Jul 13 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.6-10
- v2v: Recommends nbdkit and the Python 3 plugin.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.39.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.6-7
- OCaml 4.07.0 (final) rebuild.

* Tue Jul 10 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.6-6
- Update PHP dependencies.

* Thu Jul 05 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.6-5
- Remove ldconfig
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/SU3LJVDZ7LUSJGZR5MS72BMRAFP3PQQL/
- BR on python-unversioned-command
  https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 1:1.39.6-4
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.39.6-3
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.39.6-2
- Perl 5.28 rebuild

* Fri Jun 29 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.6-1
- New upstream version 1.39.6.
- Add new bash-completion script for libguestfs-test-tool.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.5-5
- Bump release and rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.5-4
- Bump release and rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.5-3
- OCaml 4.07.0-rc1 rebuild.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.39.5-2
- Rebuilt for Python 3.7

* Wed May 23 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.5-1
- New upstream version 1.39.5.

* Wed May 02 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.4-1
- New upstream version 1.39.4.

* Sun Apr 22 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.3-1
- New upstream version 1.39.3.
- Remove upstream patch.

* Tue Apr 10 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 1:1.39.2-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 29 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.2-2
- Add patch to fix detection of qemu mandatory locking.

* Thu Mar 29 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.2-1
- New upstream version 1.39.2.

* Tue Mar 13 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.39.1-1
- New upstream version 1.39.1.

* Fri Feb 09 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.38.0-1
- New upstream version 1.38.0.
- Enable tarball signing since we are on a stable branch.
- Fix Source URLs.

* Tue Feb 06 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.37-1
- New upstream version 1.37.37.

* Thu Jan 25 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.36-1
- New upstream version 1.37.36.
- Unbreak the linker.

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:1.37.35-3
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.35-2
- Add BR rpcgen, libtirpc-devel and rebuild against updated Ruby.

* Sun Dec 10 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.35-1
- New upstream version 1.37.35.
- Remove upstream patches.
- Add virt-builder-repository and man page.

* Thu Dec  7 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.34-4
- Remove <shareable/> for libvirt >= 3.10.

* Sun Dec  3 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.34-3
- Fix locking on NBD drives.

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.34-2
- OCaml 4.06.0 rebuild.

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.34-1
- New upstream version 1.37.34.

* Thu Oct 19 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.31-1
- New upstream version 1.37.31.

* Tue Oct 10 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.29-1
- New upstream version 1.37.29.

* Thu Oct 05 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.28-2
- Add libguestfs-ufs (BSD) subpackage.

* Thu Sep 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.28-1
- New upstream version 1.37.28.

* Sat Sep 23 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.27-1
- New upstream version 1.37.27.

* Sun Sep 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.26-1
- New upstream version 1.37.26.

* Sat Sep 16 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.25-1
- New upstream version 1.37.25.

* Tue Sep 05 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.22-1
- New upstream version 1.37.22.

* Sat Aug 19 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.21-2
- Disable zfs subpackage on s390, s390x.

* Wed Aug 09 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.21-1
- New upstream version 1.37.21.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.20-2
- OCaml 4.05.0 rebuild.

* Fri Aug 04 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.20-1
- New upstream version 1.37.20.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.37.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.19-1
- New upstream version 1.37.19.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.37.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.18-1
- New upstream version 1.37.18.

* Tue Jul 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.17-2
- New upstream version 1.37.17.
- Drop libguestfs-gobject-doc because gtk-doc is no longer provided upstream.
- Add new man page guestfs-gobject(3) to libguestfs-gobject-devel.

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.16-2
- OCaml 4.04.2 rebuild.

* Fri Jun 23 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.16-1
- New upstream version 1.37.16.

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.37.14-3
- Perl 5.26 rebuild

* Mon May 22 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.14-2
- Bump release and rebuild for ppc64, ppc64le and s390x.

* Fri May 19 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.14-1
- New upstream version 1.37.14.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.13-2
- OCaml 4.04.1 rebuild.

* Mon May 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.13-1
- New upstream version 1.37.13.

* Wed Apr 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.12-1
- New upstream version 1.37.12.

* Sat Apr 15 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.11-1
- New upstream version 1.37.11.

* Wed Apr 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.10-1
- New upstream version 1.37.10.

* Sat Apr 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.9-1
- New upstream version 1.37.9.

* Fri Mar 31 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.8-1
- New upstream version 1.37.8.

* Fri Mar 24 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.7-1
- New upstream version 1.37.7.

* Mon Mar 20 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.6-1
- New upstream version 1.37.6.

* Tue Mar 14 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.2-1
- New upstream version 1.37.2.

* Tue Mar 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.1-1
- New upstream version 1.37.1.

* Tue Feb 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.37.0-1
- New upstream version 1.37.0.

* Fri Feb 24 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.28-1
- New upstream version 1.35.28.

* Thu Feb 23 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.27-1
- New upstream version 1.35.27.

* Wed Feb 22 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.26-1
- New upstream version 1.35.26.

* Wed Feb 15 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.25-1
- New upstream version 1.35.25.

* Sat Feb 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.24-1
- New upstream version 1.35.24.

* Sat Feb 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.23-1
- New upstream version 1.35.23.

* Fri Feb 10 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.22-1
- New upstream version 1.35.22.

* Wed Feb 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.21-1
- New upstream version 1.35.21.

* Thu Feb 02 2017 Pino Toscano <ptoscano@redhat.com> - 1:1.35.20-2
- Avoid spurious dependencies on kernel-debug etc.

* Sat Jan 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.20-1
- New upstream version 1.35.20.

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:1.35.19-4
- Rebuild again for f26-ruby24 sidetag

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:1.35.19-3
- Rebuild for readline 7.x

* Thu Jan 12 2017 Vít Ondruch <vondruch@redhat.com> - 1:1.35.19-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Sat Dec 24 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.19-1
- New upstream version 1.35.19.

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1:1.35.18-3
- Second rebuild for Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1:1.35.18-2
- Rebuild for Python 3.6

* Thu Dec 15 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.18-1
- New upstream version 1.35.18.

* Sun Dec 11 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.17-1
- New upstream version 1.35.17.

* Mon Nov 14 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.14-4
- Use _isa macro on dependencies (except for noarch packages).
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/QSQ7CWSFZ3CRHH7DDGAWVUCB2KFC3OWQ/

* Fri Nov 11 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.14-3
- Drop libguestfs-live-service subpackage.
- Remove setting _hardened_build since it is now the default in Fedora.
- Some tidying up of the description section.
- Require Augeas 1.7.0.

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.14-2
- Rebuild for OCaml 4.04.0.

* Wed Oct 26 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.14-1
- New upstream version 1.35.14.
- Add dbus-devel BR for virt-p2v.

* Fri Oct 21 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.9-1
- New upstream version 1.35.9.

* Fri Oct 21 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.8-2
- Add 'Suggests: perl' for virt-edit and virt-customize.

* Wed Oct 12 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.8-1
- New upstream version 1.35.8.

* Thu Oct 06 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.6-2
- Split off virt-p2v into virt-p2v-maker so it doesn't depend on X
  (RHBZ#1382275).

* Fri Sep 23 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.6-1
- New upstream version 1.35.6.

* Mon Sep 12 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.5-1
- New upstream version 1.35.5.

* Sat Sep 03 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.4-1
- New upstream version 1.35.4.

* Thu Sep 01 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.35.3-1
- New upstream version 1.35.3.

* Fri Aug 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.49-1
- New upstream version 1.33.49.

* Wed Jul 27 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.46-1
- New upstream version 1.33.46.

* Sat Jul 23 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.45-1
- New upstream version 1.33.45.

* Tue Jul 19 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.44-1
- New upstream version 1.33.44.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.33.43-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.43-2
- Fix missing dependency on policycoreutils.

* Fri Jul 15 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.43-1
- New upstream version 1.33.43.

* Wed Jul 13 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.42-2
- Don't install libtool wrapper scripts in benchmarking subpkg.

* Sat Jul 09 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.42-1
- New upstream version 1.33.42.

* Wed Jul 06 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.41-1
- New upstream version 1.33.41.

* Fri Jul 01 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.40-1
- New upstream version 1.33.40.

* Fri Jun 24 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.39-1
- New upstream version 1.33.39.

* Tue Jun 21 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.38-2
- Bump release and rebuild.

* Sun Jun 19 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.38-1
- New upstream version 1.33.38.

* Fri Jun 17 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.37-1
- New upstream version 1.33.37.

* Mon Jun 13 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.36-1
- New upstream version 1.33.36.

* Mon Jun 06 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.35-1
- New upstream version 1.33.35.

* Fri Jun 03 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.34-1
- New upstream version 1.33.34.
- Now building virt-p2v with gtk3 not gtk2.

* Fri May 27 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.32-1
- New upstream version 1.33.32.

* Mon May 23 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.30-1
- New upstream version 1.33.30.

* Thu May 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.33.29-2
- Perl 5.24 re-rebuild of bootstrapped packages

* Wed May 18 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.29-1
- New upstream version 1.33.29.

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.33.28-2
- Perl 5.24 rebuild

* Mon May 09 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.28-1
- New upstream version 1.33.28.

* Wed May 04 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.27-1
- New upstream version 1.33.27.

* Tue May 03 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.26-1
- New upstream version 1.33.26.

* Sun May 01 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.24-1
- New upstream version 1.33.24.

* Mon Apr 25 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.23-1
- New upstream version 1.33.23.

* Fri Apr 15 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.20-1
- New upstream version 1.33.20.

* Tue Apr 12 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.19-2
- New upstream version 1.33.19.
- Build python3 in a different directory.

* Fri Apr 08 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.18-5
- Disable tests on 32 bit arm because of libvirt RHBZ#1325085.

* Thu Apr 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.18-4
- Disable tests on POWER because of RHBZ#1293024.
- Enable tests on 32 bit arm because RHBZ#1303147 supposedly fixed.
- Explicitly depend on rubygem-rdoc, needed to build Ruby docs.

* Tue Apr 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.18-1
- New upstream version 1.33.18.

* Thu Mar 31 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.16-2
- Add code to verify tarball signatures (only enabled on stable branches).

* Fri Mar 25 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.16-1
- New upstream version 1.33.16.

* Thu Mar 17 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.15-1
- New upstream version 1.33.15.

* Mon Mar 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.14-1
- New upstream version 1.33.14.

* Fri Feb 26 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.13-1
- New upstream version 1.33.13.

* Thu Feb 18 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.33.12-2
- Filter perl provides

* Fri Feb 12 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.12-1
- New upstream version 1.33.12.

* Wed Feb 10 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.11-1
- New upstream version 1.33.11.

* Mon Feb 08 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.10-2
- New upstream version 1.33.10.
- Add non-upstream patch to fix 'ssh root@remote virt-xyz ...'

* Fri Feb 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.9-1
- New upstream version 1.33.9.

* Wed Feb 03 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.8-1
- New upstream version 1.33.8.

* Fri Jan 29 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.7-1
- New upstream version 1.33.7.

* Thu Jan 28 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.6-1
- New upstream version 1.33.6.

* Tue Jan 26 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.5-1
- New upstream version 1.33.5.

* Fri Jan 22 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.4-1
- New upstream version 1.33.4.
- Add guestfs-building(1), new man page.

* Thu Jan 21 2016 Richard Jones <rjones@redhat.com> - 1:1.33.1-3
- Remove useless python*_site* macros.
- Package python3 pyo files if present.

* Sat Jan 16 2016 Richard Jones <rjones@redhat.com> - 1:1.33.1-2
- Rebuild for updated Ruby in Rawhide.

* Mon Jan 11 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.1-1
- New upstream version 1.33.1.

* Thu Jan 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.33.0-1
- New upstream development version 1.33.0.

* Wed Dec 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.30-1
- New upstream version 1.31.30.

* Sun Dec 06 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.29-1
- New upstream version 1.31.29.

* Wed Nov 25 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.28-1
- New upstream version 1.31.28.

* Fri Nov 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.27-1
- New upstream version 1.31.27.
- Add new tool: virt-v2v-copy-to-local.

* Sat Nov 14 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.26-1
- New upstream version 1.31.26.

* Wed Nov 11 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.25-3
- Drop __pycache__/*.pyo files, as these are not generated by python 3.5.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.31.25-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov 06 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.25-1
- New upstream version 1.31.25.

* Fri Nov 06 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.24-2
- Rename python-libguestfs -> python2-libguestfs.
  See: https://fedoraproject.org/wiki/Packaging:Python

* Thu Nov 05 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.24-1
- New upstream version 1.31.24.

* Sat Oct 31 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.23-1
- New upstream version 1.31.23.

* Fri Oct 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.22-1
- New upstream version 1.31.22.
- Add new manual pages guestfs-{hacking,internals,security}(1).

* Sun Oct 25 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.20-1
- New upstream version 1.31.20.
- Perl bindings switched from ExtUtils::MakeMaker to Module::Build.

* Wed Oct 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.19-1
- New upstream version 1.31.19.

* Tue Oct 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.18-1
- New upstream version 1.31.18.

* Thu Oct 15 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.17-1
- New upstream version 1.31.17.

* Tue Oct 13 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.16-2
- Add hack to supermin to get builds working temporarily.

* Fri Oct 09 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.16-1
- New upstream version 1.31.16.

* Fri Oct 09 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.15-1
- New upstream version 1.31.15.

* Wed Oct 07 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.13-1
- New upstream version 1.31.13.

* Tue Oct 06 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.11-2
- BR ocamldoc so that we build the OCaml documentation.

* Mon Oct 05 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.11-1
- New upstream version 1.31.11.

* Thu Oct 01 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.9-4
- New upstream version 1.31.9.
- Include patch which fixes 'make install' in OCaml directory.
- Switch to using RPM autopatch directive.
- Fix a few RPM "macro expanded in comment" warnings.
- Include OCaml bindings documentation in ocaml-libguestfs-devel package.
- Add opensuse virt-builder files.

* Tue Sep 29 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.8-1
- New upstream version 1.31.8.

* Mon Sep 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.7-2
- Remove tests, except sanity check.  Testing is now done after the
  package has been built.

* Sun Sep 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.7-1
- New upstream version 1.31.7.

* Sat Sep 12 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.6-1
- New upstream version 1.31.6.

* Tue Sep 08 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.5-1
- New upstream version 1.31.5.

* Fri Sep 04 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.4-1
- New upstream version 1.31.4.

* Sat Aug 29 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.3-1
- New upstream version 1.31.3.
- Disable tests on armv7 because they take nearly 24 hours to run.

* Thu Aug 13 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.2-1
- New upstream version 1.31.2.
- Enable tests on i686, arm and aarch64.
- Remove patch which is now upstream.

* Fri Aug  7 2015 Pino Toscano <ptoscano@redhat.com> - 1:1.31.1-3
- Make libguestfs-tools-c recommend libguestfs-xfs, as the default filesystem
  is XFS so we want tools to work on XFS by default.
- Remove version suffix from the docdir mentioned in the installed README.

* Sun Aug  2 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.1-2
- Skip virt-sysprep test.

* Fri Jul 31 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.31.1-1
- New upstream version 1.31.1.

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.30.0-2
- OCaml 4.02.3 rebuild.

* Tue Jul 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.30.0-1
- New upstream version 1.30.0.

* Thu Jul 09 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.50-1
- New upstream version 1.29.50.
- Add virt-dib.

* Thu Jul 02 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.49-1
- New upstream version 1.29.49.

* Tue Jun 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.48-1
- New upstream version 1.29.48.

* Thu Jun 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.47-2
- Bump release and rebuild.

* Thu Jun 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.47-1
- New upstream version 1.29.47.
- New tool: virt-get-kernel.
- Skip xfs_admin tests because of RHBZ#1233220.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.46-4
- ocaml-4.02.2 rebuild.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.29.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.29.46-2
- Perl 5.22 rebuild

* Sun Jun 07 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.46-1
- New upstream version 1.29.46.

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.29.44-2
- Perl 5.22 rebuild

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.44-1
- New upstream version 1.29.44.

* Tue May 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.43-2
- Remove several test SKIP_* variables related to bugs which have
  since been fixed.

* Sat May 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.43-1
- New upstream version 1.29.43.

* Thu May 14 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.42-1
- New upstream version 1.29.42.

* Mon May 11 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.41-1
- New upstream version 1.29.41.

* Thu May 07 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.40-2
- Add workaround for builder/index-parse.c autotools race.

* Wed May 06 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.40-1
- New upstream version 1.29.40.

* Sun May 03 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.39-1
- New upstream version 1.29.39.

* Tue Apr 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.38-1
- New upstream version 1.29.38.

* Fri Apr 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.37-1
- New upstream version 1.29.37.

* Mon Apr 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.36-2
- Remove deprecated programs: virt-list-partitions, virt-list-filesystems,
  virt-tar (RHBZ#1213298).

* Thu Apr 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.36-1
- New upstream version 1.29.36.

* Fri Apr 10 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.34-1
- New upstream version 1.29.34.
- Drop the virt-v2v test harness subpackage.

* Wed Apr 01 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.33-2
- New upstream version 1.29.33.

* Fri Mar 27 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.32-1
- New upstream version 1.29.32.

* Tue Mar 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.31-2
- New upstream version 1.29.31.
- Remove upstream patches.

* Fri Mar 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.30-5
- More upstream patches to fix virt-v2v test harness.
- Do not delete OCaml *.a files, including ones in the virt-v2v test harness.

* Sun Mar 15 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.30-4
- Enable golang on various arches.

* Thu Mar 12 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.30-3
- Add virt-v2v-test-harness subpackage.
- Add a couple of upstream patches to fix the virt-v2v test harness.
- Remove external dependency generator.  Use supermin RPM deps instead.
- Depend on fuse (for testing with fusermount etc) (RHBZ#1201507).

* Wed Mar 11 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.30-1
- New upstream version 1.29.30.

* Thu Mar  5 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.29-1
- New upstream version 1.29.29.

* Mon Mar  2 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.26-3
- Add new subpackage libguestfs-inspect-icons (RHBZ#1194158).
- Remove dependency on uml_utilities, since UML is currently broken.
- Speed python3 build by copying over the generator pod2text cache and
  disabling non-Python language bindings.
- Disable mdadm test because of mdadm hangs (RHBZ#1197305).

* Wed Feb 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.26-1
- New upstream version 1.29.26.
- ocaml-4.02.1 rebuild.

* Thu Feb 12 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.25-1
- New upstream version 1.29.25.
- Remove patches which are now upstream.

* Thu Feb 05 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.24-3
- Upstream patch to fix virt-resize/virt-builder on aarch64 (RHBZ#1189284).

* Wed Feb 04 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.24-2
- Upstream patch to fix performance regression in virt-builder (RHBZ#1188866).
- Change the way Python double-build is done so we only have to
  apply patches in one place.

* Tue Feb 03 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.24-1
- New upstream version 1.29.24.
- Add Python 3 bindings.
- Disable btrfs-qgroup-show test.

* Tue Jan 27 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.23-1
- New upstream version 1.29.23.

* Thu Jan 22 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.22-2
- New upstream version 1.29.22.
- BR ounit (will be required for building >= 1.29.23).
- Disable FUSE tests because of a bug in Rawhide.

* Mon Jan 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.20-2
- Bump release for f22-ruby.

* Sun Jan 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.20-1
- New upstream version 1.29.20.
- Rebuild upstream with automake 1.15.
- Add upstream patch to allow LVM test to be skipped.
- Add upstream patch which fixes LUA 5.3 (beta) in Rawhide.
- Skip a couple of tests which are broken by changes in Rawhide.
- Remove bogus daemon/m4 directory which has not existed for years.

* Tue Dec 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.19-1
- New upstream version 1.29.19.

* Tue Dec 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.18-1
- New upstream version 1.29.18.

* Tue Dec 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.17-1
- New upstream version 1.29.17.

* Thu Dec 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.14-1
- New upstream version 1.29.14.

* Fri Dec 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.13-1
- New upstream version 1.29.13.

* Sat Nov 29 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.12-1
- New upstream version 1.29.12.

* Thu Nov 27 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.11-1
- New upstream version 1.29.11.

* Tue Nov 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.10-1
- New upstream version 1.29.10.

* Fri Nov 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.9-1
- New upstream version 1.29.9.

* Tue Nov 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.8-1
- New upstream version 1.29.8.

* Sat Nov 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.7-1
- New upstream version 1.29.7.

* Fri Nov 07 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.6-1
- New upstream version 1.29.6.
- Remove patch which is now upstream.

* Wed Nov 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.5-1
- New upstream version 1.29.5.

* Wed Nov  5 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.4-2
- configure: Don't override upstream's qemu selection.

* Fri Oct 31 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.4-1
- New upstream version 1.29.4.

* Fri Oct 31 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.3-1
- New upstream version 1.29.3.

* Sat Oct 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.2-1
- New upstream version 1.29.2.

* Wed Oct 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.29.1-1
- New upstream version 1.29.1.

* Fri Oct 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.64-1
- New upstream version 1.27.64.

* Thu Oct 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.63-1
- New upstream version 1.27.63.

* Fri Oct 10 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.62-1
- New upstream version 1.27.62.

* Thu Oct 09 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.61-1
- New upstream version 1.27.61.

* Wed Oct 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.60-1
- New upstream version 1.27.60.

* Thu Oct 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.58-1
- New upstream version 1.27.58.

* Wed Oct 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.57-1
- New upstream version 1.27.57.

* Tue Sep 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.56-1
- New upstream version 1.27.56.

* Sat Sep 27 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.55-1
- New upstream version 1.27.55.

* Wed Sep 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.54-1
- New upstream version 1.27.54.

* Tue Sep 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.53-1
- New upstream version 1.27.53.

* Fri Sep 19 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.50-1
- New upstream version 1.27.50.

* Thu Sep 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.49-1
- New upstream version 1.27.49.
- Fix guestfish colour prompts when using white-on-black terminal (RHBZ#1144201).

* Wed Sep 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.48-1
- New upstream version 1.27.48.

* Tue Sep 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.47-1
- New upstream version 1.27.47.

* Mon Sep 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.46-1
- New upstream version 1.27.46.

* Sun Sep 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.45-1
- New upstream version 1.27.45.

* Sat Sep 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.44-1
- New upstream version 1.27.44.

* Thu Sep 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.43-1
- New upstream version 1.27.43.

* Thu Sep 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.42-1
- New upstream version 1.27.42.

* Tue Sep 09 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.41-1
- New upstream version 1.27.41.

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.27.39-2
- Perl 5.20 re-rebuild of bootstrapped packages

* Sat Sep 06 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.39-1
- New upstream version 1.27.39.
- Package virt-p2v ISO build tools together with virt-v2v in
  a separate virt-v2v subpackage.

* Fri Sep 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.38-1
- New upstream version 1.27.38.

* Thu Sep 04 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.37-1
- New upstream version 1.27.37.

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.27.36-2
- Perl 5.20 rebuild

* Tue Sep 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.36-1
- New upstream version 1.27.36.

* Mon Sep 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.35-1
- New upstream version 1.27.35.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.34-1
- New upstream version 1.27.34.

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.27.33-3
- Perl 5.20 rebuild

* Fri Aug 29 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.33-2
- New upstream version 1.27.33.
- Enable LVM filtering test (thanks Pino Toscano).

* Mon Aug 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.31-1
- New upstream version 1.27.31.

* Thu Aug 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.30-1
- New upstream version 1.27.30.

* Wed Aug 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.28-1
- New upstream version 1.27.28.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.27.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.27-1
- New upstream version 1.27.27.

* Fri Aug 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.26-2
- Java is now java-1.8.0-openjdk in Rawhide.

* Thu Aug 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.26-1
- New upstream version 1.27.26.

* Thu Aug 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.25-2
- Require mingw32-srvany >= 1.0-13 because otherwise we have a broken symlink.
- Skip virt-v2v tests since they require rhsrvany.exe which is not
  available during the tests.

* Tue Aug 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.25-1
- New upstream version 1.27.25.

* Mon Jul 28 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.24-3
- Rebuild on aarch64.

* Sun Jul 27 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.24-2
- New upstream version 1.27.24.
- Remove patch now upstream.

* Fri Jul 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.23-3
- Skip LVM test which is failing.

* Thu Jul 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.23-2
- Enable tests on aarch64, in order to study which tests fail.

* Wed Jul 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.23-1
- New upstream version 1.27.23.

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:1.27.22-3
- Rebuilt for gobject-introspection 1.41.4

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.22-2
- New upstream version 1.27.22.
- Disable golang since the Fedora package is broken again.

* Wed Jul 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.27.21-2
- Disable tests on aarch64
- ntfs-3g available on all arches
- hfsplus-tools on all arches
- KVM available on ARMv7 and aarch64

* Tue Jul 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.21-1
- New upstream version 1.27.21.

* Wed Jul 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.20-1
- New upstream version 1.27.20.

* Tue Jun 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.19-1
- New upstream version 1.27.19.

* Mon Jun 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.18-1
- New upstream version 1.27.18.

* Sat Jun 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.16-2
- Install guestfish colour prompts.

* Sat Jun 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.16-1
- New upstream version 1.27.16.

* Wed Jun 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.15-1
- New upstream version 1.27.15.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.27.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.14-1
- New upstream version 1.27.14.

* Sun May 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.13-1
- New upstream version 1.27.13.

* Fri May 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.12-2
- New upstream version 1.27.12.
- Enable golang since it is now working on Rawhide.
- Fix golang installation again.
- Delete guestfs-p2v-iso(1) (internal documentation).

* Fri May 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.11-3
- Try re-enabling x86-64 tests.
  Requires supermin >= 5.1.8-3 which supports xz-compressed kernel modules.

* Fri May 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.11-2
- New upstream version 1.27.11.

* Fri May 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.10-1
- New upstream version 1.27.10.

* Thu May 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.9-1
- New upstream version 1.27.9.

* Sat May  3 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.8-2
- Remove ruby(release) version.  Fix for Ruby 2.1.

* Fri May 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.8-1
- New upstream version 1.27.8.

* Sat Apr 26 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.7-1
- New upstream version 1.27.7.

* Tue Apr 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.6-1
- New upstream version 1.27.6.

* Wed Apr 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.5-2
- Remove /var/run/libguestfs, which is not used.

* Wed Apr 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.5-1
- New upstream version 1.27.5.

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.4-1
- New upstream version 1.27.4.

* Tue Apr  8 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.3-3
- Re-enable virt-sparsify --in-place test, see:
  https://bugzilla.redhat.com/show_bug.cgi?id=1079210#c4

* Mon Apr 07 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.3-2
- Do not use rubygem-minitest.  Temporary workaround, see:
  https://bugzilla.redhat.com/show_bug.cgi?id=1085029#c2

* Sun Apr 06 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.3-1
- New upstream version 1.27.3.

* Mon Mar 31 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.2-1
- New upstream version 1.27.2.

* Fri Mar 28 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.27.0-1
- New upstream version 1.27.0.

* Wed Mar 26 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.49-1
- New upstream version 1.25.49.

* Tue Mar 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.47-1
- New upstream version 1.25.47.
- Include new tool: virt-customize.

* Thu Mar 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.46-1
- New upstream version 1.25.46.

* Thu Mar 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.45-2
- Further split libguestfs appliance dependencies.

* Mon Mar 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.45-1
- New upstream version 1.25.45.

* Fri Mar 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.44-2
- Try to patch fstrim so it works in Koji/Rawhide.

* Thu Mar 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.44-1
- New upstream version 1.25.44.

* Sat Mar 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.43-1
- New upstream version 1.25.43.

* Thu Mar 06 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.42-1
- New upstream version 1.25.42.

* Tue Mar 04 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.41-1
- New upstream version 1.25.41.

* Mon Mar 03 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.40-1
- New upstream version 1.25.40.

* Sun Mar 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.39-2
- New upstream version 1.25.39.

* Fri Feb 28 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.38-4
- Disable hfsplus subpackage on arm & ppc.
- Disable zfs subpackage on arm.
- Disable tests on x86.

* Thu Feb 27 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.38-3
- Ensure dependencies needed by the daemon are added to base libguestfs.

* Wed Feb 26 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.38-2
- New upstream version 1.25.38.
- Requires new supermin 5.1.0.
- Split the dependencies into subpackages, at least for the less common
  filesystem types.
- In the dependency generator, we can now generate ordinary dependencies!

* Sat Feb 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.37-2
- New upstream version 1.25.37.
- Disable tests on ARM because of RHBZ#1066581.

* Tue Feb 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.36-5
- Add upstream patches, workaround for libvirt on ARM / ppc64 bug.
- Run make quickcheck (and fail early) before doing full make check.

* Mon Feb 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.36-1
- New upstream version 1.25.36.

* Sun Feb 16 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.34-1
- Enable tests on i686 as both of the referenced bugs (RHBZ#998722 &
  RHBZ#998692) are now supposed to be fixed.
- Enable tests on ARM as the bug (RHBZ#990258) is supposed to be fixed.

* Thu Feb 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.34-1
- New upstream version 1.25.34.
- Reenable tests as the kernel bug is fixed.

* Wed Feb 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.33-1
- New upstream version 1.25.33.

* Tue Feb 04 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.32-2
- Since Python package is not noarch, do not put Python files into
  shared /usr/lib/python2.X/site-packages (RHBZ#1061155).

* Tue Feb 04 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.32-1
- New upstream version 1.25.32.

* Wed Jan 29 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.31-2
- virt-make-fs has been rewritten in C.
- qemu-img is now required by the core library (for guestfs_disk_create).
- perl(String::ShellQuote) is no longer used.

* Wed Jan 29 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.31-1
- New upstream version 1.25.31.

* Sat Jan 25 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.29-1
- New upstream version 1.25.29.

* Fri Jan 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.27-1
- New upstream version 1.25.27.

* Wed Jan 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.26-1
- New upstream version 1.25.26.

* Wed Jan 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.25-2
- Update to latest Fedora golang packaging draft.
- See: https://fedoraproject.org/wiki/PackagingDrafts/Go

* Tue Jan 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.25-1
- New upstream version 1.25.25.

* Sun Jan 19 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.24-1
- New upstream version 1.25.24.

* Sat Jan 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.23-1
- New upstream version 1.25.23.

* Tue Jan 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.21-1
- New upstream version 1.25.21.

* Mon Jan 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.20-1
- New upstream version 1.25.20.

* Thu Jan 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.19-1
- New upstream version 1.25.19.

* Thu Dec 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.18-1
- New upstream version 1.25.18.

* Sat Dec 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.15-1
- New upstream version 1.25.15.

* Thu Dec 12 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.14-1
- New upstream version 1.25.14.

* Mon Dec 09 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.13-1
- New upstream version 1.25.13.

* Fri Dec 06 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.12-3
- Build golang package only on x86 and ARM.  The golang package in Fedora
  uses the same ExclusiveArch.  Thanks: Dan Horák.

* Wed Dec 04 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.12-2
- Rebuild for procps SONAME bump.

* Mon Dec 02 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.12-1
- New upstream version 1.25.12.

* Mon Nov 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.11-3
- Disable NBD test, buggy in qemu 1.7.0 (filed as RHBZ#1034433).

* Sat Nov 23 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.11-2
- Disable mdadm test, buggy in kernel 3.13 (filed as RHBZ#1033971).

* Sat Nov 23 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.11-1
- New upstream version 1.25.11.

* Wed Nov 20 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.8-2
- Rebuild to resolve broken dependency on krb libraries.
- Remove obsolete Obsoletes.
- Fix Source URL.
- Require java-headless instead of java:
  https://fedoraproject.org/wiki/Changes/HeadlessJava
- Backport upstream patch to fix btrfs.

* Thu Nov 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.8-1
- New upstream version 1.25.8.

* Sat Nov 09 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.7-1
- New upstream version 1.25.7.

* Tue Nov 05 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.6-2
- New upstream version 1.25.6.
- Add virt-index-validate tool & man page.

* Tue Nov 05 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.3-2
- Remove patches, now upstream.
- +BR flex & bison, required by libguestfs >= 1.25.4.
- +BR xz-devel (for liblzma) to accelerate virt-builder in >= 1.25.5.

* Fri Nov 01 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.3-1
- New upstream version 1.25.3.

* Wed Oct 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.2-1
- New upstream version 1.25.2.

* Sat Oct 26 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.1-1
- New upstream version 1.25.1.

* Tue Oct 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.0-2
- Don't use versioned jar file (RHBZ#1022133).

* Sat Oct 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.25.0-1
- New upstream version 1.25.0.

* Tue Oct 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.33-1
- New upstream version 1.23.33.

* Mon Oct 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.32-1
- New upstream version 1.23.32.

* Sun Oct 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.31-1
- New upstream version 1.23.31.

* Fri Oct 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.30-1
- New upstream version 1.23.30.

* Tue Oct 08 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.28-1
- New upstream version 1.23.28.

* Mon Oct 07 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.27-1
- New upstream version 1.23.27.

* Fri Oct  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.25-1
- New upstream version 1.23.25.
- Add virt-builder and its dependencies.

* Mon Sep 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.23-2
- New upstream version 1.23.23.
- Remove patch which is now upstream.

* Thu Sep 12 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.22-2
- Add patch to debug parallel tests.

* Wed Sep 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.22-1
- New upstream version 1.23.22.

* Mon Sep  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.21-2
- Disable golang bindings on ppc64 (no golang package available).

* Sat Sep  7 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.21-1
- New upstream version 1.23.21.
- Remove patches which are now upstream.
- Requires supermin >= 4.1.5 (technically only on ARM for device tree
  support, but might as well have it everywhere).

* Tue Sep  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.20-5
- Enable debugging messages in parallel virt-alignment-scan, virt-df
  in order to debug possible race condition seen in Koji.

* Mon Sep  2 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.20-4
- Rebuild now that RHBZ#1003495 is supposed to be fixed.

* Sun Sep  1 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.20-2
- New upstream version 1.23.20.

* Thu Aug 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.19-1
- New upstream version 1.23.19.
- Remove 2 x patches which are upstream.

* Thu Aug 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.18-4
- Enable gzip-compressed appliance.
- Note this requires supermin >= 4.1.4.

* Wed Aug 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.18-3
- Fix javadoc location to use _javadocdir macro.
- Call ldconfig in java post and postun scripts.
- Do not explicitly depend on perl-devel.
- Compress the ChangeLog and *.xml files in devel package.
- Create new subpackage gobject-doc for the huge HTML documentation.
- Make javadoc, gobject-doc, bash-completion, man-pages-*, tools packages
  'noarch'.

* Mon Aug 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.18-2
- New upstream version 1.23.18.
- Disable 32 bit x86 tests because of RHBZ#998722 & RHBZ#998692.

* Thu Aug 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.17-1
- New upstream version 1.23.17.
- Enable tests as cpu host-model is no longer used on TCG.

* Tue Aug 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.16-1
- New upstream version 1.23.16.

* Sun Aug 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.15-1
- New upstream version 1.23.15.

* Tue Aug  6 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.14-1
- New upstream version 1.23.14.

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.13-2
- Disable all tests because Rawhide kernel is broken (RHBZ#991808).

* Sat Aug  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.13-1
- New upstream version 1.23.13.

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 1:1.23.12-2
- Perl 5.18 rebuild

* Tue Jul 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.12-1
- New upstream version 1.23.12.
- Disable ARM tests because of libvirt error:
  XML error: No PCI buses available [code=27 domain=10] (RHBZ#990258).

* Tue Jul 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.11-2
- Enable ARM builds (thanks Dan Berrange).

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.11-1
- New upstream version 1.23.11.
- +BR systemd-devel (for systemd journal processing).
- Disable ARM builds for now.

* Tue Jul 23 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.10-1
- New upstream version 1.23.10.

* Fri Jul 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.9-1
- New upstream version 1.23.9.
- Remove 5 x patches which are all upstream.

* Thu Jul 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.8-5
- Add patches to ./run so we capture errors when i686 tests time out.
- Include upstream patch to fix double-free if appliance
  building fails (RHBZ#983218).

* Tue Jul  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.8-2
- New upstream version 1.23.8.
- Try enabling golang bindings.
- Add upstream patch to fix golang bindings.

* Wed Jul  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.7-1
- New upstream version 1.23.7.
- Disable golang bindings.

* Thu Jun 27 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.6-2
- Re-enable tests on i686, supposedly TCG problems are fixed
  (RHBZ#857026 etc.).

* Wed Jun 26 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.6-1
- New upstream version 1.23.6.

* Tue Jun 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.5-1
- New upstream version 1.23.5.
- Fix hostname inspection because of change in Augeas (RHBZ#975412).
- Upstream libguestfs now requires Augeas >= 1.0.0.
- Kernel bug which affected mdadm is fixed (RHBZ#962079).

* Fri Jun 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.4-1
- New upstream version 1.23.4.

* Mon Jun 10 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.3-1
- New upstream version 1.23.3.

* Wed Jun  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.2-2
- libguestfs-devel should depend on an explicit version of
  libguestfs-tools-c, in order that the latest package is pulled in.

* Mon Jun  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.2-1
- New upstream version 1.23.2.

* Tue May 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.23.1-1
- New upstream development branch 1.23.
- New upstream version 1.21.1.

* Tue May 21 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.40-3
- New upstream version 1.21.40.

* Wed May 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.39-1
- New upstream version 1.21.39.

* Mon May 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.38-2
- Bump and rebuild.

* Sat May 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.38-1
- New upstream version 1.21.38.

* Thu May  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.37-1
- New upstream version 1.21.37.

* Sun May  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.36-2
- Bump and rebuild.

* Thu May  2 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.36-1
- New upstream version 1.21.36.

* Tue Apr 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.35-1
- New upstream version 1.21.35.

* Mon Apr 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.34-2
- New upstream version 1.21.34.

* Thu Apr 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.33-1
- New upstream version 1.21.33.

* Tue Apr 23 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.32-1
- New upstream version 1.21.32.
- Fix stray backslash in spec file.
- Enable btrfs tests, since these are now stable enough not to fail usually.
- Skip gnulib tests which fail.

* Wed Apr 17 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.31-1
- New upstream version 1.21.31.
- Rebuild against new krb5 (RHBZ#953001).

* Tue Apr 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.30-1
- New upstream version 1.21.30.

* Sat Apr 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.29-1
- New upstream version 1.21.29.

* Thu Apr 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.28-3
- SYSLINUX only exists on x86 arches so make that dependency conditional
  (thanks Dennis Gilmore).

* Tue Apr  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.28-2
- New upstream version 1.21.28.
- Change attach-method -> backend in a few places.
- Simplify make install section so it fits on a single page.

* Thu Apr  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.27-1
- New upstream version 1.21.27.
- Add new appliance BRs: syslinux, syslinux-extlinux.
- Add a dependency on libosinfo (partial fix for RHBZ#948324).

* Tue Apr  2 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.26-4
- New upstream version 1.21.26.
- Use ./configure --with-default-backend=.. instead of attach-method.
- Remove Sys::Guestfs::Lib (removed upstream).
- Detect if network is available.
  libguestfs_buildnet macro no longer needed.
- Enable hardened build (-fPIE, RELRO).
- Remove BRs: ncurses-devel and versioned parted.

* Sat Mar 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.25-1
- New upstream version 1.21.25.

* Fri Mar 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.24-1
- New upstream version 1.21.24.
- Remove patches, now upstream.

* Fri Mar 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.23-3
- Add patch for broken 'file' command in Rawhide (RHBZ#928995).

* Thu Mar 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.23-2
- New upstream version 1.21.23.
- Remove 'Group' which is not required by modern RPM.
- Add patch to use new-style demand-loaded bash-completion scripts.
- Spin bash-completion scripts into a new libguestfs-bash-completion package.

* Mon Mar 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.22-1
- New upstream version 1.21.22.

* Sat Mar 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.21-2
- Set INSTALLDIRS on both make and make install rules.

* Fri Mar 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.21-1
- New upstream version 1.21.21.
- Remove ruby vendor patch.

* Wed Mar 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.20-1
- New upstream version 1.21.20.
- In Fedora 19, 'ruby(abi)' has been replaced by 'ruby(release)'
  and the version of the ruby ABI/release is now 2.0.0.

* Mon Mar 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.19-1
- New upstream version 1.21.19.

* Thu Mar  7 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.18-1
- New upstream version 1.21.18.

* Tue Mar  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.17-1
- New upstream version 1.21.17.
- New program 'guestunmount'.

* Fri Mar  1 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.16-1
- New upstream version 1.21.16.
- Re-enable tests, since kernel patch is upstream.

* Tue Feb 26 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.15-1
- New upstream version 1.21.15.

* Mon Feb 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.14-2
- New upstream version 1.21.14.
- Disable tests because of Rawhide kernel bug that prevents booting.

* Wed Feb 20 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.13-1
- New upstream version 1.21.13.

* Tue Feb 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.12-1
- New upstream version 1.21.12.
- Remove patch, now upstream.

* Thu Feb 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.11-2
- New upstream version 1.21.11.
- Add experimental patch to capture stack trace of segfaults in the appliance.

* Mon Feb 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.10-1
- New upstream version 1.21.10.

* Sat Feb  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.9-1
- New upstream version 1.21.9.

* Thu Feb  7 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.8-2
- Bump and rebuild.

* Tue Feb  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.8-1
- New upstream version 1.21.8.
- Remove patch which is now upstream.
- 'febootstrap' with renamed to 'supermin' upstream.
  . Depend on supermin >= 4.1.1.
  . Use new --with-supermin-packager-config option.

* Tue Feb  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.7-4
- Skip set_label tests because of RHBZ#906777.
- Disable btrfs tests again because RHBZ#863978 is not fixed.

* Mon Feb  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.7-2
- New development version 1.21.7.
- Re-enable btrfs tests, apparently fixed upstream.

* Mon Jan 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.6-1
- New development version 1.21.6.

* Sat Jan 26 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.5-3
- Bump and rebuild.

* Fri Jan 25 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.5-2
- Bump and rebuild.

* Mon Jan 21 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.5-1
- New development version 1.21.5.
- Remove upstream patch.

* Mon Jan 21 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.4-3
- Add upstream patch to allow btrfs tests to be skipped.
- Skip btrfs tests because btrfs has been broken forever (RHBZ#863978).

* Sat Jan 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.4-2
- Depend on openjdk instead of java.

* Thu Jan 17 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.4-1
- New upstream version 1.21.4.
- Add libguestfs-gobject-1.0.pc.
- Remove automake 1.13 hack, fixed upstream.
- Add explicit dependency on libcap, needed by the appliance.

* Thu Jan 17 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.3-2
- New upstream version 1.21.3.

* Sat Jan 12 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.2-3
- Bump and rebuild.

* Sat Dec 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.2-2
- New upstream version 1.21.2.
- Use new --with-febootstrap-packager-config option.

* Mon Dec 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.1-3
- Remove all RHEL-specific hacks since I've now branched RHEL 7.
- Add BR gdisk.

* Mon Dec 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.1-2
- New upstream version 1.21.1 (development branch).
- Fix source URL.
- Rebase ruby site/vendor patch.
- Use 'make check -k' so we get to see all test failures at once.
- For RHEL 7:
  * Do not depend on perl(Expect) (only needed to test virt-rescue).
  * Depend on /usr/bin/qemu-img instead of qemu-img package, since the
    package name (but not the binary) is different in RHEL 7.
  * Add workaround for libvirt/KVM bug RHBZ#878406.
  * Do not depend on libvirt-daemon-qemu.
  * Do not depend on libldm (not yet in RHEL 7: RHBZ#887894).

* Thu Dec 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.0-1
- New upstream version 1.20.0.
- New source URL for this branch.
- Reconcile upstream packagelist, BRs and Requires lists.
- Requires newest SELinux policy so that SVirt works.
- Fix patch 2.  Actually, remove and replace with a small script.

* Sat Dec 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.66-1
- New upstream version 1.19.66.

* Fri Nov 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.65-2
- Add a hack to work around glibc header bug <rpc/svc.h>.

* Thu Nov 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.65-1
- New upstream version 1.19.65.

* Sat Nov 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.64-1
- New upstream version 1.19.64.

* Sat Nov 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-3
- Re-add: Non-upstream patch to add the noapic flag on the kernel
  command line on i386 only.  This works around a bug in 32-bit qemu,
  https://bugzilla.redhat.com/show_bug.cgi?id=857026

* Fri Nov 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-2
- Remove non-upstream patch designed to work around
  https://bugzilla.redhat.com/show_bug.cgi?id=857026
  to see if this has been fixed.
- Re-enable tests on i686 to see if
  https://bugzilla.redhat.com/show_bug.cgi?id=870042
  has been fixed.

* Fri Nov 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-1
- New upstream version 1.19.63.

* Tue Nov 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.62-1
- New upstream version 1.19.62.

* Mon Nov 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.61-1
- New upstream version 1.19.61.

* Sat Nov 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.60-2
- Remove Lua bogus libtool *.la file.

* Sat Nov 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.60-1
- New upstream version 1.19.60.

* Tue Nov 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.59-1
- New upstream version 1.19.59.

* Sat Nov 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.58-1
- New upstream version 1.19.58.

* Thu Nov 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.57-1
- New upstream version 1.19.57.

* Tue Nov 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-3
- Add upstream patch to disable virt-format test, and disable
  it because wipefs utility is broken.

* Sat Nov 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-2
- Add upstream patch to fix wipefs test.

* Fri Nov 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-1
- New upstream version 1.19.56.

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.55-1
- New upstream version 1.19.55.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.54-1
- New upstream version 1.19.54.

* Wed Oct 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-3
- Disable tests on ix86 because qemu/kernel is broken (RHBZ#870042).

* Wed Oct 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-2
- Add upstream patch to fix guestfish tests.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-1
- New upstream version 1.19.53.

* Sun Oct 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.52-1
- New upstream version 1.19.52.

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.51-1
- New upstream version 1.19.51.

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.50-2
- Correct perl dependencies

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.50-1
- New upstream version 1.19.50.

* Wed Oct 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-3
- Upstream patch to workaround btrfs problems with kernel 3.7.0.

* Tue Oct 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-2
- Install all libguestfs-live-service udev rules into /usr/lib/udev/rules.d.

* Tue Oct 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-1
- New upstream version 1.19.49.

* Sun Oct 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.48-1
- New upstream version 1.19.48.

* Mon Oct 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.46-1
- New upstream version 1.19.46.

* Wed Sep 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.45-1
- New upstream version 1.19.45.

* Tue Sep 25 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.44-2
- Enable sVirt (NB: requires libvirt >= 0.10.2-3, selinux-policy >= 3.11.1-23).
- Add upstream patch to label the custom $TMPDIR used in test-launch-race.

* Mon Sep 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.44-1
- New upstream version 1.19.44.

* Sat Sep 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.43-1
- New upstream version 1.19.43.

* Tue Sep 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.42-2
- New upstream version 1.19.42.
- Rebase sVirt (disable) patch.

* Sun Sep 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.41-1
- New upstream version 1.19.41.

* Fri Sep 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-3
- Add (non-upstream) patch to add the noapic flag on the kernel
  command line on i386 only.  This works around a bug in 32-bit qemu.

* Wed Sep 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-2
- Enable tests because RHBZ#853408 has been fixed in qemu-1.2.0-3.fc18.

* Wed Sep 05 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-1
- New upstream version 1.19.40.

* Tue Sep 04 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.39-1
- New upstream version 1.19.39.

* Mon Sep 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.38-1
- New upstream version 1.19.38.

* Fri Aug 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.37-1
- New upstream version 1.19.37.

* Thu Aug 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.36-2
- New upstream version 1.19.36.
- Require libvirt-daemon-qemu (for libvirt attach method).

* Thu Aug 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.36-1
- Switch to using libvirt as the backend for running the appliance.  See:
  https://www.redhat.com/archives/libguestfs/2012-August/msg00070.html
- Use configure RPM macro instead of ./configure.

* Wed Aug 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.35-1
- New upstream version 1.19.35.

* Wed Aug 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.34-2
- Add upstream patch to fix Perl bindtests on 32 bit.

* Tue Aug 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.34-1
- New upstream version 1.19.34.

* Tue Aug 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-1
- New upstream version 1.19.33.

* Mon Aug 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-3
- Fix Perl examples directory so we only include the examples.
- Add Java examples to java-devel RPM.

* Tue Aug 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-2
- New upstream version 1.19.33.
- Reenable tests.

* Sat Aug 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.32-1
- New upstream version 1.19.32.

* Wed Aug 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.31-1
- New upstream version 1.19.31.

* Tue Aug 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.30-1
- New upstream version 1.19.30.

* Sat Aug 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.29-2
- New upstream version 1.19.29.
- Remove RELEASE NOTES from doc section, and add equivalent man page.

* Fri Aug 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.28-4
- Bump and rebuild.

* Thu Aug 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.28-3
- New upstream version 1.19.28.
- Update libguestfs-find-requires to generate ordinary lib dependencies.

* Wed Aug  1 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.27-2
- Disable tests because of RHBZ#844485.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.27-1
- New upstream version 1.19.27.

* Thu Jul 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.26-2
- Remove old RPM-isms like defattr.
- Add upstream patches to fix use of 'run' script in tests.

* Thu Jul 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.26-1
- New upstream version 1.19.26.

* Tue Jul 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.25-1
- New upstream version 1.19.25.

* Mon Jul 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.24-1
- New upstream version 1.19.24.

* Sun Jul 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.23-1
- New upstream version 1.19.23.

* Thu Jul 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.22-2
- Add upstream patch to skip mount-local test if /dev/fuse not writable.

* Thu Jul 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.22-1
- New upstream version 1.19.22.

* Wed Jul 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.21-1
- New upstream version 1.19.21.

* Tue Jul 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.20-1
- New upstream version 1.19.20.

* Mon Jul 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.19-1
- New upstream version 1.19.19.

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.18-2
- Perl 5.16 rebuild

* Mon Jul 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.18-1
- New upstream version 1.19.18.

* Fri Jul 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.17-1
- New upstream version 1.19.17.

* Wed Jul 04 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.16-1
- New upstream version 1.19.16.

* Fri Jun 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.15-1
- New upstream version 1.19.15.

* Thu Jun 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.14-1
- New upstream version 1.19.14.

* Wed Jun 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.13-2
- New upstream version 1.19.13.
- Add upstream patch to fix GObject/Javascript tests.

* Tue Jun 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.12-1
- New upstream version 1.19.12.

* Mon Jun 25 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.11-1
- New upstream version 1.19.11.

* Fri Jun 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.10-1
- New upstream version 1.19.10.

* Mon Jun 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.9-1
- New upstream version 1.19.9.

* Thu Jun 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.8-1
- New upstream version 1.19.8.

* Thu Jun 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.7-2
- New upstream version 1.19.7.
- Require febotstrap >= 3.17.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-2
- Require febootstrap >= 3.16.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-1
- New upstream version 1.19.6.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-1
- New upstream version 1.19.6.
- This version defaults to using virtio-scsi.
- Requires qemu >= 1.0.
- Requires febootstrap >= 3.15.

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.5-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.5-1
- New upstream version 1.19.5.

* Thu Jun 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.4-1
- New upstream version 1.19.4.

* Fri Jun 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.3-2
- New upstream version 1.19.3.
- Remove patches which are now upstream.

* Tue May 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-3
- Remove obsolete list of bugs in make check rule.
- Remove some obsolete test workarounds.
- Disable i386 tests (because of RHBZ#825944).

* Mon May 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-2
- Include patches to fix udev.

* Mon May 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-1
- New upstream version 1.19.2.

* Sat May 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.1-1
- New upstream version 1.19.1.

* Mon May 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.0-1
- New upstream version 1.19.0.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.43-1
- New upstream version 1.17.43.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-4
- On RHEL 7 only, remove reiserfs-utils, zerofree.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-3
- On RHEL 7 only, remove nilfs-utils.

* Tue May 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-2
- Bundled gnulib (RHBZ#821767).

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-1
- New upstream version 1.17.42.

* Fri May 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.41-1
- New upstream version 1.17.41.

* Tue May 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.40-1
- New upstream version 1.17.40.

* Tue May  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-3
- Disable hfsplus-tools on RHEL 7.

* Thu May 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-2
- BR perl-XML-XPath to run the new XML test.

* Thu May 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-1
- New upstream version 1.17.39.

* Wed May 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.38-3
- Remove explicit runtime deps for old virt-sysprep.
- Add explicit runtime dep on fuse (RHBZ#767852, thanks Pádraig Brady).
- Remove explicit versioned dep on glibc.

* Tue May  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:1.17.38-2
- Update supported filesystems for ARM

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.38-1
- New upstream version 1.17.38.

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.37-2
- Add guestfs-faq(1) (FAQ is now a man page).

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.37-1
- New upstream version 1.17.37.

* Fri Apr 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.36-2
- Add upstream patch to fix installation of gobject headers.

* Thu Apr 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.36-1
- New upstream version 1.17.36.

* Thu Apr 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.35-1
- New upstream version 1.17.35.

* Tue Apr 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.34-1
- New upstream version 1.17.34.

* Mon Apr 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.33-1
- New upstream version 1.17.33.

* Tue Apr 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.32-1
- New upstream version 1.17.32.

* Mon Apr 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.31-1
- New upstream version 1.17.31.

* Fri Apr 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.30-1
- New upstream version 1.17.30.

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.29-1
- New upstream version 1.17.29.

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.28-2
- Enable ruby 1.9 patch in RHEL 7 (RHBZ#812139).

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.28-1
- New upstream version 1.17.28.

* Wed Apr 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.27-2
- Add guestfs-performance(1) manual page.

* Tue Apr 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.27-1
- New upstream version 1.17.27.

* Tue Apr 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.26-1
- New upstream version 1.17.26.

* Mon Apr 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.25-1
- New upstream version 1.17.25.

* Sun Apr 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.24-1
- New upstream version 1.17.24.

* Sun Apr 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.23-1
- New upstream version 1.17.23.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.22-2
- Include all gobject header files.
- Include gtk-doc, and depend on the gtk-doc package at runtime.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.22-1
- New upstream version 1.17.22.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.21-2
- Bump and rebuild.

* Wed Mar 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.21-1
- New upstream version 1.17.21.

* Mon Mar 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-3
- Reenable LUKS, since RHBZ#804345 is reported to be fixed.

* Sun Mar 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-2
- Disable LUKS tests because LUKS is broken in Rawhide (RHBZ#804345).

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-1
- New upstream version 1.17.20.

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.19-2
- Add libguestfs-make-fixed-appliance (with man page).

* Fri Mar 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.19-1
- New upstream version 1.17.19.

* Thu Mar 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.18-1
- New upstream version 1.17.18.

* Wed Mar 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.17-1
- New upstream version 1.17.17.

* Wed Mar 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.16-2
- Bump and rebuild.

* Tue Mar 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.16-1
- New upstream version 1.17.16.

* Mon Mar 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.15-1
- New upstream version 1.17.15.

* Fri Mar 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.14-1
- New upstream version 1.17.14.

* Thu Mar 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.13-1
- New upstream version 1.17.13.

* Thu Mar 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.12-2
- Enable Japanese man pages, since these are in a better state upstream.

* Wed Mar 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.12-1
- New upstream version 1.17.12.

* Wed Mar 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.11-2
- Require netpbm-progs, icoutils.  These are needed for icon generation
  during inspection, but were not being pulled in before.

* Mon Mar 05 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.11-1
- New upstream version 1.17.11.

* Sat Mar 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.10-2
- New upstream version 1.17.10.
- Rebase Ruby patch against new libguestfs.

* Wed Feb 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.9-1
- New upstream version 1.17.9.

* Wed Feb 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.8-1
- New upstream version 1.17.8.

* Mon Feb 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.7-1
- New upstream version 1.17.7.

* Fri Feb 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.6-1
- +BR ruby-irb.
- Make virtio unconditional.  It's been a very long time since disabling
  virtio was a good idea.
- Disable some packages not available in RHEL 7.
- New upstream version 1.17.6.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1:1.17.5-3
- Rebuild against PCRE 8.30

* Thu Feb  9 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.5-2
- Rebuild with ruby(abi) = 1.9.1.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.5-1
- New upstream version 1.17.5.
- Remove usrmove workaround patch, now upstream.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-8
- Further Ruby 1.9 changes.

* Tue Feb 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-7
- Bump and rebuild for Ruby update.

* Mon Feb  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-6
- Add workaround for usrmove in Fedora.

* Wed Feb  1 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-1
- New upstream version 1.17.4.
- Remove patch now upstream.

* Sat Jan 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.3-2
- New upstream version 1.17.3.
- Remove patch now upstream.
- Add upstream patch to fix OCaml bytecode compilation.

* Fri Jan 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.2-3
- Upstream patch to work with udev >= 176.

* Thu Jan 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.2-2
- New upstream version 1.17.2.
- Use libdb-utils instead of old db4-utils.
- net-tools is no longer used; replaced by iproute (RHBZ#784647).
- Try re-enabling tests on i686.

* Tue Jan 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.1-1
- New upstream version 1.17.1.

* Mon Jan 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.16.0-1
- New upstream version 1.16.0.
- Remove patches which are now upstream.
- GObject: Move *.typelib file to base gobject package.

* Sun Jan 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.19-1
- New upstream version 1.15.19.
- +BR psmisc for the appliance.
- Includes GObject bindings in libguestfs-gobject and
  libguestfs-gobject-devel subpackages.
- Include upstream patches for PHP 5.4.

* Thu Jan 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.18-1
- New upstream version 1.15.18.

* Wed Jan 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.17-1
- New upstream version 1.15.17.
- New tool: virt-format.

* Tue Jan 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.16-1
- New upstream version 1.15.16.

* Sun Jan  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.15-2
- New upstream version 1.15.15.
- Updated gnulib fixes builds with gcc 4.7.
- Rebuild for OCaml 3.12.1.
- Add explicit BR perl-hivex, required for various Perl virt tools.

* Fri Dec 23 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.14-1
- New upstream version 1.15.14.
- Remove three patches, now upstream.

* Thu Dec 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.13-4
- New upstream version 1.15.13.
- Fixes Security: Mitigate possible privilege escalation via SG_IO ioctl
  (CVE-2011-4127, RHBZ#757071).
- Add three upstream patches to fix 'make check'.

* Thu Dec 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.12-1
- New upstream version 1.15.12.

* Fri Dec  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.11-1
- New upstream version 1.15.11.

* Tue Dec  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.10-1
- New upstream version 1.15.10.
- Remove patch, now upstream.

* Sat Dec  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.9-2
- New upstream version 1.15.9.
- Add upstream patch to fix Augeas library detection.
- Appliance explicitly requires libxml2 (because Augeas >= 0.10 requires it),
  although it was implicitly included already.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.8-1
- New upstream version 1.15.8.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.7-1
- New upstream version 1.15.7.

* Thu Nov 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.6-1
- New upstream version 1.15.6.

* Mon Nov 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.5-1
- New upstream version 1.15.5.
- Add guestfs-testing(1) man page.

* Thu Nov 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.4-2
- New upstream version 1.15.4.
- Remove patch which is now upstream.
- libguestfs_jni.a is no longer built.

* Fri Nov 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.3-3
- Add upstream patch to disable part of virt-df test.

* Thu Nov 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.3-1
- New upstream version 1.15.3.
- Fix list of BuildRequires so they precisely match the appliance.

* Thu Nov  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.2-1
- New upstream version 1.15.2.
- ocaml-pcre is no longer required for virt-resize.
- xmlstarlet is no longer required for virt-sysprep.

* Tue Nov  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.1-1
- New upstream version 1.15.1.

* Fri Oct 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.0-1
- Stable branch 1.14.0 was released.  This is the new development
  branch version 1.15.0.

* Wed Oct 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.26-1
- New upstream version 1.13.26.

* Wed Oct 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.25-1
- New upstream version 1.13.25.

* Mon Oct 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.24-1
- New upstream version 1.13.24.
- This version includes upstream workarounds for broken qemu, so both
  non-upstream patches have now been removed from Fedora.

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.13.23-1.1
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.23-1
- New upstream version 1.13.23.

* Wed Oct 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.22-2
- New upstream version 1.13.22.
- Remove 3x upstream patches.
- Renumber the two remaining non-upstream patches as patch0, patch1.
- Rebase patch1.

* Mon Oct 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-4
- Add upstream patch to skip FUSE tests if there is no /dev/fuse.
  This allows us also to remove the Fedora-specific patch which
  disabled these tests before.

* Sat Oct 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-3
- Add upstream patch to fix virt-sysprep test.

* Fri Oct 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-2
- New upstream version 1.13.21.
- Move virt-sysprep to libguestfs-tools, to avoid pulling in extra
  dependencies for RHEV-H.  This tool is not likely to be useful
  for RHEV-H in its current form anyway.
- Change BR cryptsetup-luks -> cryptsetup since that package changed.

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 1:1.13.20-1.1
- rebuild with new gmp

* Tue Oct 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.20-1
- New upstream version 1.13.20.

* Sat Oct  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.19-1
- New upstream version 1.13.19.
- New tool: virt-sysprep.
- Remove the old guestfish and libguestfs-mount packages, and put these
  tools into libguestfs-tools.  This change is long overdue, but is also
  necessitated by the new virt-sysprep tool.  This new tool would pull
  in guestfish anyway, so having separate packages makes no sense.
- Remove old obsoletes for virt-cat, virt-df, virt-df2 and virt-inspector,
  since those packages existed only in much older Fedora.

* Wed Oct  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.18-1
- New upstream version 1.13.18.
- New tool: virt-alignment-scan.

* Tue Oct  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.17-1
- New upstream version 1.13.17.
- New tool: virt-sparsify.

* Sat Oct  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.16-1
- New upstream version 1.13.16.

* Thu Sep 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.15-2
- Rearrange description to make it clearer.
- virt-resize was written in OCaml.  Move it to libguestfs-tools-c
  subpackage since it doesn't require Perl.

* Wed Sep 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.15-1
- New upstream version 1.13.15.
- Add lzop program to the appliance (for compress-out API).
- Remove upstream patch.

* Mon Sep 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.14-2
- Upstream patch to fix timer check failures during boot (RHBZ#502058).

* Sat Sep 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.14-1
- New upstream version 1.13.14.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.13-1
- Add Erlang bindings in erlang-libguestfs subpackage.
- Remove upstream patch.

* Fri Sep 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.12-4
- Don't require grub.  See RHBZ#737261.
- Note this (hopefully temporarily) breaks guestfs_grub_install API.
- Include upstream patch to add guestfs_grub_install into an optional group.

* Wed Sep 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.12-1
- New upstream version 1.13.12.

* Thu Sep  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.11-1
- New upstream version 1.13.11.

* Tue Aug 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.10-2
- Remove MAKEDEV dependency (RHBZ#727247).

* Sun Aug 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.10-1
- New upstream version 1.13.10.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.9-1
- New upstream version 1.13.9.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.8-1
- New upstream version 1.13.8.
- Static python library is no longer built, so don't rm it.

* Tue Aug 23 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.7-1
- New upstream version 1.13.7.
- configure --with-extra version string contains Fedora release.
- Build with make V=1 to display full compile commands.
- Remove /usr/sbin PATH setting, not used for a very long time.

* Fri Aug 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.6-2
- New upstream version 1.13.6.
- Rebase non-upstream patch to fix qemu -machine option.

* Wed Aug 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.5-1
- New upstream version 1.13.5.

* Thu Aug 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.4-1
- New upstream version 1.13.4.

* Mon Aug  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.3-4
- New upstream version 1.13.3.
- 'test-getlogin_r.c:55: assertion failed' test must now be fixed in
  gnulib/tests directory instead of daemon/tests (the latter directory
  no longer exists).
- Only run testsuite on x86_64 because of qemu bug.

* Tue Aug  2 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.2-3
- Switch Rawhide to use the new development branch (1.13).
- New upstream version 1.13.2.
- Remove upstream patch.
- Ensure config.log is printed, even in the error case.

* Tue Jul 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.1-4
- New upstream stable branch version 1.12.1.
- Remove 5 x upstream patches.
- Add non-upstream patch to deal with broken qemu -machine option.
- Add upstream patch to fix segfault in OCaml bindings.

* Tue Jul 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-11
- Bump and rebuild.

* Fri Jul 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-10
- Rebuild against fixed hivex 1.2.7-7 in dist-f16-perl.

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-9
- Attempt rebuild in dist-f16-perl.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:1.12.0-8
- Perl mass rebuild

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-4
- Disable tests, use quickcheck, because of RHBZ#723555, RHBZ#723822.

* Wed Jul 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-2
- Readd patch to fix virtio-serial test for qemu 0.15.

* Wed Jul 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-1
- New stable version 1.12.0 for Fedora 16.
- Remove upstream patch.
- Disable tests on i686 (because of RHBZ#723555).

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:1.11.20-3
- Perl mass rebuild

* Tue Jul 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.20-2
- Add upstream patch to fix virtio-serial test for qemu 0.15.

* Tue Jul 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.20-1
- New upstream version 1.11.20.
- Replace standard README file with one suited for Fedora.
- Add guestfs-java(3) manpage to libguestfs-java-devel package.

* Mon Jul 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.19-1
- New upstream version 1.11.19.
- Remove upstream patch.
- Add Ukrainian (uk) man pages subpackage.

* Fri Jul 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.18-2
- Add upstream patch to fix regression test.

* Fri Jul 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.18-1
- New upstream version 1.11.18.
- Force febootstrap >= 3.7 which contains a fix for latest Rawhide.
- Use --enable-install-daemon to install guestfsd.

* Thu Jul 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.17-1
- New upstream version 1.11.17.

* Wed Jul 13 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.16-1
- New upstream version 1.11.16.

* Tue Jul 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.15-1
- New upstream version 1.11.15.

* Wed Jul  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.14-1
- New upstream version 1.11.14.

* Wed Jul  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-3
- Further updates to libguestfs-live-service after feedback from
  Dan Berrange and Lennart Poettering.

* Tue Jul  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-2
- Add libguestfs-live-service subpackage.  This can be installed in
  virtual machines in order to enable safe editing of files in running
  guests (eg. guestfish --live).

* Thu Jun 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-1
- New upstream version 1.11.13.

* Wed Jun 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.12-3
- Bump and rebuild for parted 3.0.
- Depend on fixed parted >= 3.0-2.

* Tue Jun 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.12-1
- New upstream version 1.11.12.

* Tue Jun 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.11-1
- New upstream version 1.11.11.

* Mon Jun 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.10-3
- Temporarily stop setting CCFLAGS in perl subdirectory.
  See: http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=628522

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.11.10-2
- Perl mass rebuild

* Fri Jun 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.10-1
- New upstream version 1.11.10.
- Enable tests since fix for RHBZ#710921 is in Rawhide kernel package.

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.11.9-8
- Perl 5.14 mass rebuild

* Sun Jun  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.9-7
- Build against new parted.
- Disable tests on i686 because of RHBZ#710921.
- Remove recipes/ doc directory.  This is no longer present because it
  was replaced by a guestfs-recipes(1) man page.

* Sat Jun  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.9-1
- New upstream version 1.11.9.

* Wed May 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.8-1
- New upstream version 1.11.8.
- "zero" command test is fixed now, so we don't need to skip it.

* Tue May 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.7-3
- New upstream version 1.11.7.
- Depends on hivex >= 1.2.7.
- Remove upstream patch.
- Skip test of "zero" command (RHBZ#705499).

* Mon May  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.5-2
- configure: Use Python platform-dependent site-packages.

* Mon May  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.5-1
- New upstream version 1.11.5.
- virt-edit has been rewritten in C, therefore this tool has been moved
  into the libguestfs-tools-c package.

* Sun May  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.4-1
- New upstream version 1.11.4.

* Fri Apr 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.3-1
- New upstream version 1.11.3.

* Mon Apr 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.2-1
- New upstream version 1.11.2.
- Fixes Python bindings when used in Python threads.
- Remove upstream patch.

* Sat Apr 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.1-2
- New upstream version 1.11.1.
- Add upstream patch so we don't depend on libtool.

* Fri Apr 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.0-2
- Bump and rebuild.

* Tue Apr 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.0-1
- New upstream development branch 1.11.0.
- New Source URL.
- Remove patches which are now upstream.

* Sun Apr 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.18-4
- Include further fixes to virt-resize from upstream.

* Sat Apr  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.18-2
- New upstream version 1.9.18.
- Requires ocaml-pcre for new virt-resize.
- Remove libguestfs-test-tool-helper program which is no longer used.
- Include upstream fix for virt-resize build.

* Wed Apr  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.17-2
- Remove partially translated Ukrainian manpages.

* Tue Apr  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.17-1
- New upstream version 1.9.17.

* Fri Apr  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.16-1
- New upstream version 1.9.16.

* Fri Apr  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.15-1
- New upstream version 1.9.15.
- Add BR libconfig-devel.
- Add /etc/libguestfs-tools.conf (config file for guestfish, guestmount,
  virt-rescue; in future for other tools as well).

* Mon Mar 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.14-1
- New upstream version 1.9.14.
- Include 'acl' as BR so virt-rescue gets getfacl and setfacl programs.

* Mon Mar 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.13-2
- Include 'attr' as BR (required for getfattr, setfattr programs in
  virt-rescue).

* Thu Mar 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.13-1
- New upstream version 1.9.13.

* Fri Mar 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.12-1
- New upstream version 1.9.12.

* Wed Mar 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.11-2
- Add runtime requires on minimum glibc because of newly readable binaries.

* Tue Mar 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.11-1
- New upstream version 1.9.11.
- Add generated Ruby documentation (rdoc).

* Tue Mar  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.10-1
- New upstream version 1.9.10.
- Remove patches (now upstream).

* Fri Mar  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.9-2
- Include upstream patches to fix virt-make-fs with qemu-img 0.14.

* Fri Mar  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.9-1
- New upstream version 1.9.9.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.8-1
- New upstream version 1.9.8.

* Sun Feb  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-7
- Rebuild against rpm-4.9.0-0.beta1.6.fc15 to fix OCaml deps.  See discussion:
  http://lists.fedoraproject.org/pipermail/devel/2011-February/148398.html

* Wed Feb  2 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-6
- Add temporary non-upstream patch to fix /etc/mtab.
  See: https://www.redhat.com/archives/libguestfs/2011-February/msg00006.html
- Add fix for regressions/rhbz557655.sh so it works when tracing is enabled.
- Add guestfs-perl(3) man page.

* Tue Feb  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-3
- Enable trace in 'make check' section.

* Sun Jan 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-1
- New upstream version 1.9.7.

* Wed Jan 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.6-2
- Bump and rebuild.

* Sat Jan 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.6-1
- New upstream version 1.9.6.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.5-1
- New upstream version 1.9.5.

* Sat Jan 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.4-1
- New upstream version 1.9.4.

* Fri Jan 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.3-2
- Only runtime require febootstrap-supermin-helper (not whole of
  febootstrap).

* Tue Jan 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.3-1
- New upstream version 1.9.3.

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.2-2
- Bump and rebuild.

* Mon Jan  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.2-1
- New upstream version 1.9.2.
- New tools: virt-copy-in, virt-copy-out, virt-tar-in, virt-tar-out.
  These are just shell script wrappers around guestfish so they are
  included in the guestfish package.

* Fri Dec 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.1-1
- New upstream version 1.9.1.

* Tue Dec 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.0-2
- Bump and rebuild.

* Sun Dec 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.0-1
- New upstream development branch 1.9.0.
- Include ROADMAP in devel package.

* Thu Dec 16 2010 Richard Jones <rjones@redhat.com> - 1:1.7.24-1
- New upstream version 1.7.24.
- Adds getxattr/lgetxattr APIs to support guestfs-browser.

* Sat Dec 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.23-1
- New upstream version 1.7.23.

* Sat Dec 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.22-1
- New upstream version 1.7.22.
- Depend on febootstrap 3.3 which fixes the checksum stability problem.

* Fri Dec 10 2010 Richard Jones <rjones@redhat.com> - 1:1.7.21-1
- New upstream version 1.7.21.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 1:1.7.20-1
- New upstream version 1.7.20.
- Remove patches which are upstream.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-15
- Rebuild appliance with febootstrap 3.1-5 because we accidentally
  reopened RHBZ#654638.

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-14
- Rebuild appliance properly using febootstrap 3.1 and alternate yum repo.

* Sun Dec  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-1
- New upstream development version 1.7.19.
- Appliance building in this version has been substantially rewritten
  and this requires febootstrap >= 3.0 to build.
- createrepo no longer required.
- Supermin appliance is the default.

* Wed Dec  1 2010 Richard Jones <rjones@redhat.com> - 1:1.7.18-1
- New upstream development version 1.7.18.

* Tue Nov 30 2010 Richard Jones <rjones@redhat.com> - 1:1.7.17-1
- New upstream development version 1.7.17.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.16-1
- New upstream development version 1.7.16.
- guestfish no longer requires pod2text, hence no longer requires perl.
- Require febootstrap >= 2.11.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.15-2
- New upstream development version 1.7.15.
- Split out new libguestfs-tools-c package from libguestfs-tools.
  . This is so that the -tools-c package can be pulled in by people
    wanting to avoid a dependency on Perl, while -tools pulls in everything
    as before.
  . The C tools currently are: cat, df, filesystems, fish, inspector, ls,
    mount, rescue.
  . guestfish still requires pod2text which requires perl.  This will be
    rectified in the next release.
  . libguestfs-tools no longer pulls in guestfish.
- guestfish also depends on: less, man, vi
- Add BR db4-utils (although since RPM needs it, it not really necessary).
- Runtime requires on db4-utils should be on core lib, not tools package.
- Change all "Requires: perl-Foo" to "Requires: perl(Foo)".

* Thu Nov 25 2010 Richard Jones <rjones@redhat.com> - 1:1.7.14-1
- New upstream development version 1.7.14.

* Wed Nov 24 2010 Richard Jones <rjones@redhat.com> - 1:1.7.13-3
- New upstream development version 1.7.13.
- New manual pages containing example code.
- Ship examples for C, OCaml, Ruby, Python.
- Don't ship HTML versions of man pages.
- Rebase no-fuse-test patch to latest version.

* Tue Nov 23 2010 Richard Jones <rjones@redhat.com> - 1:1.7.12-1
- New upstream development version 1.7.12.
- New tool: virt-filesystems.  virt-list-filesystems and virt-list-partitions
  are deprecated, but still included in the package.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.11-1
- New upstream development version 1.7.11.
- Fix Source0 URL which had pointed to the 1.5 directory.
- virt-inspector is not a dependency of guestmount.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.10-1
- New upstream development version 1.7.10.

* Tue Nov 16 2010 Richard Jones <rjones@redhat.com> - 1:1.7.9-1
- New upstream development version 1.7.9.

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.8-1
- New upstream development version 1.7.8.
- Add Obsoletes so perl-Sys-Guestfs overrides perl-libguestfs (RHBZ#652587).

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.7-1
- New upstream development version 1.7.7.
- Rename perl-libguestfs as perl-Sys-Guestfs (RHBZ#652587).

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.6-1
- New upstream development version 1.7.6.

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.5-2
- New upstream development version 1.7.5.
- Remove hand-installation of Ruby bindings.
- Remove upstream patch.

* Thu Nov 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.4-2
- New upstream development version 1.7.4.
- ocaml-xml-light is no longer required.
- Remove guestfs-actions.h and guestfs-structs.h.  Libguestfs now
  only exports a single <guestfs.h> header file.
- Add patch to fix broken Perl test.
- Remove workaround for RHBZ#563103.

* Mon Nov  8 2010 Richard Jones <rjones@redhat.com> - 1:1.7.3-1
- New upstream development version 1.7.3.
- Add AUTHORS file from tarball.

* Fri Nov  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.2-1
- New upstream development version 1.7.2.
- Add requires ruby to ruby-libguestfs package.

* Wed Nov  3 2010 Richard Jones <rjones@redhat.com> - 1:1.7.1-1
- New upstream development version 1.7.1.
- Add BR gperf.

* Tue Nov  2 2010 Richard Jones <rjones@redhat.com> - 1:1.7.0-1
- New upstream development branch and version 1.7.0.

* Fri Oct 29 2010 Richard Jones <rjones@redhat.com> - 1:1.5.26-1
- New upstream development version 1.5.26.

* Thu Oct 28 2010 Richard Jones <rjones@redhat.com> - 1:1.5.25-1
- New upstream development version 1.5.25.
- Rewritten virt-inspector.
- Requires febootstrap >= 2.10.
- New virt-inspector requires db_dump program.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-2
- Attempt to run tests.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-1
- New upstream development version 1.5.24.

* Sat Oct 23 2010 Richard Jones <rjones@redhat.com> - 1:1.5.23-1
- Fix for libguestfs: missing disk format specifier when adding a disk
  (RHBZ#642934, CVE-2010-3851).

* Tue Oct 19 2010 Richard Jones <rjones@redhat.com> - 1:1.5.22-1
- New upstream development version 1.5.22.

* Sat Oct  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-2
- guestfish no longer requires virt-inspector.

* Fri Oct  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-1
- New upstream development version 1.5.21.

* Sun Sep 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.20-1
- New upstream development version 1.5.20.

* Wed Sep 22 2010 Richard Jones <rjones@redhat.com> - 1:1.5.18-1
- New upstream development version 1.5.18.
- Note that guestfish '-a' and '-d' options were broken in 1.5.17, so
  upgrading to this version is highly recommended.

* Tue Sep 21 2010 Richard Jones <rjones@redhat.com> - 1:1.5.17-1
- New upstream development version 1.5.17.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.16-1
- New upstream development version 1.5.16.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.15-1
- New upstream development version 1.5.15.

* Tue Sep 14 2010 Richard Jones <rjones@redhat.com> - 1:1.5.14-1
- New upstream development version 1.5.14.

* Mon Sep 13 2010 Richard Jones <rjones@redhat.com> - 1:1.5.13-1
- New upstream version 1.5.13.
- Removed the patch workaround for RHBZ#630583.  The same workaround
  is now upstream (the bug is not fixed).

* Sat Sep 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.12-1
- New upstream version 1.5.12.

* Fri Sep 10 2010 Richard Jones <rjones@redhat.com> - 1:1.5.11-1
- New upstream version 1.5.11.
- Note: fixes a serious bug in guestfish 'copy-out' command.

* Thu Sep  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.10-1
- New upstream version 1.5.10.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-2
- Disable tests, still failing because of RHBZ#630777.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-1
- New upstream version 1.5.9.

* Mon Sep  6 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-2
- Add patch to work around RHBZ#630583 and reenable tests.

* Sat Sep  4 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-1
- New upstream version 1.5.8.
- Add BR po4a for translations of man pages.
- Add PHP bindings.
- Remove partially-translated Japanese webpages.

* Wed Sep  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.7-1
- New upstream version 1.5.7.
- 'debug' command is enabled by default now.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.6-1
- New upstream version 1.5.6.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-2
- Use bug-fixed febootstrap 2.9.

* Thu Aug 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-1
- New upstream version 1.5.5.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-2
- Disable tests again, because the Rawhide kernel still won't boot.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-1
- New upstream development version 1.5.4.
- Now requires febootstrap >= 2.8 and qemu >= 0.12.
- Re-enable tests because RHBZ#624854 is supposed to be fixed.
- Upstream Source URL has changed.

* Wed Aug 18 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-2
- Disable tests because of RHBZ#624854.

* Tue Aug 17 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-1
- New upstream development version 1.5.3.

* Wed Aug 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.2-6
- Bump and rebuild.

* Thu Aug 05 2010 Richard Jones - 1:1.5.2-5
- Bump and rebuild.

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.2-2
- New upstream development version 1.5.2.
- +BuildRequires: cryptsetup-luks.

* Wed Jul 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.1-1
- New upstream development version 1.5.1.

* Tue Jul 20 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-7
- Requires binutils (RHBZ#616437).

* Mon Jul 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-6
- Fix libguestfs-find-requires.sh for new location of hostfiles (RHBZ#615946).

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-5
- Include RELEASE-NOTES in devel package.

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-4
- New development branch 1.5.0.
- Remove two upstream patches.
- Work around permanently broken test-getlogin_r Gnulib test.

* Mon Jun 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-4
- Explicitly depend on e2fsprogs.
- Add patch to add e2fsprogs to the appliance.
- Add patch to fix GFS kernel module problem.

* Fri Jun 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.3.21-2
- Rebuild

* Wed Jun 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-1
- New upstream version 1.3.21.

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.20-1
- New upstream version 1.3.20.
- Since upstream commit a043b6854a0c4 we don't need to run make install
  twice.

* Fri Jun  4 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.19-1
- New upstream version 1.3.19.

* Wed Jun  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.18-1
- New upstream version 1.3.18.

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.17-1
- New upstream version 1.3.17.
- Change repo name to 'fedora-14'.

* Wed May 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-6
- Co-own bash_completion.d directory.

* Tue May 25 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-4
- New upstream version 1.3.16.
- Add guestfish bash tab completion script.

* Mon May 24 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.14-1
- New upstream version 1.3.14.

* Sun May 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.13-1
- New upstream version 1.3.13.
- Add BUGS to documentation.
- Force update of hivex dependency to 1.2.2 since it contains
  important registry import fixes.
- Remove patch1, now upstream.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-3
- Backport supermin build fix from upstream.
- Further changes required for new layout of supermin appliance.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-1
- New upstream version 1.3.12.
- febootstrap >= 2.7 is required at compile time and at runtime (at runtime
  because of the new febootstrap-supermin-helper).
- Bugs fixed: 591155 591250 576879 591142 588651 507810 521674 559963 516096.

* Sat May  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.11-1
- New upstream version 1.3.11.

* Fri May  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.10-2
- New upstream version 1.3.10.

* Thu May 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-2
- Bump and rebuild against updated libconfig

* Fri Apr 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-1
- New upstream version 1.3.9.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.3.8-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.8-1
- New upstream version 1.3.8.

* Fri Apr 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.7-1
- New upstream version 1.3.7.
- NOTE: fixes a segfault in guestfish 1.3.6 when using the -a option.

* Thu Apr 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.6-1
- New upstream version 1.3.6.

* Mon Apr 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-1
- New upstream version 1.3.5.

* Sat Apr 17 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.4-1
- New upstream version 1.3.4.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.3-1
- New upstream version 1.3.3.
- New virt-resize option --LV-expand.
- New API: lvresize-free.
- Fixes RHBZ#581501.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-3
- Disable checksum-device test.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-2
- Bump and rebuild.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-1
- New upstream version 1.3.2.
- New APIs: checksum-device, part-del, part-get-bootable, part-get-mbr-id,
  part-set-mbr-id, vgscan, ntfsresize, txz-in, txz-out.
- Enhanced/fixed virt-resize tool.
- Enhanced virt-list-partitions tool.
- Fixes: 580016, 580650, 579155, 580556.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-4
- Bump and rebuild.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-3
- Runtime requires should only be on libguestfs-tools subpackage.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-2
- Missing BR on qemu-img package.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-1
- New upstream version 1.3.1.
- For explanation of apparently large version jump, see:
  https://www.redhat.com/archives/libguestfs/2010-April/msg00057.html
- New tool: virt-make-fs.
- New API: guestfs_zero_device.
- Fixes RHBZ#580246 (tar-in command hangs if uploading more than
  available space)
- Fixes RHBZ#579664 (guestfish doesn't report error when there is not
  enough space for image allocation)
- +BR perl-String-ShellQuote (for virt-make-fs).

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.89-1
- New upstream version 1.0.89.
- Improved version of virt-win-reg.
- Many smaller bugfixes.
- Requires hivex >= 1.2.1.
- Remove TERM=dumb patch which is now upstream.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-7
- Backport of TERM=dumb patch from upstream.
- Workaround failure caused by RHBZ#575734.
- Workaround unknown failure of test_swapon_label_0.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-5
- Attempted workaround for RHBZ#563103, so we can reenable tests.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-2
- Remember to check in the new sources.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-1
- New upstream version 1.0.88.
- Mainly small bugfixes.
- Update Spanish translation of libguestfs (RHBZ#576876).
- Use ext4 dev tools on RHEL 5 (RHBZ#576688).
- Add support for minix filesystem (RHBZ#576689).

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-2
- Add vim-minimal to BR, it is now required by the appliance.

* Tue Mar 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-1
- New upstream version 1.0.87.
- New tools: virt-resize and virt-list-partitions.
- New APIs: guestfs_copy_size; APIs for querying the relationship between
  LVM objects.
- Add vim to the virt-rescue appliance.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.86-1
- New upstream version 1.0.86.
- libguestfs-supermin-helper rewritten in C (from shell), reduces
  appliance boot time by 2-3 seconds.
- Fix parsing of integers in guestfish on 32 bit platforms (RHBZ#569757
  and RHBZ#567567).
- Enhance virt-inspector output for Windows guests.
- Add product_name field to virt-inspector output for all guests.
- Weaken dependencies on libntfs-3g.so, don't include SONAME in dep.
- Remove false dependency on libply (plymouth libraries).
- Spanish translation (RHBZ#570181).
- Fix bash regexp quoting bug.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-4
- Bump and rebuild.

* Thu Mar 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-3
- Bump and rebuild.

* Sat Mar 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2
- Bump and rebuild.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-1
- New upstream version 1.0.85.
- Remove hivex, now a separate upstream project and package.
- Remove supermin quoting patch, now upstream.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-6
- Fix quoting in supermin-split script (RHBZ#566511).
- Don't include bogus './builddir' entries in supermin hostfiles
  (RHBZ#566512).

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-4
- Don't include generator.ml in rpm.  It's 400K and almost no one will need it.
- Add comments to spec file about how repo building works.
- Whitespace changes in the spec file.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-3
- Bump and rebuild.

* Tue Feb 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-2
- Bump and rebuild.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-1
- New upstream version 1.0.84.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.83-8
- Bump and rebuild.

* Thu Feb 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-7
- Disable tests.  These fail in Koji (on RHEL 5 kernel) because of a
  bug in preadv/pwritev emulation in glibc (RHBZ#563103).

* Tue Feb  9 2010 Matthew Booth <mbooth@redhat.com> - 1.0.83-6
- Change buildnonet to buildnet
- Allow buildnet, mirror, updates, virtio and runtests to be configured by user
  macros.

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-5
- libguestfs-tools should require perl-XML-Writer (RHBZ#562858).

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-4
- Use virtio for block device access (RHBZ#509383 is fixed).

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-3
- Rebuild: possible timing-related build problem in Koji.

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-2
- New upstream release 1.0.83.
- This release fixes:
  Add Marathi translations (RHBZ#561671).
  Polish translations (RHBZ#502533).
  Add Gujarti translations (Sweta Kothari) (RHBZ#560918).
  Update Oriya translations (thanks Manoj Kumar Giri) (RHBZ#559498).
  Set locale in C programs so l10n works (RHBZ#559962).
  Add Tamil translation (RHBZ#559877) (thanks to I.Felix)
  Update Punjabi translation (RHBZ#559480) (thanks Jaswinder Singh)
- There are significant fixes to hive file handling.
- Add hivexsh and manual page.
- Remove two patches, now upstream.

* Sun Jan 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.82-7
- Bump and rebuild.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-6
- Backport a better fix for RHBZ557655 test from upstream.
- Backport fix for unreadable yum.log from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-3
- Backport RHBZ557655 test fix from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-1
- New upstream version 1.0.82.  This includes the two patches
  we were carrying, so those are now removed.
- This release fixes:
  RHBZ#559498 (Oriya translation).
  RHBZ#559480 (Punjabi translation).
  RHBZ#558593 (Should prevent corruption by multilib).
  RHBZ#559237 (Telugu translation).
  RHBZ#557655 (Use xstrtol/xstrtoll to parse integers in guestfish).
  RHBZ#557195 (Missing crc kernel modules for recent Linux).
- In addition this contains numerous fixes to the hivex library
  for parsing Windows Registry files, making hivex* and virt-win-reg
  more robust.
- New API call 'filesize'.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-8
- Backport special handling of libgcc_s.so.
- Backport unreadable files patch from RHEL 6 / upstream.

* Fri Jan 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-5
- Require febootstrap >= 2.6 (RHBZ#557262).

* Thu Jan 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-4
- Rebuild for unannounced soname bump (libntfs-3g.so).

* Fri Jan 15 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-3
- Rebuild for unannounced soname bump (libplybootsplash.so).

* Thu Jan 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-2
- Rebuild for broken dependency (iptables soname bump).

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-1
- New upstream version 1.0.81.
- Remove two upstream patches.
- virt-inspector: Make RPM application data more specific (RHBZ#552718).

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-14
- Reenable tests because RHBZ#553689 is fixed.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-13
- Rebuild because of libparted soname bump (1.9 -> 2.1).

* Fri Jan  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-12
- qemu in Rawhide is totally broken (RHBZ#553689).  Disable tests.

* Thu Jan  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-11
- Remove gfs-utils (deprecated and removed from Fedora 13 by the
  upstream Cluster Suite developers).
- Include patch to fix regression in qemu -serial stdio option.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-10
- Remove some debugging statements which were left in the requires
  script by accident.

* Mon Dec 21 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-9
- Generate additional requires for supermin (RHBZ#547496).

* Fri Dec 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-3
- Work around udevsettle command problem (RHBZ#548121).
- Enable tests.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-2
- Disable tests because of RHBZ#548121.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-1
- New upstream release 1.0.80.
- New Polish translations (RHBZ#502533).
- Give a meaningful error if no usable kernels are found (RHBZ#539746).
- New tool: virt-list-filesystems

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.0.79-3
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.79-2
- New upstream release 1.0.79.
- Adds FUSE test script and multiple fixes for FUSE (RHBZ#538069).
- Fix virt-df in Xen (RHBZ#538041).
- Improve speed of supermin appliance.
- Disable FUSE-related tests because Koji doesn't currently allow them.
  fuse: device not found, try 'modprobe fuse' first

* Tue Nov 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.78-2
- New upstream release 1.0.78.
- Many more filesystem types supported by this release - add them
  as dependencies.

* Tue Nov  3 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.77-1
- New upstream release 1.0.77.
- Support for mounting guest in host using FUSE (guestmount command).
- hivex*(1) man pages should be in main package, not -devel, since
  they are user commands.
- libguestfs-tools: Fix "self-obsoletion" issue raised by rpmlint.
- perl: Remove bogus script Sys/bindtests.pl.

* Thu Oct 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.75-2
- New upstream release 1.0.75.
- New library: libhivex.
- New tools: virt-win-reg, hivexml, hivexget.
- Don't require chntpw.
- Add BR libxml2-devel, accidentally omitted before.

* Tue Oct 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.74-1
- New upstream release 1.0.74.
- New API call: guestfs_find0.
- New tools: virt-ls, virt-tar.

* Wed Oct 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.73-1
- New upstream release 1.0.73.
- OCaml library now depends on xml-light.
- Deal with installed documentation.

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-2
- Force rebuild.

* Wed Sep 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-1
- New upstream release 1.0.72.
- New tools: virt-edit, virt-rescue.
- Combine virt-cat, virt-df, virt-edit, virt-inspector and virt-rescue
  into a single package called libguestfs-tools.

* Tue Sep 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.71-2
- New upstream release 1.0.71.

* Fri Sep 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-2
- Perl bindings require perl-XML-XPath (fixed RHBZ#523547).

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-1
- New upstream release 1.0.70.
- Fixes build problem related to old version of GNU gettext.

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.69-1
- New upstream release 1.0.69.
- Reenable the tests (because RHBZ#516543 is supposed to be fixed).
- New main loop code should fix RHBZ#501888, RHBZ#504418.
- Add waitpid along guestfs_close path (fixes RHBZ#518747).

* Wed Aug 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.68-2
- New upstream release 1.0.68.
- BR genisoimage.

* Thu Aug 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.67-2
- New upstream release 1.0.67.

* Fri Aug  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-5
- Set network interface to ne2k_pci (workaround for RHBZ#516022).
- Rerun autoconf because patch touches configure script.

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-1
- New upstream release 1.0.66.

* Wed Jul 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.65-1
- New upstream release 1.0.65.
- Add Obsoletes for virt-df2 (RHBZ#514309).
- Disable tests because of ongoing TCG problems with newest qemu in Rawhide.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-3
- RHBZ#513249 bug in qemu is now fixed, so try to rebuild and run tests.
- However RHBZ#503236 still prevents us from testing on i386.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-1
- New upstream release 1.0.64.
- New tool 'libguestfs-test-tool'.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.61-1
- New upstream release 1.0.61.
- New tool / subpackage 'virt-cat'.
- New BR perl-libintl.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-2
- Fix runtime Requires so they use epoch correctly.

* Tue Jul 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-1
- New upstream release 1.0.60.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.58-2
- New upstream release 1.0.58.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.57-1
- New upstream release 1.0.57.
- New tool virt-df (obsoletes existing package with this name).
- RHBZ#507066 may be fixed, so reenable tests.

* Tue Jul  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.56-2
- New upstream release 1.0.56.
- Don't rerun generator.

* Thu Jul  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.55-1
- New upstream release 1.0.55.
- New manual page libguestfs(3).

* Mon Jun 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.54-2
- New upstream release 1.0.54.
- +BR perl-XML-Writer.

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.53-1
- New upstream release 1.0.53.
- Disable all tests (because of RHBZ#507066).

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.52-1
- New upstream release 1.0.52.

* Mon Jun 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.51-1
- New upstream release 1.0.51.
- Removed patches which are now upstream.

* Sat Jun 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-5
- Remove workaround for RHBZ#507007, since bug is now fixed.
- Pull in upstream patch to fix pclose checking
  (testing as possible fix for RHBZ#507066).
- Pull in upstream patch to check waitpid return values
  (testing as possible fix for RHBZ#507066).

* Fri Jun 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-2
- New upstream release 1.0.49.
- Add workaround for RHBZ#507007.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-2
- Accidentally omitted the supermin image from previous version.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-1
- New upstream release 1.0.48.
- Should fix all the brokenness from 1.0.47.
- Requires febootstrap >= 2.3.

* Mon Jun 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.47-2
- New upstream release 1.0.47.
- Enable experimental supermin appliance build.
- Fix path to appliance.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.45-2
- New upstream release 1.0.45.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-2
- Disable ppc/ppc64 tests again because of RHBZ#505109.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- Try enabling tests on ppc & ppc64 since it looks like the bug(s?)
  in qemu which might have caused them to fail have been fixed.

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.43-1
- New upstream version 1.0.43.
- New upstream URL.
- Requires chntpw program.

* Sat Jun  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.42-1
- New upstream version 1.0.42.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.41-1
- New upstream version 1.0.41.
- Fixes a number of regressions in RHBZ#503169.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.40-1
- New upstream version 1.0.40.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.39-1
- New upstream version 1.0.39.
- Fixes:
  . libguestfs /dev is too sparse for kernel installation/upgrade (RHBZ#503169)
  . OCaml bindings build failure (RHBZ#502309)

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-2
- Disable tests on ix86 because of RHBZ#503236.

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.36-2
- New upstream version 1.0.36.
- Rerun the generator in prep section.

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Fixes multiple bugs in bindings parameters (RHBZ#501892).

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.34-1
- New upstream version 1.0.34.

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.33-1
- New upstream version 1.0.33.
- --with-java-home option is no longer required.
- Upstream contains potential fixes for:
    501878 built-in commands like 'alloc' and 'help' don't autocomplete
    501883 javadoc messed up in libguestfs java documentation
    501885 Doesn't detect missing Java, --with-java-home=no should not be needed
    502533 Polish translation of libguestfs
    n/a    Allow more ext filesystem kmods (Charles Duffy)

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.32-2
- New upstream version 1.0.32.
- Use %%find_lang macro.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.31-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.0.31.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.30-1
- New upstream version 1.0.30.  Now includes test-bootbootboot.sh script.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.29-3
- New upstream version 1.0.29 (fixes RHBZ#502007 RHBZ#502018).
- This should allow us to enable tests for i386 and x86-64.
- Added test-bootbootboot.sh script which was missed from 1.0.29 tarball.
- Pass kernel noapic flag to workaround RHBZ#502058.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.28-1
- New upstream version 1.0.28.  Nothing has visibly changed, but
  the source has been gettextized and we want to check that doesn't
  break anything.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.27-3
- Change requirement from qemu -> qemu-kvm (RHBZ#501761).

* Tue May 19 2009 Richard Jones <rjones@redhat.com> - 1.0.27-2
- New upstream version 1.0.27.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-6
- Experimentally try to reenable ppc and ppc64 builds.
- Note BZ numbers which are causing tests to fail.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-1
- New upstream version 1.0.26.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.25-4
- New upstream version 1.0.25.
- Enable debugging when running the tests.
- Disable tests - don't work correctly in Koji.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.24-1
- New upstream version 1.0.24.
- BRs glibc-static for the new command tests.
- Enable tests.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-2
- New upstream version 1.0.23.
- Don't try to use updates during build.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-3
- New upstream version 1.0.21.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.20-2
- New upstream version 1.0.20.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.19-1
- New upstream version 1.0.19.

* Tue Apr 28 2009 Richard Jones <rjones@redhat.com> - 1.0.15-1
- New upstream version 1.0.15.

* Fri Apr 24 2009 Richard Jones <rjones@redhat.com> - 1.0.12-1
- New upstream version 1.0.12.

* Wed Apr 22 2009 Richard Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Thu Apr 16 2009 Richard Jones <rjones@redhat.com> - 0.9.9-12
- Multiple fixes to get it to scratch build in Koji.

* Sat Apr  4 2009 Richard Jones <rjones@redhat.com> - 0.9.9-1
- Initial build.
