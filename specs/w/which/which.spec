# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global has_which2_alias 1

Summary: Displays where a particular program in your path is located
Name: which
Version: 2.23
Release: 3%{?dist}
License: GPL-3.0-only
Source0: http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
Source1: which2.sh
Source2: which2.csh
Patch0: which-2.21-warning.patch
Url: https://savannah.gnu.org/projects/which/
Requires: coreutils
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: readline-devel

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%autosetup -p1
 
%build
%configure
%make_build

%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
%if %{has_which2_alias}
    install -p -m 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%files
%license COPYING
%doc EXAMPLES README AUTHORS NEWS
%if %{has_which2_alias}
%attr(0644,root,root) %{_sysconfdir}/profile.d/which2.*
%endif
%{_bindir}/which
%{_infodir}/which.info*
%{_mandir}/man1/which.1*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Than Ngo <than@redhat.com> - 2.23-2
- Add a check to ensure that /proc/$$/exe can be read

* Mon Feb 03 2025 Than Ngo <than@redhat.com> - 2.23-1
- Fixed rhbz#2343361, update to 2.23

* Sat Feb 01 2025 Than Ngo <than@redhat.com> - 2.22-2
- Fixed rhbz#2343113, regression

* Mon Jan 27 2025 Than Ngo <than@redhat.com> - 2.22-1
- Fixed rhbz#2342020, update to 2.22

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 08 2023 Than Ngo <than@redhat.com> - 2.21-39
- fixed #2175953, enable which2 alias 

* Sun Feb 19 2023 Than Ngo <than@redhat.com> - 2.21-38
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Than Ngo <than@redhat.com> - 2.21-36
- which fails for long path

* Fri Aug 05 2022 Than Ngo <than@redhat.com> - 2.21-35
- disable which2 alias and function by default as it caused more problems than benefits

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 09 2022 Than Ngo <than@redhat.com> - 2.21-33
- make which2.sh script more robust,

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 02 2021 Than Ngo <than@redhat.com> - 2.21-31
- check shell correctly

* Tue Oct 26 2021 Than Ngo <than@redhat.com> - 2.21-30
- disable the --read-functions option in korn shells

* Fri Oct 15 2021 Than Ngo <than@redhat.com> - 2.21-29
- Fixed regression, use export instead alias

* Sun Oct 10 2021 Than Ngo <than@redhat.com> - 2.21-28
- Resolves: #2009547, which treats function contents as aliases when parsing ksh

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 04 2021 Than Ngo <than@redhat.com> - 2.21-26
- Resolves: #1942153, fixed unbound variable

* Mon Apr 26 2021 Than Ngo <than@redhat.com> - 2.21-25
- improved which2.sh

* Tue Mar 23 2021 Than Ngo <than@redhat.com> - 2.21-24
- fixed regression if SHELL=zsh

* Sun Mar 21 2021 Than Ngo <than@redhat.com> - 2.21-23
- fixed coverity issues
- improved which2.sh

* Thu Mar 18 2021 Than Ngo <than@redhat.com> - 2.21-22
- fixed syntax error testcase: a=b which ls

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Than Ngo <than@redhat.com> - 2.21-19
- fixed #1817138 - Invalid syntax in /etc/profile.d/which2

* Tue Mar 24 2020 Than Ngo <than@redhat.com> - 2.21-18
- set correct alias for mksh

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Than Ngo <than@redhat.com> - 2.21-16
- set correct alias for ksh

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Than Ngo <than@redhat.com> - 2.21-14
- bump release 

* Mon Feb 04 2019 Than Ngo <than@redhat.com> - 2.21-13
- bump release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 Than Ngo <than@redhat.com> - 2.21-11
- fixed more coverity issue

* Mon Jul 23 2018 Than Ngo <than@redhat.com> - 2.21-10
- Fix coverity issues

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 16 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.21-8
- Fix invalid [ ... ] syntax which results in complaints by zsh.
  https://bugzilla.redhat.com/show_bug.cgi?id=1546221
- Remove pointless Group tag, buildroot cleaning and %%defattr.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Than Ngo <than@redhat.com> - 2.21-6
- added CI tests using the standard test interface

* Wed Jan 31 2018 Than Ngo <than@redhat.com> - 2.21-5
- fixed bz#1526500 - 'declare' not found under ksh

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 27 2016 Than Ngo <than@redhat.com> - 2.21-1
- update to 2.21

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.20-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Till Maas <opensource@till.name> - 2.20-10
- Use alias instead of exported function for which to avoid bashism,
http://unix.stackexchange.com/questions/59360/#59431

