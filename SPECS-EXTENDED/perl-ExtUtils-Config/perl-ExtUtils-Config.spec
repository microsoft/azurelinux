Name:		perl-ExtUtils-Config
Version:	0.010
Release:	1%{?dist}
Summary:	A wrapper for perl's configuration
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://metacpan.org/release/ExtUtils-Config
Source0:	https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-Config-%{version}.tar.gz#/perl-ExtUtils-Config-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Config)
BuildRequires:	perl(Data::Dumper)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More) >= 0.88
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
ExtUtils::Config is an abstraction around the %%Config hash.

%prep
%setup -q -n ExtUtils-Config-%{version}

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
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::Config.3*
%{_mandir}/man3/ExtUtils::Config::MakeMaker.3*

%changelog
* Thu Dec 19 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.010-1
- Update to 0.010
- License verified

* Fri Apr 22 2022 Muhammad Falak <mwani@microsoft.com> - 0.008-19
- Add an explicit BR on `perl(blib)` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.008-18
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Fri Aug 23 2019 Paul Howarth <paul@city-fan.org> - 0.008-17
- Use an author-independent source URL

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-15
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Paul Howarth <paul@city-fan.org> - 0.008-13
- Specify all build dependencies
- Simplify find command using -delete
- Use %%license where possible
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section
  - Drop workaround for building with Test::More < 0.88

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-8
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-3
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-2
- Perl 5.20 rebuild

* Thu Jun 26 2014 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Remove set, clear, clone methods
- Don't bother with the release tests, which can't be run on EPEL < 7 anyway
- Update patch for building with old Test::More versions

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.007-7
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.007-5
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 0.007-4
- Avoid Test::Kwalitee as it tries to verify the module's signature, which will fail
  if we have to patch Makefile.PL, tests etc. for old distribution support

* Fri Jul  5 2013 Paul Howarth <paul@city-fan.org> - 0.007-3
- Don't BR: perl(Test::Kwalitee) when bootstrapping

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.007-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Initial RPM version
