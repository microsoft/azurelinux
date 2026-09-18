# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Data-Compare
Version:        1.29
Release:        7%{?dist}
Summary:        Compare perl data structures
# Some of the metadata files suggest GPL2 rather than GPL (any version)
# but the module is actually licensed "same as perl"
# See "COPYRIGHT and LICENCE" in lib/Data/Compare.pm
# See also: https://github.com/DrHyde/perl-modules-Data-Compare/issues/15
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Compare
Source0:        https://cpan.metacpan.org/modules/by-module/Data/Data-Compare-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone) >= 0.43
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More) >= 0.88
# Optional Tests
BuildRequires:  perl(JSON)
BuildRequires:  perl(Scalar::Properties)
BuildRequires:  perl(Test::Pod) >= 1.00
# Dependencies
# (none)

%description
This module compares arbitrary data structures to see if they are copies
of each other.

%prep
%setup -q -n Data-Compare-%{version}

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
%license ARTISTIC.txt GPL2.txt
%doc CHANGELOG MAINTAINERS-NOTE
%dir %{perl_vendorlib}/Data/
%dir %{perl_vendorlib}/Data/Compare/
%dir %{perl_vendorlib}/Data/Compare/Plugins/
%doc %{perl_vendorlib}/Data/Compare/Plugins.pod
%{perl_vendorlib}/Data/Compare.pm
%{perl_vendorlib}/Data/Compare/Plugins/Scalar/
%{_mandir}/man3/Data::Compare.3*
%{_mandir}/man3/Data::Compare::Plugins.3*
%{_mandir}/man3/Data::Compare::Plugins::Scalar::Properties.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr 22 2023 Paul Howarth <paul@city-fan.org> - 1.29-1
- Update to 1.29
  - Skip taint-mode tests if perl was built without taint support

* Wed Mar 15 2023 Paul Howarth <paul@city-fan.org> - 1.28-1
- Update to 1.28
  - Bug fix: undef values in hashes were treated incorrectly: need to check
    for existence, not definedness before comparing (GH#21)
- Use SPDX-format license tag
- Use %%license unconditionally
- Drop NOTES and README files as they provide nothing useful to users

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov  5 2019 Tom Callaway <spot@fedoraproject.org> - 1.27-1
- update to 1.27

* Thu Sep 19 2019 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26
  - Minor code quality improvements from Alberto Simõe
  - Reinstate check for cwd being inaccessible
- Use author-independent source URL
- Simplify find command using -delete

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-2
- Perl 5.22 rebuild

* Thu Dec 11 2014 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25
  - Add tests for really big data structures (but not yet working)
  - Check for taint-mode less insanely
  - Don't delay loading File::Find::Rule (CPAN RT#87554)
  - Bump the required JSON.pm version for tests - something's a bit broken
    around about v2.53
  - Add tests and patch to use refaddr and reftype to 'do the right thing' when
    comparing objects that overload numification and stringification
- Classify buildreqs by usage
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use %%license where possible
- Make %%files list more explicit

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 1.22-8
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.22-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.22-2
- Perl mass rebuild

* Tue Jun  7 2011 Tom Callaway <spot@fedoraproject.org> - 1.22-1
- update to 1.22
- add Requires: perl(File::Find::Rule)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.21-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.21-1
- Upstream update.
- spec file massaging.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-2
- Rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-1
- 0.17

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-1
- Update to 0.15.

* Sun Nov  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-2
- New BR: perl(Clone) is needed by t/deep-objects.t.

* Sun Nov  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-1
- Update to 0.14.

* Sun Apr 09 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.13-1
- First build.
