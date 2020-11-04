Summary:        A full-featured and high-performance event loop
Name:           libev
Version:        4.24
Release:        5%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Library
URL:            http://software.schmorp.de/pkg/libev.html
Source0:        http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz
BuildRequires:  pkg-config

%description
A full-featured and high-performance event loop that is loosely modelled after libevent, but without its limitations and bugs.

%package        devel
Summary:        Development files for libev
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library for libev

%package libevent-devel
Summary:        Compability development header with libevent for %{name}
Requires:       %{name}-devel = %{version}-%{release}
# The event.h file conflicts with one from libevent-devel
Conflicts:      libevent-devel

%description libevent-devel
This package contains a development header to make libev compatible with libevent.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -delete -print

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
%exclude %{_includedir}/event.h
%{_includedir}/*
%{_libdir}/*.so

%files libevent-devel
%defattr(-,root,root)
%{_includedir}/event.h

%changelog
* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.24-5
- Split libev-libevent-devel subpackage to resolve event.h conflicts with libevent-devel.

* Sat May 09 00:21:43 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.24-4
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
