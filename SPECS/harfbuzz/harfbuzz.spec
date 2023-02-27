Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        2.6.4
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://harfbuzz.github.io/
Source0:        https://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.xz
Patch0:         CVE-2023-25193.patch
BuildRequires:  glib-devel
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(icu-uc)
Requires:       glib
%if %{with_check}
BuildRequires:  binutils
BuildRequires:  python3-devel
BuildRequires:  which
%endif

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig(glib-2.0)
Provides:       %{name}-icu = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
# Remove all instances of "/usr/bin/env python" shabangs from test code
find . -type f -name "*.py" -exec sed -i'' -e '1 s|^#!\s*/usr/bin/env\s\+python\d\?|#! %{_bindir}/python3|' {} +
%make_build -k check

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
* Sun Feb 26 2023 Mandeep Plaha <mandeepplaha@microsoft.com> 2.6.4-5
- Add patch for CVE-2023-25193

* Wed Nov 10 2021 Hideyuki Nagase <hideyukn@microsoft.com> - 2.6.4-4
- Add which and binutils when check is enabled
- Replace %{python3} with %{_bindir}/python3
- Replace pkgconfig(glib-2.0) with glib-devel
- Replace %ldconfig_scriptlets with /sbin/ldconfig

* Thu Jun 24 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.4-3
- Fix pkgconfig(freetype2) dependency (incorrect pkgconfig name)

* Mon Jun 21 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.4-2
- Build harfbuzz with icu libraries, fontconfig libraries
- Use pkgconfig(*)-style dependencies
- Provide harbuzz-icu from devel subpackage
- Use macros throughout the spec
- Fix package tests by fixing Python shabangs
- Update URL

* Fri Apr 16 2021 Henry Li <lihl@microsoft.com> - 2.6.4-1
- Upgrade to version 2.6.4
- Remove freetype from build requirement

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.9.0-4
- Added %%license line automatically

* Mon Apr 20 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.9.0-3
- Rename "freetype2" to "freetype". 
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.9.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 1.9.0-1
- Update to version 1.9.0

* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.4.5-2
- Add glib requirement

* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.4.5-1
- Initial version
