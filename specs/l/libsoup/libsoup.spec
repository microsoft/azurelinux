# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define glib2_version 2.58.0

# Coverity scan can override this to 0, to skip checking in gtk-doc generated code
%{!?with_docs: %global with_docs 1}

Name:    libsoup
Version: 2.74.3
Release: 10%{?dist}
Summary: Soup, an HTTP library implementation

License: LGPL-2.0-only
URL: https://wiki.gnome.org/Projects/libsoup
Source0: https://download.gnome.org/sources/%{name}/2.74/%{name}-%{version}.tar.xz
# https://gitlab.gnome.org/GNOME/libsoup/-/merge_requests/385
Patch:   libsoup-2.74.3-libxml2-2.12.0-includes.patch

BuildRequires: gettext
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: glib-networking
%if %{with_docs}
BuildRequires: gtk-doc
%endif
BuildRequires: krb5-devel
BuildRequires: meson
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libbrotlidec)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libpsl)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: vala
BuildRequires: /usr/bin/ntlm_auth

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: glib-networking%{?_isa} >= %{glib2_version}

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

%package devel
Summary: Header files for the Soup library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%if %{with_docs}

%package doc
Summary: Documentation files for %{name}
BuildArch: noarch

%description doc
This package contains developer documentation for %{name}.

# %%{with_docs}
%endif

%prep
%autosetup -p1

%build
%if %{with_docs}
%define gtkdoc_flags -Dgtk_doc=true
%else
%define gtkdoc_flags -Dgtk_doc=false
%endif

%meson %gtkdoc_flags
%meson_build

%install
%meson_install

%find_lang libsoup

%files -f libsoup.lang
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/libsoup-2.4.so.1*
%{_libdir}/libsoup-gnome-2.4.so.1*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Soup*2.4.typelib

%files devel
%{_includedir}/libsoup-2.4
%{_includedir}/libsoup-gnome-2.4
%{_libdir}/libsoup-2.4.so
%{_libdir}/libsoup-gnome-2.4.so
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Soup*2.4.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libsoup-2.4.deps
%{_datadir}/vala/vapi/libsoup-2.4.vapi

%if %{with_docs}

%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/%{name}-2.4

%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 David King <amigadave@amigadave.com> - 2.74.3-4
- Fix building against libxml2 2.12.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 28 2022 David King <amigadave@amigadave.com> - 2.74.3-1
- Update to 2.74.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Kalev Lember <klember@redhat.com> - 2.74.2-1
- Update to 2.74.2

* Wed Oct 27 2021 Kalev Lember <klember@redhat.com> - 2.74.1-1
- Update to 2.74.1

* Wed Sep 08 2021 Kalev Lember <klember@redhat.com> - 2.74.0-1
- Update to 2.74.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 2.72.0-6
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 2.72.0-5
- Don't try to avoid sysprof dep any more now that sysprof-capture-devel is
  split out to a separate subpackage

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 20 2020 Kalev Lember <klember@redhat.com> - 2.72.0-3
- Try harder to avoid sysprof-devel dependency

* Sun Sep 20 2020 Kalev Lember <klember@redhat.com> - 2.72.0-2
- Tighten soname globs
- Avoid automatic requires on sysprof-devel package
- Update required glib2 version

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 2.72.0-1
- Update to 2.72.0

* Sun Sep 06 2020 Kalev Lember <klember@redhat.com> - 2.71.1-1
- Update to 2.71.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.71.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 2.71.0-1
- Update to 2.71.0

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 2.70.0-1
- Update to 2.70.0

* Mon Feb 03 2020 Kalev Lember <klember@redhat.com> - 2.69.90-1
- Update to 2.69.90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.68.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Kalev Lember <klember@redhat.com> - 2.68.3-1
- Update to 2.68.3

