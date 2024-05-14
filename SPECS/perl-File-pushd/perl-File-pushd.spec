Name:           perl-File-pushd
Version:        1.016
Release:        9%{?dist}
Summary:        Change directory temporarily for a limited scope
License:        ASL 2.0
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/File-pushd
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/File-pushd-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(lib)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.96
# Optional Tests
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
# Dependencies
Requires:       perl

%description
File::pushd does a temporary chdir that is easily and automatically reverted,
similar to pushd in some Unix command shells. It works by creating an object
that caches the original working directory. When the object is destroyed, the
destructor calls chdir to revert to the original working directory. By storing
the object in a lexical variable with a limited scope, this happens
automatically at the end of the scope.

%prep
%setup -q -n File-pushd-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.mkdn README Todo
%{perl_vendorlib}/File/
%{_mandir}/man3/File::pushd.3*

%changelog
* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.016-9
- Adding 'BuildRequires: perl-generators'.

* Fri Jul 02 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.016-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- License verified

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.016-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.016-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.016-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.016-2
- Perl 5.28 rebuild

* Mon May 21 2018 Paul Howarth <paul@city-fan.org> - 1.016-1
- Update to 1.016
  - Directories created with tempd will only be cleaned up by the PID that
    created them, not by forked children
- Switch upstream from search.cpan.org to metacpan.org

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.014-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.014-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.014-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Paul Howarth <paul@city-fan.org> - 1.014-1
- Update to 1.014
  - pushd/tempd warn if called in void context (GH#9)
  - Fixed test failures on some 5.8 perls
- Simplify find command using -delete
- Use features from recent EUMM to simplify %%install
- Use %%license
- Drop redundant Group: tag
- Make %%files list more explicit

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.009-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-3
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-2
- Perl 5.20 rebuild

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 1.009-1
- 1.009 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Petr Šabata <contyk@redhat.com> - 1.007-1
- 1.007 bump, testsuite enhancements

* Tue Apr 01 2014 Petr Šabata <contyk@redhat.com> - 1.006-1
- 1.006 bump, no code changes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.005-2
- Perl 5.18 rebuild

* Mon Mar 25 2013 Petr Šabata <contyk@redhat.com> - 1.005-1
- 1.005 bump

* Wed Mar 06 2013 Petr Pisar <ppisar@redhat.com> - 1.004-1
- 1.004 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Petr Šabata <contyk@redhat.com> - 1.003-1
- 1.003 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.002-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Petr Šabata <contyk@redhat.com> - 1.002-1
- 1.002 bump

* Thu Sep 15 2011 Petr Sabata <contyk@redhat.com> - 1.001-1
- 1.001 bump
- Remove now obsolete BuildRoot and defattr
- Migrate to EE::MM
- Correct BR

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.00-9
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.00-8
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.00-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.00-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.00-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Marcela Mašláňová <mmaslano@redhat.com> 1.00-1
- Specfile autogenerated by cpanspec 1.77.
