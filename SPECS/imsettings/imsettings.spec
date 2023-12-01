%define with_desktop_subpackages 0
Summary:        Delivery framework for general Input Method configuration
Name:           imsettings
Version:        1.8.2
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://tagoh.bitbucket.org/%{name}/
Source0:        https://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2
## Fedora specific: run IM for certain languages only
Patch0:         %{name}-constraint-of-language.patch
## Fedora specific: Disable XIM support
Patch1:         %{name}-disable-xim.patch
## Fedora specific: Enable xcompose for certain languages
Patch2:         %{name}-xinput-xcompose.patch
## Fedora specific: Force enable the IM management on imsettings for Cinnamon
Patch3:         %{name}-force-enable-for-cinnamon.patch
Patch4:         %{name}-gcc10.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  glib2 >= 2.32.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel >= 3.3.3
BuildRequires:  libX11-devel
BuildRequires:  libgxim-devel >= 0.5.0
BuildRequires:  libnotify-devel
BuildRequires:  libtool
Requires:       %{name}-desktop-module = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       /bin/bash
Requires:       xorg-x11-xinit >= 1.0.2
Requires(post): %{_sbindir}/alternatives
Requires(post): systemd
Requires(postun): %{_sbindir}/alternatives
Requires(postun): systemd
%if %{with_desktop_subpackages}
BuildRequires:  xfconf-devel
%endif

%description
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the core DBus services and some utilities.

%package        libs
Summary:        Libraries for imsettings

%description	libs
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the shared library for imsettings.

%package        devel
Summary:        Development files for imsettings
Requires:       %{name}-libs = %{version}-%{release}
Requires:       glib2-devel >= 2.32.0
Requires:       pkg-config

%description	devel
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains the development files to make any
applications with imsettings.

%package        xim
Summary:        XIM support on imsettings
Requires:       %{name} = %{version}-%{release}
Requires:       im-chooser

%description	xim
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working with XIM.

%package        gsettings
Summary:        GSettings support on imsettings
Requires:       %{name} = %{version}-%{release}
Requires:       dconf
Provides:       imsettings-desktop-module = %{version}-%{release}
Provides:       %{name}-gnome = %{version}-%{release}

%description	gsettings
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on
GNOME and Cinnamon which requires GSettings in their
own XSETTINGS daemons.

%package        qt
Summary:        Qt support on imsettings
Requires:       %{name} = %{version}-%{release}
Requires:       im-chooser
Provides:       imsettings-desktop-module = %{version}-%{release}

%description	qt
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on Qt
applications.

%if %{with_desktop_subpackages}
%package        xfce
Summary:        Xfce support on imsettings
Requires:       %{name} = %{version}-%{release}
Requires:       im-chooser-xfce
Requires:       xfce4-settings >= 4.5.99.1-2
Provides:       imsettings-desktop-module = %{version}-%{release}

%description	xfce
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on Xfce.

%package        lxde
Summary:        LXDE support on imsettings
Requires:       %{_bindir}/lxsession
Requires:       %{name} = %{version}-%{release}
Requires:       im-chooser
Requires:       lxde-settings-daemon
# Hack for upgrades: see https://bugzilla.redhat.com/show_bug.cgi?id=693809
Requires:       lxsession
Provides:       imsettings-desktop-module = %{version}-%{release}

%description	lxde
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on LXDE.

%package        mate
Summary:        MATE support on imsettings
Requires:       %{name} = %{version}-%{release}
Requires:       im-chooser
Requires:       mate-session-manager
# need to keep more deps for similar reason to https://bugzilla.redhat.com/show_bug.cgi?id=693809
Requires:       mate-settings-daemon >= 1.5.0
Provides:       imsettings-desktop-module = %{version}-%{release}

%description	mate
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on MATE.

%package        cinnamon
Summary:        Cinnamon support on imsettings
Requires:       %{name} = %{version}-%{release}
# need to keep more deps for similar reason to https://bugzilla.redhat.com/show_bug.cgi?id=693809
Requires:       cinnamon
Requires:       cinnamon-session
Requires:       im-chooser
Provides:       imsettings-desktop-module = %{version}-%{release}

