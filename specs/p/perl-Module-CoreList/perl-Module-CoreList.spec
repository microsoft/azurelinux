# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Module-CoreList
# Epoch to compete with perl.spec
Epoch:          1
Version:        5.20260119
Release: 2%{?dist}
Summary:        What modules are shipped with versions of perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-CoreList
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-CoreList-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# File::Copy not used
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
# feature not used at tests
# Getopt::Long not used at tests
BuildRequires:  perl(List::Util)
# Pod::Usage not used at tests
BuildRequires:  perl(version) >= 0.88
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(List::Util)
Requires:       perl(version) >= 0.88

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(version\\)$

%description
Module::CoreList provides information on which core and dual-life modules
are shipped with each version of perl.

%package tools
Summary:        Tool for listing modules shipped with perl
Requires:       perl(feature)
Requires:       perl(version) >= 0.88
Requires:       perl-Module-CoreList = %{epoch}:%{version}-%{release}
# The files were distributed with perl.spec's subpackage
# perl-Module-CoreList <= 1:5.020001-309
Conflicts:      perl-Module-CoreList < 1:5.20140914

%description tools
This package provides a corelist(1) tool which can be used to query what
modules were shipped with given perl version.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-tools = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}-%{version}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-CoreList-%{version}

# Help file to recognise the Perl scripts and normalize shebangs
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
rm -f %{buildroot}/%{_libexecdir}/%{name}/t/pod.t
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset PERL_CORE
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
unset PERL_CORE
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README
%{perl_vendorlib}/Module
%{_mandir}/man3/Module::CoreList*

