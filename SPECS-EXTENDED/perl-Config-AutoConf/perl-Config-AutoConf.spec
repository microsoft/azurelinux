Name:           perl-Config-AutoConf
Version:        0.318
Release:        3%{?dist}
Summary:        A module to implement some of AutoConf macros in pure Perl
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Config-AutoConf
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Config-AutoConf-%{version}.tar.gz#/perl-Config-AutoConf-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  gcc
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Slurper)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Text::ParseWords)
# Tests only
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::CBuilder)
# Unused BuildRequires:  perl(IO::String)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(/usr/bin/perl -V:version)"; echo $version))

%description
This module simulates some of the tasks autoconf macros do.  To detect
a command, a library and similar.

%prep
%setup -q -n Config-AutoConf-%{version}

%build
/usr/bin/perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
%{make_build} test

%files
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.318-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.318-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 05 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.318-1
- Update to 0.318
- Add perl(File::Slurper) as a dependency
- Use /usr/bin/perl instead of perl
- Use %%{make_install} instead of make pure_install
- Use %%{make_build} instead of make

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.317-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.317-2
- Perl 5.28 rebuild

* Sun Jun 10 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.317-1
- Update to 0.317

* Sun Apr 22 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.316-1
- Update to 0.316

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.315-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.315-1
- Update to 0.315

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.314-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.314-2
- Perl 5.26 rebuild

* Sun Apr 02 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.314-1
- Update to 0.314

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.313-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 31 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.313-1
- Update to 0.313

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.311-6
- Perl 5.24 rebuild

* Sun Mar 20 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.311-5
- Replace glibc-headers as a glibc-headers with gcc (#1230486)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.311-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.311-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.311-2
- Perl 5.22 rebuild

* Wed Jun 10 2015 Petr Šabata <contyk@redhat.com> - 0.311-1
- 0.311 bump

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.309-2
- Perl 5.22 rebuild

* Wed Feb 18 2015 Petr Šabata <contyk@redhat.com> - 0.309-1
- 0.309 bump

* Thu Nov 06 2014 Petr Šabata <contyk@redhat.com> 0.305-1
- Initial packaging
