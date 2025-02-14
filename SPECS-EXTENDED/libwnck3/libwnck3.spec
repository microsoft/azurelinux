Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global source_name libwnck

Summary: Window Navigator Construction Kit
Name: libwnck3
Version: 43.1
Release: 2%{?dist}
URL: http://download.gnome.org/sources/%{source_name}/
Source0: https://download.gnome.org/sources/%{source_name}/43/%{source_name}-%{version}.tar.xz
License: LGPL-2.0-or-later

# https://gitlab.gnome.org/GNOME/libwnck/-/merge_requests/10
Patch1:        libwnck_0001-Expose-window-scaling-factor_v43.1.patch
Patch2:        libwnck_0002-icons-Use-cairo-surfaces-to-render-icons_v43.1.patch
Patch3:        libwnck_0003-xutils-Change-icons-to-being-cairo-surfaces_v43.1.patch
Patch4:        libwnck_0004-icons-Mark-GdkPixbuf-icons-as-deprecated_v43.1.patch
Patch5:        libwnck_0005-tasklist-Add-surface-loader-function_v43.1.patch

BuildRequires: gcc
BuildRequires: meson
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: gtk-doc
BuildRequires: libXres-devel
BuildRequires: pango-devel
BuildRequires: startup-notification-devel

Requires:      startup-notification

%description
libwnck (pronounced "libwink") is used to implement pagers, tasklists,
and other such things. It allows applications to monitor information
about open windows, workspaces, their names/icons, and so forth.

%package devel
Summary: Libraries and headers for libwnck
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{source_name}-%{version} -p1

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install

%find_lang %{source_name}-3.0 --with-gnome --all-name

%ldconfig_scriptlets

%files -f %{source_name}-3.0.lang
%license COPYING
%doc AUTHORS README NEWS
%{_libdir}/%{source_name}-3.so.0*
%{_bindir}/wnck-urgency-monitor
%{_libdir}/girepository-1.0/Wnck-3.0.typelib

%files devel
%{_bindir}/wnckprop
%{_libdir}/%{source_name}-3.so
%{_libdir}/pkgconfig/*
%{_includedir}/%{source_name}-3.0/
%{_datadir}/gir-1.0/Wnck-3.0.gir
%doc %{_datadir}/gtk-doc

%changelog
* Mon 18 Sreenivasulu Malavathula <vsmalavathu@microsoft.com> - 43.1-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Mon Oct 07 2024 Wolfgang Ulbrich <raveit65.sun@gmail.com> - 43.1-1
- update to 43.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Wolfgang Ulbrich <fedora@raveit.de> - 43.0-6
- fix rhbz (#2242944)
- disable Revert-pager-do-not-change-workspace-size-from-size patch

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 07 2022 Wolfgang Ulbrich <fedora@raveit.de> - 43.0-3
- fix https://bugs.launchpad.net/ubuntu/+source/libwnck3/+bug/1990263

* Thu Sep 29 2022 Wolfgang Ulbrich <fedora@raveit.de> - 43.0-2
- fix https://gitlab.gnome.org/GNOME/libwnck/-/issues/154

* Mon Sep 19 2022 Wolfgang Ulbrich <fedora@raveit.de> - 43.0-1
- update to 43.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 19 2022 Wolfgang Ulbrich <fedora@raveit.de> - 40.1-1
- update to 40.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 12 2021 Wolfgang Ulbrich <fedora@raveit.de> - 40.0-4
- use https://gitlab.gnome.org/GNOME/libwnck/-/commit/bd8ab37
- Scale tasklist icons

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Wolfgang Ulbrich <fedora@raveit.de> - 40.0-2
- revert https://gitlab.gnome.org/GNOME/libwnck/-/commit/3456b74
- fixes rhbz #1971048
- and https://github.com/mate-desktop/mate-panel/issues/1230
 
* Wed May 26 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0
- Tighten soname globs

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Mar 28 2020 Wolfgang Ulbrich <fedora@raveit.de> - 3.36.0-1
- update to 3.36.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Phil Wyett <philwyett@kathenas.org> - 3.32.0-1
- Update to 3.32.0

* Fri Feb 01 2019 Kalev Lember <klember@redhat.com> - 3.31.4-1
- Update to 3.31.4
- Switch to the meson build system

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 22 2017 Wolfgang Ulbrich <fedora@raveit.de> - 3.24.0-2
- fix locale dir
- https://git.gnome.org/browse/libwnck/commit/?id=4feb967

* Sun Jul 02 2017 Wolfgang Ulbrich <fedora@raveit.de> - 3.24.0-1
- Update to 3.24.0
- modernize spec file

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 29 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 3.20.1-1
- Update to 3.20.1

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 3.14.1-1
- Update to 3.14.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.4.9-1
- Update to 3.4.9
- Tighten -devel subpackage deps

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.4.7-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.4.7-1
- Update to 3.4.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.4.5-1
- Update to 3.4.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.4-1
- Update to 3.4.4

* Sat Sep 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.3-1
- Update to 3.4.3

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 3.1.92-1
- Update to 3.1.92

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> 3.0.2-1
- Update to 3.0.2

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Rebuild against newer gtk3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Ray Strode <rstrode@redhat.com> 2.91.6-1
- Initial import.
