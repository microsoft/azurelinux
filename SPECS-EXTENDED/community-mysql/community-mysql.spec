Vendor:         Microsoft Corporation
Distribution:   Mariner
#   This is a fix for the https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
#   So the beaviour will be the same also in F31 nad F32
%undefine __cmake_in_source_build

# Name of the package without any prefixes
%global pkg_name %{name}
%global pkgnamepatch community-mysql

# Regression tests may take a long time (many cores recommended), skip them by
# passing --nocheck to rpmbuild or by setting runselftest to 0 if defining
# --nocheck is not possible (e.g. in koji build)
%{!?runselftest:%global runselftest 1}

# Set this to 1 to see which tests fail
%global check_testsuite 0

# In f20+ use unversioned docdirs, otherwise the old versioned one
%global _pkgdocdirname %{pkg_name}%{!?_pkgdocdir:-%{version}}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{pkg_name}-%{version}}

# By default, patch(1) creates backup files when chunks apply with offsets.
# Turn that off to ensure such files don't get included in RPMs (cf bz#884755).
%global _default_patch_flags --no-backup-if-mismatch

%global skiplist platform-specific-tests.list

# For some use cases we do not need some parts of the package
%bcond_without clibrary
%bcond_without devel
%bcond_without client
%bcond_without common
%bcond_without errmsg
%bcond_without test

# When there is already another package that ships /etc/my.cnf,
# rather include it than ship the file again, since conflicts between
# those files may create issues
%bcond_with config

# For deep debugging we need to build binaries with extra debug info
%bcond_with debug

%global boost_bundled_version 1.73.0

# Include files for systemd
%global daemon_name mysqld
%global daemon_no_prefix mysqld

# Directory for storing pid file
%global pidfiledir %{_rundir}/%{daemon_name}

# We define some system's well known locations here so we can use them easily
# later when building to another location (like SCL)
%global logrotateddir %{_sysconfdir}/logrotate.d
%global logfiledir %{_localstatedir}/log/mysql
%global logfile %{logfiledir}/%{daemon_no_prefix}.log

# Defining where database data live
%global dbdatadir %{_localstatedir}/lib/mysql

# Home directory of mysql user should be same for all packages that create it
%global mysqluserhome /var/lib/mysql

# Provide mysql names for compatibility
%bcond_without mysql_names
%bcond_without conflicts

# Make long macros shorter
%global sameevr   %{version}-%{release}

Name:             community-mysql
Version:          8.0.23
Release:          4%{?dist}
Summary:          MySQL client programs and shared libraries
URL:              http://www.mysql.com

# Exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
License:          GPLv2 with exceptions and LGPLv2 and BSD

Source0:          https://cdn.mysql.com/Downloads/MySQL-8.0/mysql-boost-%{version}.tar.gz
Source2:          mysql_config_multilib.sh
Source3:          my.cnf.in
Source6:          README.mysql-docs
Source7:          README.mysql-license
Source10:         mysql.tmpfiles.d.in
Source11:         mysql.service.in
Source12:         mysql-prepare-db-dir.sh
Source14:         mysql-check-socket.sh
Source15:         mysql-scripts-common.sh
Source17:         mysql-wait-stop.sh
Source18:         mysql@.service.in
# To track rpmlint warnings
Source30:         %{pkgnamepatch}.rpmlintrc
# Configuration for server
Source31:         server.cnf.in

# Comments for these patches are in the patch files
# Patches common for more mysql-like packages
Patch1:           %{pkgnamepatch}-install-test.patch
Patch2:           %{pkgnamepatch}-s390-tsc.patch
Patch3:           %{pkgnamepatch}-file-contents.patch
Patch4:           %{pkgnamepatch}-scripts.patch
Patch5:           %{pkgnamepatch}-paths.patch

# Patches specific for this mysql package
Patch51:          %{pkgnamepatch}-chain-certs.patch
Patch52:          %{pkgnamepatch}-sharedir.patch
Patch55:          %{pkgnamepatch}-rpath.patch
Patch75:          %{pkgnamepatch}-arm32-timer.patch
Patch78:          %{pkgnamepatch}-gcc11.patch
Patch79:          %{pkgnamepatch}-main-cast.patch
Patch80:          %{pkgnamepatch}-fix-includes-robin-hood.patch
Patch81:          %{pkgnamepatch}-boolean-fix.patch

# Patches taken from boost 1.59
Patch115: boost-1.58.0-pool.patch
Patch125: boost-1.57.0-mpl-print.patch

BuildRequires:    cmake
BuildRequires:    gcc-c++
BuildRequires:    libaio-devel
BuildRequires:    libedit-devel
BuildRequires:    libevent-devel
BuildRequires:    libicu-devel
BuildRequires:    lz4
BuildRequires:    lz4-devel
BuildRequires:    mecab-devel
BuildRequires:    bison
BuildRequires:    libzstd-devel
BuildRequires:    libcurl-devel
%ifnarch aarch64 %{arm} s390 s390x
BuildRequires:    numactl-devel
%endif
BuildRequires:    openssl
BuildRequires:    openssl-devel
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
BuildRequires:    rpcgen
BuildRequires:    libtirpc-devel
BuildRequires:    protobuf-lite-devel
BuildRequires:    rapidjson-devel
BuildRequires:    zlib
BuildRequires:    zlib-devel
BuildRequires:    multilib-rpm-config
# Tests requires time and ps and some perl modules
BuildRequires:    procps
BuildRequires:    time
BuildRequires:    perl(base)
BuildRequires:    perl(Carp)
BuildRequires:    perl(Cwd)
BuildRequires:    perl(Digest::file)
BuildRequires:    perl(Digest::MD5)
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
BuildRequires:    perl(FindBin)
BuildRequires:    perl(Data::Dumper)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(if)
BuildRequires:    perl(IO::File)
BuildRequires:    perl(IO::Handle)
BuildRequires:    perl(IO::Select)
BuildRequires:    perl(IO::Socket::INET)
BuildRequires:    perl(IPC::Open3)
BuildRequires:    perl(JSON)
BuildRequires:    perl(lib)
BuildRequires:    perl(LWP::Simple)
BuildRequires:    perl(Memoize)
BuildRequires:    perl(Net::Ping)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(Socket)
BuildRequires:    perl(strict)
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(Time::HiRes)
BuildRequires:    perl(Time::localtime)
BuildRequires:    perl(warnings)
BuildRequires:    systemd
BuildRequires:    systemd-devel
BuildRequires:    make

Requires:         bash coreutils grep
Requires:         %{name}-common%{?_isa} = %{sameevr}

Provides:         bundled(boost) = %{boost_bundled_version}

%if %{with mysql_names}
Provides:         mysql = %{sameevr}
Provides:         mysql%{?_isa} = %{sameevr}
Provides:         mysql-compat-client = %{sameevr}
Provides:         mysql-compat-client%{?_isa} = %{sameevr}
%endif

%{?with_conflicts:Conflicts:        mariadb}

# Filtering: https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::)
%global __provides_exclude_from ^(%{_datadir}/(mysql|mysql-test)/.*|%{_libdir}/mysql/plugin/.*\\.so)$

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.


%if %{with clibrary}
%package          libs
Summary:          The shared libraries required for MySQL clients
Requires:         %{name}-common%{?_isa} = %{sameevr}
%if %{with mysql_names}
Provides:         mysql-libs = %{sameevr}
Provides:         mysql-libs%{?_isa} = %{sameevr}
%endif

%description      libs
The mysql-libs package provides the essential shared libraries for any
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.
%endif


%if %{with config}
%package          config
Summary:          The config files required by server and client

%description      config
The package provides the config file my.cnf and my.cnf.d directory used by any
MariaDB or MySQL program. You will need to install this package to use any
other MariaDB or MySQL package if the config files are not provided in the
package itself.
%endif


%if %{with common}
%package          common
Summary:          The shared files required for MySQL server and client
Requires:         %{_sysconfdir}/my.cnf

%description      common
The mysql-common package provides the essential shared files for any
MySQL program. You will need to install this package to use any other
MySQL package.
%endif


%if %{with errmsg}
%package          errmsg
Summary:          The error messages files required by MySQL server
Requires:         %{name}-common%{?_isa} = %{sameevr}

%description      errmsg
The package provides error messages files for the MySQL daemon
%endif


%package          server
Summary:          The MySQL server and related files

# Require any mysql client, but prefer community-mysql client for community-mysql server
Suggests:         %{name}%{?_isa} = %{sameevr}
Requires:         mysql%{?_isa}

Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{_sysconfdir}/my.cnf
Requires:         %{_sysconfdir}/my.cnf.d
Requires:         %{name}-errmsg%{?_isa} = %{sameevr}
%{?mecab:Requires: mecab-ipadic}
Requires:         coreutils
Requires(pre):    /usr/sbin/useradd
# We require this to be present for %%{_tmpfilesdir}
Requires:         systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires: %systemd_requires}
# SYS_NICE capabilities; #1540946
Recommends:       libcap
# semanage
Requires(post):   policycoreutils-python-utils

%if %{with mysql_names}
Provides:         mysql-server = %{sameevr}
Provides:         mysql-server%{?_isa} = %{sameevr}
Provides:         mysql-compat-server = %{sameevr}
Provides:         mysql-compat-server%{?_isa} = %{sameevr}
%endif
%{?with_conflicts:Conflicts:        mariadb-server}
%{?with_conflicts:Conflicts:        mariadb-galera-server}

%description      server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.


%if %{with devel}
%package          devel
Summary:          Files for development of MySQL applications
%{?with_clibrary:Requires:         %{name}-libs%{?_isa} = %{sameevr}}
Requires:         openssl-devel
Requires:         zlib-devel
Requires:         libzstd-devel
%{?with_conflicts:Conflicts:        mariadb-devel}

%description      devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.
%endif

%if %{with test}
%package          test
Summary:          The test suite distributed with MySQL
Requires:         %{name}%{?_isa} = %{sameevr}
Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{name}-server%{?_isa} = %{sameevr}
Requires:         gzip
Requires:         lz4
Requires:         openssl
Requires:         perl(Digest::file)
Requires:         perl(Digest::MD5)
Requires:         perl(Env)
Requires:         perl(Exporter)
Requires:         perl(Fcntl)
Requires:         perl(File::Temp)
Requires:         perl(FindBin)
Requires:         perl(Data::Dumper)
Requires:         perl(Getopt::Long)
Requires:         perl(IPC::Open3)
Requires:         perl(JSON)
Requires:         perl(LWP::Simple)
Requires:         perl(Memoize)
Requires:         perl(Socket)
Requires:         perl(Sys::Hostname)
Requires:         perl(Test::More)
Requires:         perl(Time::HiRes)
%{?with_conflicts:Conflicts:        mariadb-test}
%if %{with mysql_names}
Provides:         mysql-test = %{sameevr}
Provides:         mysql-test%{?_isa} = %{sameevr}
%endif

%description      test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.
%endif


%prep
%setup -q -n mysql-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch51 -p1
%patch52 -p1
%patch55 -p1
%patch75 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1

# Patch Boost
pushd boost/boost_$(echo %{boost_bundled_version}| tr . _)
%patch115 -p0
%patch125 -p1
popd

# Modify tests to pass on all archs
pushd mysql-test

add_test () {
    echo "$1" : BUG#0 "${@:2}" >> %{skiplist}
}

touch %{skiplist}

add_test innodb.redo_log_archive_04 failed since 8.0.17
add_test clone.remote_dml_no_binlog failed since 8.0.17
add_test auth_sec.keyring_file_data_qa sporadic since 8.0.19
add_test collations.chinese sporadic since 8.0.19

# Fails when -DENABLED_LOCAL_INFILE=ON
add_test main.mysql_load_data_local_dir local infile on

add_test rpl.rpl_row_jsondiff_basic_pk failed since 8.0.22
add_test rpl.rpl_row_jsondiff_basic_nokey failed since 8.0.22

# These tests fail on armv7hl; last check 8.0.16
%ifarch %arm aarch64
add_test gis.st_latitude
add_test gis.st_longitude
# Missing hw counters
add_test perfschema.func_file_io          missing hw on arm32
add_test perfschema.func_mutex            missing hw on arm32
add_test perfschema.global_read_lock      missing hw on arm32
add_test perfschema.setup_objects         missing hw on arm32
# Test added in 8.0.19
add_test clone.remote_error_basic max_allowed_packet is 0
# Failing in ~90% of times
add_test innodb.create_tablespace
%endif

%ifarch s390x
# Fails since F32 Mass Rebuild
add_test gis.geometry_class_attri_prop
add_test gis.geometry_property_function_issimple
add_test gis.gis_bugs_crashes
add_test gis.spatial_analysis_functions_buffer
add_test gis.spatial_analysis_functions_centroid
add_test gis.spatial_analysis_functions_distance
add_test gis.spatial_operators_intersection
add_test gis.spatial_op_testingfunc_mix
add_test gis.spatial_utility_function_distance_sphere
add_test gis.spatial_utility_function_simplify
add_test innodb.log_encrypt_kill main.with_recursive
add_test innodb.mysqldump_max_recordsize
add_test main.lock_multi_bug38499
add_test main.window_std_var
add_test main.window_std_var_optimized
add_test main.with_recursive

# Fails since 8.0.21
add_test x.resource_groups
add_test gis.spatial_operators_symdifference
add_test gis.spatial_operators_union

# Fails since 8.0.22
add_test main.subquery_bugs

%endif

%ifarch %arm
# Fails since 8.0.22
add_test perfschema.relaylog

%endif

# Fails since 2021 new year
add_test main.cast
add_test innodb.alter_kill
# Unstable tests
add_test innodb.innodb_read_only
add_test perfschema.processlist_acl
add_test innodb.innodb_bug-13628249


%ifarch ppc64le
add_test sys_vars.innodb_buffer_pool_size_basic
%endif

