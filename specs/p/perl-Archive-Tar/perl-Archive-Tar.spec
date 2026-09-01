# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Archive_Tar_enables_optional_test
%else
%bcond_with perl_Archive_Tar_enables_optional_test
%endif

Name:           perl-Archive-Tar
Version:        3.04
Release:        521%{?dist}
Summary:        A module for Perl manipulation of .tar files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Archive-Tar
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Archive-Tar-%{version}.tar.gz
# Remove annoying sleep after warnings in the build script
Patch0:         Archive-Tar-2.02-Do-not-sleep-in-Makefile.PL.patch
BuildArch:      noarch
# Most of the BRS are needed only for tests, compression support at run-time
# is optional soft dependency.
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# File::Copy not used
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Zlib) >= 1.01
BuildRequires:  perl(Pod::Usage)
# Time::Local not used on Linux
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Optional run-time:
BuildRequires:  perl(IO::Compress::Bzip2) >= 2.015
%if !%{defined perl_bootstrap}
BuildRequires:  perl(IO::Compress::Xz)
%endif
# IO::String not used if perl supports useperlio which is true
# Use Compress::Zlib's version for IO::Uncompress::Bunzip2
BuildRequires:  perl(IO::Uncompress::Bunzip2) >= 2.015
%if !%{defined perl_bootstrap}
BuildRequires:  perl(IO::Uncompress::UnXz)
BuildRequires:  perl(Text::Diff)
%endif
# Tests:
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Harness) >= 2.26
BuildRequires:  perl(Test::More)
# Optional tests:
%if %{with perl_Archive_Tar_enables_optional_test} && !%{defined perl_bootstrap}
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Test::Pod) >= 0.95
%endif
Requires:       perl(IO::Zlib) >= 1.01
# Optional run-time:
Requires:       perl(IO::Compress::Bzip2) >= 2.015
%if !%{defined perl_bootstrap}
Requires:       perl(IO::Compress::Xz)
%endif
# IO::String not used if perl supports useperlio which is true
# Use Compress::Zlib's version for IO::Uncompress::Bunzip2
Requires:       perl(IO::Uncompress::Bunzip2) >= 2.015
%if !%{defined perl_bootstrap}
Requires:       perl(IO::Uncompress::UnXz)
Requires:       perl(Text::Diff)
%endif

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(IO::Zlib\\)$

%description
Archive::Tar provides an object oriented mechanism for handling tar
files.  It provides class methods for quick and easy files handling
while also allowing for the creation of tar file objects for custom
manipulation.  If you have the IO::Zlib module installed, Archive::Tar
will also support compressed or gzipped tar files.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl(ExtUtils::MakeMaker)
Requires:       perl(IPC::Cmd)
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Archive-Tar-%{version}
%patch -P0 -p1

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
rm %{buildroot}%{_libexecdir}/%{name}/t/99_pod.t
mkdir -p %{buildroot}%{_libexecdir}/%{name}/bin
for F in ptar ptardiff ptargrep; do
    ln -s %{_bindir}/"$F" %{buildroot}%{_libexecdir}/%{name}/bin
done
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
make test

%files
%doc CHANGES README
%{_bindir}/ptar*
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive::Tar*.3*
%{_mandir}/man1/ptar*.1*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.04-521
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-520
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-519
- Increase release to favour standalone package

