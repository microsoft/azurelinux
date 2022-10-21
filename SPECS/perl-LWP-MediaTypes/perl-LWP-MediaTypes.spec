# Use system-wide mailcap database
%bcond_without perl_LWP_MediaTypes_enables_mailcap

Name:           perl-LWP-MediaTypes
Version:        6.04
Release:        6%{?dist}
Summary:        Guess media type for a file or a URL
# lib/LWP/media.types:      Public Domain
# lib/LWP/MediaTypes.pm:    GPL+ or Artistic
License:        (GPL+ or Artistic) and Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/LWP-MediaTypes
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-%{version}.tar.gz#/perl-LWP-MediaTypes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Scalar::Util)
# Tests only:
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
# Optional tests:
# CPAN::Meta not helpful
# CPAN::Meta::Prereqs not helpful
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Basename)
%if %{with perl_LWP_MediaTypes_enables_mailcap}
Requires:       mailcap
%endif
Conflicts:      perl-libwww-perl < 6

%description
This module provides functions for handling media (also known as MIME)
types and encodings. The mapping from file extensions to media types is
defined by the media.types file. If the ~/.media.types file exists it is
used instead. For backwards compatibility we will also look for
~/.mime.types.

%prep
%setup -q -n LWP-MediaTypes-%{version}
%if %{with perl_LWP_MediaTypes_enables_mailcap}
# Use system-wide mailcap database
sed -i -e '/my @priv_files = ();/ s|()|("%{_sysconfdir}/mime.types")|' \
    lib/LWP/MediaTypes.pm
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 26 2022 Henry Li <lihl@microsoft.com> - 6.04-6
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.04-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.04-2
- Perl 5.30 rebuild

* Wed Mar 20 2019 Petr Pisar <ppisar@redhat.com> - 6.04-1
- 6.04 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.02-15
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.02-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.02-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.02-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.02-7
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.02-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 6.02-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Petr Šabata <contyk@redhat.com> - 6.02-1
- 6.02 bump
- Drop command macros
- Modernize the spec
- Correct the Lincense tag

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 6.01-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.01-3
- Perl mass rebuild

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> - 6.01-2
- Use MIME type database from mailcap

* Thu Mar 17 2011 Petr Pisar <ppisar@redhat.com> 6.01-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
- Conflicts with perl-libwww-perl 5* and older
