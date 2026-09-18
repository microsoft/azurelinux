# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MooseX-AttributeHelpers
Version:        0.25
Release:        29%{?dist}
Summary:        Extended Moose attribute interfaces (deprecated)
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MooseX-AttributeHelpers
Source0:        https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-AttributeHelpers-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build::Tiny) >= 0.034
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Module
BuildRequires:  perl(Moose) >= 0.56
BuildRequires:  perl(Moose::Meta::Attribute)
BuildRequires:  perl(Moose::Meta::Method)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util::TypeConstraints)
# Test Suite
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Exception) >= 0.21
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.94
# Dependencies
Requires:       perl(Moose) >= 0.56

%description
This distribution is deprecated. The features it provides have been added to
the Moose core code as Moose::Meta::Attribute::Native. This distribution should
not be used by any new code.

While Moose attributes provide you with a way to name your accessors,
readers, writers, clearers and predicates, this library provides commonly
used attribute helper methods for more specific types of data.

%prep
%setup -q -n MooseX-AttributeHelpers-%{version}

%build
perl Build.PL --installdirs=vendor
./Build
sed -i '1s,#!perl,#!%{__perl},' t/*.t

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%doc Changes README t/
%license LICENSE
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::AttributeHelpers.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Bool.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Collection::Array.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Collection::Bag.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Collection::Hash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Collection::ImmutableHash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Collection::List.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Counter.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Meta::Method::Curried.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Meta::Method::Provided.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::Array.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::Bag.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::Bool.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::Counter.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::Hash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::ImmutableHash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::List.3*
%{_mandir}/man3/MooseX::AttributeHelpers::MethodProvider::String.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Number.3*
%{_mandir}/man3/MooseX::AttributeHelpers::String.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Base.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection::Bag.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection::Hash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection::ImmutableHash.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection::List.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Counter.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::String.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Bool.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Collection::Array.3*
%{_mandir}/man3/MooseX::AttributeHelpers::Trait::Number.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-21
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Paul Howarth <paul@city-fan.org> - 0.25-19
- Spec tidy-up
  - Use author-independent source URL
  - Note in %%summary and %%description that distribution is deprecated
  - Classify build requirements by usage
  - Drop redundant %%?perl_default_filter
  - Fix permissions verbosely
  - Make %%files list more explicit

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-17
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-14
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 0.25-5
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.24 rebuild

* Thu Feb 18 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.25-1
- Update to 0.25

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 19 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.24-1
- Update to 0.24
- Remove upstreamed patch
- Switch to the Module::Build::Tiny workflow
- Clean up spec file

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-14
- Perl 5.22 rebuild

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-13
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Iain Arnell <iarnell@gmail.com> 0.23-11
- clean up spec for modern rpmbuild
- modernize dependency filtering

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.23-10
- Perl 5.18 rebuild
- Perl 5.18 compatibility (CPAN RT#81564)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.23-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.23-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-3
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-2
- Mass rebuild with perl-5.12.0

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- auto-update to 0.23 (by cpan-spec-update 0.01)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- auto-update to 0.22 (by cpan-spec-update 0.01)

* Tue Jul 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- auto-update to 0.21 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- drop br on CPAN
- auto-update to 0.19 (by cpan-spec-update 0.01)
- added a new req on perl(Moose) (version 0.56)

* Wed May 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- auto-update to 0.17 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Tue May 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-2
- add br on CPAN until M::I bundled version is updated

* Mon Apr 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- updating to 0.14
- POD tests are now explicitly for author/maintainers only; removing deps

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13
- note BR on Moose is now at 0.56 and is not optional :)

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-2
- ...and fix filtering.  heh.

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- update to 0.12
- switch to Module::Install incantations
- update BR's
- update provides filtering

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07-2
- rebuild for new perl

* Sat Jan 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07

* Fri Dec 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- update to 0.06

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-2
- bump

* Sun Nov 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05

* Sun Oct 28 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- Specfile autogenerated by cpanspec 1.73.
