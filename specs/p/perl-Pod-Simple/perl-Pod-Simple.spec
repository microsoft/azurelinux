# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Pod-Simple
# Epoch to compete with perl.spec
Epoch:          1
Version:        3.47
Release:        3%{?dist}
Summary:        Framework for parsing POD documentation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Pod-Simple
Source0:        https://cpan.metacpan.org/authors/id/K/KH/KHW/Pod-Simple-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(if)
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(Pod::Escapes) >= 1.04
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Text::Wrap) >= 98.112902
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(parent)
BuildRequires:  perl(Test) >= 1.25
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional tests:
# Text::Diff not helpful, used only in case of a failure

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Text::Wrap\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{__requires_exclude}|^perl\\(helpers\\)$


%description
Pod::Simple is a Perl library for parsing text in the POD (plain old
documentation) markup language that is typically used for writing
documentation for Perl and for Perl modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(FindBin)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Pod-Simple-%{version}

# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

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
unset PERL_CORE PERL_TEST_DIFF
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc ChangeLog README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.47-2
- Perl 5.42 rebuild

* Mon May 19 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.47-1
- 3.47 bump (rhbz#2366683)

* Tue May 13 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.46-1
- 3.46 bump (rhbz#2365701)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-3
- Perl 5.38 rebuild

* Tue May 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-2
- Add filter for private test module perl(helpers)

* Tue May 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.45-1
- 3.45 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-1
- 3.43 bump
- Package tests

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-1
- 3.42 bump

* Mon Oct 12 2020 Tom Callaway <spot@fedoraproject.org> - 1:3.41-459
- update to 3.41
- I left release at the artificially high value in case it was needed

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.40-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.40-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Tom Callaway <spot@fedoraproject.org> - 1:3.40-1
- update to 3.40

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Petr Pisar <ppisar@redhat.com> - 1:3.39-1
- 3.39 bump

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.38-2
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Petr Pisar <ppisar@redhat.com> - 1:3.38-1
- 3.38 bump

* Thu May 30 2019 Petr Pisar <ppisar@redhat.com> - 1:3.37-2
- Do not package Pod::Escapes (upstream bug #102)

* Thu May 30 2019 Tom Callaway <spot@fedoraproject.org> - 1:3.37-1
- update to 3.37

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.36-2
- Perl 5.30 rebuild

* Thu May 23 2019 Petr Pisar <ppisar@redhat.com> - 1:3.36-1
- 3.36 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.35-416
- Increase release to favour standalone package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.35-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Petr Pisar <ppisar@redhat.com> - 1:3.35-1
- 3.35 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.32-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Petr Pisar <ppisar@redhat.com> - 1:3.32-2
- Specify all dependencies

* Tue Nov  3 2015 Tom Callaway <spot@fedoraproject.org> - 1:3.32-1
- update to 3.32

* Tue Aug 25 2015 Tom Callaway <spot@fedoraproject.org> - 1:3.31-1
- update to 3.31

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.30-2
- Perl 5.22 rebuild

* Tue Feb 24 2015 Petr Pisar <ppisar@redhat.com> - 1:3.30-1
- 3.30 bump

* Fri Jan 30 2015 Petr Pisar <ppisar@redhat.com> - 1:3.29-1
- 3.29 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.28-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.28-294
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.28-293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.28-292
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1:3.28-291
- Specify all dependencies

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:3.28-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:3.28-3
- Link minimal build-root packages against libperl.so explicitly

* Thu May 23 2013 Petr Pisar <ppisar@redhat.com> - 1:3.28-2
- Specify all dependencies

* Mon May 06 2013 Petr Pisar <ppisar@redhat.com> - 1:3.28-1
- 3.28 bump

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> 1:3.26-1
- Specfile autogenerated by cpanspec 1.78.
