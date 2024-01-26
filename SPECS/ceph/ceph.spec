#disable debuginfo because ceph-debuginfo rpm is too large
%define debug_package %{nil}
%global _python_bytecompile_extra 1

Summary:        User space components of the Ceph file system
Name:           ceph
Version:        18.2.0
Release:        1%{?dist}
License:        LGPLv2 and LGPLv3 and CC-BY-SA and GPLv2 and Boost and BSD and MIT and Public Domain and GPLv3 and ASL-2.0
URL:            https://ceph.io/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://download.ceph.com/tarballs/%{name}-%{version}.tar.gz

#
# Copyright (C) 2004-2019 The Ceph Project Developers. See COPYING file
# at the top-level directory of this distribution and at
# https://github.com/ceph/ceph/blob/master/COPYING
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon.
#
# This file is under the GNU Lesser General Public License, version 2.1
#
# Please submit bugfixes or comments via http://tracker.ceph.com/
#

#################################################################################
# Mariner conditional build flags and macro definitions
#################################################################################
%bcond_with amqp_endpoint
%bcond_with ceph_test_package
%bcond_with cephfs_java
%bcond_with cmake_verbose_logging
%bcond_with kafka_endpoint
%bcond_with lttng
%bcond_with make_check
%bcond_with mgr_diskprediction
%bcond_with ocf
%bcond_with seastar
%bcond_with selinux
%bcond_with tcmalloc
%bcond_without libradosstriper

%define debug_package %{nil}

%if %{with selinux}
%{!?_selinux_policy_version: %global _selinux_policy_version 0.0.0}
%endif

%{!?_udevrulesdir: %global _udevrulesdir /lib/udev/rules.d}
%{!?tmpfiles_create: %global tmpfiles_create systemd-tmpfiles --create}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %global python3_version 3}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")


# disable dwz which compresses the debuginfo
%global _find_debuginfo_dwz_opts %{nil}


#################################################################################
# Main package dependencies
#################################################################################
Requires:       ceph-osd = %{version}-%{release}
Requires:       ceph-mds = %{version}-%{release}
Requires:       ceph-mgr = %{version}-%{release}
Requires:       ceph-mon = %{version}-%{release}
Requires(post): binutils
Requires:       systemd

BuildRequires:  libevent
BuildRequires:  libevent-devel
BuildRequires:  cryptsetup
BuildRequires:  cryptsetup-devel
BuildRequires:  expat-devel
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  gdbm
BuildRequires:  gperf
BuildRequires:  icu-devel
BuildRequires:  keyutils-devel
BuildRequires:  leveldb-devel > 1.2
BuildRequires:  libaio-devel
BuildRequires:  lua-devel
BuildRequires:  util-linux-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  curl-devel
BuildRequires:  libibverbs-devel
BuildRequires:  libnl3-devel
BuildRequires:  liboath-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  lsb-release
BuildRequires:  lz4-devel >= 1.7
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  nss-devel
BuildRequires:  parted
BuildRequires:  patch
BuildRequires:  perl
BuildRequires:  pkg-config
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-prettytable
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinxcontrib-websupport
BuildRequires:  python%{python3_pkgversion}-xml
BuildRequires:  snappy-devel
BuildRequires:  sudo
BuildRequires:  systemd-devel
BuildRequires:  util-linux
BuildRequires:  valgrind
BuildRequires:  which
BuildRequires:  xfsprogs
BuildRequires:  xfsprogs-devel
BuildRequires:  xmlstarlet
BuildRequires:  yasm

BuildRequires:  CUnit-devel
BuildRequires:  boost
BuildRequires:  cmake > 3.5
BuildRequires:  librdmacm-devel
BuildRequires:  mariner-rpm-macros
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  procps-ng

%if 0%{with cephfs_java}
BuildRequires:  java-devel
BuildRequires:  sharutils
%endif

%if 0%{with selinux}
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
%endif

%if 0%{with tcmalloc}
BuildRequires:  gperftools-devel >= 2.6.1
%endif

%if 0%{with amqp_endpoint}
BuildRequires:  librabbitmq-devel
%endif

%if 0%{with kafka_endpoint}
BuildRequires:  librdkafka-devel
%endif

%if 0%{with make_check}
BuildRequires:  jq
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libuuid-devel
BuildRequires:  python%{python3_pkgversion}-bcrypt
BuildRequires:  python%{python3_pkgversion}-cherrypy
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-dateutil
BuildRequires:  python%{python3_pkgversion}-jwt
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-pecan
BuildRequires:  python%{python3_pkgversion}-pyOpenSSL
BuildRequires:  python%{python3_pkgversion}-pyOpenSSL
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-routes
BuildRequires:  python%{python3_pkgversion}-scipy
BuildRequires:	python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-virtualenv
BuildRequires:  python%{python3_pkgversion}-werkzeug
BuildRequires:  socat
BuildRequires:  xmlsec1
BuildRequires:  xmlsec1-devel
BuildRequires:  xmlsec1-openssl
BuildRequires:  xmlsec1-openssl-devel

%ifarch x86_64
BuildRequires:  xmlsec1-nss
%endif
%endif

%if 0%{with seastar}
BuildRequires:  gcc-toolset-9-gcc-c++ >= 9.2.1-2.3
BuildRequires:  c-ares-devel
BuildRequires:  cryptopp-devel
BuildRequires:  fmt-devel
BuildRequires:  gcc-toolset-9-annobin
BuildRequires:  gcc-toolset-9-libasan-devel
BuildRequires:  gcc-toolset-9-libatomic-devel
BuildRequires:  gcc-toolset-9-libubsan-devel
BuildRequires:  gnutls-devel
BuildRequires:  hwloc-devel
BuildRequires:  libasan
BuildRequires:  libatomic
BuildRequires:  libpciaccess-devel
BuildRequires:  libubsan
BuildRequires:  lksctp-tools-devel
BuildRequires:  numactl-devel
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel
BuildRequires:  ragel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  yaml-cpp-devel
%endif

# lttng and babeltrace for rbd-replay-prep
%if %{with lttng}
BuildRequires:  libbabeltrace-devel
BuildRequires:  lttng-ust-devel
%endif


%description
Ceph is a massively scalable, open-source, distributed storage system that runs
on commodity hardware and delivers object, block and file system storage.


#################################################################################
# subpackage definitions
#################################################################################

%package base
Summary:       Ceph Base Package
Provides:      ceph-test:/usr/bin/ceph-kvstore-tool
Requires:      ceph-common = %{version}-%{release}
Requires:      librbd1 = %{version}-%{release}
Requires:      librados2 = %{version}-%{release}
Requires:      libcephfs2 = %{version}-%{release}
Requires:      librgw2 = %{version}-%{release}
%if 0%{with selinux}
Requires:      ceph-selinux = %{version}-%{release}
%endif
Requires:      cryptsetup
Requires:      e2fsprogs
Requires:      findutils
Requires:      grep
Requires:      logrotate
Requires:      parted
Requires:      psmisc
Requires:      python%{python3_pkgversion}-setuptools
Requires:      util-linux
Requires:      xfsprogs
Requires:      which
# The following is necessary due to tracker 36508 and can be removed once the
# associated upstream bugs are resolved.
%if 0%{with tcmalloc}
Requires:      gperftools-libs >= 2.6.1
%endif
%description base
Base is the package that includes all the files shared amongst ceph servers

