Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           rhash
Version:        1.3.8
Release:        4%{?dist}
Summary:        Great utility for computing hash sums

License:        MIT
URL:            https://github.com/rhash/RHash
Source0:        https://github.com/rhash/RHash/archive/v%{version}/%{name}-%{version}.tar.gz

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
%make_build OPTFLAGS="%{optflags}" OPTLDFLAGS="-g %{?__global_ldflags}" build-shared


%install
%make_install
make DESTDIR=%{buildroot} -C librhash install-so-link install-lib-headers


%check
make test-shared


%ldconfig_scriptlets


%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.8-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
