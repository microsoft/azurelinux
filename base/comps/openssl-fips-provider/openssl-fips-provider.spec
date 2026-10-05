Summary: OpenSSL FIPS provider
Name: openssl-fips-provider
Version: 3.5.8
Release: %autorelease
Epoch: 1
License: Apache-2.0
URL: https://www.openssl.org/
Source0: openssl-%{version}.tar.gz
Source1: openssl-fips-provider.cnf

Requires: openssl-libs%{?_isa} >= 1:3.5.4-13
Requires: openssl-libs%{?_isa} < 1:4.0.0
Requires: /etc/crypto-policies/back-ends/openssl_fips.config
Provides: openssl(fips-provider)
Conflicts: openssl(fips-provider)

BuildRequires: gcc
BuildRequires: g++
BuildRequires: make
BuildRequires: coreutils
BuildRequires: perl-interpreter
BuildRequires: sed
BuildRequires: /usr/bin/cmp
BuildRequires: /usr/bin/pod2man
BuildRequires: perl(Test::Harness)
BuildRequires: perl(Test::More)
BuildRequires: perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(Time::Piece)
BuildRequires: perl(IPC::Cmd)
BuildRequires: perl(Pod::Html)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(FindBin)
BuildRequires: perl(lib)
BuildRequires: perl(File::Compare)
BuildRequires: perl(File::Copy)
BuildRequires: perl(bigint)
BuildRequires: git-core

%description
The OpenSSL FIPS provider supplies FIPS-approved cryptographic
implementations for OpenSSL.

%prep
%autosetup -S git -n openssl-%{version}
sed -i '/^FIPS_VENDOR=/d; /^BUILD_METADATA=/aFIPS_VENDOR=Microsoft Azure Linux' VERSION.dat
grep -Fqx 'FIPS_VENDOR=Microsoft Azure Linux' VERSION.dat

%build
./Configure enable-fips
make -s %{?_smp_mflags}

%check
make test HARNESS_JOBS=8

# Generate the provider configuration after RPM has stripped the installed
# module so its integrity MAC covers the bytes that the package ships.
# fipsinstall receives the buildroot module path for MAC generation, so insert
# the final runtime path immediately below the generated [fips_sect] header.
# Verify both that the directive exists and that it is in the expected section.
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    LD_LIBRARY_PATH=. apps/openssl fipsinstall -ems_check -no_short_mac -rsa_pkcs15_padding_disabled -rsa_sign_x931_disabled -module $RPM_BUILD_ROOT/%{_libdir}/ossl-modules/fips.so -out $RPM_BUILD_ROOT/%{_sysconfdir}/pki/tls/openssl.d/fipsmodule.cnf \
    sed -i '/^\\[fips_sect\\]$/a module = %{_libdir}/ossl-modules/fips.so' $RPM_BUILD_ROOT/%{_sysconfdir}/pki/tls/openssl.d/fipsmodule.cnf \
    grep -Fqx 'module = %{_libdir}/ossl-modules/fips.so' $RPM_BUILD_ROOT/%{_sysconfdir}/pki/tls/openssl.d/fipsmodule.cnf \
    sed -n '/^\\[fips_sect\\]$/{n;p;q;}' $RPM_BUILD_ROOT/%{_sysconfdir}/pki/tls/openssl.d/fipsmodule.cnf | grep -Fqx 'module = %{_libdir}/ossl-modules/fips.so' \
%{nil}

%install
install -Dpm0755 providers/fips.so \
    %{buildroot}%{_libdir}/ossl-modules/fips.so
install -d %{buildroot}%{_sysconfdir}/pki/tls/openssl.d
install -Dpm0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/pki/tls/azl-openssl-fips-provider.d/openssl.cnf

%files
%license LICENSE.txt
%{_libdir}/ossl-modules/fips.so
%{_sysconfdir}/pki/tls/openssl.d/fipsmodule.cnf
%config %{_sysconfdir}/pki/tls/azl-openssl-fips-provider.d/openssl.cnf

%changelog
%autochangelog
