Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       generic-logos
Version:    18.0.0
Release:    11%{?dist}
Summary:    Icons and pictures

URL:        https://pagure.io/generic-logos
Source0:    https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2
#The KDE Logo is under a LGPL license (no version statement)
License:    GPLv2 and LGPLv2+
BuildArch:  noarch

Obsoletes:  redhat-logos
Obsoletes:  generic-logos < 17.0.0-5
Provides:   redhat-logos = %{version}-%{release}
Provides:   system-logos = %{version}-%{release}

Conflicts:  fedora-logos
Conflicts:  anaconda-images <= 10
Conflicts:  redhat-artwork <= 5.0.5
BuildRequires: fdupes
# For _kde4_* macros:
BuildRequires: kde-filesystem
# For generating the EFI icon
BuildRequires: libicns-utils
Requires(post): coreutils

%description
The generic-logos package contains various image files which can be
used by the bootloader, anaconda, and other related tools. It can
be used as a replacement for the fedora-logos package, if you are
unable for any reason to abide by the trademark restrictions on the
fedora-logos or fedora-remix-logos package.

%package httpd
Summary: Fedora-related icons and pictures used by httpd
Provides: system-logos-httpd = %{version}-%{release}
Provides: fedora-logos-httpd = %{version}-%{release}
Obsoletes:  generic-logos < 17.0.0-5
BuildArch: noarch

%description httpd
The generic-logos-httpd package contains image files which can be used by
httpd.

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/firstboot/themes/generic
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/generic
done

mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.vol %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora-media.vol  %{buildroot}%{_datadir}/pixmaps/bootloader

mkdir -p %{buildroot}%{_datadir}/pixmaps/splash
for i in gnome-splash/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps/splash
done

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

for size in scalable ; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$size/apps
  ln -s ../../../hicolor/$size/apps/fedora-logo-icon.svg icon-panel-menu.svg
  ln -s ../../../hicolor/$size/apps/fedora-logo-icon.svg gnome-main-menu.svg
  ln -s ../../../hicolor/$size/apps/fedora-logo-icon.svg kmenu.svg
  ln -s ../../../hicolor/$size/apps/fedora-logo-icon.svg start-here.svg
  install -p -m 644 pixmaps/fedora-logo-sprite.svg %{buildroot}%{_datadir}/icons/hicolor/$size/apps/fedora-logo-icon.svg
done

mkdir -p %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
mkdir -p %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
install -p -m 644 ksplash/SolarComet-kde.png %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

