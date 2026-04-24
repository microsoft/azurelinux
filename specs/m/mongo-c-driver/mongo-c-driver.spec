# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for mongo-c-driver
#
# SPDX-FileCopyrightText:  Copyright 2015-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
%global libname      libmongoc
%global libver       1.0
%global up_version   1.30.7
#global up_prever    rc0
# disabled as require a MongoDB server
%bcond_with          tests

# enable/disable man pages
%bcond_without       manpages

# disable for bootstrap (libmongocrypt needs libbson)
%bcond_without       libmongocrypt

%if 0%{?rhel} == 8
%bcond_with          libutf8proc
%else
%bcond_without       libutf8proc
%endif

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   %{up_version}%{?up_prever:~%{up_prever}}
Release: 2%{?dist}
# See THIRD_PARTY_NOTICES
License:   Apache-2.0 AND ISC AND MIT AND Zlib
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/refs/tags/%{up_version}%{?up_prever:-%{up_prever}}.tar.gz

BuildRequires: cmake >= 3.15
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
# pkg-config may pull compat-openssl10
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libsasl2)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(snappy)
%if %{with libutf8proc}
BuildRequires: pkgconfig(libutf8proc)
%endif
BuildRequires: pkgconfig(libzstd) >= 0.8.0
%if %{with tests}
BuildRequires: mongodb-server
BuildRequires: openssl
%endif
%if %{with libmongocrypt}
# grep VERSION_LESS src/*/CMakeLists.txt
BuildRequires: cmake(mongocrypt) >= 1.12.0
%endif
BuildRequires: perl-interpreter
# From man pages
%if %{with manpages}
BuildRequires: python3
BuildRequires: python3-sphinx >= 5.0
%endif

Requires:   %{name}-libs%{?_isa} = %{version}-%{release}
# Sub package removed
Obsoletes:  %{name}-tools         < 1.3.0
Provides:   %{name}-tools         = %{version}
Provides:   %{name}-tools%{?_isa} = %{version}


%description
%{name} is a client library written in C for MongoDB.


%package libs
Summary:    Shared libraries for %{name}
%if %{without libutf8proc}
Provides:   bundled(libutf8proc) = 2.8.0
%endif
Provides:   bundled(uthash) = 2.3.0

%description libs
This package contains the shared libraries for %{name}.


%package devel
Summary:    Header files and development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig
Requires:   cmake-filesystem
Requires:   pkgconfig(libzstd)
%if %{with libmongocrypt}
Requires:   cmake(mongocrypt)
%endif

%description devel
This package contains the header files and development libraries
for %{name}.

Documentation: http://mongoc.org/libmongoc/%{version}/


%package -n libbson
Summary:    Building, parsing, and iterating BSON documents
# Modified (with bson allocator and some warning fixes and huge indentation
# refactoring) jsonsl is bundled <https://github.com/mnunberg/jsonsl>.
# jsonsl upstream likes copylib approach and does not plan a release
# <https://github.com/mnunberg/jsonsl/issues/14>.
Provides:   bundled(jsonsl)

%description -n libbson
This is a library providing useful routines related to building, parsing,
and iterating BSON documents <http://bsonspec.org/>.


%package -n libbson-devel
Summary:    Development files for %{name}
Requires:   libbson%{?_isa} = %{version}-%{release}
Requires:   pkgconfig
Requires:   cmake-filesystem

%description -n libbson-devel
This package contains libraries and header files needed for developing
applications that use %{name}.

Documentation: http://mongoc.org/libbson/%{version}/


%prep
%setup -q -n %{gh_project}-%{up_version}%{?up_prever:-%{up_prever}}


%build
%cmake \
    -DBUILD_VERSION=%{up_version}%{?up_prever:-%{up_prever}} \
    -DENABLE_MONGOC:BOOL=ON \
    -DENABLE_SHM_COUNTERS:BOOL=ON \
    -DENABLE_SSL:STRING=OPENSSL \
    -DENABLE_SASL:STRING=CYRUS \
    -DENABLE_MONGODB_AWS_AUTH:STRING=ON \
    -DENABLE_AUTOMATIC_INIT_AND_CLEANUP:BOOL=OFF \
    -DENABLE_CRYPTO_SYSTEM_PROFILE:BOOL=ON \
