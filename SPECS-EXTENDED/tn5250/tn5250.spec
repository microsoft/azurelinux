Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# workaround https://bugzilla.redhat.com/show_bug.cgi?id=1290742
%undefine _hardened_build

Summary:   5250 Telnet protocol and Terminal
Name:      tn5250
Version:   0.17.4
Release:   26%{?dist}
License:   LGPLv2+
Source:    https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:   xt5250.desktop
# https://github.com/sharkcz/tn5250/tree/fedora
Patch0:    tn5250-0.17.4-fedora.patch
URL:       https://tn5250.sourceforge.net/
Requires:  dialog
Requires:  xterm
Requires:  hicolor-icon-theme
BuildRequires: gcc
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: desktop-file-utils
BuildRequires: libtool


%description
tn5250 is an implementation of the 5250 Telnet protocol.
It provides the 5250 library and a 5250 terminal emulation.


%package devel
Summary: Development tools for the 5250 protocol
Requires: ncurses-devel
Requires: openssl-devel
Requires: %{name} = %{version}-%{release}

%description devel
Libraries and header files to use with lib5250.


%prep
%setup -q
%patch 0 -p1 -b .fedora

autoreconf -vfi


%build
%configure --disable-static --disable-silent-rules

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/{48x48,64x64}/apps
install -m644 -p linux/5250.tcap $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m644 -p linux/5250.terminfo $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m644 -p tn5250-48x48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/tn5250.png
install -m644 -p tn5250-62x48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/tn5250.png
install -m644 -p tn5250-48x48.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/tn5250.xpm
install -m644 -p tn5250-62x48.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/tn5250.xpm
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib5250.la
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
desktop-file-install  \
   --dir $RPM_BUILD_ROOT/%{_datadir}/applications %{SOURCE1}
cp -pf linux/README README.Linux

/usr/bin/tic -o $RPM_BUILD_ROOT/%{_datadir}/terminfo linux/5250.terminfo


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README* TODO
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/*
%{_datadir}/terminfo/5/5250
%{_datadir}/terminfo/x/xterm-5250

%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.17.4-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.17.4-20
- Remove obsolete scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Dan Horák <dan[at]danny.cz> - 0.17.4-17
- updated for OpenSSL 1.1 (#1424139)
- spec file cleanup (#1319118)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Dan Horák <dan[at]danny.cz> - 0.17.4-14
- disable hardening to workaround bug 1290742

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 03 2013 Dan Horák <dan[at]danny.cz> - 0.17.4-10
- spec cleanup, update scriptlets
- remove rpath
- fix build with -Werror=format-security (#1037360)
- move generating terminfo to pkg build time, fixes file ownership

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 14 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 0.17.4-7
- Remove vendor tag from desktop file
- spec clean up

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.17.4-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Karsten Hopp <karsten@redhat.com> 0.17.4-1
- update icon-cache scriptlets
- update to 0.17.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.17.3-20
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17.3-19
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Karsten Hopp <karsten@redhat.com> 0.17.3-18
- fix multilib problem in /usr/bin/tn5250-config (#343301)

* Wed Dec 05 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-17
- rebuild with new openssl lib

* Mon Aug 27 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-16
- fix license tag
- rebuild

* Wed Aug 01 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-15
- change requires to hicolor-icon-theme for the icons directory
  (#250358)

* Wed Feb 28 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-14
- copy readme instead of moving it
- fix desktop file
- fix scriptlets

* Tue Feb 27 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-13
- drop buildrequirement libtool
- update icon cache on install/uninstall

* Mon Feb 26 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-12
- misc review fixes (#226496)

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-11
- fix permissions
- touch only patched files

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-10
- rename icon files to tn5250.{png,xpm}
- remove Mimetype from desktop file
- move category to desktop file
- use vendor fedora for desktop-file-install
- touch files to avoid autotools run

* Tue Feb 13 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-9
- fix icon name
- fix icon path

* Tue Feb 13 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-8
- merge review changes (#226496):
- move icons into hicolor subdir
- require fedora-logos for the icons directory
- require xterm for xt5250
- -devel subpackage requires automake, openssl-devel, ncurses-devel, pkgconfig
- Requires(post): /usr/bin/tic
- Requires(preun): coreutils
- disable static libs


* Thu Feb 01 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-7
- move tn5250,m4 and lib5250.so to -devel subpackage (#203639)
- move tn5250-config, too
- use macros

* Fri Sep 08 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-5
- fix postinstall script

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-4.1
- rebuild

* Wed Jun 28 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-4
- add buildrequires automake, libtool

* Tue May 23 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-3
- don't check for sizeof(long), the result isn't used anywhere and
  causes problems with multilib installs

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-2
- add buildrequirement openssl-devel (#191875, Andreas Thienemann)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 0.17.3-1
- update

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 0.16.5-7
- rebuilt against new openssl

* Mon Jun 27 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-6
- add buildrequires ncurses-devel (#160985)

* Thu Mar 17 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-5
- rebuild with gcc-4

* Thu Feb 17 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-4
- change Copyright: -> License:

* Tue Jan 25 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-3 
- add BuildRequires ncurses-devel (#137558)

* Tue Aug 03 2004 Karsten Hopp <karsten@redhat.de> 0.16.5-2 
- build for FC3
- add gcc34 patch

* Wed May 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ldconfig calls

* Wed Mar 19 2003 Karsten Hopp <karsten@redhat.de> 0.16.5-1
- update to 0.16.5
- run libtoolize to fix config.sub
- fix _libdir
- fix Group:
- fix URLs
- remove obsolete patch
