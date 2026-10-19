# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libjwt
Version:        1.12.1
Release: 21%{?dist}
Summary:        A Javascript Web Token library in C

License:        MPL-2.0
URL:            https://github.com/benmcollins/libjwt
Source0:        https://github.com/benmcollins/libjwt/archive/v%{version}.tar.gz

Patch0:         without_examples.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  jansson-devel
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel

%description
A Javascript Web Token library in C

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup
autoreconf -i

%build
%configure --disable-static --without-examples
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%files
%license LICENSE
%doc *.md
%{_libdir}/*.so.1*

%files devel
%doc *.md
%{_includedir}/jwt.h
%{_libdir}/libjwt.so
%{_libdir}/pkgconfig/libjwt.pc

%changelog
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
