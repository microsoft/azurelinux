Vendor:         Microsoft Corporation
Distribution:   Mariner
# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Devel_Size_enables_optional_test
%else
%bcond_with perl_Devel_Size_enables_optional_test
%endif

Name:           perl-Devel-Size
Version:        0.83
Release:        6%{?dist}
Summary:        Perl extension for finding the memory usage of Perl variables
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Devel-Size
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-Size-%{version}.tar.gz#/perl-Devel-Size-%{version}.tar.gz
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.5
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(feature)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
%if %{with perl_Devel_Size_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
# Required by t/warnings.t, but not on CPAN
#BuildRequires:  perl(Test::PerlRun)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%?perl_default_filter

%description
This module figures out the real sizes of Perl variables in bytes. Call
functions with a reference to the variable you want the size of. If the
variable is a plain scalar it returns the size of the scalar. If the
variable is a hash or an array, use a reference when calling.

%prep
%setup -q -n Devel-Size-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}" \
                 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc CHANGES
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Devel*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.83-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 0.83-5
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-2
- Perl 5.30 rebuild

* Wed May 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-1
- 0.83 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.82-2
- Perl 5.28 rebuild

* Sat Jun 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.82-1
- 0.82 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 0.81-1
- 0.81 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-2
- Perl 5.22 rebuild

* Tue Apr 28 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.80-1
- 0.80 bump

* Fri Jan 09 2015 Petr Pisar <ppisar@redhat.com> - 0.79-7
- Specify all dependencies

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.79-6
- Perl 5.20 rebuild
- Added patches provided by upstream

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.79-2
- Perl 5.18 rebuild

* Tue May 28 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.79-1
- Update to 0.79
- BR: perl(XSLoader)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Robin Lee <cheeselee@fedoraproject.org> 0.78-1
- Update to 0.78

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.77-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Iain Arnell <iarnell@gmail.com> 0.77-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use perl_default_filter

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.71-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.71-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.71-5
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.71-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.71-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.71-1
- update to 0.71

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.69-1
- update to 0.69

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.68-4
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.68-3
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.68-2
- bump

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.68-1
- update to 0.68
- refactor perl BR's

* Thu Mar 29 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.67-1
- update to 0.67

* Sat Mar 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.66-1
- update to 0.66 (0.65 update never pushed due to various issues)
- misc spec cleanups
- add br on perl(ExtUtils::MakeMaker) to satisfy any perl/perl-devel split

* Sun Feb 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.65-1
- update to 0.65

* Sun Sep 17 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.64-2
- bump

* Wed Aug 16 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.64-1
- Specfile autogenerated by cpanspec 1.68.
