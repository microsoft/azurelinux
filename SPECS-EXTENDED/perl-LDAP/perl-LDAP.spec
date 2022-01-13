Vendor:         Microsoft Corporation
Distribution:   Mariner
# Perform optional tests
%bcond_with perl_LDAP_enables_optional_test
# Support XML serialization of LDAP schemata (DSML languge)
%if 0%{?rhel}
%bcond_with perl_LDAP_enables_xml
%else
%bcond_without perl_LDAP_enables_xml
%endif

Name:           perl-LDAP
Version:        0.66
Release:        10%{?dist}
Summary:        LDAP Perl module
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/perl-ldap
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MARSCHAP/perl-ldap-%{version}.tar.gz
Source1:        LICENSE.PTR
# Optional tests need to know a location of an LDAP server executable
Patch0:         perl-ldap-0.65-Configure-usr-sbin-slapd-for-tests.patch
# Remove an unreliable cancelling test
Patch1:         perl-ldap-0.66-test-Remove-a-test-for-cancelling-asynchronous-calls.patch
# Fix a shell bang in a certificate generator script,
# <https://github.com/perl-ldap/perl-ldap/pull/55>
Patch2:         perl-ldap-0.66-Correct-a-shell-bang-in-data-regenerate_cert.sh.patch
BuildArch:      noarch
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(FindBin)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Install::AutoInstall)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::WriteAll)
# Run-time:
# Not needed for tests perl(Authen::SASL) >= 2.00
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Convert::ASN1) >= 0.2
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
# Not needed for tests perl(HTTP::Negotiate)
# Not needed for tests perl(HTTP::Response)
# Not needed for tests perl(HTTP::Status)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
%if %{with perl_LDAP_enables_optional_test}
BuildRequires:  perl(IO::Socket::SSL) >= 1.26
%endif
# Not needed for tests perl(JSON)
# Not needed for tests perl(LWP::MediaTypes)
# Not needed for tests perl(LWP::Protocol)
# Not needed for tests perl(MIME::Base64)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
# Prefer core Text::Soundex
BuildRequires:  perl(Text::Soundex)
BuildRequires:  perl(Time::Local)
%if %{with perl_LDAP_enables_xml}
BuildRequires:  perl(XML::SAX::Base)
BuildRequires:  perl(XML::SAX::Writer)
%endif
# Optional:
# Not needed for tests perl(IO::Socket::INET6)
# Not needed for tests perl(IO::Socket::IP)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More)
%if %{with perl_LDAP_enables_optional_test}
# Optional tests:
BuildRequires:  openldap-servers
BuildRequires:  perl(LWP::UserAgent)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Authen::SASL) >= 2.00
Requires:       perl(Convert::ASN1) >= 0.2
Requires:       perl(IO::Socket::SSL) >= 1.26
Requires:       perl(JSON)
%if %{with perl_LDAP_enables_xml}
Suggests:       perl(Net::LDAP::DSML)
%endif
Requires:       perl(MIME::Base64)
# Prefer core Text::Soundex
Requires:       perl(Text::Soundex)
Requires:       perl(Time::Local)

# Remove under-specified dependencies
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Net::LDAP::Filter\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Convert::ASN1\\)$

%description
Net::LDAP is a collection of modules that implements an LDAP services API
for Perl programs. The module may be used to search directories or perform
maintenance functions such as adding, deleting or modifying entries.

%if %{with perl_LDAP_enables_xml}
%package -n perl-Net-LDAP-DSML
Summary:        DSML Writer for Net::LDAP
Requires:       perl-LDAP = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(MIME::Base64)
Requires:       perl(Net::LDAP::Schema)
Requires:       perl(XML::SAX::Writer)

%description -n perl-Net-LDAP-DSML
Directory Service Markup Language (DSML) is the XML standard for representing
directory service information in XML. At the moment this Perl module only
writes DSML entry and schema entities. Reading DSML entities is a future
project.
%endif

