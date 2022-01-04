%define debug_package %{nil}
Summary:        The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations
Name:           scossl
Version:        0.1
Release:        1%{?dist}
License:        MIT License
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt-OpenSSL
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  symcrypt

%description
The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations

%prep

%setup -n microsoft-SymCrypt-OpenSSL-ccdc1d9

%build
ls /usr/lib/
cp /usr/lib/libsymcrypt.so ./
mkdir bin
cd bin

%ifarch aarch64
cmake .. -DOPENSSL_ROOT_DIR=/usr/local/ssl -DCMAKE_TOOLCHAIN_FILE=../cmake-toolchain/LinuxUserMode-ARM64.cmake
%else
cmake .. -DOPENSSL_ROOT_DIR=/usr/local/ssl -DCMAKE_TOOLCHAIN_FILE=../cmake-toolchain/LinuxUserMode-AMD64.cmake
%endif
cmake --build .

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install bin/SymCryptEngine/dynamic/libsymcryptengine.so %{buildroot}%{_libdir}/
install SymCryptEngine/inc/scossl.h %{buildroot}%{_includedir}

%files
%license LICENSE
%{_libdir}/libsymcryptengine.so
%{_includedir}/scossl.h

%changelog
* Mon Jan 01 2022 Spencer Nofzinger <spnofzin@microsoft.com> - 0.1-1
- Initial CBL-Mariner import