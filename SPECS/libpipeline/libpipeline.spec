Summary:        Library for manipulating pipelines
Name:           libpipeline
Version:        1.5.7
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://libpipeline.nongnu.org
Source0:        http://download.savannah.gnu.org/releases/libpipeline/%{name}-%{version}.tar.gz
%if %{with_check}
BuildRequires:  check
%endif

%description
Contains a library for manipulating pipelines of sub processes
in a flexible and convenient way.

%package devel
Summary:        Library providing headers and static libraries to libpipeline
Group:          Development/Libraries
Requires:       libpipeline = %{version}-%{release}

%description devel
Development files for libpipeline

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make -C tests check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.7-1
- Auto-upgrade to 1.5.7 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.5.5-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 1.5.5-2
- Remove manual pkgconfig(*) provides in toolchain specs

* Wed Jan 12 2022 Henry Li <lihl@microsoft.com> - 1.5.5-1
- Upgrade to version 1.5.5
- Verified License

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.5.0-5
- Remove libtool archive files from final packaging

*   Tue Dec 08 2020 Andrew Phelps <anphel@microsoft.com> 1.5.0-4
-   Add "check" package to fix tests. Remove sha1

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.5.0-3
-   Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.5.0-1
-   Update to 1.5.0
-   Split development files to devel package

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.1-2
-   GA - Bump release of all rpms

*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.1-1
-   Initial build. First version

*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.6-1
-   Initial build. First version