* Wed Oct 09 2019 Kalev Lember <klember@redhat.com> - 2.68.2-1
- Update to 2.68.2

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 2.68.1-1
- Update to 2.68.1

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 2.68.0-1
- Update to 2.68.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 2.67.93-1
- Update to 2.67.93

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 2.67.92-1
- Update to 2.67.92

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 2.67.91-1
- Update to 2.67.91

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.67.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Kalev Lember <klember@redhat.com> - 2.67.3-1
- Update to 2.67.3

* Mon Jun 17 2019 Kalev Lember <klember@redhat.com> - 2.67.2-1
- Update to 2.67.2

* Thu May 23 2019 Kalev Lember <klember@redhat.com> - 2.67.1-1
- Update to 2.67.1

* Wed May 15 2019 Kalev Lember <klember@redhat.com> - 2.66.2-1
- Update to 2.66.2

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.66.1-2
- Rebuild with Meson fix for #1699099

* Tue Apr 09 2019 Kalev Lember <klember@redhat.com> - 2.66.1-1
- Update to 2.66.1

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 2.66.0-1
- Update to 2.66.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 2.65.92-1
- Update to 2.65.92

* Wed Feb 20 2019 Kalev Lember <klember@redhat.com> - 2.65.91-1
- Update to 2.65.91

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 2.65.90-1
- Update to 2.65.90

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.65.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Kalev Lember <klember@redhat.com> - 2.65.2-1
- Update to 2.65.2
- Switch to the meson build system
- Co-own gir and gtk-doc directories

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 2.65.1-1
- Update to 2.65.1

