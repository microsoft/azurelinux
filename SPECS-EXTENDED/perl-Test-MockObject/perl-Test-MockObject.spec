Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Test-MockObject
Version:        1.20200122
Release:        3%{?dist}
Summary:        Perl extension for emulating troublesome interfaces
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-MockObject
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-MockObject-%{version}.tar.gz#/perl-Test-MockObject-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder)
# Optional run-time:
BuildRequires:  perl(UNIVERSAL::can) >= 1.20110617
BuildRequires:  perl(UNIVERSAL::isa) >= 1.20110614
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(fields)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::Exception) >= 0.31
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Warn) >= 0.23
BuildRequires:  perl(vars)
# Dependencies:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

%description
Test::MockObject is a highly polymorphic testing object, capable of
looking like all sorts of objects.  This makes white-box testing much
easier, as you can concentrate on what the code being tested sends to
and receives from the mocked object, instead of worrying about faking
up your own data.  (Another option is not to test difficult things.
Now you have no excuse.)

%prep
%setup -q -n Test-MockObject-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::MockObject.3*
%{_mandir}/man3/Test::MockObject::Extends.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20200122-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20200122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Tom Callaway <spot@fedoraproject.org> - 1.20200122-1
- update to 1.20200122

* Fri Oct 18 2019 Tom Callaway <spot@fedoraproject.org> - 1.20191002-1
- update to 1.20191002

* Sun Oct 13 2019 Paul Howarth <paul@city-fan.org> - 1.20180705-5
- Spec tidy-up
  - Use author-independent source URL
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely
  - Make %%files list more explicit
  - Package LICENSE file
  - Drop redundant use of %%{?perl_default_filter}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20180705-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20180705-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20180705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20180705-1
- 1.20180705 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20161202-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20161202-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20161202-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20161202-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20161202-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20161202-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20161202-1
- 1.20161202 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20150527-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20150527-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Petr Pisar <ppisar@redhat.com> - 1.20150527-4
- Specify all dependencies

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20150527-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20150527-2
- Perl 5.22 rebuild

* Thu May 28 2015 Tom Callaway <spot@fedoraproject.org> - 1.20150527-1
- update to 1.20150527

* Tue May 26 2015 Tom Callaway <spot@fedoraproject.org> - 1.20150521-1
- update to 1.20150521

* Tue Feb  3 2015 Tom Callaway <spot@fedoraproject.org> - 1.20140408-1
- update to 1.20140408

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20120301-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120301-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120301-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.20120301-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Tom Callaway <spot@fedoraproject.org> - 1.20120301-1
- update to 1.20120301

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.09-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.09-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Dec 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-7
- Add BR: perl(CGI) (Fix FTBFS: BZ 660972).

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-6
- Mass rebuild with perl-5.12.0

* Thu Feb  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.09-5
- 552253 merge review

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.09-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-1
- update to 1.09

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-2
- rebuild for new perl

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Thu Oct  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Apr 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Thu Mar 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.
- Makefile.PL -> Build.PL.

* Mon Mar 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Fri Jul 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- Update to 1.00.

* Fri Jul 15 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.15-3
- rebuilt

* Tue Dec 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-2
- Build requires Test::Simple >= 0.44 (bug 2324).

* Wed Dec 01 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-0.fdr.1
- Update to 0.15.

* Tue May 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.14-0.fdr.1
- Update to 0.14.
- Require perl >= 1:5.6.1 for vendor install dir support.
- Use pure_install to avoid perllocal.pod workarounds.
- Moved make test to section %%check.

* Wed Nov 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.1
- First build.
