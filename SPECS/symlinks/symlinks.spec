Summary:        A utility which maintains a system's symbolic links
Name:           symlinks
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Version:        1.7
Release:        8%{?dist}
License:        Copyright only
URL:            https://ibiblio.org/pub/Linux/utils/file/
# Upstream maintainer provided tarball, ibiblio no longer allowing uploads
# Upstream Source0: https://ibiblio.org/pub/Linux/utils/file/%{name}-%{version}.tar.gz
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
# Taken from https://packages.debian.org/changelogs/pool/main/s/symlinks/symlinks_1.2-4.2/symlinks.copyright
Source1:        symlinks-LICENSE.txt
BuildRequires:  gcc

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point
to nonexistent files.  Symlinks can also automatically convert
absolute symlinks to relative symlinks.

Install the symlinks package if you need a program for maintaining
symlinks on your system.

%prep
%autosetup -p1 -n %{name}-%{version}
install -m 644 %{SOURCE1} %{_builddir}/%{name}-%{version}/

%build
%make_build CFLAGS="%{optflags} $(getconf LFS_CFLAGS) %{build_ldflags}"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 symlinks %{buildroot}%{_bindir}
install -m 644 symlinks.1 %{buildroot}%{_mandir}/man1

%files
%license symlinks-LICENSE.txt
%{_bindir}/symlinks
%{_mandir}/man1/symlinks.1*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-8
- Updating naming for 3.0 version of Azure Linux.

* Wed Jul 06 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.7-7
- Re-import from Fedora 36 (license MIT)
- Adding as run dependency for package cassandra medusa
- License verified
 
* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan  8 2020 Tim Waugh <twaugh@redhta.com> - 1.7-1
- 1.7, fixes #1786376.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Tim Waugh <twaugh@redhat.com> - 1.4-21
- Build requires gcc (bug #1606459).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Than Ngo <than@redhat.com> - 1.4-19
- fixed upstream URL reference

* Wed May 09 2018 Tim Waugh <twaugh@redhat.com> - 1.4-18
- Fix partial build flags injection (bug #1573111).

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 20 2011 Tim Waugh <twaugh@redhat.com> 1.4-4
- Applied patches from Jiri Popelka:
  - Fix off-by-one error in call to readlink.
  - Fix possible buffer overrun found by coverity.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 13 2009 Tim Waugh <twaugh@redhat.com> 1.4-2
- 1.4.  All patches now upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-32
- fix license tag

* Mon Feb 11 2008 Tim Waugh <twaugh@redhat.com> 1.2-31
- Rebuild for GCC 4.3.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 1.2-30
- Rebuilt.

* Fri Feb 23 2007 Tim Waugh <twaugh@redhat.com> 1.2-29
- Use smp_mflags (bug #226445).
- Better default attributes (bug #226445).
- Make setup macro quiet (bug #226445).
- Clean build root in %%install section (bug #226445).

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 1.2-28
- Fixed build root (bug #226445).

* Tue Feb  6 2007 Tim Waugh <twaugh@redhat.com> 1.2-27
- Fixed summary (bug #226445).
- Added token URL tag (bug #226445).

* Tue Jan 30 2007 Florian La Roche <laroche@redhat.com> - 1.2-26
- do not strip away debuginfo

* Thu Jan 18 2007 Tim Waugh <twaugh@redhat.com> - 1.2-25
- Build with LFS support (bug #206407).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.2-24
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1.2-23
- s/Copyright:/License:/.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 16 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch from #89655

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.2-17
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Tue May 30 2000 Preston Brown <pbrown@redhat.com>
- fix up help output (#10236)

* Thu Feb 10 2000 Preston Brown <pbrown@redhat.com>
- do not link statically

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against the latest glibc in the sparc tree

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- changed build root to /var/tmp, not /var/lib
- updated to version 1.2

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- build-rooted
