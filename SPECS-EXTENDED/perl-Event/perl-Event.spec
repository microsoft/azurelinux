Name:		perl-Event
Version:	1.28
Release:	1%{?dist}
Summary:	Event loop processing
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Event
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETJ/Event-%{version}.tar.gz#/perl-Event-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(integer)
BuildRequires:	perl(strict)
BuildRequires:	perl(Time::HiRes)
BuildRequires:	perl(vars)
# Test Suite
BuildRequires:	perl(Symbol)
BuildRequires:	perl(Test) >= 1
%if 0%{?with_check}
BuildRequires:	perl(Test::More)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Time::HiRes)

%{?perl_default_filter}

%description
The Event module provide a central facility to watch for various types of
events and invoke a callback when these events occur. The idea is to delay the
handling of events so that they may be dispatched in priority order when it is
safe for callbacks to execute.

%prep
%setup -q -n Event-%{version}

# Fix up permissions and shellbangs
perl -pi -e 's|#!./perl|#!/usr/bin/perl|' demo/*.t t/*.t util/bench.pl
%{_fixperms} -c demo/ util/

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc ANNOUNCE Changes README README.EV TODO
%doc Tutorial.pdf Tutorial.pdf-errata.txt demo/ t/ util/
%doc %{perl_vendorarch}/Event.pod
%{perl_vendorarch}/auto/Event/
%{perl_vendorarch}/Event.pm
%{perl_vendorarch}/Event/
%{_mandir}/man3/Event.3*
%{_mandir}/man3/Event::MakeMaker.3*
%{_mandir}/man3/Event::generic.3*

%changelog
* Wed Dec 18 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 1.28-1
- Update to version 1.28
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.27-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - Only Zero(Polld) if not NULL
- BR: perl-generators unconditionally
- Drop legacy Group: tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 14 2016 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - Fix documentation typos

* Sun Jun 12 2016 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - Fix Event::PRIO_NORMAL call in Watcher.pm
  - Update Changes
- BR: perl-generators where possible

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-6
- Perl 5.24 rebuild

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 1.24-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-2
- Perl 5.22 rebuild

* Sun Mar  1 2015 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24
  - Bump minimum perl version to 5.8.0
- Drop upstreamed UTF8 patch
- Classify buildreqs by usage

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul  9 2014 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23

* Mon Jun 30 2014 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to 1.22
- This release by ETJ → update source URL
- Don't need to remove empty directories from the buildroot

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.21-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Paul Howarth <paul@city-fan.org> - 1.21-1
- Update to 1.21:
  - Silence some clang warnings
    (http://www.xray.mpe.mpg.de/mailing-lists/perl5-porters/2012-12/msg00424.html)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Perl 5.16 rebuild

* Sun Jan 15 2012 Paul Howarth <paul@city-fan.org> 1.20-1
- update to 1.20 (test suite fixes)
- BR: perl(Carp), perl(Config), perl(Exporter)
- since upstream doesn't ship license files, neither should we
- make %%files list more explicit
- use a patch to fix character encoding rather than scripted iconv
- use DESTDIR rather than PERL_INSTALL_ROOT
- no need for additional filtering on top of %%{?perl_default_filter}
- don't package INSTALL file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.15-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.15-2
- perl mass rebuild

* Wed May 11 2011 Iain Arnell <iarnell@gmail.com> 1.15-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- filter perl(attrs) from requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.12-6
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-5
- rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-4
- mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.12-3
- mass rebuild with perl-5.12.0

* Mon Dec 07 2009 Stepan Kasal <skasal@redhat.com> 1.12-2
- rebuild against perl 5.10.1

* Tue Sep 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.12-1
- add perl_default_filter
- auto-update to 1.12 (by cpan-spec-update 0.01)
- added a new req on perl(Test) (version 1)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.11-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.11-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.09-5
- rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 1.09-4
- autorebuild for GCC 4.3

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.09-3
- rebuild for new perl

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.09-2
- bump

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.09-1
- update to 1.09
- add t/ to doc

* Sat Nov 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.08-1
- update to 1.08

* Sun Oct 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- update to 1.07

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-2
- bump for mass rebuild

* Wed Jun 14 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-1
- add explicit provides: perl(Event) = version...  wasn't being picked up
  automagically for some reason
- tweaked summary line
- bumped release

* Thu Jun 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.06-0
- initial spec file for F-E