* Tue Sep 25 2018 Kalev Lember <klember@redhat.com> - 2.64.1-1
- Update to 2.64.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.64.0-2
- Rebuilt against fixed atk (#1626575)

* Wed Sep 05 2018 Kalev Lember <klember@redhat.com> - 2.64.0-1
- Update to 2.64.0

* Sun Aug 12 2018 Kalev Lember <klember@redhat.com> - 2.63.90-1
- Update to 2.63.90

* Fri Aug 10 2018 Kalev Lember <klember@redhat.com> - 2.62.3-1
- Update to 2.62.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.62.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Kalev Lember <klember@redhat.com> - 2.62.2-2
- Backport an upstream patch for CVE-2018-12910

* Tue May 08 2018 Kalev Lember <klember@redhat.com> - 2.62.2-1
- Update to 2.62.2

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 2.62.1-1
- Update to 2.62.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.62.0-1
- Update to 2.62.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 2.61.91-1
- Update to 2.61.91

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.61.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 2.61.90-1
- Update to 2.61.90
- Drop ldconfig scriptlets

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.61.2-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 09 2018 Kalev Lember <klember@redhat.com> - 2.61.2-1
- Update to 2.61.2

* Wed Dec 20 2017 Kalev Lember <klember@redhat.com> - 2.61.1-1
- Update to 2.61.1

* Thu Nov 16 2017 Milan Crha <mcrha@redhat.com> - 2.60.2-2
- Add patch for RH bug #1458498 (Crash under soup_socket_new())

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.60.2-1
- Update to 2.60.2

* Wed Oct 11 2017 Kalev Lember <klember@redhat.com> - 2.60.1-1
- Update to 2.60.1
- Remove lib64 rpaths

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 2.60.0-1
- Update to 2.60.0

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 2.59.90.1-2
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Kalev Lember <klember@redhat.com> - 2.59.90.1-1
- Update to 2.59.90.1 (CVE-2017-2885)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Tomas Popela <tpopela@redhat.com> - 2.58.1-2
- Backport negotiate fixes

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Wed May 03 2017 Milan Crha <mcrha@redhat.com> - 2.58.0-2
- Add patch for GNONE bug #781590 (Fails to connect to server due to request cancel)

* Thu Apr 20 2017 Kalev Lember <klember@redhat.com> - 2.58.0-1
- Update to 2.58.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.57.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 David King <amigadave@amigadave.com> - 2.57.1-1
- Update to 2.57.1

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 2.56.0-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 2.56.0-1
- Update to 2.56.0

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 2.55.90-1
- Update to 2.55.90

* Tue Apr 26 2016 Milan Crha <mcrha@redhat.com> - 2.54.1-1
- Update to 2.54.1
- Remove patch for NTLM auth failure with latest samba (fixed upstream)

* Fri Apr 22 2016 Milan Crha <mcrha@redhat.com> - 2.54.0.1-3
- Add 'BuildRequires: krb5-devel', to support WWW-Authenticate: Negotiate in runtime

* Tue Apr 19 2016 Milan Crha <mcrha@redhat.com> - 2.54.0.1-2
- NTLM auth failure with latest samba (rh #1327072)

* Wed Mar 23 2016 Kalev Lember <klember@redhat.com> - 2.54.0.1-1
- Update to 2.54.0.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.54.0-1
- Update to 2.54.0

* Tue Mar 15 2016 Kalev Lember <klember@redhat.com> - 2.53.92-1
- Update to 2.53.92

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 2.53.90-1
- Update to 2.53.90

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.53.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Kalev Lember <klember@redhat.com> - 2.53.2-1
- Update to 2.53.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.53.1-1
- Update to 2.53.1

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 2.52.1-1
- Update to 2.52.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.52.0-1
- Update to 2.52.0

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 2.51.92-1
- Update to 2.51.92

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.51.90-1
- Update to 2.51.90
- Use make_install macro
- Build vala bindings

* Tue Jun 23 2015 David King <amigadave@amigadave.com> - 2.51.3-1
- Update to 2.51.3
- Update URL
- Use pkgconfig for BuildRequires
- Preserve timestamps during install

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 2.50.0-1
- Update to 2.50.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 2.49.92-1
- Update to 2.49.92

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 2.49.91.1-1
- Update to 2.49.91.1

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 2.49.91-1
- Update to 2.49.91
- Use the %%license macro for the COPYING file

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.49.1-1
- Update to 2.49.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.48.0-1
- Update to 2.48.0

* Mon Sep 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.47.92-1
- Update to 2.47.92
- Tighten deps with the _isa macro

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.47.4-1
- Update to 2.47.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 2.47.3-1
- Update to 2.47.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.46.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.46.0-2
- Update dep versions

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.45.92-1
- Update to 2.45.92

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 2.45.90-1
- Update to 2.45.90

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.45.3-1
- Update to 2.45.3

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 2.44.2-1
- Update to 2.44.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 2.44.1-1
- Update to 2.44.1

* Sun Sep 29 2013 Dan Winship <danw@redhat.com> - 2.44.0-2
- Fix hang on early close with streaming API

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.43.92-1
- Update to 2.43.92

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.43.90-1
- Update to 2.43.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.43.5-1
- Update to 2.43.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.43.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Dan Winship <danw@redhat.com> - 2.43.4-1
- Update to 2.43.4

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.43.2-1
- Update to 2.43.2

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.43.1-1
- Update to 2.43.1

* Mon Apr 29 2013 Kalev Lember <kalevlember@gmail.com> - 2.42.2-1
- Update to 2.42.2

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 2.42.1-1
- Update to 2.42.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 2.41.92-1
- Update to 2.41.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 2.41.91-1
- Update to 2.41.91

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 2.41.90-1
- Update to 2.41.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 2.41.5-1
- Update to 2.41.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.41.4-1
- Updat e to 2.41.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.41.3-1
- Update to 2.41.3
- Remove libgnome-keyring build dep; no longer used

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 2.41.2-1
- Update to 2.41.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.41.1-1
- Update to 2.41.1

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.40.1-1
- Update to 2.40.1

* Tue Oct  2 2012 Matthias Clasen <mclasen@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.39.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.39.4.1-1
- Update to 2.39.4.1

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 2.39.3-1
- Update to 2.39.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 2.39.2-1
- Update to 2.39.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.39.1-1
- Update to 2.39.1
- Package the translations

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.38.1-1
- Update to 2.38.1

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.37.92-1
- Update to 2.37.92

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 2.37.91-1
- Update to 2.37.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 2.37.90-1
- Update to 2.37.90

* Mon Feb 13 2012 Matthias Clasen <mclasen@redhat.com> - 2.37.5.1-1
- Update to 2.37.5.1

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.37.5-1
- Update to 2.37.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2.37.4-1
- Update to 2.37.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.37.3-1
- Update to 2.37.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.37.2-1
- Update to 2.37.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.37.1-1
- Update to 2.37.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.36.1-1
- Update to 2.36.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 2.35.92-1
- Update to 2.35.92

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> 2.35.90-1
- Update to 2.35.90

* Wed Aug 17 2011 Matthias Clasen <mclasen@redhat.com> 2.35.5-1
- Update to 2.35.5

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 2.35.3-1
- Update to 2.35.3

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.1-1
- Update to 2.34.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.92-2
- Clean up BRs

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.92-1
- 2.33.92

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.90-1
- 2.33.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 2.33.6-1
- Update to 2.33.6

* Mon Jan 17 2011 Dan Winship <danw@redhat.com> - 2.33.5-2
- Require glib-networking, for TLS support

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.5-1
- Update to 2.33.5

* Thu Dec  2 2010 Dan Winship <danw@redhat.com> - 2.32.2-1
- Update to 2.32.2

* Thu Nov 11 2010 Dan Horák <dan[at]danny.cz> - 2.32.0-2
- bump release to win over F-14

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.31.2-5
- Rebuild with new gobject-introspection

* Fri Jul  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-4
- Rebuild for introspection format break

* Wed Jun 23 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.2-3
- libsoup-devel doesn't need gtk-doc (RH bug #604396).

* Mon Jun 21 2010 Peter Robinson <pbrobinson@gmail.com> - 2.31.2-2
- enable introspection support

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 25 2010 Nils Philippsen <nils@redhat.com> - 2.29.91-2
- rebuild for new libproxy

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Mon Feb 08 2010 Matthew Barnes <mbarnes@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-1
- Update to 2.29.5

* Wed Dec  9 2009 Dan Winship <danw@redhat.com> - 2.29.3-2
- Add patch from git to fix gir-repository build

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Wed Jun 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/libsoup/2.26/libsoup-2.26.1.changes

* Thu Apr  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0.9-1
- Upate to 2.26.0.9

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Mon Feb 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Sun Jan 25 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.4-2
- Build against libproxy

* Mon Jan 05 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Tue Dec 16 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Mon Dec 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Wed Nov 12 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.1-3
- Fix BuildRequires

* Fri Nov 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Mon Oct 20 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Sep 24 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0.1-1
- Update to 2.24.0.1

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Mon Aug 04 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Wed Jul 30 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-6
- Omit unused direct shared library dependencies (RH bug #226046).

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> - 2.23.1-5
- rebuild with new gnutls

* Sun Jun 22 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-4
- Remove unnecessary pkgconfig build requirement.

* Mon Jun 16 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-3
- Incorporate package review feedback (RH bug #226046).

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-2
- Fix source url

* Mon Apr 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Apr 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.4.1-1
- Update to 2.4.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Feb 25 2008 Matthew Barnes <mbarnes@redhat.com> - 2.3.4-1
- Update to 2.3.4

* Wed Feb 13 2008 Matthew Barnes <mbarnes@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Mon Jan 28 2008 Matthew Barnes <mbarnes@redhat.com> - 2.3.0-1
- Update to 2.3.0
- Bump glib2 requirement to >= 2.15.3.
- Clean up some redundant dependencies.
- Remove patch for RH bug #327871 (fixed in glibc).

* Mon Nov 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.104-1
- Update to 2.2.104

* Sun Oct 28 2007 Jeremy Katz <katzj@redhat.com> - 2.2.103-1
- update to 2.2.103 to fix a rhythmbox crasher (#343561)

* Mon Oct 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.102-1
- Update to 2.2.102

* Thu Oct 11 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.101-2
- Add patch for RH bug #327871 (broken Rhythmbox build).
- Suspect this is really a glibc bug.

* Fri Oct 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.101-1
- Update to 2.2.101

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.2.100-3
- Update the license field

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.2.100-2
- Don't install INSTALL

* Mon Feb 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.100-1
- Update to 2.2.100

* Mon Jan 08 2007 Matthew Barnes <mbarnes@redhat.com> - 2.2.99-1
- Update to 2.2.99

* Tue Nov 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.98-1
- Update to 2.2.98
- Remove patch for RH bug #215919 (fixed upstream).

* Fri Nov 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.97-2
- Avoid accidentally exported symbols (#215919)

* Mon Nov 06 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.97-1
- Update to 2.2.97
- Remove patch for Gnome.org bug #356809 (fixed upstream).

* Fri Nov 03 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.96-5
- Revised patch for Gnome.org bug #356809 to match upstream.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.2.96-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.96-3.fc6
- Add patch for Gnome.org bug #356809 (lingering file on uninstall).

* Tue Aug 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.96-2.fc6
- Rebuild

* Tue Jul 25 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.96
- Update to 2.2.96
- Bump glib2 requirement to >= 2.6.

* Wed Jul 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.95.1-1
- Update to 2.2.95.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.94-3.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 2.2.94-3
- rebuilt with new gnutls

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.94-1
- Update to 2.2.94

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.92-2
- Update to 2.2.92

* Sat Mar  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.91-1
- Update to 2.2.91

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.7-2
- Remove excessive Requires for the -devel package

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.7-1
- 2.2.7
- Remove static library

* Tue Aug 23 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.6.1-1
- 2.2.6.1

* Tue Aug  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.5-1
- 2.2.5
- Removed gnome-bug-306877-soup-connection-ntlm.c.patch (#160071) as this is 
  now in upstream tarball

* Mon Aug  8 2005 Tomas Mraz <tmraz@redhat.com> - 2.2.3-5
- rebuild with new gnutls

* Tue Jun 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.3-4
- add patch for NTLM domains (#160071)

* Sun Apr 24 2005 Florian La Roche <laroche@redhat.com>
- rebuild for new gnutls

* Thu Mar 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.3-2
- explicitly enable gtk-doc support

* Thu Mar 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.3-1
- 2.2.3

* Wed Mar  2 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-3
- rebuild with GCC 4

* Wed Jan 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-2
- actually uploaded the source this time

* Wed Jan 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-1
- update from 2.2.1 to 2.2.2
- add explicit devel requirements on glib2-devel, pkgconfig, gtk-doc, gnutls-devel and libxml2-devel

* Tue Oct 12 2004 David Malcolm <dmalcolm@redhat.com> - 2.2.1-1
- update from 2.2.0 to 2.2.1

* Wed Oct  6 2004 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- added requirement on libxml2 (#134700)

* Wed Sep 22 2004 David Malcolm <dmalcolm@redhat.com> - 2.2.0-2
- added requirement on gnutls, so that we build with SSL support
- fixed source download path

* Tue Aug 31 2004 David Malcolm <dmalcolm@redhat.com> - 2.2.0-1
- update from 2.1.13 to 2.2.0

* Mon Aug 16 2004 David Malcolm <dmalcolm@redhat.com> - 2.1.13-1
- 2.1.13

* Tue Jul 20 2004 David Malcolm <dmalcolm@redhat.com> - 2.1.12-1
- 2.1.12

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 David Malcolm <dmalcolm@redhat.com> - 2.1.11-1
- 2.1.11

* Thu May 20 2004 David Malcolm <dmalcolm@redhat.com> - 2.1.10-2
- added missing md5 file

* Thu May 20 2004 David Malcolm <dmalcolmredhat.com> - 2.1.10-1
- 2.1.10

* Tue Apr 20 2004 David Malcolm <dmalcolm@redhat.com> - 2.1.9-1
- Update to 2.1.9; added gtk-doc to BuildRequires and the generated files to the devel package

* Wed Mar 10 2004 Jeremy Katz <katzj@redhat.com> - 2.1.8-1
- 2.1.8

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> - 2.1.7-1
- 2.1.7

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Jeremy Katz <katzj@redhat.com> 2.1.5-1
- 2.1.5

* Wed Jan 14 2004 Jeremy Katz <katzj@redhat.com> 2.1.4-0
- update to 2.1.4

* Sat Jan  3 2004 Jeremy Katz <katzj@redhat.com> 2.1.3-0
- update to 2.1.3

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 1.99.26-2
- rebuild

* Fri Sep 19 2003 Jeremy Katz <katzj@redhat.com> 1.99.26-1
- 1.99.26

* Tue Jul 15 2003 Jeremy Katz <katzj@redhat.com> 1.99.23-3
- rebuild to pickup ppc64

* Mon Jun  9 2003 Jeremy Katz <katzj@redhat.com> 1.99.23-2
- rebuild 
- no openssl on ppc64 yet, excludearch

* Mon Jun  9 2003 Jeremy Katz <katzj@redhat.com> 1.99.23-1
- 1.99.23

* Thu Jun 5 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  5 2003 Jeremy Katz <katzj@redhat.com> 1.99.22-2
- rebuild

* Sun May 25 2003 Jeremy Katz <katzj@redhat.com> 1.99.22-1
- 1.99.22

* Tue May  6 2003 Jeremy Katz <katzj@redhat.com> 1.99.20-1
- 1.99.20

* Sun May  4 2003 Jeremy Katz <katzj@redhat.com> 1.99.17-3
- include ssl proxy so that ssl urls work properly (#90165, #90166)

* Wed Apr 16 2003 Jeremy Katz <katzj@redhat.com> 1.99.17-2
- forward port patch to use a union initializer to fix build on x86_64

* Wed Apr 16 2003 Jeremy Katz <katzj@redhat.com> 1.99.17-1
- rename package to libsoup
- update to 1.99.17
- don't obsolete soup for now, it's parallel installable

* Sun Apr  6 2003 Jeremy Katz <katzj@redhat.com> 0.7.11-1
- update to 0.7.11

* Wed Apr  2 2003 Matt Wilson <msw@redhat.com> 0.7.10-5
- added soup-0.7.10-64bit.patch to fix 64 bit platforms (#86347)

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- only runtime libs in normal rpm

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Jeremy Katz <katzj@redhat.com> 
- update url (#82347)

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.7.10-2
- use pkgconfig's openssl configuration information, if it exists

* Fri Dec 13 2002 Jeremy Katz <katzj@redhat.com> 0.7.10-1
- update to 0.7.10

* Thu Dec 12 2002 Jeremy Katz <katzj@redhat.com> 0.7.9-4
- fix fpic patch
- soup-devel should require soup

* Thu Dec 12 2002 Jeremy Katz <katzj@redhat.com> 0.7.9-3
- better lib64 patch
- fix building of libwsdl-build to use libtool so that it gets built 
  with -fPIC as needed

* Tue Dec 10 2002 Jeremy Katz <katzj@redhat.com> 0.7.9-2
- change popt handling in configure slightly so that it will work on 
  multilib arches

* Tue Dec 10 2002 Jeremy Katz <katzj@redhat.com> 0.7.9-1
- update to 0.7.9, pulling the tarball out of Ximian packages

* Wed Oct 23 2002 Jeremy Katz <katzj@redhat.com> 0.7.4-3
- fix to not try to include non-existent doc files and remove all 
  unwanted files from the build
- include api docs 
- don't build the apache module

* Wed Sep 25 2002 Jeremy Katz <katzj@redhat.com> 0.7.4-2
- various specfile tweaks to include in Red Hat Linux
- include all the files

* Tue Jan 23 2001 Alex Graveley <alex@ximian.com>
- Inital RPM config.