%files tools
%doc README
%{_bindir}/corelist
%{_mandir}/man1/corelist.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Tue Jan 20 2026 Jitka Plesnikova <jplesnik@redhat.com> - 5.20260119-1
- 5.20260119 bump (rhbz#2430994)

* Mon Jan 05 2026 Jitka Plesnikova <jplesnik@redhat.com> - 5.20251220-1
- 5.20251220 bump (rhbz#2424158)

* Mon Nov 24 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.20251120-1
- 5.20251120 bump (rhbz#2416074)

* Fri Oct 24 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.20251022-1
- 5.20251022 bump (rhbz#2406067)

* Mon Sep 29 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.20250923-1
- 5.20250923 bump (rhbz#2397602)

* Mon Aug 25 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250820-1
- 5.20250820 bump (rhbz#2389924)

* Tue Aug 05 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250803-1
- 5.20250803 bump (rhbz#2386185)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20250720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250720-1
- 5.20250720 bump (rhbz#2382318)

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250702-519
- Increase release to favour standalone package

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250702-1
- 5.20250702 bump (rhbz#2376788)

* Mon Jun 09 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250528-1
- 5.20250528 bump (rhbz#2371158)

* Tue Apr 22 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250421-1
- 5.20250421 bump (rhbz#2361330)

* Mon Apr 14 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250414-1
- 5.20250414 bump (rhbz#2359301)

* Mon Mar 24 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250321-1
- 5.20250321 bump (rhbz#2354065)

* Tue Feb 25 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250220-1
- 5.20250220 bump (rhbz#2347278)

* Tue Jan 21 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20250120-1
- 5.20250120 bump (rhbz#2339071)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20241220-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20241220-1
- 5.20241220 bump (rhbz#2333519)

* Thu Nov 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20241120-1
- 5.20241120 bump (rhbz#2327610)

* Mon Oct 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20241020-1
- 5.20241020 bump (rhbz#2320085)

* Mon Sep 23 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240920-1
- 5.20240920 bump (rhbz#2313768)

* Tue Sep 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240829-1
- 5.20240829 bump (rhbz#2309090)

* Mon Jul 22 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240720-1
- 5.20240720 bump (rhbz#2299046)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20240702-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240702-1
- 5.20240702 bump (rhbz#2295346)

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240609-510
- Increase release to favour standalone package

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240609-1
- 5.20240609 bump (rhbz#2291113)

* Mon Apr 29 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240420-1
- 5.20240420 bump (rhbz#2277538)

* Thu Mar 21 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240320-1
- 5.20240320 bump (rhbz#2270521)

* Tue Feb 27 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240223-1
- 5.20240223 bump (rhbz#2265706)

* Tue Jan 30 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20240129-1
- 5.20240129 bump (rhbz#2261642)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20231230-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20231230-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20231230-1
- 5.20231230 bump (rhbz#2256323)

* Fri Dec 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20231129-1
- 5.20231129 bump (rhbz#2252137)

* Mon Nov 20 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20231120-1
- 5.20231120 bump (rhbz#2250650)

* Thu Oct 26 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20231025-1
- 5.20231025 bump (rhbz#2246230)

* Thu Sep 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230920-1
- 5.20230920 bump (rhbz#2239940)

* Tue Aug 22 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230820-1
- 5.20230820 bump (rhbz#2233000)

* Fri Jul 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230720-1
- 5.20230720 bump (rhbz#2224451)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20230520-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230520-499
- Increase release to favour standalone package

* Mon Jul 10 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230520-1
- 5.20230520 bump

* Mon Apr 24 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230423-1
- 5.20230423 bump

* Wed Mar 22 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230320-1
- 5.20230320 bump

* Tue Feb 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230220-1
- 5.20230220 bump

* Wed Jan 25 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20230120-1
- 5.20230120 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20221220-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20221220-1
- 5.20221220 bump

* Mon Nov 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20221120-1
- 5.20221120 bump

* Fri Oct 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20221020-1
- 5.20221020 bump

* Wed Sep 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220920-1
- 5.20220920 bump

* Mon Aug 22 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220820-1
- 5.20220820 bump

* Thu Jul 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220720-1
- 5.20220720 bump

* Tue Jun 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220620-1
- 5.20220620 bump

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220527-2
- Perl 5.36 rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220527-1
- 5.20220527 bump

* Thu Apr 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220420-1
- 5.20220420 bump

* Tue Mar 22 2022 Adam Williamson <awilliam@redhat.com> - 1:5.20220320-2
- Rebuild with no changes to fix update mess on F36

* Mon Mar 21 2022 Michal Josef Špaček <mspacek@redhat.com> - 1:5.20220320-1
- 5.20220320 bump

* Wed Mar 16 2022 Michal Josef Špaček <mspacek@redhat.com> - 1:5.20220313-1
- 5.20220313 bump

* Sun Feb 20 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220220-1
- 5.20220220 bump

* Fri Jan 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20220120-1
- 5.20220120 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20211220-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20211220-1
- 5.20211220 bump

* Mon Nov 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20211120-1
- 5.20211120 bump

* Mon Oct 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20211020-1
- 5.20211020 bump

* Tue Sep 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210920-1
- 5.20210920 bump

* Mon Aug 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210820-1
- 5.20210820 bump

* Mon Aug 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210723-1
- 5.20210723 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20210620-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210620-1
- 5.20210620 bump

* Tue May 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210521-1
- 5.20210521 bump

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210520-2
- Perl 5.34 rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210520-1
- 5.20210520 bump

* Wed Apr 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210420-1
- 5.20210420 bump

* Sun Mar 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210320-1
- 5.20210320 bump

* Mon Feb 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210220-1
- 5.20210220 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20210123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210123-1
- 5.20210123 bump

* Thu Jan 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20210120-1
- 5.20210120 bump

* Mon Dec 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20201220-1
- 5.20201220 bump

* Fri Nov 20 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20201120-1
- 5.20201120 bump

* Wed Oct 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20201020-1
- 5.20201020 bump

* Mon Sep 21 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20200920-1
- 5.20200920 bump

* Fri Aug 21 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200820-1
- 5.20200820 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20200717-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200717-1
- 5.20200717 bump

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20200620-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20200620-456
- Increase release to favour standalone package

* Mon Jun 22 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200620-1
- 5.20200620 bump

* Tue Jun 09 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200603-1
- 5.20200603 bump

* Tue Jun 02 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200602-1
- 5.20200602 bump

* Wed Apr 29 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200428-1
- 5.20200428 bump

* Mon Mar 23 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200320-1
- 5.20200320 bump

* Mon Mar 16 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200314-1
- 5.20200314 bump

* Fri Feb 21 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200220-1
- 5.20200220 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20200120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20200120-1
- 5.20200120 bump

* Thu Jan 02 2020 Petr Pisar <ppisar@redhat.com> - 1:5.20191220-1
- 5.20191220 bump

* Thu Nov 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20191120-1
- 5.20191120 bump

* Mon Nov 11 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20191110-1
- 5.20191110 bump

* Mon Oct 21 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20191020-1
- 5.20191020 bump

* Mon Sep 23 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190920-1
- 5.20190920 bump

* Wed Aug 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190820-1
- 5.20190820 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20190720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190720-1
- 5.20190720 bump

* Fri Jun 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190620-1
- 5.20190620 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20190524-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20190524-2
- Perl 5.30 rebuild

* Mon May 27 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190524-1
- 5.20190524 bump

* Wed May 22 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190522-1
- 5.20190522 bump

* Tue Apr 23 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190420-1
- 5.20190420 bump

* Thu Mar 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190320-1
- 5.20190320 bump

* Thu Feb 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190220-1
- 5.20190220 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20190120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Petr Pisar <ppisar@redhat.com> - 1:5.20190120-1
- 5.20190120 bump

* Wed Dec 19 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20181218-1
- 5.20181218 bump

* Mon Dec 03 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20181130-1
- 5.20181130 bump

* Wed Nov 21 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20181120-1
- 5.20181120 bump

* Tue Oct 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20181020-1
- 5.20181020 bump

* Fri Sep 21 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20180920-1
- 5.20180920 bump

* Tue Aug 21 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180820-1
- 5.20180820 bump

* Mon Jul 23 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180720-1
- 5.20180720 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20180626-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20180626-2
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180626-1
- 5.20180626 bump

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20180622-416
- Increase release to favour standalone package

* Mon Jun 25 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180622-1
- 5.20180622 bump

* Mon Apr 23 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180420-1
- 5.20180420 bump

* Fri Apr 20 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180415-1
- 5.20180415 bump

* Mon Apr 16 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180414-1
- 5.20180414 bump

* Fri Apr 13 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180414-0.1.RC1
- 5.20180414_26 bump

* Wed Mar 21 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180221-1
- 5.20180221 bump

* Wed Feb 21 2018 Petr Pisar <ppisar@redhat.com> - 1:5.20180220-1
- 5.20180220 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20180120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20180120-1
- 5.20180120 bump

* Fri Dec 22 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20171220-1
- 5.20171220 bump

* Tue Nov 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20171120-1
- 5.20171120 bump

* Mon Oct 23 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20171020-1
- 5.20171020 bump

* Mon Sep 25 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170923-1
- 5.20170923 bump

* Thu Sep 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170920-1
- 5.20170920 bump

* Tue Aug 22 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170821-1
- 5.20170821 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20170720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170720-1
- 5.20170720 bump

* Mon Jul 17 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170715-1
- 5.20170715 bump

* Tue Jun 20 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20170621-1
- 5.20170621 bump

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20170531-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20170531-2
- Perl 5.26 rebuild

* Thu Jun 01 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170531-1
- 5.20170531 bump

* Wed May 31 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170530-1
- 5.20170530 bump

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170520-0.1
- Upgrade to 5.20170520 as provided in perl's blead git branch

* Fri Apr 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170420-1
- 5.20170420 bump

* Tue Mar 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170320-1
- 5.20170320 bump

* Tue Feb 21 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170220-1
- 5.20170220 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20170120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170120-1
- 5.20170120 bump

* Mon Jan 16 2017 Petr Pisar <ppisar@redhat.com> - 1:5.20170115-1
- 5.20170115 bump

* Wed Dec 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20161220-1
- 5.20161220 bump

* Mon Nov 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20161120-1
- 5.20161120 bump

* Fri Oct 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20161020-1
- 5.20161020 bump

* Wed Sep 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160920-1
- 5.20160920 bump

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160820-1
- 5.20160820 bump

* Fri Aug 05 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20160720-2
- Avoid loading optional modules from default . (CVE-2016-1238)

* Thu Jul 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160720-1
- 5.20160720 bump

* Tue Jun 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160620-1
- 5.20160620 bump

* Mon May 23 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160520-1
- 5.20160520 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20160507-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20160507-2
- Perl 5.24 rebuild

* Tue May 10 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160507-1
- 5.20160507 bump

* Mon May 02 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160429-1
- 5.20160429 bump

* Mon Mar 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160320-1
- 5.20160320 bump

* Mon Feb 22 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160121-1
- 5.20160121 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.20160120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Petr Pisar <ppisar@redhat.com> - 1:5.20160120-1
- 5.20160120 bump

* Tue Dec 22 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20151220-1
- 5.20151220 bump

* Mon Dec 14 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20151213-1
- 5.20151213 bump

* Mon Nov 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20151120-1
- 5.20151120 bump

* Thu Oct 22 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20151020-1
- 5.20151020 bump

* Mon Sep 21 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150920-1
- 5.20150920 bump

* Mon Sep 14 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150912-1
- 5.20150912 bump

* Tue Aug 25 2015 Tom Callaway <spot@fedoraproject.org> - 1:5.20150820-1
- 5.20150820 bump

* Tue Jul 21 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150720-1
- 5.20150720 bump

* Mon Jun 22 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150620-1
- 5.20150620 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.20150520-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20150520-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20150520-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150520-1
- 5.20150520 bump

* Tue Apr 21 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150420-1
- 5.20150420 bump

* Mon Mar 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150320-1
- 5.20150320 bump

* Mon Feb 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150220-1
- 5.20150220 bump

* Mon Feb 16 2015 Tom Callaway <spot@fedoraproject.org> - 1:5.20150214-1
- 5.20150214 bump

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150120-1
- 5.20150120 bump

* Fri Jan 02 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20141220-1
- 5.20141220 bump

* Tue Nov 25 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141120-1
- 5.20141120 bump

* Tue Oct 21 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141020-1
- 5.20141020 bump

* Wed Oct 08 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141002-1
- 5.20141002 bump

* Wed Sep 17 2014 Petr Pisar <ppisar@redhat.com> 1:5.20140914-1
- Specfile autogenerated by cpanspec 1.78.
