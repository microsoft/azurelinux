# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# INFO: Package contains data-only, no binaries, so no debuginfo is needed
%global debug_package %{nil}

# Installed destination is now xkeyboard-config-2, but upstream package
# name is the same
%global pkgconfig_name xkeyboard-config-2

#global gitdate 20110415
#global gitversion 19a0026b5

Summary:    X Keyboard Extension configuration data
Name:       xkeyboard-config
Version:    2.46
Release: 2%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License:    HPND AND HPND-sell-variant AND X11 AND X11-distribute-modifications-variant AND MIT AND MIT-open-group AND xkeyboard-config-Zinoviev
URL:        http://www.freedesktop.org/wiki/Software/XKeyboardConfig

%if 0%{?gitdate}
Source0:    %{name}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    http://xorg.freedesktop.org/archive/individual/data/%{name}/%{name}-%{version}.tar.xz
%endif

BuildArch:  noarch

BuildRequires:  gettext gettext-devel
BuildRequires:  meson
BuildRequires:  libxslt
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(x11) >= 1.4.3
BuildRequires:  pkgconfig(xorg-macros) >= 1.12
BuildRequires:  pkgconfig(xproto) >= 7.0.20
BuildRequires:  xkbcomp
BuildRequires:  git-core

%description
This package contains configuration data used by the X Keyboard Extension (XKB),
which allows selection of keyboard layouts when using a graphical interface.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
Development files for %{name}.

%prep
%autosetup -S git

%build
%meson -Dcompat-rules=true -Dxorg-rules-symlinks=true
%meson_build

%install
%meson_install

# Replace with relative symlink
rm $RPM_BUILD_ROOT%{_datadir}/X11/xkb
ln -srf $RPM_BUILD_ROOT%{_datadir}/%{pkgconfig_name} $RPM_BUILD_ROOT%{_datadir}/X11/xkb

%find_lang %{pkgconfig_name}
%find_lang %{name}

# Note: 2.45 changed the install location from the decades-old /usr/share/X11/xkb
# to a package-specific /usr/share/xkeyboard-config-2. Upstream installs a symlink
# for /usr/share/X11/xkb since those two dirctories are guaranteed to be the same.
#
# The "official" script [1] is buggy if an .rpmmoved directory already exists so
# this is an approximation taken from OpenSuSE [2]
# [1] https://fedoraproject.org/wiki/Packaging:Directory_Replacement#Replacing_a_symlink_with_a_directory_or_a_directory_with_any_type_of_file
# [2] https://build.opensuse.org/request/show/1294803
%pretrans -p <lua>
-- Define the path to directory being replaced below.
-- DO NOT add a trailing slash at the end.
local path = "%{_datadir}/X11/xkb"
local st = posix.stat(path)

if st and st.type == "directory" then
  local target = path .. ".rpmmoved"
  local suffix = 1

  while posix.stat(target) do
    suffix = suffix + 1
    target = path .. ".rpmmoved" .. suffix
  end

  os.rename(path, target)
end

%files -f %{pkgconfig_name}.lang -f %{name}.lang
%doc AUTHORS README.md COPYING docs/README.* docs/HOWTO.*
%{_mandir}/man7/%{name}.*
%{_mandir}/man7/%{pkgconfig_name}.*
%{_datadir}/X11/xkb
%{_datadir}/%{pkgconfig_name}/
%ghost %attr(0755, root, root) %dir %{_datadir}/X11/xkb.rpmmoved

%files devel
%{_datadir}/pkgconfig/%{pkgconfig_name}.pc
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Thu Oct 09 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.46-1
- xkeyboard-config 2.46

* Thu Aug 07 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.45-1
- xkeyboard-config 2.45
  xkeyboard-config changed from /usr/share/X11/xkb to /usr/share/xkeyboard-config-2/,
  with the same contents and the old location symlinked to the new one.
  Add a pretrans script to move the old location to the new one to stick with the
  upstream packaging approach.

