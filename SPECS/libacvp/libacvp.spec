Summary:        A library that implements the client-side of the ACVP protocol
Name:           libacvp
Version:        1.2.0
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://github.com/cisco/libacvp
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Source0:      https://github.com/cisco/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel

Requires:       openssl-libs

%description
A library that implements the client-side of the ACVP protocol.

%prep
%autosetup

%build
./configure \
    --prefix=%{_prefix} \
    --enable-offline \
    CFLAGS="-pthread" \
    LIBS="-ldl"
make clean
make CC=gcc

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}/*

%files
%license LICENSE
%{_datadir}/README.md
%{_libdir}/libacvp.a
%{_includedir}/acvp/*
%{_bindir}/acvp_app

%changelog
* Fri Jan 29 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.2.0-1
- First version. License verified.