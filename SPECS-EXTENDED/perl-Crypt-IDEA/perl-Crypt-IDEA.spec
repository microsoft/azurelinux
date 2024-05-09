Summary:	Perl interface to IDEA block cipher
Name:		perl-Crypt-IDEA
Version:	1.10
Release:	18%{?dist}
License:	BSD with advertising
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/Crypt-IDEA
Source0:	https://cpan.metacpan.org/modules/by-module/Crypt/Crypt-IDEA-%{version}.tar.gz#/perl-Crypt-IDEA-%{version}.tar.gz
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	sed
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
# Test Suite
BuildRequires:	perl(Test::More)
# Dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't provide private perl libs
%{?perl_default_filter}

%description
This perl extension is an implementation of the IDEA block cipher algorithm.
The module implements the Crypt::BlockCipher interface.

This implementation is copyright Systemics Ltd (https://www.systemics.com/).

%prep
%setup -q -n Crypt-IDEA-%{version}

# Remove unnecessary shellbang that points to the wrong perl interpreter anyway
sed -i -e '\|^#! */usr/local/bin/perl |d' IDEA.pm

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license COPYRIGHT
%else
%doc COPYRIGHT
%endif
%doc changes
%{perl_vendorarch}/Crypt/
%{perl_vendorarch}/auto/Crypt/
%{_mandir}/man3/Crypt::IDEA.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-12
- Perl 5.28 rebuild

* Tue Feb 20 2018 Paul Howarth <paul@city-fan.org> - 1.10-11
- BR: gcc
- Remove some legacy cruft
  - Drop BuildRoot: and Group: tags
  - Drop explicit %%clean section
  - Drop explicit buildroot cleaning in %%install section

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Paul Howarth <paul@city-fan.org> - 1.10-5
- IDEA patent expired, import from RPM Fusion

* Tue Jul 26 2016 Paul Howarth <paul@city-fan.org> - 1.10-4
- BR: perl-devel

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 1.10-3
- Classify buildreqs by usage
- Simplify find commands using -empty and -delete
- Use %%license where possible

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug  4 2013 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10
  - Made SvUPGRADE a statement
  - Corrected VERSION statement
  - Fixed _idea.c for Strawberry

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.08-11
- Mass rebuilt for Fedora 19 Features

* Tue Jul 17 2012 Paul Howarth <paul@city-fan.org> - 1.08-10
- Perl 5.16 rebuild
- Drop BR: perl(DynaLoader) - not dual-lived

* Wed May  2 2012 Paul Howarth <paul@city-fan.org> - 1.08-9
- Spec clean-up:
  - Don't need to remove empty directories from buildroot
  - Drop %%defattr, redundant since rpm 4.4

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 1.08-8
- Spec clean-up:
  - Don't use macros for commands
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - One buildreq per line
  - Add buildreqs for Perl core modules that might be dual-lived

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.08-6
- Rebuilt for perl

* Tue Aug 24 2010 Paul Howarth <paul@city-fan.org> 1.08-5
- Rebuild for Perl 5.12.1

* Wed Feb  3 2010 Paul Howarth <paul@city-fan.org> 1.08-4
- Rebuild for Perl 5.10.1
- Filter bogus provides for shared objects

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.08-3
- Rebuild for new F11 features

* Wed Jan 21 2009 Paul Howarth <paul@city-fan.org> 1.08-2
- Include "changes" file in documentation
- Use a different delimiter for sed command in %%prep to improve readability

* Thu Nov 27 2008 Paul Howarth <paul@city-fan.org> 1.08-1
- Update to 1.08
- Clean up for submission to RPM Fusion
  (https://bugzilla.rpmfusion.org/show_bug.cgi?id=195)

* Fri Dec  2 2005 Paul Howarth <paul@city-fan.org> 1.02-1
- Initial build
