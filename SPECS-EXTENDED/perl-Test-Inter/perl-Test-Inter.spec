Name:           perl-Test-Inter
Version:        1.09
Release:        5%{?dist}
Summary:        Framework for more readable interactive test scripts
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-Inter
Source0:        https://cpan.metacpan.org/authors/id/S/SB/SBECK/Test-Inter-%{version}.tar.gz#/perl-Test-Inter-%{version}.tar.gz
# Remove dependencies on release tests that are skipped, proposed to upstream,
# <https://github.com/SBECK-github/Test-Inter/pull/3>
Patch0:         Test-Inter-1.09-Do-not-require-release-test-dependencies.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
# Tests only:
BuildRequires:  perl(Config)
# File::Find::Rule not used
BuildRequires:  perl(Storable) >= 1.01
BuildRequires:  perl(Test::More)
# Test::Pod 1.00 not used
# Test::Pod::Coverage 1.00 not used
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(lib)

%description
This is another framework for writing test scripts. It is loosely inspired
by Test::More, and has most of it's functionality, but it is not a drop-in
replacement.

%prep
%setup -q -n Test-Inter-%{version}
%patch0 -p1
chmod -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
unset RELEASE_TESTING TI_END TI_MODE TI_NOCLEAN TI_QUIET TI_START TI_TESTNUM \
    TI_WIDTH
make test

%files
%license LICENSE
%doc Changes README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.09-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-2
- Perl 5.30 rebuild

* Fri Mar 15 2019 Petr Pisar <ppisar@redhat.com> - 1.09-1
- 1.09 bump

* Wed Mar 13 2019 Petr Pisar <ppisar@redhat.com> - 1.08-1
- 1.08 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Perl 5.28 rebuild

* Fri Mar 16 2018 Petr Pisar <ppisar@redhat.com> - 1.07-1
- 1.07 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 10 2015 Petr Šabata <contyk@redhat.com> - 1.06-4
- Prevent the FTBFS by correcting the build time dependency list

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-2
- Perl 5.22 rebuild

* Mon Feb 16 2015 Petr Pisar <ppisar@redhat.com> - 1.06-1
- 1.06 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 1.05-2
- Perl 5.18 rebuild

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 1.05-1
- 1.05 bump

* Wed Mar 20 2013 Petr Pisar <ppisar@redhat.com> - 1.04-1
- 1.04 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.03-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 1.03-2
- Perl mass rebuild

* Thu Jul 07 2011 Petr Pisar <ppisar@redhat.com> - 1.03-1
- 1.03 bump

* Fri Jun 24 2011 Petr Pisar <ppisar@redhat.com> - 1.02-1
- 1.02 bump
- Move to vendor path
- Remove BuildRoot and defattr

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.01-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> 1.01-1
- Specfile autogenerated by cpanspec 1.78.
- Add BuildRequires covered by perl package
- Distribute examples
- Install into perl core (i.e. do not use vendor paths)
