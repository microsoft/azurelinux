Summary:        MySQL.
Name:           mysql
Version:        8.0.32
Release:        1%{?dist}
License:        GPLv2 with exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Databases
URL:            https://www.mysql.com
# Note that the community download page is here: https://dev.mysql.com/downloads/mysql/
Source0:        https://dev.mysql.com/get/Downloads/MySQL-8.0/%{name}-boost-%{version}.tar.gz
Patch0:         CVE-2012-5627.nopatch
BuildRequires:  cmake
BuildRequires:  libtirpc-devel
BuildRequires:  openssl-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  tzdata
BuildRequires:  zlib-devel
%if %{with_check}
BuildRequires:  net-tools
BuildRequires:  sudo
BuildRequires:  shadow-utils
%endif
Requires:       tzdata

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package        devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb

%prep
%autosetup -p1

%build
# Disabling flaky 'invalid_metadata' test.
sed -i "s/\(invalid_metadata\)/DISABLED_\1/" router/tests/component/test_routing_splicer.cc

cmake . \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}   \
      -DWITH_BOOST=boost/boost_1_77_0 \
      -DINSTALL_MANDIR=share/man \
      -DINSTALL_DOCDIR=share/doc \
      -DINSTALL_DOCREADMEDIR=share/doc \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_FLAGS=-fPIC \
      -DCMAKE_CXX_FLAGS=-fPIC \
      -DWITH_EMBEDDED_SERVER=OFF \
      -DFORCE_INSOURCE_BUILD=1
%make_build

%install
%make_install

%check
# Test suite has multiple failures when run as root
chmod g+w . -R
useradd test -G root -m
sudo -u test %make_build CTEST_OUTPUT_ON_FAILURE=1 test

%files
%defattr(-,root,root)
%license LICENSE router/LICENSE.router
%doc README router/README.router
%{_libdir}/plugin/*
%{_libdir}/*.so.*
%{_libdir}/mysqlrouter/*.so*
%{_libdir}/mysqlrouter/private/*.so*
%{_libdir}/private/*.so*
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
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc
%{_libdir}/private/icudt69l/brkitr/*.res
%{_libdir}/private/icudt69l/brkitr/*.brk
%{_libdir}/private/icudt69l/brkitr/*.dict
%{_libdir}/private/icudt69l/unames.icu

%changelog
* Thu Mar 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.32-1
- Auto-upgrade to 8.0.32 - fix CVE-2023-21875 to CVE-2023-21887

* Tue Oct 25 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.31-1
- Upgrade to 8.0.31

* Fri Apr 29 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.0.29-1
- Upgrade to v8.0.29 to fix 8 CVEs.

* Wed Jan 26 2022 Neha Agarwal <pawelwi@microsoft.com> - 8.0.28-1
- Upgrade to v8.0.28 to fix 16 CVEs.

* Tue Jan 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.27-2
- Disabled flaky 'invalid_metadata' test.

* Sat Oct 30 2021 Jon Slobodzian <joslobo@microsoft.com> - 8.0.27-1
- Upgrade to 8.0.27 to fix 36 CVEs

* Mon Aug 30 2021 Thomas Crain <thcrain@microsoft.com> - 8.0.26-2
- Fix majority of package test failures by adding necessary requirements and running tests as non-root
- Add missing tzdata runtime requirement
- Add better log outputs for failed %%check tests

* Tue Jul 27 2021 Thomas Crain <thcrain@microsoft.com> - 8.0.26-1
- Upgrade to 8.0.26 to fix 31 CVEs

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
