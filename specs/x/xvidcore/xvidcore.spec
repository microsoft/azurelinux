# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sovermajor 4

Name:           xvidcore
Version:        1.3.7
Release:        14%{?dist}
Summary:        MPEG-4 Simple and Advanced Simple Profile codec
License:        GPL-2.0-or-later
URL:            https://www.xvid.com/
Source0:        https://downloads.xvid.com/downloads/%{name}-%{version_no_tilde}.tar.bz2
# fix build with -std=gnu23, reported upstream
Patch0:         %{name}-c23.patch

BuildRequires:  gcc
BuildRequires:  make
%ifarch %{ix86} x86_64
BuildRequires:  nasm >= 2.0
%endif

%description
The Xvid video codec implements MPEG-4 Simple Profile and Advanced Simple
Profile standards. It permits compressing and decompressing digital video
in order to reduce the required bandwidth of video data for transmission
over computer networks or efficient storage on CDs or DVDs. Due to its
unrivalled quality Xvid has gained great popularity and is used in many
other GPLed applications, like e.g. Transcode, MEncoder, MPlayer, Xine and
many more.

%package        devel
Summary:        Development files for the Xvid video codec
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
This package contains header files, static library and API
documentation for the Xvid video codec.


%prep
%autosetup -p1 -n %{name}
chmod -x examples/*.pl
# Convert to utf-8
for file in AUTHORS ChangeLog; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done
# Fix rpmlint wrong-file-end-of-line-encoding
for file in ChangeLog; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done
# Yes, we want to see the build output.
%{__sed} -i -e 's|@$(|$(|g' build/generic/Makefile
# Fix permissions
%{__sed} -i -e 's|644 $(BUILD_DIR)/$(SHARED_LIB)|755 $(BUILD_DIR)/$(SHARED_LIB)|g' build/generic/Makefile

%build
cd build/generic
%configure
%make_build


%install
%make_install -C build/generic
find %{buildroot} -name "*.a" -delete


%files
%doc README AUTHORS ChangeLog
%license LICENSE
%{_libdir}/libxvidcore.so.%{sovermajor}{,.*}

%files devel
%doc CodingStyle TODO examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
- Fix build with GCC15 (Dominik Mierzejewski)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.3.7-9
- Adapt for Fedora

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 11 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.7-3
- Rebuilt for i686

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.3.7-1
- Update to 1.3.7

* Thu Dec 12 2019 Leigh Scott <leigh123linux@gmail.com> - 1.3.6-1
- Update to 1.3.6

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Dominik Mierzejewski <rpm at greysector.net> - 1.3.5-4
- fix crash in check_cpu_features (rfbz#5141), patch by Peter Ross
- add missing BR: gcc

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.5-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.5-1
- Update to 1.3.5

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 25 2015 Dominik Mierzejewski <rpm at greysector.net> - 1.3.4-2
- using ldconfig to generate correct so filename is no longer needed

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.3.4-1
- Update to 1.3.4

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-5
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3.2-2
- Update to 1.3.2

* Mon Jan 10 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.3.0-0.1.rc1
- 1.3.0-rc1
- drop upstreamed noexec stack patch

* Sat Dec 11 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.2.2-1
- 1.2.2
- rebase noexec-stack patch

* Mon Sep 21 2009 Hans de Goede <j.w.r.degoede@hhs.nl> - 1.2.1-3
- Do not require an executable stack on x86_64 (rf743, rf733)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.2.1-2
- rebuild for new F11 features

* Sat Dec 20 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.2.1-1
- 1.2.1
- drop upstreamed compilation fix

* Wed Dec 03 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.2.0-1
- 1.2.0
- drop upstreamed noexec stack patch
- BR recent nasm instead of yasm
- licence seems to be just GPLv2+
- move TODO from main to -devel doc
- update summary and description
- small spec file fixes

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.1.3-4
- rebuild

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.3-3
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 3 to be higher as both livna and freshrpms latest release
- Add -ffast-math to CFLAGS

* Sat Jun 30 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.3-1
- 1.1.3, security bugfix release, fixes CVE-2007-3329 (#1563)

* Sun Mar 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.1.2-2
- fix SElinux noexec stack issue (patch by Hans de Goede)

* Sat Nov 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.2-1
- 1.1.2.
- Convert docs to UTF-8.
- Use make install DESTDIR=... instead of %%makeinstall.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.1.0-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-3
- Use yasm to build, enable asm code on x86_64.
- Drop no longer needed Obsoletes.
- Specfile cleanups.

* Sat May 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-2
- Fix library permissions and symlink.
- Don't ship static library.
- Avoid -devel dependency on perl.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 1.1.0-0.lvn.1
- Updated to 1.10
- Droped now unnecessary patch
- Droped Epoch

* Sun Feb 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.3-0.lvn.1
- 1.0.3.

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.2-0.lvn.1
- Update to 1.0.2.

* Tue Jun  8 2004 Dams <anvil[AT]livna.org> 0:1.0.1-0.lvn.1
- Updated to 1.0.1

* Mon May 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.1
- Updated to 1.0.0.
- Patch to show build output.

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.0.2.rc4
- Updated to 1.0.0-rc4.

* Mon Mar 29 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.2.rc3
- Updated to rc3

* Sat Jan 10 2004 Dams <anvil[AT]livna.org> 0:1.0.0-0.lvn.0.1.beta3
- Updated to 1.0.0-beta3
- Small spec file cleanup

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.2-0.fdr.1.0.94
- Removed comment after scriptlets

* Fri Aug 15 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.9.2-0.fdr.1
- Updated to 0.9.2.
- Updated according to current SPEC template.
- Changed to properly versioned .so-files.

* Tue Apr  8 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.3
- Cleaned up the documentation.

* Fri Apr  4 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.2
- Added epoch and release number to requires.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.1-0.fdr.1
- Updated to 0.9.1.

* Wed Apr  2 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:0.9.0-0.fdr.1
- Initial fedora RPM release.
- Changed -static back to -devel as that seems more logic.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Wed Jan 29 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fixed the location of the .h files... doh!

* Sun Jan 12 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Remove the decore.h and encore2.h inks as divx4linux 5.01 will provide them.
- Rename -devel to -static as it seems more logic.

* Fri Dec 27 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
