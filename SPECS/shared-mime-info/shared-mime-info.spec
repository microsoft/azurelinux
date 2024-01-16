# Disable pkgconfig autodep
%global __requires_exclude ^%{_bindir}/pkg-config$

Summary:        Shared MIME information database
Name:           shared-mime-info
Version:        2.2
Release:        1%{?dist}
License:        GPLv2+
URL:            https://freedesktop.org/Software/shared-mime-info
Source0:        https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/%{version}/shared-mime-info-%{version}.tar.bz2

Source1:        gnome-mimeapps.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/totem/data/mime-type-list.txt | grep -v audio/flac | grep -v ^#` ; do if grep MimeType /home/hadess/Projects/jhbuild/rhythmbox/data/rhythmbox.desktop.in.in | grep -q "$i;" ; then echo "$i=org.gnome.Rhythmbox3.desktop;rhythmbox.desktop;org.gnome.Totem.desktop;" >> totem-defaults.list ; else echo "$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; fi ; done ; for i in `cat /home/hadess/Projects/jhbuild/totem/data/uri-schemes-list.txt | grep -v ^#` ; do echo "x-scheme-handler/$i=org.gnome.Totem.desktop;" >> totem-defaults.list ; done
Source2:        totem-defaults.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/file-roller/data/supported-mime-types | sed 's/;//g'` application/x-source-rpm ; do if grep MimeType /usr/share/applications/org.gnome.Nautilus.desktop | grep -q "$i;" ; then echo "$i=org.gnome.Nautilus.desktop;org.gnome.FileRoller.desktop;" >> file-roller-defaults.list ; elif ! `grep -q $i gnome-mimeapps.list` ; then echo $i=org.gnome.FileRoller.desktop\; >> file-roller-defaults.list ; fi ; done && for i in `grep MimeType= /usr/share/applications/org.gnome.Nautilus.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do if ! `grep -q $i file-roller-defaults.list || grep -q $i gnome-mimeapps.list` ; then echo "missing handler $i" ; fi ; done
Source3:        file-roller-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/org.gnome.eog.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=org.gnome.eog.desktop\; >> eog-defaults.list ; done
Source4:        eog-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/org.gnome.Evince.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=org.gnome.Evince.desktop\; >> evince-defaults.list ; done
Source5:        evince-defaults.list
%global xdgmime_commit de283fc430460b9b3a7e61432a6d273cd64cb102
# Tarball for https://gitlab.freedesktop.org/xdg/xdgmime/-/tree/%%{xdgmime_commit}
Source6: https://gitlab.freedesktop.org/xdg/xdgmime/-/archive/%{xdgmime_commit}/xdgmime-%{xdgmime_commit}.tar.bz2
# Work-around for https://bugs.freedesktop.org/show_bug.cgi?id=40354
Patch0:         0001-Remove-sub-classing-from-OO.o-mime-types.patch
BuildRequires:  docbook-dtd-xml
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  glib-devel
BuildRequires:  itstool
BuildRequires:  libxml2-devel
BuildRequires:  mariner-rpm-macros
BuildRequires:  meson
BuildRequires:  xmlto

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%prep
%autosetup -S git
tar xjf %{SOURCE6}

mv xdgmime-*/ xdgmime/

%build
cd ./xdgmime/
make
cd ..
%meson -Dupdate-mimedb=false -Dxdgmime-path=./xdgmime/
%meson_build

%install
%meson_install

find %{buildroot}%{_datadir}/mime -type d \
| sed -e "s|^$RPM_BUILD_ROOT|%%dir |" > %{name}.files
find %{buildroot}%{_datadir}/mime -type f -not -path "*/packages/*" \
| sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" >> %{name}.files

mkdir -p %{buildroot}/%{_datadir}/applications
install -m 644 %{SOURCE1} %{buildroot}/%{_datadir}/applications/gnome-mimeapps.list
cat %{SOURCE2} >> %{buildroot}/%{_datadir}/applications/gnome-mimeapps.list
cat %{SOURCE3} >> %{buildroot}/%{_datadir}/applications/gnome-mimeapps.list
cat %{SOURCE4} >> %{buildroot}/%{_datadir}/applications/gnome-mimeapps.list
cat %{SOURCE5} >> %{buildroot}/%{_datadir}/applications/gnome-mimeapps.list

