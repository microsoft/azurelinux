# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:	Library for reading and writing sound files
Name:		libsndfile
Version:	1.2.2
Release: 11%{?dist}
License:	LGPL-2.1-or-later AND GPL-2.0-or-later AND BSD-3-Clause
URL:		http://libsndfile.github.io/libsndfile/
Source0:        https://github.com/libsndfile/libsndfile/releases/download/%{version}/libsndfile-%{version}.tar.xz
Patch0:		libsndfile-1.0.25-system-gsm.patch

#from upstream, for <= 1.2.2, rhbz#2322326
Patch1:	libsndfile-1.2.2-cve-2024-50612.patch
Patch2:	libsndfile-1.2.2-stdbool.patch

%if %{undefined rhel}
# used to regenerate test .c sources from .def files
BuildRequires:  autogen
%endif
BuildRequires:  gcc-c++
BuildRequires:	alsa-lib-devel
BuildRequires:	flac-devel
BuildRequires:	gcc
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite-devel
BuildRequires:	gsm-devel
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	python3
BuildRequires:  opus-devel
BuildRequires:  lame-devel
BuildRequires:  mpg123-devel


%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.


%package devel
Summary:	Development files for libsndfile
Requires:	%{name}%{?_isa} = %{version}-%{release} pkgconfig


%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains files needed to develop with libsndfile.


%package utils
Summary:	Command Line Utilities for libsndfile
Requires:	%{name} = %{version}-%{release}


%description utils
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains command line utilities for libsndfile.


%prep
%setup -q
%patch -P0 -p1 -b .system-gsm
%patch -P 1 -p1 -b .cve-2024-50612
%patch -P 2 -p1 -b .stdbool
rm -r src/GSM610

%build
autoreconf -I M4 -fiv # for system-gsm patch
%configure \
	--disable-dependency-tracking \
	--enable-sqlite \
	--enable-alsa \
	--enable-largefile \
	--enable-mpeg \
	--disable-static

