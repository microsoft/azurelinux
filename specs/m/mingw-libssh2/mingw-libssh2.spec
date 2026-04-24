# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Name:           mingw-libssh2
Version:        1.11.1
Release: 3%{?dist}
Summary:        MinGW Windows library implementation of the SSH2 protocol

License:        BSD-3-Clause
URL:            https://www.libssh2.org/
Source0:        https://libssh2.org/download/libssh2-%{version}.tar.gz
Source1:        https://libssh2.org/download/libssh2-%{version}.tar.gz.asc
# Daniel Stenberg's GPG keys; linked from https://daniel.haxx.se/address.html
Source2:        https://daniel.haxx.se/mykey.asc

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-zlib


%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).


# Win32
%package -n mingw32-libssh2
Summary:        MinGW Windows library implementation of the SSH2 protocol
Requires:       pkgconfig

%description -n mingw32-libssh2
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package -n mingw32-libssh2-static
Summary:        Static version of the MinGW Windows SSH2 library
Requires:       mingw32-libssh2 = %{version}-%{release}

%description -n mingw32-libssh2-static
Static version of the MinGW Windows SSH2 library.

# Win64
%package -n mingw64-libssh2
Summary:        MinGW Windows library implementation of the SSH2 protocol
Requires:       pkgconfig

%description -n mingw64-libssh2
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package -n mingw64-libssh2-static
Summary:        Static version of the MinGW Windows SSH2 library
Requires:       mingw64-libssh2 = %{version}-%{release}

%description -n mingw64-libssh2-static
Static version of the MinGW Windows SSH2 library.


%?mingw_debug_package


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n libssh2-%{version}


%build
%mingw_configure --disable-silent-rules --enable-static --enable-shared
%mingw_make %{?_smp_mflags}


%install
%mingw_make DESTDIR=$RPM_BUILD_ROOT install

# Remove .la files
find $RPM_BUILD_ROOT -name "*.la" -delete

# Remove man pages which duplicate native Fedora.
rm -r $RPM_BUILD_ROOT%{mingw32_mandir}/man3
rm -r $RPM_BUILD_ROOT%{mingw64_mandir}/man3


# Win32
%files -n mingw32-libssh2
%doc COPYING
%{mingw32_bindir}/libssh2-1.dll
%{mingw32_libdir}/libssh2.dll.a
%{mingw32_libdir}/pkgconfig/libssh2.pc
%{mingw32_includedir}/libssh2.h
%{mingw32_includedir}/libssh2_publickey.h
%{mingw32_includedir}/libssh2_sftp.h

%files -n mingw32-libssh2-static
%{mingw32_libdir}/libssh2.a

# Win64
%files -n mingw64-libssh2
%doc COPYING
%{mingw64_bindir}/libssh2-1.dll
%{mingw64_libdir}/libssh2.dll.a
%{mingw64_libdir}/pkgconfig/libssh2.pc
%{mingw64_includedir}/libssh2.h
%{mingw64_includedir}/libssh2_publickey.h
%{mingw64_includedir}/libssh2_sftp.h

%files -n mingw64-libssh2-static
%{mingw64_libdir}/libssh2.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Michael Cronenworth <mike@cchtml.com> - 1.11.1-1
- Version update

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.9.0-16
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.9.0-9
- Rebuild with mingw-gcc-12

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 1.9.0-8
- Rebuild (openssl)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 1.9.0-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.9.0-1
- Update the sources accordingly to its native counter part, rhbz#1740781

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 24 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-6
- Rebuild for new mingw-openssl.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Michael Cronenworth <mike@cchtml.com> - 1.8.0-1
- Version update

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-11
- Added win64 support (contributed by Marc-Andre Lureau)

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.1-10
- Remove .la files

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.1-9
- Renamed the source package to mingw-libssh2 (#800434)
- Spec clean up
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-8
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-5
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Sun Aug 30 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-4
- Rebuild for new mingw32-openssl
- Automatically generate debuginfo subpackage

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-2
- Use %%global instead of %%define

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.1-1
- Update to version 1.1
- Drop upstreamed patches

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.18-6
- Added -static subpackage
- Fixed %%defattr line

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.18-5
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.18-4
- Include license file.

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.18-3
- Rebuild against new OpenSSH (because of soname bump).

* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 0.18-2
- Update libtool installation.

* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.18-1
- Initial RPM release.
