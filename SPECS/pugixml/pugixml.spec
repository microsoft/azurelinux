# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global prerel rc

Name:           pugixml
Version:        1.15
Release:        1%{?dist}
Summary:        A light-weight C++ XML processing library
License:        MIT
URL:            https://pugixml.org/
VCS:            git:https://github.com/zeux/%{name}.git

Source:         https://github.com/zeux/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake gcc-c++

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

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}


%prep
%autosetup -p1


%build
%cmake -DPUGIXML_BUILD_TESTS:BOOL=ON
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%doc readme.txt
%license LICENSE.md
%{_libdir}/libpugixml.so.1*

%files devel
%{_libdir}/libpugixml.so
%{_libdir}/cmake/pugixml/
%{_libdir}/pkgconfig/pugixml.pc
%{_includedir}/*.hpp

%files doc
%doc docs/*


%changelog
* Fri Aug 29 2025 Jerry James <loganjerry@gmail.com> - 1.15-1
- Update to 1.15 (rhbz#2241663)
- Change doc subpackage architecture to noarch
- Change Source URL to tarball with the tests included
- Add a %%check script
- Do not glob the library name
- Minor spec file cleanups

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Richard Shaw <hobbes1069@gmail.com> - 1.14-1
- Update to 1.14.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Richard Shaw <hobbes1069@gmail.com> - 1.13-1
- Update to 1.13.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 16 2022 Richard Shaw <hobbes1069@gmail.com> - 1.12.1-1
- Update to 1.12.1, fixes RHBZ#2052866.

* Fri Feb 11 2022 Richard Shaw <hobbes1069@gmail.com> - 1.12-1
- Update to 1.20.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 24 2020 Richard Shaw <hobbes1069@gmail.com> - 1.11.4-1
- Update to 1.11.4.

* Sat Dec 19 2020 Richard Shaw <hobbes1069@gmail.com> - 1.11.3-1
- Update to 1.11.3.

* Thu Nov 26 2020 Richard Shaw <hobbes1069@gmail.com> - 1.11-1
- Update to 1.11.

* Wed Aug 26 2020 Jeff Law <lwa@redhat.com> - 1.10-5
- No longer force C++11 mode

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 15 2019 Richard Shaw <hobbes1069@gmail.com> - 1.10-1
- Update to 1.10.

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
