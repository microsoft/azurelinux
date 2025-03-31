Name:		perl-ExtUtils-InstallPaths
Version:	0.014
Release:	1%{?dist}
Summary:	Build.PL install path logic made easy
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/ExtUtils-InstallPaths
Source0:	https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-InstallPaths-%{version}.tar.gz#/perl-ExtUtils-InstallPaths-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::Config) >= 0.009
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec::Functions) >= 0.83
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

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
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::InstallPaths.3*

%changelog
* Fri Dec 20 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.014-1
- Update to 0.014
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.012-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
