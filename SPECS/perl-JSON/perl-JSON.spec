%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(JSON::(Backend::PP|backportPP::Boolean|Boolean|PP|PP::IncrParser)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(JSON::(backportPP|backportPP::Boolean)\\)
Summary:        Parse and convert to JSON (JavaScript Object Notation)
Name:           perl-JSON
Version:        4.10
Release:        1%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/JSON
Source0:        https://cpan.metacpan.org/modules/by-module/JSON/JSON-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
%if %{with_check}
BuildRequires:  perl(Tie::Array)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:       perl(JSON)
BuildArch:      noarch
%{?perl_default_filter}

%description
This module converts between JSON (JavaScript Object Notation) and Perl
data structure into each other. For JSON, see http://www.crockford.com/JSON/.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       coreutils
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n JSON-%{version}

# make rpmlint happy...
find .  -type f -exec chmod -c -x {} +
find t/ -type f -exec perl -pi -e 's|^#! perl|#!perl|' {} +
sed -i 's/\r//' README t/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
# t/20_unknown.t writes to CWD
DIR=$(mktemp -d)
cp -a %{_libexecdir}/%{name}/t "$DIR"
unset PERL_JSON_BACKEND PERL_JSON_DEBUG PERL_JSON_PP_USE_B
pushd "$DIR"
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -r "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.10-1
- Auto-upgrade to 4.10 - Azure Linux 3.0 - package upgrades

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 4.05-1
- Update to 4.05
- Update Source0

* Wed Mar 02 2022 Muhammad Falak <mwani@microsoft.com> - 4.02-8
- Add an explicit BR on `perl(Tie::Array)` to enable ptest

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.02-7
- Adding 'BuildRequires: perl-generators'.

* Wed Apr 28 2021 Thomas Crain <thcrain@microsoft.com> - 4.02-6
- Manually define tests subpackage, taken from Fedora 34 (license: MIT)

* Wed Oct 21 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.02-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.02-2
- Perl 5.30 rebuild

* Sat Feb 23 2019 Paul Howarth <paul@city-fan.org> - 4.02-1
- Update to 4.02
  - Fix a test that broke if perl was compiled with -Dquadmath (CPAN RT#128589)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 4.01-1
- Update to 4.01

* Fri Dec  7 2018 Paul Howarth <paul@city-fan.org> - 4.00-1
- Update to 4.00
  - BACKWARD INCOMPATIBILITY: As JSON::XS 4.0 changed its policy and enabled
    allow_nonref by default, JSON::PP, and thus JSON, also enabled allow_nonref
    by default
  - Updated backportPP with JSON::PP 4.00
  - Allow PERL_JSON_PP_USE_B environmental variable to restore old number
    detection behavior for compatibility
- RPM version resynced with upstream

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.97.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.97.001-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.97.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Paul Howarth <paul@city-fan.org> - 2.97.001-1
- Update to 2.97001
  - Updated backportPP with JSON::PP 2.97001

* Tue Nov 21 2017 Paul Howarth <paul@city-fan.org> - 2.97-1
- Update to 2.97 (upstream 2.97000 but stick to two-digit minor version
  downstream in case upstream changes back before version 3.x)

* Mon Nov 20 2017 Paul Howarth <paul@city-fan.org> - 2.96-1
- Update to 2.96

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.94-1
- Update to 2.94

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.93-3
- Perl 5.26 rebuild

* Tue May 23 2017 Petr Pisar <ppisar@redhat.com> - 2.93-2
- Filter private JSON::backportPP::Boolean

* Mon May 22 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 2.93-1
- Update to 2.93

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.90-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.90-7
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.90-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.90-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.90-4
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.90-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 03 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.90-1
- Update to 2.90

* Sun Oct 20 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.61-1
- Update to 2.61

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.59-2
- Perl 5.18 rebuild

* Sun Jun 09 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.59-1
- Update to 2.59

* Sun May 26 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.58-1
- Update to 2.58

* Sun Apr 07 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.57-1
- Update to 2.57
- Remove no-longer-used macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 2.53-7
- Add some missing and remove some obsolete deps

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.53-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 2.53-3
- update filtering macros for rpm 4.9

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.53-2
- Perl mass rebuild

* Sun May 22 2011 Paul Howarth <paul@city-fan.org> 2.53-1
- update to 2.53
  - fixed to_json (CPAN RT#68359)
  - backport JSON::PP 2.27200 (fixed incr_parse decoding string more correctly
    - CPAN RT#68032)
  - made Makefile.PL skip an installing XS question when set $ENV{PERL_ONLY} or
    $ENV{NO_XS} (CPAN RT#66820)

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> 2.51-1
- update to 2.51 (#683052)
  - import JSON::PP 2.27105 as BackportPP
  - fix documentation (CPAN RT#64738)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> 2.50-1
- update to 2.50 (#665621)
  - JSON::PP split off into separate distribution and replaced with
    JSON::backportPP instead for internal use
- BR: perl(Test::Pod)
- drop t/ from %%doc as the tests are in the -tests subpackage
- filter private module perl(JSON::backportPP) from requires
- filter private module perl(JSON::backportPP::Boolean) from provides
- filter private module perl(JSON::Backend::PP) from provides
- filter private module perl(JSON::Boolean) from provides
- filter private module perl(JSON::PP) from provides (really JSON::backportPP)
- filter private module perl(JSON::PP::IncrParser) from provides

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 2.27-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.17-2
- Mass rebuild with perl-5.12.0

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 2.17-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(HTTP::Request)
- dropped old BR on perl(HTTP::Response)
- dropped old requires on perl(HTTP::Daemon)
- dropped old requires on perl(LWP::UserAgent)
- dropped old requires on perl(Scalar::Util)

* Wed Sep 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-5
- adjust filtering so we don't drop the versioned perl(JSON:PP) prov

* Tue Sep 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-4
- bump

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-3
- update filtering

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-1
- auto-update to 2.15 (by cpan-spec-update 0.01)

* Sun Mar 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.14-1
- update to 2.14

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.12-1
- update to 2.12

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.11-1
- update to 2.11

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.09-1
- update to 2.09

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.07-1
- update to 2.x series before F9

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.15-2
- rebuild for new perl

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- update to 1.15

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.14-1
- update to 1.14

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.13-1
- update to 1.13

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.12-1
- update to 1.12
- add t/ to %%doc

* Wed Apr 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-2
- bump

* Tue Apr 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Apr 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.10-1
- Specfile autogenerated by cpanspec 1.69.1.
