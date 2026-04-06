# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without mingw

Name:           liblerc
Version:        4.0.0
Release:        9%{?dist}
Summary:        Library for Limited Error Raster Compression

License:        Apache-2.0
URL:            https://github.com/Esri/lerc
Source0:        https://github.com/Esri/lerc/archive/v%{version}/lerc-%{version}.tar.gz
# Add version suffix to mingw dll
Patch0:         lerc-dllver.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python3-devel

%if %{with mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++
%endif

%description
LERC is an open-source image or raster format which supports rapid encoding and
decoding for any pixel type (not just RGB or Byte). Users set the maximum
compression error per pixel while encoding, so the precision of the original
input image is preserved (within user defined error bounds).


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw32-%{name}
%{summary}.


%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
BuildArch:     noarch

%description -n mingw64-%{name}
%{summary}.
%endif


%prep
%autosetup -p1 -n lerc-%{version}

# Fix line endings
sed -i 's/\r$//' NOTICE README.md doc/MORE.md


%build
# Native build
%cmake
%cmake_build

%if %{with mingw}
# MinGW build
%mingw_cmake
%mingw_make_build
%endif


%install
%cmake_install
%if %{with mingw}
%mingw_make_install
%endif


%files
%license LICENSE
%doc README.md CHANGELOG.md NOTICE
%{_libdir}/libLerc.so.4

%files devel
%doc doc/*
%{_includedir}/Lerc_c_api.h
%{_includedir}/Lerc_types.h
%{_libdir}/libLerc.so
%{_libdir}/pkgconfig/Lerc.pc

%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE
%{mingw32_bindir}/libLerc-4.dll
%{mingw32_includedir}/Lerc_c_api.h
%{mingw32_includedir}/Lerc_types.h
%{mingw32_libdir}/libLerc.dll.a
%{mingw32_libdir}/pkgconfig/Lerc.pc

%files -n mingw64-%{name}
%license LICENSE
%{mingw64_bindir}/libLerc-4.dll
%{mingw64_includedir}/Lerc_c_api.h
%{mingw64_includedir}/Lerc_types.h
%{mingw64_libdir}/libLerc.dll.a
%{mingw64_libdir}/pkgconfig/Lerc.pc
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 21 2022 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Mon Jul 11 2022 Sandro Mani <manisandro@gmail.com> - 3.1-0.3.gitb1de4cd
- Re-enable mingw32 on EL9

* Fri Jun 10 2022 Orion Poplawski <orion@nwra.com> - 3.1-0.2.gitb1de4cd
- Drop mingw for non-x86_64 on EL9

* Fri May 06 2022 Sandro Mani <manisandro@gmail.com> - 3.1-0.1.gitb1de4cd
- Initial package b1de4cd
