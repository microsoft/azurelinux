## START: Set by rpmautospec
## (rpmautospec version 0.7.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# The testsuite is disabled by default.
#
# To build and run the tests use:
#
# fedpkg mockbuild --with testsuite
# or
# rpmbuild --rebuild --with testsuite samba.src.rpm
#
%bcond_with testsuite

# Build with internal talloc, tevent, tdb
#
# fedpkg mockbuild --with=testsuite --with=includelibs
# or
# rpmbuild --rebuild --with=testsuite --with=includelibs samba.src.rpm
#
%bcond_with includelibs

# fedpkg mockbuild --with=ccache
%bcond_with ccache

# ctdb is enabled by default, you can disable it with: --without clustering
%bcond_without clustering

# Define _make_verbose if it doesn't exist (RHEL8)
%{!?_make_verbose:%define _make_verbose V=1 VERBOSE=1}

# Build with Active Directory Domain Controller support by default on Fedora
%if 0%{?fedora}
%bcond_without dc
%else
%bcond_with dc
%endif

# Build a libsmbclient package by default
%bcond_without libsmbclient

# Build a libwbclient package by default
%bcond_without libwbclient

# Build with winexe by default
%if 0%{?rhel}

%ifarch x86_64
%bcond_without winexe
%else
%bcond_with winexe
#endifarch
%endif

%else
%bcond_without winexe
%endif

# Build vfs_ceph module and ctdb cepth mutex helper by default on 64bit Fedora
%if 0%{?fedora}

%ifarch aarch64 ppc64le s390x x86_64 riscv64
%bcond_without vfs_cephfs
%bcond_without ceph_mutex
%else
%bcond_with vfs_cephfs
%bcond_with ceph_mutex
#endifarch
%endif

%else
%bcond_with vfs_cephfs
%bcond_with ceph_mutex
#endif fedora
%endif

# Build vfs_gluster module by default on 64bit Fedora
%global is_rhgs 0
%if "%{dist}" == ".el7rhgs" || "%{dist}" == ".el8rhgs"
%global is_rhgs 1
%endif

%if 0%{?fedora}

%ifarch aarch64 ppc64le s390x x86_64 riscv64
%bcond_without vfs_glusterfs
%else
%bcond_with vfs_glusterfs
#endifarch
%endif

#else rhel
%else

%if 0%{?is_rhgs}
# Enable on rhgs x86_64
%ifarch x86_64
%bcond_without vfs_glusterfs
%else
%bcond_with vfs_glusterfs
#endifarch
%endif
%else
%bcond_with vfs_glusterfs
#endif is_rhgs
%endif

#endif fedora
%endif

# Build vfs_io_uring module by default on 64bit Fedora
%if 0%{?fedora} || 0%{?rhel} >= 8

%ifarch aarch64 ppc64le s390x x86_64 riscv64
%bcond_without vfs_io_uring
%else
%bcond_with vfs_io_uring
#endifarch
%endif

%else
%bcond_with vfs_io_uring
#endif fedora || rhel >= 8
%endif

# Build the ctdb-pcp-pmda package by default on Fedora, except for i686 where
# pcp is no longer supported
%if 0%{?fedora}
%ifnarch i686
%bcond_without pcp_pmda
%endif
%else
%bcond_with pcp_pmda
%endif

# Build the etcd helpers by default on Fedora
%if 0%{?fedora}
%bcond_without etcd_mutex
%else
%bcond_with etcd_mutex
%endif

%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without gpupdate
%else
%bcond_with gpupdate
%endif

%ifarch aarch64 ppc64le s390x x86_64
%bcond lmdb 1
%else
%bcond lmdb 0
%endif

%global samba_version 4.21.3

# The release field is extended:
# <pkgrel>[.<extraver>][.<snapinfo>]%%{?dist}[.<minorbump>]
# Square brackets indicate an optional item.
#
# The autorelease macro accepts these parameters to allow packagers to specify
# those added fields:
#
#  -p: Designates a pre-release, i.e. pkgrel will be prefixed with '0.'.
#  -e <extraver>: Allows specifying the extraver portion of the release.
#  -b <baserelease>: Allows specifying a custom base release number (the
#                    default is 1).
%global samba_release %autorelease

%global pre_release %nil
%if "x%{?pre_release}" != "x"
%global samba_release %autorelease -p -e %pre_release
%endif


# If one of those versions change, we need to make sure we rebuilt or adapt
# projects comsuming those. This is e.g. sssd, openchange, evolution-mapi, ...
%global libdcerpc_binding_so_version 0
%global libdcerpc_server_core_so_version 0
%global libdcerpc_so_version 0
%global libndr_krb5pac_so_version 0
%global libndr_nbt_so_version 0
%global libndr_so_version 5
%global libndr_standard_so_version 0
%global libnetapi_so_version 1
%global libsamba_credentials_so_version 1
%global libsamba_errors_so_version 1
%global libsamba_hostconfig_so_version 0
%global libsamba_passdb_so_version 0
%global libsamba_policy_so_version 0
%global libsamba_util_so_version 0
%global libsamdb_so_version 0
%global libsmbconf_so_version 0
%global libsmbldap_so_version 2
%global libtevent_util_so_version 0

%global libsmbclient_so_version 0
%global libwbclient_so_version 0

%global talloc_version 2.4.2
%global tdb_version 1.4.12
%global tevent_version 0.16.1

%global required_mit_krb5 1.20.1

# This is a network daemon, do a hardened build
# Enables PIE and full RELRO protection
%global _hardened_build 1
# Samba cannot be linked with -Wl,-z,defs (from hardened build config)
# For exmple the samba-cluster-support library is marked to allow undefined
# symbols in the samba build.
#
# https://src.fedoraproject.org/rpms/redhat-rpm-config/blob/master/f/buildflags.md
%undefine _strict_symbol_defs_build

%global _systemd_extra "Environment=KRB5CCNAME=FILE:/run/samba/krb5cc_samba"

# Make a copy of this variable to prevent repeated evaluation of the
# embedded shell command.  Avoid recursive macro definition if undefined.
%{?python3_sitearch: %global python3_sitearch %{python3_sitearch}}

Name:           samba
Version:        %{samba_version}
Release:        %{samba_release}

%if 0%{?fedora}
Epoch:          2
%else
Epoch:          0
%endif

%global samba_depver %{epoch}:%{version}-%{release}

Summary:        Server and Client software to interoperate with Windows machines
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
URL:            https://www.samba.org

# This is a xz recompressed file of https://ftp.samba.org/pub/samba/samba-%%{version}%%{pre_release}.tar.gz
Source0:        https://ftp.samba.org/pub/samba/samba-%{version}%{pre_release}.tar.gz#/samba-%{version}%{pre_release}.tar.xz
Source1:        https://ftp.samba.org/pub/samba/samba-%{version}%{pre_release}.tar.asc
Source2:        samba-pubkey_AA99442FB680B620.gpg

# Red Hat specific replacement-files
Source10:       samba.logrotate
Source11:       smb.conf.vendor
Source12:       smb.conf.example
Source13:       pam_winbind.conf
Source14:       samba.pamd
Source15:       usershares.conf.vendor
Source16:       samba-systemd-sysusers.conf
Source17:       samba-usershares-systemd-sysusers.conf
Source18:       samba-winbind-systemd-sysusers.conf

Source201:      README.downgrade
Source202:      samba.abignore

Patch0:         samba-4.21.0-s3-notifyd.patch
Patch1:         samba-4-21-pycrypt.patch
Patch2:         samba-4-21-fix-smbreadline.patch

Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-dcerpc = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libnetapi = %{samba_depver}
%if %{with libwbclient}
Requires(post): libwbclient = %{samba_depver}
Requires: libwbclient = %{samba_depver}
%endif

Requires: pam

Provides: samba4 = %{samba_depver}
Obsoletes: samba4 < %{samba_depver}

# We don't build it outdated docs anymore
Provides: samba-doc = %{samba_depver}
Obsoletes: samba-doc < %{samba_depver}

# Is not supported yet
Provides: samba-domainjoin-gui = %{samba_depver}
Obsoletes: samba-domainjoin-gui < %{samba_depver}

# SWAT been deprecated and removed from samba
Provides: samba-swat = %{samba_depver}
Obsoletes: samba-swat < %{samba_depver}

Provides: samba4-swat = %{samba_depver}
Obsoletes: samba4-swat < %{samba_depver}

Provides: bundled(libreplace)

BuildRequires: make
BuildRequires: gcc
BuildRequires: glibc-gconv-extra
BuildRequires: avahi-devel
BuildRequires: bison
BuildRequires: cups-devel
BuildRequires: dbus-devel
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: e2fsprogs-devel
BuildRequires: flex
BuildRequires: gawk
BuildRequires: gnupg2
BuildRequires: gnutls-devel >= 3.4.7
BuildRequires: gpgme-devel
BuildRequires: jansson-devel
BuildRequires: krb5-devel >= %{required_mit_krb5}
BuildRequires: libacl-devel
BuildRequires: libaio-devel
BuildRequires: libarchive-devel
BuildRequires: libattr-devel
BuildRequires: libcap-devel
BuildRequires: libicu-devel
BuildRequires: libcmocka-devel
BuildRequires: libtirpc-devel
BuildRequires: libuuid-devel
BuildRequires: libxslt
%if %{with lmdb}
BuildRequires: lmdb
BuildRequires: lmdb-devel >= 0.9.16
%endif
%if %{with winexe}
BuildRequires: mingw32-gcc
BuildRequires: mingw64-gcc
%endif
BuildRequires: ncurses-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: perl-interpreter
BuildRequires: perl-generators
BuildRequires: perl(Archive::Tar)
BuildRequires: perl(Test::More)
BuildRequires: popt-devel
BuildRequires: python3-cryptography
BuildRequires: python3-devel
BuildRequires: python3-dns
BuildRequires: python3-requests
BuildRequires: python3-setuptools
BuildRequires: quota-devel
BuildRequires: readline-devel
BuildRequires: rpcgen
BuildRequires: rpcsvc-proto-devel
BuildRequires: sed
BuildRequires: systemd-rpm-macros
BuildRequires: libtasn1-devel
# We need asn1Parser
BuildRequires: libtasn1-tools
BuildRequires: xfsprogs-devel
BuildRequires: xz
BuildRequires: zlib-devel >= 1.2.3

BuildRequires: pkgconfig(libsystemd)

%ifnarch i686 riscv64
%if 0%{?fedora} >= 37
BuildRequires: mold
%endif
%endif

%if %{with vfs_glusterfs}
BuildRequires: glusterfs-api-devel >= 3.4.0.16
BuildRequires: glusterfs-devel >= 3.4.0.16
%endif

%if %{with vfs_cephfs}
BuildRequires: libcephfs-devel
%endif

%if %{with vfs_io_uring}
BuildRequires: liburing-devel >= 0.4
%endif

%if %{with pcp_pmda}
BuildRequires: pcp-libs-devel
%endif
%if %{with ceph_mutex}
BuildRequires: librados-devel
%endif
%if %{with etcd_mutex}
BuildRequires: python3-etcd
%endif

%if %{with gpupdate}
BuildRequires: cepces-certmonger >= 0.3.8
%endif

# pidl requirements
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(FindBin)
BuildRequires: perl(Parse::Yapp)

%if %{without includelibs}
BuildRequires: libtalloc-devel >= %{talloc_version}
BuildRequires: python3-talloc-devel >= %{talloc_version}

BuildRequires: libtevent-devel >= %{tevent_version}
BuildRequires: python3-tevent >= %{tevent_version}

BuildRequires: libtdb-devel >= %{tdb_version}
BuildRequires: python3-tdb >= %{tdb_version}
%endif

%if %{with dc}
BuildRequires: bind
BuildRequires: krb5-server >= %{required_mit_krb5}
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires: python3-dateutil
%else
BuildRequires: python3-iso8601
%endif
BuildRequires: python3-gpg
BuildRequires: python3-markdown
BuildRequires: python3-pyasn1 >= 0.4.8
BuildRequires: python3-setproctitle

%if %{without includelibs}
BuildRequires: tdb-tools
#endif without includelibs
%endif

#endif with dc
%endif

%if %{with testsuite}
BuildRequires: bind-utils
BuildRequires: glibc-langpack-en
BuildRequires: git
BuildRequires: gnutls-utils
BuildRequires: jq
BuildRequires: krb5-pkinit
BuildRequires: krb5-workstation
BuildRequires: lmdb
BuildRequires: nss_wrapper
BuildRequires: pam_wrapper
BuildRequires: perl-Archive-Tar
BuildRequires: perl-Digest-MD5
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-JSON
BuildRequires: perl-JSON-Parse
BuildRequires: perl-Parse-Yapp
BuildRequires: perl-Test-Base
BuildRequires: psmisc
BuildRequires: python3-libpamtest
BuildRequires: resolv_wrapper
BuildRequires: rsync
BuildRequires: socket_wrapper
BuildRequires: sudo
BuildRequires: uid_wrapper
#endif with testsuite
%endif

# filter out perl requirements pulled in from examples in the docdir.
%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{_docdir}/.*$

### SAMBA
%description
Samba is the standard Windows interoperability suite of programs for Linux and
Unix.

### CLIENT
%package client
Summary: Samba client programs
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libsmbclient}
Requires: libsmbclient = %{samba_depver}
%endif
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-client = %{samba_depver}
Obsoletes: samba4-client < %{samba_depver}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

Provides: bundled(libreplace)

%description client
The %{name}-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.

### CLIENT-LIBS
%package client-libs
Summary: Samba client libraries
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif
Requires: krb5-libs >= %{required_mit_krb5}
# This is needed for charset conversion
Requires: glibc-gconv-extra

%description client-libs
The samba-client-libs package contains internal libraries needed by the
SMB/CIFS clients.

### COMMON
%package common
Summary: Files used by both Samba servers and clients
BuildArch: noarch

Requires(post): (systemd-standalone-tmpfiles or systemd)
%if 0%{?fedora}
Recommends:     logrotate
%endif

Provides: samba4-common = %{samba_depver}
Obsoletes: samba4-common < %{samba_depver}

%description common
samba-common provides files necessary for both the server and client
packages of Samba.

### COMMON-LIBS
%package common-libs
Summary: Libraries used by both Samba servers and clients
Requires(pre): samba-common = %{samba_depver}
Requires: samba-common = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: bundled(libreplace)

%if %{without dc} && %{without testsuite}
Obsoletes: samba-dc < %{samba_depver}
Obsoletes: samba-dc-libs < %{samba_depver}
Obsoletes: samba-dc-bind-dlz < %{samba_depver}
%endif

# ctdb-tests package has been dropped if we do not build the testsuite
%if %{with clustering}
%if %{without testsuite}
Obsoletes: ctdb-tests < %{samba_depver}
Obsoletes: ctdb-tests-debuginfo < %{samba_depver}
# endif without testsuite
%endif
# endif with clustering
%endif

# We only build glusterfs for RHGS and Fedora, so obsolete it on other versions
# of the distro
%if %{without vfs_glusterfs}
Obsoletes: samba-vfs-glusterfs < %{samba_depver}
# endif without vfs_glusterfs
%endif

%description common-libs
The samba-common-libs package contains internal libraries needed by the
SMB/CIFS clients.

### COMMON-TOOLS
%package common-tools
Summary: Tools for Samba clients
Requires: samba-common-libs = %{samba_depver}
Requires: samba-client-libs = %{samba_depver}
Requires: samba-libs = %{samba_depver}
Requires: samba-ldb-ldap-modules = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libnetapi = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: bundled(libreplace)

%description common-tools
The samba-common-tools package contains tools for SMB/CIFS clients.

### SAMBA-TOOLS
%package tools
Summary: Tools for Samba servers
# samba-tool needs python3-samba
Requires: python3-%{name} = %{samba_depver}
# samba-tool needs python3-samba-dc also on non-dc build
Requires: python3-%{name}-dc = %{samba_depver}
%if %{with dc}
# samba-tool needs mdb_copy and tdbackup for domain backup or upgrade provision
%if %{with lmdb}
Requires: lmdb
%endif
Requires: tdb-tools
Requires: python3-gpg
%endif

%description tools
The samba-tools package contains tools for Samba servers
and for GPO management on domain members.

### RPC
%package dcerpc
Summary: DCE RPC binaries
Requires: samba-common-libs = %{samba_depver}
Requires: samba-client-libs = %{samba_depver}
Requires: samba-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libnetapi = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

%description dcerpc
The samba-dcerpc package contains binaries that serve DCERPC over named pipes.

### DC
%if %{with dc} || %{with testsuite}
%package dc
Summary: Samba AD Domain Controller
Requires: %{name} = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}
Requires: %{name}-tools = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-dc-provision = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}

%if %{with libwbclient}
Requires(post): libwbclient = %{samba_depver}
Requires: libwbclient = %{samba_depver}
%endif

Requires: ldb-tools
Requires: python3-setproctitle
Requires: libldb = %{samba_depver}
Requires: python3-%{name} = %{samba_depver}
Requires: python3-%{name}-dc = %{samba_depver}
Requires: krb5-server >= %{required_mit_krb5}
Requires: bind-utils

Provides: samba4-dc = %{samba_depver}
Obsoletes: samba4-dc < %{samba_depver}

Provides: bundled(libreplace)

%description dc
The samba-dc package provides AD Domain Controller functionality

### DC-PROVISION
%package dc-provision
Summary: Samba AD files to provision a DC
BuildArch: noarch

%description dc-provision
The samba-dc-provision package provides files to setup a domain controller

#endif with dc || with testsuite
%endif

### DC-LIBS
%package dc-libs
Summary: Samba AD Domain Controller Libraries
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: samba4-dc-libs = %{samba_depver}
Obsoletes: samba4-dc-libs < %{samba_depver}

Provides: bundled(libreplace)

%description dc-libs
The %{name}-dc-libs package contains the libraries needed by the DC to
link against the SMB, RPC and other protocols.

%if %{with dc} || %{with testsuite}
### DC-BIND
%package dc-bind-dlz
Summary: Bind DLZ module for Samba AD
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: %{name}-dc = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: bind
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: bundled(libreplace)

%description dc-bind-dlz
The %{name}-dc-bind-dlz package contains the libraries for bind to manage all
name server related details of Samba AD.
#endif with dc
%endif

### DEVEL
%package devel
Summary: Developer tools for Samba libraries
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: libnetapi = %{samba_depver}

Provides: samba4-devel = %{samba_depver}
Obsoletes: samba4-devel < %{samba_depver}
Provides: python3-samba-devel = %{samba_depver}
Obsoletes: python3-samba-devel < %{samba_depver}

%description devel
The %{name}-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

### CEPH
%if %{with vfs_cephfs}
%package vfs-cephfs
Summary: Samba VFS module for Ceph distributed storage system
Requires: %{name} = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: bundled(libreplace)

%description vfs-cephfs
Samba VFS module for Ceph distributed storage system integration.
#endif with vfs_cephfs
%endif

### IOURING
%if %{with vfs_io_uring}
%package vfs-iouring
Summary: Samba VFS module for io_uring
Requires: %{name} = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: bundled(libreplace)

%description vfs-iouring
Samba VFS module for io_uring instance integration.
#endif with vfs_io_uring
%endif

### GLUSTER
%if %{with vfs_glusterfs}
%package vfs-glusterfs
Summary: Samba VFS module for GlusterFS
Requires: glusterfs-api >= 3.4.0.16
Requires: glusterfs >= 3.4.0.16
Requires: %{name} = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Obsoletes: samba-glusterfs < %{samba_depver}
Provides: samba-glusterfs = %{samba_depver}

Provides: bundled(libreplace)

%description vfs-glusterfs
Samba VFS module for GlusterFS integration.
%endif

### GPUPDATE
%if %{with gpupdate}
%package gpupdate
Summary: Samba GPO support for clients
Requires: cepces-certmonger
Requires: certmonger
Requires: %{name}-ldb-ldap-modules = %{samba_depver}
Requires: python3-%{name} = %{samba_depver}
# samba-tool needs python3-samba-dc also on non-dc build
Requires: python3-%{name}-dc = %{samba_depver}

%description gpupdate
This package provides the samba-gpupdate tool to apply Group Policy Objects
(GPO) on Samba clients.

#endif with gpupdate
%endif

### KRB5-PRINTING
%package krb5-printing
Summary: Samba CUPS backend for printing with Kerberos
Requires(pre): %{name}-client
Requires: %{name}-client = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description krb5-printing
If you need Kerberos for print jobs to a printer connection to cups via the SMB
backend, then you need to install that package. It will allow cups to access
the Kerberos credentials cache of the user issuing the print job.

### LDB-LDAP-MODULES
%package ldb-ldap-modules
Summary: Samba ldap modules for ldb
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

%description ldb-ldap-modules
This package contains the ldb ldap modules required by samba-tool and
samba-gpupdate.

### LIBS
%package libs
Summary: Samba libraries
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-libs = %{samba_depver}
Obsoletes: samba4-libs < %{samba_depver}

Provides: bundled(libreplace)

%description libs
The %{name}-libs package contains the libraries needed by programs that link
against the SMB, RPC and other protocols provided by the Samba suite.

### LIBNETAPI
%package -n libnetapi
Summary: The NETAPI library
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

%description -n libnetapi
This contains the NETAPI library from the Samba suite.

%package -n libnetapi-devel
Summary: Developer tools for the NETAPI library
Requires: libnetapi = %{samba_depver}

%description -n libnetapi-devel
The libnetapi-devel package contains the header files and libraries needed to
develop programs that link against the NETAPI library in the Samba suite.

### LIBSMBCLIENT
%if %{with libsmbclient}
%package -n libsmbclient
Summary: The SMB client library
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

%description -n libsmbclient
The libsmbclient contains the SMB client library from the Samba suite.

%package -n libsmbclient-devel
Summary: Developer tools for the SMB client library
Requires: libsmbclient = %{samba_depver}

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed
to develop programs that link against the SMB client library in the Samba
suite.
#endif {with libsmbclient}
%endif

### LIBWBCLIENT
%if %{with libwbclient}
%package -n libwbclient
Summary: The winbind client library
Requires: %{name}-client-libs = %{samba_depver}
Conflicts: sssd-libwbclient

%description -n libwbclient
The libwbclient package contains the winbind client library from the Samba
suite.

%package -n libwbclient-devel
Summary: Developer tools for the winbind library
Requires: libwbclient = %{samba_depver}
Conflicts: sssd-libwbclient-devel

Provides: samba-winbind-devel = %{samba_depver}
Obsoletes: samba-winbind-devel < %{samba_depver}

%description -n libwbclient-devel
The libwbclient-devel package provides developer tools for the wbclient
library.
#endif {with libwbclient}
%endif

### PYTHON3
%package -n python3-%{name}
Summary: Samba Python3 libraries
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: python3-cryptography
Requires: python3-dns
Requires: python3-ldb
Requires: python3-requests
Requires: python3-talloc
Requires: python3-tdb
Requires: python3-tevent
Requires: libldb = %{samba_depver}
%if %{with libsmbclient}
Requires: libsmbclient = %{samba_depver}
%endif
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: bundled(libreplace)

%description -n python3-%{name}
The python3-%{name} package contains the Python 3 libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python 3 programs.

%package -n python3-samba-test
Summary: Samba Python libraries
Requires: python3-%{name} = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}

%description -n python3-samba-test
The python3-%{name}-test package contains the Python libraries used by the test suite of Samba.
If you want to run full set of Samba tests, you need to install this package.

%package -n python3-samba-dc
Summary: Samba Python libraries for Samba AD
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-dc-libs = %{samba_depver}
Requires: python3-%{name} = %{samba_depver}
# for ms_forest_updates_markdown.py and ms_schema_markdown.py
Requires: python3-markdown
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

%description -n python3-samba-dc
The python3-%{name}-dc package contains the Python libraries needed by programs
to manage Samba AD.

### PIDL
%package pidl
Summary: Perl IDL compiler
Requires: perl-interpreter
Requires: perl(FindBin)
Requires: perl(Parse::Yapp)
BuildArch: noarch

Provides: samba4-pidl = %{samba_depver}
Obsoletes: samba4-pidl < %{samba_depver}

%description pidl
The %{name}-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols

### TEST
%package test
Summary: Testing tools for Samba servers and clients
Requires: %{name} = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}

Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-test-libs = %{samba_depver}
%if %{with dc} || %{with testsuite}
Requires: %{name}-dc-libs = %{samba_depver}
%endif
Requires: %{name}-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libnetapi = %{samba_depver}
%if %{with libsmbclient}
Requires: libsmbclient = %{samba_depver}
%endif
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif
Requires: python3-%{name} = %{samba_depver}
Requires: perl(Archive::Tar)

Provides: samba4-test = %{samba_depver}
Obsoletes: samba4-test < %{samba_depver}

Provides: bundled(libreplace)

%description test
%{name}-test provides testing tools for both the server and client
packages of Samba.

### TEST-LIBS
%package test-libs
Summary: Libraries need by the testing tools for Samba servers and clients
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: %{name}-test-devel = %{samba_depver}
Obsoletes: %{name}-test-devel < %{samba_depver}

Provides: bundled(libreplace)

%description test-libs
%{name}-test-libs provides libraries required by the testing tools.

### USERSHARES
%package usershares
Summary: Provides support for non-root user shares
Requires: %{name} = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}

%description usershares
Installing this package will provide a configuration file, group and
directories to support non-root user shares. You can configure them
as a user using the `net usershare` command.

### WINBIND
%package winbind
Summary: Samba winbind
Requires(pre): %{name}-common = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires(post): %{name}-common-libs = %{samba_depver}
Requires: %{name}-common-tools = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires(post): %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires(post): %{name}-libs = %{samba_depver}
Requires: %{name}-winbind-modules = %{samba_depver}
Suggests: %{name}-tools = %{samba_depver}
Requires: libldb = %{samba_depver}

%if %{with libwbclient}
Requires(post): libwbclient = %{samba_depver}
Requires: libwbclient = %{samba_depver}
%endif
Requires: %{name}-dcerpc = %{samba_depver}

Provides: samba4-winbind = %{samba_depver}
Obsoletes: samba4-winbind < %{samba_depver}

# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts: NetworkManager < 1.20

Provides: bundled(libreplace)

%description winbind
The samba-winbind package provides the winbind NSS library, and some client
tools.  Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.

### WINBIND-CLIENTS
%package winbind-clients
Summary: Samba winbind clients
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}
Requires: libldb = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif

Provides: samba4-winbind-clients = %{samba_depver}
Obsoletes: samba4-winbind-clients < %{samba_depver}

Provides: bundled(libreplace)

%description winbind-clients
The samba-winbind-clients package provides the wbinfo and ntlm_auth
tool.

### WINBIND-KRB5-LOCATOR
%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}
%else
Requires: %{name}-libs = %{samba_depver}
%endif
Requires: samba-client-libs = %{samba_depver}
Requires: libldb = %{samba_depver}

Provides: samba4-winbind-krb5-locator = %{samba_depver}
Obsoletes: samba4-winbind-krb5-locator < %{samba_depver}

# Handle winbind_krb5_locator.so as alternatives to allow
# IPA AD trusts case where it should not be used by libkrb5
# The plugin will be diverted to /dev/null by the FreeIPA
# freeipa-server-trust-ad subpackage due to higher priority
# and restored to the proper one on uninstall
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

Provides: bundled(libreplace)

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use

### WINBIND-MODULES
%package winbind-modules
Summary: Samba winbind modules
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
%if %{with libwbclient}
Requires: libwbclient = %{samba_depver}
%endif
Requires: pam

Provides: bundled(libreplace)

%description winbind-modules
The samba-winbind-modules package provides the NSS library and a PAM module
necessary to communicate to the Winbind Daemon

### WINEXE
%if %{with winexe}
%package winexe
Summary: Samba Winexe Windows Binary
License: GPL-3.0-only
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-common-libs = %{samba_depver}
Requires: libldb = %{samba_depver}
Requires: libwbclient = %{samba_depver}

Provides: bundled(libreplace)

%description winexe
Winexe is a Remote Windows-command executor
%endif

### CTDB
%if %{with clustering}
%package -n ctdb
Summary: A Clustered Database based on Samba's Trivial Database (TDB)

Requires: %{name}-common-libs = %{samba_depver}
Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-winbind-clients = %{samba_depver}

Requires: coreutils
# for ps and killall
Requires: psmisc
Requires: sed
Requires: tdb-tools
Requires: gawk
# for pkill and pidof:
Requires: procps-ng
# for netstat:
Requires: net-tools
Requires: ethtool
# for ip:
Requires: iproute
Requires: iptables
# for flock, getopt, kill:
Requires: util-linux

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

Provides: bundled(libreplace)

%description -n ctdb
CTDB is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.

%if %{with pcp_pmda}

%package -n ctdb-pcp-pmda
Summary: CTDB PCP pmda support
Requires: ctdb = %{samba_depver}
Requires: pcp-libs
Requires: %{name}-client-libs = %{samba_depver}

%description -n ctdb-pcp-pmda
Performance Co-Pilot (PCP) support for CTDB

#endif with pcp_pmda
%endif

%if %{with etcd_mutex}

%package -n ctdb-etcd-mutex
Summary: CTDB ETCD mutex helper
Requires: ctdb = %{samba_depver}
Requires: python3-etcd

%description -n ctdb-etcd-mutex
Support for using an existing ETCD cluster as a mutex helper for CTDB

#endif with etcd_mutex
%endif

%if %{with ceph_mutex}

%package -n ctdb-ceph-mutex
Summary: CTDB ceph mutex helper
Requires: ctdb = %{samba_depver}

%description -n ctdb-ceph-mutex
Support for using an existing CEPH cluster as a mutex helper for CTDB

#endif with ceph_mutex
%endif

#endif with clustering
%endif

### LIBLDB
%package -n libldb
Summary: A schema-less, ldap like, API and database
License: LGPL-3.0-or-later
Requires: libtalloc%{?_isa} >= %{talloc_version}
Requires: libtdb%{?_isa} >= %{tdb_version}
Requires: libtevent%{?_isa} >= %{tevent_version}

Provides: bundled(libreplace)
Obsoletes: libldb < 0:2.10
Provides: libldb = 0:2.10
Provides: libldb = %{samba_depver}

%description -n libldb
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases.

### LIBLDB-DEVEL
%package -n libldb-devel
Summary: Developer tools for the LDB library
License: LGPL-3.0-or-later
Requires: libldb%{?_isa} = %{samba_depver}
Requires: libtdb-devel%{?_isa} >= %{tdb_version}
Requires: libtalloc-devel%{?_isa} >= %{talloc_version}
Requires: libtevent-devel%{?_isa} >= %{tevent_version}

Obsoletes: libldb-devel < 0:2.10
Provides: libldb-devel = 0:2.10
Provides: libldb-devel = %{samba_depver}

%description -n libldb-devel
Header files needed to develop programs that link against the LDB library.

### LDB-TOOLS
%package -n ldb-tools
Summary: Tools to manage LDB files
License: LGPL-3.0-or-later
Requires: libldb%{?_isa} = %{samba_depver}
Obsoletes: ldb-tools < 0:2.10
Provides: ldb-tools = %{samba_depver}

%description -n ldb-tools
Tools to manage LDB files

### PYTHON3-LDB
%package -n python3-ldb
Summary: Python bindings for the LDB library
License: LGPL-3.0-or-later
Requires: libldb%{?_isa} = %{samba_depver}
Requires: python3-tdb%{?_isa} >= %{tdb_version}
Requires: samba-client-libs = %{samba_depver}
%{?python_provide:%python_provide python3-ldb}

Obsoletes: python3-ldb < 0:2.10
Provides: python3-ldb = %{samba_depver}
# These were the C bindings, only used by Samba
Obsoletes: python-ldb-devel-common < 2.10
Provides: python-ldb-devel-common = 2.10
Provides: python-ldb-devel-common = %{samba_depver}
Obsoletes: python3-ldb-devel < 2.10
Provides: python3-ldb-devel = 2.10
Provides: python3-ldb-devel = %{samba_depver}

%description -n python3-ldb
Python bindings for the LDB library

%prep
%if 0%{?fedora} || 0%{?rhel} >= 9
xzcat %{SOURCE0} | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-
%else
xzcat %{SOURCE0} | gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} -
%endif
%autosetup -n samba-%{version}%{pre_release} -p1

# Make sure we do not build with heimdal code
rm -rfv third_party/heimdal

