Summary:        Fast implementation of DEFLATE, gzip, and zlib
Name:           libdeflate
Version:        1.9
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ebiggers/libdeflate
Source0:        https://github.com/ebiggers/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make


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
sed -r -i 's/-O2 -fomit-frame-pointer -std=c99/-std=c99/' Makefile

%build
%make_build CFLAGS="%{optflags} -fpic -pie -g" USE_SHARED_LIB=1 LIBDIR=%{_libdir} PREFIX=%{_prefix}

%install
%make_install CFLAGS="%{optflags} -fpic -pie -g" USE_SHARED_LIB=1 LIBDIR=%{_libdir} PREFIX=%{_prefix}
rm %{buildroot}/%{_libdir}/*.a

%files
%doc NEWS.md README.md
%license COPYING
%{_libdir}/libdeflate.so.0

%files devel
%{_includedir}/libdeflate.h
%{_libdir}/libdeflate.so
%{_libdir}/pkgconfig/*

%files utils
%{_bindir}/libdeflate-gzip
%{_bindir}/libdeflate-gunzip

%changelog
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
