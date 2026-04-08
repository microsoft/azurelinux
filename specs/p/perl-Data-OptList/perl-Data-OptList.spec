# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if ! (0%{?rhel})
# Run extra test
%bcond_without perl_Data_OptList_enables_extra_test
# Run optional test
%bcond_without perl_Data_OptList_enables_optional_test
%else
%bcond_with perl_Data_OptList_enables_extra_test
%bcond_with perl_Data_OptList_enables_optional_test
%endif

Name:           perl-Data-OptList
Version:        0.114
Release:        7%{?dist}
Summary:        Parse and validate simple name/value option pairs
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-OptList
Source0:        https://cpan.metacpan.org/modules/by-module/Data/Data-OptList-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# Module Runtime
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Install) >= 0.921
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Data_OptList_enables_optional_test}
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
%endif
%if %{with perl_Data_OptList_enables_extra_test}
# Extra Tests
BuildRequires:  perl(Encode)
BuildRequires:  perl(Test::Pod) >= 1.41
%endif
# Dependencies
# (none)

%description
Hashes are great for storing named data, but if you want more than one entry
for a name, you have to use a list of pairs. Even then, this is really boring
to write:

$values = [
    foo => undef,
    bar => undef,
    baz => undef,
    xyz => { ... },
];

With Data::OptList, you can do this instead:

$values = Data::OptList::mkopt([
    qw(foo bar baz),
    xyz => { ... },
]);

This works by assuming that any defined scalar is a name and any reference
following a name is its value.

%prep
%setup -q -n Data-OptList-%{version}

# Fix shellbangs in tests
for F in t/*; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
make test
%if %{with perl_Data_OptList_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%license LICENSE
%doc Changes README t/
%{perl_vendorlib}/Data/
%{_mandir}/man3/Data::OptList.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May  7 2023 Paul Howarth <paul@city-fan.org> - 0.114-1
- Update to 0.114
  - Data::OptList now requires perl v5.12.0
  - Tests no longer add "-T" to shebang, so do not invoke taint mode

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Paul Howarth <paul@city-fan.org> - 0.113-1
- Update to 0.113 (rhbz#2157247)
  - Update author contact info
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.112-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Paul Howarth <paul@city-fan.org> - 0.112-1
- Update to 0.112
  - Update author contact info
  - Add perl version support to docs
  - Replace a "goto" deep in the guts with a sub call, for speed

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-16
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-13
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.110-2
- Perl 5.24 rebuild

* Fri Mar 25 2016 Paul Howarth <paul@city-fan.org> - 0.110-1
- Update to 0.110
  - Major optimization to mkopt
- Use %%license
- Simplify find expression using -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.109-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.109-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.109-5
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 0.109-4
- Do not hard-code interpreter name
- Specify all dependencies

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.109-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 13 2013 Paul Howarth <paul@city-fan.org> - 0.109-1
- Update to 0.109:
  - Update bugtracker and repo links

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.108-2
- Perl 5.18 rebuild

* Sat Jul  6 2013 Paul Howarth <paul@city-fan.org> - 0.108-1
- Update to 0.108:
  - Repackage, new bug tracker
- Explicitly run the extra tests
- Don't need to remove empty directories from the buildroot
- Drop obsoletes/provides for old -tests sub-package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.107-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.107-8
- Fix wrong script interpreter

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.107-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.107-6
- Perl 5.16 rebuild

* Sat Jan 21 2012 Paul Howarth <paul@city-fan.org> - 0.107-5
- obsolete/provide old -tests subpackage to support upgrades

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 0.107-4
- drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- drop redundant %%{?perl_default_filter}
- don't use macros for commands
- can't find any dependency cycle so drop %%{?perl_bootstrap} usage
- drop ExtUtils::MakeMaker version requirement to 6.30, actual working minimum

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.107-3
- package LICENSE file
- run test suite even when bootstrapping, as it should still pass
- run release tests too
- enhance %%description so it makes sense
- BR: perl(Test::More)

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.107-2
- Perl mass rebuild
- add perl_bootstrap macro

* Wed May 11 2011 Iain Arnell <iarnell@gmail.com> 0.107-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.106-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-3
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.106-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.106)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(List::Util) (version 0)
- altered br on perl(Sub::Install) (0.92 => 0.921)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(Params::Util) (version 0.14)
- added a new req on perl(Sub::Install) (version 0.921)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.104-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.104-1
- update to 0.104

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.103-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.103-1
- rebuild for new perl
- bump to 0.103
- fix license tag

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.101-2
- bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.101-1
- Specfile autogenerated by cpanspec 1.69.1.
