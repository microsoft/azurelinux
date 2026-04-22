# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%bcond_without perl_autodie_enables_optional_test

Name:           perl-autodie
Version:        2.37
Release: 522%{?dist}
Summary:        Replace functions with ones that succeed or die
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/autodie
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/autodie-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Fcntl)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(IPC::System::Simple) >= 0.12
%endif
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Sub::Identify is optional with a fallback
BuildRequires:  perl(Tie::RefHash)
# Tests:
# English not used
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
# Test::Perl::Critic not used
# Test::Pod 1.41 not used
# Test::Pod::Coverage 1.08 not used
# Optional tests:
%if %{with perl_autodie_enables_optional_test} && !%{defined perl_bootstrap}
BuildRequires:  perl(BSD::Resource)
BuildRequires:  perl(Import::Into) >= 1.002004
%endif
Requires:       perl(B)
Requires:       perl(Fcntl)
Requires:       perl(POSIX)
# Optional:
%if !%{defined perl_bootstrap}
# IPC::System::Simple dependency requested, bug #1183231
Requires:  perl(IPC::System::Simple) >= 0.12
%endif

# Remove falsely detected perl(lib)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(lib\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(autodie::test.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(autodie_.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Caller_helper\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Hints_.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(lethal\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(my::.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(pujHa::ghach\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Some::Module\\)

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(lib)
%if %{with perl_autodie_enables_optional_test} && !%{defined perl_bootstrap}
Requires:       perl(BSD::Resource)
Requires:       perl(Import::Into) >= 1.002004
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%description
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".

%prep
%setup -q -n autodie-%{version}
find -type f -exec chmod -x {} +

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
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
unset AUTHOR_TESTING AUTOMATED_TESTING PERL_CORE RELEASE_TESTING
# Some tests write into temporary files/directories. The solution is to
# copy the tests into a writable directory and execute them from there.
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset AUTHOR_TESTING AUTOMATED_TESTING PERL_CORE RELEASE_TESTING
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc AUTHORS Changes README.md
%{perl_vendorlib}/autodie*
%{perl_vendorlib}/Fatal*
%{_mandir}/man3/autodie*
%{_mandir}/man3/Fatal*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.37-1
- 2.37 bump (rhbz#2256130)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-499
- Increase release to favour standalone package

* Mon Jan 30 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-1
- 2.36 bump

* Mon Jan 30 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.35-1
- 2.35 bump
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-479
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.34-1
- 2.34 bump

* Fri Jan 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.33-1
- 2.33 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.32-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.32-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Petr Pisar <ppisar@redhat.com> - 2.32-1
- 2.32 bump

* Wed Jan 08 2020 Petr Pisar <ppisar@redhat.com> - 2.31-1
- 2.31 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-367
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.29-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 09 2015 Petr Pisar <ppisar@redhat.com> - 2.29-1
- 2.29 bump

* Mon Jun 22 2015 Petr Pisar <ppisar@redhat.com> - 2.28-1
- 2.28 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.27-2
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 10 2015 Petr Pisar <ppisar@redhat.com> - 2.27-1
- 2.27 bump

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-3
- Perl 5.22 rebuild

* Mon Jan 19 2015 Petr Pisar <ppisar@redhat.com> - 2.26-2
- Run-require IPC::System::Simple for fatalizing system() (bug #1183231)

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 2.26-1
- 2.26 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.25-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Mon Mar 31 2014 Petr Pisar <ppisar@redhat.com> - 2.24-1
- 2.24 bump

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 2.23-1
- 2.23 bump

* Mon Sep 23 2013 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Thu Sep 12 2013 Petr Pisar <ppisar@redhat.com> - 2.21-1
- 2.21 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.20-2
- Perl 5.18 rebuild

* Mon Jul 01 2013 Petr Pisar <ppisar@redhat.com> - 2.20-1
- 2.20 bump

* Wed Mar 06 2013 Petr Pisar <ppisar@redhat.com> - 2.16-1
- 2.16 bump

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> 2.13-1
- Specfile autogenerated by cpanspec 1.78.
