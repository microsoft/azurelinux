# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Want
Version:	0.29
Release:	33%{?dist}
Summary:	Perl module implementing a generalisation of wantarray
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Want
Source0:	https://cpan.metacpan.org/authors/id/R/RO/ROBIN/Want-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	%{__make}

BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(:VERSION) >= 5.6
BuildRequires:	perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:	perl(Carp)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Tests:
BuildRequires:	perl(blib)
BuildRequires:	perl(Config)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(threads)

%description
This module generalises the mechanism of the wantarray
function, allowing a function to determine in some detail
how its return value is going to be immediately used.

%prep
%setup -q -n Want-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="${RPM_OPT_FLAGS}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} "$RPM_BUILD_ROOT"/*

%check
%{__make} test

%files
%doc Changes README
%{perl_vendorarch}/Want*
%{perl_vendorarch}/auto/Want*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-32
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-29
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-25
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Fedora Release Engineering <corsepiu@fedoraproject.org> - 0.29-23
- Modernize spec.
- Update sources to use sha512.
- Convert licence to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-21
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-19
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-18
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-15
- Perl 5.32 rebuild

* Tue Mar 03 2020 Petr Pisar <ppisar@redhat.com> - 0.29-14
- Specify all dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-11
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-2
- Perl 5.24 rebuild

* Fri Feb 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.29-1
- Update to 0.29.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.26-4
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.22 rebuild

* Fri May 01 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.26-1
- Upstream update.

* Fri Dec 12 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.25-1
- Upstream update.

* Wed Dec 03 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.24-1
- Upstream update.
- Switch to using DESTDIR and pure_install.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.23-1
- Upstream update.
- Minor spec modernisations.

* Sun Dec 29 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.22-1
- Upstream update.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.21-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.21-3
- Perl 5.16 rebuild

* Mon Mar 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.21-2
- More *.spec typo fixes.

* Sun Mar 04 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.21-1
- Upstream update.
- Fix *.spec typo.

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.20-1
- Upstream update.
- Modernize spec.

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.18-11
- Add %%{?perl_default_filter}.
- Modernize spec.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.18-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.18-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-2
- rebuild for new perl

* Wed Feb 06 2008 Ralf Corsépius <rc040203@freenet.de> - 0.18-1
- Upstream update.

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 0.16-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.15-2
- Update license tag.

* Thu Jul 26 2007 Ralf Corsépius <rc040203@freenet.de> - 0.15-1
- Upstream update.

* Mon May 07 2007 Ralf Corsépius <rc040203@freenet.de> - 0.14-1
- Upstream update.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.12-2
- Reflect perl package split.

* Mon Sep 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.12-1
- Upstream update.

* Tue Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.10-1
- Upstream update.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.09-3
- Rebuild.

* Sat Aug 13 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-2
- Streamline with FE spec-template.

* Sat Jul 02 2005 Ralf Corsepius <ralf@links2linux.de> - 0.09-1
- Upstream update to 0.09.
