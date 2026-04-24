# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Any-Moose
Summary:        Use Moose or Mouse automagically (DEPRECATED)
Version:        0.27
Release: 34%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Any-Moose
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Any-Moose-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Moose)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Mouse) >= 0.40
BuildRequires:  perl(Test::More) >= 0.88
%if !0%{?perl_bootstrap}
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(MouseX::Types)
%endif
# Dependencies
# Virtual provides in perl-Moose and perl-Mouse
Requires:       perl(Any-Moose) >= 0.40
Requires:       perl(Carp)

%description
Any::Moose is deprecated - please use Moo for new code.

This module allows one to take advantage of the features Moose/Mouse
provides, while allowing one to let the program author determine if Moose
or Mouse should be used; when use'd, we load Mouse if Moose isn't already
loaded, otherwise we go with Moose.

%prep
%setup -q -n Any-Moose-%{version}

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
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/Any/
%{_mandir}/man3/Any::Moose.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-25
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-24
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Paul Howarth <paul@city-fan.org> - 0.27-22
- Post-bootstrap rebuild for EPEL-9

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-20
- Perl 5.34 re-rebuild of bootstrapped packages

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-19
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-16
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-15
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-12
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  8 2016 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Add deprecation warning when this module is used
- This release by ETHER → update source URL
- Package CONTRIBUTING file
- Make %%files list more explicit
- Use NO_PERLLOCAL as well as NO_PACKLIST with Makefile.PL
- Drop redundant %%{?perl_default_filter}
- Drop redundant Group: tag

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Petr Šabata <contyk@redhat.com> - 0.26-1
- 0.26 bump

* Fri Nov 07 2014 Petr Šabata <contyk@redhat.com> - 0.24-1
- 0.24 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.21-6
- Drop an extra dependency

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.21-4
- Perl 5.18 rebuild

* Sat Aug  3 2013 Jochen Schmitt <Jochen herr-schmitt de> - 0.21-3
- Rebuilt for perl-5.18.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream version (still deprecated)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 31 2012 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream version which is deprecated in favor of perl-Moo

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.18-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.18-4
- Perl 5.16 rebuild

* Fri Apr 06 2012 Iain Arnell <iarnell@gmail.com> 0.18-3
- avoid circular build-dependency with perl-MooseX-Types (patch from Paul
  Howarth rhbz#810521)

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.18-2
- drop tests-subpackage; move tests to main package documentation

* Fri Jan 13 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.18-1
- Update to 0.18

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 0.17-1
- update to latest upstream version
- require perl(Any-Moose) - provided by both perl-Moose and perl-Mouse

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.15-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.15-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jun 27 2010 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(Mouse) (0.21 => 0.40)
- altered req on perl(Mouse) (0.21 => 0.40)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-2
- rebuild against perl 5.10.1

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered req on perl(Mouse) (0.20 => 0.21)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- auto-update to 0.09 (by cpan-spec-update 0.01)
- altered br on perl(Mouse) (0.20 => 0.21)

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- submission

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
