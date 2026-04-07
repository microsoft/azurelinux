# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global majorversion 18
%global obsoletes_version %( echo $(( %majorversion + 1 )) )
%global betaversion 18beta1

Summary: PostgreSQL client library
Name: libpq
Version: %{majorversion}.0
Release: 3%{?dist}

License: PostgreSQL
Url: http://www.postgresql.org/

# Use this when 18.0 is released
# Source0: https://ftp.postgresql.org/pub/source/v%%{version}/postgresql-%%{version}.tar.bz2
# Source1: https://ftp.postgresql.org/pub/source/v%%{version}/postgresql-%%{version}.tar.bz2.sha256

Source0: https://ftp.postgresql.org/pub/source/v%{betaversion}/postgresql-%{betaversion}.tar.bz2
Source1: https://ftp.postgresql.org/pub/source/v%{betaversion}/postgresql-%{betaversion}.tar.bz2.sha256


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
BuildRequires: make
BuildRequires: libicu-devel
BuildRequires: perl

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
%autosetup -n postgresql-%{betaversion} -p1

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm


%build
# complements symbol-versioning patch
export SYMBOL_VERSION_PREFIX=RHPG_

export CFLAGS="$CFLAGS -DOPENSSL_NO_ENGINE -std=c17"
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
# preserve just errcodes.h
mv $RPM_BUILD_ROOT%{_includedir}/pgsql/server/utils/errcodes.h \
   $RPM_BUILD_ROOT%{_includedir}/pgsql
rm -r $RPM_BUILD_ROOT%_includedir/pgsql/server
mkdir -p $RPM_BUILD_ROOT%{_includedir}/pgsql/server/utils
mv $RPM_BUILD_ROOT%{_includedir}/pgsql/errcodes.h \
   $RPM_BUILD_ROOT%{_includedir}/pgsql/server/utils
rm $RPM_BUILD_ROOT%_datadir/pgsql/postgres.bki
rm $RPM_BUILD_ROOT%_datadir/pgsql/system_constraints.sql

%multilib_fix_c_header --file "%_includedir/pg_config.h"

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
* Wed Sep 17 2025 Filip Janus <fjanus@redhat.com> - 18.0-3
- Removes server based files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Nikola Davidova <ndavidov@redhat.com> - 18.0-1
- Rebase to upstream release 18.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 21 2024 Ales Nezbeda <anezbeda@redhat.com> - 16.4-1
- Update to 16.4

* Tue Jul 30 2024 Ales Nezbeda <anezbeda@redhat.com> - 16.3-5
- Disable openssl ENGINE_API
- Fedora change: https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
- BZ: 2300910

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Filip Janus <fjanus@redhat.com> - 16.3-3
- Move errcodes.h to usr/include/pgsql/server/utils/
- to be consistent with upstream

* Tue Jun 18 2024 Filip Janus <fjanus@redhat.com> - 16.3-2
- Ship errcodes.h in -devel package (kea package requires errorcodes)

* Mon May 27 2024 Ales Nezbeda <anezbeda@redhat.com> - 16.3-1
- Update to 16.3
- Remove backported OpenSSL fix

* Tue Feb 20 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 16.1-4
- Backport OpenSSL 3.2 fix from upstream master

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 5 2023 Filip Janus <fjanus@redhat.com> - 16.1-1
- Update to 16.1
- Build with ICU by default - new upstream feature

* Wed Aug 2 2023 Filip Janus <fjanus@redhat.com> - 15.3-1
- Update to the latest upstream version

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Filip Janus <fjansu@redhat.com> - 15.0-2
- Revert versioning patch
- There are no new symbols in libpq 15

* Tue Sep 27 2022 Ondrej Sloup <osloup@redhat.com> - 15.0-1
- Update to v15
- Update patches
- Resolves: https://fedoraproject.org/wiki/Changes/PostgreSQL_15

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Filip Januš <fjanus@redhat.com> - 14.3-1
- Update to 14.3

* Tue Feb 22 2022 Filip Januš <fjanus@redhat.com> - 14.2-1
- Update to 14.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Filip Januš <fjanus@redhat.com> - 14.1-1
- Update to v14
- Resolves: https://fedoraproject.org/wiki/Changes/PostgreSQL_14

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 13.4-2
- Rebuilt with OpenSSL 3.0.0

* Thu Aug 12 2021 Filip Januš <fjanus@rehdat.com> - 13.4-1
- Update to 13.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Filip Januš <fjanus@redhat.com> - 13.3-1
- Update to 13.3

* Tue Feb 16 2021 Honza Horak <hhorak@redhat.com> - 13.2-1
- Update to 13.2

* Mon Feb 08 2021 Patrik Novotný <panovotn@redhat.com> - 13.1-3
- Fix symbol versioning

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Patrik Novotný <panovotn@redhat.com> - 13.1-1
- Rebase to upstream release 13.1

* Mon Nov 02 2020 Patrik Novotný <panovotn@redhat.com> - 13.0-2
- Rebuild for symbol versioning fix

* Wed Oct 14 2020 Patrik Novotný <panovotn@redhat.com> - 13.0-1
- Rebase to upstream release 13.0

* Tue Aug 18 2020 Patrik Novotný <panovotn@redhat.com> - 12.4-1
- Rebase to upstream release 12.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 Patrik Novotný <panovotn@redhat.com> - 12.3-1
- Rebase to upstream release 12.3

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
