%define majmin %(echo %{version} | cut -d. -f1-2)

Summary:        MySQL.
Name:           mysql
Version:        8.0.45
Release:        2%{?dist}
License:        GPLv2 with exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Databases
URL:            https://www.mysql.com
Source0:        https://dev.mysql.com/get/Downloads/MySQL-%{majmin}/%{name}-boost-%{version}.tar.gz
# AZL's OpenSSL builds with the "no-chacha" option making all ChaCha
# ciphers unavailable.
Patch1:         fix-tests-for-unsupported-chacha-ciphers.patch
Patch2:         CVE-2012-2677.patch
Patch3:         CVE-2025-62813.patch
Patch4:         CVE-2025-0838.patch
BuildRequires:  cmake
BuildRequires:  libtirpc-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  zlib-devel
%if 0%{?with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb

%prep
%autosetup -p1

# Remove bundled versions of some tools to guarantee they are
# not used by MySQL:
# We're building with the '-DWITH_PROTOBUF=system' option.
rm -r extra/protobuf
# We're building with the '-DWITH_CURL=none' option.
rm -r extra/curl

%build
cmake . \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}   \
      -DWITH_BOOST=boost/boost_1_77_0 \
      -DWITH_CURL=none \
      -DWITH_PROTOBUF=system \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_DOCDIR=share/doc \
      -DINSTALL_DOCREADMEDIR=share/doc \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_FLAGS=-fPIC \
      -DCMAKE_CXX_FLAGS=-fPIC \
      -DWITH_EMBEDDED_SERVER=OFF \
      -DFORCE_INSOURCE_BUILD=1

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
# Tests expect to be run as a non-root user.
groupadd test
useradd test -g test -m
chown -R test:test .

# Exclude merge_large_tests as it fails in amd timeout in arm
# In case of failure, print the test log.
sudo -u test ctest --exclude-regex merge_large_tests || { cat Testing/Temporary/LastTest.log; false; }

