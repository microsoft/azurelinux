Summary:        I/O on in-core objects like strings and arrays for Perl
Name:           perl-IO-stringy
Version:        2.113
Release:        4%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/IO-stringy
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-Stringy-%{version}.tar.gz#/perl-IO-Stringy-%{version}.tar.gz

BuildArch:      noarch

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)

# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)

# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# New upstream maintainer for 2.112 finally got the dist name right
Provides:       perl-IO-Stringy = %{version}-%{release}

# Avoid doc-file dependency on /usr/bin/perl
%{?perl_default_filter}

%description
This toolkit primarily provides modules for performing both traditional
and object-oriented I/O) on things *other* than normal filehandles; in
particular, IO::Scalar, IO::ScalarArray, and IO::Lines.

In the more-traditional IO::Handle front, we have IO::AtomicFile, which
may be used to painlessly create files that are updated atomically.

And in the "this-may-prove-useful" corner, we have IO::Wrap, whose
exported wraphandle() function will clothe anything that's not a blessed
object in an IO::Handle-like wrapper... so you can just use OO syntax
and stop worrying about whether your function's caller handed you a
string, a globref, or a FileHandle.

%prep
%setup -q -n IO-Stringy-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license COPYING LICENSE
%doc Changes examples/ README
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::AtomicFile.3*
%{_mandir}/man3/IO::InnerFile.3*
%{_mandir}/man3/IO::Lines.3*
%{_mandir}/man3/IO::Scalar.3*
%{_mandir}/man3/IO::ScalarArray.3*
%{_mandir}/man3/IO::Stringy.3*
%{_mandir}/man3/IO::Wrap.3*
%{_mandir}/man3/IO::WrapTie.3*

%changelog
* Tue Mar 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.113-4
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.113-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Paul Howarth <paul@city-fan.org> - 2.113-1
- Update to 2.113
  - Get rid of use of Common and TBone in all tests
  - Convert to Dist::Zilla for authoring
  - Cleaned up some of the docs (needs more)

* Sat Dec 14 2019 Paul Howarth <paul@city-fan.org> - 2.112-1
- Update to 2.112
  - Added the change log from any prior source that could be found, and
    formatted the log to fit metacpan.org loose standards
  - Change use vars qw() to our $whatever instead
  - Hide IO::WrapTie subclasses from PAUSE
  - Rebuild Makefile.PL to contain all of the prerequisites
  - Convert README to README.md
  - Fix the documentation in the main module, IO::Stringy to better indicate
    where to get info and how to use the module
  - Fix the dist's META information to indicate the original author and license
  - Add a LICENSE file
  - Add AppVeyor CI testing
  - Add Travis CI testing
  - Update t/IO_InnerFile.t to use Test::More and a proper TEMP file
    (CPAN RT#103895)
- Use author-independent source URL
- Simplify find command using -delete
- Add Provides: for perl-IO-Stringy
- Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.111-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.111-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.111-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.111-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.111-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.111-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.111-2
- Perl 5.22 rebuild

* Thu Apr 23 2015 Paul Howarth <paul@city-fan.org> - 2.111-1
- Update to 2.111
  - Update maintainer's name, which is now Dianne Skoll
- Use %%license where possible

* Mon Jan 26 2015 Petr Pisar <ppisar@redhat.com> - 2.110-28
- Filter provides/requires from docdir

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 2.110-27
- Specify all dependencies

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.110-26
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.110-23
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 2.110-21
- BuildRequire perl(lib)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.110-19
- Perl 5.16 rebuild

* Fri Apr  6 2012 Paul Howarth <paul@city-fan.org> 2.110-18
- don't build-require modules that this package provides (problem stupidly
  introduced in previous release)
- don't need to remove empty directories from buildroot
- drop %%defattr, redundant since rpm 4.4

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> 2.110-17
- spec clean-up:
  - nobody else likes macros for commands
  - use DESTDIR rather than PERL_INSTALL_ROOT
  - add buildreqs for core perl modules, which may be dual-lived

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 2.110-16
- perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-15
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> 2.110-14
- rebuild to fix problems with vendorarch/lib (#661697)

* Sun May  2 2010 Marcela Maslanova <mmaslano@redhat.com> 2.110-13
- mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Paul Howarth <paul@city-fan.org> 2.110-12
- spec cleanups (see also merge review #552564)

* Sun Dec 20 2009 Robert Scheck <robert@fedoraproject.org> 2.110-11
- rebuilt against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-10
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-9
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.110-8
- rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.110-7
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 2.110-6
- clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.110-5
- buildrequire perl(ExtUtils::MakeMaker)

* Sun Sep 17 2006 Paul Howarth <paul@city-fan.org> 2.110-4
- add dist tag
- fix argument order in find command with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 2.110-3
- use search.cpan.org download URL
- use full paths for all commands used in build
- assume rpm knows about %%check and %%{perl_vendorlib}
- cosmetic spec file changes

* Wed Apr 06 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Feb 15 2005 Ville Skyttä <ville.skytta at iki.fi> 2.110-1
- 2.110
- some specfile cleanups, bringing it closer to spectemplate-perl.spec

* Wed Dec 31 2003 Ville Skyttä <ville.skytta at iki.fi> 2.109-0.fdr.1
- update to 2.109

* Thu Oct  2 2003 Michael Schwendt <rh0212ms[AT]arcor.de> 2.108-0.fdr.4
- package is now using vendor directories

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.3
- package is now noarch
- rm-ing perllocal.pod instead of excluding it

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.2
- changed Group tag value
- "make test" in build section
- added missing directory

* Sun Jun 15 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.1
- initial build
