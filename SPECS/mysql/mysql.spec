Summary:        MySQL.
Name:           mysql
Version:        8.0.40
Release:        2%{?dist}
License:        GPLv2 with exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Databases
URL:            https://www.mysql.com
Source0:        https://dev.mysql.com/get/Downloads/MySQL-8.0/%{name}-boost-%{version}.tar.gz
Patch0:         CVE-2012-5627.nopatch
# Patch can be removed after upgrading MySQL to 8.4+
# or switching to system Protobuf 3.25+ with the 'WITH_PROTOBUF=system' option.
Patch1:         CVE-2024-2410.patch
# AZL's OpenSSL builds with the "no-chacha" option making all ChaCha
# ciphers unavailable.
Patch2:         fix-tests-for-unsupported-chacha-ciphers.patch
BuildRequires:  cmake
BuildRequires:  libtirpc-devel
BuildRequires:  openssl-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  zlib-devel
%if 0%{?with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

Requires(postun): shadow-utils
Requires(pre):  shadow-utils

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb

%prep
%autosetup -p1

%build
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

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
# Tests expect to be run as a non-root user.
groupadd test
useradd test -g test -m
chown -R test:test .

# In case of failure, print the test log.
sudo -u test make test || { cat Testing/Temporary/LastTest.log; false; }

%pre
getent group  mysql  >/dev/null || groupadd -r mysql
getent passwd mysql  >/dev/null || useradd  -c "mysql" -s /bin/false -g mysql -M -r mysql

%postun
if getent passwd mysql >/dev/null; then
   userdel mysql
fi
if getent group mysql >/dev/null; then
    groupdel mysql
fi

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
%{_libdir}/private/icudt73l/brkitr/*.res
%{_libdir}/private/icudt73l/brkitr/*.brk
%{_libdir}/private/icudt73l/brkitr/*.dict
%{_libdir}/private/icudt73l/unames.icu
%{_libdir}/private/icudt73l/cnvalias.icu
%{_libdir}/private/icudt73l/uemoji.icu
%{_libdir}/private/icudt73l/ulayout.icu
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
* Tue Oct 29 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.0.40-2
- Patched CVE-2024-2410.

* Fri Oct 18 2024 Sudipta Pandit <sudpandit@microsoft.com> - 8.0.40-1
- Upgrade to 8.0.40 to fix multiple CVEs -- CVE-2024-21193, CVE-2024-21194, CVE-2024-21162, CVE-2024-21157, CVE-2024-21130,
  CVE-2024-20996, CVE-2024-21129, CVE-2024-21159, CVE-2024-21135, CVE-2024-21173, CVE-2024-21160, CVE-2024-21125, CVE-2024-21134,
  CVE-2024-21127, CVE-2024-21142, CVE-2024-21166, CVE-2024-21163, CVE-2024-21203, CVE-2024-21219, CVE-2024-21247, CVE-2024-21237,
  CVE-2024-21231, CVE-2024-21213, CVE-2024-21218, CVE-2024-21197, CVE-2024-21230, CVE-2024-21207, CVE-2024-21201, CVE-2024-21198,
  CVE-2024-21238, CVE-2024-21196, CVE-2024-21239, CVE-2024-21199, CVE-2024-21241, CVE-2024-21236, CVE-2024-21212, CVE-2024-21096,
  CVE-2024-21171, CVE-2024-21165, CVE-2023-46219
- Remove patch for CVE-2023-46218 (fixed in 8.0.37)

* Tue Jun 18 2024 Archana Choudhary <archana1@microsoft.com> - 8.0.36-1
- Upgrade to 8.0.36 to fix 10 CVEs

* Fri Jan 26 2024 Andy Zaugg <azaugg@linkedin.com> - 8.0.35-4
- Add shadow-utils dependency for rpm post and uninstall scripts

* Wed Jan 10 2024 Andy Zaugg <azaugg@linkedin.com> - 8.0.35-3
- Add mysql user as part of post scripts

* Wed Dec 20 2023 Suresh Thelkar <sthelkar@microsoft.com> - 8.0.35-2
- Patch CVE-2023-46218 

* Tue Nov 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.35-1
- Auto-upgrade to 8.0.35 - address CVE-2023-22078, CVE-2023-22068, CVE-2023-22084, CVE-2023-22070, CVE-2023-22092, CVE-2023-22079, CVE-2023-22032, CVE-2023-22103, CVE-2023-22112, CVE-2023-22059, CVE-2023-22114, CVE-2023-22097, CVE-2023-22064, CVE-2023-22066, etc.

* Wed Nov 1 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.34-1
- Auto-upgrade to 8.0.34 - address CVE-2023-22053, CVE-2023-22054, CVE-2023-22056, CVE-2023-22058, CVE-2023-22065, CVE-2023-22110, CVE-2023-22111, CVE-2023-22113, CVE-2023-22115

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
