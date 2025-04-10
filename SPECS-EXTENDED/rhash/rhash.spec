Name:           rhash
Version:        1.4.4
Release:        3%{?dist}
Summary:        Great utility for computing hash sums

License:        0BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/rhash/RHash
Source0:        https://github.com/rhash/RHash/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires:  gcc

%description
RHash is a console utility for calculation  and verification of magnet links
and a wide range of hash sums like  CRC32,  MD4, MD5,  SHA1, SHA256, SHA512,
SHA3,   AICH,  ED2K,  Tiger,  DC++ TTH,  BitTorrent BTIH,   GOST R 34.11-94,
RIPEMD-160, HAS-160, EDON-R, Whirlpool and Snefru.

Hash sums are used to  ensure and verify integrity  of large volumes of data
for a long-term storing or transferring.

Features:
 * Output in a predefined (SFV, BSD-like) or a user-defined format.
 * Can calculate Magnet links.
 * Updating hash files (adding hash sums of files missing in the hash file).
 * Calculates several hash sums in one pass
 * Ability to process directories recursively.
 * Portability: the program works the same on Linux, *BSD or Windows.


%package        devel
Summary:        Development files for lib%{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
LibRHash is a professional,  portable,  thread-safe  C library for computing
a wide variety of hash sums, such as  CRC32, MD4, MD5, SHA1, SHA256, SHA512,
SHA3,   AICH,  ED2K,  Tiger,  DC++ TTH,  BitTorrent BTIH,   GOST R 34.11-94,
RIPEMD-160, HAS-160, EDON-R, Whirlpool and Snefru.
Hash sums are used  to ensure and verify integrity of  large volumes of data
for a long-term storing or transferring.

Features:
 * Small and easy to learn interface.
 * Hi-level and Low-level API.
 * Allows calculating of several hash functions simultaneously.
 * Portability: the library works on Linux, *BSD and Windows.

The %{name}-devel package contains libraries and header files for
developing applications that use lib%{name}.


%prep
%setup -q -n RHash-%{version}
sed -i -e '/^INSTALL_SHARED/s/644/755/' librhash/Makefile

%build
INSTALL_INCDIR=%{_includedir} ./configure --sysconfdir=%{_sysconfdir} --exec-prefix=%{_prefix} --mandir=%{_mandir} --libdir=%{_libdir}
%make_build OPTFLAGS="%{optflags}" OPTLDFLAGS="-g %{?__global_ldflags}" build

%install
%make_install
make DESTDIR=%{buildroot} -C librhash install-so-link install-lib-headers

%check
make test-shared

%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%{_libdir}/*.so.1*
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Wed Dec 18 2024 Akhila Guruju <v-guakhila@microsoft.com> - 1.4.4-3
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 23 2024 Orion Poplawski <orion@nwra.com> - 1.4.4-1
- Update to 1.4.4

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 26 2022 Orion Poplawski <orion@cora.nwra.com> - 1.4.3-1
- Update to 1.4.3

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 16 2021 Orion Poplawski <orion@nwra.com> - 1.4.2-1
- Update to 1.4.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Orion Poplawski <orion@nwra.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb  4 2019 Orion Poplawski <orion@nwra.com> - 1.3.8-1
- Update to 1.3.8

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 14 2017 Orion Poplawski <orion@cora.nwra.com> - 1.3.5-1
- Update to 1.3.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Orion Poplawski <orion@cora.nwra.com> - 1.3.4-2
- Add %%check section

* Thu Mar 9 2017 Orion Poplawski <orion@cora.nwra.com> - 1.3.4-1
- Initial Fedora package
