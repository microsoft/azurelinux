Name:           ivykis
Summary:        Library for asynchronous I/O readiness notification
Version:        0.42.4
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/buytenh/ivykis
#Source0:       %{url}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

%description
Ivykis is a library for asynchronous I/O readiness notification.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%files
%license COPYING
%{_libdir}/*.so.*
%{_mandir}/man3/*.3.gz

%files devel
%{_libdir}/{*.a,*.so}
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.42.4-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 0.42.4-3
- Remove libtool archive files from final packaging

*   Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.42.4-2
-   License verified.
-   Added source URL.
-   Added 'URL', 'Vendor', and 'Distribution' tags.
*   Mon Apr 13 2020 Jonathan Chiu <jochi@microsoft.com> 0.42.4-1
-   Original version for CBL-Mariner.