# Support fallback/generic mimeapps.list (currently based on gnome-mimeapps.list), see
# https://lists.fedoraproject.org/pipermail/devel/2015-July/212403.html
# https://bugzilla.redhat.com/show_bug.cgi?id=1243049
cp %{buildroot}%{_datadir}/applications/gnome-mimeapps.list \
   %{buildroot}%{_datadir}/applications/mimeapps.list

## remove bogus translation files
## translations are already in the xml file installed
rm -rf %{buildroot}%{_datadir}/locale/*

%check
%meson_test

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:

%transfiletriggerin -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%transfiletriggerpostun -- %{_datadir}/mime
update-mime-database -n %{_datadir}/mime &> /dev/null ||:

%files -f %{name}.files
%license COPYING
%doc README.md NEWS HACKING.md data/shared-mime-info-spec.xml
%{_bindir}/*
%{_datadir}/mime/packages/*
%{_datadir}/applications/mimeapps.list
%{_datadir}/applications/gnome-mimeapps.list
# better to co-own this dir than to pull in pkgconfig
%dir %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/shared-mime-info.pc
%{_mandir}/man*/*
%{_datadir}/gettext/its/shared-mime-info.its
%{_datadir}/gettext/its/shared-mime-info.loc

%changelog
* Tue Jan 16 2024 Bala <Balakumaran.kannan@microsoft.com> - 2.2-1
- Update to 2.2

* Tue Feb 01 2022 Hideyuki Nagase <hideyukn@microsoft.com> - 2.0-5
- Apply patch to build with meson 0.60

* Wed Jul 21 2021 Vinicius Jarina <vinja@microsoft.com> - 2.0-4
- Rebuilt for Mariner Core UI
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 06 2020 Bastien Nocera <bnocera@redhat.com> - 2.0-1
+ shared-mime-info-2.0-1
- Update to 2.0

* Tue May 05 2020 Bastien Nocera <bnocera@redhat.com> - 1.15-4
+ shared-mime-info-1.15-4
- Update mime defaults (eog, totem, evince, file-roller)

* Sun Mar 08 2020 Bastien Nocera <bnocera@redhat.com> - 1.15-3
+ shared-mime-info-1.15-3
- Update eog's defaults

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Bastien Nocera <bnocera@redhat.com> - 1.15-1
+ shared-mime-info-1.15-1
- Update to 1.15

* Fri Sep 20 2019 Bastien Nocera <bnocera@redhat.com> - 1.14-1
+ shared-mime-info-1.14-1
- Update to 1.14
- Update defaults.list

* Wed Sep 11 2019 Bastien Nocera <bnocera@redhat.com> - 1.13.1-1
+ shared-mime-info-1.13.1-1
- Update to 1.13.1

* Wed Sep 11 2019 Bastien Nocera <bnocera@redhat.com> - 1.13-1
+ shared-mime-info-1.13-1
- Update to 1.13

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Bastien Nocera <bnocera@redhat.com> - 1.12-1
+ shared-mime-info-1.12-1
- Update to 1.12

* Thu Jan 17 2019 Bastien Nocera <bnocera@redhat.com> - 1.11-1
+ shared-mime-info-1.11-1
- Update to 1.11

* Wed Dec 12 2018 Bastien Nocera <bnocera@redhat.com> - 1.10-4
+ shared-mime-info-1.10-4
- Add GNOME defaults for Evince

* Thu Oct 04 2018 Bastien Nocera <bnocera@redhat.com> - 1.10-3
+ shared-mime-info-1.10-3
- Update evince's desktop filename

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Bastien Nocera <bnocera@redhat.com> - 1.10-1
+ shared-mime-info-1.10-1
- Update to 1.10

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.9-4
- BR: gcc, .spec cosmetics/cleanup

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.9-2
- cleanup scriptlets

* Mon Sep 18 2017 Bastien Nocera <bnocera@redhat.com> - 1.9-1
+ shared-mime-info-1.9-1
- Update to 1.9

