%global apiver 1.6
%global gssdp_version 1.6.2
%global docs 0
Summary:        A framework for creating UPnP devices & control points
Name:           gupnp
Version:        1.6.3
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gupnp.org/
Source0:        https://github.com/GNOME/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%if %{with docs}
BuildRequires:  docbook-style-xsl
BuildRequires:  gi-docgen
%endif
BuildRequires:  gobject-introspection-devel
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  pkgconfig(gssdp-1.6) >= %{gssdp_version}
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(uuid)
Requires:       dbus
Requires:       gssdp%{?_isa} >= %{gssdp_version}

%description
GUPnP is an object-oriented open source framework for creating UPnP
devices and control points, written in C using GObject and libsoup.
The GUPnP API is intended to be easy to use, efficient and flexible.

%package devel
Summary:        Development package for gupnp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%if %{with docs}
%package docs
Summary:        Documentation files for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description docs
This package contains developer documentation for %{name}.
%endif

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
%meson \
  -Dcontext_manager=network-manager \
%if %{with docs}
  -Dgtk_doc=true \
%else
  -Dgtk_doc=false \
%endif
  -Dexamples=false \
  %{nil}
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc AUTHORS README.md
%{_libdir}/libgupnp-%{apiver}.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GUPnP-%{apiver}.typelib

%files devel
%{_bindir}/gupnp-binding-tool-%{apiver}
%{_includedir}/gupnp-%{apiver}/
%{_libdir}/libgupnp-%{apiver}.so
%{_libdir}/pkgconfig/gupnp-%{apiver}.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GUPnP-%{apiver}.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gupnp*
%{_mandir}/man1/gupnp-binding-tool-%{apiver}.1*

%if %{with docs}
%files docs
%{_docdir}/gupnp-%{apiver}/
%endif

%changelog
* Wed Apr 17 2024 Andrew Phelps <anphel@microsoft.com> - 1.6.3-4
- Fix build break

* Wed Feb 01 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.6.3-3
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Disable docs
- License verified

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 David King <amigadave@amigadave.com> - 1.6.3-1
- Update to 1.6.3

* Mon Nov 21 2022 David King <amigadave@amigadave.com> - 1.6.2-1
- Update to 1.6.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 David King <amigadave@amigadave.com> - 1.4.3-1
- Update to 1.4.3

* Mon Jan 10 2022 David King <amigadave@amigadave.com> - 1.4.2-1
- Update to 1.4.2

* Tue Dec 07 2021 Kalev Lember <klember@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Sat Sep 18 2021 Kalev Lember <klember@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri Aug 20 2021 Kalev Lember <klember@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Kalev Lember <klember@redhat.com> - 1.2.7-1
- Update to 1.2.7

* Wed May 26 2021 Kalev Lember <klember@redhat.com> - 1.2.6-1
- Update to 1.2.6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 1.2.4-1
- Update to 1.2.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Kalev Lember <klember@redhat.com> - 1.2.3-1
- Update to 1.2.3
- Set minimum required gssdp version

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Switch to the meson build system
- Use apiver macro in the spec file instead of hardcoding
- Fix various directory ownership issues

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Kalev Lember <klember@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Bastien Nocera <bnocera@redhat.com> - 1.0.2-6
+ gupnp-1.0.2-6
- Fix Python3 substitution, and make it earlier

* Thu Feb 15 2018 Bastien Nocera <bnocera@redhat.com> - 1.0.2-5
+ gupnp-1.0.2-5
- Remove unused NetworkManager-devel BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 16 2016 Kalev Lember <klember@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 1.0.0-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 1.0.0-1
- Update to 1.0.0
- Don't set group tags
- Use make_install macro

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.99.0-1
- Update to 0.99.0
- Drop manual requires that are automatically handled by pkgconfig dep gen
- Tighten inter package dependencies with the _isa macro

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 0.20.18-1
- Update to 0.20.18

* Tue Apr 26 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.17-1
- 0.20.17 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.17.news

* Thu Feb 11 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.16-1
- 0.20.16 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.16.news

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4  2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.15-1
- 0.20.15 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.15.news

