%if ! (0%{?rhel})
# Run optional test
%bcond_without perl_Package_Stash_XS_enables_optional_test
%else
%bcond_with perl_Package_Stash_XS_enables_optional_test
%endif

Name:		perl-Package-Stash-XS
Version:	0.30
Release:	1%{?dist}
Summary:	Faster and more correct implementation of the Package::Stash API
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Package-Stash-XS
Source0:	https://cpan.metacpan.org/modules/by-module/Package/Package-Stash-XS-%{version}.tar.gz
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
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(B)
BuildRequires:	perl(base)
BuildRequires:	perl(blib)
BuildRequires:	perl(constant)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(lib)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Needs)
%if %{with perl_Package_Stash_XS_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(Package::Anon)
BuildRequires:	perl(Variable::Magic)
%endif
# Dependencies
# (none)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This is a back-end for Package::Stash, which provides the functionality in a
way that's less buggy and much faster. It will be used by default if it's
installed, and should be preferred in all environments with a compiler.

%prep
%setup -q -n Package-Stash-XS-%{version}

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
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorarch}/auto/Package/
%{perl_vendorarch}/Package/
%{_mandir}/man3/Package::Stash::XS.3*

%changelog
* Mon Feb 27 2025 Sumit Jena <v-sumitjena@microsoft.com> - 0.30-1
- Update to version 0.30
- License verified

* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com> - 0.29-7
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.29-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  2 2019 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29
  - Quiet compiler warning (GH#2)
  - Canonical repository moved to https://github.com/moose/Package-Stash-XS
- Package new CONTRIBUTING file
- Don't bother running the extra tests
- Drop EL-5 support
  - Drop legacy Group: tag
  - Drop explicit buildroot cleaning in %%install section
  - BR: perl-devel and perl(Variable::Magic) unconditionally
  - Drop workaround for building with Test::More < 0.88

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-18
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-14
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Paul Howarth <paul@city-fan.org> - 0.28-12
- Fix FTBFS when perl is not in the SRPM build root

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-11
- Perl 5.24 rebuild

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 0.28-10
- Classify buildreqs by usage
- Use %%license where possible
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-7
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.28-2
- Perl 5.18 rebuild

* Tue Jul 16 2013 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - Fix test issue

* Tue Jul 16 2013 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Handle magic more correctly in add_symbol and get_or_add_symbol
- Add upstream patch to avoid build dependency on Package::Stash
- BR: perl(Variable::Magic) for the test suite
- Update patch for building with old Test::More versions

* Thu Jan 24 2013 Paul Howarth <paul@city-fan.org> - 0.26-2
- BR: perl(Package::Anon) if we have Perl ≥ 5.14

* Fri Jan  4 2013 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - Internal refactorings to support Package::Anon stashes
- BR: perl(base) and perl(Test::Requires) for test suite
- Update patch for old distro compatibility
- Explicitly run the release/author tests

* Mon Aug 27 2012 Petr Pisar <ppisar@redhat.com> - 0.25-7
- Disable author tests on RHEL >= 7

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.25-6
- Drop EPEL-4 support
  - Test::LeakTrace now universally available
  - Suitably recent version of ExtUtils::MakeMaker now universally available
  - Drop %%defattr, redundant since rpm 4.4
- BR: perl(File::Temp)
- Don't need to remove empty directories from the buildroot

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.25-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.25-3
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.25-2
- Use %%{_fixperms} macro instead of our own chmod incantation

* Tue Sep  6 2011 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Invalid package names (for instance, Foo:Bar) are not allowed
  - Invalid stash entry names (anything containing ::) are not allowed
- Update patches to apply cleanly

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Fix the test for scalar values, again
  - Disallow assigning globrefs to scalar glob slots (this doesn't actually
    make any sense)
- Update patches for old ExtUtils::MakeMaker and Test::More versions
- perl(Pod::Coverage::TrustPod) now available in EPEL-4 too
- Don't use macros for commands

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.22-2
- Perl mass rebuild

* Sat Mar  5 2011 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Make the namespace cache lazy and weak, in case the stash is deleted
  - However, this doesn't work on 5.8, so disable the namespace caching
    entirely there
- Update patches to apply cleanly

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Make the leak tests author-only, since some smokers run release tests
  - Fix some XS forward compat stuff
- Update patches to apply cleanly

* Wed Jan 12 2011 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Lower perl prereq to 5.8.1
  - Make the leak tests release-only
- Update patches to apply cleanly
- Drop no-Test::Requires patch, no longer needed
- Drop buildreq perl(Test::Requires), no longer needed
- Add patch to skip memory leak tests if we don't have Test::LeakTrace

* Thu Jan  6 2011 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19 (more correct validity test for scalars)
- Update patch for old Test::More versions

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.17-2
- Sanitize spec for Fedora submission

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.17-1
- Initial RPM build
