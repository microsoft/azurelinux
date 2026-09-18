# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# uhttpmock is not available in RHEL, and F40 version is too new
%bcond tests %[!(0%{?rhel} || 0%{?fedora} >= 40)]

Name:           libgdata
Version:        0.18.1
Release:        15%{?dist}
Summary:        Library for the GData protocol

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            https://wiki.gnome.org/Projects/libgdata
Source0:        https://download.gnome.org/sources/%{name}/0.18/%{name}-%{version}.tar.xz

# https://gitlab.gnome.org/GNOME/libgdata/-/merge_requests/47
# Build against gcr 4
Patch0:         47.patch

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(gcr-4)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libxml-2.0)
%if %{with tests}
BuildRequires:  pkgconfig(libuhttpmock-0.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
%endif
BuildRequires:  vala

%if 0%{?fedora}
Obsoletes:      compat-libgdata19 < 0.17.1
%endif

%description
libgdata is a GLib-based library for accessing online service APIs using the
GData protocol --- most notably, Google's services. It provides APIs to access
the common Google services, and has full asynchronous support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%meson \
%if %{with tests}
  -Dalways_build_tests=true \
%else
  -Dalways_build_tests=false \
%endif
  -Dinstalled_tests=false \
  -Dgtk_doc=true \
  -Doauth1=disabled \
  %{nil}
%meson_build

%install
%meson_install

%find_lang gdata


%check
# Only the general test can be run without network access
# Actually, the general test doesn't work either without gconf
#cd gdata/tests
#./general

%ldconfig_scriptlets


%files -f gdata.lang
%license COPYING
%doc NEWS README AUTHORS
%{_libdir}/libgdata.so.22*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GData-0.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/libgdata.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GData-0.0.gir
%{_datadir}/vala/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.18.1-13
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Kalev Lember <klember@redhat.com> - 0.18.1-8
- Rebuilt for gcr soname bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 03 2022 Kalev Lember <klember@redhat.com> - 0.18.1-6
- Build against gcr 4 (thanks Bastien Nocera!)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 20 2021 Debarshi Ray <rishi@fedoraproject.org> - 0.18.1-3
- Drop the unused BuildRequires on liboauth

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Mar 05 2021 Kalev Lember <klember@redhat.com> - 0.18.1-1
- Update to 0.18.1

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 0.18.0-1
- Update to 0.18.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 12 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.17.13-2
- Remove uhttpmock-devel from BuildRequires on RHEL 9

* Thu Sep 03 2020 Kalev Lember <klember@redhat.com> - 0.17.13-1
- Update to 0.17.13

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Merlin Mathesius <mmathesi@redhat.com> - 0.17.12-2
- Minor conditional fixes for ELN

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 0.17.12-1
- Update to 0.17.12

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 21 2019 Kalev Lember <klember@redhat.com> - 0.17.11-1
- Update to 0.17.11

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Kalev Lember <klember@redhat.com> - 0.17.10-1
- Update to 0.17.10
- Switch to the meson build system

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Kalev Lember <klember@redhat.com> - 0.17.9-1
- Update to 0.17.9

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Kalev Lember <klember@redhat.com> - 0.17.8-1
- Update to 0.17.8

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com> - 0.17.7-1
- Update to 0.17.7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Kalev Lember <klember@redhat.com> - 0.17.6-3
- Fix RHEL 7 build

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.17.6-2
- BR vala instead of obsolete vala-tools subpackage

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 0.17.6-1
- Update to 0.17.6
- Don't set group tags
- Co-own gir directories instead of depending on gobject-introspection
- Use make_install macro
- Update project URLs

* Mon Sep 12 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.17.5-2
- Backport fix for crashes with zero-length files (GNOME #769727)

* Thu Jun 30 2016 Kalev Lember <klember@redhat.com> - 0.17.5-1
- Update to 0.17.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.17.4-2
- Backport fix for opening PDFs from Google Drive (GNOME #759180)

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 0.17.4-1
- Update to 0.17.4

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 0.17.3-1
- Update to 0.17.3

* Fri Jul 10 2015 Kalev Lember <klember@redhat.com> - 0.17.2-1
- Update to 0.17.2
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.17.1-2
- Obsolete the compatibility package

* Fri Apr 24 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.17.1-1
- Update to 0.17.1

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.16.1-1
- Update to 0.16.1

* Mon Nov 03 2014 Kalev Lember <kalevlember@gmail.com> - 0.16.0-2
- Fix the build on RHEL

* Thu Sep 18 2014 Kalev Lember <kalevlember@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.15.2-1
- Update to 0.15.2
- Tighten -devel deps with the _isa macro

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.15.1-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.15.1-1
- Update to 0.15.1

* Wed Jan 08 2014 Richard Hughes <rhughes@redhat.com> - 0.15.0-1
- Update to 0.15.0

* Thu Aug 29 2013 Kalev Lember <kalevlember@gmail.com> - 0.14.0-1
- Update to 0.14.0

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 0.13.4-1
- Update to 0.13.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.13.3-2
- Disable strict aliasing, since the code is not strict-aliasing-clean

* Tue Feb 26 2013 Kalev Lember <kalevlember@gmail.com> - 0.13.3-1
- Update to 0.13.3
- Add vala bindings

* Tue Feb 19 2013 Bastien Nocera <bnocera@redhat.com> 0.13.2-3
- Co-own the gtk-doc directory (#604382)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 02 2012 Kalev Lember <kalevlember@gmail.com> - 0.13.2-1
- Update to 0.13.2

* Sun Aug 12 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.13.1-2
- Add BuildRequires: gcr-devel gnome-online-accounts-devel

* Tue Jul 31 2012 Richard Hughes <hughsient@gmail.com> - 0.13.1-1
- Update to 0.13.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 0.13.0-1
- Update to 0.13.0

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Thu Mar 15 2012 Matthias Clasen <mclasen@redhat.com> - 0.11.1-1
- Update to 0.11.1

* Tue Jan 17 2012 Dan Horák <dan[at]danny.cz> - 0.11.0-3
- update BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1

* Mon Jul 04 2011 Matthew Barnes <mbarnes@redhat.com> 0.9.1-1
- Update to 0.9.1

* Mon Jun 13 2011 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.8.1-1
- Update to 0.8.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Bastien Nocera <bnocera@redhat.com> 0.8.0-1
- Update to 0.8.0

* Mon Oct 18 2010 Bastien Nocera <bnocera@redhat.com> 0.7.0-1
- Update to 0.7.0

* Wed Sep 29 2010 jkeating - 0.6.4-6
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.4-5
- Rebuild with newer gobject-introspection
- Disable tests

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.6.4-4
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.6.4-2
- Rebuild against new gobject-introspection

* Thu Apr 08 2010 Bastien Nocera <bnocera@redhat.com> 0.6.4-1
- Update to 0.6.4

* Wed Feb 17 2010 Bastien Nocera <bnocera@redhat.com> 0.6.1-2
- Rebuild to update F-13 tag

* Wed Feb 17 2010 Bastien Nocera <bnocera@redhat.com> 0.6.1-1
- Update to 0.6.1

* Mon Feb 15 2010 Bastien Nocera <bnocera@redhat.com> 0.6.0-1
- Update to 0.6.0
- Add introspection support

* Sun Nov 22 2009 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1
- Fixes queries with non-ASCII characters

* Tue Sep 22 2009 Bastien Nocera <bnocera@redhat.com> 0.5.0-1
- Update to 0.5.0

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 0.4.0-3
- Fix source URL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Bastien Nocera <bnocera@redhat.com> 0.4.0-1
- Update to 0.4.0

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 0.3.0-1
- Update to 0.3.0

* Sat Apr 25 2009 Bastien Nocera <bnocera@redhat.com> 0.2.0-1
- Update to 0.2.0

* Mon Apr 06 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.1-2
- Add check, snippet from Jason Tibbitts

* Wed Apr 01 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.1-1
- Update to 0.1.1

* Wed Apr 01 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1.0-1
- First package

