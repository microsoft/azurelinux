Summary:        A DSSSL implementation
Name:           openjade
Version:        1.3.2
Release:        64%{?dist}
License:        DMIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://openjade.sourceforge.net/
Source:         https://download.sourceforge.net/openjade/openjade-%{version}.tar.gz
#config.sub and config.guess from upstream sources (Mar 25th 2013).
#https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD
#https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD
#I can't get them from autoreconf, because of the very strange openjade structure of config files
Source2:        config.guess
Source3:        config.sub
#fix build on ppc64
Patch0:         openjade-ppc64.patch
#do not link against -lnsl
Patch1:         openjade-1.3.1-nsl.patch
#Fix dependent libs for libogrove (bug #198232).
Patch2:         openjade-deplibs.patch
#do not require OpenSP libosp.la file for build(#485114)
Patch3:         openjade-nola.patch
#upstream bug tracker fix for build with gcc46
Patch4:         openjade-1.3.2-gcc46.patch
#use Getopt:Std to prevent build failure
Patch5:         openjade-getoptperl.patch
BuildRequires:  gcc-c++
BuildRequires:  opensp-devel
BuildRequires:  perl-interpreter
Requires:       sgml-common
#Last jade version is from Red Hat 6.2
Provides:       jade = %{version}-%{release}

%description
OpenJade is an implementation of the ISO/IEC 10179:1996 standard DSSSL
(Document Style Semantics and Specification Language). OpenJade is
based on James Clark's Jade implementation of DSSSL. OpenJade is a
command-line application and a set of components. The DSSSL engine
inputs an SGML or XML document and can output a variety of formats:
XML, RTF, TeX, MIF (FrameMaker), SGML, or XML.

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1 -b .deplibs
%patch 3 -p1 -b .nola
%patch 4 -p1 -b .gcc46
%patch 5 -p1 -b .getopt


%build
cp -p %{SOURCE2} %{SOURCE3} config/
# more info: rhbz#1306162
export CXXFLAGS="%{optflags} -fno-lifetime-dse"
%configure --disable-static --datadir=%{_datadir}/sgml/%{name}-%{version} \
	--enable-splibdir=%{_libdir}
make


%install

make install install-man DESTDIR=%{buildroot}

# oMy, othis ois osilly.
ln -s openjade %{buildroot}/%{_bindir}/jade
echo ".so man1/openjade.1" > %{buildroot}/%{_mandir}/man1/jade.1

# install jade/jade $RPM_BUILD_ROOT/%{prefix}/bin/jade
cp dsssl/catalog %{buildroot}/%{_datadir}/sgml/%{name}-%{version}/
cp dsssl/{dsssl,style-sheet,fot}.dtd %{buildroot}/%{_datadir}/sgml/%{name}-%{version}/

# add unversioned/versioned catalog and symlink
mkdir -p %{buildroot}%{_sysconfdir}/sgml
cd %{buildroot}%{_sysconfdir}/sgml
touch %{name}-%{version}-%{release}.soc
ln -s %{name}-%{version}-%{release}.soc %{name}.soc
cd -

rm -f $RPM_BUILD_ROOT%{_libdir}/*.so $RPM_BUILD_ROOT%{_libdir}/*.la

%post
%{?ldconfig}
%{_bindir}/install-catalog --add %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/sgml/%{name}-%{version}/catalog >/dev/null 2>/dev/null || :

%preun
%{_bindir}/install-catalog --remove %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/sgml/%{name}-%{version}/catalog >/dev/null 2>/dev/null || :

%ldconfig_postun

%files
%doc jadedoc/* dsssl/README.jadetex
%license COPYING
%doc README VERSION
%ghost %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc
%{_sysconfdir}/sgml/%{name}.soc
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/*/*
%{_datadir}/sgml/%{name}-%{version}

