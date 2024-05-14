Name:		perl-Devel-GlobalDestruction-XS
Version:	0.03
Release:	13%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	Faster implementation of the Devel::GlobalDestruction API
URL:		https://metacpan.org/release/Devel-GlobalDestruction-XS
Source0:	https://cpan.metacpan.org/authors/id/H/HA/HAARG/Devel-GlobalDestruction-XS-%{version}.tar.gz
# Build (perl-devel split from main perl package at F-7)
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)

BuildRequires:	perl-devel

BuildRequires:	perl-generators
# Module
BuildRequires:	perl(XSLoader)
# Test suite
BuildRequires:	perl(threads)
BuildRequires:	perl(threads::shared)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This is an XS backend for Devel::GlobalDestruction and should be used through
that module.

%prep
%setup -q -n Devel-GlobalDestruction-XS-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Devel/
%{perl_vendorarch}/Devel/
%{_mandir}/man3/Devel::GlobalDestruction::XS.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.03-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  1 2016 Paul Howarth <paul@city-fan.org> - 0.03-1
- Update to 0.03
  - Stop relying on . being in @INC
- Simplify find commands using -empty and -delete

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.02-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Paul Howarth <paul@city-fan.org> - 0.02-1
- Update to 0.02
  - Update metadata to include IRC and repository web link
  - Remove unneeded prerequisite on ExtUtils::CBuilder
- This release by HAARG → update source URL
- Explicitly BR: perl-devel, needed for EXTERN.h

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.01-9
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.01-8
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.01-4
- Perl 5.18 rebuild

* Tue Apr  9 2013 Paul Howarth <paul@city-fan.org> - 0.01-3
- Drop redundant explicit dependency on perl(XSLoader) (#928418)

* Wed Mar 27 2013 Paul Howarth <paul@city-fan.org> - 0.01-2
- Sanitize for Fedora submission

* Wed Mar 27 2013 Paul Howarth <paul@city-fan.org> - 0.01-1
- Initial RPM version
