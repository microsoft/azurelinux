# This package should be renamed into perl-Locale-gettext
%global tarname Locale-gettext

Name:           perl-gettext
Version:        1.07
Release:        17%{?dist}
Summary:        Interface to gettext family of functions

License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/gettext
Source0:        https://cpan.metacpan.org/authors/id/P/PV/PVANDRY/%{tarname}-%{version}.tar.gz#/perl-%{tarname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  %{__make}
BuildRequires:  %{__perl}

BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  gettext
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(POSIX)

# Optional
BuildRequires:  perl(Encode)
# Tests:
BuildRequires:  perl(Test)

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.


%package -n perl-%{tarname}
Summary:        %{summary}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-%{tarname}
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1
%{__make} %{?_smp_mflags}


%install
%{__make} pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*


%check
%{__make} test


%files -n perl-%{tarname}
%doc README
%{perl_vendorarch}/auto/Locale
%{perl_vendorarch}/Locale
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.07-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-14
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-12
- Drop obsolete "Obsolete/Provides".
- Add BR: gcc.
- Cleanup spec.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-2
- Modernize spec.

* Thu Nov 26 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-1
- Upstream update.
- Reflect upstream having changed tarball name to Locale-gettext.
- Rename binary package to perl-Locale-gettext.
- Remove BR: per(Data::Dumper).

* Thu Sep 24 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Update to 1.06.
- Remove Obsoletes: perl-Locale-gettext.
- Remove LD_MESSAGES hack.
- Modernize spec.
- Drop compatibility-with-POSIX-module.diff (upstreamed).
- Add BR: perl(Encode).

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-33
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-32
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.05-28
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.05-25
- Perl 5.16 rebuild
- Specify all dependencies

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-24
- Add %%{?perl_default_filter}.
- Modernize spec.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-22
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-21
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-19
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-18
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-17
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-16
- Adopt Debian's compatibility-with-POSIX-module.diff (RH BZ#447859).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-13
- rebuild for new perl

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.05-12
- Rebuild for gcc43.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 1.05-11
- Update license tag.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 1.05-10
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.05-9
- Mass rebuild.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 1.05-8
- Rebuild.

* Wed Nov 02 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-7
- Work-around to "make test" not supporting LC_MESSAGES=POSIX.

* Wed Nov 02 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-6
- Obsoletes: perl-Locale-gettext <= 1.05.
- Fix minor spec file typos.

* Tue Nov 01 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-5
- FE import.
- Add Obsoletes: perl-Locale-gettext.

* Tue Nov 01 2005 Ralf Corsepius <rc040203@freenet.de> - 1.05-4
- Rename package to perl-gettext.
- Remove "Require: perl".

* Sat Aug 20 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-3
- Add Provides: perl-gettext (RH bugzilla PR 165885).

* Tue Aug 09 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-2
- Add BuildRequires: gettext.

* Sun Aug 07 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-1
- FE submission.

* Thu Aug 04 2005 Ralf Corsepius <ralf@links2linux.de> - 1.05-0
- Initial rpm.
