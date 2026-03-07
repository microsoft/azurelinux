# Plain package name for cases, where %%{name} differs (e.g. for versioned packages)
%global majorname mariadb
%define package_version 10.11.15
%define majorversion %(echo %{package_version} | cut -d'.' -f1-2 )

%define _vpath_builddir .

# Set if this package will be the default one in distribution
%{!?mariadb_default:%global mariadb_default 1}
 
# Regression tests may take a long time (many cores recommended), skip them by
%{!?runselftest:%global runselftest 0}
 
# Set this to 1 to see which tests fail, but 0 on production ready build
%global ignore_testsuite_result 0
 
# The last version on which the full testsuite has been run
# In case of further rebuilds of that version, don't require full testsuite to be run
# run only "main" suite
%global last_tested_version 10.11.11
# Set to 1 to force run the testsuite even if it was already tested in current version
%global force_run_testsuite 0
 
# Filtering: https://docs.fedoraproject.org/en-US/packaging-guidelines/AutoProvidesAndRequiresFiltering/
%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::|wsrep)
%global __provides_exclude_from ^(%{_datadir}/(mysql|mysql-test)/.*|%{_libdir}/%{majorname}/plugin/.*\\.so)$
 
# Temporary workaround to fix the "internal compiler error" described in https://bugzilla.redhat.com/show_bug.cgi?id=2239498
# TODO: Remove when the issue is resolved
%ifarch i686
%global _lto_cflags %{nil}
%endif
 
 
 
# For some use cases we do not need some parts of the package. Set to "...with" to exclude
%bcond_with    clibrary
%bcond_with    config
%bcond_with embedded
%bcond_without devel
%bcond_without client
%bcond_without common
%bcond_without errmsg
%bcond_without galera
%bcond_without backup
%if !0%{?flatpak}
%bcond_without test
%endif
 
# Page compression algorithms for various storage engines
%bcond_without lz4
%bcond_without bzip2
%bcond_without lzo
%bcond_without snappy
%bcond_without zstd
%bcond_with lzma
 
# Aditional SELinux rules from a standalone package 'mysql-selinux' (that holds rules shared between MariaDB and MySQL)
%bcond_with require_mysql_selinux
 
# For deep debugging we need to build binaries with extra debug info
%bcond_with    debug
 
# Authentication plugins
%bcond_without gssapi
%bcond_with pam
%bcond_with hashicorp
 
# The Open Query GRAPH engine (OQGRAPH) is a computation engine allowing
# hierarchies and more complex graph structures to be handled in a relational fashion
%bcond_with oqgraph

# Other plugins
# S3 storage engine
#   https://mariadb.com/kb/en/s3-storage-engine/
%bcond_with cracklib
%bcond_with connect
%bcond_with sphinx
%bcond_with s3
 
# Mroonga engine
#   https://mariadb.com/kb/en/mariadb/about-mroonga/
#   Current version in MariaDB, 7.07, only supports the x86_64
#   Mroonga upstream warns about using 32-bit package: http://mroonga.org/docs/install.html
# RocksDB engine
#   https://mariadb.com/kb/en/library/about-myrocks-for-mariadb/
#   RocksDB engine is available only for x86_64
#   RocksDB may be built with jemalloc, if specified in CMake
%ifarch x86_64
%bcond_with mroonga
%bcond_with rocksdb
%endif
 
 
 
# MariaDB 10.0 and later requires pcre >= 10.34, otherwise we need to use
# the bundled library, since the package cannot be build with older version
#   https://mariadb.com/kb/en/pcre/
%bcond_without unbundled_pcre
 
# To avoid issues with a breaking change in FMT library, bundle it on systems where FMT wasn't fixed yet
# See mariadb-libfmt.patch for detailed description.
%bcond bundled_fmt 0
%if %{with bundled_fmt}
%global fmt_bundled_version 11.0.2
%endif
 
# Include systemd files
%global daemon_name      %{majorname}
%global daemon_no_prefix %{majorname}
 
# We define some system's well known locations here so we can use them easily
# later when building to another location (like SCL)
%global logrotateddir    %{_sysconfdir}/logrotate.d
%global logfiledir       %{_localstatedir}/log/%{daemon_name}
%global logfile          %{logfiledir}/%{daemon_name}.log
# Directory for storing pid file
%global pidfiledir       %{_rundir}/%{daemon_name}
# Defining where database data live
%global dbdatadir        %{_localstatedir}/lib/mysql
 
 
 
# Set explicit conflicts with 'mysql' packages
%bcond_without conflicts_mysql
# Set explicit conflicts with 'community-mysql' names, provided by 'mysql' packages
#   'community-mysql' names are deprecated and to be removed in future Fedora
%bcond_without conflicts_community_mysql
 
# Make long macros shorter
%global sameevr   %{epoch}:%{version}-%{release}
 
Name:             %{majorname}
Version:          %{package_version}
Release:          1%{?dist}
Epoch:            3
 
Summary:          A very fast and robust SQL database server
URL:              http://mariadb.org
License:          ( GPL-2.0-only OR Apache-2.0 ) AND ( GPL-2.0-or-later OR Apache-2.0 ) AND BSD-2-Clause AND BSD-3-Clause AND CC-BY-4.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-or-later AND ( GPL-3.0-or-later WITH Bison-exception-2.2 ) AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND OpenSSL AND MIT AND OFL-1.1 AND CC0-1.0 AND PHP-3.0 AND PHP-3.01 AND zlib AND dtoa AND FSFAP AND blessing AND Info-ZIP AND Boehm-GC
Vendor:           Microsoft Corporation
Distribution:     Azure Linux 

Source0:          https://downloads.mariadb.org/interstitial/mariadb-%{version}/source/mariadb-%{version}.tar.gz
%if %{with bundled_fmt}
Source1:          https://github.com/fmtlib/fmt/releases/download/%{fmt_bundled_version}/fmt-%{fmt_bundled_version}.zip
%endif
Source2:          mysql_config_multilib.sh
Source3:          my.cnf.in
Source6:          README.mariadb-docs
Source8:          README.wsrep_sst_rsync_tunnel
Source10:         mariadb.tmpfiles.d.in
Source11:         mysql.service.in
Source12:         mariadb-prepare-db-dir.sh
Source14:         mariadb-check-socket.sh
Source15:         mariadb-scripts-common.sh
Source16:         mariadb-check-upgrade.sh
Source18:         mysql@.service.in
Source50:         rh-skipped-tests-base.list
Source51:         rh-skipped-tests-arm.list
Source52:         rh-skipped-tests-s390.list
Source53:         rh-skipped-tests-ppc.list
# Red Hat OpenStack scripts:
#   Clustercheck:
#     Maintainer:
#       Damien Ciabrini <dciabrin@redhat.com>
#     Source / Upstream:
#       Damien; based on https://github.com/olafz/percona-clustercheck
#       not updated in 5 years; low-effort maintenance
#     Purpose:
#       In Openstack, galera is accessed like an A/P database, we have a
#       load balancer (haproxy) that drives traffic to a single node and
#       performs failover when the galera node monitor fails.
#       clustercheck.sh is the monitoring script that is being called remotely
#       by haproxy. It is a glue between haproxy and the local galera node that
#       can run SQL commands to check whether the local galera is connected to the galera cluster.
#     Proposed to MariaDB upstream: https://jira.mariadb.org/browse/MDEV-12442
#       General upstream response was slightly positive
Source70:         clustercheck.sh
Source71:         LICENSE.clustercheck
 
# Upstream said: "Generally MariaDB has more allows to allow for xtradb sst mechanism".
# https://jira.mariadb.org/browse/MDEV-12646
Source72:         mariadb-server-galera.te
 
# Script to support encrypted rsync transfers when SST is required between nodes.
# https://github.com/dciabrin/wsrep_sst_rsync_tunnel/blob/master/wsrep_sst_rsync_tunnel
Source73:         wsrep_sst_rsync_tunnel
	
#   Patch4: Red Hat distributions specific logrotate fix
#   it would be big unexpected change, if we start shipping it now. Better wait for MariaDB 10.2
Patch4:           %{majorname}-logrotate.patch
#   Patch7: add to the CMake file all files where we want macros to be expanded
Patch7:           %{majorname}-scripts.patch
#   Patch9: pre-configure to comply with guidelines
Patch9:           %{majorname}-ownsetup.patch
#   Patch12: fixes of RocksDB for GCC 13
Patch12:          rocksdb-6.8-gcc13.patch
#   Patch13: bundle the FMT library
Patch13:          %{majorname}-libfmt.patch
#   Patch14: make MTR port calculation reasonably predictable
Patch14:          %{majorname}-mtr.patch

%global pkgname %{majorname}
 
BuildRequires:    make cmake gcc-c++
BuildRequires:    libxcrypt-devel
#BuildRequires:    multilib-rpm-config
BuildRequires:    selinux-policy-devel
BuildRequires:    systemd systemd-devel
 
# Page compression algorithms for various storage engines
BuildRequires:    zlib-devel
%{?with_lz4:BuildRequires:    lz4-devel >= 1.6}
%{?with_bzip2:BuildRequires:    bzip2-devel}
%{?with_lzma:BuildRequires:    xz-devel}
%{?with_lzo:BuildRequires:    lzo-devel}
%{?with_snappy:BuildRequires:    snappy-devel}
%{?with_zstd:BuildRequires:    libzstd-devel}
 
# asynchornous operations stuff; needed also for wsrep API
BuildRequires:    libaio-devel
# commands history features
BuildRequires:    libedit-devel
# CLI graphic; needed also for wsrep API
BuildRequires:    ncurses-devel
# debugging stuff
BuildRequires:    systemtap-sdt-devel
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 11
BuildRequires:    systemtap-sdt-dtrace
%endif
# Bison SQL parser; needed also for wsrep API
BuildRequires:    bison >= 2.4
#BuildRequires:    bison-devel >= 2.4
 
# use either new enough version of pcre2 or provide bundles(pcre2)
%{?with_unbundled_pcre:BuildRequires: pcre2-devel >= 10.34 pkgconf}
%{!?with_unbundled_pcre:Provides: bundled(pcre2) = %{pcre_bundled_version}}
# Few utilities needs Perl
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
# Some tests requires python
BuildRequires:    python3
# Tests requires time and ps and some perl modules
BuildRequires:    procps
BuildRequires:    time
BuildRequires:    perl(base)
BuildRequires:    perl(Cwd)
BuildRequires:    perl(Data::Dumper)
BuildRequires:    perl(English)
BuildRequires:    perl(Env)
BuildRequires:    perl(Errno)
BuildRequires:    perl(Exporter)
BuildRequires:    perl(Fcntl)
BuildRequires:    perl(File::Basename)
BuildRequires:    perl(File::Copy)
BuildRequires:    perl(File::Find)
BuildRequires:    perl(File::Spec)
BuildRequires:    perl(File::Spec::Functions)
BuildRequires:    perl(File::Temp)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IO::File)
BuildRequires:    perl(IO::Handle)
BuildRequires:    perl(IO::Select)
BuildRequires:    perl(IO::Socket)
BuildRequires:    perl(IO::Socket::INET)
BuildRequires:    perl(IPC::Open3)
BuildRequires:    perl(lib)
BuildRequires:    perl(Memoize)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(Socket)
BuildRequires:    perl(strict)
BuildRequires:    perl(Symbol)
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Term::ANSIColor)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(Time::HiRes)
BuildRequires:    perl(Time::localtime)
BuildRequires:    perl(warnings)
# for running some openssl tests rhbz#1189180
BuildRequires:    openssl openssl-devel
 
%{!?with_bundled_fmt:BuildRequires: fmt-devel >= 10.2.1-2}
 
Requires:         bash coreutils grep
BuildRequires:    perl(Test::Harness)
BuildRequires:    perl(TAP::Harness)
 
Requires:         %{pkgname}-common = %{sameevr}
 
%if %{with clibrary}
# Explicit EVR requirement for -libs is needed for RHBZ#1406320
Requires:         %{pkgname}-libs%{?_isa} = %{sameevr}
%else
# If not built with client library in this package, use connector-c
Requires:         mariadb-connector-c >= 3.0
%endif
 
# Recommend additional client utils that require Perl
Recommends:       %{pkgname}-client-utils
 
Suggests:         %{pkgname}-server%{?_isa} = %{sameevr}
 
%{?with_conflicts_mysql:Conflicts: mysql}
%{?with_conflicts_community_mysql:Conflicts: community-mysql}
# Explicitly disallow combination mariadb + mysql-server
%{?with_conflicts_mysql:Conflicts: mysql-server}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-server}
 
%define conflict_with_other_streams() %{expand:\
Provides: %{majorname}%{?1:-%{1}}-any\
Conflicts: %{majorname}%{?1:-%{1}}-any\
}
 
# Provide also mariadbXX.XX if default
%if %?mariadb_default
%define mariadbXX_if_default() %{expand:\
Provides: mariadb%{majorversion}%{?1:-%{1}} = %{sameevr}\
Provides: mariadb%{majorversion}%{?1:-%{1}}%{?_isa} = %{sameevr}\
}
%else
%define mariadbXX_if_default() %{nil}
%endif
 
%define virtual_conflicts_and_provides() %{expand:\
%conflict_with_other_streams %{**}\
%mariadbXX_if_default %{**}\
}
 
%virtual_conflicts_and_provides
 
%description -n %{pkgname}
MariaDB is a community developed fork from MySQL - a multi-user, multi-threaded
SQL database server. It is a client/server implementation consisting of
a server daemon (mariadbd) and many different client programs and libraries.
The base package contains the standard MariaDB/MySQL client programs and
utilities.
 
 
%package          -n %{pkgname}-client-utils
Summary:          Non-essential client utilities for MariaDB/MySQL applications
Requires:         %{pkgname}%{?_isa} = %{sameevr}
Requires:         perl(DBI)
 
%virtual_conflicts_and_provides client-utils
 
%description      -n %{pkgname}-client-utils
This package contains all non-essential client utilities and scripts for
managing databases. It also contains all utilities requiring Perl and it is the
only MariaDB sub-package with the corresponding server-utils one, except test
subpackage, that depends on Perl.
 
 
%if %{with clibrary}
%package          -n %{pkgname}-libs
Summary:          The shared libraries required for MariaDB/MySQL clients
Requires:         %{pkgname}-common = %{sameevr}
 
%virtual_conflicts_and_provides libs
 
%{?with_conflicts_mysql:Conflicts: mysql-libs}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-libs}
 
%description      -n %{pkgname}-libs
The mariadb-libs package provides the essential shared libraries for any
MariaDB/MySQL client program or interface. You will need to install this
package to use any other MariaDB package or any clients that need to connect
to a MariaDB/MySQL server.
%endif
 
 
# At least main config file /etc/my.cnf is shared for client and server part
# Since we want to support combination of different client and server
# implementations (e.g. mariadb library and community-mysql server),
# we need the config file(s) to be in a separate package, so no extra packages
# are pulled, because these would likely conflict.
# More specifically, the dependency on the main configuration file (/etc/my.cnf)
# is supposed to be defined as Requires: /etc/my.cnf rather than requiring
# a specific package, so installer app can choose whatever package fits to
# the transaction.
%if %{with config}
%package          -n %{pkgname}-config
Summary:          The config files required by server and client
 
