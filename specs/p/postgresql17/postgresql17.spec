# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.

# This spec file and ancillary files are licensed in accordance with
# The PostgreSQL license.

# In this file you can find the default build package list macros.
# These can be overridden by defining on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the libs package, the devel package, and the server package
# always get built.

%{!?test:%global test 1}
%{!?llvmjit:%global llvmjit 0}
%{!?external_libpq:%global external_libpq 0}
%{!?upgrade:%global upgrade 1}
%{!?plpython3:%global plpython3 1}
%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?icu:%global icu 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%{!?pam:%global pam 1}
%{!?sdt:%global sdt 1}
%{!?selinux:%global selinux 1}
%{!?runselftest:%global runselftest 1}
%{!?postgresql_default:%global postgresql_default 0}

%global majorname postgresql
%global majorversion 17

# By default, patch(1) creates backup files when chunks apply with offsets.
# Turn that off to ensure such files don't get included in RPMs.
%global _default_patch_flags --no-backup-if-mismatch

# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_of_Additional_RPM_Macros
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Don't create note file, added package_note_flags to linker by redhat-rpm-config
# will cause issue during extension build because it'll be inherited.
%undefine _package_note_file

Summary: PostgreSQL client programs
Name: %{majorname}%{majorversion}
Version: %{majorversion}.6
Release: 2%{?dist}

# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License: PostgreSQL
Url: http://www.postgresql.org/

# This SRPM includes a copy of the previous major release, which is needed for
# in-place upgrade of an old database.  In most cases it will not be critical
# that this be kept up with the latest minor release of the previous series;
# but update when bugs affecting pg_dump output are fixed.
%global prevmajorversion 16
%global prevversion %{prevmajorversion}.10
%global prev_prefix %{_libdir}/pgsql/postgresql-%{prevmajorversion}
%global precise_version %{?epoch:%epoch:}%version-%release

%global setup_version 8.9

%global service_name postgresql.service

Source0: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source3: https://ftp.postgresql.org/pub/source/v%{prevversion}/postgresql-%{prevversion}.tar.bz2
Source4: Makefile.regress
Source9: postgresql.tmpfiles.d
Source10: postgresql.pam
Source11: postgresql-bashprofile


# git: https://github.com/devexp-db/postgresql-setup
Source12: https://github.com/devexp-db/postgresql-setup/releases/download/v%{setup_version}/postgresql-setup-%{setup_version}.tar.gz

# Those here are just to enforce packagers check that the tarball was downloaded
# correctly.  Also, this allows us check that packagers-only tarballs do not
# differ with publicly released ones.
Source16: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.sha256
Source17: https://ftp.postgresql.org/pub/source/v%{prevversion}/postgresql-%{prevversion}.tar.bz2.sha256

# Comments for these patches are in the patch files.
Patch1: rpm-pgsql.patch
Patch2: postgresql-logging.patch
Patch5: postgresql-var-run-socket.patch
Patch8: postgresql-external-libpq.patch
Patch9: postgresql-server-pg_config.patch
# Upstream bug #16971: https://www.postgresql.org/message-id/16971-5d004d34742a3d35%40postgresql.org
# rhbz#1940964
Patch10: postgresql-datalayout-mismatch-on-s390.patch
Patch12: postgresql-no-libecpg.patch

# This macro is used for package names in the files section
%if %?postgresql_default
%global pkgname %{majorname}
%package -n %{pkgname}
Summary: PostgreSQL client programs
%else
%global pkgname %{majorname}%{majorversion}
%endif

BuildRequires: make
BuildRequires: libzstd-devel
BuildRequires: lz4-devel
BuildRequires: gcc
BuildRequires: perl(ExtUtils::MakeMaker) glibc-devel bison flex gawk
BuildRequires: perl(ExtUtils::Embed), perl-devel
BuildRequires: perl(Opcode)
BuildRequires: perl-FindBin
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: perl-generators
%endif
BuildRequires: readline-devel zlib-devel
BuildRequires: systemd systemd-devel util-linux
BuildRequires: multilib-rpm-config
%if %external_libpq
BuildRequires: libpq-devel >= %version
%endif
BuildRequires: docbook-style-xsl

# postgresql-setup build requires
BuildRequires: m4 elinks docbook-utils help2man

%if %plpython3
BuildRequires: python3-devel
%endif

%if %pltcl
BuildRequires: tcl-devel
%endif

%if %ssl
BuildRequires: openssl-devel
%endif

%if %kerberos
BuildRequires: krb5-devel
%endif

%if %ldap
BuildRequires: openldap-devel
%endif

%if %nls
BuildRequires: gettext >= 0.10.35
%endif

%if %uuid
BuildRequires: uuid-devel
%endif

%if %xml
BuildRequires: libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires: pam-devel
%endif

%if %sdt
BuildRequires: systemtap-sdt-devel
BuildRequires: systemtap-sdt-dtrace
%endif

%if %selinux
BuildRequires: libselinux-devel
%endif

%if %icu
BuildRequires:	libicu-devel
%endif

%if %?postgresql_default
%define postgresqlXX_if_default() %{expand:\
Provides: postgresql%{majorversion}%{?1:-%{1}} = %precise_version\
Provides: postgresql%{majorversion}%{?1:-%{1}}%{?_isa} = %precise_version\
Obsoletes: postgresql%{majorversion}%{?1:-%{1}}\
}
%else
%define postgresqlXX_if_default() %{nil}
%endif

%define conflict_with_other_streams() %{expand:\
Provides: %{majorname}%{?1:-%{1}}-any\
Conflicts: %{majorname}%{?1:-%{1}}-any\
}

%define virtual_conflicts_and_provides() %{expand:\
%conflict_with_other_streams %{**}\
%postgresqlXX_if_default %{**}\
}

Provides: %{pkgname} = %precise_version
Provides: %{pkgname}%{?_isa} = %precise_version

%virtual_conflicts_and_provides

# https://bugzilla.redhat.com/1464368
# and do not provide pkgconfig RPM provides (RHBZ#1980992) and #2121696
%global __provides_exclude_from %{_libdir}/(pgsql|pkgconfig)

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.  The PostgreSQL server can be found in the
postgresql-server sub-package.

%description -n %{pkgname}
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.  The PostgreSQL server can be found in the
postgresql-server sub-package.


%if ! %external_libpq
%package -n %{pkgname}-private-libs
Summary: The shared libraries required only for this build of PostgreSQL server
Group: Applications/Databases
# for /sbin/ldconfig
Requires(post): glibc
Requires(postun): glibc
Provides: %{pkgname}-private-libs = %precise_version
Provides: %{pkgname}-private-libs%{?_isa} = %precise_version

%virtual_conflicts_and_provides private-libs

%description -n %{pkgname}-private-libs
The postgresql-private-libs package provides the shared libraries for this
build of PostgreSQL server and plugins build with this version of server.
For shared libraries used by client packages that need to connect to a
PostgreSQL server, install libpq package instead.


%package -n %{pkgname}-private-devel
Summary: PostgreSQL development header files for this build of PostgreSQL server
Group: Development/Libraries
Requires: %{pkgname}-private-libs%{?_isa} = %precise_version
# Conflict is desired here, a user must pick one or another
Conflicts: libpq-devel
Provides: %{pkgname}-devel = %precise_version
Provides: %{pkgname}-devel%{?_isa} = %precise_version

%virtual_conflicts_and_provides private-devel

%description -n %{pkgname}-private-devel
The postgresql-private-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server.
You need to install this package if you want to develop applications which
will interact with a PostgreSQL server.
%endif


%package -n %{pkgname}-server
Summary: The programs needed to create and run a PostgreSQL server
Requires: %{pkgname}%{?_isa} = %precise_version
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires: systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires}
# We require this to be present for /usr/sbin/runuser when using --initdb (rhbz#2071437)
Requires: util-linux
# postgresql setup requires runuser from util-linux package
BuildRequires: util-linux
# Packages which provide postgresql plugins should build-require
# postgresql-server-devel and require
# postgresql-server(:MODULE_COMPAT_%%{postgresql_major}).
# This will automatically guard against incompatible server & plugin
# installation (#1008939, #1007840)
Provides: %{pkgname}-server(:MODULE_COMPAT_%{majorversion})
Provides: bundled(postgresql-setup) = %setup_version
Provides: %{pkgname}-server = %precise_version
Provides: %{pkgname}-server%{?_isa} = %precise_version
# Provide symbol regardless version. This symbol is present in every single
# postgresql stream

%virtual_conflicts_and_provides server

%description -n %{pkgname}-server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.


%package -n %{pkgname}-docs
Summary: Extra documentation for PostgreSQL
Requires: %{pkgname}%{?_isa} = %precise_version
Provides: %{pkgname}-doc = %precise_version
Provides: %{pkgname}-docs = %precise_version

%virtual_conflicts_and_provides docs

%description -n %{pkgname}-docs
The postgresql-docs package contains some additional documentation for
PostgreSQL.  Currently, this includes the main documentation in PDF format
and source files for the PostgreSQL tutorial.


%package -n %{pkgname}-contrib
Summary: Extension modules distributed with PostgreSQL
Requires: %{pkgname}%{?_isa} = %precise_version
Provides: %{pkgname}-contrib = %precise_version
Provides: %{pkgname}-contrib%{?_isa} = %precise_version

%virtual_conflicts_and_provides contrib

%description -n %{pkgname}-contrib
The postgresql-contrib package contains various extension modules that are
included in the PostgreSQL distribution.


%package -n %{pkgname}-server-devel
Summary: PostgreSQL development header files and libraries
%if %icu
Requires:	libicu-devel
%endif
%if %kerberos
Requires: krb5-devel
%endif
%if %llvmjit
Requires: clang-devel llvm-devel
%endif
%if %external_libpq
# Some extensions require libpq
# Do not make them care about whether server uses private or system-wide
# libpq, simply let the server pull the correct one
Requires: libpq-devel
%else
Requires: %{pkgname}-private-devel
%endif
Provides: %{pkgname}-server-devel = %precise_version
Provides: %{pkgname}-server-devel%{?_isa} = %precise_version

%virtual_conflicts_and_provides server-devel

%description -n %{pkgname}-server-devel
The postgresql-server-devel package contains the header files and configuration
needed to compile PostgreSQL server extension.

%package -n %{pkgname}-test-rpm-macros
Summary: Convenience RPM macros for build-time testing against PostgreSQL server
Requires: %{pkgname}-server = %precise_version
BuildArch: noarch
Provides: %{pkgname}-test-rpm-macros = %precise_version

%conflict_with_other_streams test-rpm-macros

%description -n %{pkgname}-test-rpm-macros
This package is meant to be added as BuildRequires: dependency of other packages
that want to run build-time testsuite against running PostgreSQL server.


%package -n %{pkgname}-static
Summary: Statically linked PostgreSQL libraries
Requires: %{pkgname}-server-devel%{?_isa} = %precise_version
Provides: %{pkgname}-static = %precise_version
Provides: %{pkgname}-static%{?_isa} = %precise_version

%virtual_conflicts_and_provides static

%description -n %{pkgname}-static
Statically linked PostgreSQL libraries that do not have dynamically linked
counterparts.


%if %upgrade
%package -n %{pkgname}-upgrade
Summary: Support for upgrading from the previous major release of PostgreSQL
Requires: %{pkgname}-server%{?_isa} = %precise_version
Provides: bundled(postgresql-server) = %prevversion
Provides: %{pkgname}-upgrade = %precise_version
Provides: %{pkgname}-upgrade%{?_isa} = %precise_version

%virtual_conflicts_and_provides upgrade

%description -n %{pkgname}-upgrade
The postgresql-upgrade package contains the pg_upgrade utility and supporting
files needed for upgrading a PostgreSQL database from the previous major
version of PostgreSQL.


%package -n %{pkgname}-upgrade-devel
Summary: Support for build of extensions required for upgrade process
Requires: %{pkgname}-upgrade%{?_isa} = %precise_version
Provides: %{pkgname}-upgrade-devel = %precise_version
Provides: %{pkgname}-upgrade-devel%{?_isa} = %precise_version

%virtual_conflicts_and_provides upgrade-devel