%if %{with manpages}
    -DENABLE_MAN_PAGES:BOOL=ON \
%else
    -DENABLE_MAN_PAGES:BOOL=OFF \
%endif
    -DENABLE_HTML_DOCS:BOOL=OFF \
    -DENABLE_SHARED:BOOL=ON \
    -DENABLE_STATIC:STRING=OFF \
    -DENABLE_ZLIB:STRING=SYSTEM \
    -DENABLE_ZSTD:STRING=ON \
    -DENABLE_SNAPPY:STRING=ON \
%if %{with tests}
    -DENABLE_TESTS:BOOL=ON \
%else
    -DENABLE_TESTS:BOOL=OFF \
%endif
    -DENABLE_EXAMPLES:BOOL=OFF \
    -DENABLE_UNINSTALL:BOOL=OFF \
%if %{with libmongocrypt}
    -DENABLE_CLIENT_SIDE_ENCRYPTION:BOOL=ON \
%else
    -DENABLE_CLIENT_SIDE_ENCRYPTION:BOOL=OFF \
%endif
    -DCMAKE_SKIP_RPATH:BOOL=ON \
%if %{with libutf8proc}
    -DUSE_BUNDLED_UTF8PROC:BOOL=OFF \
%else
    -DUSE_BUNDLED_UTF8PROC:BOOL=ON \
%endif
    -DENABLE_SRV:BOOL=ON \
    -DENABLE_MONGODB_AWS_AUTH:STRING=ON \
    -S .

%if 0%{?cmake_build:1}
%cmake_build
%else
make %{?_smp_mflags}
%endif


%install
%if 0%{?cmake_install:1}
%cmake_install
%else
make install DESTDIR=%{buildroot}
%endif

