# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Sub-Exporter-Progressive
Version:	0.001013
Release:	27%{?dist}
Summary:	Only use Sub::Exporter if you need it
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Sub-Exporter-Progressive
Source0:	https://cpan.metacpan.org/modules/by-module/Sub/Sub-Exporter-Progressive-%{version}.tar.gz
BuildArch:	noarch
# =============== Module Build ======================
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# =============== Module Runtime ====================
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.58
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Exporter)
BuildRequires:	perl(warnings)
# =============== Test Suite ========================
BuildRequires:	perl(constant)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.88
# =============== Module Dependencies ===============
Requires:	perl(Carp)
Requires:	perl(Exporter) >= 5.58
Requires:	perl(Sub::Exporter)

%description
Sub::Exporter is an incredibly powerful module, but with that power comes
great responsibility, er- as well as some runtime penalties. This module is a
Sub::Exporter wrapper that will let your users just use Exporter if all they
are doing is picking exports, but use Sub::Exporter if your users try to use
Sub::Exporter's more advanced features, like renaming exports, if they try to
use them.

Note that this module will export @EXPORT and @EXPORT_OK package variables for
Exporter to work. Additionally, if your package uses advanced Sub::Exporter
features like currying, this module will only ever use Sub::Exporter, so you
might as well use it directly.

%prep
%setup -q -n Sub-Exporter-Progressive-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Sub/
%{_mandir}/man3/Sub::Exporter::Progressive.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 12 2023 Paul Howarth <paul@city-fan.org> - 0.001013-21
- Spec tidy-up
  - Use SPDX-format license tag
  - Use author-independent source URL
  - Drop support for building with Test::More < 0.88
  - Drop redundant buildroot cleaning in %%install section
  - Use %%license unconditionally

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-18
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-15
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-12
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.001013-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.001013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 22 2016 Paul Howarth <paul@city-fan.org> - 0.001013-1
- Update to 0.001013
  - Avoid possible warnings about special variables only being used once
- Update old Test::More patch

* Wed Aug 24 2016 Paul Howarth <paul@city-fan.org> - 0.001012-1
- Update to 0.001012
  - Many small performance improvements
- BR: perl-generators
- Simplify find command using -delete
- Update old Test::More patch
- Package new LICENSE file

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.001011-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.001011-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001011-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.001011-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.001011-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Paul Howarth <paul@city-fan.org> - 0.001011-1
- Update to 0.001011
  - Fix in global destruction
  - Fix SYNOPSIS
  - Fix duplicate word in DESCRIPTION (CPAN RT#86072)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.001010-2
- Perl 5.18 rebuild

* Wed Mar 27 2013 Paul Howarth <paul@city-fan.org> - 0.001010-1
- Update to 0.001010
  - Fix module name in Makefile.PL (CPAN RT#83932)
  - Work around Exporter.pm not installable on perl < 5.8.0
- Update old Test::More patch

* Wed Mar 13 2013 Paul Howarth <paul@city-fan.org> - 0.001009-1
- Update to 0.001009
  - Disallow version names in random parts of the import list for consistency
    with Sub::Exporter (CPAN RT#83491)
- Update old Test::More patch, and apply if we have Test::More < 0.88

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Paul Howarth <paul@city-fan.org> - 0.001008-1
- Update to 0.001008
  - Rewrite -tag to :tag for Exporter.pm
  - Fix prereqs
- Update old Test::More patch, and apply if we have Test::More < 0.96
- Bump perl(Exporter) version requirement to 5.58

* Mon Aug 27 2012 Paul Howarth <paul@city-fan.org> - 0.001006-1
- Update to 0.001006
  - Handle ':all' correctly
- Update old Test::More patch
- Drop redundant buildreq perl(Test::Pod)

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.001005-1
- Update to 0.001005
  - Add support for tags
  - Warn if defaults are not in exports
  - Add explicit dependency on Test::More 0.89
- This release by LEONT -> update source URL
- Update old Test::More patch

* Thu Aug  9 2012 Paul Howarth <paul@city-fan.org> - 0.001004-1
- Update to 0.001004 (fix skipping when Sub::Exporter isn't installed)
- This release by MSTROUT -> update source URL
- No LICENSE file in this release
- Update old Test::More patch

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001003-1
- Update to 0.001003 (remove warning if there are no defaults)

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001002-2
- Sanitize for Fedora submission

* Wed Aug  1 2012 Paul Howarth <paul@city-fan.org> - 0.001002-1
- Initial RPM build
