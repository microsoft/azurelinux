Vendor:         Microsoft Corporation
Distribution:   Mariner
# Run optional test
%{bcond_without perl_Data_Peek_enables_option_test}

Name:           perl-Data-Peek
Version:        0.49
Release:        2%{?dist}
Summary:        Collection of low-level debug facilities
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Data-Peek
Source0:        https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/Data-Peek-%{version}.tgz
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warnings)
%if %{with perl_Data_Peek_enables_option_test}
# Optional tests:
BuildRequires:  perl(Perl::Tidy) >= 20120714
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
Data::Peek started off as DDumper being a wrapper module over Data::Dumper,
but grew out to be a set of low-level data introspection utilities that no
other module provided yet, using the lowest level of the perl internals API
as possible.

%prep
%setup -q -n Data-Peek-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc ChangeLog README CONTRIBUTING.md
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{perl_vendorarch}/DP.pm
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.49-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-1
- 0.49 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-3
- Perl 5.28 rebuild

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 0.48-2
- Rebuild with new redhat-rpm-config/perl build flags

* Tue Feb 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.48-1
- 0.48 bump

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-4
- Add build-require gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Petr Pisar <ppisar@redhat.com> - 0.47-1
- 0.47 bump

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-2
- Perl 5.24 rebuild

* Thu May 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-1
- 0.46 bump

* Wed Feb 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-1
- 0.45 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-2
- Perl 5.22 rebuild

* Wed Mar 25 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-1
- 0.44 bump

* Mon Feb 16 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump

* Mon Jan 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-1
- 0.42 bump

* Mon Sep 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-1
- 0.41 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-1
- 0.40 bump

* Wed Aug 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump
- Specify all dependencies
- Modernize spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.38-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Marcela Mašláňová <mmaslano@redhat.com> 0.38-1
- Update to 0.38

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.33-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.33-2
- Perl mass rebuild

* Mon Apr 04 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.33-1
- Specfile autogenerated by cpanspec 1.79.
- apply patch to automatically create alias -> DP on Data::Peek