# mysql-test
popd

cp %{SOURCE2} %{SOURCE3} %{SOURCE10} %{SOURCE11} %{SOURCE12} \
   %{SOURCE14} %{SOURCE15} %{SOURCE17} %{SOURCE18} %{SOURCE31} scripts

%build
# arm build ends with out of memory error for LTO enabled build
%ifarch %arm
%define _lto_cflags %{nil}
%endif

# Display warning if user tries to build as root
%if %runselftest
    if [ x"$(id -u)" = "x0" ]; then
        echo "mysql's regression tests fail if run as root."
        echo "If you really need to build the RPM as root, use"
        echo "--nocheck to skip the regression tests."
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
         -DNICE_PROJECT_NAME="MySQL" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DSYSCONFDIR="%{_sysconfdir}" \
         -DSYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
         -DINSTALL_DOCDIR="share/doc/%{_pkgdocdirname}" \
         -DINSTALL_DOCREADMEDIR="share/doc/%{_pkgdocdirname}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_INFODIR=share/info \
         -DINSTALL_LIBEXECDIR=libexec \
         -DINSTALL_LIBDIR="%{_lib}/mysql" \
         -DRPATH_LIBDIR="%{_libdir}" \
         -DINSTALL_MANDIR=share/man \
         -DINSTALL_MYSQLSHAREDIR=share/%{pkg_name} \
         -DINSTALL_MYSQLTESTDIR=share/mysql-test \
         -DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
         -DINSTALL_SBINDIR=bin \
         -DINSTALL_SUPPORTFILESDIR=share/%{pkg_name} \
         -DMYSQL_DATADIR="%{dbdatadir}" \
         -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
         -DENABLED_LOCAL_INFILE=ON \
         -DWITH_SYSTEMD=1 \
         -DSYSTEMD_SERVICE_NAME="%{daemon_name}" \
         -DSYSTEMD_PID_DIR="%{pidfiledir}" \
         -DWITH_INNODB_MEMCACHED=ON \
%ifnarch aarch64 %{arm} s390 s390x
         -DWITH_NUMA=ON \
%endif
%ifarch s390 s390x armv7hl
         -DUSE_LD_GOLD=OFF \
%endif
         -DWITH_ROUTER=OFF \
         -DWITH_SYSTEM_LIBS=ON \
         -DWITH_MECAB=system \
         -DWITH_BOOST=boost \
         -DREPRODUCIBLE_BUILD=OFF \
         -DCMAKE_C_FLAGS="%{optflags}%{?with_debug: -fno-strict-overflow -Wno-unused-result -Wno-unused-function -Wno-unused-but-set-variable}" \
         -DCMAKE_CXX_FLAGS="%{optflags}%{?with_debug: -fno-strict-overflow -Wno-unused-result -Wno-unused-function -Wno-unused-but-set-variable}" \
         -DCMAKE_EXE_LINKER_FLAGS="-pie %{build_ldflags}" \
%{?with_debug: -DWITH_DEBUG=1} \
%{?with_debug: -DMYSQL_MAINTAINER_MODE=0} \
         -DTMPDIR=/var/tmp \
         -DWITH_MYSQLD_LDFLAGS="%{build_ldflags}" \
         -DCMAKE_C_LINK_FLAGS="%{build_ldflags}" \
         -DCMAKE_CXX_LINK_FLAGS="%{build_ldflags}" \
         -B %{_vpath_builddir}

# Note: linking with GOLD disabled on Armv7hl because of https://bugs.mysql.com/bug.php?id=96698

cmake -B %{_vpath_builddir} -LAH

%cmake_build

%install
%cmake_install

# multilib support for shell scripts
# we only apply this to known Red Hat multilib arches, per bug #181335
if %multilib_capable; then
mv %{buildroot}%{_bindir}/mysql_config %{buildroot}%{_bindir}/mysql_config-%{__isa_bits}
install -p -m 0755 %{_vpath_builddir}/scripts/mysql_config_multilib %{buildroot}%{_bindir}/mysql_config
fi

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also %%{name}-file-contents.patch)
install -p -m 0644 %{_vpath_builddir}/Docs/INFO_SRC %{buildroot}%{_libdir}/mysql/
install -p -m 0644 %{_vpath_builddir}/Docs/INFO_BIN %{buildroot}%{_libdir}/mysql/

mkdir -p %{buildroot}%{logfiledir}

mkdir -p %{buildroot}%{pidfiledir}
install -p -m 0755 -d %{buildroot}%{dbdatadir}
install -p -m 0750 -d %{buildroot}%{_localstatedir}/lib/mysql-files
install -p -m 0700 -d %{buildroot}%{_localstatedir}/lib/mysql-keyring

%if %{with config}
install -D -p -m 0644 %{_vpath_builddir}/scripts/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
%endif

# install systemd unit files and scripts for handling server startup
install -D -p -m 644 %{_vpath_builddir}/scripts/mysql.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 644 %{_vpath_builddir}/scripts/mysql@.service %{buildroot}%{_unitdir}/%{daemon_name}@.service
install -D -p -m 0644 %{_vpath_builddir}/scripts/mysql.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{daemon_name}.conf
rm -r %{buildroot}%{_tmpfilesdir}/mysql.conf

# helper scripts for service starting
install -D -p -m 755 %{_vpath_builddir}/scripts/mysql-prepare-db-dir %{buildroot}%{_libexecdir}/mysql-prepare-db-dir
install -p -m 755 %{_vpath_builddir}/scripts/mysql-wait-stop %{buildroot}%{_libexecdir}/mysql-wait-stop
install -p -m 755 %{_vpath_builddir}/scripts/mysql-check-socket %{buildroot}%{_libexecdir}/mysql-check-socket
install -p -m 644 %{_vpath_builddir}/scripts/mysql-scripts-common %{buildroot}%{_libexecdir}/mysql-scripts-common
install -D -p -m 0644 %{_vpath_builddir}/scripts/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf

