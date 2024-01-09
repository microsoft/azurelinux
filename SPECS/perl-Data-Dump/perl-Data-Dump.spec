Name:           perl-Data-Dump
Version:        1.25
Release:        1%{?dist}
Summary:        Pretty printing of data structures
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Data-Dump
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/Data-Dump-%{version}.tar.gz#/perl-Data-Dump-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
# XXX: BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
# Really optional
Suggests:       perl(MIME::Base64)

%description
This module provides a single function called dump() that takes a list of
values as its argument and produces a string as its result. The string
contains Perl code that, when evaled, produces a deep copy of the original
arguments. The string is formatted for easy reading.

%prep
%setup -q -n Data-Dump-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jan 09 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.25-1
- Azure Linux 3.0 - upgrade to 1.25 

* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 1.23-15
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.23-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Petr Šabata <contyk@redhat.com> - 1.23-1
- 1.23 bump
- Drop the test suite from %%doc

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-4
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Iain Arnell <iarnell@gmail.com> 1.22-1
- update to latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.21-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 1.21-2
- Perl 5.16 rebuild

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> 1.21-1
- update to latest upstream version
- add perl_default_filter

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.19-2
- Perl mass rebuild

* Thu May 12 2011 Iain Arnell <iarnell@gmail.com> 1.19-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.15-2
- rebuild against perl 5.10.1

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- auto-update to 1.15 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.14-1
- update to 1.14

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.08-4
- rebuild for new perl

* Mon Oct 22 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.08-3
- update license tag: GPL -> GPL+

* Mon Apr 30 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.08-2
- bump

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.08-1
- Specfile autogenerated by cpanspec 1.70.