%description -n %{pkgname}-upgrade-devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which are necessary in upgrade
process.
%endif


%if %plperl
%package -n %{pkgname}-plperl
Summary: The Perl procedural language for PostgreSQL
Requires: %{pkgname}-server%{?_isa} = %precise_version
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if %runselftest
BuildRequires: perl(Opcode)
BuildRequires: perl(Data::Dumper)
%endif
Provides: %{pkgname}-plperl = %precise_version
Provides: %{pkgname}-plperl%{?_isa} = %precise_version

%virtual_conflicts_and_provides plperl

%description -n %{pkgname}-plperl
The postgresql-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.
%endif


%if %plpython3
%package -n %{pkgname}-plpython3
Summary: The Python3 procedural language for PostgreSQL
Requires: %{pkgname}-server%{?_isa} = %precise_version
Provides: %{pkgname}-plpython3 = %precise_version
Provides: %{pkgname}-plpython3%{?_isa} = %precise_version

%virtual_conflicts_and_provides plpython3

%description -n %{pkgname}-plpython3
The postgresql-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.
%endif


%if %pltcl
%package -n %{pkgname}-pltcl
Summary: The Tcl procedural language for PostgreSQL
Requires: %{pkgname}-server%{?_isa} = %precise_version
Provides: %{pkgname}-pltcl = %precise_version
Provides: %{pkgname}-pltcl%{?_isa} = %precise_version

%virtual_conflicts_and_provides pltcl

%description -n %{pkgname}-pltcl
The postgresql-pltcl package contains the PL/Tcl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Tcl.
%endif


%if %test
%package -n %{pkgname}-test
Summary: The test suite distributed with PostgreSQL
Requires: %{pkgname}-server%{?_isa} = %precise_version
Requires: %{pkgname}-server-devel%{?_isa} = %precise_version
Requires: %{pkgname}-contrib%{?_isa} = %precise_version
Provides: %{pkgname}-test = %precise_version
Provides: %{pkgname}-test%{?_isa} = %precise_version

%virtual_conflicts_and_provides test

%description -n %{pkgname}-test
The postgresql-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%if %llvmjit
%package -n %{pkgname}-llvmjit
Summary:	Just-in-time compilation support for PostgreSQL
Requires:	%{pkgname}-server%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
Requires:	llvm5.0 >= 5.0
%else
Requires:	llvm => 5.0
%endif
Provides:	postgresql-llvmjit >= %{version}-%{release}
Provides: %{pkgname}-llvmjit = %precise_version
Provides: %{pkgname}-llvmjit%{?_isa} = %precise_version

BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0

%virtual_conflicts_and_provides llvmjit

%description -n %{pkgname}-llvmjit
The postgresql-llvmjit package contains support for
just-in-time compiling parts of PostgreSQL queries. Using LLVM it
compiles e.g. expressions and tuple deforming into native code, with the
goal of accelerating analytics queries.
%endif

%prep
(
  cd "$(dirname "%{SOURCE0}")"
  sha256sum -c %{SOURCE16}
%if %upgrade
  sha256sum -c %{SOURCE17}
%endif
)
%setup -q -a 12 -n postgresql-%{version}
%patch 1 -p1
%patch 2 -p1
%patch 5 -p1
%if %external_libpq
%patch 8 -p1
%else
%patch 12 -p1
%endif
%patch 9 -p1
%patch 10 -p1


%if ! %external_libpq
%global private_soname private%{majorversion}
find . -type f -name Makefile -exec sed -i -e "s/SO_MAJOR_VERSION=\s\?\([0-9]\+\)/SO_MAJOR_VERSION= %{private_soname}-\1/" {} \;
%endif

%if %upgrade
tar xfj %{SOURCE3}

# libpq from this upgrade-only build is dropped and the libpq from the main
# version is used. Use the same major hack therefore.
%if ! %external_libpq
find . -type f -name Makefile -exec sed -i -e "s/SO_MAJOR_VERSION=\s\?\([0-9]\+\)/SO_MAJOR_VERSION= %{private_soname}-\1/" {} \;
%endif

# apply once SOURCE3 is extracted
%endif

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm

# Create a sysusers.d config file
cat >postgresql17.sysusers.conf <<EOF
u postgres 26 'PostgreSQL Server' /var/lib/pgsql /bin/bash
EOF

cat > postgresql17.tmpfiles.conf <<EOF
d /var/lib/pgsql 0700 postgres postgres -
EOF

%build
# Avoid LTO on armv7hl as it runs out of memory
%ifarch armv7hl s390x
%define _lto_cflags %{nil}
%endif
# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "postgresql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

# Building postgresql-setup

cd postgresql-setup-%{setup_version}

%configure \
    pgdocdir=%{_pkgdocdir} \
    PGVERSION=%{version} \
    PGMAJORVERSION=%{majorversion} \
    NAME_DEFAULT_PREV_SERVICE=postgresql

make %{?_smp_mflags}
cd ..

# Fiddling with CFLAGS.

CFLAGS="${CFLAGS:-%optflags}"
CFLAGS="$CFLAGS -DOPENSSL_NO_ENGINE -std=c18"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
export CFLAGS

common_configure_options='
	--disable-rpath
%if %plperl
	--with-perl
%endif
%if %pltcl
	--with-tcl
	--with-tclconfig=/usr/%_lib
%endif
%if %ldap
	--with-ldap
%endif
%if %ssl
	--with-openssl
%endif
%if %pam
	--with-pam
%endif
%if %kerberos
	--with-gssapi
%endif
%if %uuid
	--with-ossp-uuid
%endif
%if %xml
	--with-libxml
	--with-libxslt
%endif
%if %nls
	--enable-nls
%endif
%if %sdt
	--enable-dtrace
%endif
%if %selinux
	--with-selinux
%endif
	--with-system-tzdata=/usr/share/zoneinfo
	--datadir=%_datadir/pgsql
	--with-systemd
	--with-lz4
    --with-zstd
%if %icu
	--with-icu
%endif
%if %llvmjit
	--with-llvm
%endif
%if %plpython3
	--with-python
%endif
'

export PYTHON=/usr/bin/python3

# These configure options must match main build
%configure $common_configure_options

%make_build world

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

