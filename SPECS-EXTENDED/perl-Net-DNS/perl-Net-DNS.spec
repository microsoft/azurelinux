Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          perl-Net-DNS
Version:       1.21
Release:       3%{?dist}
Summary:       DNS resolver modules for Perl
# Other files:          MIT
# demo/mresolv:         GPL+ or Artistic
## Not in a binary package
# contrib/find_zonecut: GPL+ or Artistic
# contrib/check_soa:    GPL+ or Artistic
License:       (GPL+ or Artistic) and MIT
URL:           https://metacpan.org/release/Net-DNS
Source0:       https://cpan.metacpan.org/authors/id/N/NL/NLNETLABS/Net-DNS-%{version}.tar.gz#/perl-Net-DNS-%{version}.tar.gz
BuildArch:     noarch
# Build
BuildRequires: coreutils
BuildRequires: findutils
BuildRequires: glibc-common
BuildRequires: make
BuildRequires: sed
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(IO::Socket)
# Runtime
BuildRequires: perl(base)
BuildRequires: perl(Carp)
# Config not used
BuildRequires: perl(constant)
BuildRequires: perl(Data::Dumper)
%if ! (0%{?rhel} >= 7)
# Digest::BubbleBabble is optional
BuildRequires: perl(Digest::BubbleBabble)
%endif
# Digest::GOST is optional and intentionally unavailable
# Digest::GOST::CryptoPro is optional and intentionally unavailable
BuildRequires: perl(Digest::HMAC) >= 1.03
BuildRequires: perl(Digest::MD5) >= 2.13
BuildRequires: perl(Digest::SHA) >= 5.23
BuildRequires: perl(Encode)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(FileHandle)
BuildRequires: perl(integer)
BuildRequires: perl(IO::File)
# IO::Select is not used
# Prefer IO::Socket::IP over IO::Socket::INET for IPv6 support
BuildRequires: perl(IO::Socket::IP) >= 0.32
BuildRequires: perl(MIME::Base64) >= 2.13
# Prefer Net::LibIDN2 over Net::LibIDN, both are optional
BuildRequires: perl(Net::LibIDN2) >= 1
BuildRequires: perl(overload)
# PerlIO is optional
# Scalar::Util is optional
BuildRequires: perl(Socket)
BuildRequires: perl(strict)
BuildRequires: perl(Time::Local)
BuildRequires: perl(warnings)
# Win32::IPHelper is not needed
# Win32::TieRegistry is not needed
# Tests only
BuildRequires: perl(File::Find)
BuildRequires: perl(Test::Builder)
BuildRequires: perl(Test::More)
# Optional tests:
BuildRequires: perl(Test::Pod) >= 1.45
%if !%{defined perl_bootstrap}
# Build cycle: perl-Net-DNS-SEC → perl-Net-DNS
BuildRequires: perl(Net::DNS::SEC)
BuildRequires: perl(Net::DNS::SEC::RSA)
%endif
Requires:      perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Suggests:      perl(Config)
Requires:      perl(Data::Dumper)
# Digest::GOST not available
Requires:      perl(Digest::HMAC) >= 1.03
Requires:      perl(Digest::MD5) >= 2.13
Requires:      perl(Digest::SHA) >= 5.23
Requires:      perl(Encode)
# Prefer IO::Socket::IP over IO::Socket::INET for IPv6 support
Recommends:    perl(IO::Socket::IP) >= 0.32
Requires:      perl(MIME::Base64) >= 2.13
# Net::DNS::Extlang not available
Suggests:      perl(Net::DNS::SEC::DSA)
# Net::DNS::SEC::ECCGOST not available
Suggests:      perl(Net::DNS::SEC::ECDSA)
Suggests:      perl(Net::DNS::SEC::EdDSA)
Suggests:      perl(Net::DNS::SEC::Private)
Suggests:      perl(Net::DNS::SEC::RSA)
# Prefer Net::LibIDN2 over Net::LibIDN, both are optional
Suggests:      perl(Net::LibIDN2) >= 1
Suggests:      perl(Scalar::Util) >= 1.25

