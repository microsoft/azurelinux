Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libjwt
Version:        1.12.1
Release:        1%{?dist}
Summary:        A JSON Web Token library in C

License:        MPL-2.0
URL:            https://github.com/benmcollins/libjwt
Source0:        https://github.com/benmcollins/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
%autosetup -n %{name}-%{version}
autoreconf -i


%build
%configure --disable-static --without-examples
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# --without-examples does not actually disable example install in
# libjwt 1.12.1; remove the example binaries explicitly.
rm -f %{buildroot}%{_bindir}/jwtgen %{buildroot}%{_bindir}/jwtauth


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
* Wed Jun 10 2026 lakarri <lakarri@microsoft.com> - 1.12.1-1
- Initial Azure Linux import from Fedora rawhide (license: MPL-2.0).
- Required by slurmrestd (Slurm REST API daemon) for JWT-based
  authentication. Tracked via ADO #61504121.
- License verified.
