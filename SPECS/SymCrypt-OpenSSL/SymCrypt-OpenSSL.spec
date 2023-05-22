Summary:        The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations
Name:           SymCrypt-OpenSSL
Version:        1.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt-OpenSSL
#Source0:       https://github.com/microsoft/SymCrypt-OpenSSL/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  SymCrypt
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations

# Only x86_64 and aarch64 are currently supported
%ifarch x86_64
%define symcrypt_arch AMD64
%endif

%ifarch aarch64
%define symcrypt_arch ARM64
%endif

%prep
%setup -q

%build
mkdir bin; cd bin

cmake   .. \
        -DOPENSSL_ROOT_DIR="%{_prefix}/local/ssl" \
        -DCMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
        -DCMAKE_INSTALL_INCLUDEDIR=%{buildroot}%{_includedir} \
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-%{symcrypt_arch}.cmake" \
        -DCMAKE_BUILD_TYPE=Release

cmake --build .

%install
cd bin
cmake --build . --target install

%check
./bin/SslPlay/SslPlay

%files
%license LICENSE
%{_libdir}/engines-1.1/symcryptengine.so
%{_includedir}/scossl.h

%changelog
* Mon May 22 2023 Samuel Lee <saml@microsoft.com> - 1.3.0-1
- Update SymCrypt-OpenSSL to v1.3.0. Adds support for HMAC and fixes corner RSA-PSS bug. Run smoke test in check

* Mon Jun 06 2022 Samuel Lee <saml@microsoft.com> - 1.2.0-1
- Update SymCrypt-OpenSSL to v1.2.0 to improve performance and fix some corner case bugs

* Tue Mar 29 2022 Samuel Lee <saml@microsoft.com> - 1.1.0-1
- Update SymCrypt-OpenSSL to v1.1.0 to include FIPS self-tests, and fix aarch64 build

* Mon Feb 14 2022 Samuel Lee <saml@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner
- Verified license
