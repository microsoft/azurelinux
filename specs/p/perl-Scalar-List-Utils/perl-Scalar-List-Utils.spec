# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Scalar-List-Utils
Epoch:          5
Version:        1.70
Release:        1%{?dist}
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Scalar-List-Utils
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Scalar-List-Utils-%{version}.tar.gz
# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests only
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(overload)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(Tie::StdScalar)
BuildRequires:  perl(vars)

%{?perl_default_filter}

%description
This package contains a selection of subroutines that people have expressed
would be nice to have in the perl core, but the usage would not really be
high enough to warrant the use of a keyword, and the size so small such
that being individual extensions would be wasteful.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(Carp)
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)
Requires:       perl(threads)
Requires:       perl(threads::shared)
Requires:       perl(Tie::Handle)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Scalar-List-Utils-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -r -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/List*
%{perl_vendorarch}/List*
%{perl_vendorarch}/Scalar*
%{perl_vendorarch}/Sub*
%{_mandir}/man3/List*
%{_mandir}/man3/Scalar*
%{_mandir}/man3/Sub*

%files tests
%{_libexecdir}/%{name}

%changelog
* Wed Jul 30 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.70-1
- 1.70 bump (rhbz#2384547)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.69-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.69-519
- Increase release to favour standalone package

* Mon Apr 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.69-1
- 1.69 bump (rhbz#2356766)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.68-1
- 1.68 bump (rhbz#2319765)

* Mon Sep 23 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.66-1
- 1.66 bump (rhbz#2313658)

* Mon Aug 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.65-1
- 1.65 bump (rhbz#2302494)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.63-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.63-510
- Increase release to favour standalone package

* Thu Feb 08 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.63-503
- Package tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.63-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.63-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.63-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.63-499
- Increase release to favour standalone package

* Thu Jun 01 2023 Michal Josef Špaček <mspacek@redhat.com> - 5:1.63-491
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.63-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 10 2022 Jan Pazdziora <jpazdziora@redhat.com> - 5:1.63-489
- 2116427 - Rebase to upstream version 1.63.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.62-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.62-488
- Increase release to favour standalone package

* Tue Mar 22 2022 Adam Williamson <awilliam@redhat.com> - 5:1.62-464
- Rebuild with no changes to fix Bodhi issues for F36

* Mon Mar 21 2022 Jan Pazdziora <jpazdziora@redhat.com> - 5:1.62-463
- 2065327 - Rebase to upstream version 1.62.

* Fri Feb 18 2022 Jan Pazdziora <jpazdziora@redhat.com> - 5:1.61-463
- 2055228 - Rebase to upstream version 1.61.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.60-463
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 08 2021 Jan Pazdziora <jpazdziora@redhat.com> - 5:1.60-462
- 2012147 - Rebase to upstream version 1.60.

* Fri Sep 17 2021 Jan Pazdziora <jpazdziora@redhat.com> - 5:1.59-461
- 2003382 - Rebase to upstream version 1.59.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5:1.56-461
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 5:1.56-460
- Increase epoch to favour standalone package

* Thu Apr 01 2021 Jan Pazdziora <jpazdziora@redhat.com> - 4:1.56-459
- 1944897 - Rebase to upstream version 1.56.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.55-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.55-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.55-456
- Increase release to favour standalone package

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.55-456
- Increase epoch to favour standalone package

* Thu Apr 16 2020 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.55-441
- 1823191 - Rebase to upstream version 1.55.

* Thu Feb 06 2020 Tom Stellard <tstellar@redhat.com> - 3:1.54-441
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMaker

* Mon Feb 03 2020 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.54-440
- 1797333 - Rebase to upstream version 1.54.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.53-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.53-439
- 1765091 - Rebase to upstream version 1.53.

* Mon Aug 19 2019 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.52-439
- 1742608 - Rebase to upstream version 1.52.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.50-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.50-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.50-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.50-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.50-416
- Increase release to favour standalone package

* Fri Feb 23 2018 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.50-1
- 1547327 - Rebase to upstream version 1.50.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.49-1
- 1489828 - Rebase to upstream version 1.49.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.48-1
- 1464620 - Rebase to upstream version 1.48.

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.47-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 31 2016 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.47-1
- 1408347 - Rebase to upstream version 1.47.

* Fri Sep 30 2016 Jan Pazdziora <jpazdziora@redhat.com> - 3:1.46-1
- 1380561 - Rebase to upstream version 1.46.

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.45-2
- Increase epoch to favour standalone package

* Tue Mar 29 2016 Jan Pazdziora <jpazdziora@redhat.com> - 2:1.45-1
- 1.45 bump

* Fri Mar 18 2016 Jan Pazdziora <jpazdziora@redhat.com> - 2:1.44-1
- 1.44 bump

* Tue Feb 09 2016 Petr Šabata <contyk@redhat.com> - 2:1.43-1
- 1.43 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.42-2
- Perl 5.22 rebuild
- Increase Epoch to favour standalone package

* Tue May 26 2015 Petr Šabata <contyk@redhat.com> - 1:1.42-1
- 1.42 bump

* Mon Nov 24 2014 Petr Šabata <contyk@redhat.com> - 1:1.41-1
- 1.41 bump; various enhancements

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.38-5
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.38-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - Skip pairmap()'s MULTICALL implementation 5.8.9/5.10.0 as it doesn't work
    (CPAN RT#87857)
  - Comment on the fact that package "0" is defined but false (CPAN RT#88201)
  - TODO test in t/readonly.t now passes since 5.19.3 (CPAN RT#88223)
  - Added any, all, none, notall list reduction functions (inspired by
    List::MoreUtils)
  - Added List::Util::product()
  - Added Scalar::Util::unweaken()
  - Avoid C99/C++-style comments in XS code
  - Fix dualvar tests for perl 5.6; fix skip() test counts in dualvar.t
  - Neater documentation examples of other functions that can be built using
    reduce
  - Implement reduce() and first() even in the absence of MULTICALL
  - Various documentation changes/updates
  - Correct uses of overload operators in unit tests (CPAN RT#91969)

* Fri Aug 16 2013 Iain Arnell <iarnell@gmail.com> 1.31-293
- update to latest upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-292
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.27-291
- Specify all dependencies

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.27-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.27-247
- Link minimal build-root packages against libperl.so explicitly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-246
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Iain Arnell <iarnell@gmail.com> 1.27-245
- update to latest upstream version

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.25-240
- Increase release to replace perl sub-package (bug #848961)

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.25-4
- Correct dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Perl 5.16 rebuild

* Sun Mar 25 2012 Iain Arnell <iarnell@gmail.com> 1.25-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.23-2
- Perl mass rebuild

* Mon Feb 21 2011 Iain Arnell <iarnell@gmail.com> 1.23-1
- Specfile autogenerated by cpanspec 1.79.
