# Run extra tests
%if 0%{?rhel}
%bcond_with perl_Config_Tiny_enables_extra_test
%else
%bcond_without perl_Config_Tiny_enables_extra_test
%endif

Name:		perl-Config-Tiny
Version:	2.24
Release:	4%{?dist}
Summary:	Perl module for reading and writing .ini style configuration files
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Config-Tiny
Source0:	https://cpan.metacpan.org/modules/by-module/Config/Config-Tiny-%{version}.tgz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(warnings)
# Module Runtime
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(File::Spec) >= 3.30
BuildRequires:	perl(File::Temp) >= 0.22
BuildRequires:	perl(Test::More) >= 0.47
BuildRequires:	perl(UNIVERSAL)
BuildRequires:	perl(utf8)
%if %{with perl_Config_Tiny_enables_extra_test}
# Extra Tests
BuildRequires:	perl(Test::CPAN::Meta) >= 0.17
# Test::MinimumVersion → Perl::MinimumVersion → Perl::Critic → Config::Tiny
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::MinimumVersion) >= 0.101080
%endif
BuildRequires:	perl(Test::Pod) >= 1.44
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Config::Tiny is a Perl module designed for reading and writing .ini
style configuration files. It is designed for simplicity and ease of
use, and thus only supports the most basic operations.

