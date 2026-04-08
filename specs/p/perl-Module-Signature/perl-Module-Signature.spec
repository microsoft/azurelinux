# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Store keys in a temp directory
%global gnupghome %(mktemp --directory)

Name:           perl-Module-Signature
Version:        0.93
Release:        2%{?dist}
Summary:        CPAN signature management utilities and modules
License:        CC0-1.0
URL:            https://metacpan.org/release/Module-Signature
Source0:        https://cpan.metacpan.org/modules/by-module/Module/Module-Signature-%{version}.tar.gz
BuildArch:      noarch
# Module build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
# Module runtime
BuildRequires:  gnupg2
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::Diff)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# Test suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
# Dependencies
Requires:       gnupg2
Requires:       perl(Digest::SHA)
Requires:       perl(File::Temp)
Requires:       perl(IO::Socket::INET)
Requires:       perl(Text::Diff)
Requires:       perl(version)
Suggests:       perl(PAR::Dist)
Suggests:       /usr/bin/perldoc

%description
This package contains a command line tool and module for checking and creating
SIGNATURE files for Perl CPAN distributions.

%prep
%setup -q -n Module-Signature-%{version}

%build
export GNUPGHOME=%{gnupghome}
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
export GNUPGHOME=%{gnupghome}
# Don't try to run signature test because it needs access over network to keyserver,
# even if we have the necessary keys already
make test TEST_SIGNATURE=0

%clean
rm -rf %{buildroot} %{gnupghome}

