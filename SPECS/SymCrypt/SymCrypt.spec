%define debug_package %{nil}
Summary:        A core cryptographic library written by Microsoft
Name:           SymCrypt
Version:        103.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt
Source0:        https://github.com/microsoft/SymCrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/smuellerDD/jitterentropy-library/archive/v3.3.1.tar.gz#/jitterentropy-library-3.3.1.tar.gz
BuildRequires:  cmake
%ifarch aarch64
BuildRequires:  clang >= 12.0.1-4
%endif
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-pyelftools

%description
A core cryptographic library written by Microsoft

# Only x86_64 and aarch64 are currently supported
%ifarch x86_64
%define symcrypt_arch AMD64
%define symcrypt_cc gcc
%define symcrypt_cxx g++
%endif

%ifarch aarch64
%define symcrypt_arch ARM64
# Currently SymCrypt ARM64 build requires use of clang
%define symcrypt_cc clang
%define symcrypt_cxx clang++
%endif

%prep
%setup -q
%setup -q -a 1
# Create a symbolic link as if jitterentropy-library has been pulled in as git submodule
rm -rf 3rdparty/jitterentropy-library
ln -s ../jitterentropy-library-3.3.1 3rdparty/jitterentropy-library

%build
SYMCRYPT_BRANCH=main \
SYMCRYPT_COMMIT_HASH=c55c670 \
SYMCRYPT_COMMIT_TIMESTAMP=2023-12-01T15:59:37-08:00 \
cmake   -S . -B bin \
        -DSYMCRYPT_TARGET_ARCH=%{symcrypt_arch} \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_C_COMPILER=%{symcrypt_cc} \
        -DCMAKE_CXX_COMPILER=%{symcrypt_cxx} \
        -DCMAKE_C_FLAGS="-Wno-maybe-uninitialized" \
        -DCMAKE_CXX_FLAGS="-Wno-unused-but-set-variable"

cmake --build bin

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install inc/symcrypt* %{buildroot}%{_includedir}
# Use cp -P to preserve symbolic links
cp -P bin/module/generic/libsymcrypt.so* %{buildroot}%{_libdir}
chmod 755 %{buildroot}%{_libdir}/libsymcrypt.so.%{version}

%check
./bin/exe/symcryptunittest

%files
%license LICENSE
%license NOTICE
%{_libdir}/libsymcrypt.so*
%{_includedir}/*

%changelog
* Thu Dec 28 2023 Maxwell Moyer-McKee <mamckee@microsoft.com> - 103.4.1-1
- Update SymCrypt to v103.4.1 for SymCrypt-OpenSSL provider.

* Mon May 22 2023 Samuel Lee <saml@microsoft.com> - 103.0.1-1
- Update SymCrypt to v103.0.1 for FIPS certification. Run unit tests in check

* Fri Oct 07 2022 Andy Caldwell <andycaldwell@microsoft.com> - 102.0.0-2
- Update `clang` on aarch64 builds to enable `-pie`

* Mon Jun 06 2022 Samuel Lee <saml@microsoft.com> - 102.0.0-1
- Update SymCrypt to v102.0.0 to improve performance of FIPS self-tests

* Tue Apr 05 2022 Cameron Baird <cameronbaird@microsoft.com> - 101.2.0-2
- BuildRequires clang in aarch64 builds

* Tue Mar 29 2022 Samuel Lee <saml@microsoft.com> - 101.2.0-1
- Update SymCrypt to v101.2.0 to include FIPS self-tests, certifiable AES-GCM, and fix aarch64 build

* Mon Feb 14 2022 Samuel Lee <saml@microsoft.com> - 101.0.0-1
- Original version for CBL-Mariner
- Verified license
