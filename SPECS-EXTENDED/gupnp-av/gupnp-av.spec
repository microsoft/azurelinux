Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:          gupnp-av
Version:       0.14.1
Release:       1%{?dist}
Summary:       A collection of helpers for building UPnP AV applications

License:       LGPLv2.1+
URL:           https://www.gupnp.org/
Source0:       https://download.gnome.org/sources/gupnp-av/0.14/%{name}-%{version}.tar.xz
Patch0:        fix-xmlRecoverMemory-deprecation.patch

BuildRequires: glib2-devel
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel >= 1.36.0
BuildRequires: libxml2-devel
BuildRequires: libsoup-devel
BuildRequires: meson
BuildRequires: vala

%description
GUPnP is an object-oriented open source framework for creating UPnP
devices and control points, written in C using GObject and libsoup.
The GUPnP API is intended to be easy to use, efficient and flexible.

GUPnP-AV is a collection of helpers for building AV (audio/video) 
applications using GUPnP.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package docs
Summary: Documentation files for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
This package contains developer documentation for %{name}.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%check
%meson_test
#make check %{?_smp_mflags} V=1

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS README.md
%{_libdir}/libgupnp-av-1.0.so.*
%{_libdir}/girepository-1.0/GUPnPAV-1.0.typelib
%{_datadir}/%{name}

%files devel
%{_includedir}/gupnp-av-1.0
%{_libdir}/pkgconfig/gupnp-av-1.0.pc
%{_libdir}/libgupnp-av-1.0.so
%{_datadir}/gir-1.0/GUPnPAV-1.0.gir
%{_datadir}/vala/vapi/%{name}*

%files docs
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Thu Oct 24 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.14.1-1
- Update to 0.14.1
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.11-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 0.12.11-1
- Update to 0.12.11

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 16 2016 Kalev Lember <klember@redhat.com> - 0.12.10-1
- Update to 0.12.10
- Don't manually add pkgconfig dep for -devel subpackage

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 0.12.9-1
- Update to 0.12.9
- Don't set group tags
- Tighten subpackage deps with the _isa macro
- Use make_install macro

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.12.8-2
- BR vala instead of obsolete vala-tools subpackage

* Thu Feb 11 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.8-1
- 0.12.8 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.8.news
- Use %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan  6 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.7-1
- 0.12.7 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.7.news

* Wed Sep 10 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-5
- Build vala bindings

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.6-3
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-2
- Enable check

* Wed Jun 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.6-1
- 0.12.6 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.6.news

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.5-1
- 0.12.5 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.5.news

* Mon Nov 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-1
- 0.12.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.4.news

* Wed Oct 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.3-1
- 0.12.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.3.news

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.2-1
- 0.12.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.2.news

* Sun May 12 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-2
- Move xsd files to main rpm (RHBZ 962166)

* Tue Mar 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.1-1
- 0.12.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.1.news

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.0-1
- 0.12.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/gupnp-av-0.12.0.news

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.6-1
- 0.11.6 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.6.news

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.5-1
- 0.11.5 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.5.news

* Sat Dec  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.4-1
- 0.11.4 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.4.news

* Mon Nov 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.3-1
- 0.11.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.3.news

* Mon Oct 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.2-1
- 0.11.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.2.news

* Sun Oct  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.0-1
- 0.11.0 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.11/gupnp-av-0.11.0.news

* Sun Aug 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.3-1
- 0.10.3 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.10/gupnp-av-0.10.3.news

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.2-1
- 0.10.2 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.10/gupnp-av-0.10.2.news

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep  5 2011 Zeeshan Ali <zeenix@redhat.com> - 0.10.1-2
- Push a new release to build against latest gssdp and gupnp.

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.1-1
- 0.10.1 release
- http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.10/gupnp-av-0.10.1.news

* Fri Sep  2 2011 Zeeshan Ali <zeenix@redhat.com> - 0.10.0-1
- 0.10.0 release
- http://ftp.acc.umu.se/pub/GNOME/sources/gupnp-av/0.10/gupnp-av-0.10.0.news

* Thu Jun 16 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.1-1
- 0.9.1 release

* Thu Jun 16 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.0-1
- 0.9.0 release

* Sat Apr  9 2011 Peter Robinson <pbrobinson@gmail.com> - 0.8.0-1
- 0.8.0 stable release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.1-1
- Update to 0.7.1

* Mon Nov  8 2010 Peter Robinson <pbrobinson@gmail.com> 0.7.0-1
- Update to 0.7.0

* Wed Sep 29 2010 Peter Robinson <pbrobinson@gmail.com> 0.6.1-1
- Update to 0.6.1

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 0.6.0-2
- Rebuild against newer gobject-introspection

* Fri Sep 17 2010 Peter Robinson <pbrobinson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Tue Aug 17 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.9-2
- Update source URL

* Sat Aug 14 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.9-1
- Update to 0.5.9

* Tue Aug  3 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.8-2
- Add patch to fix dso linking issues

* Mon Aug  2 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.8-1
- Update to 0.5.8

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.5.7-2
- Rebuild with new gobject-introspection

* Fri Jun 25 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.7-1
- Update to 0.5.7

* Mon Jun 21 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.6-1
- Update to 0.5.6

* Fri Apr  9 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.5-1
- Update to 0.5.5

* Fri Feb  5 2010 Peter Robinson <pbrobinson@gmail.com> 0.5.4-1
- Update to 0.5.4

* Sat Nov 21 2009 Peter Robinson <pbrobinson@gmail.com> 0.5.2-1
- Update to 0.5.2

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Peter Robinson <pbrobinson@gmail.com> 0.4.1-1
- New upstream release

* Sun Apr 12 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-1
- New upstream release

* Wed Mar 4  2009 Peter Robinson <pbrobinson@gmail.com> 0.3.1-3
- Move docs to noarch subpackage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 3  2009 Peter Robinson <pbrobinson@gmail.com> 0.3.1-1
- New upstream release

* Thu Dec 18 2008 Peter Robinson <pbrobinson@gmail.com> 0.3-1
- New upstream release

* Thu Dec 18 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-7
- Add gtk-doc build req

* Mon Dec 1 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-6
- Fix directory ownership

* Sat Nov 22 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-5
- Update package summary

* Mon Oct 20 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-4
- Add some requires for the devel package

* Fri Aug 29 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-3
- Some spec file cleanups

* Tue Jun 17 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-2
- Fix build on rawhide

* Tue Jun 17 2008 Peter Robinson <pbrobinson@gmail.com> 0.2.1-1
- Initial release
