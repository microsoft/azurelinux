# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optinal tests
%bcond_without perl_Sereal_Decoder_enables_optional_test

Name:           perl-Sereal-Decoder
Version:        5.004
Release: 17%{?dist}
Summary:        Perl deserialization for Sereal format
# lib/Sereal/Decoder.pm:    GPL+ or Artistic
## Unbundled:
# miniz.c:                  MIT and Unlicense
# snappy:                   BSD
# zstd/decompress/zstd_decompress.c:    GPLv2 or BSD
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Sereal-Decoder
Source0:        https://cpan.metacpan.org/authors/id/Y/YV/YVES/Sereal-Decoder-%{version}.tar.gz
Patch0:         Sereal-Decoder-5.004-external-miniz.patch
# Build
BuildRequires:  coreutils
BuildRequires:  csnappy-devel
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libzstd-devel
BuildRequires:  make
BuildRequires:  miniz-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Devel::CheckLib) >= 1.16
BuildRequires:  perl(ExtUtils::MakeMaker) >= 7.0
# File::Find not used
# File::Path not used in inc/Sereal/BuildTools.pm
# File::Spec not used in inc/Sereal/BuildTools.pm
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests:
# Benchmark not used
BuildRequires:  perl(blib)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(integer)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::LongString)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(threads)
# Time::HiRes not used
BuildRequires:  perl(utf8)
%if %{with perl_Sereal_Decoder_enables_optional_test}
# Optional tests:
BuildRequires:  perl(Hash::Util)
BuildRequires:  perl(Test::MemoryGrowth)
%if !%{defined perl_bootstrap}
# Some tests require Sereal::Encoder 3.005003, but most of them do not require
# exact version. Thus do not constrain the version here.
BuildRequires:  perl(Sereal::Encoder)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::Scalar)
%endif
%endif

%description
This library implements a deserializer for an efficient, compact-output,
and feature-rich binary protocol called Sereal.

%prep
%setup -q -n Sereal-Decoder-%{version}

# Fix detection of miniz 3.1.0
%patch -P0

# Remove bundled Perl modules
rm -r ./inc/Devel
perl -i -ne 'print $_ unless m{^inc/Devel/}' MANIFEST
# Remove bundled csnappy
rm -r ./snappy
perl -i -ne 'print $_ unless m{^snappy/}' MANIFEST
# Remove bundled miniz
rm miniz.*
perl -i -ne 'print $_ unless m{^miniz\.}' MANIFEST
# Remove bundled zstd
rm -r zstd
perl -i -ne 'print $_ unless m{^zstd/}' MANIFEST

%build
unset DEBUG SEREAL_USE_BUNDLED_LIBS SEREAL_USE_BUNDLED_CSNAPPY \
    SEREAL_USE_BUNDLED_MINIZ SEREAL_USE_BUNDLED_ZSTD
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}" INC="$(pkg-config --cflags miniz)"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%doc Changes
%{perl_vendorarch}/auto/Sereal/
%{perl_vendorarch}/Sereal/
%{_mandir}/man3/Sereal::Decoder.3*
%{_mandir}/man3/Sereal::Performance.3*

%changelog
* Mon Sep 22 2025 Paul Howarth <paul@city-fan.org> - 5.004-16
- Fix detection of miniz 3.1.0

* Sun Aug 03 2025 Dominik Mierzejewski <dominik@greysector.net> - 5.004-15
- Rebuild after bootstrapping

* Sat Aug 02 2025 Dominik Mierzejewski <dominik@greysector.net> - 5.004-14
- Rebuild and bootstrap for miniz SONAME bump (and fix include path)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-12
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-11
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-8
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-7
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-3
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.004-2
- Perl 5.38 rebuild

