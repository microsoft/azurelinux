Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name: rarian
Version: 0.8.1
Release: 25%{?dist}
License: LGPLv2+
Summary: Documentation meta-data library
URL: https://rarian.freedesktop.org/
Source: https://download.gnome.org/sources/rarian/0.8/rarian-%{version}.tar.bz2
Source1: scrollkeeper-omf.dtd

### Patch ###

# RH bug #453342
Patch1: rarian-0.8.1-categories.patch

### Dependencies ###

Requires(post): libxml2
Requires(postun): libxml2
# for /usr/bin/xmlcatalog

Requires: libxslt
# for /usr/bin/xsltproc
Requires: coreutils, util-linux, gawk
# for basename, getopt, awk, etc

### Build Dependencies ###

BuildRequires: gcc-c++
BuildRequires: libxslt-devel

%description
Rarian is a documentation meta-data library that allows access to documents,
man pages and info pages.  It was designed as a replacement for scrollkeeper.

%package compat
License: GPLv2+
Summary: Extra files for compatibility with scrollkeeper
Requires: rarian = %{version}-%{release}
Requires(post): rarian
# The scrollkeeper version is arbitrary.  It just
# needs to be greater than what we're obsoleting.
Provides: scrollkeeper = 0.4
Obsoletes: scrollkeeper <= 0.3.14

%description compat
This package contains files needed to maintain backward-compatibility with
scrollkeeper.

%package devel
Summary: Development files for Rarian
Requires: rarian = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains files required to develop applications that use the
Rarian library ("librarian").

%prep
%setup -q
%patch 1 -p1 -b .categories

%build
%configure --disable-skdb-update
%make_build

%install
%make_install

mkdir -p %buildroot%{_datadir}/xml/scrollkeeper/dtds
cp %{SOURCE1} %buildroot%{_datadir}/xml/scrollkeeper/dtds

rm -rf %buildroot%{_libdir}/librarian.a
rm -rf %buildroot%{_libdir}/librarian.la

%ldconfig_scriptlets

%post compat
%{_bindir}/rarian-sk-update

# Add OMF DTD to XML catalog.
CATALOG=/etc/xml/catalog
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
  "https://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
  "https://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :

%postun compat

# Delete OMF DTD from XML catalog.
if [ $1 = 0 ]; then
  CATALOG=/etc/xml/catalog
  /usr/bin/xmlcatalog --noout --del \
    "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
fi

%files
%license COPYING COPYING.LIB COPYING.UTILS
%doc README ChangeLog NEWS AUTHORS
%{_bindir}/rarian-example
%{_libdir}/librarian.so.*
%{_datadir}/librarian
%{_datadir}/help

%files compat
%{_bindir}/rarian-sk-*
%{_bindir}/scrollkeeper-*
%{_datadir}/xml/scrollkeeper

%files devel
%{_includedir}/rarian
%{_libdir}/librarian.so
%{_libdir}/pkgconfig/rarian.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.1-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.8.1-21
- Add gcc-c++ as BR
- spec cleanup

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.1-13
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-3
- Shorten the summary.

* Mon Nov 10 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-2
- Add patch for RH bug #453342 (OMF category parsing).

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.0-2
- Fix source url

* Mon Feb 18 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.0-1
- Update to 0.8.0
- Silence xmlcatalog commands (RH bug #433315).

* Mon Feb 18 2008 Matthew Barnes <mbarnes@redhat.com> - 0.7.1-3
- Require libxml2 in %%post and %%postun (RH bug #433268).

* Sat Feb 09 2008 Matthew Barnes <mbarnes@redhat.com> - 0.7.1-2
- Install XML DTD for scrollkeeper OMF files (RH bug #431088).

* Tue Jan 08 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Nov 26 2007 Matthew Barnes <mbarnes@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Tue Nov 06 2007 Matthew Barnes <mbarnes@redhat.com> - 0.6.0-2
- Own /usr/share/help (RH bug #363311).

* Wed Sep 12 2007 Matthew Barnes <mbarnes@redhat.com> - 0.6.0-1
- Update to 0.6.0
- Remove patch for RH bug #254301 (fixed upstream).

* Thu Aug 30 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-3
- Add patch for RH bug #254301 (rarian-sk-config --omfdir).

* Wed Aug 22 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-2
- Mass rebuild

* Mon Aug 13 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-1
- Update to 0.5.8

* Thu Aug  9 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.6-5
- Move Provides and Obsoletes in the same package, to
  avoid unnessary complications

* Sat Aug  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.6-4
- Add a few missing Requires

* Thu Aug 02 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-3
- Fix the Obsoletes/Provides relationship.

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-2
- More package review feedback (#250150).

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-1
- Update to 0.5.6

* Tue Jul 31 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.4-2
- Incorporate package review suggestions.

* Mon Jul 30 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.4-1
- Initial packaging.
