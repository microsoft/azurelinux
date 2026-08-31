# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           caribou
Version:        0.4.21
Release:        48%{?dist}
Summary:        A simplified in-place on-screen keyboard
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://wiki.gnome.org/Projects/Caribou
Source0:        http://download.gnome.org/sources/caribou/0.4/caribou-%{version}.tar.xz
Patch1:         caribou-0.4.20-fix-python-exec.patch
Patch2:         caribou-0.4.20-multilib.patch
# caribou isn't needed in gnome-shell so don't start there
Patch3:         change_autostart_cinnamon.patch
Patch4:         fix-style-css.patch
Patch5:         Fix-compilation-error.patch
Patch6:         Fix-subkey-popmenu-not-showing-after-being-dismissed.patch
Patch7:         xadapter.vala-Remove-XkbKeyTypesMask-and-f.patch
Patch8:         drop_gir_patch.patch

BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  python3-gobject-devel
BuildRequires:  intltool
BuildRequires:  gnome-doc-utils
BuildRequires:  desktop-file-utils
BuildRequires:  gettext-devel
BuildRequires:  clutter-devel
BuildRequires:  vala
BuildRequires:  libXtst-devel
BuildRequires:  libxklavier-devel
BuildRequires:  libgee-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  at-spi2-core-devel

# Changed in F23 to pull python3-caribou default
Requires:       python3-%{name} = %{version}-%{release}
Requires:       gobject-introspection
Recommends:     caribou-gtk2-module
Requires:       caribou-gtk3-module

#Following is needed as package moved from noarch to arch
Obsoletes:      caribou < 0.4.1-3
# Obsolete retired 'gok' to make sure it gets removed with distro upgrade
Obsoletes:      gok < 2.30.1-6

%description
Caribou is a text entry application that currently manifests itself as
a simplified in-place on-screen keyboard.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Obsolete retired 'gok' to make sure it gets removed with distro upgrade
Obsoletes:      gok-devel < 2.30.1-6

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package     -n python3-caribou
Summary:        Keyboard UI for %{name}
BuildRequires:  python3-devel
BuildRequires:  python3-gobject

