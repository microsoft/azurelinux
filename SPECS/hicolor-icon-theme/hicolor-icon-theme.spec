Summary:        Basic requirement for icon themes
Name:           hicolor-icon-theme
Version:        0.17
Release:        10%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.freedesktop.org/wiki/Software/icon-theme/
Source0:        https://icon-theme.freedesktop.org/releases/%{name}-%{version}.tar.xz
BuildArch:      noarch

%description
Contains the basic directories and files needed for icon theme support.

%prep
%setup -q

# for some reason this file is executable in the tarball
chmod 0644 COPYING

%build
%configure

%install
%make_install

touch %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%transfiletriggerin -- %{_datadir}/icons/hicolor
gtk-update-icon-cache --force %{_datadir}/icons/hicolor &>/dev/null || :

%transfiletriggerpostun -- %{_datadir}/icons/hicolor
gtk-update-icon-cache --force %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license COPYING
%doc README
%dir %{_datadir}/icons/hicolor
%{_datadir}/icons/hicolor/16x16/
%{_datadir}/icons/hicolor/22x22/
%{_datadir}/icons/hicolor/24x24/
%{_datadir}/icons/hicolor/32x32/
%{_datadir}/icons/hicolor/36x36/
%{_datadir}/icons/hicolor/48x48/
%{_datadir}/icons/hicolor/64x64/
%{_datadir}/icons/hicolor/72x72/
%{_datadir}/icons/hicolor/96x96/
%{_datadir}/icons/hicolor/128x128/
%{_datadir}/icons/hicolor/192x192/
%{_datadir}/icons/hicolor/256x256/
%{_datadir}/icons/hicolor/512x512/
%{_datadir}/icons/hicolor/scalable/
%{_datadir}/icons/hicolor/symbolic/
%{_datadir}/icons/hicolor/index.theme
%ghost %{_datadir}/icons/hicolor/icon-theme.cache

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.17-10
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.17-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0.17-6
- Remove obsolete requirements for %%post/%%postun scriptlets

* Fri Feb 08 2019 Kalev Lember <klember@redhat.com> - 0.17-5
- Fix /usr/share/icons/hicolor directory ownership

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 Kalev Lember <klember@redhat.com> - 0.17-1
- Update to 0.17

* Tue Aug 22 2017 Kalev Lember <klember@redhat.com> - 0.16-1
- Update to 0.16

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Kalev Lember <klember@redhat.com> - 0.15-5
- Add file triggers for gtk-update-icon-cache

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 0.15-1
- Update to 0.15
- Use license macro for the COPYING file

* Wed Dec 10 2014 David King <amigadave@amigadave.com> - 0.14-1
- Update to 0.14, own 512x512 directory (#1044771)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 0.13-1
- Update to 0.13 (#1044407)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 0.12-3
- Update icon cache scriptlet

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Alexander Larsson <alexl@redhat.com> - 0.12-1
- Update to 0.12

* Fri Sep 25 2009 Alexander Larsson <alexl@redhat.com> - 0.11-1
- Update to 0.11

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Matthias Clasen <mclasen@redhat.com> - 0.10-5
- Update URL
- Clean up scriptlets
- Include ChangeLog

* Sun Nov 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-4
- Correct the license
- Include COPYING
- Add full source url

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Update the license field

* Fri Feb 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-2
- Own the icon cache

* Thu Nov 23 2006 Alexander Larsson <alexl@redhat.com> - 0.10-1
- Update to 0.10

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9-2.1
- rebuild

* Mon Feb 27 2006 Ray Strode <rstrode@redhat.com> 0.9-2
- Remove Prereq on gtk.  Prereq's complicate things,
  and the gtk-update-icon-cache is already protected by
  [ -x  ... ]

* Thu Jan 12 2006 Alexander Larsson <alexl@redhat.com> 0.9-1
- Update to 0.9, fixes scalable icons picked before bitmap icons

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Florian La Roche <laroche@redhat.com>
- scripts need coreutils installed

* Tue Apr 19 2005 Matthias Clasen <mclasen@redhat.com> 0.8-2
- Silence %%post

* Thu Apr 14 2005 John (J5) Palmieri <johnp@redhat.com>
- Update to 0.8

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 0.7-2
- Update the GTK+ theme icon cache on (un)install

* Fri Feb  4 2005 Alexander Larsson <alexl@redhat.com> - 0.7-1
- Update to 0.7

* Wed Feb  2 2005 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Update to 0.6

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- Update to 0.5

* Wed Sep 29 2004 GNOME <jrb@redhat.com> - 0.3-3
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  4 2004 Alexander Larsson <alexl@redhat.com> 0.3-1
- update to 0.3

* Fri Jan 16 2004 Alexander Larsson <alexl@redhat.com> 0.2-1
- Initial build.
