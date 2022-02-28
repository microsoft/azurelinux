%define _module_build 1

Summary: SGML and XML parser
Name: opensp
Version: 1.5.2
Release: 35%{?dist}
Requires: sgml-common >= 0.5
Provides: bundled(gettext) = 0.14.5
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://openjade.sourceforge.net/
Source: http://download.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
Patch0: opensp-multilib.patch
Patch1: opensp-nodeids.patch
Patch2: opensp-sigsegv.patch
Patch3: opensp-manpage.patch
License: MIT

BuildRequires:  gcc-c++

%if ! 0%{?_module_build}
BuildRequires: xmlto, jadetex
%endif

%description
OpenSP is an implementation of the ISO/IEC 8879:1986 standard SGML
(Standard Generalized Markup Language). OpenSP is based on James
Clark's SP implementation of SGML. OpenSP is a command-line
application and a set of components, including a generic API.

%package devel
Summary: Files for developing applications that use OpenSP
Requires: %{name} = %{version}-%{release}

%description devel
Header files and libtool library for developing applications that use OpenSP.


%prep
%setup -q -n OpenSP-%{version}
%patch0 -p1 -b .multilib
%patch1 -p1 -b .nodeids
%patch2 -p1 -b .sigsegv
%patch3 -p1 -b .manpage
# convert files to UTF-8
iconv -f latin1 -t utf8 ChangeLog -o ChangeLog.tmp
mv -f ChangeLog.tmp ChangeLog

# ensure that applying the above patches doesn't cause lib/parser_inst.cxx to
# be regenerated

touch lib/parser_inst.cxx

%build
%configure \
%if 0%{?_module_build}
 --disable-doc-build \
%endif
 --disable-dependency-tracking --disable-static --enable-http \
 --enable-default-catalog=%{_sysconfdir}/sgml/catalog \
 --enable-default-search-path=%{_datadir}/sgml:%{_datadir}/xml
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Get rid of libtool libraries
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# oMy, othis ois osilly.
for file in nsgmls sgmlnorm spam spent sx ; do
   ln -s o$file $RPM_BUILD_ROOT%{_bindir}/$file
%if ! 0%{?_module_build}
   echo ".so man1/o${file}.1" > $RPM_BUILD_ROOT%{_mandir}/man1/${file}.1
%endif
done

#
# Rename sx to sgml2xml.
mv $RPM_BUILD_ROOT%{_bindir}/sx $RPM_BUILD_ROOT%{_bindir}/sgml2xml
%if ! 0%{?_module_build}
mv $RPM_BUILD_ROOT%{_mandir}/man1/{sx,sgml2xml}.1
%endif

#
# Clean out (installed) redundant copies of the docs and DTDs.
rm -rf $RPM_BUILD_ROOT%{_docdir}/OpenSP
rm -rf $RPM_BUILD_ROOT%{_datadir}/OpenSP

%find_lang sp5


%check
make check || : # TODO: failures as of 1.5.2 :(


%ldconfig_scriptlets


%files -f sp5.lang
%if ! 0%{?_module_build}
%doc doc/*.htm
%doc docsrc/releasenotes.html
%endif
%doc AUTHORS BUGS COPYING ChangeLog NEWS README
%doc pubtext/opensp-implied.dcl
%{_bindir}/*
%{_libdir}/libosp.so.*
%if ! 0%{?_module_build}
%{_mandir}/man1/*.1*
%endif

%files devel
%{_includedir}/OpenSP/
%{_libdir}/libosp.so


%changelog
* Mon Jan 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.5.2-35
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Enable module build to remove doc dependencies

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Ondrej Vasik <ovasik@redhat.com> - 1.5.2-31
- add note about bundled old gettext library

* Sat Jul 21 2018 Ondrej Vasik <ovasik@redhat.com> - 1.5.2-30
- BuildRequires: gcc-c++ (#1605338)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Nils Philippsen <nils@redhat.com> - 1.5.2-25
- don't regenerate lib/parser_inst.cxx, this would require perl as a build
  dependency

* Mon Apr 24 2017 Nils Philippsen <nils@redhat.com> - 1.5.2-25
- don't build documentation during modular build
- fix bogus changelog date

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.2-21
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Ondrej Vasik <ovasik@redhat.com> - 1.5.2-18
- fix the inconsistency between man page and help (#854941)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 24 2008 Ondrej Vasik <ovasik@redhat.com> 1.5.2-10
- move conversion to prep, do not convert html doc(#226217)

* Thu Oct 23 2008 Ondrej Vasik <ovasik@redhat.com> 1.5.2-9
- convert doc files to UTF-8 (#226217)

* Wed Oct 22 2008 Ondrej Vasik <ovasik@redhat.com> 1.5.2-8
- merge review by V.Skyttä (#226217), changed license to
  MIT, dropped .la, adjusted comments

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> 1.5.2-7
- gcc43 rebuild

* Mon Aug 27 2007 Ondrej Vasik <ovasik@redhat.com> 1.5.2-6
- License tag change to BSD
- Rebuilt for F8

* Thu Jun 21 2007 Ondrej Vasik <ovasik@redhat.com> 1.5.2-5
- fixed SIGSEGV (bug #245104)

* Mon Feb 12 2007 Tim Waugh <twaugh@redhat.com> 1.5.2-4
- Fixed build root.
- Give IDs to nodes in the release notes source to prevent releasenotes.html
  having multilib conflicts (bug #228320).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-3.1
- rebuild

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1.5.2-3
- Fixed multilib fix (bug #194702).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 1.5.2-2
- Fixed multilib devel conflicts (bug #192741).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com>  1.5.2-1
- 1.5.2.

* Wed Dec 14 2005 Tim Waugh <twaugh@redhat.com>  1.5.1-2
- Backported patch from 1.5.2pre1 to fix ArcEngine crash.

* Tue Dec 13 2005 Tim Waugh <twaugh@redhat.com>  1.5.1-1
- Back down to 1.5.1 for now.
- Fixes for GCC4.1.

* Sun Dec  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.5.2-0.1.pre1
- Fix build dependencies.
- Require exact version of main package in -devel.
- Build with dependency tracking disabled.
- Add %%{_datadir}/xml to default search path.
- Run test suite during build.
- Add URL tag.
- Use %%find_lang.
- Cosmetic improvements.

* Tue Nov 29 2005 Terje Bless <link@pobox.com> 1.5.2-0.pre1
- New package OpenSP.

