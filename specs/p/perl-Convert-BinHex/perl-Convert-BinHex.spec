# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Convert-BinHex
Version:	1.125
Release:	31%{?dist}
Summary:	Convert to/from RFC1741 HQX7 (Mac BinHex)
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Convert-BinHex
Source0:	https://cpan.metacpan.org/modules/by-module/Convert/Convert-BinHex-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(integer)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
# Script Runtime
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(Getopt::Std)
# Test Suite
BuildRequires:	perl(autodie)
BuildRequires:	perl(File::Compare)
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(File::Temp) >= 0.17
BuildRequires:	perl(FindBin)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::Most)
# Extra Tests
BuildRequires:	perl(Test::Pod) >= 1.00
# Release Tests
%if !0%{?rhel:1}
BuildRequires:	perl(Test::CPAN::Changes)
%endif
# Dependencies
# (none)

# Remove Mac::Files dependency, only needed on MacOS
%global __requires_exclude ^perl\\(Mac::Files\\)

%description
Convert::BinHex extracts data from Macintosh BinHex files.

%prep
%setup -q -n Convert-BinHex-%{version}

# Don't want to ship a script with a security hole
perl -pi -e 's/^use lib .*$//' bin/*.pl

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test %{!?rhel:RELEASE_TESTING=1}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"

%files
%license COPYING LICENSE
%doc Changes README*
%{_bindir}/binhex.pl
%{_bindir}/debinhex.pl
%{perl_vendorlib}/Convert/
%{_mandir}/man1/binhex.pl.1*
%{_mandir}/man1/debinhex.pl.1*
%{_mandir}/man3/Convert::BinHex.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep  1 2024 Paul Howarth <paul@city-fan.org> - 1.125-29
- Avoid release tests for EPEL builds

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.125-24
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-21
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-18
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-15
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 27 2019 Paul Howarth <paul@city-fan.org> - 1.125-13
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.125-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Paul Howarth <paul@city-fan.org> - 1.125-1
- Update to 1.125
  - Made the Test:: modules TEST_REQUIRES (CPAN RT#108523)

* Thu Aug 20 2015 Paul Howarth <paul@city-fan.org> - 1.124-1
- Update to 1.124
  - Changed debinhex to UTF-8
  - Made the Test:: modules optional (CPAN RT#101974)
  - Fixed a manual typo (CPAN RT#88874)
- Use %%license

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.123-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.123-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.123-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep  7 2013 Paul Howarth <paul@city-fan.org> 1.123-1
- Update to 1.223
  - Fixed pod error in debinhex and added pod tests
- Drop UTF8 patch, fixed upstream
- Explicitly run the extra tests

* Sun Sep  1 2013 Paul Howarth <paul@city-fan.org> 1.122-1
- Update to 1.222
  - New upstream maintainer STEPHEN
  - Changes file reformatted
  - Moved to Dist::Zilla's OurPkgVersion for keeping $VERSIONs in sync
  - Added unit tests for OO and CRC code
- This release by STEPHEN -> update source URL
- Package new upstream Changes and LICENSE files
- Package new manpages for scripts
- Specify all dependencies
- Run the release tests too
- Clean up spec for modern rpmbuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.119-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.119-21
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.119-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.119-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.119-18
- Perl 5.16 rebuild

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 1.119-17
- nobody else likes macros for commands
- BR: perl(Carp)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.119-16
- perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-15
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 1.119-14
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.119-13
- mass rebuild with perl-5.12.0

* Thu Jan 14 2010 Paul Howarth <paul@city-fan.org> 1.119-12
- minor spec issues from merge review (#552554)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 1.119-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-10
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-9
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.119-8
- rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.119-7
- rebuild for new perl

* Sat Aug 11 2007 Paul Howarth <paul@city-fan.org> 1.119-6
- clarify license as GPL version 1 or later, or Artistic (same as perl)

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.119-5
- add perl(ExtUtils::MakeMaker) buildreq
- use tabs rather than spaces

* Sun Sep 17 2006 Paul Howarth <paul@city-fan.org> 1.119-4
- add dist tag
- fix argument order in find command with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.119-3
- use full paths for all commands used in build
- use search.cpan.org download URL
- assume rpm knows about %%check and %%{perl_vendorlib}
- cosmetic spec file changes

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.119-2
- rebuilt

* Wed Sep 15 2004 Ville Skyttä <ville.skytta at iki.fi> 1.119-1
- first build
