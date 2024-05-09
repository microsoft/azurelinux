Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           lame
Version:        3.100
Release:        9%{?dist}
Summary:        Free MP3 audio compressor

License:        GPLv2+
URL:            https://lame.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sourceforge/lame/%{name}-%{version}.tar.gz
Patch1:         %{name}-noexecstack.patch
Patch2:         libmp3lame-symbols.patch

BuildRequires:  gcc
BuildRequires:  ncurses-devel
%ifarch %{ix86}
BuildRequires:  nasm
%endif
Requires:       %{name}-libs = %{version}-%{release}

Obsoletes:      %{name}-mp3x < 3.100-7


%description
LAME is an open source MP3 encoder whose quality and speed matches
commercial encoders. LAME handles MPEG1,2 and 2.5 layer III encoding
with both constant and variable bitrates.

%package        libs
Summary:        LAME MP3 encoding library

%description    libs
LAME MP3 encoding library.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
This package development files for %{name}.





%prep
%autosetup -p1


%build
sed -i -e 's/^\(\s*hardcode_libdir_flag_spec\s*=\).*/\1/' configure
%ifarch %{ix86}
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
#From LFS:https://www.linuxfromscratch.org/blfs/view/svn/multimedia/lame.html
export ac_cv_header_xmmintrin_h=no
%endif
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86}
  --enable-nasm \
%endif
  --enable-mp3rtp

%make_build


