Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        2.6.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            http://harfbuzz.org
Source0:        https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.xz
BuildRequires:  freetype-devel
BuildRequires:  glib-devel
Requires:       glib

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package	devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 2.6.4-1
- Upgrade to version 2.6.4
- Remove freetype from build requirement

* Sat May 09 00:20:48 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.9.0-4
- Added %%license line automatically

*   Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.9.0-3
-   Rename "freetype2" to "freetype". 
-   Remove sha1 macro.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*       Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9.0-1
-       Update to version 1.9.0

*       Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 1.4.5-2
-       Add glib requirement

*       Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
-       Initial version