%files
%doc AUTHORS Changes SECURITY.md *.pub
%{_bindir}/cpansign
%{perl_vendorlib}/Module/
%{_mandir}/man1/cpansign.1*
%{_mandir}/man3/Module::Signature.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 28 2025 Paul Howarth <paul@city-fan.org> - 0.93-1
- Update to 0.93
  - The cpansign script was not installed with version 0.92 (GH#44)

* Fri Jun 27 2025 Paul Howarth <paul@city-fan.org> - 0.92-1
- Update to 0.92
 - Add SECURITY.md policy
 - Move to three-arg open
 - Remove spaces from eol
 - Change build process to Dist::Zilla
- Suggest perldoc, needed for cpansign --help

* Fri Jun 13 2025 Paul Howarth <paul@city-fan.org> - 0.90-1
- Update to 0.90
  - Fix fail on signature file with an unexpected empty line (CPAN RT#166901)
- Use %%{make_build} and %%{make_install}

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 Paul Howarth <paul@city-fan.org> - 0.89-1
- Update to 0.89 (rhbz#2312488)
  - Replace keyserver with keyserver.ubuntu.com (GH#34, GH#38)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 13 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.88-7
- Drop redundant dependency of Digest::SHA1; implementation from Digest::SHA
  is used instead

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.88-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 18 2021 Paul Howarth <paul@city-fan.org> - 0.88-1
- Update to 0.88
  - Update PAUSE keys to 2022

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.87-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul  4 2020 Paul Howarth <paul@city-fan.org> - 0.87-1
- Update to 0.87
  - Skip 3-verify.t on Crypt::OpenPGP installations

* Sat Jun 27 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-2
- Perl 5.32 re-rebuild updated packages

* Thu Jun 25 2020 Paul Howarth <paul@city-fan.org> - 0.86-1
- Update to 0.86
  - Update PAUSE and ANDK keys to 2020
  - Update documentation pertaining to SHA1
  - Fix compatibility with Crypt::OpenPGP
- Use mktemp to create temporary GPG directory

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-7
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Paul Howarth <paul@city-fan.org> - 0.83-5
- Make perl(PAR::Dist) a suggestion rather than a hard dependency

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.83-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 29 2018 Paul Howarth <paul@city-fan.org> - 0.83-1
- Update to 0.83
  - Update META.yml

* Tue Aug 28 2018 Paul Howarth <paul@city-fan.org> - 0.82-1
- Update to 0.82
  - Fix CRLF handling on Win32
  - Default to SHA256 on new hashes as SHA1 is deprecated

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.81-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.81-5
- Perl 5.26 rebuild

* Wed May 17 2017 Petr Pisar <ppisar@redhat.com> - 0.81-4
- Fix building on Perl without "." in @INC (CPAN RT#120405)

* Wed Apr  5 2017 Paul Howarth <paul@city-fan.org> - 0.81-3
- Use gnupg2 rather than gnupg (#1439089)
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop buildroot cleaning in %%install
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep  5 2016 Paul Howarth <paul@city-fan.org> - 0.81-1
- Update to 0.81
  - Document AUTHOR/MODULE_SIGNATURE_AUTHOR
- BR: perl-generators unconditionally

* Sun Jun 12 2016 Paul Howarth <paul@city-fan.org> - 0.80-1
- Update to 0.80 (build process tweaks)
- BR: perl-generators where available
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.79-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.79-2
- Perl 5.22 rebuild

* Tue May 19 2015 Paul Howarth <paul@city-fan.org> - 0.79-1
- Update to 0.79
  - Restore "cpansign --skip" functionality

* Thu Apr  9 2015 Paul Howarth <paul@city-fan.org> - 0.78-1
- Update to 0.78
  - Fix verify() use from cpanm and CPAN.pm

* Wed Apr  8 2015 Paul Howarth <paul@city-fan.org> - 0.77-1
- Update to 0.77
  - Include the latest public keys of PAUSE, ANDK and AUDREYT
  - Clarify scripts/cpansign copyright to CC0 (#965126, CPAN RT#85466)

* Wed Apr  8 2015 Paul Howarth <paul@city-fan.org> - 0.76-1
- Update to 0.76
  - Fix signature tests by defaulting to verify(skip=>1) when
    $ENV{TEST_SIGNATURE} is true

* Tue Apr  7 2015 Paul Howarth <paul@city-fan.org> - 0.75-1
- Update to 0.75
  - Fix GPG signature parsing logic
  - MANIFEST.SKIP is no longer consulted unless --skip is given
  - Properly use open() modes to avoid injection attacks
  - More protection of @INC from relative paths
- Don't try to run the signature test, which needs the network

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.73-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.73-2
- Perl 5.18 rebuild

* Fri Jun  7 2013 Paul Howarth <paul@city-fan.org> - 0.73-1
- Update to 0.73
  - Constrain the user-specified digest name to /^\w+\d+$/
  - Only allow loading Digest::* from absolute paths in @INC (CVE-2013-2145)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Paul Howarth <paul@city-fan.org> - 0.70-1
- Update to 0.70
  - Don't check gpg version if gpg does not exist

* Fri Nov  2 2012 Paul Howarth <paul@city-fan.org> - 0.69-1
- Update to 0.69
  - Support for gpg under these alternate names: gpg gpg2 gnupg gnupg2
- This release by AUDREYT -> update source URL
- BR:/R: perl(Text::Diff)
- Include Andreas Koenig's GPG key in the SRPM and import it in %%prep so
  that we don't need to get it from a keyserver in %%check

* Thu Nov  1 2012 Petr Pisar <ppisar@redhat.com> - 0.68-7
- Make building non-interactive
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Paul Howarth <paul@city-fan.org> - 0.68-5
- BR: perl(constant), perl(Data::Dumper) and perl(lib)
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.68-4
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.68-3
- BR: perl(Exporter) and perl(ExtUtils::Manifest)
- Use %%{_fixperms} macro rather than our own chmod incantation

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.68-2
- Perl mass rebuild

* Fri May 13 2011 Paul Howarth <paul@city-fan.org> - 0.68-1
- Update to 0.68
  - Fix breakage introduced by 0.67 (CPAN RT#68150)

* Thu Apr 21 2011 Paul Howarth <paul@city-fan.org> - 0.67-3
- Pseudo-merge EPEL-5/EPEL-6/Fedora versions

* Tue Apr 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.67-2
- Appease rpmbuild >= 4.9

* Tue Apr 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.67-1
- Update to 0.67

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.66-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Sep  7 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.66-1
- Update to 0.66 (#630714)

* Tue Sep  7 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.65-1
- Update to 0.65 (#630714)

* Wed Jun 30 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.64-2
- Rebuild

* Sun May  9 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.64-1
- Update to 0.64 (#590385)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-2
- Mass rebuild with perl-5.12.0

* Fri Apr 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.63-1
- Update to 0.63
- Sync with current rpmdevtools spec template

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.61-2
- Rebuild against perl 5.10.1

* Thu Nov 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.61-1
- Update to 0.61 (#538780)

* Tue Nov 17 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.60-1
- Update to 0.60 (#538043); license changed from MIT to CC0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.55-3
- Rebuild for new perl

* Tue Apr 17 2007 Ville Skyttä <ville.skytta@iki.fi> - 0.55-2
- BuildRequire perl(ExtUtils::MakeMaker) and perl(Test::More)

* Tue Aug 22 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.55-1
- 0.55
- Make PAR::Dist dependency a Requires(hint)

* Fri May 12 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.54-1
- 0.54, license changed to MIT

* Wed Feb  1 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.53-1
- 0.53

* Fri Jan 20 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.52-1
- 0.52
- Run non-live tests during build and make live ones optional, enabled
  when building with "--with livetests"

* Mon Jan  2 2006 Ville Skyttä <ville.skytta@iki.fi> - 0.51-1
- 0.51

* Mon Aug 22 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.50-1
- 0.50

* Wed Aug 10 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.45-1
- 0.45

* Thu Apr  7 2005 Ville Skyttä <ville.skytta@iki.fi> - 0.44-2
- Drop Epoch: 0 and 0.fdr. release prefix

* Fri Dec 17 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.44-0.fdr.1
- Update to 0.44

* Sun Nov 21 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.42-0.fdr.1
- Update to 0.42

* Tue Jul  6 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.41-0.fdr.2
- Require perl(Digest::SHA1) (bug 1606)

* Mon Jul  5 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.41-0.fdr.1
- Update to 0.41

* Fri Jul  2 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.40-0.fdr.1
- Update to 0.40

* Fri Jun 18 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.39-0.fdr.1
- Update to 0.39

* Mon May 31 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.4
- Really use pure_install (bug 1606)
- Fix build with older mktemp versions which require a template (bug 1606)

* Mon May 31 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.3
- Fix build in setups which do not generate debug packages (bug 1606)
- Require perl >= 1:5.6.1 for vendor install dir support
- Use pure_install to avoid perllocal.pod workarounds

* Sun Apr 25 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.2
- Require perl(:MODULE_COMPAT_*)

* Sat Mar 27 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:0.38-0.fdr.1
- First build
