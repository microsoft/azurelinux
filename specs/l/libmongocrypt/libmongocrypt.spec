# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for libmongocrypt
#
# SPDX-FileCopyrightText:  Copyright 2020-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   libmongocrypt
%global libname      %{gh_project}
%global libver       1.0
%global soname       0

Name:      %{libname}
Summary:   The companion C library for client side encryption in drivers
Version:   1.15.2
Release:   1%{?dist}

# see kms-message/THIRD_PARTY_NOTICES
# kms-message/src/kms_b64.c is ISC
# IntelRDFPMathLib is BSD-3-Clause
# everything else is ASL 2.0
License:   Apache-2.0 AND ISC AND BSD-3-Clause
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{version}.tar.gz

# drop all reference to static libraries
Patch0:    %{libname}-static.patch

BuildRequires: cmake >= 3.12
BuildRequires: gcc
BuildRequires: gcc-c++
# pkg-config may pull compat-openssl10
BuildRequires: openssl-devel
BuildRequires: cmake(bson-1.0) >= 1.11
# for documentation
BuildRequires: doxygen
BuildRequires: make
# for IntelRDFPMathLib
BuildRequires: git
Provides:      bundled(IntelRDFPMathLib) = 2.2


%description
%{summary}.


%package devel
Summary:    Header files and development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig
Requires:   cmake-filesystem

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%autosetup -n %{gh_project}-%{version}%{?prever:-dev} -p1

# Gather license files
tar xf third-party/IntelRDFPMathLib*.tar.xz --strip-components=1 */eula.txt
mv eula.txt                        LICENSE.intelrdfpmathlib
cp kms-message/THIRD_PARTY_NOTICES LICENSE.kms_b64
cp kms-message/COPYING             LICENSE.kms-message


%build
%cmake \
    -DBUILD_VERSION=%{version} \
    -DENABLE_PIC:BOOL=ON \
    -DUSE_SHARED_LIBBSON:BOOL=ON \
    -DMONGOCRYPT_MONGOC_DIR:STRING=USE-SYSTEM \
    -DENABLE_ONLINE_TESTS:BOOL=OFF \
    -DENABLE_STATIC:BOOL=OFF

%cmake_build

doxygen ./doc/Doxygen


%install
%cmake_install


%check
%ctest

if grep -r static %{buildroot}%{_libdir}/cmake; then
  : cmake configuration file contain reference to static library
  exit 1
fi


%files
%license LICENSE*
%{_libdir}/libkms_message.so.%{soname}*
%{_libdir}/libmongocrypt.so.%{soname}*


%files devel
%doc *.md
%doc doc/html
%{_includedir}/kms_message
%{_includedir}/mongocrypt
%{_libdir}/libkms_message.so
%{_libdir}/libmongocrypt.so
%{_libdir}/cmake/kms_message
%{_libdir}/cmake/mongocrypt
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Sep 16 2025 Remi Collet <remi@remirepo.net> - 1.15.2-1
- update to 1.15.2

* Fri Aug 29 2025 Remi Collet <remi@remirepo.net> - 1.15.1-1
- update to 1.15.1

* Mon Aug  4 2025 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun  4 2025 Remi Collet <remi@remirepo.net> - 1.14.1-1
- update to 1.14.1

* Mon May  5 2025 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0

* Mon Apr  7 2025 Remi Collet <remi@remirepo.net> - 1.13.1-1
- update to 1.13.1

* Fri Feb 28 2025 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0
- re-license spec file to CECILL-2.1

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov  6 2024 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Fri Aug  2 2024 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Thu May  2 2024 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1 (no change)

* Fri Feb 16 2024 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan  4 2024 Remi Collet <remi@remirepo.net> - 1.8.4-1
- update to 1.8.4 (no change)

* Tue Jan  2 2024 Remi Collet <remi@remirepo.net> - 1.8.3-1
- update to 1.8.3

