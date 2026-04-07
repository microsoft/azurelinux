# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-DateTime-Calendar-Julian
Version:	0.107
Release:	11%{?dist}
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:	Julian Calendar support for DateTime.pm
Url:		https://metacpan.org/release/DateTime-Calendar-Julian
Source:		https://cpan.metacpan.org/authors/id/W/WY/WYANT/DateTime-Calendar-Julian-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl-generators, perl-interpreter, make
BuildRequires:	perl(DateTime) >= 1.48
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)

%description
DateTime object in the Julian calendar.

%prep
%setup -q -n DateTime-Calendar-Julian-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/DateTime/
%{_mandir}/man3/DateTime::Calendar::Julian.3pm*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 05 2024 Miroslav Suchý <msuchy@redhat.com> - 0.107-9
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.107-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.107-2
- Perl 5.36 rebuild

* Tue Feb  1 2022 Tom Callaway <spot@fedoraproject.org> - 0.107-1
- update to 0.107

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 29 2021 Tom Callaway <spot@fedoraproject.org> - 0.106-1
- update to 0.106

* Sun Sep  5 2021 Tom Callaway <spot@fedoraproject.org> - 0.105-1
- update to 0.105

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.104-2
- Perl 5.34 rebuild

* Mon May  3 2021 Tom Callaway <spot@fedoraproject.org> - 0.104-1
- update to 0.104

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.103-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Tom Callaway <spot@fedoraproject.org> - 0.103-1
- update to 0.103

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.102-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 20 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.102-1
- Update to 0.102; Update URL

* Thu Aug 15 2019 Tom Callaway <spot@fedoraproject.org> - 0.101-1
- update to 0.101

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.100-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.100-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  2 2019 Tom Callaway <spot@fedoraproject.org> - 0.100-1
- update to 0.100

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-9
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-6
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 11 2016 Tom Callaway <spot@fedoraproject.org> - 0.04-4
- add pedantic br

* Mon Oct 10 2016 Tom Callaway <spot@fedoraproject.org> - 0.04-3
- add BR: perl-generators (deps are overrated)

* Mon Oct 10 2016 Tom Callaway <spot@fedoraproject.org> - 0.04-2
- do not nuke buildroot at the beginning of install. This is not 2005.

* Mon Oct 10 2016 Tom Callaway <spot@fedoraproject.org> - 0.04-1
- initial package
