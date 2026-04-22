# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      scim
Version:   1.4.18
Release: 14%{?dist}
Summary:   Smart Common Input Method platform

License:   LGPL-2.1-or-later
URL:       https://github.com/scim-im/scim/
Source0:   https://github.com/scim-im/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:   xinput-scim
Source2:   scim-icons-0.7.tar.gz
Source3:   scim-system-config
Source4:   scim-system-global

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: gtk2-devel, libXt-devel, gtk3-devel
BuildRequires: qt-devel, qt3-devel
# for autoreconf
Buildrequires: autoconf automake gettext libtool intltool
# for system ltdl
Buildrequires: libtool-ltdl-devel
# for autogen.sh
Buildrequires: gnome-common
Requires:  %{name}-libs = %{version}-%{release}
Requires:  imsettings, im-chooser
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives
Obsoletes: iiimf-gtk <= 1:12.2, iiimf-gnome-im-switcher <= 1:12.2, iiimf-server <= 1:12.2, iiimf-x <= 1:12.2
Obsoletes:  iiimf-libs-devel <= 1:12.2
Obsoletes:  iiimf-docs <= 1:12.2
Obsoletes:  iiimf-libs <= 1:12.2, iiimf-csconv <= 1:12.2
Obsoletes:  scim-lang-assamese
Obsoletes:  scim-lang-bengali
Obsoletes:  scim-lang-chinese
Obsoletes:  scim-lang-dhivehi
Obsoletes:  scim-lang-farsi
Obsoletes:  scim-lang-gujarati
Obsoletes:  scim-lang-hindi
Obsoletes:  scim-lang-japanese
Obsoletes:  scim-lang-kannada
Obsoletes:  scim-lang-korean
Obsoletes:  scim-lang-latin
Obsoletes:  scim-lang-malayalam
Obsoletes:  scim-lang-marathi
Obsoletes:  scim-lang-nepali
Obsoletes:  scim-lang-oriya
Obsoletes:  scim-lang-punjabi
Obsoletes:  scim-lang-sinhalese
Obsoletes:  scim-lang-tamil
Obsoletes:  scim-lang-telugu
Obsoletes:  scim-lang-thai
Obsoletes:  scim-lang-tibetan
Obsoletes:  scim-python
Obsoletes:  scim-python-chinese
Obsoletes:  scim-python-english
Obsoletes:  scim-python-pinyin
Obsoletes:  scim-python-xingma
Obsoletes:  scim-python-xingma-cangjie
Obsoletes:  scim-python-xingma-erbi
Obsoletes:  scim-python-xingma-wubi
Obsoletes:  scim-python-xingma-zhengma
Obsoletes:  scim-bridge-qtimm < 0.4.2
Obsoletes:  scim-bridge-qt4 < 0.4.15-3
Provides:   scim-bridge = 0.4.17
Obsoletes:  scim-bridge < 0.4.17
Patch7:     scim_panel_gtk-emacs-cc-style.patch
Patch9:     scim-fixes-compile.patch

%description
SCIM is a user friendly and full featured input method user interface and
also a development platform to make life easier for Input Method developers.


%package devel
Summary:    Smart Common Input Method platform
Requires:   %{name}-libs = %{version}-%{release}
Requires:   gtk2-devel
Requires:   pkgconfig
Obsoletes:  iiimf-libs-devel <= 1:12.2

%description devel
The scim-devel package includes the header files for the scim package.
Install scim-devel if you want to develop programs which will use scim.


%package gtk
Summary:    Smart Common Input Method Gtk IM module
# for %{_libdir}/gtk-2.0/immodules
Requires: gtk2 >= 2.11.6-7.fc8
# for update-gtk-immodules
Requires(post): gtk2 >= 2.9.1-2
Requires(postun): gtk2 >= 2.9.1-2
Provides:   scim-bridge-gtk = 0.4.17
Obsoletes:  scim-bridge-gtk < 0.4.17

%description gtk
This package provides a GTK input method module for SCIM.


%package qt
Summary:    Smart Common Input Method Qt IM module
Provides:   scim-qtimm
Obsoletes:  scim-qtimm
Provides:   scim-bridge-qt = 0.4.17
Obsoletes:  scim-bridge-qt < 0.4.17
Provides:   scim-bridge-qt3 = 0.4.17
Obsoletes:  scim-bridge-qt3 < 0.4.17

%description qt
This package provides a Qt input method module for SCIM.


%package libs
Summary:    Smart Common Input Method libraries
Obsoletes:  iiimf-libs <= 1:12.2, iiimf-csconv <= 1:12.2

%description libs
This package provides the libraries for SCIM.


%package rawcode
Summary:    SCIM Unicode Input Method Engine
Requires:   %{name} = %{version}-%{release}

%description rawcode
This package provides an Input Method Engine for inputting unicode characters
but their unicode codepoints.


%define scim_api 1.4.0

%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/scim.conf


%prep
%autosetup -a2 -p1

