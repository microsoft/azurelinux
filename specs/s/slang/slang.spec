# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora:1}
%bcond_without oniguruma
%else
%bcond_with oniguruma
%endif

Summary:	Shared library for the S-Lang extension language
Name:		slang
Version:	2.3.3
Release: 9%{?dist}
License:	GPL-2.0-or-later
URL:		https://www.jedsoft.org/slang/
Source:		https://www.jedsoft.org/releases/%{name}/%{name}-%{version}.tar.bz2
# disable test that fails with SIGHUP ignored (e.g. in koji)
Patch2:		slang-sighuptest.patch
BuildRequires: make
BuildRequires:	gcc libpng-devel zlib-devel
%{?with_oniguruma:BuildRequires: oniguruma-devel}
# static removed in 2.3.1a-3
Obsoletes:	 slang-static < 2.3.1a-3

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package slsh
Summary:	Interpreter for S-Lang scripts
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description slsh
slsh (slang-shell) is a program for interpreting S-Lang scripts. 
It supports dynamic loading of S-Lang modules and includes a readline
interface for interactive use.

This package also includes S-Lang modules that are distributed with
the S-Lang distribution.

%package devel
Summary:	Development files for the S-Lang extension language
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains files which you'll need if you want to
develop S-Lang based applications.  Documentation which may help
you write S-Lang based applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.

%prep
%setup -q
%patch -P2 -p1 -b .sighuptest

%build
%configure \
	--with-{png,z}lib=%{_libdir} \
	--with-{png,z}inc=%{_includedir} \
	--without-pcre \
%if %{with oniguruma}
	--with-oniglib=%{_libdir} \
	--with-oniginc=%{_includedir} \
%else
	--without-onig \
%endif
;

# fails with %{?_smp_mflags}
# install_doc_dir sets SLANG_DOC_DIR macro
make RPATH="" install_doc_dir=%{_pkgdocdir} all

%install
make install-all INSTALL="install -p" RPATH="" DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_docdir}/{slang,slsh}
rm -f $RPM_BUILD_ROOT%{_libdir}/libslang.a

mkdir $RPM_BUILD_ROOT%{_includedir}/slang
for h in slang.h slcurses.h; do
	ln -s ../$h $RPM_BUILD_ROOT%{_includedir}/slang/$h
done

%check
make check

%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS
%{_libdir}/libslang*.so.2*

%files slsh
%doc slsh/doc/html/slsh*.html
%config(noreplace) %{_sysconfdir}/slsh.rc
%{_bindir}/slsh
%{_libdir}/slang
%{_mandir}/man1/slsh.1*
%{_datadir}/slsh

