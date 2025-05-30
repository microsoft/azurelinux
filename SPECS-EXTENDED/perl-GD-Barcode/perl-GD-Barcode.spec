Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-GD-Barcode
Version:        1.15
Release:        34%{?dist}
Summary:        Create barcode image with GD
# see Barcode.pm
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/GD-Barcode
Source0:        https://cpan.metacpan.org/authors/id/K/KW/KWITKNR/GD-Barcode-%{version}.tar.gz#/perl-GD-Barcode-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) 
BuildRequires:  perl(GD)
# definitely not picked up automagically.
Requires:       perl(GD)

%description
GD::Barcode is a subclass of GD and allows you to create barcode images 
with GD. 

%prep
%setup -q -n GD-Barcode-%{version}
find sample/ -type f -exec sed -i 's/\r//' {} +

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README sample/ test.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15-34
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-31
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-28
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-25
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-23
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-20
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-19
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.15-16
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Petr Šabata <contyk@redhat.com> - 1.15-14
- Modernize the spec a bit and fix the dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.15-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.15-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.15-3
- rebuild for new perl

* Mon Jun 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.15-2
- bump

* Mon May 28 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- Specfile autogenerated by cpanspec 1.71.
