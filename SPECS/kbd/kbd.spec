# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# {_exec_prefix}/lib/kbd is correct even on x86_64.
# It is traditionally used for kdb data (console fonts, keymaps, ...).
# It is not used for any shared objects/executables.
%global kbd_datadir %{_exec_prefix}/lib/kbd

Name:           kbd
Version:        2.8.0
Release:        3%{?dist}
Summary:        Tools for configuring the console (keyboard, virtual terminals, etc.)
License:        GPL-2.0-or-later
URL:            http://www.kbd-project.org/

Source0:        ftp://ftp.altlinux.org/pub/people/legion/kbd/kbd-%{version}.tar.xz
Source1:        kbd-latsun-fonts.tar.bz2
Source2:        kbd-latarcyrheb-32.tar.bz2
Source3:        xml2lst.pl
Source4:        vlock.pamd
Source5:        kbdinfo.1
Source6:        cz-map.patch
# Patch0: puts additional information into man pages
Patch0:         kbd-1.15-keycodes-man.patch
# Patch1: sparc modifications
Patch1:         kbd-1.15-sparc.patch
# Patch2: adds default unicode font to unicode_start script
Patch2:         kbd-1.15-unicode_start.patch
# Patch3: fixes decimal separator in Swiss German keyboard layout, bz 882529
Patch3:         kbd-1.15.5-sg-decimal-separator.patch
# Patch4: adds xkb and legacy keymaps subdirs to loadkyes search path, bz 1028207
Patch4:         kbd-1.15.5-loadkeys-search-path.patch
# Patch5: don't hardcode font used in unicode_start, take it from vconsole.conf,
#   bz 1101007
Patch5:         kbd-2.0.2-unicode-start-font.patch
# Patch6: fixes issues found by static analysis
Patch6:         kbd-2.4.0-covscan-fixes.patch
# Patch7: adds vlock option to issue prompt before invokation of pam stack
Patch7:         kbd-2.0.4-vlock-add-prompt-option.patch

BuildRequires:  gcc, bison, flex, gettext, pam-devel, check-devel, automake
BuildRequires:  console-setup, xkeyboard-config
BuildRequires: make
Requires:       %{name}-misc = %{version}-%{release}
Requires:       %{name}-legacy = %{version}-%{release}
# Be sure that system is after UsrMove
Conflicts:      filesystem < 3
Provides:       vlock = %{version}
Conflicts:      vlock <= 1.3
Obsoletes:      vlock < 1.3-34

%description
The %{name} package contains tools for managing a Linux
system's console's behavior, including the keyboard, the screen
fonts, the virtual terminals and font files.

%package misc
Summary:        Data for kbd package
BuildArch:      noarch
 
%description misc
The %{name}-misc package contains data for kbd package - console fonts,
keymaps etc. Please note that %{name}-misc is not helpful without kbd.

%package legacy
Summary:        Legacy data for kbd package
BuildArch:      noarch
 
%description legacy
The %{name}-legacy package contains original keymaps for kbd package.
Please note that %{name}-legacy is not helpful without kbd.

%prep
%setup -q -a 1 -a 2
cp -fp %{SOURCE3} .
cp -fp %{SOURCE6} .
%autopatch -p1
aclocal
autoconf

# 7-bit maps are obsolete; so are non-euro maps
pushd data/keymaps/i386
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
popd

# remove obsolete "gr" translation
pushd po
rm -f gr.po gr.gmo
popd

# Convert to utf-8
iconv -f iso-8859-1 -t utf-8 < "ChangeLog" > "ChangeLog_"
mv "ChangeLog_" "ChangeLog"

%build
%configure --prefix=%{_prefix} --datadir=%{kbd_datadir} --mandir=%{_mandir} --localedir=%{_datadir}/locale --enable-nls
%make_build

%install
%make_install

