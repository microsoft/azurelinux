Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libjwt
Version:        1.12.1
Release:        1%{?dist}
Summary:        A JSON Web Token library in C

License:        MPL-2.0
URL:            https://github.com/benmcollins/libjwt
Source0:        https://github.com/benmcollins/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Wire up --without-examples so example binaries (jwtgen, jwtauth) are
# not built; upstream ships the flag but does not honor it in
# Makefile.am. Imported verbatim from Fedora.
Patch0:         without_examples.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel

%description
libjwt is a C library implementing JSON Web Tokens (RFC 7519). It supports
signing and verification using HMAC (HS256/384/512), RSA (RS256/384/512),
ECDSA (ES256/384/512), and RSA-PSS (PS256/384/512) algorithms via OpenSSL,
and uses Jansson for JSON encoding and decoding.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       jansson-devel
Requires:       openssl-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
autoreconf -i


%build
%configure --disable-static --without-examples
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%license LICENSE
%doc README.md
%{_libdir}/libjwt.so.*


%files devel
%doc README.md
%{_includedir}/jwt.h
%{_libdir}/libjwt.so
%{_libdir}/pkgconfig/libjwt.pc


%changelog
* Mon Jun 15 2026 lakarri <lakarri@microsoft.com> - 1.12.1-1
- Initial Azure Linux import from Fedora 44 (license: MIT).
- Required by slurmrestd (Slurm REST API daemon) for JWT-based
  authentication. Tracked via ADO #61504121.
- License verified.
