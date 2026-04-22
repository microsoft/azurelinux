# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: xmlto
Version: 0.0.29
Release: 4%{?dist}
Summary: A tool for converting XML files to various formats

License: GPL-2.0-or-later
URL: https://pagure.io/xmlto/
Source0: https://pagure.io/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: docbook-xsl
BuildRequires: libxslt
BuildRequires: util-linux, flex
BuildRequires: gcc
BuildRequires: autoconf
BuildRequires: automake

# We rely heavily on the DocBook XSL stylesheets!
Requires: docbook-xsl
Requires: libxslt
Requires: docbook-dtds
Requires: util-linux, flex

%description
This is a package for converting XML files to various formats using XSL
stylesheets.

%package tex
License: GPL-2.0-or-later
Summary: A set of xmlto backends with TeX requirements
# For full functionality, we need passivetex.
Requires: tex-passivetex
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch

%description tex
This subpackage contains xmlto backend scripts which do require
PassiveTeX/TeX for functionality.

%package xhtml
License: GPL-2.0-or-later
Summary: A set of xmlto backends for xhtml1 source format
# For functionality we need stylesheets xhtml2fo-style-xsl
Requires: xhtml2fo-style-xsl
# We require main package
Requires: xmlto = %{version}-%{release}
BuildArch: noarch

%description xhtml
This subpackage contains xmlto backend scripts for processing
xhtml1 source format.

%prep
%autosetup -n %{name}-%{version} -p1

autoreconf -i -v

%build
%configure BASH=/bin/bash
%make_build

%check
make check

%install
%make_install

%files
%license COPYING
%doc ChangeLog README.md AUTHORS.md NEWS.md
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto
%exclude %{_datadir}/xmlto/format/fo/dvi
%exclude %{_datadir}/xmlto/format/fo/ps
%exclude %{_datadir}/xmlto/format/fo/pdf
%exclude %dir %{_datadir}/xmlto/format/xhtml1/
%exclude %{_datadir}/xmlto/format/xhtml1

%files tex
%{_datadir}/xmlto/format/fo/dvi
%{_datadir}/xmlto/format/fo/ps
%{_datadir}/xmlto/format/fo/pdf