%package -n cephadm
Summary:        Utility to bootstrap Ceph clusters
Requires:       lvm2
Requires:       python%{python3_pkgversion}
%description -n cephadm
Utility to bootstrap a Ceph cluster and manage Ceph daemons deployed
with systemd and podman.

%package -n ceph-common
Summary:    Ceph Common
Requires:   librbd1 = %{version}-%{release}
Requires:   librados2 = %{version}-%{release}
Requires:   libcephfs2 = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rados = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rbd = %{version}-%{release}
Requires:   python%{python3_pkgversion}-cephfs = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rgw = %{version}-%{release}
Requires:   python%{python3_pkgversion}-ceph-argparse = %{version}-%{release}
Requires:   python%{python3_pkgversion}-ceph-common = %{version}-%{release}
Requires:   python%{python3_pkgversion}-prettytable
%if 0%{with libradosstriper}
Requires:   libradosstriper1 = %{version}-%{release}
%endif
%{?systemd_requires}
%description -n ceph-common
Common utilities to mount and interact with a ceph storage cluster.
Comprised of files that are common to Ceph clients and servers.

%package mds
Summary:    Ceph Metadata Server Daemon
Requires:   ceph-base = %{version}-%{release}
%description mds
ceph-mds is the metadata server daemon for the Ceph distributed file system.
One or more instances of ceph-mds collectively manage the file system
namespace, coordinating access to the shared OSD cluster.

%package mon
Summary:    Ceph Monitor Daemon
Provides:   ceph-test:/usr/bin/ceph-monstore-tool
Requires:   ceph-base = %{version}-%{release}

%description mon
ceph-mon is the cluster monitor daemon for the Ceph distributed file
system. One or more instances of ceph-mon form a Paxos part-time
parliament cluster that provides extremely reliable and durable storage
of cluster membership, configuration, and state.

%package mgr
Summary:        Ceph Manager Daemon
Requires:       ceph-base = %{version}-%{release}
Requires:       ceph-mgr-modules-core = %{version}-%{release}

%description mgr
ceph-mgr enables python modules that provide services (such as the REST
module derived from Calamari) and expose CLI hooks.  ceph-mgr gathers
the cluster maps, the daemon metadata, and performance counters, and
exposes all these to the python modules.

%package mgr-dashboard
Summary:        Ceph Dashboard
BuildArch:      noarch
Requires:       ceph-mgr = %{version}-%{release}
Requires:       ceph-grafana-dashboards = %{version}-%{release}
Requires:       ceph-prometheus-alerts = %{version}-%{release}
Requires:       python%{python3_pkgversion}-cherrypy
Requires:       python%{python3_pkgversion}-jwt
Requires:       python%{python3_pkgversion}-routes
Requires:       python%{python3_pkgversion}-werkzeug

%description mgr-dashboard
ceph-mgr-dashboard is a manager module, providing a web-based application
to monitor and manage many aspects of a Ceph cluster and related components.
See the Dashboard documentation at http://docs.ceph.com/ for details and a
detailed feature overview.

%if %{with mgr_diskprediction}
%package mgr-diskprediction-local
Summary:        Ceph Manager module for predicting disk failures
BuildArch:      noarch
Requires:       ceph-mgr = %{version}-%{release}
Requires:       python%{python3_pkgversion}-numpy
Requires:       python%{python3_pkgversion}-scikit-learn
Requires:       python%{python3_pkgversion}-scipy

%description mgr-diskprediction-local
ceph-mgr-diskprediction-local is a ceph-mgr module that tries to predict
disk failures using local algorithms and machine-learning databases.
%endif

%package mgr-modules-core
Summary:        Ceph Manager modules which are always enabled
BuildArch:      noarch
Requires:       python%{python3_pkgversion}-bcrypt
Requires:       python%{python3_pkgversion}-pecan
Requires:       python%{python3_pkgversion}-pyOpenSSL
Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-dateutil
Requires:       python%{python3_pkgversion}-cherrypy
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-werkzeug

%description mgr-modules-core
ceph-mgr-modules-core provides a set of modules which are always
enabled by ceph-mgr.

%package mgr-rook
BuildArch:      noarch
Summary:        Ceph Manager module for Rook-based orchestration
Requires:       ceph-mgr = %{version}-%{release}
Requires:       python%{python3_pkgversion}-kubernetes
Requires:       python%{python3_pkgversion}-jsonpatch

%description mgr-rook
ceph-mgr-rook is a ceph-mgr module for orchestration functions using
a Rook backend.

%package mgr-k8sevents
BuildArch:      noarch
Summary:        Ceph Manager module to orchestrate ceph-events to kubernetes' events API
Requires:       ceph-mgr = %{version}-%{release}
Requires:       python%{python3_pkgversion}-kubernetes

%description mgr-k8sevents
ceph-mgr-k8sevents is a ceph-mgr module that sends every ceph-events
to kubernetes' events API

%package mgr-cephadm
Summary:        Ceph Manager module for cephadm-based orchestration
BuildArch:      noarch
Requires:       ceph-mgr = %{version}-%{release}
Requires:       python%{python3_pkgversion}-remoto
Requires:       cephadm = %{version}-%{release}
Requires:       openssh-clients
Requires:       python%{python3_pkgversion}-jinja2

%description mgr-cephadm
ceph-mgr-cephadm is a ceph-mgr module for orchestration functions using
the integrated cephadm deployment tool management operations.

%package fuse
Summary:    Ceph fuse-based client
Requires:   fuse
Requires:   python%{python3_pkgversion}

%description fuse
FUSE based client for Ceph distributed network file system

%package -n rbd-fuse
Summary:    Ceph fuse-based client
Requires:   librados2 = %{version}-%{release}
Requires:   librbd1 = %{version}-%{release}

%description -n rbd-fuse
FUSE based client to map Ceph rbd images to files

%package -n rbd-mirror
Summary:    Ceph daemon for mirroring RBD images
Requires:   ceph-base = %{version}-%{release}
Requires:   librados2 = %{version}-%{release}
Requires:   librbd1 = %{version}-%{release}

%description -n rbd-mirror
Daemon for mirroring RBD images between Ceph clusters, streaming
changes asynchronously.

%package immutable-object-cache
Summary:    Ceph daemon for immutable object cache
Requires:   librados2 = %{version}-%{release}

%description immutable-object-cache
Daemon for immutable object cache.

%package -n rbd-nbd
Summary:    Ceph RBD client base on NBD
Requires:   librados2 = %{version}-%{release}
Requires:   librbd1 = %{version}-%{release}

%description -n rbd-nbd
NBD based client to map Ceph rbd images to local device

