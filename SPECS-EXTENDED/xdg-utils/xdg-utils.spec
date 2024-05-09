Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Summary: Basic desktop integration functions 
Name:    xdg-utils
Version: 1.1.3
Release: 7%{?dist}

URL:     https://portland.freedesktop.org/ 
%if 0%{?snap:1}
Source0: xdg-utils-%{version}-%{snap}.tar.gz
%else
# at least until freedesktop folks move over to release dir
Source0:  https://people.freedesktop.org/~rdieter/xdg-utils/xdg-utils-%{version}.tar.gz
#Source0: https://portland.freedesktop.org/download/xdg-utils-%{version}%{?prerelease:-%{prerelease}}.tar.gz
%endif
Source1: xdg-utils-git_checkout.sh
License: MIT 

## upstream patches (treat as sources in lookaside cache)
Patch1: 0001-open-for-post-1.1.3-development.patch
Patch2: 0002-xdg-open-better-pcmanfm-check-BR106636-BR106161.patch

# make sure BuildArch comes *after* patches, to ensure %%autosetup works right
# https://bugzilla.redhat.com/1084309
BuildArch: noarch

BuildRequires: gawk
BuildRequires: xmlto lynx

Requires: coreutils
Requires: desktop-file-utils
Requires: which

%description
The %{name} package is a set of simple scripts that provide basic
desktop integration functions for any Free Desktop, such as Linux.
They are intended to provide a set of defacto standards.  
This means that:
*  Third party software developers can rely on these xdg-utils
   for all of their simple integration needs.
*  Developers of desktop environments can make sure that their
   environments are well supported
*  Distribution vendors can provide custom versions of these utilities

The following scripts are provided at this time:
* xdg-desktop-icon      Install icons to the desktop
* xdg-desktop-menu      Install desktop menu items
* xdg-email             Send mail using the user's preferred e-mail composer
* xdg-icon-resource     Install icon resources
* xdg-mime              Query information about file type handling and
                        install descriptions for new file types
* xdg-open              Open a file or URL in the user's preferred application
* xdg-screensaver       Control the screensaver
* xdg-settings          Get various settings from the desktop environment


%prep
%autosetup -n %{name}-%{version}%{?pre:-%{pre}} -p1


%build
%configure

%if 0%{?snap:1}
make scripts-clean -C scripts 
make man scripts %{?_smp_mflags} -C scripts
%endif
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc ChangeLog LICENSE README TODO
%{_bindir}/xdg-desktop-icon
%{_bindir}/xdg-desktop-menu
%{_bindir}/xdg-email
%{_bindir}/xdg-icon-resource
%{_bindir}/xdg-mime
%{_bindir}/xdg-open
%{_bindir}/xdg-screensaver
%{_bindir}/xdg-settings
%{_mandir}/man1/xdg-desktop-icon.1*
%{_mandir}/man1/xdg-desktop-menu.1*
%{_mandir}/man1/xdg-email.1*
%{_mandir}/man1/xdg-icon-resource.1*
%{_mandir}/man1/xdg-mime.1*
%{_mandir}/man1/xdg-open.1*
%{_mandir}/man1/xdg-screensaver.1*
%{_mandir}/man1/xdg-settings.1*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.3-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.1.3-2
- pull in upstream fixes

* Thu May 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.1.3-1
- xdg-utils-1.1.3

* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.1.2-4
- pull in upstream fixes

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.1.2-1
- xdg-utils-1.1.2

* Mon Feb 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-5
- pull in upstream fixes

* Thu May 05 2016 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-4
- save mimetype defaults to ~/.config/mimeapps.list
  (instead of ~/.local/share/applications/mimeapps.list)

* Fri Apr 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- pull in latest upstream fixes

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-1
- 1.1.1

* Mon Oct 05 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-1
- 1.1.0 (final)

* Wed Sep 30 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.42.20150927git
- 20150927git snapshot

