# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Log-Dispatch-FileRotate
Version:        1.38
Release: 13%{?dist}
Summary:        Log to files that archive/rotate themselves
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Log-Dispatch-FileRotate
Source0:        https://cpan.metacpan.org/modules/by-module/Log/Log-Dispatch-FileRotate-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Log::Dispatch::File)
BuildRequires:  perl(Log::Dispatch::Output)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Encode)
BuildRequires:  perl(Log::Dispatch) >= 2.60
BuildRequires:  perl(Log::Dispatch::Screen)
BuildRequires:  perl(Path::Tiny) >= 0.018
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(utf8)
# Dependencies
Requires:       perl(Log::Dispatch) >= 2.60
Requires:       perl(version)

%description
This module provides a simple object for logging to files under the
Log::Dispatch::* system, and automatically rotating them according to
different constraints. This is basically a Log::Dispatch::File wrapper
with additions.

%prep
%setup -q -n Log-Dispatch-FileRotate-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} -c $RPM_BUILD_ROOT

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Log/Dispatch/
%{_mandir}/man3/Log::Dispatch::FileRotate.3*
%{_mandir}/man3/Log::Dispatch::FileRotate::Flock.3*
%{_mandir}/man3/Log::Dispatch::FileRotate::Mutex.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-9
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-6
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.36-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug  1 2018 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
- Drop legacy Group: tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.35-2
- Perl 5.28 rebuild

* Thu Mar  8 2018 Paul Howarth <paul@city-fan.org> - 1.35-1
- update to 1.35
- classify buildreqs by usage
- make %%files list more explicit
- don't need to remove empty directories from the buildroot

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 10 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-1
- 1.34 bump

* Mon Aug  7 2017 Tom Callaway <spot@fedoraproject.org> - 1.30-1
- update to 1.30

* Fri Jul 28 2017 Tom Callaway <spot@fedoraproject.org> - 1.29-1
- update to 1.29

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-2
- Perl 5.26 rebuild

* Tue May 23 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-1
- 1.26 bump

* Thu Apr 27 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-1
- 1.25 bump

* Fri Feb 24 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-1
- 1.24 bump

* Tue Feb 14 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-1
- 1.23 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Tom Callaway <spot@fedoraproject.org> - 1.22-1
- update to 1.22

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-21
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-18
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-17
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.19-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 1.19-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.19-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.19-7
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.19-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.19-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-1
- Upstream update.

* Fri Jun 27 2008 Ralf Corsépius <rc040203@freenet.de> - 1.18-1
- Upstream update.
- Add --with-tests.

* Tue Jun 03 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-3
- Use %%%%check in comments to work-around rpm bogusly parsing 
  %%check in comments (BZ 449419).

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Wed Apr 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.
- The author corrected the licensing terms (License: GPL+ or Artistic).

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.
- License: Artistic.

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-2
- The license is: GPL+ or Artistic.
  License information: http://rt.cpan.org/Public/Bug/Display.html?id=14563.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- First build.
