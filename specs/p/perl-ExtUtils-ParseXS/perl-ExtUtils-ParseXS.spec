# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 3.58
Name:           perl-ExtUtils-ParseXS
# Epoch to compete with perl.spec
Epoch:          1
Version:        3.58
Release:        2%{?dist}
Summary:        Module and a script for converting Perl XS code into C code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/ExtUtils-ParseXS
Source0:        https://cpan.metacpan.org/modules/by-module/ExtUtils/ExtUtils-ParseXS-%{base_version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(fields)
# ExtUtils::XSSymSet not needed
BuildRequires:  perl(File::Basename)
# Getopt::Long not tested
BuildRequires:  perl(re)
BuildRequires:  perl(Symbol)
# Tests:
BuildRequires:  perl(attributes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More) >= 0.47
Requires:       perl(Exporter) >= 5.57
Requires:       perl(fields)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Exporter\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(ExtUtils::Typemaps::Test\\)
%global __requires_exclude %{__requires_exclude}|^perl\\((TypemapTest::Foo\|IncludeTester\|PrimitiveCapture)\)

%description
ExtUtils::ParseXS will compile XS code into C code by embedding the
constructs necessary to let C functions manipulate Perl values and creates
the glue necessary to let Perl access those functions.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n ExtUtils-ParseXS-%{base_version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*
# Do not install xsubpp twice, RT#117289
rm $RPM_BUILD_ROOT%{perl_vendorlib}/ExtUtils/xsubpp
ln -s ../../../../bin/xsubpp $RPM_BUILD_ROOT%{perl_vendorlib}/ExtUtils/

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories. The easiest solution
# is to copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes
%{_bindir}/xsubpp
%{perl_vendorlib}/ExtUtils*
%{perl_vendorlib}/perlxs*
%{_mandir}/man1/xsubpp*
%{_mandir}/man3/ExtUtils*
%{_mandir}/man3/perlxs*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.58-1
- 3.58 bump (rhbz#2382307)

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.57-519
- Increase release to favour standalone package

* Wed Apr 30 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.57-1
- 3.57 bump (rhbz#2363711)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.51-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.51-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.51-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.51-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.51-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 04 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.51-501
- Replace patch update from Perl release by CPAN upstream 3.51 (rhbz#2237243)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.51-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.51-499
- Increase release to favour standalone package

* Mon Jun 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.51-1
- Upgrade to 3.51 as provided in perl-5.37.12

* Wed May 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.50-1
- Upgrade to 3.50 as provided in perl-5.37.11
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-488
- Increase release to favour standalone package

* Thu May 12 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-1
- Upgrade to 3.45 as provided in perl-5.35.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-1
- 3.44 bump

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-477
- Increase release to favour standalone package

* Thu May 06 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-1
- Upgrade to 3.43 as provided in perl-5.34.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.40-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.40-438
- Increase release to favour standalone package

* Thu May 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.40-1
- Upgrade to 3.40 as provided in perl-5.29.10

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.39-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Petr Pisar <ppisar@redhat.com> - 1:3.39-418
- Fix generating Perl prototypes for XS functions with OUTLIST parameters
  (RT#133654)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.39-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.39-416
- Increase release to favour standalone package

* Thu May 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.39-1
- Upgrade to 3.39 as provided in perl-5.28.0-RC1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 01 2017 Petr Pisar <ppisar@redhat.com> - 1:3.35-1
- 3.35 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.34-393
- Perl 5.26 rebuild

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 1:3.34-1
- Upgrade to 3.34 as provided in perl-5.25.12

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.31-368
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 13 2016 Petr Pisar <ppisar@redhat.com> - 1:3.31-367
- Remove old obsoleting perl-ExtUtils-Typemaps

* Wed Aug 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.31-366
- Avoid loading optional modules from default . (CVE-2016-1238)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.31-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.31-1
- 3.31 bump in order to dual-live with perl 5.24

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 1:3.30-3
- Remove dependency on perl-devel (bug #1129443)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 Petr Pisar <ppisar@redhat.com> - 1:3.30-1
- 3.30 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.28-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.28-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.28-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 1:3.28-1
- 3.28 bump in order to dual-live with perl 5.22

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.24-310
- Perl 5.20 rebuild
- Increase release to favour standalone package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Petr Pisar <ppisar@redhat.com> - 1:3.24-1
- 3.24 bump

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 1:3.22-1
- 3.22 bump

* Mon Aug 26 2013 Petr Pisar <ppisar@redhat.com> - 1:3.21-1
- 3.21 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.18-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:3.18-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:3.18-2
- Perl 5.18 rebuild

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> 1:3.18-1
- Specfile autogenerated by cpanspec 1.78.