# ro_win.map.gz is useless
rm -f $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/i386/qwerty/ko.map.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=2015972
# xkb Arabic layout is 'ara', not 'fa', langtable tells us to use 'ara'
ln -s fa.map.gz $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/i386/qwerty/ara.map.gz

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,%{_bindir}/kbd_mode,g;s,\<setfont\>,%{_bindir}/setfont,g' \
        $RPM_BUILD_ROOT%{_bindir}/unicode_start

# install kbdinfo manpage
gzip -c %SOURCE5 > $RPM_BUILD_ROOT/%{_mandir}/man1/kbdinfo.1.gz

# Install PAM configuration for vlock
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vlock

# Move original keymaps to legacy directory
mkdir -p $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/legacy
mv $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/{amiga,atari,i386,include,mac,ppc,sun} $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/legacy

# Convert X keyboard layouts to console keymaps
mkdir -p $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb
perl xml2lst.pl < /usr/share/X11/xkb/rules/base.xml > layouts-variants.lst
while read line; do
  XKBLAYOUT=`echo "$line" | cut -d " " -f 1`
  echo "$XKBLAYOUT" >> layouts-list.lst
  XKBVARIANT=`echo "$line" | cut -d " " -f 2`
  ckbcomp -rules base "$XKBLAYOUT" "$XKBVARIANT" | gzip > $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/"$XKBLAYOUT"-"$XKBVARIANT".map.gz
done < layouts-variants.lst

# Convert X keyboard layouts (plain, no variant)
cat layouts-list.lst | sort -u >> layouts-list-uniq.lst
while read line; do
  ckbcomp -rules base "$line" | gzip > $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/"$line".map.gz
done < layouts-list-uniq.lst

# wipe converted layouts which cannot input ASCII (#1031848)
zgrep -L "U+0041" $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/* | xargs rm -f
# wipe the xkb-converted georgian layout, it is unusable, see:
# https://bugzilla.redhat.com/show_bug.cgi?id=2336875
# https://src.fedoraproject.org/rpms/kbd/pull-request/2#comment-239318
rm -f $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/ge.map.gz

# Fix converted cz layout - add compose rules, if exists
if [ -f "$RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/cz.map.gz" ]; then
  gunzip $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/cz.map.gz
  patch $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/cz.map < %{SOURCE6}
  gzip $RPM_BUILD_ROOT%{kbd_datadir}/keymaps/xkb/cz.map
fi

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc ChangeLog AUTHORS README docs/doc/font-formats/*.html docs/doc/dvorak/*
%{_bindir}/*
%{_mandir}/*/*
%config(noreplace) %{_sysconfdir}/pam.d/vlock

%files misc
%{kbd_datadir}
%exclude %{kbd_datadir}/keymaps/legacy

%files legacy
%{kbd_datadir}/keymaps/legacy

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.8.0-2
- Fix kfont_load_font(): setfont killed by SIGSEGV
  Resolves: #2370214

* Mon Jun 09 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.8.0-1
- Update to kbd-2.8.0
  Resolves: #2369419

