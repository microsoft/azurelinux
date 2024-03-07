#TODO: BR:/R: perl(IP::Authority) when available
Summary:        Perl module for manipulation of IPv4 and IPv6 addresses
Name:           perl-Net-IP
Version:        1.26
Release:        32%{?dist}
# Some ambiguity here, see http://rt.cpan.org/Ticket/Display.html?id=28689
# HPND (MIT-like) for the IP.pm itself, and "like Perl itself" for all the other
# scripts included.
License:        HPND AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Net-IP
Source:         https://cpan.metacpan.org/modules/by-module/Net/Net-IP-%{version}.tar.gz
Patch0:         Net-IP-1.26-rt60439.patch
Patch1:         Net-IP-1.26-shellbang.patch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(FileHandle)
# Script Run-time:
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildArch:      noarch
# Dependencies:
# Not yet packaged: IP::Authority

%description
This is the Net::IP module, designed to allow easy manipulation of IPv4 and
IPv6 addresses.

Two applications using the Net::IP module are included: ipcount, an IP address
mini-calculator, which can calculate the number of IP addresses in a prefix or
all the prefixes contained in a given range; and iptab, which prints out a
handy IP "cheat sheet".

%prep
%setup -q -n Net-IP-%{version}

# Apply fix for zero networks (#197425, CPAN RT#20265, CPAN RT#60439)
%patch0

# Fix shellbangs in shipped scripts
%patch1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

# This should work for 0.0.0.0
# https://bugzilla.redhat.com/show_bug.cgi?id=197425
PERL5LIB=%{buildroot}%{perl_vendorlib} ./iptab

%files
%license COPYING
%doc Changes README
# GPL-1.0-or-later OR Artistic-1.0-Perl
%{_bindir}/ipcount
%{_bindir}/iptab
# HPND
%{perl_vendorlib}/Net/
%{_mandir}/man3/Net::IP.3*

%changelog
* Thu Oct 19 2023 Archana Choudhary <archana1@microsoft.com> - 1.26-32
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-28
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-25
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-22
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 1.26-20
- Use upstream-approved fix for zero networks (CPAN RT#60439)
- Fix shellbangs in utility scripts
- Specify all dependencies
- Use %%license

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-18
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-15
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-12
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-7
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.26-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Petr Pisar <ppisar@redhat.com> - 1.26-1
- 1.26 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.25-19
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.25-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-15
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-14
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1.25-13
- fix the source URL

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 1.25-12
- fix license tag

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.25-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-8
- Rebuild for perl 5.10 (again)

* Fri Feb  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-7
- disable tests due to upstream bug 50114

* Fri Feb  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-6
- Work around http://rt.perl.org/rt3//Public/Bug/Display.html?id=50114

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.25-5
- rebuild for new perl

* Sun Aug 12 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.25-4
- BuildRequire perl(ExtUtils::MakeMaker)
- License: MIT

* Sun Feb 04 2007 Robin Norwood <rnorwood@redhat.com> - 1.25-3
- Resolves: bz#226271
- Incorporate some fixes to the spec file from Ville:

* Wed Jul 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.25-2
- fix bug 197925 - make intip handle zero-valued IP addresses

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.25-1
- upgrade to 1.25

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.24-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Mon Oct 31 2005 Warren Togami <wtogami@redhat.com> - 1.24-2
- import into FC5 because perl-Net-DNS needs it

* Wed Oct 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.24-1
- 1.24.

* Mon Jun  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.23-3
- 1.23, patches applied upstream.
- Improve description.

* Sun May 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.22-2
- 1.22, include test case for rt.cpan.org #7528 patch.
- Patch to mute stdout noise from ip_reverse().

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.21-2
- rebuilt

* Thu Dec  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.21-1
- Update to 1.21.

* Sat Nov  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.7
- Apply fixes from rt.cpan.org #3844 and #7528.
- Some specfile cleanups.

* Sun May  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.6
- BuildRequire perl >= 1:5.6.1-34.99.6 for support for vendor installdirs.
- Use pure_install to avoid perllocal.pod workarounds.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.5
- Require perl(:MODULE_COMPAT_*).

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.4
- Reduce directory ownership bloat.

* Mon Dec  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.3
- Specfile cleanup.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.2
- Install into vendor dirs.

* Wed Jul 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20-0.fdr.1
- First build.
