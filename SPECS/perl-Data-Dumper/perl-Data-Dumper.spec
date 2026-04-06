# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 2.183

Name:           perl-Data-Dumper
Version:        2.191
Release:        521%{?dist}
Summary:        Stringify perl data structures, suitable for printing and eval
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Dumper
Source0:        https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/Data-Dumper-%{base_version}.tar.gz
# Upgrade to 2.184 based on perl-5.35.11
Patch0:         Data-Dumper-2.183-Upgrade-to-2.184.patch
# Upgrade to 2.188 based on perl-5.37.11
Patch1:         Data-Dumper-2.184-Upgrade-to-2.188.patch
# Upgrade to 2.189 based on perl-5.40.0-RC1
Patch2:         Data-Dumper-2.188-Upgrade-to-2.189.patch
# Upgrade to 2.191 based on perl-5.42.0
Patch3:         Data-Dumper-2.189-Upgrade-to-2.191.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Devel::PPPort)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# perl-Test-Simple is in cycle with perl-Data-Dumper
%if !%{defined perl_bootstrap}
# Run-time:
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(Config)
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(vars)
# Optional tests:
BuildRequires:  perl(Encode)
%endif
Requires:       perl(B::Deparse)
Requires:       perl(bytes)
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)

%{?perl_default_filter}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Testing\\)

%description
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl(Encode)
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Data-Dumper-%{base_version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

# Generate ppport.h
#perl -MDevel::PPPort \
#    -e "Devel::PPPort::WriteFile() or die 'Could not generate ppport.h: $!'"

# Help file to recognise the Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
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
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
%if !%{defined perl_bootstrap}
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test
%endif

%files
%doc Changes Todo
%{perl_vendorarch}/auto/Data*
%{perl_vendorarch}/Data*
%{_mandir}/man3/Data::Dumper*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.191-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.191-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Tue Jun 24 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.191-519
- Upgrade to 2.191 based on perl-5.42.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.189-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.189-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.189-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.189-510
- Increase release to favour standalone package

* Mon Jun 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.189-504
- Upgrade to 2.189 based on perl-5.40.0-RC1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.188-503
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.188-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.188-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.188-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.188-499
- Increase release to favour standalone package

* Tue May 16 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.188-1
- Upgrade to 2.188 based on perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.184-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.184-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.184-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.184-488
- Increase release to favour standalone package

* Wed May 11 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.184-1
- Upgrade to 2.184 based on perl-5.35.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.183-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.183-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.183-1
- 2.183 bump

* Thu Jul 01 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.182-1
- 2.182 bump

* Mon May 31 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.181-1
- 2.181 bump

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.180-4
- Perl 5.34 re-rebuild of bootstrapped packages

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.180-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.180-2
- Perl 5.34 rebuild

* Mon May 17 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.180-1
- 2.180 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.174-460
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 20 2020 Petr Pisar <ppisar@redhat.com> - 2.174-459
- Fix a memory leak when a magic throws an exception

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.174-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.174-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.174-456
- Increase release to favour standalone package

* Tue Feb 04 2020 Petr Pisar <ppisar@redhat.com> - 2.174-443
- Modernize the spec file

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 2.174-442
- Use make_build macro
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.174-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.174-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.174-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.174-438
- Increase release to favour standalone package

* Fri Apr 26 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.174-1
- Update version to 2.174 as provided in perl-5.29.10

* Wed Apr 03 2019 Petr Pisar <ppisar@redhat.com> - 2.173-3
- Fix a memory leak when croaking about a too deep recursion

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.173-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Petr Pisar <ppisar@redhat.com> - 2.173-1
- 2.173 bump

* Thu Sep 20 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.172-1
- 2.172 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.170-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.170-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.170-416
- Increase release to favour standalone package

* Wed May 23 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.170-1
- Upgrade to 2.170 as provided in perl-5.28.0-RC1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.167-399
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Petr Pisar <ppisar@redhat.com> - 2.167-398
- Fix postentry for quoted glob (bug #1532524)

* Tue Dec 05 2017 Petr Pisar <ppisar@redhat.com> - 2.167-397
- Fix quoting glob names (RT#119831)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.167-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.167-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.167-394
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.167-393
- Perl 5.26 rebuild

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 2.167-1
- Upgrade to 2.167 as provided in perl-5.25.12

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.161-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 2.161-1
- 1.161 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.160-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.160-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.160-1
- 2.160 bump in order to dual-live with perl 5.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.158-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.158-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.158-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.158-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.158-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 2.158-1
- 2.158 bump in order to dual-live with perl 5.22

* Fri Sep 19 2014 Petr Pisar <ppisar@redhat.com> - 2.154-1
- 2.154 bump (fixes CVE-2014-4330 (limit recursion when dumping deep data
  structures))

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.151-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.151-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.151-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.151-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.151-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Petr Pisar <ppisar@redhat.com> - 2.151-1
- 2.151 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.145-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.145-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.145-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.145-2
- Perl 5.18 rebuild

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> - 2.145-1
- 2.145 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 2.143-1
- 2.143 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Petr Pisar <ppisar@redhat.com> - 2.139-1
- 2.139 bump

* Fri Oct 05 2012 Petr Pisar <ppisar@redhat.com> - 2.136-1
- 2.136 bump

* Fri Aug 24 2012 Petr Pisar <ppisar@redhat.com> - 2.135.07-241
- Disable tests on bootstrap

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.135.07-240
- update the version to override the module from perl.srpm
- bump release to override sub-package from perl.spec 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.131-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.131-2
- Perl 5.16 rebuild

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> 2.131-1
- Specfile autogenerated by cpanspec 1.78.
