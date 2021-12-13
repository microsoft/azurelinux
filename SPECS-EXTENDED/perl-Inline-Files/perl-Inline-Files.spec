Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           perl-Inline-Files
Version:        0.71
Release:        5%{?dist}
Summary:        Allows for multiple inline files in a single Perl file
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Inline-Files
Source0:        https://cpan.metacpan.org/authors/id/A/AM/AMBS/Inline-Files-%{version}.tar.gz#/perl-Inline-Files-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
# Data::Dumper not used at test time
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests only
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Data::Dumper)

%description
Inline::Files generalizes the notion of the `__DATA__' marker and the
associated `<DATA>' file handle, to an arbitrary number of markers and
associated file handles.

%prep
%setup -q -n Inline-Files-%{version}
chmod -R a-x demo/* README Changes lib/Inline/Files.pm \
    lib/Inline/Files/Virtual.pm

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README demo/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.71-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.71-2
- Perl 5.30 rebuild

* Wed Apr 03 2019 Petr Pisar <ppisar@redhat.com> - 0.71-1
- 0.71 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.69-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.69-2
- Perl 5.22 rebuild

* Mon May 25 2015 Petr Šabata <contyk@redhat.com> - 0.69-1
- 0.69 bump
- Correct source URL

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.68-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.68-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Petr Šabata <contyk@redhat.com> - 0.68-5
- Modernize the spec a bit
- Update the dep list
- Drop command macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.68-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Petr Sabata <contyk@redhat.com> - 0.68-1
- 0.68 bump

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.67-2
- Perl mass rebuild

* Mon Jul 11 2011 Petr Sabata <contyk@redhat.com> - 0.67-1
- 0.67 bump

* Mon Jun 20 2011 Petr Pisar <ppisar@redhat.com> - 0.65-1
- 0.65 bump
- Remove defattr
- Correct spelling in description

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.64-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Petr Pisar <ppisar@redhat.com> - 0.64-1
- 0.64 bump
- Remove BuildRoot stuff and empty lines
- Consolidate dependencies

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-1
- update to 0.63

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.62-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.62-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.62-3
- rebuild for new perl

* Wed Nov 14 2007 Robin Norwood <rnorwood@redhat.com> - 0.62-2
- Fix permissions per package review.

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.62-1
- Initial build
