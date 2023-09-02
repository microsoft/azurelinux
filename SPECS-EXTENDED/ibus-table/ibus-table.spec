Vendor:         Microsoft Corporation
Distribution:   Mariner
# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

Name:       ibus-table
Version:    1.12.4
Release:    4%{?dist}
Summary:    The Table engine for IBus platform
License:    LGPLv2+
URL:        https://github.com/mike-fabian/ibus-table
Source0:    https://github.com/mike-fabian/ibus-table/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Requires:       ibus > 1.3.0
Requires:       python(abi) >= 3.3
%{?__python3:Requires: %{__python3}}
BuildRequires:  gcc
BuildRequires:  ibus-devel > 1.3.0
BuildRequires:  python3-devel

# Test dependencies break the package build.
# Disabling until fixed.
# %if %{with_check}
# BuildRequires:  libappstream-glib
# BuildRequires:  desktop-file-utils
# BuildRequires:  python3-mock
# BuildRequires:  python3-gobject
# BuildRequires:  python3-gobject-base
# BuildRequires:  dbus-x11
# BuildRequires:  xorg-x11-server-Xvfb
# BuildRequires:  ibus-table-chinese-wubi-jidian
# BuildRequires:  ibus-table-chinese-cangjie
# BuildRequires:  ibus-table-chinese-stroke5

# Missing test dependencies:
# BuildRequires:  appstream
# BuildRequires:  ibus-table-code
# BuildRequires:  ibus-table-latin
# BuildRequires:  ibus-table-translit
# BuildRequires:  ibus-table-tv
# A window manger is needed for the GUI test
# BuildRequires:  i3
# %endif

Obsoletes:   ibus-table-additional < 1.2.0.20100111-5

BuildArch:  noarch

%description
The Table engine for IBus platform.

%package -n %{name}-devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}, pkgconfig

%description -n %{name}-devel
Development files for %{name}.

%package tests
Summary:        Tests for the %{name} package
Requires:       %{name} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%setup -q

%build
export PYTHON=%{__python3}
%configure --disable-static --disable-additional --enable-installed-tests
%__make %{?_smp_mflags}

%install
%__rm -rf $RPM_BUILD_ROOT
export PYTHON=%{__python3}
%__make DESTDIR=${RPM_BUILD_ROOT} NO_INDEX=true install pkgconfigdir=%{_datadir}/pkgconfig

%find_lang %{name}

# Check section disabled as it leaves an unmountable /dev file, which breaks the build environment.
# %check
# appstreamcli validate --pedantic --explain --no-net %{buildroot}/%{_datadir}/metainfo/*.appdata.xml
# appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/*.appdata.xml
# desktop-file-validate \
#     $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup-table.desktop
# pushd engine
# # run doctests
#     python3 table.py
#     python3 it_util.py
# popd
# mkdir -p /tmp/glib-2.0/schemas/
# cp org.freedesktop.ibus.engine.table.gschema.xml \
#    /tmp/glib-2.0/schemas/org.freedesktop.ibus.engine.table.gschema.xml
# glib-compile-schemas /tmp/glib-2.0/schemas #&>/dev/null || :
# export XDG_DATA_DIRS=/tmp
# eval $(dbus-launch --sh-syntax)
# dconf dump /
# dconf write /org/freedesktop/ibus/engine/table/wubi-jidian/chinesemode 1
# dconf write /org/freedesktop/ibus/engine/table/wubi-jidian/spacekeybehavior false
# dconf dump /
# export DISPLAY=:1
# Xvfb $DISPLAY -screen 0 1024x768x16 &
# # A window manager and and ibus-daemon are needed to run the GUI
# # test tests/test_gtk.py, for example i3 can be used.
# #
# # To debug what is going on if there is a problem with the GUI test
# # add BuildRequires: x11vnc and start a vnc server:
# #
# #     x11vnc -display $DISPLAY -unixsock /tmp/mysock -bg -nopw -listen localhost -xkb
# #
# # Then one can view what is going on outside of the chroot with vncviewer:
# #
# #     vncviewer /var/lib/mock/fedora-32-x86_64/root/tmp/mysock
# #
# # The GUI test will be skipped if XDG_SESSION_TYPE is not x11 or wayland.
# #
# #ibus-daemon -drx
# #touch /tmp/i3config
# #i3 -c /tmp/i3config &
# #export XDG_SESSION_TYPE=x11