%prep
%setup -q -n Config-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_Config_Tiny_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))" AUTOMATED_TESTING=1
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Config/
%{_mandir}/man3/Config::Tiny.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.24-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Paul Howarth <paul@city-fan.org> - 2.24-1
- Update to 2.24
  - Delete from caveats in documentation where it used to say:
      'Config::Tiny will only recognize the first time an option is set in a
       config file. Any further attempts to set the same option later in the
       config file are ignored.'
    In reality the code uses the 2nd and subsequent values to overwrite earlier
    values
  - Make this topic a new FAQ
  - Add corresponding test t/06.repeat.key.t
  - Update POD to clarify trailing comment options
  - Add corresponding test t/07.trailing.comment.t
  - Romanize Gregory Kidrenko's name so Config::IniFiles does not get 'Wide
    char in print'
  - Move xt/pod.t to xt/author/pod.t
  - Adopt new repo structure: see
    https://savage.net.au/Ron/html/My.Workflow.for.Building.Distros.html
  - Move require 5.008001 from Tiny.pm into Makefile.PL

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-15
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-11
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-7
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.23-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Paul Howarth <paul@city-fan.org> - 2.23-1
- Update to 2.23
  - Add the utf8 BOM to the Changes file
  - Fix read() and write() so they work on files called '0' (zero)
    (CPAN RT#107754)
  - Add t/05.zero.t and t/0 to test the new code
  - Reformat the source slightly

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-2
- Perl 5.22 rebuild

* Tue Feb 17 2015 Paul Howarth <paul@city-fan.org> - 2.22-1
- Update to 2.22
  - Fix licence info in Makefile.PL to say Perl (CPAN RT#102141)

* Mon Feb 16 2015 Paul Howarth <paul@city-fan.org> - 2.21-1
- Update to 2.21
  - Patch Makefile.PL to refer to the current repo, which is on github, and
    not the original one, which is on Adam's web site (CPAN RT#102125)
  - Remove Build.PL (CPAN RT#102126)
  - Edit line lengths in the Changes file to a maximum of 100 characters
  - Edit line lengths in the docs the same way
  - Expand the SEE ALSO section of the docs
- Use %%license

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 24 2013 Paul Howarth <paul@city-fan.org> - 2.20-1
- Update to 2.20
  - Relax pre-req version requirements

* Sun Sep 15 2013 Paul Howarth <paul@city-fan.org> - 2.19-1
- Update to 2.19
  - Remove obsolete and wrong version # from Makefile.PL (CPAN RT#88658)
  - Test if read() will return undef; if so, set an error message and (still)
    return undef
  - Change VERSION => $VERSION in Makefile.PL to
    VERSION_FROM => 'lib/Config/Tiny.pm' (CPAN RT#88670)

* Fri Sep 13 2013 Paul Howarth <paul@city-fan.org> - 2.17-1
- Update to 2.17
  - Remove the file tests -efr during calls to read(); the open() tests for any
    error
  - The -f test was reporting /dev/null as a directory, not a file
    (CPAN RT#36974)
  - Clean up some error messages slightly

* Fri Sep  6 2013 Paul Howarth <paul@city-fan.org> - 2.16-1
- Update to 2.16
  - Replace Path::Tiny with File::Spec, because the former's list of
    dependencies is soooo long :-( (see CPAN RT#88435 for Tree::DAG_Node)

* Tue Sep  3 2013 Paul Howarth <paul@city-fan.org> - 2.15-1
- Update to 2.15
  - Clean up the shambolic dates in the Changes file
  - Add a note under Caveats about setting options more that once - only the
    first case is respected (CPAN RT#69795)
  - Add a $encoding parameter to read_file() and write_file(), and add
    t/04.utf8.t and t/04.utf8.txt (CPAN RT#71029, CPAN RT#85571)
  - Fix temporary directory creation in tests for BSD-based systems
  - Rename t/*.t files
  - Add MANIFEST.SKIP, Changelog.ini, Build.PL, META.json
  - Add a FAQ to the docs
  - Clean up the docs
- This release by RSAVAGE -> update source URL
- Specify all dependencies
- Drop support for old rpm versions as we need Path::Tiny, which is not
  available there

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-10
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 2.14-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.14-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.14-4
- Perl 5.16 rebuild

* Thu Jan 19 2012 Paul Howarth <paul@city-fan.org> - 2.14-3
- Reinstate compatibility with older distributions like EL-5
- Run release tests as well as the regular test suite
- BR: perl(Test::CPAN::Meta) and perl(Test::More)
- Only drop perl(Test::MinimumVersion) as a buildreq when bootstrapping, and
  add a comment about why that's needed
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Make %%files list more explicit
- No longer need to fix permissions of Tiny.pm
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 2.14-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.12-12
- Rebuild with Perl 5.14.1
- Use perl_bootstrap macro
- Add missing BR ExtUtils::MakeMaker

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.12-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.12-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.12-8
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-5
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-4
- Rebuild for perl 5.10 (again), first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-3
- Rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-2.1
- Rebuild with TMV, tests disabled for first pass

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-2
- Rebuild for new perl

* Thu Dec 13 2007 Ralf Corsépius <rc040203@freenet.de> - 2.12-1
- Update to 2.12

* Mon Oct  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.10-1
- Updated to 2.10

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.08-1
- Updated to 2.08

* Wed May 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.07-1
- Updated to 2.07

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.06-1
- Updated to 2.06

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.05-1
- Updated to 2.05

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-2
- Rebuild for FC5 (perl 5.8.8)

* Sat Jan 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-1
- Updated to 2.04

* Fri Dec 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.03-1
- Updated to 2.03

* Mon Jun 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.02-1
- Updated to 2.02

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.01-2
- Rebuilt

* Thu Mar 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.01-1
- Updated to 2.01

* Sun Jul 25 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.00-0.fdr.1
- Updated to 2.00

* Sat Jul 10 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.9-0.fdr.1
- Updated to 1.9

* Fri Jul  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.8-0.fdr.1
- Updated to 1.8

* Tue Jun 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.7-0.fdr.1
- Updated to 1.7

* Sat Jun  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.3
- Changed URL to canonical location (bug 1140)
- Added build req perl >= 1:5.6.1 and perl(Test::More) (bug 1140)
- Added missing req perl(:MODULE_COMPAT_...) (bug 1140)
- Updated to match most recent perl spec template (bug 1140)
- Removed unneeded optimization settings and find *.bs (bug 1140)

* Thu Mar 18 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.2
- Reduced directory ownership bloat

* Thu Mar 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.1
- Updated to 1.6

* Wed Jan  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:1.5-0.fdr.1
- Updated to 1.5

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:1.3-0.fdr.1
- Initial RPM release