# Get rid of rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
rm -rf __docs
mkdir __docs
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/* __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
find %{buildroot} -type f -name "*.la" -delete

# fix multilib issues
mv %{buildroot}%{_includedir}/sndfile.h \
   %{buildroot}%{_includedir}/sndfile-%{__isa_bits}.h

cat > %{buildroot}%{_includedir}/sndfile.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "sndfile-32.h"
#elif __WORDSIZE == 64
# include "sndfile-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF

%if 0%{?rhel} != 0
rm -f %{buildroot}%{_bindir}/sndfile-jackplay
%endif


%check
LD_LIBRARY_PATH=$PWD/src/.libs make check


%ldconfig_scriptlets


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
# NEWS files is missing in 1.1.0, check if it was re-added
%doc AUTHORS README
%{_libdir}/%{name}.so.1{,.*}

%files utils
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-concat
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-deinterleave
%{_bindir}/sndfile-info
%{_bindir}/sndfile-interleave
%{_bindir}/sndfile-metadata-get
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-play
%{_bindir}/sndfile-salvage
%{_mandir}/man1/sndfile-cmp.1*
%{_mandir}/man1/sndfile-concat.1*
%{_mandir}/man1/sndfile-convert.1*
%{_mandir}/man1/sndfile-deinterleave.1*
%{_mandir}/man1/sndfile-info.1*
%{_mandir}/man1/sndfile-interleave.1*
%{_mandir}/man1/sndfile-metadata-get.1*
%{_mandir}/man1/sndfile-metadata-set.1*
%{_mandir}/man1/sndfile-play.1*
%{_mandir}/man1/sndfile-salvage.1*

%files devel
%doc __docs ChangeLog
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_includedir}/sndfile-%{__isa_bits}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 27 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.2-9
- Rebuilt for flac 1.5.0

* Wed Jan 29 2025 Michal Hlavinka <mhlavink@redhat.com> - 1.2.2-8
- fix ftbfs

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.2.2-5
- fix crash in in ogg vorbis (rhbz#2322326) (CVE-2024-50612)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Michal Hlavinka <mhlavink@redhat.com> - 1.2.2-1
- updated to 1.2.2

* Tue Jul 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.1.0-8
- Avoid autogen dependency in RHEL builds

* Mon Apr 24 2023 Michal Hlavinka <mhlavink@redhat.com> - 1.1.0-7
- update license tag format (SPDX migration) for https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 13 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.1.0-5
- Rebuilt for flac 1.4.0

* Sat Sep 10 2022 Michal Hlavinka <mhlavink@redhat.com> - 1.1.0-4
- enable MP3 support

* Wed Aug 03 2022 Michal Hlavinka <mhlavink@redhat.com> - 1.1.0-3
- new MPEG support does not compile on some archs, do not enable it yet

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Michal Hlavinka <mhlavink@redhat.com> - 1.1.0-1
- updated to 1.1.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 01 2021 Michal Hlavinka <mhlavink@redhat.com> - 1.0.31-6
- fix heap buffer overflow in flac (#2027692)

* Fri Jul 23 2021 Michal Hlavinka <mhlavink@redhat.com> - 1.0.31-5
- a crafted wav file could cause heap buffer overflow that allowed an arbitrary code execution (#1984320)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 22 2021 Michal Hlavinka <mhlavink@redhat.com> - 1.0.31-3
- add opus-devel BR to satisfy configure requirements check (#1931251)

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.0.31-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 27 2021 Michal Hlavinka <mhlavink@redhat.com> - 1.0.31-1
- updated to 1.0.31

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Michal Hlavinka <mhlavink@redhat.com> - 1.0.28-8
- add gcc buildrequire

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Michal Hlavinka <mhlavink@redhat.com> - 1.0.28-6
- heap-based Buffer Overflow in psf_binheader_writef function (#1483140, CVE-2017-12562)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Michal Hlavinka <mhlavink@redhat.com> - 1.0.28-3
- fix buffer overflow in aiff (CVE-2017-6892,rhbz#1463328)

* Mon Jun 05 2017 Michal Hlavinka <mhlavink@redhat.com> - 1.0.28-2
- fix flac and pcm buffer overflows (CVE-2017-8361,CVE-2017-8362,CVE-2017-8363,CVE-2017-8365)

* Tue Apr 11 2017 Michal Hlavinka <mhlavink@redhat.com> - 1.0.28-1
- updated to 1.0.28
- fix possible buffer overflow when parsing crafted ID3 tags (#1440758, CVE-2017-7586)
- fix possible buffer overflow when parsing crafted flac file (#1440756, CVE-2017-7585)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 Michal Hlavinka <mhlavink@redhat.com> - 1.0.27-1
- updated to 1.0.27

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-19
- fix incomplete patch for CVE-2015-7805

* Fri Nov 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-18
- fix CVE-2015-7805: Heap overflow vulnerability when parsing specially
  crafted AIFF header

* Thu Aug 27 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.0.25-17
- Use __isa_bits macro instead of list of 64-bit architectures

* Sun Jul 19 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.25-16
- Fix FTBFS
- Use %%license

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-14
- fix CVE-2014-9496: 2 buffer overruns in sd2_parse_rsrc_fork (#1178840)
- division by zero leading to denial of service in psf_fwrite (#1177254)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.25-12
- Fix up previous commit

* Sat Aug  2 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.25-11
- Modernise spec
- Generic 32/64bit platform detection

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 13 2014 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-9
- fix ppc64le build (#1051639)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-7
- fix support for aarch64, another part (#969831)

* Wed Mar 27 2013 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-6
- fix support for aarch64 (#925887)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.0.25-2
- Patch to use system libgsm instead of a bundled copy.
- Make main package dep in -devel ISA qualified.
- Drop -octave Provides (not actually built with octave > 3.0).
- Don't build throwaway static lib.
- Run test suite during build.

* Thu Jul 14 2011 Michal Hlavinka <mhlavink@redhat.com> - 1.0.25-1
- Update to 1.0.25
- fixes integer overflow by processing certain PAF audio files (#721240)

* Sun Mar 27 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.24-1
- Update to 1.0.24

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.23-1
- Update to 10.0.23

* Tue Oct 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.22-1
- Update to 10.0.22

* Tue May 11 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.21-1
- Update to 10.0.21
- Do not include the static library in the package (RHBZ#556074)
- Remove BR on jack since sndfile-jackplay is not provided anymore

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.0.20-5
- Do not build against Jack on RHEL
- Fix the Source0: URL
- Fix the licence tag

* Sat Nov 14 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.20-4
- Split utils into a subpackage

* Sat Nov 14 2009 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.20-3
- Add FLAC/Ogg/Vorbis support (BR: libvorbis-devel)
- Make build verbose
- Remove rpath
- Fix ChangeLog encoding
- Move the big Changelog to the devel package

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Lennart Poettering <lpoetter@redhat.com> - 1.0.20-1
- Updated to 1.0.20

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> - 1.0.17-8
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Andreas Thienemann <andreas@bawue.net> - 1.0.17-6
- Removed spurious #endif in the libsndfile.h wrapper. Thx to Edward
  Sheldrake for finding it. Fixes #468508.
- Fix build for autoconf-2.63

* Thu Oct 23 2008 Andreas Thienemann <andreas@bawue.net> - 1.0.17-5
- Fixed multilib conflict. #342401
- Made flac support actually work correctly.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.17-4
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.17-3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Andreas Thienemann <andreas@bawue.net> - 1.0.17-2
- Adding FLAC support to libsndfile courtesy of gentoo, #237575
- Fixing CVE-2007-4974. Thanks to the gentoo people for the patch, #296221

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.17-1
- Updated to 1.0.17

* Sun Apr 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.16-1
- Updated to 1.0.16

* Thu Mar 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.0.15-1
- Updated to 1.0.15

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.0.14-1.fc5
- Updated to 1.0.14
- Dropped patch0

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-3
- rebuilt

* Sat Mar  5 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.11-2
- Fix format string bug (#149863).
- Drop explicit Epoch 0.

* Sat Dec  4 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.0.11-0.fdr.1
- Update to 1.0.11.

* Wed Oct 13 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:1.0.10-0.fdr.1
- Update to 1.0.10, update URLs, include ALSA support.
- Disable dependency tracking to speed up the build.
- Add missing ldconfig invocations.
- Make -devel require pkgconfig.
- Include developer docs in -devel.
- Provide -octave in main package, own more related dirs.
- Bring specfile up to date with current spec templates.

* Sat Apr 12 2003 Dams <anvil[AT]livna.org>
- Initial build.
