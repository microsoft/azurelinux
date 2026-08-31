# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_check 1

Name:    libb2
Summary: C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Version: 0.98.1
Release: 14%{?dist}
License: CC0-1.0 OR Apache-1.0 OR Apache-2.0
URL:     https://blake2.net/
Source0: https://github.com/BLAKE2/libb2/archive/v%{version}/libb2-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make

%description
C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp.

BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2,
and SHA-3, yet is at least as secure as the latest standard SHA-3.

%package        devel
Summary:        Development files for the Blake2 library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{summary}.

%prep
%autosetup -n libb2-%{version}

# Force default Fedora cflags
sed -e 's|CFLAGS=-O3|CFLAGS="%{optflags}"|g' -i configure.ac
autoreconf -ivf

%build
%configure --disable-silent-rules --enable-static=no --enable-native=no
%make_build

%if 0%{with_check}
%check
make check
%endif

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libb2.so.1
%{_libdir}/libb2.so.1.*

%files devel
%{_libdir}/libb2.so
%{_libdir}/pkgconfig/libb2.pc
%{_includedir}/blake2.h

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.98.1-1
- Update to latest tagged version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.98-4.20171225git60ea749
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.98-3.20171225git60ea749
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.98-2.20171225git60ea749
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.98-1.20171225git60ea749
- First RPM