%changelog
* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 1.3.2-64
- Moved from SPECS-EXTENDED to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-63
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Ondrej Vasik <ovasik@redhat.com> - 1.3.2-59
- BuildRequires for gcc-c++ (#1605320)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Ondrej Vasik <ovasik@redhat.com> - 1.3.2-57
- License should be DMIT actually

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.3.2-52
- Add BuildRequires: perl

* Mon Feb 15 2016 Pavel Raiskup <praiskup@redhat.com> - 1.3.2-51
- using -fno-lifetime-dse instead of -ftree-dse (rhbz#1306162)

* Thu Feb 11 2016 Pavel Raiskup <praiskup@redhat.com> - 1.3.2-50
- temporarily disable -ftree-dse optimization (rhbz#1306162)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.3.2-47
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Ondrej Vasik <ovasik@redhat.com> 1.3.2-43
- Use upstream config.sub and config.guess to support aarch64(#926278)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Ondrej Vasik <ovasik@redhat.com> 1.3.2-41
- avoid build failure with using Getopt::Std;

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 08 2011 Ondrej Vasik <ovasik@redhat.com> 1.3.2-38
- fix build with gcc46 (upstream bug tracker)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 10 2009 Ondrej Vasik <ovasik@redhat.com> 1.3.2-36
- Merge Review (#226213) - added url, fixed rpmlint warnings,
  no macros in changelog

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> 1.3.2-34
- disable parallel build (culprit of build failure)
  - https://bugs.gentoo.org/181651

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 25 2008 Ondrej Vasik <ovasik@redhat.com> 1.3.2-32
- do not require OpenSP libosp.la file for build(#485114)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> 1.3.2-31
- gcc43 rebuild

* Mon Aug 27 2007 Ondrej Vasik <ovasik@redhat.com> 1.3.2-30
- changed license tag to BSD
- rebuilt for F8

* Mon Jul 23 2007 Ondrej Vasik <ovasik@redhat.com> 1.3.2-29
- improved dependent libs patch (bug #237500)
- same done for libospgrove.so

* Fri Feb  9 2007 Tim Waugh <twaugh@redhat.com> 1.3.2-28
- Don't ship .so or .la files (bug #203635).
- Added dist tag to release.
- Fixed summary.
- Fixed build root.
- Removed prefix tag.

* Mon Jul 17 2006 Tim Waugh <twaugh@redhat.com> 1.3.2-27
- Rebuilt.

* Mon Jul 10 2006 Tim Waugh <twaugh@redhat.com> 1.3.2-26
- Fix dependent libs for libogrove (bug #198232).

* Mon Jun 26 2006 Florian La Roche <laroche@redhat.com> 1.3.2-25
- add redirection to /dev/null for preun

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1.3.2-24
- Rebuild against opensp.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.2-23.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.2-23.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan  6 2006 Tim Waugh <twaugh@redhat.com> 1.3.2-23
- Rebuild against new opensp.

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 1.3.2-22
- Fix SOC files.
- Quieten scriptlets.

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 1.3.2-21
- Fix location of catalog.

* Tue Dec 13 2005 Tim Waugh <twaugh@redhat.com> 1.3.2-20
- Use --enable-splibdir to prevent ambiguity.
- Move 'install-catalog --remove' to %%preun section (bug #60409).

* Thu Dec  8 2005 Terje Bless <link@pobox.com> - 1.3.2-19
- Drop -devel subpackage.

* Sun Dec  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.3.2-18
- Really BuildRequire opensp-devel.
- Clean up unneeded build dependencies and configure options.
- Drop dependency on docbook-dtds.
- Fix %%post(un) syntax and catalog installation.

* Wed Nov 30 2005 Terje Bless <link@pobox.com> 1.3.2-17
- Split opensp out into its own package.
- BuildRequire OpenSP-devel, Require OpenSP.
- Drop openjade-1.3.1-manpage.patch (it patches opensp, not openjade, and is
  obsolete with external opensp).

* Tue Mar  1 2005 Tim Waugh <twaugh@redhat.com> 1.3.2-16
- Rebuilt for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1.3.2-15
- Rebuilt.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1.3.2-14
- Build requires gettext-devel (bug #134672).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 19 2004 Tim Waugh <twaugh@redhat.com> 1.3.2-11.2
- Rebuilt.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 31 2004 Tim Waugh <twaugh@redhat.com> 1.3.2-10
- More C++ fixes (for GCC 3.4).

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-9
- No longer need httphost patch.

* Mon Oct 20 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-8
- Rebuilt.

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de> 1.3.2-7
- do not link against -lnsl

* Thu Aug  7 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-6
- Rebootstrap to create a libtool that actually works.

* Wed Aug  6 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-5
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 1.3.2-4
- rebuilt

* Thu May 22 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-3
- Fixes for GCC 3.3.
- Use --parents for %%doc.

* Tue Mar 18 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-2
- Provide sgml2xml man page (bug #83759).
- Add devel subpackage.

* Fri Mar 14 2003 Tim Waugh <twaugh@redhat.com> 1.3.2-1
- OpenSP 1.5, openjade 1.3.2.
- Renumber patches.

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 1.3.1-13
- Add openjade-ppc64.patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 1.3.1-11
- don't include -debuginfo files in package.

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com>
- Fix typo in description (bug #79395).

* Mon Nov  4 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-10
- Fix DTD retrieval from virtual hosts (bug #77137).

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 1.3.1-8
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.3.1-7
- automated rebuild

* Thu Jun 13 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-6
- Fix sgmlnorm(1) man page (bug #64136).
- Fix %%files list (bug #64323).

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.3.1-5
- automated rebuild

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-4
- Avoid bad triggers.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-3
- Rebuild in new environment.

* Mon Jan 28 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-2
- Ship man pages.

* Mon Jan 28 2002 Tim Waugh <twaugh@redhat.com> 1.3.1-1
- 1.3.1.
- Patches no longer needed: decl, strdup, foo, size_t, 31525, indev,
  ligature, twosidestartonright.
- Updated lt patch.

* Mon Jan 14 2002 Tim Waugh <twaugh@redhat.com> 1.3-22
- Enable build on GCC 3.0 onwards.
- Run libtoolize.

* Fri Nov  2 2001 Tim Waugh <twaugh@redhat.com> 1.3-21
- Enable HTTP support.  Now a DocBook XML document can be processed by
  either xsltproc or openjade.

* Tue Oct 30 2001 Tim Waugh <twaugh@redhat.com> 1.3-20
- Apply twosidestartonright patch from Ian Castle.

* Thu Oct 11 2001 Tim Waugh <twaugh@redhat.com> 1.3-19
- s/Copyright:/License:/
- Use %%{_tmppath}.
- Fix up libtool libraries (bug #46212).

* Wed Sep 12 2001 Tim Powers <timp@redhat.com> 1.3-18
- rebuild with new gcc and binutils

* Fri Jun 15 2001 Tim Waugh <twaugh@redhat.com> 1.3-17
- Apply patch from CVS to break up unintentional ligatures (bugs #11497,
  #11779)

* Mon Jun  4 2001 Tim Waugh <twaugh@redhat.com> 1.3-16
- Apply the iNdev openjade-1.3.patch patch.

* Tue May 29 2001 Tim Waugh <twaugh@redhat.com> 1.3-15
- ldconfig (bug #32824).
- Fix up some libtool problems.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com> 1.3-14
- rebuild for C++ exception handling on ia64
- build with optimization on ia64

* Tue Mar 13 2001 Tim Waugh <twaugh@redhat.com>
- Avoid creating bogus TeX output for section headings containing
  special characters (#bug 31525).

* Mon Jan 22 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- Apply original autoconf patch to s390 s390x only. This patch can
  be deleted once s390* uses a current compiler.

* Thu Jan 19 2001 Tim Waugh <twaugh@redhat.com>
- Don't conflict with stylesheets; require sgml-common >= 0.5 instead.
- Revert autoconf change, as it's still broken.

* Wed Jan 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix this autoconf macro to work on all archs :-)

* Wed Jan 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- apply patch from Fritz Elfert <felfert@to.com>
	- removed explicit stripping
	- Added autoconf macro for correctly recognizing if size_t
	  is unsigned int

* Tue Jan 16 2001 Tim Waugh <twaugh@redhat.com>
- Default catalog file is /etc/sgml/catalog.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Conflict with stylesheets (new-trials location changes).
- /usr/lib/sgml -> /usr/share/sgml/%%{name}-%%{version}.
- Remove %%post and %%postun.

* Wed Oct 18 2000 Matt Wilson <msw@redhat.com>
- rebuilt against g++-2.96-60, fixes jade on alpha

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Wed May 31 2000 Matt Wilson <msw@redhat.com>
- fix several C++ build problems (declarations)
- build against new libstdc++

* Wed May 17 2000 Matt Wilson <msw@redhat.com>
- build with -O0 on alpha
- fix -j testing

* Thu May  5 2000 Bill Nottingham <notting@redhat.com>
- openjade is maintained, and actually builds. Let's try that.

* Thu Mar  9 2000 Bill Nottingham <notting@redhat.com>
- this package is way too huge. strip *everything*

* Mon Feb 21 2000 Matt Wilson <msw@redhat.com>
- build with CXXFLAGS="-O2 -ggdb" to work around segfault on alpha

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- strip binaries

* Wed Jan  5 2000 Bill Nottingham <notting@redhat.com>
- sanitize spec file some

* Tue Aug 17 1999 Tim Powers <timp@redhat.com>
- fixed conflict problem with sgml-tools

* Sat Jul 17 1999 Tim Powers <timp@redhat.com>
- changed buildroot path to /var/tmp
- rebuilt for 6.1

* Fri Apr 23 1999 Michael K. Johnson <johnsonm@redhat.com>
- quiet scripts

* Thu Apr 23 1999 Owen Taylor <otaylor@redhat.com>
- Made requires for sgml-common into prereq
