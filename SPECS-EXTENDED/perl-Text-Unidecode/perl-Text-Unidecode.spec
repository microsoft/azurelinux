Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Text-Unidecode
Version:        1.30
Release:        12%{?dist}
Summary:        US-ASCII transliterations of Unicode text
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Text-Unidecode
Source0:        https://cpan.metacpan.org/modules/by-module/Text/Text-Unidecode-%{version}.tar.gz#/perl-Text-Unidecode-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(integer)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Test)
BuildRequires:  perl(Text::Wrap)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description

Text::Unidecode provides a function, `unidecode(...)' that takes
Unicode data and tries to represent it in US-ASCII characters (i.e.,
the universally displayable characters between 0x00 and 0x7F). The
representation is almost always an attempt at *transliteration* -- i.e.,
conveying, in Roman letters, the pronunciation expressed by the text in
some other writing system.

%prep
%setup -q -n Text-Unidecode-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README TODO.txt ChangeLog
%{perl_vendorlib}/Text/
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.30-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 27 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.30-1
- Update to 1.30

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-1
- 1.27 bump

* Fri Aug 28 2015 Petr Šabata <contyk@redhat.com> - 1.24-1
- 1.24 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-2
- Perl 5.22 rebuild

* Wed Dec 10 2014 Petr Šabata <contyk@redhat.com> - 1.23-1
- 1.23 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-2
- Perl 5.20 rebuild

* Wed Aug 20 2014 Petr Šabata <contyk@redhat.com> - 1.22-1
- 1.22 bump

* Tue Jul 01 2014 Petr Šabata <contyk@redhat.com> - 1.01-1
- A rebase after 13 years; 1.01 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.04-20
- Perl 5.18 rebuild

* Fri Jul 12 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-18
- Update dependencies
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Remove build root cleaning, BuildRoot definition and %%defattr

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-17
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.04-15
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-13
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-12
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.04-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-5
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 29 2006 Patrice Dumas <pertusus at free.fr> - 0.04-4
- rebuild for FC6

* Mon Jun 26 2006 Patrice Dumas <pertusus at free.fr> - 0.04-3
- rebuild for perl-5.8.8

* Fri Feb 17 2006 Patrice Dumas <pertusus at free.fr> - 0.04-2
- rebuild for fc5

* Sun Jan 29 2006 Patrice Dumas <pertusus at free.fr> - 0.04-1
- fedora extras submission