* Mon Dec 14 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.20.14-4
- GUPnPNetworkManager is never deallocated due to internal circular reference
  (GNOME #741257)

* Fri Jul 03 2015 Kalev Lember <klember@redhat.com> - 0.20.14-3
- Switch to Python 3 (#1192093)
- Move gupnp-binding-tool to -devel subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Kalev Lember <kalevlember@gmail.com> - 0.20.14-1
- Update to 0.20.14
- Use license macro for the COPYING file

* Tue Jan  6 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.13-1
- 0.20.13 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.13.news

* Sat Oct 11 2014 Dan Horák <dan[at]danny.cz> - 0.20.12-6
- Disable tests, they fail with libsoup-2.48 (gnome#738365)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.20.12-4
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.12-3
- Enable check

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.12-1
- 0.20.12 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.12.news
- Re-add vala bindings to devel (RHBZ 1093204)

* Tue May  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.11-1
- 0.20.11 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.11.news

* Tue Feb  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.10-1
- 0.20.10 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.10.news

* Sun Dec 15 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.9-1
- 0.20.9 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.9.news

* Sun Nov  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.8-1
- 0.20.8 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.8.news

* Wed Oct 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.7-1
- 0.20.7 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.7.news

* Mon Sep  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.6-1
- 0.20.6 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.6.news

* Wed Aug 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.5-1
- 0.20.5 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.5.news

* Tue Jul 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.4-1
- 0.20.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.4.news

* Thu May 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.3-1
- 0.20.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.3.news

* Sat Apr 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.2-1
- 0.20.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.2.news

* Tue Mar  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.1-1
- 0.20.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.1.news

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- Obsolete gupnp-vala

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-2
- bump

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.20.0-1
- 0.20.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.20/gupnp-0.20.0.news

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.4-1
- 0.19.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.4.news

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.3-1
- 0.19.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.3.news

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.2-1
- 0.19.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.2.news

* Mon Oct 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.1-1
- 0.19.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.1.news

* Sun Oct  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.19.0-1
- 0.19.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.19/gupnp-0.19.0.news

* Sun Aug 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.4-1
- 0.18.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.4.news

* Mon Aug 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.3-3
- Use NetworkManager for connectivity detection

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.3-1
- 0.18.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.3.news

* Thu Apr 26 2012 Zeeshan Ali <zeenix@redhat.com> - 0.18.2-2
- Remove bogus dependency on libgdbus-devel.

* Sun Mar 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.2-1
- 0.18.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.2.news

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.18.1-1
- 0.18.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.1.news

* Mon Sep  5 2011 Zeeshan Ali <zeenix@redhat.com> - 0.18.0-2
- Push a new release to build against latest gssdp.

* Fri Sep  2 2011 Zeeshan Ali <zeenix@redhat.com> - 0.18.0-1
- 0.18.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.18/gupnp-0.18.0.news

* Fri Aug  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.2-1
- 0.17.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.17/gupnp-0.17.2.news

* Sun Jul 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.1-1
- 0.17.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp/0.17/gupnp-0.17.1.news

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.0-1
- 0.17.0 release

* Sun May  1 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.16.1-1
- 0.16.1 stable release

* Sat Apr  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.16.0-1
- 0.16.0 stable release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.1-1
- Update to 0.15.1

* Tue Nov 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.0-1
- Update to 0.15.0

* Wed Sep 29 2010 jkeating - 0.14.0-3
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 0.14.0-2
- Rebuild against newer gobject-introspection

* Fri Sep 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.0-1
- Update to 0.14.0

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.5-2
- Update source URL

* Sat Aug 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.5-1
- Update to 0.13.5

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.13.4-4
- Rebuild with new gobject-introspection

* Mon Jun 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.4-2
- Add patch to fix build

* Mon Jun 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.4-1
- Update to 0.13.4

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-4
- Once more with feeling!

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-3
- add back missing line to spec

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-2
- bump build

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.3-1
- Update to 0.13.3

* Mon Mar  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.2-2
- Add patch to fix DSO linking. Fixes bug 564855

* Fri Dec  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.2-1
- Update to 0.13.2

* Wed Oct  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.1-1
- Update to 0.13.1

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.13.0-1
- Update to 0.13.0

* Mon Aug 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-4
- some spec file cleanups, depend on libuuid instead of e2fsprogs-devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  1 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-2
- Rebuild with new libuuid build req

* Wed Jun  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-1
- New upstream release

* Mon Apr 27 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.7-1
- New upstream release

* Wed Mar  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-4
- Move docs to noarch sub package

* Mon Mar  2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-3
- Add some extra -devel Requires packages

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-1
- New upstream release

* Wed Jan 14 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.5-1
- New upstream release

* Thu Dec 18 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-3
- Add gtk-doc build req

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-2
- Fix summary

* Mon Nov 17 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-1
- New upstream release

* Mon Oct 27 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.3-1
- New upstream release

* Mon Oct 20 2008 Colin Walters <walters@verbum.org> 0.12.2-2
- devel package requires gssdp-devel

* Sun Aug 31 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.2-1
- New upstream release

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-7
- Yet again. Interesting it builds fine in mock and not koji

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-6
- Once more with feeling

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-5
- Second go

* Thu Aug 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-4
- Fix build on rawhide

* Wed Aug 13 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-3
- Fix changelog entries

* Wed Aug 13 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-2
- Fix a compile issue on rawhide

* Mon Jun 16 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-1
- Initial release
