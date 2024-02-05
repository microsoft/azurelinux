Summary:        A library that performs asynchronous DNS operations
Name:           c-ares
Version:        1.25.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://c-ares.haxx.se/
Source0:        https://c-ares.haxx.se/download/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%if %{with_check}
BuildRequires:  gmock
BuildRequires:  gmock-devel
BuildRequires:  gtest
BuildRequires:  gtest-devel
%endif

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%package devel
Summary:        Development files for c-ares
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%prep
%autosetup
f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
autoreconf -if
%configure --enable-shared \
           --disable-static \
%if %{with_check}
	   --enable-tests \
%endif
           --disable-dependency-tracking
%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/libcares.la

%check
# Use the test method used by the CI (from github)
# Reference: https://github.com/c-ares/c-ares/blob/main/ci/test.sh
check_status=0
PWD=$(pwd)
export TEST_FILTER="--gtest_filter=-*LiveSearch*:*FamilyV4ServiceName*"
TOOLSBIN=${PWD}/src/tools
TESTDIR=${PWD}/test

${TOOLSBIN}/adig www.google.com
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TOOLSBIN}/acountry www.google.com
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TOOLSBIN}/ahost www.google.com
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TESTDIR}/arestest -4 -v $TEST_FILTER
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TESTDIR}/aresfuzz ${TESTDIR}/fuzzinput/*
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TESTDIR}/aresfuzzname ${TESTDIR}/fuzznames/*
if [[ $? -ne 0 ]]; then
	check_status=1
fi

${TESTDIR}/dnsdump ${TESTDIR}/fuzzinput/answer_a ${TESTDIR}/fuzzinput/answer_aaaa
if [[ $? -ne 0 ]]; then
	check_status=1
fi

[[ $check_status -eq 0 ]]

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE.md
%doc README.md README.msvc README.cares CHANGES NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_nameser.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_includedir}/ares_dns_record.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
* Wed Jan 24 2024 Suresh Thelkar <sthelkar@microsoft.com> - 1.25.0-1
- Auto-upgrade to 1.25.0

* Tue May 30 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.19.1-1
- Auto-upgrade to 1.19.1 - CVE-2023-32067

* Tue Apr 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.19.0-1
- Auto-upgrade to 1.19.0 - Address CVE-2022-4904

* Mon Mar 21 2022 Muhammad Falak <mwani@microsoft.com> - 1.18.1-4
- Drop all live DNS lookup from the check section to enable ptest in pipeline

* Fri Mar 04 2022 Muhammad Falak <mwani@microsoft.com> - 1.18.1-3
- Add configure option `--enable-tests`
- Use explicit testing as per official CI to enable ptest

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.18.1-2
- Removing the explicit %%clean stage.

* Sun Nov 28 2021 Muhammad Falak <mwani@microsoft.com> - 1.18.1-1
- Bump version to fix CVE-2021-3672
- License verified

* Mon Mar 15 2021 Nick Samson <nisamson@microsoft.com> - 1.17.1-1
- Removed %%sha line. Upgraded to 1.17.1 to address CVE-2020-8277.
- License confirmed as MIT. Changed URLs to use HTTPS.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.14.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.14.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 1.14.0-1
- Bump c-ares version to 1.14.0

* Fri Sep 29 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.12.0-2
- Fix for CVE-2017-1000381

* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  1.12.0-1
- Upgrade to 1.12.0

* Wed Oct 05 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-3
- Apply patch for CVE-2016-5180.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms

* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 1.10.0-1
- Initial version
