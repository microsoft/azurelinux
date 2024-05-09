Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libeasyfc
Version:	0.14.0
Release:	8%{?dist}
Summary:	Easy configuration generator interface for fontconfig

License:	LGPLv3+
URL:		https://tagoh.bitbucket.org/libeasyfc/
Source0:	https://bitbucket.org/tagoh/libeasyfc/downloads/%{name}-%{version}.tar.bz2
Patch0:		%{name}-freetype.patch
Patch1:		%{name}-fix-config.patch

BuildRequires:	glib2-devel gobject-introspection-devel libxml2-devel fontconfig-devel >= 2.12.93 harfbuzz-devel
BuildRequires:	gettext
Requires:	fontconfig >= 2.12.93

%description
libeasyfc aims to provide an easy interface to generate
fontconfig configuration on demand.

%package	gobject
Summary:	GObject interface for libeasyfc
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	gobject
libeasyfc aims to provide an easy interface to generate
fontconfig configuration on demand.

This package contains an interface for GObject.

%package	devel
Summary:	Development files for libeasyfc
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	fontconfig-devel glib2-devel

%description	devel
libeasyfc aims to provide an easy interface to generate
fontconfig configuration on demand.

This package contains the development files to make any
applications with libeasyfc.

%package	gobject-devel
Summary:	Development files for libeasyfc-gobject
Requires:	%{name}-gobject%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	glib2-devel

%description	gobject-devel
libeasyfc aims to provide an easy interface to generate
fontconfig configuration on demand.

This package contains the development files to make any
applications with libeasyfc-gobject.

%prep
%autosetup -p1


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_scriptlets
%ldconfig_scriptlets	gobject

%files
%doc README AUTHORS ChangeLog
%license COPYING
%{_libdir}/libeasyfc.so.*

%files	gobject
%{_libdir}/libeasyfc-gobject.so.*
%{_libdir}/girepository-*/Easyfc-*.typelib

%files	devel
%{_includedir}/libeasyfc
%exclude %{_includedir}/libeasyfc/ezfc-gobject.h
%{_libdir}/libeasyfc.so
%{_libdir}/pkgconfig/libeasyfc.pc
%{_datadir}/gtk-doc/html/libeasyfc

%files	gobject-devel
%{_includedir}/libeasyfc/ezfc-gobject.h
%{_libdir}/libeasyfc-gobject.so
%{_libdir}/pkgconfig/libeasyfc-gobject.pc
%{_datadir}/gir-*/Easyfc-*.gir

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Akira TAGOH <tagoh@redhat.com> - 0.14.0-6
- Fix the issue config can't be turned on when no user config dir is available.
  Resolves: rhbz#1750732

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Akira TAGOH <tagoh@redhat.com> - 0.14.0-2
- Use ldconfig rpm macro.

* Fri Feb 16 2018 Akira TAGOH <tagoh@redhat.com> - 0.14.0-1
- New upstream release.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb  8 2016 Akira TAGOH <tagoh@redhat.com> - 0.13.1-1
- New upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Akira TAGOH <tagoh@redhat.com> - 0.13.0-5
- Fix a crash when config files contains fonts not installed on the system.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.13.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 30 2013 Akira TAGOH <tagoh@redhat.com> - 0.13.0-1
- New upstream release.

* Fri Mar 29 2013 Akira TAGOH <tagoh@redhat.com> - 0.12.1-1
- New upstream release.

* Mon Feb 25 2013 Akira TAGOH <tagoh@redhat.com> - 0.11-1
- New upstream release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Akira TAGOH <tagoh@redhat.com> - 0.10-1
- New upstream release.

* Mon Jul 23 2012 Akira TAGOH <tagoh@redhat.com> - 0.9-1
- New upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Akira TAGOH <tagoh@redhat.com> - 0.8-1
- New upstream release.

* Tue Feb 28 2012 Akira TAGOH <tagoh@redhat.com> - 0.7-1
- New upstream release.

* Wed Feb 08 2012 Akira TAGOH <tagoh@redhat.com> - 0.6-2
- Move .typelib in the libeasyfc-gobject package (#788112)

* Mon Feb 06 2012 Akira TAGOH <tagoh@redhat.com> - 0.6-1
- New upstream release.

* Tue Jan 24 2012 Akira TAGOH <tagoh@redhat.com> - 0.5-1
- New upstream release.

* Wed Jan 18 2012 Akira TAGOH <tagoh@redhat.com> - 0.4-1
- New upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Akira TAGOH <tagoh@redhat.com> - 0.3-1
- New upstream release.

* Fri Dec  9 2011 Akira TAGOH <tagoh@redhat.com> - 0.2-1
- New upstream release.
- Removes %%doc from subpackages as per the suggestions in the review.

* Wed Dec  7 2011 Akira TAGOH <tagoh@redhat.com> - 0.1-1
- Initial packaging.