rm %{buildroot}%{_libdir}/mysql/*.a
rm %{buildroot}%{_mandir}/man1/comp_err.1*

# put logrotate script where it needs to be
mkdir -p %{buildroot}%{logrotateddir}
mv %{buildroot}%{_datadir}/%{pkg_name}/mysql-log-rotate %{buildroot}%{logrotateddir}/%{daemon_name}
chmod 644 %{buildroot}%{logrotateddir}/%{daemon_name}

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# for back-ward compatibility and SELinux, let's keep the mysqld in libexec
# and just create a symlink in /usr/sbin
mv %{buildroot}%{_bindir}/mysqld %{buildroot}%{_libexecdir}/mysqld
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_libexecdir}/mysqld %{buildroot}%{_sbindir}/mysqld

%if %{with debug}
mv %{buildroot}%{_bindir}/mysqld-debug %{buildroot}%{_libexecdir}/mysqld
%endif

# copy additional docs into build tree so %%doc will find them
install -p -m 0644 %{SOURCE6} %{_vpath_srcdir}/%{basename:%{SOURCE6}}
install -p -m 0644 %{SOURCE7} %{_vpath_srcdir}/%{basename:%{SOURCE7}}

# Install the list of skipped tests to be available for user runs
install -p -m 0644 %{_vpath_srcdir}/mysql-test/%{skiplist} %{buildroot}%{_datadir}/mysql-test

%if %{without clibrary}
unlink %{buildroot}%{_libdir}/mysql/libmysqlclient.so
rm -r %{buildroot}%{_libdir}/mysql/libmysqlclient*.so.*
rm -r %{buildroot}%{_sysconfdir}/ld.so.conf.d
%endif

%if %{without devel}
rm %{buildroot}%{_bindir}/mysql_config*
rm -r %{buildroot}%{_includedir}/mysql
rm %{buildroot}%{_datadir}/aclocal/mysql.m4
rm %{buildroot}%{_libdir}/pkgconfig/mysqlclient.pc
rm %{buildroot}%{_libdir}/mysql/libmysqlclient*.so
rm %{buildroot}%{_mandir}/man1/mysql_config.1*
%endif

%if %{without client}
rm %{buildroot}%{_bindir}/{mysql,mysql_config_editor,\
mysql_plugin,mysqladmin,mysqlbinlog,\
mysqlcheck,mysqldump,mysqlpump,mysqlimport,mysqlshow,mysqlslap,my_print_defaults}
rm %{buildroot}%{_mandir}/man1/{mysql,mysql_config_editor,\
mysql_plugin,mysqladmin,mysqlbinlog,\
mysqlcheck,mysqldump,mysqlpump,mysqlimport,mysqlshow,mysqlslap,my_print_defaults}.1*
%endif

%if %{with config}
mkdir -p %{buildroot}%{_sysconfdir}/my.cnf.d
%else
#rm %{buildroot}%{_sysconfdir}/my.cnf
%endif

%if %{without common}
rm -r %{buildroot}%{_datadir}/%{pkg_name}/charsets
%endif

%if %{without errmsg}
rm %{buildroot}%{_datadir}/%{pkg_name}/{messages_to_error_log.txt,messages_to_clients.txt}
rm -r %{buildroot}%{_datadir}/%{pkg_name}/{english,bulgarian,czech,danish,dutch,estonian,\
french,german,greek,hungarian,italian,japanese,korean,norwegian,norwegian-ny,\
polish,portuguese,romanian,russian,serbian,slovak,spanish,swedish,ukrainian}
%endif

%if %{without test}
rm %{buildroot}%{_bindir}/{mysql_client_test,mysqlxtest,mysqltest_safe_process,zlib_decompress}
rm -r %{buildroot}%{_datadir}/mysql-test
%endif

%check
%if %{with test}
%if %runselftest
pushd %_vpath_builddir
make test VERBOSE=1
pushd mysql-test
cp ../../mysql-test/%{skiplist} .
# builds might happen at the same host, avoid collision
export MTR_BUILD_THREAD=%{__isa_bits}

./mtr %{?with_debug:--debug-server} \
  --mem --parallel=auto --force --retry=2 \
  --mysqld=--binlog-format=mixed \
  --suite-timeout=720 --testcase-timeout=30 \
  --report-unstable-tests --clean-vardir \
%if %{check_testsuite}
  --max-test-fail=0 || :
%else
  --skip-test-list=%{skiplist}
%endif
rm -r var $(readlink var)
popd
popd
%endif
%endif

%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{mysqluserhome} -s /sbin/nologin \
  -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :

%post server
%systemd_post %{daemon_name}.service
if [ ! -e "%{logfile}" -a ! -h "%{logfile}" ] ; then
    install /dev/null -m0640 -omysql -gmysql "%{logfile}"
fi

%preun server
%systemd_preun %{daemon_name}.service

%postun server
%systemd_postun_with_restart %{daemon_name}.service

%if %{with client}
%files
%{_bindir}/mysql
%{_bindir}/mysql_config_editor
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlpump
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config_editor.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlpump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%endif

%if %{with clibrary}
%files libs
%{_libdir}/mysql/libmysqlclient*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/*
%endif

%if %{with config}
%files config
# although the default my.cnf contains only server settings, we put it in the
# common package because it can be used for client settings too.
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%endif

%if %{with common}
%files common
%license LICENSE
%doc README README.mysql-license README.mysql-docs
%doc storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%dir %{_libdir}/mysql
%dir %{_datadir}/%{pkg_name}
%{_datadir}/%{pkg_name}/charsets
%endif

%if %{with errmsg}
%files errmsg
%{_datadir}/%{pkg_name}/messages_to_error_log.txt
%{_datadir}/%{pkg_name}/messages_to_clients.txt
%{_datadir}/%{pkg_name}/english
%lang(bg) %{_datadir}/%{pkg_name}/bulgarian
%lang(cs) %{_datadir}/%{pkg_name}/czech
%lang(da) %{_datadir}/%{pkg_name}/danish
%lang(nl) %{_datadir}/%{pkg_name}/dutch
%lang(et) %{_datadir}/%{pkg_name}/estonian
%lang(fr) %{_datadir}/%{pkg_name}/french
%lang(de) %{_datadir}/%{pkg_name}/german
%lang(el) %{_datadir}/%{pkg_name}/greek
%lang(hu) %{_datadir}/%{pkg_name}/hungarian
%lang(it) %{_datadir}/%{pkg_name}/italian
%lang(ja) %{_datadir}/%{pkg_name}/japanese
%lang(ko) %{_datadir}/%{pkg_name}/korean
%lang(no) %{_datadir}/%{pkg_name}/norwegian
%lang(no) %{_datadir}/%{pkg_name}/norwegian-ny
%lang(pl) %{_datadir}/%{pkg_name}/polish
%lang(pt) %{_datadir}/%{pkg_name}/portuguese
%lang(ro) %{_datadir}/%{pkg_name}/romanian
%lang(ru) %{_datadir}/%{pkg_name}/russian
%lang(sr) %{_datadir}/%{pkg_name}/serbian
%lang(sk) %{_datadir}/%{pkg_name}/slovak
%lang(es) %{_datadir}/%{pkg_name}/spanish
%lang(sv) %{_datadir}/%{pkg_name}/swedish
%lang(uk) %{_datadir}/%{pkg_name}/ukrainian
%endif

%files server
%{_bindir}/ibd2sdi
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/my_print_defaults
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_ssl_rsa_setup
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysqld_pre_systemd
%{_bindir}/mysqldumpslow
%{_bindir}/innochecksum
%{_bindir}/perror

%config(noreplace) %{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf

%{_sbindir}/mysqld
# sys_nice capability required for rhbz#1628814
%caps(cap_sys_nice=ep) %{_libexecdir}/mysqld

%{_libdir}/mysql/INFO_SRC
%{_libdir}/mysql/INFO_BIN
%if %{without common}
%dir %{_datadir}/%{pkg_name}
%endif

%dir %{_libdir}/mysql/plugin
%{_libdir}/mysql/plugin/adt_null.so
%{_libdir}/mysql/plugin/auth_socket.so
%{_libdir}/mysql/plugin/component_audit_api_message_emit.so
%{_libdir}/mysql/plugin/component_log_filter_dragnet.so
%{_libdir}/mysql/plugin/component_log_sink_json.so
%{_libdir}/mysql/plugin/component_log_sink_syseventlog.so
%{_libdir}/mysql/plugin/component_mysqlbackup.so
%{_libdir}/mysql/plugin/component_query_attributes.so
%{_libdir}/mysql/plugin/component_reference_cache.so
%{_libdir}/mysql/plugin/component_validate_password.so
%{_libdir}/mysql/plugin/connection_control.so
%{_libdir}/mysql/plugin/daemon_example.ini
%{_libdir}/mysql/plugin/ddl_rewriter.so
%{_libdir}/mysql/plugin/group_replication.so
%{_libdir}/mysql/plugin/ha_example.so
%{_libdir}/mysql/plugin/ha_mock.so
%{_libdir}/mysql/plugin/innodb_engine.so
%{_libdir}/mysql/plugin/keyring_file.so
%{_libdir}/mysql/plugin/keyring_udf.so
%{_libdir}/mysql/plugin/libmemcached.so
%{_libdir}/mysql/plugin/libpluginmecab.so
%{_libdir}/mysql/plugin/locking_service.so
%{_libdir}/mysql/plugin/mypluglib.so
%{_libdir}/mysql/plugin/mysql_clone.so
%{_libdir}/mysql/plugin/mysql_no_login.so
%{_libdir}/mysql/plugin/rewrite_example.so
%{_libdir}/mysql/plugin/rewriter.so
%{_libdir}/mysql/plugin/semisync_master.so
%{_libdir}/mysql/plugin/semisync_slave.so
%{_libdir}/mysql/plugin/validate_password.so
%{_libdir}/mysql/plugin/version_token.so

%{_mandir}/man1/ibd2sdi.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_ssl_rsa_setup.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/lz4_decompress.1*
%{_mandir}/man8/mysqld.8*

%{_datadir}/%{pkg_name}/dictionary.txt
%{_datadir}/%{pkg_name}/*.sql

%{_unitdir}/%{daemon_name}*
%{_libexecdir}/mysql-prepare-db-dir
%{_libexecdir}/mysql-wait-stop
%{_libexecdir}/mysql-check-socket
%{_libexecdir}/mysql-scripts-common

%{_tmpfilesdir}/%{daemon_name}.conf
%attr(0755,mysql,mysql) %dir %{dbdatadir}
%attr(0750,mysql,mysql) %dir %{_localstatedir}/lib/mysql-files
%attr(0700,mysql,mysql) %dir %{_localstatedir}/lib/mysql-keyring
%attr(0755,mysql,mysql) %dir %{pidfiledir}
%attr(0750,mysql,mysql) %dir %{logfiledir}
%attr(0640,mysql,mysql) %config %ghost %verify(not md5 size mtime) %{logfile}
%config(noreplace) %{logrotateddir}/%{daemon_name}

%if %{with devel}
%files devel
%{_bindir}/mysql_config*
%exclude %{_bindir}/mysql_config_editor
%{_includedir}/mysql
%{_datadir}/aclocal/mysql.m4
%if %{with clibrary}
%{_libdir}/mysql/libmysqlclient.so
%endif
%{_libdir}/pkgconfig/mysqlclient.pc
%{_mandir}/man1/mysql_config.1*
%endif

%if %{with test}
%files test
%{_bindir}/mysql_client_test
%{_bindir}/mysqltest
%{_bindir}/mysqltest_safe_process
%{_bindir}/mysqlxtest
%{_bindir}/mysqld_safe
%{_bindir}/comp_err
%{_bindir}/zlib_decompress
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%{_mandir}/man1/zlib_decompress.1*

%dir %{_libdir}/mysql/plugin
%{_libdir}/mysql/plugin/auth.so
%{_libdir}/mysql/plugin/auth_test_plugin.so
%{_libdir}/mysql/plugin/component_example_component1.so
%{_libdir}/mysql/plugin/component_example_component2.so
%{_libdir}/mysql/plugin/component_example_component3.so
%{_libdir}/mysql/plugin/component_log_sink_test.so
%{_libdir}/mysql/plugin/component_mysqlx_global_reset.so
%{_libdir}/mysql/plugin/component_pfs_example_component_population.so
%{_libdir}/mysql/plugin/component_pfs_example.so
%{_libdir}/mysql/plugin/component_test_audit_api_message.so
%{_libdir}/mysql/plugin/component_test_backup_lock_service.so
%{_libdir}/mysql/plugin/component_test_component_deinit.so
%{_libdir}/mysql/plugin/component_test_host_application_signal.so
%{_libdir}/mysql/plugin/component_test_mysql_current_thread_reader.so
%{_libdir}/mysql/plugin/component_test_mysql_runtime_error.so
%{_libdir}/mysql/plugin/component_test_pfs_notification.so
%{_libdir}/mysql/plugin/component_test_pfs_resource_group.so
%{_libdir}/mysql/plugin/component_test_status_var_service_int.so
%{_libdir}/mysql/plugin/component_test_status_var_service_reg_only.so
%{_libdir}/mysql/plugin/component_test_status_var_service.so
%{_libdir}/mysql/plugin/component_test_status_var_service_str.so
%{_libdir}/mysql/plugin/component_test_status_var_service_unreg_only.so
%{_libdir}/mysql/plugin/component_test_string_service_charset.so
%{_libdir}/mysql/plugin/component_test_string_service_long.so
%{_libdir}/mysql/plugin/component_test_string_service.so
%{_libdir}/mysql/plugin/component_test_system_variable_source.so
%{_libdir}/mysql/plugin/component_test_sys_var_service_int.so
%{_libdir}/mysql/plugin/component_test_sys_var_service_same.so
%{_libdir}/mysql/plugin/component_test_sys_var_service.so
%{_libdir}/mysql/plugin/component_test_sys_var_service_str.so
%{_libdir}/mysql/plugin/component_test_udf_registration.so
%{_libdir}/mysql/plugin/component_test_udf_services.so
%{_libdir}/mysql/plugin/component_udf_reg_3_func.so
%{_libdir}/mysql/plugin/component_udf_reg_avg_func.so
%{_libdir}/mysql/plugin/component_udf_reg_int_func.so
%{_libdir}/mysql/plugin/component_udf_reg_int_same_func.so
%{_libdir}/mysql/plugin/component_udf_reg_only_3_func.so
%{_libdir}/mysql/plugin/component_udf_reg_real_func.so
%{_libdir}/mysql/plugin/component_udf_unreg_3_func.so
%{_libdir}/mysql/plugin/component_udf_unreg_int_func.so
%{_libdir}/mysql/plugin/component_udf_unreg_real_func.so
%{_libdir}/mysql/plugin/libdaemon_example.so
%{_libdir}/mysql/plugin/libtest_framework.so
%{_libdir}/mysql/plugin/libtest_services.so
%{_libdir}/mysql/plugin/libtest_services_threaded.so
%{_libdir}/mysql/plugin/libtest_session_attach.so
%{_libdir}/mysql/plugin/libtest_session_detach.so
%{_libdir}/mysql/plugin/libtest_session_info.so
%{_libdir}/mysql/plugin/libtest_session_in_thd.so
%{_libdir}/mysql/plugin/libtest_sql_2_sessions.so
%{_libdir}/mysql/plugin/libtest_sql_all_col_types.so
%{_libdir}/mysql/plugin/libtest_sql_cmds_1.so
%{_libdir}/mysql/plugin/libtest_sql_commit.so
%{_libdir}/mysql/plugin/libtest_sql_complex.so
%{_libdir}/mysql/plugin/libtest_sql_errors.so
%{_libdir}/mysql/plugin/libtest_sql_lock.so
%{_libdir}/mysql/plugin/libtest_sql_processlist.so
%{_libdir}/mysql/plugin/libtest_sql_replication.so
%{_libdir}/mysql/plugin/libtest_sql_reset_connection.so
%{_libdir}/mysql/plugin/libtest_sql_shutdown.so
%{_libdir}/mysql/plugin/libtest_sql_sleep_is_connected.so
%{_libdir}/mysql/plugin/libtest_sql_sqlmode.so
%{_libdir}/mysql/plugin/libtest_sql_stmt.so
%{_libdir}/mysql/plugin/libtest_sql_stored_procedures_functions.so
%{_libdir}/mysql/plugin/libtest_sql_views_triggers.so
%{_libdir}/mysql/plugin/libtest_x_sessions_deinit.so
%{_libdir}/mysql/plugin/libtest_x_sessions_init.so
%{_libdir}/mysql/plugin/pfs_example_plugin_employee.so
%{_libdir}/mysql/plugin/qa_auth_client.so
%{_libdir}/mysql/plugin/qa_auth_interface.so
%{_libdir}/mysql/plugin/qa_auth_server.so
%{_libdir}/mysql/plugin/replication_observers_example_plugin.so
%{_libdir}/mysql/plugin/test_security_context.so
%{_libdir}/mysql/plugin/test_services_host_application_signal.so
%{_libdir}/mysql/plugin/test_services_plugin_registry.so
%{_libdir}/mysql/plugin/test_udf_services.so
%{_libdir}/mysql/plugin/udf_example.so
%endif

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 8.0.23-4
- Remove epoch

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.23-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Oct 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.23-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Adding a patch to fix building issue on Linux.

* Thu Feb 04 2021 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.23-1
- Update to MySQL 8.0.23
- Created community-mysql-fix-includes-robin-hood.patch

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 14:21:47 CET 2021 Adrian Reber <adrian@lisas.de> - 8.0.22-2
- Rebuilt for protobuf 3.14

* Wed Oct 21 2020 Lukas Javorsky <ljavorsk@redhat.com> - 8.0.22-1
- Update to MySQL 8.0.22
- community-mysql-certs-expired.patch patched by upstream
- community-mysql-lto.patch patched by upstream

* Tue Oct 20 2020 Jeff Law <law@redhat> - 8.0.21-16
- Fix another missing #include for gcc-11

* Tue Oct 06 2020 Jeff Law <law@redhat> - 8.0.21-15
- Add missing #include for gcc-11

* Thu Oct 01 13:33:42 CEST 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 8.0.21-14
- Rebuilt for libevent 2.1.12 (again)

* Wed Sep 23 2020 Adrian Reber <adrian@lisas.de> - 8.0.21-13
- Rebuilt for protobuf 3.13

* Tue Sep 15 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-12
- Rebuild due to libevent soname change

* Tue Aug 25 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-11
- Start building the MeCab plugin

* Mon Aug 24 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-10
- Fix the filelist. A number of shared libraries in the plugindir
  are part of the testsuite and thus should reside in *-test subpackage
  It will be best to keep the file list explicit to avoid this in the future

* Tue Aug 18 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-9
- I encounter the ARM memory exaustion in the end
  Looks like it is only issue on some machines

* Tue Aug 18 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-8
- I haven't encounter the ARM memory exaustion on Fedora build infrastructure
  Let's enable it and see how it will work

* Mon Aug 17 2020 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.21-7
- Use upstream patch to enable LTO
- Skip LTO on ARM due to out of memory issue

* Thu Aug 13 2020 Michal Schorm <mschorm@redhat.com> - 8.0.21-6
- Do a proper out-of-source CMake builds
- Force the CMake change regarding the in-source builds also to F31 and F32
- Use CMake macros instead of cmake & make direct commands
- %%cmake macro covers the %%{set_build_flags}, so they are not needed
- Remove ancient obsoletes

* Wed Aug 12 2020 Honza Horak <hhorak@redhat.com> - 8.0.21-5
- Check that we have correct versions in bundled(*) Provides
- Remove re2 dependency that is not needed any more

* Thu Aug 06 2020 Jeff Law <law@redhat.com> - 8.0.21-4
- Disable LTO

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.21-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.21-1
- Update to MySQL 8.0.21

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 8.0.20-3
- Rebuilt for protobuf 3.12

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 8.0.20-2
- Rebuild for ICU 67

* Sun Apr 26 2020 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.20-1
- Update to MySQL 8.0.20

* Wed Apr 01 2020 Jitka Plesnikova <jplesnik@redhat.com> - 8.0.19-3
- Specify all perl dependencies

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.19-1
- Update to MySQL 8.0.19

* Thu Dec 19 2019 Adrian Reber <adrian@lisas.de> - 8.0.18-6
- Include patch to build against protobuf 3.11

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 8.0.18-5
- Rebuild for protobuf 3.11

* Fri Nov 15 2019 Michal Schorm <mschorm@redhat.com> - 8.0.18-4
- Typo fixup

* Mon Nov 11 2019 Michal Schorm <mschorm@redhat.com> - 8.0.18-3
- Let the devel package require the libzstd-devel

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 8.0.18-2
- Rebuild for ICU 65

* Mon Oct 14 2019 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.18-1
- Update to MySQL 8.0.18

* Mon Aug 19 2019 Michal Schorm <mschorm@redhat.com> - 8.0.17-2
- Use RELRO hardening on all binaries

* Wed Jul 31 2019 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.17-1
- Update to MySQL 8.0.17

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Michal Schorm <mschorm@redhat.com> - 8.0.16-2
- Remove SysVInit stuff, no longer needed
- Clean up the SPECfile

* Fri Apr 26 2019 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.16-1
- Update to MySQL 8.0.16
- Rediff sharedir patch
- Refresh skip list and use new, required format
- Remove GCC9 patch now upstream
- Upstream: my_safe_process renamed and moved into proper location
- Use upstream option to skip router build
- OpenSSL 1.1.1 and TLSv1.3 is now supported, enable tests
- Update version of bundled Boost
- Start requiring mysql-selinux package

* Mon Feb 11 2019 Michal Schorm <mschorm@redhat.com> - 8.0.15-1
- Update to MySQL 8.0.15

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Honza Horak <hhorak@redhat.com> - 8.0.14-2
- Use RPATH for mysqld, so we can later set capabilities
- Set capabilities for mysqld the correct way

* Mon Jan 21 2019 Lars Tangvald <lars.tangvald@oracle.com> - 8.0.14-1
- Update to MySQL 8.0.14
- Remove fedora version condition that are no longer relevant
- Update skipped tests list
- CVEs fixed: #1666778
  CVE-2019-2420 CVE-2019-2434 CVE-2019-2436 CVE-2019-2455 CVE-2019-2481
  CVE-2019-2482 CVE-2019-2486 CVE-2019-2494 CVE-2019-2495 CVE-2019-2502
  CVE-2019-2503 CVE-2019-2507 CVE-2019-2510 CVE-2019-2528 CVE-2019-2529
  CVE-2019-2530 CVE-2019-2531 CVE-2019-2532 CVE-2019-2533 CVE-2019-2534
  CVE-2019-2535 CVE-2019-2536 CVE-2019-2537 CVE-2019-2539

* Wed Jan 16 2019 Michal Schorm <mschorm@redhat.com> - 8.0.13-3
- Tweak handling of the mysql-selinux requirement

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 8.0.13-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Oct 23 2018 Michal Schorm <mschorm@redhat.com> - 8.0.13-1
- Rebase to 8.0.13
- ICU patch removed; upstreamed
- Patch for MySQL Router introduced. Do not build it.
- CVEs fixed:
  CVE-2018-3276 CVE-2018-3200 CVE-2018-3137 CVE-2018-3284 CVE-2018-3195
  CVE-2018-3173 CVE-2018-3212 CVE-2018-3279 CVE-2018-3162 CVE-2018-3247
  CVE-2018-3156 CVE-2018-3161 CVE-2018-3278 CVE-2018-3174 CVE-2018-3282
  CVE-2018-3285 CVE-2018-3187 CVE-2018-3277 CVE-2018-3144 CVE-2018-3145
  CVE-2018-3170 CVE-2018-3186 CVE-2018-3182 CVE-2018-3133 CVE-2018-3143
  CVE-2018-3283 CVE-2018-3171 CVE-2018-3251 CVE-2018-3286 CVE-2018-3185
  CVE-2018-3280 CVE-2018-3203 CVE-2018-3155

* Thu Sep 06 2018 Michal Schorm <mschorm@redhat.com> - 8.0.12-2
- Fix the SYS_NICE capabilities
  Related: #1540946
- Add requires for the semanage binary

* Wed Aug 01 2018 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 8.0.12-1
- Update to MySQL 8.0.12

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 8.0.11-5
- Move log file to a directory owned by mysql user
  Resolves: #1590369
- Use explicitly openssl-devel as dependency for -devel sub-package

* Thu Jul 12 2018 Honza Horak <hhorak@redhat.com> - 8.0.11-4
- Move mysqld back to /usr/libexec, and create a symlink in /usr/sbin

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 8.0.11-2
- MySQL 8.0 has notify support
- SQL restart command needs MYSQLD_PARENT_PID=1
- Increase LimitNOFILE
- Disable symbolic links is default (and option deprecated)
- Move mysqld to /usr/bin, with mysqld_safe gone there no reason
  to have mysqld in libexec
- FIPS mode is now supported:
   https://dev.mysql.com/doc/refman/8.0/en/fips-mode.html
- Remove legacy embedded refs from cnf files
- Clean up patches: re-numbering and removing
- Recommend to use systemctl edit to modify service files

* Fri Apr 20 2018 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 8.0.11-1
- Update to MySQL 8.0.11 (GA).

* Thu Apr 19 2018 Michal Schorm <mschorm@redhat.com> - 5.7.22-1
- Rebase to 5.7.22 version
- CVE fixes: #1568963
            CVE-2018-2755 CVE-2018-2758 CVE-2018-2759 CVE-2018-2761 CVE-2018-2762
            CVE-2018-2766 CVE-2018-2769 CVE-2018-2771 CVE-2018-2773 CVE-2018-2775
            CVE-2018-2776 CVE-2018-2777 CVE-2018-2778 CVE-2018-2779 CVE-2018-2780
            CVE-2018-2781 CVE-2018-2782 CVE-2018-2784 CVE-2018-2786 CVE-2018-2787
            CVE-2018-2810 CVE-2018-2812 CVE-2018-2813 CVE-2018-2816 CVE-2018-2817
            CVE-2018-2818 CVE-2018-2819 CVE-2018-2839 CVE-2018-2846

* Tue Feb 27 2018 Michal Schorm <mschorm@redhat.com> - 5.7.21-6
- Rebuilt after Rawhide & f28 & f27 & f26 merge

* Sun Feb 25 2018 Michal Schorm <mschorm@redhat.com> - 5.7.21-5
- Rebuilt for ldconfig_post and ldconfig_postun bug
  Related: #1548331

* Mon Feb 19 2018 Michal Schorm <mschorm@redhat.com> - 5.7.21-3
- Move my_print_defaults binary to the server package to resolve conflict with mariadb

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
- Removed 'static' library subpackage

* Sun Jan 21 2018 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.21-1
- Update to MySQL 5.7.21, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-21.html
- Add rpcgen to buildrep
- Add support for libtirpc
- Fix for various CVEs listed on
  http://www.oracle.com/technetwork/security-advisory/cpujan2018-3236628.html
- Add fix for libxcrypt - do not assume "crypt()" function is provided by glibc
  Resolves: #1536881
- Fix obsoletes using isa macro, remove the line entirely
  Resolves: #1537210

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 5.7.20-5
- Rebuilt for switch to libxcrypt

* Tue Jan 02 2018 Michal Schorm <mschorm@redhat.com> - 5.7.20-4
- Provide subackage with a client static library
  Needed by mysql-connector-odbc package
- Remove Group tag as it shouldn't be used anymore

* Sat Dec 09 2017 Honza Horak <hhorak@redhat.com> - 5.7.20-3
- Port for OpenSSL 1.1
  Fix tests that expect some particular ciphers

* Tue Nov 28 2017 Michal Schorm <mschorm@redhat.com> - 5.7.20-2
- In F>27 stick to upstream library version naming

* Wed Oct 25 2017 Michal Schorm <mschorm@redhat.com> - 5.7.20-1
- Fix owner and perms on log file in post script
  Related: #1497694

* Mon Oct 16 2017 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.20-1
- Update to MySQL 5.7.20, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-20.html
- Move all test binaries to -test package
- Dont ship unneeded man pages on systemd platforms
- Remove mysql_config_editor from -devel package, shipped in client
- CVE fixes: #1503701
            CVE-2017-10155 CVE-2017-10227 CVE-2017-10268 CVE-2017-10276 CVE-2017-10279
            CVE-2017-10283 CVE-2017-10286 CVE-2017-10294 CVE-2017-10314 CVE-2017-10378
            CVE-2017-10379 CVE-2017-10384

* Mon Aug 28 2017 Honza Horak <hhorak@redhat.com> - 5.7.19-6
- Add bundled(boost) virtual provide
- Support --defaults-group-suffix option in systemd unit file
  Related: #1400702

* Fri Aug 04 2017 Honza Horak <hhorak@redhat.com> - 5.7.19-5
- Allow to use MD5 in FIPS mode
  Related: #1449689
- Remove snippets from mysql-preparep-db-dir.sh that could have security impact
  Do not run parts of SysV init script as root if possible
  Related: CVE-2017-3312
- Include mysqld@.service file and do not run start scripts in the unit file as root

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Michal Schorm <mschorm@redhat.com> - 5.7.19-2
- Replication tests in the testsuite enabled, they don't fail anymore
- Retry count in the testsuite dropped to 0

* Wed Jul 12 2017 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.19-1
- Update to MySQL 5.7.19, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-19.html
- Use new --report-unstable-tests to handle unstable tests
- Prefer /run over /var/run (#1462688)
- Resolves: #1462688; /run
            #1406172; random failures of the testsuite
            #1417880, #1417883, #1417885, #1417887,  #1417890, #1417891, #1417893,
            #1417894, #1417896; replication tests
- CVE fixes: #1472716
            CVE-2017-3633, CVE-2017-3634, CVE-2017-3635, CVE-2017-3641, CVE-2017-3647
            CVE-2017-3648, CVE-2017-3649, CVE-2017-3651, CVE-2017-3652, CVE-2017-3653

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 5.7.18-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed Apr 19 2017 Michal Schorm <mschorm@redhat.com> - 5.7.18-2
- 'force' option for 'rm' removed in specfile
- CVEs fixed by previous commit, #1443407:
  CVE-2017-3308 CVE-2017-3309 CVE-2017-3329 CVE-2017-3450
  CVE-2017-3453 CVE-2017-3456 CVE-2017-3461 CVE-2017-3462
  CVE-2017-3463 CVE-2017-3464 CVE-2017-3599 CVE-2017-3600

* Mon Apr 03 2017 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.18-1
- Update to MySQL 5.7.18, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-18.html
- Remove patch for test fix now upstream
- Sample my-*.cnf is gone

* Wed Feb 15 2017 Michal Schorm <mschorm@redhat.com> - 5.7.17-4
- Fix of broken cross mysql-mariadb dependecies
- Fix of community-mysql server-client dependecy
- Testsuite retry count lifted to 3 tries

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.17-2
- Fix test that used a hardcoded date (2017-01-01)

* Mon Dec 12 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.17-1
- Update to MySQL 5.7.17, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-17.html
- Add new plugin: connnection_control.so
- Add MySQL Group Replication: group_replication.so
- Add numactl-devel to buildreq and enable NUMA support (if available)
- Simplify boost path
- Build compat-openssl10 in rawhide for now
- Reqs. in -devel packages was incomplete

* Tue Oct 18 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.16-1
- Update to MySQL 5.7.16, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-16.html

* Tue Sep 06 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.15-1
- Update to MySQL 5.7.15, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-15.html
- Remove patches now upstream (buf_block_align,  lz4)
- perl(JSON) needed for tests
- Adjust list of problematic tests

* Wed Aug 10 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.14-2
- Skip rpl tests, unstable in Fedora build environment

* Tue Aug 09 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.14-1
- Update to MySQL 5.7.14, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-14.html
- Remove patches for bugs fixed upstream
- Fix for bug #79378 (buf_block_align)
- Fix for bug #82426 (build failure with system liblz4)
- Further reduce list of tests known to fail on certain platforms
- Set check_testsuite to 0 to make sure the build fails if any tests fail

* Wed Jul 13 2016 Norvald H. Ryeng <norvald.ryeng@oracle.com> - 5.7.13-1
- Update to MySQL 5.7.13, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-13.html

* Mon Jun 27 2016 Pavel Raiskup <praiskup@redhat.com> - 5.7.12-2
- BR multilib-rpm-config and use it for multilib workarounds

* Tue May 24 2016 Jakub Dorňák <jdornak@redhat.com> - 5.7.12-1
- Update to 5.7.12
  Thanks to Norvald H. Ryeng

* Sun Feb 14 2016 Honza Horak <hhorak@redhat.com> - 5.7.11-2
- Remove duplicate tmpfiles.d file
  Resolves: #1288216

* Thu Feb 11 2016 Honza Horak <hhorak@redhat.com> - 5.7.11-1
- Update to 5.7.11
  Thanks to Norvald H. Ryeng
  Removing tar ball with boost and using mysql tar ball with boost bundled

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Honza Horak <hhorak@redhat.com> - 5.7.10-2
- Use mysqld instead of mysqld_safe (mysqld_safe not necessary for 5.7)
  Use mysqld --initialize-insecure instead of mysql_install_db
  Create /var/lib/mysql-files (used by secure-file-priv)
    http://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_secure_file_priv
  Remove unnecessary Perl dependencies (mysqlhotcopy was removed in 5.7)
  Thanks Norvald H. Ryeng

* Wed Dec 16 2015 Jakub Dorňák <jdornak@redhat.com> - 5.7.10-1
- Update to 5.7.10

* Fri Oct  2 2015 Jakub Dorňák <jdornak@redhat.com> - 5.7.9-1
- Update to 5.7.9

* Thu Oct  1 2015 Jakub Dorňák <jdornak@redhat.com> - 5.6.27-1
- Update to 5.6.27

* Thu Jul 30 2015 Jakub Dorňák <jdornak@redhat.com> - 5.6.26-1
- Update to 5.6.26

* Tue Jul 21 2015 Jakub Dorňák <jdornak@redhat.com> - 5.6.25-1
- Update to 5.6.25

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.24-3
- gcc5 makes gcc49-aarch64 patch obsolete (and wrong)

* Fri Apr 10 2015 Honza Horak <hhorak@redhat.com> - 5.6.24-2
- Fix for big integers on gcc5

* Thu Apr 09 2015 Honza Horak <hhorak@redhat.com> - 5.6.24-1
- Update to 5.6.24

* Tue Mar 03 2015 Honza Horak <hhorak@redhat.com> - 5.6.23-4
- Do not use scl prefix more than once in paths
  Based on https://www.redhat.com/archives/sclorg/2015-February/msg00038.html
- Check permissions when starting service on RHEL-6
  Resolves: #1194699
- Wait for daemon ends
  Related: #1072958

* Mon Feb 23 2015 Honza Horak <hhorak@redhat.com> - 5.6.23-3
- Expand paths in perl scripts in mysql-test
- Use correct path in install_db script warning
- Use --no-defaults when checking server status before starting

* Thu Jan 29 2015 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.23-1
- Update to MySQL 5.6.23, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-23.html
- Expired certs patch now obsolete
- Fixed changelog
- Refreshed file contents patch
- Man pages fixed upstream
- Fix typo in server.cnf.in

* Mon Jan 26 2015 Honza Horak <hhorak@redhat.com> - 5.6.22-6
- Do not own /var/log

* Sun Jan 25 2015 Honza Horak <hhorak@redhat.com> - 5.6.22-5
- Use correct dir for config files

* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 5.6.22-4
- Move server settings to renamed config file under my.cnf.d dir

* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 5.6.22-3
- Fix path for sysconfig file
  Filter provides in el6 properly
  Fix initscript file location

* Mon Jan 12 2015 Honza Horak <hhorak@redhat.com> - 5.6.22-2
- Add configuration file for server

* Wed Dec  3 2014 Jakub Dorňák <jdornak@redhat.com> - 5.6.22-1
- Update to MySQL 5.6.22

* Wed Oct 08 2014 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.21-5
- Fix rhbz #1149986

* Wed Oct 01 2014 Honza Horak <hhorak@redhat.com> - 5.6.21-4
- Add bcond_without mysql_names

* Mon Sep 29 2014 Honza Horak <hhorak@redhat.com> - 5.6.21-3
- Check upgrade script added to warn about need for mysql_upgrade
- Move mysql_plugin into base and errmsg-utf8.txt into -errmsg to correspond
  with MariaDB upstream packages
- Add with_debug option

* Thu Sep 25 2014 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.21-2
- Using %%cmake macro break some tests, reverted
- Unwanted dtrace dep fixed upstream

* Wed Sep 24 2014 Honza Horak <hhorak@redhat.com> - 5.6.20-1
- Update to MySQL 5.6.21, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-21.html

* Thu Sep 04 2014 Honza Horak <hhorak@redhat.com> - 5.6.20-5
- Fix paths in mysql_install_db script
  Related: #1134328
- Use %%cmake macro
- Install systemd service file on RHEL-7+
  Server requires any mysql package, so it should be fine with older client

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Honza Horak <hhorak@redhat.com> - 5.6.20-3
- Introduce -config subpackage and ship base config files here

* Tue Aug 05 2014 Honza Horak <hhorak@redhat.com> - 5.6.20-2
- Adopt changes from mariadb to sync spec files

* Thu Jul 31 2014 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.20-1
- Update to MySQL 5.6.20, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-20.html
- Rebase install and pluginerrmsg patch
- Drop dos2unix from buildreq, files fixed upstream
- No need to add -O3, it's default
- LDFLAGS is passed by cmake option, not from environment
- Using __requires_exclude in conditional don't seems to work, swap
  to dist macros
- Avoid unwanted dtrace dep
- Fix mysql.init and mysql-prepare-db-dir
- Logfile name must match value from /etc/my.cnf (and be known
  by SELinux policy)

* Tue Jul 22 2014 Honza Horak <hhorak@redhat.com> - 5.6.19-5
- Hardcoded paths removed to work fine in chroot
- Spec rewrite to be more similar to oterh MySQL implementations
- Include SysV init script if built on older system
- Add possibility to not ship some sub-packages
- Port scripts for systemd unit from MariaDB

* Mon Jul 21 2014 Honza Horak <hhorak@redhat.com> - 5.6.19-4
- Port some latest changes from MariaDB package to sync those packages
- Error messages now provided by a separate package (thanks Alexander Barkov)

* Fri Jun 27 2014 Honza Horak <hhorak@redhat.com> - 5.6.19-3
- Add mysql-compat-server symbol, common symbol for arbitrary MySQL
  implementation
- Require /etc/my.cnf instead of shipping it
- Server requires any compatible mysql-compat-client package

* Thu Jun 12 2014 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.19-2
- Fix build on aarch64
- Rebase cipherspec patch

* Wed Jun 11 2014 Bjorn Munch <bjorn.munch@oracle.com> - 5.6.19-1
- Update to MySQL 5.6.19, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-19.html
- outfile_loaddata resolved on all archs
- Solaris files not installed, no need to remove
- Simplify multilib install
- Use install's -D option some places
- Add explicit conflict with mariadb-galera-server

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Bjorn Munch <bjorn.munch@oracle.com> 5.6.17-2
- Fix multiple mtr sessions

* Fri Apr 04 2014 Bjorn Munch <bjorn.munch@oracle.com> 5.6.17-1
- Update to MySQL 5.6.17, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-17.html
- libmysqld built as shared lib now supported upstream
- Remove patches now upstream: truncate-file, rhbz1059545, ssltest
  and regex-werror
- Use more standard (and tested) build flags, while still respect
  optflags and hardened_build
- libmysqlclient_r* symlinks are fixed upstream
- Remove sysv to systemd logic
- Rework skipping of arch specific tests
- Multiple mtr sessions are supported by default

* Mon Feb  3 2014 Honza Horak <hhorak@redhat.com> 5.6.16-2
- Rebuild -man-pages.patch to apply smoothly

* Fri Jan 31 2014 Bjorn Munch <bjorn.munch@oracle.com> 5.6.16-1
- Update to MySQL 5.6.16, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-16.html
- Patches now upstream: tmpdir, cve-2013-1861, covscan-signexpr,
  covscan-stroverflow
- Fixed upstream: innodbwarn
- ldconfig needed in embedded subpackage
- Remove unused generate-tarball.sh from tree
- Rediff mysql-install patch
- Make symvers 18 default, provide symvers 16 for backward compat
  (bz #1045013)
- Man page patch disabled due too many conflicts
- Memcached build patched to not remove -Werror=<something> in CFLAGS

* Thu Jan 30 2014 Honza Horak <hhorak@redhat.com> 5.6.15-4
  Fix for CVE-2014-0001
  Resolves: #1059545
- Don't test EDH-RSA-DES-CBC-SHA cipher, it seems to be removed from openssl
  which now makes mariadb/mysql FTBFS because openssl_1 test fails
  Related: #1044565

* Fri Jan 24 2014 Honza Horak <hhorak@redhat.com> 5.6.15-3
- Disable tests for ppc(64) and s390(x):
  innodb.innodb_ctype_ldml main.ctype_ldml main.ps_ddl main.ps_ddl1
  Related: #1056972

* Mon Dec 16 2013 Honza Horak <hhorak@redhat.com> 5.6.15-2
- Some spec file clean-up based on Bjorn Munch's suggestions
- Enable InnoDB Memcached plugin

* Mon Dec  9 2013 Honza Horak <hhorak@redhat.com> 5.6.15-1
- Update to MySQL 5.6.15, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-15.html

* Fri Oct 11 2013 Honza Horak <hhorak@redhat.com> 5.6.14-2
- Fix my.cnf to not conflict with mariadb
  Resolves: #1003115

* Wed Oct  9 2013 Honza Horak <hhorak@redhat.com> 5.6.14-1
- Update to MySQL 5.6.14, for various fixes described at
  https://dev.mysql.com/doc/relnotes/mysql/5.6/en/news-5-6-14.html
- Incorporate changes done by Bjorn Munch <bjorn.munch@oracle.com>

* Mon Sep  2 2013 Honza Horak <hhorak@redhat.com> 5.5.33-2
- Enhanced my.cnf to be the same as in mariadb
  Resolves: #1003115

* Tue Aug 20 2013 Honza Horak <hhorak@redhat.com> 5.5.33-1
- Update to MySQL 5.5.33, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-33.html

* Tue Aug 20 2013 Honza Horak <hhorak@redhat.com> 5.5.32-12
- Fix multilib header location for arm

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 5.5.32-11
- Perl 5.18 rebuild

* Fri Jul 26 2013 Honza Horak <hhorak@redhat.com> 5.5.32-10
- Copy some generated files in order find-debuginfo.sh finds them
  Related: #729040
- Fix systemd and perl requirements

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.5.32-9
- Perl 5.18 rebuild

* Mon Jul 15 2013 Honza Horak <hhorak@redhat.com> 5.5.32-8
- Revert path change to ldconfig, UsrMove is not complete yet

* Wed Jul 10 2013 Honza Horak <hhorak@redhat.com> 5.5.32-7
- Arm support for multilib hacks

* Tue Jul  9 2013 Honza Horak <hhorak@redhat.com> 5.5.32-6
- Use proper path to ldconfig
- Use xz instead of gzip
  Resolves: #982387

* Mon Jul  1 2013 Honza Horak <hhorak@redhat.com> 5.5.32-5
- Fix misleading error message when uninstalling built-in plugins
  Related: #966645

* Thu Jun 27 2013 Honza Horak <hhorak@redhat.com> 5.5.32-4
- Remove external man pages, upstream fixed man pages license
- Apply fixes found by Coverity static analysis tool

* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 5.5.32-3
- Use man pages from 5.5.30, because their license do not
  allow us to ship them since 5.5.31

* Fri Jun  7 2013 Honza Horak <hhorak@redhat.com> 5.5.32-1
- Update to MySQL 5.5.32, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-32.html

* Mon Jun  3 2013 Honza Horak <hhorak@redhat.com> 5.5.31-7
- Use /var/tmp as default tmpdir to prevent potential issues
  Resolves: #905635
- Fix test suite requirements
- Fix for CVE-2013-1861 backported from MariaDB
  Resolves: #921836

* Wed May 29 2013 Jan Stanek <jstanek@redhat.com> 5.5.31-6
- Added missing command-line options to man-pages (#948930)

* Tue Apr 30 2013 Honza Horak <hhorak@redhat.com> 5.5.31-5
- Remove mysql provides from devel sub-packages to not build against
  community-mysql if mysql-devel is specified

* Fri Apr 26 2013 Honza Horak <hhorak@redhat.com> 5.5.31-4
- Fix building with relro and PIE

* Thu Apr 25 2013 Honza Horak <hhorak@redhat.com> 5.5.31-3
- Fix paths in -plugin-test patch

* Mon Apr 22 2013 Honza Horak <hhorak@redhat.com> 5.5.31-2
- Build with _hardened_build
- Fix some paths and require perl(Env), which is needed by tests

* Fri Apr 19 2013 Honza Horak <hhorak@redhat.com> 5.5.31-1
- Update to MySQL 5.5.31, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-31.html

* Wed Mar 20 2013 Honza Horak <hhorak@redhat.com> 5.5.30-5
- Renaming package MySQL to community-mysql to handle issues
  introduced by case-insensitive operations of yum and for proper
  prioritizing mariadb over community-mysql

* Tue Mar 12 2013 Honza Horak <hhorak@redhat.com> 5.5.30-4
- Allow server to be installed without client side
- Separate -lib and -common sub-packages
- Fix some path issues in tests

* Mon Mar 11 2013 Honza Horak <hhorak@redhat.com> 5.5.30-3
- Adjusting major soname number of libmysqlclient to avoid
  library name conflicts with mariadb

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.30-1
- Update to MySQL 5.5.30, for various fixes described at
  http://dev.mysql.com/doc/relnotes/mysql/5.5/en/news-5-5-30.html

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Use real- prefix for cross-package requirements

* Mon Feb 11 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Provide own symbols with real- prefix to distinguish packages from other
  MySQL implementations unambiguously

* Wed Jan  2 2013 Tom Lane <tgl@redhat.com> 5.5.29-1
- Update to MySQL 5.5.29, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-29.html
- Fix inaccurate default for socket location in mysqld-wait-ready
Resolves: #890535

* Thu Dec  6 2012 Honza Horak <hhorak@redhat.com> 5.5.28-3
- Rebase patches to not leave backup files when not applied smoothly
- Use --no-backup-if-mismatch to prevent including backup files

* Wed Dec  5 2012 Tom Lane <tgl@redhat.com> 5.5.28-2
- Add patch for CVE-2012-5611
Resolves: #883642
- Widen DH key length from 512 to 1024 bits to meet minimum requirements
  of FIPS 140-2
Related: #877124

* Sat Sep 29 2012 Tom Lane <tgl@redhat.com> 5.5.28-1
- Update to MySQL 5.5.28, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-28.html
- Clean up partially-created database files when mysql_install_db fails
Related: #835131
- Honor user and group settings from service file in mysqld-prepare-db-dir
Resolves: #840431
- Export THR_KEY_mysys as a workaround for inadequate threading support
Resolves: #846602
- Adopt new systemd macros for server package install/uninstall triggers
Resolves: #850222
- Use --no-defaults when invoking mysqladmin to wait for the server to start
Related: #855704

* Sun Aug  5 2012 Tom Lane <tgl@redhat.com> 5.5.27-1
- Update to MySQL 5.5.27, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-27.html

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.25a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Tom Lane <tgl@redhat.com> 5.5.25a-1
- Update to MySQL 5.5.25a, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25a.html
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25.html
- Don't use systemd's Restart feature; rely on mysqld_safe instead
Resolves: #832029

* Mon Jun 11 2012 Tom Lane <tgl@redhat.com> 5.5.24-1
- Update to MySQL 5.5.24, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-24.html
  including the fix for CVE-2012-2122
Resolves: #830680
- Tweak logrotate script to put the right permissions on mysqld.log
- Minor specfile fixes for recent packaging guidelines changes

* Sat Apr 28 2012 Tom Lane <tgl@redhat.com> 5.5.23-1
- Update to MySQL 5.5.23, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-23.html

* Sat Mar 24 2012 Tom Lane <tgl@redhat.com> 5.5.22-1
- Update to MySQL 5.5.22, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-22.html
- Turn on PrivateTmp in service file
Resolves: #782513
- Comment out the contents of /etc/logrotate.d/mysqld, so that manual
  action is needed to enable log rotation.  Given the multiple ways in
  which the rotation script can fail, it seems imprudent to try to make
  it run by default.
Resolves: #799735

* Tue Mar 20 2012 Honza Horak <hhorak@redhat.com> 5.5.21-3
- Revise mysql_plugin test patch so it moves plugin files to
  a temporary directory (better solution to #789530)

* Tue Mar 13 2012 Honza Horak <hhorak@redhat.com> 5.5.21-2
- Fix ssl-related tests to specify expected cipher explicitly
Related: #789600
- Fix several strcpy calls to check destination size

* Mon Feb 27 2012 Tom Lane <tgl@redhat.com> 5.5.21-1
- Update to MySQL 5.5.21, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-21.html
- Hack openssl regression test to still work with rawhide's openssl
- Fix assorted failures in post-install regression tests (mysql-test RPM)
Resolves: #789530

* Fri Feb 10 2012 Tom Lane <tgl@redhat.com> 5.5.20-2
- Revise our test-disabling method to make it possible to disable tests on a
  platform-specific basis, and also to get rid of mysql-disable-test.patch,
  which broke in just about every upstream update (Honza Horak)
- Disable cycle-counter-dependent regression tests on ARM, since there is
  not currently any support for that in Fedora ARM kernels
Resolves: #773116
- Add some comments to mysqld.service documenting how to customize it
Resolves: #785243

* Fri Jan 27 2012 Tom Lane <tgl@redhat.com> 5.5.20-1
- Update to MySQL 5.5.20, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-20.html
  as well as security fixes described at
  http://www.oracle.com/technetwork/topics/security/cpujan2012-366304.html
Resolves: #783828
- Re-include the mysqld logrotate script, now that it's not so bogus
Resolves: #547007

* Wed Jan  4 2012 Tom Lane <tgl@redhat.com> 5.5.19-1
- Update to MySQL 5.5.19, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-19.html

* Sun Nov 20 2011 Tom Lane <tgl@redhat.com> 5.5.18-1
- Update to MySQL 5.5.18, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-18.html

* Sat Nov 12 2011 Tom Lane <tgl@redhat.com> 5.5.17-1
- Update to MySQL 5.5.17, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-17.html
- Get rid of version-number assumption in sysv-to-systemd conversion trigger

* Wed Nov 02 2011 Honza Horak <hhorak@redhat.com> 5.5.16-4
- Don't assume all ethernet devices are named ethX
Resolves: #682365
- Exclude user definition from my.cnf, user is defined in mysqld.service now
Resolves: #661265

* Sun Oct 16 2011 Tom Lane <tgl@redhat.com> 5.5.16-3
- Fix unportable usage associated with va_list arguments
Resolves: #744707

* Sun Oct 16 2011 Tom Lane <tgl@redhat.com> 5.5.16-2
- Update to MySQL 5.5.16, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-16.html

* Fri Jul 29 2011 Tom Lane <tgl@redhat.com> 5.5.15-2
- Update to MySQL 5.5.15, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-15.html

* Wed Jul 27 2011 Tom Lane <tgl@redhat.com> 5.5.14-3
- Convert to systemd startup support (no socket activation, for now anyway)
Related: #714426

* Tue Jul 12 2011 Tom Lane <tgl@redhat.com> 5.5.14-2
- Remove make_scrambled_password and make_scrambled_password_323 from mysql.h,
  since we're not allowing clients to call those functions anyway
Related: #690346

* Mon Jul 11 2011 Tom Lane <tgl@redhat.com> 5.5.14-1
- Update to MySQL 5.5.14, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-14.html

* Wed Jul  6 2011 Tom Lane <tgl@redhat.com> 5.5.13-2
- Remove erroneously-included Default-Start line from LSB init block
Resolves: #717024

* Thu Jun  2 2011 Tom Lane <tgl@redhat.com> 5.5.13-1
- Update to MySQL 5.5.13, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-13.html

* Tue May 10 2011 Tom Lane <tgl@redhat.com> 5.5.12-1
- Update to MySQL 5.5.12, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-12.html

* Tue May 10 2011 Tom Lane <tgl@redhat.com> 5.5.10-3
- Add LSB init block to initscript, to ensure sane ordering at system boot
Resolves: #703214
- Improve initscript start action to notice when mysqladmin is failing
  because of configuration problems
Related: #703476
- Remove exclusion of "gis" regression test, since upstream bug 59908
  is fixed (for some value of "fixed") as of 5.5.10.

* Wed Mar 23 2011 Tom Lane <tgl@redhat.com> 5.5.10-2
- Add my_make_scrambled_password to the list of symbols exported by
  libmysqlclient.so.  Needed at least by pure-ftpd.

* Mon Mar 21 2011 Tom Lane <tgl@redhat.com> 5.5.10-1
- Update to MySQL 5.5.10, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-10.html
  Note that this includes a rather belated soname version bump for
  libmysqlclient.so, from .16 to .18
- Add tmpfiles.d config file so that /var/run/mysqld is recreated at boot
  (only needed in Fedora 15 and later)
Resolves: #658938

* Wed Feb 16 2011 Tom Lane <tgl@redhat.com> 5.5.9-2
- Disable a regression test that is now showing platform-dependent results
Resolves: #674253

* Sat Feb 12 2011 Tom Lane <tgl@redhat.com> 5.5.9-1
- Update to MySQL 5.5.9, for various fixes described at
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-9.html
- Add %%{?_isa} to cross-subpackage Requires, per latest packaging guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tom Lane <tgl@redhat.com> 5.5.8-9
- Support s390/s390x in performance schema's cycle-counting functions
  (needed to make regression tests pass on these platforms)

* Thu Feb  3 2011 Tom Lane <tgl@redhat.com> 5.5.8-8
- PPC64 floating-point differences are not masked by -ffloat-store after all,
  so let's just disable gis regression test till upstream makes it less picky
Resolves: #674253
- Add __perllib_requires setting to make rpm 4.9 do what we need

* Wed Feb  2 2011 Tom Lane <tgl@redhat.com> 5.5.8-7
- Work around some portability issues on PPC64
Resolves: #674253

* Thu Jan 20 2011 Tom Lane <tgl@redhat.com> 5.5.8-6
- Remove no-longer-needed special switches in CXXFLAGS, per yesterday's
  discussion in fedora-devel about -fexceptions.
- Rebuild needed anyway to check compatibility with latest systemtap.

* Thu Jan 13 2011 Tom Lane <tgl@redhat.com> 5.5.8-5
- Fix failure to honor MYSQL_HOME environment variable
Resolves: #669364

* Thu Jan 13 2011 Tom Lane <tgl@redhat.com> 5.5.8-4
- Fix crash during startup of embedded mysqld library
Resolves: #667365

* Mon Jan  3 2011 Tom Lane <tgl@redhat.com> 5.5.8-3
- my_print_help, load_defaults, free_defaults, and handle_options all turn
  out to be documented/recommended in Paul DuBois' MySQL book, so we'd better
  consider them part of the de-facto API.
Resolves: #666728

* Mon Dec 27 2010 Tom Lane <tgl@redhat.com> 5.5.8-2
- Add mysql_client_errors[] to the set of exported libmysqlclient symbols;
  needed by PHP.

* Thu Dec 23 2010 Tom Lane <tgl@redhat.com> 5.5.8-1
- Update to MySQL 5.5.8 (major version bump).  Note this includes removal
  of libmysqlclient_r.so.
- Add a linker version script to hide libmysqlclient functions that aren't
  part of the documented API.

* Mon Nov  1 2010 Tom Lane <tgl@redhat.com> 5.1.52-1
- Update to MySQL 5.1.52, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-52.html
Resolves: #646569

* Thu Oct  7 2010 Tom Lane <tgl@redhat.com> 5.1.51-2
- Re-disable the outfile_loaddata test, per report from Dan Horak.

* Wed Oct  6 2010 Tom Lane <tgl@redhat.com> 5.1.51-1
- Update to MySQL 5.1.51, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-51.html

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-2
- Include my_compiler.h in distribution, per upstream bug #55846.
  Otherwise PHP, for example, won't build.

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-1
- Update to MySQL 5.1.50, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-50.html
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-49.html

* Wed Jul 14 2010 Tom Lane <tgl@redhat.com> 5.1.48-3
- Fix FTBFS with gcc 4.5.
Related: #614293

* Tue Jul 13 2010 Tom Lane <tgl@redhat.com> 5.1.48-2
- Duplicate COPYING and EXCEPTIONS-CLIENT in -libs and -embedded subpackages,
  to ensure they are available when any subset of mysql RPMs are installed,
  per revised packaging guidelines
- Allow init script's STARTTIMEOUT/STOPTIMEOUT to be overridden from sysconfig
Related: #609734

* Mon Jun 21 2010 Tom Lane <tgl@redhat.com> 5.1.48-1
- Update to MySQL 5.1.48, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-48.html
  including a fix for CVE-2010-2008
Related: #614214

* Fri Jun  4 2010 Tom Lane <tgl@redhat.com> 5.1.47-2
- Add back "partition" storage engine
Resolves: #597390
- Fix broken "federated" storage engine plugin
Related: #587170
- Read all certificates in SSL certificate files, to support chained certs
Related: #598656

* Mon May 24 2010 Tom Lane <tgl@redhat.com> 5.1.47-1
- Update to MySQL 5.1.47, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-47.html
  including fixes for CVE-2010-1848, CVE-2010-1849, CVE-2010-1850
Resolves: #592862
Resolves: #583717
- Create mysql group explicitly in pre-server script, to ensure correct GID
Related: #594155

* Sat Apr 24 2010 Tom Lane <tgl@redhat.com> 5.1.46-1
- Update to MySQL 5.1.46, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-46.html

* Thu Mar 25 2010 Tom Lane <tgl@redhat.com> 5.1.45-2
- Fix multiple problems described in upstream bug 52019, because regression
  tests fail on PPC if we don't.

* Wed Mar 24 2010 Tom Lane <tgl@redhat.com> 5.1.45-1
- Update to MySQL 5.1.45, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-45.html

* Sun Feb 21 2010 Tom Lane <tgl@redhat.com> 5.1.44-2
- Add "Obsoletes: mysql-cluster" to fix upgrade-in-place from F-12
- Bring init script into some modicum of compliance with Fedora/LSB standards
Related: #557711
Related: #562749

* Sat Feb 20 2010 Tom Lane <tgl@redhat.com> 5.1.44-1
- Update to MySQL 5.1.44, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-44.html
- Remove mysql.info, which is not freely redistributable
Resolves: #560181
- Revert broken upstream fix for their bug 45058
Resolves: #566547

* Sat Feb 13 2010 Tom Lane <tgl@redhat.com> 5.1.43-2
- Remove mysql-cluster, which is no longer supported by upstream in this
  source distribution.  If we want it we'll need a separate SRPM for it.

* Fri Feb 12 2010 Tom Lane <tgl@redhat.com> 5.1.43-1
- Update to MySQL 5.1.43, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-43.html

* Fri Jan 29 2010 Tom Lane <tgl@redhat.com> 5.1.42-7
- Add backported patch for CVE-2008-7247 (upstream bug 39277)
Related: #543619
- Use non-expired certificates for SSL testing (upstream bug 50702)

* Tue Jan 26 2010 Tom Lane <tgl@redhat.com> 5.1.42-6
- Emit explicit error message if user tries to build RPM as root
Related: #558915

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 5.1.42-5
- Correct Source0: tag and comment to reflect how to get the tarball

* Fri Jan  8 2010 Tom Lane <tgl@redhat.com> 5.1.42-4
- Disable symbolic links by default in /etc/my.cnf
Resolves: #553652

* Tue Jan  5 2010 Tom Lane <tgl@redhat.com> 5.1.42-3
- Remove static libraries (.a files) from package, per packaging guidelines
- Change %%define to %%global, per packaging guidelines

* Sat Jan  2 2010 Tom Lane <tgl@redhat.com> 5.1.42-2
- Disable building the innodb plugin; it tickles assorted gcc bugs and
  doesn't seem entirely ready for prime time anyway.

* Fri Jan  1 2010 Tom Lane <tgl@redhat.com> 5.1.42-1
- Update to MySQL 5.1.42, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-42.html
- Start mysqld_safe with --basedir=/usr, to avoid unwanted SELinux messages
Resolves: #547485

* Thu Dec 17 2009 Tom Lane <tgl@redhat.com> 5.1.41-2
- Stop waiting during "service mysqld start" if mysqld_safe exits
Resolves: #544095

* Mon Nov 23 2009 Tom Lane <tgl@redhat.com> 5.1.41-1
- Update to MySQL 5.1.41, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-41.html
  including fixes for CVE-2009-4019
Related: #540906
- Don't set old_passwords=1; we aren't being bug-compatible with 3.23 anymore
Resolves: #540735

* Tue Nov 10 2009 Tom Lane <tgl@redhat.com> 5.1.40-1
- Update to MySQL 5.1.40, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-40.html
- Do not force the --log-error setting in mysqld init script
Resolves: #533736

* Sat Oct 17 2009 Tom Lane <tgl@redhat.com> 5.1.39-4
- Replace kluge fix for ndbd sparc crash with a real fix (mysql bug 48132)

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 5.1.39-3
- Work around two different compiler bugs on sparc, one by backing off
  optimization from -O2 to -O1, and the other with a klugy patch
Related: #529298, #529299
- Clean up bogosity in multilib stub header support: ia64 should not be
  listed (it's not multilib), sparc and sparc64 should be

* Wed Sep 23 2009 Tom Lane <tgl@redhat.com> 5.1.39-2
- Work around upstream bug 46895 by disabling outfile_loaddata test

* Tue Sep 22 2009 Tom Lane <tgl@redhat.com> 5.1.39-1
- Update to MySQL 5.1.39, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-39.html

* Mon Aug 31 2009 Tom Lane <tgl@redhat.com> 5.1.37-5
- Work around unportable assumptions about stpcpy(); re-enable main.mysql test
- Clean up some obsolete parameters to the configure script

* Sat Aug 29 2009 Tom Lane <tgl@redhat.com> 5.1.37-4
- Remove one misguided patch; turns out I was chasing a glibc bug
- Temporarily disable "main.mysql" test; there's something broken there too,
  but we need to get mysql built in rawhide for dependency reasons

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.1.37-3
- rebuilt with new openssl

* Fri Aug 14 2009 Tom Lane <tgl@redhat.com> 5.1.37-2
- Add a couple of patches to improve the probability of the regression tests
  completing in koji builds

* Sun Aug  2 2009 Tom Lane <tgl@redhat.com> 5.1.37-1
- Update to MySQL 5.1.37, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-37.html

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Tom Lane <tgl@redhat.com> 5.1.36-1
- Update to MySQL 5.1.36, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-36.html

* Sat Jun  6 2009 Tom Lane <tgl@redhat.com> 5.1.35-1
- Update to MySQL 5.1.35, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-35.html
- Ensure that /var/lib/mysql is created with the right SELinux context
Resolves: #502966

* Fri May 15 2009 Tom Lane <tgl@redhat.com> 5.1.34-1
- Update to MySQL 5.1.34, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-34.html
- Increase startup timeout per bug #472222

* Wed Apr 15 2009 Tom Lane <tgl@redhat.com> 5.1.33-2
- Increase stack size of ndbd threads for safety's sake.
Related: #494631

* Tue Apr  7 2009 Tom Lane <tgl@redhat.com> 5.1.33-1
- Update to MySQL 5.1.33.
- Disable use of pthread_setschedparam; doesn't work the way code expects.
Related: #477624

* Wed Mar  4 2009 Tom Lane <tgl@redhat.com> 5.1.32-1
- Update to MySQL 5.1.32.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Tom Lane <tgl@redhat.com> 5.1.31-1
- Update to MySQL 5.1.31.

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-2
- hm, apparently --with-innodb and --with-ndbcluster are still needed
  even though no longer documented ...

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-1
- Update to MySQL 5.1.30.  Note that this includes an ABI break for
  libmysqlclient (it's now got .so major version 16).
- This also updates mysql for new openssl build

* Wed Oct  1 2008 Tom Lane <tgl@redhat.com> 5.0.67-2
- Build the "embedded server" library, and package it in a new sub-RPM
  mysql-embedded, along with mysql-embedded-devel for devel support files.
Resolves: #149829

* Sat Aug 23 2008 Tom Lane <tgl@redhat.com> 5.0.67-1
- Update to mysql version 5.0.67
- Move mysql_config's man page to base package, again (apparently I synced
  that change the wrong way while importing specfile changes for ndbcluster)

* Sun Jul 27 2008 Tom Lane <tgl@redhat.com> 5.0.51a-2
- Enable ndbcluster support
Resolves: #163758
- Suppress odd crash messages during package build, caused by trying to
  build dbug manual (which we don't install anyway) with dbug disabled
Resolves: #437053
- Improve mysql.init to pass configured datadir to mysql_install_db,
  and to force user=mysql for both mysql_install_db and mysqld_safe.
Related: #450178

* Mon Mar  3 2008 Tom Lane <tgl@redhat.com> 5.0.51a-1
- Update to mysql version 5.0.51a

* Mon Mar  3 2008 Tom Lane <tgl@redhat.com> 5.0.45-11
- Fix mysql-stack-guard patch to work correctly on IA64
- Fix mysql.init to wait correctly when socket is not in default place
Related: #435494

* Mon Mar 03 2008 Dennis Gilmore <dennis@ausil.us> 5.0.45-10
- add sparc64 to 64 bit arches for test suite checking
- add sparc, sparcv9 and sparc64 to multilib handling

* Thu Feb 28 2008 Tom Lane <tgl@redhat.com> 5.0.45-9
- Fix the stack overflow problem encountered in January.  It seems the real
issue is that the buildfarm machines were moved to RHEL5, which uses 64K not
4K pages on PPC, and because RHEL5 takes the guard area out of the requested
thread stack size we no longer had enough headroom.
Related: #435337

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.45-8
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Tom Lane <tgl@redhat.com> 5.0.45-7
- Unbelievable ... upstream still thinks that it's a good idea to have a
  regression test that is guaranteed to begin failing come January 1.
- ... and it seems we need to raise STACK_MIN_SIZE again too.

* Thu Dec 13 2007 Tom Lane <tgl@redhat.com> 5.0.45-6
- Back-port upstream fixes for CVE-2007-5925, CVE-2007-5969, CVE-2007-6303.
Related: #422211

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 5.0.45-5
- Rebuild for new openssl

* Sat Aug 25 2007 Tom Lane <tgl@redhat.com> 5.0.45-4
- Seems we need explicit BuildRequires on gawk and procps now
- Rebuild to fix Fedora toolchain issues

* Sun Aug 12 2007 Tom Lane <tgl@redhat.com> 5.0.45-3
- Recent perl changes in rawhide mean we need a more specific BuildRequires

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 5.0.45-2
- Update License tag to match code.
- Work around recent Fedora change that makes "open" a macro name.

* Sun Jul 22 2007 Tom Lane <tgl@redhat.com> 5.0.45-1
- Update to MySQL 5.0.45
Resolves: #246535
- Move mysql_config's man page to base package
Resolves: #245770
- move my_print_defaults to base RPM, for consistency with Stacks packaging
- mysql user is no longer deleted at RPM uninstall
Resolves: #241912

* Thu Mar 29 2007 Tom Lane <tgl@redhat.com> 5.0.37-2
- Use a less hacky method of getting default values in initscript
Related: #233771, #194596
- Improve packaging of mysql-libs per suggestions from Remi Collet
Resolves: #233731
- Update default /etc/my.cnf ([mysql.server] has been bogus for a long time)

* Mon Mar 12 2007 Tom Lane <tgl@redhat.com> 5.0.37-1
- Update to MySQL 5.0.37
Resolves: #231838
- Put client library into a separate mysql-libs RPM to reduce dependencies
Resolves: #205630

* Fri Feb  9 2007 Tom Lane <tgl@redhat.com> 5.0.33-1
- Update to MySQL 5.0.33
- Install band-aid fix for "view" regression test designed to fail after 2006
- Don't chmod -R the entire database directory tree on every startup
Related: #221085
- Fix unsafe use of install-info
Resolves: #223713
- Cope with new automake in F7
Resolves: #224171

* Thu Nov  9 2006 Tom Lane <tgl@redhat.com> 5.0.27-1
- Update to MySQL 5.0.27 (see CVE-2006-4031, CVE-2006-4226, CVE-2006-4227)
Resolves: #202247, #202675, #203427, #203428, #203432, #203434, #208641
- Fix init script to return status 1 on server start timeout
Resolves: #203910
- Move mysqldumpslow from base package to mysql-server
Resolves: #193559
- Adjust link options for BDB module
Resolves: #199368

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.0.22-2.1
- rebuild

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 5.0.22-2
- Work around brew's tendency not to clean up failed builds completely,
  by adding code in mysql-testing.patch to kill leftover mysql daemons.

* Thu Jun  8 2006 Tom Lane <tgl@redhat.com> 5.0.22-1
- Update to MySQL 5.0.22 (fixes CVE-2006-2753)
- Install temporary workaround for gcc bug on s390x (bz #193912)

* Tue May  2 2006 Tom Lane <tgl@redhat.com> 5.0.21-2
- Fix bogus perl Requires for mysql-test

* Mon May  1 2006 Tom Lane <tgl@redhat.com> 5.0.21-1
- Update to MySQL 5.0.21

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 5.0.18-4
- Modify multilib header hack to not break non-RH arches, per bug #181335
- Remove logrotate script, per bug #180639.
- Add a new mysql-test RPM to carry the regression test files;
  hack up test scripts as needed to make them run in /usr/share/mysql-test.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Tom Lane <tgl@redhat.com> 5.0.18-2
- err-log option has been renamed to log-error, fix my.cnf and initscript

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Tom Lane <tgl@redhat.com> 5.0.18-1
- Update to MySQL 5.0.18

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-4
- fix my_config.h for ppc platforms

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-3
- my_config.h needs to guard against 64-bit platforms that also define the
  32-bit symbol

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 5.0.16-2
- oops, looks like we want uname -i not uname -m

* Mon Dec 12 2005 Tom Lane <tgl@redhat.com> 5.0.16-1
- Update to MySQL 5.0.16
- Add EXCEPTIONS-CLIENT license info to the shipped documentation
- Make my_config.h architecture-independent for multilib installs;
  put the original my_config.h into my_config_$ARCH.h
- Add -fwrapv to CFLAGS so that gcc 4.1 doesn't break it

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Tom Lane <tgl@redhat.com> 5.0.15-3
- Make stop script wait for daemon process to disappear (bz#172426)

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 5.0.15-2
- Rebuild due to openssl library update.

* Thu Nov  3 2005 Tom Lane <tgl@redhat.com> 5.0.15-1
- Update to MySQL 5.0.15 (scratch build for now)

* Wed Oct  5 2005 Tom Lane <tgl@redhat.com> 4.1.14-1
- Update to MySQL 4.1.14

* Tue Aug 23 2005 Tom Lane <tgl@redhat.com> 4.1.12-3
- Use politically correct patch name.

* Tue Jul 12 2005 Tom Lane <tgl@redhat.com> 4.1.12-2
- Fix buffer overflow newly exposed in isam code; it's the same issue
  previously found in myisam, and not very exciting, but I'm tired of
  seeing build warnings.

* Mon Jul 11 2005 Tom Lane <tgl@redhat.com> 4.1.12-1
- Update to MySQL 4.1.12 (includes a fix for bz#158688, bz#158689)
- Extend mysql-test-ssl.patch to solve rpl_openssl test failure (bz#155850)
- Update mysql-lock-ssl.patch to match the upstream committed version
- Add --with-isam to re-enable the old ISAM table type, per bz#159262
- Add dependency on openssl-devel per bz#159569
- Remove manual.txt, as upstream decided not to ship it anymore;
  it was redundant with the mysql.info file anyway.

* Mon May  9 2005 Tom Lane <tgl@redhat.com> 4.1.11-4
- Include proper locking for OpenSSL in the server, per bz#155850

* Mon Apr 25 2005 Tom Lane <tgl@redhat.com> 4.1.11-3
- Enable openssl tests during build, per bz#155850
- Might as well turn on --disable-dependency-tracking

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 4.1.11-2
- Avoid dependency on <asm/atomic.h>, cause it won't build anymore on ia64.
  This is probably a cleaner solution for bz#143537, too.

* Thu Apr  7 2005 Tom Lane <tgl@redhat.com> 4.1.11-1
- Update to MySQL 4.1.11 to fix bz#152911 as well as other issues
- Move perl-DBI, perl-DBD-MySQL dependencies to server package (bz#154123)
- Override configure thread library test to suppress HAVE_LINUXTHREADS check
- Fix BDB failure on s390x (bz#143537)
- At last we can enable "make test" on all arches

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 4.1.10a-1
- Update to MySQL 4.1.10a to fix security vulnerabilities (bz#150868,
  for CAN-2005-0711, and bz#150871 for CAN-2005-0709, CAN-2005-0710).

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 4.1.10-3
- Fix package Requires: interdependencies.

* Sat Mar  5 2005 Tom Lane <tgl@redhat.com> 4.1.10-2
- Need -fno-strict-aliasing in at least one place, probably more.
- Work around some C spec violations in mysql.

* Fri Feb 18 2005 Tom Lane <tgl@redhat.com> 4.1.10-1
- Update to MySQL 4.1.10.

* Sat Jan 15 2005 Tom Lane <tgl@redhat.com> 4.1.9-1
- Update to MySQL 4.1.9.

* Wed Jan 12 2005 Tom Lane <tgl@redhat.com> 4.1.7-10
- Don't assume /etc/my.cnf will specify pid-file (bz#143724)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 4.1.7-9
- Rebuilt for new readline.

* Tue Dec 21 2004 Tom Lane <tgl@redhat.com> 4.1.7-8
- Run make test on all archs except s390x (which seems to have a bdb issue)

* Mon Dec 13 2004 Tom Lane <tgl@redhat.com> 4.1.7-7
- Suppress someone's silly idea that libtool overhead can be skipped

* Sun Dec 12 2004 Tom Lane <tgl@redhat.com> 4.1.7-6
- Fix init script to not need a valid username for startup check (bz#142328)
- Fix init script to honor settings appearing in /etc/my.cnf (bz#76051)
- Enable SSL (bz#142032)

* Thu Dec  2 2004 Tom Lane <tgl@redhat.com> 4.1.7-5
- Add a restorecon to keep the mysql.log file in the right context (bz#143887)

* Tue Nov 23 2004 Tom Lane <tgl@redhat.com> 4.1.7-4
- Turn off old_passwords in default /etc/my.cnf file, for better compatibility
  with mysql 3.x clients (per suggestion from Joe Orton).

* Fri Oct 29 2004 Tom Lane <tgl@redhat.com> 4.1.7-3
- Handle ldconfig more cleanly (put a file in /etc/ld.so.conf.d/).

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 4.1.7-2
- rebuild in devel branch

* Wed Oct 27 2004 Tom Lane <tgl@redhat.com> 4.1.7-1
- Update to MySQL 4.1.x.

* Tue Oct 12 2004 Tom Lane <tgl@redhat.com> 3.23.58-13
- fix security issues CAN-2004-0835, CAN-2004-0836, CAN-2004-0837
  (bugs #135372, 135375, 135387)
- fix privilege escalation on GRANT ALL ON `Foo\_Bar` (CAN-2004-0957)

* Wed Oct 06 2004 Tom Lane <tgl@redhat.com> 3.23.58-12
- fix multilib problem with mysqlbug and mysql_config
- adjust chkconfig priority per bug #128852
- remove bogus quoting per bug #129409 (MySQL 4.0 has done likewise)
- add sleep to mysql.init restart(); may or may not fix bug #133993

* Tue Oct 05 2004 Tom Lane <tgl@redhat.com> 3.23.58-11
- fix low-priority security issues CAN-2004-0388, CAN-2004-0381, CAN-2004-0457
  (bugs #119442, 125991, 130347, 130348)
- fix bug with dropping databases under recent kernels (bug #124352)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 3.23.58-10
- rebuilt

* Sat Apr 17 2004 Warren Togami <wtogami@redhat.com> 3.23.58-9
- remove redundant INSTALL-SOURCE, manual.*
- compress manual.txt.bz2
- BR time

* Tue Mar 16 2004 Tom Lane <tgl@redhat.com> 3.23.58-8
- repair logfile attributes in %%files, per bug #102190
- repair quoting problem in mysqlhotcopy, per bug #112693
- repair missing flush in mysql_setpermission, per bug #113960
- repair broken error message printf, per bug #115165
- delete mysql user during uninstall, per bug #117017
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- fix chown syntax in mysql.init
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 18 2003 Kim Ho <kho@redhat.com> 3.23.58-5
- update mysql.init to use anonymous user (UNKNOWN_MYSQL_USER) for
  pinging mysql server (#108779)

* Mon Oct 27 2003 Kim Ho <kho@redhat.com> 3.23.58-4
- update mysql.init to wait (max 10 seconds) for mysql server to
  start (#58732)

* Mon Oct 27 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-3
- re-enable Berkeley DB support (#106832)
- re-enable ia64 testing

* Fri Sep 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-2
- rebuilt

* Mon Sep 15 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-1
- upgrade to 3.23.58 for security fix

* Tue Aug 26 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-2
- rebuilt

* Wed Jul 02 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-1
- revert to prior version of MySQL due to license incompatibilities
  with packages that link against the client.  The MySQL folks are
  looking into the issue.

* Wed Jun 18 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-4
- restrict test on ia64 (temporary)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 4.0.13-3
- rebuilt

* Thu May 29 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-2
- fix filter-requires-mysql.sh with less restrictive for mysql-bench

* Wed May 28 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-1
- update for MySQL 4.0
- back-level shared libraries available in mysqlclient10 package

* Fri May 09 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-2
- add sql-bench package (#90110)

* Wed Mar 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-1
- upgrade to 3.23.56 for security fixes
- remove patch for double-free (included in 3.23.56)

* Tue Feb 18 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.54a-11
- enable thread safe client
- add patch for double free fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Karsten Hopp <karsten@redhat.de> 3.23.54a-9
- disable checks on s390x

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 3.23.54a-8
- use internal dep generator.

* Wed Jan  1 2003 Bill Nottingham <notting@redhat.com> 3.23.54a-7
- fix mysql_config on hammer

* Sun Dec 22 2002 Tim Powers <timp@redhat.com> 3.23.54a-6
- don't use rpms internal dep generator

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> 3.23.54a-5
- Push it into the build system

* Mon Dec 16 2002 Joe Orton <jorton@redhat.com> 3.23.54a-4
- upgrade to 3.23.54a for safe_mysqld fix

* Thu Dec 12 2002 Joe Orton <jorton@redhat.com> 3.23.54-3
- upgrade to 3.23.54 for latest security fixes

* Tue Nov 19 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-5
- Always include <errno.h> for errno
- Remove unpackaged files

* Tue Nov 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not prereq userdel, not used at all

* Mon Sep  9 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-4
- Use %%{_libdir}
- Add patch for x86-64

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-3
- rebuilt with gcc-3.2-7

* Thu Aug 29 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-2
- Add --enable-local-infile to configure - a new option
  which doesn't default to the old behaviour (#72885)

* Fri Aug 23 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-1
- 3.23.52. Fixes a minor security problem, various bugfixes.

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 3.23.51-5
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-4
- rebuild

* Thu Jul 18 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-3
- Fix #63543 and #63542

* Thu Jul 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-2
- Turn off bdb on PPC(#68591)
- Turn off the assembly optimizations, for safety.

* Wed Jun 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-1
- Work around annoying auto* thinking this is a crosscompile
- 3.23.51

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 10 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.50-2
- Add dependency on perl-DBI and perl-DBD-MySQL (#66349)

* Thu May 30 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.50-1
- 3.23.50

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-4
- Rebuild
- Don't set CXX to gcc, it doesn't work anymore
- Exclude Alpha

* Mon Apr  8 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-3
- Add the various .cnf examples as doc files to mysql-server (#60349)
- Don't include manual.ps, it's just 200 bytes with a URL inside (#60349)
- Don't include random files in /usr/share/mysql (#60349)
- langify (#60349)

* Thu Feb 21 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-2
- Rebuild

* Sun Feb 17 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-1
- 3.23.49

* Thu Feb 14 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.48-2
- work around perl dependency bug.

* Mon Feb 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.48-1
- 3.23.48

* Thu Jan 17 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-4
- Use kill, not mysqladmin, to flush logs and shut down. Thus,
  an admin password can be set with no problems.
- Remove reload from init script

* Wed Jan 16 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-3
- remove db3-devel from buildrequires,
  MySQL has had its own bundled copy since the mid thirties

* Sun Jan  6 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-1
- 3.23.47
- Don't build for alpha, toolchain immature.

* Mon Dec  3 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.46-1
- 3.23.46
- use -fno-rtti and -fno-exceptions, and set CXX to increase stability.
  Recommended by mysql developers.

* Sun Nov 25 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.45-1
- 3.23.45

* Wed Nov 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.44-2
- centralize definition of datadir in the initscript (#55873)

* Fri Nov  2 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.44-1
- 3.23.44

* Thu Oct  4 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.43-1
- 3.23.43

* Mon Sep 10 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.42-1
- 3.23.42
- reenable innodb

* Tue Aug 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.41-1
- 3.23.41 bugfix release
- disable innodb, to avoid the broken updates
- Use "mysqladmin flush_logs" instead of kill -HUP in logrotate
  script (#51711)

* Sat Jul 21 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.40, bugfix release
- Add zlib-devel to buildrequires:

* Fri Jul 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- BuildRequires-tweaking

* Thu Jun 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Reenable test, but don't run them for s390, s390x or ia64
- Make /etc/my.cnf config(noplace). Same for /etc/logrotate.d/mysqld

* Thu Jun 14 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29
- enable innodb
- enable assembly again
- disable tests for now...

* Tue May 15 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.38
- Don't use BDB on Alpha - no fast mutexes

* Tue Apr 24 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.37
- Add _GNU_SOURCE to the compile flags

* Wed Mar 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Make it obsolete our 6.2 PowerTools packages
- 3.23.36 bugfix release - fixes some security issues
  which didn't apply to our standard configuration
- Make "make test" part of the build process, except on IA64
  (it fails there)

* Tue Mar 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.35 bugfix release
- Don't delete the mysql user on uninstall

* Tue Mar 13 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.34a bugfix release

* Wed Feb  7 2001 Trond Eivind Glomsrd <teg@redhat.com>
- added readline-devel to BuildRequires:

* Tue Feb  6 2001 Trond Eivind Glomsrd <teg@redhat.com>
- small i18n-fixes to initscript (action needs $)

* Tue Jan 30 2001 Trond Eivind Glomsrd <teg@redhat.com>
- make it shut down and rotate logs without using mysqladmin
  (from #24909)

* Mon Jan 29 2001 Trond Eivind Glomsrd <teg@redhat.com>
- conflict with "MySQL"

* Tue Jan 23 2001 Trond Eivind Glomsrd <teg@redhat.com>
- improve gettextizing

* Mon Jan 22 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.32
- fix logrotate script (#24589)

* Wed Jan 17 2001 Trond Eivind Glomsrd <teg@redhat.com>
- gettextize
- move the items in Requires(post): to Requires: in preparation
  for an errata for 7.0 when 3.23.31 is released
- 3.23.31

* Tue Jan 16 2001 Trond Eivind Glomsrd <teg@redhat.com>
- add the log file to the rpm database, and make it 0640
  (#24116)
- as above in logrotate script
- changes to the init sequence - put most of the data
  in /etc/my.cnf instead of hardcoding in the init script
- use /var/run/mysqld/mysqld.pid instead of
  /var/run/mysqld/pid
- use standard safe_mysqld
- shut down cleaner

* Mon Jan 08 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.30
- do an explicit chmod on /var/lib/mysql in post, to avoid
  any problems with broken permissons. There is a report
  of rm not changing this on its own (#22989)

* Mon Jan 01 2001 Trond Eivind Glomsrd <teg@redhat.com>
- bzipped source
- changed from 85 to 78 in startup, so it starts before
  apache (which can use modules requiring mysql)

* Wed Dec 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29a

* Tue Dec 19 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add requirement for new libstdc++, build for errata

* Mon Dec 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29

* Mon Nov 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.28 (gamma)
- remove old patches, as they are now upstreamed

* Tue Nov 14 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Add a requirement for a new glibc (#20735)
- build on IA64

* Wed Nov  1 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable more assembly

* Wed Nov  1 2000 Jakub Jelinek <jakub@redhat.com>
- fix mysql on SPARC (#20124)

* Tue Oct 31 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.27

* Wed Oct 25 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add patch for fixing bogus aliasing in mysql from Jakub,
  which should fix #18905 and #18620

* Mon Oct 23 2000 Trond Eivind Glomsrd <teg@redhat.com>
- check for negative niceness values, and negate it
  if present (#17899)
- redefine optflags on IA32 FTTB

* Wed Oct 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.26, which among other fixes now uses mkstemp()
  instead of tempnam().
- revert changes made yesterday, the problem is now
  isolated

* Tue Oct 17 2000 Trond Eivind Glomsrd <teg@redhat.com>
- use the compat C++ compiler FTTB. Argh.
- add requirement of ncurses4 (see above)

* Sun Oct 01 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.25
- fix shutdown problem (#17956)

* Tue Sep 26 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Don't try to include no-longer-existing PUBLIC file
  as doc (#17532)

* Tue Sep 12 2000 Trond Eivind Glomsrd <teg@redhat.com>
- rename config file to /etc/my.cnf, which is what
  mysqld wants... doh. (#17432)
- include a changed safe_mysqld, so the pid file option
  works.
- make mysql dir world readable to they can access the
  mysql socket. (#17432)
- 3.23.24

* Wed Sep 06 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.23

* Sun Aug 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Add "|| :" to condrestart to avoid non-zero exit code

* Thu Aug 24 2000 Trond Eivind Glomsrd <teg@redhat.com>
- it's mysql.com, not mysql.org and use correct path to
  source (#16830)

* Wed Aug 16 2000 Trond Eivind Glomsrd <teg@redhat.com>
- source file from /etc/rc.d, not /etc/rd.d. Doh.

* Sun Aug 13 2000 Trond Eivind Glomsrd <teg@redhat.com>
- don't run ldconfig -n, it doesn't update ld.so.cache
  (#16034)
- include some missing binaries
- use safe_mysqld to start the server (request from
  mysql developers)

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Tue Aug 01 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.22. Disable the old patches, they're now in.

* Thu Jul 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- bugfixes in the initscript
- move the .so link to the devel package

* Wed Jul 19 2000 Trond Eivind Glomsrd <teg@redhat.com>
- rebuild due to glibc changes

* Tue Jul 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable compiler patch
- don't include info directory file

* Mon Jul 17 2000 Trond Eivind Glomsrd <teg@redhat.com>
- move back to /etc/rc.d/init.d

* Fri Jul 14 2000 Trond Eivind Glomsrd <teg@redhat.com>
- more cleanups in initscript

* Thu Jul 13 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add a patch to work around compiler bug
  (from monty@mysql.com)

* Wed Jul 12 2000 Trond Eivind Glomsrd <teg@redhat.com>
- don't build the SQL daemon statically (glibc problems)
- fix the logrotate script - only flush log if mysql
  is running
- change the reloading procedure 
- remove icon - glint is obsolete a long time ago

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrd <teg@redhat.com>
- try the new compiler again
- build the SQL daemon statically
- add compile time support for complex charsets
- enable assembler
- more cleanups in initscript

* Sun Jul 09 2000 Trond Eivind Glomsrd <teg@redhat.com>
- use old C++ compiler
- Exclusivearch x86

* Sat Jul 08 2000 Trond Eivind Glomsrd <teg@redhat.com>
- move .so files to devel package
- more cleanups
- exclude sparc for now

* Wed Jul 05 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.21
- remove file from /etc/sysconfig
- Fix initscript a bit - initialization of databases doesn't
  work yet
- specify the correct licenses
- include a /etc/my.conf (empty, FTTB)
- add conditional restart to spec file

* Sun Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrd <teg@redhat.com>
- update to 3.23.20
- use %%configure, %%makeinstall, %%{_tmppath}, %%{_mandir},
  %%{_infodir}, /etc/init.d
- remove the bench package
- change some of the descriptions a little bit
- fix the init script
- some compile fixes
- specify mysql user
- use mysql uid 27 (postgresql is 26)
- don't build on ia64

* Sat Feb 26 2000 Jos Vos <jos@xos.nl>
- Version 3.22.32 release XOS.1 for LinuX/OS 1.8.0
- Upgrade from version 3.22.27 to 3.22.32.
- Do "make install" instead of "make install-strip", because "install -s"
  now appears to fail on various scripts.  Afterwards, strip manually.
- Reorganize subpackages, according to common Red Hat packages: the client
  program and shared library become the base package and the server and
  some accompanying files are now in a separate server package.  The
  server package implicitly requires the base package (shared library),
  but we have added a manual require tag anyway (because of the shared
  config file, and more).
- Rename the mysql-benchmark subpackage to mysql-bench.

* Mon Jan 31 2000 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.2 for LinuX/OS 1.7.1
- Add post(un)install scripts for updating ld.so.conf (client subpackage).

* Sun Nov 21 1999 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.1 for LinuX/OS 1.7.0
- Initial version.
- Some ideas borrowed from Red Hat Powertools 6.1, although this spec
  file is a full rewrite from scratch.