* Wed Jul 15 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.41.20150715git
- 20150715git snapshot

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.40.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 24 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.39.rc3
- 'xdg-mime query default' return multiple .desktop entries (fdo#60329,#1195718)

* Sat Feb 21 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.38.rc3
- minor s/$arg/$target/ fix for prior commit

* Fri Feb 20 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.37.rc3
- xdg-open wrongly passes all command line arguments as one argument to e.g. okular on non Gnome desktops (#1191981)

* Mon Jan 19 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.36.rc3
- pull in upstream performance improvement (fdo#88524)

* Mon Jan 19 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.35.rc3
- pull in latest commits, notably more fdo screensaver fixes

* Tue Jan 06 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.34.rc3
- refresh for latest attepmt to fix upstream BR66670

* Mon Jan 05 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.33.rc3
- pull in latest commits

* Sat Jan 03 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.32.rc3
- xdg-utils-1.1.0-rc3

* Tue Oct 21 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.31.rc2
- workaround %%autosetup failure harder (#1084309)

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.30.rc2
- workaround %%autosetup failure, again (#1084309)

* Thu Oct 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.29.rc2
- xdg-screensaver plasma5 support

* Mon Sep 22 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.28.rc2
- plasma5: ktraderclient5, kreadconfig5, kwriteconfig5

* Mon Sep 22 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.27.rc2
- more upstream goodness, initial plasma5 support

* Sat Sep 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.26.rc2
- pull in latest upstream fixes

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.25.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Till Maas <opensource@till.name> - 1.1.0-0.24.rc2
- Fix patch from 1.1.0-0.23.rc2 (#1086122)

* Fri Apr 11 2014 Till Maas <opensource@till.name> - 1.1.0-0.23.rc2
- Fix handling of desktop files with multiple groups (#1086122)

* Fri Apr 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.22.rc2
- drop using %%autosetup (it didn't work?)

* Sun Mar 30 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-0.21.rc2
- .spec housecleaning (remove deprecated stuff)
- pull in latest upstream fixes, including...
- xdg-open does not substitute all field codes in Exec key (#1056431, fdo#49204)

* Fri Feb 07 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.20.rc2
- 1.1.0-rc2

* Sat Oct 05 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.18.20131005git
- 20131005 snapshot

* Mon Aug 05 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.17.20120809git
- BR: text-www-browser (#992895)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.16.20120809git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.15.20120809git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.14.20120809git
- 20120809 snapshot

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.13.20120302git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.12.20120302git
- 20120302 snapshot
- patches for unknown DE (#769305)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.11.20111207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.10.20110714git
- fix gnome-screensaver detection bogosity (#702540,#736159)
- xdg-open: x-www-browser: command not found (#755553)
- drop htmlview hackage

* Thu Jul 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.9.20110714
- 20110714 snapshot
- xdg-mime : use 'file --mime-type' instead of 'file -i'

* Thu Jun 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.8.20110510
- rebuild

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.7.20110510
- fix gnome3 detection, gnome-default-applications-properties error output

* Thu May 05 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.6.20110505
- Error in xdg-open script (#702347)

* Wed May 04 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.5.20110504
- 20110504 snapshot
- xdg-email does not work (#690840)

* Fri Apr 08 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.4.20110408
- 20110408 snapshot
- Shouldn't use user's defaults.list (#678656)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.3.20110201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.2.20110201
- 20110201 snapshot
- add gnome3 support, make default browser work again for xdg-settings (#654746)

* Mon Jan 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-0.1.rc1
- xdg-utils-1.1.0-rc1

* Thu Oct 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-21.20101028
- lxde support (#580835, fdo#26058))

* Fri Jul 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-20.20100709
- xdg-screensaver: consider gnome-screensaver a separate DE (fdo#20027)

* Fri Jul 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-19.20100709
- xdg-open man page needs updating to include FILE and SEE ALSO (#603841)
- xdg-open should call mimeopen with -L option (#430072)
- xdg-desktop-icon :  use localized desktop folder name (fdo#19011)

* Fri Apr 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-18.20100409
- xdg-settings fixes (#580715, fdo#26284)

* Mon Jan 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-17.20100118cvs
- xdg-screensaver resume activates the screensaver on KDE4 (fdo#26085) 

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-16.20091217cvs
- xdg-mime: line 531: kde-config: command not found (#545702)
- xdg-email calls gconftool which doesn't exist (#548529)

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-15.20091016cvs
- add Obsoletes: htmlview (#541179, f13+)

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-14.20091016cvs
- prefer gvfs-open over gnome-open (#529287)
- DE=gnome, if org.gnome.SessionManager exists on dbus (#529287)

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-13.20090928cvs
- xdg-open: use kde-open

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-12.20090921cvs
- suppress stderr from kde-config (#524724)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-11.20090913cvs
- 20090913cvs snapshot
- xdg-open in xdg-utils expects xprop to be available (#506857)

* Mon Aug 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-10.20090824cvs
- 20090824cvs snapshot

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9.20081121cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-8.20081121cvs
- revert.  kfmclient openURL is largely useless 

* Wed Apr 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-7.20081121cvs
- xdg-open: s/kfmclient exec/kfmclient openURL/ (CVE-2009-0068, rh#472010, fdo#19377)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6.20081121cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-5.20081121cvs
- upstreamed a few more patches, rebase to cvs snapshot

* Fri Jan 25 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.0.2-4
- Fix for CVE-2008-0386 (#429513)

* Fri Jan 18 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-3
- fix mimeopen support (#429280)
- spec cosmetics: cleanup macro usage

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-2
- Requires: which (#312601)

* Sun Jun 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-1
- xdg-utils-1.0.2

* Mon Apr 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-3
- add htmlview,links to browser fallbacks

* Tue Dec 19 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-2
- fix typo in xdg-icon-resource manpage

* Mon Nov 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.1-1
- xdg-utils-1.0.1

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net 1.0-3
- actually *use* mimeopen patch (#210797)

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-2
- prefer mimeopen as generic default (#210797)

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-1
- 1.0(final)

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.9.rc1
- update %%description (#208926)

* Wed Sep 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.8.rc1
- 1.0rc1

* Fri Sep 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.7.beta4
- 1.0beta4

* Mon Aug 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.6.beta3
- 1.0beta3

* Thu Jul 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.5.20060721
- Release: append/use %%{?dist}

* Wed Jul 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.4.20060721
- specfile cosmetics, tabs -> spaces
- %%makeinstall -> make install DESTDIR=...

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.3.20060721
- 20060721 snapshot
- optgnome.patch

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.2.beta1
- Requires: desktop-file-utils

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.1.beta1
- 1.0beta1

