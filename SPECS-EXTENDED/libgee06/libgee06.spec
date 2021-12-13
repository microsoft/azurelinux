Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           libgee06
Version:        0.6.8
Release:        17%{?dist}
Summary:        GObject collection library

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Libgee
#VCS:           git:git://git.gnome.org/libgee
Source0:        https://download.gnome.org/sources/libgee/0.6/libgee-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
# Bootstrap requirements
# BuildRequires:  autoconf automake libtool
# BuildRequires:  vala

%description
libgee is a collection library providing GObject-based interfaces and
classes for commonly used data structures.

libgee provides the following interfaces:

* Iterable
  * Collection
    * List
    * Set
    * MultiSet
    * Queue
      * Deque
* Iterator
* Map
* MultiMap

The ArrayList, HashSet, HashMap, HashMultiSet, HashMultiMap,
LinkedList, PriorityQueue, TreeSet, TreeMap, TreeMultiSet, and
TreeMultiMap classes provide a reasonable sample implementation of
those interfaces. In addition, a set of abstract classes are provided
to ease the implementation of new collections.

Around that, the API provide means to retrieve read-only views,
efficient sort algorithms, simple, bi-directional or index-based
mutable iterators depending on the collection type.

libgee is written in Vala and can be used like any GObject-based C library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libgee-%{version}
# ChangeLog not UTF8
iconv -f iso88591 -t utf8 ChangeLog -o ChangeLog.new
touch -r ChangeLog ChangeLog.new
mv ChangeLog.new ChangeLog


%build
(if ! test -x configure; then
    NOCONFIGURE=1 ./autogen.sh;
    CONFIGFLAGS=--enable-gtk-doc;
 fi;
 %configure --disable-static $CONFIGFLAGS
)
make %{?_smp_mflags}


%check
make check


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Gee-1.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gee-1.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gee-1.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gee-1.0.vapi


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.8-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 15 2019 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.6.8-14
- Update project and download URLs

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.6.8-4
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 0.6.8-1
- Update to 0.6.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.6.1-1
- Update to 0.6.6.1

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.6-1
- Update to 0.6.6

* Sun Sep 23 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb  7 2012 Michel Salim <salimma@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep  9 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-5
- spec cleanup

* Thu Sep  8 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-4
- libgee06, based on the last 0.6.x series libgee for F-16

* Thu Sep  1 2011 Michel Salim <salimma@fedoraproject.org> - 0.6.1-3
- Move typelib file to main package (# 735081)
- Re-enable unit tests on all Fedora releases
- -devel subpackage no longer depends on vala and gobject-introspection-devel

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sun Dec 12 2010 Michel Salim <salimma@fedoraproject.org> - 0.6.0-2
- Update spec to support snapshot builds (# 609294)

* Thu Oct 28 2010 Michel Salim <salimma@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Wed Sep 29 2010 jkeating - 0.5.3-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Michel Salim <salimma@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3
- Rebuild against newer gobject-introspection

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.5.2-2
- Add BR on gobject-introspection-devel.

* Wed Aug 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2.
- Remove buildroot & clean section. No longer needed.

* Thu Jun 17 2010 Michel Salim <salimma@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Sat Oct  3 2009 Michel Salim <salimma@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 Michel Salim <salimma@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.4-2
- Run unit tests only on releases with glib2 >= 2.16

* Sat Dec 13 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4

* Mon Aug 25 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.1-3
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Michel Salim <michel.sylvan@gmail.com> - 0.1.1-2
- Move pkgconfig requirement to -devel subpackage

* Sat Jan 26 2008 Michel Salim <michel.sylvan@gmail.com> - 0.1.1-1
- Initial Fedora package