* Wed Feb 18 2015 Till Maas <opensource@till.name> - 2.20-9
- Check functions (#1194044)
- Use %%license

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Than Ngo <than@redhat.com> - 2.20-1
- 2.2.0
- disable alias which for cshell

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Warren Togami <wtogami@redhat.com> 2.19-3
- install-info should exit gracefully when --nodocs

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 2.19-2
- rebuilt

* Fri Jan 25 2008 Than Ngo <than@redhat.com> 2.19-1
- 2.19, fix #399551, #430159

* Tue Nov 27 2007 Than Ngo <than@redhat.com> - 2.18-5
- fix permission which-2 scripts

* Tue Nov 27 2007 Than Ngo <than@redhat.com> 2.18-4
- fix permission which-2 scripts

* Mon Nov 26 2007 Karsten Hopp <karsten@redhat.com> 2.18-3
- add dir entry for info page

* Tue Nov 20 2007 Than Ngo <than@redhat.com> 2.18-2
- cleanup specfile

* Tue Nov 13 2007 Than Ngo <than@redhat.com> 2.18-1
- 2.18

* Tue Nov 13 2007 Than Ngo <than@redhat.com> 2.16-10
- cleanup specfile
- get rid of dev dependency

* Mon Apr 23 2007 Than Ngo <than@redhat.com> - 2.16-9
- add missing which-2 script for csh
- cleanup specfile #226539

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 2.16-8
- install-info scriptlet failures

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 2.16-7
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.16-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.16-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 2.16-6
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 2.16-5
- rebuilt

* Sat Aug 07 2004 Than Ngo <than@redhat.com> 2.16-4
- add missing URL (thanks to  Robert Scheck)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.16
- fix %%preun

* Thu Jul 17 2003 Than Ngo <than@redhat.com> 2.14-8
- rebuild

* Thu Jul 17 2003 Than Ngo <than@redhat.com> 2.14-7
- added Prereq: dev (bug #99275)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Than Ngo <than@redhat.com> 2.14-4
- cleanup code (bug #78478)

* Thu Nov 14 2002 Tim Powers <timp@redhat.com> 2.14-3
- redirect info dir warnings to /dev/null

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 2.14-1
- add missing info file

* Mon Jul 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.14 wih better support for current bash

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Than Ngo <than@redhat.com> 2.13-3
- use access instead stat in AFS environment (bug #60353)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.13

* Sat Aug  4 2001 Than Ngo <than@redhat.com>
- fix bug 50844

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Sep 10 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- 2.12 (only man-page fix)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- FHS packaging.

* Sun May 21 2000 Ngo Than <than@redhat.de>
- put man pages in /usr/share/man/*

* Thu Apr 20 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.11
- change from root:bin -> root:root

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Sun Jan 16 2000 Preston Brown <pbrown@redhat.com>
- newer stuff rom Carlo (2.10).  Author's email: carlo@gnu.org

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- adopted Carlo's specfile.

* Fri Sep 24 1999 Carlo Wood <carlo@gnu.org>
- There should not be a reason anymore to include README.alias in the rpm docs.
- Don't install as root.root in RPM_BUILD_ROOT, in order to allow to build
  rpm as non-root.
- Bug fix
- Added /etc/profile.d for automatic alias inclusion.

* Wed Aug 25 1999 Carlo Wood <carlo@gnu.org>
- Added README.alias.

* Wed Aug 11 1999 Carlo Wood <carlo@gnu.org>
- Typo in comment.

* Thu May 27 1999 Carlo Wood <carlo@gnu.org>
- Typo fix
- Moved maintainer targets from makefile to Makefile.am.

* Tue May 18 1999 Carlo Wood <carlo@gnu.org>
- Typo in appended changelog.
- Appended the old change log of `which-2.0.spec' to (this) changelog,
  which is generated from the CVS log of `which-2.0.spec.in'.
- Generate which-2.spec from which-2.spec.in with automatic VERSION
  and CHANGELOG substitution.

* Fri May 14 1999 Carlo Wood <carlo@gnu.org>
- Moved assignment of CFLAGS to the configure line, using RPM_OPT_FLAGS now.
- Corrected Source: line to point to ftp.gnu.org.

* Sat Apr 17 1999 Carlo Wood <carlo@gnu.org>
- Started to use automake and autoconf

* Fri Apr 09 1999 Carlo Wood <carlo@gnu.org>
- Renamed which-2.0.spec to which-2.spec

