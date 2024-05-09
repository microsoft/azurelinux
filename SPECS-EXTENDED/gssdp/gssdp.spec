%global device_sniffer 0
%global docs 0
%global manpages 0
Summary:        Resource discovery and announcement over SSDP
Name:           gssdp
Version:        1.6.2
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.gupnp.org/
Source0:        https://github.com/GNOME/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(gio-2.0)
%if %{with device_sniffer}
BuildRequires:  pkgconfig(gtk4)
%endif
BuildRequires:  pkgconfig(libsoup-3.0)
%if %{with docs}
BuildRequires:  gi-docgen
%endif
BuildRequires:  gobject-introspection-devel >= 1.36
BuildRequires:  meson
BuildRequires:  vala >= 0.20
%if %{with manpages}
BuildRequires:  %{_bindir}/pandoc
%endif

%description
GSSDP implements resource discovery and announcement over SSDP and is part
of gUPnP.  GUPnP is an object-oriented open source framework for creating
UPnP devices and control points, written in C using GObject and libsoup. The
GUPnP API is intended to be easy to use, efficient and flexible.

%package devel
Summary:        Development package for gssdp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with gssdp.

%if %{with device_sniffer}
%package utils
Summary:        Various GUI utuls for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains GUI utilies for %{name}.
%endif

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
%if %{with docs}
       -Dgtk_doc=true \
%else
       -Dgtk_doc=false \
%endif
%if %{with manpages}
       -Dmanpages=true \
%else
       -Dmanpages=false \
%endif
%if %{with device_sniffer}
	-Dsniffer=true
%else
	-Dsniffer=false
%endif

%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/libgssdp-1.6.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GSSDP-1.6.typelib

%files devel
%{_includedir}/gssdp-1.6/
%{_libdir}/libgssdp-1.6.so
%{_libdir}/pkgconfig/gssdp-1.6.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GSSDP-1.6.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gssdp*

%if %{with device_sniffer}
%files utils
%{_bindir}/gssdp-device-sniffer
%{_mandir}/man1/gssdp-device-sniffer.1*
%endif

%if %{with docs}
%files docs
%{_docdir}/gssdp-1.6/
%endif

%changelog
* Tue Jan 31 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.6.2-3
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- Disable gssdp-device-sniffer, docs and manpage sub-package builds
- License verified

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 David King <amigadave@amigadave.com> - 1.6.2-1
- Update to 1.6.2 (#2078238)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 18 2021 Kalev Lember <klember@redhat.com> - 1.4.0.1-1
- Update to 1.4.0.1

* Fri Aug 20 2021 Kalev Lember <klember@redhat.com> - 1.3.1-1
- Update to 1.3.1
- Tighten soname globs

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Kalev Lember <klember@redhat.com> - 1.2.3-1
- Update to 1.2.3

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Avoid redefining license macro
- Fix various issues with directory ownership

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3
- Switch to the meson build system

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Bastien Nocera <bnocera@redhat.com> - 1.0.2-5
+ gssdp-1.0.2-5
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
- Rely on pkgconfig depgen instead of manually specifying -devel requires
- Tighten subpackage deps with the _isa macro
- Use make_install macro

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 0.99.0-1
- Update to 0.99.0
- Remove lib64 rpath from gssdp-device-sniffer

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 0.14.16-1
- Update to 0.14.16

* Tue Apr 26 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.15-1
- 0.14.15 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.15.news

* Thu Feb 11 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.14-1
- 0.14.14 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.14.news

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4  2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.13-1
- 0.14.13 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.13.news

* Wed Nov 25 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.12-1
- 0.14.12 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.12.news
- Use %%license

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan  6 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.11-1
- 0.14.11 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.11.news

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.10-1
- 0.14.10 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.10.news

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 27 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.9-1
- 0.14.9 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.9.news

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.14.8-4
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.8-3
- Enable check

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.8-1
- 0.14.8 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.8.news

* Tue Feb  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.7-1
- 0.14.7 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.7.news

* Sun Nov  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.6-1
- 0.14.6 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.6.news

* Mon Sep  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.5-1
- 0.14.5 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.5.news

* Tue Jul 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.4-1
- 0.14.4 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.4.news

* Thu May 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.3-1
- 0.14.3 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.3.news

* Tue Mar  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.2-1
- 0.14.2 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.2.news

* Sat Feb 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.1-1
- 0.14.1 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.1.news

* Wed Feb 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.14.0
- 0.14.0 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.14/gssdp-0.14.0.news

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.2-1
- 0.13.2 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.13/gssdp-0.13.2.news

* Mon Oct 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.1-1
- 0.13.1 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.13/gssdp-0.13.1.news

* Sun Oct  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.13.0-1
- 0.13.0 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.13/gssdp-0.13.0.news

* Tue Aug 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.2.1-2
- Enable vala bindings

* Tue Aug 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.2.1-1
- 0.12.2.1 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.12/gssdp-0.12.2.1.news

* Sun Aug 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.2-1
- 0.12.2 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.12/gssdp-0.12.2.news

* Thu Jul 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.1-4
- Split utils out to a sub package to reduce libs deps. RHBZ #840689

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.1-1
- 0.12.1 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.12/gssdp-0.12.1.news

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.12.0-2
- Rebuild to break bogus libpng dep

* Fri Sep  2 2011 Zeeshan Ali <zeenix@redhat.com> - 0.12.0-1
- 0.12.0 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.12/gssdp-0.12.0.news

* Fri Aug  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.2-1
- 0.11.2 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.11/gssdp-0.11.2.news

* Sun Jul 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.1-1
- 0.11.1 release
- https://ftp.gnome.org/pub/GNOME/sources/gssdp/0.11/gssdp-0.11.1.news

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.0-1
- 0.11.0 release

* Sat Apr  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.0-1
- 0.10.0 stable release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.2-1
- Update to 0.9.2

* Thu Dec  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.1-1
- Update to 0.9.1

* Fri Nov 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.0-1
- Update to 0.9.0

* Wed Sep 29 2010 jkeating - 0.8.0-3
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 0.8.0-2
- Rebuild against newer gobject-introspection

* Fri Sep 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0-1
- Update to 0.8.0

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-6
- Update source URL

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.7.2-5
- Rebuild with new gobject-introspection

* Mon Jun 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-4
- Fix the build with introspection enabled

* Wed Jun 16 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-3
- Drop gir-devel and gtk-doc requirements

* Sun Apr 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-2
- Enable gobject introspection support

* Fri Apr  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.2-1
- Update to 0.7.2

* Mon Feb 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-2
- Add patch to fix DSO linking. Fixes bug 564764

* Fri Dec  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.1-1
- Update to 0.7.1

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.7.0-2
- Remove unneeded libglade BR

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.7.0-1
- Update to 0.7.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.4-3
- Move docs to noarch subpackage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.4-1
- New upstream release

* Thu Dec 18 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.3-3
- Add gtk-doc build req

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.3-2
- Fix summary

* Mon Oct 27 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.3-1
- New upstream version

* Sun Aug 31 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.2-1
- New upstream version

* Tue Aug 26 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-4
- Move glade files from devel to main rpm

* Tue Aug 12 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-3
- Patch to fix the build in rawhide

* Fri Aug 8 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-2
- Updates based on feedback

* Mon May 19 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.1-1
- Initial package 