# make check && rc=0 || rc=1
# cat tests/*.log
# if [ $rc != 0 ] ; then
#     exit $rc
# fi

%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/%{name}
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/ibus/component/table.xml
%{_datadir}/applications/ibus-setup-table.desktop
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.engine.table.gschema.xml
%{_bindir}/%{name}-createdb
%{_libexecdir}/ibus-engine-table
%{_libexecdir}/ibus-setup-table
%{_mandir}/man1/*

%files devel
%{_datadir}/pkgconfig/%{name}.pc

%files tests
%dir %{_libexecdir}/installed-tests
%{_libexecdir}/installed-tests/%{name}
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/%{name}

%changelog
* Fri Sep 01 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.4-4
- Disabling test dependencies due to build failures.

* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.4-3
- Disabling missing test dependency.
- License verified.

* Thu Jun 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.12.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Gate build-time check requirements behind the %%with_check macro

* Sun Jan 24 2021 Mike FABIAN <mfabian@redhat.com> - 1.12.4-1
- Update to 1.12.4
- Update translations from Weblate (updated es, cs, fa, pt_BR, zh_CN).
  zh_CN is 100% complete now.

* Wed Jan 06 2021 Mike FABIAN <mfabian@redhat.com> - 1.12.3-1
- Update to 1.12.3
- Pass the key for the command 'cancel' (default Esc) through
  if the preedit is empty
- Resolves: https://github.com/kaio/ibus-table/issues/64

* Mon Jan 04 2021 Mike FABIAN <mfabian@redhat.com> - 1.12.2-1
- Update to 1.12.2
- Update translations from Weblate
  (updated ca, cs, es, fa, ja, pt_BR, pt_PT, tr, zh_CN, zh_HK, zh_TW)

* Fri Sep 04 2020 Mike FABIAN <mfabian@redhat.com> - 1.12.1-1
- Update to 1.12.1
- Enable compose support.
- Add buttons to move key bindings for a command up or down.
- Make translations of 'Edit key bindings for command “%s”' work
- Added it_util.py to POTFILES, it had translatable strings for
  the “About” dialog and the key settings dialog.
- Update translations from Weblate (updated ca, de, fr, tr, uk)

* Wed Aug 26 2020 Mike FABIAN <mfabian@redhat.com> - 1.12.0-1
- Update to 1.12.0
- New setup tool, now keybindings can be configured with a GUI.
- Resolves: https://github.com/kaio/ibus-table/issues/57
- Resolves: https://bugzilla.redhat.com/show_bug.cgi?id=1133127
- Put exact (except tone) pinyin matches next after exact
  matches in the candidate list.
- Resolves: https://github.com/kaio/ibus-table/issues/63
- Allow lookup table orientation “System Default” in the setup
- Remove “spacekeybehavior” option, it became useless as all
  keybindings are configurable now.
- Added a “debuglevel” option.
- Update translations from Weblate (updated ca, cs, de, es, fa,
  fr, ja, pt_BR, pt_PT, uk, zh_TW, zh_HK, zh_CN)

* Sun Aug 16 2020 Mike FABIAN <mfabian@redhat.com> - 1.11.0-1
- Update to 1.11.0
- Make key bindings configurable.
  Only via the command line for the moment, not yet easy to do
  for normal users. I have to rewrite the setup tool eventually
  to make that possible.
- Resolves: https://github.com/ibus/ibus/issues/2241

* Wed Jul 15 2020 Mike FABIAN <mfabian@redhat.com> - 1.10.1-1
- Update to 1.10.1
- Add GUI test
- Make output of ibus-table-createdb deterministic
- Update translations from Weblate (updated fr, tr, zh_CN)

* Wed Jul 01 2020 Mike FABIAN <mfabian@redhat.com> - 1.10.0-1
- Update to 1.10.0
- Add suggestion mode feature
- Resolves: https://github.com/mike-fabian/ibus-table/pull/9
- Resolves: rhbz#835376
- Add test cases for suggestion mode feature
- Fix problems with the behaviour of the property menus
- Use python logging module with log file rotation instead
  of writing to stdout/stderr
- Update translations from Weblate (updated de, es, fr, pt_BR, pt_PT, tr, uk)

* Wed Feb 12 2020 Mike FABIAN <mfabian@redhat.com> - 1.9.25-1
- update to 1.9.25
- Fix crash when changing some options using the menu or the floating panel
- Resolves: rhbz#1803028
- Translation updates (pt_PT)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Mike FABIAN <mfabian@redhat.com> - 1.9.24-1
- update to 1.9.24
- Fixed two typos in message ids (Thanks to Rafael Fontenelle)
- Translation updates (tr, fr, fa, pt, uk)
- New test cases for ibus-table-others

* Tue Jan 07 2020 Mike FABIAN <mfabian@redhat.com> - 1.9.23-1
- update to 1.9.23
- Add exist_ok=True in os.makedirs(path, exist_ok=True) to
  avoid failure due to race condition.
- Resolves:rhbz#1786652
- Move MockEngine classes into a separate file and make
  test_itb.py runnable standalone
- Translation updates for several languages (French at 100%
  now, Brazilian Portuguese at 100% now, Portuguese
  (Portugal) new and now at 31.5%)

* Tue Dec 17 2019 Mike FABIAN <mfabian@redhat.com> - 1.9.22-1
- update to 1.9.22
- Add Turkish translation from Weblate, 100% translated
- Minor translation fixes in some other languages (Punctuation fixes)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Mike FABIAN <mfabian@redhat.com> - 1.9.21-4
- Fix FTBFS in Fedora rawhide/f30: Add gcc and dbus-x11 to BuildRequires
  (Resolves: rhbz#1676299)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 09 2018 Mike FABIAN <mfabian@redhat.com> - 1.9.21-2
- Require the Python interpreter directly instead of using the package name
- Related: rhbz#1619153

* Wed Aug 29 2018 Mike FABIAN <mfabian@redhat.com> - 1.9.21-1
- update to 1.9.21
- Migrate IBusConfig to GSettings.
  Resolves: https://github.com/mike-fabian/ibus-table/issues/4
- Add a test suite
- Add missing tags to ibus-table-createdb.sgml.
  Resolves: https://github.com/mike-fabian/ibus-table/issues/3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.20-2
- Rebuilt for Python 3.7

* Thu May 03 2018 Mike FABIAN <mfabian@redhat.com> - 1.9.20-1
- update to 1.9.20
- Draw InputMode text instead of icon into panel on non-Gnome desktops.
  Resolves: https://github.com/mike-fabian/ibus-table/issues/6
  (Thanks to Takao Fujiwara)
- Make it work with Python2 again

* Mon Apr 30 2018 Mike FABIAN <mfabian@redhat.com> - 1.9.19-1
- update to 1.9.19
- Sync phrases cache from/to external storage (thanks to heiher).
- Update translations from zanata (cs new)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Mike FABIAN <mfabian@redhat.com> - 1.9.18-1
- update to 1.9.18
- validate ibus-table.appdata.xml in %%check
- Update translations from zanata (pt_BR updated, es new)
- Don't query user database if user define phrase and
  dynamic adjust are disabled (thanks to heiher)
- Enable hash map based cache for user database enabled
  (thanks to heiher)
- Import hash map based cache for table database (thanks to
  heiher)
- Install appstream metadata to /usr/share/metainfo/ (thanks
  to jbicha)
- Fix some appdata validation issues (thanks to jbicha)
- Fix bug in Unihan_Variants.txt, 著 U+8457 is both
  simplified *and* traditional Chinese (thanks to heiher)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Mike FABIAN <mfabian@redhat.com> - 1.9.17-1
- update to 1.9.17
- Load .desktop file for ibus-setup-table correctly under Gnome Wayland
- Set WM_CLASS of ibus-setup-table correctly

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Mike FABIAN <mfabian@redhat.com> - 1.9.16-1
- update to 1.9.16
- Avoid running initialization code of ibus_table_location.py
  when using ibus-table-createdb.
- Make it work on Python 3.6 (Unbreak sqlite on Python 3.6)
  (Resolves: rhbz#1413580).

* Mon Jan 16 2017 Mike FABIAN <mfabian@redhat.com> - 1.9.15-1
- update to 1.9.15
- Update translations from zanata (ca, de, fr, uk updated)
- Point to new home-page in the “About” tab.
- Improve README

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.9.14-2
- Rebuild for Python 3.6

* Wed Aug 24 2016 Mike FABIAN <mfabian@redhat.com> - 1.9.14-1
- update to 1.9.14
- Fix bug in Unihan_Variants.txt, 乾 U+4E7E is both simplified
  and traditional Chinese (thanks to Heiher <r@hev.cc>)

* Tue Aug 23 2016 Mike FABIAN <mfabian@redhat.com> - 1.9.13-1
- update to 1.9.13
- When ignoring key release events, “False” should be returned, not “True”
- Resolves: Resolves: rhbz#1369514
- add ibus-table.appdata.xml and make it translatable
- pull some new translations and updates from Zanata
  (ca, fr, pt_BR, and uk are new, ja, zh_CN, and
  zh_TW have updates).

* Wed Mar 16 2016 Mike FABIAN <mfabian@redhat.com> - 1.9.12-1
- update to 1.9.12
- Show the table code in the candidate list when pinyin mode is used
- Resolves: rhbz#1318109

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.11-1
- update to 1.9.11
- Fix bug in Unihan_Variants.txt, U+9762 and U+7CFB are both simplified *and* traditional Chinese
- Resolves: rhbz#1285379
- Add a few more IBus.Text.new_from_string() conversions to make it work on older systems

* Tue Nov 24 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.10-2
- update to 1.9.10
- Fix bug in Unihan_Variants.txt, U+8868 and U+6770 are both simplified *and* traditional Chinese
- Resolves: rhbz#1284749

* Tue Nov 17 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.9-1
- update to 1.9.9
- Fix hotkey matching
- Resolves: rhbz#1282683

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 21 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.8-1
- update to 1.9.8
- Get option 'lookuptableorientation' default value from database (Thanks to Heiher <r@hev.cc>).

* Wed Oct 14 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.7-1
- update to 1.9.7
- When matching hotkeys, ignore all modifiers not requested in the match
- Fix U+8986 in Unihan_variants.txt, it is both simplified *and* traditional Chinese
- Resolves: rhbz#1271036
- Update Unihan_Variants.txt from "2014-05-09 Unicode 7.0.0" to "2015-04-30 Unicode 8.0.0"

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.6-1
- update to 1.9.6
- Use os.path.expanduser('~') instead of os.getenv('HOME')
- Resolves: rhbz#1218023

* Mon Apr 13 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.5-1
- update to 1.9.5
- Don’t strip space when parsing phrases from a source table
- Resolves: rhbz#1211208

* Sat Mar 07 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.4-1
- update to 1.9.4
- Check existence of old log files before trying to delete them
- Resolves: rhbz#1199673

* Mon Mar 02 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.3-1
- update to 1.9.3
- Try to get the English name of the table if run in locale C/POSIX
- Resolves: rhbz#1197001

* Fri Jan 09 2015 Mike FABIAN <mfabian@redhat.com> - 1.9.2-1
- update to 1.9.2
- Use directories according to theXDG Base Directory Specification
- Resolves: rhbz#1172524
- When a leading invalid character is passed through, it needs
  to be remembered in self._prev_char
- Change class “KeyEvent” to store the keycode as well

* Tue Sep 30 2014 Mike FABIAN <mfabian@redhat.com> - 1.9.1-1
- update to 1.9.1
- Use proper fallback when reading the localized table name
- Show pinyin mode as well in the input mode indicator

* Tue Sep 16 2014 Mike FABIAN <mfabian@redhat.com> - 1.9.0-1
- update to 1.9.0
- Redesign the property menus, use sub-menus instead of toggles

* Sun Sep 14 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.11-1
- update to 1.8.11
- fixes a Python backtrace when the dconf key
  /desktop/ibus/engine/table/wubi-jidian86/onechar was not set
* Thu Sep 04 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.10-1
- update to 1.8.10
- Disable auto_commit option for tables which do not have RULES
- Resolves: rhbz#1135759
- Disable hotkey to switch Chinese mode if database is not Chinese
- Disable “onechar” (Phrase mode/Single char mode) option for non-CJK databases

* Tue Aug 26 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.9-1
- update to 1.8.9
- Move some options into a new tab “Details”
- Ignore Shift+Space hotkey to switch fullwidth/halfwidth if the database is not for CJK
- Resolves: rhbz#1133422
- Pass IBus.KEY_KP_Enter to the application if the preedit is empty
- Resolves: rhbz#1133424

* Thu Aug 14 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.8-1
- update to 1.8.8
- Show keyboard shortcuts also in the property menu entries
- Remove “Hide Candidates/Display Candidates” from the properties menu
- If the database is not CJK, set sensitivity to comboboxes
  useful only for CJK to OFF
- Disable properties related to fullwidth/halfwidth for non-CJK tables
- Resolves: rhbz#1128912 - With the new "rusle" table in
  ibus-table-cyrillic, typing space works strangely

* Mon Aug 11 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.7-1
- update to 1.8.7
- Use the “notify::text” signal instead of “activate” on GtkEntry widget.
  This is to make changes in the text entry widgets in the setup tool apply
  immediately.
- Move the “Restore all defaults” button into the GtkButtonBox at the bottom
- Update Unihan_Variants.txt from “2013-02-25 Unicode 6.3.0” to “2014-05-09 Unicode 7.0.0”

* Tue Jul 29 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.6-1
- update to 1.8.6
- Escape % and _ if they are not intended as wildcards
- Resolves: rhbz#1123981

* Mon Jul 21 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.5-1
- update to 1.8.5
- Always write xml output in UTF-8 encoding, not in the encoding
  of the current locale
- Resolves: rhbz#1120919

* Mon Jul 07 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.4-1
- update to 1.8.4
- Tweak defaults for Chinese mode taken from the locale
- Fix prompts for array30 table and don’t use prompts in pinyin mode
- Make it possible to use select keys like F1, F2, F3 ...
- For cangjie* and quick* tables: Use big5 order if the
  freq from the table is the same

* Wed Jun 25 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.3-1
- update to 1.8.3
- Insert a special candidate for the wildcard character itself
  if only a wildcard character has been typed
- Make wildchard characters configurable
- Resolves: rhbz#1110325 - Unable to input question marks in Wubi-jidian

* Mon Jun 09 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.2-1
- update to 1.8.2
- Better sorting of the lookup table in the mixed Chinese modes
- Do not create useless indexes
- Resolves: rhbz#1105465

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.1-1
- update to 1.8.1
- Added support for wildcards (both in table and in pinyin mode)
- Don’t show the prompt characters defined in the table in
  pinyin mode in the auxiliary text

* Tue Jun 03 2014 Mike FABIAN <mfabian@redhat.com> - 1.8.0-1
- update to 1.8.0
- adapt tools/ibus-table-query tothe new database format

* Wed May 28 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140528-1
- update to 1.5.0.20140528
- Use Unicode code point as a last ditch sort key for the candidates
- Fix bug in Unihan_Variants.txt, 同 is both simplified *and* traditional Chinese
- Update Unihan_Variants.txt from “2011-08-08 Unicode 6.1.0” to “2013-02-25 Unicode 6.3.0” and regenerate engine/chinese_variants.py

* Tue May 27 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140527-1
- update to 1.5.0.20140527
- Put exact matches always at the top of the candidate list
- Fix typo in the filtering for Chinese mode 3 (All characters with traditional Chinese first)
- Support prompt characters (e.g. for cangjie and stroke5)

* Mon May 19 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140519-1
- update to 1.5.0.20140519
- rewrite major parts of ibus-table, fix many bugs.

* Wed Apr 16 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140416-1
- Do not fail when the environment variable HOME is not set
- Resolves: rhbz#1088138
- some code cleanup

* Wed Apr 09 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140409-1
- Make toggling pinyin mode with the right shift key work
- Don’t try to colour system phrases and user phrases differently in pinyin mode
- Resolves: rhbz#1084684
- Don’t switch off pinyin mode in clear()
- Make usage of engine name and dconf key consistent

* Wed Apr 02 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140402-1
- Fix a regression caused by the Python3 port in tabcreatedb.py (This fixes the build of ibus-table-chinese)

* Wed Mar 12 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140312-2
- fix yet another regression introduced by the Python3 port (problem occured when filtering Chinese characters, see rhbz#1072940 comment#18)
- Resolves: rhbz#1072940

* Wed Mar 12 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140312-1
- update to latest upstream
- fix another regression introduced by the Python3 port (a spelling mistake in a variable name)
- Resolves: rhbz#1072940

* Tue Mar 11 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140311-1
- update to latest upstream
- fix a regression introduced by the Python3 port
- add a .desktop file and make the setup tool work with Gnome
- make it possible to interrupt the setup tool with Control-C from the command line

* Thu Mar 06 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140306-1
- update to latest upstream
- Resolves: rhbz#1072940 - Left Shift stopped work for ibus-table-1.5.0.20140218-1.fc20.noarch
- port from Python2 to Python3, require Python3 in this rpm now
- fix directory for setup tool, setup tool should work now
- add profiling support

* Tue Feb 18 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20140218-1
- update to latest upstream
- Resolves: rhbz#1061345 - ibus-table shows entered text in password fields
- remove patches which are included upstream
- remove old, unused patches

* Fri Jan 24 2014 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20130419-3
- Resolves: rhbz#1051365 - suggestion: move ibus-table-createdb to a subpackage
- When tabcreatedb.py is called without any options, print a usage message. Do not just show a cryptic backtrace.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0.20130419-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Mike FABIAN <mfabian@redhat.com> - 1.5.0.20130419-1
- update to latest upstream
- remove patches which are included upstream
- Resolves: #948454 - Man page scan results for ibus-table

* Thu Feb 14 2013 Mike FABIAN <mfabian@redhat.com> - 1.5.0-2
- Resolves: #911487 - Non-Chinese tables from the ibus-table-other package do not work
- Add auto_select functionality to select the first phrase when typing.
  Useful for Cyrillic transliteration
- Update cmode property in chinese mode only
- Fall back to auto_select = False if neither dconf nor the table
  have a value for auto_select
- Preedit needs to be updated on page-up and page-down

* Mon Jan 28 2013 Mike FABIAN <mfabian@redhat.com> - 1.5.0-1
- update to latest upstream 1.5.0  from Caius ‘kaio’ Chance’s repository
- add patches for better simplified/traditional Chinese detection
- Resolves: #857967 - simplified/traditional Chinese detection in ibus-table does not work well

* Thu Jan 10 2013 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20130110-1
- Resolves: #513901 ibus-table setup does not store config settings
- update to latest upstream 1.4.99.20130110 from Caius ‘kaio’ Chance’s repository, 1.5.0 branch
- When detecting the Chinese mode from the environment, also check LC_ALL
- Fix typo in self._chinese_mode variable (The typo broke the SC/TC property)
- Make cursor in lookup table always visible (became invisible after the port to GObjectIntrospection)
- apply changes in values of dconf keys immediately

* Tue Jan 08 2013 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20130108-1
- update to latest upstream 1.4.99.20130108 from Caius ‘kaio’ Chance’s repository, 1.5.0 branch
- includes port to GObjectIntrospection now

* Thu Jan 03 2013 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20130103-1
- update to latest upstream 1.4.99.20130103 from Caius ‘kaio’ Chance’s repository, 1.5.0 branch

* Tue Nov 13 2012 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20121113-1
- update to latest upstream 1.4.99.20121113 from Caius ‘kaio’ Chance’s repository, using rel20121101 git tag
- remove ibus-table-1.4.99.20120907-improve-chinese-category-check.patch (included upstream)
- remove fix-ipa-x-sampa-table-and-phrases-containing-spaces.patch (included upstream)
- Fix marking of translatable strings for gettext
- update zh_??.po files
- Add German translation
- Do not fail if the ~/.ibus/byo-tables/ directory does not exist

* Thu Sep 13 2012 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20120907-3
- Resolves: #856903
- Fix ipa-x-sampa table and phrases containing spaces in emoji-table
  Currently there is a regular expression which filters out several
  lines defining valid phrases. The emoji-table for example has phrases
  containing spaces which are currently filtered out and the ipa-x-sampa
  table has trailing comments which are filtered out as well.

* Tue Sep 11 2012 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20120907-2
- Resolves: #856320
- Improve check whether a phrase is simplified or traditional Chinese
  The improvement is to ignore all non-Han characters when
  doing the check.
  This is to avoid classifying a simplified Chinese string as
  traditional just because it happens to include some non-Chinese
  characters, for example box drawing characters, which cannot be
  converted to gb2312 but happen to be convertible to big5hkscs.
  This fixes the problem in the emoji-table input method that most
  phrases cannot be input at all.

* Fri Sep 07 2012 Mike FABIAN <mfabian@redhat.com> - 1.4.99.20120907-1
- Relates: #855250
- see comment#1 in #855250
- update to latest upstream 1.4.99.20120907 from Caius 'kaio' Chance's repository
- remove ibus-table-1.3.9.20110827-add-some-keys-for-translit.patch (included upstream)
- remove ibus-table-1.3.9.20110827-enable-non-ascii.patch (included upstream)

* Wed Sep 05 2012 Mike FABIAN <mfabian@redhat.com> - 1.3.9.20110827-4
- Resolves: #845798
- add ibus-table-1.3.9.20110827-add-some-keys-for-translit.patch (from Yuwei YU, upstream)
- add ibus-table-1.3.9.20110827-enable-non-ascii.patch  (from Yuwei YU, upstream)
- add ibus-table-1.3.9.20110827-uppercase-umlauts.patch to allow uppercase as well in translit

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9.20110827-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9.20110827-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 31 2011 Caius 'kaio' Chance - 1.3.9.20110827-1
- Updated to upstream. 

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.20100621-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Ding-Yi Chen <dchen@redhat.com> - 1.3.0.20100621-4
- Rebuild for ibus-1.4

* Wed Sep  1 2010 Jens Petersen <petersen@redhat.com> - 1.3.0.20100621-3
- remove the redundant post and postun scripts (#625330)

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.0.20100621-2
- recompiling .py files against Python 2.7 (rhbz#623320)

* Mon Jun 21 2010 Caius Chance <cchance@redhat.com> - 1.2.0.20100621-1
- Updated from upstream which tarball was rebuilt with IBus 1.3.

* Wed Mar 10 2010 Caius 'kaio' Chance <cchance at redhat.com> - 1.2.0.20100111-7
- Add template.txt in files.

* Wed Mar 10 2010 Caius 'kaio' Chance <cchance at redhat.com> - 1.2.0.20100111-6
- Disable -additional.

* Wed Mar 10 2010 Caius 'kaio' Chance <cchance at redhat.com> - 1.2.0.20100111-5
- Remove -additional for obsoletion by ibus-table-latin and ibus-table-code.

* Mon Feb 15 2010 Caius 'kaio' Chance <cchance at redhat.com> - 1.2.0.20100111-4.fc13
- Fixed latex.svg location.

* Fri Jan 29 2010 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20100111-3.fc13
- Split .pc to -devel subpackage.

* Thu Jan 14 2010 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20100111-2.fc13
- Temporary keep files of additional available in ibus-table until 
  ibus-table-{code,latin} packages are ready in repository.

* Mon Jan 11 2010 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20100111-1.fc13
- Updated source from upstream.
- Migreate tables from ibus-table-additional to ibus-table-latin and ibus-table-code.

* Wed Jan 06 2010 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090912-3.fc13
- Apply parsing equal sign patch.

* Wed Nov 11 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090912-2.fc13
- Fix crashing caused by speedmeter.

* Fri Sep 04 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090912-1.fc12
- Upgraded to upstream source.

* Fri Sep 04 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090904-1.fc12
- Updated source with additional tables separated.

* Thu Sep 03 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090902-2.fc12
- Rebuilt.

* Wed Sep 02 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090902-1.fc12
- Updated source.

* Tue Aug 04 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090804-1.fc12
- Cleaned up unused dcommit contents.

* Mon Aug 03 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090803-1.fc12
- Updated to upstream.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090625-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090625-2.fc12
- Rebuilt.

* Wed Jul 01 2009 Caius 'kaio' Chance <k at kaio.me> - 1.2.0.20090625-1.fc12
- Updated source from upstream, which released for IBus 1.2 and so on.

* Wed May 27 2009 Caius 'kaio' Chance <cchance@redhat.com> - 1.1.0.20090527-1.fc12
- Updated source from upstream, which with candidate order fix.

* Mon Mar 16 2009 Caius Chance <cchance@redhat.com> - 1.1.0.20090316-1.fc11
- Resolves: rhbz#490396
- Updated source tarball.
- Disabled speedmeter until config option is implemented.

* Fri Mar  6 2009 Jens Petersen <petersen@redhat.com> - 1.1.0.20090220-5
- make pkgconfig noarch with ibus-table-pkgconfig-noarch.patch
- fix license field: actually LGPL
- drop gettext-devel BR
- require ibus > 1.1.0

* Mon Mar 02 2009 Caius Chance <cchance@redhat.com> - 1.1.0.20090220-4.fc11
- Rebuilt.

* Mon Mar 02 2009 Caius Chance <cchance@redhat.com> - 1.1.0.20090220-3.fc11
- Rebuilt.

* Mon Mar 02 2009 Caius Chance <cchance@redhat.com> - 1.1.0.20090220-2.fc11
- Rebuilt.

* Mon Mar 02 2009 Caius Chance <cchance@redhat.com> - 1.1.0.20090220-1.fc11
- Resolves: rhbz#484650
- Updated to latest upstream release.
- Splitted chinese input methods into modules.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.20081014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Caius Chance <cchance@redhat.com> - 0.1.1.20081014-4
- Resolves: rhbz#466430 rhbz#466844
- Added wildcard features.
- Added preedit clearance on refocus.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081014-3
- Rebuild for Python 2.6

* Mon Dec 1 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081014-2
- Modified spec file to own all directories created by ibus-table.

* Tue Oct 14 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081014-1
- Update to 0.1.1.20081014.

* Mon Sep 01 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Tue Aug 19 2008 Yu Yuwei <acevery@gmail.com> - 0.1.1.20080829-1
- The first version.
