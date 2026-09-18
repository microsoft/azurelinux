# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Suspect that upstream prefers single-decimal versions
%global cpan_version 3.75
%global rpm_version 3.7.5

# This arch-specific package has no binaries and generates no debuginfo
%global debug_package %{nil}

Name:		perl-common-sense
Summary:	"Common sense" Perl defaults 
Version:	%{rpm_version}
Release:	20%{?dist}
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/common-sense
Source0:	https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/common-sense-%{cpan_version}.tar.gz
Patch1:		common-sense-3.71-podenc.patch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(feature)
BuildRequires:	perl(strict)
BuildRequires:	perl(utf8)
BuildRequires:	perl(warnings)
BuildRequires:	/usr/bin/pod2man
BuildRequires:	/usr/bin/pod2text
# Module Runtime
# (no additional dependencies)
# Test Suite
# (no additional dependencies)
# Dependencies

%description
This module implements some sane defaults for Perl programs, as defined
by two typical (or not so typical - use your common sense) specimens of
Perl coders:

It's supposed to be mostly the same, with much lower memory usage, as:

	use utf8;
	use strict qw(vars subs);
	use feature qw(say state switch);
	use feature qw(unicode_strings unicode_eval current_sub fc evalbytes);
	no feature qw(array_base);
	no warnings;
	use warnings qw(FATAL closed threads internal debugging pack
			prototype inplace io pipe unpack malloc
			deprecated glob digit printf layer
			reserved taint closure semicolon);
	no warnings qw(exec newline unopened);

%prep
%setup -q -n common-sense-%{cpan_version}

# Specify POD encoding
%patch -P 1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

# Have a non-empty manpage
pod2man sense.pod > %{buildroot}%{_mandir}/man3/common::sense.3pm

%check
make test

%files
%license LICENSE
%doc Changes README t/
%dir %{perl_vendorarch}/common/
%{perl_vendorarch}/common/sense.pm
%doc %{perl_vendorarch}/common/sense.pod
%{_mandir}/man3/common::sense.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Paul Howarth <paul@city-fan.org> - 3.7.5-15
- Use %%license unconditionally

* Wed Aug 09 2023 Petr Pisar <ppisar@redhat.com> - 3.7.5-14
- Adapt a spec file to rpm-4.18.92

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Michal Josef Špaček <mspacek@redhat.com> - 3.7.5-12
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.5-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.5-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.5-3
- Perl 5.32 re-rebuild updated packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.5-2
- Perl 5.32 rebuild

* Thu Apr  2 2020 Paul Howarth <paul@city-fan.org> - 3.7.5-1
- Update to 3.75
  - Make build (more) reproducible
  - Removed "portable" from the warnings list, as 32-bit perls (as opposed to
    32-bit platforms) are practically extinct and it warns about a weird subset
    of operations, e.g. 64-bit hex() is not ok, 64-bit addition is fine, makes
    no sense; additionally, other than hex/oct etc. harassment, there is
    nothing in this category that otherwise could be useful
- Specify all build dependencies
- Drop ancient obsoletes/provides for removed tests sub-package
- Drop redundant buildroot cleaning in %%install section
- Simplify find command using -delete
- Fix permissions verbosely

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-12
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-9
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.4-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Paul Howarth <paul@city-fan.org> - 3.7.4-1
- Update to 3.74
  - The generated README file was empty
- Use %%license where possible

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.3-4
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.7.3-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Paul Howarth <paul@city-fan.org> - 3.7.3-1
- Update to 3.73
  - Move pod to separate file, to further improve loading times
  - Make it arch-specific, adding a test that warns when an old version is
    still installed
  - Due to a logic glitch, warnings were not enabled at all on 5.16
  - Remove "deprecated", as it turned out to be yet another time bomb as p5p
    don't care the least about backwards compatibility anymore
    (https://rt.perl.org/Public/Bug/Display.html?id=119123)
- Manually generate the manpage so we get a non-empty one

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.6-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 3.6-2
- Perl 5.16 rebuild

* Sun Jun 17 2012 Paul Howarth <paul@city-fan.org> - 3.6-1
- Update to 3.6:
  - Work around more 5.16 breakage - $^H doesn't work as nicely as P5P make
    you believe
  - Add features: unicode_strings current_sub fc evalbytes
  - Disable features: array_base

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 3.5-2
- Perl 5.16 rebuild

* Sat Mar 24 2012 Paul Howarth <paul@city-fan.org> - 3.5-1
- Update to 3.5:
  - Localise $^W, as this causes warnings with 5.16 when some lost soul uses
    -w; common::sense doesn't support $^W, but tries to shield module authors
    and programs from its ill effects
- Don't need to remove empty directories from buildroot
- Drop %%defattr, redundant since rpm 4.4

* Sat Jan 21 2012 Paul Howarth <paul@city-fan.org> - 3.4-5
- Obsolete/provide old -tests subpackage to support upgrades

* Thu Jan 19 2012 Paul Howarth <paul@city-fan.org> - 3.4-4
- Reinstate compatibility with older distributions like EL-5
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't use macros for commands
- Make %%files list more explicit
- Use tabs

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.4-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> - 3.4-1
- Update to latest upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Iain Arnell <iarnell@gmail.com> - 3.3-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0-2
- Mass rebuild with perl 5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> - 3.0-1
- Update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- Updating to latest GA CPAN version (3.0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.0-3
- Rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.0-2
- Update summary (though now we deviate from upstream)

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.0-1
- Auto-update to 1.0 (by cpan-spec-update 0.01)

* Fri Aug 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
