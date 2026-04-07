# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Use File::Slurper for reading file content
%bcond_without perl_Config_AutoConf_enables_File_Slurper
# Use Scalar::Util for detecting numbers
%bcond_without perl_Config_AutoConf_enables_Scalar_Util

Name:           perl-Config-AutoConf
Version:        0.320
Release:        13%{?dist}
Summary:        A module to implement some of AutoConf macros in pure Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Config-AutoConf
Source0:        https://cpan.metacpan.org/authors/id/A/AM/AMBS/Config-AutoConf-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  gcc
BuildRequires:  make
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
%if %{with perl_Config_AutoConf_enables_File_Slurper}
BuildRequires:  perl(File::Slurper)
%endif
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
%if %{with perl_Config_AutoConf_enables_Scalar_Util}
BuildRequires:  perl(Scalar::Util) >= 1.18
%endif
BuildRequires:  perl(Text::ParseWords)
# Tests only
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::CBuilder)
# Unused BuildRequires:  perl(IO::String)
BuildRequires:  perl(Test::More)
%if %{with perl_Config_AutoConf_enables_File_Slurper}
Suggests:       perl(File::Slurper)
%endif
%if %{with perl_Config_AutoConf_enables_Scalar_Util}
Suggests:       perl(Scalar::Util) >= 1.18
%endif

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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.320-7
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.320-4
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.320-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 27 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.320-1
- Update to 0.320

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.319-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.319-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Petr Pisar <ppisar@redhat.com> - 0.319-2
- Suggest File::Slurper for reading file content
- Suggest Scalar::Util for detecting numbers

* Sun Oct 04 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.319-1
- Update to 0.319

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.318-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.318-3
- Perl 5.32 rebuild

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
