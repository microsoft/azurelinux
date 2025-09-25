Name: rarian
Version: 0.8.6
Release: 2%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License: LGPL-2.1-or-later AND Zlib
Summary: Documentation meta-data library
URL: https://rarian.freedesktop.org/
Source: https://gitlab.freedesktop.org/rarian/rarian/-/releases/%{version}/downloads/assets/rarian-%{version}.tar.bz2
Source1: scrollkeeper-omf.dtd

### Dependencies ###

Requires(post): libxml2
Requires(postun): libxml2
# for /usr/bin/xmlcatalog

Requires: libxslt
# for /usr/bin/xsltproc
Requires: coreutils, util-linux, gawk
# for basename, getopt, awk, etc

### Build Dependencies ###

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: check-devel
BuildRequires: tinyxml2-devel
# Used by the tests
BuildRequires: man-db
BuildRequires: info
BuildRequires: man-pages

%description
Rarian is a documentation meta-data library that allows access to documents,
man pages and info pages.  It was designed as a replacement for scrollkeeper.

%package compat
License: GPL-2.0-or-later
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
License: LGPL-2.1-or-later AND Zlib
Requires: rarian = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains files required to develop applications that use the
Rarian library ("librarian").

%prep
%setup -q

%build
%configure --disable-skdb-update
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%check
make VERBOSE=1 check

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
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
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
* Fri Mar 07 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.8.6-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Sat Dec 14 2024 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.6-1
- Update to rarian 0.8.6.
- Fixes: rhbz#2326394
- Changes to use tinyxml2 instead of tinyxml.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 09 2023 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.5-1
- Update to 0.8.5. Fixes rhbz#2251261.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat May 06 2023 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.4-1
- Upgrade to 0.8.4.

* Wed Feb 22 2023 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.2-1
- Update to 0.8.2 (fixes crash rhbz#2123124)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Florian Weimer <fweimer@redhat.com> - 0.8.1-43
- C99 compatibility fix

* Wed Nov 23 2022 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.1-42
- Convert to using rpmautospec.

* Wed Nov 23 2022 Troy Curtis Jr <troy@troycurtisjr.com> - 0.8.1-41
- SPDX migration.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 25 2021 Yago Rubio Sanfiz <iagorubio@fedoraproject.org> - 0.8.1-38
- Make sure RPATH is stripped to resolve FTBFS (rhbz 1987917).

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> - 0.8.1-35
- Add BuildRequires: make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-34
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.1-29
- Remove obsolete Group tag

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.1-28
- Remove obsolete ldconfig scriptlets

* Tue Jul 17 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 0.8.1-27
- add gcc-c++ as BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Jason Tibbitts <tibbs@math.uh.edu> - 0.8.1-25
- Remove needless use of %%defattr

* Mon Jul 09 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.8.1-24
- add BuildRequires: gcc

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.1-23
- Remove %%clean section

* Tue Feb 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.1-22
- Remove BuildRoot definition

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-20
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 0.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.1-15
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Dennis Gilmore <dennis@ausil.us> - 0.8.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 0.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 0.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- dist-git conversion

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 0.8.1-6
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Jul 27 2009 Jesse Keating <jkeating@fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Jesse Keating <jkeating@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.8.1-3
- Shorten the summary.

* Tue Nov 11 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.8.1-2
- Add patch for RH bug #453342 (OMF category parsing).

* Tue Sep 02 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 0.8.0-2
- fix source url

* Mon Mar 10 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 - Silence xmlcatalog commands (RH bug #433315).

* Mon Feb 18 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.7.1-3
- Require libxml2 in %%post and %%postun (RH bug #433268).

* Sun Feb 10 2008 Matthew Barnes <mbarnes@fedoraproject.org> - 0.7.1-2
- Install XML DTD for scrollkeeper OMF files (RH bug #431088).

* Tue Jan 08 2008 Bastien Nocera <hadess@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Tue Nov 27 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.7.0-2
- Forget to commit sources again.

* Tue Nov 27 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Tue Nov 06 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.6.0-2
- Own /usr/share/help (RH bug #363311).

* Wed Sep 12 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 - Remove patch for RH bug #254301 (fixed upstream).

* Thu Aug 30 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.8-4
- Add patch for RH bug #254301 (rarian-sk-config --omfdir).

* Thu Aug 30 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.8-3
- Add patch for RH bug #254301 (rarian-sk-config --omfdir).

* Wed Aug 22 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.8-2
- Mass rebuild

* Tue Aug 14 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.8-1
- Update to 0.5.8

* Thu Aug 09 2007 Matthias Clasen <mclasen@fedoraproject.org> - 0.5.6-4
- move provides

* Sun Aug 05 2007 Matthias Clasen <mclasen@fedoraproject.org> - 0.5.6-3
- add a few missing requires

* Thu Aug 02 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.6-2
- Fix the Obsoletes/Provides relationship.

* Thu Aug 02 2007 Matthew Barnes <mbarnes@fedoraproject.org> - 0.5.6-1
- More package review feedback (#250150).
