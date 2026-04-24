# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-ExtUtils-InstallPaths
Version:	0.015
Release: 2%{?dist}
Summary:	Build.PL install path logic made easy
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/ExtUtils-InstallPaths
Source0:	https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-InstallPaths-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::Config) >= 0.009
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(File::Spec::Functions) >= 0.83
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Dependencies
# (none)

%description
This module tries to make install path resolution as easy as possible.

When you want to install a module, it needs to figure out where to install
things. The nutshell version of how this works is that default installation
locations are determined from ExtUtils::Config, and they may be individually
overridden by using the install_path attribute. An install_base attribute lets
you specify an alternative installation root like /home/foo and prefix does
something similar in a rather different (and more complicated) way. destdir
lets you specify a temporary installation directory like /tmp/install in case
you want to create bundled-up installable packages.

%prep
%setup -q -n ExtUtils-InstallPaths-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::InstallPaths.3*

%changelog
* Sat Sep 27 2025 Paul Howarth <paul@city-fan.org> - 0.015-1
- Update to 0.015
  - Restore installing non-standard types

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Drop 5.006 support
  - Compensate for perls without installsitescript
- Use %%{make_build} and %%{make_install}

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 26 2024 Paul Howarth <paul@city-fan.org> - 0.013-1
- Update to 0.013
  - Try to install any installable paths

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-12
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 0.012-7
- Use an author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.012-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.012-2
- Perl 5.28 rebuild

* Fri May 11 2018 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012
  - Allow an argument to install_map with source dirs
  - Make tests prove and 5.6 friendly
- Release tests moved to xt/, so don't bother with them
- Simplify find command using -delete
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-10
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-9
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.011-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.22 rebuild

* Mon Feb 16 2015 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - Make EU::IP compatible with perl 5.6
  - Declare dependency on File::Spec 0.83 for case_sensitive
- Use %%license where possible
- Don't attempt to run the release tests on old EL versions prior to EL-7 as
  they require Test::Pod ≥ 1.41

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Deprecated usage of legacy configuration variables
  - Generate default paths more dynamically

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.009-6
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.009-4
- Perl 5.18 rebuild

* Tue Apr 16 2013 Paul Howarth <paul@city-fan.org> - 0.009-3
- Drop non-dual-lived buildreqs (#947454)

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.009-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.009-1
- Initial RPM version
