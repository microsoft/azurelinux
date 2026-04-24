# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Inherit additional methods from Digest::Base
%bcond_without perl_Digest_SHA_enables_digest_base
# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Digest_SHA_enables_optional_test
%else
%bcond_with perl_Digest_SHA_enables_optional_test
%endif

Name:           perl-Digest-SHA
Epoch:          1
Version:        6.04
Release: 522%{?dist}
Summary:        Perl extension for SHA-1/224/256/384/512
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Digest-SHA
Source0:        https://cpan.metacpan.org/authors/id/M/MS/MSHELOR/Digest-SHA-%{version}.tar.gz
# Since 5.80, upstream overrides CFLAGS because they think it improves
# performance. Revert it.
Patch0:         Digest-SHA-5.93-Reset-CFLAGS.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
# Getopt::Long not used at tests
BuildRequires:  perl(integer)
BuildRequires:  perl(warnings)
# XSLoader or DynaLoader
BuildRequires:  perl(XSLoader)
# Optional run-time
%if %{with perl_Digest_SHA_enables_digest_base}
BuildRequires:  perl(Digest::base)
%endif
# Tests
BuildRequires:  perl(FileHandle)
%if %{with perl_Digest_SHA_enables_optional_test}
# Optional tests
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 0.08
%endif
%endif
Requires:       perl(Carp)
# Optional but recommended
%if %{with perl_Digest_SHA_enables_digest_base}
Requires:       perl(Digest::base)
%endif
# XSLoader or DynaLoader
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
Digest::SHA is a complete implementation of the NIST Secure Hash Standard. It
gives Perl programmers a convenient way to calculate SHA-1, SHA-224, SHA-256,
SHA-384, SHA-512, SHA-512/224, and SHA-512/256 message digests. The module can
handle all types of input, including partial-byte data.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Digest-SHA-%{version}
%patch -P0 -p1
chmod -x examples/*
perl -MExtUtils::MakeMaker -e 'ExtUtils::MM_Unix->fixin(q{examples/dups})'

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE='%{optflags}'
%{make_build}

%install
%{make_install}
find '%{buildroot}' -type f -name '*.bs' -empty -delete
%{_fixperms} -c '%{buildroot}'

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
# Remove author tests
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t
rm %{buildroot}%{_libexecdir}/%{name}/t/podcover.t
# Create a temporary file in /tmp
perl -i -pe 's{"methods.tmp"}{"/tmp/methods.tmp"}' %{buildroot}%{_libexecdir}/%{name}/t/methods.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes examples/ README
%{_bindir}/shasum
%{perl_vendorarch}/auto/Digest/
%{perl_vendorarch}/Digest/
%{_mandir}/man1/shasum.1*
%{_mandir}/man3/Digest::SHA.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-519
- Increase release to favour standalone package

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.04-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.04-499
- Increase release to favour standalone package

* Sun Feb 26 2023 Paul Howarth <paul@city-fan.org> - 1:6.04-1
- 6.04 bump (rhbz#2173329)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 09 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.03-1
- 6.03 bump
- Package tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-488
- Increase release to favour standalone package

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-477
- Increase release to favour standalone package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-456
- Increase release to favour standalone package

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 1:6.02-442
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:6.02-2
- Perl 5.28 rebuild

* Mon Apr 23 2018 Paul Howarth <paul@city-fan.org> - 1:6.02-1
- 6.02 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 1:6.01-1
- 6.01 bump

* Mon Dec 11 2017 Petr Pisar <ppisar@redhat.com> - 1:6.00-1
- 6.00 bump

* Thu Oct 12 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.98-1
- 5.98 bump

* Fri Sep 08 2017 Petr Pisar <ppisar@redhat.com> - 1:5.97-1
- 5.97 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.96-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.96-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.96-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.96-393
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 1:5.96-1
- 5.96 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.95-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.95-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.95-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.95-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.95-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.95-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.95-2
- Perl 5.22 rebuild

* Fri Jan 30 2015 Petr Pisar <ppisar@redhat.com> - 1:5.95-1
- 5.95 bump

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 1:5.93-2
- Do not build-require version module

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 1:5.93-1
- 5.93 bump

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.92-5
- Perl 5.20 re-rebuild of bootstrapped packages

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.92-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1:5.92-1
- 5.92 bump

* Mon May 26 2014 Petr Pisar <ppisar@redhat.com> - 1:5.91-1
- 5.91 bump

* Fri May 09 2014 Petr Pisar <ppisar@redhat.com> - 1:5.90-1
- 5.90 bump

* Fri Apr 25 2014 Petr Pisar <ppisar@redhat.com> - 1:5.89-1
- 5.89 bump

* Tue Mar 18 2014 Petr Pisar <ppisar@redhat.com> - 1:5.88-1
- 5.88 bump

* Wed Feb 19 2014 Petr Pisar <ppisar@redhat.com> - 1:5.87-1
- 5.87 bump

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 1:5.86-1
- 5.86 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.85-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:5.85-2
- Perl 5.18 rebuild

* Fri Jun 28 2013 Petr Pisar <ppisar@redhat.com> - 1:5.85-1
- 5.85 bump

* Mon Mar 11 2013 Petr Pisar <ppisar@redhat.com> - 1:5.84-1
- 5.84 bump

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 1:5.83-1
- 5.83 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 1:5.82-1
- 5.82 bump

* Tue Jan 15 2013 Petr Pisar <ppisar@redhat.com> - 1:5.81-1
- 5.81 bump

* Tue Dec 11 2012 Petr Pisar <ppisar@redhat.com> - 1:5.80-1
- 5.80 bump

* Fri Nov 30 2012 Petr Pisar <ppisar@redhat.com> - 1:5.74-2
- Restore epoch value broken in 5.73 bump

* Mon Nov 26 2012 Petr Pisar <ppisar@redhat.com> - 0:5.74-1
- 5.74 bump

* Thu Nov 01 2012 Petr Pisar <ppisar@redhat.com> - 0:5.73-2
- 5.73 bump

* Wed Sep 26 2012 Petr Pisar <ppisar@redhat.com> - 1:5.72-1
- 5.72 bump

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:5.71-240
- bump release to override sub-package from perl.spec 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.71-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:5.71-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1:5.71-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1:5.71-2
- Omit optional POD tests on bootstrap

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 1:5.71-1
- 5.71 bump

* Tue Feb 14 2012 Petr Pisar <ppisar@redhat.com> 1:5.70-1
- Specfile autogenerated by cpanspec 1.78.
