# Want to use Devel::GlobalDestruction::XS with perl < 5.13.7
%global want_xs 0%{?fedora} < 16 && 0%{?rhel} < 7

Name:		perl-Devel-GlobalDestruction
Version:	0.14
Release:	13%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	Expose PL_dirty, the flag that marks global destruction
URL:		https://metacpan.org/release/Devel-GlobalDestruction
Source:		https://cpan.metacpan.org/authors/id/H/HA/HAARG/Devel-GlobalDestruction-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl-generators
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Text::ParseWords)
# Module Runtime
BuildRequires:	perl(B)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Exporter::Progressive) >= 0.001011
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(threads)
BuildRequires:	perl(threads::shared)
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Use Devel::GlobalDestruction::XS on older perls
%if %{want_xs}
BuildRequires:	perl(Devel::GlobalDestruction::XS)
Requires:	perl(Devel::GlobalDestruction::XS)
%endif

%description
Perl's global destruction is a little tricky to deal with with respect to
finalizers because it's not ordered and objects can sometimes disappear.

Writing defensive destructors is hard and annoying, and usually if global
destruction is happening you only need the destructors that free up non
process local resources to actually execute.

For these constructors you can avoid the mess by simply bailing out if
global destruction is in effect.

%prep
%setup -q -n Devel-GlobalDestruction-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README t/
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::GlobalDestruction.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.14-13
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  1 2016 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Stop relying on . being in @INC
  - Switch to ExtUtils::HasCompiler to detect presence of a compiler
- Classify buildreqs by usage

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 0.13-7
- Use distribution instead of perl version to control build-time dependencies

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-3
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Include README
  - Include minimum perl version 5.6 in metadata

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov  1 2013 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Fix detection when loaded during global destruction by checking B::main_cv
    instead of B::main_start
  - Bump Sub::Exporter::Progressive dependency to fix loading in global
    destruction
- Specify all dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.18 rebuild

* Wed Apr  3 2013 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Fix upgrading from version 0.09 or older
- This release by HAARG -> update source URL

* Wed Mar 27 2013 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10 (#928262)
  - Rewrite pure-perl implementation in terms of B::main_start (greatly
    simplifies code)
  - Fix pure-perl behavior under $^C (CPAN RT#78619)
  - Separate XS portion into a compiler-optional dependency
    Devel::GlobalDestruction::XS
- Bump perl(Sub::Exporter::Progressive) version requirement to 0.001006
- Package is always noarch now
- BR:/R: perl(Devel::GlobalDestruction::XS) with perl < 5.13.7
- BR: perl(threads::shared) for the test suite

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug  9 2012 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Rewrite completely broken pure-perl GD detection under threads
  - Fix pure-perl implementation incorrectly reporting GD during END phase
- This release by RIBASUSHI -> update source URL

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Switch to Sub::Exporter::Progressive
- BR: perl(Sub::Exporter::Progressive) ≥ 0.001002 rather than plain
  perl(Sub::Exporter)

* Thu Jul 26 2012 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Actually detect errors in pure-perl test
  - Add prototype to pure-perl pre-5.14 version
- This release by FLORA -> update source URL
- BR: perl(File::Spec), perl(File::Temp) and perl(threads)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.06-2
- Perl 5.16 rebuild

* Thu Jun 14 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - De-retardize XS-less behavior under SpeedyCGI
  - Test suite now works from within space-containing paths
- This release by RIBASUSHI -> update source URL

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.05-2
- Perl 5.16 rebuild

* Fri Apr 27 2012 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Add pure-perl implementation for situations where neither ${^GLOBAL_PHASE}
    nor XS are available
- This release by DOY -> update source URL
- BR: perl(XSLoader) only if we're doing an XS build, and in that case add a
  runtime dependency on it and BR: perl(ExtUtils::CBuilder) ≥ 0.27 too
- Add runtime dependency on perl(Carp)
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 13 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - To detect a perl with ${^GLOBAL_PHASE}, check for the feature itself
    instead of a specific perl version
  - Update the documentation to reflect the use of ${^GLOBAL_PHASE} if available
  - Stop depending on Scope::Guard for the tests
  - Upgrade ppport.h from version 3.13 to 3.19
- Drop no-longer-necessary buildreq perl(Scope::Guard)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- BR: perl(XSLoader)

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.03-3
- Fedora 17 mass rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-2
- Perl mass rebuild

* Fri Jun 24 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Drop the XS code on perl versions recent enough to have ${^GLOBAL_PHASE}
    (5.13.7 onwards)
  - Require at least Perl 5.6
    - Use XSLoader without a fallback to DynaLoader
    - Use our instead of use vars
- This release by FLORA -> update source URL
- Package is noarch from perl 5.13.7
- Package Changes file
- Use %%{?perl_default_filter}

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-11
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-10
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-8
- rebuild against perl 5.10.1

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-7
- bump

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-5
- Stripping bad provides of private Perl extension libs

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 03 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-3
- bump

* Sat Nov 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-2
- tweak summary

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- clean up for review submission

* Sun Oct 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