Requires:       python3-gobject
Requires:       python3-pyatspi
Requires:       %{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3
BuildArch:      noarch

%description  -n python3-caribou
This package contains caribou python3 GUI

%package        gtk2-module
Summary:        Gtk2 module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk2-module
This package contains caribou module for gtk2 applications.

%package        gtk3-module
Summary:        Gtk3 module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    gtk3-module
This package contains caribou module for gtk3 applications.

%package        antler
Summary:        Keyboard implementation for %{name}
Requires:       python3-%{name} = %{version}-%{release}
Obsoletes:      caribou < 0.4.1-3

%description    antler
This package contains caribou keyboard implementation for
non-gnome-shell sessions.

%prep
%autosetup -p1

gettextize --copy --force
aclocal --install -I m4
autoreconf --verbose --force --install

find -name '*.vala' -exec touch {} \;

%build
%configure --disable-static PYTHON=python3
make clean
%make_build

%install
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'

desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop || :
desktop-file-validate %{buildroot}%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop || :

%find_lang caribou

%ldconfig_scriptlets

%files -f caribou.lang
%doc NEWS README
%license COPYING
%{_bindir}/caribou-preferences
%{_datadir}/caribou
%{_libdir}/girepository-1.0/Caribou-1.0.typelib
%{_sysconfdir}/xdg/autostart/caribou-autostart.desktop
%{_datadir}/dbus-1/services/org.gnome.Caribou.Daemon.service
%{_datadir}/glib-2.0/schemas/org.gnome.caribou.gschema.xml
%{_libdir}/libcaribou.so.0*
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/caribou-gtk-module.desktop
%{_libexecdir}/caribou

%files -n python3-caribou
%{python3_sitelib}/caribou

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/caribou-1.0.pc
%{_datadir}/gir-1.0/Caribou-1.0.gir
%{_datadir}/vala

%files gtk2-module
%{_libdir}/gtk-2.0/modules/libcaribou-gtk-module.so

%files gtk3-module
%{_libdir}/gtk-3.0/modules/libcaribou-gtk-module.so

%files antler
%{_datadir}/antler
%{_datadir}/dbus-1/services/org.gnome.Caribou.Antler.service
%{_libexecdir}/antler-keyboard
%{_datadir}/glib-2.0/schemas/org.gnome.antler.gschema.xml


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.21-48
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.21-47
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.4.21-45
- Rebuilt for Python 3.14

* Fri May 16 2025 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-44
- Fix m4 issue with new gettext

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.4.21-42
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.4.21-40
- Rebuilt for Python 3.13

* Wed Mar 27 2024 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-39
- Fix buildrequires

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-36
- Disable modern c build flags due to vala issue

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Python Maint <python-maint@redhat.com> - 0.4.21-34
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Sep 24 2022 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-32
- Only recommend gtk2-module

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.4.21-30
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.21-27
- Rebuilt for Python 3.10

* Tue Apr 20 2021 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-26
- Fix build (rhbz#1951450)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-24
- Fix last commit

* Wed Jan 13 2021 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-23
- Patch to fix crash

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-21
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-19
- Remove all if defs as the python2 sub-package was removed

* Wed Jan 08 2020 Leigh Scott <leigh123linux@gmail.com> - 0.4.21-18
- Fix style.css issue (rhbz#1789053)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-16
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-13
- Remove python2 subpackage (#1628174)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-11
- Rebuilt for Python 3.7

* Mon May 07 2018 Pete Walter <pwalter@fedoraproject.org> - 0.4.21-10
- Bump release so it's not covered by fedora-obsolete-packages (#1568670)

* Tue May 01 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.4.21-9
- Fix gnome missing schema issue

* Sat Apr 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.4.21-8
- Unretire
- Change autostart as gnome-shell has it's own builtin OSK application

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.21-6
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.21-2
- Rebuild for Python 3.6

* Sun Jul 24 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.4.21-1
- Update to 0.4.21

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.20-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.4.20-2
- Resolves:rh#1324995: caribou-preferences string import error
- Use %%license for COPYING
- move python-caribou to python2-caribou
- Add virtual provides for python packages

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 0.4.20-1
- Update to 0.4.20

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.19-1
- Update to 0.4.19

* Fri Oct 09 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.18.1-3
- Resolves:rh#1228935: gnome-shell: strlen(): gnome-shell killed by SIGSEGV

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.18.1-1
- Update to 0.4.18.1

* Thu Apr 09 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.18-3
- Resolves:rh#1210302: Fix dependencies for python{,3}-caribou

* Thu Apr 02 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.18-2
- Change Cariou to pull python3-caribou default in F23

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.18-1
- Update to 0.4.18

* Fri Feb 20 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.17-2
- Added python3 subpackage

* Tue Feb 17 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.17-1
- Update to 0.4.17

* Tue Nov 25 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.4.16-1
- Update to 0.4.16

* Tue Sep 16 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.4.15-1
- Update to 0.4.15

* Sun Sep 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.14-2
- Fix a possible crash with new dbus activation code (#1138934)

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.14-1
- Update to 0.4.14

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.13-6
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.13-4
- Rebuilt for cogl soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.13-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.13-2
- Rebuilt for cogl soname bump

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 0.4.13-1
- Update to 0.4.13

* Sat Aug 24 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.12-1
- Update to 0.4.12

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 0.4.11-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.11-1
- Update to 0.4.11

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 0.4.10-1
- Update to 0.4.10

* Mon Mar 04 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.9-1
- Update to 0.4.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.4.8-2
- Rebuilt for cogl soname bump

* Tue Feb 19 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.8-1
- Update to 0.4.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.7-2
- vala .vapi and .deps files should be installed by -devel

* Wed Jan 16 2013 Parag Nemade <pnemade AT redhat DOT com> - 0.4.7-1
- Update to 0.4.7

* Thu Dec 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.6-1
- Update to 0.4.6

* Tue Dec 18 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.5-1
- Update to 0.4.5
- Resolves:rh#744852 - Pressing | in on-screen keyboard produces <
- Resolves:rh#880379 - Another service acquired %%s, quitting..
- Resolves:rh#880382

* Wed Nov 21 2012 Parag Nemade <pnemade AT redhat DOT com> - 0.4.4.2-6
- Resolves:rh#878716 - need some spec cleanup

* Thu Nov 15 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-5
- Apply patch1

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-4
- Patch from Rui Matos for exec python in shell shim scripts

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-3
- Fix multilib patch

* Tue Nov 13 2012 Rui Matos <tiagomatos@gmail.com> - 0.4.4.2-2
- Fix dependencies, caribou and antler both need python-caribou

* Tue Nov 13 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.4.2-1
- Update to 0.4.4.2 release

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Wed Jul 25 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.3-3
- Correct the obsoletes

* Tue Jul 24 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.3-2
- Obsolete gok

* Thu Jul 19 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.3-1
- Update to 0.4.3 release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.2-1
- Update to 0.4.2 release

* Tue Feb 07 2012 Parag Nemade <pnemade AT redhat.com> - 0.4.1-5
- Resolves:rh#768033 - Update Requires for caribou

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-3
- split package to subpackages -gtk2-module, -gtk3-module, -antler and python-caribou

* Thu Nov 17 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-2
- Resolves:rh#753149 - Upgraded F15 -> F16 gnome fails - wrong version of caribou

* Tue Oct 18 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.1-1
- upstream release 0.4.1

* Tue Sep 27 2011 Parag Nemade <pnemade AT redhat.com> - 0.4.0-1
- upstream release 0.4.0

* Tue Sep 20 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.92-1
- upstream release 0.3.92

* Tue Sep 06 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.91-1
- Update to new upstream release 0.3.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-2
- Rebuild with pygobject3

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.3-1
- Update to new upstream release 0.3.3

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.3.2-2
- Tweak BuildRequires

* Tue Jun 14 2011 Parag Nemade <pnemade AT redhat.com> - 0.3.2-1
- Update to new upstream release 0.3.2

* Fri May  6 2011 Christopher Aillon <caillon@redhat.com> - 0.2.00-3
- Update scriptlets per packaging guidelines

* Thu May 05 2011 Parag Nemade <pnemade AT redhat.com> - 0.2.00-2
- Caribou now only be shown in GNOME. (rh#698603)
- Add desktop-file-validate for caribou-autostart.desktop
- Add ||: for caribou-autostart.desktop to skip the error.

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.2.00-1
- Update to 0.2.00

* Tue Mar 22 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.92-1
- Update to 0.1.92

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.91-1
- Update to 0.1.91

* Thu Mar 10 2011 Parag Nemade <pnemade AT redhat.com> - 0.1.7-1
- Update to 0.1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-3
- Require pyatspi, not at-spi-python

* Sat May 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-2
- Rewrite spec for autotools

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Wed Jan 21 2009 Ben Konrath <ben@bagu.org> - 0.0.2-1
- Initial release.
