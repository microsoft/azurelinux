# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           cjson
Version:        1.7.18
Release: 4%{?dist}
Summary:        Ultralightweight JSON parser in ANSI C

# several files in tests/ are Apache-2.0 but are not packaged
License:        MIT
URL:            https://github.com/DaveGamble/cJSON
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
 
BuildRequires:  gcc
BuildRequires:  cmake

%description
cJSON aims to be the dumbest possible parser that you can get your job
done with. It's a single file of C, and a single header file.
 
%package devel
Summary:        Development files for cJSON
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       cmake-filesystem
  
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use cJSON.
  
%prep
%autosetup -n cJSON-%{version}

%build
%cmake -DENABLE_CJSON_TEST=ON -DENABLE_TARGET_EXPORT=ON
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_libdir}/*.{la,a}

%check
%ctest

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig 

%files
%license LICENSE
%doc README.md
%{_libdir}/libcjson*.so.*
 
%files devel
%doc CHANGELOG.md CONTRIBUTORS.md
%{_libdir}/libcjson.so
%{_libdir}/pkgconfig/libcjson.pc
%{_libdir}/cmake/cJSON/
%{_includedir}/cjson/

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Sep 26 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.18-1
- Update to new upstream version (closes rhbz#2237124)
- Fix rhbz#2277268, closes rhbz#2277269

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Apr 07 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.17.-1
- Update to latest upstream version 1.7.17 (closes rhbz#2255953)
- Fix rhbz#2254647

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 01 2023 Petr Menšík <pemensik@redhat.com> - 1.7.15-1
- Update to 1.7.15
- Export also CMake module

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.14-2
- Adjust license tag, it's MIT and ASL 2.0 (#1905273)
- Replace ldconfig scriplets
- Fix requires:

* Mon Dec 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.14-1
- Initial package for Fedora
