# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

%global run_tests 0

Name:           mingw-libgcrypt
Version:        1.10.3
Release: 6%{?dist}
Summary:        MinGW Windows gcrypt encryption library

# Automatically converted from old format: LGPLv2+ and GPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+ AND GPL-2.0-or-later

URL:            ftp://ftp.gnupg.org/gcrypt/libgcrypt/
Source0: https://www.gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
Source1: https://www.gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2: wk@g10code.com

# Pass the annobin flags to the libgcrypt.so (#2016349)
Patch1: libgcrypt-1.10.1-annobin.patch

# MinGW-specific patches

# Workaround a bug in libtool:
# libgcrypt-use-correct-def-file.patch
Patch1000:      libgcrypt-use-correct-def-file.patch

BuildArch:      noarch

BuildRequires:  autoconf, automake, libtool
BuildRequires:  make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-libgpg-error

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-libgpg-error

BuildRequires:  gcc
#BuildRequires:  autoconf automake libtool

%if %run_tests
BuildRequires:  wine
%endif


%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.

This is a Windows cross-compiled version of the library.


# Win32
%package -n mingw32-libgcrypt
Summary:        MinGW Windows gcrypt encryption library

%description -n mingw32-libgcrypt
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.

This is a Windows cross-compiled version of the library.

%package -n mingw32-libgcrypt-static
Summary:        Static library for mingw32-libgcrypt development
Requires:       mingw32-libgcrypt = %{version}-%{release}
Requires:       mingw32-libgpg-error-static

%description -n mingw32-libgcrypt-static
Static library for mingw32-libgcrypt development.

# Win64
%package -n mingw64-libgcrypt
Summary:        MinGW Windows gcrypt encryption library

%description -n mingw64-libgcrypt
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.

This is a Windows cross-compiled version of the library.

%package -n mingw64-libgcrypt-static
Summary:        Static library for mingw64-libgcrypt development
Requires:       mingw64-libgcrypt = %{version}-%{release}
Requires:       mingw64-libgpg-error-static

%description -n mingw64-libgcrypt-static
Static library for mingw64-libgcrypt development.


%?mingw_debug_package


%prep
%setup -q -n libgcrypt-%{version}
%patch -P1 -p1

%patch -P1000 -p0 -b .def

autoreconf -i --force


%build
MINGW64_CONFIGURE_ARGS="ac_cv_sys_symbol_underscore=no --disable-padlock-support"
%mingw_configure --enable-shared --enable-static --enable-pubkey-ciphers='dsa elgamal rsa ecc'
%mingw_make %{?_smp_mflags}


%check
%if %run_tests
# Stupid Wine doesn't load DLLs from the PATH any
# more, so libtool scripts don't work.  As a result
# we need to use the following Big Hack.
make -C build_win32/tests check ||:
pushd build_win32/src/.libs
for t in $(pwd)/../../tests/*.exe; do
  wine $t
done
popd
%endif


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# Remove info pages which duplicate what is in Fedora natively.
rm -rf $RPM_BUILD_ROOT%{mingw32_infodir}
rm -rf $RPM_BUILD_ROOT%{mingw64_infodir}

rm -rf $RPM_BUILD_ROOT%{mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw64_mandir}

rm $RPM_BUILD_ROOT%{mingw32_libdir}/libgcrypt.def
rm $RPM_BUILD_ROOT%{mingw64_libdir}/libgcrypt.def

rm $RPM_BUILD_ROOT%{mingw32_libdir}/libgcrypt.la
rm $RPM_BUILD_ROOT%{mingw64_libdir}/libgcrypt.la


%files -n mingw32-libgcrypt
%doc COPYING COPYING.LIB
%{mingw32_bindir}/dumpsexp.exe
%{mingw32_bindir}/hmac256.exe
%{mingw32_bindir}/mpicalc.exe
%{mingw32_bindir}/libgcrypt-20.dll
%{mingw32_bindir}/libgcrypt-config
%{mingw32_libdir}/libgcrypt.dll.a
%{mingw32_libdir}/pkgconfig/libgcrypt.pc
%{mingw32_includedir}/gcrypt.h
%{mingw32_datadir}/aclocal/libgcrypt.m4

%files -n mingw32-libgcrypt-static
%{mingw32_libdir}/libgcrypt.a

%files -n mingw64-libgcrypt
%doc COPYING COPYING.LIB
%{mingw64_bindir}/dumpsexp.exe
%{mingw64_bindir}/hmac256.exe
%{mingw64_bindir}/mpicalc.exe
%{mingw64_bindir}/libgcrypt-20.dll
%{mingw64_bindir}/libgcrypt-config
%{mingw64_libdir}/libgcrypt.dll.a
%{mingw64_libdir}/pkgconfig/libgcrypt.pc
%{mingw64_includedir}/gcrypt.h
%{mingw64_datadir}/aclocal/libgcrypt.m4


%files -n mingw64-libgcrypt-static
%{mingw64_libdir}/libgcrypt.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.10.3-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 08 2024 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-1
- Rebase to libgcrypt 1.10.3 to match Fedora (RHBZ#2268272)
- Add *.pc (pkgconf) files

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.8.4-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.8.4-1
- Update the sources accordingly to its native counter-panter, rhbz#1740734

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 29 2018 Christophe Fergeau <cfergeau@redhat.com> - 1.8.3-1
- Update to 1.8.3, this syncs mingw-libgcrypt with the native libgcrypt package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 1.6.3-3
- Use global instead of define.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3
- Fixes CVE-2014-3591 CVE-2015-0837 (RHBZ #1198153 #1198156)

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- Add cleared ECC support
- Disable padlock support in Win64 for now (breaks compilation)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.0-6
- Made the win64 asm code work properly

* Sun Oct 21 2012 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 1.5.0-5
- Add static libraries
- Fix compile of assembly code for mingw64

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.5.0-3
- Rebuilt for %%mingw_configure arg parsing issue

* Sat Mar 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.0-2
- Simplify the use of mingw macros
- Improved the win64 patch a bit (shouldn't have any visible effects)

* Sun Mar 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0
- Added win64 support

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.4-9
- Remove .la files

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.4-8
- Renamed the source package to mingw-libgcrypt (#800428)
- Spec clean up

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.4-7
- Rebuild against the mingw-w64 toolchain
- Use correct .def file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.4-2
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.4-1
- Update to Fedora native version 1.4.4:
  . Remove potentially patented ECC support.
  . Do not abort when the fips mode kernel flag is inaccessible
    due to permissions (#470219).
- For review (Michel Alexandre Salim):
  . Remove *.def file.
  . Make description clearer.
  . Distribute the license files.
- The license for binaries is GPLv2+, so update the license field.
- Add check section (disabled by default).
- Why did we set PATH before configure? Removed.
- Added BR mingw32-dlfcn suggested by auto-buildrequires.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-3
- Use _smp_mflags.
- Disable static libraries.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.3-1
- Update to 1.4.3 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-6
- Remove info pages.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-5
- Set PATH so it finds gpg-error-config

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-4
- Remove static library.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
