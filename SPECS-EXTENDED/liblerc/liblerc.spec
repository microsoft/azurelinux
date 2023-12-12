Summary:        Library for Limited Error Raster Compression
Name:           liblerc
Version:        4.0.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/Esri/lerc
Source0:        https://github.com/Esri/lerc/archive/v%{version}/lerc-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python3-devel

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

%prep
%autosetup -p1 -n lerc-%{version}

# Fix line endings
sed -i 's/\r$//' NOTICE README.md doc/MORE.md


%build
# Native build
%cmake
%cmake_build


%install
%cmake_install

%check
# Run your C++ program
g++ -o test src/LercTest/main.cpp -L. -lLerc
./test

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

%changelog
* Wed Aug 09 2023 Archana Choudhary <archana1@microsoft.com> - 4.0.0-3
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Remove mingw execution blocks
- License verified

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