* Mon Jan 27 2025 Adam Williamson <awilliam@redhat.com> - 2.7.1-3
- Add Georgian layout and font (from upstream PR #127)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.7.1-1
- Update to kbd-2.7.1
  Resolves: #2331264

* Tue Dec 17 2024 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.7-1
- Update to kbd-2.7
  Resolves: #2331264

* Tue Sep 10 2024 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.4-5
- Add vlock option to issue prompt before invokation of pam stack

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.4-1
- Update to kbd-2.6.4
  Resolves: #2254010

* Wed Sep 20 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.3-1
- Update to kbd-2.6.3
  Resolves: #2239620

* Thu Aug 24 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.2-1
- Update to kbd-2.6.2
  Resolves: #2232126

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.1-1
- Update to kbd-2.6.1
  Resolves: #2218174

* Tue Jun 13 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.6.0-1
- Update to kbd-2.6.0
  Resolves: #2214279

* Fri May 26 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.5.1-6
- SPDX migration

* Tue Feb 21 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.5.1-5
- Update patch adding compose rules for converted cz layout
  Resolves: #2171583

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 21 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.5.1-3
- Require kbd-legacy in main kbd package again
  Resolves: #2127513

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.5.1-1
- Update to kbd-2.5.1
  Resolves: #2097840

* Wed Jun 08 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.5.0-1
- Update to kbd-2.5.0
  Resolves: #2092957

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 21 2021 Adam Williamson <awilliam@redhat.com> - 2.4.0-8
- Symlink fa.map.gz to ara.map.gz so Arabic console layout works (#2015972)
- Drop one mapping from fa.map that causes it to fail to load

* Mon Sep 13 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-7
- Use default Finnish xkb-converted layout
  Resolves: #2001787

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-5
- Fix setfont exit code

* Tue Apr 27 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-4
- Remove one part of the static analysis fix that actually breaks the package
  Resolves: #1953782

* Thu Apr 22 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-3
- Fix issues detected by static analysis
- Fix layout->keymap conversion broken by change in xkeyboard-config
  (patch by Peter Hutterer)
  Related: #1950406

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-1
- Update to kbd-2.4.0
  Resolves: #1908123

* Thu Oct 29 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-4
- Don't require kbd-legacy in main kbd package anymore
  Resolves: #1891811

* Wed Sep 23 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-3
- Exclude test library instead of removing it to fix --nocheck builds
  Resolves: #1881515

* Fri Aug 28 2020 Adam Williamson <awilliam@redhat.com> - 2.3.0-2
- Rebuild with grep #1872913 fix to correctly drop non-ASCII layouts
  Resolves: #1872922

* Wed Jul 29 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-1
- Make changes in converted layouts conditionally
- Use make macros, patch by Tom Stellard <tstellar@redhat.com>
  (https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro)
- Update to kbd-2.3.0
  Resolves: #1855867

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 17 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.0-3
- Use upstream test suite in %%check

* Thu Mar 05 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.0-2
- Don't move binaries to /bin, shouldn't be needed after UsrMove
- Move kbd data (console fonts, keymaps, ...) to /usr
  Resolves: #1809257

* Mon Feb 10 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.0-1
- Update to kbd-2.2.0
  Resolves: #1742036

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.4-12
- Apply only tty non-breaking fixes from -10

* Tue Nov 13 2018 Adam Williamson <awilliam@redhat.com> - 2.0.4-11
- Drop fixes from -10 for now as they are breaking ttys (#1649531)

* Mon Nov 12 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.4-10
- Fix issues detected by static analysis

* Mon Aug 13 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.4-9
- Remove the link from open to openvt
  (related discussion and rationale in Debian bug tracker, bug #732796)

* Mon Jul 30 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.4-8
- Drop initscripts Require, use %%license

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.4-6
- Add BuildRequires gcc
- Escape macro in comment, remove Group tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.4-1
- Update to kbd-2.0.4
  Resolves: #1411174

* Tue Oct 11 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-4
- Fix FTBFS
  Resolves: #1381878

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 06 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-2
- Add compose rules to generated cz.map
  Resolves: #1181581

* Wed Jul 15 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-1
- Update to kbd-2.0.3
  Resolves: #1242684

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.0.2-6
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Oct 06 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.2-5
- Rename and keep Finnish xkb converted layout (patch by Marko Myllynen)
  Related: #1117891

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.2-3
- Fix unicode_start hardcodes font
  Resolves: #1101007

* Wed Jul 16 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.2-2
- Remove Finnish xkb converted layout
  Resolves: #1117891

* Tue Jul 08 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.2-1
- Update to kbd-2.0.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 17 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-6
- Add man page for kbdinfo, link open man page to openvt man page

* Wed Nov 27 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-5
- Add missing patch for loadkeys search path

* Tue Nov 26 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-4
- Add xkb and legacy keymaps subdirs to loadkyes search path, remove symlinks
  Related: #1028207
- Don't convert layouts that can't input ASCII (patch by Adam Williamson)
  Resolves: #1031848
- Fix vlock doesn't perform PAM account management or credential reinitialization
  (patch by  Dmitry V. Levin)
  Resolves: #913311

* Wed Nov 06 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-3
- Add PAM config for vlock
  Resolves: #913309

* Mon Nov 04 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-2
- Fix URL
- Remove source files already included in upstream tarball

* Mon Nov 04 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-1
- Update to kbd-2.0.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-8
- Add vlock to obsoletes

* Wed May 22 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-7
- Convert also plain layouts (no variant), point relevant symlinks to them

* Tue May 21 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-6
- Original keymaps moved to legacy dir, created symlinks to xkb keymaps

* Thu Feb 21 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-5
- Fix decimal separator in Swiss German keyboard layout
  Resolves: #882529

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-3
- Include xkb layouts from xkeyboard-config converted to console keymaps
- Add version to vlock provides
  Resolves: #902564

* Mon Jan 21 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-2
- Fix loadkeys regression
  Resolves: #902259

* Mon Jan 14 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.5-1
- Update to kbd-1.15.5 (removed kbd-1.15-resizecon-x86_64.patch,
  kbd-1.15-defkeymap.patch, kbd-1.15.3-fix-es-translation.patch,
  kbd-1.15.3-loadkeys-d.patch)

* Thu Sep 13 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.3-8
- Fix link to upstream tarball

* Tue Aug 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.3-7
- Fix issues found by fedora-review utility in the spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.3-4
- Ship double scaled latarcyrheb console font for high resolution screens
  (created by Tom Horsley)
  Resolves: #617768

* Mon Oct 24 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.3-3
* Fix loadkeys -d option (patch by Jaroslav Skarvada)
  Resolves: #744567

* Tue Aug 23 2011 Vitezlsav Crhonek <vcrhonek@redhat.com> - 1.15.3-2
- Add missing dumpkeys option to man page
  Resolves: #732121

* Mon Aug 22 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.3-1
- Update to kbd-1.15.3

* Thu Apr 21 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.2-3
- Add French Canadian Dvorak keymap
  Resolves: #680989

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15.2-1
- Update to kbd-1.15.2 (removed kbd-1.15-quiet_doc.patch and romanian keymaps, both are
  part of the upstream tarball now)

* Thu Jun 24 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-11
- Ship /lib/kbd in separate subpackage

* Mon Jun 14 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-10
- Fix name referring to default keymap

* Wed Aug 26 2009 Karsten Hopp <karsten@redhat.com> 1.15-9
- drop excludearch s390x, we need this package to be able to build other packages on s390x

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-7
- Add loadkeys 'q' option to loadkeys manpage and --help
  Resolves: #487538

* Mon Mar  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-6
- Remove static loadkeys binary (it's not needed anymore)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-4
- Merge review (drop Provides/Obsoletes, change Prereq to Requires,
  add URL, convert ChangeLog to utf-8, replace locale destination
  with macro, add COPYING and add dvorak documentation)
  Resolves: #225958

* Thu Jan 29 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-3
- Rename conflicting keymaps to have unique names
  Resolves: #481674

* Mon Jan 12 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-2
- Move loadkeys to /bin

* Thu Jan  8 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-1
- Update to kbd-1.15

* Mon Sep  8 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-32
- Rediff all patches to work with patch --fuzz=0
- Add static loadkeys
  Related: #451672

* Tue Feb 26 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-31
- Fix trq.map
  Resolves: #216710

* Fri Feb 22 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-30
- Rebuild fo GCC 4.3

* Tue Nov 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-29
- Stop kbdrate using consolehelper
  Resolves: #393231

* Thu Nov 15 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-28
- Fix ro.map.gz, add ro_std.map.gz, drop ro_win.map.gz,
  add Lat2-Terminus16.psf console font (many thanks to Alexandru Szasz
  <alexxed@gmail.com>)
  Resolves: #253892

* Wed Oct 17 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-27
- Add resizecons (with man page) for x86_64
  Resolves: #333651

* Mon Oct 15 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-26
- Fix ro.map to generate right unicode for s, S, t, T with comma
- Fix LatArCyrHeb-16 unicode mapping table to show comma-version
  of s, S, t, T and cedilla-version of s, S, t, T as the same glyph
  (because there is no font in kbd for comma-version)
  Resolves: #329071

* Tue Sep 18 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-25
- Add new romanian keymap
  Resolves: #253892

* Mon Aug 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-24
- Fix license
- Symlink sr-cy layout to sr-latin
  Resolves: #253957

* Tue Jul  3 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-23
- Rebuild

* Tue Jul  3 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-22
- Fix sun12x22 font missing unicode mapping table
  Resolves: #244628

* Tue Jan  9 2007 Miloslav Trmac <mitr@redhat.com> - 1.12-21
- Add a "ko" (Korean) keyboard layout, equivalent to the "us" layout
  Resolves: #220151

* Thu Dec  7 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-20
- Document that setkeycodes doesn't affect USB keyboards and that the kernel
  doesn't provide the raw scan codes by default
  Resolves: #211803

* Tue Oct 31 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-19
- Ship "el" translation instead of the obsolete "gr" translation
  Resolves: #210749
- Fix %% quoting in %%changelog

* Fri Sep 29 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-18
- Add a missing tilde to U+00E3 in latarcyrheb-sun16.psfu (#204470)

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 1.12-17
- Obsoletes/Provides open
- Create a symlink from open to openvt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.12-16.1
- rebuild

* Sun Jul  9 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-16
- Don't include <asm/kbdio.h> on SPARC (#198040, patch by Dennis Gilmore
  <dennis@ausil.us>)

* Mon May 29 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-15
- Fix missing BuildRequires (#193406)

* Mon Mar 27 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-14
- Don't install resizecons.8 on non-x86 (#186877, patch by Keiichi Mori
  <kmori@redhat.com>)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.12-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.12-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-13
- Fix build with new coreutils
- Hardcode paths in unicode_start to avoid a few file lookups (#178329)
- Drop unnecessary Prereq: sed mktemp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-12
- Don't reload the keymap in unicode_start (#172425)

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-11
- Don't ship character set lists (they are already in glibc-common) and an
  obsolete copy of kbd.FAQ

* Fri May 20 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-10
- Don't attempt to open directories as source files (#141634, original patch by
  Paul Nasrat)

* Tue May 17 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-9
- Fix another violation of C aliasing rules (#157720, patch by Jan Kratochvil)

* Sat Mar 12 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-8
- Fix violation of C aliasing rules (#150440)

* Sun Mar  6 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-7
- Don't run ldconfig
- Don't strip executables

* Fri Mar  4 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-6
- Rebuild with gcc4

* Sun Feb 20 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-5
- Put "Meta_acute" back in German keymaps, just ignore it in (loadkeys -u)
  (patch by Jochen Schmitt)
- Don't ship patch backup files, simpler way

* Sat Feb 19 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-4
- Don't ship a patch backup file
- Mention in setfont.8 that 512-glyph fonts reduce the number of available
  colors (#140935, patch by Dmitry Butskoj)
- Remove "Meta_acute" from German keymaps (#143124)
- Make the %%triggerun script condition more precise, ignore failure of the
  script

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Adrian Havill <havill@redhat.com>
- update to 1.12

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 14 2004 Bill Nottingham <notting@redhat.com> 1.08-12
- remove speakup patch at request of author

* Wed Jan 14 2004 Bill Nottingham <notting@redhat.com> 1.08-12
- remove speakup patch at request of author

* Fri Oct 10 2003 Bill Nottingham <notting@redhat.com> 1.08-11
- remove keytable init script (#106783)

* Tue Aug 12 2003 Adrian Havill <havill@rtedhat.com> 1.08-10.1
- bump for RHEL

* Tue Aug 12 2003 Adrian Havill <havill@rtedhat.com> 1.08-10
- apply the rukbd patch (#78218)

* Thu Jul 31 2003 Adrian Havill <havill@redhat.com> 1.08-9
- don't print "plus before..." warnings about non-supported capslock
  in unimode <Andries.Brouwer@cwi.nl> (#81855)

* Wed Jul 30 2003 Adrian Havill <havill@redhat.com> 1.08-8
- replaced Russian keyboard map with working UTF-8 equivalent (#79338)

* Thu Jul 24 2003 Adrian Havill <havill@redhat.com> 1.08-7
- make euro/latin-9 the default instead of latin-1 and 7-bit (#97013)
- fix swedish keymap; se, not sv (#88791)
- add fr-latin0 legacy alias of fr-latin-9 (#88324)
- add ".map" ext to filename param of init script (#90562)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 06 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- build new rpm

* Fri Feb 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- ExcludeArch mainframe

* Thu Jan 30 2003 Bill Nottingham <notting@redhat.com> 1.08-4
- remove condrestart from initscript

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec  6 2002 Nalin Dahyabhai <nalin@redhat.com> 1.08-2
- only output terminal unicode init sequence if both stdout and stderr are
  connected to terminals, so that it doesn't show up when script outputs
  get piped to files

* Fri Nov 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.08-1
- update to 1.08
- drop updates which went mainline

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.06-27
- add detached signature
- remove directory names from PAM configuration so that the same config file
  can be used for any arch on multilib systems

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 1.06-26
- don't munge /etc/sysconfig/i18n

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 1.06-25
- don't run setsysfont in upgrade trigger on console-tools

* Thu Aug 29 2002 Jakub Jelinek <jakub@redhat.com> 1.06-24
- use cyr-sun16 cyrillic chars in latarcyrheb-sun16 font
  instead of old LatArCyrHeb-16 chars
- add Euro character to latarcyrheb-sun16
- use latarcyrheb-sun16 by default in unicode_start script

* Tue Aug 27 2002 Jakub Jelinek <jakub@redhat.com> 1.06-23
- add back lat[02]-sun16 fonts plus latarcyrheb-sun16 font

* Thu Aug 22 2002 Karsten Hopp <karsten@redhat.de>
- needs to conflict with older util-linux packages
  (kbdrate moved between packages)

* Tue Aug 13 2002 Bill Nottingham <notting@redhat.com> 1.06-21
- remove Evil Hack in favor of slightly-less-evil-hack in initscripts

* Tue Jul  9 2002 Bill Nottingham <notting@redhat.com> 1.06-20
- fix speakup keymap names

* Tue Jul 09 2002 Phil Knirsch <pknirsch@redhat.com> 1.06-19
- Evil hack to make setfont work correctly on all consoles (#68018)

* Thu Jun 27 2002 Bill Nottingham <notting@redhat.com> 1.06-18
- move unicode_stop to /bin too
- fix path to loadkeys in keytable.init
- add in speakup keymaps

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.06-16
- fix incorrect path in console.apps configuration file

* Thu May 30 2002 Bill Nottingham <notting@redhat.com> 1.06-14
- move some more stuff to /bin (unicode_start and dependencies)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-12
- Rebuild in new environment

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-11
- Oops, actually list the pam files in %%files

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-10
- Add and consolehelper'ify kbdrate

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-9
- Re-remove kbdrate

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-7
- Fix build in current environment
- Get rid of kbdrate, it's in util-linux these days

* Wed Jul 18 2001 Matt Wilson <msw@redhat.com>
- added a patch (Patch4) that allows --tty= in setfont
- modified patch not to break translations

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-4
- Add cyrillic patches from leon@geon.donetsk.ua (#47144)

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-3
- Fix "Alt+AltGr=Compose" in qwertz-keyboards

* Mon Jun 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-2
- Fix "make install" and init script (#45327)

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 1.0.6
- use %%{_tmppath}
- use find_lang
- support new gettext
- remove some patch files, which are included in 1.0.6
- fix to use RPM_OPT_FLAGS

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.05-3
- Fix up resizecons

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.05-2
- Build everything, obsoletes console-tools
- s/Copyright:/License:/
- License is GPL, not just distributable
- Add our compose mappings from old console-tools
- Add triggerpostun -- console-tools magic to get sane fonts and mappings

* Tue Apr 17 2001 Erik Troan <ewt@redhat.com>
- initial packaging for kbdrate