%files devel
%doc doc/*/cslang*.txt doc/*/cref.txt doc/README doc/*/slang*.txt doc/*.txt
%{_libdir}/libslang*.so
%{_libdir}/pkgconfig/slang.pc
%{_includedir}/sl*.h
%{_includedir}/slang

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.3-3
- disable pcre module (#2128372)
- convert license tag to SPDX

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 08 2022 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.3-1
- update to 2.3.3

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.2-4
- don't use memcpy() on overlapping buffers

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 01 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.2-2
- Rebuild against oniguruma 6.8.1

* Mon Mar 05 2018 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.2-1
- update to 2.3.2
- add gcc to build requirements
- include soname in file list

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-0.2.pre20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.2-0.1.pre20
- update to 2.3.2-pre20
- drop unnecessary macro
- use macro for ldconfig scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.1a-3
- drop static subpackage (#1436909)
- remove Group tags and indent spec (#1436909)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.1a-1
- update to 2.3.1a

* Mon Oct 31 2016 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.1-1
- update to 2.3.1

* Sun Oct 30 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-7
- Rebuild for oniguruma 6.1.1

* Mon Jul 18 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-6
- Rebuild for oniguruma 6

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.0-4
- Use %%license
- Don't ship NEWS and Changlog
- Ship developer docs in -devel

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.0-2
- remove duplicate declaration in slang.h (#1203896)

* Wed Dec 10 2014 Miroslav Lichvar <mlichvar@redhat.com> - 2.3.0-1
- update to 2.3.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.4-11
- use _pkgdocdir if available (#994097)
- build static objects in build section
- make some dependencies arch-specific

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 05 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.4-9
- add support for aarch64 (#926541)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.4-7
- fix building without oniguruma

* Thu Jan 24 2013 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.4-6
- buildrequire oniguruma-devel only on Fedora
- run test suite
- remove obsolete macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.2.4-4
- Rebuild against PCRE 8.30

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.2.4-2
- Rebuild for new libpng

* Mon Apr 11 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.4-1
- update to 2.2.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.3-1
- update to 2.2.3

* Mon Nov 08 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.2-3
- fix libdir in pkgconfig file (#650373)

* Wed Jul 21 2010 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.2-2
- move headers to /usr/include (#609977)

* Mon Dec 07 2009 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.2-1
- update to 2.2.2

* Mon Sep 07 2009 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.1-1
- update to 2.2.1

* Mon Aug 03 2009 Miroslav Lichvar <mlichvar@redhat.com> - 2.2.0-1
- update to 2.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.4-2
- convert changes.txt to UTF-8, comment patches (#226420)

* Mon Sep 08 2008 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.4-1
- update to 2.1.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.3-3
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.3-2
- drop lang patch
- build oniguruma module (#226420)

* Mon Nov 05 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.3-1
- update to 2.1.3

* Tue Sep 25 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.2-2
- fix integer underflow in compute_hash (#302181)
- fix SLang_set_error when called from signal handler (#297661)

* Mon Sep 17 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.2-1
- update to 2.1.2

* Thu Aug 23 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.1-2
- update license tag
- buildrequire gawk

* Mon Jul 09 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.1-1
- update to 2.1.1

* Fri Jun 15 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.1.0-1
- update to 2.1.0
- create -slsh subpackage for slsh and modules

* Mon Feb 19 2007 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.7-2
- ignore background color of trailing spaces if terminal has bce (#217276)
- move static library to -static subpackage
- spec cleanup

* Mon Nov 06 2006 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.7-1
- update to 2.0.7

* Wed Jul 12 2006 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.6-3
- don't build unpackaged stuff
- package just txt files from doc directory

* Tue May 23 2006 Peter Jones <pjones@redhat.com> - 2.0.6-2
- put static lib back; it is required by anaconda

* Mon May 22 2006 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.6-1
- update to slang-2.0.6
- move .so.2 link to main package
- don't package static library and utf8 link
- remove requires for libtool and libtermcap
- rearrange doc files (#191583)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.5-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.5-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec 2 2005 Petr Raszyk <praszyk@redhat.com> - 2.0.5-5
- A patch by Bill Nottingham <notting@redhat.com>
  (#174761). slang-LANG.patch
  slang reads automatically sh-env-variable LANG.

* Mon Nov 21 2005 Petr Raszyk <praszyk@redhat.com> - 2.0.5-3
- Rebuild.

* Mon Nov 21 2005 Petr Raszyk <praszyk@redhat.com> - 2.0.5-1
- Upgrade to slang 20005.
- (#161536). slang-nointerlibc2.patch
- slang-makefile.patch

* Mon Oct 24 2005 Petr Raszyk <praszyk@redhat.com> - 1.4.9-23
- rebuild

* Mon Oct 24 2005 Petr Raszyk <praszyk@redhat.com> - 1.4.9-22
- libslang-utf8.so should not use the symbol __libc_enable_secure 
- (#161536). slang-nointerlibc.patch
- Additional some comments/hints for C-Frame 121

* Sun Oct 16 2005 Florian La Roche <laroche@redhat.com>
- set _filter_GLIBC_PRIVATE

* Sun Oct 16 2005 Florian La Roche <laroche@redhat.com>
- add exec perms to shared libs

* Mon Sep  5 2005 Petr Raszyk <praszyk@redhat.com> - 1.4.9-19
- One line in the patch 'slang-utf8-acs.ptach' commented out (#138445). 

* Thu Aug 18 2005 Petr Raszyk <praszyk@redhat.com> - 1.4.9-18
- Patch to resolve the problem with displaying the 'x' character
  in the latin2 mode (#139127) 

* Fri Mar 18 2005 Petr Rockai <prockai@redhat.com> - 1.4.9-17
- Patch to compile with gcc4 by Robert Scheck (#151029). (Weeird,
  probably on march 2nd the used buildroot wasn't updated with
  gcc4 yet?).

* Wed Mar 02 2005 Petr Rockai <prockai@redhat.com>
- rebuild

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Sun Aug 1 2004 Alan Cox <alan@redhat.com>
- fixed requires so slang-devel pulls in libtermcap-devel (#125299)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec  5 2003 Jeremy Katz <katzj@redhat.com> 1.4.9-2
- rebuild to fix libslang-utf8.so.1 symlink

* Tue Oct 28 2003 Adrian Havill <havill@redhat.com> 1.4.9-1
- big upgrade to 1.4.9
- manually redid partially rotted utf patch for sldisply.c
- no longer necessary to chmod the so files
- change copyright header to license

* Fri Jun 13 2003 Bill Nottingham <notting@redhat.com> 1.4.5-18
- fix segfault in slcurses (#97216)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Jakub Jelinek <jakub@redhat.com> 1.4.5-15
- for ACS characters, take them as is, not through wcrtomb
  and assume wcwidth returns 1 for them

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 1.4.5-13
- set execute bits on library so that requires are genereted.

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 1.4.5-12
- remove unpackaged files from the buildroot
- lib64'ize

* Wed Jul 24 2002 Bill Nottingham <notting@redhat.com> 1.4.5-11
- fix write-before-beginning-of-string in SLsmg_write_nwchars

* Tue Jul  9 2002 Bill Nottingham <notting@redhat.com> 1.4.5-10
- fix segfault in odd environments

* Mon Jul  8 2002 Bill Nottingham <notting@redhat.com> 1.4.5-9
- tweak UTF-8 linedrawing patch slightly; add README describing some of
  the changes
- fix a utee/dtee typo

* Wed Jun 26 2002 Bill Nottingham <notting@redhat.com> 1.4.5-7
- add patch to support ACS linedrawing characters in UTF-8

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Bill Nottingham <notting@redhat.com> 1.4.5-5
- removed keymap patch (#59171)
- added Debian utf8 patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar  5 2002 Bill Nottingham <notting@redhat.com>
- fix symlink & ia64 fubarness

* Mon Mar  4 2002 Bill Nottingham <notting@redhat.com>
- update to 1.4.5

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add link from library major version number

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- added patch to fix Alt/Meta key handling (originally from mutt,
  <jorton@btconnect.com>)

* Fri Jun  1 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- forced to use RPM_OPT_FLAGS for ELF_CFLAGS too

* Mon Mar 12 2001 Bill Nottingham <notting@redhat.com>
- update to 1.4.4

* Tue Feb 27 2001 Bill Nottingham <notting@redhat.com>
- have slang-devel require slang = %%{version}

* Tue Aug 29 2000 Bill Nottingham <notting@redhat.com>
- update to 1.4.2

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- added defattr

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- autoconf fix for ia64

* Mon Apr 24 2000 Bill Nottingham <notting@redhat.com>
- update to 1.4.1

* Wed Mar 29 2000 Bill Nottingham <notting@redhat.com>
- fix background color problem with newt

* Thu Mar  2 2000 Bill Nottingham <notting@redhat.com>
- resurrect for the devel tree

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Oct 21 1998 Bill Nottingham <notting@redhat.com>
- libslang.so goes in -devel

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de

* Sat Jun  6 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.2.2 with buildroot.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 18 1998 Erik Troan <ewt@redhat.com>
- rebuilt to find terminfo in /usr/share

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Sep 1 1997 Donnie Barnes <djb@redhat.com>
- upgraded to 0.99.38 (will it EVER go 1.0???)
- all patches removed (all appear to be in this version)

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

