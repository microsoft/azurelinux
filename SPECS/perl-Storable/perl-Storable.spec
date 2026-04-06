# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 3.25
Name:           perl-Storable
Epoch:          1
Version:        3.37
Release:        521%{?dist}
Summary:        Persistence for Perl data structures
# Storable.pm:  GPL+ or Artistic
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Storable
Source0:        https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/Storable-%{base_version}.tar.gz
# Unbundled from perl 5.37.12
Patch0:         Storable-3.25-Upgrade-to-3.32.patch
# Unbundled from perl 5.42.0
Patch1:         Storable-3.32-Upgrade-to-3.37.patch
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Devel::PPPort)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Win32 not used on Linux
# Win32API::File not used on Linux
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Fcntl is optional, but locking is good
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(IO::File)
# Log::Agent is optional
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Tie::Array)
# Optional tests:
# gzip not used
# Data::Dump not used
# Data::Dumper not used
BuildRequires:  perl(B::Deparse) >= 0.61
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Hash::Util)
# Test::LeakTrace omitted because it's not a core module requried for building
# core Storable.
BuildRequires:  perl(Tie::Hash)
Requires:       perl(Config)
# Fcntl is optional, but locking is good
Requires:       perl(Fcntl)
Requires:       perl(IO::File)

%{?perl_default_filter}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(HAS_OVERLOAD\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(STDump\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(STTestLib\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(testlib.pl\\)

%description
The Storable package brings persistence to your Perl data structures
containing scalar, array, hash or reference objects, i.e. anything that
can be conveniently stored to disk and retrieved at a later time.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(B::Deparse) >= 0.61
Requires:       perl(Digest::MD5)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Storable-%{base_version}

# Generate ppport.h which is used since 1.32
perl -MDevel::PPPort \
    -e 'Devel::PPPort::WriteFile() or die "Could not generate ppport.h: $!"'

# Help generators to recognize Perl scripts
for F in t/*.t t/*.pl; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
find %{buildroot} -type f -name '*.3pm' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
cat > %{buildroot}/%{_libexecdir}/%{name}/test << 'EOF'
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
chmod +x %{buildroot}/%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
unset PERL_CORE PERL_TEST_MEMORY PERL_RUN_SLOW_TESTS
make test

%files
%doc ChangeLog README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Storable*
%{_mandir}/man3/Storable*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.37-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.37-520
- Filter private test requires

* Sun Jul 06 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.37-519
- Upgrade to 3.37 as provided in perl-5.42.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.32-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.32-499
- Increase release to favour standalone package

* Mon Jun 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.32-1
- Upgrade to 3.32 as provided in perl-5.37.12

* Thu May 18 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.31-1
- Upgrade to 3.31 as provided in perl-5.37.11

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.26-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.26-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.26-488
- Upgrade to 3.26 as provided in perl-5.35.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 30 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.25-1
- 3.25 bump
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.23-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.23-477
- Upgrade to 3.23 as provided in perl-5.34.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.21-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.21-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.21-456
- Upgrade to 3.21 as provided in perl-5.32.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.15-443
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Petr Pisar <ppisar@redhat.com> - 1:3.15-442
- Fix a buffer overflow when processing a vstring longer than 2^31-1
  (Perl GH#17306)

* Thu Aug 08 2019 Petr Pisar <ppisar@redhat.com> - 1:3.15-441
- Fix array length check in a store hook

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.15-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Petr Pisar <ppisar@redhat.com> - 1:3.15-439
- Fix deep cloning regular expression objects (RT#134179)

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.15-438
- Increase release to favour standalone package

* Wed Apr 24 2019 Petr Pisar <ppisar@redhat.com> - 1:3.15-1
- 3.15 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Petr Pisar <ppisar@redhat.com> - 1:3.11-6
- Storable-3.11 source archive repackaged without a t/CVE-2015-1592.inc file
  (RT#133706)

* Mon Aug 27 2018 Petr Pisar <ppisar@redhat.com> - 1:3.11-5
- Fix recursion check (RT#133326)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.11-3
- Perl 5.28 rebuild

* Tue Jun 05 2018 Petr Pisar <ppisar@redhat.com> - 1:3.11-2
- Do not package empty Storable::Limit(3pm) manual page

* Mon Apr 30 2018 Petr Pisar <ppisar@redhat.com> - 1:3.11-1
- 3.11 bump

* Mon Apr 23 2018 Petr Pisar <ppisar@redhat.com> - 1:3.09-1
- 3.09 bump

* Thu Apr 19 2018 Petr Pisar <ppisar@redhat.com> - 1:3.06-1
- 3.06 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.62-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.62-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.62-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.62-393
- Perl 5.26 rebuild

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 1:2.62-1
- Upgrade to 2.62 as provided in perl-5.25.12

* Mon Feb 06 2017 Petr Pisar <ppisar@redhat.com> - 1:2.56-368
- Fix a stack buffer overflow in deserialization of hooks (RT#130635)
- Fix a memory leak of a class name from retrieve_hook() on an exception
  (RT#130635)

* Tue Dec 20 2016 Petr Pisar <ppisar@redhat.com> - 1:2.56-367
- Fix crash in Storable when deserializing malformed code reference
  (RT#68348, RT#130098)

* Wed Aug 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.56-366
- Avoid loading optional modules from default . (CVE-2016-1238)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.56-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.56-1
- 2.56 bump in order to dual-live with perl 5.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.53-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.53-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.53-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.53-2
- Perl 5.22 rebuild

* Wed May 06 2015 Petr Pisar <ppisar@redhat.com> - 1:2.53-1
- 2.53 bump in order to dual-live with perl 5.22

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.51-4
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.51-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 2.51-1
- 2.51 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.45-1
- 2.45 bump

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.39-3
- Link minimal build-root packages against libperl.so explicitly

* Tue Jun 11 2013 Petr Pisar <ppisar@redhat.com> - 2.39-2
- Do not export private libraries

* Fri May 24 2013 Petr Pisar <ppisar@redhat.com> 2.39-1
- Specfile autogenerated by cpanspec 1.78.
