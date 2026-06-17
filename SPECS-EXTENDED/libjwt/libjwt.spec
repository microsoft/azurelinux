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
BuildRequires:  check-devel
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


%check
%make_build check


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

* Fri Jun 12 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.1-22
- Rebuilt for openssl 4.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1.12.1-18
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Apr 13 2024 Miroslav Suchý <msuchy@redhat.com> - 1.12.1-16
- convert license to SPDX

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.12.1-9
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 18 2021 Philip Kovacs <pkfed@fedoraproject.org> - 1.12.1-7
- Remove examples from build

* Tue Apr 13 2021 Philip Kovacs <pkfed@fedoraproject.org> - 1.12.1-6
- Fix canonical changelog dates

* Tue Apr 13 2021 Philip Kovacs <pkfed@fedoraproject.org> - 1.12.1-5
- Build for EPEL7/8

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 7 2020 Jared K. Smith <jsmith@fedoraproject.org> - 1.12.1-3
- More minor fixes for package review

* Tue Nov 3 2020 Jared K. Smith <jsmith@fedoraproject.org> - 1.12.1-2
- Update dependencies for package review

* Thu Oct 29 2020 Jared K. Smith <jsmith@fedoraproject.org> - 1.12.1-1
- Initial packaging
