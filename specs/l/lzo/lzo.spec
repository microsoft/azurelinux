# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           lzo
Version:        2.10
Release:        15%{?dist}
Summary:        Data compression library with very fast (de)compression
License:        gpl-2.0-or-later
URL:            http://www.oberhumer.com/opensource/lzo/

Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
Patch0:         lzo-2.08-configure.patch
Patch1:         lzo-2.08-rhbz1309225.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package minilzo
Summary:        Mini version of lzo for apps which don't need the full version

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%package devel
Summary:        Development files for the lzo library
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-minilzo = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.


%prep
%autosetup -p1
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
%{make_build} CFLAGS+=-fno-strict-aliasing

# build minilzo too (bz 439979)
gcc %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -Wl,-z,now -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o


%install
%{make_install}
find $RPM_BUILD_ROOT -name '*.la' -delete

install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/lzo

#Remove doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/lzo

%check
make check test


%ldconfig_scriptlets
%ldconfig_scriptlets minilzo


%files
%license COPYING
%doc AUTHORS THANKS NEWS
%{_libdir}/liblzo2.so.*

%files minilzo
%license COPYING
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so
%{_libdir}/pkgconfig/lzo2.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10-11
- Converted license tag to SPDX

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 02 2020 Michael Cronenworth <mike@cchtml.com> - 2.10-2
- Disable -fno-strict-aliasing (RHBZ#1807737)

* Sun Feb  9 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2.10-1
- Update to 2.10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.08-12
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Karsten Hopp <karsten@redhat.com> - 2.08-8
- remove -O1 workaround, add patch by Jakub Jelinek instead (bug #1309225)

* Wed Feb 17 2016 Karsten Hopp <karsten@redhat.com> - 2.08-7
- use -O1 compiler optimizations on ppc64le (bug #1309225)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.08-5
- Link libminilzo with -z now

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.08-2
- fix license handling

* Mon Jun 30 2014 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.08-1
- New upstream
- Fix CVE-2014-4607

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 14 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.06-1
- Upgrade to latest upstream
- Apply patch from Nicolas Chauvet

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May  1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.03-1
- New upstream release
- Changed the license to GPLv2+

* Wed Apr  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-5
- Fix configure failure with -Werror-implicit-function-declaration in CFLAGS
- Add a minilzo subpackage which contains a shared version of minilzo, to be
  used by all applications which ship with their own copy of it (bz 439979)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.02-4
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-3
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-2
- FE6 Rebuild

* Wed Jul 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-1
- New upstream release 2.02, soname change!

* Mon Jul 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.08-7
- Taking over as maintainer since Anvil has other priorities
- Add a patch to fix asm detection on i386 (bug 145882, 145893). Thanks to
  Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe> for the initial patch.
- Removed unused build dependency on nasm
- Remove static lib
- Cleanup %%doc a bit

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.08-6.fc5
- Rebuild for new gcc

* Tue Jan 17 2006 Dams <anvil[AT]livna.org> - 1.08-5.fc5
- Bumped release for gcc 4.1 rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.08-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.08-0.fdr.2
- Typo un devel description
- Added post and postun scriptlets
- Added URL in Source0

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.
