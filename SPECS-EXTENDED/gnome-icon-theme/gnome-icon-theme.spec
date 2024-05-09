Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:    GNOME icon theme
Name:       gnome-icon-theme
Version:    3.12.0
License:    CC-BY-SA or LGPLv3+
Release:    16%{?dist}
URL:        https://www.gnome.org

#VCS: git:git://git.gnome.org/gnome-icon-theme
Source0: https://download.gnome.org/sources/gnome-icon-theme/3.12/%{name}-%{version}.tar.xz
Source1: legacy-icon-mapping.xml

BuildRequires:  gcc
BuildRequires:  perl(File::Find)
BuildRequires: gtk2
BuildRequires: icon-naming-utils >= 0.8.7
BuildRequires: intltool
BuildRequires: librsvg2
Requires: hicolor-icon-theme

BuildArch: noarch

%description
This package contains the default icon theme used by the GNOME desktop.

%package legacy
Summary: Old names for icons in gnome-icon-theme
Requires: %{name} = %{version}-%{release}

%description legacy
This package contains symlinks to make the icons in gnome-icon-theme
available under old names.

%package devel

Summary: Development files for gnome-icon-theme
Requires: %{name} = %{version}-%{release}

%description devel
Development files for gnome-icon-theme

%prep
%setup -q

%build
%configure --enable-icon-mapping

%install
make install DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_datadir}/icons/gnome/icon-theme.cache

