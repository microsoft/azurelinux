# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-aliased
Version:	0.34
Release:	31%{?dist}
Summary:	Use shorter versions of class names
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/aliased
Source0:	https://cpan.metacpan.org/authors/id/E/ET/ETHER/aliased-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Module::Build::Tiny) >= 0.039
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(B)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
# Runtime
Requires:	perl(Carp)

%description
aliased is simple in concept but is a rather handy module. It loads the
class you specify and exports into your namespace a subroutine that returns
the class name. You can explicitly alias the class to another name or, if
you prefer, you can do so implicitly. In the latter case, the name of the
subroutine is the last part of the class name.

%prep
%setup -q -n aliased-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/aliased.pm
%{_mandir}/man3/aliased.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.34-25
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-22
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-19
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-16
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-2
- Perl 5.22 rebuild

* Tue Jan  6 2015 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Re-release to fix problematic $VERSION declaration (CPAN RT#101095)

* Mon Dec 22 2014 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Don't inherit from Exporter
  - Fix docs issues
  - Fix warnings on perl 5.21.6 and up (CPAN RT#100359)
- This release by ETHER → update source URL
- Switch to Module::Build::Tiny flow
- Modernize spec, dropping support for ancient distributions

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.31-2
- Perl 5.18 rebuild

* Tue Feb 19 2013 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Added prefix() function (CPAN RT#48289)
  - Moved Test::More to build_requires (CPAN RT#48926)
  - Moved author tests to xt/author
- Explicitly run the author tests
- BR: perl(lib) and perl(Test::More) for the test suite
- Add patch to support building with Test::More < 0.88
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.30-9
- Perl 5.16 rebuild

* Mon Jan 16 2012 Paul Howarth <paul@city-fan.org> - 0.30-8
- Spec clean-up:
  - BR: perl(Exporter)
  - Make %%files list more explicit
  - Don't use macros for commands
  - Use tabs

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.30-6
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.30-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.30-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.30-2
- rebuild against perl 5.10.1

* Sat Aug 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.30-1
- auto-update to 0.30 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- update to 0.22

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-2
- rebuild for new perl

* Fri Mar 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- update to 0.21

* Thu Oct 12 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.20-2
- bump

* Mon Oct 09 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- Specfile autogenerated by cpanspec 1.69.