* Thu Aug 07 2025 Peter Hutterer <peter.hutterer@redhat.com> - 2.44-3
- Remove packaging hacks, with meson now have a clean build

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 10 2025 Peter Hutterer <peter.hutterer@redhat.com> 2.44-1
- xkeyboard-config 2.44

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 03 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.43-1git}
- xkeyboard-config 2.43

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Peter Hutterer <peter.hutterer@redhat.com> 2.42-1
- xkeyboard-config 2.42

* Wed Feb 07 2024 Peter Hutterer <peter.hutterer@redhat.com> - 2.41-1
- xkeyboard-config 2.41

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.40-2
- SPDX migration

* Fri Oct 13 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.40-1
- xkeyboard-config 2.40

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 12 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.39-1
- xkeyboard-config 2.39

* Tue Feb 07 2023 Peter Hutterer <peter.hutterer@redhat.com> - 2.38-1
- xkeyboard-config 2.38

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 26 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 2.36-3
- Backport upstream MR to allow Apple MacBook keyboards to type \ properly

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.36-1
- xkeyboard-config 2.36

* Wed Feb 09 2022 Peter Hutterer <peter.hutterer@redhat.com> - 2.35.1-1
- xkeyboard-config 2.35.1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 07 2021 Peter Hutterer <peter.hutterer@redhat.com> - 2.34-1
- xkeyboard-config 2.34

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Peter Hutterer <peter.hutterer@redhat.com> 2.33-3
- xkeyboard-config 2.33

