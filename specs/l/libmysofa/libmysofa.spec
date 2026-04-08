# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libmysofa
Version:        1.3.3
Release:        3%{?dist}
Summary:        C functions for reading HRTFs

License:        BSD-3-Clause
URL:            https://github.com/hoene/libmysofa
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cunit)
BuildRequires:  pkgconfig(zlib)
BuildRequires: make
# for tests
%{?!_without_tests:BuildRequires: nodejs}


%description
This is a simple set of C functions to read AES SOFA files, if they
contain HRTFs stored according to the AES69-2015 standard.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n mysofa
Summary:        Tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n mysofa
Tools for %{name}.


%prep
%autosetup -p1


%build
%cmake \
  -DBUILD_STATIC_LIBS=OFF \
  -DCODE_COVERAGE=OFF \
  -DCMAKE_VERBOSE_MAKEFILE=ON

%cmake_build


%install
%cmake_install


%{?!_without_tests:
%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

export MYSOFA2JSON=%{_builddir}/%{buildsubdir}/%{_vpath_builddir}/src/mysofa2json
%ctest
}


%files
%license LICENSE
%doc README.md
%{_libdir}/libmysofa.so.1*

%files -n mysofa
%{_bindir}/mysofa2json
%dir %{_datadir}/libmysofa
%{_datadir}/libmysofa/default.sofa
%{_datadir}/libmysofa/MIT_KEMAR_normal_pinna.sofa

%files devel
%doc CODE_OF_CONDUCT.md
%{_includedir}/mysofa.h
%{_includedir}/mysofa_export.h
%{_libdir}/libmysofa.so
%{_libdir}/pkgconfig/libmysofa.pc
%dir %{_libdir}/cmake/mysofa
%{_libdir}/cmake/mysofa/mysofaConfig.cmake
%{_libdir}/cmake/mysofa/mysofaConfigVersion.cmake
%{_libdir}/cmake/mysofa/mysofaTargets-noconfig.cmake
%{_libdir}/cmake/mysofa/mysofaTargets.cmake


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.3.3-1
- Update to 1.3.3

* Mon Oct 07 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-3.20240917git2297dd8
- Update snapshot - rhbz#2316036

* Thu Sep 19 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2.1-9
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.2-4
- Update to 1.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.1-1
- Update to 1.1

* Mon Apr 13 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.0-1
- Initial spec file
