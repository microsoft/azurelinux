# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Port of libtls from LibreSSL to OpenSSL
Name:           libretls
Version:        3.8.1
Release:        6%{?dist}
# libretls itself is ISC but uses other source codes, breakdown:
# BSD-3-Clause: compat/strsep.c
# MIT: compat/timegm.c
# LicenseRef-Fedora-Public-Domain: compat/{{explicit_bzero,ftruncate,pread,pwrite}.c,chacha_private.h}
License:        ISC AND BSD-3-Clause AND MIT AND LicenseRef-Fedora-Public-Domain
URL:            https://git.causal.agency/libretls/about/
Source0:        https://causal.agency/libretls/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel >= 1.1.1b
BuildRequires:  man

%description
LibreTLS is a port of libtls from LibreSSL to OpenSSL. OpenBSD's libtls is a
new TLS library, designed to make it easier to write foolproof applications.

%package devel
Summary:        Development files for libretls
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libretls-devel package contains libraries and header files for developing
applications that use libtls.

%if 0%{!?_without_static:1}
%package static
Summary:        Static library for libretls
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libretls-static package includes static libraries of libretls. Install it
if you need to link statically with libtls.
%endif

%prep
%setup -q

%build
%configure %{?_without_static:--disable-static}
%make_build

%install
%make_install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/libtls.la

# Convert README man page to text file
MANWIDTH=72 man ./README.7 | col -bx > README
touch -c -r README.7 README

# Install README man page as libtls.7
sed -e 's/README 7/libtls 7/g' -i README.7
touch -c -r README README.7
install -D -p -m 0644 README.7 $RPM_BUILD_ROOT%{_mandir}/man7/libtls.7

%ldconfig_scriptlets

%files
%doc README
%{_libdir}/libtls.so.28*
%{_mandir}/man7/libtls.7*

%files devel
%{_libdir}/libtls.so
%{_libdir}/pkgconfig/libtls.pc
%{_includedir}/tls.h
%{_mandir}/man3/tls_*.3*

%if 0%{!?_without_static:1}
%files static
%{_libdir}/libtls.a
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 05 2023 Robert Scheck <robert@fedoraproject.org> 3.8.1-1
- Upgrade to 3.8.1 (#2243450)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 24 2022 Robert Scheck <robert@fedoraproject.org> 3.7.0-1
- Upgrade to 3.7.0 (#2156116)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat May 14 2022 Robert Scheck <robert@fedoraproject.org> 3.5.2-1
- Upgrade to 3.5.2 (#2086096)

* Tue Mar 22 2022 Robert Scheck <robert@fedoraproject.org> 3.5.1-1
- Upgrade to 3.5.1 (#2066532)

* Sun Feb 27 2022 Robert Scheck <robert@fedoraproject.org> 3.5.0-1
- Upgrade to 3.5.0 (#2058999)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Robert Scheck <robert@fedoraproject.org> 3.4.2-1
- Upgrade to 3.4.2 (#2027520)

* Fri Oct 15 2021 Robert Scheck <robert@fedoraproject.org> 3.4.1-1
- Upgrade to 3.4.1 (#2014653)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.3.4-2
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 24 2021 Robert Scheck <robert@fedoraproject.org> 3.3.4-1
- Upgrade to 3.3.4 (#1997265)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3p1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Robert Scheck <robert@fedoraproject.org> 3.3.3p1-1
- Upgrade to 3.3.3p1 (#1964579)

* Sat May 08 2021 Robert Scheck <robert@fedoraproject.org> 3.3.3-1
- Upgrade to 3.3.3 (#1958568)

* Wed Apr 21 2021 Robert Scheck <robert@fedoraproject.org> 3.3.2-1
- Upgrade to 3.3.2 (#1952200)

* Sat Mar 06 2021 Robert Scheck <robert@fedoraproject.org> 3.3.1p1-1
- Upgrade to 3.3.1p1

* Fri Mar 05 2021 Robert Scheck <robert@fedoraproject.org> 3.3.1-1
- Upgrade to 3.3.1 (#1935540)
- Initial spec file for Fedora and Red Hat Enterprise Linux
