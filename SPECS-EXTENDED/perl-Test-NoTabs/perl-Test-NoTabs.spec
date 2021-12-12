Name:		perl-Test-NoTabs
Version:	2.02
Release:	9%{?dist}
Summary:	Check the presence of tabs in your project
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Test-NoTabs
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Test-NoTabs-%{version}.tar.gz#/perl-Test-NoTabs-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Optional Tests
%if "%{?rhel}" != "6"
BuildRequires:	perl(CPAN::Meta) >= 2.120900
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module scans your project/distribution for any perl files (scripts,
modules, etc.) for the presence of tabs.

%prep
%setup -q -n Test-NoTabs-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::NoTabs.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Paul Howarth <paul@city-fan.org> - 2.02-7
- Use author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-2
- Perl 5.28 rebuild

* Tue Apr 24 2018 Paul Howarth <paul@city-fan.org> - 2.02-1
- Update to 2.02
  - Altered a test to not bake @INC into -I options for a subprocess, to avoid
    too-long commands

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-2
- Perl 5.26 rebuild

* Wed Apr 12 2017 Paul Howarth <paul@city-fan.org> - 2.00-1
- Update to 2.00
  - Migrated off Module::Install, added META.json and other modern tooling
- This release by ETHER → update source URL
- Ship new LICENSE file
- Simplify find command using -delete
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.4-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.4-2
- Perl 5.22 rebuild

* Thu Jan 29 2015 Paul Howarth <paul@city-fan.org> - 1.4-1
- Update to 1.4
  - Removed boilerplate section "EXPORT" from pod (CPAN RT#96937)
  - Tightened checking for pod lines (CPAN RT#95747)
- Classify buildreqs by usage
- BR: tar > 1.15.1, which can't unpack tarballs with unknown extended
  attributes without generating a non-zero exit code

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.3-7
- Perl 5.18 rebuild

* Sun Jul  7 2013 Paul Howarth <paul@city-fan.org> - 1.3-6
- Revert unbundling of Module::Install*, which causes numerous bootstrap build
  dependency cycles

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.3-4
- Remove BR: perl(ExtUtils::MakeMaker)
- Replace bundled modules Module::Install* by BR perl(inc::Module::Install)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.3-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Paul Howarth <paul@city-fan.org> - 1.3-1
- Update to 1.3
  - Fix regex to ignore '.svn', but not 'Xsvn' - unescaped

* Sun Jun 17 2012  Paul Howarth <paul@city-fan.org> - 1.2-1
- Update to 1.2
  - Fix to ignore inc/ for Module::Install
- BR: perl(Cwd), perl(ExtUtils::MakeMaker), perl(File::Spec), perl(File::Temp)
  and perl(Test::Builder)
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.1-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1-2
- Perl mass rebuild

* Fri Apr 29 2011 Paul Howarth <paul@city-fan.org> 1.1-1
- Update to 1.1
  - Fix test fails if cwd or perl has a space in its path (CPAN RT#67376)
- Remove remaining uses of macros for commands

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> 1.0-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Wed Jun 16 2010 Paul Howarth <paul@city-fan.org> 1.0-3
- Clean up for Fedora submission

* Mon May 17 2010 Paul Howarth <paul@city-fan.org> 1.0-2
- Fix dist tag for RHEL-6 Beta

* Thu Feb 11 2010 Paul Howarth <paul@city-fan.org> 1.0-1
- Update to 1.0 (patches upstreamed)

* Wed Feb 10 2010 Paul Howarth <paul@city-fan.org> 0.9-2
- Add patch and test case for CPAN RT#53727 (broken POD breaks tab detection)
- Fix a `Parentheses missing around "my" list' warning in old Perls (RT#54477)

* Mon Feb  1 2010 Paul Howarth <paul@city-fan.org> 0.9-1
- Initial RPM version