%package tests
Summary:        Tests for %{name}
Requires:       coreutils
Requires:       perl-LDAP = %{version}-%{release}
# perl-Test-Harness for "prove" command
Requires:       perl-Test-Harness
Requires:       perl(Convert::ASN1) >= 0.2
Requires:       perl(File::Basename)
Requires:       perl(File::Compare)
Requires:       perl(File::Path)
Requires:       perl(File::Spec)
Requires:       perl(IO::File)
Requires:       perl(Net::LDAP)
Requires:       perl(Net::LDAP::ASN)
Requires:       perl(Net::LDAP::Constant)
Requires:       perl(Net::LDAP::Control::Assertion)
Requires:       perl(Net::LDAP::Control::ManageDsaIT)
Requires:       perl(Net::LDAP::Control::MatchedValues)
Requires:       perl(Net::LDAP::Control::PostRead)
Requires:       perl(Net::LDAP::Control::PreRead)
Requires:       perl(Net::LDAP::Control::ProxyAuth)
Requires:       perl(Net::LDAP::Control::Sort)
Requires:       perl(Net::LDAP::Entry)
Requires:       perl(Net::LDAP::Extension::Cancel)
Requires:       perl(Net::LDAP::Filter)
Requires:       perl(Net::LDAP::FilterMatch)
Requires:       perl(Net::LDAP::LDIF)
Requires:       perl(Net::LDAP::Schema)
Requires:       perl(Net::LDAP::Util)
Requires:       perl(Net::LDAPI)
Requires:       perl(Test::More)
# Prefer core Text::Soundex
Requires:       perl(Text::Soundex)
%if %{with perl_LDAP_enables_xml}
Requires:       perl(Net::LDAP::DSML)
Requires:       perl(XML::SAX::Base)
Requires:       perl(XML::SAX::Writer)
%endif
%if %{with perl_LDAP_enables_optional_test}
# Optional tests:
Requires:       openldap-servers
Requires:       perl(IO::Socket::SSL) >= 1.26
Requires:       perl(Net::LDAPS)
Requires:       perl(LWP::UserAgent)
%endif

%description tests
Tests from %{name}-%{version}. Execute them with "%{_libexecdir}/%{name}/test".


