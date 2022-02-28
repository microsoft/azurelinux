Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		perl-Class-Load-XS
Version:	0.10
Release:	12%{?dist}
Summary:	XS implementation of parts of Class::Load
License:	Artistic 2.0
URL:		https://metacpan.org/release/Class-Load-XS
Source0:	https://cpan.metacpan.org/modules/by-module/Class/Class-Load-XS-%{version}.tar.gz#/perl-Class-Load-XS-%{version}.tar.gz
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Class::Load) >= 0.20
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(constant)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(lib)
BuildRequires:	perl(Module::Implementation) >= 0.04
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Needs)
BuildRequires:	perl(Test::Without::Module)
BuildRequires:	perl(version)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides an XS implementation for portions of Class::Load.
See Class::Load for API details.

%prep
%setup -q -n Class-Load-XS-%{version}

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
%{perl_vendorarch}/auto/Class/
%{perl_vendorarch}/Class/
%{_mandir}/man3/Class::Load::XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-2
- Perl 5.26 rebuild

* Tue Apr 11 2017 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Fix test to handle altered Test::Without::Module exception message

* Fri Apr  7 2017 Paul Howarth <paul@city-fan.org> - 0.09-8
- Fix FTBFS with Test::Without::Module ≥ 0.19
  (https://github.com/moose/Class-Load/pull/2)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-6
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 0.09-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-2
- Perl 5.22 rebuild

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Updated to 0.09
  - Optimized some perl API calls
- Use %%license

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08:
  - Switched packaging to just EUMM, as MBT wants the .xs file in a different
    place
- Switch to ExtUtils::MakeMaker flow

* Thu Feb 13 2014 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07:
  - Repository moved to the github moose organization
- This release by ETHER -> update source URL
- Switch to Module::Build::Tiny flow
- Package upstream's CONTRIBUTING and README.md files
- Don't need to remove empty directories from the buildroot
- Don't bother with the author/release tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 0.06-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct  8 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06:
  - Require Class::Load 0.20 in the code, not just the distro metadata
    (CPAN RT#80002)
  - Weird classes with either an ISA or VERSION constant would cause the XS to
    blow up badly (CPAN RT#79998)
  - Fixed some broken logic that lead to a segfault from the
    014-weird-constants.t test on some Perls (CPAN RT#80059)
- Bump perl(Class::Load) version requirement to 0.20
- Drop explicit requirement for perl(Class::Load), no longer needed

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.04-2
- Perl 5.16 rebuild

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04:
  - Some small test changes for the latest Module::Implementation and
    Class::Load
- Bump Class::Load version requirement to 0.15
- BR: perl(constant), perl(Module::Implementation) ≥ 0.04, 
  perl(Test::Requires), perl(Test::Without::Module) and perl(version) for test 
  suite

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Rebuild for gcc 4.7 in Rawhide

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03:
  - Explicitly include Test::Fatal as a test prerequisite (CPAN RT#72493)

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize spec for Fedora submission

* Wed Nov 16 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