mkdir -p %{buildroot}%{_datadir}/plymouth/themes/charge/
for i in plymouth/charge/* ; do
    install -p -m 644 $i %{buildroot}%{_datadir}/plymouth/themes/charge/
done

# File or directory names do not count as trademark infringement
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install	-p -m 644 icons/Fedora/scalable/apps/* %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -p -m 644 pixmaps/fedora-logo-sprite.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 pixmaps/fedora-logo-sprite.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/start-here.svg

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/places/
pushd %{buildroot}%{_datadir}/icons/hicolor/scalable/places/
ln -s ../apps/start-here.svg .
popd

(cd anaconda; make DESTDIR=%{buildroot} install)

# save some dup'd icons
%fdupes %{buildroot}/

%post
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/hicolor/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
  if [ -f %{_kde4_iconsdir}/Fedora-KDE/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/Fedora-KDE/index.theme || :
  fi
fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/oxygen/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/oxygen/index.theme || :
  fi
fi


%files
%license COPYING COPYING-kde-logo
%doc README
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/boot/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/pixmaps/*
%exclude %{_datadir}/pixmaps/poweredby.png
%{_datadir}/plymouth/themes/charge/*
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
%{_kde4_iconsdir}/oxygen/

%files httpd
%license COPYING
%{_datadir}/pixmaps/poweredby.png

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 18.0.0-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Aug 04 2019 Neal Gompa <ngompa13@gmail.com> - 18.0.0-9
- Update URLs for new location
- Correctly store license files
- Switch from hardlink to fdupes for deduplication (#1721939)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Bill Nottingham <notting@splat.cc> - 18.0.0-3
- properly put icons in hicolor themes (#1444124)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Bill Nottingham <notting@splat.cc> - 18.0.0-1
- update boot file definition, add anconda sidebar/topbar logos

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 22 2013 Bill Nottingham <notting@redhat.com> - 17.0.0-5
- Add a -httpd subpackage. (#1031288)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  2 2012 Bill Nottingham <notting@redhat.com> - 17.0.0-1
- update for Fedora 17 - .vol files for mactel boot

* Fri Oct 14 2011 Bill Nottingham <notting@redhat.com> - 16.0.0-1
- update syslinux & firstboot splashes for F16

* Tue Mar 22 2011 Bill Nottingham <notting@redhat.com> - 15.0.0-1
- update for Fedora 15

* Fri Dec 17 2010 Matthew Garrett <mjg@redhat.com> - 14.0.2-1
- add an icon for Mac EFI bootloaders

* Mon Nov 29 2010 Bill Nottingham <notting@redhat.com> - 14.0.1-3
- prereq coreutils (#657766)

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 14.0.1-2
- s/Fedora-KDE/oxygen/ icons (#615621)
- use hardlink to save a little space
 
* Tue Sep 14 2010 Bill Nottingham <notting@redhat.com> - 14.0.1-1
- fix for new anaconda paths

* Mon Sep 13 2010 Bill Nottingham <notting@redhat.com> - 14.0-1
- update for Fedora 14

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 13.0.2-1
- sync with current anaconda reality (#618598, <jkeating@redhat.com>)

* Sat Jul 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 13.0.1-3
- fix %%postun scriptlet error

* Fri Jun 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 13.0.1-2
- Fedora-KDE icons are now fedora-kde-icons-theme, not kde-settings
- include icon scriplets
- drop ancient Conflicts: kdebase ...

* Tue May  4 2010 Bill Nottingham <notting@redhat.com> - 13.0.1-1
- Add logos to make firstboot work

* Mon May  3 2010 Bill Nottingham <notting@redhat.com> - 13.0-1
- Update for Fedora 13

* Sat Dec 26 2009 Fabian Affolter <fabian@bernewireless.net> - 12.2-3
- Changed SourceO to upstream link
- Added URL and README
- Added version to LGPL of the KDE logo
- Minor cosmetic layout changes

* Wed Nov  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12.2-2
- kde icon installation

* Fri Oct 30 2009 Bill Nottingham <notting@redhat.com> - 12.2-1
- tweak anaconda.png/svg to match rest of icons (<duffy@redhat.com>)

* Fri Oct 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12.1-1
- 12.1 (add generic versions of anaconda.png/svg)

* Thu Oct  1 2009 Bill Nottingham <notting@redhat.com> - 12.0-1
- update for F12 (<duffy@redhat.com>)

* Tue May 12 2009 Bill Nottingham <notting@redhat.com> - 11.0.1-1
- Add new plymouth artwork (#500239)

* Wed Apr 22 2009 Bill Nottingham <notting@redhat.com> - 11.0.0-1
- updates for Fedora 11

* Wed Dec  3 2008 Bill Nottingham <notting@redhat.com> - 10.0.2-1
- fix syslinux splash (accidentally branded)

* Tue Oct 28 2008 Bill Nottingham <notting@redhat.com> - 10.0.1-1
- incorporate KDE logo into upstream source distribution
- fix system-logo-white.png for compiz bleeding (#468258)

* Mon Oct 27 2008 Jaroslav Reznik <jreznik@redhat.com> - 10.0.0-3
- Solar Comet generic splash logo redesign

* Sun Oct 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 10.0.0-2
- Add (current version of) KDE logo for SolarComet KSplash theme

* Thu Oct 23 2008 Bill Nottingham <notting@redhat.com> - 10.0.0-1
- update for current fedora-logos, with Solar theme

* Fri Jul 11 2008 Bill Nottingham <notting@redhat.com> - 9.99.0-1
- add a system logo for plymouth's spinfinity plugin

* Tue Apr 15 2008 Bill Nottingham <notting@redhat.com> - 9.0.0-1
- updates for current fedora-logos (much thanks to <duffy@redhat.com>)
- remove KDE Infinity splash
 
* Mon Oct 29 2007 Bill Nottingham <notting@redhat.com> - 8.0.2-1
- Add Infinity splash screen for KDE

* Thu Sep 13 2007 Bill Nottingham <notting@redhat.com> - 7.92.1-1
- add powered-by logo (#250676)
- updated rhgb logo (<duffy@redhat.com>)

* Tue Sep 11 2007 Bill Nottinghan <notting@redhat.com> - 7.92.0-1
- initial packaging. Forked from fedora-logos, adapted from the Fedora
  Art project's Infinity theme
