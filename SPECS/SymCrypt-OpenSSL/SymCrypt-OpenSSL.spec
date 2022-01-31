Summary:        The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations
Name:           SymCrypt-OpenSSL
Version:        101.0.0
Release:        1%{?dist}
License:        MIT License
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt-OpenSSL
#Source0:       https://github.com/microsoft/SymCrypt-OpenSSL/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define debug_package %{nil}
BuildRequires:  SymCrypt
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations

%prep
%setup -q

%build
mkdir bin; cd bin

cmake   .. \
        -DOPENSSL_ROOT_DIR="%{_prefix}/local/ssl" \
        -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
        -DCMAKE_INSTALL_INCLUDEDIR=%{buildroot}%{_includedir} \
%ifarch x86_64
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-AMD64.cmake" \
%endif
%ifarch aarch64
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-ARM64.cmake" \
%endif
        -DCMAKE_BUILD_TYPE=Release

cmake --build .

%install
cd bin
cmake --build . --target install

%files
%license LICENSE
%{_libdir}/engines-1.1/symcryptengine.so
%{_includedir}/scossl.h

%changelog
* Mon Jan 31 2022 Samuel Lee <saml@microsoft.com> - 101.0.0-1
- Original version for CBL-Mariner