# Don't install icons that conflict with gnome-control-center package
# https://gitlab.gnome.org/GNOME/gnome-control-center/issues/3
rm $RPM_BUILD_ROOT%{_datadir}/icons/gnome/*/categories/gnome-control-center.png

cp %{SOURCE1} .
export INU_DATA_DIR=$PWD
(cd $RPM_BUILD_ROOT%{_datadir}/icons/gnome
for size in 8x8 16x16 22x22 24x24 32x32 48x48 256x256; do
        cd $size || continue;
        echo -e "Adding rtl variants for $size"
        for dir in `find . -type d`; do
                context="`echo $dir | cut -c 3-`"
                if [ $context ]; then
                        icon-name-mapping -c $context
                fi
        done
        cd ..
done
)

# Add scalable directories for symbolic icons
(cd $RPM_BUILD_ROOT%{_datadir}/icons/gnome

mkdir -p scalable/actions
mkdir -p scalable/apps
mkdir -p scalable/devices
mkdir -p scalable/emblems
mkdir -p scalable/mimetypes
mkdir -p scalable/places
mkdir -p scalable/status
)

touch files.txt

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root)"
 find icons/gnome \( -name *-rtl.png -or -name *-ltr.png -or -type f \) -printf "%%%%{_datadir}/%%p\n"
 find icons/gnome -type d -printf "%%%%dir %%%%{_datadir}/%%p\n"
) > files.txt

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root)"
 find icons/gnome \( -type l -and -not -name *-rtl.png -and -not -name *-ltr.png \) -printf "%%%%{_datadir}/%%p\n"
) > legacy.txt

%transfiletriggerin -- %{_datadir}/icons/gnome
gtk-update-icon-cache --force %{_datadir}/icons/gnome &>/dev/null || :

%transfiletriggerpostun -- %{_datadir}/icons/gnome
gtk-update-icon-cache --force %{_datadir}/icons/gnome &>/dev/null || :

%files -f files.txt
%license COPYING COPYING_CCBYSA3 COPYING_LGPL
%doc AUTHORS
%ghost %{_datadir}/icons/gnome/icon-theme.cache

%files legacy -f legacy.txt

%files devel
%{_datadir}/pkgconfig/gnome-icon-theme.pc

%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.12.0-16
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.12.0-15
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.12.0-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Apr 14 2018 Kalev Lember <klember@redhat.com> - 3.12.0-9
- Don't install icons that conflict with gnome-control-center package
  (#1567531)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Kalev Lember <klember@redhat.com> - 3.12.0-6
- Add file triggers for gtk-update-icon-cache

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Matthias Clasen <mclasen@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.5-1
- Update to 3.11.5 

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 3.8.2-4
- Update license to LGPLv3+

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 3.8.2-3
- Split pc file into devel package properly as per guidelines (972372)
- Update to proper license (LGPLv2+)
- Update BR's (use gnome-common)
- Update bogus changelog dates
- Make spec file easier to read
- Add missing url tag

* Sat Jun  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-2
- Drop dep on pkgconfig, instead co-own /usr/share/pkgconfig

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar  5 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Thu Jan 03 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1.2-1
- Update to 3.2.1.2

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1.1-1
- Update to 3.2.1.1

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-2
- Update icon cache scriptlet

* Tue Apr  5 2011 Christopher Aillon <caillon@redhat.com> 3.0.0-1
- Update to 3.0.0

* Wed Mar 30 2011 Matthias Clasen <mclasen@redhat.com> 2.91.93-1
- Update to 2.91.93

* Tue Mar 29 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-6
- Drop the logos package; there shall be no system-logos
  other than fedora-logos...

* Thu Mar 24 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-3
- Make the logos package noarch

* Thu Mar 24 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-2
- Add a logos subpackage

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> 2.91.92-1
- Update to 2.91.92

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-1
- Update to 2.91.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Don't include icon cache

* Mon Feb  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-2
- No longer ship gtk- legacy symlinks in the main package,
  GTK+ doesn't use them anymore
- Do ship -rtl/-ltr symlinks for some names

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> 2.31.0-1
- Update to 2.31.0

* Sun Jun 13 2010 Matthias Clasen <mclasen@redhat.com> 2.30.3-2
- Another attempt to split legacy off

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.3-1
- Update to 2.30.3

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 2.30.2.1-2
- Add scalable directories for symbolic icons

* Thu Apr 29 2010 Bastien Nocera <bnocera@redhat.com> 2.30.2.1-1
- Update to 2.30.2.1

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.2-1
- Update to 2.30.2

* Tue Apr 20 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-2
- Drop extra icons
- Split off a legacy subpackage

* Sun Apr 18 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Fri Apr  2 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-2
- Fix a zoom icon

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> 2.29.3-1
- 2.29.3

* Tue Mar 23 2010 Bastien Nocera <bnocera@redhat.com> 2.29.2-3
- Update scriptlets

* Tue Mar 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.2-2
- Add gtk-missing-image to legacy mapping

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.2-1
- Update to 2.29.2
- The .pc file is back

* Mon Mar  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.0-3
- Add process-working animation back

* Sun Feb 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.0-2
- Fix up some issues with icons that got lost

* Fri Feb 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.0-1
- Update to 2.29.0

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-2
- Add gtk print icons.

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Add a window icon so we don't show missing icons in window frames

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Sat Mar  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-3
- Add a 48x48 spinner back

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb 17 2009 David Zeuthen <davidz@redhat.com> - 2.24.0-3
- Update device icons

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Tweak summary and description

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Wed Jul 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-2
- Re-add the symlinks for gtk stock icons again

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri Jun 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Re-add the symlinks for gtk stock icons, remove some other symlinks

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Wed Apr 16 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-6
- Refresh disc icons

* Tue Apr  1 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-5
- Switch open and close padlock encrypted drives/media
- Replace the flash media icons with something that is compatible
  with the GPL that gnome-icon-theme is under (thanks Mike Langlie)

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-4
- Rebuild

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-3
- Switch media-encrypted and drive-encrypted

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-2
- Add a bunch of device icons from Mike Langlie

* Tue Mar 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Rebuild with newer icon-naming-utils

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90
- Further correction of the license field

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6
- Update license field

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Thu Dec 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4.1-1
- Update to 2.17.4.1

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Tue Nov 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2.1-2
- Fix duplicate emblems in nautilus (#217090)

* Sun Nov 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2.1-1
- Update to 2.17.2.1

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-2
- Fix broken symlinks (#208399)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-1
- Update to 2.16.0.1

* Sun Sep  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> 2.15.92-1.fc6
- Update to 2.15.92
- Require pkgconfig

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> 2.15.91-1.fc6
- Update to 2.15.91

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> 2.15.3-1
- Update to 2.15.3

* Wed Jun  7 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-3
- Fix a problem in %%post (#194323)

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-2
- Add BuildRequires for perl-XML-Parser

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-1
- Update to 2.15.2

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.1-1
- Update to 2.15.1

* Wed Mar 22 2006 Matthias Clasen <mclasen@redhat.com> 2.14.2-2
- Update to 2.14.2
- Add symlinks to make application/xml work

* Sat Feb 25 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-1
- Update to 2.14.1

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-2
- Add small epiphany icon (again!!)

* Sun Feb 12 2006 Ray Strode <rstrode@redhat.com> 2.14.0-1
- Update to 2.14.0

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-4
- Add better shutdown icon

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-3
- Add the spinner back

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-2
- Add back some icons that went missing
- Fix redhat- symlinks that were broken since FC1

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-1
- Update to 2.13.7

* Mon Jan 23 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5.1-2
- Fix a typo in index.theme

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5.1-1
- Update to 2.13.5.1
- BuildRequire icon-naming-utils

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-1
- Update to 2.13.4

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-2
- Update to 2.12.1

* Sat Oct  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-2
- Only call gtk-update-icon-cache on directories which have a
  theme index file

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- update to 2.12.0

* Fri Jul 08 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-6
- update the redone icons with new ones from dfong

* Tue Jul 05 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-5
- replace some upstream icons with redone ones 

* Wed Apr 13 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-4
- Fix redhat-office link

* Wed Apr 13 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-3
- More relative symlink fixes

* Tue Apr 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.1-2
- Use relative symlinks instead of absolute ones, 
  which the build system no longer accepts.

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> - 2.10.1-1
- Update to upstream version 2.10.1

* Thu Mar 17 2005 John (J5) Palmieri <johnp@redhat.com> - 2.9.92-1
- Update to upstream version 2.9.92

* Mon Mar  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-2
- Fix %%post 

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-3
- Silence %%post

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-2
- Prereq gtk2 since we use gtk-update-icon-cache in %%post

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- Update to 2.9.90
- Update icon caches in %%post

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Sep  1 2004 Alexander Larsson <alexl@redhat.com> - 2.7.90-2
- Import copies of fallback icon in other packages (#128800, #114534)

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.90-1
- update to 2.7.90

* Wed Aug  4 2004 Owen Taylor <otaylor@redhat.com> - 1.3.6-1
- Update to 1.3.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 1.2.0-1
- update to 1.2.0

* Wed Mar 10 2004 Alexander Larsson <alexl@redhat.com> 1.1.90-1
- update to 1.1.90

* Wed Mar  3 2004 Alexander Larsson <alexl@redhat.com> 1.1.8-2
- remove redhat-main-menu symlink (#100407)

* Mon Feb 23 2004 Alexander Larsson <alexl@redhat.com> 1.1.8-1
- update to 1.1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 19 2004 Alexander Larsson <alexl@redhat.com> 1.1.5-1
- 1.1.5
- Removed hidden patch. Why should gnome not be visible?
  Its not like you don't see all the kde themes from Gnome, and
  they don't work well in Gnome.

* Thu Oct  9 2003 Alexander Larsson <alexl@redhat.com> 1.0.9-2
- Fix symlinks for redhat menu icons

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 1.0.9-1
- update to 1.0.9

* Tue Jul 15 2003 Matt Wilson <msw@redhat.com> 1.0.6-1
- update to 1.0.6

* Wed Jul  9 2003 Alexander Larsson <alexl@redhat.com> 1.0.5-1.E
- Rebuild

* Tue Jul  1 2003 Alexander Larsson <alexl@redhat.com> 1.0.5-1
- Update to 1.0.5

* Fri Jun 13 2003 Elliot Lee <sopwithredhat.com> 1.0.2-3
- Update evolution icon link again

* Fri May 16 2003 Alexander Larsson <alexl@redhat.com> 1.0.2-2
- Update evolution icon link (#90050)

* Mon Mar 31 2003 Alexander Larsson <alexl@redhat.com> 1.0.2-1
- Update to 1.0.2

* Sun Feb 16 2003 Than Ngo <than@redhat.com> 1.0.0-4
- remove kde hicolor patch, it's not required anymore
- add patch to make gnome icon theme hidden in KDE

* Mon Feb 10 2003 Alexander Larsson <alexl@redhat.com> 1.0.0-3
- inherit from hicolor to make kde work

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 1.0.0-1
- Update to 1.0.0

* Fri Jan 17 2003 Havoc Pennington <hp@redhat.com> 0.1.5-2
- make the gnome theme contain some symlinks to cover 
  the redhat-*.png names

* Mon Dec 16 2002 Alexander Larsson <alexl@redhat.com> 0.1.5-1
- Update to 0.1.5

* Wed Dec  4 2002 Alexander Larsson <alexl@redhat.com> 0.1.3-1
- Initial build.
