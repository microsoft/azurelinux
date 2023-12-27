Name:           perl-Clone
Version:        0.46
Release:        1%{?dist}
Summary:        Recursively copy perl data types
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/dist/Clone
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GARU/Clone-%{version}.tar.gz#/perl-Clone-%{version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(B)
BuildRequires:  perl(B::COW) >= 0.004
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)

# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides a clone() method that makes recursive
copies of nested hash, array, scalar and reference types,
including tied variables and objects.

clone() takes a scalar argument and an optional parameter that
can be used to limit the depth of the copy. To duplicate lists,
arrays or hashes, pass them in by reference.

%prep
%setup -q -n Clone-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README.md
%{perl_vendorarch}/auto/Clone/
%{perl_vendorarch}/Clone.pm
%{_mandir}/man3/Clone.3*

%changelog
* Wed Dec 27 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 0.46-1
- Azure Linux 3.0 - upgrade to 0.46

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.43-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jul 30 2019 Paul Howarth <paul@city-fan.org> - 0.43-1
- Update to 0.43
  - Fix an issue when cloning a NULL mg_ptr pointer

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Paul Howarth <paul@city-fan.org> - 0.42-1
- Update to 0.42
  - Make handling of mg_ptr safer
  - Change license wording on some test files to make the entire dist
    released under the same terms as Perl itself (GH#20)

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Paul Howarth <paul@city-fan.org> - 0.41-1
- Update to 0.41
  - Check the CowREFCNT of a COWed PV; this should fix some issues people have
    been having with 0.40 on DBD drives and DBIx::Class
  - Make buildtools files not executable

* Wed Oct 24 2018 Paul Howarth <paul@city-fan.org> - 0.40-1
- Update to 0.40
  - Reuse COWed PV when cloning (fixes CPAN RT#97535)
  - Extra protection against potential infinite loop
  - Improved tests

* Thu Oct  4 2018 Tom Callaway <spot@fedoraproject.org> - 0.39-9
- Remove non-free test files (bz1600131)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-7
- Perl 5.28 rebuild

* Wed Mar  7 2018 Paul Howarth <paul@city-fan.org> - 0.39-6
- BR: gcc for build and perl(Storable) for optional test
- Simplify find command using -empty
- Drop legacy Group: tag
- Ship README file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-2
- Perl 5.26 rebuild

* Mon Apr 10 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.38-2
- Perl 5.22 rebuild

* Fri Mar 20 2015 Tom Callaway <spot@fedoraproject.org> - 0.38-1
- update to 0.38

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 0.36-1
- 0.36 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.34-4
- Perl 5.18 rebuild

* Mon Jun 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.34-3
- Update dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Petr Šabata <contyk@redhat.com> - 0.34-1
- 0.34 bump for DBI 1.623
- Modernize the spec
- Update filters and Source URL

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.31-10
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.31-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.31-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.31-2
- filter private Perl solibs from provides
- remove some executable bits -- keep rpmlint happy

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31-1
- update to 0.31

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.28-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.28-3
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-1
- bump to 0.28

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.27-2
- license fix

* Fri Jul 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.27-1
- bump to 0.27

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-1
- bump to 0.22

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.20-2
- bump for fc6

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.20-1
- bump to 0.20
- new BR: perl-Taint-Runtime

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.18-3
- bump for FC-5

* Fri Jan  6 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.18-2
- don't pass optflags twice
- remove .bs files

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.18-1
- Initial package for Fedora Extras
