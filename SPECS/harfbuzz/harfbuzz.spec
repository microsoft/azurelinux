Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        8.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://harfbuzz.github.io/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  gcc-c++
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  make
%global with_check 1
%if %{with_check}
BuildRequires:  python3-devel
%endif
Requires:       glib

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package	    devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig(glib-2.0)
Provides:       %{name}-icu = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --disable-static --with-gobject --enable-introspection
%{make_build}

%install
%{make_install}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
# Remove all instances of "/usr/bin/env python" shabangs from test code
find . -type f -name "*.py" -exec sed -i'' -e '1 s|^#!\s*/usr/bin/env\s\+python3\d\?|#! %{python3}|' {} +
%make_build -k check

%ldconfig_scriptlets

%ldconfig_scriptlets devel

%files
%defattr(-,root,root)
%license COPYING
%doc NEWS AUTHORS README
%{_libdir}/*.so*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/HarfBuzz-0.0.typelib
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/HarfBuzz-0.0.gir
%{_libdir}/libharfbuzz-icu.so.*

%changelog
* Mon Jan 29 2024 Bala <balakumaran.kannan@microsoft.com> - 8.3.0-1
- Update source to 8.3.0
- Removed CVE-2023-25193 patch as it was merged to latest version

* Wed Feb 22 2023 Minghe Ren <mingheren@microsoft.com> - 3.4.0-3
- Add patch for CVE-2023-25193 

* Tue Apr 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.0-2
- Fixing invalid source URL.

* Thu Feb 17 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.4.0-1
- Update source to v3.4.0
- Make check section sed for /usr/bin/env/python3, rather than .../python
- License verified

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
