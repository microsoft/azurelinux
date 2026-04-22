# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		openbox
Version:	3.6.1
Release: 30%{?dist}
Summary:	A highly configurable and standards-compliant X11 window manager

License:	GPL-2.0-or-later
URL:		http://openbox.org
Source0:	http://openbox.org/dist/%{name}/%{name}-%{version}.tar.xz
Source1:	http://icculus.org/openbox/tools/setlayout.c
Source2:	xdg-menu
Source3:	menu.xml
Source4:	terminals.menu
Patch1:		openbox-python3.patch
Patch2:		openbox-kf5menu.patch
Patch3:		openbox-calc-layer.patch

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# required by xdg-menu and xdg-autostart scripts
Requires:	python3-pyxdg
# used by xdg-menu for icon support (optional)
Suggests:	python3-gobject
# as discussed in https://bugzilla.redhat.com/860997
Requires:	redhat-menus

BuildRequires: make
BuildRequires:	gcc
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	pango-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXt-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXinerama-devel
BuildRequires:	imlib2-devel
# workaround for yum to install correct libpng-devel
BuildRequires:	libpng-devel
Provides:	firstboot(windowmanager)

# gdm-control, gnome-control-center and openbox-gnome were removed in 3.5.2-5
Obsoletes:	gdm-control < 3.5.2-5
Obsoletes:	gnome-panel-control < 3.5.2-5
Obsoletes:	%{name}-gnome < 3.5.2-5

%description
Openbox is a window manager designed explicity for standards-compliance and
speed. It is fast, lightweight, and heavily configurable (using XML for its
configuration data). It has many features that make it unique among window
managers: window resistance, chainable key bindings, customizable mouse
actions, multi-head/Xinerama support, and dynamically generated "pipe menus."

For a full list of the FreeDesktop.org standards with which it is compliant,
please see the COMPLIANCE file in the included documentation of this package. 
For a graphical configuration editor, you'll need to install the obconf
package.


%package	devel
Summary:	Development files for %{name}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	pango-devel
Requires:	libxml2-devel
Requires:	glib2-devel

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package	libs
Summary:	Shared libraries for %{name}

%description	libs
The %{name}-libs package contains shared libraries used by %{name}.


%package	kde
Summary:	KDE integration for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	plasma-workspace
BuildArch:	noarch

%description	kde
The %{name}-kde package contains the files needed for using %{name} inside a
KDE session.


%prep
%setup -q
%patch -P1 -p1 -b .python3
%patch -P2 -p1 -b .kf5menu
%patch -P3 -p1 -b .calc-layer


%build
%configure \
	--disable-static
## Fix RPATH hardcoding.
sed -ie 's|^hardcode_libdir_flag_spec=.*$|hardcode_libdir_flag_spec=""|g' libtool
sed -ie 's|^runpath_var=LD_RUN_PATH$|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS -o setlayout %{SOURCE1} -lX11

%install
%make_install

install setlayout %{buildroot}%{_bindir}
install -p %{SOURCE2} %{buildroot}%{_libexecdir}/openbox-xdg-menu
sed 's|_LIBEXECDIR_|%{_libexecdir}|g' < %{SOURCE3} \
	> %{buildroot}%{_sysconfdir}/xdg/%{name}/menu.xml

install -m644 -p %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/%{name}/terminals.menu

# 'make install' misses these two, so we install them manually
install -m644 -D data/gnome-session/openbox-gnome.session \
	%{buildroot}%{_datadir}/gnome-session/sessions/openbox-gnome.session
install -m644 -D data/gnome-session/openbox-gnome-fallback.session \
	%{buildroot}%{_datadir}/gnome-session/sessions/openbox-gnome-fallback.session

# remove unpackaged files
pushd %{buildroot}
rm ./%{_bindir}/{gdm-control,gnome-panel-control,%{name}-gnome-session}
rm ./%{_datadir}/xsessions/%{name}-gnome.desktop
rm ./%{_datadir}/gnome/wm-properties/openbox.desktop
rm ./%{_datadir}/gnome-session/sessions/openbox-gnome*.session
rm ./%{_mandir}/man1/%{name}-gnome-session*.1*
popd