%virtual_conflicts_and_provides config
 
%description      -n %{pkgname}-config
The package provides the config file my.cnf and my.cnf.d directory used by any
MariaDB or MySQL program. You will need to install this package to use any
other MariaDB or MySQL package if the config files are not provided in the
package itself.
%endif
 
 
%if %{with common}
%package          -n %{pkgname}-common
Summary:          The shared files required by server and client
BuildArch:        noarch
%if 0%{?flatpak}
Requires:         mariadb-connector-c-config
%else
Requires:         %{_sysconfdir}/my.cnf
%endif
 
# Only conflicts, provides would add %%{_isa} provides for noarch,
# which is not wanted
%conflict_with_other_streams common
 
%if %{without clibrary}
Obsoletes: %{pkgname}-libs <= %{sameevr}
%endif
 
%description      -n %{pkgname}-common
The package provides the essential shared files for any MariaDB program.
You will need to install this package to use any other MariaDB package.
%endif
 
 
%if %{with errmsg}
%package          -n %{pkgname}-errmsg
Summary:          The error messages files required by server and embedded
BuildArch:        noarch
Requires:         %{pkgname}-common = %{sameevr}
 
# Only conflicts, provides would add %%{_isa} provides for noarch,
# which is not wanted
%conflict_with_other_streams errmsg
 
%description      -n %{pkgname}-errmsg
The package provides error messages files for the MariaDB daemon and the
embedded server. You will need to install this package to use any of those
MariaDB packages.
%endif
 
 
%if %{with galera}
%package          -n %{pkgname}-server-galera
Summary:          The configuration files and scripts for galera replication
Requires:         %{pkgname}-common = %{sameevr}
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
#Requires:         galera >= 26.4.3
BuildRequires:    selinux-policy-devel
Requires(post):   (libselinux-utils if selinux-policy-targeted)
Requires(post):   (policycoreutils if selinux-policy-targeted)
Requires(post):   (policycoreutils-python-utils if selinux-policy-targeted)
# wsrep requirements
Requires:         lsof
# Default wsrep_sst_method
Requires:         rsync
 
%virtual_conflicts_and_provides server-galera
 
%description      -n %{pkgname}-server-galera
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mariadbd)
and many different client programs and libraries. This package contains
added files to allow MariaDB server to operate as a Galera cluster
member. MariaDB is a community developed fork originally from MySQL.
%endif
 
 
%package          -n %{pkgname}-server
Summary:          The MariaDB server and related files
 
Requires:         %{pkgname}%{?_isa} = %{sameevr}
Requires:         %{pkgname}-common = %{sameevr}
Requires:         %{pkgname}-errmsg = %{sameevr}
Recommends:       %{pkgname}-server-utils%{?_isa} = %{sameevr}
Recommends:       %{pkgname}-backup%{?_isa} = %{sameevr}
%{?with_cracklib:Recommends:   %{pkgname}-cracklib-password-check%{?_isa} = %{sameevr}}
%{?with_gssapi:Recommends:     %{pkgname}-gssapi-server%{?_isa} = %{sameevr}}
%{?with_rocksdb:Suggests:      %{pkgname}-rocksdb-engine%{?_isa} = %{sameevr}}
%{?with_sphinx:Suggests:       %{pkgname}-sphinx-engine%{?_isa} = %{sameevr}}
%{?with_oqgraph:Suggests:      %{pkgname}-oqgraph-engine%{?_isa} = %{sameevr}}
%{?with_connect:Suggests:      %{pkgname}-connect-engine%{?_isa} = %{sameevr}}
%{?with_pam:Suggests:          %{pkgname}-pam%{?_isa} = %{sameevr}}
 
%{?with_bundled_fmt:Provides: bundled(fmt) = %{fmt_bundled_version}}
 
Suggests:         mytop
Suggests:         logrotate
 
%if 0%{?flatpak}
Requires:         mariadb-connector-c-config
%else
Requires:         %{_sysconfdir}/my.cnf
Requires:         %{_sysconfdir}/my.cnf.d
%endif
 
%virtual_conflicts_and_provides server
 
# Additional SELinux rules (common for MariaDB & MySQL) shipped in a separate package
# For cases, where we want to fix a SELinux issues in MariaDB sooner than patched selinux-policy-targeted package is released
%if %{with require_mysql_selinux}
# The *-selinux package should only be required on SELinux enabled systems. Therefore the following rich dependency syntax should be used:
Requires:         (mysql-selinux >= 1.0.10 if selinux-policy-targeted)
# This ensures that the *-selinux package and all its dependencies are not pulled into containers and other systems that do not use SELinux.
# https://fedoraproject.org/wiki/SELinux/IndependentPolicy#Adding_dependency_to_the_spec_file_of_corresponding_package
%endif
 
Requires:         coreutils
Requires(pre):    /usr/sbin/useradd
# We require this to be present for %%{_tmpfilesdir}
Requires:         systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires}
# RHBZ#1496131; use 'iproute' instead of 'net-tools'
Requires:         iproute
 
%{?with_conflicts_mysql:Conflicts: mysql-server}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-server}
# Explicitly disallow combination mariadb-server + mysql
%{?with_conflicts_mysql:Conflicts: mysql}
%{?with_conflicts_community_mysql:Conflicts: community-mysql}
 
%description      -n %{pkgname}-server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mariadbd)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed fork from MySQL.
 
 
%if %{with oqgraph}
%package          -n %{pkgname}-oqgraph-engine
Summary:          The Open Query GRAPH engine for MariaDB
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
# boost and Judy required for oograph
BuildRequires:    boost-devel >= 1.40.0
BuildRequires:    Judy-devel
 
%virtual_conflicts_and_provides oqgraph-engine
 
%description      -n %{pkgname}-oqgraph-engine
The package provides Open Query GRAPH engine (OQGRAPH) as plugin for MariaDB
database server. OQGRAPH is a computation engine allowing hierarchies and more
complex graph structures to be handled in a relational fashion. In a nutshell,
tree structures and friend-of-a-friend style searches can now be done using
standard SQL syntax, and results joined onto other tables.
%endif
 
 
%if %{with connect}
%package          -n %{pkgname}-connect-engine
Summary:          The CONNECT storage engine for MariaDB
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
 
# As per https://jira.mariadb.org/browse/MDEV-21450
BuildRequires:    libxml2-devel
 
%virtual_conflicts_and_provides connect-engine
 
%description      -n %{pkgname}-connect-engine
The CONNECT storage engine enables MariaDB to access external local or
remote data (MED). This is done by defining tables based on different data
types, in particular files in various formats, data extracted from other DBMS
or products (such as Excel), or data retrieved from the environment
(for example DIR, WMI, and MAC tables).
%endif
 
 
%if %{with backup}
%package          -n %{pkgname}-backup
Summary:          The mariabackup tool for physical online backups
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
BuildRequires:    libarchive-devel
 
%virtual_conflicts_and_provides backup
 
%description      -n %{pkgname}-backup
MariaDB Backup is an open source tool provided by MariaDB for performing
physical online backups of InnoDB, Aria and MyISAM tables.
For InnoDB, "hot online" backups are possible.
%endif
 
 
%if %{with rocksdb}
%package          -n %{pkgname}-rocksdb-engine
Summary:          The RocksDB storage engine for MariaDB
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
Provides:         bundled(rocksdb)
 
%virtual_conflicts_and_provides rocksdb-engine
 
%description      -n %{pkgname}-rocksdb-engine
The RocksDB storage engine is used for high performance servers on SSD drives.
%endif
 
 
%if %{with cracklib}
%package          -n %{pkgname}-cracklib-password-check
Summary:          The password strength checking plugin
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
BuildRequires:    cracklib-dicts cracklib-devel
Requires:         cracklib-dicts
 
BuildRequires:    selinux-policy-devel
Requires(post):   (libselinux-utils if selinux-policy-targeted)
Requires(post):   (policycoreutils if selinux-policy-targeted)
Requires(post):   (policycoreutils-python-utils if selinux-policy-targeted)
 
%virtual_conflicts_and_provides cracklib-password-check
 
%description      -n %{pkgname}-cracklib-password-check
CrackLib is a password strength checking library. It is installed by default
in many Linux distributions and is invoked automatically (by pam_cracklib.so)
whenever the user login password is modified.
Now, with the cracklib_password_check password validation plugin, one can
also use it to check MariaDB account passwords.
%endif
 
 
%if %{with gssapi}
%package          -n %{pkgname}-gssapi-server
Summary:          GSSAPI authentication plugin for server
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
BuildRequires:    krb5-devel
 
%virtual_conflicts_and_provides gssapi-server
 
%description      -n %{pkgname}-gssapi-server
GSSAPI authentication server-side plugin for MariaDB for passwordless login.
This plugin includes support for Kerberos on Unix.
%endif
 
 
%if %{with pam}
%package          -n %{pkgname}-pam
Summary:          PAM authentication plugin for the MariaDB server
 
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
# This subpackage NEED the 'mysql' user/group (created during mariadb-server %%pre) to be available prior installation
Requires(pre):    %{pkgname}-server%{?_isa} = %{sameevr}
 
BuildRequires:    pam-devel
 
%virtual_conflicts_and_provides pam
 
%description      -n %{pkgname}-pam
PAM authentication server-side plugin for MariaDB.
%endif
 
 
%if %{with sphinx}
%package          -n %{pkgname}-sphinx-engine
Summary:          The Sphinx storage engine for MariaDB
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
BuildRequires:    sphinx libsphinxclient libsphinxclient-devel
Requires:         sphinx libsphinxclient
 
%virtual_conflicts_and_provides sphinx-engine
 
%description      -n %{pkgname}-sphinx-engine
The Sphinx storage engine for MariaDB.
%endif
 
 
%if %{with s3}
%package          -n %{pkgname}-s3-engine
Summary:          The S3 storage engine for MariaDB
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
 
BuildRequires:    curl-devel
 
%virtual_conflicts_and_provides s3-engine
 
%description      -n %{pkgname}-s3-engine
The S3 read only storage engine allows archiving MariaDB tables in Amazon S3,
or any third-party public or private cloud that implements S3 API,
but still have them accessible for reading in MariaDB.
%endif


%package          -n %{pkgname}-server-utils
Summary:          Non-essential server utilities for MariaDB/MySQL applications
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
# mysqlhotcopy needs DBI/DBD support
Requires:         perl(DBI) 
#Requires:        perl(DBD::MariaDB)
 
%virtual_conflicts_and_provides server-utils
 
%{?with_conflicts_mysql:Conflicts: mysql-server}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-server}
 
%description      -n %{pkgname}-server-utils
This package contains all non-essential server utilities and scripts for
managing databases. It also contains all utilities requiring Perl and it is
the only MariaDB sub-package with the corresponding client-utils one, except
test subpackage, that depends on Perl.

 
%if %{with devel}
%package          -n %{pkgname}-devel
Summary:          Files for development of MariaDB/MySQL applications
%{?with_clibrary:Requires:         %{pkgname}-libs%{?_isa} = %{sameevr}}
Requires:         openssl-devel
%if %{without clibrary}
Requires:         mariadb-connector-c-devel >= 3.0
%endif
 
%virtual_conflicts_and_provides devel
 
%{?with_conflicts_mysql:Conflicts: mysql-devel}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-devel}
 
%description      -n %{pkgname}-devel
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed branch of MySQL.
%if %{with clibrary}
This package contains everything needed for developing MariaDB/MySQL client
and server plugins and applications.
%else
This package contains everything needed for developing MariaDB/MySQL server
plugins and applications. For developing client applications, use
mariadb-connector-c package.
%endif
%endif
 
 
%if %{with embedded}
%package          -n %{pkgname}-embedded
Summary:          MariaDB as an embeddable library
Requires:         %{pkgname}-common = %{sameevr}
Requires:         %{pkgname}-errmsg = %{sameevr}
 
%virtual_conflicts_and_provides embedded
 
%description      -n %{pkgname}-embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed fork from MySQL.
 
 
%package          -n %{pkgname}-embedded-devel
Summary:          Development files for MariaDB as an embeddable library
Requires:         %{pkgname}-embedded%{?_isa} = %{sameevr}
Requires:         %{pkgname}-devel%{?_isa} = %{sameevr}
# embedded-devel should require libaio-devel (rhbz#1290517)
Requires:         libaio-devel
 
%virtual_conflicts_and_provides embedded-devel
 
%{?with_conflicts_mysql:Conflicts: mysql-embedded-devel}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-embedded-devel}
 
%description      -n %{pkgname}-embedded-devel
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed fork from MySQL.
This package contains files needed for developing and testing with
the embedded version of the MariaDB server.
%endif
 
 
%if %{with test}
%package          -n %{pkgname}-test
Summary:          The test suite distributed with MariaDB
Requires:         %{pkgname}%{?_isa} = %{sameevr}
Requires:         %{pkgname}-common = %{sameevr}
Requires:         %{pkgname}-server%{?_isa} = %{sameevr}
Requires:         patch
Requires:         perl(Env)
Requires:         perl(Exporter)
Requires:         perl(Fcntl)
Requires:         perl(File::Temp)
Requires:         perl(Data::Dumper)
Requires:         perl(Getopt::Long)
Requires:         perl(IPC::Open3)
Requires:         perl(Socket)
Requires:         perl(Sys::Hostname)
Requires:         perl(Test::More)
Requires:         perl(Time::HiRes)
 
%virtual_conflicts_and_provides test
 
%{?with_conflicts_mysql:Conflicts: mysql-test}
%{?with_conflicts_community_mysql:Conflicts: community-mysql-test}
 
%description      -n %{pkgname}-test
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed fork from MySQL.
This package contains the regression test suite distributed with the MariaDB
sources.
%endif
 
 
%prep
%setup -q -n %{majorname}-%{version}
 
# Remove bundled code that is unused (all cases in which we use the system version of the library instead)
# as required by https://docs.fedoraproject.org/en-US/packaging-guidelines/#bundling
rm -r zlib libmariadb/external/zlib
rm -r win libmariadb/win
rm -r extra/wolfssl
rm -r storage/columnstore
rm -r debian
 
%if %{with bundled_fmt}
mkdir -p redhat-linux-build/extra/libfmt/
mv %{SOURCE1} redhat-linux-build/extra/libfmt/
%endif
 
# Remove JAR files that upstream puts into tarball
find . -name "*.jar" -type f -exec rm --verbose -f {} \;
# Remove testsuite for the mariadb-connector-c
rm -rf libmariadb/unittest
%if %{without rocksdb}
rm -r storage/rocksdb/
%endif

	
%patch -P4 -p1
%patch -P7 -p1
%patch -P9 -p1
%if %{with rocksdb}
%patch -P12 -p1 -d storage/rocksdb/rocksdb/
%endif
%if %{with bundled_fmt}
%patch -P13 -p1
%endif
 
