%global libgit2_version 1.9.0
%global glib2_version 2.44.0

Name:           libgit2-glib
Version:        1.2.0
Release:        8%{?dist}
Summary:        Git library for GLib

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://wiki.gnome.org/Projects/Libgit2-glib
Source0:        https://download.gnome.org/sources/libgit2-glib/1.2/libgit2-glib-%{version}.tar.xz
# https://gitlab.gnome.org/GNOME/libgit2-glib/-/merge_requests/40
Patch:          libgit2-1.8.x.patch
# https://gitlab.gnome.org/GNOME/libgit2-glib/-/merge_requests/46
Patch:          libgit2-1.9.x.patch

BuildRequires:  gcc
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(libgit2) >= %{libgit2_version}
BuildRequires:  libssh2-devel
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  python3-devel
BuildRequires:  vala

%description
libgit2-glib is a glib wrapper library around the libgit2 git access library.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=true \
       -Dpython=true

%meson_build

%install
%meson_install

%files
%license COPYING
%doc AUTHORS NEWS
%{_libdir}/libgit2-glib-1.0.so.0{,.*}
%{_libdir}/girepository-1.0/Ggit-1.0.typelib
%dir %{python3_sitearch}/gi
%dir %{python3_sitearch}/gi/overrides
%{python3_sitearch}/gi/overrides/*

%files devel
%{_includedir}/libgit2-glib-1.0/
%{_libdir}/libgit2-glib-1.0.so
%{_libdir}/pkgconfig/libgit2-glib-1.0.pc
%{_datadir}/gir-1.0/Ggit-1.0.gir
%{_datadir}/vala/
%doc %{_datadir}/gtk-doc/

%changelog
* Tue Jan 14 2025 Pete Walter <pwalter@fedoraproject.org> - 1.2.0-8
- Patch for libgit2 1.9.x support

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2.0-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.0-5
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.0-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Kalev Lember <klember@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Wed Aug 16 2023 Pete Walter <pwalter@fedoraproject.org> - 1.1.0-8
- Rebuild for libgit2 1.7.x

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.12

* Sun Mar 05 2023 Pete Walter <pwalter@fedoraproject.org> - 1.1.0-5
- Rebuild for libgit2 1.6.x

* Fri Jan 27 2023 Pete Walter <pwalter@fedoraproject.org> - 1.1.0-4
- Rebuild for libgit2 1.5.x

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Pete Walter <pwalter@fedoraproject.org> - 1.1.0-2
- Rebuild for libgit2 1.4.x

* Mon Aug 08 2022 Kalev Lember <klember@redhat.com> - 1.1.0-1
- Update to 1.1.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0.1-3
- Rebuilt for Python 3.11

* Sun Feb 20 2022 Igor Raits <igor.raits@gmail.com> - 1.0.0.1-2
- Rebuild for libgit2 1.4.x

* Thu Jan 20 2022 David King <amigadave@amigadave.com> - 1.0.0.1-1
- Update to 1.0.0.1

* Sun Nov 28 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.99.0.1-10
- Rebuild for libgit2 1.3.x

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.99.0.1-8
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 19:00:21 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.99.0.1-6
- Rebuild for libgit2 1.1.x

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.99.0.1-4
- Rebuilt for Python 3.9

* Wed Apr 15 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.99.0.1-3
- Rebuild against libgit2 1.0.0

* Tue Mar 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.99.0.1-2
- Rebuild for libgit2 0.99

* Tue Mar 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.99.0.1-1
- Update to 0.99.0.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.28.0.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.28.0.1-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.28.0.1-2
- Rebuild for libgit2 0.28.x

* Thu May 09 2019 Kalev Lember <klember@redhat.com> - 0.28.0.1-1
- Update to 0.28.0.1

* Wed Feb 13 2019 Kalev Lember <klember@redhat.com> - 0.27.8-1
- Update to 0.27.8

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 04 2018 Pete Walter <pwalter@fedoraproject.org> - 0.27.7-1
- Update to 0.27.7

* Fri Aug 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26.4-4
- Add compatibility with libgit2 0.27.x

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.26.4-2
- Rebuilt for Python 3.7

* Fri Mar 02 2018 Kalev Lember <klember@redhat.com> - 0.26.4-1
- Update to 0.26.4
- Switch to the meson build system

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26.2-2
- Switch to %%ldconfig_scriptlets

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0.26.2-1
- Update to 0.26.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 0.26.0-1
- Update to 0.26.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.0-2
- Rebuild for libgit2 0.26.x

* Thu Feb 16 2017 Kalev Lember <klember@redhat.com> - 0.25.0-1
- Update to 0.25.0

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.25.0-0.1
- Finally backport all patches to build this thing

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.24.4-5
- Backport patches to support libgit-0.25.x

* Tue Jan 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.24.4-4
- Rebuild for libgit2-0.25.x

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.24.4-3
- Rebuild for Python 3.6

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.24.4-2
- BR vala instead of obsolete vala-tools subpackage

* Wed Sep 07 2016 Kalev Lember <klember@redhat.com> - 0.24.4-1
- Update to 0.24.4

* Thu Aug 25 2016 Kalev Lember <klember@redhat.com> - 0.24.3-1
- Update to 0.24.3

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 0.24.2-1
- Update to 0.24.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-2
- Rebuild for libgit2 0.24.0

* Tue Mar 15 2016 Richard Hughes <rhughes@redhat.com> - 0.24.0-1
- Update to 0.24.0

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 0.23.10-1
- Update to 0.23.10

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Kalev Lember <klember@redhat.com> - 0.23.8-1
- Update to 0.23.8

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 0.23.6-1
- Update to 0.23.6

* Tue Aug 11 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.23.4-1
- Update to latest upstream version

* Thu Aug  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.23.2-1
- Update to latest upstream version

* Tue Aug  4 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.23.0-2
- Pull in post-release fixes from upstream (so micro version bump)

* Thu Jul 30 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 0.23.0-1
- Update to 0.23.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 0.22.8-1
- Update to 0.22.8

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 0.22.6-2
- Fix ssh detection

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 0.22.6-1
- Update to 0.22.6

* Sat Apr 11 2015 Kalev Lember <kalevlember@gmail.com> - 0.22.4-1
- Update to 0.22.4
- Use license macro for the COPYING file

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.22.2-1
- Update to 0.22.2

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 0.22.0-1
- Update to 0.22.0

* Tue Nov 04 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.24-1
- Update to 0.0.24

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.22-1
- Update to 0.0.22

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.20-1
- Update to 0.0.20

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.18-2
- Rebuilt for gobject-introspection 1.41.4

* Mon Jun 30 2014 Ignacio Casal Quinteiro <icq@gnome.org> - 0.0.18-1
- Update to 0.0.18

* Sun Jun 22 2014 Ignacio Casal Quinteiro <icq@gnome.org> - 0.0.16-1
- Update to 0.0.16

* Sun Jun 22 2014 Ignacio Casal Quinteiro <icq@gnome.org> - 0.0.14-1
- Update to 0.0.14

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Mar 25 2014 Ignacio Casal Quinteiro <icq@gnome.org> - 0.0.12-1
- Update to 0.0.12

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 0.0.6-1
- Update to 0.0.6

* Sun Jun 16 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.2-2
- Review fixes: depend on python3-gobject (#974834)

* Sun Jun 16 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.2-1
- Initial Fedora build
