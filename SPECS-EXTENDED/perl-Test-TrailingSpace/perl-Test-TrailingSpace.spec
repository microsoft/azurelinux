Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Test-TrailingSpace
Version:        0.0601
Release:        11%{?dist}
Summary:        Test for trailing space in source files
License:        MIT
URL:            https://metacpan.org/release/Test-TrailingSpace
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-TrailingSpace-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14.0
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(autodie)
BuildRequires:  perl(File::Find::Object::Rule) >= 0.0301
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::TreeCreate)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::Builder::Tester)
# Dependencies:
# (none)

%description
This module is used to test for presence of trailing space.

%prep
%setup -qn Test-TrailingSpace-%{version}

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
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::TrailingSpace.3*

%changelog
* Tue Apr 08 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.0601-11
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 29 2023 Paul Howarth <paul@city-fan.org> - 0.0601-6
- SPDX migration

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.0601-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 27 2021 Paul Howarth <paul@city-fan.org> - 0.0601-1
- Update to 0.0601
  - Split File::TreeCreate off to its own distribution

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0600-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.0600-5
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0600-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0600-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.0600-2
- Perl 5.32 rebuild

* Sun Jun  7 2020 Paul Howarth <paul@city-fan.org> - 0.0600-1
- Update to 0.0600
  - Avoid excessive callback calls by having the _path_cb take the $rule
    object (optimization)

* Sun Jun  7 2020 Paul Howarth <paul@city-fan.org> - 0.0501-1
- Update to 0.0501
  - Try to fix t/dogfood.t tests failures on MS Windows

* Fri Jun  5 2020 Paul Howarth <paul@city-fan.org> - 0.0500-1
- Update to 0.0500
  - Convert the file processing to use a code generated callback (a speed
    optimization)

* Wed May 20 2020 Paul Howarth <paul@city-fan.org> - 0.0400-1
- Update to 0.0400
  - Add the 'find_cr' and 'find_tabs' options
- Module now requires Perl 5.14

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.0302-3
- BR: perl(blib) for t/00-compile.t

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0302-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 0.0302-1
- Update to 0.0302
  - Now at https://github.com/shlomif/perl-test-trailingspace
  - Convert to https://metacpan.org/pod/Dist::Zilla::PluginBundle::SHLOMIF
- Switch to ExtUtils::MakeMaker flow

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.0301-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.0301-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.0301-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov  2 2016 Paul Howarth <paul@city-fan.org> - 0.0301-1
- Update to 0.0301
  - Skip "sample-data" in t/dogfood.t, which caused problems with parallel
    testing

* Thu May 19 2016 Paul Howarth <paul@city-fan.org> - 0.0300-1
- Update to 0.0300
  - Made abs_path_prune_re affect files as well; this way one can skip files
    with offending extensions
- BR: perl-generators

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.0205-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 09 2015 Petr Pisar <ppisar@redhat.com> - 0.0205-1
- 0.0205 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0204-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0204-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0204-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Christopher Meng <rpm@cicku.me> - 0.0204-1
- Update to 0.0204

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.0203-1
- Initial Package.
