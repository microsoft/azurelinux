# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run prefork and optional test
%if ! (0%{?rhel})
%{bcond_without perl_Module_ScanDeps_enables_prefork}
%{bcond_without perl_Module_ScanDeps_enables_optional_tests}
%else
%{bcond_with perl_Module_ScanDeps_enables_prefork}
%{bcond_with perl_Module_ScanDeps_enables_optional_tests}
%endif

Name:           perl-Module-ScanDeps
Summary:        Recursively scan Perl code for dependencies
Version:        1.37
Release:        3%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Module-ScanDeps
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
# CPANPLUS::Backend is optional and not used by tests
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# Digest::MD5 is optional and not used by tests
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
# Getopt::Long not used by tests
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Metadata)
# Storable is optional and not used by tests
# subs not used by tests
# Text::ParseWords not used by tests
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
# VMS::Filespec never used
# Tests:
BuildRequires:  perl(autouse)
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(blib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(if)
BuildRequires:  perl(IPC::Run3) >= 0.048
BuildRequires:  perl(less)
BuildRequires:  perl(lib)
BuildRequires:  perl(Net::FTP)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Requires)
# Optional tests:
%if %{with perl_Module_ScanDeps_enables_optional_tests}
BuildRequires:  perl(Module::Pluggable)
%if !%{defined perl_bootstrap} && %{with perl_Module_ScanDeps_enables_prefork}
# Cycle: perl-Module-ScanDeps → perl-prefork → perl-Perl-MinimumVersion
# → perl-Perl-Critic → perl-Pod-Spell → perl-File-ShareDir-ProjectDistDir
# → perl-Path-Tiny → perl-Unicode-UTF8 → perl-Module-Install
# → perl-Module-ScanDeps
BuildRequires:  perl(prefork)
%endif
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(B)
Requires:       perl(DynaLoader)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(File::Find)
Requires:       perl(FindBin)
Requires:       perl(Text::ParseWords)
Recommends:     perl(Digest::MD5)
Recommends:     perl(Storable)
Suggests:       perl(CPANPLUS::Backend)

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}/%{name}
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_libexecdir}/%{name}/t/data
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Utils\\)

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(AutoLoader)
Requires:       perl(autouse)
Requires:       perl(Carp)
Requires:       perl(if)
Requires:       perl(less)
Requires:       perl(Net::FTP)
# Optional tests:
%if %{with perl_Module_ScanDeps_enables_optional_tests}
Requires:       perl(Module::Pluggable)
%if !%{defined perl_bootstrap} && %{with perl_Module_ScanDeps_enables_prefork}
Requires:       perl(prefork)
%endif
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Module-ScanDeps-%{version}