cp -p scim-icons/icons/*.png data/icons
cp -p scim-icons/pixmaps/*.png data/pixmaps

# use our system config & global file
mv configs/config{,.orig} 
cp -p %{SOURCE3} configs/config
mv configs/global{,.orig} 
cp -p %{SOURCE4} configs/global

./bootstrap


%build
%configure --disable-static --enable-ld-version-script --with-gtk-version=2
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="%{__install} -p"

# remove .la files
find ${RPM_BUILD_ROOT} -name '*.la' | xargs rm

# remove scim-setup.desktop file since it is confusing with im-chooser
rm ${RPM_BUILD_ROOT}/%{_datadir}/applications/scim-setup.desktop
# remove capplet
rm ${RPM_BUILD_ROOT}/%{_datadir}/control-center-2.0/capplets/scim-setup.desktop

# don't need this
rm -f docs/html/FreeSans.ttf

# install xinput config file
mkdir -pm 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/X11/xinit/xinput.d
install -pm 644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_xinputconf}

%find_lang %{name}



%post
# remove old xinput.d alternatives
%define cjk_langs ja_JP ko_KR zh_CN zh_HK zh_TW
%define indic_langs as_IN bn_IN gu_IN hi_IN kn_IN ml_IN or_IN pa_IN ta_IN te_IN
%define supported_langs %{cjk_langs} %{indic_langs} ne_NE si_LK th_TH vi_VN
for llcc in %{supported_langs}; do
   %{_sbindir}/alternatives --remove xinput-$llcc %{_sysconfdir}/X11/xinit/xinput.d/scim &>/dev/null || :
   # if alternative was set to manual scim, reset to auto
   [ -L %{_sysconfdir}/alternatives/xinput-$llcc -a "`readlink %{_sysconfdir}/alternatives/xinput-$llcc`" = "%{_sysconfdir}/X11/xinit/xinput.d/scim" ] && %{_sbindir}/alternatives --auto xinput-$llcc &>/dev/null || :
done

# xinputrc alternative
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 82 || :


%post gtk
%{_bindir}/update-gtk-immodules %{_host} || :


%ldconfig_scriptlets libs


%postun
if [ "$1" = "0" ]; then
   %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
   # if alternative was set to manual scim, reset to auto
   [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :
fi


%postun gtk
%{_bindir}/update-gtk-immodules %{_host} || :


%files -f %{name}.lang
%doc AUTHORS COPYING README ChangeLog TODO
%dir %{_sysconfdir}/scim
%config(noreplace) %{_sysconfdir}/scim/*
%{_bindir}/*
%dir %{_libdir}/scim-1.0
%{_libdir}/scim-1.0/scim-helper-launcher
%{_libdir}/scim-1.0/scim-helper-manager
%{_libdir}/scim-1.0/scim-launcher
%{_libdir}/scim-1.0/scim-panel-gtk
%dir %{_libdir}/scim-1.0/%{scim_api}
%{_libdir}/scim-1.0/%{scim_api}/Filter
%{_libdir}/scim-1.0/%{scim_api}/FrontEnd
%{_libdir}/scim-1.0/%{scim_api}/Helper
%dir %{_libdir}/scim-1.0/%{scim_api}/IMEngine
%{_libdir}/scim-1.0/%{scim_api}/SetupUI
%{_datadir}/scim
%{_datadir}/pixmaps/*
%config(noreplace) %{_xinputconf}

%files devel
%doc docs/developers
%{_includedir}/scim-1.0
%{_libdir}/libscim*.so
%{_libdir}/pkgconfig/*.pc

%files gtk
%{_libdir}/gtk-2.0/*/immodules/im-scim.so
%{_libdir}/gtk-3.0/*/immodules/im-scim.so

%files qt
%{_libdir}/qt4/plugins/inputmethods/*.so
%{_libdir}/qt-3.3/lib/qt3/plugins/inputmethods/*.so


%files libs
%{_libdir}/libscim-*.so.*
%dir %{_libdir}/scim-1.0
%dir %{_libdir}/scim-1.0/%{scim_api}
%{_libdir}/scim-1.0/%{scim_api}/Config
%dir %{_libdir}/scim-1.0/%{scim_api}/IMEngine
%{_libdir}/scim-1.0/%{scim_api}/IMEngine/socket.so


%files rawcode
%{_libdir}/scim-1.0/%{scim_api}/IMEngine/rawcode.so


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Feb  7 2025 Peng Wu <pwu@redhat.com> - 1.4.18-12
- Fix build
- Resolves: RHBZ#2341330

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 28 2023 Peng Wu <pwu@redhat.com> - 1.4.18-7
- Migrate to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Peng Wu <pwu@redhat.com> - 1.4.18-3
- Update the xinput-scim file

* Thu Aug 19 2021 Peng Wu <pwu@redhat.com> - 1.4.18-2
- Obsoletes scim-bridge
- The code of scim-bridge is merged into scim

* Wed Aug 18 2021 Peng Wu <pwu@redhat.com> - 1.4.18-1
- Update to 1.4.18

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.17-6
- Escape macros in %%changelog

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Peng Wu <pwu@redhat.com> - 1.4.17-3
- Fixes GCC 7 build

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun  2 2016 Peng Wu <pwu@redhat.com> - 1.4.17-1
- Update to 1.4.17

* Tue Apr 12 2016 Peng Wu <pwu@redhat.com> - 1.4.16-1
- Update to 1.4.16

* Mon Feb 15 2016 Peng Wu <pwu@redhat.com> - 1.4.15-7
- Fixes compile with gcc 6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 Peng Wu <pwu@redhat.com> - 1.4.15-5
- Fixes gtk3 input method module dependency

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Rex Dieter <rdieter@fedoraproject.org> 1.4.15-3
- rebuild (gcc)

* Tue Feb 24 2015 Than Ngo <than@redhat.com> - 1.4.15-2
- rebuilt against new gcc5

* Wed Oct 29 2014 Peng Wu <pwu@redhat.com> - 1.4.15-1
- Update to 1.4.15

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Peng Wu <pwu@redhat.com> - 1.4.14-7
- Fixes rawhide build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Peng Wu <pwu@redhat.com> - 1.4.14-4
- Obsoletes scim-python

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012  Peng Wu <pwu@redhat.com> - 1.4.14-2
- Use gtk2 for setup ui

* Mon Jun 25 2012  Peng Wu <pwu@redhat.com> - 1.4.14-1
- Update to 1.4.14

* Mon May 07 2012  Peng Wu <pwu@redhat.com> - 1.4.13-1
- Update to 1.4.13

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011  Peng Wu <pwu@redhat.com> - 1.4.11-1
- Update to 1.4.11

* Tue Jun 21 2011  Peng Wu <pwu@redhat.com> - 1.4.10-3
- As src/ltdl.cpp is removed from source tar ball, remove patch scim-1.4.7-syslibltdl.patch scim-1.4.8-fix-dlopen.patch

* Tue Jun 21 2011  Peng Wu <pwu@redhat.com> - 1.4.10-2
- Refresh patch for 1.4.10
- Remove patch scim-1.4.5-panel-menu-fixes.patch scim_x11_frontend-ic-focus-LTC27940-215953.patch scim-1.4.7-trayicon.patch

* Tue Jun 21 2011  Peng Wu <pwu@redhat.com> - 1.4.10-1
- Update to 1.4.10
- Remove patch scim_panel_gtk-icon-size-fixes.patch scim-gtkimm-default-snooper-off-213796.patch scim-1.4.5-no-rpath-libdir.patch scim-1.4.7-remove-locale.patch scim-1.4.7-fix-fallback.patch scim-1.4.7-fix-capslock.patch scim-1.4.7-fix-gdm.patch scim-1.4.7-remove-help-frame.patch scim-1.4.7-timeout.patch scim-1.4.7-menu-pos.patch scim-1.4.7-xim-wrong-format.patch scim-1.4.7-bz462820.patch scim-1.4.7-imdkit-read-property-properly.patch

* Fri Mar 25 2011  Peng Wu <pwu@redhat.com> - 1.4.9-8
- Obsoletes scim-lang-* and iiimf

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov  5 2009 Jens Petersen <petersen@redhat.com> - 1.4.9-6
- really remove FreeSans.ttf (reported by nim-nim)

* Tue Sep 29 2009 Peng Huang <phuang@redhat.com> - 1.4.9-4
- Remove workaround patch added in 1.4.9-3.
- The bug 517001 has been fixed in glibc.

* Thu Aug 27 2009 Peng Huang <phuang@redhat.com> - 1.4.9-3
- Fix bug 517001 dlopen/dlclose of im-scim.so causes segfault.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May  2 2009 Jens Petersen <petersen@redhat.com> - 1.4.9-1
- update to 1.4.9
- ta.po is now upstream and scim-1.4.7-translation-update-431995.patch
  no longer needed

* Wed Mar 25 2009 Peng Huang <phuang@redhat.com> - 1.4.8-3
- Use lt_dlopenadvise to replace lt_dlopenext to fix bug 491841

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Jens Petersen <petersen@redhat.com> - 1.4.8-1
- update to 1.4.8 release
- initial-locale-hotkey-186861.patch no longer needed
- drop scim-1.4.7_translation-update.tar.bz2 and just add ta.po
- update scim-1.4.7-translation-update-431995.patch
- scim-fix-unload-segfault.patch no longer needed
- add scim-1.4.7-syslibltdl.patch from Gentoo to build with libtool2
- buildrequire libtool-ltdl-devel

* Tue Dec  2 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-37
- make libs subpackage own its dirs for multilib (#473664)

* Fri Nov 21 2008 Peng Huang <phuang@redhat.com> - 1.4.7-36
- Redownload scim-1.4.7.tar.gz from upstream to fix BADSOURCE.

* Thu Oct 16 2008 Peng Huang <phuang@redhat.com> - 1.4.7-35
- Read data from WindowProperty properly (#466657) by Tagoh.

* Fri Oct 10 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-34
- require im-chooser (#466252)
- add scim-thai to the Thai meta package

* Sun Oct 05 2008 Peng Huang <phuang@redhat.com> - 1.4.7-33
- Add ICON="/usr/share/scim/icons/trademark.png" in xinput-scim

* Fri Sep 19 2008 Peng Huang <phuang@redhat.com> - 1.4.7-32
- Resolve: bug 462820 by Parag.

* Wed Aug 27 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-31.fc10
- bring back Ctrl+Space hotkey by default for all locale by popular demand
- drop disabling of uncommon IMEs from global system config since less used
  Chinese tables have been moved to scim-tables-chinese-extra

* Tue Aug 26 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-30.fc10
- restore scim_x11_frontend-ic-focus-LTC27940-215953.patch (#440163)

* Sat Aug 02 2008 Peng Huang <phuang@redhat.com> - 1.4.7-29.fc10
- add patch scim-1.4.7-xim-wrong-format.patch to fix bug 457566 by Akira TAGOH.

* Thu Jul 17 2008 Peng Huang <phuang@redhat.com> - 1.4.7-28.fc10
- add patch scim-1.4.7-menu-pos.patch to fix bug 444711.

* Thu Jul 17 2008 Peng Huang <phuang@redhat.com> - 1.4.7-27.fc10
- add patch scim-1.4.7-timeout.patch to fix bug 444150.
- add patch scim-1.4.7-trayicon.patch to fix bug 447848.

* Mon Jun 30 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-26.fc10
- make xinput script no longer require multilib immodules
  (Julian Sikorski, #448268)
- remove the hacks in xinput script counting the number of IMEs

* Mon Jun 16 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-25.fc10
- require imsettings instead of im-chooser

* Fri Jun 13 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-24.fc10
- scim-sinhala is renamed to scim-sayura

* Wed Apr 30 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-23.fc9
- remove the multilib scim-bridge-gtk requires hack from scim-lang-* (#444681)

* Wed Apr  9 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-22.fc9
- added translations for es, gu, hi, kn, ml, mr, pt_BR, ru, ta, te
  (Red Hat L10n Team, #431995)
- added translations for sk and vi from upstream
- updated translations for de, it, ja, ko, pa, zh_CN (Red Hat L10n Team)
- scim-1.4.7-ja-sinhala-236715.patch is no longer required

* Wed Apr 02 2008 Peng Huang <phuang@redhat.com> - 1.4.7-21.fc9
- Update scim.conf to check qtimm in qt4 folder for qtimm.
- Re-add scim-1.4.7-fix-capslock.patch to fix bug #431222.

* Thu Mar 20 2008 Peng Huang <phuang@redhat.com> - 1.4.7-20.fc9
- Replase scim-system-config.patch with scim-system-global.

* Thu Mar 20 2008 Peng Huang <phuang@redhat.com> - 1.4.7-19.fc9
- Drop scim-system-config.patch and scim-1.4.7-fix-capslock.patch.
- Ignore capslock mask to fix bug #431222.

* Thu Mar 13 2008 Peng Huang <phuang@redhat.com> - 1.4.7-18.fc9
- Replace scim-pinyin to scim-python-pinyin for scim-lang-chinese

* Mon Mar 10 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-17.fc9
- remove the frame around the help text in the help dialog

* Wed Mar 5 2008 Peng Huang <phuang@redhat.com> - 1.4.7-16.fc9
- Remove scim-restart script for fixing #435889.

* Tue Mar 4 2008 Peng Huang <phuang@redhat.com> - 1.4.7-15.fc9
- Let scim gtkim context work with gtk plug widget #251878.

* Mon Mar 3 2008 Peng Huang <phuang@redhat.com> - 1.4.7-14.fc9
- Fix capslock problem #431222.

* Mon Mar 3 2008 Peng Huang <phuang@redhat.com> - 1.4.7-13,fc9
- Fix fallback problem in gtkim module #235147.

* Tue Feb 26 2008 Peng Huang <phuang@redhat.com> - 1.4.7-12.fc9
- Update to scim.conf to use /usr/bin/scim to start scim processes.

* Thu Feb 21 2008 Peng Huang <phuang@redhat.com> - 1.4.7-11.fc9
- Update to scim.conf to make scim can work with imsettings.

* Fri Feb 15 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-10.fc9
- make Wijesekera the default input method for Sinhala

* Thu Feb 14 2008 Peng Huang <phuang@redhat.com> - 1.4.7-9.fc9
- remove support locales in gtk im-scim module to avoid gtk automatically
  picking up scim im module.
- rebuild for gcc43

* Mon Jan 21 2008 Jens Petersen <petersen@redhat.com> - 1.4.7-8.fc9
- change the default Simplified Chinese IME to scim-python Pinyin
- do not set the trigger hotkey for all locale by default
- remove unused ChangeFactoryGlobally key from system config

* Fri Oct 19 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-7.fc8
- quote backquotes in xinput config file (#339271)

* Fri Oct 12 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-6
- make scim-lang-*.x86_64 require scim-bridge-gtk multilib (#327151)

* Thu Sep 20 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-5
- %%{_sysconfdir}/X11/xinit/xinput.d is now owned by im-chooser
- no longer require xorg-x11-xinit

* Tue Sep 18 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-4
- source none.conf in xinput script when skipping scim startup

* Thu Sep 13 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-3
- add scim-1.4.7-ja-sinhala-236715.patch to add Japanese translation of
  Sinhala (#236715)
- gtk2 now owns %%{_libdir}/gtk-2.0/immodules
- add Nepali meta package
- specify full paths in xinput script and use SHORT_DESC

* Fri Aug 17 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-2
- update License field
- modify xinput.d script to not startup scim if no IMEs are installed
- devel package requires pkgconfig
- improve meta package macro language in summary and description 
- subpackage rawcode engine
- update meta packages for m17n-contrib
- move ownership of libdir dirs to main package

* Wed Jun 27 2007 Jens Petersen <petersen@redhat.com> - 1.4.7-1
- update to 1.4.7 release

* Fri Jun 22 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-6
- make Cangjie3 the default input method for Hong Kong and disable Cangjie
  by default instead of Cangjie3 and Cangjie5 (Roy Chan, #245121)

* Thu Jun 21 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-5
- add scim-lang-* meta packages to aid yum package group handling of scim
  core packages so they no longer need to be installed by default

* Tue Jun  5 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-4
- drop scim_panel_gtk-settle-toolbar-after-drag.patch since it interferes with
  user toolbar placement (reported by Ryo Dairiki, #242610)

* Wed May 30 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-3
- save the hotkey for lang in initial-locale-hotkey-186861.patch again

* Tue May 29 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-2
- fix initial-locale-hotkey-186861.patch to read system hotkey config
  correctly (reported by Eugene Teo, #241629)

* Mon May 21 2007 Jens Petersen <petersen@redhat.com> - 1.4.6-1
- update to 1.4.6 release
  - scim_panel-observe-workarea-xprop-204442.patch and
    scim_x11_frontend-ic-focus-LTC27940-215953.patch are no longer needed
  - update scim-1.4.5-panel-menu-fixes.patch and
    scim_panel_gtk-icon-size-fixes.patch

* Fri May  4 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-18
- completely remove scim-setup.desktop to stop it appearing in
  "Applications -> Other" (#238966)

* Wed May  2 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-17
- remove scim-setup from the desktop preferences menu since it is confusing
  with im-chooser and can be started directly from the scim command menu

* Tue May  1 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-16
- unrevert the last changes to initial-locale-hotkey-186861.patch to allow
  no hotkey to be set and define Ctrl+space as the default hotkey for all
  locale again in system config
- require im-chooser

* Wed Apr 18 2007 Warren Togami <wtogami@redhat.com> - 1.4.5-15
- revert previous change made in #235435 due to a more complete solution
  in #236974.  SCIM will no longer start by default on non-Asian locales.
  Non-Asian desktop users can choose to enable scim explicitly with im-chooser.

* Tue Apr 17 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-14
- update initial-locale-hotkey-186861.patch to really turn off the Ctrl-Space
  hotkey by default for non-Asian users (#235435)

* Wed Apr 11 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-13
- do not set a hotkey by default for non-Asian users (#235435)
- move the scim system config file from scim-system-default-config.patch
  into a source file scim-system-config

* Wed Apr  4 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-12
- add X-GNOME-PersonalSettings category to scim-setup.desktop (#234167)
- also use desktop-file-install instead of scim-setup-desktop-file.patch to
  remove Applications category

* Tue Mar 13 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-11
- improve sourceforge url to main tarball (#226395)
- preserve timestamps under make install (#226395)

* Mon Mar 12 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-10
- make only scim-libs own lib directories used by both scim and scim-libs
  since scim requires scim-libs (#226395)
- update desktop file to remove deprecated X-Fedora and Applications
  categories with scim-setup-desktop-file.patch (#226395)

* Fri Mar  9 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-9
- add scim-1.4.5-no-rpath-libdir.patch to remove rpaths to libdir
- rpmlint cleanup (#226395)

* Mon Feb 12 2007 Jens Petersen <petersen@redhat.com> - 1.4.5-8
- separate gtk immodule out to a separate subpackage
- update icons with improvements by Andy Fitzsimon
- add functions to xinput script to test for presence of immodules

* Fri Dec 15 2006 Jens Petersen <petersen@redhat.com> - 1.4.5-7
- improve scim_panel-observe-workarea-xprop-204442.patch to autosnap within
  desktop workarea (#204442)
- add scim_panel_gtk-settle-toolbar-after-drag.patch to autosnap toolbar after
  dragging
- improve initial-locale-hotkey-186861.patch not to set next/previous factory
  and show menu hotkeys by default (#219247)
- remove show factory menu hotkey and add super and hyper as valid modifiers
  in scim-system-default-config.patch
- improve scim-1.4.5-panel-menu-fixes.patch to correctly name recently used
  factories for same language (#217324)

* Fri Dec  1 2006 Jens Petersen <petersen@redhat.com> - 1.4.5-6
- fix scim-restart quoting for pkill -f
- rename scim-turn-off-snooper.patch to
  scim-gtkimm-default-snooper-off-213796.patch

* Fri Dec  1 2006 Jens Petersen <petersen@redhat.com> - 1.4.5-5
- move dl modules used by im-scim.so back to scim-libs for multilib (#215583)
- revert gtkimm-clear-preedit-on-reset-174143.patch for now to be consistent
  with scim-bridge and upstream behaviour (#174143)
- improve scim-restart to also restart xim socket and only kill user's own
  processes (#205547)

* Fri Nov 24 2006 Shawn Huang <phuang@redhat.com> - 1.4.5-4
- add scim-gtkimm-default-snooper-off-213796.patch to turn off key snooper in
  im-scim to avoid crashes when clicking during scim gtkimm preedit (#213796)

* Fri Nov 17 2006 Jens Petersen <petersen@redhat.com> - 1.4.5-3
- add scim_panel-observe-workarea-xprop.patch to make toolbar respect desktop
  work area (Takuro Ashie, #204442)
- add scim_x11_frontend-ic-focus-LTC27940-215953.patch from cvs to fix XIM
  focus preedit commit issue (Shoji Sugiyama, #215953)
- add scim_panel_gtk-emacs-cc-style.patch to set emacs cc-mode style for panel
- reduce systray icon size even more to 11

* Fri Nov 17 2006 Shawn Huang <phuang@redhat.com> - 1.4.5-2
- add scim-fix-unload-segfault.patch to fix xim process segfaulting
  when already running (#206995)

* Tue Nov  7 2006 Jens Petersen <petersen@redhat.com> - 1.4.5-1
- update to 1.4.5 release
- no longer need scim.pc-versioned-moduledir-179706.patch,
  scim_panel_gtk-systray-click-199187.patch,
  scim_panel_gtk-menu-recently-used-factories.patch,
  scim_backup-default-engine-2letter-locale-197058.patch,
  scim_utility-Assamese-locale-fix.patch,
  scim-gtkimm-underline-attrib-206397.patch,
  and scim_x11_frontend-underline-attrib-206397.patch
- update scim-system-default-config.patch, scim_panel_gtk-icon-size-fixes.patch
- add scim-1.4.5-panel-menu-fixes.patch to fix latest factory menu labelling
- improve scim-restart script to also handle scim-bridge (#205547)
- obsolete iiimf-csconv (#211875)
- add Hangul keysym to Korean hotkeys (#212115)

* Thu Nov  2 2006 Jens Petersen <petersen@redhat.com>
- return scim-bridge-qt support to xinput script

* Tue Oct  3 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-35
- reduce tray icon size to 12 to fit button in
  scim_panel_gtk-icon-size-fixes.patch
- add scim-gtkimm-underline-attrib-206397.patch and
  scim_x11_frontend-underline-attrib-206397.patch from upstream cvs (#206397)
- make Chinese full/half width icons darker

* Tue Sep  5 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-34
- remove dist tag from xorg-x11-xinit requires (#204154)
- remove scim-bridge-qt from xinput script for now
- buildrequire gettext instead of gettext-devel

* Fri Sep  1 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-33
- update xinput.d script for scim-bridge
- improvements to menu and full/half width icons (Andy Fitzsimon)

* Thu Aug 24 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-32
- revert tray icon to a button to get transparency working (#198259)
- better full/half icons (Andy Fitzsimon)
- silence remove of old alternatives (#203794)

* Wed Aug  9 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-31
- improve scim_panel_gtk-menu-recently-used-factories.patch to handle
  two letter locale and "other"
- simplify scim_panel_gtk-systray-click-199187.patch to handle switching
  between tray menus better (Qingyu Wang)
- add scim_backup-default-engine-2letter-locale.patch to improve matching of
  m17n maps (#197058)
- add scim_utility-Assamese-locale-fix.patch to list Assamese as as_IN

* Mon Aug  7 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-30
- improvements to scim_panel_gtk-menu-recently-used-factories.patch
  - only list up to 5 recently used factories and only when more than 5 in menu
  - keep menu entry of recenty used factory in original place too
  - fix display of English/European entry
- bring back Ctrl+space hotkey for Japanese and Korean users for backward
  compatibility (#201173)
- include European keyboard in default factories again to avoid breaking
  deadkey support in XIM apps (lxo, #188357)
- move scim modules to the main package

* Fri Jul 28 2006 Qingyu Wang <qwang@redhat.com> - 1.4.4-29
- fix scim_panel_gtk-systray-click-199187.patch for second click away from icon

* Thu Jul 27 2006 Qingyu Wang <qwang@redhat.com> - 1.4.4-26
- fixed the bug 199187 with scim_panel_gtk-systray-click-199187.patch

* Mon Jul 24 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-25
- suffix xinput file with .conf and bump priority to 82
- xinput sub-scripts moved to a subdir
- clearer new half-letter and half-punct icons (Andy Fitzsimon)

* Mon Jul 17 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-24
- update to latest scim-1.4 branch
  - should fix systray icon transparency (Saturo Sato, #198259)
- list factories on menu in most recently used order with
  scim_panel_gtk-menu-recently-used-factories.patch (#187027)
- new set of icons based on Tango project design (Andy Fitzsimon, #187024)
- change defaults to no sticky icon in toolbar and vertical lookup window
- fix various icon size problems with scim_panel_gtk-icon-size-fixes.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-23.1
- rebuild

* Wed Jul  5 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-23
- use xinputrc instead of xinput.d (#194458)
- require xorg-x11-xinit >= 1.0.2-5.fc6

* Wed Jul  5 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-22
- update to head of scim-1.4 branch
  - buildrequire doxygen and build html for snapshots
  - rawcode-unicode-maxlength.patch, scim-panjabi-punjabi.patch, and
    factory-menu-singlet-submenus-187027.patch no longer needed
- prereq gtk2 >= 2.9.1-2 and ignore update-gtk-immodules errors
- remove with_libstdc_preview macro

* Tue Jun 20 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-21
- changes to default system config (scim-system-default-config.patch):
  - set default IMEs for Chinese locale (#187028)
  - only set next and previous factory hotkeys for Chinese locale
  - do not set F9 as a hotkey in Korean locale (#195633)
  - disable rawcode, European keyboard, and various scim-tables Chinese tables
    by default (#187028)

* Thu Jun 15 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-20
- use _host not _target_platform for update-gtk-immodules in scripts (#195343)

* Tue Jun 13 2006 Qingyu Wang <qwang@redhat.com> - 1.4.4-19
- add initial-locale-hotkey-186861.patch to implement locale-based subkeys
  to initialize users' hotkey configuration keys (#186861)
- update scim-system-default-config.patch with localized hotkeys for
  Japanese and Korean

* Thu Jun  1 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-18
- scim-bridge moved to Extras for now (also fixes #191886)

* Tue May 16 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-17
- update to scim-bridge 0.1.8 (#191329)
- test factory-menu-singlet-submenus-187027.patch to avoid having language
  submenus for a single IME

* Tue May  9 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-16
- update to scim-bridge 0.1.7
- improve qtimm setup in xinput.d file

* Tue Apr 18 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-15
- scim-bridge-0.1.6

* Mon Apr 10 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-14
- subpackage scim-bridge and add xinput.d file for scim-bridge
  - add scim_ver and scim_bridge_ver

* Fri Apr  7 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-13
- update to scim-bridge-0.1.4

* Mon Apr  3 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-12
- update to scim-bridge-0.1.3
  - no longer need to bootstrap

* Fri Mar 31 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-11
- include experimental scim-bridge-0.1.2 by Ryo Dairiki (#185693)
  - make scim-bridge the default gtkimmodule for now
- reenable qtimm module (#182177)

* Fri Mar 31 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-10
- build without libstdc++so7 for now
- turn on scim by default for all locale: add xinput.d/default
- drop the redundant module dirs in scim-1.0/
- add Alt-` to list of default hotkeys for Japanese users with us keyboard

* Wed Mar 29 2006 Jens Petersen <petersen@redhat.com>
- make scim-libs prereq libstdc++so7 to avoid update-gtk-immodules error when
  installing on i386 (#186365)
- setup xinput.d for some more locale (as_IN, or_IN, si_LK, vi_VN, and zh_HK)

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-9
- make scim-libs prereq gtk2 > 2.8 to avoid update-gtk-immodules error
  when upgrading from FC4 (#183636)

* Wed Mar  1 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-8
- add scim-system-default-config.patch
  - add Zenkaku_Hankaku as trigger hotkey for Japanese users
  - use static XIM event flow so deadkeys work under XIM in off state (#169975)
- add alternatives as prereq for %%post and %%postun (pknirsch, #182853)

* Fri Feb 24 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-6
- fix Punjabi spelling with scim-panjabi-punjabi.patch (aalam)

* Mon Feb 20 2006 Warren Togami <wtogami@redhat.com> - 1.4.4-5
- Add epoch to iiimf Obsoletes so it actually removes it (#173071)
  NOTE: The goal of these Obsoletes is for the official supported 
  upgrade path to work smoothly.  If users want to use iiimf, they
  are free to do so but their package must be compatible.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-4.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-4
- parse the libstdc++so7 datestamp from the wrapper script

* Thu Feb  9 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-3
- build conditionally with libstdc++so7 preview to workround libstdc++ weak
  symbol version conflicts for c++ gtk apps built with older gcc
  (Benjamin Kosnik, #166041)
  - add with_libstdc_preview switch and tweak libtool to link against newer lib
- do not change scim_binary_version in scim.pc-versioned-moduledir-179706.patch
- set qtimm to xim for now

* Fri Feb  3 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-2
- remove scim-reload-engines-165655.patch since it seems to break input after
  reloading configuration (#179807)
- add gtkimm-clear-preedit-on-reset-174143.patch to clear the preedit buffer
  when IME turned off (Qian Shen, #174143)
- add rawcode-unicode-maxlength.patch to improve input of unicode codes
  (James Su, #173102)
- add scim.pc-versioned-moduledir-179706.patch to include api version in
  moduledir in scim.pc so that IMEs get installed in versioned dir by default
  (Akira Tagoh, #179706)

* Fri Jan 13 2006 Jens Petersen <petersen@redhat.com> - 1.4.4-1
- update to 1.4.4 bugfix release
  - scim-gtk-langs-167090.patch no longer needed since 1.4.3
- move scim dl modules to scim-libs for multilib to work correctly
  - define %%scim_api

* Mon Dec 19 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-9
- enable linker symbol versioning now that mt_alloc is fixed (#173220)
- buildrequire libXt-devel for configure
- buildrequire autoconf, automake, and libtool for autoreconf

* Fri Dec 16 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-8
- rebuild with gcc-4.1

* Mon Nov 14 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-7
- make "reload config" reload IMEs with scim-reload-engines-165655.patch
  (Qian Shen, #165655)
- add iiimf obsoletes for upgrading (#173071)

* Tue Nov  1 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-6
- avoid errors in postun script when uninstalling

* Thu Oct  6 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-5
- fixing quoting in scim-restart
- make post and postun scripts for scim-libs

* Thu Sep 22 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-4
- make scim-devel require scim-libs
- add xinput.d entries for Indic langs

* Thu Sep 15 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-3
- move libs and the gtk immodule to scim-libs for multilib

* Fri Sep  9 2005 Jens Petersen <petersen@redhat.com>
- improve scim-restart script to take account of the config module in use
  (Liu Cougar)

* Fri Sep  2 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-2
- add scim-restart script to make it easier to restart scim after updating
  IMEs with scim-add-restart.patch
- add scim-gtk-langs-167090.patch to set gtk immodule language list empty
  for now so that rhgb doesn't load scim (Warren Togami, #167088)

* Wed Aug 17 2005 Jens Petersen <petersen@redhat.com> - 1.4.2-1
- update to 1.4.2 release

* Thu Aug 11 2005 Jens Petersen <petersen@redhat.com> - 1.4.1-1
- update to 1.4.1 bugfix release
- source scim-qtimm script if present from scim xinput script

* Mon Aug  1 2005 Jens Petersen <petersen@redhat.com> - 1.4.0-3
- bring back the xinput alternatives settings for now
- quote the postun readlink test (wcalee@myrealbox.com, #164674)

* Sat Jul 30 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com>
- don't explicitly --disable-ld-version-script since this turns on versioning

* Sat Jul 30 2005 Jens Petersen <petersen@redhat.com>
- own the system xinput.d dir

* Wed Jul 27 2005 Jens Petersen <petersen@redhat.com> - 1.4.0-2
- initial build for Fedora Core
- remove xinput alternatives settings out to IME packages
- drop the old Chinese manual from docs for now
- make scim-1.0 dirs accessible

* Fri Jul 16 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com> - 1.4.0-1
- update to 1.4.0 release

* Sat Jul  9 2005 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- update to 1.3.3 release
- disable linking with version-scripts for now since they cause some problems
- disable building of static libs

* Tue Jul  5 2005 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- update to 1.3.2 test release
- don't set xinput.d script executable
- no need to set XMODIFIERS explicitly and QT_IM_MODULE in xinput.d script

* Mon Jun 20 2005 Ryo Dairiki <ryo-dairiki@users.sourceforge.net> - 1.2.3-2
- Remove one of doubled capplets for setup.

* Sat May 28 2005 Ryo Dairiki <ryo-dairiki@users.sourceforge.net> - 1.2.3-1
- update to 1.2.3 release

* Fri Mar 13 2005 Ryo Dairiki <ryo-dairiki@users.sourceforge.net> - 1.2.2-9
- Initial packaging for Fedora Extras
- cleanup and fixes (Konstantin Ryabitsev, Jens Petersen)

* Sun Jan 9 2005 James Su <suzhe@tsinghua.org.cn>
- Remove GConf Config module.

* Wed Jan 5 2005 James Su <suzhe@tsinghua.org.cn>
- Remove table IMEngine.

* Fri Aug 6 2004 James Su <suzhe@tsinghua.org.cn>
- Move scim-launcher and scim-panel-gtk to /usr/lib/scim-1.0.

* Sun Jun 20 2004  James Su <suzhe@tsinghua.org.cn>
- Merge all things into one package.

* Sat Jun 19 2004  James Su <suzhe@tsinghua.org.cn>
- Added /usr/libexec/scim-launcher.
- Remove setup module for SocketFrontEnd and SocketIMEngine.

* Mon Mar 8 2004  James Su <suzhe@turbolinux.com.cn>
- Added scim-config-agent.

* Thu Oct 30 2003 James Su <suzhe@turbolinux.com.cn>
- Added Simplified Chinese User Manual.

* Wed Sep 03 2003 James Su <suzhe@turbolinux.com.cn>
- cleanup spec.

* Tue Sep 02 2003 James Su <suzhe@turbolinux.com.cn>
- upto 0.8.0

* Tue Jul 29 2003 James Su <suzhe@turbolinux.com.cn>
- updated to include scim-panel-gtk.

* Thu Jun 19 2003 James Su <suzhe@turbolinux.com.cn>
- updated to include scim-setup and its modules.

* Thu Apr 3 2003 James Su <suzhe@turbolinux.com.cn>
- added suite package, which includes all necessary components of SCIM.

* Tue Mar 25 2003 James Su <suzhe@turbolinux.com.cn>
- updated to v0.4.0

* Wed Feb 26 2003 James Su <suzhe@turbolinux.com.cn>
- implemented dynamic adjust feature for generic table module.
- fixed key handling bug in generic table module.

* Mon Feb 10 2003 James Su <suzhe@turbolinux.com.cn>
- Replaced highlight_start and highlight_end in scim_server
  and scim_frontend with AttributeList (scim_attributes.h)
- Moved icons/* to data/icons and gtkstringview.* to
  utils/

* Thu Jan 2 2003 James Su <suzhe@turbolinux.com.cn>
- updated configure.ac and Makefile.am
- ready to release 0.3.0

* Tue Nov 12 2002 James Su <suzhe@turbolinux.com.cn>
- merged signal system from libinti.
- implemented namespace scim.
- implemented referenced object.
- version 0.3.0

* Tue Nov 05 2002 James Su <suzhe@turbolinux.com.cn>
- minor fixes for table IM module.

* Mon Nov 04 2002 James Su <suzhe@turbolinux.com.cn>
- More IMdkit memory leak fixes.
- Table input method bugfixes.
- version 0.2.2

* Fri Nov 01 2002 James Su <suzhe@turbolinux.com.cn>
- improved table input method.
- actually fixed the memleaks within IMdkit.
- pumped the version to 0.2.1

* Thu Oct 31 2002 James Su <suzhe@turbolinux.com.cn>
- fixed some memory leaks in IMdkit
- reduced memory usage.
- upgraded to libtool-1.4.3

* Tue Oct 29 2002 James Su <suzhe@turbolinux.com.cn>
- finished Generic Table input server module.
- fixed several bugs in scim-lib.

* Thu Oct 10 2002 James Su <suzhe@turbolinux.com.cn>
- used gettext to support i18n message.
- added release info to lib name.

* Mon Sep 30 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.4
- added Embedded Lookup Table style into X11 FrontEnd.
- use wchar_t instead of unsigned long if __STDC_ISO_10646__ defined.

* Sun Sep 22 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.3
- config button of X11 FrontEnd was disabled.

* Fri Sep 6 2002 James Su <suzhe@turbolinux.com.cn>
- simplified the utilities and lookup table interface.

* Wed Aug 21 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.2
- added configuration options to disable modules.
- enhanced X11 FrontEnd.

* Sun Aug 11 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.1
- X11 FrontEnd was enhanced.

* Sat Aug 10 2002 James Su <suzhe@turbolinux.com.cn>
- version 0.1.0
- many bugfixes.
- Help window of X11 FrontEnd was implemented.
- scim can exit cleanly.

* Fri Aug 2 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.13.
- Minor bugfixes.

* Mon Jul 29 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.12.
- Minor bugfixes.

* Sun Jul 28 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.11.
- Minor bugfixes.

* Sun Jul 21 2002 James Su <suzhe@turbolinux.com.cn>
- SCIM 0.0.10.
- Added Simple Config module.

* Sat Jun 22 2002 James Su <suzhe@turbolinux.com.cn>
- first public release of SCIM.

