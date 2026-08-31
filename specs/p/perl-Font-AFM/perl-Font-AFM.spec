# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Font-AFM
Version:        1.20
Release:        51%{?dist}
Summary:        Perl interface to Adobe Font Metrics files

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Font-AFM
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/Font-AFM-%{version}.tar.gz


BuildArch:      noarch

BuildRequires:  %{__make}
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?fedora} >= 40
# REGRESSION: dnf5 is unable to BuildRequires: files
BuildRequires: urw-base35-nimbus-sans-fonts
%else
# This is what is actually BuildRequired
BuildRequires:  %{_fontbasedir}/urw-base35/NimbusSans-Bold.afm
%endif

%description
Interface to Adobe Font Metrics files

%prep
%setup -q -n Font-AFM-%{version}
# We don't have Helvetica, use NimbusSans-Bold.afm instead
sed -i -e 's,Helvetica,NimbusSans-Bold,g' t/afm.t
# Change the expected string width to match NimbusSans-Bold.
# 4558 is a sum of widths of characters from testing 'Gisle Aas' string
# in NimbusSans-Bold - see NimbusSans-Bold.afm for specific character
# length.
sed -i -e 's,4279,4558,g' t/afm.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}


%install
%{make_install}
chmod -R u+w $RPM_BUILD_ROOT/*


%check
%{__make} test METRICS=%{_fontbasedir}/urw-base35


%files
%doc Changes README
%{perl_vendorlib}/Font
%{_mandir}/man3/Font*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 20 2024 Xavier Bachelot <xavier@bachelot.org> - 1.20-49
- Fix typo in Fedora conditional breaking EPEL build
- Remove spurious tabs

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jan 28 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-47
- Add work-around to dnf5's regression to not support BuildRequires: on files.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-42
- Modernize spec.
- Convert license to SPDX.
- Update sources to sha512.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-40
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-37
- Perl 5.34 rebuild

* Fri Mar 19 2021 Zdenek Dohnal <zdohnal@redhat.com> - 1.20-36
- use NimbusSans-Bold font in test instead of phvr

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-33
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-30
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-27
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-24
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-22
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-20
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-18
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-17
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.20-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Petr Šabata <contyk@redhat.com> - 1.20-12
- BuildRequire perl(Carp)
- Drop command macros
- Reflect metrics copyright in the License tag

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.20-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.20-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.20-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.19-7
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.19-6
- rebuild for new perl

* Fri Aug 31 2007 Ralf Corsépius <rc040203@freenet.de> - 1.19-5
- BR: perl(ExtUtils::MakeMaker).
- Update license tag.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.19-4
- Mass rebuild.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 1.19-3
- Rebuild for perl-5.8.8.

* Sun Aug 21 2005 Ralf Corsepius <ralf@links2linux.de>	- 1.19-3
- Changelog cleanup.

* Sun Aug 21 2005 Ralf Corsepius <ralf@links2linux.de>	- 1.19-2
- Review feedback.

* Thu Aug 18 2005 Ralf Corsepius <ralf@links2linux.de>	- 1.19-1
- FE submission.
