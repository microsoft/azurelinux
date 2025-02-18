%global require_ibus_version 1.3.99
%global require_libhangul_version 0.1.0

Name:       ibus-hangul
Version:    1.5.5
Release:    6%{?dist}
Summary:    The Hangul engine for IBus input platform
License:    GPL-2.0-or-later
URL:        https://github.com/libhangul/ibus-hangul
Source0:    https://github.com/libhangul/ibus-hangul/releases/download/%{version}/%{name}-%{version}.tar.xz

# not upstreamed patches
Patch1:     ibus-hangul-setup-abspath.patch

BuildRequires:  gettext-devel, automake, libtool
BuildRequires:  libhangul-devel >= %{require_libhangul_version}
BuildRequires:  pkgconfig
BuildRequires:  ibus-devel >= %{require_ibus_version}
BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  gtk3-devel
BuildRequires:  make

Requires:   ibus >= %{require_ibus_version}
Requires:   libhangul >= %{require_libhangul_version}
Requires:   python3-gobject
Requires:   python3

%description
The Hangul engine for IBus platform. It provides Korean input method from
libhangul.

%package tests
Summary:        Tests for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -p1

%build
./autogen.sh
%configure \
           --disable-static \
           --with-python=python3 \
           %{?_with_hotkeys} \
           --enable-installed-tests \
           %{nil}

make %{?_smp_mflags}

%install
make DESTDIR=${RPM_BUILD_ROOT} install INSTALL="install -p"

%py_byte_compile %{python3} $RPM_BUILD_ROOT%{_datadir}/ibus-hangul/setup

rm -f ${RPM_BUILD_ROOT}%{_bindir}/ibus-setup-hangul
sed -i 's!^Exec=ibus-setup-hangul!Exec=%{_libexecdir}/ibus-setup-hangul!' ${RPM_BUILD_ROOT}%{_datadir}/applications/ibus-setup-hangul.desktop

desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/ibus-setup-hangul.desktop

%find_lang %{name}

