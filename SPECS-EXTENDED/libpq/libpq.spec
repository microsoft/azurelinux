%global majorversion 12
%global obsoletes_version %( echo $(( %majorversion + 1 )) )

Summary: PostgreSQL client library
Name: libpq
Version: %{majorversion}.2
Release: 3%{?dist}

License: PostgreSQL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://www.postgresql.org/

Source0: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source1: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.sha256


# Comments for these patches are in the patch files.
Patch1: libpq-10.3-rpm-pgsql.patch
Patch2: libpq-10.3-var-run-socket.patch
Patch3: libpq-12.1-symbol-versioning.patch

BuildRequires: gcc
BuildRequires: glibc-devel bison flex gawk
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: krb5-devel
BuildRequires: openldap-devel
BuildRequires: gettext
BuildRequires: multilib-rpm-config

Obsoletes: postgresql-libs < %obsoletes_version
Provides: postgresql-libs = %version-%release


%description
The libpq package provides the essential shared library for any PostgreSQL
client program or interface.  You will need to install this package to use any
other PostgreSQL package or any clients that need to connect to a PostgreSQL
server.


%package devel
Summary: Development files for building PostgreSQL client tools
Requires: %name%{?_isa} = %version-%release
# Historically we had 'postgresql-devel' package which was used for building
# both PG clients and PG server modules;  let's have this fake provide to cover
# most of the depending packages and the rest (those which want to build server
# modules) need to be fixed to require postgresql-server-devel package.
Provides: postgresql-devel = %version-%release
Obsoletes: postgresql-devel < %obsoletes_version

%description devel
The libpq package provides the essential shared library for any PostgreSQL
client program or interface.  You will need to install this package to build any
package or any clients that need to connect to a PostgreSQL server.


%prep
( cd "$(dirname "%SOURCE1")" ; sha256sum -c "%SOURCE1" )
%autosetup -n postgresql-%version -p1

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm


%build
# complements symbol-versioning patch
export SYMBOL_VERSION_PREFIX=RHPG_

# We don't build server nor client (e.g. /bin/psql) binaries in this package, so
# we can disable some configure options.
%configure \
    --disable-rpath \
    --with-ldap \
    --with-openssl \
    --with-gssapi \
    --enable-nls \
    --without-readline \
    --datadir=%_datadir/pgsql

%global build_subdirs \\\
        src/include \\\
        src/common \\\
        src/port \\\
        src/interfaces/libpq \\\
        src/bin/pg_config

for subdir in %build_subdirs; do
    %make_build -C "$subdir"
done


%install
for subdir in %build_subdirs; do
    %make_install -C "$subdir"
done

# remove files not to be packaged
find $RPM_BUILD_ROOT -name '*.a' -delete
rm -r $RPM_BUILD_ROOT%_includedir/pgsql/server

%multilib_fix_c_header --file "%_includedir/pg_config.h"
%multilib_fix_c_header --file "%_includedir/pg_config_ext.h"

find_lang_bins ()
{
    lstfile=$1 ; shift
    cp /dev/null "$lstfile"
    for binary; do
        %find_lang "$binary"-%majorversion
        cat "$binary"-%majorversion.lang >>"$lstfile"
    done
}

find_lang_bins %name.lst        libpq5
find_lang_bins %name-devel.lst  pg_config


%files -f %name.lst
%license COPYRIGHT
%_libdir/libpq.so.5*
%dir %_datadir/pgsql
%doc %_datadir/pgsql/pg_service.conf.sample


%files devel -f %name-devel.lst
%_bindir/pg_config
%_includedir/*
%_libdir/libpq.so
%_libdir/pkgconfig/libpq.pc


%changelog
* Wed Dec 08 2021 Thomas Crain <thcrain@microsoft.com> - 12.2-3
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 17 2020 Patrik Novotný <panovotn@redhat.com> - 12.2-1
- Rebase to upstream release 12.2

* Tue Feb 04 2020 Patrik Novotný <panovotn@redhat.com> - 12.1-1
- Rebase to upstream release 12.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Patrik Novotný <panovotn@redhat.com> - 11.6-1
- Rebase to upstream version 11.6

* Wed Aug 07 2019 Petr Kubat <pkubat@redhat.com> - 11.5-1
- New upstream version 11.5

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Petr Kubat <pkubat@redhat.com> - 11.4-1
- New upstream version 11.4

* Fri May 10 2019 Pavel Raiskup <praiskup@redhat.com> - 11.3-2
- obsolete anything < %%majorversion+1

* Thu May 09 2019 Patrik Novotný <panovotn@redhat.com> - 11.3-1
- New upstream version 11.3

* Mon Feb 18 2019 Pavel Raiskup <praiskup@redhat.com> - 11.2-2
- fix dnf system-upgrade from f29 to f29+, rhbz#1677849

* Thu Feb 14 2019 Pavel Raiskup <praiskup@redhat.com> - 11.2-1
- latest upstream release, per release notes:
  https://www.postgresql.org/docs/11/static/release-11-1.html
  https://www.postgresql.org/docs/11/static/release-11-2.html

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Pavel Raiskup <praiskup@redhat.com> - 11.0-1
- latest upstream release, per release notes:
  https://www.postgresql.org/docs/11/static/release-11-0.html

* Tue Sep 04 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-4
- fix provides/obsoletes to final state

* Thu Aug 30 2018 Pavel Raiskup <praiskup@redhat.com> - 10.5-1
- libpq packaging for Fedora
