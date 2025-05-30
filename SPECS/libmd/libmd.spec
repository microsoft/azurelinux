Summary:        Library that provides message digest functions from BSD systems
Name:           libmd
Version:        1.1.0
Release:        6%{?dist}
# Breakdown in COPYING file of libmd release tarball
License:        BSD-2-Clause AND BSD-3-Clause AND ISC AND Beerware AND LicenseRef-Fedora-Public-Domain
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.hadrons.org/software/libmd/
Source0:        https://libbsd.freedesktop.org/releases/%{name}-%{version}.tar.xz
Source1:        https://libbsd.freedesktop.org/releases/%{name}-%{version}.tar.xz.asc
Source2:        https://keys.openpgp.org/vks/v1/by-fingerprint/4F3E74F436050C10F5696574B972BF3EA4AE57A3
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make

%description
The libmd library provides a few message digest ("hash") functions, as
found on various BSD systems, either on their libc or on a library with
the same name, and with a compatible API.

%package devel
Summary:        Development files for the message digest library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config

%description devel
The libmd-devel package includes header files and libraries necessary
for developing programs which use the message digest library.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q

%build
%configure --disable-static
%make_build

%install
%make_install

# Don't install any libtool .la files
rm -f %{buildroot}%{_libdir}/%{name}.la

%check
make check

%ldconfig_scriptlets

%files
%license COPYING
%doc ChangeLog README
%{_libdir}/%{name}.so.0*
%{_mandir}/man7/%{name}.7*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/md2.h
%{_includedir}/md4.h
%{_includedir}/md5.h
%{_includedir}/ripemd.h
%{_includedir}/rmd160.h
%{_includedir}/sha.h
%{_includedir}/sha1.h
%{_includedir}/sha2.h
%{_includedir}/sha256.h
%{_includedir}/sha512.h
%{_mandir}/man3/MD2*.3*
%{_mandir}/man3/MD4*.3*
%{_mandir}/man3/MD5*.3*
%{_mandir}/man3/RMD160*.3*
%{_mandir}/man3/SHA1*.3*
%{_mandir}/man3/SHA256*.3*
%{_mandir}/man3/SHA384*.3*
%{_mandir}/man3/SHA512*.3*
%{_mandir}/man3/md2.3*
%{_mandir}/man3/md4.3*
%{_mandir}/man3/md5.3*
%{_mandir}/man3/rmd160.3*
%{_mandir}/man3/sha1.3*
%{_mandir}/man3/sha2.3*

%changelog
* Wed Sep 11 2024 Zhichun Wan <zhichunwan@microsoft.com> - 1.1.0-6
- Initial Azure Linux import from Fedora 42 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Robert Scheck <robert@fedoraproject.org> 1.1.0-1
- Upgrade to 1.1.0 (#2214865)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Robert Scheck <robert@fedoraproject.org> 1.0.4-2
- Update license identifier to SPDX expression (#2094582 #c11)

* Wed Jun 08 2022 Robert Scheck <robert@fedoraproject.org> 1.0.4-1
- Upgrade to 1.0.4 (#2094582)
- Initial spec file for Fedora and Red Hat Enterprise Linux
