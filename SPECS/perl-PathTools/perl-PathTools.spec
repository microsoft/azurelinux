# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 3.75

Name:           perl-PathTools
Version:        3.94
Release:        520%{?dist}
Summary:        PathTools Perl module (Cwd, File::Spec)
# Cwd.xs:                   BSD-3-Clause
# other files:              GPL-1.0-or-later OR Artistic-1.0-Perl
License:        ( GPL-1.0-or-later OR Artistic-1.0-Perl ) AND BSD-3-Clause
URL:            https://metacpan.org/release/PathTools
Source0:        https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/PathTools-%{base_version}.tar.gz
# Disable VMS tests (bug #973713)
Patch0:         PathTools-3.74-Disable-VMS-tests.patch
# Unbundled from perl 5.29.10
Patch1:         PathTools-3.75-Upgrade-to-3.78.patch
# Unbundled from perl 5.34.0
Patch2:         PathTools-3.78-Upgrade-to-3.80.patch
# Unbundled from perl 5.35.11
Patch3:         PathTools-3.80-Upgrade-to-3.84.patch
# Unbundled from perl 5.37.11
Patch4:         PathTools-3.84-Upgrade-to-3.89.patch
# Unbundled from perl 5.40.1
Patch5:         PathTools-3.89-Upgrade-to-3.91.patch
# Unbundled from perl 5.42.0
Patch6:         PathTools-3.91-Upgrade-to-3.94.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
# File::Basename not needed because of removed File::Spec::VMS
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
# Optional run-time:
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)
Requires:       perl(Carp)
Requires:       perl(Errno)
Requires:       perl(Scalar::Util)
# XSLoader is optional only because miniperl does not support XS. With perl we
# almost certainly want it.
Recommends:     perl(XSLoader)

%{?perl_default_filter}

%description
This is the combined distribution for the File::Spec and Cwd modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n PathTools-%{base_version}

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
rm lib/File/Spec/VMS.pm
#perl -i -ne 'print $_ unless m{^\Qlib/File/Spec/VMS.pm\E}' MANIFEST

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -pe "s#qr{blib}#qr{%{perl_vendorarch}}#" %{buildroot}%{_libexecdir}/%{name}/t/cwd.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%doc Changes
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cwd.pm
%{perl_vendorarch}/File/
%{_mandir}/man3/Cwd*
%{_mandir}/man3/File::Spec*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.94-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.94-519
- Upgrade to 3.94 as provided in 5.42.0

* Tue Jan 21 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.91-513
- Upgrade to 3.91 as provided in 5.40.1
  version of File::Spec was updated

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.91-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.91-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.91-510
- Increase release to favour standalone package

* Mon Jun 03 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.91-503
- Upgrade to 3.91 as provided in 5.40.0-RC1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.89-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.89-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.89-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.89-499
- Increase release to favour standalone package

* Thu May 18 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.89-1
- Upgrade to 3.89 as provided in perl-5.37.11
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.84-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.84-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.84-488
- Increase release to favour standalone package

* Thu May 12 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.84-1
- Upgrade to 3.84 as provided in perl-5.35.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.80-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.80-478
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 06 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.80-477
- Upgrade to 3.80 as provided in perl-5.34.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.78-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 05 2020 Petr Pisar <ppisar@redhat.com> - 3.78-458
- Fix an off-by-one in bsd_realpath()

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.78-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.78-456
- Increase release to favour standalone package

* Thu Feb 06 2020 Tom Stellard <tstellar@redhat.com> - 3.78-441
- Spec file cleanups: Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- https://fedoraproject.org/wiki/Perl/Tips#ExtUtils::MakeMake

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.78-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.78-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.78-438
- Increase release to favour standalone package

* Thu Apr 25 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.78-1
- Upgrade to 3.78 as provided in perl-5.29.10

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Petr Pisar <ppisar@redhat.com> - 3.75-1
- 3.75 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.74-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.74-416
- Increase release to favour standalone package

* Mon Feb 19 2018 Petr Pisar <ppisar@redhat.com> - 3.74-1
- 3.74 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.67-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.67-395
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.67-394
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.67-393
- Perl 5.26 rebuild

* Thu May 11 2017 Petr Pisar <ppisar@redhat.com> - 3.67-1
- Upgrade to 3.67 as provided in perl-5.25.12

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.63-367
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-366
- Avoid loading optional modules from default . (CVE-2016-1238)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-1
- 3.63 bump in order to dual-live with perl 5.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 3.62-1
- 3.62 bump

* Mon Jan 11 2016 Petr Pisar <ppisar@redhat.com> - 3.60-2
- Fix CVE-2015-8607 (File::Spec::canonpath() loses tain) (bug #1297455)

* Thu Nov 19 2015 Petr Pisar <ppisar@redhat.com> - 3.60-1
- 3.60 bump

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 3.59-1
- 3.59 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.56-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-2
- Perl 5.22 rebuild

* Mon Apr 27 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-1
- 3.56 bump in order to dual-live with Perl 5.22

* Tue Jan 13 2015 Petr Pisar <ppisar@redhat.com> - 3.47-311
- Require constant module

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-1
- 3.47 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 3.40-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.40-4
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.40-3
- Disable VMS test (bug #973713)

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 3.40-2
- Do not distribute File::Spec::VMS (bug #973713)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 3.40-1
- 3.40 bump

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 3.39.01-1
- 3.39_01 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.33-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.33-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 3.33-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.33-3
- Perl mass rebuild

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.33-2
- Own the %%{perl_vendorarch}/File dir.

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.33-1
- Specfile autogenerated by cpanspec 1.79.
