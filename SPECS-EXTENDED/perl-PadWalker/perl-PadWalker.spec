Name:           perl-PadWalker
Version:        2.3
Release:        9%{?dist}
Summary:        Play with other people's lexical variables
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/PadWalker
Source0:        https://cpan.metacpan.org/authors/id/R/RO/ROBIN/PadWalker-%{version}.tar.gz#/perl-PadWalker-%{version}.tar.gz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
PadWalker is a module that allows you to inspect (and even change!)
lexical variables in any subroutine that called you. It will only show
those variables that are in scope at the point of the call.

%prep
%setup -q -n PadWalker-%{version}

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
%doc Changes README
%{perl_vendorarch}/auto/PadWalker/
%{perl_vendorarch}/PadWalker.pm
%{_mandir}/man3/PadWalker.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.3-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.3-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 12 2017 Paul Howarth <paul@city-fan.org> - 2.3-1
- Update to 2.3
  - Make tests work with -Ddefault_inc_excludes_dot (CPAN RT#120421)
- Simplify find commands using -empty and -delete
- Drop legacy Group: tag

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.2-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.2-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 26 2015 Paul Howarth <paul@city-fan.org> - 2.2-1
- Update to 2.2
  - Convert to PERL_NO_GET_CONTEXT
    https://github.com/robinhouston/PadWalker/pull/2
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.1-2
- Perl 5.22 rebuild

* Sun Apr 26 2015 Paul Howarth <paul@city-fan.org> - 2.1-1
- Update to 2.1
  - Another bleadperl fix (CPAN RT#101037)

* Mon Dec 15 2014 Paul Howarth <paul@city-fan.org> - 2.0-1
- Update to 2.0
  - Restore compatibility with perl 5.8 (CPAN RT#100262)
  - Restore compatibility with bleadperl (PR#3)

* Tue Nov 11 2014 Paul Howarth <paul@city-fan.org> - 1.99-1
- Update to 1.99
  - Make it compatible with bleadperl (CPAN RT#100262)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.98-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 27 2013 Paul Howarth <paul@city-fan.org> - 1.98-1
- Update to 1.98
  - Improve peek_sub error handling (CPAN RT#89679)
- Specify all dependencies
- Don't use macros for commands
- Make %%files list more explicit

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.96-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Petr Pisar <ppisar@redhat.com> - 1.96-1
- 1.96 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.92-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.92-6
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Iain Arnell <iarnell@gmail.com> 1.92-4
- really rebuild against perl-5.14

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.92-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Steven Pritchard <steve@kspei.com> 1.92-1
- Update to 1.92.

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.9-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.9-4
- Mass rebuild with perl-5.12.0

* Fri Mar 19 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.9-3
- PERL_INSTALL_ROOT => DESTDIR, perl_default_filter (XS package)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.9-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.9-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7-2
- Rebuild for perl 5.10 (again)

* Thu Feb 21 2008 Steven Pritchard <steve@kspei.com> 1.7-1
- Update to 1.7.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6-2
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1.6-1
- Update to 1.6.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jan  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.5-1
- Update to 1.5.

* Thu Jan  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.3-1
- Update to 1.3.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.2-1
- Update to 1.2.

* Mon Oct 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.1-1
- Update to 1.1.

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.0-2
- Rebuild for FC6.

* Fri May 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.0-1
- First build.