%install
%make_install INSTALL="install -p"
rm -f %{buildroot}%{_libdir}/*.la
# Some apps still expect to find <lame.h>
ln -sf lame/lame.h %{buildroot}%{_includedir}/lame.h
rm -rf %{buildroot}%{_docdir}/%{name}


%check
make test


%ldconfig_scriptlets libs


%files
%doc README TODO USAGE doc/html/*.html
%{_bindir}/lame
%{_bindir}/mp3rtp
%{_mandir}/man1/lame.1*

%files libs
%doc ChangeLog
%license COPYING LICENSE
%{_libdir}/libmp3lame.so.0*

%files devel
%doc API HACKING STYLEGUIDE
%{_libdir}/libmp3lame.so
%{_includedir}/lame
%{_includedir}/lame.h




%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.100-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.100-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Robert Scheck <robert@fedoraproject.org> - 3.100-7
- Disable packaging of gtk+-based lame-mp3x (#1760961, #1760995 #c1)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.100-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.100-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.100-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.100-2
- Switch to %%ldconfig_scriptlets

* Sun Oct 22 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 3.100-1
- Update to 3.100 (#1470202, #1505172)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.99.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.99.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 3.99.5-8
- Rebuilt for inclusion into Fedora

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.99.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 18 2016 Sérgio Basto <sergio@serjux.com> - 3.99.5-6
- Clean spec, Vascom patches series, rfbz #4201, add license tag

* Sun Dec 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.99.5-5
- Fix FTBFS on i686

* Sat Dec 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.99.5-4
- Rebuilt for F-21

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 3.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.99.5-2
- Mass rebuilt for Fedora 19 Features

* Tue Apr 17 2012 Matthias Saou <matthias@saou.eu> 3.99.5-1
- Update to 3.99.5.

* Sun Feb 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.99.4-1
- Update to 3.99.4

* Tue Jul 06 2010 Dominik Mierzejewski <rpm at greysector.net> - 3.98.4-1
- update to 3.98.4
- drop obsolete (build)requirements

* Sat Feb 27 2010 Dominik Mierzejewski <rpm at greysector.net> - 3.98.3-1
- update to 3.98.3

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.98.2-3
- rebuild for new F11 features

* Mon Oct 20 2008 Dominik Mierzejewski <rpm at greysector.net> - 3.98.2-2
- update to 3.98.2
- preserve file timestamps
- drop obsolete patch
- no need to call autoreconf anymore
- fix parallel make builds

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 3.97-7
- rebuild

* Thu Oct  4 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 3.97-6
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 6 to be higher as both livna and freshrpms latest release
- Update license tag for new license tag guidelines
- Add --enable-decode-layer1 to configure flags
- Make Source0 the advised sf.net download url
- Make ChangeLog UTF-8
- Don't duplicate the COPYING ChangeLog and LICENSE docs betweent the main
  and the -libs package

* Fri Sep 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.97-5
- BuildRequire pkgconfig for gtk+-devel in EL-5.

* Sun Mar 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 3.97-4
- fix rpaths and SELinux noexec stack issue (patch by Hans de Goede)

* Wed Nov 01 2006 Dominik Mierzejewski <rpm at greysector.net> - 3.97-3
- fix FC6+ binutils issues (patch by Rex Dieter)

* Thu Sep 28 2006 Dominik Mierzejewski <rpm at greysector.net> - 3.97-2
- Split off -libs subpackage
- Reenable parallel make

* Sun Sep 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.97-1
- 3.97, 3DNow! asm patch applied upstream.

* Wed Sep 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.96.1-7
- Avoid rpaths (from Ubuntu).
- Don't ship static libraries.
- Drop unneeded zero epochs.
- Build with dependency tracking disabled.
- Prune pre-2003 changelog entries.
- Other specfile cleanups.

* Sun May 14 2006 Noa Resare <noa@resare.com> 3.96.1-6
- Adding a patch to fix the 3DNow! asm and re-enable it

* Fri Apr  7 2006 Dams <anvil[AT]livna.org> - 3.96.1-5
- Disabling nasm for now. (bug #892)

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Dec 27 2005 Thorsten Leemhuis <fedora[at]leemhuis.info> 3.96.1-0.lvn.4
- add defattr to files of mp3x subpackage

* Tue Dec 27 2005 Thorsten Leemhuis <fedora[at]leemhuis.info> 3.96.1-0.lvn.3
- Drop Epoch

* Sat Sep 17 2005 W. Michael Petullo <mike[at]flyn.org> - 0:3.96.1-0.lvn.2
- Split mp3x into its own package to remove general gtk+ requirement.

* Sun Jul 25 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:3.96.1-0.lvn.1
- Updated to 3.96.1.

* Thu Apr 15 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:3.96-0.lvn.1
- Updated to 3.96.

* Tue Jan 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.95.1-0.lvn.3
- Enable mp3x and mp3rtp.
- Run tests in the %%check section.
- Use "make install DESTDIR=..." instead of %%makeinstall.
- s/fdr/lvn/ in release tag.

* Tue Jan 27 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:3.95.1-0.fdr.2
- Disabled parallel make (#61).

* Sat Jan 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:3.95.1-0.fdr.1
- Updated to 3.95.1.
- Spec file edited to match current Fedora template.
- Re-wrote descriptions.
- Converted spec file to UTF-8.

* Sat Aug 16 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.8
- Patch configure instead of configure.in to avoid regenerating build files (bug 223).

* Mon Jul 21 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.7
- Rebuild to get source permissions right (bug 223).
- Removed Requires: /usr/bin/find (bug 223).

* Sat May 10 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.6
- Use RPM_BUILD_ROOT and RPM_OPT_FLAGS instead of macros.

* Sat May 10 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.5
- Backed out Vorbis changes (bug 198, 223).

* Fri May  2 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.4
- Fixed problems with Makefiles being removed from documentation upon
  installation.

* Fri Apr 25 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.3
- Honour %%optflags.
- Vorbis support (bug #198).
- Added LICENSE to documentation.

* Fri Apr  4 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.2
- Minor adjustments of optimisation flags and configure settings.
- Killed some noise caused by a bad gtk macro.
- Added epoch numbers to requires.

* Wed Apr  2 2003 Marius Jøhndal <mariuslj at ifi.uio.no> 0:3.93.1-0.fdr.1
- Initial Fedora RPM release.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Mon Jan 13 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 3.93.1.
- Removed Epoch: tag, upgrade by hand! :-/
