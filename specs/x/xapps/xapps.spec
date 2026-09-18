# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xapps
Version:        2.8.8
Release:        6%{?dist}
Summary:        Common files for XApp desktop apps

License:        LGPL-3.0-only
URL:            https://github.com/linuxmint/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        http://packages.linuxmint.com/pool/main/f/flags/flags_1.0.2.tar.xz
Patch0:         watcher_fix_libexec.patch

ExcludeArch:    %{ix86}

BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  libdbusmenu-gtk3-devel
BuildRequires:  libX11-devel
BuildRequires:  libgnomekbd-devel
BuildRequires:  meson
BuildRequires:  python3-gobject-devel
BuildRequires:  python3-devel
BuildRequires:  vala

Requires:       fpaste
%if 0%{?fedora}
Recommends:     inxi
%endif
Requires:       python3-xapps-overrides%{?_isa} = %{version}-%{release}
Requires:       xdg-utils
Requires:       xorg-x11-xinit
Recommends:     switcheroo-control
Obsoletes:      python2-xapps-overrides < %{version}-%{release}

%description
This package includes files that are shared between several XApp
apps (i18n files and configuration schemas).

%package        mate
Summary:        Mate status applet with HIDPI support
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    mate
Mate status applet with HIDPI support

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development libraries and header files for
developing XApp apps.

%package     -n python3-xapps-overrides
Summary:        Python%{python3_version} files for %{name}

Requires:       python3-gobject-base%{?_isa}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       python3-xapps-overrides = %{version}-%{release}
Provides:       python3-xapps-overrides%{?_isa} = %{version}-%{release}

%description -n python3-xapps-overrides
Python%{python3_version} files for XApp apps.

%prep
%autosetup -p1 -n xapp-%{version}

%build
%meson \
 --buildtype=debugoptimized \
 -D deprecated_warnings=false
%meson_build

%install
%meson_install
tar -xf %{SOURCE1} -C %{buildroot}%{_datadir} --strip 3
rm %{buildroot}%{_datadir}/format

%{_bindir}/desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/xapp-sn-watcher.desktop

%find_lang xapp

%ldconfig_scriptlets