%package radosgw
Summary:    Rados REST gateway
Requires:   ceph-base = %{version}-%{release}
%if 0%{with selinux}
Requires:   ceph-selinux = %{version}-%{release}
%endif
Requires:   librados2 = %{version}-%{release}
Requires:   librgw2 = %{version}-%{release}
Requires:   mailcap

%description radosgw
RADOS is a distributed object store used by the Ceph distributed
storage system.  This package provides a REST gateway to the
object store that aims to implement a superset of Amazon's S3
service as well as the OpenStack Object Storage ("Swift") API.

%if %{with ocf}
%package resource-agents
Summary:    OCF-compliant resource agents for Ceph daemons
Requires:   ceph-base = %{version}
Requires:   resource-agents

%description resource-agents
Resource agents for monitoring and managing Ceph daemons
under Open Cluster Framework (OCF) compliant resource
managers such as Pacemaker.
%endif

%package osd
Summary:    Ceph Object Storage Daemon
Provides:   ceph-test:/usr/bin/ceph-osdomap-tool
Requires:   ceph-base = %{version}-%{release}
Requires:   lvm2
Requires:   sudo
Requires:   libstoragemgmt

%description osd
ceph-osd is the object storage daemon for the Ceph distributed file
system.  It is responsible for storing objects on a local file system
and providing access to them over the network.

%if 0%{with seastar}
%package crimson-osd
Summary:    Ceph Object Storage Daemon (crimson)
Requires:   ceph-osd = %{version}-%{release}

%description crimson-osd
crimson-osd is the object storage daemon for the Ceph distributed file
system.  It is responsible for storing objects on a local file system
and providing access to them over the network.
%endif

%package -n librados2
Summary:    RADOS distributed object store client library

%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librados-devel
Summary:    RADOS headers
Requires:   librados2 = %{version}-%{release}
Provides:   librados2-devel = %{version}-%{release}
Obsoletes:  librados2-devel < %{version}-%{release}

%description -n librados-devel
This package contains C libraries and headers needed to develop programs
that use RADOS object store.

%package -n libradospp-devel
Summary:    RADOS headers
Requires:   librados2 = %{version}-%{release}
Requires:   librados-devel = %{version}-%{release}

%description -n libradospp-devel
This package contains C++ libraries and headers needed to develop programs
that use RADOS object store.

%package -n librgw2
Summary:    RADOS gateway client library
Requires:   librados2 = %{version}-%{release}

%description -n librgw2
This package provides a library implementation of the RADOS gateway
(distributed object store with S3 and Swift personalities).

%package -n librgw-devel
Summary:    RADOS gateway client library
Requires:   librados-devel = %{version}-%{release}
Requires:   librgw2 = %{version}-%{release}
Provides:   librgw2-devel = %{version}-%{release}
Obsoletes:  librgw2-devel < %{version}-%{release}

%description -n librgw-devel
This package contains libraries and headers needed to develop programs
that use RADOS gateway client library.

%package -n python%{python3_pkgversion}-rgw
Summary:    Python 3 libraries for the RADOS gateway
Requires:   librgw2 = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rados = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-rgw}
Provides:   python-rgw = %{version}-%{release}
Obsoletes:  python-rgw < %{version}-%{release}

%description -n python%{python3_pkgversion}-rgw
This package contains Python 3 libraries for interacting with Cephs RADOS
gateway.

%package -n python%{python3_pkgversion}-rados
Summary:    Python 3 libraries for the RADOS object store
Requires:   python%{python3_pkgversion}
Requires:   librados2 = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-rados}
Provides:   python-rados = %{version}-%{release}
Obsoletes:  python-rados < %{version}-%{release}

%description -n python%{python3_pkgversion}-rados
This package contains Python 3 libraries for interacting with Cephs RADOS
object store.

%if 0%{with libradosstriper}
%package -n libradosstriper1
Summary:    RADOS striping interface
Requires:   librados2 = %{version}-%{release}

%description -n libradosstriper1
Striping interface built on top of the rados library, allowing
to stripe bigger objects onto several standard rados objects using
an interface very similar to the rados one.

%package -n libradosstriper-devel
Summary:    RADOS striping interface headers
Requires:   libradosstriper1 = %{version}-%{release}
Requires:   librados-devel = %{version}-%{release}
Requires:   libradospp-devel = %{version}-%{release}
Provides:   libradosstriper1-devel = %{version}-%{release}
Obsoletes:  libradosstriper1-devel < %{version}-%{release}

%description -n libradosstriper-devel
This package contains libraries and headers needed to develop programs
that use RADOS striping interface.
%endif

%package -n librbd1
Summary:    RADOS block device client library
Requires:   librados2 = %{version}-%{release}

%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n librbd-devel
Summary:    RADOS block device headers
Requires:   librbd1 = %{version}-%{release}
Requires:   librados-devel = %{version}-%{release}
Requires:   libradospp-devel = %{version}-%{release}
Provides:   librbd1-devel = %{version}-%{release}
Obsoletes:  librbd1-devel < %{version}-%{release}

%description -n librbd-devel
This package contains libraries and headers needed to develop programs
that use RADOS block device.

%package -n python%{python3_pkgversion}-rbd
Summary:    Python 3 libraries for the RADOS block device
Requires:   librbd1 = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rados = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-rbd}
Provides:   python-rbd = %{version}-%{release}
Obsoletes:  python-rbd < %{version}-%{release}

%description -n python%{python3_pkgversion}-rbd
This package contains Python 3 libraries for interacting with Cephs RADOS
block device.

%package -n libcephfs2
Summary:    Ceph distributed file system client library

%description -n libcephfs2
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n libcephfs-devel
Summary:    Ceph distributed file system headers
Requires:   libcephfs2 = %{version}-%{release}
Requires:   librados-devel = %{version}-%{release}
Provides:   libcephfs2-devel = %{version}-%{release}
Obsoletes:  libcephfs2-devel < %{version}-%{release}

%description -n libcephfs-devel
This package contains libraries and headers needed to develop programs
that use Cephs distributed file system.

%package -n python%{python3_pkgversion}-cephfs
Summary:    Python 3 libraries for Ceph distributed file system
Requires:   libcephfs2 = %{version}-%{release}
Requires:   python%{python3_pkgversion}-rados = %{version}-%{release}
Requires:   python%{python3_pkgversion}-ceph-argparse = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-cephfs}
Provides:   python-cephfs = %{version}-%{release}
Obsoletes:  python-cephfs < %{version}-%{release}

%description -n python%{python3_pkgversion}-cephfs
This package contains Python 3 libraries for interacting with Cephs distributed
file system.

%package -n python%{python3_pkgversion}-ceph-argparse
Summary:    Python 3 utility libraries for Ceph CLI
%{?python_provide:%python_provide python%{python3_pkgversion}-ceph-argparse}

%description -n python%{python3_pkgversion}-ceph-argparse
This package contains types and routines for Python 3 used by the Ceph CLI as
well as the RESTful interface. These have to do with querying the daemons for
command-description information, validating user command input against those
descriptions, and submitting the command to the appropriate daemon.