%prep
%setup -q -n perl-ldap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod -c 644 bin/* contrib/* lib/Net/LDAP/DSML.pm
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' contrib/*
# Remove bundled libraries
rm -rf inc
sed -i -e '/^inc\// d' MANIFEST
# Remove tests specific for XML support if the support is disabled
%if !%{with perl_LDAP_enables_xml}
rm t/05dsml.t
sed -i -e '/^t\/05dsml\.t/ d' MANIFEST
%endif
find -type f \! -name 'regenerate_cert.sh' -exec chmod -x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
# FIXME: Generators should scan these non-executable files
cp -a data t test.cfg %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test <<'EOF'
#!/bin/bash
set -e
# t/common.pl reads from ./data and writes into ./temp. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I .
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test
%{_fixperms} %{buildroot}/*

cp %{SOURCE1} .

%check
make test
 
%files
%license LICENSE.PTR
%doc Changes CREDITS
%doc contrib/ bin/
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/LWP/
%{perl_vendorlib}/Net/
%exclude %{perl_vendorlib}/Net/LDAP/DSML.pm
%{_mandir}/man3/*.3pm*
%exclude %{_mandir}/man3/Net::LDAP::DSML.3pm*

%if %{with perl_LDAP_enables_xml}
%files -n perl-Net-LDAP-DSML
%{perl_vendorlib}/Net/LDAP/DSML.pm
%{_mandir}/man3/Net::LDAP::DSML.3pm*
%endif

%files tests
%{_libexecdir}/%{name}

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.66-10
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.66-9
- Remove epoch

* Fri Jan 29 2021 Joe Schmitt <joschmit@microsoft.com> - 1:0.66-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable optional tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.66-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Petr Pisar <ppisar@redhat.com> - 1:0.66-6
- Fix tests subpackage test script
- Fix a shell bang in a certificate generator script

* Mon Aug 26 2019 Petr Pisar <ppisar@redhat.com> - 1:0.66-5
- Package tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.66-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.66-3
- Perl 5.30 rebuild

* Thu Apr 25 2019 Petr Pisar <ppisar@redhat.com> - 1:0.66-2
- Remove an unreliable cancelling test

* Tue Apr 16 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.66-1
- 0.66 bump

* Thu Apr 04 2019 Petr Pisar <ppisar@redhat.com> - 1:0.65-13
- Correct misspellings in Net::LDAP::FAQ
- Perform tests against a server
- Net::LDAP::DSML moved to perl-Net-LDAP-DSML package due to XML dependencies

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-2
- Perl 5.22 rebuild

* Tue Apr 07 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.65-1
- 0.65 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.64-2
- Perl 5.20 rebuild

* Mon Jun 23 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.64-1
- 0.64 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.63-1
- 0.63 bump

* Mon Apr 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.62-1
- 0.62 bump

* Mon Mar 31 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.61-1
- 0.61 bump

* Tue Mar 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.60-1
- 0.60 bump

* Wed Mar 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.59-1
- 0.59 bump

* Thu Jan 02 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.58-1
- 0.58 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 1:0.57-2
- Perl 5.18 rebuild

* Wed Jul 31 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.57-1
- 0.57 bump

* Mon Jun 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.56-1
- 0.56 bump

* Wed Apr 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.55-1
- 0.55 bump

* Wed Apr 03 2013 Petr Pisar <ppisar@redhat.com> - 1:0.54-1
- 0.54 bump

* Mon Jan 28 2013 Petr Šabata <contyk@redhat.com> - 1:0.53-1
- 0.53 enhancement update

* Thu Jan 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.52-1
- 0.52 bump

* Mon Dec 03 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.51-1
- 0.51 bump

* Mon Nov 26 2012 Petr Pisar <ppisar@redhat.com> - 1:0.50-1
- 0.50 bump

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 1:0.49-2
- Add a few missing deps
- Drop command macros
- Modernize the spec

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 1:0.49-1
- 0.49 bump

* Mon Sep 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.47-1
- 0.47 bump

* Fri Sep 14 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.46-1
- 0.46 bump
- Should fix: RT#72108, RT#74572, RT#74759, RT#77180
- Removed bundled libraries. Use perl(inc::Module::Install).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1:0.44-2
- Perl 5.16 rebuild
- Specify all dependencies

* Mon Feb  6 2012  Marcela Maslanova <mmaslano@redhat.com> - 1:0.44-1
- update which should fix RT#66753
- clean specfile according to new guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.40-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1:0.40-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.40-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.40-2
- Mass rebuild with perl-5.12.0

* Mon Apr 12 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.40-1
- update

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.34-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.34-4
- rebuild for new perl

* Mon Apr 09 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-3
- Resolves: bz#226267
- Only filter out the unversioned Provides: perl(Net::LDAP::Filter) to
  avoid breaking dependencies.

* Thu Apr 05 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-2
- Resolves: bz#226267
- Filter out provides perl(Net::LDAP::Filter) per package review.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-1
- New version: 0.34

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 1:0.33-3
- Bugzilla: 207430
- Incorporate fixes from Jose Oliveira's patch
- Add perl(IO::Socket::SSL) as a BuildRequires as well
- Other cleanups from Jose

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 0.33-1.3
- Add a requirement for IO::Socket::SSL, per bug #122066

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.33-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Tue Apr 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.33-1
- Update to 0.33.

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.3202-1
- Update to 0.3202.
- Specfile cleanup. (#153766)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.31-5
- rebuild

* Wed Mar 10 2004 Chip Turner <cturner@redhat.com> - 0.31-1
- Specfile autogenerated.

