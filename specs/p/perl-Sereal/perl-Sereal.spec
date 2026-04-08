# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Sereal_enables_optional_test
%else
%bcond_with perl_Sereal_enables_optional_test
%endif

Name:           perl-Sereal
Version:        5.004
Release:        7%{?dist}
Summary:        Fast, compact, powerful binary (de-)serialization
# Makefile.PL defines LICENSE
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Sereal
Source0:        https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-%{version}.tar.gz
BuildArch:      noarch
# Build:
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
# blib not used
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
# Devel::CheckLib not used
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# File::Find not used
# File::Path not used
# File::Spec not used
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Sereal::Decoder) >= %{version}
BuildRequires:  perl(Sereal::Encoder) >= %{version}
# Tests:
# Benchmark not used
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
# Hash::Util is needed on perl >= 5.25. It's in an eval to proceed to
# num_buckets() definition with older perls.
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(integer)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sereal::Decoder::Constants)
BuildRequires:  perl(Sereal::Encoder::Constants)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::LongString)
BuildRequires:  perl(Test::MemoryGrowth)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::Scalar)
# Time::HiRes not used
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(utf8)
BuildRequires:  perl(version)
%if %{with perl_Sereal_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Test::Deep) >= 0.110
BuildRequires:  perl(Test::Deep::NoTest)
%endif

%description
Sereal is an efficient, compact-output, binary and feature-rich serialization
protocol. The Perl encoder is implemented as the Sereal::Encoder module, the
Perl decoder correspondingly as Sereal::Decoder. This Sereal module is a very
thin wrapper around both Sereal::Encoder and Sereal::Decoder. It depends on
both and loads both.

%prep
%setup -q -n Sereal-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Sereal.pm
%{_mandir}/man3/Sereal.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 19 2023 Paul Howarth <paul@city-fan.org> - 5.004-1
- Update to 5.004 (rhbz#2188044)
  - Decoder fixes: fix thaw ordering for frozen objects - nested THAW
    operations now happen in the documented LIFO order (GH#283, GH#285)

* Wed Feb  8 2023 Paul Howarth <paul@city-fan.org> - 5.003-1
- Update to 5.003 (rhbz#2168014)
  - Update Miniz to 3.0.2, Zstd to 1.5.2 and Devel::CheckLib to 1.16
    (note: this package uses the system versions of these)
  - Assorted build fixes related to these updates
  - OpenBSD build fixes

* Wed Feb  1 2023 Paul Howarth <paul@city-fan.org> - 5.002-1
- Update to 5.002 (rhbz#2166279)
  - Fix up Decoder tests to run on perl 5.8, which has no defined-or
  - Ensure that Encoder depends on the correct version of the Decoder
  - Test compatibility fixes when no perl is already installed
  - Add t/195_backcompat.t to check if the latest decoder will seamlessly
    handle reading output from older versions
  - Test compatibility fixes with version 3 and earlier

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Sep  4 2022 Paul Howarth <paul@city-fan.org> - 5.001-1
- Update to 5.001
  - First official release of protocol 5
    - Better support for non-standard NV types
    - Support for the new Perl 5.36 bools
- Use SPDX-format license tag

* Thu Jul 28 2022 Paul Howarth <paul@city-fan.org> - 4.025-1
- Update to 4.025
  - Changes to the FREEZE/THAW mechanism
    - Remove the part that says that FREEZE cannot return a list; it can, and
      we have supported it for a very long time, although I have not checked
      how far back this support goes
    - If you use the FREEZE/THAW API's you should upgrade to this version or
      later
  - Test fixes for t/020_sort_keys.t hanging on some perls that do not come
    bundled with Hash::Util

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.023-2
- Perl 5.36 rebuild

* Sun Feb 20 2022 Paul Howarth <paul@city-fan.org> - 4.023-1
- Update to 4.023
  - Bump encoder and decoder dependencies to 4.023

* Sat Feb 19 2022 Paul Howarth <paul@city-fan.org> - 4.022-1
- Update to 4.022
  - Bump encoder and decoder dependencies to 4.022

* Fri Feb 18 2022 Paul Howarth <paul@city-fan.org> - 4.021-1
- Update to 4.021
  - Bump encoder and decoder dependencies to 4.021

* Thu Feb 17 2022 Paul Howarth <paul@city-fan.org> - 4.020-1
- Update to 4.020
  - Bump encoder and decoder dependencies to 4.020

* Mon Feb  7 2022 Paul Howarth <paul@city-fan.org> - 4.019-1
- Update to 4.019
  - Fix build issue with latest perl
  - Bump encoder and decoder dependencies to 4.019
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.018-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.018-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.018-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Petr Pisar <ppisar@redhat.com> - 4.018-1
- 4.018 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Petr Pisar <ppisar@redhat.com> - 4.017-1
- 4.017 bump

* Wed Jul 08 2020 Petr Pisar <ppisar@redhat.com> - 4.015-1
- 4.015 bump

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.014-2
- Perl 5.32 rebuild

* Mon Jun 15 2020 Petr Pisar <ppisar@redhat.com> - 4.014-1
- 4.014 bump

* Thu Jun 11 2020 Petr Pisar <ppisar@redhat.com> - 4.012-1
- 4.012 bump

* Tue Feb 04 2020 Petr Pisar <ppisar@redhat.com> - 4.011-1
- 4.011 bump

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 4.009-2
- Build-require Hash::Util needed for tests

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 4.009-1
- 4.009 bump

* Thu Jan 30 2020 Petr Pisar <ppisar@redhat.com> - 4.008-1
- 4.008 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.007-2
- Perl 5.30 rebuild

* Wed Apr 10 2019 Petr Pisar <ppisar@redhat.com> - 4.007-1
- 4.007 bump

* Tue Apr 09 2019 Petr Pisar <ppisar@redhat.com> - 4.006-1
- 4.006 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.005-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.005-1
- 4.005 bump

* Tue Nov 14 2017 Petr Pisar <ppisar@redhat.com> - 4.004-1
- 4.004 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.015-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 05 2016 Petr Pisar <ppisar@redhat.com> - 3.015-1
- 3.015 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.014-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Petr Pisar <ppisar@redhat.com> - 3.014-1
- 3.014 bump

* Wed Dec 02 2015 Petr Pisar <ppisar@redhat.com> - 3.009-1
- 3.009 bump

* Mon Nov 30 2015 Petr Pisar <ppisar@redhat.com> - 3.008-1
- 3.008 bump

* Fri Nov 27 2015 Petr Pisar <ppisar@redhat.com> - 3.007-1
- 3.007 bump

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 3.006-1
- 3.006 bump

* Tue Sep 29 2015 Petr Pisar <ppisar@redhat.com> 3.005-1
- Specfile autogenerated by cpanspec 1.78.
