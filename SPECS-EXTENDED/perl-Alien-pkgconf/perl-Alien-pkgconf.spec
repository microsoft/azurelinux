Name:           perl-Alien-pkgconf
Version:        0.17
Release:        2%{?dist}
Summary:        Discover pkgconf and libpkgconf
# Other files:              GPL+ or Artistic
## Not used
# pkgconf-1.3.9/aclocal.m4: GPLv3+ with exceptions
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Alien-pkgconf
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-pkgconf-%{version}.tar.gz#/perl-Alien-pkgconf-%{version}.tar.gz
# This is a full-arch package because it stores data about arch-specific
# libpkgconf.so library and it stores them into arch-specific directory.
# But it does not install any ELF, therefore disable debuginfo generation.
%global debug_package %{nil}
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# FFI::CheckLib is optional but provides additional data to bake into a binary
# package
BuildRequires:  perl(FFI::CheckLib)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(JSON::PP) >= 2.27400
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconf
BuildRequires:  pkgconfig(libpkgconf) >= 1.5.2
# script/system.pl is executed at build time
# Run-time:
BuildRequires:  perl(File::ShareDir) >= 1.102
# Tests:
# An XS code is built by Test::Alien::xs_ok() in t/xs.t
BuildRequires:  perl-devel
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test2::Bundle::Extended)
BuildRequires:  perl(Test2::Bundle::More)
BuildRequires:  perl(Test2::V0) >= 0.000065
# This RPM package ensures libpkgconf.so is installed on the system
Requires:       libpkgconf-devel(%{__isa}) = %(type -p pkgconf >/dev/null && pkgconf --exists libpkgconf && pkgconf --modversion libpkgconf || echo 0)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::ShareDir) >= 1.102
Requires:       perl(JSON::PP) >= 2.27400

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((File::ShareDir|JSON::PP)\\)$

%description
This Perl module provides you with the information that you need to invoke
pkgconf or link against libpkgconf. It isn't intended to be used directly,
but rather to provide the necessary package by a CPAN module that needs
libpkgconf, such as PkgConfig::LibPkgConf.

%prep
%setup -q -n Alien-pkgconf-%{version}

%build
unset ALIEN_FORCE ALIEN_INSTALL_TYPE
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Alien
%{_mandir}/man3/*

%changelog
* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 0.17-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable tests to avoid Alien circular dependency.

* Tue May 19 2020 Petr Pisar <ppisar@redhat.com> - 0.17-1
- 0.17 bump

* Mon Feb 24 2020 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Petr Pisar <ppisar@redhat.com> - 0.15-8
- Rebuild against pkgconf 1.6.3

* Fri Jul 12 2019 Petr Pisar <ppisar@redhat.com> - 0.15-7
- Rebuild against pkgconf 1.6.2

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-6
- Perl 5.30 rebuild

* Wed Mar 27 2019 Petr Pisar <ppisar@redhat.com> - 0.15-5
- Rebuild against pkgconf 1.6.1

* Mon Feb 11 2019 Petr Pisar <ppisar@redhat.com> - 0.15-4
- Rebuild against pkgconf 1.6.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Petr Pisar <ppisar@redhat.com> - 0.15-2
- Rebuild against pkgconf 1.5.4

* Tue Sep 04 2018 Petr Pisar <ppisar@redhat.com> - 0.15-1
- 0.15 bump

* Mon Jul 23 2018 Petr Pisar <ppisar@redhat.com> - 0.14-1
- 0.14 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-2
- Perl 5.28 rebuild

* Fri Jun 29 2018 Petr Pisar <ppisar@redhat.com> - 0.12-1
- 0.12 bump

* Fri Jun 29 2018 Petr Pisar <ppisar@redhat.com> - 0.11-8
- Rebuild against pkgconf 1.5.1

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Perl 5.28 rebuild

* Sat Mar 31 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-6
- Actually rebuild against pkgconf 1.4.2

* Sat Mar 31 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-5
- Rebuild for pkgconf 1.4.2

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Petr Pisar <ppisar@redhat.com> - 0.11-3
- Rebuild against pkgconf-1.4.1

* Fri Jan 05 2018 Neal Gompa <ngompa13@gmail.com> - 0.11-2
- Rebuild for pkgconf 1.4.0

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 0.11-1
- 0.11 bump

* Tue Dec 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-15
- Rebuild for pkgconf 1.3.90

* Mon Dec 11 2017 Petr Pisar <ppisar@redhat.com> - 0.10-14
- Rebuild against pkgconf-1.3.12

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-13
- Rebuild against pkgconf-1.3.10

* Mon Oct 02 2017 Petr Pisar <ppisar@redhat.com> - 0.10-12.1
- Really rebuild against pkgconf-1.3.9

* Fri Sep 22 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10-12
- Rebuild against pkgconf-1.3.9

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Petr Pisar <ppisar@redhat.com> - 0.10-9
- Rebuild against pkgconf-1.3.8

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-8
- Perl 5.26 rebuild

* Tue May 30 2017 Petr Pisar <ppisar@redhat.com> - 0.10-7
- Rebuild against pkgconf-1.3.7

* Fri May 12 2017 Petr Pisar <ppisar@redhat.com> - 0.10-6
- Rebuild against libpkgconf-1.3.6

* Wed Apr 05 2017 Petr Pisar <ppisar@redhat.com> - 0.10-5
- Rebuild against libpkgconf-1.3.5

* Mon Apr 03 2017 Petr Pisar <ppisar@redhat.com> - 0.10-4
- Rebuild against libpkgconf-1.3.4

* Tue Mar 28 2017 Petr Pisar <ppisar@redhat.com> - 0.10-3
- Rebuild against libpkgconf-1.3.3

* Mon Mar 27 2017 Petr Pisar <ppisar@redhat.com> - 0.10-2
- Rebuild against libpkgconf-1.3.2

* Thu Mar 09 2017 Petr Pisar <ppisar@redhat.com> 0.10-1
- Specfile autogenerated by cpanspec 1.78.
