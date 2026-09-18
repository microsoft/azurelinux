# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-B-Utils
Version:        0.27
Release:        34%{?dist}
Summary:        Helper functions for op tree manipulation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/B-Utils
Source0:        https://cpan.metacpan.org/modules/by-module/B/B-Utils-%{version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::Depends) >= 0.302
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Task::Weaken)
# Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(subs)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Config)
BuildRequires:  perl(Test::More) >= 0.88
# Dependencies

%{?perl_default_filter}

%description
Helper functions for op tree manipulation.

%prep
%setup -q -n B-Utils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/B/
%{perl_vendorarch}/B/
%{_mandir}/man3/B::Utils.3*
%{_mandir}/man3/B::Utils::OP.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-33
- Perl 5.42 rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-30
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-26
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-23
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-20
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-17
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Paul Howarth <paul@city-fan.org> - 0.27-15
- Spec tidy-up
  - Use author-independent source URL
  - Use %%{make_build} and %%{make_install}
  - Fix permissions verbosely

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-4
- Perl 5.24 rebuild

* Thu Apr 21 2016 Paul Howarth <paul@city-fan.org> - 0.27-3
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find command using -empty and -delete
- Make %%files list more explicit

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 23 2015 Petr Šabata <contyk@redhat.com> - 0.27-1
- 0.27 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.22 rebuild

* Tue Apr 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-1
- 0.26 bump

* Tue Nov 11 2014 Petr Šabata <contyk@redhat.com> - 0.25-1
- 0.25 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-9
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.21-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.21-2
- Perl 5.16 rebuild

* Mon Mar 26 2012 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream version

* Mon Mar 12 2012 Iain Arnell <iarnell@gmail.com> 0.19-1
- update to latest upstream version

* Thu Jan 05 2012 Iain Arnell <iarnell@gmail.com> 0.17-1
- update to latest upstream version

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15-2
- Perl mass rebuild

* Wed Apr 20 2011 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version

* Sun Mar 20 2011 Iain Arnell <iarnell@gmail.com> 0.14-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 0.13-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- tweak buildrequires

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-2
- Mass rebuild with perl-5.12.0

* Thu Jan 14 2010 Iain Arnell <iarnell@gmail.com> 0.11-1
- update to latest upstream version

* Mon Jan 04 2010 Iain Arnell <iarnell@gmail.com> 0.10-1
- update to latest upstream version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-2
- rebuild against perl 5.10.1

* Wed Sep 02 2009 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream
- use perl_default_filter 

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 08 2008 Iain Arnell <iarnell@gmail.com> 0.07-2
- BR Test::Signature

* Fri Dec 05 2008 Iain Arnell 0.07-1
- Specfile autogenerated by cpanspec 1.77.