%build
%if %{with includelibs}
%global _talloc_lib ,talloc,pytalloc,pytalloc-util
%global _tevent_lib ,tevent,pytevent
%global _tdb_lib ,tdb,pytdb
%else
%global _talloc_lib ,!talloc,!pytalloc,!pytalloc-util
%global _tevent_lib ,!tevent,!pytevent
%global _tdb_lib ,!tdb,!pytdb
#endif with includelibs
%endif

%global _samba_bundled_libraries !popt%{_talloc_lib}%{_tevent_lib}%{_tdb_lib}

%global _samba_idmap_modules idmap_ad,idmap_rid,idmap_ldap,idmap_hash,idmap_tdb2
%global _samba_pdb_modules pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4

%if %{with testsuite}
%global _samba_auth_modules auth_wbc,auth_unix,auth_server,auth_samba4,auth_skel
%global _samba_vfs_modules vfs_dfs_samba4,vfs_fake_dfq
%else
%global _samba_auth_modules auth_wbc,auth_unix,auth_server,auth_samba4
%global _samba_vfs_modules vfs_dfs_samba4
%endif

%global _samba_modules %{_samba_idmap_modules},%{_samba_pdb_modules},%{_samba_auth_modules},%{_samba_vfs_modules}

%global _libsmbclient %nil
%global _libwbclient %nil

%if %{without libsmbclient}
%global _libsmbclient smbclient,
%endif

%if %{without libwbclient}
%global _libwbclient wbclient,
%endif

%global _default_private_libraries !ldb,!dcerpc-samr,!samba-policy,!tevent-util,!dcerpc,!samba-hostconfig,!samba-credentials,!dcerpc_server,!samdb,
%global _samba_private_libraries %{_default_private_libraries}%{_libsmbclient}%{_libwbclient}

# TODO: resolve underlinked python modules
export python_LDFLAGS="$(echo %{__global_ldflags} | sed -e 's/-Wl,-z,defs//g')"

# Use the mold linker if possible
export python_LDFLAGS="$(echo %{__global_ldflags} | sed -e 's/-Wl,-z,defs//g')"

%ifnarch i686 riscv64
%if 0%{?fedora} >= 37
export LDFLAGS="%{__global_ldflags} -fuse-ld=mold"
export python_LDFLAGS="$(echo ${LDFLAGS} | sed -e 's/-Wl,-z,defs//g')"
#endif fedora >= 37
%endif
#endif narch i686
%endif

# Add support for mock ccache plugin
%if %{with ccache}
CCACHE="$(command -v ccache)"
if [ -n "${CCACHE}" ]; then
    ${CCACHE} -s
    export CC="${CCACHE} gcc"
fi
%endif

%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=/var/lib/samba/lock \
        --with-statedir=/var/lib/samba \
        --with-cachedir=/var/lib/samba \
        --disable-rpath-install \
        --with-shared-modules=%{_samba_modules} \
        --bundled-libraries=%{_samba_bundled_libraries} \
        --private-libraries=%{_samba_private_libraries} \
        --with-pam \
        --with-pie \
        --with-relro \
        --without-fam \
        --with-system-mitkrb5 \
        --with-experimental-mit-ad-dc \
%if %{without dc} && %{without testsuite}
        --without-ad-dc \
%endif
%if %{without vfs_glusterfs}
        --disable-glusterfs \
%endif
%if %{with clustering}
        --with-cluster-support \
%endif
%if %{with testsuite}
        --enable-selftest \
%endif
%if %{with pcp_pmda}
        --enable-pmda \
%endif
%if %{with ceph_mutex}
        --enable-ceph-reclock \
%endif
%if %{with etcd_mutex}
        --enable-etcd-reclock \
%endif
        --with-profiling-data \
        --with-systemd \
        --with-quotas \
        --systemd-install-services \
        --with-systemddir=/usr/lib/systemd/system \
        --systemd-smb-extra=%{_systemd_extra} \
        --systemd-nmb-extra=%{_systemd_extra} \
        --systemd-winbind-extra=%{_systemd_extra} \
%if %{with clustering}
        --systemd-ctdb-extra=%{_systemd_extra} \
%endif
        --systemd-samba-extra=%{_systemd_extra}

# Do not use %%make_build, make is just a wrapper around waf in Samba!
%{__make} %{?_smp_mflags} %{_make_verbose}

pushd pidl
%__perl Makefile.PL PREFIX=%{_prefix}

%make_build
popd

pushd lib/ldb
doxygen Doxyfile
popd

%install
%if !%{with testsuite}
# Do not use %%make_install, make is just a wrapper around waf in Samba!
%{__make} %{?_smp_mflags} %{_make_verbose} install DESTDIR=%{buildroot}

install -d -m 0755 %{buildroot}/usr/{sbin,bin}
install -d -m 0755 %{buildroot}%{_libdir}/security
install -d -m 0755 %{buildroot}/var/lib/samba
install -d -m 0755 %{buildroot}/var/lib/samba/certs
install -d -m 0755 %{buildroot}/var/lib/samba/drivers
install -d -m 0755 %{buildroot}/var/lib/samba/lock
install -d -m 0755 %{buildroot}/var/lib/samba/private
install -d -m 0755 %{buildroot}/var/lib/samba/private/certs
install -d -m 0755 %{buildroot}/var/lib/samba/scripts
install -d -m 0755 %{buildroot}/var/lib/samba/sysvol
install -d -m 0755 %{buildroot}/var/lib/samba/usershares
install -d -m 0755 %{buildroot}/var/lib/samba/winbindd_privileged
install -d -m 0755 %{buildroot}/var/log/samba/old
install -d -m 0755 %{buildroot}/run/samba
install -d -m 0755 %{buildroot}/run/winbindd
install -d -m 0755 %{buildroot}/%{_libdir}/samba
install -d -m 0755 %{buildroot}/%{_libdir}/samba/ldb
install -d -m 0755 %{buildroot}/%{_libdir}/pkgconfig

touch %{buildroot}%{_libexecdir}/samba/cups_backend_smb

# Install other stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/samba

install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/samba/smb.conf
install -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/samba/smb.conf.example
install -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/samba/usershares.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/security
install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/pam.d/samba

echo 127.0.0.1 localhost > %{buildroot}%{_sysconfdir}/samba/lmhosts

# openLDAP database schema
install -d -m 0755 %{buildroot}%{_sysconfdir}/openldap/schema
install -m644 examples/LDAP/samba.schema %{buildroot}%{_sysconfdir}/openldap/schema/samba.schema

install -m 0744 packaging/printing/smbprint %{buildroot}%{_bindir}/smbprint

install -d -m 0755 %{buildroot}%{_tmpfilesdir}
# Create /run/samba.
echo "d /run/samba  755 root root" > %{buildroot}%{_tmpfilesdir}/samba.conf
%if %{with clustering}
echo "d /run/ctdb 755 root root" > %{buildroot}%{_tmpfilesdir}/ctdb.conf
%endif

install -d -m 0755 %{buildroot}%{_sysusersdir}
install -m 0644 %{SOURCE16} %{buildroot}%{_sysusersdir}/samba.conf
install -m 0644 %{SOURCE17} %{buildroot}%{_sysusersdir}/samba-usershares.conf
install -m 0644 %{SOURCE18} %{buildroot}%{_sysusersdir}/samba-winbind.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba
%if %{with clustering}
cat > %{buildroot}%{_sysconfdir}/sysconfig/ctdb <<EOF
# CTDB configuration is now in %%{_sysconfdir}/ctdb/ctdb.conf
EOF

install -d -m 0755 %{buildroot}%{_sysconfdir}/ctdb
install -m 0644 ctdb/config/ctdb.conf %{buildroot}%{_sysconfdir}/ctdb/ctdb.conf
%endif

install -m 0644 %{SOURCE201} packaging/README.downgrade

# NetworkManager online/offline script
install -d -m 0755 %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd \
            %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/30-winbind

# winbind krb5 plugins
install -d -m 0755 %{buildroot}%{_libdir}/krb5/plugins/libkrb5
touch %{buildroot}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

%if %{without dc} && %{without testsuite}
for i in \
    %{_mandir}/man8/samba.8 \
    %{_mandir}/man8/samba_downgrade_db.8 \
    %{_unitdir}/samba.service \
    ; do
    rm -f %{buildroot}$i
done
%endif

%if %{without gpupdate}
rm -f %{buildroot}%{_sbindir}/samba-gpupdate
rm -f %{buildroot}%{_mandir}/man8/samba-gpupdate.8*
%endif

%if %{without vfs_glusterfs}
rm -f %{buildroot}%{_mandir}/man8/vfs_glusterfs.8*
%endif

%if %{without vfs_cephfs}
rm -f %{buildroot}%{_mandir}/man8/vfs_ceph.8*
rm -f %{buildroot}%{_mandir}/man8/vfs_ceph_snapshots.8*
%endif

# This makes the right links, as rpmlint requires that
# the ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n %{buildroot}%{_libdir}

%if %{without dc} && %{without testsuite}
for f in samba/libsamba-python-private-samba.so; do
    rm -f %{buildroot}%{_libdir}/$f
done
#endif without dc
%endif

%if %{with testsuite}
rm -f %{buildroot}%{_mandir}/man8/vfs_nfs4acl_xattr.8*
#endif with testsuite
%endif

pushd pidl
%{__make} DESTDIR=%{buildroot} install_vendor

rm -f %{buildroot}%{perl_archlib}/perllocal.pod
rm -f %{buildroot}%{perl_archlib}/vendor_perl/auto/Parse/Pidl/.packlist

# Already packaged by perl Parse:Yapp
rm -rf %{buildroot}%{perl_vendorlib}/Parse/Yapp
popd

