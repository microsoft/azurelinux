# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if 0%{?fedora}
%bcond_without perl_Dist_CheckConflicts_enables_extra_test
%else
%bcond_with perl_Dist_CheckConflicts_enables_extra_test
%endif

Name:		perl-Dist-CheckConflicts
Version:	0.11
Release: 34%{?dist}
Summary:	Declare version conflicts for your dist
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Dist-CheckConflicts
Source0:	https://cpan.metacpan.org/modules/by-module/Dist/Dist-CheckConflicts-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Module::Runtime) >= 0.009
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.88
# Extra Tests
%if %{with perl_Dist_CheckConflicts_enables_extra_test}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
%endif
# Dependencies
# (none)

%description
One shortcoming of the CPAN clients that currently exist is that they have no
way of specifying conflicting downstream dependencies of modules. This module
attempts to work around this issue by allowing you to specify conflicting
versions of modules separately, and deal with them after the module is done
installing.

For instance, say you have a module Foo, and some other module Bar uses Foo. If
Foo were to change its API in a non-backwards-compatible way, this would cause
Bar to break until it is updated to use the new API. Foo can't just depend on
the fixed version of Bar, because this will cause a circular dependency
(because Bar is already depending on Foo), and this doesn't express intent
properly anyway - Foo doesn't use Bar at all. The ideal solution would be for
there to be a way to specify conflicting versions of modules in a way that would
let CPAN clients update conflicting modules automatically after an existing
module is upgraded, but until that happens, this module will allow users to do
this manually.

%prep
%setup -q -n Dist-CheckConflicts-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_Dist_CheckConflicts_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Dist/
%{_mandir}/man3/Dist::CheckConflicts.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-25
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-22
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-19
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.11-18
- Spec tidy-up
  - Use author-independent source URL
  - Drop support for building with Test::More < 0.88
  - Specify all build dependencies
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete
  - Fix permissions verbosely
  - Use %%license where possible

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-12
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr  3 2014 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Drop the dep on List::MoreUtils
    (https://github.com/doy/dist-checkconflicts/pull/8)
- Update patch for building with Test::More < 0.88
- Don't try to run the extra tests for EPEL builds
- Specify version requirements for extra test modules

* Wed Dec 18 2013 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - We need Module::Runtime 0.009 for module_notional_filename (#6)
- Update patch for building with Test::More < 0.88
- Drop %%defattr, redundant since rpm 4.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.09-2
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Support Perl 5.6.x

* Wed Jul 10 2013 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Instead of silently ignoring conflicts that do not compile, issue a
    conflict warning (CPAN RT#75486)
- BR: perl(Module::Runtime)
- Classify buildreqs by usage
- Explicitly run the extra tests

* Sat Jun 22 2013 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Add optional runtime conflict warnings
  - Require 5.8.1, clean up a few things and add a few more tests
  - Use Exporter instead of Sub::Exporter
- Update patch for building with Test::More < 0.88
- Drop patch for building with old ExtUtils::MakeMaker, no longer needed
- Don't need to remove empty directories from the buildroot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.02-6
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.02-5
- Pod::Coverage::TrustPod now available in all supported releases
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.02-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Tue Jan  4 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