: Static library
rm -f  %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/cmake/*static*
rm -rf %{buildroot}%{_libdir}/pkgconfig/*static*
: Documentation
rm -rf %{buildroot}%{_datadir}/%{name}


%check
ret=0

%if %{with tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --ipv6 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
export MONGOC_TEST_OFFLINE=on
export MONGOC_TEST_SKIP_MOCK=on
#export MONGOC_TEST_SKIP_SLOW=on

make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)
%endif

if grep -r static %{buildroot}%{_libdir}/cmake/*%{libver}; then
  : cmake configuration file contain reference to static library
  ret=1
fi
exit $ret



%files
%{_bindir}/mongoc-stat

%files libs
%license COPYING
%license THIRD_PARTY_NOTICES
%{_libdir}/%{libname}-%{libver}.so.*

%files devel
%doc src/%{libname}/examples
%doc NEWS
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.so
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_libdir}/cmake/%{libname}-%{libver}
%{_libdir}/cmake/mongoc-%{libver}
%{_libdir}/cmake/mongoc-%{version}
%if %{with manpages}
%{_mandir}/man3/mongoc*
%endif

%files -n libbson
%license COPYING
%license THIRD_PARTY_NOTICES
%{_libdir}/libbson*.so.*

%files -n libbson-devel
%doc src/libbson/examples
%doc src/libbson/NEWS
%{_includedir}/libbson-%{libver}
%{_libdir}/libbson*.so
%{_libdir}/cmake/libbson-%{libver}
%{_libdir}/cmake/bson-%{libver}
%{_libdir}/cmake/bson-%{version}
%{_libdir}/pkgconfig/libbson-*.pc
%if %{with manpages}
%{_mandir}/man3/bson*
%{_mandir}/man3/libbson*
%endif


%changelog
* Wed Feb  4 2026 Remi Collet <remi@remirepo.net> - 1.30.7-1
- update to 1.30.7

* Wed Oct  8 2025 Remi Collet <remi@remirepo.net> - 1.30.6-1
- update to 1.30.6

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Remi Collet <remi@remirepo.net> - 1.30.5-1
- update to 1.30.5

* Wed May  7 2025 Remi Collet <remi@remirepo.net> - 1.30.4-1
- update to 1.30.4

* Wed Apr  9 2025 Remi Collet <remi@remirepo.net> - 1.30.3-1
- update to 1.30.3
- add configuration for mongoc and bson cmake targets

* Wed Mar  5 2025 Remi Collet <remi@remirepo.net> - 1.30.2-1
- update to 1.30.2

* Tue Feb 25 2025 Remi Collet <remi@remirepo.net> - 1.30.1-1
- update to 1.30.1

* Tue Feb 18 2025 Remi Collet <remi@remirepo.net> - 1.30.0-2
- add upstream patch for GCC 15
  https://jira.mongodb.org/browse/CDRIVER-5889

* Thu Feb  6 2025 Remi Collet <remi@remirepo.net> - 1.30.0-1
- update to 1.30.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan  7 2025 Remi Collet <remi@remirepo.net> - 1.29.2-1
- update to 1.29.2

* Thu Dec 12 2024 Remi Collet <remi@remirepo.net> - 1.29.1-1
- update to 1.29.1
- re-license spec file to CECILL-2.1

* Thu Nov  7 2024 Remi Collet <remi@remirepo.net> - 1.29.0-1
- update to 1.29.0
- raise dependency to libmongocrypt 1.12.0

* Thu Oct 10 2024 Remi Collet <remi@remirepo.net> - 1.28.1-1
- update to 1.28.1

* Mon Oct  7 2024 Remi Collet <remi@remirepo.net> - 1.28.0-2
- rebuild for utf8proc #2316935

* Thu Sep 19 2024 Remi Collet <remi@remirepo.net> - 1.28.0-1
- update to 1.28.0
- raise dependency to libmongocrypt 1.11.0

* Wed Sep  4 2024 Remi Collet <remi@remirepo.net> - 1.27.6-1
- update to 1.27.6

* Wed Aug  7 2024 Remi Collet <remi@remirepo.net> - 1.27.5-1
- update to 1.27.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 1.27.4-1
- update to 1.27.4

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 1.27.3-1
- update to 1.27.3

* Wed Jun  5 2024 Remi Collet <remi@remirepo.net> - 1.27.2-1
- update to 1.27.2

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 1.27.1-1
- update to 1.27.1

* Thu May  2 2024 Remi Collet <remi@remirepo.net> - 1.27.0-1
- update to 1.27.0
- raise dependency to libmongocrypt 1.10.0

* Wed Apr  3 2024 Remi Collet <remi@remirepo.net> - 1.26.2-1
- update to 1.26.2

* Wed Mar  6 2024 Remi Collet <remi@remirepo.net> - 1.26.1-1
- update to 1.26.1

* Fri Feb 16 2024 Remi Collet <remi@remirepo.net> - 1.26.0-1
- update to 1.26.0
- raise dependency to libmongocrypt 1.8.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan  3 2024 Remi Collet <remi@remirepo.net> - 1.25.4-1
- update to 1.25.4

* Wed Dec 13 2023 Remi Collet <remi@remirepo.net> - 1.25.3-1
- update to 1.25.3

* Wed Dec  6 2023 Remi Collet <remi@remirepo.net> - 1.25.2-1
- update to 1.25.2

* Wed Nov  8 2023 Remi Collet <remi@remirepo.net> - 1.25.1-1
- update to 1.25.1

* Mon Nov  6 2023 Remi Collet <remi@remirepo.net> - 1.25.0-1
- update to 1.25.0
- drop dependency on libicu
- add dependency on libutf8proc
- open https://jira.mongodb.org/browse/CDRIVER-4767 unusable archive

* Wed Sep  6 2023 Remi Collet <remi@remirepo.net> - 1.24.4-1
- update to 1.24.4 (no change)

* Thu Aug 17 2023 Remi Collet <remi@remirepo.net> - 1.24.3-1
- update to 1.24.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 František Zatloukal <fzatlouk@redhat.com> - 1.24.2-2
- Rebuilt for ICU 73.2

* Thu Jul 13 2023 Remi Collet <remi@remirepo.net> - 1.24.2-1
- update to 1.24.2

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 1.24.1-2
- Rebuilt for ICU 73.2

* Wed Jun 21 2023 Remi Collet <remi@remirepo.net> - 1.24.1-1
- update to 1.24.1

* Wed Jun 21 2023 Remi Collet <remi@remirepo.net> - 1.24.0-1
- update to 1.24.0

* Wed Jun  7 2023 Remi Collet <remi@remirepo.net> - 1.23.5-1
- update to 1.23.5

* Tue May  9 2023 Remi Collet <remi@remirepo.net> - 1.23.4-1
- update to 1.23.4

* Wed Apr  5 2023 Remi Collet <remi@remirepo.net> - 1.23.3-1
- update to 1.23.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan  4 2023 Remi Collet <remi@remirepo.net> - 1.23.2-1
- update to 1.23.2
- use SPDX license ID

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 1.23.1-3
- Rebuild for ICU 72

* Thu Oct 20 2022 Remi Collet <remi@remirepo.net> - 1.23.1-2
- update to 1.23.1

* Thu Sep  8 2022 Remi Collet <remi@remirepo.net> - 1.23.0-1
- update to 1.23.0

* Wed Aug  3 2022 Remi Collet <remi@remirepo.net> - 1.22.1-1
- update to 1.22.1
- raise dependency to libmongocrypt 1.5.2

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.22.0-3
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Remi Collet <remi@remirepo.net> - 1.22.0-1
- update to 1.22.0
- raise dependency to libmongocrypt 1.5.0

* Wed Jun  8 2022 Remi Collet <remi@remirepo.net> - 1.21.2-1
- update to 1.21.2 (no change)

* Wed Mar  2 2022 Remi Collet <remi@remirepo.net> - 1.21.1-1
- update to 1.21.1

* Wed Feb  2 2022 Remi Collet <remi@remirepo.net> - 1.21.0-1
- update to 1.21.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan  6 2022 Remi Collet <remi@remirepo.net> - 1.20.1-1
- update to 1.20.1

* Thu Nov 18 2021 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0

* Thu Nov  4 2021 Remi Collet <remi@remirepo.net> - 1.19.2-1
- update to 1.19.2

* Wed Oct  6 2021 Remi Collet <remi@remirepo.net> - 1.19.1-1
- update to 1.19.1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.19.0-2
- Rebuilt with OpenSSL 3.0.0

* Fri Sep  3 2021 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0

* Fri Jul 30 2021 Remi Collet <remi@remirepo.net> - 1.18.0-3
- use better fix for invalid RPATH using upstream solution from
  https://jira.mongodb.org/browse/CDRIVER-4013

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0

* Wed Jul  7 2021 Remi Collet <remi@remirepo.net> - 1.17.7-1
- update to 1.17.7

* Thu Jun  3 2021 Remi Collet <remi@remirepo.net> - 1.17.6-2
- update to 1.17.6
- fix invalid rpath

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 1.17.5-3
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 1.17.5-2
- Rebuild for ICU 69

* Fri Apr  9 2021 Remi Collet <remi@remirepo.net> - 1.17.5-1
- update to 1.17.5 (no change)

* Thu Feb  4 2021 Remi Collet <remi@remirepo.net> - 1.17.4-1
- update to 1.17.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 2020 Remi Collet <remi@remirepo.net> - 1.17.3-1
- update to 1.17.3

* Wed Nov  4 2020 Remi Collet <remi@remirepo.net> - 1.17.2-1
- update to 1.17.2

* Wed Oct  7 2020 Remi Collet <remi@remirepo.net> - 1.17.1-1
- update to 1.17.1

* Fri Jul 31 2020 Remi Collet <remi@remirepo.net> - 1.17.0-1
- update to 1.17.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0~rc0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Remi Collet <remi@remirepo.net> - 1.17.0~rc0-2
- use more cmake macros
- add upstream patch for latest sphinx

* Fri Jul 17 2020 Remi Collet <remi@remirepo.net> - 1.17.0~rc0-1
- update to 1.17.0-rc0

* Thu Jun 11 2020 Remi Collet <remi@remirepo.net> - 1.17.0~beta2-2
- rebuild

* Wed Jun 10 2020 Remi Collet <remi@remirepo.net> - 1.17.0~beta2-1
- update to 1.17.0-beta2
- drop patch merged upstream

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 1.17.0~beta-2
- Rebuild for ICU 67

* Wed Apr 15 2020 Remi Collet <remi@remirepo.net> - 1.17.0~beta-1
- update to 1.17.0-beta
- fix cmake for static lilbraries using patch from
  https://github.com/mongodb/mongo-c-driver/pull/600

* Mon Mar 09 2020 Honza Horak <hhorak@redhat.com> - 1.16.2-2
- Add missing devel libraries to the mongo-c-driver devel sub-package,
  so depended packages find them

* Tue Feb 25 2020 Remi Collet <remi@remirepo.net> - 1.16.2-1
- update to 1.16.2 (no change)

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 1.16.1-1
- update to 1.16.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Remi Collet <remi@remirepo.net> - 1.16.0-3
- enable client side encryption
- add dependency to libmongocrypt

* Sat Jan 18 2020 Remi Collet <remi@remirepo.net> - 1.16.0-2
- clean reference to static library in cmake files
- see https://jira.mongodb.org/browse/CDRIVER-3495

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0
- disable client side encryption until #1792224 is approved

* Wed Dec 18 2019 Remi Collet <remi@remirepo.net> - 1.15.3-1
- update to 1.15.3

* Thu Nov  7 2019 Remi Collet <remi@remirepo.net> - 1.15.2-1
- update to 1.15.2
- add zstd compression support on EL-8

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 1.15.1-2
- Rebuild for ICU 65

* Mon Sep  2 2019 Remi Collet <remi@remirepo.net> - 1.15.1-1
- update to 1.15.1

* Wed Aug 21 2019 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0
- add zstd compression support on Fedora
- use python3 during the build

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0

* Thu Jan 31 2019 Remi Collet <remi@remirepo.net> - 1.13.1-1
- update to 1.13.1
- disable test suite, as MongoDB server is required

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 1.13.0-4
- Rebuild for ICU 63

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 1.13.0-3
- Append curdir to CMake invokation. (#1668512)

* Wed Sep 19 2018 Remi Collet <remi@remirepo.net> - 1.13.0-2
- enable test suite on all 64-bit arches
  but skip tests relying on the mock server

* Tue Sep 18 2018 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0
- open https://jira.mongodb.org/browse/CDRIVER-2827 make install fails
- open https://jira.mongodb.org/browse/CDRIVER-2828 test failures
- disable test suite

* Thu Jul 19 2018 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.11.0-2
- Rebuild for ICU 62

* Sat Jun 23 2018 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0
- add dependency on libicu

* Wed Jun 20 2018 Remi Collet <remi@remirepo.net> - 1.10.3-1
- update to 1.10.3

* Fri Jun  8 2018 Remi Collet <remi@remirepo.net> - 1.10.2-1
- update to 1.10.2
- soname switch back to 0

* Thu May 31 2018 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Mon May 28 2018 Remi Collet <remi@remirepo.net> - 1.10.0-2
- add patch from https://github.com/mongodb/mongo-c-driver/pull/498
  for https://jira.mongodb.org/browse/CDRIVER-2667
  "mongoc-stat is not supported on your platform"
- open https://jira.mongodb.org/browse/CDRIVER-2668
  "mongoc-stat build but not installed"

* Mon May 28 2018 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0
- also build libbson and create new sub-packages
- switch to cmake
- soname bump to 1

* Wed May  2 2018 Remi Collet <remi@remirepo.net> - 1.9.5-1
- update to 1.9.5

* Tue Apr 10 2018 Remi Collet <remi@remirepo.net> - 1.9.4-1
- update to 1.9.4
- ensure all libraries referenced in pkgconfig file are required by devel
  reported as https://jira.mongodb.org/browse/CDRIVER-2603, #1560611

* Wed Mar 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.9.3-2
- Fix docs build with Sphinx >= 1.7

* Thu Mar  1 2018 Remi Collet <remi@remirepo.net> - 1.9.3-1
- update to 1.9.3

* Thu Feb 22 2018 Remi Collet <remi@remirepo.net> - 1.9.2-5
- add workaround for https://jira.mongodb.org/browse/CDRIVER-2516
- enable test suite

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 1.9.2-4
- drop ldconfig scriptlets
- disable again test suite

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 1.9.2-2
- enable test suite on 64-bit

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 1.9.2-1
- update to 1.9.2 (no change)

* Wed Jan 10 2018 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1

* Fri Dec 22 2017 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0
- raise dependency on libbson 1.9

* Fri Nov 17 2017 Remi Collet <remi@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Thu Oct 12 2017 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Fri Sep 15 2017 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- update to 1.8.0

* Thu Aug 10 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0
- disable test suite in rawhide (mongodb-server is broken)

* Tue Aug  8 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.1.rc2
- update to 1.7.0-rc2
- add --with-snappy and --with-zlib build options

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.2

* Tue Mar 28 2017 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Wed Mar  8 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-2
- rebuild with new upstream tarball
- add examples in devel documentation
- use patch instead of sed hacks for rpm specific changes

* Tue Mar  7 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1
- open https://jira.mongodb.org/browse/CDRIVER-2078
  can't build man pages

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add fix for https://jira.mongodb.org/browse/CDRIVER-2042
  from https://github.com/mongodb/mongo-c-driver/pull/421

* Thu Jan 12 2017 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- update to 1.5.3

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2
- run server on both IPv4 and IPv6
- open https://jira.mongodb.org/browse/CDRIVER-1988 - Failed test
- revert IPv6 commit

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- update to 1.5.1

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Fri Nov 18 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.5.rc6
- update to 1.5.0-rc6

* Fri Nov  4 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.4.rc4
- update to 1.5.0-rc4

* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.3.rc3
- update to 1.5.0-rc3
- drop patches merged upstream

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.2.rc2
- open https://jira.mongodb.org/browse/CDRIVER-1703 missing files
- open https://jira.mongodb.org/browse/CDRIVER-1702 broken test
- enable test suite

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.1.rc2
- update to 1.5.0-rc2
- drop crypto patch merged upstream
- drop the private library
- disable test suite

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 1.3.5-6
- Rebuild against libbson-1.4.0 (bug #1361166)

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-5
- add BR on perl, FTBFS from Koschei

* Mon Jun 13 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-4
- add workaround to abicheck failure
  see https://bugzilla.redhat.com/1345868

* Mon May 16 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-2
- add patch to enforce system crypto policies

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5
- use --disable-automatic-init-and-cleanup build option
- ignore check for libbson version = libmongoc version

* Sat Mar 19 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- build with MONGOC_NO_AUTOMATIC_GLOBALS

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4
- drop patch merged upstream

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- cleanup for review
- move libraries in "libs" sub-package
- add patch to skip online tests
  open https://github.com/mongodb/mongo-c-driver/pull/314
- temporarily disable test suite on arm  (#1303864)
- temporarily disable test suite on i686/F24+ (#1313018)

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- move tools in devel package

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- open https://jira.mongodb.org/browse/CDRIVER-1040 - ABI breaks

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.6.rc0
- Update to 1.2.0-rc0

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.5.20150903git3eaf73e
- add patch to export library verson in the API
  open https://github.com/mongodb/mongo-c-driver/pull/265

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.4.20150903git3eaf73e
- update to version 1.2.0beta1 from git snapshot
- https://jira.mongodb.org/browse/CDRIVER-828 missing tests/json

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.3.beta
- more upstream patch (for EL-6)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.beta
- Upstream version 1.2.0beta

* Wed May 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Upstream version 1.1.6

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Upstream version 1.1.5

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-3
- test build for upstream patch

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- cleanup build dependencies and options

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Initial package
- open https://jira.mongodb.org/browse/CDRIVER-624 - gcc 5