* Tue Apr 20 2021 Peter Hutterer <peter.hutterer@redhat.com> 2.32-3
- Restore the xorg ruleset, console-setup and possibly others are still
  using those (#1951459)

* Fri Apr 09 2021 Peter Hutterer <peter.hutterer@redhat.com> 2.32-2
- Allow for a "custom" layout

* Tue Feb 16 2021 Peter Hutterer <peter.hutterer@redhat.com> 2.32-1
- xkeyboard-config 2.32
- build with meson now
- drop the xorg ruleset, no longer in use. Everything is hardcoded to evdev
  these days.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 01 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.31-3
- Add make to BuildRequires

* Wed Nov 04 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.31-2
- Fix BuildRequires for git, we only need git-core

* Wed Oct 07 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.31-1
- xkeyboard-config 2.31

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 19 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.30-2
- Fix a syntax error in the indian symbols file

* Wed Jun 03 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.30-1
- xkeyboard-config 2.30

* Fri Jan 31 2020 Peter Hutterer <peter.hutterer@redhat.com> 2.29-1
- xkeyboard-config 2.29

* Fri Oct 25 2019 Peter Hutterer <peter.hutterer@redhat.com> 2.28-1
- xkeyboard-config 2.28

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Peter Hutterer <peter.hutterer@redhat.com> 2.27-1
- xkeyboard-config 2.27
- drop intltool, no longer needed, see upstream commit e8026f673e

* Mon May 27 2019 Peter Hutterer <peter.hutterer@redhat.com> 2.26-2
- xkeyboard-config 2.26, with sources this time

* Mon May 27 2019 Peter Hutterer <peter.hutterer@redhat.com> 2.26-1
- xkeyboard-config 2.26

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-3
- Remove high-keycode removal patches, xkbcomp 1.4.2 has been in stable for
  long enough (related #1587998)

* Thu Jun 07 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-2
- Revert two high keycode mappings, xkbcomp fails to parse those.
  (#1587998)

* Tue Jun 05 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.24-1
- xkeyboard-config 2.24

* Wed Feb 07 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.23.1-1
- Fix typo in polish keyboard layout
- xkeyboard-config 2.23.1
- use autosetup

* Wed Jan 31 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.23-1
- xkeyboard-config 2.23

* Fri Oct 06 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.22-1
- xkeyboard-config 2.22

* Tue Sep 05 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.21-3
- Fix typo in tel-salara (#1469407)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.21-1
- xkeyboard-config 2.21

* Fri May 12 2017 Hans de Goede <hdegoede@redhat.com> - 2.20-4
- Add evdev mappings for KEY_SOUND, KEY_UWB, KEY_WWAN and KEY_RFKILL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.20-2
- Add BuildRequires: git

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.20-1
- xkeyboard-config 2.20

* Mon Dec 05 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.19-2
- Bump to keep F25 upgrade path happy, no changes.

* Tue Oct 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.19-1
- xkeyboard-config 2.19

* Fri Jun 03 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.18-1
- xkeyboard-config 2.18

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Peter Hutterer <peter.hutterer@redhat.com> 2.17-1
- xkeyboard-config 2.17

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Tue Dec 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.16-2
- Add br(thinkpad) to the xml file (#1292881)

* Thu Oct 15 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.16-1
- xkeyboard-config 2.16

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.15-1
- xkeyboard-config 2.15

* Thu Jan 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 2.14-1
- xkeyboard-config 2.14

* Tue Nov 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.13-3
- Add U+05BA (point holam haser for vav) on il(biblical) (#1132511)

* Thu Oct 23 2014 Simone Caronni <negativo17@gmail.com> - 2.13-2
- Clean up SPEC file, fix rpmlint warnings.
- Remove non-valid configure option.

* Wed Oct 01 2014 Adam Jackson <ajax@redhat.com> 2.13-1
- xkeyboard-config 2.13

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.12-1
- xkeyboard-config 2.12

* Thu Jan 30 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.11-1
- xkeyboard-config 2.11

* Mon Oct 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.10.1-1
- xkeyboard-config 2.20.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-3
- Fix changelog - percent sign needs to be escaped

* Wed Jul 17 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-2
- Fix up three bogus changelog dates

* Thu May 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.9-1
- xkeyboard-config 2.9

* Wed May 15 2013 Daniel Drake <dsd@laptop.org> 2.8-3
- Add upstream patches for OLPC mechanical keyboard support

* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-2
- Fix a bunch of language codes (#952510, #952519)

* Thu Jan 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.8-1
- xkeyboard-config 2.8

* Wed Jan 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 2.7-4
- Fix Mali layout previously mapped to in(mal) (#647433)

* Wed Nov 14 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-3
- Rebuild with fixed xkbcomp, re-create the right directory listing (not
  that anyone actually uses it)

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 2.7-2
- Fix {?dist} tag

* Thu Sep 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.7-1
- xkeyboard-config 2.7

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-2
- Revert broken fix for is keyboard (#826220)

* Thu May 31 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.6-1
- xkeyboard-config 2.6
- change source URL, 2.6 is in a different directory
- force autoreconf, update to use intltoolize as autopoint

* Wed May 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.5.1-2
- Add upstream patch to fix OLPC azerty keyboard

* Thu Feb 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5.1-1
- xkeyboard-config 2.5.1

* Mon Jan 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.5-1
- xkeyboard-config 2.5

* Thu Jan 19 2012 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-4
- Move Ungrab and ClearGrab from the default layout to option
  grab:break_actions (#783044)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-2
- Change Serbian layouts to mark the cyrillic ones (#769751)

* Wed Oct 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.4.1-1
- xkeyboard-config 2.4.1
- change source URL from ftp.x.org to http://xorg.freedesktop.org, ftp takes
  too long to update

* Tue Jun 14 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-2
- Add 0001-Use-XSL-to-generate-man-page-from-the-rules-XML.patch, ship
  man-page
- Fix up broken git repo initialization when building from a tarball

* Thu Jun 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.3-1
- xkeyboard-config 2.3

* Fri Apr 15 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2.20110415git19a0026b5
- Snapshot from git to fix French Canadian layouts (#694472)

* Wed Apr 06 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- xkeyboard-config 2.2.1, 2.2 had a broken configure check
- Add new BR and don't disable build/runtime deps checks

* Mon Apr 04 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.2-1
- xkeyboard-config 2.2
- reinstate the git bits removed in previous commit

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.99-2
- Update to 2.1.99 release

* Fri Mar 11 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20110311-git9333b2f3
- add bits required to build from git
- update to today's git snapshot

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 2.1-1
- xkeyboard-config 2.1
