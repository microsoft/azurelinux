Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Perl bindings for the Newt library
Name: perl-Newt
Version: 1.08
Release: 56%{?dist}
URL: https://metacpan.org/pod/Newt
Source: https://cpan.metacpan.org/authors/id/A/AM/AMEDINA/Newt-1.08.tar.gz
Patch0: newt-perl-1.08-debian.patch
Patch1: newt-perl-1.08-typemap.patch
Patch2: newt-perl-1.08-fix.patch
Patch3: newt-perl-1.08-xs.patch
Patch4: newt-perl-1.08-lang.patch
Patch5: perl-Newt-bz385751.patch
Patch6: perl-Newt-1.08-export.patch
Patch7: perl-Newt-1.08-pod.patch
Patch8: perl-Newt-1.08-formdestroy.patch
BuildRequires:  gcc
BuildRequires: newt-devel, perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::MakeMaker)
Obsoletes: newt-perl < 1.08-15
Provides: newt-perl = %{version}-%{release}
Requires: %(eval `perl -V:version`; echo "perl(:MODULE_COMPAT_$version)")
License: GPL+ or Artistic

%description
This package provides Perl bindings for the Newt widget
library, which provides a color text mode user interface.

%prep
%setup -q -n Newt-%{version}
%patch0 -p1 -b .debian
%patch1 -p1 -b .valist
%patch2 -p1 -b .fix
%patch3 -p1 -b .exes
%patch4 -p1 -b .lang
%patch5 -p1 -b .bz385751
%patch6 -p1 -b .export
%patch7 -p1 -b .doc
%patch8 -p1 -b .formdestroy
rm -rf newtlib

%build
perl Makefile.PL PREFIX=%{_prefix} INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%files
%doc ChangeLog README
%{perl_vendorarch}/Newt.pm
%{perl_vendorarch}/auto/Newt
%{_mandir}/man3/Newt*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.08-56
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-53
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-50
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-46
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-44
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.08-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-41
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-40
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Petr Pisar <ppisar@redhat.com> - 1.08-38
- Specify all build-time dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.08-35
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.08-32
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.08-30
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.08-29
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 17 2010 Joe Orton <jorton@redhat.com> - 1.08-27
- drop Newt::Form::DESTROY method (Petr Pisar, #600670)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-26
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.08-25
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Joe Orton <jorton@redhat.com> 1.08-23
- add fixes from Joe Ogulin (#489825)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-21
- resolve bz 385751

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-20
- Rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.08-19
- Autorebuild for GCC 4.3

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.08-18
- rebuild for new perl

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 1.08-17
- clarify License tag

* Tue Mar  6 2007 Joe Orton <jorton@redhat.com> 1.08-15
- rename to perl-Newt; Obsolete and Provide newt-perl (#226196)

* Thu Mar  1 2007 Joe Orton <jorton@redhat.com> 1.08-14
- various cleanups (Jason Tibbs, #226196)
- require perl-devel

* Tue Feb 27 2007 Joe Orton <jorton@redhat.com> 1.08-13
- clean up URL, Source, BuildRoot, BuildRequires

* Thu Dec 14 2006 Joe Orton <jorton@redhat.com> 1.08-12
- fix test.pl (Charlie Brady, #181674)

* Thu Dec 14 2006 Joe Orton <jorton@redhat.com> 1.08-11
- fix directory ownership (#216610)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 1.08-10
- fix compiler warnings (#155977)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.08-9.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.08-9.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.08-9.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 27 2005 Petr Rockai <prockai@redhat.com> - 1.08-9
- rebuild against newt 0.52.0

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 1.08-8
- rebuild

* Tue Aug 17 2004 Joe Orton <jorton@redhat.com> 1.08-7
- add perl MODULE_COMPAT requirement

* Mon Aug 16 2004 Joe Orton <jorton@redhat.com> 1.08-6
- rebuild

* Mon Sep  8 2003 Joe Orton <jorton@redhat.com> 1.08-5
- fix issue with non-English LANG setting (#67735)

* Tue Aug  5 2003 Joe Orton <jorton@redhat.com> 1.08-4
- rebuild

* Thu May  9 2002 Joe Orton <jorton@redhat.com> 1.08-3
- add newt requirement

* Wed Apr 03 2002 Gary Benson <gbenson@redhat.com> 1.08-2
- tweak perl dependency as suggested by cturner@redhat.com

* Wed Mar 20 2002 Gary Benson <gbenson@redhat.com>
- make like all the other perl modules we ship (bind to perl version,
  use perl dependency finding scripts, build filelist automatically).
- include documentation
- build against perl 5.6.1

* Thu Jan 10 2002 Joe Orton <jorton@redhat.com>
- Adapted for RHL

* Tue Sep 11 2001 Mark Cox <mjc@redhat.com>
- Change paths to new layout

* Mon Jun 11 2001 Joe Orton <jorton@redhat.com>
- Initial revision.