%patch -P14 -p1

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE50} | tee -a mysql-test/unstable-tests
 
# disable some tests failing on different architectures
%ifarch %{arm} aarch64
cat %{SOURCE51} | tee -a mysql-test/unstable-tests
%endif
 
%ifarch s390 s390x
cat %{SOURCE52} | tee -a mysql-test/unstable-tests
%endif
 
%ifarch ppc ppc64 ppc64p7 ppc64le
cat %{SOURCE53} | tee -a mysql-test/unstable-tests
%endif
 
cp %{SOURCE2} %{SOURCE3} %{SOURCE10} %{SOURCE11} %{SOURCE12} \
   %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE18} %{SOURCE70} %{SOURCE73} scripts
 
%if %{with galera}
# prepare selinux policy
mkdir selinux
sed 's/mariadb-server-galera/%{majorname}-server-galera/' %{SOURCE72} > selinux/%{majorname}-server-galera.te
%endif
 
 
# Get version of PCRE, that upstream use
pcre_version=`grep -e "https://github.com/PCRE2Project/pcre2/releases/download" cmake/pcre.cmake | sed -r "s;.*pcre2-([[:digit:]]+\.[[:digit:]]+).*;\1;" `
 
# Check if the PCRE version in macro 'pcre_bundled_version', used in Provides: bundled(...), is the same version as upstream actually bundles
%if %{without unbundled_pcre}
if [ %{pcre_bundled_version} != "$pcre_version" ] ; then
  echo -e "\n Error: Bundled PCRE version is not correct. \n\tBundled version number: %{pcre_bundled_version} \n\tUpstream version number: $pcre_version\n"
  exit 1
fi
%else
# Check if the PCRE version that upstream use, is the same as the one present in system
pcre_system_version=`pkgconf /usr/%{_lib}/pkgconfig/libpcre2-*.pc --modversion 2>/dev/null | head -n 1`
 
if [ "$pcre_system_version" != "$pcre_version" ] ; then
  echo -e "\n Warning: Error: Bundled PCRE version is not correct. \n\tSystem version number: $pcre_system_version \n\tUpstream version number: $pcre_version\n"
fi
%endif
 
 
 
%build
# fail quickly and obviously if user tries to build as root
%if %runselftest
    if [ x"$(id -u)" = "x0" ]; then
        echo "mysql's regression tests fail if run as root."
        echo "If you really need to build the RPM as root, use"
        echo "--nocheck to skip the regression tests."
        exit 1
    fi
%endif
 
# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.
%cmake \
         -DBUILD_CONFIG=mysql_release \
         -DFEATURE_SET="community" \
         -DINSTALL_LAYOUT=RPM \
         -DDAEMON_NAME="%{daemon_name}" \
         -DDAEMON_NO_PREFIX="%{daemon_no_prefix}" \
         -DLOG_LOCATION="%{logfile}" \
         -DPID_FILE_DIR="%{pidfiledir}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DRPM="%{?rhel:rhel%{rhel}}%{!?rhel:fedora%{fedora}}" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
         -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
         -DINSTALL_DOCDIR="share/doc/%{majorname}" \
         -DINSTALL_DOCREADMEDIR="share/doc/%{majorname}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_INFODIR=share/info \
         -DINSTALL_LIBDIR="%{_lib}" \
         -DINSTALL_MANDIR=share/man \
         -DINSTALL_MYSQLSHAREDIR=share/%{majorname} \
         -DINSTALL_MYSQLTESTDIR=%{?with_test:share/mysql-test}%{!?with_test:} \
         -DINSTALL_PLUGINDIR="%{_lib}/%{majorname}/plugin" \
         -DINSTALL_SBINDIR=libexec \
         -DINSTALL_SCRIPTDIR=bin \
         -DINSTALL_SUPPORTFILESDIR=share/%{majorname} \
         -DMYSQL_DATADIR="%{dbdatadir}" \
         -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
         -DTMPDIR=/var/tmp \
         -DGRN_DATA_DIR=share/%{majorname}-server/groonga \
         -DGROONGA_NORMALIZER_MYSQL_PROJECT_NAME=%{majorname}-server/groonga-normalizer-mysql \
         -DENABLED_LOCAL_INFILE=ON \
         -DENABLE_DTRACE=ON \
         -DSECURITY_HARDENED=OFF \
         -DWITH_WSREP=%{?with_galera:ON}%{!?with_galera:OFF} \
         -DWITH_INNODB_DISALLOW_WRITES=%{?with_galera:ON}%{!?with_galera:OFF} \
         -DWITH_EMBEDDED_SERVER=%{?with_embedded:ON}%{!?with_embedded:OFF} \
         -DWITH_MARIABACKUP=%{?with_backup:ON}%{!?with_backup:NO} \
         -DWITH_UNIT_TESTS=%{?with_test:ON}%{!?with_test:NO} \
         -DCONC_WITH_SSL=%{?with_clibrary:ON}%{!?with_clibrary:NO} \
         -DWITH_SSL=system \
         -DWITH_ZLIB=system \
         -DWITH_LIBFMT=%{?with_bundled_fmt:bundled}%{!?with_bundled_fmt:system} \
         -DPLUGIN_PROVIDER_LZ4=%{?with_lz4:DYNAMIC}%{!?with_lz4:NO} \
         -DWITH_ROCKSDB_LZ4=%{?with_lz4:ON}%{!?with_lz4:OFF} \
         -DPLUGIN_PROVIDER_BZIP2=%{?with_bzip2:DYNAMIC}%{!?with_bzip2:NO} \
         -DWITH_ROCKSDB_BZip2=%{?with_bzip2:ON}%{!?with_bzip2:OFF} \
         -DPLUGIN_PROVIDER_LZMA=%{?with_lzma:DYNAMIC}%{!?with_lzma:NO} \
         \
         -DPLUGIN_MROONGA=%{?with_mroonga:DYNAMIC}%{!?with_mroonga:NO} \
         -DPLUGIN_OQGRAPH=%{?with_oqgraph:DYNAMIC}%{!?with_oqgraph:NO} \
         -DPLUGIN_CRACKLIB_PASSWORD_CHECK=%{?with_cracklib:DYNAMIC}%{!?with_cracklib:NO} \
         -DPLUGIN_ROCKSDB=%{?with_rocksdb:DYNAMIC}%{!?with_rocksdb:NO} \
         -DPLUGIN_SPHINX=%{?with_sphinx:DYNAMIC}%{!?with_sphinx:NO} \
         -DPLUGIN_CONNECT=%{?with_connect:DYNAMIC}%{!?with_connect:NO} \
         -DPLUGIN_S3=%{?with_s3:DYNAMIC}%{!?with_s3:NO} \
         -DPLUGIN_AUTH_PAM=%{?with_pam:YES}%{!?with_pam:NO} \
         -DPLUGIN_AUTH_PAM_V1=%{?with_pam:DYNAMIC}%{!?with_pam:NO} \
         -DPLUGIN_COLUMNSTORE=NO \
         -DPLUGIN_CLIENT_ED25519=OFF \
         -DPLUGIN_CACHING_SHA2_PASSWORD=%{?with_clibrary:DYNAMIC}%{!?with_clibrary:OFF} \
         -DPLUGIN_AWS_KEY_MANAGEMENT=OFF \
         -DCONNECT_WITH_MONGO=OFF \
         -DCONNECT_WITH_JDBC=OFF \
         -DPLUGIN_HASHICORP_KEY_MANAGEMENT=%{?with_hashicorp:DYNAMIC}%{!?with_hashicorp:NO}
 
# The -DSECURITY_HARDENED is used to force a set of compilation flags for hardening
# The issue is that the MariaDB upstream level of hardening is lower than expected by Red Hat
# We disable this option to the default compilation flags (which have higher level of hardening) will be used
 
 
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
 
%if %{with debug}
# Override all optimization flags when making a debug build
# -D_FORTIFY_SOURCE requires optimizations enabled. Disable the fortify.
%undefine _fortify_level
CFLAGS=`echo "$CFLAGS" | sed -r 's/-O[0123]//'`
 
CFLAGS="$CFLAGS -O0 -g"
 
# Fixes for Fedora 32 & Rawhide (GCC 10.0):
%if 0%{?fedora} >= 32
CFLAGS="$CFLAGS -Wno-error=class-memaccess"
CFLAGS="$CFLAGS -Wno-error=enum-conversion"
# endif f32
%endif
# endif debug
%endif
 
CXXFLAGS="$CFLAGS"
CPPFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS CPPFLAGS
 
 
# Print all Cmake options values; "-LAH" means "List Advanced Help"
#cmake -B %{_vpath_builddir} -LAH
 
%cmake_build
# build selinux policy
%if %{with galera}
#pushd selinux
#make -f /usr/share/selinux/devel/Makefile %{majorname}-server-galera.pp
%endif
 
 
 
%install
%cmake_install
# multilib header support #1625157
#for header in mysql/server/my_config.h mysql/server/private/config.h; do
#%multilib_fix_c_header --file %{_includedir}/$header
#done
 
ln -s mysql_config.1.gz %{buildroot}%{_mandir}/man1/mariadb_config.1.gz
 
# multilib support for shell scripts
# we only apply this to known Red Hat multilib arches, per bug #181335
if [ %multilib_capable ]
then
mv %{buildroot}%{_bindir}/mysql_config %{buildroot}%{_bindir}/mysql_config-%{__isa_bits}
install -p -m 0755 %{_vpath_builddir}/scripts/mysql_config_multilib %{buildroot}%{_bindir}/mysql_config
# Copy manual page for multilib mysql_config; https://jira.mariadb.org/browse/MDEV-11961
ln -s mysql_config.1 %{buildroot}%{_mandir}/man1/mysql_config-%{__isa_bits}.1
fi
 
# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also %%{majorname}-file-contents.patch)
install -p -m 644 %{_vpath_builddir}/Docs/INFO_SRC %{buildroot}%{_libdir}/%{majorname}/
install -p -m 644 %{_vpath_builddir}/Docs/INFO_BIN %{buildroot}%{_libdir}/%{majorname}/
rm -r %{buildroot}%{_datadir}/doc/%{majorname}/MariaDB-server-%{version}
 
# Logfile creation
mkdir -p %{buildroot}%{logfiledir}
chmod 0750 %{buildroot}%{logfiledir}
touch %{buildroot}%{logfile}
 
# current setting in my.cnf is to use /var/run/mariadb for creating pid file,
# however since my.cnf is not updated by RPM if changed, we need to create mysqld
# as well because users can have odd settings in their /etc/my.cnf
mkdir -p %{buildroot}%{pidfiledir}
install -p -m 0755 -d %{buildroot}%{dbdatadir}
 
%if %{with config}
install -D -p -m 0644 %{_vpath_builddir}/scripts/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
%else
rm %{_vpath_builddir}/scripts/my.cnf
rm %{buildroot}%{_sysconfdir}/my.cnf
%endif
 
# use different config file name for each variant of server (mariadb / mysql)
mv %{buildroot}%{_sysconfdir}/my.cnf.d/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{majorname}-server.cnf
 
# Remove upstream SysV init script and a symlink to that, we use systemd
rm %{buildroot}%{_libexecdir}/rcmysql
# Remove upstream Systemd service files
rm -r %{buildroot}%{_datadir}/%{majorname}/systemd
# Our downstream Systemd service file have set aliases to the "mysql" names in the [Install] section.
# They can be enabled / disabled by "systemctl enable / diable <service_name>"
rm %{buildroot}%{_unitdir}/{mysql,mysqld}.service
 
# install systemd unit files and scripts for handling server startup
install -D -p -m 644 %{_vpath_builddir}/scripts/mysql.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 644 %{_vpath_builddir}/scripts/mysql@.service %{buildroot}%{_unitdir}/%{daemon_name}@.service
 
# helper scripts for service starting
install -p -m 755 %{_vpath_builddir}/scripts/mariadb-prepare-db-dir %{buildroot}%{_libexecdir}/mariadb-prepare-db-dir
install -p -m 755 %{_vpath_builddir}/scripts/mariadb-check-socket %{buildroot}%{_libexecdir}/mariadb-check-socket
install -p -m 755 %{_vpath_builddir}/scripts/mariadb-check-upgrade %{buildroot}%{_libexecdir}/mariadb-check-upgrade
install -p -m 644 %{_vpath_builddir}/scripts/mariadb-scripts-common %{buildroot}%{_libexecdir}/mariadb-scripts-common
 
# Install downstream version of tmpfiles
install -D -p -m 0644 %{_vpath_builddir}/scripts/mariadb.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{majorname}.conf
echo "d %{pidfiledir} 0755 mysql mysql -" >>%{buildroot}%{_tmpfilesdir}/%{majorname}.conf
 
# Install additional cracklib selinux policy
%if %{with cracklib}
mkdir -p %{buildroot}%{_datadir}/selinux/packages/targeted/
mv %{buildroot}%{_datadir}/mariadb/policy/selinux/mariadb-plugin-cracklib-password-check.pp %{buildroot}%{_datadir}/selinux/packages/targeted/%{majorname}-plugin-cracklib-password-check.pp
rm %{buildroot}%{_datadir}/mariadb/policy/selinux/mariadb-plugin-cracklib-password-check.te
%endif
 
