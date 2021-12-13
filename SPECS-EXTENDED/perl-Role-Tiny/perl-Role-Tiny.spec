Name:           perl-Role-Tiny
Version:        2.001004
Release:        3%{?dist}
Summary:        A nouvelle cuisine portion size slice of Moose
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Role-Tiny
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Role-Tiny-%{version}.tar.gz#/perl-Role-Tiny-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Method::Modifiers) >= 1.05
BuildRequires:  perl(Exporter)
BuildRequires:  perl(mro)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Class::Method::Modifiers) >= 1.05
Requires:       perl(mro)

# perl-Role-Tiny was split from perl-Moo
Conflicts:      perl-Moo < 0.009014

%description
Role::Tiny is a minimalist role composition tool.

%prep
%setup -q -n Role-Tiny-%{version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}

%{_fixperms} -c %{buildroot}

%check
%{make_build} test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/Role/
%{_mandir}/man3/Role::Tiny.3*
%{_mandir}/man3/Role::Tiny::With.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.001004-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.001004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Paul Howarth <paul@city-fan.org> - 2.001004-1
- Update to 2.001004

* Wed Oct  9 2019 Paul Howarth <paul@city-fan.org> - 2.001003-1
- Update to 2.001003
- Drop redundant use of %%{?_smp_mflags} with %%{make_build}

* Thu Oct  3 2019 Paul Howarth <paul@city-fan.org> - 2.001001-1
- Update to 2.001001
- This release by HAARG: update source URL
- Classify buildreqs by usage
- Fix permissions verbosely
- Drop redundant use of %%{?perl_default_filter}

* Wed Aug 07 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000008-1
- Update to 2.000008

* Sun Aug 04 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000007-1
- Update to 2.000007
- Replace calls to %%{__perl} with /usr/bin/perl
- Replace calls to "make pure_install" with %%{make_install}
- Replace calls to "make" with %%{make_build}
- Tage LICENSE file as such

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-8
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.000006-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 12 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000006-1
- Update to 2.000006

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000005-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.000005-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 06 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000005-1
- Update to 2.000005

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.000003-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.000003-2
- Perl 5.24 rebuild

* Fri May 06 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000003-1
- Update to 2.000003

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.000001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000001-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.000001-2
- Perl 5.22 rebuild

* Sat Apr 25 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000001-1
- Update to 2.000001

* Sun Mar 01 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.000000-1
- Update to 2.000000

* Mon Nov 10 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.003004-1
- Update to 1.003004

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.003003-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.003003-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Paul Howarth <paul@city-fan.org> - 1.003003-1
- Update to 1.003003
  - Overloads specified as method names rather than subrefs are now applied
    properly
  - Allow superclass to provide conflicting methods (CPAN RT#91054)
  - Use ->is_role internally to check if a package is a role
  - Document that Role::Tiny applies strict and fatal warnings
- Require Class::Method::Modifiers at runtime
- Make %%files list more explicit

* Tue Mar 25 2014 Petr Pisar <ppisar@redhat.com> - 1.003002-2
- Break build-cycle: perl-Role-Tiny → perl-namespace-autoclean → perl-Moose →
  perl-Test-Spelling → perl-Pod-Spell → perl-File-ShareDir-ProjectDistDir →
  perl-Path-IsDev → perl-Role-Tiny

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 1.003002-1
- 1.003002 bump

* Fri Aug 16 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003001-1
- 1.003001 bump
- Specify all dependencies

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.002005-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.002005-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Iain Arnell <iarnell@gmail.com> 1.002004-1
- update to latest upstream version

* Sun Oct 28 2012 Iain Arnell <iarnell@gmail.com> 1.002002-1
- update to latest upstream version

* Sat Oct 27 2012 Iain Arnell <iarnell@gmail.com> 1.002001-1
- update to latest upstream version

* Sat Oct 20 2012 Iain Arnell <iarnell@gmail.com> 1.002000-1
- update to latest upstream version

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 1.001005-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Iain Arnell <iarnell@gmail.com> 1.001004-1
- update to latest upstream version

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.001002-2
- Perl 5.16 rebuild

* Tue May 08 2012 Iain Arnell <iarnell@gmail.com> 1.001002-1
- update to latest upstream version

* Fri Apr 27 2012 Iain Arnell <iarnell@gmail.com> 1.001001-1
- update to latest upstream version
- don't explicity require Class::Method::Modifiers

* Wed Apr 04 2012 Iain Arnell <iarnell@gmail.com> 1.000001-1
- update to latest upstream version

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 1.000000-3
- explicitly conflict with perl-Moo < 0.009014; this module used to be
  distributed as part of Moo

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 1.000000-2
- fix spelling of cuisine in summary

* Sun Apr 01 2012 Iain Arnell <iarnell@gmail.com> 1.000000-1
- Specfile autogenerated by cpanspec 1.79.
