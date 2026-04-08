# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-nettle
Version:        3.10.2
Release:        1%{?dist}

Summary: MinGW package for nettle cryptographic library
# Automatically converted from old format: LGPLv3+ or GPLv2+ - review is highly recommended.
License: LGPL-3.0-or-later OR GPL-2.0-or-later
URL:    http://www.lysator.liu.se/~nisse/nettle/

Source0: http://www.lysator.liu.se/~nisse/archive/nettle-%{version}.tar.gz
Source1: http://www.lysator.liu.se/~nisse/archive/nettle-%{version}.tar.gz.sig
Source2: nettle-release-keyring.gpg
# MinGW does not support explicit_bzero()
#Patch0:  nettle-3.8-zeroize-stack.patch
Patch1:  nettle-3.10-hobble-to-configure.patch

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  mingw32-gmp
BuildRequires:  mingw64-gmp
BuildRequires:  mingw32-openssl
BuildRequires:  mingw64-openssl

BuildRequires:  autoconf, automake
BuildRequires:  gcc
BuildRequires:  m4


%description
Nettle is a cryptographic library that is designed to fit easily in
more or less any context: In crypto toolkits for object-oriented
languages (C++, Python, Pike, ...), in applications like LSH or GNUPG,
or even in kernel space.


# Mingw32
%package -n mingw32-nettle
Summary: MinGW package for nettle cryptographic library


%description -n mingw32-nettle
Nettle is a cryptographic library that is designed to fit easily in
more or less any context: In crypto toolkits for object-oriented
languages (C++, Python, Pike, ...), in applications like LSH or GNUPG,
or even in kernel space.


# Mingw64
%package -n mingw64-nettle
Summary: MinGW package for nettle cryptographic library


%description -n mingw64-nettle
Nettle is a cryptographic library that is designed to fit easily in
more or less any context: In crypto toolkits for object-oriented
languages (C++, Python, Pike, ...), in applications like LSH or GNUPG,
or even in kernel space.


%?mingw_debug_package


%prep
%autosetup -Tb 0 -p1 -n nettle-%{version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'


%build
autoreconf -ifv
%mingw_configure --enable-shared --enable-fat \
  --disable-sm3 --disable-sm4 --disable-ecc-secp192r1 --disable-ecc-secp224r1
%mingw_make %{?_smp_mflags}


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# Clean out files that should not be part of the rpm.
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/libnettle.a
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/libnettle.a
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/libhogweed.a
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/libhogweed.a
rm -rf $RPM_BUILD_ROOT%{mingw32_infodir}/
rm -rf $RPM_BUILD_ROOT%{mingw64_infodir}/


# Win32
%files -n mingw32-nettle
%doc README
%license COPYINGv2 COPYING.LESSERv3
%{mingw32_bindir}/nettle-hash.exe
%{mingw32_bindir}/nettle-lfib-stream.exe
%{mingw32_bindir}/nettle-pbkdf2.exe
%{mingw32_bindir}/pkcs1-conv.exe
%{mingw32_bindir}/sexp-conv.exe
%{mingw32_bindir}/libnettle-8.dll
%{mingw32_bindir}/libhogweed-6.dll
%{mingw32_libdir}/libnettle.dll.a
%{mingw32_libdir}/libhogweed.dll.a
%{mingw32_libdir}/pkgconfig/nettle.pc
%{mingw32_libdir}/pkgconfig/hogweed.pc
%dir %{mingw32_includedir}/nettle
%{mingw32_includedir}/nettle/*.h


# Win64
%files -n mingw64-nettle
%doc README
%license COPYINGv2 COPYING.LESSERv3
%{mingw64_bindir}/nettle-hash.exe
%{mingw64_bindir}/nettle-lfib-stream.exe
%{mingw64_bindir}/nettle-pbkdf2.exe
%{mingw64_bindir}/pkcs1-conv.exe
%{mingw64_bindir}/sexp-conv.exe
%{mingw64_bindir}/libnettle-8.dll
%{mingw64_bindir}/libhogweed-6.dll
%{mingw64_libdir}/libnettle.dll.a
%{mingw64_libdir}/libhogweed.dll.a
%{mingw64_libdir}/pkgconfig/nettle.pc
%{mingw64_libdir}/pkgconfig/hogweed.pc
%dir %{mingw64_includedir}/nettle
%{mingw64_includedir}/nettle/*.h


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 3.7.2-11
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.7.2-4
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 13 2021 Michael Cronenworth <mike@cchtml.com> - 3.7.2-1
- New upstream release.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 3.5.1-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 3.5.1-1
- Update the sources accordingly to its native counter part, rhbz#1740768

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 03 2019 Michael Cronenworth <mike@cchtml.com> - 3.4.1-1
- New upstream release

* Fri Aug 24 2018 Richard W.M. Jones <rjones@redhat.com> - 3.4-3
- Rebuild for new mingw-openssl.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Michael Cronenworth <mike@cchtml.com> - 3.4-1
- New upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 03 2016 Michael Cronenworth <mike@cchtml.com> - 3.3-1
- New upstream release
- Fixed CVE-2016-6489 (#1362018)

* Wed Feb 03 2016 Michael Cronenworth <mike@cchtml.com> - 3.2-1
- New upstream release
- Fixed CVE-2015-8803 secp256r1 calculation bug (#1304305)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Michael Cronenworth <mike@cchtml.com> - 3.1.1-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 26 2014 Michael Cronenworth <mike@cchtml.com> - 2.7.1-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Michael Cronenworth <mike@cchtml.com> - 2.6-1
- New upstream release

* Wed Aug 29 2012 Michael Cronenworth <mike@cchtml.com> - 2.4-2
- Missing BR m4

* Tue Jul 10 2012 Michael Cronenworth <mike@cchtml.com> - 2.4-1
- Initial RPM package
