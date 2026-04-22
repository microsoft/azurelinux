# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		perl-File-Copy-Recursive-Reduced
Version:	0.008
Release: 5%{?dist}
Summary:	Recursive copying of files and directories within Perl 5 toolchain
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/File-Copy-Recursive-Reduced
Source0:	https://cpan.metacpan.org/modules/by-module/File/File-Copy-Recursive-Reduced-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Capture::Tiny)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(lib)
BuildRequires:	perl(Path::Tiny)
BuildRequires:	perl(Test::More) >= 0.44
# Dependencies
# (none)

%description
This library is intended as a not-quite-drop-in replacement for certain
functionality provided by CPAN distribution File-Copy-Recursive. The library
provides methods similar enough to that distribution's fcopy() and dircopy()
functions to be usable in those CPAN distributions often described as being
part of the Perl toolchain.

%prep
%setup -q -n File-Copy-Recursive-Reduced-%{version}

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
%license LICENSE
%doc Changes README Todo
%{perl_vendorlib}/File/
%{_mandir}/man3/File::Copy::Recursive::Reduced.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 25 2024 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Encoding directive added to POD
  - Corrections in test files to guard against CPANtesters who run tests with
    PERL_AUTHOR_TESTING turned on

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 16 2023 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Corrections in tests to better accommodate Windows path separators

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.006-17
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-14
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-8
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.006-2
- Perl 5.28 rebuild

* Tue Apr 24 2018 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - File::Copy::Recursive 0.41 has been released to CPAN and addresses the
    problem which was the focus of File::Copy::Recursive::Reduced; Hence, FCR2
    is now feature-complete

* Fri Apr 20 2018 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005
  - Introduce rcopy(), a stripped-down replacement for
    File::Copy::Recursive::rcopy()
  - Implement copying of symlinks within all three public functions; at this
    point we should be able to make substitutions for File::Copy::Recursive's
    fcopy(), dircopy() and rcopy() functions in a large proportion of toolchain
    libraries, particularly in test suites

* Wed Apr 18 2018 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
