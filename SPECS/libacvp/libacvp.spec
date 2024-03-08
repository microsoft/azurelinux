Summary:        A library that implements the client-side of the ACVP protocol
Name:           libacvp
Version:        2.0.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries
URL:            https://github.com/cisco/libacvp
Source0:        https://github.com/cisco/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  curl-devel
BuildRequires:  gcc
BuildRequires:  make

Requires:       %{name}-libs = %{version}-%{release}

%description
A library that implements the client-side of the ACVP protocol.

%package app
Summary:        LibACVP application for OpenSSL
Group:          Applications/System
BuildRequires:  openssl-devel

%description app
This app provides the glue between the OpenSSL module under test
and the library itself.

%package devel
Summary:        LibACVP application for OpenSSL
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for LibACVP.

%package libs
Summary:        LibACVP application for OpenSSL
Group:          Applications/System

%description libs
LibACVP shared libraries.

%prep
%autosetup -p1

%build
./configure \
    --disable-static \
    --prefix=%{_prefix} \
    --with-libcurl-dir=%{_prefix} \
    --with-ssl-dir=%{_prefix} \
    CFLAGS="-pthread -DACVP_NO_RUNTIME -DOPENSSL_KWP -DOPENSSL_KDF_SUPPORT -O2 -g -fcommon" \
    LIBS="-ldl"
make clean
make CC=gcc

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print

%files
%license LICENSE
%doc %{_datadir}/README.md

%files app
%{_bindir}/acvp_app

%files devel
%{_includedir}/acvp/*
%{_libdir}/libacvp.so

%files libs
%{_libdir}/libacvp.so.*

%changelog
* Tue Mar 05 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-1
- Update to version 2.0.1.
- Split out -devel and -libs subpackages.
- Disabled static library build.
- Disabled offline mode.

* Wed Oct 05 2022 Andy Caldwell <andycaldwell@microsoft.com> - 1.3.0-3
- Enable building without `glibc-static`

* Wed Nov 17 2021 Andrew Phelps <anphel@microsoft.com> - 1.3.0-2
- Set -fcommon to compile with gcc11

* Fri Jul 30 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.3.0-1
- Update to version 1.3.0
- Add patch to support OpenSSL ACVP testing.

* Mon Feb 08 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.2.0-1
- Original version for CBL-Mariner. License verified.