# The object files shouldn't be copied to rpm bz#1187514
rm -f src/tutorial/*.o

# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path.  When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.  This function
# never exits directly nor stops rpmbuild where `set -e` is enabled.
run_testsuite()
{
	make -k -C "$1" MAX_CONNECTIONS=5 check && return 0 || test_failure=1
	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find "$1" -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

test_failure=0

%if %runselftest
	run_testsuite "src/test/regress"
	make clean -C "src/test/regress"
	run_testsuite "src/pl"
	run_testsuite "contrib"
%endif

# "assert(ALL_TESTS_OK)"
test "$test_failure" -eq 0

%if %test
	# undo the "make clean" above
	make all -C src/test/regress
%endif

%if %upgrade
	pushd postgresql-%{prevversion}

	# The upgrade build can be pretty stripped-down, but make sure that
	# any options that affect on-disk file layout match the previous
	# major release!

	# The set of built server modules here should ideally create superset
	# of modules we used to ship in %%prevversion (in the installation
	# the user will upgrade from), including *-contrib or *-pl*
	# subpackages.  This increases chances that the upgrade from
	# %%prevversion will work smoothly.

upgrade_configure ()
{
	# Note we intentionally do not use %%configure here, because we *don't* want
	# its ideas about installation paths.

	# The -fno-aggressive-loop-optimizations is hack for #993532
	CFLAGS="$CFLAGS -fno-aggressive-loop-optimizations -DOPENSSL_NO_ENGINE" ./configure \
		--build=%{_build} \
		--host=%{_host} \
		--prefix=%prev_prefix \
		--disable-rpath \
		--with-lz4 \
        --with-zstd \
%if %icu
		--with-icu \
%endif
%if %plperl
		--with-perl \
%endif
%if %pltcl
		--with-tcl \
%endif
%if %ldap
       --with-ldap \
%endif
%if %pam
       --with-pam \
%endif
%if %kerberos
       --with-gssapi \
%endif
%if %uuid
       --with-ossp-uuid \
%endif
%if %xml
       --with-libxml \
       --with-libxslt \
%endif
%if %nls
       --enable-nls \
%endif
%if %sdt
       --enable-dtrace \
%endif
%if %selinux
       --with-selinux \
%endif
%if %plpython3
		--with-python \
%endif
		--with-tclconfig=/usr/%_lib \
		--with-system-tzdata=/usr/share/zoneinfo \
		"$@"
}

	upgrade_configure \

	make %{?_smp_mflags} all
	make -C contrib %{?_smp_mflags} all
	popd
# endif upgrade
%endif


%install
cd postgresql-setup-%{setup_version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

# For some reason, having '%%doc %%{_pkgdocdir}/README.rpm-dist' in %%files
# causes FTBFS (at least on RHEL6), see rhbz#1250006.
mv $RPM_BUILD_ROOT/%{_pkgdocdir}/README.rpm-dist ./

cat > $RPM_BUILD_ROOT%{_sysconfdir}/postgresql-setup/upgrade/postgresql.conf <<EOF
id              postgresql
major           %{prevmajorversion}
data_default    %{_localstatedir}/pgsql/data
package         postgresql-upgrade
engine          %{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin
description     "Upgrade data from system PostgreSQL version (PostgreSQL %{prevmajorversion})"
redhat_sockets_hack no
EOF

make DESTDIR=$RPM_BUILD_ROOT install-world

# We ship pg_config through libpq-devel
mv $RPM_BUILD_ROOT/%_mandir/man1/pg_{,server_}config.1
%if %external_libpq
rm $RPM_BUILD_ROOT/%_includedir/pg_config*.h
rm $RPM_BUILD_ROOT/%_includedir/libpq/libpq-fs.h
rm $RPM_BUILD_ROOT/%_includedir/postgres_ext.h
rm -r $RPM_BUILD_ROOT/%_includedir/pgsql/internal/
%else
ln -s pg_server_config $RPM_BUILD_ROOT/%_bindir/pg_config
rm $RPM_BUILD_ROOT/%{_libdir}/libpq.a
%endif

# make sure these directories exist even if we suppressed all contrib modules
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/contrib
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/extension

# multilib header hack
for header in \
	%{_includedir}/pgsql/server/pg_config.h \
	%{_includedir}/pgsql/server/pg_config_ext.h
do
%multilib_fix_c_header --file "$header"
done

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial
cp -p src/tutorial/* $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial

%if %pam
install -d $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/pam.d/postgresql
%endif

mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_tmpfilesdir}/postgresql.conf

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/.bash_profile

rm $RPM_BUILD_ROOT/%{_datadir}/man/man1/ecpg.1

%if %upgrade
	pushd postgresql-%{prevversion}
	make DESTDIR=$RPM_BUILD_ROOT install
	make -C contrib DESTDIR=$RPM_BUILD_ROOT install
	popd

	# remove stuff we don't actually need for upgrade purposes
	pushd $RPM_BUILD_ROOT%{_libdir}/pgsql/postgresql-%{prevmajorversion}
	rm bin/clusterdb
	rm bin/createdb
	rm bin/createuser
	rm bin/dropdb
	rm bin/dropuser
	rm bin/ecpg
	rm bin/initdb
	rm bin/pg_basebackup
	rm bin/pg_dump
	rm bin/pg_dumpall
	rm bin/pg_restore
	rm bin/pgbench
	rm bin/psql
	rm bin/reindexdb
	rm bin/vacuumdb
	rm -rf share/doc
	rm -rf share/man
	rm -rf share/tsearch_data
	rm lib/*.a
	# Drop libpq.  This might need some tweaks once there's
	# soname bump between %%prevversion and %%version.
	rm lib/libpq.so*
	# Drop libraries.
	rm lib/lib{ecpg,ecpg_compat,pgtypes}.so*
	rm share/*.bki
	rm share/*.sample
	rm share/*.sql
	rm share/*.txt
	rm share/extension/*.sql
	rm share/extension/*.control
	popd
	cat <<EOF > $RPM_BUILD_ROOT%macrosdir/macros.postgresql-upgrade
%%postgresql_upgrade_prefix %prev_prefix
EOF
%endif

# Let plugins use the same llvmjit settings as server has
cat <<EOF >> $RPM_BUILD_ROOT%macrosdir/macros.postgresql
%%postgresql_server_llvmjit %llvmjit
EOF

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
	cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
	# pg_regress binary should be only in one subpackage,
	# there will be a symlink from -test to -devel
	rm -f $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/pg_regress
	rm -f $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/refint.so
	rm -f $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/autoinc.so
	ln -sf ../../pgxs/src/test/regress/pg_regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/pg_regress
	ln -sf ../../autoinc.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/autoinc.so
	ln -sf ../../refint.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/refint.so
	pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
	rm -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	sed 's|@bindir@|%{_bindir}|g' \
		< %{SOURCE4} \
		> $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
	chmod 0644 $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
%endif

rm -rf doc/html # HACK! allow 'rpmbuild -bi --short-circuit'
mv $RPM_BUILD_ROOT%{_docdir}/pgsql/html doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/pgsql

# remove files not to be packaged
rm $RPM_BUILD_ROOT%{_libdir}/libpgfeutils.a

%if !%plperl
rm -f $RPM_BUILD_ROOT%{_bindir}/pgsql/hstore_plperl.so
%endif

# no python2, yet installed, remove
rm -f $RPM_BUILD_ROOT%{_datadir}/pgsql/extension/*_plpythonu*
rm -f $RPM_BUILD_ROOT%{_datadir}/pgsql/extension/*_plpython2u*

%if %nls
find_lang_bins ()
{
	lstfile=$1 ; shift
	cp /dev/null "$lstfile"
	for binary; do
		%find_lang "$binary"-%{majorversion}
		cat "$binary"-%{majorversion}.lang >>"$lstfile"
	done
}
find_lang_bins devel.lst pg_server_config
find_lang_bins server.lst \
	initdb pg_basebackup pg_controldata pg_ctl pg_resetwal pg_rewind plpgsql \
	postgres pg_checksums pg_verifybackup pg_combinebackup \
    pg_walsummary
find_lang_bins contrib.lst \
	pg_amcheck pg_archivecleanup pg_test_fsync pg_test_timing pg_waldump
find_lang_bins main.lst \
	pg_dump pg_upgrade pgscripts psql \
%if ! %external_libpq
libpq%{private_soname}-5
%endif

%if %plperl
find_lang_bins plperl.lst plperl
%endif
%if %plpython3
find_lang_bins plpython3.lst plpython
%endif
%if %pltcl
find_lang_bins pltcl.lst pltcl
%endif
%endif

install -m0644 -D postgresql17.sysusers.conf %{buildroot}%{_sysusersdir}/postgresql17.conf
install -m0644 -D postgresql17.tmpfiles.conf %{buildroot}%{_tmpfilesdir}/postgresql17.conf

%post -n %{pkgname}-server
%systemd_post %service_name


%preun -n %{pkgname}-server
%systemd_preun %service_name


%postun -n %{pkgname}-server
%systemd_postun_with_restart %service_name


%check
%if %runselftest
make -C postgresql-setup-%{setup_version} check
%endif

# FILES sections.
%files -f main.lst -n %{pkgname}
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/TODO
%doc COPYRIGHT HISTORY
%doc README.rpm-dist
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_restore
%{_bindir}/pg_upgrade
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_isready.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/pg_upgrade.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%if %llvmjit
# Install bitcode directory along with the main package,
# so that extensions can use this dir.
%dir %{_libdir}/pgsql/bitcode
%endif


%if ! %external_libpq
%files -n %{pkgname}-private-libs
%{_libdir}/libpq.so.*
%endif


%files -n %{pkgname}-docs
%doc doc/html
%{_libdir}/pgsql/tutorial/


%files -n %{pkgname}-contrib -f contrib.lst
%doc contrib/spi/*.example
%{_bindir}/oid2name
%{_bindir}/pg_amcheck
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_waldump

%{_bindir}/pg_walsummary
%{_bindir}/pg_combinebackup

%{_bindir}/pgbench
%{_bindir}/vacuumlo
%{_datadir}/pgsql/extension/amcheck*
%{_datadir}/pgsql/extension/autoinc*
%{_datadir}/pgsql/extension/bloom*
%{_datadir}/pgsql/extension/btree_gin*
%{_datadir}/pgsql/extension/btree_gist*
%{_datadir}/pgsql/extension/citext*
%{_datadir}/pgsql/extension/cube*
%{_datadir}/pgsql/extension/dblink*
%{_datadir}/pgsql/extension/dict_int*
%{_datadir}/pgsql/extension/dict_xsyn*
%{_datadir}/pgsql/extension/earthdistance*
%{_datadir}/pgsql/extension/file_fdw*
%{_datadir}/pgsql/extension/fuzzystrmatch*
%{_datadir}/pgsql/extension/hstore*
%{_datadir}/pgsql/extension/insert_username*
%{_datadir}/pgsql/extension/intagg*
%{_datadir}/pgsql/extension/intarray*
%{_datadir}/pgsql/extension/isn*
%if %{plperl}
%{_datadir}/pgsql/extension/jsonb_plperl*
%endif
%if %{plpython3}
%{_datadir}/pgsql/extension/jsonb_plpython3u*
%endif
%{_datadir}/pgsql/extension/lo*
%{_datadir}/pgsql/extension/ltree*
%{_datadir}/pgsql/extension/moddatetime*
%{_datadir}/pgsql/extension/pageinspect*
%{_datadir}/pgsql/extension/pg_buffercache*
%{_datadir}/pgsql/extension/pg_freespacemap*
%{_datadir}/pgsql/extension/pg_prewarm*
%{_datadir}/pgsql/extension/pg_stat_statements*
%{_datadir}/pgsql/extension/pg_surgery*
%{_datadir}/pgsql/extension/pg_trgm*
%{_datadir}/pgsql/extension/pg_visibility*
%{_datadir}/pgsql/extension/pg_walinspect*
%{_datadir}/pgsql/extension/pgcrypto*
%{_datadir}/pgsql/extension/pgrowlocks*
%{_datadir}/pgsql/extension/pgstattuple*
%{_datadir}/pgsql/extension/postgres_fdw*
%{_datadir}/pgsql/extension/refint*
%{_datadir}/pgsql/extension/seg*
%{_datadir}/pgsql/extension/tablefunc*
%{_datadir}/pgsql/extension/tcn*
%{_datadir}/pgsql/extension/tsm_system_rows*
%{_datadir}/pgsql/extension/tsm_system_time*
%{_datadir}/pgsql/extension/unaccent*
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/amcheck.so
%{_libdir}/pgsql/auth_delay.so
%{_libdir}/pgsql/auto_explain.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/bloom.so
%{_libdir}/pgsql/btree_gin.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/citext.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/dict_int.so
%{_libdir}/pgsql/dict_xsyn.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/file_fdw.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/hstore.so
%if %plperl
%{_libdir}/pgsql/hstore_plperl.so
%endif
%if %plpython3
%{_libdir}/pgsql/hstore_plpython3.so
%endif
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/isn.so
%if %plperl
%{_libdir}/pgsql/jsonb_plperl.so
%endif
%if %plpython3
%{_libdir}/pgsql/jsonb_plpython3.so
%endif
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%if %plpython3
%{_libdir}/pgsql/ltree_plpython3.so
%endif
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pageinspect.so
%{_libdir}/pgsql/passwordcheck.so
%{_libdir}/pgsql/pg_buffercache.so
%{_libdir}/pgsql/pg_freespacemap.so
%{_libdir}/pgsql/pg_stat_statements.so
%{_libdir}/pgsql/pg_surgery.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/pg_visibility.so
%{_libdir}/pgsql/pg_walinspect.so
%{_libdir}/pgsql/basic_archive.so
%{_libdir}/pgsql/basebackup_to_shell.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgrowlocks.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/postgres_fdw.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/tcn.so
%{_libdir}/pgsql/test_decoding.so
%{_libdir}/pgsql/tsm_system_rows.so
%{_libdir}/pgsql/tsm_system_time.so
%{_libdir}/pgsql/unaccent.so
%{_mandir}/man1/oid2name.*
%{_mandir}/man1/pg_amcheck.*
%{_mandir}/man1/pg_archivecleanup.*
%{_mandir}/man1/pg_recvlogical.*
%{_mandir}/man1/pg_test_fsync.*
%{_mandir}/man1/pg_test_timing.*
%{_mandir}/man1/pg_waldump.*
%{_mandir}/man1/pgbench.*
%{_mandir}/man1/vacuumlo.*
%{_mandir}/man3/dblink*
%if %selinux
%{_datadir}/pgsql/contrib/sepgsql.sql
%{_libdir}/pgsql/sepgsql.so
%endif
%if %ssl
%{_datadir}/pgsql/extension/sslinfo*
%{_libdir}/pgsql/sslinfo.so
%endif
%if %uuid
%{_datadir}/pgsql/extension/uuid-ossp*
%{_libdir}/pgsql/uuid-ossp.so
%endif
%if %xml
%{_datadir}/pgsql/extension/xml2*
%{_libdir}/pgsql/pgxml.so
%endif

%files -n %{pkgname}-server -f server.lst
%{_bindir}/initdb
%{_bindir}/pg_basebackup

%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_receivewal
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetwal
%{_bindir}/pg_rewind
%{_bindir}/pg_checksums
%{_bindir}/pg_verifybackup

%{_bindir}/pg_createsubscriber

%{_bindir}/postgres
%{_bindir}/postgresql-setup
%{_bindir}/postgresql-upgrade
%dir %{_datadir}/pgsql
%{_datadir}/pgsql/*.sample
%dir %{_datadir}/pgsql/contrib
%dir %{_datadir}/pgsql/extension
%{_datadir}/pgsql/extension/plpgsql*
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/snowball_create.sql
%{_datadir}/pgsql/sql_features.txt
%{_datadir}/pgsql/system_constraints.sql
%{_datadir}/pgsql/system_functions.sql
%{_datadir}/pgsql/system_views.sql
%{_datadir}/pgsql/timezonesets/
%{_datadir}/pgsql/tsearch_data/
%dir %{_datadir}/postgresql-setup
%{_datadir}/postgresql-setup/library.sh
%dir %{_libdir}/pgsql
%{_libdir}/pgsql/*_and_*.so
%{_libdir}/pgsql/dict_snowball.so
%{_libdir}/pgsql/euc2004_sjis2004.so
%{_libdir}/pgsql/libpqwalreceiver.so
%{_libdir}/pgsql/pg_prewarm.so
%{_libdir}/pgsql/pgoutput.so
%{_libdir}/pgsql/plpgsql.so
%dir %{_usr}/libexec/initscripts/legacy-actions/postgresql
%{_usr}/libexec/initscripts/legacy-actions/postgresql/*
%{_libexecdir}/postgresql-check-db-dir
%dir %{_sysconfdir}/postgresql-setup
%dir %{_sysconfdir}/postgresql-setup/upgrade
%config %{_sysconfdir}/postgresql-setup/upgrade/*.conf
%{_mandir}/man1/initdb.*
%{_mandir}/man1/pg_basebackup.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_receivewal.*
%{_mandir}/man1/pg_resetwal.*
%{_mandir}/man1/pg_rewind.*
%{_mandir}/man1/pg_checksums.*
%{_mandir}/man1/pg_verifybackup.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postgresql-new-systemd-unit.*
%{_mandir}/man1/postgresql-setup.*
%{_mandir}/man1/postgresql-upgrade.*

%{_mandir}/man1/pg_walsummary.*
%{_mandir}/man1/pg_combinebackup.*
%{_mandir}/man1/pg_createsubscriber.*

%{_sbindir}/postgresql-new-systemd-unit
%{_tmpfilesdir}/postgresql.conf
%{_tmpfilesdir}/postgresql17.conf
%{_unitdir}/*postgresql*.service
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql
%attr(644,postgres,postgres) %config(noreplace) %{?_localstatedir}/lib/pgsql/.bash_profile
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/backups
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/data
%ghost %attr(755,postgres,postgres) %dir %{_rundir}/postgresql
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%{_sysusersdir}/postgresql17.conf


%files -n %{pkgname}-server-devel -f devel.lst
%{_bindir}/pg_server_config
%dir %{_datadir}/pgsql
%{_datadir}/pgsql/errcodes.txt
%dir %{_includedir}/pgsql
%{_includedir}/pgsql/server
%{_libdir}/pgsql/pgxs/
%{_mandir}/man1/pg_server_config.*
%{_mandir}/man3/SPI_*
%{macrosdir}/macros.postgresql


%if ! %external_libpq
%files -n %{pkgname}-private-devel
%{_bindir}/pg_config
%{_includedir}/libpq-events.h
%{_includedir}/libpq-fe.h
%{_includedir}/postgres_ext.h
%{_includedir}/pgsql/internal/*.h
%{_includedir}/pgsql/internal/libpq/pqcomm.h

%{_includedir}/pgsql/internal/libpq/protocol.h

%{_includedir}/libpq/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libpq.so
%{_includedir}/pg_config*.h
%endif


%files -n %{pkgname}-test-rpm-macros
%{_datadir}/postgresql-setup/postgresql_pkg_tests.sh
%{macrosdir}/macros.postgresql-test


%files -n %{pkgname}-static
%{_libdir}/libpgcommon.a
%{_libdir}/libpgport.a
%{_libdir}/libpgcommon_shlib.a
%{_libdir}/libpgport_shlib.a


%if %upgrade
%files -n %{pkgname}-upgrade
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin/pg_config
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pgxs
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pkgconfig
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/share


%files -n %{pkgname}-upgrade-devel
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin/pg_config
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/include
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pkgconfig
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pgxs
%{macrosdir}/macros.postgresql-upgrade
%endif

%if %llvmjit
%files -n %{pkgname}-llvmjit
%defattr(-,root,root)
%{_libdir}/pgsql/bitcode/*
%{_libdir}/pgsql/llvmjit.so
%{_libdir}/pgsql/llvmjit_types.bc
%endif

%if %plperl
%files -n %{pkgname}-plperl -f plperl.lst
%{_datadir}/pgsql/extension/bool_plperl*
%{_datadir}/pgsql/extension/plperl*
%{_libdir}/pgsql/bool_plperl.so
%{_libdir}/pgsql/plperl.so
%endif


%if %pltcl
%files -n %{pkgname}-pltcl -f pltcl.lst
%{_datadir}/pgsql/extension/pltcl*
%{_libdir}/pgsql/pltcl.so
%endif


%if %plpython3
%files -n %{pkgname}-plpython3 -f plpython3.lst
%{_datadir}/pgsql/extension/plpython3*
%{_libdir}/pgsql/plpython3.so
%endif


%if %test
%files -n %{pkgname}-test
%attr(-,postgres,postgres) %{_libdir}/pgsql/test
%endif


%changelog
* Thu Aug 14 2025 Packit <hello@packit.dev> - 17.6-1
- Update to version 17.6
- Resolves: rhbz#2388579

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 17.5-6
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 17.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Filip Janus <fjanus@redhat.com> - 17.5-4
- Enable zstd support
- Enable tmpfiles.d configuration

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 17.5-3
- Perl 5.42 rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 17.5-2
- Rebuilt for Python 3.14

* Wed May 21 2025 Packit <hello@packit.dev> - 17.5-1
- Update to version 17.5
- Resolves: rhbz#2365101

* Thu Apr 03 2025 Packit <hello@packit.dev> - 17.4-1
- Update to version 17.4
- Resolves: rhbz#2326274

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 17.2-2
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Wed Jan 29 2025 Filip Janus <fjanus@redhat.com> - 17.2-1 
- Update to 17.2
- stick with std=c18

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 1 2024 Filip Janus <fjanus@redhat.com> - 17.0-1
- Initial packaging of pg17

* Mon Sep 16 2024 Filip Janus <fjanus@redhat.com> - 16.3-6
- Fix typos in provides

* Mon Aug 05 2024 Filip Janus <fjanus@redhat.com> - 16.3-5
- Add Obsoletes of versioned alternative stream from F39
- It makes the upgrade path clear

* Mon Jul 29 2024 Lumír Balhar <lbalhar@redhat.com> - 16.3-4
- Add new systemtap-sdt-dtrace to build deps

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 3 2024 Filip Janus <fjanus@redhat.com> - 16.3-2
- Disable openssl ENGINE_API
- Fedora change: https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
- BZ: 2295339

* Mon Jun 17 2024 Ales Nezbeda <anezbeda@redhat.com> - 16.3-1
- Update to 16.3
- Remove unneeded libXML and OpenSSL patches

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 16.1-9
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 16.1-8
- Rebuilt for Python 3.13

* Mon Feb 26 2024 Filip Janus <fjanus@redhat.com> - 16.1-7
- Remove /var/run/postgresql

* Tue Feb 20 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 16.1-6
- Backport OpenSSL 3.2 fix from upstream master

* Mon Feb 5 2024 Filip Janus <fjanus@redhat.com> - 16.1-5
- Add versioned provide to the default version
- Obsolete versioned is no more needed since only default stream provides
  postgresql symbol

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 16.1-4
- Rebuild for ICU 74

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 5 2024 Filip Janus <fjanus@redhat.com> - 16.1-2
- Add symbol any to ensure conflict with othere postgresql streams
- sympol postgresql is now used only for setting the default version
  of postgresql in the repository
- It was done due to dnf feature. more about it:
  https://github.com/rpm-software-management/dnf5/issues/620

* Mon Nov 27 2023 Filip Janus <fjanus@redhat.com> - 16.1-1
- Update to 16.1
- Initial import of demodularized version

* Wed Oct 25 2023 Filip Janus <fjanus@redhat.com> - 16.0-2
- Remove unused beta macro from spec
- add support for setting default PG stream using
  postgresql_default macro

* Wed Sep 20 2023 Filip Janus <fjanus@redhat.com> - 16.0-1
- Add temporary fix for failing perl test
- plperl_warning.patch
- Related: https://bugzilla.redhat.com/show_bug.cgi?id=2238686

* Fri Sep 15 2023 Filip Janus <fjanus@redhat.com> - 16.0-1
- Update to 16.0

* Mon Jun 05 2023 Filip Janus <fjanus@redhat.com> - 16.beta
- Initial build of postgresql 16
- Remove pdf documentation
- Fix linter issues (patchx -> patch x)
- Remove postmaster symbol since it was deprecated see:
	https://www.postgresql.org/docs/current/app-postmaster.html
- Provide new symbol postgresql-unit

* Mon Jan 16 2023 Filip Janus <fjanus@redhat.com> - 15.1-1
- Demodularization of package
- Remove build warnings - file listed twice

* Thu Jul 07 2022 Filip Januš <fjanus@redhat.com> - 14.3-6
- enable lz4

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 14.3-5
- Rebuilt for Python 3.11

* Mon Jun 06 2022 Honza Horak <hhorak@redhat.com> - 14.3-4
- Fix compatibility with Perl 5.36
  Resolves: #2092426

* Mon Jun 06 2022 Honza Horak <hhorak@redhat.com> - 14.3-3
- Fix handling of errors during transaction with Python 3.11
  Resolves: #2023272

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 14.3-2
- Perl 5.36 rebuild

* Tue May 31 2022 Honza Horak <hhorak@redhat.com> - 14.3-1
- Update to 14.3
  Also fixes: CVE-2022-1552

* Mon Apr 04 2022 Filip Janus <fjanus@redhat.com> - 14.2-3
- Add build requirement util-linux

* Wed Feb 23 2022 Marek Kulik <mkulik@redhat.com> - 14.2-2
- Disable package note generation due to extension build issue.

* Wed Feb 09 2022 Filip Janus <fjanus@redhat.com> - 14.2-1
- Update to 14.2

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Filip Januš <fjanus@redhat.com> - 14.1-1
- Update to 14.1
- Update postgresql-setup to v8.7
- Resolves: https://fedoraproject.org/wiki/Changes/PostgreSQL_14

* Mon Dec 13 2021 Marek Kulik <mkulik@redhat.com> - 13.5-1
- Update to 13.5
  Remove patch postgresql-pgcrypto-openssl3-init.patch - already in upstream

* Thu Nov 18 2021 Marek Kulik <mkulik@redhat.com> - 13.4-5
- Update postgresql-setup to v8.6

* Tue Oct 19 2021 Filip Januš <fjanus@redhat.com> - 13.4-4
- rebuild after llvm .so name chnage

* Wed Oct 06 2021 Filip Januš <fjanus@redhat.com> - 13.4-3
- Add patch 13 - corrects initialization of ciphers
- Add patch 14 - disable unsupported ciphers in test suite

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 13.4-2
- Rebuilt with OpenSSL 3.0.0

* Thu Aug 12 2021 Filip Januš <fjanus@rehdat.com> - 13.4-1
- Update to 13.4
- Disable postgresql-subtransaction-test.patch
  now succeeds without patch

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Filip Januš <fjanus@redhat.com> - 13.3-4
- Enable ssl and other features for upgrade server

* Fri Jun 04 2021 Honza Horak <hhorak@redhat.com> - 13.3-3
- Build with a private libpq
  Resolves: #1905584

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 13.3-2
- Rebuilt for Python 3.10

* Fri May 21 2021 Filip Januš <fjanus@redhat.com> - 13.3-1
- Update to 13.3

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 13.2-9
- Perl 5.34 rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 13.2-8
- Rebuild for ICU 69

* Tue May 11 2021 Honza Horak <hhorak@redhat.com> - 13.2-7
- Fix subtransaction test for Python 3.10
  Resolves: #1959080

* Thu Apr 22 2021 Honza Horak <hhorak@redhat.com> - 13.2-6
- Fix jit failure on s390x
  Thanks to Tom Stellard
  Related: #1940964

* Tue Apr 20 2021 Honza Horak <hhorak@redhat.com> - 13.2-5
- Add macro for llvmjit settings

* Wed Mar 17 2021 Honza Horak <hhorak@redhat.com> - 13.2-4
- Remove plpython2 entirely, same as upstream did
  Resolves: #1913681
- Disable llvmjit in order to build at all
  Related: #1940964

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 13.2-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Feb 17 2021 Honza Horak <hhorak@redhat.com> - 13.2-2
- Do not build plpython on RHEL > 8
  Related: #1913681

* Tue Feb 16 2021 Honza Horak <hhorak@redhat.com> - 13.2-1
- Update to 13.2

* Fri Feb 12 2021 Michal Schorm <mschorm@redhat.com> - 13.1-2
- Remove ancient PPC64 hack

* Wed Jan 13 2021 Honza Horak <hhorak@redhat.com> - 13.1-1
- Rebase to usptream release 13.1

* Wed Jan 13 2021 Patrik Novotný <panovotn@redhat.com> - 12.5-1
- Rebase to upstream release 12.5
  Patch for libpq 13.x build time compatibility
  Fixes CVE-2020-25694
  Fixes CVE-2020-25695
  Fixes CVE-2020-25696

* Wed Jan 06 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Honza Horak <hhorak@redhat.com> - 12.4-4
- Update postgresql-setup to v8.5

* Fri Oct 09 2020 Honza Horak <hhorak@redhat.com> - 12.4-3
- Removing problematic requirements on ppc64 arch
  Resolves: #1882642

* Fri Aug 21 2020 Jeff Law <law@redhat.com> - 12.4-2
- Re-enable LTO

* Tue Aug 18 2020 Patrik Novotný <panovotn@redhat.com> - 12.4-1
- Rebase to upstream release 12.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 12.3-5
- Disable LTO

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 12.3-4
- Perl 5.32 rebuild

* Sat Jun 06 2020 Pavel Raiskup <praiskup@redhat.com> - 12.3-3
- add docbook-style-xsl to BuildRequires

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 12.3-2
- Rebuilt for Python 3.9

* Tue May 19 2020 Patrik Novotný <panovotn@redhat.com> - 12.3-2
- Drop postgresql-man.patch

* Mon May 18 2020 Patrik Novotný <panovotn@redhat.com> - 12.3-1
- Rebase to upstream release 12.3

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 12.2-3
- Rebuild for ICU 67

* Thu Mar 12 2020 Patrik Novotný <panovotn@redhat.com> - 12.2-2
- Fix requirements for JIT in postgresql-server-devel
- Fix build issues regarding new perl update

* Fri Feb 14 2020 Patrik Novotný <panovotn@redhat.com> - 12.2-1
- Rebase to upstream release 12.2

* Tue Feb 11 2020 Patrik Novotný <panovotn@redhat.com> - 12.1-1
- Rebase to upstream release 12.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Patrik Novotný <panovotn@redhat.com> - 11.6-1
- Rebase to upstream version 11.6

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 11.5-6
- Rebuild for ICU 65

* Thu Sep 05 2019 Patrik Novotný <panovotn@redhat.com> - 11.5-5
- postgresql-server-devel requires krb5-devel

* Tue Sep 03 2019 Patrik Novotný <panovotn@redhat.com> - 11.5-4
- Add explicit obsoletes to plpython2 package

* Mon Sep 02 2019 Patrik Novotný <panovotn@redhat.com> - 11.5-3
- Rename plpython to plpython2 and provide plpython virtually.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 11.5-2
- Rebuilt for Python 3.8

* Wed Aug 07 2019 Petr Kubat <pkubat@redhat.com> - 11.5-1
- New upstream version 11.5
  https://www.postgresql.org/docs/11/release-11-5.html

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Petr Kubat <pkubat@redhat.com> - 11.4-1
- New upstream version 11.4
  https://www.postgresql.org/docs/11/release-11-4.html

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 11.3-2
- Perl 5.30 rebuild

* Thu May 09 2019 Patrik Novotný <panovotn@redhat.com> - 11.3-1
- Rebase to upstream release 11.3
  https://www.postgresql.org/docs/11/release-11-3.html

* Tue Mar 05 2019 Pavel Raiskup <praiskup@redhat.com> - 11.2-3
- update postgresql-setup to 8.4 (related to rhbz#1668301)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.2-2
- Rebuild for readline 8.0

* Thu Feb 14 2019 Patrik Novotný <panovotn@redhat.com> - 11.2-1
- Rebase to upstream release 11.2

* Thu Feb 14 2019 Pavel Raiskup <praiskup@redhat.com> - 11.1-5
- protect against building server against older libpq library

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Pavel Raiskup <praiskup@redhat.com> - 11.1-3
- build with ICU support, to provide more opt-in collations

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 11.1-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Nov 07 2018 Patrik Novotný <panovotn@redhat.com> - 11.1-1
- Rebase to upstream release 11.1
  https://www.postgresql.org/docs/11/release-11-1.html

* Fri Oct 26 2018 Pavel Raiskup <praiskup@redhat.com> - 11.0-2
- build also contrib *plpython3 modules

* Tue Oct 16 2018 Pavel Raiskup <praiskup@redhat.com> - 11.0-1
- new upstream release, per release notes:
  https://www.postgresql.org/docs/11/static/release-11.html

* Wed Sep 05 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-4
- build without postgresql-libs; libraries moved to libpq and libecpg

* Mon Aug 27 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-3
- devel subpackage provides postgresql-server-devel and libecpg-devel
  (first step for rhbz#1618698)

* Mon Aug 27 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-2
- packaging cleanup
- devel subpackage to provide libpq-devel (first step for rhbz#1618698)

* Wed Aug 08 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-1
- update to 10.5 per release notes:
  https://www.postgresql.org/docs/10/static/release-10-5.html

* Thu Aug 02 2018 Pavel Raiskup <praiskup@redhat.com> - 10.4-8
- new postgresql-setup, the %%postgresql_tests* macros now start
  the build-time server on random port number

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Pavel Raiskup <praiskup@redhat.com> - 10.4-6
- drop ppc64 patch, gcc is already fixed (rhbz#1544349)
- move pg_config*.mo files into devel subpackage

* Mon Jul 09 2018 Pavel Raiskup <praiskup@redhat.com> - 10.4-5
- re-enable -O3 for 64bit PPC boxes
- explicitly set PYTHON=python2, /bin/python doesn't exist fc29+

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 10.4-4
- Perl 5.28 rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 10.4-3
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 10.4-2
- Rebuilt for Python 3.7

* Wed May 09 2018 Pavel Raiskup <praiskup@redhat.com> - 10.4-1
- update to 10.4 per release notes:
  https://www.postgresql.org/docs/10/static/release-10-4.html

* Thu Apr 26 2018 Pavel Raiskup <praiskup@redhat.com> - 10.3-5
- pltcl: drop tcl-pltcl dependency (rhbz#1571181)

* Thu Apr 19 2018 Pavel Raiskup <praiskup@redhat.com> - 10.3-4
- upgrade: package plpython*.so modules

* Mon Apr 16 2018 Pavel Raiskup <praiskup@redhat.com> - 10.3-3
- upgrade: package plperl.so and pltcl.so
- upgrade: package contrib modules
- upgrade: drop dynamic libraries

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 10.3-2
- define %%precise_version helper macro
- drop explicit libpq.so provide from *-libs
- update postgresql-setup tarball
- add postgresql-test-rpm-macros package

* Thu Mar 01 2018 Pavel Raiskup <praiskup@redhat.com> - 10.3-1
- update to 10.3 per release notes:
  https://www.postgresql.org/docs/10/static/release-10-3.html

* Thu Feb 08 2018 Petr Kubat <pkubat@redhat.com> - 10.2-1
- update to 10.2 per release notes:
  https://www.postgresql.org/docs/10/static/release-10-2.html

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 10.1-5
- Rebuilt for switch to libxcrypt

* Tue Dec 19 2017 Pavel Raiskup <praiskup@redhat.com> - 10.1-4
- configure with --with-systemd (rhbz#1414314)
- disable startup timeout of PostgreSQL service (rhbz#1525477)

* Wed Dec 13 2017 Pavel Raiskup <praiskup@redhat.com> - 10.1-3
- unify %%configure options for python2/python3 configure
- drop --with-krb5 option, not supported since PostgreSQL 9.4
- python packaging - requires/provides s/python/python2/

* Tue Nov 14 2017 Pavel Raiskup <praiskup@redhat.com> - 10.1-2
- postgresql-setup v7.0

* Wed Nov 08 2017 Pavel Raiskup <praiskup@redhat.com> - 10.1-1
- update to 10.1 per release notes:
  https://www.postgresql.org/docs/10/static/release-10-1.html

* Mon Nov 06 2017 Pavel Raiskup <praiskup@redhat.com> - 10.0-4
- rebase to new postgresql-setup 6.0 version, to fix CVE-2017-15097

* Thu Oct 12 2017 Pavel Raiskup <praiskup@redhat.com> - 10.0-3
- confess that we bundle setup scripts and previous version of ourseleves
- provide %%postgresql_upgrade_prefix macro

* Mon Oct 09 2017 Pavel Raiskup <praiskup@redhat.com> - 10.0-2
- stricter separation of files in upgrade/upgrade-devel

* Mon Oct 09 2017 Jozef Mlich <jmlich@redhat.com> - 10.0-2
- support for upgrade with extenstions
  i.e the postgresql-upgrade-devel subpackage was added (rhbz#1475177)

* Fri Oct 06 2017 Pavel Raiskup <praiskup@redhat.com> - 10.0-1
- update to 10.0 per release notes:
  https://www.postgresql.org/docs/10/static/release-10.html

* Tue Sep 05 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.5-2
- move %%_libdir/pgsql into *-libs subpackage

* Tue Aug 29 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.5-1
- update to 9.6.5 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6-5.html

* Tue Aug 08 2017 Petr Kubat <pkubat@redhat.com> - 9.6.4-1
- update to 9.6.4 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6-4.html

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.3-7
- drop perl rpath patch; libperl.so* is now in %%_libdir (rhbz#1474417)

* Mon Jun 26 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.3-6
- don't provide libpqwalreceiver.so() soname

* Wed Jun 21 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.3-5
- drop the __os_install_post redefinition hack

* Mon Jun 12 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.3-4
- drop -DLINUX_OOM_SCORE_ADJ=0 define from CFLAGS (rhbz#1110969, rhbz#1436554)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 9.6.3-3
- Perl 5.26 rebuild

* Mon May 22 2017 Petr Kubat <pkubat@redhat.com> - 9.6.3-2
- fix indentation issues in hstore_plperlu test-case (rhbz#1453111)

* Thu May 11 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.3-1
- update to 9.6.3 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6-3.html

* Mon Apr 24 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.2-4
- rebase to postgresql-setup 5.1

* Mon Apr 10 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.2-3
- spring cleanup

* Mon Mar 27 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.2-2
- rebuild for rhbz#1436006

* Wed Feb 22 2017 Pavel Raiskup <praiskup@redhat.com> - 9.6.2-1
- update to 9.6.2 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6-2.html
- remove mistakenly isntalled libpgfeutils.a

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 9.6.1-3
- Rebuild for readline 7.x

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 9.6.1-2
- Rebuild for Python 3.6

* Wed Oct 26 2016 Pavel Raiskup <praiskup@redhat.com> - 9.6.1-1
- update to 9.6.1 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6-1.html
- add gen_sources.sh script
- remove plpython build hack, fixed upstream
- remove aarch64 and ppc64p7 hacks, fixed by the %%configure call

* Tue Oct 04 2016 Pavel Raiskup <praiskup@redhat.com> - 9.6.0-1
- rebase the postgresql-setup tarball

* Fri Sep 30 2016 Pavel Raiskup <praiskup@redhat.com> - 9.6.0-1
- update to 9.6.0 per release notes:
  https://www.postgresql.org/docs/9.6/static/release-9-6.html

* Fri Aug 12 2016 Petr Kubat <pkubat@redhat.com> - 9.5.4-1
- update to 9.5.4 per release notes:
  http://www.postgresql.org/docs/9.5/static/release-9-5-4.html

* Mon Jun 20 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.3-3
- use multilib-rpm-config package for multilib hacks

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 9.5.3-2
- Perl 5.24 rebuild

* Thu May 12 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.3-1
- update to 9.5.3 per release notes:
  http://www.postgresql.org/docs/9.5/static/release-9-5-3.html

* Mon May 09 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.2-2
- fix the test subpackage, pg_regress now uses --bindir

* Sun Apr 03 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.2-1
- update to 9.5.2 per release notes
  http://www.postgresql.org/docs/9.5/static/release-9-5-2.html

* Fri Feb 26 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.1-2
- package static libraries without dynamic counterparts (rhbz#784281)

* Tue Feb 09 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.1-1
- update to 9.5.1 per release notes
  http://www.postgresql.org/docs/9.5/static/release-9-5-1.html

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Pavel Raiskup <praiskup@redhat.com> - 9.5.0-1
- update to 9.5.0 per release notes
  http://www.postgresql.org/docs/9.5/static/release-9-5.html
- update postgresql-setup to v4.0 to reflect new packaging style

* Wed Dec 16 2015 Pavel Kajaba <pkajaba@redhat.com> - 9.4.5-5
- fixed problem with xml2 test (rhbz#1286692)

* Thu Dec 3 2015 Pavel Kajaba <pkajaba@redhat.com> - 9.4.5-4
- fixed short-circuit build

* Thu Nov 12 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.5-3
- fix testsuite failure with new Python 3.5 (rhbz#1280404)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.5-2
- devel package should not require the main package (rhbz#1272219)
- multilib fix, more general solution (rhbz#1190346)

* Tue Oct 06 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.5-1
- update to 9.4.5 per release notes
  http://www.postgresql.org/docs/9.4/static/release-9-4-5.html

* Fri Sep 25 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-6
- postgresql-setup rebase to 3.4 (rhbz#1265319, rhbz#1247477)

* Thu Sep 17 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-5
- enable hardening (safe for kernel 4.1+) (see rhbz#952946 comment #24)

* Tue Aug 04 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-4
- install README.rpm-dist properly (rhbz#1249708)

* Tue Jul 14 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-3
- revert/fix part of e6acde1a9 commit related to multilib hack (rhbz#1242873)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-1
- fix for Perl 5.22 rebase (rhbz#1231279)

* Thu Jun 11 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.4-1
- update to 9.4.4 per release notes
  http://www.postgresql.org/docs/9.4/static/release-9-4-4.html

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 9.4.3-2
- Perl 5.22 rebuild

* Wed Jun 03 2015 Jozef Mlich <jmlich@redhat.com> - 9.4.3-1
- update to 9.4.3 per release notes
  http://www.postgresql.org/docs/9.4/static/release-9-4-3.html

* Thu May 21 2015 Jozef Mlich <jmlich@redhat.com> - 9.4.2-1
- update to 9.4.2 per release notes
  http://www.postgresql.org/docs/9.4/static/release-9-4-2.html

* Thu May 21 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.1-4
- make the %%check phase more verbose for FAIL cases
- don't FTBFS on f23+ where hardening is on by default

* Wed Mar 25 2015 Jozef Mlich <jmlich@redhat.com> - 9.4.1-3
- update to postgresql-setup 3.3

* Thu Mar 19 2015 Jozef Mlich <jmlich@redhat.com> - 9.4.1-2
- Adding tcl-pgtcl into Requires of -tcl subpackage

* Wed Feb 04 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.1-1
- update to 9.4.1 per release notes
  http://www.postgresql.org/docs/9.4/static/release-9-4-1.html

* Tue Feb 03 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.0-2
- sort file lists alphabetically

* Tue Dec 23 2014 Jozef Mlich <jmlich@redhat.com> - 9.4.0-1
- update to 9.4.0 per release notes
  http://www.postgresql.org/docs/9.4/static/index.html

* Mon Nov 24 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-8
- print regression.diffs contents to stdout (#1118392)

* Mon Oct 20 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-7
- be forgiving of variant spellings of locale names in pg_upgrade (#1007802)

* Sun Sep 21 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-6
- postgresql-setup & relatives are now in separate tarball

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 9.3.5-5
- Perl 5.20 rebuild

* Thu Aug 21 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-4
- install macros.postgresql, not postgresql.macros

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-2
- fix the prevversion sum link and comment a little

* Tue Jul 22 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.5-1
- update to 9.3.5 per release notes
  http://www.postgresql.org/docs/9.3/static/release-9-3-5.html

* Fri Jul 18 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.4-8
- provide postgresql-doc for postgresql-docs package (#1086420)
- move html documentation to *-docs subpackage (#1086420)
- provide postgresql-server(:MODULE_COMPAT_%%{postgresql_major}) to guard
  against incompatible plugin installation (#1008939)

* Thu Jun 19 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.4-7
- OOM handling compatible with 9.5+, by Tom Lane (#1110969)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Honza Horak <hhorak@redhat.com> - 9.3.4-5
- Rebuild for Python 3.4

* Fri May 23 2014 Honza Horak <hhorak@redhat.com> - 9.3.4-4
- Change plpython_do test a bit so it is universal for all python versions

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 9.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed May 14 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.4-2
- set basic $PATH when it is empty or unset, (#1097317)

* Thu Mar 20 2014 Jozef Mlich <jmlich@redhat.com> - 9.3.4-1
- update to 9.3.4 minor version per release notes:
  http://www.postgresql.org/docs/9.3/static/release-9-3-4.html

* Thu Mar 13 2014 Jozef Mlich <jmlich@redhat.com> - 9.3.3-2
- Fix WAL replay of locking an updated tuple
  kudos to Alvaro Herrera

* Thu Feb 20 2014 Jozef Mlich <jmlich@redhat.com> - 9.3.3-1
- update to 9.3.3 minor version per release notes:
  http://www.postgresql.org/docs/9.3/static/release-9-3-3.html

* Thu Jan 23 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-7
- postgresql-setup: typos

* Tue Jan 21 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-6
- add PGSETUP_PGUPGRADE_OPTIONS env var for postgresql-setup

* Mon Jan 20 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-5
- fix the postgresql-setup --version option

* Mon Jan 20 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-4
- postgresql-setup(upgrade): don't stop old server when it can not be started
- postgresql-setup(initdb, upgrade): add $PGSETUP_INITDB_OPTIONS
- postgresql-setup: do not pretend 'sh' compatibility
- move script generation to proper place
- postgresql-setup: document a little and genrate manual page

* Fri Jan 10 2014 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-3
- build with -O3 on ppc64 (private #1051075)

* Fri Dec 13 2013 Pavel Raiskup <praiskup@redhat.com> - 9.3.2-2
- lint the postgresql-setup script

* Thu Dec 12 2013 Jozef Mlich <jmlich@redhat.com> - 9.3.2-2
- don't fail if user has badly configure 'postgres' user access (#1040364)

* Thu Dec 05 2013 Jozef Mlich <jmlich@redhat.com> - 9.3.2-1
- update to 9.3.2 minor version per release notes:
  http://www.postgresql.org/docs/9.3/static/release-9-3-2.html

* Thu Oct 17 2013 Jozef Mlich <jmlich@redhat.com> - 9.3.1-2
- the prevversion (see package upgrade process) is updated
  from 9.2.4 to 9.2.5

* Thu Oct 10 2013 Jozef Mlich <jmlich@redhat.com> - 9.3.1-1
- update to 9.3.1 minor version per release notes:
  http://www.postgresql.org/docs/9.3/static/release-9-3-1.html

* Tue Sep 10 2013 Pavel Raiskup <praiskup@redhat.com> - 9.3.0-1
- update to 9.3 major version per release notes:
  http://www.postgresql.org/docs/9.3/static/release-9-3.html

* Thu Aug 15 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-11
- upgrade: stop old server in case of permissions problem (#896161)

* Mon Aug 12 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-10
- disable aggressive loop optimizations for old codebase (#993532)

* Wed Aug 07 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-9
- generate links docdir links in postgresql-check-db-dir correctly (#994048)

* Tue Aug 06 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-8
- allow `rpmbuild -bi --short-circuit`

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-6
- split aarch64 patch to allow build without postgresql-upgrade

* Tue Jul 23 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-5
- fix testsuite to allow build against Perl 5.18

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 9.2.4-5
- Perl 5.18 rebuild

* Tue Jul 09 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-4
- do not use -b for manual page fixes

* Thu Jun 20 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-3
- fix README.rpm-dist for the bug (#969050)
- replace hard-wired path with %%{_datadir}

* Thu Jun 13 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-3
- add atomic operations support for aarch64 to preupgrade version also (#970661)
- apply the forgotten man-page-day patch (#948933)

* Thu Jun 13 2013 Jan Stanek <jstanek@redhat.com> - 9.2.4-3
- added patch for manual pages (#948933)

* Tue Jun 11 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-2
- postgresql-setup: don't create whole path to server's data to make sure that
  the parent directory has correct permissions (#972425)

* Wed Jun 05 2013 Pavel Raiskup <praiskup@redhat.com> - 9.2.4-2
- fix rpmlint warnings
- fix aarch64 build by defining missing atomic operations (#970661)

* Thu Apr  4 2013 Tom Lane <tgl@redhat.com> 9.2.4-1
- Update to PostgreSQL 9.2.4, for various fixes described at
  http://www.postgresql.org/docs/9.2/static/release-9-2-4.html
  including the fixes for CVE-2013-1899, CVE-2013-1900, CVE-2013-1901
Resolves: #929223, #929255, #929328
- fix build for aarch64 and ppc64p7

* Thu Feb  7 2013 Tom Lane <tgl@redhat.com> 9.2.3-1
- Update to PostgreSQL 9.2.3, for various fixes described at
  http://www.postgresql.org/docs/9.2/static/release-9-2-3.html
  including the fix for CVE-2013-0255
Resolves: #908722
- Make the package build with selinux option disabled
Resolves: #894367
- Include old version of pg_controldata in postgresql-upgrade subpackage
Related: #896161

* Thu Jan  3 2013 Tom Lane <tgl@redhat.com> 9.2.2-3
- Prevent creation of TCP socket during pg_upgrade regression test, so that
  concurrent RPM builds on the same machine won't fail
Resolves: #891531
- Make sure $PGDATA/pg_log/ gets the right SELinux label in postgresql-setup
Resolves: #891547

* Wed Dec 19 2012 Tom Lane <tgl@redhat.com> 9.2.2-2
- Make building of plpython3 dependent on Fedora version, per guidelines
Resolves: #888419

* Thu Dec  6 2012 Tom Lane <tgl@redhat.com> 9.2.2-1
- Update to PostgreSQL 9.2.2, for various fixes described at
  http://www.postgresql.org/docs/9.2/static/release-9-2-2.html
- Use new systemd install/uninstall trigger macros conditionally,
  so that package can still be installed on pre-F18 branches

* Mon Sep 24 2012 Tom Lane <tgl@redhat.com> 9.2.1-1
- Update to PostgreSQL 9.2.1, for various fixes described at
  http://www.postgresql.org/docs/9.2/static/release-9-2-1.html
  including a nasty data-loss bug
- Adopt new systemd macros for server package install/uninstall triggers
Resolves: #850277

* Mon Sep 10 2012 Tom Lane <tgl@redhat.com> 9.2.0-1
- Update to PostgreSQL 9.2.0 (major version bump);
  in-place upgrade support now works from 9.1.x as the previous version
- Add postgresql-plpython3 subpackage with PL/Python built against Python 3

* Tue Aug 28 2012 Tom Lane <tgl@redhat.com> 9.1.5-2
- Remove unnecessary ldconfig calls in pre/post triggers
Resolves: #849344

* Fri Aug 17 2012 Tom Lane <tgl@redhat.com> 9.1.5-1
- Update to PostgreSQL 9.1.5, for various fixes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-5.html
  including the fixes for CVE-2012-3488, CVE-2012-3489

* Mon Aug 13 2012 Tom Lane <tgl@redhat.com> 9.1.4-5
- Back-port upstream support for postmaster listening on multiple Unix sockets
- Configure postmaster to create sockets in both /var/run/postgresql and /tmp;
  the former is now the default place for libpq to contact the postmaster.
Resolves: #825448
- Annotate postgresql.conf about not setting port number there
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Tom Lane <tgl@redhat.com> 9.1.4-3
- Update code to use oom_score_adj not oom_adj, thereby suppressing
  whining in the kernel log
- Add "legacy action" scripts to support "service postgresql initdb" and
  "service postgresql upgrade" in a now-approved fashion (requires a
  recent version of initscripts to work)
Resolves: #800416

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 9.1.4-2
- Perl 5.16 rebuild

* Mon Jun  4 2012 Tom Lane <tgl@redhat.com> 9.1.4-1
- Update to PostgreSQL 9.1.4, for various fixes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-4.html
  including the fixes for CVE-2012-2143, CVE-2012-2655
Resolves: #826606
- Update previous version (embedded in postgresql-upgrade) to 9.0.8
  because fix in whole-row variable dumping could be needed for upgrades
- Revert fix for bug #800416, per fedora-packaging discussion at
  http://lists.fedoraproject.org/pipermail/packaging/2012-April/008314.html
  "service postgresql initdb" is dead and will stay that way

* Sat Mar 17 2012 Tom Lane <tgl@redhat.com> 9.1.3-3
- Fix postgresql-setup to rely on systemd to parse the unit file, instead
  of using ad-hoc code
Resolves: #804290

* Tue Mar 13 2012 Tom Lane <tgl@redhat.com> 9.1.3-2
- Fix postgresql-setup to look for unit file in /usr/lib and to ignore
  comments therein
Resolves: #802835
- Resurrect a now-mostly-dummy postgresql init script, so that people can
  keep on using "service postgresql initdb" if they wish
Resolves: #800416

* Mon Feb 27 2012 Tom Lane <tgl@redhat.com> 9.1.3-1
- Update to PostgreSQL 9.1.3, for various fixes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-3.html
  including the fixes for CVE-2012-0866, CVE-2012-0867, CVE-2012-0868
Resolves: #797918

* Mon Jan  9 2012 Tom Lane <tgl@redhat.com> 9.1.2-2
- Make systemd unit file more user-friendly by resurrecting the old init
  script's checks for data directory presence and version match
Resolves: #771496

* Mon Dec  5 2011 Tom Lane <tgl@redhat.com> 9.1.2-1
- Update to PostgreSQL 9.1.2, for various fixes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-2.html

* Wed Nov 02 2011 Honza Horak <hhorak@redhat.com> 9.1.1-2
- Create a symlink of pg_regress instead of full copy;
  Don't strip symbols from regress libs
Related: #729012

* Mon Sep 26 2011 Tom Lane <tgl@redhat.com> 9.1.1-1
- Update to PostgreSQL 9.1.1, for various fixes described at
  http://www.postgresql.org/docs/9.1/static/release-9-1-1.html
- Enable build (but not test) of contrib/sepgsql
- Clean up specfile build options so that turning options off works again

* Mon Sep 12 2011 Tom Lane <tgl@redhat.com> 9.1.0-1
- Update to PostgreSQL 9.1.0 (major version bump);
  in-place upgrade support now works from 9.0.x as the previous version

* Wed Jul 27 2011 Tom Lane <tgl@redhat.com> 9.0.4-8
- Convert to systemd startup support
Resolves: #696427

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 9.0.4-7
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 9.0.4-6
- Perl mass rebuild

* Wed Jul  6 2011 Tom Lane <tgl@redhat.com> 9.0.4-5
- Remove erroneously-included Default-Start line from LSB init block
Related: #717024

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 9.0.4-4
- Perl mass rebuild
- incorporate upstream patch to make it build with Perl 5.14

* Fri Jun 10 2011 Tom Lane <tgl@redhat.com> 9.0.4-3
- Work around gcc 4.6.0 bug (temporary backport from next upstream release)

* Tue May 10 2011 Tom Lane <tgl@redhat.com> 9.0.4-2
- Add LSB init block to initscript, to ensure sane ordering at system boot
Resolves: #703215

* Mon Apr 18 2011 Tom Lane <tgl@redhat.com> 9.0.4-1
- Update to PostgreSQL 9.0.4, for various fixes described at
  http://www.postgresql.org/docs/9.0/static/release-9-0-4.html
- Add %%{?_isa} to cross-subpackage Requires, per latest packaging guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Tom Lane <tgl@redhat.com> 9.0.3-2
- Remove filter-requires-perl-Pg.sh, which doesn't seem to be needed now that
  PyGreSQL has been split out; and our use of it isn't compatible with rpm 4.9
  anyway

* Tue Feb  1 2011 Tom Lane <tgl@redhat.com> 9.0.3-1
- Update to PostgreSQL 9.0.3, for various fixes described at
  http://www.postgresql.org/docs/9.0/static/release-9-0-3.html
  including the fix for CVE-2010-4015
Resolves: #674296

* Tue Dec 28 2010 Tom Lane <tgl@redhat.com> 9.0.2-1
- Update to PostgreSQL 9.0.2 (major version bump)
- Create infrastructure for in-place database upgrade using pg_upgrade
Resolves: #398221

* Thu Dec 16 2010 Tom Lane <tgl@redhat.com> 8.4.6-1
- Update to PostgreSQL 8.4.6, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-6.html
- Ensure we don't package any .gitignore files from the source tarball
Related: #642210

* Tue Oct  5 2010 Tom Lane <tgl@redhat.com> 8.4.5-1
- Update to PostgreSQL 8.4.5, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-5.html
  including the fix for CVE-2010-3433
Related: #639371
- Add -p "$pidfile" to initscript's status call to improve corner cases.
Related: #561010

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 8.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild
- Duplicate COPYRIGHT in -libs subpackage, per revised packaging guidelines

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 8.4.4-2
- Mass rebuild with perl-5.12.0

* Mon May 17 2010 Tom Lane <tgl@redhat.com> 8.4.4-1
- Update to PostgreSQL 8.4.4, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-4.html
  including fixes for CVE-2010-1169 and CVE-2010-1170
Resolves: #593032

* Sun Mar 14 2010 Tom Lane <tgl@redhat.com> 8.4.3-1
- Update to PostgreSQL 8.4.3, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-3.html

* Mon Feb 22 2010 Tom Lane <tgl@redhat.com> 8.4.2-8
- Bring init script into some modicum of compliance with Fedora/LSB standards
Resolves: #201043

* Thu Feb 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> 8.4.2-7
- adjust license tag to reflect OSI decision

* Tue Jan 26 2010 Tom Lane <tgl@redhat.com> 8.4.2-6
- Emit explicit error message if user tries to build RPM as root
Related: #558921

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 8.4.2-5
- Latest version of systemtap needs the probes.o file to be built again
Resolves: #557266
- Provide script and instructions for building the documentation PDF

* Mon Jan 11 2010 Tom Lane <tgl@redhat.com> 8.4.2-4
- Arrange for the postmaster, but not any of its child processes, to be run
  with oom_adj -17.  This compensates for the OOM killer not being smart about
  accounting for shared memory usage.

* Sat Jan  9 2010 Tom Lane <tgl@redhat.com> 8.4.2-3
- Remove the postgresql-python and postgresql-tcl subpackages.  These files
  are now broken out as their own packages (PyGreSQL and tcl-pgtcl,
  respectively), to reflect the now longstanding split of upstream projects.
Related: #452306, #452321

* Tue Jan  5 2010 Tom Lane <tgl@redhat.com> 8.4.2-2
- Remove static libraries (.a files) from package, per packaging guidelines
- Change %%define to %%global, per packaging guidelines

* Wed Dec 16 2009 Tom Lane <tgl@redhat.com> 8.4.2-1
- Update to PostgreSQL 8.4.2, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-2.html
  including two security issues
Related: #546321
Related: #547662
- Use -N not the obsolete -n in useradd call
Resolves: #495727
- Clean up specfile to eliminate rpmlint gripes, mainly by removing
  no-longer-needed provisions for superseding rh-postgresql

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 8.4.1-5
- rebuild against perl 5.10.1

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 8.4.1-4
- add sparc/sparc64 to multilib header support

* Mon Sep 21 2009 Tom Lane <tgl@redhat.com> 8.4.1-3
- Ensure pgstartup.log gets the right ownership/permissions during initdb
Resolves: #498959

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 8.4.1-2
- Use password-auth common PAM configuration instead of system-auth

* Wed Sep  9 2009 Tom Lane <tgl@redhat.com> 8.4.1-1
- Update to PostgreSQL 8.4.1, for various fixes described at
  http://www.postgresql.org/docs/8.4/static/release-8-4-1.html
  including two security issues
Related: #522085
Related: #522092

* Tue Sep 01 2009 Karsten Hopp <karsten@redhat.com> 8.4.0-3.2
- bump release and build again with the correct libssl

* Tue Sep 01 2009 Karsten Hopp <karsten@redhat.com> 8.4.0-3.1
- disable dtrace on s390x as a workaround until #520469 has been fixed

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 8.4.0-3
- rebuilt with new openssl

* Thu Aug 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> 8.4.0-2
- update License tag to MIT (PostgreSQL calls it "BSD", but it is MIT)
- Note: This changes nothing from a license compatibility perspective.

* Mon Aug 17 2009 Tom Lane <tgl@redhat.com> 8.4.0-1
- Update to PostgreSQL 8.4.0.  See release notes at
  http://www.postgresql.org/docs/8.4/static/release-8-4.html

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 21 2009 Tom Lane <tgl@redhat.com> 8.3.7-1
- Update to PostgreSQL 8.3.7, for various fixes described at
  http://www.postgresql.org/docs/8.3/static/release-8-3-7.html
  notably the fix for CVE-2009-0922

* Tue Mar 10 2009 Tom Lane <tgl@redhat.com> 8.3.6-4
- Prevent dependent packages from needing to include sys/sdt.h
  (unintended side effect of previous patch)
- Use -O1 on alpha, per report from Oliver Falk; -O2 tickles gcc bugs

* Sun Mar  8 2009 Tom Lane <tgl@redhat.com> 8.3.6-3
- Enable tracing via systemtap
Resolves: #488941

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Tom Lane <tgl@redhat.com> 8.3.6-1
- Update to PostgreSQL 8.3.6, for various fixes described at
  http://www.postgresql.org/docs/8.3/static/release-8-3-6.html

* Wed Jan 21 2009 Dennis Gilmore <dennis@ausil.us> 8.3.5-4
- use -O1 on sparc64

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 8.3.5-3
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 8.3.5-2
- Rebuild for Python 2.6

* Sun Nov  2 2008 Tom Lane <tgl@redhat.com> 8.3.5-1
- Update to PostgreSQL 8.3.5.
- Improve display from init script's initdb action, per Michael Schwendt

* Thu Sep 25 2008 Tom Lane <tgl@redhat.com> 8.3.4-1
- Update to PostgreSQL 8.3.4.

* Mon Jul 28 2008 Tom Lane <tgl@redhat.com> 8.3.3-3
- Fix build failure caused by new default patch fuzz = 0 policy in rawhide.

* Fri Jun 20 2008 Tom Lane <tgl@redhat.com> 8.3.3-2
- Install Pgtcl in /usr/lib/tcl$TCL_VERSION, not directly in /usr/lib.
  Needed because tcl 8.5 no longer puts /usr/lib into its package search path.
  NOTE: do not back-port this change into branches using pre-8.5 tcl, because
  /usr/lib/tcl8.4 had been a symlink to /usr/share/tcl8.4, and /usr/share
  is exactly where we must not put Pgtcl.
Resolves: #228263

* Wed Jun 11 2008 Tom Lane <tgl@redhat.com> 8.3.3-1
- Update to PostgreSQL 8.3.3.
- Remove postgresql-prefer-ncurses.patch, no longer needed in recent
  Fedora releases because libtermcap is gone.

* Sat May 17 2008 Tom Lane <tgl@redhat.com> 8.3.1-5
- rebuild because of buildsystem hiccup

* Sat May 17 2008 Tom Lane <tgl@redhat.com> 8.3.1-4
- Enable LDAP support
Resolves: #445315
- Use -Wl,--as-needed to suppress bogus dependencies for libraries that
  are really only needed by some of the subpackages

* Mon Apr 28 2008 Tom Lane <tgl@redhat.com> 8.3.1-3
- Fix build breakage on PPC due to incorrect configure test
Related: #444317

* Sat Apr 26 2008 Tom Lane <tgl@redhat.com> 8.3.1-2
- Clean up cross-subpackage Requires: to ensure that updating any one
  subpackage brings in the matching versions of others.
Resolves: #444271

* Tue Mar 25 2008 Tom Lane <tgl@redhat.com> 8.3.1-1
- Update to PostgreSQL 8.3.1.

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 8.3.0-3
- add Requires for versioned perl (libperl.so)

* Wed Feb  6 2008 Tom Lane <tgl@redhat.com> 8.3.0-2
- Enable the new GSSAPI support in 8.3.0.

* Mon Feb  4 2008 Tom Lane <tgl@redhat.com> 8.3.0-1
- Update to PostgreSQL 8.3.0.

* Fri Jan 18 2008 Tom Lane <tgl@redhat.com> 8.3RC2-1
- Update to PostgreSQL 8.3RC2 (not waiting for 8.3.0 because Fedora 9 alpha
  should be 8.3-based not 8.2-based).
- Update to pgtcl 1.6.2

* Mon Jan  7 2008 Tom Lane <tgl@redhat.com> 8.2.6-1
- Update to PostgreSQL 8.2.6 to fix CVE-2007-4769, CVE-2007-4772,
  CVE-2007-6067, CVE-2007-6600, CVE-2007-6601
- Make initscript and pam config files be installed unconditionally;
  seems new buildroots don't necessarily have those directories in place

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 8.2.5-2
- Rebuild for new openssl

* Thu Sep 20 2007 Tom Lane <tgl@redhat.com> 8.2.5-1
- Update to PostgreSQL 8.2.5 and pgtcl 1.6.0

* Tue Sep  4 2007 Tom Lane <tgl@redhat.com> 8.2.4-6
- Fix multilib problem for /usr/include/ecpg_config.h (which is new in 8.2.x)

* Sat Aug 25 2007 Tom Lane <tgl@redhat.com> 8.2.4-5
- Use nicer solution for tzdata file substitution: upstream discussion
  concluded that hardwiring the path was better than a symlink after all.

* Wed Aug 22 2007 Tom Lane <tgl@redhat.com> 8.2.4-4
- Use tzdata package's data files instead of private copy, so that
  postgresql-server need not be turned for routine timezone updates
- Don't remove postgres user/group during RPM uninstall, per Fedora
  packaging guidelines
- Seems we need an explicit BuildRequires on gawk now
- Rebuild to fix Fedora toolchain issues

* Sun Aug 12 2007 Tom Lane <tgl@redhat.com> 8.2.4-3
- Recent perl changes in rawhide mean we need a more specific BuildRequires

* Wed Jun 20 2007 Tom Lane <tgl@redhat.com> 8.2.4-2
- Fix oversight in postgresql-test makefile: pg_regress isn't a shell script
  anymore.  Per upstream bug 3398.

* Tue Apr 24 2007 Tom Lane <tgl@redhat.com> 8.2.4-1
- Update to PostgreSQL 8.2.4 for CVE-2007-2138, data loss bugs
Resolves: #237682

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 8.2.3-2
- rebuild with tcl-8.4

* Wed Feb  7 2007 Tom Lane <tgl@redhat.com> 8.2.3-1
- Update to PostgreSQL 8.2.3 due to regression induced by security fix
Resolves: #227522

* Sun Feb  4 2007 Tom Lane <tgl@redhat.com> 8.2.2-1
- Update to PostgreSQL 8.2.2 to fix CVE-2007-0555, CVE-2007-0556
Related: #225496

* Fri Jan 12 2007 Tom Lane <tgl@redhat.com> 8.2.1-2
- Split -pl subpackage into three new packages to reduce dependencies
  and track upstream project's packaging.

* Wed Jan 10 2007 Tom Lane <tgl@redhat.com> 8.2.1-1
- Update to PostgreSQL 8.2.1
- Update to pgtcl 1.5.3
- Be sure we link to libncurses, not libtermcap which is disappearing in Fedora

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 8.2.0-2
- rebuild for python 2.5

* Mon Dec  4 2006 Tom Lane <tgl@redhat.com> 8.2.0-1
- Update to PostgreSQL 8.2.0
- Update to PyGreSQL 3.8.1
- Fix chcon arguments in test/regress/Makefile
Related: #201035
- Adjust init script to not fool /etc/rc.d/rc
Resolves: #161470
- Change init script to not do initdb automatically, but require
  manual "service postgresql initdb" for safety.  Per upstream discussions.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.1.4-1.1
- rebuild

* Mon May 22 2006 Tom Lane <tgl@redhat.com> 8.1.4-1
- Update to PostgreSQL 8.1.4 (includes fixes for CVE-2006-2313, CVE-2006-2314;
  see bug #192173)
- Update to PyGreSQL 3.8
- Suppress noise from chcon, per bug #187744

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 8.1.3-2
- Remove JDBC from this build; we will package it as separate SRPM

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 8.1.3-1.1
- rebump for build order issues during double-long bump

* Mon Feb 13 2006 Tom Lane <tgl@redhat.com> 8.1.3-1
- Update to PostgreSQL 8.1.3 (fixes bug #180617, CVE-2006-0553)
- Update to jdbc driver build 405
- Modify multilib header hack to not break non-RH arches, per bug #177564

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.1.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Tom Lane <tgl@redhat.com> 8.1.2-1
- Update to PostgreSQL 8.1.2
- Repair extraneous quote in pgtcl configure script ... odd that bash
  didn't use to spit up on this.

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 8.1.1-3
- fix pg_config.h for 64-bit and ppc platforms
- update Makefile.regress (needs to --load-language=plpgsql)

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 8.1.1-2
- oops, looks like we want uname -i not uname -m

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 8.1.1-1
- Update to PostgreSQL 8.1.1
- Make pg_config.h architecture-independent for multilib installs;
  put the original pg_config.h into pg_config_$ARCH.h

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 8.1.0-4
- Update included PDF-format manual to 8.1.

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 8.1.0-3
- Rebuild due to openssl library update.

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 8.1.0-2
- Rebuild due to openssl library update.

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 8.1.0-1
- Update to PostgreSQL 8.1.0, PyGreSQL 3.7, and jdbc driver build 404
- Fix PAM config file (must have account not only auth) (bug #167040)
- Add BuildPrereq: libxslt-devel (bug #170141)
- Sync with PGDG SRPM as much as feasible

* Fri Oct 14 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Tue Oct  4 2005 Tom Lane <tgl@redhat.com> 8.0.4-2
- Add rpath to plperl.so (bug #162198)

* Tue Oct  4 2005 Tom Lane <tgl@redhat.com> 8.0.4-1
- Update to PostgreSQL 8.0.4, PyGreSQL 3.6.2, and jdbc driver build 312
- Adjust pgtcl link command to ensure it binds to correct libpq (bug #166665)
- Remove obsolete Conflicts: against other python versions (bug #166754)
- Add /etc/pam.d/postgresql (bug #167040)
- Include contrib/xml2 in build (bug #167492)

* Tue May 10 2005 Tom Lane <tgl@redhat.com> 8.0.3-1
- Update to PostgreSQL 8.0.3 (includes security and data-loss fixes; see
  bz#156727, CAN-2005-1409, CAN-2005-1410)
- Update to jdbc driver build 311
- Recreate postgres user after superseding an rh-postgresql install (bug #151911)
- Ensure postgresql server is restarted if running during an upgrade

* Thu Apr 14 2005 Florian La Roche <laroche@redhat.com> 8.0.2-2
- rebuild for postgresql-tcl

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 8.0.2-1
- Update to PostgreSQL 8.0.2.

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 8.0.1-5
- Remove unwanted rpath specification from pgtcl (bz#150649)

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 8.0.1-4
- Attach Obsoletes: declarations for rh-postgresql to subpackages (bz#144435)
- Make Requires: and Prereq: package linkages specify release not only
  version, as per recent mailing list discussion.

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 8.0.1-3
- rebuild with openssl-0.9.7e

* Mon Feb 21 2005 Tom Lane <tgl@redhat.com> 8.0.1-2
- Repair improper error message in init script when PGVERSION doesn't match.
- Arrange for auto update of version embedded in init script.

* Sun Jan 30 2005 Tom Lane <tgl@redhat.com> 8.0.1-1
- Update to PostgreSQL 8.0.1.
- Add versionless symlinks to jar files (bz#145744)

* Wed Jan 19 2005 Tom Lane <tgl@redhat.com> 8.0.0-1
- Update to PostgreSQL 8.0.0, PyGreSQL 3.6.1, pgtcl 1.5.2,
  and jdbc driver build 309.
- Extensive cleanout of obsolete cruft in patch set.
- Regression tests are run during RPM build (NOTE: cannot build as root when
  this is enabled).
- Postmaster stderr goes someplace useful, not /dev/null (bz#76503, #103767)
- Make init script return a useful exit status (bz#80782)
- Move docs' tutorial directory to %%{_libdir}/pgsql/tutorial, since it
  includes .so files that surely do not belong under /usr/share.
- Remove useless .sgml files from docs RPM (bz#134450)
- Put regression tests under /usr/lib64 on 64-bit archs, since .so files
  are not architecture-independent.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 7.4.6-5
- Rebuilt for new readline.

* Tue Jan 11 2005 Dan Walsh <dwalsh@redhat.com> 7.4.6-4
- Add restorecon to postgresql.init in order to restore database to correct
- SELinux context.

* Thu Dec 16 2004 Tom Lane <tgl@redhat.com> 7.4.6-3
- Update to PyGreSQL 3.6 (to fix bug #142711)
- Adjust a few file permissions (bug #142431)
- Assign %%{_libdir}/pgsql to base package instead of -server (bug #74003)

* Mon Nov 15 2004 Tom Lane <tgl@redhat.com> 7.4.6-2
- Rebuild so python components play with python 2.4 (bug 139160)

* Sat Oct 23 2004 Tom Lane <tgl@redhat.com> 7.4.6-1
- Update to PostgreSQL 7.4.6 (bugs 136947, 136949)
- Make init script more paranoid about mkdir step of initializing a new
  database (bugs 136947, 136949)

* Wed Oct 20 2004 Tom Lane <tgl@redhat.com> 7.4.5-4
- Remove contrib/oidjoins stuff from installed fileset; it's of no use
  to ordinary users and has a security issue (bugs 136300, 136301)
- adjust chkconfig priority (bug 128852)

* Tue Oct 05 2004 Tom Lane <tgl@redhat.com> 7.4.5-3
- Solve the stale lockfile problem (bugs 71295, 96981, 134090)
- Use runuser instead of su for SELinux (bug 134588)

* Mon Aug 30 2004 Tom Lane <tgl@redhat.com> 7.4.5-2
- Update to PyGreSQL 3.5.

* Tue Aug 24 2004 Tom Lane <tgl@redhat.com> 7.4.5-1
- Update to PostgreSQL 7.4.5.
- Update JDBC jars to driver build 215.
- Add Obsoletes: entries for rh-postgresql packages, per bug 129278.

* Sat Jul 10 2004 Tom Lane <tgl@redhat.com> 7.4.3-3
- Undo ill-considered chkconfig change that causes server to start
  immediately upon install.  Mea culpa (bug 127552).

* Sat Jul 03 2004 Tom Lane <tgl@redhat.com> 7.4.3-2
- Update JDBC jars to driver build 214.

* Wed Jun 23 2004 Tom Lane <tgl@redhat.com> 7.4.3-1
- Update to PostgreSQL 7.4.3.
- Uninstalling server RPM stops postmaster first, per bug 114846.
- Fix su commands to not assume PG user's shell is sh-like, per bug 124024.
- Fix permissions on postgresql-python doc files, per bug 124822.
- Minor postgresql.init improvements.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com> 7.4.2-1
- Update to PostgreSQL 7.4.2; sync with community SRPM as much as possible.
- Support PGOPTS from /etc/sysconfig/pgsql, per bug 111504.
- Fix permissions on /etc/sysconfig/pgsql, per bug 115278.
- SELinux patch in init file: always su </dev/null, per bug 117901.
- Rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Tom Lane <tgl@redhat.com>
- Update to PostgreSQL 7.4.1.
- Rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- Fix chown syntax in postgresql.init also.
- Rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 9 2004 Lamar Owen <lowen@pari.edu>
- 7.4.1-1PGDG
- Merge Sander Steffann's changes up to 7.4-0.5PGDG
- Proper 7.4.1 JDBC jars this time.
- Patch for no pl/python from Alvaro

* Fri Dec 05 2003 David Jee <djee@redhat.com> 7.4-5
- Rebuild for Perl 5.8.2.

* Mon Dec 01 2003 David Jee <djee@redhat.com> 7.4-4
- Add PyGreSQL patch for deprecated column pg_type.typprtlen [Bug #111263]
- Add headers patch which moves ecpg headers to /usr/include/ecpg
  [Bug #111195]

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-3
- uncomment buildrequires tcl-devel

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-2
- rebuild

* Mon Nov 24 2003 David Jee <djee@redhat.com> 7.4-1
- initial Red Hat build
- move jars to /usr/share/java
- fix rpm-multilib patch to use sysconfig

* Fri Nov 21 2003 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
- 7.4-0.1PGDG
- Development JDBC jars in addition to the 7.3 jars; will replace the
- 7.3 jars once 7.4 official jars are released.
- Changed to use the bzip2 source to save a little size.
- Removed some commented out portions of the specfile.
- Removed the 7.3.4 PDF docs.  Will replace with 7.4 PDF's once they
- are ready.

* Tue Nov 18 2003 Kaj J. Niemi <kajtzu@fi.basen.net> 7.4-0.1
- 7.4
- Fixed Patch #1 (now rpm-pgsql-7.4.patch)
- Fixed Patch #2 (now rpm-multilib-7.4.patch):
- Patch #4 is unnecessary (upstream)
- Fixed Patch #6 (now postgresql-7.4-src-tutorial.patch)
- Added Patch #8 (postgresql-7.4-com_err.patch) as com_err()
  is provided by e2fsprogs and CPPFLAGS gets lost somewhere
  inside configure (bad macro?)
- No 7.4 PDF docs available yet (Source #17)
- PyGreSQL is separated from the upstream distribution but
  we include it as usual (Source #18)
- Default to compiling libpq and ECPG as fully thread-safe

- 7.4 Origin.  See previous spec files for previous history. Adapted
- from Red Hat and PGDG's 7.3.4 RPM, directly descended from
- postgresql-7.3.4-2 as shipped in Fedora Core 1.
