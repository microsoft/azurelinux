Name:           perl-Import-Into
Version:        1.002005
Release:        15%{?dist}
Summary:        Import packages into other packages
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Import-Into
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Import-Into-%{version}.tar.gz#/perl-Import-Into-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Module Runtime
BuildRequires:  perl(Module::Runtime)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
Loading Import::Into creates a global method import::into which you can call on
any package to import it into another package.

%prep
%setup -q -n Import-Into-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor --skipdeps NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Import/
%{_mandir}/man3/Import::Into.3*

%changelog
* Thu Aug 22 2024 Neha Agarwal <nehaagrwal@microsoft.com> - 1.002005-15
- Promote package to Core repository.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.002005-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.002005-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.002005-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.002005-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.002005-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.002005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 28 2015 Petr Šabata <contyk@redhat.com> - 1.002005-1
- 1.002005 bump
- Update source URL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.002004-2
- Perl 5.22 rebuild

* Thu Nov 13 2014 Paul Howarth <paul@city-fan.org> - 1.002004-1
- Update to 1.002004
  - Module loading is now done while importing, making it unnecessary to load
    them beforehand (CPAN RT#96995)
  - Fix prerequisite declarations for older toolchain

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.002002-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  7 2014 Paul Howarth <paul@city-fan.org> - 1.002002-1
- Update to 1.002002
  - Minor metadata updates
- This release by ETHER -> update source URL
- Classify buildreqs by usage

* Wed Mar 12 2014 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001
  - Allow specifying by caller level, as well as specifying file, line, and
    version
  - Fix tests and Makefile.PL to support perl 5.6
- This release by HAARG -> update source URL
- Specify all dependencies
- Make %%files list more explicit

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.001001-2
- Perl 5.18 rebuild

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.001001-1
- update to latest upstream version

* Sat Feb 16 2013 Iain Arnell <iarnell@gmail.com> 1.001000-1
- Specfile autogenerated by cpanspec 1.79.
