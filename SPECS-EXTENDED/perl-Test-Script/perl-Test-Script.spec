Name:           perl-Test-Script
Version:        1.29
Release:        12%{?dist}
Summary:        Cross-platform basic tests for scripts
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Script
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Test-Script-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:  perl-generators
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Probe::Perl) >= 0.01
BuildRequires:  perl(Test2::API)
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
The intent of this module is to provide a series of basic tests for scripts
in the bin directory of your Perl distribution.

%prep
%setup -q -n Test-Script-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-7
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-2
- Perl 5.34 rebuild

* Mon May 17 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-1
- Update to 1.29.
- Modernize spec.

* Sat Mar 13 2021 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.27-1
- Update to 1.27.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.26-1
- Update to 1.26.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Update to 1.25.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-4
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-1
- Update to 1.23.

* Mon Jul 17 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-1
- Update to 1.20.

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-2
- Perl 5.26 rebuild

* Thu Apr 13 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18-1
- Update to 1.18.

* Wed Mar 08 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.16-1
- Update to 1.16.
- Activate t2/ testsuite.

* Thu Feb 23 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.15-1
- Update to 1.15.
- Modernize spec.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.14-1
- Update to 1.14.
- Eliminate perl_bootstrap.

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-2
- Perl 5.24 rebuild

* Wed May 04 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-1
- Update to 1.12.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.10-5
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-2
- Perl 5.22 rebuild

* Mon May 18 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.10-1
- Upstream update.
- BR: Test::More >= 0.96.

* Mon May 11 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.09-1
- Upstream update.
- Reflect upstream Source0: having changed.
- Reflect upstream BR-changes.
- Modernize spec.

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-18
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-17
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-15
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.07-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-11
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.07-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.07-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-6
- Perl mass rebuild
- perl_bootstrap macro

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 25 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-3
- Reactivate pmv tests.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-2
- Mass rebuild with perl-5.12.0

* Tue Dec 15 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-1
- Upstream update.
- Reflect Source0-URL having changed.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.06-2
- rebuild against perl 5.10.1

* Mon Sep 28 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.
- BR: perl(Probe::Perl)
- Activate AUTOMATED_TESTING=1 RELEASE_TESTING=1.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.03-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-4
- Rebuild for perl 5.10 (again)

* Sat Jan 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-3
- rebuild for new perl

* Tue Sep 18 2007 Ralf Corsépius <rc040203@freenet.de> - 1.02-2
- Reflect license tag changes.
- BR: perl(Test::More).
- Remove BR: perl.
- Add chmod -x Changes lib/Test/*pm

* Tue Aug 07 2007 Ralf Corsépius <rc040203@freenet.de> - 1.02-1
- Specfile autogenerated by cpanspec 1.73.