* Wed Feb 26 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.04-1
- 3.04 bump (rhbz#2347586)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.02-513
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.02-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.02-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.02-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.02-3
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.02-2
- Perl 5.38 rebuild

* Thu Apr 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.02-1
- 3.02 bump

* Mon Mar 27 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.00-1
- 3.00 bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.40-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.40-488
- Increase release to favour standalone package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.40-1
- 2.40 bump
- Package tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-477
- Increase release to favour standalone package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.38-2
- Perl 5.32 re-rebuild of bootstrapped packages

* Thu Jun 25 2020 Petr Pisar <ppisar@redhat.com> - 2.38-1
- 2.38 bump

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-456
- Increase release to favour standalone package

* Fri Feb 14 2020 Petr Pisar <ppisar@redhat.com> - 2.36-2
- Do not require non-core IO::Compress::Xz and IO::Uncompress::UnXz modules on
  bootstrapping

* Mon Feb 03 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.36-1
- 2.36 bump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.32-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.32-438
- Increase release to favour standalone package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 13 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.32-1
- 2.32 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.30-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.30-416
- Increase release to favour standalone package

* Tue Jun 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.30-1
- 2.30 bump

* Fri Jun 08 2018 Petr Pisar <ppisar@redhat.com> - 2.28-1
- 2.28 bump
- Fixes CVE-2018-12015 (directory traversal) (bug #1588761)

* Wed Apr 04 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-6
- Do not run optional test on RHEL

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-2
- Perl 5.26 rebuild

* Mon May 15 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.26-1
- 2.26 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.24-1
- 2.24 bump

* Fri Dec 16 2016 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Fri Dec 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-1
- 2.20 bump

* Tue Nov 08 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.18-1
- 2.18 bump

* Wed Nov 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.16-1
- 2.16 bump

* Fri Oct 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.14-1
- 2.14 bump

* Mon Oct 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.12-1
- 2.12 bump

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 2.10-1
- 2.10 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.08-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.08-2
- Perl 5.24 rebuild

* Thu May 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.08-1
- 2.08 bump

* Tue Apr 26 2016 Petr Pisar <ppisar@redhat.com> - 2.06-1
- 2.06 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.04-348
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-2
- Perl 5.22 rebuild

* Tue Dec 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-1
- 2.04 bump

* Wed Dec 10 2014 Petr Pisar <ppisar@redhat.com> - 2.02-2
- Remove unneeded dependencies
- Remove annoying sleep after warnings in the build script

* Thu Sep 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-1
- 2.02 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-2
- Perl 5.20 rebuild

* Mon Jun 23 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-1
- 2.00 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.96-1
- 1.96 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.92-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.92-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.92-1
- 1.92 bump
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Update dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 18 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.90-2
- Add BRs perl(lib), perl(IO::File)

* Thu Sep 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.90-1
- 1.90 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.88-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.88-3
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Šabata <contyk@redhat.com> - 1.88-2
- 1.88 bump
- Drop command macros

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.84-2
- Omit optional Test::Pod tests on bootstrap

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.84-1
- 1.84 bump #802981 

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Petr Šabata <contyk@redhat.com> - 1.82-1
- 1.82 bump

* Fri Oct 14 2011 Petr Sabata <contyk@redhat.com> - 1.80-1
- 1.80 bump

* Fri Sep 09 2011 Petr Pisar <ppisar@redhat.com> - 1.78-1
- 1.78 bump
- Remove BuildRoot and defattr code from spec

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.76-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Petr Pisar <ppisar@redhat.com> - 1.76-1
- 1.76 bump

* Mon Jan 03 2011 Petr Sabata <psabata@redhat.com> - 1.74-1
- 1.74 bump

* Fri Nov 19 2010 Petr Pisar <ppisar@redhat.com> - 1.72-1
- 1.72 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 1.68-1
- 1.68 bump

* Tue Jul 13 2010 Petr Pisar <ppisar@redhat.com> - 1.64-1
- 1.64 bump

* Tue Jul 13 2010 Petr Pisar <ppisar@redhat.com> - 1.62-1
- 1.62 bump (bug #607687)

* Thu Aug 23 2007 Robin Norwood <rnorwood@redhat.com> - 1.34-1
- Upgrade to latest upstream version: 1.34
- Fix license tag
- Fix BuildRequires for ExtUtils::MakeMaker and Test::Pod

* Mon Jun 04 2007 Robin Norwood <rnorwood@redhat.com> - 1.32-1
- Upgrade to latest upstream version: 1.32

* Mon Mar 05 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-4
- Fix changelog

* Mon Feb 19 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-3
- Incorporate specfile improvements from Jose Oliveira.

* Fri Feb 16 2007 Robin Norwood <rnorwood@redhat.com> - 1.30-2
- Resolves: rhbz#226239 - Remove tabs from spec file for package review

* Tue Sep 19 2006 Robin Norwood <rnorwood@redhat.com> - 1.30-1
- Bump to 1.30

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.29-1.1
- rebuild

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 1.29-1
- Upgrade to upstream version 1.29

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.28-1
- Upgrade to upstream version 1.28
- Rebuild for perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 1.26

* Mon Apr 25 2005 Warren Togami <wtogami@redhat.com> - 1.23-4
- remove beehive workaround

* Sun Apr 03 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 1.23-1
- Update to 1.23.
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.08-3
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.08-1
- update to upstream 1.08

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Fri Feb 08 2002 cturner@redhat.com
- Specfile autogenerated