%files
%defattr(-,root,root)
%license LICENSE router/LICENSE.router
%doc README router/README.router
%{_libdir}/plugin/*
%{_libdir}/*.so.*
%{_libdir}/mysqlrouter/*.so*
%{_libdir}/mysqlrouter/private/*.so*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%{_prefix}/mysqlrouter-log-rotate
%exclude %{_prefix}/mysql-test
%exclude %{_prefix}/docs
%exclude %{_datadir}
%exclude %{_prefix}/*.router

%files devel
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/private/icudt77l/brkitr/*.res
%{_libdir}/private/icudt77l/brkitr/*.brk
%{_libdir}/private/icudt77l/brkitr/*.dict
%{_libdir}/private/icudt77l/unames.icu
%{_libdir}/private/icudt77l/ulayout.icu
%{_libdir}/private/icudt77l/uemoji.icu
%{_libdir}/private/icudt77l/cnvalias.icu
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
* Mon Feb 16 2026 Aditya Singh <v-aditysing@microsoft.com> - 8.0.45-2
- Patch for CVE-2025-0838
- Exclude merge_large_tests in package test.

* Wed Jan 21 2026 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.45-1
- Upgrade to 8.0.45 for CVE-2026-21948, CVE-2026-21968, 
  CVE-2026-21941, CVE-2026-21964, CVE-2026-21936, CVE-2026-21937

* Tue Oct 28 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 8.0.44-2
- Patch for CVE-2025-62813

* Wed Oct 22 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.44-1
- Upgrade to 8.0.44 for CVE-2025-53069, CVE-2025-53042, CVE-2025-53044, CVE-2025-53040, CVE-2025-53062, CVE-2025-53053, CVE-2025-53045, CVE-2025-53054

* Wed Jul 23 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 8.0.43-1
- Upgrade to 8.0.43 to fix CVE-2025-50081,CVE-2025-50077,CVE-2025-50099,CVE-2025-50102,CVE-2025-53023,CVE-2025-50096,CVE-2025-50084,CVE-2025-50104,CVE-2025-50098,CVE-2025-50085,CVE-2025-50093,CVE-2025-50087,CVE-2025-50083,CVE-2025-50082,CVE-2025-50086,CVE-2025-50092,CVE-2025-50094,CVE-2025-50100,CVE-2025-50097,CVE-2025-50101,CVE-2025-50091,CVE-2025-50078,CVE-2025-50080,CVE-2025-50079

* Wed Jun 04 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.42-1
- Upgrade to 8.0.42 to fix CVE-2025-30687, CVE-2025-30705, CVE-2025-30699, CVE-2025-30681, CVE-2025-30721, CVE-2025-21581, CVE-2025-30685,
  CVE-2025-30704, CVE-2025-30703, CVE-2025-30683, CVE-2025-30689, CVE-2025-21579, CVE-2025-30695, CVE-2025-21585, CVE-2025-30715,
  CVE-2025-21574, CVE-2025-30682, CVE-2025-21580, CVE-2025-21575, CVE-2025-21577, CVE-2025-30693, CVE-2025-30696, CVE-2025-30688,
  CVE-2025-21584, CVE-2025-30684

* Wed Mar 26 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.41-1
- Upgrade to 8.0.41 to fix CVE-2025-21490 & CVE-2024-11053
- Remove patch for CVE-2024-9681
- Remove patch for CVE-2025-0725 as we are building without curl

* Mon Feb 10 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.40-6
- Patch CVE-2025-0725

* Mon Jan 27 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 8.0.40-5
- Fix CVE-2024-9681

* Tue Nov 12 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.40-4
- Patched CVE-2012-2677.

* Tue Nov 05 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.40-3
- Explicitly setting "WITH_CURL=none".

* Mon Oct 28 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.40-2
- Switch to ALZ version of protobuf instead of using the bundled one.

* Fri Oct 18 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.40-1
- Auto-upgrade to 8.0.40 - Fix multiple CVEs -- CVE-2024-21193, CVE-2024-21194, CVE-2024-21162, CVE-2024-21157, CVE-2024-21130,
  CVE-2024-20996, CVE-2024-21129, CVE-2024-21159, CVE-2024-21135, CVE-2024-21173, CVE-2024-21160, CVE-2024-21125, CVE-2024-21134,
  CVE-2024-21127, CVE-2024-21142, CVE-2024-21166, CVE-2024-21163, CVE-2024-21203, CVE-2024-21219, CVE-2024-21247, CVE-2024-21237,
  CVE-2024-21231, CVE-2024-21213, CVE-2024-21218, CVE-2024-21197, CVE-2024-21230, CVE-2024-21207, CVE-2024-21201, CVE-2024-21198,
  CVE-2024-21238, CVE-2024-21196, CVE-2024-21239, CVE-2024-21199, CVE-2024-21241, CVE-2024-21236, CVE-2024-21212, CVE-2024-21096,
  CVE-2024-21171, CVE-2024-21165, CVE-2023-46219

* Thu Feb 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.36-1
- Auto-upgrade to 8.0.36

* Mon Apr 24 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.33-1
- Auto-upgrade to 8.0.33 - address CVE-2023-21976, CVE-2023-21972, CVE-2023-21982, CVE-2023-21977, CVE-2023-21980

* Thu Feb 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.32-1
- Auto-upgrade to 8.0.32 - CVE-2023-21879 CVE-2023-21875 CVE-2023-21877 CVE-2023-21876 CVE-2023-21878 CVE-2023-21883 CVE-2023-21881 CVE-2023-21880 CVE-2023-21882 CVE-2023-21887 

* Mon Oct 24 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.31-1
- Upgrade to 8.0.31

* Thu Jun 23 2022 Henry Beberman <henry.beberman@microsoft.com> - 8.0.29-1
- Upgrade to 8.0.29 to fix 17 CVEs

* Wed Jan 26 2022 Neha Agarwal <thcrain@microsoft.com> - 8.0.28-1
- Upgrade to 8.0.28 to fix 16 CVEs

* Sat Apr 24 2021 Thomas Crain <thcrain@microsoft.com> - 8.0.24-1
- Upgrade to 8.0.24 to fix 30 CVEs
- Update source URL

* Thu Feb 11 2021 Rachel Menge <rachelmenge@microsoft.com> - 8.0.23-1
- Upgrade to 8.0.23. Fixes CVE-2020-15358.

* Thu Nov 05 2020 Rachel Menge <rachelmenge@microsoft.com> - 8.0.22-2
- Added no patch for CVE-2012-5627

* Tue Nov 03 2020 Rachel Menge <rachelmenge@microsoft.com> - 8.0.22-1
- Upgrade to 8.0.22. Fixes 40 CVES.
- Lint spec

* Tue Aug 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 8.0.21-1
- Upgrade to 8.0.21. Fixes 32 CVEs.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.0.20-2
- Added %%license line automatically

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.0.20-1
- Upgrade to 8.0.20. Fixes 70 CVEs.
- Update URL.
- Fix CVE-2020-2804.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 8.0.17-1
- Update to version 8.0.17. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.0.14-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 22 2019 Siju Maliakkal <smaliakkal@vmware.com> - 8.0.14-1
- Upgrade to 8.0.14

* Wed Jan 02 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> - 8.0.13-1
- Upgrade to version 8.0.13
- Workaround for broken DCMAKE_BUILD_TYPE=RELEASE(Mysql Bug#92945). Revert in next version

* Mon Nov 19 2018 Ajay Kaher <akaher@vmware.com> - 8.0.12-4
- Enabling for aarch64

* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> - 8.0.12-3
- Adding BuildArch

* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> - 8.0.12-2
- Use libtirpc instead obsoleted rpc from glibc.

* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 8.0.12-1
- Update to version 8.0.12

* Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 5.7.23-1
- Update to version 5.7.23 to get it to build with gcc 7.3

* Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> - 5.7.20-2
- Added patch for CVE-2018-2696

* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.20-1
- Update to version 5.7.20

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 5.7.18-3
- Fix typo in description

* Fri Jul 14 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.18-2
- Run make test in the %check section

* Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.7.18-1
- Initial packaging for Photon
