## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond CHECK 1

Name:           ngtcp2
Version:        1.19.0
Release:        %autorelease
Summary:        Implementation of RFC 9000 QUIC protocol

License:        MIT
URL:            https://github.com/ngtcp2/ngtcp2
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz.asc
Source2:        https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf4f3b91474d1eb29889bd0ef7e8403d5d673c366#/tatsuhiro-t.asc
# Release does not contain all parts to build documentation
# https://github.com/ngtcp2/ngtcp2/pull/1404
Source3:        %{url}/raw/refs/tags/v%{version}/doc/mkapiref.py
Source4:        %{url}/raw/refs/tags/v%{version}/doc/source/index.rst
Source5:        %{url}/raw/refs/tags/v%{version}/doc/source/programmers-guide.rst

BuildRequires:  autoconf
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  libev-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  gnupg2

%description
"Call it TCP/2. One More Time."

ngtcp2 project is an effort to implement RFC9000 QUIC protocol.

%package devel
Summary:        The ngtcp2 development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Suggests:       %{name}-crypto-any-devel%{?_isa} = %{version}-%{release}

%description devel
"Call it TCP/2. One More Time."

ngtcp2 project is an effort to implement RFC9000 QUIC protocol.

Development headers and libraries.

%package crypto-gnutls
Summary:        The ngtcp2 GnuTLS crypto provider
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description crypto-gnutls
"Call it TCP/2. One More Time." RFC9000 QUIC protocol.

GnuTLS library provider.

%package crypto-gnutls-devel
Summary:        The ngtcp2 GnuTLS crypto provider headers
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-crypto-gnutls%{?_isa} = %{version}-%{release}
BuildRequires:  gnutls-devel >= 3.7.5
Requires:       gnutls-devel >= 3.7.5
Provides:       %{name}-crypto-any-devel = %{version}-%{release}

%description crypto-gnutls-devel
"Call it TCP/2. One More Time." RFC9000 QUIC protocol.

GnuTLS library provider headers.

%package crypto-ossl
Summary:        The ngtcp2 dependency for OpenSSL
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description crypto-ossl
"Call it TCP/2. One More Time." RFC9000 QUIC protocol.

OpenSSL library provider.

%package crypto-ossl-devel
Summary:        The ngtcp2 dependency for OpenSSL headers
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-crypto-ossl%{?_isa} = %{version}-%{release}
BuildRequires:  openssl-devel >= 3.5.0
Requires:       openssl-devel >= 3.5.0
Provides:       %{name}-crypto-any-devel = %{version}-%{release}

%description crypto-ossl-devel
"Call it TCP/2. One More Time." RFC9000 QUIC protocol.

OpenSSL library provider headers.

%package doc
Summary:        The ngtcp2 API documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
"Call it TCP/2. One More Time." RFC9000 QUIC protocol.

Development API documentation.

%prep
%autosetup -p1
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
install -p -m 755 %{SOURCE3} doc/
install -p -m 644 %{SOURCE4} doc/source/
install -p -m 644 %{SOURCE5} doc/source/


%build
autoreconf -fsi
%configure --with-gnutls --with-openssl --with-libev --disable-static --enable-werror
%make_build
%make_build html

rm -f doc/build/html/.buildinfo


%install
%make_install
# Required on epel9
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}*.la

%check
%if %{with CHECK}
# does not yet compile: https://github.com/ngtcp2/ngtcp2/issues/1673
%make_build check
%endif

%files
%license COPYING
%doc README.rst
#doc SECURITY.md
%doc AUTHORS
%{_libdir}/libngtcp2.so.16*


%files crypto-gnutls
%{_libdir}/libngtcp2_crypto_gnutls.so.8*


%files crypto-ossl
%{_libdir}/libngtcp2_crypto_ossl.so.0*


%files devel
%doc ChangeLog
%{_libdir}/libngtcp2.so
%{_libdir}/pkgconfig/libngtcp2.pc
%{_includedir}/%{name}/
%exclude %{_includedir}/%{name}/ngtcp2_crypto_*.h


%files crypto-gnutls-devel
%{_libdir}/libngtcp2_crypto_gnutls.so
%{_libdir}/pkgconfig/libngtcp2_crypto_gnutls.pc
%{_includedir}/%{name}/ngtcp2_crypto_gnutls.h


%files crypto-ossl-devel
%{_libdir}/libngtcp2_crypto_ossl.so
%{_libdir}/pkgconfig/libngtcp2_crypto_ossl.pc
%{_includedir}/%{name}/ngtcp2_crypto_ossl.h


%files doc
%doc doc/build/html/


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.19.0-3
- Latest state for ngtcp2

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 08 2026 Petr Menšík <pemensik@redhat.com> - 1.19.0-1
- Update to 1.19.0 (rhbz#2424570)

* Mon Nov 24 2025 Petr Menšík <pemensik@redhat.com> - 1.18.0-1
- Update to 1.18.0 (rhbz#2404703)

* Wed Oct 01 2025 Petr Menšík <pemensik@redhat.com> - 1.16.0-1
- Update to 1.16.0 (rhbz#2397791)

* Wed Oct 01 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-8
- Do not recommend crypto devel from main devel

* Wed Oct 01 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-7
- Remove ossl library from main devel package. Keep it just on crypto-ossl-
  devel

* Fri Sep 19 2025 Yanko Kaneti <yaneti@declera.com> - 1.15.1-6
- Fixup crypto-ossl requires typo

* Thu Sep 18 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-5
- Add separate devel packages for crypto backends

* Thu Sep 18 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-4
- Require both crypto backends from devel subpackage

* Thu Sep 18 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-3
- Add OpenSSL subpackage and multiple crypto supports

* Thu Sep 11 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-2
- Remove lib*.la after installation explicitly

* Thu Sep 11 2025 Petr Menšík <pemensik@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Thu Sep 11 2025 Petr Menšík <pemensik@redhat.com> - 1.13.0-1
- Initial spec for 1.13.0 version
## END: Generated by rpmautospec
