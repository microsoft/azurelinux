%global pkgname mysql

# Include files for systemd
%global daemon_name       mysqld
%global daemon_no_prefix  mysqld

# Set this to 1 to see which tests fail, but 0 on production ready build
%global ignore_testsuite_result 0

Summary:        MySQL.
Name:           mysql
Version:        8.0.36
Release:        2%{?dist}
License:        GPLv2 with exceptions AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Databases
URL:            https://www.mysql.com
Source0:        https://dev.mysql.com/get/Downloads/MySQL-8.0/%{name}-boost-%{version}.tar.gz
Source1:        mysql.service
Source2:        mysql@.service
Source3:        mysql.tmpfiles.d
# Skipped tests lists
Source50:       rh-skipped-tests-list-base.list
Source51:       rh-skipped-tests-list-arm.list
Source52:       rh-skipped-tests-list-s390.list
Source53:       rh-skipped-tests-list-ppc.list
Patch0:         CVE-2012-5627.nopatch
BuildRequires:  cmake
BuildRequires:  libtirpc-devel
BuildRequires:  openssl-devel
BuildRequires:  rpcsvc-proto-devel
BuildRequires:  zlib-devel
BuildRequires:  systemd
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
Requires:       systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires: %systemd_requires}

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb

%prep
%autosetup -p1

# Needed for unit tests (different from MTR tests), which we doesn't run, as they doesn't work on some architectures: #1989847
rm -r extra/googletest
 
# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE50} | tee -a mysql-test/%{skiplist}
 
# disable some tests failing on different architectures
%ifarch aarch64
cat %{SOURCE51} | tee -a mysql-test/%{skiplist}
%endif
 
%ifarch s390x
cat %{SOURCE52} | tee -a mysql-test/%{skiplist}
%endif
 
%ifarch ppc64le
cat %{SOURCE53} | tee -a mysql-test/%{skiplist}
%endif

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} scripts

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
      -DWITH_SYSTEMD=1 \
      -DSYSTEMD_SERVICE_NAME="%{daemon_name}" \
      -DSYSTEMD_PID_DIR="%{pidfiledir}" \
      -DFORCE_INSOURCE_BUILD=1 \
      -DINSTALL_MYSQLTESTDIR=share/mysql-test \
      -DWITH_UNIT_TESTS=0

# Note: disabling building of unittests to workaround #1989847

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# install systemd unit files and scripts for handling server startup
install -D -p -m 644 scripts/mysql.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 644 scripts/mysql@.service %{buildroot}%{_unitdir}/%{daemon_name}@.service
install -D -p -m 0644 scripts/mysql.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{daemon_name}.conf
rm -r %{buildroot}%{_tmpfilesdir}/%{daemon_name}.conf

# Install the list of skipped tests to be available for user runs
install -p -m 0644 %{_vpath_srcdir}/mysql-test/%{skiplist} %{buildroot}%{_datadir}/mysql-test
	
rm %{buildroot}%{_bindir}/{mysql_client_test,mysqlxtest,mysqltest_safe_process,zlib_decompress}
# rm -r %{buildroot}%{_datadir}/mysql-test

%check
pushd
# Note: disabling building of unittests to workaround #1989847
pushd mysql-test
cp ../../mysql-test/%{skiplist} .
 
# Builds might happen at the same host, avoid collision
#   The port used is calculated as 10 * MTR_BUILD_THREAD + 10000
#   The resulting port must be between 5000 and 32767
export MTR_BUILD_THREAD=$(( $(date +%s) % 2200 ))
 
(
  set -ex
  cd %{buildroot}%{_datadir}/mysql-test
 
  export common_testsuite_arguments=" %{?with_debug:--debug-server} --parallel=auto --force --retry=2 --suite-timeout=900 --testcase-timeout=30 --skip-combinations --max-test-fail=5 --report-unstable-tests --clean-vardir --nocheck-testcases "
 
  # If full testsuite has already been run on this version and we don't explicitly want the full testsuite to be run
  if [[ "%{last_tested_version}" == "%{version}" ]] && [[ %{force_run_testsuite} -eq 0 ]]
  then
    # in further rebuilds only run the basic "main" suite (~800 tests)
    echo "running only base testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments --suite=main --skip-test-list=%{skiplist}
  fi
 
 # If either this version wasn't marked as tested yet or I explicitly want to run the testsuite, run everything we have (~4000 test)
  if [[ "%{last_tested_version}" != "%{version}" ]] || [[ %{force_run_testsuite} -ne 0 ]]
  then
    echo "running advanced testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments \
    %if %{ignore_testsuite_result}
      --max-test-fail=9999 || :
    %else
      --skip-test-list=%{skiplist}
    %endif
  fi
 
  # There might be a dangling symlink left from the testing, remove it to not be installed
  rm -r var $(readlink var)
)
 
popd

%files
%defattr(-,root,root)
%license LICENSE router/LICENSE.router
%doc README router/README.router
%{_libdir}/plugin/*
%{_libdir}/*.so.*
%{_libdir}/mysqlrouter/*.so*
%{_libdir}/mysqlrouter/private/*.so*
%{_libdir}/private/*.so*
%{_libdir}/systemd/system/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%{_prefix}/mysqlrouter-log-rotate
%{_prefix}/%{_libdir}/systemd/system/*.service
%{_prefix}/%{_libdir}/tmpfiles.d/*.conf
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
%{_libdir}/private/icudt73l/ulayout.icu
%{_libdir}/private/icudt73l/uemoji.icu
%{_libdir}/private/icudt73l/cnvalias.icu
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
* Thu Jun 20 2024 Betty Lakes <bettylakes@microsoft.com> - 8.0.36-2
- Add systemd dependency and unit test workaround

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
