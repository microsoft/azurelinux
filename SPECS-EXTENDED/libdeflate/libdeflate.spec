Summary:        Fast implementation of DEFLATE, gzip, and zlib

Name:           libdeflate
Version:        1.22
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ebiggers/libdeflate
Source0:        https://github.com/ebiggers/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires: zlib-devel

%description
libdeflate is a library for fast, whole-buffer DEFLATE-based compression and
decompression, supporting DEFLATE, gzip, and zlib.

%package devel
Summary:        Development files for libdeflate
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libdeflate.

%package utils
Summary:        Binaries from libdeflate
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Binaries from libdeflate.


%prep
%autosetup

%build
cmake_opts="\
    -DLIBDEFLATE_BUILD_STATIC_LIB:BOOL=OFF \
    -DLIBDEFLATE_BUILD_SHARED_LIB:BOOL=ON \
    -DLIBDEFLATE_COMPRESSION_SUPPORT:BOOL=ON \
    -DLIBDEFLATE_DECOMPRESSION_SUPPORT:BOOL=ON \
    -DLIBDEFLATE_ZLIB_SUPPORT:BOOL=ON \
    -DLIBDEFLATE_GZIP_SUPPORT:BOOL=ON \
    -DLIBDEFLATE_FREESTANDING:BOOL=OFF \
    -DLIBDEFLATE_BUILD_GZIP:BOOL=ON \
    -DLIBDEFLATE_BUILD_TESTS:BOOL=ON \
    -DLIBDEFLATE_USE_SHARED_LIBS:BOOL=ON"

%cmake $cmake_opts
%cmake_build 

%install
%cmake_install


%files
%doc NEWS.md README.md
%license COPYING
%{_libdir}/libdeflate.so.0

%files devel
%{_includedir}/libdeflate.h
%{_libdir}/libdeflate.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/libdeflate/

%files utils
%{_bindir}/libdeflate-gzip
%{_bindir}/libdeflate-gunzip


%changelog
* Mon Oct 14 2024 Jyoti kanase <v-jykanase@microsoft.com> - 1.22-1
- Update to version 1.22
- License verified

* Wed Jan 18 2023 Suresh Thelkar <sthelkar@microsoft.com> - 1.9-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Nick Black <dankamongmen@gmail.com> 1.9-2
- install new pkgconfig file

* Thu Jan 13 2022 Nick Black <dankamongmen@gmail.com> 1.9-1
- new upstream 1.9

* Tue Nov 23 2021 Nick Black <dankamongmen@gmail.com> 1.8-1
- Initial import (#2023061)
