# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global base_version 1.9764

Name:           perl-Time-HiRes
Epoch:          4
Version:        1.9778
Release:        520%{?dist}
Summary:        High resolution alarm, sleep, gettimeofday, interval timers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Time-HiRes
Source0:        https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Time-HiRes-%{base_version}.tar.gz
# Unbundled from perl 5.37.12
Patch0:         Time-HiRes-1.9764-Upgrade-to-1.9775.patch
# Unbundled from perl 5.40.0-RC1
Patch1:         Time-HiRes-1.9775-Upgrade-to-1.9777.patch
# Unbundled from perl 5.42.0
Patch2:         Time-HiRes-1.9777-Upgrade-to-1.9778.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::Constant)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests:
# t/utime.t executes df and mount on NetBSD only.
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(POSIX)
Requires:       perl(Carp)

%{?perl_default_filter}

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(t::Watchdog\\)

%description
The Time::HiRes module implements a Perl interface to the usleep, nanosleep,
ualarm, gettimeofday, and setitimer/getitimer system calls, in other words,
high resolution time and timers.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n Time-HiRes-%{base_version}

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
unset PERL_CORE
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# utime.t needs to write into temporary files. The solution is to copy the
# tests into a writable directory and execute them from there.
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
%doc Changes README TODO
%{perl_vendorarch}/auto/Time*
%{perl_vendorarch}/Time*
%{_mandir}/man3/Time::HiRes*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9778-520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9778-519
- Upgrade to 1.9778 as provided in perl-5.42.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9777-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9777-511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9777-510
- Increase release to favour standalone package

* Tue Jun 04 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9777-503
- Upgrade to 1.9777 as provided in perl-5.40.0-RC1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9775-502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9775-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9775-500
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9775-499
- Increase release to favour standalone package

* Tue Jun 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9775-1
- Upgrade to 1.9775 as provided in perl-5.37.12

* Thu May 18 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9774-1
- Upgrade to 1.9774 as provided in perl-5.37.11
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9770-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9770-489
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9770-488
- Upgrade to 1.9770 as provided in perl-5.35.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9767-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9767-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9767-478
- Perl 5.34 rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4:1.9767-477
- Upgrade to 1.9767 as provided in perl-5.34.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4:1.9764-460
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 09 2020 Petr Pisar <ppisar@redhat.com> - 4:1.9764-459
- Introduce an epoch not to regress comparing to RHEL (bug #1895852)

* Tue Aug 11 2020 Petr Pisar <ppisar@redhat.com> - 1.9764-458
- Use an upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9764-457
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.9764-456
- Upgrade to 1.9764 as provided in perl-5.32.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9760-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9760-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.9760-438
- Increase release to favour standalone package

* Tue Feb 19 2019 Petr Pisar <ppisar@redhat.com> - 1.9760-1
- 1.9760 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9759-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9759-417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.9759-416
- Increase release to favour standalone package

* Thu May 24 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.9759-1
- Upgrade to 1.9759 as provided in perl-5.28.0-RC1

* Thu Mar 22 2018 Petr Pisar <ppisar@redhat.com> - 1.9758-1
- 1.9758 bump

* Fri Mar 16 2018 Petr Pisar <ppisar@redhat.com> - 1.9757-1
- 1.9757 bump

* Thu Mar 15 2018 Petr Pisar <ppisar@redhat.com> - 1.9756-1
- 1.9756 bump

* Fri Feb 16 2018 Petr Pisar <ppisar@redhat.com> - 1.9754-1
- 1.9754 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9753-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Petr Pisar <ppisar@redhat.com> - 1.9753-1
- 1.9753 bump

* Fri Jan 05 2018 Petr Pisar <ppisar@redhat.com> - 1.9752-1
- 1.9752 bump

* Thu Jan 04 2018 Petr Pisar <ppisar@redhat.com> - 1.9751-1
- 1.9751 bump

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 1.9750-1
- 1.9750 bump

* Fri Dec 22 2017 Petr Pisar <ppisar@redhat.com> - 1.9749-1
- 1.9749 bump

* Thu Aug 17 2017 Petr Pisar <ppisar@redhat.com> - 1.9746-1
- 1.9746 bump

* Wed Aug 16 2017 Petr Pisar <ppisar@redhat.com> - 1.9745-1
- 1.9745 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9744-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.9744-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Petr Pisar <ppisar@redhat.com> - 1.9744-1
- 1.9742 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9742-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.9742-2
- Perl 5.26 rebuild

* Tue Apr 18 2017 Petr Pisar <ppisar@redhat.com> - 1.9742-1
- 1.9742 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9741-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Petr Pisar <ppisar@redhat.com> - 1.9741-1
- 1.9741 bump

* Mon Sep 26 2016 Petr Pisar <ppisar@redhat.com> - 1.9740-1
- 1.9740 bump

* Mon Jul 04 2016 Petr Pisar <ppisar@redhat.com> - 1.9739-1
- 1.9739 bump

* Mon Jun 27 2016 Petr Pisar <ppisar@redhat.com> - 1.9738-1
- 1.9738 bump

* Thu Jun 23 2016 Petr Pisar <ppisar@redhat.com> - 1.9737-1
- 1.9737 bump

* Wed Jun 22 2016 Petr Pisar <ppisar@redhat.com> - 1.9735-1
- 1.9735 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9733-365
- Increase release to favour standalone package

* Mon Apr 25 2016 Petr Pisar <ppisar@redhat.com> - 1.9733-1
- 1.9733 bump

* Mon Mar 14 2016 Petr Pisar <ppisar@redhat.com> - 1.9732-1
- 1.9732 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9728-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 1.9728-1
- 1.9728 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9726-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.9726-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.9726-311
- Perl 5.22 rebuild

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.9726-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.9726-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9726-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9726-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Petr Šabata <contyk@redhat.com> - 1.9726-1
- 1.9726 bugfix bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9725-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.9725-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.9725-273
- Perl 5.18 rebuild

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 1.9725-272
- Increase release number to superseed perl.spec's sub-package

* Fri Apr 26 2013 Petr Pisar <ppisar@redhat.com> 1.9725-1
- Specfile autogenerated by cpanspec 1.78.