%files xhtml
%dir %{_datadir}/xmlto/format/xhtml1/
%{_datadir}/xmlto/format/xhtml1/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jun 11 2024 Ondrej Sloup <osloup@redhat.com> - 0.0.29-1
- Rebase to the latest upstream version

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 0.0.28-25
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 23 2023 Ondrej Sloup <osloup@redhat.com> - 0.0.28-22
- Update license tag to the SPDX format

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 24 2022 Florian Weimer <fweimer@redhat.com> - 0.0.28-19
- Apply upstream patches to support building in stricer C99 mode

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Ondrej Vasik <ovasik@redhat.com> - 0.0.28-10
- add BuildRequires for gcc (#1606744)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Than Ngo <than@redhat.com> - 0.0.28-8
- use the passivetex from texlive

* Mon Jul 02 2018 Ondrej Vasik <ovasik@redhat.com> - 0.0.28-7
- upstream moved to pagure.io/xmlto (#1502443)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Ondrej Vasik <ovasik@redhat.com> 0.0.28-1
- New version 0.0.28
- fix broken temp files removal
- do not detect links browser as elinks

* Tue Nov 10 2015 Ondrej Vasik <ovasik@redhat.com> 0.0.27-1
- New version 0.0.27
- remove several bashisms in scripts
- add new option --profile for preprocessing documents
  with profiling stylesheet
- fix several potential crashes in xmlif (found by static analysis)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 05 2014 Ondrej Vasik <ovasik@redhat.com> - 0.0.26-1
- New version 0.0.26
- fix build with automake 1.13+
- fix warning in searchpath option

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 09 2013 Ondrej Vasik <ovasik@redhat.com> - 0.0.25-6
- drop hard requirement for text-www-browser (any package that
  needs docbook->txt for build  may buildrequire any of
  w3m/lynx/elinks as suggested by script)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Ondrej Vasik <ovasik@redhat.com> - 0.0.25-3
- fix the noextensions option (#830266)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.25-1
- fix handling of external data objects with fop
  (deb #568894)

* Tue Nov 29 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.24-2
- fix the functionality of fop.extensions (#757035)

* Thu Jul 14 2011 Ondrej Vasik <ovasik@redhat.com> - 0.0.24-1
- new release 0.0.24, basic support for docbook->epub
  conversion, use backend extensions by default
  (--noextensions) to disable it

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 13 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-3
- workaround passivetex limitation for chapter titles starting
  with L(#526273)

* Thu Sep 24 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-2
- ensure the default shell is /bin/bash instead of /bin/sh

* Mon Sep 21 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.23-1
- New version 0.0.23
- added autodetection for more common tools like
  gnu cp or tail
- added option --noautosize to prevent overriding
  of user-defined or system-default paper size
- use shell built-in 'type -t' instead of 'which'
  utility for detection of file availability

* Sat Aug 01 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.22-3
- make subpackages noarch, preserve timestamps - merge
  review (#226568)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 25 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.22-1
- New version 0.0.22
- autodetection for tools/program paths, consolidated
  error code handling, build warnings cleanup

* Mon Mar 16 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-9
- reenable noent switch - bug is on lcdproc side
- add xhtml support(subpackage) (#145140)

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-8
- temporarily disable noent switch - blocks lcdproc doc build
  (#488093)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-6
- fix cleaning up of temporary files with libpaper(Debian)
- fix xmllint postvalid (added noent option), use nonet
  switch

* Mon Jan 05 2009 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-5
- fix stringparam option functionality

* Tue Dec 16 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-4
- merge review(#226568)
  correct doc filelist attributes, add License GPL+ for xmlif

* Fri Dec 12 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-3
- merge review(#226568):
  ship documentation files, fix license tag, use recommended
  parallel make, make install instead of macro, require libxslt
  instead of direct binary requirement

* Fri Jul 11 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-2
- xmlto-tex subpackage to prevent requirements for
  passivetex/tex for all backends(#454341)

* Fri Jun 20 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.21-1
- new version 0.0.21

* Tue May 13 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-3
- fixed errorneus handling of backend stylesheet(#446092)
- removed unused patches

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-2
- gcc4.3 rebuild

* Thu Jan 17 2008 Ondrej Vasik <ovasik@redhat.com> - 0.0.20-1
- new version 0.0.20
- added experimental fop support(additional output formats)
- possibility to read stylesheet from STDIN, using recursive
  cp in docbook formats, updated man pages

* Wed Nov 28 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.19-1
- new version 0.0.19
- added dist tag

* Fri Oct 12 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-17
- generalized text-www-browser requirements(#174566)

* Mon Oct  8 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-16
- fixed warning message from find in usage() display(#322121)

* Wed Sep 19 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-15
- fixed wrong source URL

* Thu Aug 23 2007 Ondrej Vasik <ovasik@redhat.com> - 0.0.18-14
- rebuilt for F8
- changed License tag to GPLv2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-13.1
- rebuild

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-13
- Removed debugging.

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-12
- Debug build.

* Thu Jun  8 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-11
- Rebuilt.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 0.0.18-10
- Rebuilt.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-9.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.0.18-9.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug  8 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-9
- Fixed quoting in scripts (bug #165338).

* Mon Aug  1 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-8
- Requires w3m (bug #164798).

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-7
- Rebuild for new man-pages stylesheet.

* Mon Apr  4 2005 Tim Waugh <twaugh@redhat.com>
- Requires util-linux and flex, as does the build.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-6
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 0.0.18-5
- Rebuilt.

* Thu Jul  1 2004 Tim Waugh <twaugh@redhat.com> 0.0.18-4
- Magic encoding is enabled again (bug #126921).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 21 2004 Tim Waugh <twaugh@redhat.com> 0.0.18-1
- 0.0.18.

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 0.0.17-1
- 0.0.17.

* Tue Nov 18 2003 Tim Waugh <twaugh@redhat.com> 0.0.16-1
- 0.0.16.

* Tue Oct  7 2003 Tim Waugh <twaugh@redhat.com> 0.0.15-1
- 0.0.15.

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without tetex(passivetex) dependency

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 0.0.14-3
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Tim Waugh <twaugh@redhat.com> 0.0.14-1
- 0.0.14.

* Sun May 11 2003 Tim Waugh <twaugh@redhat.com> 0.0.13-1
- 0.0.13.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan  3 2003 Tim Waugh <twaugh@redhat.com> 0.0.12-2
- Disable magic encoding detection, since the stylesheets don't handle
  it well at all (bug #80732).

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.12-1
- 0.0.12.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 0.0.11-1
- 0.0.11.
- xmlto.mak no longer needed.
- CVS patch no longer needed.
- Update docbook-xsl requirement.
- Ship xmlif.
- Run tests.
- No longer a noarch package.

* Tue Jul  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-4
- Ship xmlto.mak.

* Thu Jun 27 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-3
- Some db2man improvements from CVS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.0.10-2
- automated rebuild

* Tue Jun 18 2002 Tim Waugh <twaugh@redhat.com> 0.0.10-1
- 0.0.10.
- No longer need texinputs patch.

* Tue Jun 18 2002 Tim Waugh <twaugh@redhat.com> 0.0.9-3
- Fix TEXINPUTS problem with ps and dvi backends.

* Thu May 23 2002 Tim Powers <timp@redhat.com> 0.0.9-2
- automated rebuild

* Wed May  1 2002 Tim Waugh <twaugh@redhat.com> 0.0.9-1
- 0.0.9.
- The nonet patch is no longer needed.

* Fri Apr 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-3
- Don't fetch entities over the network.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-2
- Rebuild in new environment.

* Tue Feb 12 2002 Tim Waugh <twaugh@redhat.com> 0.0.8-1
- 0.0.8.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 0.0.7-2
- Require the DocBook DTDs.

* Mon Jan 21 2002 Tim Waugh <twaugh@redhat.com> 0.0.7-1
- 0.0.7 (bug #58624, bug #58625).

* Wed Jan 16 2002 Tim Waugh <twaugh@redhat.com> 0.0.6-1
- 0.0.6.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.0.5-4
- automated rebuild

* Wed Jan  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-3
- 0.0.6pre2.

* Wed Jan  9 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-2
- 0.0.6pre1.

* Tue Jan  8 2002 Tim Waugh <twaugh@redhat.com> 0.0.5-1
- 0.0.5.

* Mon Dec 17 2001 Tim Waugh <twaugh@redhat.com> 0.0.4-2
- 0.0.4.
- Apply patch from CVS to fix silly typos.

* Sat Dec  8 2001 Tim Waugh <twaugh@redhat.com> 0.0.3-1
- 0.0.3.

* Wed Dec  5 2001 Tim Waugh <twaugh@redhat.com>
- Built for Red Hat Linux.

* Fri Nov 23 2001 Tim Waugh <twaugh@redhat.com>
- Initial spec file.
