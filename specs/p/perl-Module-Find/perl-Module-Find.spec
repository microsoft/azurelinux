# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-Module-Find
Version:	0.17
Release:	2%{?dist}
Summary:	Find and use installed modules in a (sub)category
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Module-Find
Source0:	https://cpan.metacpan.org/modules/by-module/Module/Module-Find-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Pod::Perldoc)
# Module Runtime
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
# Optional Tests
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
# Dependencies
Requires:	perl(Exporter)

%description
Module::Find lets you find and use modules in categories. This can be very
useful for auto-detecting driver or plug-in modules. You can differentiate
between looking in the category itself or in all subcategories.

%prep
%setup -q -n Module-Find-%{version}

# Generate Changes file from POD
perldoc -t Find.pm |
	perl -n -e 'if (/^HISTORY/ ... !/^[[:space:]]/) { print if /^[[:space:]]/ }' > Changes
touch --reference=Find.pm Changes

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
%doc Changes README examples/
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Find.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 17 2025 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Avoid warnings when extracting the distribution tarball, which prevented
    installation under cpanm and other tools (GH#13, CPAN RT#148978)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.16-3
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug  1 2022 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Fix an issue where symlink tests failed on systems that do not support
    creation of symlinks; the issue appears on Windows systems due to changed
    behaviour in File::Find described at:
    https://github.com/Perl/perl5/issues/19995
    Symlink tests were previously skipped if symlink() is not available, and
    now also if creation of a symlink is not possible
  - Fix failing symlink test on Windows
    https://github.com/crenz/Module-Find/issues/9

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-9
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Removed file readability check (GH#4, CPAN RT#99055)
  - Now supports @INC hooks (GH#6)
  - Now filters out filenames starting with a dot (GH#7)
  - Now uses strict (GH#8)
  - Fixed CPAN RT#122016: test/ files show up in metacpan
  - Module::Find now uses @ModuleDirs (if specified) for loading modules
    (CPAN RT#127657); previously, when using setmoduledirs() to set an array
    of directories that did not contain @INC, Module::Find would find the
    modules correctly, but load them from @INC

* Wed Sep 25 2019 Paul Howarth <paul@city-fan.org> - 0.13-15
- Spec tidy-up
  - Use author-independent source URL
  - Specify all build dependencies
  - Keep timestamp of Changes file constant
  - Drop redundant buildroot cleaning in %%install section
  - Simplify find command using -delete

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-13
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-10
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-2
- Perl 5.22 rebuild

* Tue Mar 10 2015 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Link to Module::Pluggable and Class::Factory::Util in "SEE ALSO"
  - Align package name parsing with how perl does it (allowing single quotes
    as module separator)
- Classify buildreqs by usage

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb  7 2014 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Fixed CPAN RT#81077: useall fails in taint mode
  - Fixed CPAN RT#83596: Documentation doesn't describe behaviour if a module
    fails to load
  - Clarified documentation for useall and usesub
  - Fixed CPAN RT#62923: setmoduledirs(undef) doesn't reset to searching @INC
  - Added more explicit tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.11-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 0.11-4
- Add some missing dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.16 rebuild

* Tue May 22 2012 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11:
  - defined(@array) is deprecated under Perl 5.15.7 (CPAN RT#74251)
- Don't need to remove empty directories from buildroot
- Drop %%defattr, redundant since rpm 4.4

* Wed Jan 25 2012 Paul Howarth <paul@city-fan.org> - 0.10-4
- BR: perl(ExtUtils::MakeMaker), perl(File::Find), perl(File::Spec) and
  perl(Pod::Perldoc)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use search.cpan.org source URL
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10-2
- Perl mass rebuild

* Tue Mar 15 2011 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10:
  - Fixed META.yml generation (CPAN RT#38302)
  - Removed Unicode BOM from Find.pm (CPAN RT#55010)
- Generate Changes file from POD in Find.pm

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-2
- Rebuild against perl 5.10.1

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- Update to 0.06
- Add examples/

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-2
- Rebuild for new perl

* Tue Dec 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-1
- First build
