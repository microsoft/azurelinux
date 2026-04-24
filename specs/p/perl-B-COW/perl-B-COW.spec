# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-B-COW
Version:	0.007
Release: 12%{?dist}
Summary:	Additional B helpers to check Copy On Write status
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/B-COW
Source0:	https://cpan.metacpan.org/modules/by-module/B/B-COW-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(Devel::Peek)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::More) >= 0.88
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
# Runtime

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
B::COW provides some naïve additional B helpers to check the Copy On Write
(COW) status of one SvPV (a Perl string variable).

A COWed SvPV is sharing its string (the PV) with other SvPVs. It's a (kind of)
Read Only C string, which would be Copied On Write (COW). More than one SV can
share the same PV, but when one PV needs to alter it, it would perform a copy
of it, decreasing the COWREFCNT counter. One SV can then drop the COW flag when
it's the only one holding a pointer to the PV. The COWREFCNT is stored at the
end of the PV, after the null byte terminating the string. That value is
limited to 255: when we reach 255, a new PV would be created.

%prep
%setup -q -n B-COW-%{version}

%build
perl Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{optflags}" \
	NO_PACKLIST=1 \
	NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes examples/ README
%{perl_vendorarch}/auto/B/
%{perl_vendorarch}/B/
%{_mandir}/man3/B::COW.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-10
- Perl 5.42 rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-7
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-3
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 21 2022 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Advertise XSLoader dependency in metadata

* Tue Oct 18 2022 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Disable prototypes to silence warning

* Sat Oct 15 2022 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005
  - Add version to Test::More use to ensure correct version
  - Remove useless MIN_PERL_VERSION_FOR_COW
  - Update CI workflow
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-9
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-6
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.004-3
- Perl 5.32 rebuild

* Fri Apr 24 2020 Paul Howarth <paul@city-fan.org> - 0.004-2
- Use %%{make_build} and %%{make_install}

* Fri Apr 24 2020 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004
  - Fix CowREFCNT issues on big endian

* Tue Apr 21 2020 Paul Howarth <paul@city-fan.org> - 0.003-2
- Sanitize for Fedora submission

* Tue Apr 21 2020 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
