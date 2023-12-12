%global so_version 1

Summary:        Library that implements the Generic Tagged Arrays file format
Name:           libgta
Version:        1.2.1
Release:        9%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://marlam.de/gta/
Source0:        https://marlam.de/gta/releases/%{name}-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc

%description
Libgta is a portable library that implements the GTA (Generic Tagged Arrays)
file format. It provides interfaces for C and C++.

%package devel
Summary:        Development Libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        API documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
The %{name}-doc package contains HTML API documentation and
examples for %{name}.

%prep
%setup -q

%build
%cmake -D GTA_BUILD_STATIC_LIB:BOOL=FALSE
%cmake_build

%install
%cmake_install

# Remove documentation; will install it with doc macro
rm -rf %{buildroot}%{_docdir}


%check
%ctest


%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS README
%{_libdir}/%{name}.so.%{so_version}
%{_libdir}/%{name}.so.%{so_version}.*

%files devel
%{_libdir}/cmake/GTA-%{version}
%{_libdir}/pkgconfig/gta.pc
%{_includedir}/gta
%{_libdir}/%{name}.so

%files doc
%doc doc/example*

%changelog
* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 1.2.1-9
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.2.1-5
- Guard against unintentional so-version bumps

* Fri May 21 2021 Sandro Mani <manisandro@gmail.com> - 1.2.1-4
- Rebuild (gdal)

* Wed May 19 2021 Jiri Kucera <jkucera@redhat.com> - 1.2.1-3
- Fix FTBFS (bz1923686)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 15 2020 Volker Fröhlich <volker27@gmx.at> - 1.2.1-1
- New upstream release
- Switch to the now-preferred cmake build system

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Volker Fröhlich <volker27@gmx.at> - 1.0.9-1
- New upstream release
- New URL

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 25 2014 Volker Fröhlich <volker27@gmx.at> - 1.0.7-1
- New upstream release
- Install the cmake find script

* Wed Dec 17 2014 Volker Fröhlich <volker27@gmx.at> - 1.0.6-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Volker Fröhlich <volker27@gmx.at> - 1.0.4-3
- Rebuild for imagemagick ABI version 16

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb  3 2013 Volker Fröhlich <volker27@gmx.at> 1.0.4-1
- New upstream release

* Sun Sep  2 2012 Volker Fröhlich <volker27@gmx.at> 1.0.3-1
- New upstream release
- Run checks

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb  7 2012 Volker Fröhlich <volker27@gmx.at> 1.0.2-2
- Add a doc sub-package for API documentation

* Sat Jan 28 2012 Volker Fröhlich <volker27@gmx.at> 1.0.2-1
- New upstream release
- Remove DESTDIR correction for install-exec-hook (now upstream)

* Thu Jan  5 2012 Volker Fröhlich <volker27@gmx.at> 1.0.1-1
- Initial package for Fedora