# Help file to recognise the Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm -f %{buildroot}%{_libexecdir}/%{name}/t/0-pod.t
perl -i -pe 's{ "-Mblib",}{}' %{buildroot}%{_libexecdir}/%{name}/t/19-autosplit.t
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
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc AUTHORS Changes README
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
%{_mandir}/man3/Module::ScanDeps.3pm*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.37-1
- 1.37 bump (rhbz#2327393); Fix CVE-2024-10224

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.35-1
- 1.35 bump (rhbz#2248014)

* Thu Oct 05 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-2
- Add test BR perl(AutoLoader) (rhbz#2242265)

* Mon Sep 25 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.34-1
- 1.34 bump (rhbz#2240459)

* Wed Aug 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.33-1
- 1.33 bump (rhbz#2229212)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.32-1
- 1.32 bump (rhbz#2219879)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-8
- Perl 5.36 re-rebuild of bootstrapped packages

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-7
- Perl 5.36 rebuild

* Thu Apr 21 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-6
- Add build-condition for optional tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-2
- Perl 5.34 rebuild

* Thu Apr 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.31-1
- 1.31 bump
- Package tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-2
- Do not use optional perl(prefork) for ELN

* Thu Jan 14 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-1
- 1.30 bump

* Wed Aug 19 2020 Petr Pisar <ppisar@redhat.com> - 1.29-1
- 1.29 bump

* Thu Aug 06 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.28-1
- 1.28 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-9
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-8
- Perl 5.32 rebuild

* Thu Mar 12 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-7
- Add BRs: perl(less), perl(Carp)
- Use make_* macros

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.27-1
- 1.27 bump

* Fri Dec 14 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.26-1
- 1.26 bump

* Tue Aug 21 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.25-1
- 1.25 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-5
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-4
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.24-1
- 1.24 bump

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.23-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 18 2016 Petr Pisar <ppisar@redhat.com> - 1.23-1
- 1.23 bump (license changed to "GPL+ or Artistic")

* Mon Sep 19 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.22-1
- 1.22 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-2
- Perl 5.24 rebuild

* Tue Apr 05 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-1
- 1.21 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Petr Šabata <contyk@redhat.com> - 1.20-1
- 1.20 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.19-2
- Perl 5.22 rebuild

* Thu May 28 2015 Petr Šabata <contyk@redhat.com> - 1.19-1
- 1.19 bump

* Fri Jan 30 2015 Petr Šabata <contyk@redhat.com> - 1.18-1
- 1.18 bump

* Tue Nov 04 2014 Petr Pisar <ppisar@redhat.com> - 1.17-1
- 0.17 bump

* Mon Sep 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.20 rebuild

* Mon Aug 25 2014 Petr Pisar <ppisar@redhat.com> - 1.15-1
- 1.15 bump

* Mon Aug 11 2014 Petr Šabata <contyk@redhat.com> - 1.14-1
- 1.14 bump
- Add the bundled Module::Install dependencies to the BR list

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Petr Pisar <ppisar@redhat.com> - 1.13-2
- Break build-cycle: perl-Module-ScanDeps → perl-prefork
  → perl-Perl-MinimumVersion → perl-Perl-Critic → perl-Pod-Spell
  → perl-File-ShareDir-ProjectDistDir → perl-Path-Tiny → perl-Unicode-UTF8
  → perl-Module-Install → perl-Module-ScanDeps

* Fri Jan 03 2014 Petr Pisar <ppisar@redhat.com> - 1.13-1
- 1.13 bump

* Mon Oct  7 2013 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Fix test broken by indirect base.pm disuse (CPAN RT#89000)
  - New %%Preload rule for Net::HTTPS (e.g. used by LWP::Protocol::https)
    - Look for IO::Socket::SSL or Net::SSL
  - New %%Preload rule for YAML::Any
    - Try to figure out what YAML::Any would have used
      (using YAML::Any->implementation)
    - As fallback, include anything below YAML
- Make %%files list more explicit
- Drop redundant %%{?perl_default_filter}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.10-3
- Perl 5.18 rebuild

* Tue Feb  5 2013 Paul Howarth <paul@city-fan.org> - 1.10-2
- Revert to using bundled Module::Install to avoid build dependency cycles
  (#906007)

* Tue Oct 23 2012 Petr Pisar <ppisar@redhat.com> - 1.10-1
- 1.10 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 1.08-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Petr Šabata <contyk@redhat.com> - 1.08-1
- 1.08 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Petr Šabata <contyk@redhat.com> - 1.07-1
- 1.07 bump

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 1.06-1
- 1.06 bump

* Thu Nov 03 2011 Petr Sabata <contyk@redhat.com> - 1.05-1
- 1.05 bump

* Mon Jul 25 2011 Petr Sabata <contyk@redhat.com> - 1.04-1
- 1.04 bump

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.02-2
- Perl mass rebuild

* Thu May  5 2011 Petr sabata <psabata@redhat.com> - 1.02-1
- 1.02 bump (rhbz#691369)
- Removing now obsolete Buildroot and defattr
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.98-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.98)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(File::Temp) (version 0)
- added a new req on perl(Module::Build::ModuleInfo) (version 0)
- added a new req on perl(version) (version 0)

* Fri Jun 11 2010 Petr Sabata <psabata@redhat.com> - 0.97-1
- Update to the latest version

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.95-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.95-1
- auto-update to 0.95 (by cpan-spec-update 0.01)
- add perl_default_filter (pro forma)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.89-1
- Update to 0.89.
- BR Test::More and prefork.
- Improve description.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.84-1
- Update to 0.84.

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.82-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.82-1
- Update to 0.82.
- BR version.

* Thu Jan 24 2008 Steven Pritchard <steve@kspei.com> 0.81-1
- Update to 0.81.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.
- BR ExtUtils::MakeMaker.

* Wed Jun 27 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.75-1
- Update to 0.75.

* Sat May  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.74-1
- Update to 0.74.

* Sat Mar 31 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.73-1
- Update to 0.73.

* Sun Feb  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.72-1
- Update to 0.72.
- Added perl(Module::Pluggable) to the build requirements list (t/2-pluggable.t).

* Fri Jan  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.71-1
- Update to 0.71.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.70-1
- Update to 0.70.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.69-1
- Update to 0.69.

* Sat Oct 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.68-1
- Update to 0.68.

* Sun Sep 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.66-1
- Update to 0.66.

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.64-1
- Update to 0.64.

* Mon Sep  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-1
- Update to 0.63.

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.62-1
- Update to 0.62.

* Sat Jul  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.61-1
- Update to 0.61.

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.60-1
- Update to 0.60.

* Sun May  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.59-2
- Source URL corrected (failed to detect the maintainer change).

* Wed May  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.59-1
- Update to 0.59.

* Thu Mar 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.57-1
- Update to 0.57.

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.56-1
- Update to 0.56.

* Tue Jan 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.53-1
- Update to 0.53.

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.51-1
- Update to Fedora Extras Template.

* Sat Jan 08 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.51-0.fdr.1
- First build.
