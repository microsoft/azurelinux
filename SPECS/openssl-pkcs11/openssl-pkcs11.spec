# Define the directory where the OpenSSL engines are installed
%global enginesdir %{_libdir}/engines-1.1
Summary:        A PKCS#11 engine for use with OpenSSL
Name:           openssl-pkcs11
Version:        0.4.10
Release:        10%{?dist}
# The source code is LGPLv2+ except eng_back.c and eng_parse.c which are BSD
License:        LGPLv2+ AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/OpenSC/libp11
Source0:        https://github.com/OpenSC/libp11/releases/download/libp11-%{version}/libp11-%{version}.tar.gz
Patch0:         openssl-pkcs11-0.4.10-various-bug-fixes.patch
Patch1:         openssl-pkcs11-0.4.10-search-objects-in-all-matching-tokens.patch
Patch2:         openssl-pkcs11-0.4.10-add-support-pin-source.patch
Patch3:         openssl-pkcs11-0.4.10-set-rsa-flag-ext-pkey.patch
Patch4:         openssl-pkcs11-0.4.10-set-rsa-fips-method-flag.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  openssl >= 1.0.2
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  doxygen
%if %{with_check}
BuildRequires:  procps-ng
BuildRequires:  opensc
BuildRequires:  softhsm
%endif
Requires:       openssl-libs >= 1.0.2
Requires:       p11-kit-trust

# Package renamed from libp11 to openssl-pkcs11 in release 0.4.7-4
Provides:       libp11%{?_isa} = %{version}-%{release}
Obsoletes:      libp11 < 0.4.7-4
# The engine_pkcs11 subpackage is also provided
Provides:       engine_pkcs11%{?_isa} = %{version}-%{release}
Obsoletes:      engine_pkcs11 < 0.4.7-4

# The libp11-devel subpackage was removed in libp11-0.4.7-1, but not obsoleted
# This Obsoletes prevents the conflict in updates by removing old libp11-devel
Obsoletes:      libp11-devel < 0.4.7-4

%description -n openssl-pkcs11
openssl-pkcs11 enables hardware security module (HSM), and smart card support in
OpenSSL applications. More precisely, it is an OpenSSL engine which makes
registered PKCS#11 modules available for OpenSSL applications. The engine is
optional and can be loaded by configuration file, command line or through the
OpenSSL ENGINE API.

# The libp11-devel subpackage was reintroduced in libp11-0.4.7-7 for Fedora

%package -n libp11-devel
Summary:        Files for developing with libp11
Requires:       %{name} = %{version}-%{release}

%description -n libp11-devel
The libp11-devel package contains libraries and header files for
developing applications that use libp11.

%prep
%autosetup -p 1 -n libp11-%{version}

%build
autoreconf -fvi
export CFLAGS="%{optflags}"

%configure --disable-static --enable-api-doc --with-enginesdir=%{enginesdir}

make V=1 %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{enginesdir}
make install DESTDIR=%{buildroot}

# Remove libtool .la files
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{enginesdir}/*.la

# Remove documentation automatically installed by make install
rm -rf %{buildroot}%{_docdir}/libp11/

%check
make check %{?_smp_mflags} || { cat tests/*.log; false; }

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libp11.so.*
%{enginesdir}/*.so

%files -n libp11-devel
%doc examples/ doc/api.out/html/
%{_libdir}/libp11.so
%{_libdir}/pkgconfig/libp11.pc
%{_includedir}/*.h

%changelog
* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.10-10
- Removing 'exit' calls from the '%%check' section.

* Fri Feb 25 2022 Muhammad Falak <mwani@microsoft.caom> - 04.10-9
- Move BR on doxygen out the `%{with_check}` gate to fix build break

* Tue Feb 08 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.4.10-8
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.10-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 27 2020 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-6
- Set RSA_FLAG_FIPS_METHOD for RSA methods (#1827535)

* Mon Feb 03 2020 James Cassell <cyberpear@fedoraproject.org> - 0.4.10-5
- minimization: depend on openssl-libs rather than openssl

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-3
- Added support for "pin-source" within PKCS#11 URI (#1670026)
- Search objects in all matching tokens (#1760751)
- Set flag RSA_FLAG_EXT_PKEY for RSA keys (#1760541)
- Fixed various bugs

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-1
- Added BuildRequires for openssl >= 1.0.2

* Thu Apr 04 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.10-1
- Update to upstream version 0.4.10

* Tue Feb 19 2019 Anderson Sasaki <ansasaki@redhat.com> - 0.4.9-1
- Update to upstream version 0.4.9

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.8-2
- Require OpenSSL >= 1.0.2
- Fixed missing declaration of ERR_get_CKR_code()
- Add support to use EC keys and tests (#1619184)
- Exposed check_fork() API
- Fixed memory leak of RSA objects in pkcs11_store_key()
- Updated OpenSSL license in eng_front.c
- Fixed build for old C dialects
- Allow engine to use private key without PIN
- Require DEBUG to be defined to print debug messages
- Changed package description (#1614699)

* Mon Aug 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.8-1
- Update to 0.4.8-1
- RSA key generation on the token
- RSA-OAEP and RSA-PKCS encryption support
- RSA-PSS signature support
- Support for OpenSSL 1.1.1 beta
- Removed support for OpenSSL 0.9.8
- Various bug fixes and enhancements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-7
- Reintroduce libp11-devel subpackage to Fedora (#1583719)

* Tue Mar 13 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-6
- Obsolete libp11-devel to fix update

* Tue Mar 06 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-5
- Fixed broken Obsoletes

* Thu Mar 01 2018 Anderson Sasaki <ansasaki@redhat.com> - 0.4.7-4
- Package renamed from libp11 to openssl-pkcs11