%description	cinnamon
IMSettings is a framework that delivers Input Method
settings and applies the changes so they take effect
immediately without any need to restart applications
or the desktop.

This package contains a module to get this working on Cinnamon.
%endif

%prep
%autosetup -p1

%build
autoreconf -f
%configure	\
	--with-xinputsh=50-xinput.sh \
	--disable-static \
	--disable-schemas-install
%make_build

%install
%make_install

# change the file attributes
chmod 0755 %{buildroot}%{_libexecdir}/imsettings-target-checker.sh
chmod 0755 %{buildroot}%{_libexecdir}/xinputinfo.sh
chmod 0755 %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/50-xinput.sh

# clean up the unnecessary files
find %{buildroot} -type f -name "*.la" -delete -print
rm -f %{buildroot}%{_libdir}/imsettings/libimsettings-{gconf,mateconf}.so
%if ! %{with_desktop_subpackages}
rm -f %{buildroot}%{_libdir}/imsettings/libimsettings-{lxde,xfce,mate-gsettings,cinnamon-gsettings}.so
%endif

desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/imsettings-start.desktop

%find_lang %{name}


#%%check
## Disable it because it requires DBus session
# make check

%post
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/none.conf 10
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xcompose.conf 20
alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xim.conf 30
systemctl reload dbus.service 2>&1 || :

%postun
if [ "$1" = 0 ]; then
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/none.conf
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xcompose.conf
	alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/xim.conf
	systemctl reload dbus.service 2>&1 || :
fi

%ldconfig_scriptlets	libs

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%dir %{_libdir}/imsettings
%{_bindir}/imsettings-info
%{_bindir}/imsettings-list
%{_bindir}/imsettings-reload
%{_bindir}/imsettings-switch
%{_libexecdir}/imsettings-check
%{_libexecdir}/imsettings-daemon
%{_libexecdir}/xinputinfo.sh
%{_libexecdir}/imsettings-functions
%{_libexecdir}/imsettings-target-checker.sh
%{_datadir}/dbus-1/services/*.service
%{_datadir}/pixmaps/*.png
%{_sysconfdir}/X11/xinit/xinitrc.d/50-xinput.sh
%{_sysconfdir}/X11/xinit/xinput.d
%{_sysconfdir}/xdg/autostart/imsettings-start.desktop
%{_mandir}/man1/imsettings-*.1*

%files libs
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libimsettings.so.5*

%files devel
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_includedir}/imsettings
%{_libdir}/libimsettings.so
%{_libdir}/pkgconfig/imsettings.pc
%{_libdir}/girepository-*/IMSettings-*.typelib
%{_datadir}/gir-*/IMSettings-*.gir
%{_datadir}/gtk-doc/html/imsettings

%files xim
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/imsettings-xim
%{_libdir}/imsettings/libimsettings-xim.so

%files gsettings
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-gsettings.so

%files qt
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-qt.so

%if %{with_desktop_subpackages}
%files xfce
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-xfce.so

%files lxde
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-lxde.so

%files mate
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-mate-gsettings.so

%files cinnamon
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/imsettings/libimsettings-cinnamon-gsettings.so
%endif


%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.8.2-3
- License verified
- Lint spec

* Tue Jun 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.8.2-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Disable desktop environment-based subpackages

* Wed Jan 29 2020 Akira TAGOH <tagoh@redhat.com> - 1.8.2-2
- Fix the build issue.

