Name:           perl-Devel-CheckLib
Version:        1.16
Release:        1%{?dist}
Summary:        Check that a library is available

License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Devel-CheckLib
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz#/perl-Devel-CheckLib-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Text::ParseWords)
# Tests:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(lib)
BuildRequires:  perl(blib)
BuildRequires:  perl(Test::More) >= 0.88
# Optional tests
BuildRequires:  perl(Mock::Config)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.

%prep
%setup -q -n Devel-CheckLib-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc CHANGES README TODO
%{_bindir}/*
%{perl_vendorlib}/Devel*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.16-1
- Auto-upgrade to 1.16 - Azure Linux 3.0 - package upgrades

* Mon Jul 25 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.14-5
- Move from SPECS-EXTENDED to SPECS

* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com> - 1.14-4
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Denis Fateyev <denis@fateyev.com> - 1.14-1
- Update to 1.14

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-2
- Perl 5.28 rebuild

* Wed Jun 20 2018 Denis Fateyev <denis@fateyev.com> - 1.13-1
- Update to 1.13

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.26 rebuild

* Thu Jun 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-1
- Update to 1.11

* Tue Apr 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-1
- Update to 1.10

* Sat Mar 25 2017 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.09-1
- Update to 1.09 (bug #1435192).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Perl 5.24 rebuild

* Sat Apr  9 2016 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.07-1
- Update to 1.07.

* Sun Apr  3 2016 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.06-1
- Update to 1.06.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 19 2015 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.05-1
- Update to 1.05.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Sat Mar 21 2015 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.03-1
- Update to 1.03.

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.99-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.99-2
- Perl 5.18 rebuild

* Thu Apr  4 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99-1
- Update to 0.99.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 0.98-4
- Specify all dependencies
- Package TODO

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.98-2
- Perl 5.16 rebuild

* Sat Mar 17 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.98-1
- Update to 0.98.

* Mon Feb 27 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-1
- Update to 0.97.

* Fri Feb  3 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.96-1
- Update to 0.96.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.95-1
- Update to 0.95.

* Wed Oct 19 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.94-1
- First build.
