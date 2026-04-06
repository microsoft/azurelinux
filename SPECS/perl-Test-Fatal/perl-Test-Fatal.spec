# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if ! (0%{?rhel})
# Run extra test
%bcond_without perl_Test_Fatal_enables_extra_test
# Run optional test
%bcond_without perl_Test_Fatal_enables_optional_test
%else
%bcond_with perl_Test_Fatal_enables_extra_test
%bcond_with perl_Test_Fatal_enables_optional_test
%endif

Summary:	Incredibly simple helpers for testing code with exceptions 
Name:		perl-Test-Fatal
Version:	0.017
Release:	8%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Test-Fatal
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-Fatal-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.78
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Try::Tiny) >= 0.07
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(overload)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More) >= 0.65
%if %{with perl_Test_Fatal_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
%endif
%if %{with perl_Test_Fatal_enables_extra_test}
# Extra Tests
BuildRequires:	perl(Encode)
BuildRequires:	perl(Test::Pod) >= 1.41
%endif
# Runtime
Requires:	perl(Test::Builder)

%description
Test::Fatal is an alternative to the popular Test::Exception. It does much
less, but should allow greater flexibility in testing exception-throwing code
with about the same amount of typing.

%prep
%setup -q -n Test-Fatal-%{version}

# Avoid doc-file dependencies
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if %{with perl_Test_Fatal_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Fatal.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Update packaging and metadata
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.016-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 10 2020 Paul Howarth <paul@city-fan.org> - 0.016-1
- Update to 0.016
  - Add default descriptions to tests
  - Work on ancient Test::Builder code
- Use author-independent source URL
- Simplify find command using -delete
- Fix permissions verbosely

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-16
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.014-2
- Perl 5.22 rebuild

* Wed Dec 10 2014 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Avoid assuming that t/todo.t is always called t/todo.t
- Classify buildreqs by usage
- Use %%license

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 24 2013 Paul Howarth <paul@city-fan.org> - 0.013-1
- Update to 0.013
  - Rebuild to get a newer compile test that may work on 5.6.x

* Tue Sep 17 2013 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012
  - Go back to auto-detecting the required Test::More, reverting the changes
    made for CPAN RT#62699
- Drop support for all current EL releases (5 and 6) since we need Test::More
  version 0.96 or later for the test suite

* Tue Sep 17 2013 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - More clearly (and correctly) document the way NOT to use Test::Fatal
  - Try to fix $TODO not working when the user test uses $T::B::Level
- Explicitly run the extra tests
- Package examples directory as documentation
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.010-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.010-2
- Perl 5.16 rebuild

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Avoid tickling an overloading bug in perl 5.6 during testing
    (CPAN RT#74847)

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> - 0.009-1
- Update to 0.009
  - Advise against using isnt(exception{...},undef)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Revert the mistake by which 0.004 allowed blocks after "exception" as well
    as "success"
- BR: perl(Carp)
- Update patch for building with ExtUtils::MakeMaker < 6.30

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.006-2
- Perl mass rebuild

* Thu Jun  2 2011 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Crank back the Test::More and Exporter requirements (CPAN RT#62699)
  - Add lives_ok and dies_ok emulation (CPAN RT#67598)
- Versions patch replaced by workaround for old ExtUtils::MakeMaker
- BR: perl(Test::Builder::Tester)

* Tue Apr 26 2011 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005
  - Fix the logic that picks tests for 5.13.1+

* Tue Apr 26 2011 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004
  - success blocks now allow trailing blocks like finally, catch, etc.
- Remove remaining uses of macros for commands
- Re-order %%install section to conventional position in spec

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 29 2010 Paul Howarth <paul@city-fan.org> - 0.003-1
- Update to 0.003
  - More tests for false exceptions, especially on 5.13
- Update versions patch

* Thu Oct 28 2010 Paul Howarth <paul@city-fan.org> - 0.002-1
- Update to 0.002
  - Add tests for handling of false exceptions
  - Fix precedence error in documentation
- Update versions patch

* Wed Oct 27 2010 Paul Howarth <paul@city-fan.org> - 0.001-2
- Sanitize spec for Fedora submission

* Tue Oct 26 2010 Paul Howarth <paul@city-fan.org> - 0.001-1
- Initial RPM version
