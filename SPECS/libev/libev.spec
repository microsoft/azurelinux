Summary:       A full-featured and high-performance event loop
Name:          libev
Version:       4.24
Release:       4%{?dist}
License:       BSD-2-Clause
URL:           http://software.schmorp.de/pkg/libev.html
Source0:       http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz
Group:         System/Library
Vendor:        Microsoft Corporation
Distribution:  Mariner
BuildRequires: pkg-config

%description
A full-featured and high-performance event loop that is loosely modelled after libevent, but without its limitations and bugs.

%package        devel
Summary:        Development files for libev
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library for libev

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/*.so.*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.24-4
- Added %%license line automatically

*   Wed Apr 08 2020 Joe Schmitt <joschmit@microsoft.com> 4.24-3
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
-   Fix changelog styling
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.24-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Apr 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.24-1
-   Initial Version.