* Tue Sep  5 2023 Remi Collet <remi@remirepo.net> - 1.8.2-1
- update to 1.8.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Remi Collet <remi@remirepo.net> - 1.8.1-1
- update to 1.8.1

* Tue May  9 2023 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0

* Wed Apr 19 2023 Remi Collet <remi@remirepo.net> - 1.7.4-1
- update to 1.7.4

* Wed Apr  5 2023 Remi Collet <remi@remirepo.net> - 1.7.3-1
- update to 1.7.3

* Mon Feb 13 2023 Remi Collet <remi@remirepo.net> - 1.7.2-1
- update to 1.7.2

* Mon Feb  6 2023 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1
- open https://jira.mongodb.org/browse/MONGOCRYPT-532 32-bit not supported
- fix i686 build using patch from
  https://github.com/mongodb/libmongocrypt/pull/561

* Tue Jan 24 2023 Remi Collet <remi@remirepo.net> - 1.7.0-1
- update to 1.7.0
- drop patch merged upstream
- open https://jira.mongodb.org/browse/MONGOCRYPT-521 broken LTO build
- add upstream patch for LTO
- open https://jira.mongodb.org/browse/MONGOCRYPT-522 using shared libbson
- adapt our patch for shared libbson
- open https://jira.mongodb.org/browse/MONGOCRYPT-523 offline build
- add upstream patch to use bundled IntelRDFPMathLib20U2
- open https://jira.mongodb.org/browse/MONGOCRYPT-524 32-bit not supported

* Fri Jan 20 2023 Remi Collet <remi@remirepo.net> - 1.6.2-2
- add patch for GCC 13 from
  https://github.com/mongodb/libmongocrypt/pull/535

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec  7 2022 Remi Collet <remi@remirepo.net> - 1.6.2-1
- update to 1.6.2

* Thu Oct  6 2022 Remi Collet <remi@remirepo.net> - 1.6.1-1
- update to 1.6.1 (no change)

* Thu Sep  8 2022 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0

* Mon Aug  1 2022 Remi Collet <remi@remirepo.net> - 1.5.2-1
- update to 1.5.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1
- open https://jira.mongodb.org/browse/MONGOCRYPT-451 build with shared libbson
- open https://jira.mongodb.org/browse/MONGOCRYPT-460 ABI/API breakage

* Fri Jun 17 2022 Remi Collet <remi@remirepo.net> - 1.4.1-1
- update to 1.4.1

* Tue Apr 19 2022 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0

* Mon Mar 21 2022 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2 (no change)

* Wed Mar  2 2022 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov  5 2021 Remi Collet <remi@remirepo.net> - 1.3.0-2
- add patch for OpenSSL 3.0 from
  https://github.com/mongodb/libmongocrypt/pull/213

* Fri Nov  5 2021 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0
- open https://jira.mongodb.org/browse/MONGOCRYPT-359
  compatibility with OpenSSL 3.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.2.2-2
- Rebuilt with OpenSSL 3.0.0

* Wed Sep  8 2021 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0

* Tue Jan 12 2021 Remi Collet <remi@remirepo.net> - 1.1.0-1
- update to 1.1.0

* Thu May 14 2020 Remi Collet <remi@remirepo.net> - 1.0.4-2
- fix cmake macros usage, FTBFS  #1864026

* Thu May 14 2020 Remi Collet <remi@remirepo.net> - 1.0.4-1
- update to 1.0.4

* Thu Feb 13 2020 Remi Collet <remi@remirepo.net> - 1.0.3-1
- update to 1.0.3
- drop patch merged upstream

* Wed Feb 12 2020 Remi Collet <remi@remirepo.net> - 1.0.2-1
- update to 1.0.2
- drop patches merged upstream
- install missing header using patch from
  https://github.com/mongodb/libmongocrypt/pull/90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Remi Collet <remi@remirepo.net> - 1.0.1-2
- modernize spec from review #1792224
- add generated html documentation

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 1.0.1-1
- initial package
- fix installation layout using patch from
  https://github.com/mongodb/libmongocrypt/pull/87