%check
make check \
    DISABLE_GUI_TESTS="ibus-hangul" \
    VERBOSE=1

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libexecdir}/ibus-engine-hangul
%{_libexecdir}/ibus-setup-hangul
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/ibus-hangul
%{_datadir}/ibus/component/*
%{_datadir}/applications/ibus-setup-hangul.desktop
%{_datadir}/icons/hicolor/*/apps/*

%files tests
%dir %{_libexecdir}/installed-tests
%{_libexecdir}/installed-tests/ibus-hangul
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/ibus-hangul

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May  9 2023 Peng Wu <pwu@redhat.com> - 1.5.5-2
- Migrate to SPDX license

* Thu May  4 2023 Peng Wu <pwu@redhat.com> - 1.5.5-1
- Update to 1.5.5

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Peng Wu <pwu@redhat.com> - 1.5.4-14
- Update ibus-hangul-gtk4-sync.patch

* Tue Aug 23 2022 Peng Wu <pwu@redhat.com> - 1.5.4-13
- Rebuild the package

* Fri Aug 19 2022 Peng Wu <pwu@redhat.com> - 1.5.4-12
- Fix forward key event issue with ibus-gtk4
- Add ibus-hangul-gtk4-sync.patch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 21 2022 Tomas Popela <tpopela@redhat.com> - 1.5.4-10
- Drop BR on gnome-common as the project was moved away from intltool
- Drop duplicated libtool BR

* Fri Jun 10 2022 Peng Wu <pwu@redhat.com> - 1.5.4-9
- Drop BuildRequires: intltool

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.4-6
- Delete ibus write-cache in scriptlet

* Wed Apr 21 2021 Takao Fujiwara <tfujiwar@redhat.com> - 1.5.4-5
- Resolves: #1948197 Change post to posttrans

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Peng Wu <pwu@redhat.com> - 1.5.4-3
- Add tests sub package

* Wed Sep  2 2020 Peng Wu <pwu@redhat.com> - 1.5.4-2
- Clean up the spec file

* Mon Aug 24 2020 Peng Wu <pwu@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Peng Wu <pwu@redhat.com> - 1.5.3-3
- Switch to use py_byte_compile rpm macro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Peng Wu <pwu@redhat.com> - 1.5.3-1
- Update to 1.5.3

* Tue Aug  6 2019 Peng Wu <pwu@redhat.com> - 1.5.1-7
- Change default mode to latin

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 19 2019 Peng Wu <pwu@redhat.com> - 1.5.1-5
- Fixes double commit issue with web browser
- Add patch ibus-hangul-fixes-reset.patch

* Fri Mar 22 2019 Peng Wu <pwu@redhat.com> - 1.5.1-4
- Change default mode to hangul

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.5.1-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Peng Wu <pwu@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Peng Wu <pwu@redhat.com> - 1.5.0-13
- Resolves: RHBZ#1296121

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.0-11
- Remove obsolete scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-7
- Rebuild for Python 3.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul  2 2015 Daiki Ueno <dueno@redhat.com> - 1.5.0-5
- require python3-gobject instead of pygobject3, to avoid python2
  dependency.  Suggested by Miro Hrončok.

* Thu Jul 02 2015 Petr Viktorin <pviktori@redhat.com> - 1.5.0-4
- Use autogen in RPM build
- Use Python 3 for setup scripts

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.5.0-2
- Register as an AppStream component.

* Wed Nov 26 2014 Daiki Ueno <dueno@redhat.com> - 1.5.0-1
- Update version to 1.5.0
- Drop upstreamed patches: dconf-prefix.patch and setup-ui.patch

* Tue Sep 16 2014 Daiki Ueno <dueno@redhat.com> - 1.4.2-10
- Add ibus-hangul-setup-ui.patch
- Fix bug 1115411 - [abrt] ibus-hangul: main.py:43:__init__:Error:
  gtk-builder-error-quark: Invalid property: GtkNotebook.tab_hborder
  on line 21 (11)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-7
- Invoke ibus-setup-hangul with the absolute path.
- Fix bug 1012732 - Click ibus hangul setup on gnome-shell top bar's
  ibus -> No Response

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-5
- Remove ibus-setup-hangul symlink in %%{_bindir}.
- Fix bogus changelog date.

* Tue Apr  2 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-4
- Fix the last update which didn't apply the patch.

* Tue Apr  2 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-3
- Remove have_bridge_hotkey and need_pygobject3 macros which does no
  longer make sense after F17
- Add ibus-hangul-dconf-prefix.patch
- Fix bug 909509 - Hangul Keybaord doesn't be changed in IBusHangul Setup

* Wed Mar 27 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-2
- Pull the latest config.guess and config.sub for ARM64 port

* Tue Jan 29 2013 Daiki Ueno <dueno@redhat.com> - 1.4.2-1
- Update version to 1.4.2.
- Remove ibus-hangul-setup-gi.patch

* Wed Nov 21 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-9
- Fix a typo (R: -> BR: python2-devel)

* Wed Nov 21 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-8
- Cleanup the spec file

* Thu Nov 15 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-7
- Re-add ibus-hangul-HEAD.patch based on recent upstream change
- Apply ibus-hangul-add-hangul-hotkey.patch only for F-15 and F-16

* Wed Oct 31 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-6
- Add ibus-hangul-engine-name.patch
- Update ibus-hangul-setup-gi.patch
- Fix bug 870318 - Change of “Automatic reordering” setup option
  cannot be applied in ibus-hangul setup (thanks Mike FABIAN for the patch)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  8 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-4
- Fix ibus-hangul-setup-gi.patch
- Remove previously applied ibus-hangul-setup-race-condition.patch
- Fix bug 828597 - [abrt] ibus-hangul-1.4.1-2.fc16:
  main.py:184:on_value_changed:TypeError: 'NoneType' object is not
  iterable

* Wed Jun  6 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-3
- Fix ibus-setup-hangul race condition
- Fix bug 828597 - [abrt] ibus-hangul-1.4.1-2.fc16:
  main.py:184:on_value_changed:TypeError: 'NoneType' object is not
  iterable

* Tue May  1 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-2
- Add pygobject3 to dependencies on F-16.
- Fix bug 816890 - [abrt] ibus-hangul-1.4.0-5.fc16:
  main.py:23:<module>:ImportError: No module named gi.repository

* Tue Apr 17 2012 Daiki Ueno <dueno@redhat.com> - 1.4.1-1
- Update version to 1.4.1.
- Check RHEL version as well as Fedora version.

* Tue Mar  6 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-5
- Revive <hotkey> in hangul.xml.
- Remove unnecessary BR: ibus.
- Port ibus-setup-hangul to use gobject-introspection.

* Mon Mar  5 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-4
- Package the latest git master.
- Fix bug 799776 - [abrt] ibus-hangul-1.4.0-3.fc17
- Remove upstreamed patches: ibus-hangul-xx-icon-symbol.patch,
  ibus-hangul-no-ibus-daemon.patch, and
  ibus-hangul-use-system-icon.patch

* Fri Feb 10 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-3
- Add ibus-hangul-use-system-icon.patch
- Fix bug 789230 - ibus hangul Icon missing in gnome-shell (fedora 17)

* Tue Jan 31 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-2
- Add ibus-hangul-no-ibus-daemon.patch.
- Fix bug 784377 - [abrt] ibus-hangul-1.4.0-1.fc16

* Thu Jan 12 2012 Daiki Ueno <dueno@redhat.com> - 1.4.0-1
- Update version to 1.4.0.
- Remove ibus-hangul-ibus-1.4.patch.
- Drop %%defattr(-,root,root,-) from %%files.
- Pass -p to install to preserve file timestamps.
- Install ibus-setup-hangul.desktop properly.

* Thu Nov 24 2011 Daiki Ueno <dueno@redhat.com> - 1.3.2-1
- Update version to 1.3.2.

* Mon Oct 24 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-8
- Rebuild with the latest libhangul.

* Fri Aug 19 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-7
- Enable --with-hotkeys for F16 or later.
- Fix bug 731913 - No Hangul Key in keyboard Shortcuts

* Mon Jul 18 2011 Daiki Ueno <ueno@unixuser.org> - 1.3.1-6
- Fix entity reference for icon symbol.
- Fix bug 722566 - Cannot select Hangul Input Method on Ibus Preferences

* Thu Jul  7 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-5
- Don't specify --with-hotkeys.

* Mon Jul  4 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-4
- Added ibus-hangul-xx-icon-symbol.patch to enable the engine symbol & hotkeys.

* Wed May 11 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-3
- Update ibus-1.4 patch.
- Move the ibus version check into the patch from this spec.
- Fix bug 695971 - Hangul Keybaord Layout works to only dubeolsik

* Mon Apr  4 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-2
- Apply ibus-1.4 patch conditionally for SRPM compatibility.
- Drop buildroot, %%clean and cleaning of buildroot in %%install

* Mon Feb 28 2011 Daiki Ueno <dueno@redhat.com> - 1.3.1-1
- Update version to 1.3.1.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.20100329-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-4
- Add ibus-hangul-gvariant.patch for ibus-1.3.99

* Mon Aug 23 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-3
- Update ibus-hangul-HEAD.patch

* Tue Aug  3 2010 Daiki Ueno <dueno@redhat.com> - 1.3.0.20100329-1
- Update version to 1.3.0.20100329
- Add ibus-hangul-HEAD.patch to synch it with the git master

* Thu Feb 04 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20100102-1
- Update version to 1.2.0.20100102
- Add ibus-hangul-phuang.patch for ibus-1.2.99

* Fri Dec 11 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20091031-1
- Update version to 1.2.0.20091031.
- Drop ibus-hangul-1.1.0.20090328-right-ctrl-hanja.patch and
  ibus-hangul-1.1.0.20090328-hanja-arrow-keys.patch temporarily, because
  patches conflict with 1.2.0.20091031, and the key configure will available
  in next release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090617-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090330-1
- Update version to 1.2.0.20090617.

* Sun Apr 12 2009 Warren Togami <wtogami@redhat.com> - 1.1.0.20090330-2
- Bug 493706: ibus-hangul Hanja arrow keys are wrong
- Bug 493509: ibus-hangul missing right Ctrl for Hanja button
  These fixes are not ideal, but they make it usable for Fedora 11.
  These must become configurable in a future version.

* Mon Mar 30 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090330-1
- Update version to 1.1.0.20090330.
- Fix bug 486056 - missing options for 2bul, 3bul and other Korean layouts
- Fix bug 487269 - missing Hanja Conversion

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0.20090211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090211-1
- Update version to 1.1.0.20090211.

* Thu Feb 05 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.1.0.20090205-1
- Update version to 1.1.0.20090205.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-2
- Rebuild for Python 2.6

* Thu Oct 23 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20081023-1
- Update to 0.1.1.20081023.

* Tue Sep 09 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Fri Aug 08 2008 Peng Huang <shawn.p.huang@gmail.com> - 0.1.1.20080823-1
- The first version.
