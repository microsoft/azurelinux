Name:          zenity
Version:       4.0.3
Release:       1%{?dist}
Summary:       Display dialog boxes from shell scripts

License:       LGPL-2.1-or-later
URL:           https://wiki.gnome.org/Projects/Zenity
Source:        https://download.gnome.org/sources/%{name}/4.0/%{name}-%{version}.tar.xz

BuildRequires: pkgconfig(libadwaita-1) >= 1.2
BuildRequires: /usr/bin/help2man
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: itstool
BuildRequires: meson
BuildRequires: which
# Tests
BuildRequires: xwayland-run
BuildRequires: mutter
BuildRequires: mesa-dri-drivers

%description
Zenity lets you display Gtk+ dialog boxes from the command line and through
shell scripts. It is similar to gdialog, but is intended to be saner. It comes
from the same family as dialog, Xdialog, and cdialog.

%prep
%autosetup -p1


%build
%meson
# Man page generation requires running the in-tree zenity command.
%{shrink:xwfb-run -c mutter -w 10 -- %meson_build}


%install
%meson_install

# we don't want a perl dependency just for this
rm -f %{buildroot}/%{_bindir}/gdialog

%find_lang zenity --with-gnome

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Zenity.desktop


%files -f zenity.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/zenity
%{_datadir}/applications/org.gnome.Zenity.desktop
%{_datadir}/icons/hicolor/48*48/apps/zenity.png
%{_mandir}/man1/zenity.1*


%changelog
* Thu Oct 24 2024 David King <amigadave@amigadave.com> - 4.0.3-1
- Update to 4.0.3

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 David King <amigadave@amigadave.com> - 4.0.2-1
- Update to 4.0.2

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 4.0.1-1
- Update to 4.0.1

* Sat Dec 09 2023 Kalev Lember <klember@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 3.99.91-1
- Update to 3.99.91

* Wed Nov 22 2023 Kalev Lember <klember@redhat.com> - 3.99.90-1
- Update to 3.99.90

* Thu Sep 21 2023 Kalev Lember <klember@redhat.com> - 3.99.2-1
- Update to 3.99.2

* Mon Aug 14 2023 Kalev Lember <klember@redhat.com> - 3.99.1-1
- Update to 3.99.1

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.99.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Kalev Lember <klember@redhat.com> - 3.99.0-1
- Update to 3.99.0

* Mon May 08 2023 Adam Williamson <awilliam@redhat.com> - 3.92.0-2
- Backport two patches from upstream to hopefully really fix crashes (#2177287)

* Tue May 02 2023 David King <amigadave@amigadave.com> - 3.92.0-1
- Update to 3.92.0

* Thu Apr 20 2023 Adam Williamson <awilliam@redhat.com> - 3.91.0-3
- Backport MRs #26 and #27 to fix bugs in tree views (#2184783)
- Backport MR #28 to fix some console error spam

* Thu Apr 20 2023 Adam Williamson <awilliam@redhat.com> - 3.91.0-2
- Backport MR #25 for crash when --no-cancel and/or --auto-close are used (#2177287)

* Tue Mar 07 2023 David King <amigadave@amigadave.com> - 3.91.0-1
- Update to 3.91.0

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 3.90.0-1
- Update to 3.90.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.43.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.43.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Honore Doktorr <hdfssk@gmail.com> - 3.43.0-2
- Add missing BuildRequires for pkgconfig(libnotify)
- enable libnotify option for meson build

* Thu Jul 07 2022 David King <amigadave@amigadave.com> - 3.43.0-1
- Update to 3.43.0

* Wed Apr 27 2022 David King <amigadave@amigadave.com> - 3.42.1-1
- Update to 3.42.1

* Fri Apr 01 2022 David King <amigadave@amigadave.com> - 3.42.0-1
- Update to 3.42.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 06 2021 Kalev Lember <klember@redhat.com> - 3.41.0-2
- Fix eln build

* Mon Aug 23 2021 Kalev Lember <klember@redhat.com> - 3.41.0-1
- Update to 3.41.0
- Switch to meson build system

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 04 2021 David King <amigadave@amigadave.com> - 3.32.0-6
- Use make macros

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 22 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 05 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Fri Dec 01 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Don't set group tags

* Wed Mar 23 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 17 2015 Kalev Lember <klember@redhat.com> - 3.18.1.1-1
- Update to 3.18.1.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0
- Use make_install macro

* Tue Jun 23 2015 David King <amigadave@amigadave.com> - 3.16.3-1
- Update to 3.16.3
- Use pkgconfig for BuildRequires
- Preserve timestamps during install
- Update man page glob in files section

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Wed May 13 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0
- Use license macro for the COPYING file

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Mon Sep 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Thu Apr 24 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.12.0-1
- Update to 3.12.0
- Make build more verbose
- Fix bogus dates in %%changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-2
- Minor spec file updates for 3.8

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0
- Don't run autoreconf and intltoolize in the spec file; the tarball should be
  good enough

* Mon Mar 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.2.0-4
- Don't introduce a webkit dependency (#804451)

* Tue Mar  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2.0-3
- Fix F-17 FTBFS

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-5
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-3
- Rebuild against newer gtk

* Tue Jan 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Avoid a segfault (#670895)

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1.1-2
- Rebuild against new gtk

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1.1-1
- Update to 2.91.1.1
- Drop space-saving hack

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update 2.26.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3.1-1
- Update to 2.23.3.1

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Sat Feb  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.1-3
- Rebuild for gcc 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Rebuild to fix upgrade path

* Tue Nov 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates)

* Mon Oct 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-3
- Rebuild against new dbus-glib

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Drop yelp dependency to avoid exploding live cds (#295091)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Thu Aug 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-2
- Drop gdialog and the perl dependency

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-4
- Use %%find_lang for help files

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Incorporate package review feedback

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Mon Dec  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-2
- Add a BuildRequires for libnotify-devel

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0
- Add missing BRs

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-4
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-3
- Add missing BuildRequires

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-2
- Rebuild

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-1
- Update to 2.15.2
- Remove po/LINGUAS fixes

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.1-1
- Update to 2.15.1

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-4
- More package review feedback

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-3
- Incorporate package review feedback

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-2
- Initial revision