* Wed Apr 19 2023 Paul Howarth <paul@city-fan.org> - 5.004-1
- Update to 5.004 (rhbz#2188045)
  - Fix thaw ordering for frozen objects: nested THAW operations now happen in
    the documented LIFO order (GH#283, GH#285)

* Wed Feb  8 2023 Paul Howarth <paul@city-fan.org> - 5.003-1
- Update to 5.003 (rhbz#2168015)
  - Update Miniz to 3.0.2, Zstd to 1.5.2 and Devel::CheckLib to 1.16
    (note: in this package we use the system versions of these)
  - Assorted build fixes related to these updates
  - OpenBSD build fixes

* Wed Feb  1 2023 Paul Howarth <paul@city-fan.org> - 5.002-1
- Update to 5.002 (rhbz#2166280)
  - Test compatibility fixes with version 3 and earlier
  - Test compatibility fixes when no perl is already installed
  - Add t/195_backcompat.t to check if the latest decoder will seamlessly
    handle reading output from older versions
  - Ensure that Encoder depends on the correct version of the Decoder
  - Fix up Decoder tests to run on perl 5.8, which has no defined-or

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Petr Pisar <ppisar@redhat.com> - 5.001-3
- Finish bootstrapping against miniz-3.0.0 (bug #2137798)

* Tue Nov 01 2022 Petr Pisar <ppisar@redhat.com> - 5.001-2
- Rebuild against miniz-3.0.0 (bug #2137798)

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
    - If you use the FREEZE/THAW API's you should upgrade to this version
  - Test fixes for t/020_sort_keys.t hanging on some perls that do not come
    bundled with Hash::Util

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.023-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.023-3
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.023-2
- Perl 5.36 rebuild

* Sun Feb 20 2022 Paul Howarth <paul@city-fan.org> - 4.023-1
- Update to 4.023
  - Make it possible to upgrade with passing tests when using
    Sereal::Decoder 4.015-4.019 on threaded debugging perls

* Sat Feb 19 2022 Paul Howarth <paul@city-fan.org> - 4.022-1
- Update to 4.022
  - Better logic to make it possible to upgrade with passing tests when using
    Sereal::Decoder 4.019 on threaded debugging perls

* Fri Feb 18 2022 Paul Howarth <paul@city-fan.org> - 4.021-1
- Update to 4.021
  - Make it possible to upgrade with passing tests when using
    Sereal::Decoder 4.019 on threaded debugging perls

* Thu Feb 17 2022 Paul Howarth <paul@city-fan.org> - 4.020-1
- Update to 4.020
  - Fix "panic: free from wrong pool" errors on threaded builds

* Mon Feb  7 2022 Paul Howarth <paul@city-fan.org> - 4.019-1
- Update to 4.019
  - Fix build issue with latest perl
  - Update bundled zstd to 1.5.1 (note: this package uses system zstd)
- Fix permissions verbosely
- Make %%files list more explicit

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.018-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.018-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.018-4
- Perl 5.34 re-rebuild of bootstrapped packages

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

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.014-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.014-2
- Perl 5.32 rebuild

* Mon Jun 15 2020 Petr Pisar <ppisar@redhat.com> - 4.014-1
- 4.014 bump

* Thu Jun 11 2020 Petr Pisar <ppisar@redhat.com> - 4.012-1
- 4.012 bump

* Tue Feb 04 2020 Petr Pisar <ppisar@redhat.com> - 4.011-1
- 4.011 bump

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 4.009-1
- 4.009 bump

* Thu Jan 30 2020 Petr Pisar <ppisar@redhat.com> - 4.008-1
- 4.008 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.007-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.007-5
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.007-4
- Perl 5.30 rebuild

* Wed May 22 2019 Petr Pisar <ppisar@redhat.com> - 4.007-3
- Finish a bootstrap cycle when rebuild against miniz-2.1.0

* Wed May 22 2019 Petr Pisar <ppisar@redhat.com> - 4.007-2
- Rebuild against miniz-2.1.0

* Wed Apr 10 2019 Petr Pisar <ppisar@redhat.com> - 4.007-1
- 4.007 bump

* Tue Apr 09 2019 Petr Pisar <ppisar@redhat.com> - 4.006-1
- 4.006 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.005-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.005-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.005-1
- 4.005 bump

* Mon Nov 13 2017 Petr Pisar <ppisar@redhat.com> - 4.004-1
- 4.004 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.015-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.015-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.015-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 05 2016 Petr Pisar <ppisar@redhat.com> - 3.015-1
- 3.015 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.014-4
- Perl 5.24 re-rebuild of bootstrapped packages

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

* Fri Nov 27 2015 Petr Pisar <ppisar@redhat.com> - 3.007-2
- Do not constrain Sereal::Encoder version

* Fri Nov 27 2015 Petr Pisar <ppisar@redhat.com> - 3.007-1
- 3.007 bump

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 3.006-1
- 3.006 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.005-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.005-2
- Perl 5.22 rebuild

* Tue Jan 06 2015 Petr Pisar <ppisar@redhat.com> - 3.005-1
- 3.005 bump

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 3.004-1
- 3.004 bump

* Wed Nov 12 2014 Petr Pisar <ppisar@redhat.com> - 3.003-1
- 3.003 bump

* Thu Nov 06 2014 Petr Pisar <ppisar@redhat.com> - 3.002-2
- Finish Sereal bootstrap

* Fri Oct 10 2014 Petr Pisar <ppisar@redhat.com> 3.002-1
- Specfile autogenerated by cpanspec 1.78.
