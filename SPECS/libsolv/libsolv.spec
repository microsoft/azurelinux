Summary:        A free package dependency solver
Name:           libsolv
Version:        0.7.28
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/openSUSE/libsolv
Source0:        https://github.com/openSUSE/libsolv/archive/%{version}/%{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake
BuildRequires:  rpm-devel
Requires:       expat-libs

%description
Libsolv is a free package management library, using SAT technology to solve requests.
It supports debian, rpm, archlinux and haiku style distributions.

%package devel
Summary:        Development headers for libsolv
Requires:       %{name} = %{version}-%{release}
Requires:       expat-devel

%description devel
The libsolv-devel package contains libraries, header files and documentation
for developing applications that use libsolv.

%package tools
Summary:        Libsolv tooling
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       bzip2
Requires:       coreutils
Requires:       findutils
Requires:       gzip
Requires:       xz

%description tools
%{summary}

%prep
%autosetup

%build
%cmake \
    -DENABLE_COMPLEX_DEPS=ON            \
    -DENABLE_RPMDB=ON                   \
    -DENABLE_RPMDB_BYRPMHEADER=ON       \
    -DENABLE_RPMDB_LIBRPM=ON            \
    -DENABLE_RPMMD=ON                   \
    -DENABLE_COMPS=ON
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build test

%files
%defattr(-,root,root)
%license LICENSE.BSD
%{_libdir}/libsolv.so.1*
%{_libdir}/libsolvext.so.1*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsolv.so
%{_libdir}/libsolvext.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/*
%{_mandir}/man3/*

%files tools
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Jan 31 2024 Sam Meluch <sammeluch@microsoft.com> - 0.7.28-1
- Upgrade libsolv to version 0.7.28

* Tue Jun 20 2023 Sam Meluch <sammeluch@microsoft.com> - 0.7.24-1
- add ENABLE_COMPS option to support dnf5
- Upgrade to version 0.7.24

* Fri Jan 14 2022 Henry Li <lihl@microsoft.com> - 0.7.20-1
- Upgrade to version 0.7.20
- License Verified

* Tue Oct 19 2021 Jon Slobodzian <joslobo@microsoft.com> - 0.7.19-2
- RPM no longer requires libdb, so remove dependency from libsolv

* Tue Aug 14 2021 Thomas Crain <thcrain@microsoft.com> - 0.7.19-1
- Upgrade to latest upstream
- Install files to %%{_libdir} instead of %%{_lib64dir}
- Lint spec

*   Thu Jun 11 2020 Joe Schmitt <joschmit@microsoft.com> 0.7.7-4
-   Add "pkgconfig(libsolvext)" to the "devel" subpackage.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.7.7-3
-   Added %%license line automatically

*   Tue May 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.7.7-2
-   Separating a "-tools" sub package out of the default "libsolv".

*   Tue May 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.7.7-1
-   Update version to 0.7.7.
-   Moving providing of "pkgconfig(libsolv)" into the "devel" subpackage.

*   Tue Mar 17 2020 Andrew Phelps <anphel@microsoft.com> 0.7.4-1
-   Update version to 0.7.4. License verified.

*   Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 0.6.35-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 0.6.35-1
-   Updated to 0.6.35 and added a patch to fix Index outofBound

*   Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> 0.6.26-5
-   Fix for CVE-2018-20532, CVE-2018-20533, CVE-2018-20534.

*   Thu Mar 01 2018 Xiaolin Li <xiaolinl@vmware.com> 0.6.26-4
-   provides pkgconfig(libsolv).

*   Fri Apr 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.26-3
-   update libdb make config

*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.26-2
-   Requires expat-libs and expat-devel.

*   Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com>  0.6.26-1
-   Upgrade to 0.6.26

*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6.19-4
-   Added -devel subpackage.

*   Thu Oct 27 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.19-3
-   use libdb

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.19-2
-   GA - Bump release of all rpms

*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  0.6.19-1
-   Upgrade to 0.6.19

*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6.17-1
-   Updated to version 0.6.17

*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6.6-3
-   Updated build-requires after creating devel package for db.

*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.6.6-2
-   Updated group.

*   Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.6.6-1
-   Initial build. First version
