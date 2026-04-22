# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional tests
%if ! (0%{?rhel})
%bcond_without perl_Compress_Bzip2_enables_optional_test
%else
%bcond_with perl_Compress_Bzip2_enables_optional_test
%endif

Name:           perl-Compress-Bzip2
Version:        2.28
Release: 25%{?dist}
Summary:        Interface to Bzip2 compression library
# bzlib-src/win-tst-dlltest.c (unbundled):  Public Domain
# bzlib-src/LICENSE (unbundled):            BSD-4-Clause
# bzlib-src/manual.ps (unbundled):          GPL+ with exception and OFL
# other files:                              GPL-1.0-or-later OR Artistic-1.0-Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Compress-Bzip2
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Compress-Bzip2-%{version}.tar.gz
BuildRequires:  bzip2-devel >= 1.0.5
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.1
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# VMS::Filespec not needed
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant) >= 1.04
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Cwd)
# Memory::Usage not used
BuildRequires:  perl(Test::More)
# Test::Kwalitee not used
# Optional tests:
%if !%{defined perl_bootstrap} && %{with perl_Compress_Bzip2_enables_optional_test}
BuildRequires:  perl(Test::LeakTrace)
%endif
Requires:       perl(constant) >= 1.04

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(constant\\)$

%description
The Compress::Bzip2 module provides a Perl interface to the Bzip2 compression
library. A relevant subset of the functionality provided by Bzip2 is available
in Compress::Bzip2. Compress::Bzip2 is not well integrated into PerlIO, use
the preferred IO::Compress::Bzip2 instead.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       bash
Requires:       bzip2
Requires:       coreutils
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Compress-Bzip2-%{version}
# Remove bundled bzip2 library
find bzlib-src -mindepth 1 -type f \! -name 'sample*' -delete
perl -i -ne 'print $_ unless m{^bzlib-src/}' MANIFEST
find bzlib-src -type f >>MANIFEST
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 \
    OPTIMIZE="$RPM_OPT_FLAGS"
%make_build

%install
%make_install
# Install tests
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
cp -a t %{buildroot}/%{_libexecdir}/%{name}
# Remove author tests
rm -f %{buildroot}/%{_libexecdir}/%{name}/t/900*
# Remove memory usage test
rm -f %{buildroot}/%{_libexecdir}/%{name}/t/090-memory-usage.pl
mkdir -p %{buildroot}/%{_libexecdir}/%{name}/bzlib-src
for F in sample0.bz2 sample0.ref sample1.bz2 sample1.ref sample2.bz2 sample2.ref sample3.bz2 sample3.ref; do
    cp "bzlib-src/$F" %{buildroot}/%{_libexecdir}/%{name}/bzlib-src/
done
cp -a config.in %{buildroot}/%{_libexecdir}/%{name}/
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
%{_fixperms} %{buildroot}

%check
make test

%files
%license COPYING
%doc ANNOUNCE Changes NEWS README.md
%{perl_vendorarch}/Compress/
%{perl_vendorarch}/auto/Compress/
%{_mandir}/man3/*.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-23
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-22
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-19
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-18
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-14
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-13
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Michal Josef Špaček <mspacek@redhat.com> - 2.28-11
- Cleanup build in spec file
- Package tests
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-9
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-8
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-5
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.28-4
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Petr Pisar <ppisar@redhat.com> - 2.28-1
- 2.28 bump

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27-4
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27-3
- Perl 5.32 rebuild

* Wed May 27 2020 Petr Pisar <ppisar@redhat.com> - 2.27-2
- A dummy release to overcome a Koji failure

* Wed May 27 2020 Petr Pisar <ppisar@redhat.com> - 2.27-1
- 2.27 bump

* Tue Feb 04 2020 Petr Pisar <ppisar@redhat.com> - 2.26-16
- NO_PERLLOCAL=1 needs a recent ExtUtils::MakeMaker

* Tue Feb 04 2020 Tom Stellard <tstellar@redhat.com> - 2.26-15
- Use make_build macro
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-12
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-8
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-7
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-2
- Perl 5.26 rebuild

* Tue Apr 11 2017 Petr Pisar <ppisar@redhat.com> - 2.26-1
- 2.26 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Petr Pisar <ppisar@redhat.com> - 2.24-1
- 2.24 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.22-2
- Perl 5.22 rebuild

* Thu Feb 19 2015 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Fri Jan 30 2015 Petr Pisar <ppisar@redhat.com> - 2.20-1
- 2.20 bump

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 2.19-2
- Do not build-require version module

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 2.19-1
- 2.19 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 2.18-1
- 2.18 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 2.17-1
- 2.17 bump
- License changed to (GPL+ or Artistic)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.16-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Petr Pisar <ppisar@redhat.com> - 2.16-1
- 2.16 bump

* Mon Apr 08 2013 Petr Pisar <ppisar@redhat.com> - 2.15-1
- 2.15 bump

* Thu Apr 04 2013 Petr Pisar <ppisar@redhat.com> - 2.13-1
- 2.13 bump

* Wed Mar 27 2013 Petr Pisar <ppisar@redhat.com> - 2.10-1
- 2.10 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.09-15
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-10
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.09-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-6.2
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.09-5.2
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-4.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-4
- Rebuild for FC6.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-3
- Rebuild for FC5 (perl 5.8.8).

* Mon Jan  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-2
- Applied two of the Ville's suggestions (#177166): trimmed down
  the description to the first paragraph and added the file ANNOUNCE
  as documentation.

* Thu Aug 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-1
- Update to 2.09.

* Mon May 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.07-1
- Update to 2.07.

* Mon Apr 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-1
- Update to 2.04.

* Sun Apr 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.03-1
- Update to 2.03.

* Sun Apr 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.00-1
- Update to 2.00.

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- First build.