* Wed Sep 06 2017 Bastien Nocera <bnocera@redhat.com> - 1.8-6
+ shared-mime-info-1.8-6
- Update file-roller-defaults.list updates

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Bastien Nocera <bnocera@redhat.com> - 1.8-3
+ shared-mime-info-1.8-3
- Assign CSV files to LO Calc not Math

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Kalev Lember <klember@redhat.com> - 1.8-1
- Update to 1.8

* Mon Sep 05 2016 Bastien Nocera <bnocera@redhat.com> - 1.7-1
- Update to 1.7

* Sat Jun 04 2016 Bastien Nocera <bnocera@redhat.com> - 1.6-3
- Remove file-roller as handler for cbz/cbr files
  See https://bugzilla.gnome.org/show_bug.cgi?id=767244

* Sat Jun 04 2016 Bastien Nocera <bnocera@redhat.com> - 1.6-2
- Allow detecting multi-page DjVu files by filename

* Tue Feb 23 2016 Bastien Nocera <bnocera@redhat.com> 1.6-1
- Update to 1.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Sep 24 2015 Rex Dieter <rdieter@fedoraproject.org> 1.5-2
- shared-mime-info requires /usr/bin/pkg-config (#1266089)

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com> 1.5-1
- Update to 1.5

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> 1.4-7
- Add file triggers for rebuilding the mime database

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 1.4-6
- Provide generic/fallback mimeapps.list too (#1243049)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Bastien Nocera <bnocera@redhat.com> 1.4-4
- Make LibreOffice Math the default for CSV files (#1214896)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 05 2015 Bastien Nocera <bnocera@redhat.com> 1.4-2
- Rename defaults.list to be GNOME specific and follow
  the latest changes in the shared mime info spec

* Thu Feb 05 2015 Bastien Nocera <bnocera@redhat.com> 1.4-1
- Update to 1.4

* Tue Sep 30 2014 Bastien Nocera <bnocera@redhat.com> 1.3-15
- Fix Totem being the default music player (#1146001)

* Wed Sep 03 2014 Bastien Nocera <bnocera@redhat.com> 1.3-14
- Change default viewer to be eog (#1136953)

* Tue Sep 02 2014 Bastien Nocera <bnocera@redhat.com> 1.3-13
- Update for totem desktop name change in GNOME 3.14

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Tom Callaway <spot@fedoraproject.org - 1.3-11
- fix license handling

* Thu Jul 31 2014 Kalev Lember <kalevlember@gmail.com> - 1.3-10
- Update defaults.list for gedit desktop filename change

* Tue Jul 08 2014 Colin Walters <walters@redhat.com> - 1.3-9
- Add requires(post) on coreutils to ensure /usr/bin/touch is present
- Resolves: rhbz#1114119

* Tue Jul 08 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-8
- scriptlet polish

* Thu Jul 03 2014 Bastien Nocera <bnocera@redhat.com> 1.3-7
- Update defaults.list for nautilus desktop filename change (#1095008)

* Fri Jun 27 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-6
- pull in upstream support for new -n option, re-enable fsync default on (#1052173)

* Thu Jun 26 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-5
- include PKGSYSTEM_ENABLE_FSYNC upstream implementation, except default off (#1052173)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- support PKGSYSTEM_ENABLE_FSYNC (#1052173, #fdo70366)

* Tue May 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-2
- %%configure --disable-silent-rules

* Mon May 05 2014 Bastien Nocera <bnocera@redhat.com> 1.3-1
- Update to 1.3

* Mon May 05 2014 Bastien Nocera <bnocera@redhat.com> 1.2-3
- Fix file-roller's desktop filename for GNOME 3.12

* Thu Nov 07 2013 Bastien Nocera <bnocera@redhat.com> 1.2-2
- Update totem mime-type list
- Handle legacy Real Media files by default now that RealPlayer
  doesn't exist any more

* Mon Sep 30 2013 Bastien Nocera <bnocera@redhat.com> 1.2-1
- Update to 1.2
- Open disk images with gnome-disk-image-writer

* Mon Aug 26 2013 Kalev Lember <kalevlember@gmail.com> - 1.1-7
- Don't open XWD files in eog / gthumb (#735611)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun  8 2013 Matthias Clasen <mclasen@redhat.com> - 1.1-5
- Drop pkgconfig dep, instead co-own /usr/share/pkgconfig

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.1-4
- Update for file-roller desktop file vendor prefix removal

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.1-3
- Update for eog desktop file vendor prefix removal

* Sun Feb 17 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1-2
- De-vendorize defaults.list (https://fedorahosted.org/fesco/ticket/1077)

* Wed Feb 13 2013 Bastien Nocera <bnocera@redhat.com> 1.1-1
- Update to 1.1

* Fri Nov 30 2012 Bastien Nocera <bnocera@redhat.com> 1.0-6
- Open src.rpm files in file-roller instead of PackageKit

* Mon Nov 05 2012 Bastien Nocera <bnocera@redhat.com> 1.0-6
- Rebuild file-roller's default list

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Rex Dieter <rdieter@fedoraproject.org> 
- 1.0-4
- defaults.list: s/mozilla-firefox/firefox/ (see #736558)
- defaults.list: s/gpk-install-file/gpk-install-local-file/
- defaults.list: application/x-catalog=gpk-install-catalog.desktop (#770019) 

* Fri May 11 2012 Bastien Nocera <bnocera@redhat.com> 1.0-3
- Use gnome-disk-image-mounter from gnome-disk-utility to handle
  CD images by default (#820403)

* Wed Mar  7 2012 Matthias Clasen <mclasen@redhat.com> - 1.0-2
- Own/%%ghost files generated by update-mime-database from
  freedesktop.org.xml (patch by Ville Skyttä, #716451))

* Tue Jan 17 2012 Bastien Nocera <bnocera@redhat.com> 1.0-1
- Update to 1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Jon Masters <jcm@jonmasters.org> 0.91-6
- Fix interpretation of MP3 files as application/x-designer (#755472)

* Mon Oct 24 2011 Rex Dieter <rdieter@fedoraproject.org> 0.91-5
- s/mozilla-firefox.desktop/firefox.desktop/ (f17+, #736558)

* Thu Oct 13 2011 Bastien Nocera <bnocera@redhat.com> 0.91-4
- Make Evolution the default calendar (and not Gedit...)

* Thu Oct 13 2011 Bastien Nocera <bnocera@redhat.com> 0.91-3
- Make shotwell the default for camera roll handling
- Make shotwell-viewer the default image viewer (for the
  image types it handles)
- Prefer Rhythmbox to Totem for music files

* Sun Sep 18 2011 Bastien Nocera <bnocera@redhat.com> 0.91-2
- Fix changelog entries

* Sun Sep 18 2011 Bastien Nocera <bnocera@redhat.com> 0.91-1
- Update to 0.91

* Thu Aug 25 2011 Bastien Nocera <bnocera@redhat.com> 0.90-9
- Never try to load OO.o files in file-roller

* Thu May 26 2011 Bastien Nocera <bnocera@redhat.com> 0.90-8
- Fix LibreOffice associations (patch from Caolan McNamara, #707971)

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.90-7
- Fix name of nautilus.desktop file (#698502)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Bastien Nocera <bnocera@redhat.com> 0.90-5
- Auto-generate file-roller's bindings as well

* Wed Dec 08 2010 Bastien Nocera <bnocera@redhat.com> 0.90-4
- Update defaults.list and update for newer desktop names,
  with help from Edward Sheldrake (#659457)

* Tue Dec 07 2010 Bastien Nocera <bnocera@redhat.com> 0.90-3
- Add Firefox as the default for application/xhtml+xml
  (#660657)

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 0.90-2
- Update list of defaults, adding new mime-types for Totem,
  as well as scheme handlers, and install defaults for
  Evolution and Firefox

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 0.90-1
- Update to 0.90

* Thu Nov  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.80-2
- rebuild for new libxml

* Thu Sep 30 2010 Bastien Nocera <bnocera@redhat.com> 0.80-1
- Update to 0.80

* Tue Jul  6 2010 Colin Walters <walters@verbum.org> - 0.71-4
- Fix previous change to be Requires(post); spotted by
  Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>

* Sat Jul  3 2010 Colin Walters <walters@verbum.org> - 0.71-3
- Requires(pre) on glib, since update-mime-database uses it
- Remove /dev/null redirection, we should see future errors
  And really, RPM is dumb here - this stuff needs to go to
  log files.

* Tue Jun 01 2010 Bastien Nocera <bnocera@redhat.com> 0.71-2
- Update some OO.o defaults, patch from Caolan McNamara

* Mon Feb 01 2010 Bastien Nocera <bnocera@redhat.com> 0.71-1
- Update to 0.71

* Tue Oct 06 2009 Bastien Nocera <bnocera@redhat.com> 0.70-1
- Update to 0.70

* Thu Sep 24 2009 - Caolán McNamara <caolanm@redhat.com> - 0.60-5
- Resolves: rhbz#508559 openoffice.org desktop files changed name

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 - Bastien Nocera <bnocera@redhat.com> - 0.60-3
- Remove Totem as handling Blu-ray and HD-DVD
- Use brasero-ncb.desktop instead of nautilus-cd-burner for blank devices
- Update media mime-types for Rhythmbox/Totem

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 - Bastien Nocera <bnocera@redhat.com> - 0.60-1
- Update to 0.60

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-6
- Update with comments from Orcan Ogetbil <orcanbahri@yahoo.com>

* Wed Nov 26 2008 - Julian Sikorski <belegdol[at]gmail[dot]com> - 0.51-5
- Fix text/plain, gedit installs gedit.desktop and not gnome-gedit.desktop

* Wed Oct 29 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-4
- Add patch to avoid picture CD being anything with a pictures directory
  (#459365)

* Thu Oct 02 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-3
- Use evince, not tetex-xdvi.desktop for DVI files (#465242)

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-2
- Use Firefox and not redhat-web as the default app for HTML files (#452184)

* Wed Jul 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.51-1
- Update to 0.51

* Tue Jul 22 2008 - Bastien Nocera <bnocera@redhat.com> - 0.50-1
- Update to 0.50

* Sat Jun 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.40-2
- update license tag

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.40-1
- Update to 0.40

* Mon May 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.30-1
- Update to 0.30

* Fri May  2 2008 David Zeuthen <davidz@redhat.com> - 0.23-9
- Fix defaults for x-content/image-dcf (#445032)

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-8
- Make mount-archive.desktop the default for iso images (#442960)

* Tue Apr 15 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-7
- Update the desktop file name for Gimp, too

* Tue Apr 15 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-6
- Change default for rpm to gpk-install-file (#442485)

* Thu Mar 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.23-5
- Make Totem the default for the mime-types it handles (#366101)
- And make sure Rhythmbox is the second default only for the mime-types
  it handles

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-4
- Change default for rpm to pk-install-file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.23-3
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.23-2
- Add defaults for content types

* Tue Dec 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.23-1
- Update to 0.23

* Tue Nov 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-5
- Remove Totem as the default music/movie player, it will be the
  default for movies, as only it handles them, and Rhythmbox can
  handle missing plugins now

* Mon Nov 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-4
- Make Totem the default for the mime-types it handles (#366101)

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 0.22-3
- Rebuild for PPC toolchain bug
- BuildRequires: gawk

* Tue Aug 21 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-2
- Don't say that webcal files are handled by evolution-2.0, it can't
- Disable vCard mapping as well, as evolution doesn't handle it
  (See http://bugzilla.gnome.org/show_bug.cgi?id=309073)

* Mon Jul 30 2007 - Bastien Nocera <bnocera@redhat.com> - 0.22-1
- Update to 0.22

* Tue Apr 17 2007 - Bastien Nocera <bnocera@redhat.com> - 0.20-2
- Fix the dia association (#194313)

* Tue Feb 06 2007 - Bastien Nocera <bnocera@redhat.com> - 0.20-1
- Update to 0.20, and remove outdated patches

* Fri Nov 10 2006 Christopher Aillon <caillon@redhat.com> - 0.19-2
- Alias image/pdf to application/pdf

* Fri Aug 25 2006 Christopher Aillon <caillon@redhat.com> - 0.19-1
- Update to 0.19

* Wed Jul 26 2006 Matthias Clasen <mclasen@redhat.com> - 0.18-2
- add an inode/directory entry to defaults.list (#187021)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.18-1.1
- rebuild

* Wed Jul  5 2006 Kristian Høgsberg <krh@redhat.com> - 0.18-1
- Update to 0.18 and drop backported patches.

* Thu Jun 29 2006 Kristian Høgsberg <krh@redhat.com> - 0.17-3
- Adding PDF fix backported from CVS.

* Wed Mar 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.17-2
- Backport upstream change to fix postscript vs. matlab confusion

* Thu Mar 16 2006 Matthias Clasen <mclasen@redhat.com> - 0.17-1
- Update to 0.17

* Mon Feb 13 2006 Ray Strode <rstrode@redhat.com> - 0.16.cvs20060212-3
- add gthumb as fallback

* Mon Feb 13 2006 Ray Strode <rstrode@redhat.com> - 0.16.cvs20060212-2
- make eog the default image viewer

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 0.16.cvs20060212-1
- Newer CVS snapshot

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.16.cvs20051219-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Caolan McNamara <caolanm@redhat.com> - 0.16.cvs20051219-2
- rh#179138# add openoffice.org as preferred app for oasis formats 

* Mon Dec 19 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051219-1
- Newer cvs snapshot

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051201-1
- Incorporate upstream changes

* Wed Nov 02 2005 John (J5) Palmieri <johnp@redhat.com> - 0.16.cvs20051018-2
- Change all refs of eog to gthumb in defaults.list

* Tue Oct 18 2005 Matthias Clasen <mclasen@redhat.com> - 0.16.cvs20051018-1
- Incorporate upstream changes

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 0.16-6
- Add glade to defaults.list

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 0.16-5
- Make sure Type1 fonts are recognized as such (#160909)

* Fri Jun 17 2005 David Zeuthen <davidz@redhat.com> - 0.16-4
- Add MIME-types for .pcf Cisco VPN settings files (fdo #3560)

* Fri May 20 2005 Dan Williams <dcbw@redhat.com> - 0.16-3
- Update OpenOffice.org desktop file names. #155353
- WordPerfect default now OOo Writer, since Abiword is in Extras

* Sun Apr  3 2005 David Zeuthen <davidz@redhat.com> - 0.16-2
- Make Evince the default for application/pdf and application/postscript
- Remove remaining references to gnome-ggv (application/x-gzpostscript and
  image/x-eps) as this is no longer in the distribution

* Fri Apr  1 2005 David Zeuthen <davidz@redhat.com> - 0.16-1
- Update to upstream release 0.16
- Drop all patches as they are in the new upstream release

* Wed Mar  9 2005 David Zeuthen <davidz@redhat.com> - 0.15-11
- Add mimetypes for OOo2 (#150546)

* Mon Oct 18 2004 Alexander Larsson <alexl@redhat.com> - 0.15-10
- Fix for mime sniffing on big-endian

* Thu Oct 14 2004 Colin Walters <walters@redhat.com> - 0.15-9
- Handle renaming of hxplay.desktop to realplay.desktop

* Wed Oct 13 2004 Matthias Clasen <mclasen@redhat.com> - 0.15-8
- Handle XUL files. #134122

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> - 0.15-7
- Make helix default for ogg and mp3, will switch wav/flac too 
  when support is added

* Wed Oct  6 2004 Alexander Larsson <alexl@redhat.com> - 0.15-6
- Change default pdf viewer to ggv

* Tue Sep  7 2004 Alexander Larsson <alexl@redhat.com> - 0.15-4
- Fixed evo desktop file reference in defaults.list

* Mon Sep  6 2004 Caolan McNamara <caolanm@redhat.com> - 0.15-3
- wpd can be opened in abiword, but not in openoffice.org (#114907)

* Fri Sep  3 2004 Alexander Larsson <alexl@redhat.com> - 0.15-2
- Add list of default apps (#131643)

* Mon Aug 30 2004 Jonathan Blandford <jrb@redhat.com> 0.15-1
- bump version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 22 2004 Alex Larsson <alexl@redhat.com> 0.14-1
- update to 0.14

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 0.13-1
- 0.13

* Fri Jan 16 2004 Alexander Larsson <alexl@redhat.com> mime-info
- Initial build.
