Name:           perl-Class-XSAccessor
Version:        1.19
Release:        22%{?dist}
Summary:        Generate fast XS accessors without run-time compilation
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Class-XSAccessor
Source0:        https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/Class-XSAccessor-%{version}.tar.gz#/perl-Class-XSAccessor-%{version}.tar.gz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(Time::HiRes)
# Dependencies:
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Do not require private module
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}perl\\(Class::XSAccessor::Heavy\\)

%description
Class::XSAccessor implements fast read, write and read/write accessors in
XS. Additionally, it can provide predicates such as has_foo() for testing
whether the attribute foo is defined in the object. It only works with
objects that are implemented as ordinary hashes. Class::XSAccessor::Array
implements the same interface for objects that use arrays for their
internal representation.

%prep
%setup -q -n Class-XSAccessor-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Class*
%{_mandir}/man3/Class::*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 0.19-22
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.19-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-15
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-11
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-9
- Perl 5.24 rebuild

* Wed Apr 20 2016 Paul Howarth <paul@city-fan.org> - 1.19-8
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-5
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Petr Pisar <ppisar@redhat.com> - 1.19-1
- 1.19 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.18-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Petr Šabata <contyk@redhat.com> - 1.18-1
- 1.18 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-1
- 1.16 bump
- Replace PERL_INSTALL_ROOT with DESTDIR
- Add BR perl(Carp)

* Fri Aug 31 2012 Petr Šabata <contyk@redhat.com> - 1.14-1
- 1.14 bump (no changes for Fedora)
- Drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.13-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Petr Šabata <contyk@redhat.com> - 1.13-1
- 1.13 bump
- Remove BuildRoot and defattr
- Remove ::Array self-obsolete

* Mon Sep 05 2011 Petr Sabata <contyk@redhat.com> - 1.12-1
- 1.12 bump

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 1.11-4
- RPM 4.9 dependency filtering added

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Petr Sabata <psabata@redhat.com> - 1.11-1
- New upstream release, v1.11

* Fri Dec  3 2010 Petr Sabata <psabata@redhat.com> - 1.10-1
- New upstream release, v1.10

* Mon Nov  8 2010 Petr Sabata <psabata@redhat.com> - 1.09-1
- New upstream release, v1.09

* Wed Sep 29 2010 jkeating - 1.08-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Petr Pisar <ppisar@redhat.com> - 1.08-2
- Do not require private perl(Class::XSAccessor::Heavy)
- Correct Summary spelling
- Enable tests

* Mon Sep 20 2010 Petr Sabata <psabata@redhat.com> - 1.08-1
- New upstream release, v1.08

* Thu Sep  2 2010 Petr Sabata <psabata@redhat.com> - 1.07-1
- New upstream release, v1.07

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-5
- Mass rebuild with perl-5.12.0

* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-4
- rebuild with obsoletes in spec

* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-3
- Class::XSAccessor::Array became a part of this package - fixes conflict of man

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.05-2
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Stepan Kasal <skasal@redhat.com> - 1.03-2
- rebuild with AutoXS::Header 1.02

* Mon Jun  1 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-1
- update

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Marcela Mašláňová <mmaslano@redhat.com> 0.14-1
- update to 0.14

* Fri Dec 05 2008 Marcela Mašláňová <mmaslano@redhat.com> 0.11-1
- Specfile autogenerated by cpanspec 1.77.
