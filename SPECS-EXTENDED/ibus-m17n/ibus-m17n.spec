%global require_ibus_version 1.4.0

Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       ibus-m17n
Version:    1.4.18
Release:    2%{?dist}
Summary:    The M17N engine for IBus platform
License:    GPL-2.0-or-later
URL:        https://github.com/ibus/ibus-m17n
Source0:    https://github.com/ibus/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext-devel >= 0.19
BuildRequires:  gtk3-devel
BuildRequires:  ibus-devel >= %{require_ibus_version}
BuildRequires:  libappstream-glib
BuildRequires:  libtool
BuildRequires:  libtool
BuildRequires:  m17n-lib-devel
BuildRequires:  make

Requires:   ibus >= %{require_ibus_version}
Requires:   m17n-lib

%description
M17N engine for IBus input platform. It allows input of many languages using
the input table maps from m17n-db.

%prep
%autosetup

%build
autoreconf -vif
%configure --disable-static --with-gtk=3.0
%{make_build}

%install
%{make_install}

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README
%license COPYING
%{_datadir}/metainfo/m17n.appdata.xml
%{_datadir}/ibus-m17n
%{_datadir}/icons/hicolor/16x16/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/22x22/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/24x24/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/32x32/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/48x48/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/64x64/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/128x128/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/256x256/apps/ibus-m17n.png
%{_datadir}/icons/hicolor/scalable/apps/ibus-m17n.svg
%{_libexecdir}/ibus-engine-m17n
%{_libexecdir}/ibus-setup-m17n
%{_datadir}/ibus/component/*
%{_datadir}/applications/ibus-setup-m17n.desktop
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.engine.m17n.gschema.xml

%changelog
* Mon Mar 06 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.4.18-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License Verified

* Wed Dec 07 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.18-1
- Update to 1.4.18
- Add new icon

* Sat Nov 26 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.17-2
- Migrate license tag to SPDX

* Sat Sep 17 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.17-1
- Update to 1.4.17
- Fix problem that sa-IAST input method cannot be activated and make settings of sa-IAST work
  (Resolves: https://github.com/ibus/ibus-m17n/issues/52)
- Let IBusM17nEngine inherit from IBusEngineSimple to enable compose support
  (Resolves: https://github.com/ibus/ibus-m17n/pull/51)

* Thu Sep 08 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.13-1
- Update to 1.4.13
- Translation update from Weblate (ar updated 100%, ka added 100%)

* Sat Sep 03 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.11-1
- Update to 1.4.11
- Added translation using Weblate (Arabic, 100%)
- Add 256x256 icon to m17n.appdata.xml

* Wed Aug 03 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.10-1
- Update to 1.4.10
- Add language to longname in --xml output to make engines which have exactly
  the same icon distinguishable in the engine switcher
- Make the icon of the current engine appear at the left of floating panel of ibus.
  And also show the full engine name as a tooltip on that icon
  Before only a generic gear wheel ⚙️ was shown, the same for
  all engines, so one could not distinguish which engine was
  selected in the floating panel.
- Show also the engine name in the title of the setup tool window.
  I.e. instead of just “Preferences” show something like
  “Preferences m17n:t:latn-post”.
- Better icon and a screenshot which can be shown in gnome-software
- Improvements in m17n.appdata.xml

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Mike FABIAN <mfabian@redhat.com> - 1.4.9-1
- Update to 1.4.9
- Free lang and name after engine_name is built
  (Resolves: https://github.com/ibus/ibus-m17n/issues/39)
- Just return from ibus_m17n_engine_callback with nullable m17n
- Accept virtual engine names for CI
- Hide status from the panel if status == title (by Daiki Ueno)

* Tue Oct 19 2021 Mike FABIAN <mfabian@redhat.com> - 1.4.8-1
- Update to 1.4.8
- Remove gnome-common requirement and re-write autogen.sh (by Parag Nemade)
  (Resolves: https://github.com/ibus/ibus-m17n/pull/37)
- Translation update from Weblate for Sinhala

* Tue Oct 19 2021 Parag Nemade <pnemade AT redhat DOT com> - 1.4.7-2
- Remove BR: gnome-common and pkgconfig as it is not needed for released tarball

* Fri Aug 13 2021 Mike FABIAN <mfabian@redhat.com> - 1.4.7-1
- Update to 1.4.7
- Assign symbols to all the new inscript2 engines (and add some other missing symbols)
  (Resolves: https://github.com/ibus/ibus-m17n/issues/34)
- Allow to use kbd engines (#32)
  (Resolves: https://github.com/ibus/ibus-m17n/issues/32)
- ibus-m17n-xkb-options.patch from Fedora included upstream
- ibus-m17n-enable-ar-kbd.patch from Fedora included upstream

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Mike FABIAN <mfabian@redhat.com> - 1.4.6-1
- Update to 1.4.6
- Make inscript2 engines rank higher than inscript engines
- Resolves: rhbz#1982546

* Fri Mar 12 2021 Mike FABIAN <mfabian@redhat.com> - 1.4.5-1
- Update to  1.4.5
- Use ibus_engine_update_preedit_with_mode() *always* with IBUS_ENGINE_PREEDIT_COMMIT mode
- Translation update from Weblate, bn new and 100% complete, pt_BR now 100% complete
- Remove redundant target for desktop.in file

* Thu Jan 28 2021 Mike FABIAN <mfabian@redhat.com> - 1.4.4-1
- Update to  1.4.4
- Translation update from Weblate, zh_CN now 100% complete.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Mike FABIAN <mfabian@redhat.com> - 1.4.3-1
- Update to  1.4.3
- New translation: es (Spanish) 100%.

* Sat Apr 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 1.4.2-4
- No need to call autogen.sh in %%prep section

* Wed Mar 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 1.4.2-3
- Use make_build and make_install macros

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Mike FABIAN <mfabian@redhat.com> - 1.4.2-1
- Update to  1.4.2
- New translations: tr (Turkish) 100%, uk (Ukrainian) 100%,
  id (Indonesian) 100%, ja_JP (Japanese) 100%.
- Translation updates: zh_CN, pt_BR

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Mike FABIAN <mfabian@redhat.com> - 1.4.1-1
- Update to  1.4.1
- Fix for google code issue 1781 in ibus-m17n for kk (Correct symbols for kk input methods)
- Add German translations
- Add m17n.appdata.xml

* Tue Oct 23 2018 Mike FABIAN <mfabian@redhat.com> - 1.4.0-1
- Update to  1.4.0
- Migration from IBusConfig to GSettings
- Remove patches which are included upstream now

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.3.4-26
- Fix the upstream URL and Source0 tags

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.3.4-21
- Resolves:rhbz#1076945 - Enable default ar-kbd.mim for Arabic language

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.3.4-18
- Register as an AppStream component.

* Thu Nov  6 2014 Daiki Ueno <dueno@redhat.com> - 1.3.4-17
- Add ibus-m17n-content-type.patch
- Fix bug 1024071 - ibus-m17n is enabled in the password entry field
  of the lock screen

* Tue Sep 16 2014 Daiki Ueno <dueno@redhat.com> - 1.3.4-16
- Add ibus-m17n-fix-preferences-ui.patch
- Fix bug 1117720 - ibus-m17n input method's setup option does not work

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Daiki Ueno <dueno@redhat.com> - 1.3.4-13
- Use gettext-0.19 instead of intltool (#1078169)

* Wed Sep  4 2013 Daiki Ueno <dueno@redhat.com> - 1.3.4-12
- Add ibus-m17n-fix-preedit-color.patch
- Fix bug 995842 - Preedit background colour in ibus-m17n is always
  black and preedit underlining is always off

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Daiki Ueno <dueno@redhat.com> - 1.3.4-10
- Add ibus-m17n-fix-data-location.patch
- Fix bug 962144 [abrt] ibus-m17n-1.3.4-9.fc19:
  setup_dialog_load_config: Process /usr/libexec/ibus-setup-m17n was
  killed by signal 11 (SIGSEGV)

* Wed May  1 2013 Daiki Ueno <dueno@redhat.com> - 1.3.4-9
- Update ibus-m17n-xkb-options.patch to set XKB option for Inscript2
- Fix bug 957993 - ibus-m17n doesn't automatically map Alt_R to AltGr
  when Inscript2 maps are used

* Fri Apr 26 2013 Daiki Ueno <deno@redhat.com> - 1.3.4-8
- Update ibus-m17n-HEAD.patch to the latest upstream master
- Remove unnecessary and not upstreamable patches
- Use gtk3 always
- Fix bug 912592 - ibus-m17n should use default keyboard in most cases

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 Daiki Ueno <dueno@redhat.com> - 1.3.4-6
- Add ibus-m17n-desktop-file.patch
  Fix bug 860955 - ibus-m17n setup is not enabled in
  gnome-control-center region, .desktop file is missing

* Wed Sep 26 2012 Daiki Ueno <dueno@redhat.com> - 1.3.4-5
- Add ibus-m17n-honor-user-cflags.patch

* Wed Aug 15 2012 Daiki Ueno <dueno@redhat.com> - 1.3.4-4
- Add ibus-m17n-translit-layout.patch
- Fix bug 847495 - For non-US keyboard layout Ibus-m17n adds English
  (US) to the list of input methods and other input methods use US
  layout
- Require eekboard-service instead of eekboard
- Fix bug 847500 - Don't install Eekboard by default in the desktop spin

* Thu Aug  2 2012 Daiki Ueno <dueno@redhat.com> - 1.3.4-3
- Add ibus-m17n-fix-mtext-config.patch
- Fix bug 836397 - [abrt] ibus-m17n-1.3.3-11.fc17: mtext_data: Process
  /usr/libexec/ibus-setup-m17n was killed by signal 11 (SIGSEGV)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Daiki Ueno <dueno@redhat.com> - 1.3.4-1
- New upstream release.

* Tue Apr  3 2012 Daiki Ueno <dueno@redhat.com> - 1.3.3-12
- Check %%{rhel} version in addition to %%{fedora}
- Remove unnecessary %%defattr(-,root,root,-) from %%files
- Drop libxklavier-devel from BR

* Fri Mar 30 2012 Daiki Ueno <dueno@redhat.com> - 1.3.3-11
- Revive m17n:zh:pinyin with a different label ("hanyu pinyin (m17n)")
- Rebase ibus-m17n-virtkbd.patch

* Tue Mar  6 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.3-9
- Rebuild for ibus 1.4.99.20120304

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-7
- Add ibus-m17n-custom-setup-element.patch
- Fix bug 760427 - engine preferences button in ibus-setup doesn't
  work for ibus-m17n

* Fri Nov 18 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-6
- Add ibus-m17n-blacklist-engines.patch
  https://lists.fedoraproject.org/pipermail/i18n/2011-October/001194.html

* Thu Sep 29 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-5
- Add ibus-m17n-hide-title-status.patch.
- Fix bug 741157 - ibus-m17n: m17n "title" variable appears as a
  dormant button on the language panel

* Fri Sep 16 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-4
- Fix Indic IME symbols (thanks to pravins).

* Fri Sep  9 2011 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.3-3
- Rebuild with the latest ibus 1.3.99.20110817-4 and eekboard 1.0.3

* Fri Sep  2 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-2
- Revive iok patch.

* Thu Sep  1 2011 Daiki Ueno <dueno@redhat.com> - 1.3.3-1
- New upstream release.
- Add ibus-m17n-default-xml-override.patch.
- Add ibus-m17n-virtkbd.patch, instead of ibus-m17n-iok.patch.

* Tue Aug  9 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-10
- Set symbol for m17n:ne:rom.

* Mon Aug  8 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-9
- Update ibus-m17n-xkb-options.patch.
- Don't set XKB options directly from engine but via ibus-xkb

* Fri Aug  5 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-8
- Update ibus-m17n-xx-icon-symbol.patch.
- Fix bug 727024 - ibus compose file needs a symbol tag for gnome-shell
- Update ibus-m17n-xkb-options.patch.

* Thu Jul  7 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-7
- don't specify --with-hotkey.

* Mon Jul  4 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-6
- Add ibus-m17n-xkb-options.patch.
- Add ibus-m17n-xx-icon-symbol.patch.
- Drop surrounding-text patches since they are included in the HEAD patch.

* Wed Jun 15 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-5
- Add ibus-m17n-stsreq.patch.
- Fix bug 711126 - ibus: surrounding text support fails for the first
  syllable upon activation

* Tue Jun  7 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-4
- Add ibus-m17n-stscap.patch.
- Fix bug 711126 - ibus: surrounding text support fails for the first
  syllable upon activation

* Mon May 23 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-3
- Update ibus-m17n-HEAD.patch.

* Mon May 23 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-2
- Bump the release to fix upgrade path.
- Fix bug 706602 - ibus-m17n-1.3.2-2.fc14 > ibus-m17n-1.3.2-1.fc15
- Drop preparing/cleaning buildroot.

* Mon Mar  7 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-1
- New upstream release.

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.3.1-18
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 1.3.1-16
- Rebuild against newer gtk

* Fri Jan 14 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-15
- Update iok patch.
- Fix bug 669128 - [abrt] ibus-m17n-1.3.1-14.fc15:
  Process /usr/libexec/ibus-engine-m17n was killed by signal 6 (SIGABRT)

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 1.3.1-14
- Rebuild against newer gtk3

* Mon Dec 27 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-13
- Update iok patch.

* Wed Dec 22 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-12
- Update surrounding-text patch.

* Fri Dec 10 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-11
- Update ibus-m17n-HEAD.patch.
- Lower si-samanala.mim rank per request from a Sinhala user.

* Wed Dec  8 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-10
- Update ibus-m17n-HEAD.patch.
- Fix bug 658336 - ibus-m17n: define the IM ranks in a config file and
  not in a compiled binary

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.1-9
- Rebuild against newer gtk3

* Tue Nov  9 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-8
- Apply ibus-m17n-ibus-1.4.patch for ibus-1.3.99.
- Specify backup filename for each patch.

* Fri Nov  5 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-7
- Rename ibus-m17n-fedora.patch to ibus-m17n-HEAD.patch since the
  changes are merged into upstream.
- Update ibus-m17n-HEAD.patch with upstream fix 08e06310
- Fix bug 649230 - [si] last input character is committed late in
  wijesekara input method

* Fri Oct 22 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-6
- Link ibus-setup-m17n with GTK+ 3.0.

* Tue Oct 12 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-5
- put several Fedora patches into one.
- Fix bug 640896 - Ibus does not load all the keymaps for a language
  that is used for logging in.

* Tue Oct  5 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-4
- Remove Shift+AltGr patch; apply a simplified AltGr patch.
- Fix bug 639963 - SHIFT switch is not working in layouts as expected.

* Fri Oct  1 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-3
- Apply a patch to handle Shift+AltGr.
- Update surrounding-text patch.
- Fix bug 634829 - [abrt] ibus-m17n-1.3.1-1.fc14: shift_state: Process
  /usr/libexec/ibus-engine-m17n was killed by signal 11 (SIGSEGV).

* Thu Sep 16 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-2
- Apply surrounding text patch.  Bug 435880.

* Fri Sep  3 2010 Daiki Ueno <dueno@redhat.com> - 1.3.1-1
- Update to 1.3.1.
- Fix bug 615158 - Do not change the background colour of the pre-edit buffer
- Add gtk2-devel to BR
- Install ibus-setup-m17n in %%{_libexecdir}

* Thu Aug 26 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0-4
- Rebuild with ibus 1.3.7 to avoid ABI incompatibility.  Bug 627256.

* Tue Jul 27 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0-3
- Update ibus-m17n-HEAD.patch.
- Fix regression with the previous update.  See comment 7 of bug 614867.

* Fri Jul 16 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0-2
- Update ibus-m17n-HEAD.patch.
- Fix bug 614867 - Invisible pre-edit buffer when using m17n Wijesekera keyboard layout
- Update iok patch.

* Mon Mar 29 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.3.0-1
- Update to 1.3.0.
- Update iok patch.
- Fix bug 577148 - IOK screen appears with all keyboard layouts on ibus language panel

* Tue Feb 02 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.2.99.20100202-1
- Update to 1.2.99.20100202.
- Update iok patch.

* Thu Dec 17 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20091217-1
- Update to 1.2.0.20091217.
- Update iok patch.

* Fri Nov 20 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20091120-1
- Update to 1.2.0.20091120.
- Fix bug 530976

* Fri Oct 23 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090617-5
- Update iok patch to fix bug 530493.

* Wed Oct 14 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090617-4
- Update iok patch to fix build error.

* Tue Oct 13 2009 Parag <pnemade@redhat.com> - 1.2.0.20090617-3
- Re-enable iok support to ibus-m17n.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090617-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090617-1
- Update to 1.2.0.20090617.

* Thu Mar 05 2009 Parag <pnemade@redhat.com> - 1.1.0.20090211-4
- Add iok support to ibus-m17n.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0.20090211-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090211-2
- Add patch ibus-m17n-HEAD.patch from upstream git tree.
- Make Control + Alt + ... available. (#482789)

* Wed Feb 11 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090211-1
- Update to 1.1.0.20090211.

* Thu Feb 05 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090205-1
- Update to 1.1.0.20090205.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081013-4
- Rebuild for Python 2.6

* Thu Oct 16 2008 Jens Petersen <petersen@redhat.com> - 0.1.1.20081013-3
- move the .engine files to m17n-db and m17n-contrib (#466410)

* Wed Oct 15 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081013-2
- Move unicode, rfc1345 to generic package, and syrc-phonetic to syriac package.

* Mon Oct 13 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081013-1
- Update to 0.1.1.20081013.

* Thu Oct 09 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081009-1
- Update to 0.1.1.20081009.

* Mon Sep 01 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Sat Aug 23 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080823-1
- Update to 0.1.1.20080823.

* Fri Aug 15 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080815-1
- Update to 0.1.1.20080815.

* Tue Aug 12 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080812-1
- Update to 0.1.1.20080812.

* Thu Aug 07 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.0.20080810-1
- The first version.
