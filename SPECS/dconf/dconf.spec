%define glib2_version 2.44.0
%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        A configuration system
Name:           dconf
Version:        0.36.0
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://wiki.gnome.org/Projects/dconf
Source0:        https://download.gnome.org/sources/dconf/%{majmin}/%{name}-%{version}.tar.xz
Patch1:         dconf-override.patch
BuildRequires:  bash-completion
BuildRequires:  dbus-devel
BuildRequires:  gcc
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  vala
Requires:       dbus
Requires:       glib2 >= %{glib2_version}

%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%package        devel
Summary:        Header files and libraries for dconf development
Requires:       %{name} = %{version}-%{release}

%description devel
dconf development package. Contains files needed for doing software
development using dconf.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_sysconfdir}/dconf/profile

cat << EOF > %{buildroot}%{_sysconfdir}/dconf/profile/user
user-db:user
system-db:local
system-db:site
system-db:distro
EOF

mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d/locks
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/site.d/locks
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/distro.d/locks

%posttrans
dconf update

%files
%license COPYING
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/db/local.d
%dir %{_sysconfdir}/dconf/db/local.d/locks
%dir %{_sysconfdir}/dconf/db/site.d
%dir %{_sysconfdir}/dconf/db/site.d/locks
%dir %{_sysconfdir}/dconf/db/distro.d
%dir %{_sysconfdir}/dconf/db/distro.d/locks
%dir %{_sysconfdir}/dconf/profile
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf.so.1*
%{_datadir}/bash-completion/completions/dconf
%{_mandir}/man1/dconf-service.1.gz
%{_mandir}/man1/dconf.1.gz
%{_mandir}/man7/dconf.7.gz
%config(noreplace) %{_sysconfdir}/dconf/profile/user

%files devel
%{_includedir}/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.36.0-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Dec 08 2021 Thomas Crain <thcrain@microsoft.com> - 0.36.0-3
- License verified (corrected to just LGPLv2+)
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.36.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 10 2020 Kalev Lember <klember@redhat.com> - 0.36.0-1
- Update to 0.36.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Kalev Lember <klember@redhat.com> - 0.35.1-1
- Update to 0.35.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 0.34.0-1
- Update to 0.34.0

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 0.33.2-1
- Update to 0.33.2

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Kalev Lember <klember@redhat.com> - 0.33.1-1
- Update to 0.33.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 0.32.0-1
- Update to 0.32.0

* Fri Mar 08 2019 Kalev Lember <klember@redhat.com> - 0.31.92-1
- Update to 0.31.92

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.31.2-1
- Update to 0.31.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Kalev Lember <klember@redhat.com> - 0.31.1-1
- Update to 0.31.1
- Update project URLs

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 0.30.1-1
- Update to 0.30.1

* Wed Sep 05 2018 Kalev Lember <klember@redhat.com> - 0.30.0-1
- Update to 0.30.0

* Tue Aug 21 2018 Owen Taylor <otaylor@redhat.com> - 0.28.0-3
- Add a patch to enable DCONF_USER_CONFIG_DIR environment variable

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 0.28.0-1
- Update to 0.28.0

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 0.27.1-1
- Update to 0.27.1
- Switch to the meson build system
- Don't set group tags
- Remove obsolete rpm scriptlets
- Fix gtk-doc directory ownership
- Tighten soname glob

* Mon Feb 19 2018 Ray Strode <rstrode@redhat.com> - 0.26.1-3
- Add systemd dbs for distro, site, and machine local dconf databases
  Resolves: #1546644

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 0.26.1-1
- Update to 0.26.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Colin Walters <walters@verbum.org> - 0.26.0-3
- Backport patch to work around gtype threading

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 23 2016 Kalev Lember <klember@redhat.com> - 0.26.0-1
- Update to 0.26.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 0.25.1-1
- Update to 0.25.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.24.0-1
- Update to 0.24.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 0.23.2-1
- Update to 0.23.2

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.23.1-1
- Update to 0.23.1
- This drops the -editor subpackage which now lives in a separate
  dconf-editor SRPM.
