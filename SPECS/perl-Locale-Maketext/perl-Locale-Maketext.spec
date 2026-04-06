# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 1.32

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Locale_Maketext_enables_optional_test
%else
%bcond_with perl_Locale_Maketext_enables_optional_test
%endif

Name:           perl-Locale-Maketext
Version:        1.33
Release:        521%{?dist}
Summary:        Framework for localization
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Locale-Maketext
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/Locale-Maketext-%{base_version}.tar.gz
# Unbundled from perl 5.37.11
Patch0:         Locale-Maketext-1.32-Upgrade-to-1.33.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(I18N::LangTags) >= 0.31
BuildRequires:  perl(I18N::LangTags::Detect)
BuildRequires:  perl(integer)
# utf8 is used only if it has already been loaded
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
# Optional tests:
%if %{with perl_Locale_Maketext_enables_optional_test} && !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.14
%endif
Requires:       perl(I18N::LangTags) >= 0.31
# utf8 is used only if it has already been loaded
Requires:       perl(warnings)

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(I18N::LangTags\\)$

%description
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Locale-Maketext-%{base_version}
%patch -P0 -p1
perl -i -ne 'print $_ unless m{^t/00_load.t}' MANIFEST
perl -i -ne 'print $_ unless m{^t/pod.t}' MANIFEST

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
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc ChangeLog README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-499
- Increase release to favour standalone package

* Wed May 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-1
- Upgrade to 1.33 as provided in perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 23 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-1
- 1.32 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-488
- Increase release to favour standalone package

* Tue Apr 19 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-1
- 1.31 bump

* Mon Apr 04 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-1
- 1.30 bump
- Package tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-416
- Increase release to favour standalone package

* Thu May 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.29-1
- Upgrade to 1.29 as provided in perl-5.28.0-RC1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 27 2016 Petr Pisar <ppisar@redhat.com> - 1.28-1
- 1.28 bump

* Thu Jun 23 2016 Petr Pisar <ppisar@redhat.com> - 1.27-1
- 1.27 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-3
- Perl 5.22 rebuild

* Fri Jan 09 2015 Petr Pisar <ppisar@redhat.com> - 1.26-2
- Require undetected warnings module explicitly

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 1.26-1
- 1.26 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Petr Pisar <ppisar@redhat.com> - 1.25-1
- 1.25 bump

* Mon Nov 11 2013 Petr Pisar <ppisar@redhat.com> - 1.23-293
- Fix escaping backslashes (bug #1026763)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.23-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.23-2
- Perl 5.18 rebuild

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> 1.23-1
- Specfile autogenerated by cpanspec 1.78.
