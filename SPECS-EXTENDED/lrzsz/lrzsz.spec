Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: The lrz and lsz modem communications programs
Name: lrzsz
Version: 0.12.20
Release: 50%{?dist}
License: GPLv2+
Source: https://www.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Patch1: lrzsz-0.12.20-glibc21.patch
Patch2: lrzsz-0.12.20.patch
Patch3: lrzsz-0.12.20-man.patch
Patch4: lrzsz-0.12.20-aarch64.patch
Url: https://www.ohse.de/uwe/software/lrzsz.html
BuildRequires: gcc gettext

%description
Lrzsz (consisting of lrz and lsz) is a cosmetically modified
zmodem/ymodem/xmodem package built from the public-domain version of
the rzsz package. Lrzsz was created to provide a working GNU
copylefted Zmodem solution for Linux systems.

%prep
%setup -q

%patch 1 -p1 -b .glibc21
%patch 2 -p1 -b .crc
%patch 3 -p1 -b .man
%patch 4 -p1 -b .aarch64

rm -f po/*.gmo

%build
%configure --disable-pubdir \
           --enable-syslog \
           --program-transform-name=s/l//

make %{?_smp_mflags}

%install
%makeinstall
for m in rb rx; do ln -s rz.1 %{buildroot}%{_mandir}/man1/$m.1; done
for m in sb sx; do ln -s sz.1 %{buildroot}%{_mandir}/man1/$m.1; done

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.20-50
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-46
- add man page symlinks for sb, sx, rb, rx programs (#1611501)

* Fri Jul 20 2018 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-45
- add gcc to build requirements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.12.20-37
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-33
- use recent config.sub and config.guess for aarch64 (#926093)
- remove obsolete macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 07 2011 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-29
- fix typos in sz man page (#668900)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-25
- rebuild message catalogs (#485024)
- remove dot from summary

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12.20-24
- fix license tag

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 0.12.20-23
- rebuilt against GCC 3.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-22.1
- rebuild

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 0.12.20-22
- add BR on gettext #193513

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-21.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-21.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 0.12.20-21
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 0.12.20-20
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 0.12.20-15
- Fixed a bug with 16 bit ZMODEM transfer, jordanc@censoft.com (bug #75473)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 0.12.20-12
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Aug 10 2001 Than Ngo <than@redhat.com> 0.12.20-10
- Copyright->License
- use %%find_lang

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- use RPM macros

* Sat May 27 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- cleanup specfile
- add Url
- put man pages to correct place

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Sat Feb 05 2000 Preston Brown <pbrown@redhat.com>
- rebuild to compress man pages, get new description

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 0.12.20, i18n translations included.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups 

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- Upgraded to 0.12.14 and changed makefiles so gettext isnt built.
