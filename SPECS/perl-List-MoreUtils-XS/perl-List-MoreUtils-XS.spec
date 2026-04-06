# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra tests
%if ! (0%{?rhel})
%bcond_without perl_List_MoreUtils_XS_enables_extra_test
%else
%bcond_with perl_List_MoreUtils_XS_enables_extra_test
%endif

Name:		perl-List-MoreUtils-XS
Version:	0.430
Release:	18%{?dist}
Summary:	Provide compiled List::MoreUtils functions
# Code from List-MoreUtils < 0.417 is GPL-1.0-or-later OR Artistic-1.0-Perl
# Anything after that is Apache-2.0
# "git blame" on the upstream repo will probably be needed to
# determine the license of any particular chunk of code
License:	(GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:		https://metacpan.org/release/List-MoreUtils-XS
Source0:	https://cpan.metacpan.org/modules/by-module/List/List-MoreUtils-XS-%{version}.tar.gz
Patch0:		List-MoreUtils-XS-0.430-unbundle.patch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Capture::Tiny)
BuildRequires:	perl(Config::AutoConf) >= 0.315
BuildRequires:	perl(ExtUtils::CBuilder)
# Module Runtime
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader) >= 0.22
# Test Suite
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Math::Trig)
BuildRequires:	perl(overload)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Storable)
BuildRequires:	perl(Test::Builder::Module)
%if %{with perl_List_MoreUtils_XS_enables_extra_test}
BuildRequires:	perl(Test::LeakTrace)
%endif
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Tie::Array)
# Dependencies
# (none)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides accelerated versions of functions in List::MoreUtils.

%prep
%setup -q -n List-MoreUtils-XS-%{version}

# Unbundle bundled modules except private inc::Config::AutoConf::LMU
%patch -P 0
find inc/ -type f ! -name LMU.pm -print -delete
perl -i -ne 'print $_ unless m{^inc/} and not m{LMU\.pm}' MANIFEST

%build
perl Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{optflags}"\
	NO_PERLLOCAL=1 \
	NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license ARTISTIC-1.0 GPL-1 LICENSE
%doc Changes MAINTAINER.md README.md
%{perl_vendorarch}/auto/List/
%{perl_vendorarch}/List/
%{_mandir}/man3/List::MoreUtils::XS.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-17
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-14
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-10
- Perl 5.38 rebuild

* Tue Jun 13 2023 Paul Howarth <paul@city-fan.org> - 0.430-9
- Disable extra test in RHEL builds (based on
  https://src.fedoraproject.org/rpms/perl-List-MoreUtils-XS/pull-request/1)
- Silence build-time warnings about missing bundled modules

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.430-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 2020 Paul Howarth <paul@city-fan.org> - 0.430-1
- Update to 0.430
  - Fix parts of CPAN RT#123989: more $a/$b/$_ refcounting bugs
    - Since some bugs are simply reported wrong, dealing with them breaks more
      (including running code) than it solves - way too heavy to feel better...
  - Introduce functions slide and slideatatime
  - Toolchain fixes
  - Fix LANG=nb_NO.utf8 related str tests fails (CPAN RT#133128)
  - Fix typo (GH#7)
  - Fix parts of CPAN RT#132043: listcmp misbehave in XS implementation
- Use author-independent source URL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-9
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-6
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.428-3
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.428-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Paul Howarth <paul@city-fan.org> - 0.428-1
- Update to 0.428
  - Fix build fails on perl ≥ 5.27.4 with -DDEBUGGING (CPAN RT#123613)
  - Update ppport.h to 3.37 for improved blead support
  - Fix context arg to croak() (CPAN RT#123869)
  - Fix one() returning true on empty list (CPAN RT#123870)
  - Pamper $a/$b/$_ refcounting bugs (CPAN RT#123868)

* Tue Oct  3 2017 Paul Howarth <paul@city-fan.org> - 0.426-1
- Update to 0.426
  - Fix broken format in part (GH#4)
  - Fix gcc 4.7 sequence point warning (GH#5)
  - Fix incorrect padname resolving for perl > 5.21.6 (CPAN RT#122883)
  - Fix compiling issue on CentOS 4 and CentOS 5

* Sat Aug 19 2017 Paul Howarth <paul@city-fan.org> - 0.423-1
- Update to 0.423
  - Fix dealing with lists with one element on bremove/binsert (GH#2)
  - Add support for compilers before C99
  - Fix some 32-bit compiler warnings
  - Add support for compilers without statement expression feature

* Tue Aug 15 2017 Paul Howarth <paul@city-fan.org> - 0.422-1
- Update to 0.422
  - Rename 'occurances' into 'occurrences' (CPAN RT#91991, CPAN RT#122806)
  - Add DESCRIPTION to Pod clarifying the role of List::MoreUtils::XS
  - Improve Makefile.PL regarding some build artifacts

* Tue Aug 15 2017 Paul Howarth <paul@city-fan.org> - 0.421-1
- Update to 0.421
  - Fix a lot of potential memory leaks when callbacks throw exceptions
  - Add some new functions: qsort, binsert, bremove, listcmp, arrayify
    (CPAN RT#17230), samples (CPAN RT#77562), minmaxstr (CPAN RT#106401),
    lower_bound, upper_bound, equal_range, frequencies, occurances, mode
    (CPAN RT#91991), zip6 (CPAN RT#42921), reduce_0, reduce_1, reduce_u
  - Improve tests
  - Make List::MoreUtils::XS independent from List::MoreUtils
    Note that List::MoreUtils::XS doesn't guarantee API stability: this
    feature is only provided through List::MoreUtils as frontend
  - Improve configure toolchain to use Config::AutoConf 0.315
  - Speed up some inner loops by hinting the expected result
  - Fix mind screwed up issue in upper_bound and reduce elements visited in
    equal_range
  - Correct license in META (CPAN RT#122702)
  - Fix issues with -DPERL_IMPLICIT_SYS on Windows with Strawberry-Perl

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.418-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.418-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.418-4
- Perl 5.26 rebuild

* Mon Apr  3 2017 Paul Howarth <paul@city-fan.org> - 0.418-3
- Incorporate package review feedback (#1437588)
  - Fix URL
  - Unbundle bundled modules except private inc::Config::AutoConf::LMU

* Thu Mar 30 2017 Paul Howarth <paul@city-fan.org> - 0.418-2
- Sanitize for Fedora submission

* Thu Mar 30 2017 Paul Howarth <paul@city-fan.org> - 0.418-1
- Initial RPM version
