# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Net-SNMP
Version:        6.0.1
Release:        44%{?dist}
Summary:        Object oriented interface to SNMP

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Net-SNMP
Source0:        https://cpan.metacpan.org/authors/id/D/DT/DTOWN/Net-SNMP-v%{version}.tar.gz
Patch0:         Net-SNMP-v6.0.1-Switch_from_Socket6_to_Socket.patch
Patch1:         Net-SNMP-v6.0.1-Simple_rewrite_to_Digest-HMAC-helpers.patch
Patch2:         Net-SNMP-v6.0.1-Split_usm.t_to_two_parts.patch
Patch3:         Net-SNMP-v6.0.1-Add_tests_for_another_usm_scenarios.patch
Patch4:         Net-SNMP-v6.0.1-Rewrite_from_Digest-SHA1-to-Digest-SHA.patch

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
# Carp not used at tests
# Crypt::DES 2.03 not used at tests
# Digest::HMAC_MD5 1.01 not used at tests
# Digest::HMAC_SHA1 1.03 not used at tests
# Digest::MD5 2.11 not used at tests
# Digest::SHA1 1.02 not used at tests
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Socket)
# Optional run-time:
# Crypt::Rijndael 1.02 not used at tests
# Sys::Hostname not used at tests
# Tests:
BuildRequires:  perl(Test)
Requires:       perl(Carp)
Requires:       perl(Crypt::DES) >= 2.03
Requires:       perl(Digest::HMAC_MD5) => 1.01
Requires:       perl(Digest::HMAC_SHA1) => 1.03
Requires:       perl(Digest::MD5) >= 2.11
# Optional run-time:
# Crypt::Rijndael 1.02

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Crypt::DES|Digest::HMAC_MD5|Digest::HMAC_SHA1|Digest::MD5)\\)$

%description
The Net::SNMP module implements an object oriented interface to the
Simple Network Management Protocol.  Perl applications can use the
module to retrieve or update information on a remote host using the
SNMP protocol.  The module supports SNMP version-1, SNMP version-2c
(Community-Based SNMPv2), and SNMP version-3.  The Net::SNMP module
assumes that the user has a basic understanding of the Simple Network
Management Protocol and related network management concepts.


%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness


%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".


%prep
%setup -q -n Net-SNMP-v%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
perl -MConfig -pi -e 's|^#!.*perl|$Config{startperl}|' examples/*.pl

chmod -c a-x examples/*.pl

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done


%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}


%install
%{make_install}
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test


%check
make test



%files
%doc Changes README examples/
%{_bindir}/*
%{perl_vendorlib}/Net/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*


%files tests
%{_libexecdir}/%{name}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 04 2024 Michal Josef Špaček <mspacek@redhat.com> - 6.0.1-41
- Add patch to add tests for other USM scenarios
- Add patch to rewrite from Digest::SHA1 to Digest::SHA
- Add patch to rewrite usage of HMAC with same dependencies
- Add patch to split test files for better readability
- Improve patch for switch from Socket6 to Socket
- Package tests
- Rename patch to better name with source dist version

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-37
- Modernize spec
- Update license to SPDX format

* Wed Jun 14 2023 Petr Salaba <psalaba@redhat.com> - 6.0.1-36
- Switch from Socket6 to Socket

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-33
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-30
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-27
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-24
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-21
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-18
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-16
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 17 2015 Petr Pisar <ppisar@redhat.com> - 6.0.1-14
- Specify all dependencies (bug #1243871)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-12
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.1-11
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 6.0.1-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.0.1-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.0.1-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 6.0.1-1
- update to 6.0.1, which removed all occurrences of the "locked" attribute, 
  deprecated in perl 5.12.0
- okay to use Socket6 now.

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.2.0-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.2.0-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.2.0-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.2.0-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.2.0-1
- First build.
