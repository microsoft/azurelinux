Summary:        A light-weight C++ XML processing library
Name:           pugixml
Version:        1.11.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment
URL:            https://pugixml.org
#Source0:       https://github.com/zeux/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc

%description
pugixml is a light-weight C++ XML processing library.
It features:
- DOM-like interface with rich traversal/modification capabilities
- Extremely fast non-validating XML parser which constructs the DOM tree from
  an XML file/buffer
- XPath 1.0 implementation for complex data-driven tree queries
- Full Unicode support with Unicode interface variants and automatic encoding
  conversions

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for package %{name}

%prep
%setup -q

%build
mkdir build && cd build
%cmake .. -DBUILD_TESTS:BOOL=ON
%make_build

%check
make check -C build

%install
%make_install -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE.md
%doc readme.txt
%{_libdir}/libpugixml.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/pugiconfig.hpp
%{_includedir}/pugixml.hpp
%{_libdir}/libpugixml.so
%{_libdir}/cmake/pugixml
%{_libdir}/pkgconfig/pugixml.pc

%changelog
* Thu Feb 03 2022 Minghe Ren <mingheren@microsoft.com> - 1.11.4-1
- Update to Version 1.11.4

* Mon Oct 12 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.10-2
- License verified
- Update Source0

* Wed Feb 12 2020 Nick Bopp <nichbop@microsoft.com> - 1.10-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- Update to 1.10

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 06 2018 Richard Shaw <hobbes1069@gmail.com> - 1.9-1
- Update to 1.9.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Richard Shaw <hobbes1069@gmail.com> - 1.8-1
- Update to latest upstream release.

* Tue Sep 27 2016 Richard Shaw <hobbes1069@gmail.com> - 1.7-3
- Add build flags for c++11 for mkvtoolnix.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Richard Shaw <hobbes1069@gmail.com> - 1.7-1
- Update to latest upstream release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Richard Shaw <hobbes1069@gmail.com> - 1.6-1
- Update to latest upstream release.

* Tue Feb  3 2015 Richard Shaw <hobbes1069@gmail.com> - 1.5-1
- Update to latest upstream release.

* Wed Sep 03 2014 Orion Poplawski <orion@cora.nwra.com> - 1.4-1
- Update to 1.4
- Split documentation out into -doc sub-package
- Add cmake export information

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan 05 2012 Richard Shaw <hobbes1069@gmail.com> - 1.0-2
- Rebuild for GCC 4.7.0.

* Fri Jul 08 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0-1
- Initial Release