%files -f xapp.lang
%license COPYING
%doc README.md
%{_sysconfdir}/xdg/autostart/xapp-sn-watcher.desktop
%{_sysconfdir}/X11/xinit/xinitrc.d/80xapp-gtk3-module.sh
%{_bindir}/pastebin
%{_bindir}/upload-system-info
%{_bindir}/xapp-gpu-offload
%{_bindir}/xfce4-set-wallpaper
%{_libdir}/libxapp.so.*
%{_libdir}/girepository-1.0/XApp-1.0.typelib
%{_libdir}/gtk-3.0/modules/libxapp-gtk3-module.so
%dir %{_libexecdir}/xapps/
%{_libexecdir}/xapps/xapp-sn-watcher
%{_datadir}/dbus-1/services/org.x.StatusNotifierWatcher.service
%{_datadir}/iso-flag-png/
%{_datadir}/glib-2.0/schemas/org.x.apps.*.xml
%{_datadir}/icons/hicolor/scalable/*/*.svg

%files mate
%{_libexecdir}/xapps/*.py
%{_datadir}/dbus-1/services/org.mate.panel.applet.MateXAppStatusAppletFactory.service
%{_datadir}/mate-panel/applets/org.x.MateXAppStatusApplet.mate-panel-applet

%files devel
%{_includedir}/*
%{_libdir}/libxapp.so
%{_libdir}/pkgconfig/xapp.pc
%{_datadir}/gir-1.0/XApp-1.0.gir
%{_datadir}/glade/catalogs/xapp-glade-catalog.xml
%{_datadir}/vala/vapi/xapp.vapi
%{_datadir}/vala/vapi/xapp.deps

%files -n python3-xapps-overrides
%{python3_sitearch}/gi/overrides/XApp.py
%{python3_sitearch}/gi/overrides/__pycache__/XApp.cpython-%{python3_version_nodots}*.py*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.8.8-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.8.8-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.8.8-3
- Rebuilt for Python 3.14

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Leigh Scott <leigh123linux@gmail.com> - 2.8.8-1
- Update to 2.8.8

* Fri Dec 06 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.7-1
- Update to 2.8.7

* Mon Nov 25 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.6-1
- Update to 2.8.6

* Mon Jul 22 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.5-1
- Update to 2.8.5

* Mon Jul 22 2024 Miro Hrončok <mhroncok@redhat.com> - 2.8.4-4
- Ensure python3-xapps-overrides Requires correct python(abi)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.4-2
- Fix build requires

* Tue Jun 18 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.4-1
- Update to 2.8.4

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.8.3-2
- Rebuilt for Python 3.13

* Tue Jun 04 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.3-1
- Update to 2.8.3

* Tue Mar 26 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.2-3
- Fix buildrequires

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Leigh Scott <leigh123linux@gmail.com> - 2.8.2-1
- Update to 2.8.2 release

* Tue Dec 05 2023 Leigh Scott <leigh123linux@gmail.com> - 2.8.1-1
- Update to 2.8.1 release

* Sat Nov 25 2023 Leigh Scott <leigh123linux@gmail.com> - 2.8.0-1
- Update to 2.8.0 release

* Tue Jul 25 2023 Leigh Scott <leigh123linux@gmail.com> - 2.6.1-4
- Fix meld issue

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.6.1-2
- Rebuilt for Python 3.12

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 2.6.1-1
- Update to 2.6.1 release

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 2.6.0-2
- Use recommends switcheroo-control

* Thu Jun 01 2023 Leigh Scott <leigh123linux@gmail.com> - 2.6.0-1
- Update to 2.6.0 release

* Wed Mar 29 2023 Leigh Scott <leigh123linux@gmail.com> - 2.4.3-1
- Update to 2.4.3 release

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 2.4.1-1
- Update to 2.4.1 release

* Sun Jul 24 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.14-1
- Update to 2.2.14 release

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.13-1
- Update to 2.2.13 release

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.2.10-2
- Rebuilt for Python 3.11

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.10-1
- Update to 2.2.10 release

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 01 2022 Leigh Scott <leigh123linux@gmail.com> - 2.2.8-1
- Update to 2.2.8 release

* Mon Dec 06 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.6-1
- Update to 2.2.6 release

* Wed Nov 24 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.5-1
- Update to 2.2.5 release

* Thu Nov 04 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.4-1
- Update to 2.2.4 release

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.2-1
- Update to 2.2.2 release

* Thu Jun 10 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.1-1
- Update to 2.2.1 release

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-2
- Rebuilt for Python 3.10

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 2.2.0-1
- Update to 2.2.0 release

* Mon Apr 26 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.7-1
- Update to 2.0.7 release

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.6-1
- Update to 2.0.6 release

* Sat Jan  2 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.5-1
- Update to 2.0.5 release

* Sun Dec 13 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.4-1
- Update to 2.0.4 release

* Thu Dec 10 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.3-1
- Update to 2.0.3 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.1-2
- Add patch to fix perms

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.1-1
- Update to 2.0.1 release

* Wed Nov 25 2020 Leigh Scott <leigh123linux@gmail.com> - 2.0.0-1
- Update to 2.0.0 release

* Wed Sep  9 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.10-1
- Update to 1.8.10 release

* Sat Aug 15 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.9-1
- Update to 1.8.9 release

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.8-1
- Update to 1.8.8 release

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.7-1
- Update to 1.8.7 release

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.6-2
- Rebuilt for Python 3.9

* Sat May 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.6-1
- Update to 1.8.6 release

* Thu May 21 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.5-1
- Update to 1.8.5 release

* Wed May 13 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.4-2
- Fix sn-watcher issue

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.4-1
- Update to 1.8.4 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.6.10-1
- Update to 1.6.10 release

* Thu Jan 09 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.6.9-1
- Update to 1.6.9 release

* Wed Dec 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.8-1
- Update to 1.6.8 release

* Tue Dec 10 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.7-1
- Update to 1.6.7 release

* Sat Dec 07 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.6-1
- Update to 1.6.6 release

* Fri Nov 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.5-1
- Update to 1.6.5 release

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.4-1
- Update to 1.6.4 release

* Tue Nov 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.3-1
- Update to 1.6.3 release

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.2-1
- Update to 1.6.2 release

* Tue Nov 19 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.1-2
- Add Mate status applet

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.1-1
- Update to 1.6.1 release

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.9-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.9-1
- Update to 1.4.9 release

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.8-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.8-1
- Update to 1.4.8 release

* Sun Jun 23 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.7-1
- Update to 1.4.7 release

* Fri Jun 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.6-1
- Update to 1.4.6 release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.5-1
- Update to 1.4.5 release

* Tue Nov 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.4-1
- Update to 1.4.4 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.2-1
- Update to 1.4.2 release

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-1
- Update to 1.4.1 release

* Mon Nov 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- Add Obsoletes python2-xapps-overrides to main package

* Tue Oct 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Update to 1.4.0 release

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.2-2
- Drop EPEL/RHEL support
- Drop python2 support

* Wed Aug 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.2-1
- Update to 1.2.2 release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-3
- Rebuilt for Python 3.7

* Sun Jun 10 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.1-2
- Fix rhbz#1589423

* Sun May 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.1-1
- Update to 1.2.1 release

* Mon Apr 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.0-1
- Update to 1.2.0 release

* Mon Apr 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-0.2.20180311gite5ca157
- Update to latest git

* Fri Mar 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-0.1.20180309gitfea3ca8
- Fix version

* Fri Mar 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-0.3.20180309gitfea3ca8
- Update to latest git

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-0.2.20180203git83d0f77
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-0.1.20180203git83d0f77
- Update to latest git

* Sat Nov 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-13
- Add a base preferences dialog

* Mon Nov 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-12
- Fix Requires for F26

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-11
- Fix Requires for EPEL7

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-10
- Fix globbing of __pycache__

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-9
- Fix Python3 macro again

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-8
- Fix archful Requires

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-7
- Fix Python3 macro

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-6
- Fix build

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.4-5
- Adaptions for EPEL7

* Mon Nov 13 2017 Troy Curtis, Jr <troycurtisjr@gmail.com> - 1.0.4-4
- Have python2-xapps-overrides require xapps instead of the other way around.
- Use python macros

* Sat Nov 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-3
- Add requires python2-gobject-base

* Thu Oct 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-2
- build python XApp overrides

* Tue Oct 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-1
- update to 1.0.4 release

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.3-6
- Preserve mode of files when changing hashbang

* Tue Aug 29 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.3-5
- Use Python2 on epel

* Mon Aug 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-4
- Fix requires for epel

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 03 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-1
- update to 1.0.3 release
- add build requires gtk-doc

* Thu Feb 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-5
- Add python3-gobject-base instead of python-gobject-base

* Thu Feb 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-4
- Add some upstream fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-2
- Rebuild for Python 3.6

* Mon Nov 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-1
- update to 1.0.2 release

* Sat Nov 05 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.3.gita8d5277
- update to latest git

* Tue Oct 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.2.git0f28d18
- fix review issues

* Sat Oct 08 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.1.git7e7567a
- first build
