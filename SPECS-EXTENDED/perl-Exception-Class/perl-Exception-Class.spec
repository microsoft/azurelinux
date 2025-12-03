Name:           perl-Exception-Class
Version:        1.45
Release:        1%{?dist}
Summary:        Module that allows you to declare real exception classes in Perl
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Exception-Class
Source0:        https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Exception-Class-%{version}.tar.gz#/perl-Exception-Class-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.75
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Class::Data::Inheritable) >= 0.02
BuildRequires:  perl(Devel::StackTrace) >= 2.00
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.96
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Exception::Class allows you to declare exception hierarchies in your
modules in a "Java-esque" manner.

%prep
%setup -q -n Exception-Class-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README.md
%{perl_vendorlib}/Exception/
%{_mandir}/man3/Exception::Class.3*
%{_mandir}/man3/Exception::Class::Base.3*

%changelog
* Thu Dec 19 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 1.45-1
- Update to 1.45
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - You can now pass "frame_filter", "filter_frames_early" and "skip_frames"
    to the throw() method of an exception class; these will be passed on to
    the Devel::StackTrace constructor (GH#6)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - The full_message() method in Exception::Class::Base now calls message()
    instead of accessing the object's hash key, which makes it easier to
    override message() in a subclass (GH#11)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan  5 2017 Paul Howarth <paul@city-fan.org> - 1.42-1
- Update to 1.42
  - Generated exception classes are now added to %%INC; if you subclass a
    generated class with "use base" then base.pm will no longer attempt to load
    the requested class (GH#8)

* Fri Dec  9 2016 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - Switch to GitHub Issues
- Author/Release tests moved to xt/, so don't bother trying to run them

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - Fixed broken metadata (GH#3)
- Add patch to support building without Test::Code::TidyAll

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-2
- Perl 5.22 rebuild

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - Replaced the Exception::Class::Base->NoRefs method with UnsafeRefCapture to
    match changes in Devel::StackTrace 2.00; the old method is deprecated but
    will continue to work
- Classify buildreqs by usage
- Modernize spec
- Run the author/release tests too

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - An exception without a message will now default to either the associated
    exception class description or the string "[Generic exception]" (PR #2)
  - Added field_hash() and context_hash() methods (PR #1)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.37-3
- Perl 5.18 rebuild

* Wed Jun 26 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-2
- License is GPL+ or Artistic now
- Specify all dependencies

* Sun Feb 24 2013 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - I now recommend you use Throwable instead of this module; it has a nicer,
    more modern interface
  - Fixed warning from basic.t on 5.17.x (CPAN RT#79121)
  - 1.33 did not declare any prereqs (CPAN RT#79677)
  - Require Class::Data::Inheritable ≥ 0.02
  - Fixed some stupidity in the tests that appears to have been highlighted by
    recent changes to Devel::StackTrace (CPAN RT#81245)
  - Fixed various bugs and confusion in the docs
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Make the %%files list more explicit
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop release testing (now more extensive and would fail anyway)
- Drop support for distributions older than EL-6 (test suite would need
  patching for EL-5 anyway)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-7
- Update dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.32-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.32-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Steven Pritchard <steve@kspei.com> 1.32-1
- Update to 1.32.
- License is now Artistic 2.0.
- Switch back to building with ExtUtils::MakeMaker/Makefile.PL.  (Dave
  Rolsky needs to make up his mind.)
- Add README to docs.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.29-2
- rebuild against perl 5.10.1

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-1
- Upstream update (Required by other packages, fix mass rebuild breakdowns).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Steven Pritchard <steve@kspei.com> 1.26-1
- Update to 1.26.
- Bump Devel::StackTrace dependency to 1.20.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 1.24-1
- Update to 1.24.
- Bump Devel::StackTrace dependency to 1.17.
- Clean up to match current cpanspec output.
- Improve Summary and description.
- Build with Module::Build.
- BR Test::Pod and Test::Pod::Coverage and define IS_MAINTAINER.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23-6
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.23-5
- rebuild against new perl

* Sat Dec 29 2007 Ralf Corsépius 1.23-4
- BR: perl(Test::More) (BZ 419631).
- Adjust License-tag.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.23-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.23-2
- Canonicalize Source0 URL.
- Fix find option order.
- Drop executable bit from Exception/Class.pm to avoid a rpmlint warning.

* Fri Feb 03 2006 Steven Pritchard <steve@kspei.com> 1.23-1
- Update to 1.23

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 1.22-1
- Update to 1.22

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 1.21-3
- Remove explicit core module dependencies
- Add COPYING and Artistic

* Wed Aug 17 2005 Steven Pritchard <steve@kspei.com> 1.21-2
- Minor spec cleanup

* Tue Aug 16 2005 Steven Pritchard <steve@kspei.com> 1.21-1
- Specfile autogenerated.
