# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname Imath
%global sover 29
%global pyver_under %(%{python3} -Esc "import sys; sys.stdout.write('{0.major}_{0.minor}'.format(sys.version_info))")

Name:           imath
Version:        3.1.12
Release:        4%{?dist}
Summary:        Library of 2D and 3D vector, matrix, and math operations for computer graphics

License:        BSD-3-Clause
URL:            https://github.com/AcademySoftwareFoundation/Imath
Source0:        https://github.com/AcademySoftwareFoundation/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

Patch0:         imath-python-test.patch

BuildRequires:  cmake
BuildRequires:  gcc gcc-c++
BuildRequires:  make
BuildRequires:  boost-devel
BuildRequires:  python3-devel
# For documentation generation
BuildRequires:  doxygen
BuildRequires:  python3-sphinx
BuildRequires:  python3-breathe

%description
Imath is a basic, light-weight, and efficient C++ representation of 2D and 3D
vectors and matrices and other simple but useful mathematical objects,
functions, and data types common in computer graphics applications, including
the “half” 16-bit floating-point type.


%package -n python3-%{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Python module for Imath

%description -n python3-%{name}
%{summary}.


%package devel
Summary:        Development files for Imath
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-%{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       python3-devel

%description devel
%{summary}.


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%cmake  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DPYTHON=ON \
		-DDOCS=ON \
		-DINSTALL_DOCS=OFF \
		--trace-source=docs/CMakeLists.txt

%cmake_build


%install
%cmake_install

# Fixup documentation so it can get installed correctly in imath-devel
#rm -rf %{__cmake_builddir}/docs/sphinx/.{doctrees,buildinfo}
#mv %{__cmake_builddir}/docs/sphinx ./html


%check
%ctest


%files
%license LICENSE.md
%doc CHANGES.md CODE_OF_CONDUCT.md CONTRIBUTING.md CONTRIBUTORS.md README.md SECURITY.md
%{_libdir}/libImath-3_1.so.%{sover}*

%files -n python3-%{name}
%{_libdir}/libPyImath_Python%{pyver_under}-3_1.so.%{sover}*
%{python3_sitearch}/imath.so
%{python3_sitearch}/imathnumpy.so

%files devel
#doc html/
%{_includedir}/Imath/
%{_libdir}/pkgconfig/Imath.pc
%{_libdir}/pkgconfig/PyImath.pc
%{_libdir}/cmake/Imath/
%{_libdir}/libImath.so
%{_libdir}/libImath-3_1.so
%{_libdir}/libPyImath_Python%{pyver_under}-3_1.so


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.1.12-3
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 Richard Shaw <hobbes1069@gmail.com> - 3.1.12-1
- Update to 3.1.12.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 3.1.11-2
- Rebuilt for Python 3.13

* Fri Mar 15 2024 Richard Shaw <hobbes1069@gmail.com> - 3.1.11-1
- Update to 3.1.11.

* Sat Feb 10 2024 Richard Shaw <hobbes1069@gmail.com> - 3.1.10-1
- Update to 3.1.10.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 3.1.9-4
- Rebuilt for Boost 1.83

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 3.1.9-2
- Rebuilt for Python 3.12

* Thu Jun 01 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.9-1
- Update to 3.1.9.

* Mon May 29 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.8-1
- Update to 3.1.8.

* Mon Mar 20 2023 Richard Shaw <hobbes1069@gmail.com> - 3.1.7-1
- Update to 3.1.7.
- Update license to SPDX identifier.

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 3.1.6-3
- Rebuilt for Boost 1.81

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Richard Shaw <hobbes1069@gmail.com> - 3.1.6-1
- Update to 3.1.6.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.1.5-3
- Rebuilt for Python 3.11

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 3.1.5-2
- Rebuilt for Boost 1.78

* Fri Apr 15 2022 Richard Shaw <hobbes1069@gmail.com> - 3.1.5-1
- Update to 3.1.5.

* Sun Jan 23 2022 Richard Shaw <hobbes1069@gmail.com> - 3.1.4-1
- Update to 3.1.4.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 24 2021 Richard Shaw <hobbes1069@gmail.com> - 3.1.3-1
- Update to 3.1.3.

* Wed Aug 11 2021 Josef Ridky <jridky@redhat.com> - 3.1.2-1
- New upstream release 3.1.2

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 3.0.2-6
- Rebuilt for Boost 1.76

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.0.2-4
- Rebuilt for Python 3.10

* Thu May 27 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.2-3
- Add main package as dependency to python package.

* Tue May 25 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.2-2
- Update spec per reviewer comments.

* Thu May 20 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.2-1
- Update to 3.0.2.

* Wed Apr 07 2021 Richard Shaw <hobbes1069@gmail.com> - 3.0.1-1
- Initial packaging.
