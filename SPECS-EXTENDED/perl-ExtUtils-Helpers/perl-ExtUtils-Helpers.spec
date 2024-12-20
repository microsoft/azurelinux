Name:		perl-ExtUtils-Helpers
Version:	0.028
Release:	1%{?dist}
Summary:	Various portability utilities for module builders
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/ExtUtils-Helpers
Source0:	https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-Helpers-%{version}.tar.gz#/perl-ExtUtils-Helpers-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module (File::Copy only needed for VMS support, not packaged)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(strict)
BuildRequires:	perl(Text::ParseWords) >= 3.24
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Cwd)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides various portable helper functions for module building
modules.

%prep
%setup -q -n ExtUtils-Helpers-%{version}

# Don't include VMS and Windows helpers, which may pull in unwelcome dependencies
rm -f lib/ExtUtils/Helpers/{VMS,Windows}.pm
perl -ni -e 'print unless /^lib\/ExtUtils\/Helpers\/(VMS|Windows)\.pm$/;' MANIFEST

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
%doc Changes README
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::Helpers.3*
%{_mandir}/man3/ExtUtils::Helpers::Unix.3*

%changelog
* Fri Dec 20 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.028-1
- Update to version 0.028
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.026-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 0.026-12
- Use an author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Paul Howarth <paul@city-fan.org> - 0.026-8
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.026-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 10 2016 Paul Howarth <paul@city-fan.org> - 0.026-1
- Update to 0.026
  - Fix Win32 dependency

* Fri Sep  2 2016 Paul Howarth <paul@city-fan.org> - 0.025-1
- Update to 0.025
  - Make split_like_shell always unixy
  - Remove Module::Load dependency
  - Remove done_testing; it requires Test::More 0.88
- Drop VMS and Windows versions to avoid unwelcome dependencies
- Drop now-redundant patch for building with Test::More < 0.88
- Use %%license where possible
- Simplify find command using -delete

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-10
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.022-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.022-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-6
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-5
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.022-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar  7 2014 Paul Howarth <paul@city-fan.org> - 0.022-1
- Update to 0.022
  - Cleaned up remains of former functions
  - Skip IO layers on <5.8 for 5.6 compatibility
  - Don't swallow pl2bat exceptions
- Drop patch for using Text::ParseWords < 3.24; even EL-5 has it

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.021-4
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.021-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.021-2
- Perl 5.18 rebuild

* Tue May  7 2013 Paul Howarth <paul@city-fan.org> - 0.021-1
- Update to 0.021
  - Always use the right environmental variable for home directory
  - Use configuration provided manpage extension
- Update patch for building with Test::More < 0.88

* Mon Apr 29 2013 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.020
  - Fix man3_pagename for top level domains
- Update patch for building with Test::More < 0.88

* Wed Apr 24 2013 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.019
  - Fix make_executable for '#!/usr/bin/perl'

* Tue Apr 16 2013 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Don't need Pod::Man
- Drop BR: perl(Pod::Man), no longer used

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Fix man3_pagename to properly split dirs
- Update patch for building with Test::More < 0.88

* Sat Apr 13 2013 Paul Howarth <paul@city-fan.org> - 0.016-1
- Update to 0.016
  - Made man3_pagename more flexible with paths
  - Reverted pl2bat to a more original state
  - Rewrote fixin code
  - Re-added detildefy
  - Add some fixes to batch file generation
- BR: perl(Carp) and perl(Module::Load), now required by the module
- Drop BR: perl(Test::Kwalitee), no longer used
- Update patch for using Test::ParseWords 3.22
- Drop now-redundant POD encoding patch

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.014-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.014-1
- Initial RPM version