%package -n python%{python3_pkgversion}-ceph-common
Summary:    Python 3 utility libraries for Ceph
Requires:   python%{python3_pkgversion}-PyYAML
%{?python_provide:%python_provide python%{python3_pkgversion}-ceph-common}

%description -n python%{python3_pkgversion}-ceph-common
This package contains data structures, classes and functions used by Ceph.
It also contains utilities used for the cephadm orchestrator.

%if 0%{with cephfs_shell}
%package -n cephfs-shell
Summary:    Interactive shell for Ceph file system
Requires:   python%{python3_pkgversion}-cmd2
Requires:   python%{python3_pkgversion}-colorama
Requires:   python%{python3_pkgversion}-cephfs

%description -n cephfs-shell
This package contains an interactive tool that allows accessing a Ceph
file system without mounting it  by providing a nice pseudo-shell which
works like an FTP client.
%endif

%if 0%{with ceph_test_package}
%package -n ceph-test
Summary:    Ceph benchmarks and test tools
Requires:   ceph-common = %{version}-%{release}
Requires:   xmlstarlet
Requires:   jq
Requires:   socat

%description -n ceph-test
This package contains Ceph benchmarks and test tools.
%endif

%if 0%{with cephfs_java}

%package -n libcephfs_jni1
Summary:    Java Native Interface library for CephFS Java bindings
Requires:   java
Requires:   libcephfs2 = %{version}-%{release}

%description -n libcephfs_jni1
This package contains the Java Native Interface library for CephFS Java
bindings.

%package -n libcephfs_jni-devel
Summary:    Development files for CephFS Java Native Interface library

Requires:   java
Requires:   libcephfs_jni1 = %{version}-%{release}
Provides:   libcephfs_jni1-devel = %{version}-%{release}
Obsoletes:  libcephfs_jni1-devel < %{version}-%{release}
%description -n libcephfs_jni-devel
This package contains the development files for CephFS Java Native Interface
library.

%package -n cephfs-java
Summary:    Java libraries for the Ceph File System
Requires:   java
Requires:   libcephfs_jni1 = %{version}-%{release}
Requires:       junit
BuildRequires:  junit

%description -n cephfs-java
This package contains the Java libraries for the Ceph File System.

%endif

%package -n rados-objclass-devel
Summary:        RADOS object class development kit
Requires:       libradospp-devel = %{version}-%{release}

%description -n rados-objclass-devel
This package contains libraries and headers needed to develop RADOS object
class plugins.

%if 0%{with selinux}

%package selinux
Summary:            SELinux support for Ceph MON, OSD and MDS
Requires:           ceph-base = %{version}-%{release}
Requires:           libselinux-utils
Requires:           policycoreutils
Requires(post):     ceph-base = %{version}-%{release}
Requires(post):     gawk
Requires(post):     policycoreutils
Requires(post):     selinux-policy-base >= %{_selinux_policy_version}
Requires(postun):   policycoreutils

%description selinux
This package contains SELinux support for Ceph MON, OSD and MDS. The package
also performs file-system relabelling which can take a long time on heavily
populated file-systems.

%endif

%package grafana-dashboards
Summary:    The set of Grafana dashboards for monitoring purposes
BuildArch:  noarch

%description grafana-dashboards
This package provides a set of Grafana dashboards for monitoring of
Ceph clusters. The dashboards require a Prometheus server setup
collecting data from Ceph Manager "prometheus" module and Prometheus
project "node_exporter" module. The dashboards are designed to be
integrated with the Ceph Manager Dashboard web UI.

%package prometheus-alerts
Summary:        Prometheus alerts for a Ceph deplyoment
BuildArch:      noarch
Group:          System/Monitoring
%description prometheus-alerts
This package provides Ceph’s default alerts for Prometheus.

#################################################################################
# common
#################################################################################
%prep
%autosetup -p1

# Despite disabling diskprediction, some unpackaged files stick around
# Delete directories to prevent these files from being built/installed later
cd %{_topdir}/BUILD/%{name}-%{version}
rm -rf ./src/pybind/mgr/diskprediction_local
rm -rf ./src/pybind/mgr/diskprediction_cloud

%build
# LTO can be enabled as soon as the following GCC bug is fixed:
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48200
%define _lto_cflags %{nil}

%if 0%{with seastar}
. /opt/rh/gcc-toolset-9/enable
%endif

%if 0%{with cephfs_java}
# Find jni.h
for i in /usr/{lib64,lib}/jvm/java/include{,/linux}; do
    [ -d $i ] && java_inc="$java_inc -I$i"
done
%endif

export CPPFLAGS="$java_inc"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"

%if 0%{with seastar}
# seastar uses longjmp() to implement coroutine. and this annoys longjmp_chk()
export CXXFLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g')
%endif

# Parallel build settings ...
CEPH_MFLAGS_JOBS="%{?_smp_mflags}"
CEPH_SMP_NCPUS=$(echo "$CEPH_MFLAGS_JOBS" | sed 's/-j//')
%if 0%{?__isa_bits} == 32
# 32-bit builds can use 3G memory max, which is not enough even for -j2
CEPH_SMP_NCPUS="1"
%endif
# do not eat all memory
echo "Available memory:"
free -h
echo "System limits:"
ulimit -a
if test -n "$CEPH_SMP_NCPUS" -a "$CEPH_SMP_NCPUS" -gt 1 ; then
    mem_per_process=2500
    max_mem=$(LANG=C free -m | sed -n "s|^Mem: *\([0-9]*\).*$|\1|p")
    max_jobs="$(($max_mem / $mem_per_process))"
    test "$CEPH_SMP_NCPUS" -gt "$max_jobs" && CEPH_SMP_NCPUS="$max_jobs" && echo "Warning: Reducing build parallelism to -j$max_jobs because of memory limits"
    test "$CEPH_SMP_NCPUS" -le 0 && CEPH_SMP_NCPUS="1" && echo "Warning: Not using parallel build at all because of memory limits"
fi
export CEPH_SMP_NCPUS
export CEPH_MFLAGS_JOBS="-j$CEPH_SMP_NCPUS"

env | sort

