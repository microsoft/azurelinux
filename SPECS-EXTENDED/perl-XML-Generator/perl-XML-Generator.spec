Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:            XML-Generator Perl module
Name:               perl-XML-Generator
Version:            1.04
Release:            25%{?dist}
License:            GPL+ or Artistic
URL:                https://metacpan.org/release/XML-Generator
BuildArch:          noarch
Source0:            https://cpan.metacpan.org/authors/id/B/BH/BHOLZMAN/XML-Generator-%{version}.tar.gz#/perl-XML-Generator-%{version}.tar.gz
BuildRequires:      coreutils
BuildRequires:      findutils
BuildRequires:      make
BuildRequires:      perl-interpreter
BuildRequires:      perl-generators
BuildRequires:      perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:      perl(base)
BuildRequires:      perl(Carp)
BuildRequires:      perl(constant)
BuildRequires:      perl(overload)
BuildRequires:      perl(strict)
BuildRequires:      perl(vars)
BuildRequires:      perl(warnings)
BuildRequires:      perl(XML::DOM)
# Tests:
BuildRequires:      perl(Test)
# Optional tests:
BuildRequires:      perl(Tie::IxHash)
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:           perl(warnings)

%description
perl module for generating XML documents

%prep
%setup -q -n XML-Generator-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-22
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-19
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-16
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-14
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Petr Pisar <ppisar@redhat.com> - 1.04-12
- Specify all dependencies

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-10
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 1.04-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.04-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> - 1.04-1
- 1.04 bump
- Removing now obsolete defattr

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.03-2
- Perl mass rebuild

* Tue Apr 26 2011 Petr Sabata <psabata@redhat.com> - 1.03-1
- 1.03 bump
- Buildroot removed, general cleanup
- Added overload and base to BuildRequires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.01-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Dennis Gilmore <dennis@ausil.us> - 1.01-3
- BR perl(XML::DOM) 
- remove OPTIMIZE option from %%build

* Wed Jan 28 2009 Dennis Gilmore <dennis@ausil.us> - 1.01-2
- add back XML::Generator::DOM

* Wed Jan 28 2009 Dennis Gilmore <dennis@ausil.us> - 1.01-1
- spec file cleanups
- update to 1.01

* Fri Jun 20 2008 Jan Pazdziora 0.99-13
- Remove XML::Generator::DOM.

* Tue Mar 25 2008 Jan Pazdziora 0.99-12
- Move build process to dist-cvs.

* Wed Jun 23 2004 <dparker@redhat.com> - 0.99-8
- Specfile autogenerated.

