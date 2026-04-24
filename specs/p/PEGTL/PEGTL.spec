# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package   %{nil}

Name:           PEGTL
Version:        2.8.3
Release: 14%{?dist}
Summary:        Parsing Expression Grammar Template Library
License:        MIT
URL:            https://github.com/taocpp/%{name}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch:          PEGTL-compiler-warning.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
# Faster than make, with no disadvantages
BuildRequires:  ninja-build

%description
The Parsing Expression Grammar Template Library (PEGTL) is a zero-dependency
C++11 header-only library for creating parsers according to a Parsing
Expression Grammar (PEG).

%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel

%description devel
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%autosetup -p1

%build
# Default cmake path is /usr/share/pegtl/cmake. This is OK, but we prefer
# /usr/share/cmake/pegtl to reduce clutter in /usr/share.
%cmake \
    -DPEGTL_INSTALL_INCLUDE_DIR:PATH='%{_includedir}' \
    -DPEGTL_INSTALL_DOC_DIR:PATH='%{_pkgdocdir}' \
    -DPEGTL_INSTALL_CMAKE_DIR:PATH='%{_datadir}/cmake/pegtl' \
    -GNinja
%cmake_build

%install
%cmake_install
# The default installation of documentation is useless: it just installs the
# LICENSE file where we do not want it. Remove its handiwork and deal with
# documentation manually.
rm -rv %{buildroot}%{_pkgdocdir}

%check
%ctest

%files devel
%doc README.md doc/
%license LICENSE
%{_includedir}/tao/pegtl.hpp
%{_includedir}/tao/pegtl/
%{_datadir}/cmake/pegtl/

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-11
- Switch to CMake, run tests, and ship CMake files
- Use a better source URL

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 03 2020 Attila Lakatos <alakatos@redhat.com> - 2.8.3-1
- Update to 2.8.3
Resolves: rhbz#1742557

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Orion Poplawski <orion@nwra.com> - 2.8.1-1
- Update to 2.8.1

* Wed Jul 31 2019 Daniel Kopecek <dkopecek@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Daniel Kopecek <dkopecek@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Daniel Kopecek <dkopecek@redhat.com> - 1.3.1-1
- Initial package
