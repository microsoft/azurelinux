Name:           perl-IPC-Run3
Version:        0.048
Release:        19%{?dist}
Summary:        Run a subprocess in batch mode
License:        GPL+ or Artistic or BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/IPC-Run3
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/IPC-Run3-%{version}.tar.gz#/perl-IPC-Run3-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.31
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)

# For improved tests
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# RHBZ #1062267 / https://rt.cpan.org/Public/Bug/Display.html?id=52317
# Patch from
# https://github.com/rschupp/IPC-Run3/commit/8ebe48760cfdc78fbf4fc46413dde9470121b99e
Patch0:         0001-test-and-fix-for-RT-52317-Calling-run3-garbles-STDIN.patch

%description
This module allows you to run a subprocess and redirect stdin, stdout,
and/or stderr to files and perl data structures. It aims to satisfy 99% of
the need for using system, qx, and open3 with a simple, extremely Perlish
API and none of the bloat and rarely used features of IPC::Run.

%prep
%setup -q -n IPC-Run3-%{version}
%patch0 -p1

# Perms in tarballs are broken 
find -type f -exec chmod -x {} \;

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test RELEASE_TESTING=1

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.048-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-16
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-13
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.048-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.048-6
- Add %%license.
- Modernize spec.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.048-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.048-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.048-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.048-1
- Upstream update.
- Add RELEASE_TESTING=1 to work around upstream trying to discourage
  us from running pod-tests.

* Tue Feb 11 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.046-4
- Add 0001-test-and-fix-for-RT-52317-Calling-run3-garbles-STDIN.patch (RHBZ#1062267).
- Spec-file cosmetics.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.046-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.046-2
- Perl 5.18 rebuild

* Wed Jul 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.046-1
- Upstream update.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.045-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Petr Šabata <contyk@redhat.com> - 0.045-4
- Add missing BRs
- Drop command macros
- Remove redundant parens from the Licence tag

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.045-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.045-2
- Perl 5.16 rebuild

* Thu Jan 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.045-1
- Upstream update.
- Modernize spec file.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.044-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.044-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.044-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Sep 13 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.044-1
- Upstream update.
- BR: perl(Test::More), perl(Time::HiRes).

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.043-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.043-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.043-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Ralf Corsépius <corsepiu@fedoraproject.org> 0.043-1
- Upstream update.
- Reflect upstream URL having changed.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.042-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ralf Corsépius <corsepiu@fedoraproject.org> 0.042-3
- Change %%summary.

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.042-2
- fix license tag (technically, it was correct before, but this keeps rpmlint from
  flagging this package as a false positive)

* Mon Aug 25 2008 Ralf Corsépius <corsepiu@fedoraproject.org> 0.042-1
- Upstream update.

* Fri Aug 08 2008 Ralf Corsépius <rc040203@freenet.de> 0.041-1
- Upstream update.

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.040-5
- reorder license tag so it doesn't flag as a false positive

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.040-4
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.040-3
- Rebuild for perl 5.10 (again), disable tests for first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.040-2
- rebuild normally, second pass

* Sat Jan 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.040-1.1
- rebuild for new perl, disable tests and TPC for first pass

* Fri Dec 28 2007 Ralf Corsépius <rc040203@freenet.de> 0.040-1
- Upstream update.
- chmod -x files from source tarball.

* Tue Nov 27 2007 Ralf Corsépius <rc040203@freenet.de> 0.039-2
- Bump release to please koji suckage.

* Tue Nov 27 2007 Ralf Corsépius <rc040203@freenet.de> 0.039-1
- Upstream update.

* Fri Sep 07 2007 Ralf Corsépius <rc040203@freenet.de> 0.037-2
- Initial import.
- Update license tag.

* Tue Aug 07 2007 Ralf Corsépius <rc040203@freenet.de> 0.037-1
- Initial submission.