%if %{with test}
# mysql-test includes one executable that doesn't belong under /usr/share, so move it and provide a symlink
mv %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir}
ln -s ../../../../../bin/my_safe_process %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process
# Provide symlink expected by RH QA tests
ln -s unstable-tests %{buildroot}%{_datadir}/mysql-test/rh-skipped-tests.list
%endif
 
 
# Client that uses libmysqld embedded server.
# Pretty much like normal mysql command line client, but it doesn't require a running mariadb server.
%{?with_embedded:rm %{buildroot}%{_bindir}/{mariadb-,mysql_}embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_,mariadb-}embedded.1*
# Static libraries
rm %{buildroot}%{_libdir}/*.a
# This script creates the MySQL system tables and starts the server.
# Upstream says:
#   It looks like it's just "mysql_install_db && mysqld_safe"
#   I've never heard of anyone using it, I'd say, no need to pack it.
rm %{buildroot}%{_datadir}/%{majorname}/binary-configure
# FS files first-bytes recoginiton
# Not updated by upstream since nobody realy use that
rm %{buildroot}%{_datadir}/%{majorname}/magic
 
# Upstream ships them because of, https://jira.mariadb.org/browse/MDEV-10797
# In Fedora we use our own systemd unit files and scripts
rm %{buildroot}%{_datadir}/%{majorname}/mysql.server
rm %{buildroot}%{_datadir}/%{majorname}/mysqld_multi.server
 
# Binary for monitoring MySQL performance
# Shipped as a standalone package in Fedora
rm %{buildroot}%{_bindir}/mytop
rm %{buildroot}%{_mandir}/man1/mytop.1*
 
# Should be shipped with mariadb-connector-c
rm %{buildroot}%{_mandir}/man1/mariadb_config.1*
 
# for compatibility with upstream RPMs, create mysqld symlink in sbin
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_libexecdir}/mysqld %{buildroot}%{_sbindir}/mysqld
ln -s %{_libexecdir}/mariadbd %{buildroot}%{_sbindir}/mariadbd
 
# copy additional docs into build tree so %%doc will find them
install -p -m 0644 %{SOURCE6} %{basename:%{SOURCE6}}
install -p -m 0644 %{SOURCE16} %{basename:%{SOURCE16}}
 
%if %{with galera}
# Add wsrep_sst_rsync_tunnel script
install -p -m 0755 scripts/wsrep_sst_rsync_tunnel %{buildroot}%{_bindir}/wsrep_sst_rsync_tunnel
install -p -m 0644 %{SOURCE8} %{basename:%{SOURCE8}}
 
# install the clustercheck script
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/sysconfig/clustercheck
install -p -m 0755 %{_vpath_builddir}/scripts/clustercheck %{buildroot}%{_bindir}/clustercheck
# clustercheck license
install -p -m 0644 %{SOURCE71} %{basename:%{SOURCE71}}
 
# install galera config file
sed -i -r 's|^wsrep_provider=none|wsrep_provider=%{_libdir}/galera/libgalera_smm.so|' %{_vpath_builddir}/support-files/wsrep.cnf
install -p -m 0644 %{_vpath_builddir}/support-files/wsrep.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/galera.cnf
 
# install additional galera selinux policy
#install -p -m 644 -D selinux/%{majorname}-server-galera.pp %{buildroot}%{_datadir}/selinux/packages/targeted/%{majorname}-server-galera.pp
 
# Fix Galera Replication config file
#   The replication requires cluster address upon startup (which is end-user specific).
#   Disable it entirely, rather than have it failing out-of-the-box.
sed -i 's/^wsrep_on=1/wsrep_on=0/' %{buildroot}%{_sysconfdir}/my.cnf.d/galera.cnf
%endif
 
# remove duplicate logrotate script
rm %{buildroot}%{_datadir}/mariadb/mariadb.logrotate
# Remove AppArmor files
rm -r %{buildroot}%{_datadir}/%{majorname}/policy/apparmor
 
# Buildroot does not have symlink /lib64 --> /usr/lib64
%if %{with pam}
mv %{buildroot}/%{_lib}/security %{buildroot}%{_libdir}
%endif
 
# Disable plugins
%if %{with gssapi}
sed -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%endif
%if %{with cracklib}
sed -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%endif
 
%if %{without embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
%endif
 
 
%if %{without clibrary}
# Client part should be included in package 'mariadb-connector-c'
[ -e %{buildroot}%{_libdir}/pkgconfig/libmariadb.pc ] && rm %{buildroot}%{_libdir}/pkgconfig/libmariadb.pc
[ -e %{buildroot}/usr/lib64/pkgconfig/libmariadb.pc ] && rm %{buildroot}/usr/lib64/pkgconfig/libmariadb.pc
 
rm %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
# Client library and links
rm %{buildroot}%{_libdir}/libmariadb.so.*
unlink %{buildroot}%{_libdir}/libmysqlclient.so
unlink %{buildroot}%{_libdir}/libmysqlclient_r.so
unlink %{buildroot}%{_libdir}/libmariadb.so
rm %{buildroot}%{_mandir}/man3/*
# Client plugins
rm %{buildroot}%{_libdir}/%{majorname}/plugin/{dialog.so,mysql_clear_password.so,sha256_password.so}
%if %{with gssapi}
rm %{buildroot}%{_libdir}/%{majorname}/plugin/auth_gssapi_client.so
%endif
%endif
 
%if %{without clibrary} || %{without devel}
rm %{buildroot}%{_bindir}/mysql_config*
rm %{buildroot}%{_bindir}/mariadb_config
rm %{buildroot}%{_bindir}/mariadb-config
rm %{buildroot}%{_mandir}/man1/mysql_config*.1*
%endif
 
%if %{without clibrary} && %{with devel}
# This files are already included in mariadb-connector-c
rm %{buildroot}%{_includedir}/mysql/mysql_version.h
rm %{buildroot}%{_includedir}/mysql/{errmsg.h,ma_list.h,ma_pvio.h,mariadb_com.h,\
mariadb_ctype.h,mariadb_dyncol.h,mariadb_stmt.h,mariadb_version.h,ma_tls.h,mysqld_error.h,mysql.h,mariadb_rpl.h}
rm -r %{buildroot}%{_includedir}/mysql/{mariadb,mysql}
%endif
 
%if %{without devel}
rm -r %{buildroot}%{_includedir}/mysql
rm %{buildroot}%{_datadir}/aclocal/mysql.m4
rm %{buildroot}%{_libdir}/pkgconfig/mariadb.pc
%if %{with clibrary}
rm %{buildroot}%{_libdir}/libmariadb*.so
unlink %{buildroot}%{_libdir}/libmysqlclient.so
unlink %{buildroot}%{_libdir}/libmysqlclient_r.so
%endif
%endif
 
%if %{without client}
rm %{buildroot}%{_bindir}/msql2mysql
rm %{buildroot}%{_bindir}/{mysql,mariadb}
rm %{buildroot}%{_bindir}/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}
rm %{buildroot}%{_bindir}/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}
 
rm %{buildroot}%{_mandir}/man1/msql2mysql.1*
rm %{buildroot}%{_mandir}/man1/{mysql,mariadb}.1*
rm %{buildroot}%{_mandir}/man1/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}.1*
rm %{buildroot}%{_mandir}/man1/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}.1*
 
rm %{buildroot}%{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%endif
 
%if %{without common}
rm -r %{buildroot}%{_datadir}/%{majorname}/charsets
%endif
 
%if %{without errmsg}
rm %{buildroot}%{_datadir}/%{majorname}/errmsg-utf8.txt
rm -r %{buildroot}%{_datadir}/%{majorname}/{english,czech,danish,dutch,estonian,\
french,german,greek,hungarian,italian,japanese,korean,norwegian,norwegian-ny,\
polish,portuguese,romanian,russian,serbian,slovak,spanish,swedish,ukrainian,hindi,\
bulgarian,chinese,georgian}
%endif
 
%if %{without test}
%if %{with embedded}
rm %{buildroot}%{_bindir}/test-connect-t
rm %{buildroot}%{_bindir}/{mysql_client_test_embedded,mysqltest_embedded}
rm %{buildroot}%{_bindir}/{mariadb-client-test-embedded,mariadb-test-embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
# endif embedded
%endif
%if %{with pam}
rm %{buildroot}/suite/plugins/pam/mariadb_mtr
rm %{buildroot}/suite/plugins/pam/pam_mariadb_mtr.so
# endif pam
%endif
rm %{buildroot}%{_bindir}/{mysql_client_test,mysqltest}
rm %{buildroot}%{_bindir}/{mariadb-client-test,mariadb-test}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test,mysqltest,my_safe_process}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test,mariadb-test}.1*
rm %{buildroot}%{_mandir}/man1/{mysql-test-run,mysql-stress-test}.pl.1*
%endif
 
%if %{without rocksdb}
rm %{buildroot}%{_mandir}/man1/{mysql_,mariadb-}ldb.1*
rm %{buildroot}%{_mandir}/man1/myrocks_hotbackup.1*
%endif
 
%if %{without backup}
rm %{buildroot}%{_mandir}/man1/maria{,db-}backup.1*
rm %{buildroot}%{_mandir}/man1/mbstream.1*
%endif
 
%if %{without s3}
rm %{buildroot}%{_mandir}/man1/aria_s3_copy.1*
%endif
 
%check
cd unittest
perl ./unit.pl --verbose run
%if %{with test}
%if %runselftest
# The cmake build scripts don't provide any simple way to control the
# options for mysql-test-run, so ignore the make target and just call it
# manually.  Nonstandard options chosen are:
# --force to continue tests after a failure
# no retries please
# test SSL with --ssl
# skip tests that are listed in rh-skipped-tests.list
# avoid redundant test runs with --binlog-format=mixed
# increase timeouts to prevent unwanted failures during mass rebuilds
 
# Usefull arguments:
#    --do-test=mysql_client_test_nonblock \
#    --skip-rpl
#    --suite=roles
#    --mem for running in the RAM; Not enough space in KOJI for this
 
(
  set -ex
  cd %{buildroot}%{_datadir}/mysql-test
 
  export common_testsuite_arguments=" --port-base=$(( $(date +%s) % 20000 + 10000 )) --parallel=auto --force --retry=2 --suite-timeout=900 --testcase-timeout=30 --mysqld=--binlog-format=mixed --force-restart --shutdown-timeout=60 --max-test-fail=5 "
 
  # If full testsuite has already been run on this version and we don't explicitly want the full testsuite to be run
  if [[ "%{last_tested_version}" == "%{version}" ]] && [[ %{force_run_testsuite} -eq 0 ]]
  then
    # in further rebuilds only run the basic "main" suite (~800 tests)
    echo -e "\n\nRunning just the base testsuite\n\n"
    perl ./mysql-test-run.pl $common_testsuite_arguments --ssl --suite=main --mem --skip-test-list=unstable-tests
  fi
 
  # If either this version wasn't marked as tested yet or I explicitly want to run the testsuite, run everything we have (~4000 test)
  if [[ "%{last_tested_version}" != "%{version}" ]] || [[ %{force_run_testsuite} -ne 0 ]]
  then
    echo -e "\n\nRunning the advanced testsuite\n\n"
    perl ./mysql-test-run.pl $common_testsuite_arguments --ssl --big-test --skip-test=spider \
    %if %{ignore_testsuite_result}
      --max-test-fail=9999 || :
    %else
      --skip-test-list=unstable-tests
    %endif
 
    # Spider tests can't be run in the Fedora KOJI at this moment, see #2291227
    %if 0
    # Second run for the SPIDER suites that fail with SCA (ssl self signed certificate)
    perl ./mysql-test-run.pl $common_testsuite_arguments --skip-ssl --big-test --suite=spider,spider/bg,spider/bugfix \
    %if %{ignore_testsuite_result}
      --max-test-fail=999 || :
    %else
      --skip-test-list=unstable-tests
    %endif
    %endif
  # blank line
  fi
 
  # There might be a dangling symlink left from the testing, remove it to not be installed
  rm -rf ./var
  # Remove temporary files created by the testsuite execution
  find ./ -type f -name '*~' -exec rm {} +
)
 
# NOTE: the Spider SE has 2 more hidden testsuites "oracle" and "oracle2".
#       however, all of the tests fail with: "failed: 12521: Can't use wrapper 'oracle' for SQL connection"
 
%endif
%endif
 
 
 
%pre -n %{pkgname}-server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{dbdatadir} -s /sbin/nologin \
  -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :
 
%post -n %{pkgname}-server
%systemd_post %{daemon_name}.service
 
%preun -n %{pkgname}-server
%systemd_preun %{daemon_name}.service
 
%postun -n %{pkgname}-server
%systemd_postun_with_restart %{daemon_name}.service
 
%if %{with galera}
%post -n %{pkgname}-server-galera
#%selinux_modules_install -s "targeted" %{_datadir}/selinux/packages/targeted/%{majorname}-server-galera.pp
 
# Allow ports needed for the replication:
# https://fedoraproject.org/wiki/SELinux/IndependentPolicy#Port_Labeling
if [ $1 -eq 1 ]; then
  # https://mariadb.com/kb/en/library/configuring-mariadb-galera-cluster/#network-ports
  #   Galera Replication Port
  semanage port -a -t mysqld_port_t -p tcp 4567 >/dev/null 2>&1 || :
  semanage port -a -t mysqld_port_t -p udp 4567 >/dev/null 2>&1 || :
  #   IST Port
  semanage port -a -t mysqld_port_t -p tcp 4568 >/dev/null 2>&1 || :
  #   SST Port
  semanage port -a -t mysqld_port_t -p tcp 4444 >/dev/null 2>&1 || :
fi
 
%postun -n %{pkgname}-server-galera
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s "targeted" %{majorname}-server-galera
 
    # Delete port labeling when the package is removed
    # https://fedoraproject.org/wiki/SELinux/IndependentPolicy#Port_Labeling
    semanage port -d -t mysqld_port_t -p tcp 4567 >/dev/null 2>&1 || :
    semanage port -d -t mysqld_port_t -p udp 4567 >/dev/null 2>&1 || :
    semanage port -d -t mysqld_port_t -p tcp 4568 >/dev/null 2>&1 || :
    semanage port -d -t mysqld_port_t -p tcp 4444 >/dev/null 2>&1 || :
fi
%endif
 
%if %{with cracklib}
%post -n %{pkgname}-cracklib-password-check
%selinux_modules_install -s "targeted" %{_datadir}/selinux/packages/targeted/%{majorname}-plugin-cracklib-password-check.pp
 
%postun -n %{pkgname}-cracklib-password-check
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s "targeted" %{majorname}-plugin-cracklib-password-check
fi
%endif
 
 
 
%if %{with client}
%files -n %{pkgname}
%{_bindir}/msql2mysql
%{_bindir}/{mysql,mariadb}
%{_bindir}/mysql{admin,binlog,check,dump,import,_plugin,show,slap,_waitpid}
%{_bindir}/mariadb-{admin,binlog,check,dump,import,plugin,show,slap,waitpid}
 
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/{mysql,mariadb}.1*
%{_mandir}/man1/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}.1*
%{_mandir}/man1/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}.1*
 
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
 
%files -n %{pkgname}-client-utils
%{_bindir}/mysql{access,_find_rows}
%{_bindir}/mariadb-{access,find-rows}
%{_mandir}/man1/mysql{access,_find_rows}.1*
%{_mandir}/man1/mariadb-{access,find-rows}.1*
%endif
 
%if %{with clibrary}
%files -n %{pkgname}-libs
%exclude %{_libdir}/{libmysqlclient.so.18,libmariadb.so,libmysqlclient.so,libmysqlclient_r.so}
%{_libdir}/libmariadb.so*
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%endif
 
%if %{with config}
%files -n %{pkgname}-config
# although the default my.cnf contains only server settings, we put it in the
# common package because it can be used for client settings too.
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%endif
 
%if %{with common}
%files -n %{pkgname}-common
%doc %{_datadir}/doc/%{majorname}
%dir %{_datadir}/%{majorname}
%{_datadir}/%{majorname}/charsets
%if %{with clibrary}
%{_libdir}/%{majorname}/plugin/dialog.so
%{_libdir}/%{majorname}/plugin/mysql_clear_password.so
%endif
%endif
 
%if %{with errmsg}
%files -n %{pkgname}-errmsg
%{_datadir}/%{majorname}/errmsg-utf8.txt
%{_datadir}/%{majorname}/english
%lang(cs) %{_datadir}/%{majorname}/czech
%lang(da) %{_datadir}/%{majorname}/danish
%lang(nl) %{_datadir}/%{majorname}/dutch
%lang(et) %{_datadir}/%{majorname}/estonian
%lang(fr) %{_datadir}/%{majorname}/french
%lang(de) %{_datadir}/%{majorname}/german
%lang(el) %{_datadir}/%{majorname}/greek
%lang(hi) %{_datadir}/%{majorname}/hindi
%lang(hu) %{_datadir}/%{majorname}/hungarian
%lang(it) %{_datadir}/%{majorname}/italian
%lang(ja) %{_datadir}/%{majorname}/japanese
%lang(ko) %{_datadir}/%{majorname}/korean
%lang(no) %{_datadir}/%{majorname}/norwegian
%lang(no) %{_datadir}/%{majorname}/norwegian-ny
%lang(pl) %{_datadir}/%{majorname}/polish
%lang(pt) %{_datadir}/%{majorname}/portuguese
%lang(ro) %{_datadir}/%{majorname}/romanian
%lang(ru) %{_datadir}/%{majorname}/russian
%lang(sr) %{_datadir}/%{majorname}/serbian
%lang(sk) %{_datadir}/%{majorname}/slovak
%lang(es) %{_datadir}/%{majorname}/spanish
%lang(sv) %{_datadir}/%{majorname}/swedish
%lang(uk) %{_datadir}/%{majorname}/ukrainian
%lang(bg) %{_datadir}/%{majorname}/bulgarian
%lang(zh) %{_datadir}/%{majorname}/chinese
%lang(ka) %{_datadir}/%{majorname}/georgian
%endif
 
%if %{with galera}
%files -n %{pkgname}-server-galera
%doc Docs/README-wsrep
%license LICENSE.clustercheck
%{_bindir}/clustercheck
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%{_mandir}/man1/galera_new_cluster.1*
%{_mandir}/man1/galera_recovery.1*
%config(noreplace) %{_sysconfdir}/my.cnf.d/galera.cnf
%attr(0640,root,root) %ghost %config(noreplace) %{_sysconfdir}/sysconfig/clustercheck
#%{_datadir}/selinux/packages/targeted/%{majorname}-server-galera.pp
%endif
 
%files -n %{pkgname}-server
 
%{_bindir}/aria_{chk,dump_log,ftdump,pack,read_log}
%{_bindir}/mariadb-service-convert
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/my_print_defaults
 
%{_bindir}/mariadb-conv
 
%{_bindir}/mysql_{install_db,secure_installation,tzinfo_to_sql}
%{_bindir}/mariadb-{install-db,secure-installation,tzinfo-to-sql}
%{_bindir}/{mysqld_,mariadbd-}safe
%{_bindir}/{mysqld_safe_helper,mariadbd-safe-helper}
 
%{_bindir}/innochecksum
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%if %{with galera}
# wsrep_sst_common should be moved to /usr/share/mariadb: https://jira.mariadb.org/browse/MDEV-14296
%{_bindir}/wsrep_*
%{_mandir}/man1/wsrep_*.1*
%doc README.wsrep_sst_rsync_tunnel
%endif
 
%config(noreplace) %{_sysconfdir}/my.cnf.d/%{majorname}-server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset
%config(noreplace) %{_sysconfdir}/my.cnf.d/spider.cnf
 
%{?with_lz4:%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_lz4.cnf}
%{?with_bzip2:%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_bzip2.cnf}
%{?with_lzma:%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_lzma.cnf}
%{?with_lzo:%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_lzo.cnf}
%{?with_snappy:%config(noreplace) %{_sysconfdir}/my.cnf.d/provider_snappy.cnf}
 
%{?with_hashicorp:%config(noreplace) %{_sysconfdir}/my.cnf.d/hashicorp_key_management.cnf}
 
%{_sbindir}/mysqld
%{_sbindir}/mariadbd
%{_libexecdir}/{mysqld,mariadbd}
 
%{_libdir}/%{majorname}/INFO_SRC
%{_libdir}/%{majorname}/INFO_BIN
%if %{without common}
%dir %{_datadir}/%{majorname}
%endif
 
%dir %{_libdir}/%{majorname}
%dir %{_libdir}/%{majorname}/plugin
 
%{_libdir}/%{majorname}/plugin/*
%{?with_oqgraph:%exclude %{_libdir}/%{majorname}/plugin/ha_oqgraph.so}
%{?with_connect:%exclude %{_libdir}/%{majorname}/plugin/ha_connect.so}
%{?with_cracklib:%exclude %{_libdir}/%{majorname}/plugin/cracklib_password_check.so}
%{?with_rocksdb:%exclude %{_libdir}/%{majorname}/plugin/ha_rocksdb.so}
%{?with_gssapi:%exclude %{_libdir}/%{majorname}/plugin/auth_gssapi.so}
%{?with_sphinx:%exclude %{_libdir}/%{majorname}/plugin/ha_sphinx.so}
%{?with_s3:%exclude %{_libdir}/%{majorname}/plugin/ha_s3.so}
%if %{with clibrary}
%exclude %{_libdir}/%{majorname}/plugin/dialog.so
%exclude %{_libdir}/%{majorname}/plugin/mysql_clear_password.so
%endif
 
# PAM plugin; moved to a standalone sub-package
%exclude %{_libdir}/%{majorname}/plugin/{auth_pam_v1.so,auth_pam.so}
%exclude %dir %{_libdir}/%{majorname}/plugin/auth_pam_tool_dir
%exclude %{_libdir}/%{majorname}/plugin/auth_pam_tool_dir/auth_pam_tool
 
%{_mandir}/man1/aria_{chk,dump_log,ftdump,pack,read_log}.1*
%{_mandir}/man1/mariadb-service-convert.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/my_print_defaults.1*
 
%{_mandir}/man1/mariadb-conv.1*
 
%{_mandir}/man1/mysql_{install_db,secure_installation,tzinfo_to_sql}.1*
%{_mandir}/man1/mariadb-{install-db,secure-installation,tzinfo-to-sql}.1*
%{_mandir}/man1/{mysqld_,mariadbd-}safe.1*
%{_mandir}/man1/{mysqld_safe_helper,mariadbd-safe-helper}.1*
 
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man8/{mysqld,mariadbd}.8*
 
%{_mandir}/man1/mysql.server.1*
 
%{_datadir}/%{majorname}/mini-benchmark
%{_datadir}/%{majorname}/fill_help_tables.sql
%{_datadir}/%{majorname}/maria_add_gis_sp.sql
%{_datadir}/%{majorname}/maria_add_gis_sp_bootstrap.sql
%{_datadir}/%{majorname}/mysql_system_tables.sql
%{_datadir}/%{majorname}/mysql_sys_schema.sql
%{_datadir}/%{majorname}/mysql_system_tables_data.sql
%{_datadir}/%{majorname}/mysql_test_data_timezone.sql
%{_datadir}/%{majorname}/mysql_performance_tables.sql
%{_datadir}/%{majorname}/mysql_test_db.sql
%if %{with mroonga}
%dir %{_datadir}/%{majorname}/mroonga
%dir %{_datadir}/%{majorname}-server
%dir %{_datadir}/%{majorname}-server/groonga
%dir %{_datadir}/%{majorname}-server/groonga-normalizer-mysql
%{_datadir}/%{majorname}/mroonga/install.sql
%{_datadir}/%{majorname}/mroonga/uninstall.sql
%license %{_datadir}/%{majorname}/mroonga/COPYING
%license %{_datadir}/%{majorname}/mroonga/AUTHORS
%license %{_datadir}/%{majorname}-server/groonga-normalizer-mysql/lgpl-2.0.txt
%license %{_datadir}/%{majorname}-server/groonga/COPYING
%doc %{_datadir}/%{majorname}-server/groonga-normalizer-mysql/README.md
%doc %{_datadir}/%{majorname}-server/groonga/README.md
%endif
%if %{with galera}
%{_datadir}/%{majorname}/wsrep.cnf
%{_datadir}/%{majorname}/wsrep_notify
%endif
%dir %{_datadir}/%{majorname}/policy
%dir %{_datadir}/%{majorname}/policy/selinux
%{_datadir}/%{majorname}/policy/selinux/README
%{_datadir}/%{majorname}/policy/selinux/mariadb-server.*
%{_datadir}/%{majorname}/policy/selinux/mariadb.*
 
# More on socket activation or extra port service at
# https://mariadb.com/kb/en/systemd/
%{_unitdir}/%{daemon_name}.service
%{_unitdir}/%{daemon_name}@.service
%{_unitdir}/%{daemon_name}.socket
%{_unitdir}/%{daemon_name}@.socket
%{_unitdir}/%{daemon_name}-extra.socket
%{_unitdir}/%{daemon_name}-extra@.socket
%{_unitdir}/%{daemon_name}@bootstrap.service.d
 
%{_libexecdir}/mariadb-prepare-db-dir
%{_libexecdir}/mariadb-check-socket
%{_libexecdir}/mariadb-check-upgrade
%{_libexecdir}/mariadb-scripts-common
 
%attr(0755,mysql,mysql) %dir %{pidfiledir}
%attr(0755,mysql,mysql) %dir %{dbdatadir}
%attr(0750,mysql,mysql) %dir %{logfiledir}
# This does what it should.
# RPMLint error "conffile-without-noreplace-flag /var/log/mariadb/mariadb.log" is false positive.
%attr(0660,mysql,mysql) %config %ghost %verify(not md5 size mtime) %{logfile}
%config(noreplace) %{logrotateddir}/%{daemon_name}
 
%{_tmpfilesdir}/%{majorname}.conf
%{_sysusersdir}/%{majorname}.conf
 
%if %{with cracklib}
%files -n %{pkgname}-cracklib-password-check
%config(noreplace) %{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%{_libdir}/%{majorname}/plugin/cracklib_password_check.so
%{_datadir}/selinux/packages/targeted/%{majorname}-plugin-cracklib-password-check.pp
%endif
 
%if %{with backup}
%files -n %{pkgname}-backup
%{_bindir}/maria{,db-}backup
%{_bindir}/mbstream
%{_mandir}/man1/maria{,db-}backup.1*
%{_mandir}/man1/mbstream.1*
%endif
 
%if %{with rocksdb}
%files -n %{pkgname}-rocksdb-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/rocksdb.cnf
%{_bindir}/myrocks_hotbackup
%{_bindir}/{mysql_,mariadb-}ldb
%{_bindir}/sst_dump
%{_libdir}/%{majorname}/plugin/ha_rocksdb.so
%{_mandir}/man1/{mysql_,mariadb-}ldb.1*
%{_mandir}/man1/myrocks_hotbackup.1*
%endif
 
%if %{with gssapi}
%files -n %{pkgname}-gssapi-server
%{_libdir}/%{majorname}/plugin/auth_gssapi.so
%config(noreplace) %{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%endif
 
%if %{with pam}
%files -n %{pkgname}-pam
%{_libdir}/%{majorname}/plugin/{auth_pam_v1.so,auth_pam.so}
%attr(0755,root,root) %dir %{_libdir}/%{majorname}/plugin/auth_pam_tool_dir
# SUID-to-root binary. Access MUST be restricted (https://jira.mariadb.org/browse/MDEV-25126)
%attr(4750,root,mysql) %{_libdir}/%{majorname}/plugin/auth_pam_tool_dir/auth_pam_tool
%{_libdir}/security/pam_user_map.so
%config(noreplace) %{_sysconfdir}/security/user_map.conf
%endif
 
%if %{with sphinx}
%files -n %{pkgname}-sphinx-engine
%{_libdir}/%{majorname}/plugin/ha_sphinx.so
%endif
 
%if %{with oqgraph}
%files -n %{pkgname}-oqgraph-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/oqgraph.cnf
%{_libdir}/%{majorname}/plugin/ha_oqgraph.so
%endif
 
%if %{with connect}
%files -n %{pkgname}-connect-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/connect.cnf
%{_libdir}/%{majorname}/plugin/ha_connect.so
%endif
 
%if %{with s3}
%files -n %{pkgname}-s3-engine
%{_bindir}/aria_s3_copy
%{_mandir}/man1/aria_s3_copy.1*
%config(noreplace) %{_sysconfdir}/my.cnf.d/s3.cnf
%{_libdir}/%{majorname}/plugin/ha_s3.so
%endif
 
%files -n %{pkgname}-server-utils
# Perl utilities
%{_bindir}/mysql{_convert_table_format,dumpslow,_fix_extensions,hotcopy,_setpermission}
%{_bindir}/mariadb-{convert-table-format,dumpslow,fix-extensions,hotcopy,setpermission}
%{_bindir}/{mysqld_,mariadbd-}multi
 
%{_mandir}/man1/mysql{_convert_table_format,dumpslow,_fix_extensions,hotcopy,_setpermission}.1*
%{_mandir}/man1/mariadb-{convert-table-format,dumpslow,fix-extensions,hotcopy,setpermission}.1*
%{_mandir}/man1/{mysqld_,mariadbd-}multi.1*
# Utilities that can be used remotely
%{_bindir}/{mysql_,mariadb-}upgrade
%{_bindir}/perror
%{_mandir}/man1/{mysql_,mariadb-}upgrade.1*
%{_mandir}/man1/perror.1*

%if %{with devel}
%files -n %{pkgname}-devel
%{_includedir}/*
%{_datadir}/aclocal/mysql.m4
%{_libdir}/pkgconfig/*mariadb.pc
%if %{with clibrary}
%{_mandir}/man3/*
%{_libdir}/{libmysqlclient.so.18,libmariadb.so,libmysqlclient.so,libmysqlclient_r.so}
%{_bindir}/mysql_config*
%{_bindir}/mariadb_config*
%{_bindir}/mariadb-config
%{_libdir}/libmariadb.so
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlclient_r.so
%{_mandir}/man1/mysql_config*
%endif
%endif
 
%if %{with embedded}
%files -n %{pkgname}-embedded
%{_libdir}/libmariadbd.so.*
 
%files -n %{pkgname}-embedded-devel
%{_libdir}/libmysqld.so
%{_libdir}/libmariadbd.so
%endif
 
%if %{with test}
%files -n %{pkgname}-test
%if %{with embedded}
%{_bindir}/test-connect-t
%{_bindir}/{mysql_client_test_embedded,mysqltest_embedded}
%{_bindir}/{mariadb-client-test-embedded,mariadb-test-embedded}
%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
%endif
%{_bindir}/{mysql_client_test,mysqltest,mariadb-client-test,mariadb-test}
%{_bindir}/my_safe_process
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%{_mandir}/man1/{mysql_client_test,mysqltest,mariadb-client-test,mariadb-test}.1*
%{_mandir}/man1/my_safe_process.1*
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*
%endif
 
%changelog
* Mon Dec 29 2025 BinduSri Adabala <v-badabala@microsoft.com> - 10.11.15-1
- Upgrade to 10.11.15 for CVE-2025-13699

* Fri Apr 04 2025 Mayank Singh <mayansingh@microsoft.com> - 10.11.11-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified
- Fix CVE-2023-52971 with an upstream patch

* Thu Mar 27 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.11.11-1
- Auto-upgrade to 10.11.11 - for CVE-2025-21490

* Tue Nov 05 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.11.10-1
- Auto-upgrade to 10.11.10 - to address CVE-2024-21096

* Wed Feb 05 2025 Michal Schorm <mschorm@redhat.com> - 3:10.11.11-1
- Rebase to 10.11.11
 
* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3:10.11.10-4
- Add explicit BR: libxcrypt-devel
 
* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.11.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Fri Nov 29 2024 Timothée Ravier <tim@siosm.fr> - 3:10.11.10-2
- Split mariadb-access & mariadb-find-rows into a client-utils subpackage
 
* Sat Nov 16 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.10-1
- Rebase to 10.11.10
 
* Tue Aug 13 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.9-1
- Rebase to 10.11.9
 
* Tue Jul 23 2024 Lumír Balhar <lbalhar@redhat.com> - 3:10.11.8-5
- Add new systemtap-sdt-dtrace to build deps
 
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.11.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Mon Jun 10 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.8-3
- Bump release for rebuild
 
* Sun Jun 09 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.8-2
- Add wsrep_sst_rsync_tunnel script
 
* Fri Jun 07 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.8-1
- Rebase to 10.11.8
 
* Thu Jun 06 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.7-1
- Rebase to 10.11.7
- Patch 10 removed, the main.ssl_cipher test has been fixed
  and re-enabled by upstream and now passes on all architectures
 
* Tue Apr 09 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3:10.11.6-4
- Fix my.cnf dependency
 
* Wed Feb 7 2024 Filip Janus <fjanus@redhat.com> - 3:10.11.6-3
- Rename macros related to demodularization
 
* Wed Jan 31 2024 Filip Janus <fjanus@redhat.com> - 3:10.11.6-2
- Apply demodularization
- the default stream builds mariadb.rpm
- the non-default stream builds mariadbXX.XX.rpm
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.11.6-1
- Rebase to 10.11.6
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.10.7-1
- Rebase to 10.10.7
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.9.8-1
- Rebase to 10.9.8
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.8.8-1
- Rebase to 10.8.8
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.7.8-1
- Rebase to 10.7.8
 
* Thu Jan 25 2024 Michal Schorm <mschorm@redhat.com> - 3:10.6.16-1
- Rebase to 10.6.16
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Thu Nov 16 2023 Michal Schorm <mschorm@redhat.com> - 3:10.5.23-1
- Rebase to 10.5.23
 
* Mon Sep 04 2023 Michal Schorm <mschorm@redhat.com> - 3:10.5.22-1
- Rebase to 10.5.22
 
* Wed Jul 26 2023 Michal Schorm <mschorm@redhat.com> - 3:10.5.21-1
- Rebase to version 10.5.21
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Tue May 30 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.20-1
- Rebase to version 10.5.20
- Patches 11 and 13 were upstreamed
 
* Fri Apr 28 2023 Siddhesh Poyarekar <siddhesh@redhat.com> - 3:10.5.19-2
- Use _fortify_level to disable fortification in debug builds.
 
* Fri Apr 28 2023 Michal Schorm <mschorm@redhat.com> - 3:10.5.19-1
- Rebase to 10.5.19
 
* Tue Apr 11 2023 Florian Weimer <fweimer@redhat.com> - 3:10.5.18-3
- Port to C99
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Wed Nov 16 2022 Michal Schorm <mschorm@redhat.com> - 3:10.5.18-1
- Rebase to 10.5.18
- OpenSSL 3 patch upstreamed
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Mon Jun 13 2022 Michal Schorm <mschorm@redhat.com> - 3:10.5.16-2
- Release bump for rebuild
 
* Mon May 23 2022 Michal Schorm <mschorm@redhat.com> - 3:10.5.16-1
- Rebase to 10.5.16
 
* Sun Feb 20 2022 Michal Schorm <mschorm@redhat.com> - 3:10.5.15-1
- Rebase to 10.5.15
 
* Mon Feb 07 2022 Honza Horak <hhorak@redhat.com> - 3:10.5.13-3
- Fix md5 in FIPS mode with OpenSSL 3.0.0
  Resolves: #2050541
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Dec 02 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.13-1
- Rebase to 10.5.13
 
* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3:10.5.12-3
- Rebuilt with OpenSSL 3.0.0
 
* Thu Aug 26 2021 Marek Kulik <mkulik@redhat.com> - 3:10.5.12-2
- Add patch for mysql_setpermissions: BZ#1976224
 
* Sat Aug 07 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.12-1
- Rebase to 10.5.12
 
* Tue Aug 03 2021 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.11-4
- Set user_map.conf file to be noreplace config file
- Related: BZ#1989534
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Wed Jul 14 2021 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.11-2
- Rebuild against pcre2-10.37 (bug #1965025)
 
* Thu Jul 01 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.11-1
- Rebase to 10.5.11
 
* Wed May 12 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.10-2
- Use modified sources instead of the upstream original ones
 
* Tue May 11 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.10-1
- Rebase to 10.5.10
 
* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 3:10.5.9-5
- Rebuilt for removed libstdc++ symbol (#1937698)
 
* Thu Mar 18 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.9-4
- Move PAM plugin to standalone subpackage
 
* Thu Mar 18 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.9-3
- Fixed permissions on files from PAMv2 plugin
 
* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3:10.5.9-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.
 
* Wed Feb 24 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.9-1
- Rebase to 10.5.9
 
* Tue Feb 16 2021 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.8-8
- Replace the tokudb Obsoletes to the right place
- Resolves: #1928757
 
* Fri Feb 12 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.8-7
- Enhance the logrotate script
- Resolves: #1683981
 
* Fri Feb 12 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.8-6
- Fix Perl database driver dependency
 
* Wed Feb 10 2021 Michal Schorm <mschorm@redhat.com> - 3:10.5.8-5
- Add support for S3 storage engine
 
* Thu Jan 28 2021 Honza Horak <hhorak@redhat.com> - 3:10.5.8-4
- For compatibility with upstream RPMs, create mysqld symlink in sbin
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Fri Dec 11 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.8-2
- Add tokudb-engine to obsoletes
- Resolves: #1906559
 
* Wed Nov 11 2020 Michal Schorm <mschorm@redhat.com> - 3:10.5.8-1
- Rebase to 10.5.8
 
* Fri Nov 06 2020 Michal Schorm <mschorm@redhat.com> - 3:10.5.7-1
- Rebase to 10.5.7
 
* Mon Sep 21 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.5-1
- Rebase to 10.5.5
- Fix mariadb-ownsetup
- Add manual for aria_s3_copy
 
* Wed Sep 16 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.4-1
- Rebase to 10.5.4
- Add spider.cnf to the server config files
 
* Mon Sep 14 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.5.3-1
- Rebase to 10.5.3
 
* Fri Sep 11 2020 Michal Schorm <mschorm@redhat.com> - 3:10.5.2-1
- Test rebase to 10.5.2 - Beta
- TokuDB SE has been deprecated
 
* Thu Sep 10 2020 Michal Schorm <mschorm@redhat.com> - 3:10.5.1-1
- Test rebase to 10.5.1 - Beta
 
* Thu Sep 10 2020 Michal Schorm <mschorm@redhat.com> - 3:10.5.0-1
- Test rebase to 10.5.0 - Alpha
 
* Sun Sep 06 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.14-3
- Resolves: #1851605
 
* Thu Sep 03 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.14-2
- Resolves: #1873999, #1874446
 
* Thu Aug 20 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.14-1
- Rebase to 10.4.14
 
* Tue Aug 18 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.13-7
- Do CMake out-of-source builds
- Force the CMake change regarding the in-source builds also to F31 and F32
- Use CMake macros instead of cmake & make direct commands
- %%cmake macro covers the %%{set_build_flags}, so they are not needed
  Other changes to compile flags must be specified *after* the %%cmake macro
 
* Wed Aug 05 2020 Jeff Law <law@redhat.com> - 3:10.4.13-6
- Disable LTO
 
* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.4.13-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.4.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Tue Jul 14 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.13-3
- Make conflicts between corresponding mariadb and mysql packages explicit
- Get rid of the Conflicts macro, it was intended to mark conflicts with
  *upstream* packages
 
* Fri Jun 05 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.13-2
- Extend Perl "Requires" filtering to wsrep
  Resolves: #1845376
 
* Fri Jun 05 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.13-1
- Rebase to 10.4.13
 
* Sun May 24 2020 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.4.12-6
- Remove mariadb_rpl.h from includedir to prevent conflict with connector-c's libraries
 
* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 3:10.4.12-5
- Fix string quoting for rpm >= 4.16
 
* Thu Mar 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3:10.4.12-4
- Add perl dependencies needed for tests
 
* Mon Mar 16 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.12-3
- Rebase mariadb-connector-c git submodule to commit fbf1db6
  For fix: https://jira.mariadb.org/browse/CONC-441
 
* Tue Mar 10 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.12-2
- Update the fix for building in the debug mode
 
* Thu Feb 06 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.12-1
- Rebase to 10.4.12
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Fri Jan 17 2020 Michal Schorm <mschorm@redhat.com> - 3:10.4.11-1
- Rebase to 10.4.11
  Related: #1756468
- Remove 'bench' subpackage. Upstream no longer maintains it.
- Use Valgrind for debug builds
- Remove ancient obsoletions
- Tweak build flags
- Add patch for auth_pam_tool directory
 
* Fri Jan 10 2020 Michal Schorm <mschorm@redhat.com> - 3:10.3.21-1
- Rebase to 10.3.21
 
* Mon Nov 18 2019 Lukas Javorsky <ljavorsk@redhat.com> - 3:10.3.20-3
- Change path of groonga's packaged files
- Fix bz#1763287
 
* Tue Nov 12 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.20-2
- Rebuild on top fo new mariadb-connector-c
 
* Mon Nov 11 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.20-1
- Rebase to 10.3.20
 
* Wed Nov 06 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.19-1
- Rebase to 10.3.19
 
* Thu Oct 31 2019 Carl George <carl@george.computer> - 3:10.3.18-1
- Rebase to 10.3.18
 
* Wed Sep 11 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.17-3
- Disable building of the ed25519 client plugin.
  From now on it will be shipped by 'mariadb-connector-c' package
 
* Fri Sep 06 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.17-2
- Fix the debug build
 
* Thu Aug 01 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.17-1
- Rebase to 10.3.17
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Tue Jun 18 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.16-1
- Rebase to 10.3.16
- Added patch for armv7hl builds of spider SE
 
* Tue Jun 11 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.15-1
- Rebase to 10.3.15
- CVEs fixed:
  CVE-2019-2510 CVE-2019-2537
- CVEs fixed:
  CVE-2019-2614 CVE-2019-2627 CVE-2019-2628
 
* Tue Jun 11 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-15
- Remove Cassandra subpackage; it is no longer developed
 
* Thu Mar 21 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-14
- Fix building of TokuDB with Jemalloc 5
- Fix building with / without lz4
 
* Thu Mar 21 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-13
- Add patch for mysqld_safe --dry-run
 
* Wed Mar 20 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-12
- Add patch for server pkgconfig file location
 
* Sat Feb 23 2019 Pavel Raiskup <praiskup@redhat.com> - 3:10.3.12-11
- conditionally depend on selinux-policy-targeted again (rhbz#1665643)
 
* Mon Feb 11 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-10
- Disable the requirement of mysql-selinux, until its bug is solved for good; #1665643
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.3.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Wed Jan 30 2019 Honza Horak <hhorak@redhat.com> - 3:10.3.12-8
- Fix several SSL tests that failed because of different SSL cipher expectation
 
* Wed Jan 23 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-7
- Fix TokuDB Jemalloc ld_preload
  Resolves: #1668375
- Tweak macros usage
 
* Sat Jan 19 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-6
- Enable mysql-selinux requirement
- Tweak the testsuite execution, speed up the testsuite on rebuilds
- Change weak dependency of RocksDB and TokuDB storage engines
  from Recommends to Suggests
- Add "Suggests" weak dependencies to more storage engines
 
* Wed Jan 16 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-5
- Tweak handling of the mysql-selinux requirement, leave disabled due to #1665643
 
* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3:10.3.12-4
- Rebuilt for libcrypt.so.2 (#1666033)
 
* Fri Jan 11 2019 Kevin Fenzi <kevin@scrye.com> - 3:10.3.12-3
- Drop mysql-selinux recommends for now due to bug #1665643
 
* Wed Jan 09 2019 Honza Horak <hhorak@redhat.com> - 3:10.3.12-2
- Use specific python shebang
 
* Tue Jan 08 2019 Michal Schorm <mschorm@redhat.com> - 3:10.3.12-1
- Rebase to 10.3.12
- Disable building of the caching_sha2_password plugin, it is shipped
  by 'mariadb-connector-c'
- Remove libmariadb.pc, is it shipped by 'mariadb-connector-c'
 
* Mon Dec 10 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.11-1
- Rebase to 10.3.11
- CVEs fixed:
  CVE-2018-3282, CVE-2016-9843, CVE-2018-3174, CVE-2018-3143, CVE-2018-3156
  CVE-2018-3251, CVE-2018-3185, CVE-2018-3277, CVE-2018-3162, CVE-2018-3173
  CVE-2018-3200, CVE-2018-3284
 
* Fri Oct 05 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.10-1
- Rebase to 10.3.10
 
* Tue Sep 04 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.9-2
- Fix parallel installability of x86_64 and i686 devel packages
 
* Mon Aug 20 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.9-1
- Rebase to 10.3.9
 
* Fri Aug 10 2018 Petr Lautrbach <plautrba@redhat.com> - 3:10.3.8-5
- Update mariadb-server-galera sub-package to require the correct package with /usr/sbin/semanage
 
* Wed Jul 25 2018 Honza Horak <hhorak@redhat.com> - 3:10.3.8-4
- Do not build config on systems where mariadb-connector-c-config exists instead
 
* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 3:10.3.8-3
- Move config files mysql-clients.cnf and enable_encryption.preset to correct
  sub-packages, similar to what upstream does
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Tue Jul 03 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.8-1
- Rebase to 10.3.8
- Build TokuDB with jemalloc
 
* Wed Jun 27 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.7-2
- Rebase to 10.3.7
- Remove the galera obsoletes
 
* Tue Jun 05 2018 Honza Horak <hhorak@redhat.com> - 3:10.2.15-2
- Use mysqladmin for checking the socket
- Jemalloc dependency moved to the TokuDB subpackage.
  CMake jemalloc option removed, not used anymore.
  The server doesn't need jemalloc since 10.2: https://jira.mariadb.org/browse/MDEV-11059
- Build MariaDB with TokuDB without Jemalloc.
 
* Wed May 23 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.15-1
- Rebase to 10.2.15
- CVEs fixed: #1568962
  CVE-2018-2755 CVE-2018-2761 CVE-2018-2766 CVE-2018-2771 CVE-2018-2781
  CVE-2018-2782 CVE-2018-2784 CVE-2018-2787 CVE-2018-2813 CVE-2018-2817
  CVE-2018-2819 CVE-2018-2786 CVE-2018-2759 CVE-2018-2777 CVE-2018-2810
 
* Thu Mar 29 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.14-1
- Rebase to 10.2.14
- Update testsuite run for SSL self signed certificates
 
* Tue Mar 6 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.13-2
- Further fix of ldconfig scriptlets for F27
- Fix hardcoded paths, move unversioned libraries and symlinks to the devel subpackage
 
* Thu Mar 1 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.13-1
- Rebase to 10.2.13
 
* Mon Feb 26 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-8
- SPECfile refresh, RHEL6, SySV init and old fedora stuff removed
 
* Sun Feb 25 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-7
- Rebuilt for ldconfig_post and ldconfig_postun bug
  Related: #1548331
 
* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Fri Jan 26 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-5
- Use '-ldl' compiler flag when associated library used
  Resolves: #1538990
 
* Thu Jan 25 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-4
- Fix the upgrade path. Build TokuDB subpackage again, but build a unsupported
  configuration by upstream (without Jemalloc).
  Jemmalloc has been updated to version 5, which isn't backwards compatible.
- Use downstream tmpfiles instead of the upstream one
  Related: #1538066
 
* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3:10.2.12-3
- Rebuilt for switch to libxcrypt
 
* Thu Jan 11 2018 Honza Horak <hhorak@redhat.com> - 3:10.2.12-1
- Do not build connect plugin with mongo and jdbc connectors
- Support MYSQLD_OPTS and _WSREP_NEW_CLUSTER env vars in init script,
  same as it is done in case of systemd unit file
  Related: #1455850
- Print the same messages as before when starting the service in SysV init,
  to not scare users
  Related: #1463411
 
* Wed Jan 10 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-1
- Rebase to 10.2.12
- Temporary fix for https://jira.mariadb.org/browse/MDEV-14537 removed
- TokuDB disabled
 
* Mon Dec 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.11-2
- Temporary fix for #1523875 removed, bug in Annobin fixed
  Resolves: #1523875
 
* Sat Dec 09 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.11-1
- Rebase to 10.2.11
- Temporary fix for https://jira.mariadb.org/browse/MDEV-14537 introduced
- Temporary fix for #1523875 intoruced
  Related: #1523875
 
* Wed Dec 06 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.10-2
- Fix PID file location
  Related: #1483331, #1515779
- Remove 'Group' tags as they should not be used any more
  Related: https://fedoraproject.org/wiki/RPMGroups
 
* Mon Nov 20 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.10-1
- Rebase to 10.2.10 version
- Patch 2: mariadb-install-test.patch has been incorporated by upstream
- Patch 8: mariadb-install-db-sharedir.patch; upstream started to use macros
- Update PCRE check
- Start using location libdir/mariadb for plugins
- Move libraries to libdir
- Divided to more sub-packages to match upstream's RPM list
  Resolves: #1490401; #1400463
- Update of Cmake arguments to supported format
  Related: https://lists.launchpad.net/maria-discuss/msg04852.html
- Remove false Provides
 
* Thu Oct 05 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-3
- Fix client library obsolete
  Related: #1498956
- Enable testsuite again
- RPMLint error fix:
  Remove unused python scripts which remained from TokuDB upstream
- RPMLint error fix: description line too long
 
* Wed Oct 04 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-2
- Fix of "with" and "without" macros, so they works
- Use 'iproute' dependency instead of 'net-tools'
  Related: #1496131
- Set server package to own /usr/lib64/mysql directory
- Use correct obsolete, so upgrade from maridb 10.1 to 10.2 is possible
  with dnf "--allowerasing" option
  Related: #1497234
- Fix building with client library
 
* Thu Sep 28 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-1
- Rebase to 10.2.9
- Testsuite temorarly disabled in order to fast deploy critical fix
  Related: #1497234
 
* Wed Sep 20 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.8-5
- Fix building without client library part
- Start building mariadb without client library part,
  use mariadb-connector-c package >= 3.0 instead
- Use obosletes of "-libs" in "-common", if built without client library part
 
* Mon Aug 28 2017 Honza Horak <hhorak@redhat.com> - 3:10.2.8-2
- Fix paths in galera_recovery and galera_new_cluster
  Resolves: #1403416
- Support --defaults-group-suffix properly in systemd unit file
  Resolves: #1485777
- Allow 4567 port for tcp as well
- Install mysql-wait-ready on RHEL-6 for the SysV init
- Run mysql-prepare-db-dir as non-root
- Sync mysql.init with community-mysql
 
* Sun Aug 20 2017 Honza Horak <hhorak@redhat.com> - 3:10.2.8-1
- Rebase to 10.2.8
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Tue Jul 25 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.7-6
- Revert previous change, go back to libmariadb headers (RHBZ #1474764)
 
* Fri Jul 21 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.7-5
- Install correct headers (server, not client) - MDEV-13370
 
* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 3:10.2.7-4
- Rebuilt for s390x binutils bug
 
* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 3:10.2.7-3
- Rebuilt for Boost 1.64
 
* Thu Jul 13 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.7-2
- Remove mysql-wait-* scripts. They aren't needed when using systemd "Type=notify"
 
* Thu Jul 13 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.7-1
- Rebase to 10.2.7
- Get back mysql_config, its "--libmysqld-libs" is still needed
 
* Wed Jul 12 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.6-4
- Add manual Provides: for the libmysqlcient compat symlink
 
* Wed Jul 12 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.6-3
- Move libmysqlclient.so.18 compat link to -libs subpackage
 
* Tue Jul 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.6-2
- Disable Dtrace
- Disable Sphinx, circural dependency
 
* Tue Jul 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.6-1
- Rebase to 10.2.6
- SSL patch removed
- 'libmariadb.so.3' replaced 'limysqlclient.so.18.0.0', symlinks provided
- "make test" removed, it needs running server and same test are included in the testsuite
 
* Mon Jul 10 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.25-1
- Rebase to 10.1.25
- Disable plugins 'cracklib' and 'gssapi' by default
- Related: #1468028, #1464070
- Looks like the testsuite removes its 'var' content correctly,
  no need to do that explicitly.
 
* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3:10.1.24-5
- Rebuild due to bug in RPM (RHBZ #1468476)
 
* Mon Jun 19 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-4
- Use "/run" location instead of "/var/run" symlink
- Related: #1455811
- Remove AppArmor files
 
* Fri Jun 09 2017 Honza Horak <hhorak@redhat.com> - 3:10.1.24-3
- Downstream script mariadb-prepare-db-dir fixed for CVE-2017-3265
- Resolves: #1458940
- Check properly that datadir includes only expected files
- Related: #1356897
 
* Wed Jun 07 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-2
- Fixed incorrect Jemalloc initialization; #1459671
 
* Fri Jun 02 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-1
- Rebase to 10.1.24
- Build dependecies Bison and Libarchive added, others corrected
- Disabling Mroonga engine for i686 architecture, as it is not supported by MariaDB
- Removed patches: (fixed by upstream)
    Patch5:  mariadb-file-contents.patch
    Patch14: mariadb-example-config-files.patch
    Patch31: mariadb-string-overflow.patch
    Patch32: mariadb-basedir.patch
    Patch41: mariadb-galera-new-cluster-help.patch
- Resolves: rhbz#1414387
    CVE-2017-3313
- Resolves partly: rhbz#1443408
    CVE-2017-3308 CVE-2017-3309 CVE-2017-3453 CVE-2017-3456 CVE-2017-3464
 
* Tue May 23 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-6
- Plugin oqgraph enabled
- Plugin jemalloc enabled
- 'force' option for 'rm' removed
- Enabled '--big-test' option for the testsuite
- Disabled '--skip-rpl' option for the testsuite = replication tests enabled
- Multilib manpage added
 
* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:10.1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild
 
* Tue Mar 07 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-4
- Cracklib plugin enabled
- Removed strmov patch, it is no longer needed. The issue was fixed long ago in both MariaDB and MySQL
 
* Wed Feb 15 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-3
- Fix for some RPMLint issues
- Fix: Only server utilities can be move to server-utils subpackage. The rest (from client)
  were moved back to where they came from (client - the main subpackage)
- Added correct "Obsoletes" for the server-utils subpackage
- Fixed FTBFS in F26 on x86_64, because of -Werror option
- Related: #1421092, #1395127
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Tue Jan 24 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-1
- Rebase to version 10.1.21
- Most of the non-essential utilites has been moved to the new sub-package mariadb-server-utils
- Patches "admincrash" and "errno" removed, they are no longer relevant
  "mysql-embedded-check.c" removed, no longer relevant
- Buildrequires krb5-devel duplicity removed
- Manpage for mysql_secure_installation extended
- Preparation for the CrackLib plugin to be added (waiting for correct SELinux rules to be relased)
- Related: #1260821, #1205082, #1414387
 
* Tue Jan 03 2017 Honza Horak <hhorak@redhat.com> - 3:10.1.20-3
- Add explicit EVR requirement in main package for -libs
- Related: #1406320
 
* Tue Dec 20 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.20-2
- Use correct macro when removing doc files
- Resolves: #1400981
 
* Sat Dec 17 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.20-1
- Rebase to version 10.1.20
- Related: #1405258
 
* Fri Dec 02 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-6
- Move patch from specfile to standalone patch file
- Related: #1382988
 
* Thu Dec 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 3:10.1.19-6
- -devel: use pkgconfig(openssl) to allow any implementation (like compat-openssl10)
 
* Wed Nov 30 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-5
- Testsuite blacklists heavily updated. Current tracker: #1399847
- Log-error option added to all config files examples
- Resolves: #1382988
 
* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-4
- JdbcMariaDB.jar test removed
- PCRE version check added
- Related: #1382988, #1396945, #1096787
 
* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-4
- test suite ENABLED, consensus was made it still should be run every build
 
* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-2
- fixed bug 1382988
- added comment to the test suite
- test suite DISABLED for most builds in Koji, see comments
 
* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-1
- Update to 10.1.19
- added temporary support to build with OpenSSL 1.0 on Fedora >= 26
- added krb5-devel pkg as Buldrquires to prevent gssapi failure
 
* Tue Oct  4 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.18-1
- Update to 10.1.18
 
* Wed Aug 31 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.17-1
- Update to 10.1.17
 
* Mon Aug 29 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.16-2
- Fixed galera replication
- Resolves: #1352946
 
* Tue Jul 19 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.16-1
- Update to 10.1.16
 
* Fri Jul 15 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.14-5
- Fail build when test-suite fails
- Use license macro for inclusion of licenses
 
* Thu Jul 14 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.14-4
- Revert Update to 10.1.15, this release is broken
  https://lists.launchpad.net/maria-discuss/msg03691.html
 
* Thu Jul 14 2016 Honza Horak <hhorak@redhat.com> - 2:10.1.15-3
- Check datadir more carefully to avoid unwanted data corruption
- Related: #1335849
 
* Thu Jul  7 2016 Jakub Dorňák <jdornak@redhat.com> - 2:10.1.15-2
- Bump epoch
  (related to the downgrade from the pre-release version)
 
* Fri Jul  1 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.15-1
- Update to 10.1.15
 
* Fri Jul  1 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.14-3
- Revert "Update to 10.2.0"
  It is possible that MariaDB 10.2.0 won't be stable till f25 GA.
 
* Tue Jun 21 2016 Pavel Raiskup <praiskup@redhat.com> - 1:10.1.14-3
- BR multilib-rpm-config and use it for multilib workarounds
- install architecture dependant pc file to arch-dependant location
 
* Thu May 26 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.2.0-2
- Fix mysql-prepare-db-dir
- Resolves: #1335849
 
* Thu May 12 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.2.0-1
- Update to 10.2.0
 
* Thu May 12 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.14-1
- Add selinux policy
- Update to 10.1.14 (includes various bug fixes)
- Add -h and --help options to galera_new_cluster
 
* Thu Apr  7 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-3
- wsrep_on in galera.cnf
 
* Tue Apr  5 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-2
- Moved /etc/sysconfig/clustercheck
  and /usr/share/mariadb/systemd/use_galera_new_cluster.conf
  to mariadb-server-galera
 
* Tue Mar 29 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-1
- Update to 10.1.13
 
* Wed Mar 23 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-4
- Fixed conflict with mariadb-galera-server
 
* Tue Mar 22 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-3
- Add subpackage mariadb-server-galera
- Resolves: 1310622
 
* Tue Mar 01 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.12-2
- Rebuild for BZ#1309199 (symbol versioning)
 
* Mon Feb 29 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-1
- Update to 10.1.12
 
* Tue Feb 16 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-9
- Remove dangling symlink to /etc/init.d/mysql
 
* Sat Feb 13 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-8
- Use epoch for obsoleting mariadb-galera-server
 
* Fri Feb 12 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-7
- Add Provides: bundled(pcre) in case we build with bundled pcre
- Related: #1302296
- embedded-devel should require libaio-devel
- Resolves: #1290517
 
* Fri Feb 12 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-6
- Fix typo s/obsolate/obsolete/
 
* Thu Feb 11 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-5
- Add missing requirements for proper wsrep functionality
- Obsolate mariadb-galera & mariadb-galera-server (thanks Tomas Repik)
- Resolves: #1279753
- Re-enable using libedit, which should be now fixed
- Related: #1201988
- Remove mariadb-wait-ready call from systemd unit, we have now systemd notify support
- Make mariadb@.service similar to mariadb.service
 
* Mon Feb 08 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-4
- Use systemd unit file more compatible with upstream
 
* Sun Feb 07 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-3
- Temporarily disabling oqgraph for
  https://mariadb.atlassian.net/browse/MDEV-9479
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:10.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Wed Feb  3 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.11-1
- Update to 10.1.11
 
* Tue Jan 19 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.10-1
- Update to 10.1.10
 
* Mon Dec 07 2015 Dan Horák <dan[at]danny.cz> - 1:10.1.8-3
- rebuilt for s390(x)
 
* Tue Nov 03 2015 Honza Horak <hhorak@redhat.com> - 1:10.1.8-2
- Expand variables in server.cnf
 
* Thu Oct 22 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.8-1
- Update to 10.1.8
 
* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1:10.0.21-2
- Rebuilt for Boost 1.59
 
* Mon Aug 10 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.21-1
- Update to 10.0.21
 
* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159
 
* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1:10.0.20-2
- rebuild for Boost 1.58
 
* Tue Jun 23 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.20-1
- Update to 10.0.20
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Wed Jun 03 2015 Dan Horák <dan[at]danny.cz> - 1:10.0.19-2
- Update lists of failing tests (jdornak)
- Related: #1149647
 
* Mon May 11 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.19-1
- Update to 10.0.19
 
* Thu May 07 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.18-1
- Update to 10.0.18
 
* Thu May 07 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-4
- Include client plugins into -common package since they are used by both -libs
  and base packages.
- Do not use libedit
- Related: #1201988
- Let plugin dir to be owned by -common
- Use correct comment in the init script
- Related: #1184604
- Add openssl as BuildRequires to run some openssl tests during build
- Related: #1189180
- Fail in case any command in check fails
- Related: #1124791
- Fix mysqladmin crash if run with -u root -p
- Resolves: #1207170
 
* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:10.0.17-3
- Rebuilt for GCC 5 C++11 ABI change
 
* Fri Mar 06 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-2
- Wait for daemon ends
- Resolves: #1072958
- Do not include symlink to libmysqlclient if not shipping the library
- Do not use scl prefix more than once in paths
  Based on https://www.redhat.com/archives/sclorg/2015-February/msg00038.html
 
* Wed Mar 04 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-1
- Rebase to version 10.0.17
- Added variable for turn off skipping some tests
 
* Tue Mar 03 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.16-6
- Check permissions when starting service on RHEL-6
- Resolves: #1194699
- Do not create test database by default
- Related: #1194611
 
* Fri Feb 13 2015 Matej Muzila <mmuzila@redhat.com> - 1:10.0.16-4
- Enable tokudb
 
* Tue Feb 10 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.16-3
- Fix openssl_1 test
 
* Wed Feb  4 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.16-2
- Include new certificate for tests
- Update lists of failing tests
- Related: #1186110
 
* Tue Feb  3 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.16-9
- Rebase to version 10.0.16
- Resolves: #1187895
 
* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1:10.0.15-9
- Rebuild for boost 1.57.0
 
* Mon Jan 26 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-8
- Fix typo in the config file
 
* Sun Jan 25 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-7
- Do not create log file in post script
 
* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-6
- Move server settings to config file under my.cnf.d dir
 
* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-5
- Fix path for sysconfig file
  Filter provides in el6 properly
  Fix initscript file location
 
* Tue Jan 06 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-4
- Disable failing tests connect.mrr, connect.updelx2 on ppc and s390
 
* Mon Dec 22 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.15-3
- Fix macros paths in my.cnf
- Create old location for pid file if it remained in my.cnf
 
* Fri Dec 05 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.15-2
- Rework usage of macros and remove some compatibility artefacts
 
* Thu Nov 27 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.15-1
- Update to 10.0.15
 
* Thu Nov 20 2014 Jan Stanek <jstanek@redhat.com> - 1:10.0.14-8
- Applied upstream fix for mysql_config --cflags output.
- Resolves: #1160845
 
* Fri Oct 24 2014 Jan Stanek <jstanek@redhat.com> - 1:10.0.14-7
- Fixed compat service file.
- Resolves: #1155700
 
* Mon Oct 13 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-6
- Remove bundled cmd-line-utils
- Related: #1079637
- Move mysqlimport man page to proper package
- Disable main.key_cache test on s390
  Releated: #1149647
 
* Wed Oct 08 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-5
- Disable tests connect.part_file, connect.part_table
  and connect.updelx
- Related: #1149647
 
* Wed Oct 01 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-4
- Add bcond_without mysql_names
  Use more correct path when deleting mysql logrotate script
 
* Wed Oct 01 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-3
- Build with system libedit
- Resolves: #1079637
 
* Mon Sep 29 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-2
- Add with_debug option
 
* Mon Sep 29 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-1
- Update to 10.0.14
 
* Wed Sep 24 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-8
- Move connect engine to a separate package
  Rename oqgraph engine to align with upstream packages
- Move some files to correspond with MariaDB upstream packages
  client.cnf into -libs, mysql_plugin and msql2mysql into base,
  tokuftdump and aria_* into -server, errmsg-utf8.txt into -errmsg
- Remove duplicate cnf files packaged using %%doc
- Check upgrade script added to warn about need for mysql_upgrade
 
* Wed Sep 24 2014 Matej Muzila <mmuzila@redhat.com> - 1:10.0.13-7
- Client related libraries moved from mariadb-server to mariadb-libs
- Related: #1138843
 
* Mon Sep 08 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-6
- Disable vcol_supported_sql_funcs_myisam test on all arches
- Related: #1096787
- Install systemd service file on RHEL-7+
  Server requires any mysql package, so it should be fine with older client
 
* Thu Sep 04 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-5
- Fix paths in mysql_install_db script
- Resolves: #1134328
- Use %%cmake macro
 
* Tue Aug 19 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-4
- Build config subpackage everytime
- Disable failing tests: innodb_simulate_comp_failures_small, key_cache
  rhbz#1096787
 
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Thu Aug 14 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-2
- Include mysqld_unit only if required; enable tokudb in f20-
 
* Wed Aug 13 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-1
- Rebase to version 10.0.13
 
* Tue Aug 12 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-8
- Introduce -config subpackage and ship base config files here
 
* Tue Aug  5 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-7
- Adopt changes from mysql, thanks Bjorn Munch <bjorn.munch@oracle.com>
 
* Mon Jul 28 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-6
- Use explicit sysconfdir
- Absolut path for default value for pid file and error log
 
* Tue Jul 22 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-5
- Hardcoded paths removed to work fine in chroot
- Spec rewrite to be more similar to oterh MySQL implementations
- Use variable for daemon unit name
- Include SysV init script if built on older system
- Add possibility to not ship some sub-packages
 
* Mon Jul 21 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-4
- Reformating spec and removing unnecessary snippets
 
* Tue Jul 15 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-3
- Enable OQGRAPH engine and package it as a sub-package
- Add support for TokuDB engine for x86_64 (currently still disabled)
- Re-enable tokudb_innodb_xa_crash again, seems to be fixed now
- Drop superfluous -libs and -embedded ldconfig deps (thanks Ville Skyttä)
- Separate -lib and -common sub-packages
- Require /etc/my.cnf instead of shipping it
- Include README.mysql-cnf
- Multilib support re-worked
- Introduce new option with_mysqld_unit
- Removed obsolete mysql-cluster, the package should already be removed
- Improve error message when log file is not writable
- Compile all binaries with full RELRO (RHBZ#1092548)
- Use modern symbol filtering with compatible backup
- Add more groupnames for server's my.cnf
- Error messages now provided by a separate package (thanks Alexander Barkov)
- Expand paths in helper scripts using cmake
 
* Wed Jun 18 2014 Mikko Tiihonen <mikko.tiihonen@iki.fi> - 1:10.0.12-2
- Use -fno-delete-null-pointer-checks to avoid segfaults with gcc 4.9
 
* Tue Jun 17 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.12-1
- Rebase to version 10.0.12
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Tue Jun  3 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.11-4
- rebuild with tests failing on different arches disabled (#1096787)
 
* Thu May 29 2014 Dan Horák <dan[at]danny.cz> - 1:10.0.11-2
- rebuild with tests failing on big endian arches disabled (#1096787)
 
* Wed May 14 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.11-1
- Rebase to version 10.0.11
 
* Mon May 05 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.10-3
- Script for socket check enhanced
 
* Thu Apr 10 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.10-2
- use system pcre library
 
* Thu Apr 10 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.10-1
- Rebase to version 10.0.10
 
* Wed Mar 12 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.36-2
- Server crashes on SQL select containing more group by and left join statements using innodb tables
- Resolves: #1065676
- Fix paths in helper scripts
- Move language files into mariadb directory
 
* Thu Mar 06 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.36-1
- Rebase to 5.5.36
  https://kb.askmonty.org/en/mariadb-5536-changelog/
 
* Tue Feb 25 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-5
- Daemon helper scripts sanity changes and spec files clean-up
 
* Tue Feb 11 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-4
- Fix typo in mysqld.service
- Resolves: #1063981
 
* Wed Feb  5 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-3
- Do not touch the log file in post script, so it does not get wrong owner
- Resolves: #1061045
 
* Thu Jan 30 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-1
- Rebase to 5.5.35
  https://kb.askmonty.org/en/mariadb-5535-changelog/
  Also fixes: CVE-2014-0001, CVE-2014-0412, CVE-2014-0437, CVE-2013-5908,
  CVE-2014-0420, CVE-2014-0393, CVE-2013-5891, CVE-2014-0386, CVE-2014-0401,
  CVE-2014-0402
- Resolves: #1054043
- Resolves: #1059546
 
* Tue Jan 14 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.34-9
- Adopt compatible system versioning
- Related: #1045013
- Use compatibility mysqld.service instead of link
- Related: #1014311
 
* Mon Jan 13 2014 Rex Dieter <rdieter@fedoraproject.org> 1:5.5.34-8
- move mysql_config alternatives scriptlets to -devel too
 
* Fri Jan 10 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-7
- Build with -O3 on ppc64
- Related: #1051069
- Move mysql_config to -devel sub-package and remove Require: mariadb
- Related: #1050920
 
* Fri Jan 10 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 1:5.5.34-6
- Disable main.gis-precise test also for AArch64
- Disable perfschema.func_file_io and perfschema.func_mutex for AArch64
  (like it is done for 32-bit ARM)
 
* Fri Jan 10 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-5
- Clean all non-needed doc files properly
 
* Wed Jan  8 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-4
- Read socketfile location in mariadb-prepare-db-dir script
 
* Mon Jan  6 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-3
- Don't test EDH-RSA-DES-CBC-SHA cipher, it seems to be removed from openssl
  which now makes mariadb/mysql FTBFS because openssl_1 test fails
- Related: #1044565
- Use upstream's layout for symbols version in client library
- Related: #1045013
- Check if socket file is not being used by another process at a time
  of starting the service
- Related: #1045435
- Use %%ghost directive for the log file
- Related: 1043501
 
* Wed Nov 27 2013 Honza Horak <hhorak@redhat.com> 1:5.5.34-2
- Fix mariadb-wait-ready script
 
* Fri Nov 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.34-1
- Rebase to 5.5.34
 
* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-4
- Fix spec file to be ready for backport by Oden Eriksson
- Resolves: #1026404
 
* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-3
- Add pam-devel to build-requires in order to build
- Related: #1019945
- Check if correct process is running in mysql-wait-ready script
- Related: #1026313
 
* Mon Oct 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-2
- Turn on test suite
 
* Thu Oct 10 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-1
- Rebase to 5.5.33a
  https://kb.askmonty.org/en/mariadb-5533-changelog/
  https://kb.askmonty.org/en/mariadb-5533a-changelog/
- Enable outfile_loaddata test
- Disable tokudb_innodb_xa_crash test
 
* Mon Sep  2 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-12
- Re-organize my.cnf to include only generic settings
- Resolves: #1003115
- Move pid file location to /var/run/mariadb
- Make mysqld a symlink to mariadb unit file rather than the opposite way
- Related: #999589
 
* Thu Aug 29 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-11
- Move log file into /var/log/mariadb/mariadb.log
- Rename logrotate script to mariadb
- Resolves: #999589
 
* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1:5.5.32-10
- fix alternatives usage
 
* Tue Aug 13 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-9
- Multilib issues solved by alternatives
- Resolves: #986959
 
* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.32-8
- Perl 5.18 rebuild
 
* Wed Jul 31 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-7
- Do not use login shell for mysql user
 
* Tue Jul 30 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-6
- Remove unneeded systemd-sysv requires
- Provide mysql-compat-server symbol
- Create mariadb.service symlink
- Fix multilib header location for arm
- Enhance documentation in the unit file
- Use scriptstub instead of links to avoid multilib conflicts
- Add condition for doc placement in F20+
 
* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 1:5.5.32-5
- remove "Requires(pretrans): systemd" since its not possible
- when installing mariadb and systemd at the same time. as in a new install
 
* Sat Jul 27 2013 Kevin Fenzi <kevin@scrye.com> 1:5.5.32-4
- Set rpm doc macro to install docs in unversioned dir
 
* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-3
- add Requires(pre) on systemd for the server package
 
* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-2
- replace systemd-units requires with systemd
- remove solaris files
 
* Fri Jul 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.32-1
- Rebase to 5.5.32
  https://kb.askmonty.org/en/mariadb-5532-changelog/
- Clean-up un-necessary systemd snippets
 
* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.31-7
- Perl 5.18 rebuild
 
* Mon Jul  1 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-6
- Test suite params enhanced to decrease server condition influence
- Fix misleading error message when uninstalling built-in plugins
- Related: #966873
 
* Thu Jun 27 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-5
- Apply fixes found by Coverity static analysis tool
 
* Wed Jun 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-4
- Do not use pretrans scriptlet, which doesn't work in anaconda
- Resolves: #975348
 
* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-3
- Explicitly enable mysqld if it was enabled in the beginning
  of the transaction.
 
* Thu Jun 13 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-2
- Apply man page fix from Jan Stanek
 
* Fri May 24 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-1
- Rebase to 5.5.31
  https://kb.askmonty.org/en/mariadb-5531-changelog/
- Preserve time-stamps in case of installed files
- Use /var/tmp instead of /tmp, since the later is using tmpfs,
  which can cause problems
- Resolves: #962087
- Fix test suite requirements
 
* Sun May  5 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-2
- Remove mytop utility, which is packaged separately
- Resolve multilib conflicts in mysql/private/config.h
 
* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-1
- Rebase to 5.5.30
  https://kb.askmonty.org/en/mariadb-5530-changelog/
 
* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-11
- Obsolete MySQL since it is now renamed to community-mysql
- Remove real- virtual names
 
* Thu Mar 21 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-10
- Adding epoch to have higher priority than other mysql implementations
  when comes to provider comparison
 
* Wed Mar 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-9
- Let mariadb-embedded-devel conflict with MySQL-embedded-devel
- Adjust mariadb-sortbuffer.patch to correspond with upstream patch
 
* Mon Mar  4 2013 Honza Horak <hhorak@redhat.com> 5.5.29-8
- Mask expected warnings about setrlimit in test suite
 
* Thu Feb 28 2013 Honza Horak <hhorak@redhat.com> 5.5.29-7
- Use configured prefix value instead of guessing basedir
  in mysql_config
- Resolves: #916189
- Export dynamic columns and non-blocking API functions documented
  by upstream
 
* Wed Feb 27 2013 Honza Horak <hhorak@redhat.com> 5.5.29-6
- Fix sort_buffer_length option type
 
* Wed Feb 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-5
- Suppress warnings in tests and skip tests also on ppc64p7
 
* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-4
- Suppress warning in tests on ppc
- Enable fixed index_merge_myisam test case
 
* Thu Feb 07 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Packages need to provide also %%_isa version of mysql package
- Provide own symbols with real- prefix to distinguish from mysql
  unambiguously
- Fix format for buffer size in error messages (MDEV-4156)
- Disable some tests that fail on ppc and s390
- Conflict only with real-mysql, otherwise mariadb conflicts with ourself
 
* Tue Feb 05 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Let mariadb-libs to own /etc/my.cnf.d
 
* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.29-1
- Rebase to 5.5.29
  https://kb.askmonty.org/en/mariadb-5529-changelog/
- Fix inaccurate default for socket location in mysqld-wait-ready
- Resolves: #890535
 
* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-8
- Enable obsoleting mysql
 
* Wed Jan 30 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-7
- Adding necessary hacks for perl dependency checking, rpm is still
  not wise enough
- Namespace sanity re-added for symbol default_charset_info
 
* Mon Jan 28 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-6
- Removed %%{_isa} from provides/obsoletes, which doesn't allow
  proper obsoleting
- Do not obsolete mysql at the time of testing
 
* Thu Jan 10 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-5
- Added licenses LGPLv2 and BSD
- Removed wrong usage of %%{epoch}
- Test-suite is run in %%check
- Removed perl dependency checking adjustment, rpm seems to be smart enough
- Other minor spec file fixes
 
* Tue Dec 18 2012 Honza Horak <hhorak@redhat.com> 5.5.28a-4
- Packaging of MariaDB based on MySQL package
