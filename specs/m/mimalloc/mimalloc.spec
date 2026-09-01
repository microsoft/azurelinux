# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

Name:           mimalloc
Version:        2.2.3
Release:        2%{?dist}
Summary:        A general purpose allocator with excellent performance

License:        MIT
URL:            https://github.com/microsoft/mimalloc
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Fix ppc64le build
# Patch0:         3966953b7f0f11d2ec33097c5da4356d5b7db7e8.patch
# Patch1:         cc3c14f2ed374f908e60a3bf29c1dff84fc8cfc2.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
mimalloc (pronounced "me-malloc")
is a general purpose allocator with excellent performance characteristics.
Initially developed by Daan Leijen for the run-time systems.

%package devel
Summary:        Development environment for %name
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development package for mimalloc.

%prep
%autosetup -p1
# Remove unneded binary from sources
rm -rf bin


%build
%cmake \
    -DMI_BUILD_OBJECT=OFF \
    -DMI_OVERRIDE=OFF \
    -DMI_INSTALL_TOPLEVEL=ON \
    -DMI_BUILD_STATIC=OFF \
    -DMI_BUILD_TESTS=OFF \
    -DMI_OPT_ARCH=OFF \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc readme.md
%{_libdir}/lib%{name}.so.2*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 31 2025 Vasiliy Glazov <vascom2@gmail.com> - 2.2.3-1
- Update to 2.2.3

* Sat Jan 25 2025 Christoph Erhardt <fedora@sicherha.de> - 2.1.9-3
- Disable architecture-specific optimizations

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Vasiliy Glazov <vascom2@gmail.com> - 2.1.9-1
- Update to 2.1.9

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Vasiliy Glazov <vascom2@gmail.com> - 2.1.7-1
- Update to 2.1.7

* Wed Apr 24 2024 Vasiliy Glazov <vascom2@gmail.com> - 2.1.4-1
- Update to 2.1.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 12 2023 Vasiliy Glazov <vascom2@gmail.com> - 2.1.2-1
- Update to 2.1.2

* Wed Apr 05 2023 Vasiliy Glazov <vascom2@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Fri Mar 31 2023 Vasiliy Glazov <vascom2@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 28 2022 Vasiliy Glazov <vascom2@gmail.com> - 2.0.9-1
- Update to 2.0.9

* Mon Nov 14 2022 Vasiliy Glazov <vascom2@gmail.com> - 2.0.7-1
- Update to 2.0.7

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 15 2022 Vasiliy Glazov <vascom2@gmail.com> - 2.0.6-1
- Update to 2.0.6

* Tue Feb 15 2022 Vasiliy Glazov <vascom2@gmail.com> - 2.0.5-1
- Update to 2.0.5

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Vasiliy Glazov <vascom2@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Wed Sep 29 2021 Vasiliy Glazov <vascom2@gmail.com> - 2.0.2-2
- Clean spec to follow packaging guidelines

* Wed Sep 29 2021 Vasiliy Glazov <vascom2@gmail.com> - 2.0.2-1
- Initial packaging for Fedora
