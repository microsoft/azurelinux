Name:           perl-Lingua-EN-Inflect
Version:        1.904
Release:        5%{?dist}
Summary:        Convert singular to plural, select "a" or "an"
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Lingua-EN-Inflect
Source0:        https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/Lingua-EN-Inflect-%{version}.tar.gz#/perl-Lingua-EN-Inflect-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Env)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Carp)

%description
%{summary}.

%prep
%setup -q -n Lingua-EN-Inflect-%{version}
chmod -x Changes README lib/Lingua/EN/Inflect.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Lingua/
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.904-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.904-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.904-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.904-2
- Perl 5.30 rebuild

* Wed May 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.904-1
- 1.904 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.903-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.903-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.903-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.903-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.903-1
- 1.903 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.902-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.902-2
- Perl 5.26 rebuild

* Thu Jun  1 2017 Tom Callaway <spot@fedoraproject.org> - 1.902-1
- update to 1.902

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.901-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 3 2017 Tom Callaway <spot@fedoraproject.org> - 1.901-1
- update to 1.901

* Fri Jul 29 2016 Tom Callaway <spot@fedoraproject.org> - 1.900-1
- update to 1.900

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.899-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.899-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.899-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Tom Callaway <spot@fedoraproject.org> - 1.899-1
- update to 1.899

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.895-6
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.895-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.895-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.895-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.895-2
- Perl 5.18 rebuild

* Tue Feb 26 2013 Petr Pisar <ppisar@redhat.com> - 1.895-1
- 1.895 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.892-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.892-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.892-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.892-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.892-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.892-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.892-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.892-1
- update to 1.892

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.89-12
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.89-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.89-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.89-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.89-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.89-7
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-6
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-5
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-4
- bump for fc6

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-3
- chmod -x files that don't need to be executable (hooray upstream)
- own Lingua directory correctly

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.89-1
- Initial package for Fedora Extras