- Use the %%license macro for the COPYING file

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.22.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Sep 19 2014 Kalev Lember <kalevlember@gmail.com> - 0.22.0-1
- Update to 0.22.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.21.0-1
- Update to 0.21.0

* Fri Jul 11 2014 Parag <paragn AT fedoraproject DOT org> - 0.20.0-4
- Fix the directory ownership (rh#1056020)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 0.20.0-2
- Specify minimum glib version

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 0.20.0-1
- Update to 0.20.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 0.19.92-1
- Update to 0.19.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 0.19.91-1
- Update to 0.19.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 0.19.90-1
- Update to 0.19.90

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 0.19.3-1
- Update to 0.19.3

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 0.19.2-1
- Update to 0.19.2

* Thu Sep 26 2013 Kalev Lember <kalevlember@gmail.com> - 0.18.0-2
- Add missing glib-compile-schemas scriptlets to the -editor subpackage

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 0.18.0-1
- Update to 0.18.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.17.1-1
- Update to 0.17.1

* Mon Aug 05 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 0.17.0-3
- Fix bogus date in changelog

- Compilation should be more verbose, add V=1
- Upstream does not install dconf-editor ui files

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 0.17.0-1
- Update to 0.17.0

* Sat Jun  8 2013 Matthias Clasen <mclasen@redhat.com> - 0.16.0-2
- Move the editor schema to the right subpackage

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Mon Feb 11 2013 Kalev Lember <kalevlember@gmail.com> - 0.15.3-1
- Update to 0.15.3
- Install the HighContrast icons and update the icon cache scriptlets to take
  this into account

* Sat Dec 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.15.2-2
- -devel: drop Requires: glib2-devel, already gets pulled in via pkgconfig deps
- -editor: add icon scriptlets
- tighten subpkg deps via %%{_isa}

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 0.15.2-1
- Update to 0.15.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 0.15.0-3
- Move some of the rpm scriptlets back to %%posttrans
  (glib-compile-schemas, icon cache)

* Thu Nov  8 2012 Marek Kasik <mkasik@redhat.com> - 0.15.0-2
- Move dconf-editor's man page to the dconf-editor sub-package

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.15.0-1
- Update to 0.15.0
- Remove upstreamed patch

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-4
- Move %%posttrans commands to %%post (rpmlint related)

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-3
- Update License field
- Update Source URL
- Add link of corresponding bug for the memory leak patch

* Wed Nov  7 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-2.1
- Merge spec-file fixes from f18 branch

* Sun Oct 21 2012 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Fix a memory leak
- Update to 0.14.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 0.13.4-1
- Update to 0.13.4

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 0.13.0-2
- Add missing file to file list.

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 0.13.0-1
- Update to 0.13.0

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.1-1
- Update to 0.12.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 0.11.7-1
- Update to 0.11.7

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 0.11.6-1
- Update to 0.11.6

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 0.11.5-1
- Update to 0.11.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Fri Nov  4 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-2
- Fix a typo (#710700)

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.5-1
- Update to 0.7.5

* Fri May  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed Apr  6 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.3-2
- Fix a crash in dconf-editor

* Tue Mar 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-3
- Rebuild for newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Jan 17 2011 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Wed Sep 29 2010 jkeating - 0.5.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Fix up shared library symlinks (#621733)

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- Update to 0.5

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Wed Jun 30 2010 Colin Walters <walters@verbum.org> - 0.4.1-2
- Changes to support snapshot builds

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 0.4.1-1
- Update to 0.4.1
- Include dconf-editor (in a subpackage)

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> 0.4-2
- Rebuild against glib 2.25.9

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Tue Jun 08 2010 Richard Hughes <rhughes@redhat.com> 0.3.2-0.1.20100608
- Update to a git snapshot so that users do not get a segfault in every
  application using GSettings.

* Wed Jun 02 2010 Bastien Nocera <bnocera@redhat.com> 0.3.1-2
- Rebuild against latest glib2

* Mon May 24 2010 Matthias Clasen <mclasen@redhat.com> 0.3.1-1
- Update to 0.3.1
- Add a -devel subpackage

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 0.3-3
- Make batched writes (e.g. with delayed settings) work

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 0.3-2
- Make the registration of the backend work

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> 0.3-1
- Initial packaging
