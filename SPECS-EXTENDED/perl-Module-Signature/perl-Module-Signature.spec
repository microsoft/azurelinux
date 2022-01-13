Name:           perl-Module-Signature
Version:        0.83
Release:        8%{?dist}
Summary:        CPAN signature management utilities and modules
License:        CC0 and (GPL+ or Artistic)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Module-Signature
Source0:        https://cpan.metacpan.org/modules/by-module/Module/Module-Signature-%{version}.tar.gz#/perl-Module-Signature-%{version}.tar.gz
BuildArch:      noarch
# Module build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(FindBin)
BuildRequires:  perl(inc::Module::Install) >= 0.92
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Install::Can)
BuildRequires:  perl(Module::Install::External)
BuildRequires:  perl(Module::Install::Makefile)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::Scripts)
BuildRequires:  perl(Module::Install::WriteAll)
BuildRequires:  sed
# Module runtime
BuildRequires:  gnupg2
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Text::Diff)
BuildRequires:  perl(version)
# Test suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(lib)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)
# Module runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       gnupg2
Requires:       perl(Digest::SHA)
Requires:       perl(Digest::SHA1)
Requires:       perl(File::Temp)
Requires:       perl(IO::Socket::INET)
Requires:       perl(Text::Diff)
Requires:       perl(version)
Suggests:       perl(PAR::Dist)

%description
This package contains a command line tool and module for checking and creating
SIGNATURE files for Perl CPAN distributions.

%prep
%setup -q -n Module-Signature-%{version}
# Remove bundled modules
rm -r ./inc/*
sed -i -e '/^inc\//d' MANIFEST

# Create a GPG directory for testing, to avoid using ~/.gnupg
mkdir --mode=0700 gnupghome

%build
export GNUPGHOME=$(pwd)/gnupghome
perl Makefile.PL INSTALLDIRS=vendor --skipdeps </dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
export GNUPGHOME=$(pwd)/gnupghome
make test

%files
%license README
%doc AUTHORS Changes *.pub
%{_bindir}/cpansign
%{perl_vendorlib}/Module/
%{_mandir}/man1/cpansign.1*
%{_mandir}/man3/Module::Signature.3*

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.83-8
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.83-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