mkdir build
cd build
CMAKE=cmake
${CMAKE} .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
    -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR=%{_unitdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR=%{_localstatedir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/ceph \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DWITH_MANPAGE=ON \
    -DWITH_PYTHON3=%{python3_version} \
    -DWITH_MGR_DASHBOARD_FRONTEND=OFF \
%if 0%{without mgr_diskprediction}
    -DMGR_DISABLED_MODULES=diskprediction_local\
%endif
%if 0%{without ceph_test_package}
    -DWITH_TESTS=OFF \
%endif
%if 0%{with cephfs_java}
    -DWITH_CEPHFS_JAVA=ON \
%endif
%if 0%{with selinux}
    -DWITH_SELINUX=ON \
%endif
%if %{with lttng}
    -DWITH_LTTNG=ON \
    -DWITH_BABELTRACE=ON \
%else
    -DWITH_LTTNG=OFF \
    -DWITH_BABELTRACE=OFF \
%endif
    $CEPH_EXTRA_CMAKE_ARGS \
%if 0%{with ocf}
    -DWITH_OCF=ON \
%endif
%ifarch aarch64 armv7hl mips mipsel ppc ppc64 ppc64le %{ix86} x86_64
    -DWITH_BOOST_CONTEXT=ON \
%else
    -DWITH_BOOST_CONTEXT=OFF \
%endif
%if 0%{with cephfs_shell}
    -DWITH_CEPHFS_SHELL=ON \
%endif
%if 0%{with libradosstriper}
    -DWITH_LIBRADOSSTRIPER=ON \
%else
    -DWITH_LIBRADOSSTRIPER=OFF \
%endif
%if 0%{with amqp_endpoint}
    -DWITH_RADOSGW_AMQP_ENDPOINT=ON \
%else
    -DWITH_RADOSGW_AMQP_ENDPOINT=OFF \
%endif
%if 0%{with kafka_endpoint}
    -DWITH_RADOSGW_KAFKA_ENDPOINT=ON \
%else
    -DWITH_RADOSGW_KAFKA_ENDPOINT=OFF \
%endif
%if 0%{with cmake_verbose_logging}
    -DCMAKE_VERBOSE_MAKEFILE=ON \
%endif
    -DBOOST_J=$CEPH_SMP_NCPUS \
    -DWITH_GRAFANA=ON

%if %{with cmake_verbose_logging}
cat ./CMakeFiles/CMakeOutput.log
cat ./CMakeFiles/CMakeError.log
%endif

make "$CEPH_MFLAGS_JOBS"


%if 0%{with make_check}
%check
# run in-tree unittests
cd build
ctest "$CEPH_MFLAGS_JOBS"
%endif


%install
pushd build
make DESTDIR=%{buildroot} install
# we have dropped sysvinit bits
rm -f %{buildroot}/%{_sysconfdir}/init.d/ceph
popd

%if 0%{with seastar}
# package crimson-osd with the name of ceph-osd
install -m 0755 %{buildroot}%{_bindir}/crimson-osd %{buildroot}%{_bindir}/ceph-osd
%endif

install -m 0644 -D src/etc-rbdmap %{buildroot}%{_sysconfdir}/ceph/rbdmap
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_sysconfdir}/sysconfig/ceph
install -m 0644 -D systemd/ceph.tmpfiles.d %{buildroot}%{_tmpfilesdir}/ceph-common.conf
install -m 0644 -D systemd/50-ceph.preset %{buildroot}%{_libexecdir}/systemd/system-preset/50-ceph.preset
mkdir -p %{buildroot}%{_sbindir}
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph
chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf
install -m 0644 -D COPYING %{buildroot}%{_docdir}/ceph/COPYING
install -m 0644 -D etc/sysctl/90-ceph-osd.conf %{buildroot}%{_sysctldir}/90-ceph-osd.conf

install -m 0755 src/cephadm/cephadm %{buildroot}%{_sbindir}/cephadm
mkdir -p %{buildroot}%{_sharedstatedir}/cephadm
chmod 0700 %{buildroot}%{_sharedstatedir}/cephadm
mkdir -p %{buildroot}%{_sharedstatedir}/cephadm/.ssh
chmod 0700 %{buildroot}%{_sharedstatedir}/cephadm/.ssh
touch %{buildroot}%{_sharedstatedir}/cephadm/.ssh/authorized_keys
chmod 0600 %{buildroot}%{_sharedstatedir}/cephadm/.ssh/authorized_keys

# udev rules
install -m 0644 -D udev/50-rbd.rules %{buildroot}%{_udevrulesdir}/50-rbd.rules

# sudoers.d
install -m 0600 -D sudoers.d/ceph-smartctl %{buildroot}%{_sysconfdir}/sudoers.d/ceph-smartctl

#set up placeholder directories
mkdir -p %{buildroot}%{_sysconfdir}/ceph
mkdir -p %{buildroot}%{_localstatedir}/run/ceph
mkdir -p %{buildroot}%{_localstatedir}/log/ceph
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mon
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/crash
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/crash/posted
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/radosgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rbd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rbd-mirror

# prometheus alerts
install -m 644 -D monitoring/ceph-mixin/prometheus_alerts.yml %{buildroot}/etc/prometheus/ceph/ceph_default_alerts.yml

#################################################################################
# files and systemd scriptlets
#################################################################################
%files

%files base
%{_bindir}/ceph-crash
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-kvstore-tool
%{_bindir}/ceph-run
%{_libexecdir}/systemd/system-preset/50-ceph.preset
%{_sbindir}/ceph-create-keys
%dir %{_libexecdir}/ceph
%{_libexecdir}/ceph/ceph_common.sh
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/*
%dir %{_libdir}/ceph
%dir %{_libdir}/ceph/erasure-code
%{_libdir}/ceph/erasure-code/libec_*.so*
%dir %{_libdir}/ceph/compressor
%{_libdir}/ceph/compressor/libceph_*.so*
%{_unitdir}/ceph-crash.service
%dir %{_libdir}/ceph/crypto
%{_libdir}/ceph/crypto/libceph_*.so*
%if %{with lttng}
%{_libdir}/libos_tp.so*
%{_libdir}/libosd_tp.so*
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/sysconfig/ceph
%config(noreplace) %{_sysconfdir}/sudoers.d/ceph-smartctl
%{_unitdir}/ceph.target
%dir %{python3_sitelib}/ceph_volume
%{python3_sitelib}/ceph_volume/*
%{python3_sitelib}/ceph_volume-*
%{_mandir}/man8/ceph-deploy.8*
%{_mandir}/man8/ceph-create-keys.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/ceph-kvstore-tool.8*
#set up placeholder directories
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/crash
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/crash/posted
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/tmp
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-osd
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mds
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rgw
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mgr
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rbd
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rbd-mirror

%post base
/sbin/ldconfig
%systemd_post ceph.target ceph-crash.service
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph.target ceph-crash.service >/dev/null 2>&1 || :
fi

%preun base
%systemd_preun ceph.target ceph-crash.service

%postun base
/sbin/ldconfig
%systemd_postun ceph.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
fi

%pre -n cephadm
getent group cephadm >/dev/null || groupadd -r cephadm
getent passwd cephadm >/dev/null || useradd -r -g cephadm -s /bin/bash -c "cephadm user for mgr/cephadm" -d %{_sharedstatedir}/cephadm cephadm
exit 0

%files -n cephadm
%{_sbindir}/cephadm
%{_mandir}/man8/cephadm.8*
%attr(0700,cephadm,cephadm) %dir %{_sharedstatedir}/cephadm
%attr(0700,cephadm,cephadm) %dir %{_sharedstatedir}/cephadm/.ssh
%attr(0600,cephadm,cephadm) %{_sharedstatedir}/cephadm/.ssh/authorized_keys

%files common
%dir %{_docdir}/ceph
%doc %{_docdir}/ceph/sample.ceph.conf
%license %{_docdir}/ceph/COPYING
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-syn
%{_bindir}/cephfs-data-scan
%{_bindir}/cephfs-journal-tool
%{_bindir}/cephfs-mirror
%{_bindir}/cephfs-top
%{_bindir}/cephfs-table-tool
%{_bindir}/rados
%{_bindir}/radosgw-admin
%{_bindir}/rbd
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/rbdmap
%{_sbindir}/mount.ceph
%{_unitdir}/cephfs-mirror@.service
%{_unitdir}/cephfs-mirror.target
%if %{with lttng}
%{_bindir}/rbd-replay-prep
%endif
%{_bindir}/ceph-post-file
%{_tmpfilesdir}/ceph-common.conf
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-diff-sorted.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/rbdmap.8*
%{_mandir}/man8/rbd-replay.8*
%{_mandir}/man8/rbd-replay-many.8*
%{_mandir}/man8/rbd-replay-prep.8*
%{_mandir}/man8/rgw-orphan-list.8*
%{_mandir}/man8/cephfs-mirror.8*
%{_mandir}/man8/cephfs-top.8*
%{python3_sitelib}/cephfs_top-*.egg-info
%dir %{_datadir}/ceph/
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_unitdir}/rbdmap.service
%dir %{_udevrulesdir}
%{_udevrulesdir}/50-rbd.rules
%attr(3770,ceph,ceph) %dir %{_localstatedir}/log/ceph/
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/
%exclude %{_includedir}/libcephsqlite.h
%exclude %{_libdir}/libcephsqlite.so

%pre common
CEPH_GROUP_ID=167
CEPH_USER_ID=167
/usr/sbin/groupadd ceph -g $CEPH_GROUP_ID -o -r 2>/dev/null || :
/usr/sbin/useradd ceph -u $CEPH_USER_ID -o -r -g ceph -s /sbin/nologin -c "Ceph daemons" -d %{_localstatedir}/lib/ceph 2>/dev/null || :
exit 0

%post common
%tmpfiles_create %{_tmpfilesdir}/ceph-common.conf

%postun common
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf %{_localstatedir}/log/ceph
    rm -rf %{_sysconfdir}/ceph
fi

%files mds
%{_bindir}/ceph-mds
%{_mandir}/man8/ceph-mds.8*
%{_unitdir}/ceph-mds@.service
%{_unitdir}/ceph-mds.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mds

%post mds
%systemd_post ceph-mds@\*.service ceph-mds.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mds.target >/dev/null 2>&1 || :
fi

%preun mds
%systemd_preun ceph-mds@\*.service ceph-mds.target

%postun mds
%systemd_postun ceph-mds@\*.service ceph-mds.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mds@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mgr
%{_bindir}/ceph-mgr
%dir %{_datadir}/ceph/mgr
%{_datadir}/ceph/mgr/mgr_module.*
%{_datadir}/ceph/mgr/__pycache__/mgr*.py*
%{_datadir}/ceph/mgr/mgr_util.*
%{_unitdir}/ceph-mgr@.service
%{_unitdir}/ceph-mgr.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mgr

%post mgr
%systemd_post ceph-mgr@\*.service ceph-mgr.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mgr.target >/dev/null 2>&1 || :
fi

%preun mgr
%systemd_preun ceph-mgr@\*.service ceph-mgr.target

%postun mgr
%systemd_postun ceph-mgr@\*.service ceph-mgr.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mgr@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mgr-dashboard
%{_datadir}/ceph/mgr/dashboard

%post mgr-dashboard
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%postun mgr-dashboard
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%if %{with mgr_diskprediction}
%files mgr-diskprediction-local
%{_datadir}/ceph/mgr/diskprediction_local

%post mgr-diskprediction-local
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%postun mgr-diskprediction-local
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi
%endif

%files mgr-modules-core
%dir %{_datadir}/ceph/mgr
%{_datadir}/ceph/mgr/alerts
%{_datadir}/ceph/mgr/balancer
%{_datadir}/ceph/mgr/crash
%{_datadir}/ceph/mgr/devicehealth
%{_datadir}/ceph/mgr/influx
%{_datadir}/ceph/mgr/insights
%{_datadir}/ceph/mgr/iostat
%{_datadir}/ceph/mgr/localpool
%{_datadir}/ceph/mgr/mds_autoscaler
%{_datadir}/ceph/mgr/mirroring
%{_datadir}/ceph/mgr/nfs
%{_datadir}/ceph/mgr/orchestrator
%{_datadir}/ceph/mgr/osd_perf_query
%{_datadir}/ceph/mgr/osd_support
%{_datadir}/ceph/mgr/pg_autoscaler
%{_datadir}/ceph/mgr/progress
%{_datadir}/ceph/mgr/prometheus
%{_datadir}/ceph/mgr/rbd_support
%{_datadir}/ceph/mgr/restful
%{_datadir}/ceph/mgr/selftest
%{_datadir}/ceph/mgr/snap_schedule
%{_datadir}/ceph/mgr/stats
%{_datadir}/ceph/mgr/status
%{_datadir}/ceph/mgr/telegraf
%{_datadir}/ceph/mgr/telemetry
%{_datadir}/ceph/mgr/test_orchestrator
%{_datadir}/ceph/mgr/volumes
%{_datadir}/ceph/mgr/zabbix

%files mgr-rook
%{_datadir}/ceph/mgr/rook

%post mgr-rook
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%postun mgr-rook
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%files mgr-k8sevents
%{_datadir}/ceph/mgr/k8sevents

%post mgr-k8sevents
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%postun mgr-k8sevents
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%files mgr-cephadm
%{_datadir}/ceph/mgr/cephadm

%post mgr-cephadm
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%postun mgr-cephadm
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl try-restart ceph-mgr.target >/dev/null 2>&1 || :
fi

%files mon
%{_bindir}/ceph-mon
%{_bindir}/ceph-monstore-tool
%{_mandir}/man8/ceph-mon.8*
%{_unitdir}/ceph-mon@.service
%{_unitdir}/ceph-mon.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mon

%post mon
%systemd_post ceph-mon@\*.service ceph-mon.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mon.target >/dev/null 2>&1 || :
fi

%preun mon
%systemd_preun ceph-mon@\*.service ceph-mon.target

%postun mon
%systemd_postun ceph-mon@\*.service ceph-mon.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mon@\*.service > /dev/null 2>&1 || :
  fi
fi

%files fuse
%{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*
%{_mandir}/man8/mount.fuse.ceph.8*
%{_sbindir}/mount.fuse.ceph
%{_unitdir}/ceph-fuse@.service
%{_unitdir}/ceph-fuse.target

%files -n rbd-fuse
%{_bindir}/rbd-fuse
%{_mandir}/man8/rbd-fuse.8*

%files -n rbd-mirror
%{_bindir}/rbd-mirror
%{_mandir}/man8/rbd-mirror.8*
%{_unitdir}/ceph-rbd-mirror@.service
%{_unitdir}/ceph-rbd-mirror.target

%post -n rbd-mirror
%systemd_post ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-rbd-mirror.target >/dev/null 2>&1 || :
fi

%preun -n rbd-mirror
%systemd_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target

%postun -n rbd-mirror
%systemd_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-rbd-mirror@\*.service > /dev/null 2>&1 || :
  fi
fi

%files immutable-object-cache
%{_bindir}/ceph-immutable-object-cache
%{_mandir}/man8/ceph-immutable-object-cache.8*
%{_unitdir}/ceph-immutable-object-cache@.service
%{_unitdir}/ceph-immutable-object-cache.target

%post immutable-object-cache
%systemd_post ceph-immutable-object-cache@\*.service ceph-immutable-object-cache.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-immutable-object-cache.target >/dev/null 2>&1 || :
fi

%preun immutable-object-cache
%systemd_preun ceph-immutable-object-cache@\*.service ceph-immutable-object-cache.target

%postun immutable-object-cache
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-immutable-object-cache@\*.service ceph-immutable-object-cache.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-immutable-object-cache@\*.service > /dev/null 2>&1 || :
  fi
fi

%files -n rbd-nbd
%{_bindir}/rbd-nbd
%{_mandir}/man8/rbd-nbd.8*

%files radosgw
%{_bindir}/ceph-diff-sorted
%{_bindir}/radosgw
%{_bindir}/radosgw-token
%{_bindir}/radosgw-es
%{_bindir}/radosgw-object-expirer
%{_bindir}/rgw-orphan-list
%{_bindir}/rgw-gap-list
%{_bindir}/rgw-gap-list-comparator
%{_libdir}/libradosgw.so*
%{_mandir}/man8/radosgw.8*
%dir %{_localstatedir}/lib/ceph/radosgw
%{_unitdir}/ceph-radosgw@.service
%{_unitdir}/ceph-radosgw.target

%post radosgw
/sbin/ldconfig
%systemd_post ceph-radosgw@\*.service ceph-radosgw.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-radosgw.target >/dev/null 2>&1 || :
fi

%preun radosgw
%systemd_preun ceph-radosgw@\*.service ceph-radosgw.target

%postun radosgw
/sbin/ldconfig
%systemd_postun ceph-radosgw@\*.service ceph-radosgw.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-radosgw@\*.service > /dev/null 2>&1 || :
  fi
fi

%files osd
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-bluestore-tool
%{_bindir}/ceph-erasure-code-tool
%{_bindir}/ceph-objectstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph-osd
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%{_sbindir}/ceph-volume
%{_sbindir}/ceph-volume-systemd
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/ceph-bluestore-tool.8*
%{_mandir}/man8/ceph-volume.8*
%{_mandir}/man8/ceph-volume-systemd.8*
%{_unitdir}/ceph-osd@.service
%{_unitdir}/ceph-osd.target
%{_unitdir}/ceph-volume@.service
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/osd
%config(noreplace) %{_sysctldir}/90-ceph-osd.conf

%post osd
%systemd_post ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-osd.target >/dev/null 2>&1 || :
fi
%if 0%{?sysctl_apply}
    %sysctl_apply 90-ceph-osd.conf
%else
    /usr/lib/systemd/systemd-sysctl %{_sysctldir}/90-ceph-osd.conf > /dev/null 2>&1 || :
%endif

%preun osd
%systemd_preun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target

%postun osd
%systemd_postun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
if [ $1 -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-osd@\*.service ceph-volume@\*.service > /dev/null 2>&1 || :
  fi
fi

%if 0%{with seastar}
%files crimson-osd
%{_bindir}/crimson-osd
%endif

%if %{with ocf}

%files resource-agents
%dir %{_prefix}/lib/ocf
%dir %{_prefix}/lib/ocf/resource.d
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(0755,-,-) %{_prefix}/lib/ocf/resource.d/ceph/rbd

%endif

%files -n librados2
%{_libdir}/librados.so.*
%dir %{_libdir}/ceph
%{_libdir}/ceph/libceph-common.so.*
%if %{with lttng}
%{_libdir}/librados_tp.so.*
%endif
%dir %{_sysconfdir}/ceph

%post -n librados2 -p /sbin/ldconfig

%postun -n librados2 -p /sbin/ldconfig

%files -n librados-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/rados_types.h
%{_libdir}/librados.so
%if %{with lttng}
%{_libdir}/librados_tp.so
%endif
%{_bindir}/librados-config
%{_mandir}/man8/librados-config.8*

%files -n libradospp-devel
%dir %{_includedir}/rados
%{_includedir}/rados/buffer.h
%{_includedir}/rados/buffer_fwd.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/inline_memory.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/librados_fwd.hpp
%{_includedir}/rados/page.h
%{_includedir}/rados/rados_types.hpp

%files -n python%{python3_pkgversion}-rados
%{python3_sitearch}/rados.cpython*.so
%{python3_sitearch}/rados-*.egg-info

%if 0%{with libradosstriper}
%files -n libradosstriper1
%{_libdir}/libradosstriper.so.*

%post -n libradosstriper1 -p /sbin/ldconfig

%postun -n libradosstriper1 -p /sbin/ldconfig

%files -n libradosstriper-devel
%dir %{_includedir}/radosstriper
%{_includedir}/radosstriper/libradosstriper.h
%{_includedir}/radosstriper/libradosstriper.hpp
%{_libdir}/libradosstriper.so
%endif

%files -n librbd1
%{_libdir}/librbd.so.*
%if %{with lttng}
%{_libdir}/librbd_tp.so.*
%endif
%{_libdir}/ceph/librbd/libceph_*.so*

%post -n librbd1 -p /sbin/ldconfig

%postun -n librbd1 -p /sbin/ldconfig

%files -n librbd-devel
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/librbd.so
%if %{with lttng}
%{_libdir}/librbd_tp.so
%endif

%files -n librgw2
%{_libdir}/librgw.so.*
%if %{with lttng}
%{_libdir}/librgw_op_tp.so.*
%{_libdir}/librgw_rados_tp.so.*
%endif

%post -n librgw2 -p /sbin/ldconfig

%postun -n librgw2 -p /sbin/ldconfig

%files -n librgw-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librgw.h
%{_includedir}/rados/rgw_file.h
%{_libdir}/librgw.so
%if %{with lttng}
%{_libdir}/librgw_op_tp.so
%{_libdir}/librgw_rados_tp.so
%endif

%files -n python%{python3_pkgversion}-rgw
%{python3_sitearch}/rgw.cpython*.so
%{python3_sitearch}/rgw-*.egg-info

%files -n python%{python3_pkgversion}-rbd
%{python3_sitearch}/rbd.cpython*.so
%{python3_sitearch}/rbd-*.egg-info

%files -n libcephfs2
%{_libdir}/libcephfs.so.*
%dir %{_sysconfdir}/ceph

%post -n libcephfs2 -p /sbin/ldconfig

%postun -n libcephfs2 -p /sbin/ldconfig

%files -n libcephfs-devel
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%{_includedir}/cephfs/ceph_ll_client.h
%{_libdir}/libcephfs.so
%{_includedir}/cephfs/metrics/Types.h

%files -n python%{python3_pkgversion}-cephfs
%{python3_sitearch}/cephfs.cpython*.so
%{python3_sitearch}/cephfs-*.egg-info
%{python3_sitelib}/ceph_volume_client.py
%{python3_sitelib}/__pycache__/ceph_volume_client.cpython*.py*

%files -n python%{python3_pkgversion}-ceph-argparse
%{python3_sitelib}/ceph_argparse.py
%{python3_sitelib}/__pycache__/ceph_argparse.cpython*.py*
%{python3_sitelib}/ceph_daemon.py
%{python3_sitelib}/__pycache__/ceph_daemon.cpython*.py*

%files -n python%{python3_pkgversion}-ceph-common
%{python3_sitelib}/ceph
%{python3_sitelib}/ceph-*.egg-info

%if 0%{with cephfs_shell}
%files -n cephfs-shell
%{python3_sitelib}/cephfs_shell-*.egg-info
%{_bindir}/cephfs-shell
%endif

%if 0%{with ceph_test_package}
%files -n ceph-test
%{_bindir}/ceph-client-debug
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_objectstore_bench
%{_bindir}/ceph_perf_objectstore
%{_bindir}/ceph_perf_local
%{_bindir}/ceph_perf_msgr_client
%{_bindir}/ceph_perf_msgr_server
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_test_*
%{_bindir}/ceph-coverage
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-dedup-tool
%{_mandir}/man8/ceph-debugpack.8*
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%endif

%if 0%{with cephfs_java}
%files -n libcephfs_jni1
%{_libdir}/libcephfs_jni.so.*

%post -n libcephfs_jni1 -p /sbin/ldconfig

%postun -n libcephfs_jni1 -p /sbin/ldconfig

%files -n libcephfs_jni-devel
%{_libdir}/libcephfs_jni.so

%files -n cephfs-java
%{_javadir}/libcephfs.jar
%{_javadir}/libcephfs-test.jar
%endif

%files -n rados-objclass-devel
%dir %{_includedir}/rados
%{_includedir}/rados/objclass.h

%if 0%{with selinux}
%files selinux
%attr(0600,root,root) %{_datadir}/selinux/packages/ceph.pp
%{_datadir}/selinux/devel/include/contrib/ceph.if
%{_mandir}/man8/ceph_selinux.8*

%post selinux
# backup file_contexts before update
. /etc/selinux/config
FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

# Install the policy
/usr/sbin/semodule -i %{_datadir}/selinux/packages/ceph.pp

# Load the policy if SELinux is enabled
if ! /usr/sbin/selinuxenabled; then
    # Do not relabel if selinux is not enabled
    exit 0
fi

if diff ${FILE_CONTEXT} ${FILE_CONTEXT}.pre > /dev/null 2>&1; then
   # Do not relabel if file contexts did not change
   exit 0
fi

# Check whether the daemons are running
/usr/bin/systemctl status ceph.target > /dev/null 2>&1
STATUS=$?

# Stop the daemons if they were running
if test $STATUS -eq 0; then
    /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
fi

# Relabel the files fix for first package install
/usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null

rm -f ${FILE_CONTEXT}.pre
# The fixfiles command won't fix label for /var/run/ceph
/usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

# Start the daemons iff they were running before
if test $STATUS -eq 0; then
    /usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
fi
exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    # backup file_contexts before update
    . /etc/selinux/config
    FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
    cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

    # Remove the module
    /usr/sbin/semodule -n -r ceph > /dev/null 2>&1

    # Reload the policy if SELinux is enabled
    if ! /usr/sbin/selinuxenabled ; then
        # Do not relabel if SELinux is not enabled
        exit 0
    fi

    # Check whether the daemons are running
    /usr/bin/systemctl status ceph.target > /dev/null 2>&1
    STATUS=$?

    # Stop the daemons if they were running
    if test $STATUS -eq 0; then
        /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
    fi

    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
    rm -f ${FILE_CONTEXT}.pre
    # The fixfiles command won't fix label for /var/run/ceph
    /usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

    # Start the daemons if they were running before
    if test $STATUS -eq 0; then
    /usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
    fi
fi
exit 0
%endif

%files grafana-dashboards
%attr(0755,root,root) %dir %{_sysconfdir}/grafana
%attr(0755,root,root) %dir %{_sysconfdir}/grafana/dashboards
%attr(0755,root,root) %dir %{_sysconfdir}/grafana/dashboards/ceph-dashboard
%config %{_sysconfdir}/grafana/dashboards/ceph-dashboard/*

%files prometheus-alerts
%attr(0755,root,root) %dir %{_sysconfdir}/prometheus/ceph
%config %{_sysconfdir}/prometheus/ceph/ceph_default_alerts.yml

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 16.2.10-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Aug 05 2022 Cameron Baird <cameronbaird@microsoft.com> - 16.2.10-1
- Update source to v16.2.10 to address CVE-2022-0670
- Install ceph-smartctl instead of ceph-osd-smartctl
- Since ceph-smartctl now seems needed for daemons of multiple subpackages, 
    moved %files entry for ceph-smartctl from osd to base 

* Wed Mar 09 2022 Mateusz Malisz <mamalisz@microsoft.com> - 16.2.5-4
- Add libevent as a build requires to fix build error/warning for some hostnames

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 16.2.5-3
- Add patch to fix build with snappy >= 1.1.9

* Thu Feb 17 2022 Andrew Phelps <anphel@microsoft.com> - 16.2.5-2
- Use _topdir instead of hard-coded value /usr/src/mariner

* Mon Jan 03 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 16.2.5-1
- Updated to version 16.2.5.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 16.2.0-6
- Removing the explicit %%clean stage.

* Tue Sep 21 2021 Henry Li <lihl@microsoft.com> - 16.2.0-5
- Use util-linux-devel as BR instead of util-linux-libs

* Tue Aug 31 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 16.2.0-4
- Enabling the "libradosstriper" subpackages.

* Wed Aug 18 2021 Thomas Crain <thcrain@microsoft.com> - 16.2.0-3
- Enable python byte compilation for directories outside of %%python3_site{lib,arch}

* Thu Jun 17 2021 Neha Agarwal <nehaagarwal@microsoft.com> 16.2.0-2
- Disable debuginfo because ceph-debuginfo rpm is too large

* Fri May 21 2021 Neha Agarwal <nehaagarwal@microsoft.com> 16.2.0-1
- Update package version to fix CVE-2020-25660, CVE-2020-25678 and CVE-2020-27781

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 15.2.4-2
- Include python bytecompiled files in the resulting package.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 15.2.4-1
- Initial CBL-Mariner import from Ceph source (license: LGPLv2.1)
- License verified
