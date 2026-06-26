Summary:        The SymCrypt engine for OpenSSL (SCOSSL) allows the use of OpenSSL with SymCrypt as the provider for core cryptographic operations
Name:           SymCrypt-OpenSSL
Version:        1.9.6
Release:        %autorelease
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt-OpenSSL
Source0:        https://github.com/microsoft/SymCrypt-OpenSSL/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0001:      0001-register-symcrypt-provider-for-config-drop-in.patch
Patch0002:      0002-skip-sha1-signature-tests-disabled-by-crypto-policy.patch
# The v1.9.6 release tag shipped without bumping the CMake project version, so
# the provider reports 1.9.5 via OSSL_PROV_PARAM_VERSION. Correct it downstream.
Patch0003:      0003-bump-project-version-to-match-release-tag.patch

BuildRequires:  openssl-devel
BuildRequires:  openssl-devel-engine
BuildRequires:  SymCrypt >= 103.8.0
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

Requires:       SymCrypt >= 103.8.0
Requires:       openssl-libs

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
%autosetup -p1

%build
%cmake   \
        -DKEYSINUSE_ENABLED=1 \
        -DOPENSSL_ROOT_DIR="%{_prefix}/local/ssl" \
        -DSYMCRYPT_ROOT_DIR=%{buildroot}%{_includedir}/.. \
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-%{symcrypt_arch}.cmake" \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo

%cmake_build

%install
mkdir -p %{buildroot}%{_libdir}/engines-3/
mkdir -p %{buildroot}%{_libdir}/ossl-modules/
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/openssl.d/
mkdir -p %{buildroot}%{_localstatedir}/log/keysinuse/

# We still install the engine for backwards compatibility with legacy applications. Callers must
# explicitly load the engine to use it. It will be removed in a future release.
install %{__cmake_builddir}/SymCryptEngine/dynamic/symcryptengine.so %{buildroot}%{_libdir}/engines-3/symcryptengine.so
install %{__cmake_builddir}/SymCryptProvider/symcryptprovider.so %{buildroot}%{_libdir}/ossl-modules/symcryptprovider.so
install SymCryptEngine/inc/e_scossl.h %{buildroot}%{_includedir}/e_scossl.h
install SymCryptProvider/symcrypt_prov.cnf %{buildroot}%{_sysconfdir}/pki/tls/openssl.d/symcrypt_prov.cnf

%check
# Run in a subshell so the exit code of the test does not affect the main shell's exit code.
# This is important because the entire section is wrapped in a script by rpmbuild itself.
# The test is run twice: once with the default provider and once with the SymCrypt provider.
# The SHA-1 RSA sign/verify cases are removed by Patch1, since SHA-1 signatures
# are disabled by the default crypto policy on Azure Linux.
(
        set -e
        ./%{__cmake_builddir}/SslPlay/SslPlay
        ./%{__cmake_builddir}/SslPlay/SslPlay --provider-path ./%{__cmake_builddir}/SymCryptProvider/ --provider symcryptprovider --no-engine
)

%files
%license LICENSE
%{_libdir}/engines-3/symcryptengine.so
%{_libdir}/ossl-modules/symcryptprovider.so
%{_includedir}/e_scossl.h
%config %{_sysconfdir}/pki/tls/openssl.d/symcrypt_prov.cnf

# The log directory for certsinuse logging has permissions set to 1733.
# These permissions are a result of a security review to mitigate potential risks:
# - Group and others are denied read access to prevent user-level code from inferring
#   details about other running applications and their certsinuse usage.
# - All users have write and execute permissions to create new log files and to
#   check file attributes (e.g., to ensure a log file hasn't been tampered with or
#   replaced by a symlink).
# - The sticky bit is set to prevent malicious users from deleting the log files
#   and interfering with certsinuse alerting mechanisms.
%dir %attr(1733, root, root) %{_localstatedir}/log/keysinuse/

%changelog
%autochangelog