# Install libldb manpages
cp -a lib/ldb/apidocs/man/* %{buildroot}%{_mandir}
# Remove manpages we don't want
rm -f %{buildroot}%{_mandir}/man3/_*
rm -f %{buildroot}%{_mandir}/man3/PyLdb*

# CTDB
%if %{with clustering}
touch %{buildroot}%{_libexecdir}/ctdb/statd_callout
#endif with clustering
%endif

#endif !with testsuite
%endif

%check
%if %{with testsuite}
#
# samba3.smb2.timestamps.*:
#
# The test fails on ext4 as it uses two high-order bits
# in the timestamp so the year 2038 problem is deferred till 2446.
# https://bugzilla.samba.org/show_bug.cgi?id=14546
#
for t in samba3.smb2.timestamps.time_t_15032385535 \
         samba3.smb2.timestamps.time_t_10000000000 \
         samba3.smb2.timestamps.time_t_4294967295 \
         ; do
    echo "^$t" >> selftest/knownfail.d/fedora.%{dist}
done
cat selftest/knownfail.d/fedora.%{dist}

export TDB_NO_FSYNC=1
export NMBD_DONT_LOG_STDOUT=1
export SMBD_DONT_LOG_STDOUT=1
export WINBINDD_DONT_LOG_STDOUT=1
export SAMBA_DCERPCD_DONT_LOG_STDOUT=1
%{__make} %{?_smp_mflags} test FAIL_IMMEDIATELY=1
#endif with testsuite
%endif

%if !%{with testsuite}
%post
%systemd_post samba-bgqd.service
%systemd_post smb.service
%systemd_post nmb.service

%preun
%systemd_preun samba-bgqd.service
%systemd_preun smb.service
%systemd_preun nmb.service

%postun
%systemd_postun_with_restart samba-bgqd.service
%systemd_postun_with_restart smb.service
%systemd_postun_with_restart nmb.service

%pre common
# This creates the group 'printadmin'
%sysusers_create_compat %{SOURCE16}

%post common
%{?ldconfig}
%tmpfiles_create %{_tmpfilesdir}/samba.conf
if [ -d /var/cache/samba ]; then
    mv /var/cache/samba/netsamlogon_cache.tdb /var/lib/samba/ 2>/dev/null
    mv /var/cache/samba/winbindd_cache.tdb /var/lib/samba/ 2>/dev/null
    rm -rf /var/cache/samba/
    ln -sf /var/cache/samba /var/lib/samba/
fi

%post client
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
    cups_backend_smb \
    %{_bindir}/smbspool 10

%postun client
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove cups_backend_smb %{_bindir}/smbspool
fi

%ldconfig_scriptlets client-libs

%ldconfig_scriptlets common-libs

%if %{with dc}
%ldconfig_scriptlets dc-libs

%post dc
%systemd_post samba.service

%preun dc
%systemd_preun samba.service

%postun dc
%systemd_postun_with_restart samba.service
#endif with dc
%endif

%post krb5-printing
%{_sbindir}/update-alternatives --install %{_libexecdir}/samba/cups_backend_smb \
	cups_backend_smb \
	%{_libexecdir}/samba/smbspool_krb5_wrapper 50

%postun krb5-printing
if [ $1 -eq 0 ] ; then
	%{_sbindir}/update-alternatives --remove cups_backend_smb %{_libexecdir}/samba/smbspool_krb5_wrapper
fi

%ldconfig_scriptlets libs

%if %{with libsmbclient}
%ldconfig_scriptlets -n libsmbclient
%endif

%if %{with libwbclient}
%pre -n libwbclient
if [ $1 -gt 1 ] ; then
    rm -rf %{_libdir}/samba/wbclient/ 2>/dev/null
    rm -f /etc/alternatives/libwbclient.so* 2>/dev/null
    rm -f /var/lib/alternatives/libwbclient.so* 2>/dev/null
fi
%{?ldconfig}
#endif {with libwbclient}
%endif

%ldconfig_scriptlets test

%pre usershares
# This creates the group 'usershares'
%sysusers_create_compat %{SOURCE17}

%pre winbind
# This creates the group 'wbpriv'
%sysusers_create_compat %{SOURCE18}

%post winbind
%systemd_post winbind.service

%preun winbind
%systemd_preun winbind.service

%postun winbind
%systemd_postun_with_restart winbind.service

%postun winbind-krb5-locator
if [ "$1" -ge "1" ]; then
        if [ "`readlink %{_sysconfdir}/alternatives/winbind_krb5_locator.so`" == "%{_libdir}/samba/krb5/winbind_krb5_locator.so" ]; then
                %{_sbindir}/update-alternatives --set winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
        fi
fi

%post winbind-krb5-locator
%{_sbindir}/update-alternatives --install %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so \
                                winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so 10

%preun winbind-krb5-locator
if [ $1 -eq 0 ]; then
        %{_sbindir}/update-alternatives --remove winbind_krb5_locator.so %{_libdir}/samba/krb5/winbind_krb5_locator.so
fi

%ldconfig_scriptlets winbind-modules

%if %{with clustering}
%post -n ctdb
/usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/ctdb.conf
%systemd_post ctdb.service

%preun -n ctdb
%systemd_preun ctdb.service

%postun -n ctdb
%systemd_postun_with_restart ctdb.service
%endif

%ldconfig_scriptlets -n libldb
%ldconfig_scriptlets -n python3-ldb

### SAMBA
%files
%doc examples/autofs examples/LDAP examples/misc
%doc examples/printer-accounting examples/printing
%doc packaging/README.downgrade
%{_bindir}/smbstatus
%{_sbindir}/eventlogadm
%{_sbindir}/nmbd
%{_sbindir}/smbd
%if %{with dc}
# This is only used by vfs_dfs_samba4
%{_libdir}/samba/libdfs-server-ad-private-samba.so
%endif
%dir %{_libdir}/samba/auth
%{_libdir}/samba/auth/unix.so
%dir %{_libdir}/samba/vfs
%{_libdir}/samba/vfs/acl_tdb.so
%{_libdir}/samba/vfs/acl_xattr.so
%{_libdir}/samba/vfs/aio_fork.so
%{_libdir}/samba/vfs/aio_pthread.so
%{_libdir}/samba/vfs/audit.so
%{_libdir}/samba/vfs/btrfs.so
%{_libdir}/samba/vfs/cap.so
%{_libdir}/samba/vfs/catia.so
%{_libdir}/samba/vfs/commit.so
%{_libdir}/samba/vfs/crossrename.so
%{_libdir}/samba/vfs/default_quota.so
%if %{with dc}
%{_libdir}/samba/vfs/dfs_samba4.so
%endif
%{_libdir}/samba/vfs/dirsort.so
%{_libdir}/samba/vfs/expand_msdfs.so
%{_libdir}/samba/vfs/extd_audit.so
%{_libdir}/samba/vfs/fake_perms.so
%{_libdir}/samba/vfs/fileid.so
%{_libdir}/samba/vfs/fruit.so
%{_libdir}/samba/vfs/full_audit.so
%{_libdir}/samba/vfs/gpfs.so
%{_libdir}/samba/vfs/glusterfs_fuse.so
%{_libdir}/samba/vfs/linux_xfs_sgid.so
%{_libdir}/samba/vfs/media_harmony.so
%{_libdir}/samba/vfs/offline.so
%{_libdir}/samba/vfs/preopen.so
%{_libdir}/samba/vfs/readahead.so
%{_libdir}/samba/vfs/readonly.so
%{_libdir}/samba/vfs/recycle.so
%{_libdir}/samba/vfs/shadow_copy.so
%{_libdir}/samba/vfs/shadow_copy2.so
%{_libdir}/samba/vfs/shell_snap.so
%{_libdir}/samba/vfs/snapper.so
%{_libdir}/samba/vfs/streams_depot.so
%{_libdir}/samba/vfs/streams_xattr.so
%{_libdir}/samba/vfs/syncops.so
%{_libdir}/samba/vfs/time_audit.so
%{_libdir}/samba/vfs/unityed_media.so
%{_libdir}/samba/vfs/virusfilter.so
%{_libdir}/samba/vfs/widelinks.so
%{_libdir}/samba/vfs/worm.so
%{_libdir}/samba/vfs/xattr_tdb.so

%dir %{_libexecdir}/samba
%{_libexecdir}/samba/samba-bgqd

%dir %{_datadir}/samba
%dir %{_datadir}/samba/mdssvc
%{_datadir}/samba/mdssvc/elasticsearch_mappings.json

%{_unitdir}/nmb.service
%{_unitdir}/smb.service
%{_unitdir}/samba-bgqd.service
%dir %{_sysconfdir}/openldap/schema
%config %{_sysconfdir}/openldap/schema/samba.schema
%config(noreplace) %{_sysconfdir}/pam.d/samba
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man8/eventlogadm.8*
%{_mandir}/man8/samba-bgqd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/vfs_acl_tdb.8*
%{_mandir}/man8/vfs_acl_xattr.8*
%{_mandir}/man8/vfs_aio_fork.8*
%{_mandir}/man8/vfs_aio_pthread.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_btrfs.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_crossrename.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_dirsort.8*
%{_mandir}/man8/vfs_expand_msdfs.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_fileid.8*
%{_mandir}/man8/vfs_fruit.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_glusterfs_fuse.8*
%{_mandir}/man8/vfs_linux_xfs_sgid.8*
%{_mandir}/man8/vfs_media_harmony.8*
%{_mandir}/man8/vfs_offline.8*
%{_mandir}/man8/vfs_preopen.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%{_mandir}/man8/vfs_shadow_copy2.8*
%{_mandir}/man8/vfs_shell_snap.8*
%{_mandir}/man8/vfs_snapper.8*
%{_mandir}/man8/vfs_streams_depot.8*
%{_mandir}/man8/vfs_streams_xattr.8*
%{_mandir}/man8/vfs_syncops.8*
%{_mandir}/man8/vfs_time_audit.8*
%{_mandir}/man8/vfs_unityed_media.8*
%{_mandir}/man8/vfs_virusfilter.8*
%{_mandir}/man8/vfs_widelinks.8*
%{_mandir}/man8/vfs_worm.8*
%{_mandir}/man8/vfs_xattr_tdb.8*

%attr(775,root,printadmin) %dir /var/lib/samba/drivers

### CLIENT
%files client
%doc source3/client/README.smbspool
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/dumpmscat
%{_bindir}/mvxattr
%{_bindir}/mdsearch
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/regdiff
%{_bindir}/regpatch
%{_bindir}/regshell
%{_bindir}/regtree
%{_bindir}/rpcclient
%{_bindir}/samba-regedit
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/smbtree
%{_bindir}/wspsearch
%dir %{_libexecdir}/samba
%ghost %{_libexecdir}/samba/cups_backend_smb
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/oLschema2ldif.1*
%{_mandir}/man1/regdiff.1*
%{_mandir}/man1/regpatch.1*
%{_mandir}/man1/regshell.1*
%{_mandir}/man1/regtree.1*
%{_mandir}/man1/log2pcap.1*
%{_mandir}/man1/mdsearch.1*
%{_mandir}/man1/mvxattr.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/wspsearch.1*
%{_mandir}/man7/traffic_learner.7.*
%{_mandir}/man7/traffic_replay.7.*
%{_mandir}/man8/cifsdd.8.*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/smbspool.8*

%if %{with includelibs}
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbrestore
%{_bindir}/tdbtool

%{_mandir}/man1/ldbadd.1.gz
%{_mandir}/man1/ldbdel.1.gz
%{_mandir}/man1/ldbedit.1.gz
%{_mandir}/man1/ldbmodify.1.gz
%{_mandir}/man1/ldbrename.1.gz
%{_mandir}/man1/ldbsearch.1.gz
%{_mandir}/man8/tdbbackup.8.gz
%{_mandir}/man8/tdbdump.8.gz
%{_mandir}/man8/tdbrestore.8.gz
%{_mandir}/man8/tdbtool.8.gz
#endif with includelibs
%endif

### CLIENT-LIBS
%files client-libs
%{_libdir}/libdcerpc-binding.so.%{libdcerpc_binding_so_version}*
%{_libdir}/libdcerpc-server-core.so.%{libdcerpc_server_core_so_version}*
%{_libdir}/libdcerpc.so.%{libdcerpc_so_version}*
%{_libdir}/libndr-krb5pac.so.%{libndr_krb5pac_so_version}*
%{_libdir}/libndr-nbt.so.%{libndr_nbt_so_version}*
%{_libdir}/libndr-standard.so.%{libndr_standard_so_version}*
%{_libdir}/libndr.so.%{libndr_so_version}*
%{_libdir}/libsamba-credentials.so.%{libsamba_credentials_so_version}*
%{_libdir}/libsamba-errors.so.%{libsamba_errors_so_version}*
%{_libdir}/libsamba-hostconfig.so.%{libsamba_hostconfig_so_version}*
%{_libdir}/libsamba-passdb.so.%{libsamba_passdb_so_version}*
%{_libdir}/libsamba-util.so.%{libsamba_util_so_version}*
%{_libdir}/libsamdb.so.%{libsamdb_so_version}*
%{_libdir}/libsmbconf.so.%{libsmbconf_so_version}*
%{_libdir}/libsmbldap.so.%{libsmbldap_so_version}*
%{_libdir}/libtevent-util.so.%{libtevent_util_so_version}*

%dir %{_libdir}/samba
%{_libdir}/samba/libCHARSET3-private-samba.so
%{_libdir}/samba/libMESSAGING-SEND-private-samba.so
%{_libdir}/samba/libMESSAGING-private-samba.so
%{_libdir}/samba/libaddns-private-samba.so
%{_libdir}/samba/libads-private-samba.so
%{_libdir}/samba/libasn1util-private-samba.so
%{_libdir}/samba/libauth-private-samba.so
%{_libdir}/samba/libauthkrb5-private-samba.so
%{_libdir}/samba/libcli-cldap-private-samba.so
%{_libdir}/samba/libcli-ldap-common-private-samba.so
%{_libdir}/samba/libcli-ldap-private-samba.so
%{_libdir}/samba/libcli-nbt-private-samba.so
%{_libdir}/samba/libcli-smb-common-private-samba.so
%{_libdir}/samba/libcli-spoolss-private-samba.so
%{_libdir}/samba/libcliauth-private-samba.so
%{_libdir}/samba/libclidns-private-samba.so
%{_libdir}/samba/libcluster-private-samba.so
%{_libdir}/samba/libcmdline-contexts-private-samba.so
%{_libdir}/samba/libcommon-auth-private-samba.so
%{_libdir}/samba/libctdb-event-client-private-samba.so
%{_libdir}/samba/libdbwrap-private-samba.so
%{_libdir}/samba/libdcerpc-pkt-auth-private-samba.so
%{_libdir}/samba/libdcerpc-samba-private-samba.so
%{_libdir}/samba/libevents-private-samba.so
%{_libdir}/samba/libflag-mapping-private-samba.so
%{_libdir}/samba/libgenrand-private-samba.so
%{_libdir}/samba/libgensec-private-samba.so
%{_libdir}/samba/libgpext-private-samba.so
%{_libdir}/samba/libgpo-private-samba.so
%{_libdir}/samba/libgse-private-samba.so
%{_libdir}/samba/libhttp-private-samba.so
%{_libdir}/samba/libinterfaces-private-samba.so
%{_libdir}/samba/libiov-buf-private-samba.so
%{_libdir}/samba/libkrb5samba-private-samba.so
%{_libdir}/samba/libldbsamba-private-samba.so
%{_libdir}/samba/liblibcli-lsa3-private-samba.so
%{_libdir}/samba/liblibcli-netlogon3-private-samba.so
%{_libdir}/samba/liblibsmb-private-samba.so
%{_libdir}/samba/libmessages-dgm-private-samba.so
%{_libdir}/samba/libmessages-util-private-samba.so
%{_libdir}/samba/libmscat-private-samba.so
%{_libdir}/samba/libmsghdr-private-samba.so
%{_libdir}/samba/libmsrpc3-private-samba.so
%{_libdir}/samba/libndr-samba-private-samba.so
%{_libdir}/samba/libndr-samba4-private-samba.so
%{_libdir}/samba/libnet-keytab-private-samba.so
%{_libdir}/samba/libnetif-private-samba.so
%{_libdir}/samba/libnpa-tstream-private-samba.so
%{_libdir}/samba/libposix-eadb-private-samba.so
%{_libdir}/samba/libprinter-driver-private-samba.so
%{_libdir}/samba/libprinting-migrate-private-samba.so
%{_libdir}/samba/libreplace-private-samba.so
%{_libdir}/samba/libregistry-private-samba.so
%{_libdir}/samba/libsamba-cluster-support-private-samba.so
%{_libdir}/samba/libsamba-debug-private-samba.so
%{_libdir}/samba/libsamba-modules-private-samba.so
%{_libdir}/samba/libsamba-security-private-samba.so
%{_libdir}/samba/libsamba-sockets-private-samba.so
%{_libdir}/samba/libsamba3-util-private-samba.so
%{_libdir}/samba/libsamdb-common-private-samba.so
%{_libdir}/samba/libsecrets3-private-samba.so
%{_libdir}/samba/libserver-id-db-private-samba.so
%{_libdir}/samba/libserver-role-private-samba.so
%{_libdir}/samba/libsmb-transport-private-samba.so
%{_libdir}/samba/libsmbclient-raw-private-samba.so
%{_libdir}/samba/libsmbd-base-private-samba.so
%{_libdir}/samba/libsmbd-shim-private-samba.so
%{_libdir}/samba/libsmbldaphelper-private-samba.so
%{_libdir}/samba/libstable-sort-private-samba.so
%{_libdir}/samba/libsys-rw-private-samba.so
%{_libdir}/samba/libsocket-blocking-private-samba.so
%{_libdir}/samba/libtalloc-report-printf-private-samba.so
%{_libdir}/samba/libtalloc-report-private-samba.so
%{_libdir}/samba/libtdb-wrap-private-samba.so
%{_libdir}/samba/libtime-basic-private-samba.so
%{_libdir}/samba/libtorture-private-samba.so
%{_libdir}/samba/libutil-crypt-private-samba.so
%{_libdir}/samba/libutil-reg-private-samba.so
%{_libdir}/samba/libutil-setid-private-samba.so
%{_libdir}/samba/libutil-tdb-private-samba.so

%if %{without libwbclient}
%{_libdir}/samba/libwbclient.so.*
#endif without libwbclient
%endif

%if %{without libsmbclient}
%{_libdir}/samba/libsmbclient.so.%{libsmbclient_so_version}*
%{_mandir}/man7/libsmbclient.7*
#endif without libsmbclient
%endif

%if %{with includelibs}
%{_libdir}/samba/libldb-*.so
%{_libdir}/samba/libtalloc-private-samba.so
%{_libdir}/samba/libtdb-private-samba.so
%{_libdir}/samba/libtevent-private-samba.so

%{_mandir}/man3/ldb.3.gz
%{_mandir}/man3/talloc.3.gz
#endif with includelibs
%endif

### COMMON
%files common
%doc README.md WHATSNEW.txt
%license COPYING
%{_tmpfilesdir}/samba.conf
%{_sysusersdir}/samba.conf
%dir %{_sysconfdir}/logrotate.d/
%config(noreplace) %{_sysconfdir}/logrotate.d/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(0700,root,root) %dir /var/log/samba/old
%ghost %dir /run/samba
%ghost %dir /run/winbindd
%dir /var/lib/samba
%dir /var/lib/samba/certs
%attr(700,root,root) %dir /var/lib/samba/private
%attr(700,root,root) %dir /var/lib/samba/private/certs
%dir /var/lib/samba/lock
%attr(755,root,root) %dir %{_sysconfdir}/samba
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%{_sysconfdir}/samba/smb.conf.example
%config(noreplace) %{_sysconfdir}/samba/lmhosts
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*

### COMMON-LIBS
%files common-libs
# common libraries
%{_libdir}/samba/libcmdline-private-samba.so

%dir %{_libdir}/samba/ldb

%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so

### COMMON-TOOLS
%files common-tools
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/samba-log-parser
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/testparm
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/samba-log-parser.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man8/net.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbpasswd.8*

### TOOLS
%files tools
%{_bindir}/samba-tool
%{_mandir}/man8/samba-tool.8*

### RPC
%files dcerpc
%dir %{_libexecdir}/samba
%{_libexecdir}/samba/samba-dcerpcd
%{_libexecdir}/samba/rpcd_classic
%{_libexecdir}/samba/rpcd_epmapper
%{_libexecdir}/samba/rpcd_fsrvp
%{_libexecdir}/samba/rpcd_lsad
%{_libexecdir}/samba/rpcd_mdssvc
%{_libexecdir}/samba/rpcd_spoolss
%{_libexecdir}/samba/rpcd_winreg
%{_libexecdir}/samba/rpcd_witness
%{_mandir}/man8/samba-dcerpcd.8*

### DC
%if %{with dc}
%files dc
%{_unitdir}/samba.service
%{_sbindir}/samba
%{_sbindir}/samba_dnsupdate
%{_sbindir}/samba_downgrade_db
%{_sbindir}/samba_kcc
%{_sbindir}/samba_spnupdate
%{_sbindir}/samba_upgradedns

%{_libdir}/krb5/plugins/kdb/samba.so

%{_libdir}/samba/auth/samba4.so
%dir %{_libdir}/samba/gensec
%{_libdir}/samba/gensec/krb5.so
%{_libdir}/samba/ldb/acl.so
%{_libdir}/samba/ldb/aclread.so
%{_libdir}/samba/ldb/anr.so
%{_libdir}/samba/ldb/audit_log.so
%{_libdir}/samba/ldb/count_attrs.so
%{_libdir}/samba/ldb/descriptor.so
%{_libdir}/samba/ldb/dirsync.so
%{_libdir}/samba/ldb/dns_notify.so
%{_libdir}/samba/ldb/dsdb_notification.so
%{_libdir}/samba/ldb/encrypted_secrets.so
%{_libdir}/samba/ldb/extended_dn_in.so
%{_libdir}/samba/ldb/extended_dn_out.so
%{_libdir}/samba/ldb/extended_dn_store.so
%{_libdir}/samba/ldb/group_audit_log.so
%{_libdir}/samba/ldb/instancetype.so
%{_libdir}/samba/ldb/lazy_commit.so
%{_libdir}/samba/ldb/linked_attributes.so
%{_libdir}/samba/ldb/new_partition.so
%{_libdir}/samba/ldb/objectclass.so
%{_libdir}/samba/ldb/objectclass_attrs.so
%{_libdir}/samba/ldb/objectguid.so
%{_libdir}/samba/ldb/operational.so
%{_libdir}/samba/ldb/paged_results.so
%{_libdir}/samba/ldb/partition.so
%{_libdir}/samba/ldb/password_hash.so
%{_libdir}/samba/ldb/ranged_results.so
%{_libdir}/samba/ldb/repl_meta_data.so
%{_libdir}/samba/ldb/resolve_oids.so
%{_libdir}/samba/ldb/rootdse.so
%{_libdir}/samba/ldb/samba3sam.so
%{_libdir}/samba/ldb/samba3sid.so
%{_libdir}/samba/ldb/samba_dsdb.so
%{_libdir}/samba/ldb/samba_secrets.so
%{_libdir}/samba/ldb/samldb.so
%{_libdir}/samba/ldb/schema_data.so
%{_libdir}/samba/ldb/schema_load.so
%{_libdir}/samba/ldb/secrets_tdb_sync.so
%{_libdir}/samba/ldb/show_deleted.so
%{_libdir}/samba/ldb/subtree_delete.so
%{_libdir}/samba/ldb/subtree_rename.so
%{_libdir}/samba/ldb/tombstone_reanimate.so
%{_libdir}/samba/ldb/unique_object_sids.so
%{_libdir}/samba/ldb/update_keytab.so
%{_libdir}/samba/ldb/vlv.so
%{_libdir}/samba/ldb/wins_ldb.so

%{_libdir}/samba/vfs/posix_eadb.so
%dir /var/lib/samba/sysvol
%{_mandir}/man8/samba.8*
%{_mandir}/man8/samba_downgrade_db.8*
%dir %{_datadir}/samba/admx
%{_datadir}/samba/admx/GNOME_Settings.admx
%{_datadir}/samba/admx/samba.admx
%dir %{_datadir}/samba/admx/en-US
%{_datadir}/samba/admx/en-US/GNOME_Settings.adml
%{_datadir}/samba/admx/en-US/samba.adml
%dir %{_datadir}/samba/admx/ru-RU
%{_datadir}/samba/admx/ru-RU/GNOME_Settings.adml

%files dc-provision
%license source4/setup/ad-schema/licence.txt
%{_datadir}/samba/setup

#endif with dc
%endif
### DC-LIBS
%files dc-libs
%{_libdir}/libsamba-policy.so.%{libsamba_policy_so_version}*
%{_libdir}/samba/libauth4-private-samba.so
%{_libdir}/samba/libsamba-net-private-samba.so

%if %{with dc}
%{_libdir}/samba/libdb-glue-private-samba.so
%{_libdir}/samba/libpac-private-samba.so
%{_libdir}/samba/libprocess-model-private-samba.so
%{_libdir}/samba/libservice-private-samba.so

%dir %{_libdir}/samba/process_model
%{_libdir}/samba/process_model/prefork.so
%{_libdir}/samba/process_model/standard.so
%dir %{_libdir}/samba/service
%{_libdir}/samba/service/cldap.so
%{_libdir}/samba/service/dcerpc.so
%{_libdir}/samba/service/dns.so
%{_libdir}/samba/service/dns_update.so
%{_libdir}/samba/service/drepl.so
%{_libdir}/samba/service/kcc.so
%{_libdir}/samba/service/kdc.so
%{_libdir}/samba/service/ldap.so
%{_libdir}/samba/service/nbtd.so
%{_libdir}/samba/service/ntp_signd.so
%{_libdir}/samba/service/s3fs.so
%{_libdir}/samba/service/winbindd.so
%{_libdir}/samba/service/wrepl.so

%{_libdir}/libdcerpc-server.so.*
%{_libdir}/samba/libad-claims-private-samba.so
%{_libdir}/samba/libauthn-policy-util-private-samba.so
%{_libdir}/samba/libdsdb-module-private-samba.so
%{_libdir}/samba/libdsdb-garbage-collect-tombstones-private-samba.so
%{_libdir}/samba/libscavenge-dns-records-private-samba.so

### DC-BIND
%files dc-bind-dlz
%attr(770,root,named) %dir /var/lib/samba/bind-dns
%dir %{_libdir}/samba/bind9
%{_libdir}/samba/bind9/dlz_bind9_10.so
%{_libdir}/samba/bind9/dlz_bind9_11.so
%{_libdir}/samba/bind9/dlz_bind9_12.so
%{_libdir}/samba/bind9/dlz_bind9_14.so
%{_libdir}/samba/bind9/dlz_bind9_16.so
%{_libdir}/samba/bind9/dlz_bind9_18.so
#endif with dc
%endif

### DEVEL
%files devel
%{_includedir}/samba-4.0/charset.h
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/hresult.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/ntstatus_gen.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/core/werror_gen.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/dcesrv_core.h
%{_includedir}/samba-4.0/domain_credentials.h
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/claims.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_misc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl_c.h
%{_includedir}/samba-4.0/gen_ndr/netlogon.h
%{_includedir}/samba-4.0/gen_ndr/samr.h
%{_includedir}/samba-4.0/gen_ndr/security.h
%{_includedir}/samba-4.0/gen_ndr/server_id.h
%{_includedir}/samba-4.0/gen_ndr/svcctl.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smb3posix.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/blocking.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/discard.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/substitute.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util/tfork.h
%{_includedir}/samba-4.0/util_ldb.h
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc-server-core.so
%{_libdir}/libdcerpc.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so
%{_libdir}/libndr.so
%{_libdir}/libsamba-credentials.so
%{_libdir}/libsamba-errors.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-util.so
%{_libdir}/libsamdb.so
%{_libdir}/libsmbconf.so
%{_libdir}/libtevent-util.so
%{_libdir}/pkgconfig/dcerpc.pc
%{_libdir}/pkgconfig/dcerpc_samr.pc
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_krb5pac.pc
%{_libdir}/pkgconfig/ndr_nbt.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/pkgconfig/samba-credentials.pc
%{_libdir}/pkgconfig/samba-hostconfig.pc
%{_libdir}/pkgconfig/samba-policy.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/samdb.pc
%{_libdir}/libsamba-passdb.so
%{_libdir}/libsamba-policy.so
%{_libdir}/libsmbldap.so

%if %{with dc}
%{_includedir}/samba-4.0/dcerpc_server.h
%{_libdir}/libdcerpc-server.so
%{_libdir}/pkgconfig/dcerpc_server.pc
%endif

%if %{without libsmbclient}
%{_includedir}/samba-4.0/libsmbclient.h
#endif without libsmbclient
%endif

%if %{without libwbclient}
%{_includedir}/samba-4.0/wbclient.h
#endif without libwbclient
%endif

### VFS-CEPHFS
%if %{with vfs_cephfs}
%files vfs-cephfs
%{_libdir}/samba/vfs/ceph.so
%{_libdir}/samba/vfs/ceph_new.so
%{_libdir}/samba/vfs/ceph_snapshots.so
%{_mandir}/man8/vfs_ceph.8*
%{_mandir}/man8/vfs_ceph_new.8*
%{_mandir}/man8/vfs_ceph_snapshots.8*
%endif

### VFS-IOURING
%if %{with vfs_io_uring}
%files vfs-iouring
%{_libdir}/samba/vfs/io_uring.so
%{_mandir}/man8/vfs_io_uring.8*
%endif

### VFS-GLUSTERFS
%if %{with vfs_glusterfs}
%files vfs-glusterfs
%{_libdir}/samba/vfs/glusterfs.so
%{_mandir}/man8/vfs_glusterfs.8*
%endif

### GPUPDATE
%if %{with gpupdate}
%files gpupdate
%{_mandir}/man8/samba-gpupdate.8*
%{_sbindir}/samba-gpupdate
#endif with gpupdate
%endif

### KRB5-PRINTING
%files krb5-printing
%attr(0700,root,root) %{_libexecdir}/samba/smbspool_krb5_wrapper
%{_mandir}/man8/smbspool_krb5_wrapper.8*

### LDB-LDAP-MODULES
%files ldb-ldap-modules
%{_libdir}/samba/ldb/ldbsamba_extensions.so
%{_libdir}/samba/ldb/ildap.so
%{_libdir}/samba/ldb/ldap.so

### LIBS
%files libs
%{_libdir}/libdcerpc-samr.so.*

%{_libdir}/samba/libLIBWBCLIENT-OLD-private-samba.so
%{_libdir}/samba/libauth-unix-token-private-samba.so
%{_libdir}/samba/libdcerpc-samba4-private-samba.so
%{_libdir}/samba/libdnsserver-common-private-samba.so
%{_libdir}/samba/libshares-private-samba.so
%{_libdir}/samba/libsmbpasswdparser-private-samba.so
%{_libdir}/samba/libxattr-tdb-private-samba.so
%{_libdir}/samba/libREG-FULL-private-samba.so
%{_libdir}/samba/libRPC-SERVER-LOOP-private-samba.so
%{_libdir}/samba/libRPC-WORKER-private-samba.so

### LIBNETAPI
%files -n libnetapi
%{_libdir}/libnetapi.so.%{libnetapi_so_version}*

### LIBNETAPI-DEVEL
%files -n libnetapi-devel
%{_includedir}/samba-4.0/netapi.h
%{_libdir}/libnetapi.so
%{_libdir}/pkgconfig/netapi.pc

### LIBSMBCLIENT
%if %{with libsmbclient}
%files -n libsmbclient
%{_libdir}/libsmbclient.so.*

### LIBSMBCLIENT-DEVEL
%files -n libsmbclient-devel
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*
#endif {with libsmbclient}
%endif

### LIBWBCLIENT
%if %{with libwbclient}
%files -n libwbclient
%{_libdir}/libwbclient.so.%{libwbclient_so_version}*

### LIBWBCLIENT-DEVEL
%files -n libwbclient-devel
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc
#endif {with libwbclient}
%endif

### PIDL
%files pidl
%doc pidl/README
%attr(755,root,root) %{_bindir}/pidl
%dir %{perl_vendorlib}/Parse
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl.pm
%dir %{perl_vendorlib}/Parse/Pidl
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Base.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/CUtil.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Expr.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/ODL.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Typelist.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/IDL.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Compat.pm
%dir %{perl_vendorlib}/Parse/Pidl/Wireshark
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Wireshark/Conformance.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Wireshark/NDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Dump.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba3
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/ServerNDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/ClientNDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba3/Template.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Header.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/COM
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Header.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Proxy.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/COM/Stub.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Python.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/Template.pm
%dir %{perl_vendorlib}/Parse/Pidl/Samba4/NDR
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Server.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/ServerCompat.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Client.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/NDR/Parser.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Samba4/TDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/NDR.pm
%attr(644,root,root) %{perl_vendorlib}/Parse/Pidl/Util.pm
%attr(644,root,root) %{_mandir}/man1/pidl.1*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Dump.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::NDR.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Util.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Wireshark::Conformance.3pm*
%attr(644,root,root) %{_mandir}/man3/Parse::Pidl::Wireshark::NDR.3pm*

### PYTHON3
%files -n python3-%{name}
%dir %{python3_sitearch}/samba/
%{python3_sitearch}/samba/__init__.py
%dir %{python3_sitearch}/samba/__pycache__
%{python3_sitearch}/samba/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/__pycache__/auth_util.*.pyc
%{python3_sitearch}/samba/__pycache__/colour.*.pyc
%{python3_sitearch}/samba/__pycache__/common.*.pyc
%{python3_sitearch}/samba/__pycache__/dbchecker.*.pyc
%{python3_sitearch}/samba/__pycache__/descriptor.*.pyc
%{python3_sitearch}/samba/__pycache__/dnsresolver.*.pyc
%{python3_sitearch}/samba/__pycache__/drs_utils.*.pyc
%{python3_sitearch}/samba/__pycache__/functional_level.*.pyc
%{python3_sitearch}/samba/__pycache__/getopt.*.pyc
%{python3_sitearch}/samba/__pycache__/gkdi.*.pyc
%{python3_sitearch}/samba/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/samba/__pycache__/idmap.*.pyc
%{python3_sitearch}/samba/__pycache__/join.*.pyc
%{python3_sitearch}/samba/__pycache__/lsa_utils.*.pyc
%{python3_sitearch}/samba/__pycache__/logger.*.pyc
%{python3_sitearch}/samba/__pycache__/mdb_util.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_display_specifiers.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_schema.*.pyc
%{python3_sitearch}/samba/__pycache__/ndr.*.pyc
%{python3_sitearch}/samba/__pycache__/ntacls.*.pyc
%{python3_sitearch}/samba/__pycache__/nt_time.*.pyc
%{python3_sitearch}/samba/__pycache__/policies.*.pyc
%{python3_sitearch}/samba/__pycache__/safe_tarfile.*.pyc
%{python3_sitearch}/samba/__pycache__/sd_utils.*.pyc
%{python3_sitearch}/samba/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/__pycache__/subnets.*.pyc
%{python3_sitearch}/samba/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/samba/__pycache__/upgrade.*.pyc
%{python3_sitearch}/samba/__pycache__/upgradehelpers.*.pyc
%{python3_sitearch}/samba/__pycache__/xattr.*.pyc
%{python3_sitearch}/samba/_glue.*.so
%{python3_sitearch}/samba/_ldb.*.so
%{python3_sitearch}/samba/auth.*.so
%{python3_sitearch}/samba/auth_util.py
%{python3_sitearch}/samba/dbchecker.py
%{python3_sitearch}/samba/colour.py
%{python3_sitearch}/samba/common.py
%{python3_sitearch}/samba/compression.*.so
%{python3_sitearch}/samba/credentials.*.so
%{python3_sitearch}/samba/crypto.*.so
%dir %{python3_sitearch}/samba/dcerpc
%dir %{python3_sitearch}/samba/dcerpc/__pycache__
%{python3_sitearch}/samba/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/dcerpc/__init__.py
%{python3_sitearch}/samba/dcerpc/atsvc.*.so
%{python3_sitearch}/samba/dcerpc/auth.*.so
%{python3_sitearch}/samba/dcerpc/base.*.so
%{python3_sitearch}/samba/dcerpc/claims.*.so
%{python3_sitearch}/samba/dcerpc/conditional_ace.*.so
%{python3_sitearch}/samba/dcerpc/dcerpc.*.so
%{python3_sitearch}/samba/dcerpc/dfs.*.so
%{python3_sitearch}/samba/dcerpc/dns.*.so
%{python3_sitearch}/samba/dcerpc/dnsp.*.so
%{python3_sitearch}/samba/dcerpc/drsblobs.*.so
%{python3_sitearch}/samba/dcerpc/drsuapi.*.so
%{python3_sitearch}/samba/dcerpc/echo.*.so
%{python3_sitearch}/samba/dcerpc/epmapper.*.so
%{python3_sitearch}/samba/dcerpc/gkdi.*.so
%{python3_sitearch}/samba/dcerpc/gmsa.*.so
%{python3_sitearch}/samba/dcerpc/idmap.*.so
%{python3_sitearch}/samba/dcerpc/initshutdown.*.so
%{python3_sitearch}/samba/dcerpc/irpc.*.so
%{python3_sitearch}/samba/dcerpc/krb5ccache.*.so
%{python3_sitearch}/samba/dcerpc/krb5pac.*.so
%{python3_sitearch}/samba/dcerpc/lsa.*.so
%{python3_sitearch}/samba/dcerpc/messaging.*.so
%{python3_sitearch}/samba/dcerpc/mdssvc.*.so
%{python3_sitearch}/samba/dcerpc/mgmt.*.so
%{python3_sitearch}/samba/dcerpc/misc.*.so
%{python3_sitearch}/samba/dcerpc/nbt.*.so
%{python3_sitearch}/samba/dcerpc/netlogon.*.so
%{python3_sitearch}/samba/dcerpc/ntlmssp.*.so
%{python3_sitearch}/samba/dcerpc/preg.*.so
%{python3_sitearch}/samba/dcerpc/samr.*.so
%{python3_sitearch}/samba/dcerpc/schannel.*.so
%{python3_sitearch}/samba/dcerpc/security.*.so
%{python3_sitearch}/samba/dcerpc/server_id.*.so
%{python3_sitearch}/samba/dcerpc/smb_acl.*.so
%{python3_sitearch}/samba/dcerpc/smb3posix.*.so
%{python3_sitearch}/samba/dcerpc/smbXsrv.*.so
%{python3_sitearch}/samba/dcerpc/spoolss.*.so
%{python3_sitearch}/samba/dcerpc/srvsvc.*.so
%{python3_sitearch}/samba/dcerpc/svcctl.*.so
%{python3_sitearch}/samba/dcerpc/unixinfo.*.so
%{python3_sitearch}/samba/dcerpc/winbind.*.so
%{python3_sitearch}/samba/dcerpc/windows_event_ids.*.so
%{python3_sitearch}/samba/dcerpc/winreg.*.so
%{python3_sitearch}/samba/dcerpc/winspool.*.so
%{python3_sitearch}/samba/dcerpc/witness.*.so
%{python3_sitearch}/samba/dcerpc/wkssvc.*.so
%{python3_sitearch}/samba/dcerpc/xattr.*.so
%{python3_sitearch}/samba/descriptor.py
%{python3_sitearch}/samba/dnsresolver.py
%dir %{python3_sitearch}/samba/domain
%{python3_sitearch}/samba/domain/__init__.py
%{python3_sitearch}/samba/domain/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/domain/models/__init__.py
%{python3_sitearch}/samba/domain/models/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/auth_policy.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/auth_silo.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/claim_type.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/computer.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/constants.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/container.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/exceptions.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/fields.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/gmsa.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/group.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/model.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/org.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/person.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/query.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/registry.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/site.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/subnet.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/types.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/user.*.pyc
%{python3_sitearch}/samba/domain/models/__pycache__/value_type.*.pyc
%{python3_sitearch}/samba/domain/models/auth_policy.py
%{python3_sitearch}/samba/domain/models/auth_silo.py
%{python3_sitearch}/samba/domain/models/claim_type.py
%{python3_sitearch}/samba/domain/models/computer.py
%{python3_sitearch}/samba/domain/models/constants.py
%{python3_sitearch}/samba/domain/models/container.py
%{python3_sitearch}/samba/domain/models/exceptions.py
%{python3_sitearch}/samba/domain/models/fields.py
%{python3_sitearch}/samba/domain/models/gmsa.py
%{python3_sitearch}/samba/domain/models/group.py
%{python3_sitearch}/samba/domain/models/model.py
%{python3_sitearch}/samba/domain/models/org.py
%{python3_sitearch}/samba/domain/models/person.py
%{python3_sitearch}/samba/domain/models/query.py
%{python3_sitearch}/samba/domain/models/registry.py
%{python3_sitearch}/samba/domain/models/schema.py
%{python3_sitearch}/samba/domain/models/site.py
%{python3_sitearch}/samba/domain/models/subnet.py
%{python3_sitearch}/samba/domain/models/types.py
%{python3_sitearch}/samba/domain/models/user.py
%{python3_sitearch}/samba/domain/models/value_type.py
%{python3_sitearch}/samba/drs_utils.py
%{python3_sitearch}/samba/dsdb.*.so
%{python3_sitearch}/samba/dsdb_dns.*.so
%{python3_sitearch}/samba/functional_level.py
%{python3_sitearch}/samba/gensec.*.so
%{python3_sitearch}/samba/getopt.py
%{python3_sitearch}/samba/gkdi.py
%{python3_sitearch}/samba/graph.py
%{python3_sitearch}/samba/hostconfig.py
%{python3_sitearch}/samba/idmap.py
%{python3_sitearch}/samba/join.py
%{python3_sitearch}/samba/lsa_utils.py
%{python3_sitearch}/samba/messaging.*.so
%{python3_sitearch}/samba/ndr.py
%{python3_sitearch}/samba/net.*.so
%{python3_sitearch}/samba/net_s3.*.so
%{python3_sitearch}/samba/ntstatus.*.so
%{python3_sitearch}/samba/posix_eadb.*.so
%dir %{python3_sitearch}/samba/emulate
%dir %{python3_sitearch}/samba/emulate/__pycache__
%{python3_sitearch}/samba/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/samba/emulate/__pycache__/traffic_packets.*.pyc
%{python3_sitearch}/samba/emulate/__init__.py
%{python3_sitearch}/samba/emulate/traffic.py
%{python3_sitearch}/samba/emulate/traffic_packets.py
%dir %{python3_sitearch}/samba/gp
%dir %{python3_sitearch}/samba/gp/__pycache__
%{python3_sitearch}/samba/gp/__init__.py
%{python3_sitearch}/samba/gp/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gpclass.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_centrify_crontab_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_centrify_sudoers_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_cert_auto_enroll_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_drive_maps_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_chromium_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_ext_loader.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_firefox_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_firewalld_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_gnome_settings_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_msgs_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_scripts_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_sec_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_smb_conf_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/gp_sudoers_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_access_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_files_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_issue_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_motd_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_openssh_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_startup_scripts_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_sudoers_ext.*.pyc
%{python3_sitearch}/samba/gp/__pycache__/vgp_symlink_ext.*.pyc
%{python3_sitearch}/samba/gp/gpclass.py
%{python3_sitearch}/samba/gp/gp_gnome_settings_ext.py
%{python3_sitearch}/samba/gp/gp_scripts_ext.py
%{python3_sitearch}/samba/gp/gp_sec_ext.py
%{python3_sitearch}/samba/gp/gp_centrify_crontab_ext.py
%{python3_sitearch}/samba/gp/gp_centrify_sudoers_ext.py
%{python3_sitearch}/samba/gp/gp_cert_auto_enroll_ext.py
%{python3_sitearch}/samba/gp/gp_drive_maps_ext.py
%{python3_sitearch}/samba/gp/gp_chromium_ext.py
%{python3_sitearch}/samba/gp/gp_ext_loader.py
%{python3_sitearch}/samba/gp/gp_firefox_ext.py
%{python3_sitearch}/samba/gp/gp_firewalld_ext.py
%{python3_sitearch}/samba/gp/gp_msgs_ext.py
%{python3_sitearch}/samba/gp/gp_smb_conf_ext.py
%{python3_sitearch}/samba/gp/gp_sudoers_ext.py
%dir %{python3_sitearch}/samba/gp/util
%dir %{python3_sitearch}/samba/gp/util/__pycache__
%{python3_sitearch}/samba/gp/util/__pycache__/logging.*.pyc
%{python3_sitearch}/samba/gp/util/logging.py
%{python3_sitearch}/samba/gp/vgp_access_ext.py
%{python3_sitearch}/samba/gp/vgp_files_ext.py
%{python3_sitearch}/samba/gp/vgp_issue_ext.py
%{python3_sitearch}/samba/gp/vgp_motd_ext.py
%{python3_sitearch}/samba/gp/vgp_openssh_ext.py
%{python3_sitearch}/samba/gp/vgp_startup_scripts_ext.py
%{python3_sitearch}/samba/gp/vgp_sudoers_ext.py
%{python3_sitearch}/samba/gp/vgp_symlink_ext.py
%{python3_sitearch}/samba/gpo.*.so
%dir %{python3_sitearch}/samba/gp_parse
%{python3_sitearch}/samba/gp_parse/__init__.py
%dir %{python3_sitearch}/samba/gp_parse/__pycache__
%{python3_sitearch}/samba/gp_parse/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_aas.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_csv.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_inf.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_ini.*.pyc
%{python3_sitearch}/samba/gp_parse/__pycache__/gp_pol.*.pyc
%{python3_sitearch}/samba/gp_parse/gp_aas.py
%{python3_sitearch}/samba/gp_parse/gp_csv.py
%{python3_sitearch}/samba/gp_parse/gp_inf.py
%{python3_sitearch}/samba/gp_parse/gp_ini.py
%{python3_sitearch}/samba/gp_parse/gp_pol.py
%{python3_sitearch}/samba/hresult.*.so
%{python3_sitearch}/samba/logger.py
%{python3_sitearch}/samba/mdb_util.py
%{python3_sitearch}/samba/ms_display_specifiers.py
%{python3_sitearch}/samba/ms_schema.py
%{python3_sitearch}/samba/netbios.*.so
%dir %{python3_sitearch}/samba/netcmd
%{python3_sitearch}/samba/netcmd/__init__.py
%dir %{python3_sitearch}/samba/netcmd/__pycache__
%{python3_sitearch}/samba/netcmd/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/common.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/computer.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/contact.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dbcheck.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/delegation.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dns.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/drs.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/dsacl.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/encoders.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/forest.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/fsmo.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/gpcommon.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/group.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ldapcmp.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/main.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/nettime.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ntacl.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/ou.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/processes.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/pso.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/rodc.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/shell.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/spn.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/testparm.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/validators.*.pyc
%{python3_sitearch}/samba/netcmd/__pycache__/visualize.*.pyc
%{python3_sitearch}/samba/netcmd/common.py
%{python3_sitearch}/samba/netcmd/computer.py
%{python3_sitearch}/samba/netcmd/contact.py
%{python3_sitearch}/samba/netcmd/dbcheck.py
%{python3_sitearch}/samba/netcmd/delegation.py
%dir %{python3_sitearch}/samba/netcmd/domain
%{python3_sitearch}/samba/netcmd/domain/__init__.py
%dir %{python3_sitearch}/samba/netcmd/domain/__pycache__
%{python3_sitearch}/samba/netcmd/domain/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/backup.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/classicupgrade.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/common.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/dcpromo.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/demote.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/functional_prep.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/info.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/join.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/keytab.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/leave.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/level.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/passwordsettings.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/provision.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/samba3upgrade.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/schemaupgrade.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/tombstones.*.pyc
%{python3_sitearch}/samba/netcmd/domain/__pycache__/trust.*.pyc
%dir %{python3_sitearch}/samba/netcmd/domain/auth
%{python3_sitearch}/samba/netcmd/domain/auth/__init__.py
%dir %{python3_sitearch}/samba/netcmd/domain/auth/__pycache__
%{python3_sitearch}/samba/netcmd/domain/auth/__pycache__/__init__.*.pyc
%dir %{python3_sitearch}/samba/netcmd/domain/auth/policy
%{python3_sitearch}/samba/netcmd/domain/auth/policy/computer_allowed_to_authenticate_to.py
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__init__.py
%{python3_sitearch}/samba/netcmd/domain/auth/policy/policy.py
%dir %{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/computer_allowed_to_authenticate_to.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/policy.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/service_allowed_to_authenticate_from.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/service_allowed_to_authenticate_to.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/user_allowed_to_authenticate_from.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/__pycache__/user_allowed_to_authenticate_to.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/policy/service_allowed_to_authenticate_from.py
%{python3_sitearch}/samba/netcmd/domain/auth/policy/service_allowed_to_authenticate_to.py
%{python3_sitearch}/samba/netcmd/domain/auth/policy/user_allowed_to_authenticate_from.py
%{python3_sitearch}/samba/netcmd/domain/auth/policy/user_allowed_to_authenticate_to.py
%dir %{python3_sitearch}/samba/netcmd/domain/auth/silo
%{python3_sitearch}/samba/netcmd/domain/auth/silo/__init__.py
%{python3_sitearch}/samba/netcmd/domain/auth/silo/member.py
%dir %{python3_sitearch}/samba/netcmd/domain/auth/silo/__pycache__
%{python3_sitearch}/samba/netcmd/domain/auth/silo/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/silo/__pycache__/member.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/silo/__pycache__/silo.*.pyc
%{python3_sitearch}/samba/netcmd/domain/auth/silo/silo.py
%{python3_sitearch}/samba/netcmd/domain/backup.py
%dir %{python3_sitearch}/samba/netcmd/domain/claim
%{python3_sitearch}/samba/netcmd/domain/claim/__init__.py
%dir %{python3_sitearch}/samba/netcmd/domain/claim/__pycache__
%{python3_sitearch}/samba/netcmd/domain/claim/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/domain/claim/__pycache__/claim_type.*.pyc
%{python3_sitearch}/samba/netcmd/domain/claim/__pycache__/value_type.*.pyc
%{python3_sitearch}/samba/netcmd/domain/claim/claim_type.py
%{python3_sitearch}/samba/netcmd/domain/claim/value_type.py
%{python3_sitearch}/samba/netcmd/domain/classicupgrade.py
%{python3_sitearch}/samba/netcmd/domain/common.py
%{python3_sitearch}/samba/netcmd/domain/dcpromo.py
%{python3_sitearch}/samba/netcmd/domain/demote.py
%{python3_sitearch}/samba/netcmd/domain/functional_prep.py
%{python3_sitearch}/samba/netcmd/domain/info.py
%{python3_sitearch}/samba/netcmd/domain/join.py
%dir %{python3_sitearch}/samba/netcmd/domain/kds
%{python3_sitearch}/samba/netcmd/domain/kds/__init__.py
%dir %{python3_sitearch}/samba/netcmd/domain/kds/__pycache__
%{python3_sitearch}/samba/netcmd/domain/kds/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/domain/kds/__pycache__/root_key.*.pyc
%{python3_sitearch}/samba/netcmd/domain/kds/root_key.py
%{python3_sitearch}/samba/netcmd/domain/keytab.py
%{python3_sitearch}/samba/netcmd/domain/leave.py
%{python3_sitearch}/samba/netcmd/domain/level.py
%{python3_sitearch}/samba/netcmd/domain/passwordsettings.py
%{python3_sitearch}/samba/netcmd/domain/provision.py
%{python3_sitearch}/samba/netcmd/domain/samba3upgrade.py
%{python3_sitearch}/samba/netcmd/domain/schemaupgrade.py
%{python3_sitearch}/samba/netcmd/domain/tombstones.py
%{python3_sitearch}/samba/netcmd/domain/trust.py
%{python3_sitearch}/samba/netcmd/dns.py
%{python3_sitearch}/samba/netcmd/drs.py
%{python3_sitearch}/samba/netcmd/dsacl.py
%{python3_sitearch}/samba/netcmd/encoders.py
%{python3_sitearch}/samba/netcmd/forest.py
%{python3_sitearch}/samba/netcmd/fsmo.py
%{python3_sitearch}/samba/netcmd/gpcommon.py
%{python3_sitearch}/samba/netcmd/gpo.py
%{python3_sitearch}/samba/netcmd/group.py
%{python3_sitearch}/samba/netcmd/ldapcmp.py
%{python3_sitearch}/samba/netcmd/main.py
%{python3_sitearch}/samba/netcmd/nettime.py
%{python3_sitearch}/samba/netcmd/ntacl.py
%{python3_sitearch}/samba/netcmd/ou.py
%{python3_sitearch}/samba/netcmd/processes.py
%{python3_sitearch}/samba/netcmd/pso.py
%{python3_sitearch}/samba/netcmd/rodc.py
%{python3_sitearch}/samba/netcmd/schema.py
%dir %{python3_sitearch}/samba/netcmd/service_account
%{python3_sitearch}/samba/netcmd/service_account/__init__.py
%{python3_sitearch}/samba/netcmd/service_account/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/service_account/__pycache__/group_msa_membership.*.pyc
%{python3_sitearch}/samba/netcmd/service_account/__pycache__/service_account.*.pyc
%{python3_sitearch}/samba/netcmd/service_account/group_msa_membership.py
%{python3_sitearch}/samba/netcmd/service_account/service_account.py
%{python3_sitearch}/samba/netcmd/shell.py
%{python3_sitearch}/samba/netcmd/sites.py
%{python3_sitearch}/samba/netcmd/spn.py
%{python3_sitearch}/samba/netcmd/testparm.py
%dir %{python3_sitearch}/samba/netcmd/user
%{python3_sitearch}/samba/netcmd/user/__init__.py
%{python3_sitearch}/samba/netcmd/user/add.py
%{python3_sitearch}/samba/netcmd/user/add_unix_attrs.py
%dir %{python3_sitearch}/samba/netcmd/user/auth
%{python3_sitearch}/samba/netcmd/user/auth/__init__.py
%{python3_sitearch}/samba/netcmd/user/auth/policy.py
%dir %{python3_sitearch}/samba/netcmd/user/auth/__pycache__
%{python3_sitearch}/samba/netcmd/user/auth/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/user/auth/__pycache__/policy.*.pyc
%{python3_sitearch}/samba/netcmd/user/auth/__pycache__/silo.*.pyc
%{python3_sitearch}/samba/netcmd/user/auth/silo.py
%{python3_sitearch}/samba/netcmd/user/delete.py
%{python3_sitearch}/samba/netcmd/user/disable.py
%{python3_sitearch}/samba/netcmd/user/edit.py
%{python3_sitearch}/samba/netcmd/user/enable.py
%{python3_sitearch}/samba/netcmd/user/getgroups.py
%{python3_sitearch}/samba/netcmd/user/list.py
%{python3_sitearch}/samba/netcmd/user/move.py
%{python3_sitearch}/samba/netcmd/user/password.py
%dir %{python3_sitearch}/samba/netcmd/user/__pycache__
%{python3_sitearch}/samba/netcmd/user/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/add.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/add_unix_attrs.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/delete.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/disable.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/edit.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/enable.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/getgroups.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/list.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/move.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/password.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/rename.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/sensitive.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/setexpiry.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/setpassword.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/setprimarygroup.*.pyc
%{python3_sitearch}/samba/netcmd/user/__pycache__/unlock.*.pyc
%dir %{python3_sitearch}/samba/netcmd/user/readpasswords
%{python3_sitearch}/samba/netcmd/user/readpasswords/common.py
%{python3_sitearch}/samba/netcmd/user/readpasswords/get_kerberos_ticket.py
%{python3_sitearch}/samba/netcmd/user/readpasswords/getpassword.py
%{python3_sitearch}/samba/netcmd/user/readpasswords/__init__.py
%dir %{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/common.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/get_kerberos_ticket.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/getpassword.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/show.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/__pycache__/syncpasswords.*.pyc
%{python3_sitearch}/samba/netcmd/user/readpasswords/show.py
%{python3_sitearch}/samba/netcmd/user/readpasswords/syncpasswords.py
%{python3_sitearch}/samba/netcmd/user/rename.py
%{python3_sitearch}/samba/netcmd/user/sensitive.py
%{python3_sitearch}/samba/netcmd/user/setexpiry.py
%{python3_sitearch}/samba/netcmd/user/setpassword.py
%{python3_sitearch}/samba/netcmd/user/setprimarygroup.py
%{python3_sitearch}/samba/netcmd/user/unlock.py
%{python3_sitearch}/samba/netcmd/validators.py
%{python3_sitearch}/samba/netcmd/visualize.py
%{python3_sitearch}/samba/ntacls.py
%{python3_sitearch}/samba/nt_time.py
%{python3_sitearch}/samba/param.*.so
%{python3_sitearch}/samba/policies.py
%{python3_sitearch}/samba/policy.*.so
%{python3_sitearch}/samba/registry.*.so
%{python3_sitearch}/samba/reparse_symlink.*.so
%{python3_sitearch}/samba/security.*.so
%{python3_sitearch}/samba/safe_tarfile.py
%dir %{python3_sitearch}/samba/samba3
%{python3_sitearch}/samba/samba3/__init__.py
%dir %{python3_sitearch}/samba/samba3/__pycache__
%{python3_sitearch}/samba/samba3/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/samba3/__pycache__/libsmb_samba_internal.*.pyc
%{python3_sitearch}/samba/samba3/libsmb_samba_cwrapper.cpython*.so
%{python3_sitearch}/samba/samba3/libsmb_samba_internal.py
%{python3_sitearch}/samba/samba3/mdscli.*.so
%{python3_sitearch}/samba/samba3/param.*.so
%{python3_sitearch}/samba/samba3/passdb.*.so
%{python3_sitearch}/samba/samba3/smbconf.*.so
%{python3_sitearch}/samba/samba3/smbd.*.so
%{python3_sitearch}/samba/sd_utils.py
%{python3_sitearch}/samba/sites.py
%{python3_sitearch}/samba/smbconf.*.so
%{python3_sitearch}/samba/subnets.py
%dir %{python3_sitearch}/samba/subunit
%{python3_sitearch}/samba/subunit/__init__.py
%dir %{python3_sitearch}/samba/subunit/__pycache__
%{python3_sitearch}/samba/subunit/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/subunit/__pycache__/run.*.pyc
%{python3_sitearch}/samba/subunit/run.py
%{python3_sitearch}/samba/tdb_util.py
%{python3_sitearch}/samba/upgrade.py
%{python3_sitearch}/samba/upgradehelpers.py
%{python3_sitearch}/samba/werror.*.so
%{python3_sitearch}/samba/xattr.py
%{python3_sitearch}/samba/xattr_native.*.so
%{python3_sitearch}/samba/xattr_tdb.*.so
%{_libdir}/samba/libsamba-net-join.cpython*.so
%{_libdir}/samba/libsamba-python.cpython*.so

%if %{with includelibs}
%{_libdir}/samba/libpyldb-util.cpython*.so

%{python3_sitearch}/__pycache__/_ldb_text*.pyc
%{python3_sitearch}/__pycache__/_tdb_text*.pyc
%{python3_sitearch}/__pycache__/tevent*.pyc
%{python3_sitearch}/_ldb_text.py
%{python3_sitearch}/_tdb_text.py
%{python3_sitearch}/_tevent.cpython*.so
%{python3_sitearch}/ldb.cpython*.so
#FIXME why is it missing?
#%{python3_sitearch}/talloc.cpython*.so
%{python3_sitearch}/tdb.cpython*.so
%{python3_sitearch}/tevent.py
#endif with includelibs
%endif

%files -n python3-%{name}-dc
%{python3_sitearch}/samba/samdb.py
%{python3_sitearch}/samba/schema.py

%{python3_sitearch}/samba/__pycache__/domain_update.*.pyc
%{python3_sitearch}/samba/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/samba/__pycache__/forest_update.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_forest_updates_markdown.*.pyc
%{python3_sitearch}/samba/__pycache__/ms_schema_markdown.*.pyc
%{python3_sitearch}/samba/__pycache__/remove_dc.*.pyc
%{python3_sitearch}/samba/__pycache__/samdb.*.pyc
%{python3_sitearch}/samba/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/__pycache__/uptodateness.*.pyc

%{python3_sitearch}/samba/dcerpc/dnsserver.*.so
%if %{with dc}
%{python3_sitearch}/samba/dckeytab.*.so
%endif
%{python3_sitearch}/samba/domain_update.py
%{python3_sitearch}/samba/forest_update.py
%{python3_sitearch}/samba/ms_forest_updates_markdown.py
%{python3_sitearch}/samba/ms_schema_markdown.py

%dir %{python3_sitearch}/samba/kcc
%{python3_sitearch}/samba/kcc/__init__.py
%{python3_sitearch}/samba/kcc/debug.py
%{python3_sitearch}/samba/kcc/graph.py
%{python3_sitearch}/samba/kcc/graph_utils.py
%{python3_sitearch}/samba/kcc/kcc_utils.py
%{python3_sitearch}/samba/kcc/ldif_import_export.py
%{python3_sitearch}/samba/dnsserver.py

%dir %{python3_sitearch}/samba/kcc/__pycache__
%{python3_sitearch}/samba/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/debug.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/samba/kcc/__pycache__/ldif_import_export.*.pyc

%dir %{python3_sitearch}/samba/provision
%{python3_sitearch}/samba/provision/backend.py
%{python3_sitearch}/samba/provision/common.py
%{python3_sitearch}/samba/provision/kerberos.py
%{python3_sitearch}/samba/provision/kerberos_implementation.py
%{python3_sitearch}/samba/provision/sambadns.py

%dir %{python3_sitearch}/samba/provision/__pycache__
%{python3_sitearch}/samba/provision/__init__.py
%{python3_sitearch}/samba/provision/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/backend.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/common.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/kerberos.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/kerberos_implementation.*.pyc
%{python3_sitearch}/samba/provision/__pycache__/sambadns.*.pyc

%{python3_sitearch}/samba/remove_dc.py
%{python3_sitearch}/samba/uptodateness.py

%files -n python3-%{name}-test
%dir %{python3_sitearch}/samba/tests
%{python3_sitearch}/samba/tests/__init__.py
%dir %{python3_sitearch}/samba/tests/__pycache__
%{python3_sitearch}/samba/tests/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_dsdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/audit_log_pass_change.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_pass_change.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_ncalrpc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_netlogon.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_netlogon_bad_creds.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_samlogon.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/auth_log_winbind.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/common.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/complex_expressions.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/compression.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/conditional_ace_assembler.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/conditional_ace_bytes.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/conditional_ace_claims.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/core.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/cred_opt.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dckeytab.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_aging.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_forwarder.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_invalid.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_packet.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_tkey.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dns_wildcard.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_api.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_dns.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_lock.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_quiet_env_tests.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_quiet_provision_tests.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/dsdb_schema_attributes.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/docs.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/domain_backup.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/domain_backup_offline.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/encrypted_secrets.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gensec.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/get_opt.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/getdcname.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gkdi.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/glue.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/gpo_member.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/group_audit.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/hostconfig.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/imports.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/join.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/krb5_credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_raw.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_referrals.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_spn.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_upn_sam_account.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ldap_whoami.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/loadparm.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/logfiles.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/libsmb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/libsmb-basic.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/lsa_string.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/messaging.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netbios.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netcmd.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/net_join_no_spnego.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/net_join.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/netlogonsvc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntacls.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntacls_backup.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlmdisabled.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/ntlm_auth_krb5.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind_chauthtok.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind_setcred.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pam_winbind_warn_pwd_expire.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/param.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_fl2003.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_fl2008.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_gpgme.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_hash_ldap.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_quality.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/password_test.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/policy.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/posixacl.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/prefork_restart.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/process_limits.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/provision.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/pso.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/py_credentials.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/registry.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/reparsepoints.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3idmapdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3param.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3passdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3registry.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3windb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/s3_net_join.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/safe_tarfile.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samba_upgradedns_lmdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samba_startup_fl_change.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samba3sam.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samdb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/samdb_api.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/sddl.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/sddl_conditional_ace.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/security.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/security_descriptors.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/segfault.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/sid_strings.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb1posix.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb2symlink.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb3unix.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smbconf.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smb-notify.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smbd_base.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/smbd_fuzztest.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/source.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/source_chars.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/strings.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/subunitrun.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/tdb_util.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/token_factory.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgrade.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgradeprovision.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/upgradeprovisionneeddc.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/usage.*.pyc
%{python3_sitearch}/samba/tests/__pycache__/xattr.*.pyc
%{python3_sitearch}/samba/tests/audit_log_base.py
%{python3_sitearch}/samba/tests/audit_log_dsdb.py
%{python3_sitearch}/samba/tests/audit_log_pass_change.py
%{python3_sitearch}/samba/tests/auth.py
%{python3_sitearch}/samba/tests/auth_log.py
%{python3_sitearch}/samba/tests/auth_log_base.py
%{python3_sitearch}/samba/tests/auth_log_ncalrpc.py
%{python3_sitearch}/samba/tests/auth_log_netlogon_bad_creds.py
%{python3_sitearch}/samba/tests/auth_log_netlogon.py
%{python3_sitearch}/samba/tests/auth_log_pass_change.py
%{python3_sitearch}/samba/tests/auth_log_samlogon.py
%{python3_sitearch}/samba/tests/auth_log_winbind.py
%dir %{python3_sitearch}/samba/tests/blackbox
%{python3_sitearch}/samba/tests/blackbox/__init__.py
%dir %{python3_sitearch}/samba/tests/blackbox/__pycache__
%{python3_sitearch}/samba/tests/blackbox/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/bug13653.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/check_output.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/claims.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/downgradedatabase.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/gmsa.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/http_chunk.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/http_content.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/mdsearch.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/misc_dfs_widelink.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/ndrdump.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/netads_dns.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/netads_json.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/rpcd_witness_samba_only.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/samba_dnsupdate.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcacls.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcacls_basic.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcacls_dfs_propagate_inherit.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcacls_propagate_inhertance.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcacls_save_restore.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcontrol.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/smbcontrol_process.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_learner.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_replay.*.pyc
%{python3_sitearch}/samba/tests/blackbox/__pycache__/traffic_summary.*.pyc
%{python3_sitearch}/samba/tests/blackbox/bug13653.py
%{python3_sitearch}/samba/tests/blackbox/check_output.py
%{python3_sitearch}/samba/tests/blackbox/claims.py
%{python3_sitearch}/samba/tests/blackbox/downgradedatabase.py
%{python3_sitearch}/samba/tests/blackbox/gmsa.py
%{python3_sitearch}/samba/tests/blackbox/http_chunk.py
%{python3_sitearch}/samba/tests/blackbox/http_content.py
%{python3_sitearch}/samba/tests/blackbox/mdsearch.py
%{python3_sitearch}/samba/tests/blackbox/misc_dfs_widelink.py
%{python3_sitearch}/samba/tests/blackbox/ndrdump.py
%{python3_sitearch}/samba/tests/blackbox/netads_dns.py
%{python3_sitearch}/samba/tests/blackbox/netads_json.py
%{python3_sitearch}/samba/tests/blackbox/rpcd_witness_samba_only.py
%{python3_sitearch}/samba/tests/blackbox/samba_dnsupdate.py
%{python3_sitearch}/samba/tests/blackbox/smbcacls.py
%{python3_sitearch}/samba/tests/blackbox/smbcacls_basic.py
%{python3_sitearch}/samba/tests/blackbox/smbcacls_dfs_propagate_inherit.py
%{python3_sitearch}/samba/tests/blackbox/smbcacls_propagate_inhertance.py
%{python3_sitearch}/samba/tests/blackbox/smbcacls_save_restore.py
%{python3_sitearch}/samba/tests/blackbox/smbcontrol.py
%{python3_sitearch}/samba/tests/blackbox/smbcontrol_process.py
%{python3_sitearch}/samba/tests/blackbox/traffic_learner.py
%{python3_sitearch}/samba/tests/blackbox/traffic_replay.py
%{python3_sitearch}/samba/tests/blackbox/traffic_summary.py
%{python3_sitearch}/samba/tests/common.py
%{python3_sitearch}/samba/tests/compression.py
%{python3_sitearch}/samba/tests/complex_expressions.py
%{python3_sitearch}/samba/tests/conditional_ace_assembler.py
%{python3_sitearch}/samba/tests/conditional_ace_bytes.py
%{python3_sitearch}/samba/tests/conditional_ace_claims.py
%{python3_sitearch}/samba/tests/core.py
%{python3_sitearch}/samba/tests/credentials.py
%{python3_sitearch}/samba/tests/cred_opt.py
%dir %{python3_sitearch}/samba/tests/dcerpc
%{python3_sitearch}/samba/tests/dcerpc/__init__.py
%dir %{python3_sitearch}/samba/tests/dcerpc/__pycache__
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/array.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/bare.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/binding.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/dnsserver.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/integer.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/lsa.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/lsa_utils.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/mdssvc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/misc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/raw_protocol.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/raw_testcase.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/registry.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/rpc_talloc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/rpcecho.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/sam.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/samr_change_password.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/srvsvc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/string_tests.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/testrpc.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/__pycache__/unix.*.pyc
%{python3_sitearch}/samba/tests/dcerpc/array.py
%{python3_sitearch}/samba/tests/dcerpc/bare.py
%{python3_sitearch}/samba/tests/dcerpc/binding.py
%{python3_sitearch}/samba/tests/dcerpc/dnsserver.py
%{python3_sitearch}/samba/tests/dcerpc/integer.py
%{python3_sitearch}/samba/tests/dcerpc/lsa.py
%{python3_sitearch}/samba/tests/dcerpc/lsa_utils.py
%{python3_sitearch}/samba/tests/dcerpc/mdssvc.py
%{python3_sitearch}/samba/tests/dcerpc/misc.py
%{python3_sitearch}/samba/tests/dcerpc/raw_protocol.py
%{python3_sitearch}/samba/tests/dcerpc/raw_testcase.py
%{python3_sitearch}/samba/tests/dcerpc/registry.py
%{python3_sitearch}/samba/tests/dcerpc/rpc_talloc.py
%{python3_sitearch}/samba/tests/dcerpc/rpcecho.py
%{python3_sitearch}/samba/tests/dcerpc/sam.py
%{python3_sitearch}/samba/tests/dcerpc/samr_change_password.py
%{python3_sitearch}/samba/tests/dcerpc/srvsvc.py
%{python3_sitearch}/samba/tests/dcerpc/string_tests.py
%{python3_sitearch}/samba/tests/dcerpc/testrpc.py
%{python3_sitearch}/samba/tests/dcerpc/unix.py
%{python3_sitearch}/samba/tests/dckeytab.py
%{python3_sitearch}/samba/tests/dns.py
%{python3_sitearch}/samba/tests/dns_aging.py
%{python3_sitearch}/samba/tests/dns_base.py
%{python3_sitearch}/samba/tests/dns_forwarder.py
%dir %{python3_sitearch}/samba/tests/dns_forwarder_helpers
%{python3_sitearch}/samba/tests/dns_forwarder_helpers/__pycache__/server.*.pyc
%{python3_sitearch}/samba/tests/dns_forwarder_helpers/server.py
%{python3_sitearch}/samba/tests/dns_invalid.py
%{python3_sitearch}/samba/tests/dns_packet.py
%{python3_sitearch}/samba/tests/dns_tkey.py
%{python3_sitearch}/samba/tests/dns_wildcard.py
%{python3_sitearch}/samba/tests/dsdb.py
%{python3_sitearch}/samba/tests/dsdb_api.py
%{python3_sitearch}/samba/tests/dsdb_dns.py
%{python3_sitearch}/samba/tests/dsdb_lock.py
%{python3_sitearch}/samba/tests/dsdb_schema_attributes.py
%{python3_sitearch}/samba/tests/dsdb_quiet_env_tests.py
%{python3_sitearch}/samba/tests/dsdb_quiet_provision_tests.py
%{python3_sitearch}/samba/tests/docs.py
%{python3_sitearch}/samba/tests/domain_backup.py
%{python3_sitearch}/samba/tests/domain_backup_offline.py
%dir %{python3_sitearch}/samba/tests/emulate
%{python3_sitearch}/samba/tests/emulate/__init__.py
%dir %{python3_sitearch}/samba/tests/emulate/__pycache__
%{python3_sitearch}/samba/tests/emulate/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/emulate/__pycache__/traffic.*.pyc
%{python3_sitearch}/samba/tests/emulate/__pycache__/traffic_packet.*.pyc
%{python3_sitearch}/samba/tests/emulate/traffic.py
%{python3_sitearch}/samba/tests/emulate/traffic_packet.py
%{python3_sitearch}/samba/tests/encrypted_secrets.py
%{python3_sitearch}/samba/tests/gensec.py
%{python3_sitearch}/samba/tests/getdcname.py
%{python3_sitearch}/samba/tests/get_opt.py
%{python3_sitearch}/samba/tests/gkdi.py
%{python3_sitearch}/samba/tests/glue.py
%{python3_sitearch}/samba/tests/gpo.py
%{python3_sitearch}/samba/tests/gpo_member.py
%{python3_sitearch}/samba/tests/graph.py
%{python3_sitearch}/samba/tests/group_audit.py
%{python3_sitearch}/samba/tests/hostconfig.py
%{python3_sitearch}/samba/tests/imports.py
%{python3_sitearch}/samba/tests/join.py
%dir %{python3_sitearch}/samba/tests/kcc
%{python3_sitearch}/samba/tests/kcc/__init__.py
%dir %{python3_sitearch}/samba/tests/kcc/__pycache__
%{python3_sitearch}/samba/tests/kcc/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/graph.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/graph_utils.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/kcc_utils.*.pyc
%{python3_sitearch}/samba/tests/kcc/__pycache__/ldif_import_export.*.pyc
%{python3_sitearch}/samba/tests/kcc/graph.py
%{python3_sitearch}/samba/tests/kcc/graph_utils.py
%{python3_sitearch}/samba/tests/kcc/kcc_utils.py
%{python3_sitearch}/samba/tests/kcc/ldif_import_export.py
%dir %{python3_sitearch}/samba/tests/krb5
%dir %{python3_sitearch}/samba/tests/krb5/__pycache__
%{python3_sitearch}/samba/tests/krb5/__pycache__/alias_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/as_canonicalization_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/as_req_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/authn_policy_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/claims_in_pac.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/claims_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/compatability_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/conditional_ace_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/device_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/etype_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/fast_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/gkdi_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/gmsa_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/group_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kcrypto.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kdc_base_test.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kdc_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kdc_tgs_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kdc_tgt_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/kpasswd_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/lockout_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/ms_kile_client_principal_lookup_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/nt_hash_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/pac_align_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/pkinit_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/protected_users_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/raw_testcase.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/rfc4120_constants.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/rfc4120_pyasn1.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/rfc4120_pyasn1_generated.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/rodc_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/simple_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/s4u_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/salt_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/spn_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_ccache.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_idmap_nss.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_ldap.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_min_domain_uid.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_rpc.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/test_smb.*.pyc
%{python3_sitearch}/samba/tests/krb5/__pycache__/xrealm_tests.*.pyc
%{python3_sitearch}/samba/tests/krb5/alias_tests.py
%{python3_sitearch}/samba/tests/krb5/as_canonicalization_tests.py
%{python3_sitearch}/samba/tests/krb5/as_req_tests.py
%{python3_sitearch}/samba/tests/krb5/authn_policy_tests.py
%{python3_sitearch}/samba/tests/krb5/claims_in_pac.py
%{python3_sitearch}/samba/tests/krb5/claims_tests.py
%{python3_sitearch}/samba/tests/krb5/compatability_tests.py
%{python3_sitearch}/samba/tests/krb5/conditional_ace_tests.py
%{python3_sitearch}/samba/tests/krb5/device_tests.py
%{python3_sitearch}/samba/tests/krb5/etype_tests.py
%{python3_sitearch}/samba/tests/krb5/fast_tests.py
%{python3_sitearch}/samba/tests/krb5/gkdi_tests.py
%{python3_sitearch}/samba/tests/krb5/gmsa_tests.py
%{python3_sitearch}/samba/tests/krb5/group_tests.py
%{python3_sitearch}/samba/tests/krb5/kcrypto.py
%{python3_sitearch}/samba/tests/krb5/kdc_base_test.py
%{python3_sitearch}/samba/tests/krb5/kdc_tests.py
%{python3_sitearch}/samba/tests/krb5/kdc_tgs_tests.py
%{python3_sitearch}/samba/tests/krb5/kdc_tgt_tests.py
%{python3_sitearch}/samba/tests/krb5/kpasswd_tests.py
%{python3_sitearch}/samba/tests/krb5/lockout_tests.py
%{python3_sitearch}/samba/tests/krb5/ms_kile_client_principal_lookup_tests.py
%{python3_sitearch}/samba/tests/krb5/nt_hash_tests.py
%{python3_sitearch}/samba/tests/krb5/pac_align_tests.py
%{python3_sitearch}/samba/tests/krb5/pkinit_tests.py
%{python3_sitearch}/samba/tests/krb5/protected_users_tests.py
%{python3_sitearch}/samba/tests/krb5/raw_testcase.py
%{python3_sitearch}/samba/tests/krb5/rfc4120_constants.py
%{python3_sitearch}/samba/tests/krb5/rfc4120_pyasn1.py
%{python3_sitearch}/samba/tests/krb5/rfc4120_pyasn1_generated.py
%{python3_sitearch}/samba/tests/krb5/rodc_tests.py
%{python3_sitearch}/samba/tests/krb5/simple_tests.py
%{python3_sitearch}/samba/tests/krb5/test_idmap_nss.py
%{python3_sitearch}/samba/tests/krb5/test_ccache.py
%{python3_sitearch}/samba/tests/krb5/test_ldap.py
%{python3_sitearch}/samba/tests/krb5/test_min_domain_uid.py
%{python3_sitearch}/samba/tests/krb5/test_rpc.py
%{python3_sitearch}/samba/tests/krb5/test_smb.py
%{python3_sitearch}/samba/tests/krb5/s4u_tests.py
%{python3_sitearch}/samba/tests/krb5/salt_tests.py
%{python3_sitearch}/samba/tests/krb5/spn_tests.py
%{python3_sitearch}/samba/tests/krb5/xrealm_tests.py
%{python3_sitearch}/samba/tests/krb5_credentials.py
%{python3_sitearch}/samba/tests/ldap_raw.py
%{python3_sitearch}/samba/tests/ldap_spn.py
%{python3_sitearch}/samba/tests/ldap_referrals.py
%{python3_sitearch}/samba/tests/ldap_upn_sam_account.py
%{python3_sitearch}/samba/tests/ldap_whoami.py
%{python3_sitearch}/samba/tests/libsmb.py
%{python3_sitearch}/samba/tests/libsmb-basic.py
%{python3_sitearch}/samba/tests/loadparm.py
%{python3_sitearch}/samba/tests/logfiles.py
%{python3_sitearch}/samba/tests/lsa_string.py
%{python3_sitearch}/samba/tests/messaging.py
%dir %{python3_sitearch}/samba/tests/ndr
%{python3_sitearch}/samba/tests/ndr/gkdi.py
%{python3_sitearch}/samba/tests/ndr/gmsa.py
%dir %{python3_sitearch}/samba/tests/ndr/__pycache__
%{python3_sitearch}/samba/tests/ndr/__pycache__/gkdi.*.pyc
%{python3_sitearch}/samba/tests/ndr/__pycache__/gmsa.*.pyc
%{python3_sitearch}/samba/tests/ndr/__pycache__/wbint.*.pyc
%{python3_sitearch}/samba/tests/ndr/wbint.py
%{python3_sitearch}/samba/tests/netbios.py
%{python3_sitearch}/samba/tests/netcmd.py
%{python3_sitearch}/samba/tests/net_join_no_spnego.py
%{python3_sitearch}/samba/tests/net_join.py
%{python3_sitearch}/samba/tests/netlogonsvc.py
%{python3_sitearch}/samba/tests/ntacls.py
%{python3_sitearch}/samba/tests/ntacls_backup.py
%{python3_sitearch}/samba/tests/ntlmdisabled.py
%{python3_sitearch}/samba/tests/ntlm_auth.py
%{python3_sitearch}/samba/tests/ntlm_auth_base.py
%{python3_sitearch}/samba/tests/ntlm_auth_krb5.py
%{python3_sitearch}/samba/tests/pam_winbind.py
%{python3_sitearch}/samba/tests/pam_winbind_chauthtok.py
%{python3_sitearch}/samba/tests/pam_winbind_setcred.py
%{python3_sitearch}/samba/tests/pam_winbind_warn_pwd_expire.py
%{python3_sitearch}/samba/tests/param.py
%{python3_sitearch}/samba/tests/password_hash.py
%{python3_sitearch}/samba/tests/password_hash_fl2003.py
%{python3_sitearch}/samba/tests/password_hash_fl2008.py
%{python3_sitearch}/samba/tests/password_hash_gpgme.py
%{python3_sitearch}/samba/tests/password_hash_ldap.py
%{python3_sitearch}/samba/tests/password_quality.py
%{python3_sitearch}/samba/tests/password_test.py
%{python3_sitearch}/samba/tests/policy.py
%{python3_sitearch}/samba/tests/posixacl.py
%{python3_sitearch}/samba/tests/prefork_restart.py
%{python3_sitearch}/samba/tests/process_limits.py
%{python3_sitearch}/samba/tests/provision.py
%{python3_sitearch}/samba/tests/pso.py
%{python3_sitearch}/samba/tests/py_credentials.py
%{python3_sitearch}/samba/tests/registry.py
%{python3_sitearch}/samba/tests/reparsepoints.py
%{python3_sitearch}/samba/tests/s3idmapdb.py
%{python3_sitearch}/samba/tests/s3param.py
%{python3_sitearch}/samba/tests/s3passdb.py
%{python3_sitearch}/samba/tests/s3registry.py
%{python3_sitearch}/samba/tests/s3windb.py
%{python3_sitearch}/samba/tests/s3_net_join.py
%{python3_sitearch}/samba/tests/safe_tarfile.py
%{python3_sitearch}/samba/tests/samba3sam.py
%{python3_sitearch}/samba/tests/samba_startup_fl_change.py
%{python3_sitearch}/samba/tests/samba_upgradedns_lmdb.py
%dir %{python3_sitearch}/samba/tests/samba_tool
%{python3_sitearch}/samba/tests/samba_tool/__init__.py
%dir %{python3_sitearch}/samba/tests/samba_tool/__pycache__
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/__init__.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/base.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/computer.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/contact.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/demote.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/dnscmd.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/domain_auth_policy.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/domain_auth_silo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/domain_claim.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/domain_kds_root_key.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/domain_models.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/drs_clone_dc_data_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/dsacl.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/forest.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/fsmo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/gpo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/gpo_exts.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/group.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/help.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/join.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/join_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/join_member.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/ntacl.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/ou.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/passwordsettings.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/processes.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/promote_dc_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/provision_lmdb_size.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/provision_password_check.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/provision_userPassword_crypt.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/rodc.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/schema.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/service_account.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/silo_base.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/sites.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/timecmd.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_auth_policy.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_auth_silo.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_check_password_script.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_get_kerberos_ticket.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_getpassword_gmsa.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_base.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_gpg.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_virtualCryptSHA_userPassword.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/user_wdigest.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/visualize.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/__pycache__/visualize_drs.*.pyc
%{python3_sitearch}/samba/tests/samba_tool/base.py
%{python3_sitearch}/samba/tests/samba_tool/computer.py
%{python3_sitearch}/samba/tests/samba_tool/contact.py
%{python3_sitearch}/samba/tests/samba_tool/demote.py
%{python3_sitearch}/samba/tests/samba_tool/dnscmd.py
%{python3_sitearch}/samba/tests/samba_tool/domain_auth_policy.py
%{python3_sitearch}/samba/tests/samba_tool/domain_auth_silo.py
%{python3_sitearch}/samba/tests/samba_tool/domain_claim.py
%{python3_sitearch}/samba/tests/samba_tool/domain_kds_root_key.py
%{python3_sitearch}/samba/tests/samba_tool/domain_models.py
%{python3_sitearch}/samba/tests/samba_tool/drs_clone_dc_data_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/dsacl.py
%{python3_sitearch}/samba/tests/samba_tool/forest.py
%{python3_sitearch}/samba/tests/samba_tool/fsmo.py
%{python3_sitearch}/samba/tests/samba_tool/gpo.py
%{python3_sitearch}/samba/tests/samba_tool/gpo_exts.py
%{python3_sitearch}/samba/tests/samba_tool/group.py
%{python3_sitearch}/samba/tests/samba_tool/help.py
%{python3_sitearch}/samba/tests/samba_tool/join.py
%{python3_sitearch}/samba/tests/samba_tool/join_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/join_member.py
%{python3_sitearch}/samba/tests/samba_tool/ntacl.py
%{python3_sitearch}/samba/tests/samba_tool/ou.py
%{python3_sitearch}/samba/tests/samba_tool/passwordsettings.py
%{python3_sitearch}/samba/tests/samba_tool/processes.py
%{python3_sitearch}/samba/tests/samba_tool/promote_dc_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/provision_lmdb_size.py
%{python3_sitearch}/samba/tests/samba_tool/provision_password_check.py
%{python3_sitearch}/samba/tests/samba_tool/provision_userPassword_crypt.py
%{python3_sitearch}/samba/tests/samba_tool/rodc.py
%{python3_sitearch}/samba/tests/samba_tool/schema.py
%{python3_sitearch}/samba/tests/samba_tool/service_account.py
%{python3_sitearch}/samba/tests/samba_tool/silo_base.py
%{python3_sitearch}/samba/tests/samba_tool/sites.py
%{python3_sitearch}/samba/tests/samba_tool/timecmd.py
%{python3_sitearch}/samba/tests/samba_tool/user.py
%{python3_sitearch}/samba/tests/samba_tool/user_auth_policy.py
%{python3_sitearch}/samba/tests/samba_tool/user_auth_silo.py
%{python3_sitearch}/samba/tests/samba_tool/user_check_password_script.py
%{python3_sitearch}/samba/tests/samba_tool/user_get_kerberos_ticket.py
%{python3_sitearch}/samba/tests/samba_tool/user_getpassword_gmsa.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_base.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_gpg.py
%{python3_sitearch}/samba/tests/samba_tool/user_virtualCryptSHA_userPassword.py
%{python3_sitearch}/samba/tests/samba_tool/user_wdigest.py
%{python3_sitearch}/samba/tests/samba_tool/visualize.py
%{python3_sitearch}/samba/tests/samba_tool/visualize_drs.py
%{python3_sitearch}/samba/tests/samdb.py
%{python3_sitearch}/samba/tests/samdb_api.py
%{python3_sitearch}/samba/tests/sddl.py
%{python3_sitearch}/samba/tests/sddl_conditional_ace.py
%{python3_sitearch}/samba/tests/security.py
%{python3_sitearch}/samba/tests/security_descriptors.py
%{python3_sitearch}/samba/tests/segfault.py
%{python3_sitearch}/samba/tests/sid_strings.py
%{python3_sitearch}/samba/tests/smb.py
%{python3_sitearch}/samba/tests/smb1posix.py
%{python3_sitearch}/samba/tests/smb2symlink.py
%{python3_sitearch}/samba/tests/smb3unix.py
%{python3_sitearch}/samba/tests/smbconf.py
%{python3_sitearch}/samba/tests/smb-notify.py
%{python3_sitearch}/samba/tests/smbd_base.py
%{python3_sitearch}/samba/tests/smbd_fuzztest.py
%{python3_sitearch}/samba/tests/source.py
%{python3_sitearch}/samba/tests/source_chars.py
%{python3_sitearch}/samba/tests/strings.py
%{python3_sitearch}/samba/tests/subunitrun.py
%{python3_sitearch}/samba/tests/tdb_util.py
%{python3_sitearch}/samba/tests/token_factory.py
%{python3_sitearch}/samba/tests/upgrade.py
%{python3_sitearch}/samba/tests/upgradeprovision.py
%{python3_sitearch}/samba/tests/upgradeprovisionneeddc.py
%{python3_sitearch}/samba/tests/usage.py
%{python3_sitearch}/samba/tests/xattr.py

### TEST
%files test
%{_bindir}/gentest
%{_bindir}/locktest
%{_bindir}/masktest
%{_bindir}/ndrdump
%{_bindir}/smbtorture
%{_mandir}/man1/gentest.1*
%{_mandir}/man1/locktest.1*
%{_mandir}/man1/masktest.1*
%{_mandir}/man1/ndrdump.1*
%{_mandir}/man1/smbtorture.1*

### TEST-LIBS
%files test-libs
%if %{with dc}
%{_libdir}/samba/libdlz-bind9-for-torture-private-samba.so
%endif
%{_libdir}/samba/libdsdb-module-private-samba.so

### USERSHARES
%files usershares
%config(noreplace) %{_sysconfdir}/samba/usershares.conf
%attr(1770,root,usershares) %dir /var/lib/samba/usershares
%{_sysusersdir}/samba-usershares.conf

### WINBIND
%files winbind
%{_libdir}/samba/idmap
%{_libdir}/samba/nss_info
%{_libdir}/samba/libnss-info-private-samba.so
%{_libdir}/samba/libidmap-private-samba.so
%{_sbindir}/winbindd
%{_sysusersdir}/samba-winbind.conf
%attr(750,root,wbpriv) %dir /var/lib/samba/winbindd_privileged
%{_unitdir}/winbind.service
%{_prefix}/lib/NetworkManager
%{_mandir}/man8/winbindd.8*
%{_mandir}/man8/idmap_*.8*

### WINBIND-CLIENTS
%files winbind-clients
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_libdir}/samba/krb5/winbind_krb5_localauth.so
%{_mandir}/man1/ntlm_auth.1.gz
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man8/winbind_krb5_localauth.8*

### WINBIND-KRB5-LOCATOR
%files winbind-krb5-locator
%ghost %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
%dir %{_libdir}/samba/krb5
%{_libdir}/samba/krb5/winbind_krb5_locator.so
# correct rpm package?
%{_libdir}/samba/krb5/async_dns_krb5_locator.so
%{_mandir}/man8/winbind_krb5_locator.8*

### WINBIND-MODULES
%files winbind-modules
%{_libdir}/libnss_winbind.so*
%{_libdir}/libnss_wins.so*
%{_libdir}/security/pam_winbind.so
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf
%{_mandir}/man5/pam_winbind.conf.5*
%{_mandir}/man8/pam_winbind.8*

%if %{with clustering}
%files -n ctdb
%doc ctdb/README
%doc ctdb/doc/examples
# Obsolete
%config(noreplace, missingok) %{_sysconfdir}/sysconfig/ctdb

%dir %{_sysconfdir}/ctdb
%config(noreplace) %{_sysconfdir}/ctdb/ctdb.conf
%config(noreplace) %{_sysconfdir}/ctdb/notify.sh
%config(noreplace) %{_sysconfdir}/ctdb/debug-hung-script.sh
%config(noreplace) %{_sysconfdir}/ctdb/ctdb-crash-cleanup.sh
%config(noreplace) %{_sysconfdir}/ctdb/debug_locks.sh

%{_sysconfdir}/ctdb/functions
%{_sysconfdir}/ctdb/nfs-linux-kernel-callout
%ghost %{_sysconfdir}/ctdb/statd-callout

# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/events
%dir %{_sysconfdir}/ctdb/events/legacy
%dir %{_sysconfdir}/ctdb/events/notification
%{_sysconfdir}/ctdb/events/notification/README

# CTDB scripts, no config files
# script with executable bit means activated
%dir %{_sysconfdir}/ctdb/nfs-checks.d
%{_sysconfdir}/ctdb/nfs-checks.d/README
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/00.portmapper.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/10.status.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/20.nfs.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/30.nlockmgr.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/40.mountd.check
%config(noreplace) %{_sysconfdir}/ctdb/nfs-checks.d/50.rquotad.check

%{_sbindir}/ctdbd
%{_bindir}/ctdb
%{_bindir}/ctdb_diagnostics
%{_bindir}/ltdbtool
%{_bindir}/onnode
%{_bindir}/ping_pong

%dir %{_libexecdir}/ctdb
%{_libexecdir}/ctdb/ctdb-config
%{_libexecdir}/ctdb/ctdb-event
%{_libexecdir}/ctdb/ctdb-eventd
%{_libexecdir}/ctdb/ctdb_killtcp
%{_libexecdir}/ctdb/ctdb_lock_helper
%{_libexecdir}/ctdb/ctdb_lvs
%{_libexecdir}/ctdb/ctdb_mutex_fcntl_helper
%{_libexecdir}/ctdb/ctdb_natgw
%{_libexecdir}/ctdb/ctdb-path
%{_libexecdir}/ctdb/ctdb_recovery_helper
%{_libexecdir}/ctdb/ctdb_takeover_helper
%{_libexecdir}/ctdb/smnotify
%{_libexecdir}/ctdb/statd_callout
%{_libexecdir}/ctdb/statd_callout_helper
%{_libexecdir}/ctdb/tdb_mutex_check

%dir %{_localstatedir}/lib/ctdb/
%dir %{_localstatedir}/lib/ctdb/persistent
%dir %{_localstatedir}/lib/ctdb/state
%dir %{_localstatedir}/lib/ctdb/volatile

%{_mandir}/man1/ctdb.1.gz
%{_mandir}/man1/ctdb_diagnostics.1.gz
%{_mandir}/man1/ctdbd.1.gz
%{_mandir}/man1/onnode.1.gz
%{_mandir}/man1/ltdbtool.1.gz
%{_mandir}/man1/ping_pong.1.gz
%{_mandir}/man5/ctdb.conf.5.gz
%{_mandir}/man5/ctdb-script.options.5.gz
%{_mandir}/man5/ctdb.sysconfig.5.gz
%{_mandir}/man7/ctdb.7.gz
%{_mandir}/man7/ctdb-tunables.7.gz
%{_mandir}/man7/ctdb-statistics.7.gz

%{_tmpfilesdir}/ctdb.conf

%{_unitdir}/ctdb.service

%dir %{_datadir}/ctdb
%dir %{_datadir}/ctdb/events
%dir %{_datadir}/ctdb/events/legacy/
%{_datadir}/ctdb/events/legacy/00.ctdb.script
%{_datadir}/ctdb/events/legacy/01.reclock.script
%{_datadir}/ctdb/events/legacy/05.system.script
%{_datadir}/ctdb/events/legacy/10.interface.script
%{_datadir}/ctdb/events/legacy/11.natgw.script
%{_datadir}/ctdb/events/legacy/11.routing.script
%{_datadir}/ctdb/events/legacy/13.per_ip_routing.script
%{_datadir}/ctdb/events/legacy/20.multipathd.script
%{_datadir}/ctdb/events/legacy/31.clamd.script
%{_datadir}/ctdb/events/legacy/40.vsftpd.script
%{_datadir}/ctdb/events/legacy/41.httpd.script
%{_datadir}/ctdb/events/legacy/46.update-keytabs.script
%{_datadir}/ctdb/events/legacy/47.samba-dcerpcd.script
%{_datadir}/ctdb/events/legacy/48.netbios.script
%{_datadir}/ctdb/events/legacy/49.winbind.script
%{_datadir}/ctdb/events/legacy/50.samba.script
%{_datadir}/ctdb/events/legacy/60.nfs.script
%{_datadir}/ctdb/events/legacy/70.iscsi.script
%{_datadir}/ctdb/events/legacy/91.lvs.script
%dir %{_datadir}/ctdb/scripts
%{_datadir}/ctdb/scripts/winbind_ctdb_updatekeytab.sh

%if %{with pcp_pmda}
%files -n ctdb-pcp-pmda
%dir %{_localstatedir}/lib/pcp/pmdas/ctdb
%{_localstatedir}/lib/pcp/pmdas/ctdb/Install
%{_localstatedir}/lib/pcp/pmdas/ctdb/README
%{_localstatedir}/lib/pcp/pmdas/ctdb/Remove
%{_localstatedir}/lib/pcp/pmdas/ctdb/domain.h
%{_localstatedir}/lib/pcp/pmdas/ctdb/help
%{_localstatedir}/lib/pcp/pmdas/ctdb/pmdactdb
%{_localstatedir}/lib/pcp/pmdas/ctdb/pmns
#endif with pcp_pmda
%endif

%if %{with etcd_mutex}
%files -n ctdb-etcd-mutex
%{_libexecdir}/ctdb/ctdb_etcd_lock
%{_mandir}/man7/ctdb-etcd.7.gz
#endif with etcd_mutex
%endif

%if %{with ceph_mutex}
%files -n ctdb-ceph-mutex
%{_libexecdir}/ctdb/ctdb_mutex_ceph_rados_helper
%{_mandir}/man7/ctdb_mutex_ceph_rados_helper.7.gz
#endif with ceph_mutex
%endif

#endif with clustering
%endif

%if %{with winexe}
### WINEXE
%files winexe
%{_bindir}/winexe
%{_mandir}/man1/winexe.1.gz
%endif

%files -n libldb
%{_libdir}/libldb.so.*
%dir %{_libdir}/samba
%{_libdir}/samba/libldb-key-value-private-samba.so
%{_libdir}/samba/libldb-tdb-err-map-private-samba.so
%{_libdir}/samba/libldb-tdb-int-private-samba.so
%if %{with lmdb}
%{_libdir}/samba/libldb-mdb-int-private-samba.so
%endif

%dir %{_libdir}/samba/ldb
%{_libdir}/samba/ldb/asq.so
%{_libdir}/samba/ldb/ldb.so
%if %{with lmdb}
%{_libdir}/samba/ldb/mdb.so
%endif
%{_libdir}/samba/ldb/paged_searches.so
%{_libdir}/samba/ldb/rdn_name.so
%{_libdir}/samba/ldb/sample.so
%{_libdir}/samba/ldb/server_sort.so
%{_libdir}/samba/ldb/skel.so
%{_libdir}/samba/ldb/tdb.so

%files -n libldb-devel
%{_includedir}/samba-4.0/ldb_module.h
%{_includedir}/samba-4.0/ldb_handlers.h
%{_includedir}/samba-4.0/ldb_errors.h
%{_includedir}/samba-4.0/ldb_version.h
%{_includedir}/samba-4.0/ldb.h
%{_libdir}/libldb.so

%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb*.gz
%{_mandir}/man3/ldif*.gz

%files -n ldb-tools
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir}/samba/libldb-cmdline-private-samba.so
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%files -n python3-ldb
%{python3_sitearch}/ldb.cpython-*.so
%{_libdir}/samba/libpyldb-util.cpython-*-private-samba.so
%{python3_sitearch}/_ldb_text.py
%{python3_sitearch}/__pycache__/_ldb_text.cpython-*.py*
#endif !with testsuite
%endif

%changelog
## START: Generated by rpmautospec
* Thu Jan 23 2025 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.3-5
- Fix building with gcc 15

* Thu Jan 23 2025 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.3-4
- Fix stack use after return in new crypt module

* Tue Jan 07 2025 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.3-3
- Remove 'Requires: python3-crypt-r' also from samba-tools

* Tue Jan 07 2025 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.3-2
- Use upstream Patch instead of python3-crypt-r

* Tue Jan 07 2025 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.3-1
- Update to version 4.21.3
- resolves: rhbz#2335911

* Tue Jan 07 2025 Anoop C S <anoopcs@samba.org> - 2:4.21.2-7
- Remove unused macro samba_requires_eq

* Tue Jan 07 2025 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.2-6
- Add always to samba-devel: Requires: samba-dc-libs

* Tue Nov 26 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.2-2
- Add python3-crypt-r as requirement for samba-tool

* Mon Nov 25 2024 Günther Deschner <gd@samba.org> - 2:4.21.2-1
- Update to version 4.21.2
- resolves: rhbz#2328717

* Tue Oct 22 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.1-7
- Fix samba 4.20 -> 4.21 upgrade for the removed python3-samba-devel

* Thu Oct 17 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.1-6
- Revert "Re-enable linking with mold on i686"

* Wed Oct 16 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.1-5
- Fix even more rpminspect warnings

* Tue Oct 15 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.1-4
- Fix some more rpminspect warnings

* Tue Oct 15 2024 Andreas Schneider <asn@redhat.com> - 2:4.21.1-3
- Fix several rpminspect warnings

* Mon Oct 14 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.1-1
- Update to version 4.21.1
- resolves: rhbz#2318518

* Wed Oct 02 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-14
- Don't use RTLD_DEEPBIND by default in libldb
- resolves: rhbz#2278016

* Wed Oct 02 2024 Pavel Filipenský <pfilipensky@samba.org> - 2:4.21.0-13
- Build with ceph again for ppc64le

* Thu Sep 26 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2:4.21.0-12
- Always include libsamba-policy and libsamba-net-private-samba

* Wed Sep 25 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2:4.21.0-11
- Fix ELN build

* Mon Sep 23 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-10
- Add cert directories to samba-common

* Fri Sep 13 2024 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.21.0-9
- Fix Samba integration with FreeIPA
- resolves: rhbz#2309199

* Mon Sep 02 2024 Günther Deschner <gd@samba.org> - 2:4.21.0-8
- Update required tdb version
- related: rhbz#2309153

* Mon Sep 02 2024 Günther Deschner <gd@samba.org> - 2:4.21.0-7
- Update to version 4.21.0
- resolves: rhbz#2309153

* Mon Sep 02 2024 Günther Deschner <gd@samba.org> - 2:4.21.0-0.6.rc4
- Update to version 4.21.0rc4
- resolves: rhbz#2300469

* Mon Sep 02 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-0.5.rc3
- Fix ldb requires and provides
- related: rhbz#230046

* Mon Sep 02 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-0.4.rc3
- Fix manpages for libldb

* Mon Sep 02 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-0.3.rc3
- Update to version 4.21.0rc3
- related: rhbz#230046

* Mon Sep 02 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.21.0-0.2.rc2
- Remove also python-ldb-devel-common
- related: rhbz#230046

* Mon Sep 02 2024 Günther Deschner <gd@samba.org> - 2:4.21.0-0.1.rc2
- Update to Samba 4.21.0rc2
- Package libldb a public library
- resolves: #2300469

* Sat Aug 17 2024 Peter Robinson <pbrobinson@gmail.com> - 2:4.20.4-1
- Update to version 4.20.4

* Mon Aug 05 2024 Christoph Erhardt <fedora@sicherha.de> - 2:4.20.2-5
- Re-enable linking with mold on i686

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.20.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Andreas Schneider <asn@cryptomilk.org> - 2:4.20.2-3
- Move README.md and WHATSNEW.txt to samba-common

* Tue Jun 25 2024 Günther Deschner <gd@samba.org> - 2:4.20.2-2
- resolves: #2293108 - Move LICENSE file to samba-common

* Wed Jun 19 2024 Günther Deschner <gd@samba.org> - 2:4.20.2-1
- resolves: #2293100 - Update to version 4.20.2

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 2:4.20.1-4
- Rebuilt for Python 3.13

* Wed May 08 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.1-1
- resolves: #2279780 - Update to version 4.20.1

* Wed Mar 27 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.0-7
- resolves: #2271916 - Update to version 4.20.0

* Tue Mar 12 2024 Richard W.M. Jones <rjones@redhat.com> - 2:4.20.0-0.6.rc4
- Bump and rebuild package (for riscv64)

* Mon Mar 11 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.0rc4-5
- resolves: #2269037 - Update to version 4.20.0rc4

* Mon Feb 26 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.0rc3-4
- resolves: #2266039 - Update to version 4.20.0rc3

* Mon Feb 12 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.0rc2-3
- resolves: #2263874 - Update to version 4.20.0rc2

* Thu Feb 01 2024 Pete Walter <pwalter@fedoraproject.org> - 2:4.20.0-0.2.rc1
- Rebuild for ICU 74

* Mon Jan 29 2024 Guenther Deschner <gdeschner@redhat.com> - 4.20.0rc1-1
- resolves: #2260895 - Update to version 4.20.0rc1

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Andreas Schneider <asn@redhat.com> - 4.29.4-3
- Fix samba-gpupdate on Fedora/RHEL

* Tue Jan 09 2024 Andreas Schneider <asn@redhat.com> - 4.19.4-2
- resolves: rhbz#2256326 - Create all groups using systemd

* Mon Jan 08 2024 Guenther Deschner <gdeschner@redhat.com> - 4.19.4-1
- resolves: #2257287 - Update to version 4.19.4

* Tue Nov 28 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.3-2
- Disable performance co-pilot support for i686

* Mon Nov 27 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.3-1
- resolves: #2251766 - Update to version 4.19.3

* Wed Nov 15 2023 Andreas Schneider <asn@redhat.com> - 4.19.2-2
- Package samba-gpupdate also for RHEL9

* Mon Oct 16 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.2-1
- resolves: #2244496 - Update to version 4.19.2

* Tue Oct 10 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.1-1
- resolves: #2243073 - Update to version 4.19.1
- resolves: #2241881, #2243228: Security fix for CVE-2023-3961
- resolves: #2241882, #2243231: Security fix for CVE-2023-4091
- resolves: #2241883, #2243230: Security fix for CVE-2023-4154
- resolves: #2241884, #2243229: Security fix for CVE-2023-42669
- resolves: #2241885, #2243232: Security fix for CVE-2023-42670

* Mon Sep 04 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.0-1
- resolves: #2237259 - Update to version 4.19.0

* Mon Aug 28 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.0-0.5.rc4
- resolves: #2232744 - Update to version 4.19.0rc4

* Fri Aug 18 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.0-0.4.rc3
- resolves: #2232744 - Update to version 4.19.0rc3

* Wed Aug 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2:4.19.0-0.3.rc2
- Move ad-claims and authn-policy-util to dc-libs

* Tue Aug 15 2023 Adam Williamson <awilliam@redhat.com> - 4.19.0-0.2.rc2
- python3-samba-dc requires python3-markdown now

* Tue Aug 08 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.0-0.1.rc2
- resolves: #2227246 - Update to version 4.19.0rc2

* Mon Aug 07 2023 Guenther Deschner <gdeschner@redhat.com> - 4.19.0-0.0.rc1
- resolves: #2227246 - Update to version 4.19.0rc1

* Thu Jul 20 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.5-0
- resolves: #2224040 - Update to version 4.18.5
- resolves: #2222791, #2224254 - Security fix for CVE-2022-2127
- resolves: #2222792, #2224255 - Security fix for CVE-2023-3347
- resolves: #2222793, #2224253 - Security fix for CVE-2023-34966
- resolves: #2222794, #2224252 - Security fix for CVE-2023-34967
- resolves: #2222795, #2224250 - Security fix for CVE-2023-34968

* Sat Jul 15 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.4-3
- resolves: #2223091 - Fix netlogon LogonGetCapabilities level 2 error handling

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2:4.18.4-2
- Rebuilt for ICU 73.2

* Wed Jul 05 2023 Python Maint <python-maint@redhat.com> - 2:4.18.4-1
- Rebuilt for Python 3.12

* Wed Jul 05 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.4-0
- resolves: #2219799 - Update to version 4.18.4

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 2:4.18.3-5
- Rebuilt for Python 3.12

* Mon Jun 26 2023 Adam Williamson <awilliam@redhat.com> - 4.18.3-4
- Only run libwbclient %pre on upgrade, not fresh install

* Fri Jun 23 2023 Andreas Schneider <asn@redhat.com> - 4.18.3-3
- resolves: rhbz#2211577 - Fix libwbclient package upgrades

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2:4.18.3-2
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Andreas Schneider <asn@redhat.com> - 4.18.3-1
- resolves: #2203539 - Also cover mit_kdc.log by logrotate

* Thu Jun 01 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.3-0
- resolves: #2211453 - Update to version 4.18.3

* Wed Apr 19 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.2-0
- resolves: #2187991 - Update to version 4.18.2

* Wed Mar 29 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.1-0
- resolves: #2182787 - Update to version 4.18.1
- resolves: #2182772, #2182773 - Security fixes for CVE-2023-0225
- resolves: #2182774, #2182775 - Security fixes for CVE-2023-0922
- resolves: #2182776, #2182777 - Security fixes for CVE-2023-0614

* Tue Mar 21 2023 Andreas Schneider <asn@redhat.com> - 4.18.0-12
- Fix ctdb file lists when built with test suite enabled

* Fri Mar 17 2023 Kalev Lember <klember@redhat.com> - 4.18.0-10
- Move libstable-sort-samba4.so to samba-client-libs subpackage

* Wed Mar 08 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.0-9
- resolves: #2176469 - Update to version 4.18.0

* Wed Mar 01 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.0rc4-8
- resolves: #2174415 - Update to version 4.18.0rc4

* Tue Feb 28 2023 Andreas Schneider <asn@redhat.com> - 4.18.0-0.7.rc3
- resolves: #2173619 - Add missing Requires for glibc-gconv-extra

* Thu Feb 23 2023 Pavel Filipenský <pfilipen@redhat.com> - 4.18.0-0.6.rc3
- SPDX migration

* Wed Feb 15 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.0rc3-6
- resolves: #2166416 - Update to version 4.18.0rc3

* Mon Feb 13 2023 Pavel Filipenský <pfilipen@redhat.com> - 4.18.0rc2-5
- Create package samba-tools, move there samba-tool binary

* Thu Feb 02 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.0rc2-3
- resolves: #2166416 - Update to version 4.18.0rc2

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.18.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Guenther Deschner <gdeschner@redhat.com> - 4.18.0rc1-0
- resolves: #2162097 - Update to version 4.18.0rc1

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2:4.17.4-4
- Rebuild for ICU 72

* Thu Dec 22 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.4-3
- Create package dc-libs also for 'non-dc build'

* Tue Dec 20 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.4-2
- Fix '--without dc' build: delete libauth4-samba4.so

* Mon Dec 19 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.4-1
- Create a samba-dcerpc sub-package
- Fix package installation without samba and samba-dc package

* Fri Dec 16 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.4-0
- resolves: #2153906 - Update to version 4.17.4
- resolves: #2154362, #2154363 - Security fixes for CVE-2022-38023
- resolves: #2154303, #2154304 - Security fixes for CVE-2022-37966
- resolves: #2154320, #2154322 - Security fixes for CVE-2022-37967

* Thu Dec  1 2022 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.17.3-2
- Rebuild against krb5 1.20.1, new KDB interface

* Mon Nov 21 2022 Florian Weimer <fweimer@redhat.com> - 2:4.17.3-1
- Remove C89-specific language constructs from configure checks
- Fix feature detection for major/minor macros

* Tue Nov 15 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.3-0
- resolves: #2142959 - Update to version 4.17.3
- resolves: #2140960, #2143117 - Security fixes for CVE-2022-42898

* Wed Nov 02 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.2-1
- Always add epoch to samba_depver to fix osci.brew-build.rpmdeplint.functional

* Tue Oct 25 2022 Andreas Schneider <asn@redhat.com> - 4.17.2-1
- Update to version 4.17.2
- Fix CVE-2022-3592: A malicious client can use a symlink to escape the
  exported

* Mon Oct 24 2022 Andreas Schneider <asn@redhat.com> - 4.17.1-2
- Add missing dependency for wbinfo used by ctdb scripts

* Wed Oct 19 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.1-1
- Update to version 4.17.1
- resolves: rhbz#2127301 - Permission denied calling SMBC_getatr when file not exists
- resolves: rhbz#2133818 - rpcclient 4.17.0 unable to resolve server hostname

* Wed Oct 05 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-2
- Move group creation logic to sysusers.d fragment

* Tue Sep 13 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-1
- resolves: rhbz#2118818 - Update to version 4.17.0
- resolves: rhbz#2121138 - Fix CVE-2022-32743
- resolves: rhbz#2122650 - Fix CVE-2022-1615

* Tue Sep 13 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-0.11.rc5
- resolves: rhbz#2093656 - Split out libnetapi(-devel) sub-packages
- resolves: rhbz#2096405 - Add samba-usershare package

* Tue Sep 06 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.0-0.10.rc5
- resolves: #2118818 - Update to version 4.17.0rc5

* Wed Aug 31 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.0-0.9.rc4
- resolves: #2118818 - Update to version 4.17.0rc4

* Thu Aug 25 2022 Adam Williamson <awilliam@redhat.com> - 4.17.0-0.8.rc3
- Rebuild with no changes to fix F37 update grouping

* Thu Aug 25 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-0.7.rc3
- python3-samba package should not require the samba package

* Tue Aug 23 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.17.0-0.6.rc3
- resolves: #2118818 - Update to version 4.17.0rc3

* Fri Aug 19 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-0.5.rc2
- Create a samba-gpupdate sub-package for GPO client support

* Fri Aug 19 2022 Andreas Schneider <asn@redhat.com> - 4.17.0-0.4.rc2
- Split out a samba-ldb-ldap-modules subpackage

* Thu Aug 18 2022 Kalev Lember <klember@redhat.com> - 2:4.17.0-0.3.rc2
- Avoid requiring systemd as per updated packaging guidelines

* Wed Aug 17 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.0rc2-2
- resolves: #2118818 - Update to version 4.17.0rc2

* Wed Aug 10 2022 Andreas Schneider <asn@redhat.com> - 4.17.0rc1-1
- Make sure we detect if SO version numbers of public libraries change.

* Mon Aug 08 2022 Guenther Deschner <gdeschner@redhat.com> - 4.17.0rc1-0
- resolves: #2116503 - Update to version 4.17.0rc1

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 2:4.16.4-1
- Rebuilt for ICU 71.1

* Wed Jul 27 2022 Guenther Deschner <gdeschner@redhat.com> - 4.16.4-0
- resolves: #2111490 - Update to version 4.16.4
- resolves: #2108196, #2111729 - Security fixes for CVE-2022-32742
- resolves: #2108205, #2111731 - Security fixes for CVE-2022-32744
- resolves: #2108211, #2111732 - Security fixes for CVE-2022-32745
- resolves: #2108215, #2111734 - Security fixes for CVE-2022-32746

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Andreas Schneider <asn@redhat.com> - 4.16.3-1
- Update to version 4.16.3

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2:4.16.2-1
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Guenther Deschner <gdeschner@redhat.com> - 4.16.2-0
- Update to Samba 4.16.2
- resolves: #2096167

* Wed Jun 08 2022 Andreas Schneider <asn@redhat.com> - 4.16.1-7
- resolves: rhbz#2093833 - Remove weak dependency for logrotate for CentOS/RHEL

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.16.1-6
- Perl 5.36 rebuild

* Fri May 13 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.1-5
- Fix rpminspect abidiff

* Fri May 06 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.1-2
- Update requires for packages

* Thu May 05 2022 Tomas Popela <tpopela@redhat.com> - 4.16.1-1
- Don't require full systemd for tmp files handling in samba-common

* Mon May 02 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.1-0
- Update to Samba 4.16.1
- resolves: #2080915

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2:4.16.0-7
- Rebuild with mingw-gcc-12

* Tue Mar 22 2022 Guenther Deschner <gdeschner@redhat.com> - 4.16.0-6
- Update to Samba 4.16.0
- resolves: #2066290

* Wed Mar 09 2022 Guenther Deschner <gdeschner@redhat.com> - 4.16.0-0.5.rc5
- Update to Samba 4.16.0rc5
- resolves: #2042518

* Tue Mar 01 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.0-0.4.rc4
- Update to Samba 4.16.0rc4
- resolves: #2042518

* Wed Feb 23 2022 Andreas Schneider <asn@redhat.com> - 4.16.0-0.3.rc3
- resolves: rhbz#2036443 - Fix samba-tool on builds with samba-dc

* Tue Feb 15 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.0rc3
- Update to Samba 4.16.0rc3
- resolves: #2042518

* Tue Feb 01 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.0rc2
- Update to Samba 4.16.0rc2
- resolves: #2046120, #2048566 - Security fixes for CVE-2021-44141
- resolves: #2046146, #2048570 - Security fixes for CVE-2021-44142
- resolves: #2046134, #2048568 - Security fixes for CVE-2022-0336
- resolves: #2042518

* Wed Jan 26 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.0rc1
- Exclude temporarily ceph on ppc64le to fix failing build

* Tue Jan 25 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.16.0rc1
- Update to Samba 4.16.0rc1
- resolves: #2042518

* Thu Jan 20 2022 Pavel Filipenský <pfilipen@redhat.com> - 4.15.4-0
- Update to Samba 4.15.4
- resolves: #2009673, #2039034 - Security fixes for CVE-2021-20316
- resolves: #2042518

* Wed Dec 15 2021 Pavel Filipenský <pfilipen@redhat.com> - 4.15.3-1
- Fix resolv_wrapper with glibc 2.34
- resolves: #2019669

* Wed Dec 08 2021 Pavel Filipenský <pfilipen@redhat.com> - 4.15.3-0
- Update to Samba 4.15.3
- resolves: #2030382

* Sat Nov 13 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.2-3
- Fix IPA DC schannel support

* Thu Nov 11 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.2-2
- Fix winbind trusted domain regression
- related: #2021716
- Fix logfile handling
- Fix smbclient -N failures in container setups

* Tue Nov 09 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.2-0
- Update to Samba 4.15.2
- resolves: #2019660, #2021711 - Security fixes for CVE-2016-2124
- resolves: #2019672, #2021716 - Security fixes for CVE-2020-25717
- resolves: #2019726, #2021718 - Security fixes for CVE-2020-25718
- resolves: #2019732, #2021719 - Security fixes for CVE-2020-25719
- resolves: #2021728, #2021729 - Security fixes for CVE-2020-25721
- resolves: #2019764, #2021721 - Security fixes for CVE-2020-25722
- resolves: #2021726, #2021727 - Security fixes for CVE-2021-3738
- resolves: #2019666, #2021715 - Security fixes for CVE-2021-23192
- resolves: #2021625

* Fri Nov 05 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.1-1
- Fix winexe core dump
- resolves: #2020376

* Wed Oct 27 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.1-0
- Update to Samba 4.15.1
- resolves: #2017847

* Mon Sep 20 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-13
- Update to Samba 4.15.0
- resolves: #2005817

* Mon Sep 13 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.12.rc7
- Update to Samba 4.15.0rc7
- resolves: #2003740

* Thu Sep 09 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.11.rc6
- Update to Samba 4.15.0rc6
- resolves: #2002546

* Tue Sep 07 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.10.rc5
- Update to Samba 4.15.0rc5
- resolves: #2001827

* Wed Sep 01 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.9.rc4
- Update to Samba 4.15.0rc4
- resolves: #2000079

* Thu Aug 26 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.8.rc3
- Update to Samba 4.15.0rc3
- resolves: #1998024

* Wed Aug 25 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.7.rc2
- Add ceph and etcd mutex helpers for CTDB

* Mon Aug 16 2021 Anoop C S <anoopcs@samba.org> - 4.15.0-0.6.rc2
- Avoid removing PyDSDB library files from buildroot for non AD DC build

* Fri Aug 13 2021 Adam Williamson <awilliam@redhat.com> - 4.15.0-0.5.rc2
- Fix samba-common-tools dependency

* Thu Aug 12 2021 Andreas Schneider <asn@redhat.com> - 4.15.0-0.4.rc2
- Package samba-tool correctly

* Mon Aug 09 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0-0.3.rc2
- Update to Samba 4.15.0rc2
- resolves: #1991634

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.15.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0rc1-1
- Fix ctdb-pcp-pmda install
- resolves: #1983369

* Thu Jul 15 2021 Guenther Deschner <gdeschner@redhat.com> - 4.15.0rc1-0
- Update to Samba 4.15.0rc1
- resolves: #1982623

* Wed Jul 14 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.6-1
- Build with pcp-pmda support by default on Fedora
- resolves: #1552276

* Tue Jul 13 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.6-0
- Update to Samba 4.14.6
- resolves: #1981764

* Thu Jun 24 2021 Andreas Schneider <asn@redhat.com> - 4.14.5-3
- Create a subpackage for vfs-io-uring

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2:4.14.5-1
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.5-0
- Update to Samba 4.14.5
- resolves: #1966456

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.14.4-3
- Perl 5.34 rebuild

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2:4.14.4-2
- Rebuild for ICU 69

* Tue May 18 2021 Andreas Schneider <asn@redhat.com> - 4.14.4-1
- Fixed building with gcc 11.x
- Fixed quota support

* Thu Apr 29 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.4-0
- Update to Samba 4.14.4
- resolves: #1949442, #1955027 - Security fixes for CVE-2021-20254
- resolves: #1955011

* Wed Apr 28 2021 Anoop C S <anoopcs@samba.org> - 4.14.3-2
- resolves: #1954263 - wrong conditional build check of AD DC

* Tue Apr 20 2021 Andreas Schneider <asn@redhat.com> - 4.14.3-1
- resolves: #1942378 - Drop NIS support

* Tue Apr 20 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.3-0
- Update to Samba 4.14.3
- resolves: #1951531

* Mon Apr 19 2021 Michal Ambroz <rebus _AT seznam.cz> - 4.14.2-4
  - Added python3-ldb to BR

* Mon Apr 19 2021 Andreas Schneider <asn@redhat.com> - 4.12.2-3
- resolves: #1949295 - Remove findsmb script

* Wed Apr 14 2021 Richard W.M. Jones <rjones@redhat.com> - 2:4.14.2-2
- Rebuild for updated liburing.

* Wed Apr 07 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.14.2-1
- Fix memory leaks in RPC server
- resolves: #1946950

* Thu Mar 25 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.2-0
- Update to Samba 4.14.2
- related: #1941400, #1942496 - Security fixes for CVE-2020-27840
- related: #1941402, #1942497 - Security fixes for CVE-2021-20277

* Wed Mar 24 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.1-0
- Update to Samba 4.14.1
- resolves: #1941400, #1942496 - Security fixes for CVE-2020-27840
- resolves: #1941402, #1942497 - Security fixes for CVE-2021-20277

* Tue Mar 09 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.0-3
- Update to Samba 4.14.0

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2:4.14.0-0.0.rc4.2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.0rc4-0
- Update to Samba 4.14.0rc4

* Thu Feb 18 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.0rc3-0
- Update to Samba 4.14.0rc3

* Thu Feb 04 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.0rc2-0
- Update to Samba 4.14.0rc2

* Wed Jan 27 2021 Guenther Deschner <gdeschner@redhat.com> - 4.14.0rc1-0
- Update to Samba 4.14.0rc1

* Tue Jan 26 2021 Guenther Deschner <gdeschner@redhat.com> - 4.13.4-0
- Update to Samba 4.13.4

* Wed Dec 16 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.3-1
- Rebuild against krb5-1.19
- Resolves: rhbz#1915928

* Tue Dec 15 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.3-0
- Update to Samba 4.13.3

* Wed Nov 25 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.2-2
- rhbz#1892745, rhbz#1900232: smbclient mget crashes (upstream bug 14517)
- Merge RHEL 8.4 patches:
  - FIPS-related enhancements
  - FreeIPA Global Catalog patches

* Tue Nov 03 2020 Andreas Schneider <asn@redhat.com> - 4.13.2-1
- Create a python3-samba-devel package to avoid unnessary dependencies

* Tue Nov 03 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.2-0
- Update to Samba 4.13.2

* Thu Oct 29 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.1-0
- Update to Samba 4.13.1
- resolves: #1892631, #1892634 - Security fixes for CVE-2020-14318
- resolves: #1891685, #1892628 - Security fixes for CVE-2020-14323
- resolves: #1892636, #1892640 - Security fixes for CVE-2020-14383

* Mon Oct 26 2020 Andreas Schneider <asn@redhat.com> - 4.13.0-14
- Fixed dbcheck running in a release tarball
- Updated internal resolv_wrapper copy to verison 1.1.7

* Sun Oct 25 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.0-13
- Report 'samba' daemon status back to systemd
- Support dnspython 2.0.0 or later in samba_dnsupdate

* Thu Oct 22 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.0-12
- Add preliminary support for S4U operations in Samba AD DC
  resolves: #1836630 - Samba DC: Remote Desktop cannot access files
- Fix lookup_unix_user_name to allow lookup of realm-qualified users and groups
  required for upcoming FreeIPA Global Catalog support

* Tue Sep 22 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0-11
- Update to Samba 4.13.0

* Fri Sep 18 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc6-10
- Update to Samba 4.13.0rc6
- resolves: #1879822, #1880703 - Security fixes for CVE-2020-1472

* Wed Sep 16 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc5-9
- Update to Samba 4.13.0rc5

* Mon Sep 07 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc4-8
- Update to Samba 4.13.0rc4

* Fri Aug 28 2020 Neal Gompa <ngompa13@gmail.com> - 4.13.0rc3-6
- Enable winexe by default everywhere

* Fri Aug 28 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc3-5
- Update to Samba 4.13.0rc3

* Fri Aug 14 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc2-4
- Update to Samba 4.13.0rc2

* Wed Aug 12 2020 Andreas Schneider <asn@redhat.com> - 4.13.0rc1-3
- resolves: #1865831 - Add missing /usr/lib64/samba/krb5 directory
- resolves: #1866989 - Remove obsolete python3-crypto dependency

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.13.0-0.2.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2:4.13.0-0.2.rc1
- Use make macros
  https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 14 2020 Andreas Schneider <asn@redhat.com> - 4.13.0rc1-1
- Move mdssvc data files to correct package

* Thu Jul 09 2020 Guenther Deschner <gdeschner@redhat.com> - 4.13.0rc1-0
- Update to Samba 4.13.0rc1

* Wed Jul 08 2020 Merlin Mathesius <mmathesi@redhat.com> - 4.12.5-1
- Remove nonexistent --without-winexe option from configure

* Thu Jul 02 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.5-0
- Update to Samba 4.12.5

* Thu Jul 02 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.4-0
- Update to Samba 4.12.4
- resolves: #1849489, #1853255 - Security fixes for CVE-2020-10730
- resolves: #1849491, #1853256 - Security fixes for CVE-2020-10745
- resolves: #1849509, #1853276 - Security fixes for CVE-2020-10760
- resolves: #1851298, #1853259 - Security fixes for CVE-2020-14303

* Sat Jun 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.12.3-1.1
- Perl 5.32 re-rebuild updated packages

* Thu Jun 25 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.3-1
- Add BuildRequires for python3-setuptools

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.12.3-0.4
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2:4.12.3-0.3
- Rebuilt for Python 3.9

* Tue May 19 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.3-0
- Update to Samba 4.12.3

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2:4.12.2-1.2
- Rebuild for ICU 67

* Wed May 13 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.2-1
- Add support for building the new experimental io_uring VFS module

* Tue Apr 28 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.2-0
- Update to Samba 4.12.2
- resolves: #1825731, #1828870 - Security fixes for CVE-2020-10700
- resolves: #1825734, #1828872 - Security fixes for CVE-2020-10704

* Sun Apr 12 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.1-1
- Revert POSIX stat tuning in libsmbclient
- Resolves: rhbz#1801442

* Tue Apr 07 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.1-0
- Update to Samba 4.12.1

* Sat Mar 21 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.0-6
- Fix samba_requires_eq macro definition
- Resolves rhbz#1815739

* Tue Mar 10 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0-5
- Add build requirement for perl-FindBin
- resolves: #1661213 - Add winexe subpackage for remote windows command execution

* Tue Mar 03 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0-3
- Update to Samba 4.12.0

* Wed Feb 26 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0rc4-2
- Update to Samba 4.12.0rc4

* Wed Feb 19 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0rc3-2
- Update to Samba 4.12.0rc3

* Tue Feb 04 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0rc2-2
- Update to Samba 4.12.0rc2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.12.0-0.1.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.0.rc1-1
- Allow building against krb5 1.18 beta and require it for Rawhide

* Wed Jan 22 2020 Guenther Deschner <gdeschner@redhat.com> - 4.12.0rc1-0
- Update to Samba 4.12.0rc1

* Tue Jan 21 2020 Guenther Deschner <gdeschner@redhat.com> - 4.11.5-0
- Update to Samba 4.11.5
- resolves: #1791201, #1793405 - Security fixes for CVE-2019-14902
- resolves: #1791207, #1793407 - Security fixes for CVE-2019-14907
- resolves: #1791204, #1793406 - Security fixes for CVE-2019-19344

* Mon Dec 16 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.4-0
- Update to Samba 4.11.4

* Tue Dec 10 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.3-0
- Update to Samba 4.11.3
- resolves: #1778586, #1781542 - Security fixes for CVE-2019-14861
- resolves: #1778589, #1781545 - Security fixes for CVE-2019-14870

* Thu Dec 05 2019 Andreas Schneider <asn@redhat.com> - 4.11.2-2
- Restart winbindd on samba-winbind package upgrade

* Wed Nov 06 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.2-1
- Update DES removal patch

* Tue Oct 29 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.2-0
- Update to Samba 4.11.2
- resolves: #1763137, #1766558 - Security fixes for CVE-2019-10218
- resolves: #1764126, #1766559 - Security fixes for CVE-2019-14833

* Sun Oct 27 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.1-1
- resolves: #1757071 - Deploy new samba DC fails

* Fri Oct 18 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.1-0
- Update to Samba 4.11.1

* Tue Sep 17 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0-3
- Update to Samba 4.11.0

* Wed Sep 11 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0rc4-2
- Update to Samba 4.11.0rc4

* Tue Sep 03 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0rc3-2
- Update to Samba 4.11.0rc3
- resolves: #1746225, #1748308 - Security fixes for CVE-2019-10197

* Tue Aug 27 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0rc2-2
- resolves: #1746014 - re-add pidl

* Mon Aug 26 2019 Lubomir Rintel <lkundrak@v3.sk> - 2:4.11.0-0.1.rc2
- Move the NetworkManager dispatcher script out of /etc

* Wed Aug 21 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0rc2-0
- Update to Samba 4.11.0rc2

* Tue Aug 20 2019 Guenther Deschner <gdeschner@redhat.com> - 4.11.0rc1-0
- Update to Samba 4.11.0rc1

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2:4.10.6-1.1
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.10.6-1
- Fix Samba bug https://bugzilla.samba.org/show_bug.cgi?id=14091
- Fixes: Windows systems cannot resolve IPA users and groups over LSA RPC

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.10.6-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.6-0
- Update to Samba 4.10.6

* Mon Jul 01 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.5-2
- resolves: #1718113 - Avoid deprecated time.clock in wafsamba
- resolves: #1711638 - Update to latest waf version 2.0.17

* Thu Jun 20 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.5-1
- resolves: #1602824 - Make vfs_fruit operable with other remote VFS modules
- resolves: #1716455 - Avoid pathconf() in get_real_filename() VFS calls
- resolves: #1706090, #1700791 - Fix smbspool

* Wed Jun 19 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.5-0
- Update to Samba 4.10.5
- resolves: #1711816, #1721872 - Security fixes for CVE-2019-12435
- resolves: #1711837, #1721873 - Security fixes for CVE-2019-12436

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.10.4-1.1
- Perl 5.30 rebuild

* Tue May 28 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.4-1
- Add missing ctdb directories
- resolves: #1656777

* Wed May 22 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.4-0
- Update to Samba 4.10.4

* Tue May 14 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.3-0
- Update to Samba 4.10.3
- resolves: #1705877, #1709679 - Security fixes for CVE-2018-16860

* Mon Apr 15 2019 Andreas Schneider <asn@redhat.com> - 4.10.2-1
- resolves: #1699230 - Rebuild for MIT Kerberos soname bump of libkadm5srv

* Mon Apr 08 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.2-0
- Update to Samba 4.10.2
- resolves: #1689010, #1697718 - Security fixes for CVE-2019-3870
- resolves: #1691518, #1697717 - Security fixes for CVE-2019-3880

* Wed Apr 03 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.1-0
- Update to Samba 4.10.1

* Mon Mar 25 2019 Andreas Schneider <asn@redhat.com> - 4.10.0-6
- resolves: #1692347 - Add missing DC requirement for its python3 tools

* Wed Mar 20 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0-5
- Fix build failure (duplication during install)

* Tue Mar 19 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0-4
- Update to Samba 4.10.0

* Wed Mar 06 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0rc4-2
- Update to Samba 4.10.0rc4

* Fri Feb 22 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0rc3-2
- Update to Samba 4.10.0rc3

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:4.10.0-0.2.rc2.1
- Rebuild for readline 8.0

* Thu Feb 14 2019 Andreas Schneider <asn@redhat.com> - 4.10.0rc2-2
- resolves: #1672231 - Fix public NDR API

* Tue Feb 12 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0rc2-1
- resolves: #1674547 - Move samba.xattr modules out of python3 test package

* Wed Feb 06 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0rc2-0
- Update to Samba 4.10.0rc2

* Tue Jan 15 2019 Guenther Deschner <gdeschner@redhat.com> - 4.10.0rc1-0
- Update to Samba 4.10.0rc1

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2:4.9.4-0.1
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Dec 20 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.4-0
- Update to Samba 4.9.4

* Tue Nov 27 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.3-0
- Update to Samba 4.9.3
- resolves: #1625449, #1654078 - Security fixes for CVE-2018-14629
- resolves: #1642545, #1654082 - Security fixes for CVE-2018-16841
- resolves: #1646377, #1654091 - Security fixes for CVE-2018-16851
- resolves: #1646386, #1654092 - Security fixes for CVE-2018-16852
- resolves: #1647246, #1654093 - Security fixes for CVE-2018-16853
- resolves: #1649278, #1654095 - Security fixes for CVE-2018-16857

* Thu Nov 08 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.2-0
- Update to Samba 4.9.2

* Wed Sep 26 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.1-2
- Package ctdb/doc/examples

* Mon Sep 24 2018 Andreas Schneider <asn@redhat.com> - 4.9.1-1
- Update to Samba 4.9.1

* Thu Sep 13 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.0-4
- Update to Samba 4.9.0

* Thu Sep 06 2018 Andreas Schneider <asn@redhat.com> - 4.9.0rc5-3
- Update to Samba 4.9.0rc5

* Wed Aug 29 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.0rc4-3
- Update to Samba 4.9.0rc4

* Thu Aug 16 2018 Andreas Schneider <asn@redhat.com> - 4.9.0rc3-3
- Fix python3 packaging

* Wed Aug 15 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.0rc3-2
- Update to Samba 4.9.0rc3
- resolves: #1589651, #1617916 - Security fixes for CVE-2018-1139
- resolves: #1580230, #1618613 - Security fixes for CVE-2018-1140
- resolves: #1612805, #1618697 - Security fixes for CVE-2018-10858
- resolves: #1610640, #1617910 - Security fixes for CVE-2018-10918
- resolves: #1610645, #1617911 - Security fixes for CVE-2018-10919

* Wed Aug 01 2018 Andreas Schneider <asn@redhat.com> - 4.9.0rc2-2
- Add some spec file cleanups

* Wed Aug 01 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.0rc2-0
- Update to Samba 4.9.0rc2

* Thu Jul 12 2018 Guenther Deschner <gdeschner@redhat.com> - 4.9.0rc1-0
- Update to Samba 4.9.0rc1

* Thu Jul 12 2018 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.8.3-4.1
- Scope to local __bss_start symbol (typo in a patch)
- Fixes https://bugzilla.redhat.com/show_bug.cgi?id=1600035

* Thu Jul 12 2018 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.8.3-4
- Change scope to local for symbols automatically added by upcoming binutils 2.31
- Fixes https://bugzilla.redhat.com/show_bug.cgi?id=1600035

* Wed Jul 11 2018 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.8.3-3
- Rebuild Samba against binutils 2.30.90-2.fc29
- Fixes https://bugzilla.redhat.com/show_bug.cgi?id=1600035
- Add explicit BuildRequires for gcc

* Fri Jul 06 2018 Petr Pisar <ppisar@redhat.com>
- Perl 5.28 rebuild

* Thu Jul 05 2018 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.8.3-2
- Fix rawhide build by explicitly using /usr/bin/python2

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com>
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2:4.8.3-1.2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.8.3-1.1
- Perl 5.28 rebuild

* Tue Jun 26 2018 Andreas Schneider <asn@redhat.com> - 4.8.3-1
- Update to Samba 4.8.3
- Remove python(2|3)-subunit dependency

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2:4.8.2-1.1
- Rebuilt for Python 3.7

* Wed May 16 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.2-0
- Update to Samba 4.8.2

* Wed May 09 2018 Andreas Schneider <asn@redhat.com> - 4.8.1-1
- resolves: #1574177 - Fix smbspool command line argument handling

* Thu Apr 26 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.1-0
- Update to Samba 4.8.1

* Wed Mar 14 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.0-7
- resolves: #1554754, #1554756 - Security fixes for CVE-2018-1050 CVE-2018-1057
- resolves: #1555112 - Update to Samba 4.8.0

* Tue Mar 13 2018 Andreas Schneider <asn@redhat.com> - 4.8.0rc4-6
- resolves: #1552652 - Fix usage of nc in ctdb tests and only recommned it

* Fri Mar 02 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.0rc4-5
- Update to Samba 4.8.0rc4

* Mon Feb 12 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.0rc3-4
- Update to Samba 4.8.0rc3

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:4.8.0-0.3.rc2.1
- Escape macros in %%changelog

* Fri Jan 26 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.0rc2-3
- Update to Samba 4.8.0rc2

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 2:4.8.0-0.2.rc1
- Explicitly BR: rpcsvc-proto-devel

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2:4.8.0-0.1.rc1.1
- Rebuilt for switch to libxcrypt

* Mon Jan 15 2018 Guenther Deschner <gdeschner@redhat.com> - 4.8.0rc1-1
- Update to Samba 4.8.0rc1

* Mon Jan 08 2018 Andreas Schneider <asn@redhat.com> - 4.7.4-1
- resolves: #1508092 - Add missing dependency for tdbbackup

* Mon Dec 25 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.4-0
- Update to Samba 4.7.4

* Mon Dec 04 2017 Andreas Schneider <asn@redhat.com> - 4.7.3-3
- resolves: #1520163 - Link libaesni-intel-samba4.so with -z noexecstack

* Thu Nov 30 2017 Andreas Schneider <asn@redhat.com> - 4.7.3-2
- Fix deamon startup with systemd

* Thu Nov 23 2017 Bastien Nocera <bnocera@redhat.com> - 4.7.3-1
- Enable AES acceleration on Intel compatible CPUs by default

* Tue Nov 21 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.3-0
- Update to Samba 4.7.3
- resolves: #1515692 - Security fix for CVE-2017-14746 and CVE-2017-15275

* Wed Nov 15 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.2-0
- resolves: #1513452 - Update to Samba 4.7.2

* Mon Nov 13 2017 Andreas Schneider <asn@redhat.com> - 4.7.1-2
- Fix release number

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.7.1-1
- Remove old crufty coreutils requires

* Thu Nov 02 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.1-0
- resolves: #1508871 - Update to Samba 4.7.1

* Mon Oct 30 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.0-18
- Force samba-dc to use the same libldb version as LDB modules compiled
- resolves: #1507420 - LDB / Samba module version mismatch

* Fri Oct 27 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-17
- Move dsdb libs to python2-samba-dc

* Thu Oct 26 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-16
- Create python[2|3]-samba-dc packages

* Wed Oct 25 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-15
- related: #1499140 - Fix several dependency issues
- Fix building with MIT Kerberos 1.16

* Fri Oct 13 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-14
- resolves: #1499140 - Move libdfs-server-ad to the correct subpackage

* Fri Oct 06 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.0-13
- Move /usr/lib{64,}/samba/libdsdb-garbage-collect-tombstones-samba4.so to samba-dc-libs
- Rebuild in rawhide against new krb5 1.16 and docbook-xml

* Thu Sep 21 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.0-12
- Update to Samba 4.7.0
- resolves: #1493441 - Security fix for CVE-2017-12150 CVE-2017-12151 CVE-2017-12163

* Sun Sep 17 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.0-0.11.rc6
- Update to Samba 4.7.0rc6

* Wed Sep 13 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.0-0.11.rc5
- resolves: #1491137 - dcerpc/__init__.py is not packaged for py3

* Tue Sep 12 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.10.rc5
- resolves: #1476175 - Create seperate package for bind_dlz module

* Tue Aug 29 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.0-0.9.rc5
- Update to Samba 4.7.0rc5

* Tue Aug 08 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.9.rc3
- Add printadmin group for printer driver handling

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2:4.7.0-0.8.rc3.2
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.7.0-0.8.rc3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 26 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.8.rc3
- resolves: #1301002 - Enable avahi support

* Tue Jul 25 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.0-0.7.rc3
- Update to Samba 4.7.0rc3

* Mon Jul 24 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.7.rc1
- Rename samba-python to python2-samba
- Update build requirement for libcephfs

* Thu Jul 20 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.0-0.6.rc1
- Use Python 2 explicitly for samba-tool and other Python-based tools
- Install samba.service as it is required for the AD DC case

* Tue Jul 18 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.0-0.5.rc1
- Convert more rpc modules to python3
- Explicitly specify Python artifacts in the spec to be able to catch unpackaged ones
- Split 'make test' Python code into separate python2-samba-test/python3-samba-test sub-packages
- Remove embedded python2-dns version, require python{2,3}-dns instead

* Thu Jul 06 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.4.rc1
- Add python3 support
- Fix %%posttrans for libwbclient-devel

* Thu Jul 06 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.3.rc1
- Do not install conflicting file _ldb_text.py

* Wed Jul 05 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.2.rc1
- Fix requirement generation for shared libraries

* Wed Jul 05 2017 Andreas Schneider <asn@redhat.com> - 4.7.0-0.1.rc1
- Build Samba with Active Directory support!

* Mon Jun 12 2017 Guenther Deschner <gdeschner@redhat.com> - 4.7.0-0.0.rc1
- Update to Samba 4.7.0rc1

* Mon Jun 12 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.5-0
- Update to Samba 4.6.5

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.6.4-1.1
- Perl 5.26 rebuild

* Wed May 24 2017 Andreas Schneider <asn@redhat.com> - 4.6.4-1
- #resolves: #1451486 - Add source tarball comment

* Wed May 24 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.4-0
- Update to Samba 4.6.4
- resolves: #1455050 - Security fix for CVE-2017-7494

* Tue Apr 25 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.3-0
- Update to Samba 4.6.3

* Fri Mar 31 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.2-0
- Update to Samba 4.6.2
- related: #1435156 - Security fix for CVE-2017-2619

* Thu Mar 23 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.1-0
- Update to Samba 4.6.1
- resolves: #1435156 - Security fix for CVE-2017-2619

* Wed Mar 15 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.0-4
- Export arcfour_crypt_blob to Python as samba.crypto.arcfour_encrypt
- Makes possible to run trust to AD in FreeIPA in FIPS mode

* Fri Mar 10 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.0-3
- auth/credentials: Always set the the realm if we set the principal from the ccache
- resolves: #1430761 - credentials_crb5: use gss_acquire_cred for client-side GSSAPI use case

* Thu Mar 09 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.0-2
- resolves: #1430761 - credentials_krb5: use gss_acquire_cred for client-side GSSAPI use case

* Tue Mar 07 2017 Andreas Schneider <asn@redhat.com> - 4.6.0-1
- Update to Samba 4.6.0

* Wed Mar 01 2017 Andreas Schneider <asn@redhat.com> - 4.6.0-0.3.rc4
- Update to Samba 4.6.0rc4

* Tue Feb 14 2017 Andreas Schneider <asn@redhat.com> - 4.6.0-0.1.rc3
- Update to Samba 4.6.0rc3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-0.1.rc2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.0-0.1.rc2
- Update to Samba 4.6.0rc2

* Thu Jan 12 2017 Andreas Schneider <asn@redhat.com> - 4.6.0-0.1.rc1
- resolves: #1319098 - Add missing Requires for pre-required packages

* Thu Jan 05 2017 Guenther Deschner <gdeschner@redhat.com> - 4.6.0-0.1.rc1
- Update to Samba 4.6.0rc1

* Mon Dec 19 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.3-0
- Update to Samba 4.5.3
- resolves: #1405984 - CVE-2016-2123,CVE-2016-2125 and CVE-2016-2126

* Wed Dec 07 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.2-0
- Update to Samba 4.5.2

* Mon Dec 05 2016 Rex Dieter <rdieter@fedoraproject.org> - -
- rebuild (libldb)

* Fri Nov 04 2016 Anoop C S <anoopcs@redhat.com> - 4.5.1-1
- Fix glfs_realpath allocation in vfs_glusterfs

* Wed Oct 26 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.1-0
- Update to Samba 4.5.1

* Mon Oct 17 2016 Andreas Schneider <asn@redhat.com> - 4.5.0-3
- resolves: 1375973 - Fix tevent incompatibility issue

* Wed Sep 14 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.0-2
- Fix smbspool alternatives handling during samba-client uninstall

* Wed Sep 07 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.0-1
- Update to Samba 4.5.0

* Mon Aug 29 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.0rc3-0
- Update to Samba 4.5.0rc3

* Mon Aug 15 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.0rc2-0
- Update to Samba 4.5.0rc2

* Thu Jul 28 2016 Guenther Deschner <gdeschner@redhat.com> - 4.5.0rc1-0
- Update to Samba 4.5.0rc1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.4.5-1.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.5-1
- Update to Samba 4.4.5
- resolves: #1353504 - CVE-2016-2119

* Thu Jun 23 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.4-4
- resolves: #1348899 - Import of samba.ntacls fails

* Mon Jun 20 2016 Andreas Schneider <asn@redhat.com> - 4.4.4-3
- resolves: #1337260 - Small fix to the example smb.conf file

* Wed Jun 15 2016 Andreas Schneider <asn@redhat.com> - 4.4.4-2
- Fix resolving trusted domain users on domain member

* Tue Jun 07 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.4-1
- Update to Samba 4.4.4
- resolves: #1343529

* Wed May 25 2016 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.4.3-2
- Fix libsystemd patch (#1125086) so that it actually works

* Mon May 23 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2:4.4.3-1.2
- Rebuild to drop libsystemd-daemon dependency (#1125086)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.4.3-1.1
- Perl 5.24 rebuild

* Mon May 02 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.3-1
- Update to Samba 4.4.3
- resolves: #1332178

* Tue Apr 12 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.2-1
- Update to Samba 4.4.2, fix badlock security bug
- resolves: #1326453 - CVE-2015-5370
- resolves: #1326453 - CVE-2016-2110
- resolves: #1326453 - CVE-2016-2111
- resolves: #1326453 - CVE-2016-2112
- resolves: #1326453 - CVE-2016-2113
- resolves: #1326453 - CVE-2016-2114
- resolves: #1326453 - CVE-2016-2115
- resolves: #1326453 - CVE-2016-2118

* Tue Mar 22 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-1
- Update to Samba 4.4.0

* Wed Mar 16 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.8.rc5
- Update to Samba 4.4.0rc5

* Tue Mar 08 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.7.rc4
- Update to Samba 4.4.0rc4
- resolves: #1315942 - CVE-2015-7560 Incorrect ACL get/set allowed on symlink path

* Tue Feb 23 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.6.rc3
- Update to Samba 4.4.0rc3

* Wed Feb 17 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.5.rc2
- Activate multi channel support (switched off by default)

* Mon Feb 15 2016 Andreas Schneider <asn@redhat.com> - 4.4.0-0.4.rc2
- More spec file fixes
- resolves: #1306542 - scriptlet failure because of comments

* Mon Feb 15 2016 Andreas Schneider <asn@redhat.com> - 4.4.0-0.3.rc2
- More spec file fixes

* Mon Feb 15 2016 Andreas Schneider <asn@redhat.com> - 4.4.0-0.2.rc2
- More spec file fixes

* Wed Feb 10 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.1.rc2
- Update to Samba 4.4.0rc2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:4.4.0-0.1.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Guenther Deschner <gdeschner@redhat.com> - 4.4.0-0.0.rc1
- Update to Samba 4.4.0rc1

* Fri Jan 22 2016 Alexander Bokovoy <abokovoy@redhat.com> - 4.3.4-1
- resolves: #1300038 - PANIC: Bad talloc magic value - wrong talloc version used/mixed

* Tue Jan 12 2016 Guenther Deschner <gdeschner@redhat.com> - 4.3.4-0
- resolves: #1261230 - Update to Samba 4.3.4

* Wed Dec 16 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.3-0
- Update to Samba 4.3.3
- resolves: #1292069
- CVE-2015-3223 Remote DoS in Samba (AD) LDAP server
- CVE-2015-5252 Insufficient symlink verification in smbd
- CVE-2015-5296 Samba client requesting encryption vulnerable to
                downgrade attack
- CVE-2015-5299 Missing access control check in shadow copy code
- CVE-2015-7540 DoS to AD-DC due to insufficient checking of asn1
                memory allocation

* Tue Dec 15 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.2-2
- revert dependencies to samba-common and -tools

* Tue Dec 01 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.2-1
- resolves: #1261230 - Update to Samba 4.3.2

* Wed Nov 18 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.1-3
- resolves: #1282931 - Fix DCE/RPC bind nak parsing

* Fri Oct 23 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.1-2
- Fix dependencies to samba-common

* Tue Oct 20 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.1-1
- resolves: #1261230 - Update to Samba 4.3.1

* Mon Oct 12 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.0-3
- Use separate lockdir

* Mon Oct 12 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.0-2
- resolves: #1270568 - Samba fails to start after update to 4.3.0

* Tue Sep 08 2015 Guenther Deschner <gdeschner@redhat.com> - 4.3.0-1
- resolves: #1088911 - Update to Samba 4.3.0

* Tue Sep 01 2015 Andreas Schneider <asn@redhat.com> - 4.3.0-0.1rc4
- Update to Samba 4.3.0rc4

* Mon Aug 31 2015 Andreas Schneider <asn@redhat.com> - 4.3.0-0.1rc3
- Update to Samba 4.3.0rc3

* Tue Jul 14 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.3-0
- resolves: #1088911 - Update to Samba 4.2.3

* Fri Jun 19 2015 Andreas Schneider <asn@redhat.com> - 4.2.2-1
- resolves: #1227911 - Enable tar support for smbclient
- resolves: #1234908 - Own the /var/lib/samba directory
- Enable hardened build

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.2.2-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.2.2-0.1
- Perl 5.22 rebuild

* Thu May 28 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.2-0
- Update to Samba 4.2.2

* Mon May 11 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.1-8
- Fixes: #1219832: Samba 4.2 broke FreeIPA trusts to AD
- Remove usage of deprecated API from gnutls

* Thu Apr 30 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.1-7
- Fix LSASD daemon
- resolves: #1217346 - FreeIPA trusts to AD broken due to Samba 4.2 failure to run LSARPC pipe externally

* Mon Apr 27 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.1-6
- Remove samba-common-tools from samba-client package as it brings back Python 2.7

* Mon Apr 27 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.1-5
- Require samba-common-tools in samba package
- Require samba-common-tools in samba-client package
- resolves: #1215631 - /usr/bin/net moved to samba-common-tools but the package is not required by samba

* Sat Apr 25 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.1-4
- Fix systemd library detection (incomplete patch upstream)

* Fri Apr 24 2015 Andreas Schneider <asn@redhat.com> - 4.2.1-3
- resolves: #1214973 - Fix libwbclient alternatives link.

* Wed Apr 22 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.1-2
- Add vfs snapper module.

* Tue Apr 21 2015 Andreas Schneider <asn@redhat.com> - 4.2.1-1
- Update to Samba 4.2.1
- resolves: #1213373 - Fix DEBUG macro issues in public headers

* Wed Apr 08 2015 Andreas Schneider <asn@redhat.com> - 4.2.0-3
- resolves: #1207381 - Fix libsystemd detection.

* Tue Mar 10 2015 Andreas Schneider <asn@redhat.com> - 4.2.0-2
- Fix the AD build.
- Create samba-client-libs subpackage.
- Fix multiarch issues by splitting the samba-common package.

* Thu Mar 05 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.0-1
- Update to Samba 4.2.0

* Tue Mar 03 2015 Andreas Schneider <asn@redhat.com> - 4.2.0-0.5.rc5
- Update to Samba 4.2.0rc5

* Fri Jan 16 2015 - Andreas Schneider <asn@redhat.com> - 4.2.0-0.4.rc4
- Update to Samba 4.2.0rc4
- resolves: #1154600 - Install missing samba pam.d configuration file.

* Mon Jan 12 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.0-0.6.rc3
- Fix awk as a dependency (and require gawk)

* Mon Jan 12 2015 Michael Adam <madam@redhat.com> - 4.2.0-0.5.rc3
- Add dependencies for ctdb.

* Fri Jan 09 2015 Stephen Gallagher <sgallagh@redhat.com> 4.2.0-0.4.rc3
- Apply the DEBUG patch

* Fri Jan 09 2015 Andreas Schneider <asn@redhat.com> - 4.2.0-0.3.rc3
- Fix issues with conflicting DEBUG macros.

* Tue Jan 06 2015 Michael Adam <madam@redhat.com> - 4.2.0-0.2.rc3
- Improve dependencies of vfs-glusterfs and vfs-cephfs.
- Remove unused python_libdir.
- Fix malformed changelog entries.

* Tue Jan 06 2015 Guenther Deschner <gdeschner@redhat.com> - 4.2.0-0.2.rc3
- Fix ctdb and libcephfs dependencies.

* Mon Jan 05 2015 Andreas Schneider <asn@redhat.com> - 4.2.0-0.1.rc3
- Update to Samba 4.2.0rc3
  + Samba provides ctdb packages now.

* Tue Dec 16 2014 Andreas Schneider <asn@redhat.com> - 4.2.0-0.3.rc2
- resolves: #1174412 - Build VFS Ceph module.
- resolves: #1169067 - Move libsamba-cluster-support.so to samba-libs package.
- resolves: #1016122 - Move smbpasswd to samba-common package.

* Fri Nov 21 2014 Andreas Schneider <asn@redhat.com> - 4.2.0-0.2.rc2
- Use alternatives for libwbclient.
- Add cwrap to BuildRequires.

* Wed Nov 12 2014 Andreas Schneider <asn@redhat.com> - 4.2.0-0.1.rc2
- Update to Samba 4.2.0rc2.

* Tue Oct 07 2014 Andreas Schneider <asn@redhat.com> - 4.1.12-5
- resolves: #1033595 - Fix segfault in winbind.

* Wed Sep 24 2014 Andreas Schneider <asn@redhat.com> - 4.1.12-1
- Update to Samba 4.1.12.

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.1.11-1.4
- Perl 5.20 mass

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:4.1.11-1.3
- Perl 5.20 rebuild

* Wed Aug 20 2014 Kalev Lember <kalevlember@gmail.com> - 2:4.1.11-1.2
- Rebuilt for rpm dependency generator failure (#1131892)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.11-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 1 2014 Jared Smith <jsmith@fedoraproject.org> - 4.1.11-1
- Update to upstream Samba 4.1.11 release
- resolves: #1126015 - Fix CVE-2014-3560

* Mon Jun 23 2014 Guenther Deschner <gdeschner@redhat.com> - 4.1.9-3
- Update to Samba 4.1.9.
- resolves: #1112251 - Fix CVE-2014-0244 and CVE-2014-3493.

* Wed Jun 11 2014 Guenther Deschner <gdeschner@redhat.com> - 4.1.8-3
- Update to Samba 4.1.8.
- resolves: #1102528 - CVE-2014-0178.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.1.6-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Andreas Schneider <asn@redhat.com> - 4.1.6-3
- Add systemd integration to the service daemons.

* Tue Mar 18 2014 Andreas Schneider <asn@redhat.com> - 4.1.6-2
- Created a samba-test-libs package.

* Tue Mar 11 2014 Andreas Schneider <asn@redhat.com> - 4.1.6-1
- Fix CVE-2013-4496 and CVE-2013-6442.
- Fix installation of pidl.

* Fri Feb 21 2014 Andreas Schneider <asn@redhat.com> - 4.1.5-1
- Update to Samba 4.1.5.

* Fri Feb 07 2014 Andreas Schneider <asn@redhat.com> - 4.1.4-1
- Update to Samba 4.1.4.

* Wed Jan 08 2014 Andreas Schneider <asn@redhat.com> - 4.1.3-3
- resolves: #1042845 - Do not build with libbsd.

* Tue Dec 10 2013 Guenther Deschner <gdeschner@redhat.com> - 4.1.3-2
- resolves: #1019469 - Fix winbind debug message NULL pointer derreference.

* Mon Dec 09 2013 Andreas Schneider <asn@redhat.com> - 4.1.3-1
- Update to Samba 4.1.3.
- resolves: #1039454 - CVE-2013-4408.
- resolves: #1039500 - CVE-2012-6150.

* Mon Nov 25 2013 Andreas Schneider <asn@redhat.com> - 4.1.2-1
- Update to Samba 4.1.2.

* Mon Nov 18 2013 Guenther Deschner <gdeschner@redhat.com> - 4.1.1-3
- resolves: #948509 - Fix manpage correctness.

* Fri Nov 15 2013 Andreas Schneider <asn@redhat.com> - 4.1.1-2
- related: #884169 - Fix strict aliasing warnings.

* Mon Nov 11 2013 Andreas Schneider <asn@redhat.com> - 4.1.1-1
- resolves: #1024544 - Fix CVE-2013-4475.
- Update to Samba 4.1.1.

* Mon Nov 11 2013 Andreas Schneider <asn@redhat.com> - 4.1.0-5
- related: #884169 - Fix the upgrade path.

* Wed Oct 30 2013 Andreas Schneider <asn@redhat.com> - 4.1.0-4
- related: #884169 - Add direct dependency to samba-libs in the
                     glusterfs package.
- resolves: #996567 - Fix userPrincipalName composition.
- related: #884169 - Fix memset call with zero length in in ntdb.

* Fri Oct 18 2013 Andreas Schneider <asn@redhat.com> - 4.1.0-3
- resolves: #1020329 - Build glusterfs VFS plguin.

* Tue Oct 15 2013 Andreas Schneider <asn@redhat.com> - 4.1.0-2
- resolves: #1018856 - Fix installation of pam_winbind after upgrade.
- related: #1010722 - Split out a samba-winbind-modules package.
- related: #985609

* Fri Oct 11 2013 Andreas Schneider <asn@redhat.com> - 4.1.0-1
- related: #985609 - Update to Samba 4.1.0.

* Tue Oct 01 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.8
- related: #985609 - Update to Samba 4.1.0rc4.
- resolves: #1010722 - Split out a samba-winbind-modules package.

* Wed Sep 11 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.7
- related: #985609 - Update to Samba 4.1.0rc3.
- resolves: #1005422 - Add support for KEYRING ccache type in pam_winbindd.

* Wed Sep 04 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.6
- resolves: #717484 - Enable profiling data support.

* Thu Aug 22 2013 Guenther Deschner <gdeschner@redhat.com> - 2:4.1.0-0.5
- resolves: #996160 - Fix winbind with trusted domains.

* Wed Aug 14 2013 Andreas Schneider <asn@redhat.com> 2:4.1.0-0.4
- resolves: #996160 - Fix winbind nbt name lookup segfault.

* Mon Aug 12 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.3
- related: #985609 - Update to Samba 4.1.0rc2.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2:4.1.0-0.2.rc1.1
- Perl 5.18 rebuild

* Wed Jul 24 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.2
- resolves: #985985 - Fix file conflict between samba and wine.
- resolves: #985107 - Add support for new default location for Kerberos
                      credential caches.

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 2:4.1.0-0.1.rc1.1
- Perl 5.18 rebuild

* Wed Jul 17 2013 Andreas Schneider <asn@redhat.com> - 2:4.1.0-0.1
- Update to Samba 4.1.0rc1.

* Mon Jul 15 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.7-2
- resolves: #972692 - Build with PIE and full RELRO.
- resolves: #884169 - Add explicit dependencies suggested by rpmdiff.
- resolves: #981033 - Local user's krb5cc deleted by winbind.
- resolves: #984331 - Fix samba-common tmpfiles configuration file in wrong
                      directory.

* Wed Jul 03 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.7-1
- Update to Samba 4.0.7.

* Fri Jun 07 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.6-3
- Add UPN enumeration to passdb internal API (bso #9779).

* Wed May 22 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.6-2
- resolves: #966130 - Fix build with MIT Kerberos.
- List vfs modules in spec file.

* Tue May 21 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.6-1
- Update to Samba 4.0.6.
- Remove SWAT.

* Wed Apr 10 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.5-1
- Update to Samba 4.0.5.
- Add UPN enumeration to passdb internal API (bso #9779).
- resolves: #928947 - samba-doc is obsolete now.
- resolves: #948606 - LogRotate should be optional, and not a hard "Requires".

* Fri Mar 22 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.4-3
- resolves: #919405 - Fix and improve large_readx handling for broken clients.
- resolves: #924525 - Don't use waf caching.

* Wed Mar 20 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.4-2
- resolves: #923765 - Improve packaging of README files.

* Wed Mar 20 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.4-1
- Update to Samba 4.0.4.

* Mon Mar 11 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.3-4
- resolves: #919333 - Create /run/samba too.

* Mon Mar 04 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.3-3
- Fix the cache dir to be /var/lib/samba to support upgrades.

* Thu Feb 14 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.3-2
- resolves: #907915 - libreplace.so => not found

* Thu Feb 07 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.3-1
- Update to Samba 4.0.3.
- resolves: #907544 - Add unowned directory /usr/lib64/samba.
- resolves: #906517 - Fix pidl code generation with gcc 4.8.
- resolves: #908353 - Fix passdb backend ldapsam as module.

* Wed Jan 30 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.2-1
- Update to Samba 4.0.2.
- Fixes CVE-2013-0213.
- Fixes CVE-2013-0214.
- resolves: #906002
- resolves: #905700
- resolves: #905704
- Fix conn->share_access which is reset between user switches.
- resolves: #903806
- Add missing example and make sure we don't introduce perl dependencies.
- resolves: #639470

* Wed Jan 16 2013 Andreas Schneider <asn@redhat.com> - 2:4.0.1-1
- Update to Samba 4.0.1.
- Fixes CVE-2013-0172.

* Mon Dec 17 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-174
- Fix typo in winbind-krb-locator post uninstall script.

* Tue Dec 11 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-173
- Update to Samba 4.0.0.

* Thu Dec 06 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-171.rc6
- Fix typo in winbind-krb-locator post uninstall script.

* Tue Dec 04 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-170.rc6
- Update to Samba 4.0.0rc6.
- Add /etc/pam.d/samba for swat to work correctly.
- resolves #882700

* Fri Nov 23 2012 Guenther Deschner <gdeschner@redhat.com> - 2:4.0.0-169.rc5
- Make sure ncacn_ip_tcp client code looks for NBT_NAME_SERVER name types.

* Thu Nov 15 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-168.rc5
- Reduce dependencies of samba-devel and create samba-test-devel package.

* Tue Nov 13 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-167.rc5
- Use workaround for winbind default domain only when set.
- Build with old ctdb support.

* Tue Nov 13 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-166.rc5
- Update to Samba 4.0.0rc5.

* Mon Nov 05 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-165.rc4
- Fix library dependencies of libnetapi.

* Mon Nov 05 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-164.rc4
- resolves: #872818 - Fix perl dependencies.

* Tue Oct 30 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-163.rc4
- Update to Samba 4.0.0rc4.

* Mon Oct 29 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-162.rc3
- resolves: #870630 - Fix scriptlets interpeting a comment as argument.

* Fri Oct 26 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-161.rc3
- Add missing Requries for python modules.
- Add NetworkManager dispatcher script for winbind.

* Fri Oct 19 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-160.rc3
- resolves: #867893 - Move /var/log/samba to samba-common package for
                      winbind which requires it.

* Thu Oct 18 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-159.rc3
- Compile default auth methods into smbd.

* Tue Oct 16 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-158.rc3
- Move pam_winbind.conf and the manpages to the right package.

* Tue Oct 16 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-157.rc3
* resolves: #866959 - Build auth_builtin as static module.

* Tue Oct 16 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-156.rc3
- Update systemd Requires to reflect latest packaging guidelines.

* Tue Oct 16 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-155.rc3
- Add back the AES patches which didn't make it in rc3.

* Tue Oct 16 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-154.rc3
- Update to 4.0.0rc3.
- resolves: #805562 - Unable to share print queues.
- resolves: #863388 - Unable to reload smbd configuration with systemctl.

* Wed Oct 10 2012 Alexander Bokovoy <abokovoy@redhat.com> - 2:4.0.0-153.rc2
- Use alternatives to configure winbind_krb5_locator.so
- Fix Requires for winbind.

* Thu Oct 04 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-152.rc2
- Add kerberos AES support.
- Fix printing initialization.

* Tue Oct 02 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-151.rc2
- Update to 4.0.0rc2.

* Wed Sep 26 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-150.rc1
- Fix Obsoletes/Provides for update from samba4.
- Bump release number to be bigger than samba4.

* Wed Sep 26 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-96.rc1
- Package smbprint again.

* Wed Sep 26 2012 Andreas Schneider <asn@redhat.com> - 2:4.0.0-95.rc1
- Update to 4.0.0rc1.

* Mon Aug 20 2012 Guenther Deschner <gdeschner@redhat.com> - 2:3.6.7-94.2
- Update to 3.6.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:3.6.6-93.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Guenther Deschner <gdeschner@redhat.com> - 2:3.6.6-93
- Fix printing tdb upgrade for 3.6.6
- resolves: #841609

* Sun Jul 15 2012 Ville Skyttä <ville.skytta@iki.fi> - 2:3.6.6-92
- Call ldconfig at libwbclient and -winbind-clients post(un)install time.
- Fix empty localization files, use %%find_lang to find and %%lang-mark them.
- Escape macros in %%changelog.
- Fix source tarball URL.

* Tue Jun 26 2012 Guenther Deschner <gdeschner@redhat.com> - 2:3.6.6-91
- Update to 3.6.6

* Thu Jun 21 2012 Andreas Schneider <asn@redhat.com> - 2:3.6.5-90
- Fix ldonfig.
- Require systemd for samba-common package.
- resolves: #829197

* Mon Jun 18 2012 Andreas Schneider <asn@redhat.com> - 2:3.6.5-89
- Fix usrmove paths.
- resolves: #829197

* Tue May 15 2012 Andreas Schneider <asn@redhat.com> - 2:3.6.5-88
- Move tmpfiles.d config to common package as it is needed for smbd and
  winbind.
- Make sure tmpfiles get created after installation.

* Wed May 09 2012 Guenther Deschner <gdeschner@redhat.com> - 2:3.6.5-87
- Correctly use system iniparser library

* Fri May 04 2012 Andreas Schneider <asn@redhat.com> - 2:3.6.5-86
- Bump Epoch to fix a problem with a Samba4 update in testing.

* Mon Apr 30 2012 Guenther Deschner <gdeschner@redhat.com> - 1:3.6.5-85
- Security Release, fixes CVE-2012-2111
- resolves: #817551

* Mon Apr 23 2012 Andreas Schneider <asn@redhat.com> - 1:3.6.4-84
- Fix creation of /var/run/samba.
- resolves: #751625

* Fri Apr 20 2012 Guenther Deschner <gdeschner@redhat.com> - 1:3.6.4-83
- Avoid private krb5_locate_kdc usage
- resolves: #754783

* Thu Apr 12 2012 Jon Ciesla <limburgher@gmail.com> - 1:3.6.4-82
- Update to 3.6.4
- Fixes CVE-2012-1182

* Mon Mar 19 2012 Andreas Schneider <asn@redhat.com> - 1:3.6.3-81
- Fix provides for of libwclient-devel for samba-winbind-devel.

* Thu Feb 23 2012 Andreas Schneider <asn@redhat.com> - 1:3.6.3-80
- Add commented out 'max protocol' to the default config.

* Mon Feb 13 2012 Andreas Schneider <asn@redhat.com> - 1:3.6.3-79
- Create a libwbclient package.
- Replace winbind-devel with libwbclient-devel package.

* Mon Jan 30 2012 Andreas Schneider <asn@redhat.com> - 1:3.6.3-78
- Update to 3.6.3
- Fixes CVE-2012-0817

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.6.1-77.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Andreas Schneider <asn@redhat.com> - 1:3.6.1-77
- Fix winbind cache upgrade.
- resolves: #760137

* Fri Nov 18 2011 Andreas Schneider <asn@redhat.com> - 1:3.6.1-76
- Fix piddir to match with systemd files.
- Fix crash bug in the debug system.
- resolves: #754525

* Fri Nov 04 2011 Andreas Schneider <asn@redhat.com> - 1:3.6.1-75
- Fix systemd dependencies
- resolves: #751397

* Wed Oct 26 2011 Andreas Schneider <asn@redhat.com> - 1:3.6.1-74
- Update to 3.6.1

* Tue Oct 04 2011 Guenther Deschner <gdeschner@redhat.com> - 1:3.6.0-73
- Fix nmbd startup
- resolves: #741630

* Tue Sep 20 2011 Tom Callaway <spot@fedoraproject.org> - 1:3.6.0-72
- convert to systemd
- restore epoch from f15

* Sat Aug 13 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0-71
- Update to 3.6.0 final

* Sun Jul 31 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0rc3-70
- Update to 3.6.0rc3

* Tue Jun 07 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0rc2-69
- Update to 3.6.0rc2

* Tue May 17 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0rc1-68
- Update to 3.6.0rc1

* Wed Apr 27 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre3-67
- Update to 3.6.0pre3

* Wed Apr 13 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre2-66
- Update to 3.6.0pre2

* Fri Mar 11 2011 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre1-65
- Enable quota support

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.0-64pre1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre1-64
- Add %%ghost entry for /var/run using tmpfs
- resolves: #656685

* Thu Aug 26 2010 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre1-63
- Put winbind krb5 locator plugin into a separate rpm
- resolves: #627181

* Tue Aug 03 2010 Guenther Deschner <gdeschner@redhat.com> - 3.6.0pre1-62
- Update to 3.6.0pre1

* Wed Jun 23 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.4-61
- Update to 3.5.4

* Wed May 19 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.3-60
- Update to 3.5.3
- Make sure nmb and smb initscripts return LSB compliant return codes
- Fix winbind over ipv6

* Wed Apr 07 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.2-59
- Update to 3.5.2

* Mon Mar 08 2010 Simo Sorce <ssorce@redhat.com> - 3.5.1-58
- Security update to 3.5.1
- Fixes CVE-2010-0728

* Mon Mar 08 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.0-57
- Remove cifs.upcall and mount.cifs entirely

* Mon Mar 01 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.0-56
- Update to 3.5.0

* Fri Feb 19 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.0rc3-55
- Update to 3.5.0rc3

* Tue Jan 26 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.0rc2-54
- Update to 3.5.0rc2

* Fri Jan 15 2010 Jeff Layton <jlayton@redhat.com> - 3.5.0rc1-53
- separate out CIFS tools into cifs-utils package

* Fri Jan 08 2010 Guenther Deschner <gdeschner@redhat.com> - 3.5.0rc1-52
- Update to 3.5.0rc1

* Tue Dec 15 2009 Guenther Deschner <gdeschner@redhat.com> - 3.5.0pre2-51
- Update to 3.5.0pre2
- Remove umount.cifs

* Wed Nov 25 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.3-49
- Various updates to inline documentation in default smb.conf file
- resolves: #483703

* Thu Oct 29 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.3-48
- Update to 3.4.3

* Fri Oct 09 2009 Simo Sorce <ssorce@redhat.com> - 3.4.2-47
- Spec file cleanup
- Fix sources upstream location
- Remove conditionals to build talloc and tdb, now they are completely indepent
  packages in Fedora
- Add defattr() where missing
- Turn all tabs into 4 spaces
- Remove unused migration script
- Split winbind-clients out of main winbind package to avoid multilib to include
  huge packages for no good reason

* Thu Oct 01 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.2-0.46
- Update to 3.4.2
- Security Release, fixes CVE-2009-2813, CVE-2009-2948 and CVE-2009-2906

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 3.4.1-0.45
- Use password-auth common PAM configuration instead of system-auth

* Wed Sep 09 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.1-0.44
- Update to 3.4.1

* Thu Aug 20 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0-0.43
- Fix cli_read()
- resolves: #516165

* Thu Aug 06 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0-0.42
- Fix required talloc version number
- resolves: #516086

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.4.0-0.41.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0-0.41
- Fix Bug #6551 (vuid and tid not set in sessionsetupX and tconX)
- Specify required talloc and tdb version for BuildRequires

* Fri Jul 03 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0-0.40
- Update to 3.4.0

* Fri Jun 19 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0rc1-0.39
- Update to 3.4.0rc1

* Mon Jun 08 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0pre2-0.38
- Update to 3.4.0pre2

* Thu Apr 30 2009 Guenther Deschner <gdeschner@redhat.com> - 3.4.0pre1-0.37
- Update to 3.4.0pre1

* Wed Apr 29 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.4-0.36
- Update to 3.3.4

* Mon Apr 20 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.3-0.35
- Enable build of idmap_tdb2 for clustered setups

* Wed Apr  1 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.3-0.34
- Update to 3.3.3

* Thu Mar 26 2009 Simo Sorce <ssorce@redhat.com> - 3.3.2-0.33
- Fix nmbd init script nmbd reload was causing smbd not nmbd to reload the
  configuration
- Fix upstream bug 6224, nmbd was waiting 5+ minutes before running elections on
  startup, causing your own machine not to show up in the network for 5 minutes
  if it was the only client in that workgroup (fix committed upstream)

* Thu Mar 12 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.2-0.31
- Update to 3.3.2
- resolves: #489547

* Thu Mar  5 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.1-0.30
- Add libcap-devel to requires list (resolves: #488559)

* Tue Mar  3 2009 Simo Sorce <ssorce@redhat.com> - 3.3.1-0.29
- Make the talloc and ldb packages optionsl and disable their build within
  the samba3 package, they are now built as part of the samba4 package
  until they will both be released as independent packages.

* Wed Feb 25 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.1-0.28
- Enable cluster support

* Tue Feb 24 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.1-0.27
- Update to 3.3.1

* Sat Feb 21 2009 Simo Sorce <ssorce@redhat.com> - 3.3.0-0.26
- Rename ldb* tools to ldb3* to avoid conflicts with newer ldb releases

* Tue Feb  3 2009 Guenther Deschner <gdeschner@redhat.com> - 3.3.0-0.25
- Update to 3.3.0 final
- Add upstream fix for ldap connections to AD (Bug #6073)
- Remove bogus perl dependencies (resolves: #473051)

* Fri Nov 28 2008 Guenther Deschner <gdeschner@redhat.com> - 3.3.0-0rc1.24
- Update to 3.3.0rc1

* Thu Nov 27 2008 Simo Sorce <ssorce@redhat.com> - 3.2.5-0.23
- Security Release, fixes CVE-2008-4314

* Thu Sep 18 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.4-0.22
- Update to 3.2.4
- resolves: #456889
- move cifs.upcall to /usr/sbin

* Wed Aug 27 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.3-0.21
- Security fix for CVE-2008-3789

* Mon Aug 25 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.2-0.20
- Update to 3.2.2

* Mon Aug 11 2008 Simo Sorce <ssorce@redhat.com> - 3.2.1-0.19
- Add fix for CUPS problem, fixes bug #453951

* Wed Aug  6 2008 Simo Sorce <ssorce@redhat.com> - 3.2.1-0.18
- Update to 3.2.1

* Tue Jul  1 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-2.17
- Update to 3.2.0 final
- resolves: #452622

* Tue Jun 10 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.rc2.16
- Update to 3.2.0rc2
- resolves: #449522
- resolves: #448107

* Fri May 30 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.rc1.15
- Fix security=server
- resolves: #449038, #449039

* Wed May 28 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.rc1.14
- Add fix for CVE-2008-1105
- resolves: #446724

* Fri May 23 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.rc1.13
- Update to 3.2.0rc1

* Wed May 21 2008 Simo Sorce <ssorce@redhat.com> - 3.2.0-1.pre3.12
- make it possible to print against Vista and XP SP3 as servers
- resolves: #439154

* Thu May 15 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre3.11
- Add "net ads join createcomputer=ou1/ou2/ou3" fix (BZO #5465)

* Fri May 09 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre3.10
- Add smbclient fix (BZO #5452)

* Fri Apr 25 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre3.9
- Update to 3.2.0pre3

* Tue Mar 18 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre2.8
- Add fixes for libsmbclient and support for r/o relocations

* Mon Mar 10 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre2.7
- Fix libnetconf, libnetapi and msrpc DSSETUP call

* Thu Mar 06 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre2.6
- Create separate packages for samba-winbind and samba-winbind-devel
- Add cifs.spnego helper

* Wed Mar 05 2008 Guenther Deschner <gdeschner@redhat.com> - 3.2.0-1.pre2.3
- Update to 3.2.0pre2
- Add talloc and tdb lib and devel packages
- Add domainjoin-gui package

* Fri Feb 22 2008 Simo Sorce <ssorce@redhat.com> - 3.2.0-0.pre1.3
- Try to fix GCC 4.3 build
- Add --with-dnsupdate flag and also make sure other flags are required just to
  be sure the features are included without relying on autodetection to be
  successful

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:3.2.0-1.pre1.2
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 3.2.0-0.pre1.2
- Rebuild for openldap bump

* Thu Oct 18 2007 Guenther Deschner <gdeschner@redhat.com> 3.2.0-0.pre1.1.fc9
- 32/64bit padding fix (affects multilib installations)

* Mon Oct 8 2007 Simo Sorce <ssorce@redhat.com> 3.2.0-0.pre1.fc9
- New major relase, minor switched from 0 to 2
- License change, the code is now GPLv3+
- Numerous improvements and bugfixes included
- package libsmbsharemodes too
- remove smbldap-tools as they are already packaged separately in Fedora
- Fix bug 245506

* Tue Oct 2 2007 Simo Sorce <ssorce@redhat.com> 3.0.26a-1.fc8
- rebuild with AD DNS Update support

* Tue Sep 11 2007 Simo Sorce <ssorce@redhat.com> 3.0.26a-0.fc8
- upgrade to the latest upstream realease
- includes security fixes released today in 3.0.26

* Fri Aug 24 2007 Simo Sorce <ssorce@redhat.com> 3.0.25c-4.fc8
- add fix reported upstream for heavy idmap_ldap memleak

* Tue Aug 21 2007 Simo Sorce <ssorce@redhat.com> 3.0.25c-3.fc8
- fix a few places were "open" is used an interfere with the new glibc

* Tue Aug 21 2007 Simo Sorce <ssorce@redhat.com> 3.0.25c-2.fc8
- remove old source
- add patch to fix samba bugzilla 4772

* Tue Aug 21 2007 Guenther Deschner <gdeschner@redhat.com> 3.0.25c-0.fc8
- update to 3.0.25c

* Fri Jun 29 2007 Simo Sorce <ssorce@redhat.com> 3.0.25b-3.fc8
- handle cases defined in #243766

* Tue Jun 26 2007 Simo Sorce <ssorce@redhat.com> 3.0.25b-2.fc8
- update to 3.0.25b
- better error codes for init scripts: #244823

* Tue May 29 2007 Günther Deschner <gdeschner@redhat.com>
- fix pam_smbpass patch.

* Fri May 25 2007 Simo Sorce <ssorce@redhat.com>
- update to 3.0.25a as it contains many fixes
- add a fix for pam_smbpass made by Günther but committed upstream after 3.0.25a was cut.

* Mon May 14 2007 Simo Sorce <ssorce@redhat.com>
- final 3.0.25
- includes security fixes for CVE-2007-2444,CVE-2007-2446,CVE-2007-2447

* Mon Apr 30 2007 Günther Deschner <gdeschner@redhat.com>
- move to 3.0.25rc3

* Thu Apr 19 2007 Simo Sorce <ssorce@redhat.com>
- fixes in the spec file
- moved to 3.0.25rc1
- addedd patches (merged upstream so they will be removed in 3.0.25rc2)

* Wed Apr 4 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-12.fc7
- fixes in smb.conf
- advice in smb.conf to put scripts in /var/lib/samba/scripts
- create /var/lib/samba/scripts so that selinux can be happy
- fix Vista problems with msdfs errors

* Tue Apr 03 2007 Guenther Deschner <gdeschner@redhat.com> 3.0.24-11.fc7
- enable PAM and NSS dlopen checks during build
- fix unresolved symbols in libnss_wins.so (bug #198230)

* Fri Mar 30 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-10.fc7
- set passdb backend = tdbsam as default in smb.conf
- remove samba-docs dependency from swat, that was a mistake
- put back COPYING and other files in samba-common
- put examples in samba not in samba-docs
- leave only stuff under docs/ in samba-doc

* Thu Mar 29 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-9.fc7
- integrate most of merge review proposed changes (bug #226387)
- remove libsmbclient-devel-static and simply stop shipping the
  static version of smbclient as it seem this is deprecated and
  actively discouraged

* Wed Mar 28 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-8.fc7
- fix for bug #176649

* Mon Mar 26 2007 Simo Sorce <ssorce@redhat.com>
- remove patch for bug 106483 as it introduces a new bug that prevents
  the use of a credentials file with the smbclient tar command
- move the samba private dir from being the same as the config dir
  (/etc/samba) to /var/lib/samba/private

* Mon Mar 26 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-7.fc7
- make winbindd start earlier in the init process, at the same time
  ypbind is usually started as well
- add a sepoarate init script for nmbd called nmb, we need to be able
  to restart nmbd without dropping al smbd connections unnecessarily

* Fri Mar 23 2007 Simo Sorce <ssorce@redhat.com>
- add samba.schema to /etc/openldap/schema

* Thu Mar 22 2007 Florian La Roche <laroche@redhat.com>
- adjust the Requires: for the scripts, add "chkconfig --add smb"

* Tue Mar 20 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-6.fc7
- do not put comments inline on smb.conf options, they may be read
  as part of the value (for example log files names)

* Mon Mar 19 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-5.fc7
- actually use the correct samba.pamd file not the old samba.pamd.stack file
- fix logifles and use upstream convention of log.* instead of our old *.log
  Winbindd creates its own log.* files anyway so we will be more consistent
- install our own (enhanced) default smb.conf file
- Fix pam_winbind acct_mgmt PAM result code (prevented local users from
  logging in). Fixed by Guenther.
- move some files from samba to samba-common as they are used with winbindd
  as well

* Fri Mar 16 2007 Guenther Deschner <gdeschner@redhat.com> 3.0.24-4.fc7
- fix arch macro which reported Vista to Samba clients.

* Thu Mar 15 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-3.fc7
- Directories reorg, tdb files must go to /var/lib, not
  to /var/cache, add migration script in %%post common
- Split out libsmbclient, devel and doc packages
- Remove libmsrpc.[h|so] for now as they are not really usable
- Remove kill -HUP from rotate, samba use -HUP for other things
  noit to reopen logs

* Tue Feb 20 2007 Simo Sorce <ssorce@redhat.com> 3.0.24-2.fc7
- New upstream release
- Fix packaging issue wrt idmap modules used only by smbd
- Addedd Vista Patchset for compatibility with Windows Vista
- Change default of "msdfs root", it seem to cause problems with
  some applications and it has been proposed to change it for
  3.0.25 upstream

* Fri Sep 1 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23c-2
- New upstream release.

* Tue Aug 8 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23b-2
- New upstream release.

* Mon Jul 24 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23a-3
- Fix the -logfiles patch to close
  bz#199607 Samba compiled with wrong log path.
  bz#199206 smb.conf has incorrect log file path

* Mon Jul 24 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23a-2
- Upgrade to new upstream 3.0.23a
- include upstream samr_alias patch

* Tue Jul 11 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23-2
- New upstream release.
- Use modified filter-requires-samba.sh from packaging/RHEL/setup/
  to get rid of bogus dependency on perl(Unicode::MapUTF8)
- Update the -logfiles and -smb.conf patches to work with 3.0.23

* Thu Jul 6 2006 Jay Fenlason <fenlason@redhat.com> 3.0.23-0.RC3
- New upstream RC release.
- Update the -logfiles, and -passwd patches for
  3.0.23rc3
- Include the change to smb.init from Bastien Nocera <bnocera@redhat.com>)
  to close
  bz#182560 Wrong retval for initscript when smbd is dead
- Update this spec file to build with 3.0.23rc3
- Remove the -install.mount.smbfs patch, since we don't install
  mount.smbfs any more.

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 2.0.21c-3
- rebuilt with new gnutls

* Fri Mar 17 2006 Jay Fenlason <fenlason@redhat.com> 2.0.21c-2
- New upstream version.

* Mon Feb 13 2006 Jay Fenlason <fenlason@redhat.com> 3.0.21b-2
- New upstream version.
- Since the rawhide kernel has dropped support for smbfs, remove smbmount
  and smbumount.  Users should use mount.cifs instead.
- Upgrade to 3.0.21b

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:3.0.20b-2.1.1
- bump again for double-long bug on ppc(64)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 13 2005 Jay Fenlason <fenlason@redhat.com> 3.0.20b-2
- turn on -DLDAP_DEPRECATED to allow access to ldap functions that have
  been depricated in 2.3.11, but which don't have well-documented
  replacements (ldap_simple_bind_s(), for example).
- Upgrade to 3.0.20b, which includes all the previous upstream patches.
- Updated the -warnings patch for 3.0.20a.
- Include  --with-shared-modules=idmap_ad,idmap_rid to close
  bz#156810 --with-shared-modules=idmap_ad,idmap_rid
- Include the new samba.pamd from Tomas Mraz (tmraz@redhat.com) to close
  bz#170259 pam_stack is deprecated

* Sun Nov 13 2005 Warren Togami <wtogami@redhat.com> 3.0.20-3
- epochs from deps, req exact release
- rebuild against new openssl

* Mon Aug 22 2005 Jay Fenlason <fenlason@redhat.com> 3.0.20-2
- New upstream release
  Includes five upstream patches -bug3010_v1, -groupname_enumeration_v3,
    -regcreatekey_winxp_v1, -usrmgr_groups_v1, and -winbindd_v1
  This obsoletes the -pie and -delim patches
  the -warning and -gcc4 patches are obsolete too
  The -man, -passwd, and -smbspool patches were updated to match 3.0.20pre1
  Also, the -quoting patch was implemented differently upstream
  There is now a umount.cifs executable and manpage
  We run autogen.sh as part of the build phase
  The testprns command is now gone
  libsmbclient now has a man page
- Include -bug106483 patch to close
  bz#106483 smbclient: -N negates the provided password, despite documentation
- Added the -warnings patch to quiet some compiler warnings.
- Removed many obsolete patches from CVS.

* Mon May 2 2005 Jay Fenlason <fenlason@redhat.com> 3.0.14a-2
- New upstream release.
- the -64bit-timestamps, -clitar, -establish_trust, user_rights_v1,
  winbind_find_dc_v2 patches are now obsolete.

* Thu Apr 7 2005 Jay Fenlason <fenlason@redhat.com> 3.0.13-2
- New upstream release
- add my -quoting patch, to fix swat with strings that contain
  html meta-characters, and to use correct quote characters in
  lists, closing bz#134310
- include the upstream winbindd_2k3sp1 patch
- include the -smbclient patch.
- include the -hang patch from upstream.

* Thu Mar 24 2005 Florian La Roche <laroche@redhat.com>
- add a "exit 0" to the postun of the main samba package

* Wed Mar  2 2005 Tomas Mraz <tmraz@redhat.com> 3.0.11-5
- rebuild with openssl-0.9.7e

* Thu Feb 24 2005 Jay Fenlason <fenlason@redhat.com> 3.0.11-4
- Use the updated filter-requires-samba.sh file, so we don't accidentally
  pick up a dependency on perl(Crypt::SmbHash)

* Fri Feb 18 2005 Jay Fenlason <fenlason@redhat.com> 3.0.11-3
- add -gcc4 patch to compile with gcc 4.
- remove the now obsolete -smbclient-kerberos.patch
- Include four upstream patches from
  http://samba.org/~jerry/patches/post-3.0.11/
  (Slightly modified the winbind_find_dc_v2 patch to apply easily with
  rpmbuild).

* Fri Feb 4 2005 Jay Fenlason <fenlason@redhat.com> 3.0.11-2
- include -smbspool patch to close bz#104136

* Wed Jan 12 2005 Jay Fenlason <fenlason@redhat.com> 3.0.10-4
- Update the -man patch to fix ntlm_auth.1 too.
- Move pam_smbpass.so to the -common package, so both the 32
  and 64-bit versions will be installed on multiarch platforms.
  This closes bz#143617
- Added new -delim patch to fix mount.cifs so it can accept
  passwords with commas in them (via environment or credentials
  file) to close bz#144198

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 3.0.10-3
- Rebuilt for new readline.

* Fri Dec 17 2004 Jay Fenlason <fenlason@redhat.com> 3.0.10-2
- New upstream release that closes CAN-2004-1154  bz#142544
- Include the -64bit patch from Nalin.  This closes bz#142873
- Update the -logfiles patch to work with 3.0.10
- Create /var/run/winbindd and make it part of the -common rpm to close
  bz#142242

* Mon Nov 22 2004 Jay Fenlason <fenlason@redhat.com> 3.0.9-2
- New upstream release.  This obsoletes the -secret patch.
  Include my changetrustpw patch to make "net ads changetrustpw" stop
  aborting.  This closes #134694
- Remove obsolete triggers for ancient samba versions.
- Move /var/log/samba to the -common rpm.  This closes #76628
- Remove the hack needed to get around the bad docs files in the
  3.0.8 tarball.
- Change the comment in winbind.init to point at the correct pidfile.
  This closes #76641

* Mon Nov 22 2004 Than Ngo <than@redhat.com> 3.0.8-4
- fix unresolved symbols in libsmbclient which caused applications
  such as KDE's konqueror to fail when accessing smb:// URLs. #139894

* Thu Nov 11 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-3.1
- Rescue the install.mount.smbfs patch from Juanjo Villaplana
  (villapla@si.uji.es) to prevent building the srpm from trashing your
  installed /usr/bin/smbmount

* Tue Nov 9 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-3
- Include the corrected docs tarball, and use it instead of the
  obsolete docs from the upstream 3.0.8 tarball.
- Update the logfiles patch to work with the updated docs.

* Mon Nov 8 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-2
- New upstream version fixes CAN-2004-0930.  This obsoletes the
  disable-sendfile, salt, signing-shortkey and fqdn patches.
- Add my <fenlason@redhat.com> ugly non-ascii-domain patch.
- Updated the pie patch for 3.0.8.
- Updated the logfiles patch for 3.0.8.

* Tue Oct 26 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-0.pre2
- New upstream version
- Add Nalin's signing-shortkey patch.

* Tue Oct 19 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-0.pre1.3
- disable the -salt patch, because it causes undefined references in
  libsmbclient that prevent gnome-vfs from building.

* Fri Oct 15 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-0.pre1.2
- Re-enable the x_fclose patch that was accidentally disabled
  in 3.0.8-0.pre1.1.  This closes #135832
- include Nalin's -fqdn and -salt patches.

* Wed Oct 13 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-0.pre1.1
- Include disable-sendfile patch to default "use sendfile" to "no".
  This closes #132779

* Wed Oct 6 2004 Jay Fenlason <fenlason@redhat.com>
- Include patch from Steven Lawrance (slawrance@yahoo.com) that modifies
  smbmnt to work with 32-bit uids.

* Mon Sep 27 2004 Jay Fenlason <fenlason@redhat.com> 3.0.8-0.pre1
- new upstream release.  This obsoletes the ldapsam_compat patches.

* Wed Sep 15 2004 Jay Fenlason <fenlason@redhat.com> 3.0.7-4
- Update docs section to not carryover the docs/manpages directory
  This moved many files from /usr/share/doc/samba-3.0.7/docs/* to
  /usr/share/doc/samba-3.0.7/*
- Modify spec file as suggested by Rex Dieter (rdieter@math.unl.edu)
  to correctly create libsmbclient.so.0 and to use %%_initrddir instead
  of rolling our own.  This closes #132642
- Add patch to default "use sendfile" to no, since sendfile appears to
  be broken
- Add patch from Volker Lendecke <vl@samba.org> to help make
  ldapsam_compat work again.
- Add patch from "Vince Brimhall" <vbrimhall@novell.com> for ldapsam_compat
  These two patches close bugzilla #132169

* Mon Sep 13 2004 Jay Fenlason <fenlason@redhat.com> 3.0.7-3
- Upgrade to 3.0.7, which fixes CAN-2004-0807 CAN-2004-0808
  This obsoletes the 3.0.6-schema patch.
- Update BuildRequires line to include openldap-devel openssl-devel
  and cups-devel

* Mon Aug 16 2004 Jay Fenlason <fenlason@redhat.com> 3.0.6-3
- New upstream version.
- Include post 3.0.6 patch from "Gerald (Jerry) Carter" <jerry@samba.org>
  to fix a duplicate in the LDAP schema.
- Include 64-bit timestamp patch from Ravikumar (rkumar@hp.com)
  to allow correct timestamp handling on 64-bit platforms and fix #126109.
- reenable the -pie patch.  Samba is too widely used, and too vulnerable
  to potential security holes to disable an important security feature
  like -pie.  The correct fix is to have the toolchain not create broken
  executables when programs compiled -pie are stripped.
- Remove obsolete patches.
- Modify this spec file to put libsmbclient.{a,so} in the right place on
  x86_64 machines.

* Thu Aug  5 2004 Jason Vas Dias <jvdias@redhat.com> 3.0.5-3
- Removed '-pie' patch - 3.0.5 uses -fPIC/-PIC, and the combination
- resulted in executables getting corrupt stacks, causing smbmnt to
- get a SIGBUS in the mount() call (bug 127420).

* Fri Jul 30 2004 Jay Fenlason <fenlason@redhat.com> 3.0.5-2
- Upgrade to 3.0.5, which is a regression from 3.0.5pre1 for a
  security fix.
- Include the 3.0.4-backport patch from the 3E branch.  This restores
  some of the 3.0.5pre1 and 3.0.5rc1 functionality.

* Tue Jul 20 2004 Jay Fenlason <fenlason@redhat.com> 3.0.5-0.pre1.1
- Backport base64_decode patche to close CAN-2004-0500
- Backport hash patch to close CAN-2004-0686
- use_authtok patch from Nalin Dahyabhai <nalin@redhat.com>
- smbclient-kerberos patch from Alexander Larsson <alexl@redhat.com>
- passwd patch uses "*" instead of "x" for "hashed" passwords for
  accounts created by winbind.  "x" means "password is in /etc/shadow" to
  brain-damaged pam_unix module.

* Fri Jul 2 2004 Jay Fenlason <fenlason@redhat.com> 3.0.5.0pre1.0
- New upstream version
- use %% { SOURCE1 } instead of a hardcoded path
- include -winbind patch from Gerald (Jerry) Carter (jerry@samba.org)
  https://bugzilla.samba.org/show_bug.cgi?id=1315
  to make winbindd work against Windows versions that do not have
  128 bit encryption enabled.
- Moved %%{_bindir}/net to the -common package, so that folks who just
  want to use winbind, etc don't have to install -client in order to
  "net join" their domain.
- New upstream version obsoletes the patches added in 3.0.3-5
- Remove smbgetrc.5 man page, since we don't ship smbget.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 4 2004 Jay Fenlason <fenlason@redhat.com> 3.0.3-5
- Patch to allow password changes from machines patched with
  Microsoft hotfix MS04-011.
- Include patches for https://bugzilla.samba.org/show_bug.cgi?id=1302
  and https://bugzilla.samba.org/show_bug.cgi?id=1309

* Thu Apr 29 2004 Jay Fenlason <fenlason@redhat.com> 3.0.3-4
- Samba 3.0.3 released.

* Wed Apr 21 2004 jay Fenlason <fenlason@redhat.com> 3.0.3-3.rc1
- New upstream version
- updated spec file to make libsmbclient.so executable.  This closes
  bugzilla #121356

* Mon Apr 5 2004 Jay Fenlason <fenlason@redhat.com> 3.0.3-2.pre2
- New upstream version
- Updated configure line to remove --with-fhs and to explicitly set all
  the directories that --with-fhs was setting.  We were overriding most of
  them anyway.  This closes #118598

* Mon Mar 15 2004 Jay Fenlason <fenlason@redhat.com> 3.0.3-1.pre1
- New upstream version.
- Updated -pie and -logfiles patches for 3.0.3pre1
- add krb5-devel to buildrequires, fixes #116560
- Add patch from Miloslav Trmac (mitr@volny.cz) to allow non-root to run
  "service smb status".  This fixes #116559

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 16 2004 Jay Fenlason <fenlason@redhat.com> 3.0.2a-1
- Upgrade to 3.0.2a

* Mon Feb 16 2004 Karsten Hopp <karsten@redhat.de> 3.0.2-7
- fix ownership in -common package

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Jay Fenlason <fenlason@redhat.com>
- Change all requires lines to list an explicit epoch.  Closes #102715
- Add an explicit Epoch so that %%{epoch} is defined.

* Mon Feb 9 2004 Jay Fenlason <fenlason@redhat.com> 3.0.2-5
- New upstream version: 3.0.2 final includes security fix for #114995
  (CAN-2004-0082)
- Edit postun script for the -common package to restart winbind when
  appropriate.  Fixes bugzilla #114051.

* Mon Feb 2 2004 Jay Fenlason <fenlason@redhat.com> 3.0.2-3rc2
- add %%dir entries for %%{_libdir}/samba and %%{_libdir}/samba/charset
- Upgrade to new upstream version
- build mount.cifs for the new cifs filesystem in the 2.6 kernel.

* Mon Jan 19 2004 Jay Fenlason <fenlason@redhat.com> 3.0.2-1rc1
- Upgrade to new upstream version

* Wed Dec 17 2003 Felipe Alfaro Solana <felipe_alfaro@linuxmail.org> 3.0.1-1
- Update to 3.0.1
- Removed testparm patch as it's already merged
- Removed Samba.7* man pages
- Fixed .buildroot patch
- Fixed .pie patch
- Added new /usr/bin/tdbdump file

* Thu Sep 25 2003 Jay Fenlason <fenlason@redhat.com> 3.0.0-15
- New 3.0.0 final release
- merge nmbd-netbiosname and testparm patches from 3E branch
- updated the -logfiles patch to work against 3.0.0
- updated the pie patch
- update the VERSION file during build
- use make -j if avaliable
- merge the winbindd_privileged change from 3E
- merge the "rm /usr/lib" patch that allows Samba to build on 64-bit
  platforms despite the broken Makefile

* Mon Aug 18 2003 Jay Fenlason <fenlason@redhat.com>
- Merge from samba-3E-branch after samba-3.0.0rc1 was released

* Wed Jul 23 2003 Jay Fenlason <fenlason@redhat.com> 3.0.0-3beta3
- Merge from 3.0.0-2beta3.3E
- (Correct log file names (#100981).)
- (Fix pidfile directory in samab.log)
- (Remove obsolete samba-3.0.0beta2.tar.bz2.md5 file)
- (Move libsmbclient to the -common package (#99449))

* Sun Jun 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.8a-4
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Jay Fenlason <fenlason@redhat.com> 2.2.8a-2
- add libsmbclient.so for gnome-vfs-extras
- Edit specfile to specify /var/run for pid files
- Move /tmp/.winbindd/socket to /var/run/winbindd/socket

* Wed May 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ldconfig calls

* Thu Apr 24 2003 Jay Fenlason <fenlason@redhat.com> 2.2.8a-1
- upgrade to 2.2.8a
- remove old .md5 files
- add "pid directory = /var/run" to the smb.conf file.  Fixes #88495
- Patch from jra@dp.samba.org to fix a delete-on-close regression

* Mon Mar 24 2003 Jay Fenlason <fenlason@redhat.com> 2.2.8-0
- Upgrade to 2.2.8
- removed commented out patches.
- removed old patches and .md5 files from the repository.
- remove duplicate /sbin/chkconfig --del winbind which causes
  warnings when removing samba.
- Fixed minor bug in smbprint that causes it to fail when called with
  more than 10 parameters: the accounting file (and spool directory
  derived from it) were being set wrong due to missing {}.  This closes
  bug #86473.
- updated smb.conf patch, includes new defaults to close bug #84822.

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 20 2003 Jonathan Blandford <jrb@redhat.com> 2.2.7a-5
- remove swat.desktop file

* Thu Feb 20 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.7a-4
- relink libnss_wins.so with SHLD="%%{__cc} -lnsl" to force libnss_wins.so to
  link with libnsl, avoiding unresolved symbol errors on functions in libnsl

* Mon Feb 10 2003 Jay Fenlason <fenlason@redhat.com> 2.2.7a-3
- edited spec file to put .so files in the correct directories
  on 64-bit platforms that have 32-bit compatability issues
  (sparc64, x86_64, etc).  This fixes bugzilla #83782.
- Added samba-2.2.7a-error.patch from twaugh.  This fixes
  bugzilla #82454.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Jay Fenlason <fenlason@redhat.com> 2.2.7a-1
- Update to 2.2.7a
- Change default printing system to CUPS
- Turn on pam_smbpass
- Turn on msdfs

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.2.7-5
- use internal dep generator.

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 2.2.7-4
- don't use rpms internal dep generator

* Mon Dec 02 2002 Elliot Lee <sopwith@redhat.com> 2.2.7-3
- Fix missing doc files.
- Fix multilib issues

* Wed Nov 20 2002 Bill Nottingham <notting@redhat.com> 2.2.7-2
- update to 2.2.7
- add patch for LFS in smbclient (<tcallawa@redhat.com>)

* Wed Aug 28 2002 Trond Eivind Glomsød <teg@redhat.com> 2.2.5-10
- logrotate fixes (#65007)

* Mon Aug 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-9
- /usr/lib was used in place of %%{_libdir} in three locations (#72554)

* Mon Aug  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-8
- Initscript fix (#70720)

* Fri Jul 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-7
- Enable VFS support and compile the "recycling" module (#69796)
- more selective includes of the examples dir

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-6
- Fix the lpq parser for better handling of LPRng systems (#69352)

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-5
- desktop file fixes (#69505)

* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-4
- Enable ACLs

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-3
- Make it not depend on Net::LDAP - those are doc files and examples

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-1
- 2.2.5

* Fri Jun 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-5
- Move the post/preun of winbind into the -common subpackage,
  where the script is (#66128)

* Tue Jun  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-4
- Fix pidfile locations so it runs properly again (2.2.4
  added a new directtive - #65007)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-2
- Fix #64804

* Thu May  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-1
- 2.2.4
- Removed some zero-length and CVS internal files
- Make it build

* Wed Apr 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-6
- Don't use /etc/samba.d in smbadduser, it should be /etc/samba

* Thu Apr  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-5
- Add libsmbclient.a w/headerfile for KDE (#62202)

* Tue Mar 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-4
- Make the logrotate script look the correct place for the pid files

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.2.3a-3
- include interfaces.o in pam_smbpass.so, which needs symbols from interfaces.o
  (patch posted to samba-list by Ilia Chipitsine)

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-2
- Rebuild

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-1
- 2.2.3a

* Mon Feb  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3-1
- 2.2.3

* Thu Nov 29 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-8
- New pam configuration file for samba

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-7
- Enable PAM session controll and password sync

* Tue Nov 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-6
- Move winbind files to samba-common. Add separate initscript for
  winbind
- Fixes for winbind - protect global variables with mutex, use
  more secure getenv

* Thu Nov  8 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-5
- Teach smbadduser about "getent passwd"
- Fix more pid-file references
- Add (conditional) winbindd startup to the initscript, configured in
  /etc/sysconfig/samba

* Wed Nov  7 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-4
- Fix pid-file reference in logrotate script
- include pam and nss modules for winbind

* Mon Nov  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-3
- Add "--with-utmp" to configure options (#55372)
- Include winbind, pam_smbpass.so, rpcclient and smbcacls
- start using /var/cache/samba, we need to keep state and there is
  more than just locks involved

* Sat Nov 03 2001 Florian La Roche <Florian.LaRoche@redhat.de> 2.2.2-2
- add "reload" to the usage string in the startup script

* Mon Oct 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-1
- 2.2.2

* Tue Sep 18 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1a-5
- Add patch from Jeremy Allison to fix IA64 alignment problems (#51497)

* Mon Aug 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Don't include smbpasswd in samba, it's in samba-common (#51598)
- Add a disabled "obey pam restrictions" statement - it's not
  active, as we use encrypted passwords, but if the admin turns
  encrypted passwords off the choice is available. (#31351)

* Wed Aug  8 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use /var/cache/samba instead of /var/lock/samba
- Remove "domain controller" keyword from smb.conf, it's
  deprecated (from #13704)
- Sync some examples with smb.conf.default
- Fix password synchronization (#16987)

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Tweaks of BuildRequires (#49581)

* Wed Jul 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.1a bugfix release

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.1, which should work better for XP

* Sat Jun 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.0a security fix
- Mark lograte and pam configuration files as noreplace

* Fri Jun 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add the /etc/samba directory to samba-common

* Thu Jun 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add improvements to the smb.conf as suggested in #16931

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- (these changes are from the non-head version)
- Don't include /usr/sbin/samba, it's the same as the initscript
- unset TMPDIR, as samba can't write into a TMPDIR owned
  by root (#41193)
- Add pidfile: lines for smbd and nmbd and a config: line
  in the initscript  (#15343)
- don't use make -j
- explicitly include /usr/share/samba, not just the files in it

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- mount.smb/mount.smbfs go in /sbin, *not* %%{_sbindir}

* Fri Jun  8 2001 Preston Brown <pbrown@redhat.com>
- enable encypted passwords by default

* Thu Jun  7 2001 Helge Deller <hdeller@redhat.de>
- build as 2.2.0-1 release
- skip the documentation-directories docbook, manpages and yodldocs
- don't include *.sgml documentation in package
- moved codepage-directory to /usr/share/samba/codepages
- make it compile with glibc-2.2.3-10 and kernel-headers-2.4.2-2

* Mon May 21 2001 Helge Deller <hdeller@redhat.de>
- updated to samba 2.2.0
- moved codepages to %%{_datadir}/samba/codepages
- use all available CPUs for building rpm packages
- use %%{_xxx} defines at most places in spec-file
- "License:" replaces "Copyright:"
- dropped excludearch sparc
- de-activated japanese patches 100 and 200 for now
  (they need to be fixed and tested wth 2.2.0)
- separated swat.desktop file from spec-file and added
  german translations
- moved /etc/sysconfig/samba to a separate source-file
- use htmlview instead of direct call to netscape in
  swat.desktop-file

* Mon May  7 2001 Bill Nottingham <notting@redhat.com>
- device-remove security fix again (<tridge@samba.org>)

* Fri Apr 20 2001 Bill Nottingham <notting@redhat.com>
- fix tempfile security problems, officially (<tridge@samba.org>)
- update to 2.0.8

* Sun Apr  8 2001 Bill Nottingham <notting@redhat.com>
- turn of SSL, kerberos

* Thu Apr  5 2001 Bill Nottingham <notting@redhat.com>
- fix tempfile security problems (patch from <Marcus.Meissner@caldera.de>)

* Thu Mar 29 2001 Bill Nottingham <notting@redhat.com>
- fix quota support, and quotas with the 2.4 kernel (#31362, #33915)

* Mon Mar 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the PAM code some more to try to do a setcred() after initgroups()
- pull in all of the optflags on i386 and sparc
- don't explicitly enable Kerberos support -- it's only used for password
  checking, and if PAM is enabled it's a no-op anyway

* Mon Mar  5 2001 Tim Waugh <twaugh@redhat.com>
- exit successfully from preun script (bug #30644).

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Wed Feb 14 2001 Bill Nottingham <notting@redhat.com>
- updated japanese stuff (#27683)

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix trigger (#26859)

* Wed Feb  7 2001 Bill Nottingham <notting@redhat.com>
- add i18n support, japanese patch (#26253)

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n improvements in initscript (#26537)

* Wed Jan 31 2001 Bill Nottingham <notting@redhat.com>
- put smbpasswd in samba-common (#25429)

* Wed Jan 24 2001 Bill Nottingham <notting@redhat.com>
- new i18n stuff

* Sun Jan 21 2001 Bill Nottingham <notting@redhat.com>
- rebuild

* Thu Jan 18 2001 Bill Nottingham <notting@redhat.com>
- i18n-ize initscript
- add a sysconfig file for daemon options (#23550)
- clarify smbpasswd man page (#23370)
- build with LFS support (#22388)
- avoid extraneous pam error messages (#10666)
- add Urban Widmark's bug fixes for smbmount (#19623)
- fix setgid directory modes (#11911)
- split swat into subpackage (#19706)

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- set a default CA certificate path in smb.conf (#19010)
- require openssl >= 0.9.5a-20 to make sure we have a ca-bundle.crt file

* Mon Oct 16 2000 Bill Nottingham <notting@redhat.com>
- fix swat only_from line (#18726, others)
- fix attempt to write outside buildroot on install (#17943)

* Mon Aug 14 2000 Bill Nottingham <notting@redhat.com>
- add smbspool back in (#15827)
- fix absolute symlinks (#16125)

* Sun Aug 6 2000 Philipp Knirsch <pknirsch@redhat.com>
- bugfix for smbadduser script (#15148)

* Mon Jul 31 2000 Matt Wilson <msw@redhat.com>
- patch configure.ing (patch11) to disable cups test
- turn off swat by default

* Fri Jul 28 2000 Bill Nottingham <notting@redhat.com>
- fix condrestart stuff

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- add copytruncate to logrotate file (#14360)
- fix init script (#13708)

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back
- remove 'Using Samba' book from %%doc
- move stuff to /etc/samba (#13708)
- default configuration tweaks (#13704)
- some logrotate tweaks

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- fix logrotate script (#13698)

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- fix initscripts req (prereq /etc/init.d)

* Wed Jul 5 2000 Than Ngo <than@redhat.de>
- add initdir macro to handle the initscript directory
- add a new macro to handle /etc/pam.d/system-auth

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable Kerberos 5 and SSL support
- patch for duplicate profile.h headers

* Thu Jun 29 2000 Bill Nottingham <notting@redhat.com>
- fix init script

* Tue Jun 27 2000 Bill Nottingham <notting@redhat.com>
- rename samba logs (#11606)

* Mon Jun 26 2000 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Jun 16 2000 Bill Nottingham <notting@redhat.com>
- configure the swat stuff usefully
- re-integrate some specfile tweaks that got lost somewhere

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- rebuild to get rid of cups dependency

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak logrotate configurations to use the PID file in /var/lock/samba

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- rebuild in new environment

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- change PAM setup to use system-auth

* Mon May  8 2000 Bill Nottingham <notting@redhat.com>
- fixes for ia64

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- switch to %%configure

* Wed Apr 26 2000 Nils Philippsen <nils@redhat.de>
- version 2.0.7

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- simplify preun

* Thu Mar 16 2000 Bill Nottingham <notting@redhat.com>
- fix yp_get_default_domain in autoconf
- only link against readline for smbclient
- fix log rotation (#9909)

* Fri Feb 25 2000 Bill Nottingham <notting@redhat.com>
- fix trigger, again.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- fix trigger.

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- turn on quota support

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fox dependencies
- man pages are compressed

* Fri Jan 21 2000 Bill Nottingham <notting@redhat.com>
- munge post scripts slightly

* Wed Jan 19 2000 Bill Nottingham <notting@redhat.com>
- turn on mmap again. Wheee.
- ship smbmount on alpha

* Mon Dec  6 1999 Bill Nottingham <notting@redhat.com>
- turn off mmap. ;)

* Wed Dec  1 1999 Bill Nottingham <notting@redhat.com>
- change /var/log/samba to 0700
- turn on mmap support

* Thu Nov 11 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.6

* Fri Oct 29 1999 Bill Nottingham <notting@redhat.com>
- add a %%defattr for -common

* Tue Oct  5 1999 Bill Nottingham <notting@redhat.com>
- shift some files into -client
- remove /home/samba from package.

* Tue Sep 28 1999 Bill Nottingham <notting@redhat.com>
- initscript oopsie. killproc <name> -HUP, not other way around.

* Sun Sep 26 1999 Bill Nottingham <notting@redhat.com>
- script cleanups. Again.

* Wed Sep 22 1999 Bill Nottingham <notting@redhat.com>
- add a patch to fix dropped reconnection attempts

* Mon Sep  6 1999 Jeff Johnson <jbj@redhat.com>
- use cp rather than mv to preserve /etc/services perms (#4938 et al).
- use mktemp to generate /etc/tmp.XXXXXX file name.
- add prereqs on sed/mktemp/killall (need to move killall to /bin).
- fix trigger syntax (i.e. "samba < 1.9.18p7" not "samba < samba-1.9.18p7")

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- sed "s|nawk|gawk|" /usr/bin/convert_smbpasswd

* Sat Aug 21 1999 Bill Nottingham <notting@redhat.com>
- fix typo in mount.smb

* Fri Aug 20 1999 Bill Nottingham <notting@redhat.com>
- add a %%trigger to work around (sort of) broken scripts in
  previous releases

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Mon Aug  9 1999 Bill Nottingham <notting@redhat.com>
- add domain parsing to mount.smb

* Fri Aug  6 1999 Bill Nottingham <notting@redhat.com>
- add a -common package, shuffle files around.

* Fri Jul 23 1999 Bill Nottingham <notting@redhat.com>
- add a chmod in %%postun so /etc/services & inetd.conf don't become unreadable

* Wed Jul 21 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.5
- fix mount.smb - smbmount options changed again.........
- fix postun. oops.
- update some stuff from the samba team's spec file.

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- split off clients into separate package
- don't run samba by default

* Mon Jun 14 1999 Bill Nottingham <notting@redhat.com>
- fix one problem with mount.smb script
- fix smbpasswd on sparc with a really ugly kludge

* Thu Jun 10 1999 Dale Lovelace <dale@redhat.com>
- fixed logrotate script

* Tue May 25 1999 Bill Nottingham <notting@redhat.com>
- turn of 64-bit locking on 32-bit platforms

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- so many releases, so little time
- explicitly uncomment 'printing = bsd' in sample config

* Tue May 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.4a
- fix mount.smb arg ordering

* Fri Apr 16 1999 Bill Nottingham <notting@redhat.com>
- go back to stop/start for restart (-HUP didn't work in testing)

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- add a mount.smb to make smb mounting a little easier.
- smb filesystems apparently don't work on alpha. Oops.

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- always create codepages

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- updated init script to use graceful restart (not stop/start)

* Tue Mar  9 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.3

* Thu Feb 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.2

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- swat swat

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- fix bash2 breakage in post script

* Fri Feb  5 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.0

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- make sure all binaries are stripped

* Thu Sep 17 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.18p10.
- fix %%triggerpostun.

* Tue Jul 07 1998 Erik Troan <ewt@redhat.com>
- updated postun triggerscript to check $0
- clear /etc/codepages from %%preun instead of %%postun

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
- made the %%postun script a tad less agressive; no reason to remove
  the logs or lock file (after all, if the lock file is still there,
  samba is still running)
- the %%postun and %%preun should only exectute if this is the final
  removal
- migrated %%triggerpostun from Red Hat's samba package to work around
  packaging problems in some Red Hat samba releases

* Sun Apr 26 1998 John H Terpstra <jht@samba.anu.edu.au>
- minor tidy up in preparation for release of 1.9.18p5
- added findsmb utility from SGI package

* Wed Mar 18 1998 John H Terpstra <jht@samba.anu.edu.au>
- Updated version and codepage info.
- Release to test name resolve order

* Sat Jan 24 1998 John H Terpstra <jht@samba.anu.edu.au>
- Many optimisations (some suggested by Manoj Kasichainula <manojk@io.com>
- Use of chkconfig in place of individual symlinks to /etc/rc.d/init/smb
- Compounded make line
- Updated smb.init restart mechanism
- Use compound mkdir -p line instead of individual calls to mkdir
- Fixed smb.conf file path for log files
- Fixed smb.conf file path for incoming smb print spool directory
- Added a number of options to smb.conf file
- Added smbadduser command (missed from all previous RPMs) - Doooh!
- Added smbuser file and smb.conf file updates for username map

## END: Generated by rpmautospec
