# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# noarch, but to avoid *.list files interfering with signature test
%global debug_package %{nil}

# Similarly, for package note feature
%undefine _package_note_file

# Store keys in a temp directory
%global gnupghome %(mktemp --directory)

Name:           perl-Test-Signature
Version:        1.11
Release:        35%{?dist}
Summary:        Automated SIGNATURE testing
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Signature
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Signature-%{version}.tar.gz
# Audrey Tang's public key (3C3501A0), from the Module::Signature 0.61 distribution
Source1:        AUDREY2006.pub
# Petr Pisar's public key (4B528393E6A3B0DFB2EF3A6412C9C5C767C6FAA2)
Source2:        ppisar2011.pub
Patch0:         Test-Signature-1.11-Fix-building-on-Perl-without-.-in-INC.patch 
Patch1:         Test-Signature-1.11-Resign-patched-code.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# Dependencies of bundled Module::Install
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
# Module Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Signature)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(Test::More)
# Optional Tests
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Test::Pod) >= 0.95
# Dependencies
# Package just skips (or, optionally, fails) testing if Module::Signature not installed
Requires:       perl(Module::Signature)
# Likewise, needs Socket to connect to keyserver
Requires:       perl(Socket)

%description
Module::Signature allows you to verify that a distribution has not been
tampered with. Test::Signature lets that be tested as part of the
distribution's test suite.

%prep
%setup -q -n Test-Signature-%{version}

# Fix building on Perl without "." in @INC (CPAN RT#121760)
%patch -P 0 -p1
# Required to pass tests after patching
%patch -P 1 -p1

# Import upstream's GPG key so we don't need to fetch it from a keyserver
# when running the signature test
export GNUPGHOME=%{gnupghome}
gpg2 --import %{SOURCE1}
gpg2 --import %{SOURCE2}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
export GNUPGHOME=%{gnupghome}
make test

%clean
rm -rf %{buildroot} %{gnupghome}

%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Signature.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-27
- Perl 5.36 rebuild

* Fri Mar 11 2022 Paul Howarth <paul@city-fan.org> - 1.11-26
- Work around FTBFS triggered by package note feature

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-23
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 10 2020 Paul Howarth <paul@city-fan.org> - 1.11-21
- Use author-independent source URL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-19
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-16
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-13
- Perl 5.28 rebuild

* Thu Apr  5 2018 Paul Howarth <paul@city-fan.org> - 1.11-12
- Use mktemp to create GNUPGHOME, simplifying build process

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-9
- Perl 5.26 rebuild

* Thu May 18 2017 Petr Pisar <ppisar@redhat.com> - 1.11-8
- Fix building on Perl without "." in @INC (CPAN RT#121760)

* Thu Apr  6 2017 Paul Howarth <paul@city-fan.org> - 1.11-7
- Use gnupg2 rather than gnupg (#1439206)
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop buildroot cleaning in %%install
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.22 rebuild

* Wed Apr  8 2015 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Compatibility with Module::Signature 0.75+
- Classify buildreqs by usage
- Don't use macros for commands
- Avoid clobbering ~/.gnupg for local builds
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Import upstream's GPG key in %%prep so we don't need to fetch it from a
  keyserver when running the signature test

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-18
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.10-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.10-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-10
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.10-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 07 2008 Iain Arnell <iarnell@gmail.com> 1.10-2
- remove explicit requires

* Fri Dec 05 2008 Iain Arnell 1.10-1
- Specfile autogenerated by cpanspec 1.77.