* Tue Dec 24 2019 Akira TAGOH <tagoh@redhat.com> - 1.8.2-1
- New upstream release.
- Fix a segfault on XFCE. (#1697211)
- Call bash directly instead of sh (#1771526)

* Sat Oct 12 2019 Gris Ge <fge@redhat.com> - 1.8.1-3
- Fix build on RHEL/CentOS 8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 Akira TAGOH <tagoh@redhat.com> - 1.8.1-1
- New upstream release.

* Thu Feb 21 2019 Akira TAGOH <tagoh@redhat.com> - 1.8.0-3
- Don't set environment variables on GNOME. (#1673288)

* Mon Feb 18 2019 Akira TAGOH <tagoh@redhat.com> - 1.8.0-1
- New upstream release.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Adam Williamson <awilliam@redhat.com> - 1.7.3-6
- Rebuild for new libxfconf

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Akira TAGOH <tagoh@redhat.com> - 1.7.3-4
- Use ldconfig rpm macro.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Akira TAGOH <tagoh@redhat.com> - 1.7.3-2
- Fix the unbound variable issue in xinput.sh (#1533079)

* Thu Dec  7 2017 Akira TAGOH <tagoh@redhat.com> - 1.7.3-1
- New upstream release.
- Fix the GNOME detection. (#1520396)

* Sat Sep 23 2017 Akira TAGOH <tagoh@redhat.com> - 1.7.2-5
- Reload dbus.service instead of calling through dbus-send.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 13 2016 Akira TAGOH <tagoh@redhat.com> - 1.7.2-1
- New upstream release.

* Tue Jun  7 2016 Akira TAGOH <tagoh@redhat.com> - 1.7.1-1
- New upstream release.
- Fix the desktop-specific issue with IBus (#1330089)

* Mon Feb 22 2016 Akira TAGOH <tagoh@redhat.com> - 1.7.0-1
- Fix the desktop detection. (#1310063)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Akira TAGOH <tagoh@redhat.com> - 1.6.8-5
- Fix the fail on configure.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.6.8-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 21 2015 Akira TAGOH <tagoh@redhat.com> - 1.6.8-3
- rebuild

* Thu Jan 15 2015 Akira TAGOH <tagoh@redhat.com> - 1.6.8-1
- New upstream release.
- Fix a glib assertion. (#1181765)

* Thu Dec 04 2014 David King <amigadave@amigadave.com> - 1.6.7-7
- Update dbus-send dependency for new dbus (#1170586)

* Thu Nov  6 2014 Akira TAGOH <tagoh@redhat.com> - 1.6.7-6
- Add Suggests: imsettings-gsettings to address the dependency issue with dnf. (#1151550)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.7-4
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Akira TAGOH <tagoh@redhat.com> - 1.6.7-2
- Remove possibly unnecessary unpackaged files at the build time. (#1075690)

* Tue Nov 26 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.7-1
- New upstream release.

* Thu Oct 10 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.6-1
- New upstream release.
- Enable imsettings forcibly for Cinnamon so far.

* Thu Oct 10 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.5-1
- New upstream release.
- Add a module to support the latest Cinnamon Desktop. (#1017141)

* Mon Sep 30 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.4-1
- New upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.3-1
- New upstream release.
- Remove BR: docbook2X.

* Mon May 27 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.2-1
- New upstream release.

* Mon Apr  8 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.1-2
- Have a look gsettings on gnome-classic too.

* Wed Apr  3 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.1-1
- New upstream release.
- Support gnome-classic session. (#947394)

* Tue Mar 12 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.0-3
- Run input methods on even non-GNOME desktops. (#920188)

* Tue Feb 12 2013 Kalev Lember <kalevlember@gmail.com> - 1.6.0-2
- Correct the imsettings-gnome obsoletes version

* Fri Feb  8 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.0-1
- New upstream release.
  - Add Cinnamon support.
- Rename imsettings-gnome to imsettings-gsettings

* Thu Dec 20 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.1-2
- Fix dep errors.

* Wed Dec 19 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.1-1
- New upstream release.
  - Get rid of AutostartCondition. (#887951)
- Update upstream URL.

* Fri Nov 23 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.0-2
- Rebuilt against the latest version of libgxim.

* Thu Nov 22 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.0-1
- New upstream release.
  - MATE 1.5 support

* Mon Oct 22 2012 Akira TAGOH <tagoh@redhat.com> - 1.4.0-2
- No autostart on gnome-shell. (#868458)

* Wed Oct 17 2012 Akira TAGOH <tagoh@redhat.com> - 1.4.0-1
- New upstream release.
  - Add MATE Desktop support. (#866328)

* Tue Aug 28 2012 Akira TAGOH <tagoh@redhat.com> - 1.3.1-1
- New upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Akira TAGOH <tagoh@redhat.com> - 1.3.0-1
- New upstream release.
- Drop imsettings-*-disable-fallbackim.patch.

* Mon Apr 23 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.9-1
- New upstream release.
  - fallback to lookup the default configuration on XDG dirs
- Disable fallback immodule feature for XFCE and LXDE so far.

* Mon Mar 19 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.8.1-1
- New upstream release.

* Fri Mar  2 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.8-2
- Update po files.

* Fri Feb 10 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.8-1
- New upstream release.
- would possibly fix crash issues.
  (#772342, #766125, #757443, #740175, #720891)

* Mon Jan 23 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.7.1-1
- New upstream release.

* Thu Jan 19 2012 Akira TAGOH <tagoh@redhat.com> - 1.2.7-1
- New upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.6-1
- New upstream release.

* Tue Oct 11 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.5-3
- Own %%{_libdir}/imsettings. (#744892)

* Tue Oct  4 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.5-2
- Add Requires: dconf to imsettings-gnome to ensure
  it works on KDE. (#742910)

* Fri Sep  9 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.5-1
- New upstream release.

* Wed Jul 13 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.4-1
- New upstream release.
  - Fix taking CPU load after killing IM process. (#718092)

* Tue May 31 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.3-1
- New upstream release.
  - Set some environment variables explicitly to avoid IM
    not working in some cases. (#700513)
  - Fix an abort issue. (#701431)
  - Support the latest LXDE.
  - Get rid of Qt dependency.

* Tue May 10 2011 Bill Nottingham <notting@redhat.com> - 1.2.2-3
- further hacks for imsettings upgrades (#693809)

* Tue May 10 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.2-2
- Revert the dependency of im-chooser (#693809)

* Tue Apr 26 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.2-1
- New upstream release.
  - Fix an issue keeping alive the defunct process.
  - Stop a notification when no backend modules available. (#693809)
  - Better handling of detecting the supported toolkits/desktops.

* Thu Apr 21 2011 Christopher Aillon <caillon@redhat.com> - 1.2.1-2
- Bring in the correct desktop IM module (#693809)

* Wed Mar 30 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.1-1
- New upstream release.

* Mon Feb 14 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.0-1
- New upstream release.
  - Improve a performance. (#676813)
  - Do not update .xinputrc if -n option to imsettings-switch is given.
  - Stop the daemon process with the certain methods.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.0-2
- Get rid of the debugging code to avoid the unnecessary warning.

* Wed Feb  2 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.0-1
- New upstream release.
  - Add GNOME3 support.

* Mon Jan 31 2011 Akira TAGOH <tagoh@redhat.com> - 1.0.1-1
- New upstream release.
  - Fix an abort issue. (#670263)

* Wed Jan  5 2011 Akira TAGOH <tagoh@redhat.com> - 1.0.0-1
- New upstream release.
  - fix a locale handling (#526205)

* Thu Nov  4 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.1-4
- Fix the build fail in the LXDE backend.

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com>
- rebuild against libnotify 0.7.0 (#649063)

* Thu Aug 19 2010 Jens Petersen <petersen@redhat.com>
- add also am_ET, el_GR, and ru_RU to X compose lang list (#623931)

* Tue Aug 10 2010 Jens Petersen <petersen@redhat.com> - 0.108.1-2
- only enable XIM for X locale compose for necessary locales (#623931)
  (so far pt_BR and fi_FI):
- drop imsettings-none.conf-gtk-xim-default.patch
- add imsettings-xinput-xcompose.patch

* Mon Aug  2 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.1-1
- New upstream release.
  - Fix a crash with imsettings-lxde-helper. (#603582)
  - cleanup the unnecessary patches.

* Thu Jun 24 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.0-4
- Fix a segfault. (#599924)

* Tue May 18 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.0-3
- Don't restart the IM process when the exit status is 0.

* Thu Apr 15 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.0-2
- Fix issue the invocation of IM always fails in the internal status. (#582448)
- Add imsettings-lxde subpackage.

* Tue Mar 23 2010 Akira TAGOH <tagoh@redhat.com> - 0.108.0-1
- New upstream release.
- Fix the abort issue. (#570462)
- clean up the unnecessary patches.

* Tue Feb 16 2010 Akira TAGOH <tagoh@redhat.com> - 0.107.4-8
- Fix a segfault issue when /bin/sh points to non-bash shell. (#553680)

* Tue Feb  9 2010 Akira TAGOH <tagoh@redhat.com> - 0.107.4-7
- Add -lX11 to avoid DSO issue.

* Fri Feb  5 2010 Akira TAGOH <tagoh@redhat.com> - 0.107.4-6
- Fix an abort issue on GConf backend. (#543005)

* Mon Jan  4 2010 Akira TAGOH <tagoh@redhat.com> - 0.107.4-5
- Fix an abort issue. (#530357)

* Tue Nov 24 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.4-4
- Fix a segfault issue on XFCE desktop. (#540062)

* Mon Nov  2 2009 Jens Petersen <petersen@redhat.com> - 0.107.4-3
- none.conf: default GTK to xim if available like qt does to fix
  current missing X locale compose for gtk and X (#505100)

* Fri Oct 16 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.4-2
- Run IM for Maithili by default. (#529144)

* Mon Sep 28 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.4-1
- New upstream release.
  - Update the translations.
  - Remove the unnecessary patches:
    - imsettings-unref-notify.patch
    - imsettings-unref-later.patch
    - imsettings-update-info.patch
    - imsettings-close-fd.patch

* Thu Sep 17 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.3-5
- Fix taking too much CPU issue.

* Tue Sep 15 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.3-4
- Update the IM information as needed if the configuration file is written
  in the script. (#523349)

* Fri Sep 11 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.3-3
- Fix keeping IM process running as the defunct process. (#522689)

* Tue Sep  8 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.3-2
- Fix aborting after dbus session closed. (#520976)

* Tue Sep  1 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.3-1
- New upstream release.
  - Fix taking CPU load after switching IM.
  - Fix getting stuck after starting some IM.

* Mon Aug 31 2009 Akira TAGOH <tagoh@redhat.com>
- Add a conditional build to disable xfce module for RHEL.

* Thu Aug 27 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.2-1
- New upstream release.
  - Stop IM process properly with the DBus disconnect signal. (#518970)
  - Update the translation. (#517679)

* Fri Aug 14 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.1-2
- export the certain environment variables.

* Fri Aug 14 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.1-1
- New upstream release.
  - Fix memory leaks.

* Wed Aug 12 2009 Akira TAGOH <tagoh@redhat.com> - 0.107.0-1
- New upstream release.
  - Pop up an error if failed to invoke IM. (#497946)
  - Fix the duplicate recommendation message issue. (#514852)

* Thu Jul 27 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.2-5
- Support immodule only configuration file.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.2-3
- Support immodule only configuration file.

* Mon Apr 13 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.2-2
- Disable applet by default.

* Tue Apr  7 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.2-1
- New upstream release.
  - Fix a freeze issue on X applications with switching IM (#488877)
  - Fix a segfault issue with switching IM (#488899)
  - Fix not creating .xinputrc with disabiling IM first time (#490587)
  - Invoke IM for certain locales. (#493406)

* Wed Mar 18 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.1-2
- Fix XIM-related issues.
- Fix a parser error during reading Compose data. (#484142)
- Get rid of more debugging messages.

* Tue Mar 10 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.1-1
- New upstream release.
  - Fix a double-free issue. (#485595)
  - Workaround to get the accelerator keys working on X apps. (#488713)
  - Get rid of debugging messages (#489119)

* Mon Feb 23 2009 Akira TAGOH <tagoh@redhat.com> - 0.106.0-1
- New upstream release.
  - Fix a parser error for Compose data. (#484142)
  - Allow a lowername or .conf name for IM name. (#471833)
  - Add Xfconf support. (#478669)
- Remove unnecessary autostart files anymore. (#475907)

* Tue Oct 28 2008 Akira TAGOH <tagoh@redhat.com> - 0.105.1-3
- imsettings-fix-registertriggerkeys.patch: Fix to send
  XIM_REGISTER_TRIGGERKEYS anyway. (#468833)

* Mon Oct 27 2008 Akira TAGOH <tagoh@redhat.com> - 0.105.1-2
- imsettings-fix-unpredictable-session-order.patch: Run imsettings-applet with
  --disable-xsettings for GNOME/XFCE. (#466206)

* Thu Oct 23 2008 Akira TAGOH <tagoh@redhat.com> - 0.105.1-1
- New upstream release.
  - Fix another freeze issue. (#452849)
- imsettings-r210.patch: removed.

* Tue Oct 21 2008 Akira TAGOH <tagoh@redhat.com> - 0.105.0-4
- Read %%{_sysconfdir}/X11/xinput.d/none.conf for non-CJKI locales to make
  consistency in the status on im-chooser. so it would /disables/ IM regardless
  of what the kind of locales you use and what the kind of IM you installed.
  NOTE: if you can't input any characters with GTK+ application, you may
  implicitly use the different buiit-in immodule. you can modify none.conf to
  get the right thing then.
- imsettings-r210.patch: backport to allow starting none without warnings.

* Fri Oct 17 2008 Than Ngo <than@redhat.com> 0.105.0-3
- readd the workaround for KDE

* Tue Oct 14 2008 Than Ngo <than@redhat.com> 0.105.0-2
- get rid of workaround for KDE

* Tue Oct 14 2008 Akira TAGOH <tagoh@redhat.com> - 0.105.0-1
- New upstream release.
  - Have a workaround for the race condition issue. (#452849)
  - Fix a freeze issue with ibus. (#465431)
  - Fix a freeze issue on Desktops not supporting XSETTINGS.

* Wed Oct 01 2008 Than Ngo <than@redhat.com> 0.104.1-3
- add workaround for KDE

* Mon Sep 29 2008 Akira TAGOH <tagoh@redhat.com> - 0.104.1-2
- Fix a gconf error in %%pre. (#464453)

* Thu Sep 25 2008 Akira TAGOH <tagoh@redhat.com> - 0.104.1-1
- New upstream release.
  - Fix a segfault issue. (#462899)
  - Suppress the unnecessary notification. (#463797)
  - Add .schemas file missing. real fix of #460703.

* Wed Sep 17 2008 Akira TAGOH <tagoh@redhat.com> - 0.104.0-1
- New upstream release.
  - Fix deadkey issue under XIM. (#457901)
  - Correct .desktop file for imsettings-applet (#460695)
  - Hide a status icon by default. (#460703)

* Fri Aug 29 2008 Akira TAGOH <tagoh@redhat.com> - 0.103.0-1
- New upstream release.
  - im-xsettings-daemon doesn't run automatically. (#459443)
- Enable XIM support again. (#457635)
- BR: libgxim-devel and libnotify-devel

* Tue Jul 29 2008 Akira TAGOH <tagoh@redhat.com> - 0.102.0-1
- New upstream release.
  - Fix no recommendation updated. (#455363)
  - Work on WMs not own/bring up XSETTINGS manager. (#455228)

* Tue Jul  8 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.3-2
- rebuild.

* Thu Jul  3 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.3-1
- New upstream release.
  - Use the system-wide xinputrc if .xinputrc is a dangling
    symlink. (#453358)

* Thu Jun 26 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.2-3
- Disable XIM support so far. (#452849, #452870)

* Wed Jun 18 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.2-2
- Backport patch from upstream to solve issues.
  - always saying IM is running when no .xinputrc.
  - workaround for a delay of that IM is ready for XIM.

* Tue Jun 17 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.2-1
- New upstream release.
  - Fix a typo in the help message. (#451739)
  - Fix a invalid memory access. (#451753)

* Mon Jun 16 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.1-2
- Add Reqruies: glib2-devel, dbus-glib-devel to -devel.

* Thu Jun 12 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.1-1
- New upstream release.
- Add Requires pkgconfig to -devel.

* Wed Jun 11 2008 Akira TAGOH <tagoh@redhat.com> - 0.101.0-1
- New upstream release.
- Add Requires alternatives for %%post and %%postun.
- Improve summary.
- Remove imsettings-reload from %%post and %%postun. these are
  no longer needed.

* Wed Jun  4 2008 Akira TAGOH <tagoh@redhat.com> - 0.100.0-1
- Initial package.