%{?perl_default_filter}

# Do not export under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Digest::HMAC\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Digest::MD5\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Digest::SHA\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(MIME::Base64\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CONFIG\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(OS_CONF\\)$
# Do not export under-specified provides
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((Net::DNS::Text)\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((Net::DNS::RR::OPT)\\)$

%description
Net::DNS is a collection of Perl modules that act as a Domain Name System
(DNS) resolver. It allows the programmer to perform DNS queries that are
beyond the capabilities of gethostbyname and gethostbyaddr.

The programmer should be somewhat familiar with the format of a DNS packet and
its various sections. See RFC 1035 or DNS and BIND (Albitz & Liu) for details.

%package Nameserver
Summary:        DNS server for Perl
License:        MIT
Recommends:     perl(IO::Socket::IP) >= 0.32

%description Nameserver
Instances of the "Net::DNS::Nameserver" class represent DNS server objects.

%prep
%setup -q -n Net-DNS-%{version} 
chmod -x demo/*
sed -i -e '1 s,^#!/usr/local/bin/perl,#!%{__perl},' demo/*
for i in Changes; do
    iconv -f iso8859-1 -t utf-8 "$i" > "${i}.conv"
    touch -r "$i" "${i}.iconv"
    mv -f "${i}.conv" "$i"
done

%build
export PERL_MM_USE_DEFAULT=yes
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 --no-online-tests
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc README Changes demo
%{perl_vendorlib}/Net/
%exclude %{perl_vendorlib}/Net/DNS/Resolver/cygwin.pm
%exclude %{perl_vendorlib}/Net/DNS/Resolver/MSWin32.pm
%{_mandir}/man3/Net::DNS*.3*
%exclude %{_mandir}/man3/Net::DNS::Resolver::cygwin.3*
%exclude %{_mandir}/man3/Net::DNS::Resolver::MSWin32.3*
# perl-Net-DNS-Nameserver
%exclude %{perl_vendorlib}/Net/DNS/Nameserver.pm
%exclude %{_mandir}/man3/Net::DNS::Nameserver*

%files Nameserver
%{perl_vendorlib}/Net/DNS/Nameserver.pm
%{_mandir}/man3/Net::DNS::Nameserver*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.21-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-1
- 1.21 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-2
- Perl 5.30 rebuild

* Wed May 22 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.20-1
- 1.20 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-1
- 1.19 bump

* Wed Oct 03 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.18-1
- 1.18 bump

* Tue Aug 07 2018 Petr Pisar <ppisar@redhat.com> - 1.17-1
- 1.17 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.28 rebuild

* Wed Feb 14 2018 Paul Wouters <pwouters@redhat.com> - 1.15
- Resolves rhbz#1544065 Update to 1.15 - Maintenance only

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Paul Wouters <pwouters@redhat.com> - 1.14-1
- Updated to 1.14

* Tue Oct 31 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-1
- Updated to 1.13

* Fri Aug 18 2017 Paul Wouters <pwouters@redhat.com> - 1.12-1
- Updated to 1.12

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-2
- Perl 5.26 rebuild

* Tue May 09 2017 Paul Wouters <pwouters@redhat.com> - 1.10-1
- Resolves: rhbz#1448614 perl-Net-DNS-1.10 is available

* Tue Apr 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-1
- 1.09 bump

* Tue Mar 21 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-1
- 1.08 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 01 2017 Paul Wouters <pwouters@redhat.com> - 1.07-1
- Update to 1.07 (Net::DNS::Nameserver EDNS reply fixes, Net::DNS::Zonefile parse fixes)

* Wed Jun 01 2016 Paul Wouters <pwouters@redhat.com> - 1.06-3
- Remove dependancy on perl-Net-DNS-SEC (required code was moved in here)

* Tue May 31 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-2
- Remove OS_CONF from requires

* Mon May 30 2016 Paul Wouters <pwouters@redhat.com> - 1.06-1
- Update to 1.06 (rhbz#1315525)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-2
- Filter perl(CONFIG) from requires

* Thu Dec 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-1
- 1.02 bump

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 1.01-3
- Build-require Time::Local (bug #1264751)

* Tue Sep 01 2015 Petr Pisar <ppisar@redhat.com> - 1.01-2
- Break build cycle: perl-Net-DNS-SEC → perl-Net-DNS → perl-Net-DNS-SEC

* Fri Aug 07 2015 Petr Šabata <contyk@redhat.com> - 1.01-1
- 1.01 bump
- The package is now noarch as the binary bits were dropped
- Furthermore, the license was changed to Perl and MIT

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-2
- Perl 5.22 rebuild

* Fri Feb 27 2015 Petr Šabata <contyk@redhat.com> - 0.83-1
- 0.83 bump
- Correct the dependency list
- Modernize the spec a bit

* Tue Jan 20 2015 Paul Wouters <pwouters@redhat.com> - 0.82-1
- Updated to 0.82 Support for IPv6 link-local addresses with scope_id

* Wed Oct 29 2014 Paul Wouters <pwouters@redhat.com> - 0.81-1
- Updated to 0.81, Fixes AXFR BADSIG and infinite recursion in Net::DNS::Resolver
- Resolves rhbz#1151572

* Mon Sep 22 2014 Paul Wouters <pwouters@redhat.com> - 0.80-1
- Updated to 0.80 with "Too late to run INIT block" fix and new force_v6 option

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.79-2
- Perl 5.20 rebuild

* Sun Aug 24 2014 Paul Wouters <pwouters@redhat.com> - 0.79-1
- Updated to 0.79 with OPENPGPKEY RRtype support

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Paul Wouters <pwouters@redhat.com> - 0.78-1
- Updated to 0.78, various bugfixes and multiline TXT rdata printing support

* Sat Jun 14 2014 Paul Wouters <pwouters@redhat.com> - 0.77-1
- Updated to 0.77, a "quickfix release" fixing AXFR support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Petr Šabata <contyk@redhat.com> - 0.76-1
- More fixes related to spamassassin

* Fri May 23 2014 Petr Šabata <contyk@redhat.com> - 0.75_1-1
- Update to the latest development release, fixing a number of
  regressions introduced with 0.75

* Mon May 12 2014 Petr Šabata <contyk@redhat.com> - 0.75-1
- 0.75 bump

* Mon Jan 20 2014 Petr Šabata <contyk@redhat.com> - 0.74-1
- 0.74 bump, fixes the server crash on malformed queries

* Fri Nov 29 2013 Paul Wouters <pwouters@redhat.com> - 0.73-1
- Updated to 0.73

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 0.72-5
- Specify more dependencies

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.72-4
- Perl 5.18 rebuild

* Wed May 22 2013 Petr Pisar <ppisar@redhat.com> - 0.72-3
- Add BSD, ISC, and MIT to licenses
- Specify all dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 0.72-1
- 0.72 bump

* Mon Dec 17 2012 Petr Šabata <contyk@redhat.com> - 0.71-1
- 0.71 bump

* Fri Dec 07 2012 Petr Pisar <ppisar@redhat.com> - 0.70-1
- 0.70 bump

* Thu Dec 06 2012 Paul Howarth <paul@city-fan.org> - 0.69-2
- Fix renamed Win32 excludes

* Thu Dec 06 2012 Petr Šabata <contyk@redhat.com> - 0.69-1
- 0.69 bump
- Update source URL

* Fri Aug 10 2012 Petr Pisar <ppisar@redhat.com> - 0.68-5
- Digest::BubbleBabble is not available in RHEL >= 7

* Fri Aug 10 2012 Petr Pisar <ppisar@redhat.com> - 0.68-4
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.68-2
- Perl 5.16 rebuild

* Thu Feb 02 2012 Petr Šabata <contyk@redhat.com> - 0.68-1
- 0.68 bump
- Spec cleanup
- Package 'demo' as documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.67-1
- update to 0.67

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.66-4
- Perl mass rebuild

* Fri Jun 03 2011 Petr Sabata <contyk@redhat.com> - 0.66-3
- Introduce IPv6 support and prevent interactive build (#710375)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.66-1
- update

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.65-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.65-2
- rebuild against perl 5.10.1

* Thu Sep 17 2009 Warren Togami <wtogami@redhat.com> - 0.65-1
- 0.65

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.63-4
- 437681 remove previous patch and use upstream patch, which should solve
        all problems with noisy logs.

* Wed Apr  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-3
- fix patch to not require Socket6

* Wed Apr  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-2
- fix AF_INET6/PF_INET6 redefine noise (bz 437681)

* Wed Mar 19 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.63-1
- upgrade on new upstream version which fix CVE-2007-6341 - no security impact.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.61-7
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.61-6
- Autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.61-5
- rebuild for new perl

* Fri Dec 21 2007 Paul Howarth <paul@city-fan.org> - 0.61-4
- Fix file ownership for Nameserver subpackage
- Fix argument order for find with -depth

* Fri Dec 14 2007 Robin Norwood <rnorwood@redhat.com> - 0.61-3
- Split Nameserver.pm into subpackage, per recommendation from
  upstream maintainer Dick Franks.
  - Separates the server bits from the client bits.
  - Removes the dependancy on perl(Net::IP) from perl-Net-DNS
- Add BR for perl(Test::Pod) and perl(Digest::BubbleBabble)

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.61-2
- Update license tag
- Convert Changes to utf-8

* Thu Aug 09 2007 Robin Norwood <rnorwood@redhat.com> - 0.61-1
- Update to latest upstream version

* Sat Jun 23 2007 Robin Norwood <rnorwood@redhat.com> - 0.60-1
- Upgrade to latest upstream version - 0.60

* Thu Apr 05 2007 Robin Norwood <rnorwood@redhat.com> - 0.59-2
- Resolves: bz#226270
- Fixed issues brought up during package review
- BuildRequires should not require perl, and fixed the format.
- Fixed the BuildRoot

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 0.59-1
- Upgrade to upstream version 0.59 per bug #208315

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.58-1.fc6
- Upgrade to upstream version 0.58

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.57-1.1
- rebuild

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 0.57-1
- Upgrade to upstream version 0.57

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.55-1.1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.55-1.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.55-1.1
- rebuild for new perl-5.8.8

* Mon Dec 19 2005 Jason Vas Dias <jvdias@redhat.com> - 0.55-1
- Upgrade to upstream version 0.55

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sun Oct 30 2005 Warren Togami <wtogami@redhat.com> - 0.53-1
- 0.53 buildreq perl-Net-IP

* Sat Apr  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.49-2
- Explicitly disable tests requiring network access at build time.
- Exclude Win32 and Cygwin specific modules.
- More specfile cleanups.
- Honor $RPM_OPT_FLAGS.

* Sat Apr 02 2005 Robert Scheck <redhat@linuxnetz.de> 0.49-1
- upgrade to 0.49 and spec file cleanup (#153186)

* Thu Mar 17 2005 Warren Togami <wtogami@redhat.com> 0.48-3
- reinclude ia64, thanks jvdias

* Tue Mar 15 2005 Warren Togami <wtogami@redhat.com> 0.48-2
- exclude ia64 for now due to Bug #151127

* Mon Oct 11 2004 Warren Togami <wtogami@redhat.com> 0.48-1
- #119983 0.48 fixes bugs

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.45-4
- rebuild

* Thu Apr 29 2004 Chip Turner <cturner@redhat.com> 0.45-3
- fix bug 122039 -- add filter-depends.sh to remove Win32 deps

* Fri Apr 23 2004 Chip Turner <cturner@redhat.com> 0.45-1
- bump, no longer noarch

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 0.45-1
- update to 0.45

* Mon Oct 20 2003 Chip Turner <cturner@redhat.com> 0.31-3.2
- fix interactive build issue

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Aug  6 2002 Chip Turner <cturner@localhost.localdomain>
- update to 0.26

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Sat Jun 15 2002 cturner@redhat.com
- Specfile autogenerated