%find_lang %{name}
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_datadir}/doc/%{name}


%files -f %{name}.lang
%doc AUTHORS CHANGELOG COMPLIANCE COPYING README
%doc data/*.xsd data/menu.xml doc/rc-mouse-focus.xml
%dir %{_sysconfdir}/xdg/%{name}/
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_bindir}/%{name}
%{_bindir}/%{name}-session
%{_bindir}/obxprop
%{_bindir}/setlayout
%{_libexecdir}/openbox-*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/themes/*/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-session.1*
%{_mandir}/man1/obxprop.1*

%files	libs
%doc COPYING
%{_libdir}/libobrender.so.*
%{_libdir}/libobt.so.*

%files	devel
%{_includedir}/%{name}/
%{_libdir}/libobrender.so
%{_libdir}/libobt.so
%{_libdir}/pkgconfig/*.pc

%files  kde
%{_bindir}/%{name}-kde-session
%{_datadir}/xsessions/%{name}-kde.desktop
%{_mandir}/man1/%{name}-kde-session*.1*

%ldconfig_scriptlets libs

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Leigh Scott <leigh123linux@gmail.com> - 3.6.1-23
- Rebuild fo new imlib2

* Thu Apr 27 2023 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-22
- fix crash with new glib (#2178299)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 09 2020 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-16
- update XDG menu prefix in KDE session script (#1851755)
- drop obsolete KDE4 requirement

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 09 2019 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-13
- remove obmenu from description

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-9
- fix pyxdg requirement

* Tue Apr 17 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-8
- switch packaged python scripts to python3

* Mon Feb 26 2018 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-7
- build setlayout with hardening LDFLAGS (#1548830)
- use macro for ldconfig scriptlets
- add gcc to build requirements

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 02 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.6.1-1
- update to 3.6.1

* Thu Jun 25 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.6-3
- restore libobrender compatibility (#1231693)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Miroslav Lichvar <mlichvar@redhat.com> - 3.6-1
- update to 3.6

* Thu Mar 05 2015 Rex Dieter <rdieter@fedoraproject.org> 3.5.2-7
- -kde: fix deps for plasma5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.2-5
- drop gnome subpackages (#964977)
- fix typo in description (#1064959)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Christoph Wickert <cwickert@fedoraproject.org> - 3.5.2-3
- gdm-control depends on gdm, not on gnome-panel (#964977)

* Thu Aug 15 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.2-2
- Add workaround for yum to install correct libpng-devel in build

* Tue Aug 13 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-12.20121001git782b28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-11.20121001git782b28
- Update to git snapshot 20121001git782b28
- Update xdg-menu to work with latest gtk3 (#914830)
- Make some dependencies arch-specific
- Make gnome and kde subpackages noarch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-9
- Update xdg-menu to work with latest pyxdg (#874633)
- Remove unnecessary macros

* Fri Sep 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 3.5.0-8
- Require redhat-menus (#860997)
- Use upstream's gnome-session 3 fixes instead of ours

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 3.5.0-6
- Fix crash on unexpected NET_WM_MOVERESIZE_CANCEL messages (#827800)
- Make sub-packages for gdm-control and gnome-panel-control (#750056)

* Fri Mar 30 2012 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-5
- increase doubleclick timeout (#727995)
- fix another crash in xdg-menu (#799663)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-3
- fix xdg-menu to not crash without icon file (#737112)

* Fri Sep 30 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-2
- build with imlib support
- fix xdg-menu to handle -caption in desktop files (#678827)
- update xdg-menu to use pyxdg and gtk via introspection (#737112)

* Fri Aug 05 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.5.0-1
- update to 3.5.0
- don't own gnome directories (#718042)

* Fri May 06 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.2-8
- update gnome-session support (#702460)
- make subpackages for gnome and kde session files (#520245)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.11.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.2-6
- add support for new gnome-session (#669391)

* Wed Sep 29 2010 jkeating - 3.4.11.2-5
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 3.4.11.2-4
- Provide firstboot(windowmanager)
- Remove obsolete Encoding key from openbox.desktop

* Tue Sep 07 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.2-3
- generate terminals menu (#622426)
- remove double quotes from menu labels (#630109)

* Mon Jul 12 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.2-2
- add COPYING to libs subpackage

* Mon May 17 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.2-1
- update to 3.4.11.2
- require pyxdg (#590322)

* Fri Apr 16 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11.1-1
- update to 3.4.11.1

* Tue Feb 09 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.11-1
- update to 3.4.11
- fix linking with --no-add-needed

* Thu Jan 21 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.10-3
- fix gnome-session script again (#552760)

* Mon Jan 18 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.10-2
- fix crash when window is added to focus order while focus cycling
- fix gnome-session script

* Fri Jan 08 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.10-1
- Update to 3.4.10

* Mon Jan 04 2010 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.9-2
- Rename obprop to obxprop to avoid conflict with openbabel (#549152)

* Sat Dec 19 2009 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.9-1
- Update to 3.4.9

* Thu Dec 10 2009 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.8-1
- Update to 3.4.8
- Fix crash in xdg-autostart on desktop files with TryExec (#544006)

* Tue Sep 22 2009 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-11
- Add support for 24-bit images (#524708)
- Update setlayout.c

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.7.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Luke Macken <lmacken@redhat.com> - 3.4.7.2-8
- Require the gnome-menus package to get our xdg-menu dynamic pipe menu
  to work out of the box.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 09 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-7
- Restore gnome session script (#474143)
- Use DESKTOP_AUTOSTART_ID to avoid gnome-session registration timeout

* Thu Oct 02 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-6
- Drop gnome session script (gnome-session no longer supports $WINDOW_MANAGER)
- Add application desktop file to allow starting openbox in gnome-session
  when configured in gconf

* Thu Sep 04 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-5
- Don't use --choose-session option in gnome session script

* Fri Aug 01 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-4
- Remove field codes from commands in xdg-menu (#452403)
- Add support for launching applications in xterm to xdg-menu

* Tue Jun 10 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-3
- Clean up properties after gdm in session scripts (#444135)
- Add license to xdg-menu script

* Tue May 20 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-2
- Drop numdesks patch (#444135)

* Wed May 14 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.2-1
- Update to 3.4.7.2
- Use gnome menus by default (Luke Macken) (#443548)
- Force setting number of desktops (#444135)

* Thu Apr 17 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.7.1-1
- Update to 3.4.7.1
- Don't require /usr/share/themes

* Wed Feb 06 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.6.1-1
- Update to 3.4.6.1

* Sun Feb 03 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.6-1
- Update to 3.4.6

* Mon Jan 07 2008 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.5-1
- Update to 3.4.5

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.4-2
- Rebuild

* Sun Aug 05 2007 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.4-1
- Update to 3.4.4
- Update license tag

* Mon Jul 23 2007 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.3-1
- Update to 3.4.3
- Package setlayout tool

* Wed Jun 13 2007 Miroslav Lichvar <mlichvar@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Mon Jun 04 2007 Peter Gordon <peter@thecodergeek.com> - 3.3.1-7
- Own %%{_datadir}/gnome/wm-properties instead of depending on gnome-session
  in order to reduce dependency bloat. (Resolves bug 242339; thanks to Miroslav
  Lichvar for the bug report.) 

* Tue Mar 27 2007 Peter Gordon <peter@thecodergeek.com> - 3.3.1-6
- Split shared libraries into a -libs subpackage to properly handle multilib
  setups. (This precludes the further need to %%ghost the byte-compiled
  themeupdate scripts which was introduced in the previous release.)
- Fix handling of the startup_notification build conditional. It will actually
  work properly now. :)
- Remove the hardcoded RPATH using some sed invocations from the packaging
  guidelines. 

* Mon Feb 12 2007 Peter Gordon <peter@thecodergeek.com> - 3.3.1-5
- %%ghost the byte-compiled themeupdate scripts to fix multilib conflict
  (bug #228379).

* Thu Nov 23 2006 Peter Gordon <peter@thecodergeek.com> - 3.3.1-4
- Don't own %%{_datadir}/gnome/wm-properties anymore, as that's now owned
  by gnome-session in Rawhide and we should not have ownership conflicts with
  Core packages.

* Mon Oct 02 2006 Peter Gordon <peter@thecodergeek.com> - 3.3.1-3
- Rebuild to pick up unwind info generation fixes in new GCC

* Wed Sep 20 2006 Peter Gordon <peter@thecodergeek.com> - 3.3.1-2
- Allow building with startup-notification as an rpmbuild option (though it is
  disabled by default as recommended by upstream).

* Sat Sep 09 2006 Peter Gordon <peter@thecodergeek.com> - 3.3.1-1
- Update to new 3.3.1 from upstream

* Sun Aug 27 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-3
- Mass FC6 rebuild

* Sat Aug 26 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-2
- Bump release to fix sources tagging issue

* Sat Aug 26 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-1
- Update to 3.3 final release from upstream
- Remove the slew of versioning macros, as it's overkill for this and just adds
  unneeded complexity to the spec.

* Wed Jun 28 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.8.rc2.1
- Add missing BuildRequires: libXxf86vm-devel

* Wed Jun 28 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.8.rc2
- Unconditionalize the BuildRequires for modular X.org, since it's branched
  for a specific Fedora release. 

* Mon Jun 26 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.7.rc2
- Own the %%{_datadir}/gnome/wm-properties directory (#195292)

* Fri Jun 23 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.6.rc2
- Add %%{_datadir}/themes to Requires (#195292)

* Tue Jun 20 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.5.rc2
- Own all created theme directories (#195292)
- Fix previous review bug IDs in this %%changelog to point to the recreated
  review bug (due to recent bugzilla outage) 

* Sun Jun 18 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.4.rc2
- Don't default to an executable xsession script (#195292)

* Mon Jun 12 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.3.rc2 
- Fix versioning to conform to the Extras packaging guidelines

* Mon Jun 12 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.rc2.2 
- Add %%{_datadir}/xsessions .desktop file for easy selection of Openbox at
  login screen (#195292)

* Fri Jun 09 2006 Peter Gordon <peter@thecodergeek.com> - 3.3-0.rc2.1 
- Unorphan, rewriting nearly all of the spec file
- Update to upstream 3.3 RC2

* Sun Jul 27 2003 Chris Ricker <kaboom@gatech.edu> 0:2.3.1-0.fdr.5
- Need to own /etc/X11/gdm/Sessions && /etc/X11/gdm (#440)
- Need to conflict with fluxbox (#422 / #440)

* Tue Jul 22 2003 Chris Ricker <kaboom@gatech.edu> 0:2.3.1-0.fdr.4
- Need to own /usr/share/apps/switchdesk (#422)

* Mon Jul 21 2003 Chris Ricker <kaboom@gatech.edu> 0:2.3.1-0.fdr.3
- More spec revisions (#422); change make and preserve timestamps

* Sun Jul 20 2003 Chris Ricker <kaboom@gatech.edu> 0:2.3.1-0.fdr.2
- Minor spec revisions (#422); add epoch and versions to changelogs

* Sun Jul 06 2003 Chris Ricker <kaboom@gatech.edu> 0:2.3.1-0.fdr.1
- Add switchdesk support
- Add display manager support
- Fix NLS build on Cambridge
- Fedora'ize the spec

* Sun Jun 29 2003 Chris Ricker <kaboom@gatech.edu>
- Rev to 2.3.1 release
- Make go with GCC 3.3

* Tue Mar 18 2003 Chris Ricker <kaboom@gatech.edu>
- Package of 2.3.0 release
