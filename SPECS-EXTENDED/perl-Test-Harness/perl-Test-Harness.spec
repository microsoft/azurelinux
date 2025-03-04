Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Run optional tests
%if ! (0%{?rhel})
%bcond_without perl_Test_Harness_enables_optional_test
%else
%bcond_with perl_Test_Harness_enables_optional_test
%endif

Name:           perl-Test-Harness
Version:        3.50
Release:        2%{?dist}
Summary:        Run Perl standard test scripts with statistics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-Harness
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Test-Harness-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Remove hard-coded shell bangs
Patch0:         Test-Harness-3.38-Remove-shell-bangs.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::ParseWords)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Optional run-time:
BuildRequires:  perl(Encode)
# Keep Pod::Usage 1.12 really optional
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Time::HiRes)
# Tests:
BuildRequires:  perl(Data::Dumper)
# Dev::Null bundled for bootstrap
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
# Optional tests:
%if %{with perl_Test_Harness_enables_optional_test}
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(File::Temp)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(TAP::Formatter::HTML) >= 0.10
BuildRequires:  perl(TAP::Harness::Archive)
BuildRequires:  perl(YAML)
%endif
%endif
Suggests:       perl(Term::ANSIColor)
Suggests:       perl(Time::HiRes)

# Filter example dependencies
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}^%{_datadir}/doc
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_datadir}/doc

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(My.*\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(Dev::Null\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(EmptyParser\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(IO::c55Capture\\)
%global __requires_exclude %{__requires_exclude}|^perl\\(NoFork\\)

%description
This package allows tests to be run and results automatically aggregated and
output to STDOUT.

Although, for historical reasons, the Test-Harness distribution takes its name
from this module it now exists only to provide TAP::Harness with an interface
that is somewhat backwards compatible with Test::Harness 2.xx. If you're
writing new code consider using TAP::Harness directly instead.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Test-Harness-%{version}
%patch -P0 -p1

# Help generators to recognize Perl scripts
for F in `find t -name *.t -o -name *.pl`; do
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
rm %{buildroot}%{_libexecdir}/%{name}/t/000-load.t
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
%doc Changes Changes-2.64 examples README
%{perl_vendorlib}/App*
%{perl_vendorlib}/TAP*
%{perl_vendorlib}/Test*
%{_bindir}/prove
%{_mandir}/man1/prove*
%{_mandir}/man3/App::Prove*
%{_mandir}/man3/TAP::Base*
%{_mandir}/man3/TAP::Formatter*
%{_mandir}/man3/TAP::Harness*
%{_mandir}/man3/TAP::Object*
%{_mandir}/man3/TAP::Parser*
%{_mandir}/man3/Test::*

%files tests
%{_libexecdir}/%{name}

%changelog

%changelog
* Thu Dec 19 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 3.50-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Aug 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.50-1
- 3.50 bump (rhbz#2304673)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.48-512
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.48-511
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.48-510
- Increase release to favour standalone package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.48-1
- 3.48 bump (rhbz#2241802)

* Wed Aug 23 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.47-1
- 3.47 bump (rhbz#2231692)

* Wed Aug 09 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.46-1
- 3.46 bump (rhbz#2229823)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.44-501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-500
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-499
- Increase release to favour standalone package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.44-491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.44-490
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-489
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-488
- Increase release to favour standalone package

* Tue Apr 19 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.44-1
- 3.44 bump
- Package tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-480
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.43-479
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-478
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-477
- Increase release to favour standalone package

* Thu May 06 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.43-1
- Upgrade to 3.43 as provided in perl-5.34.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-459
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-457
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-456
- Increase release to favour standalone package

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-441
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-440
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-439
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-438
- Increase release to favour standalone package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-419
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.42-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-417
- Perl 5.28 re-rebuild of bootstrapped packages

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.42-416
- Increase release to favour standalone package

* Tue Mar 20 2018 Petr Pisar <ppisar@redhat.com> - 1:3.42-1
- 3.42 bump

* Wed Feb 28 2018 Petr Pisar <ppisar@redhat.com> - 1:3.41-1
- 3.41 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.39-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:3.39-2
- Perl 5.26 rebuild

* Thu Apr 06 2017 Petr Pisar <ppisar@redhat.com> - 3.39-1
- 3.39 bump

* Tue Mar 14 2017 Petr Pisar <ppisar@redhat.com> - 3.38-1
- 3.38 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-369
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 13 2016 Petr Pisar <ppisar@redhat.com> - 3.36-368
- Remove old obsoleting perl-TAP-Harness-Env

* Wed Aug 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.36-367
- Avoid loading optional modules from default . (CVE-2016-1238)

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.36-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.36-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 3.36-1
- 3.36 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.35-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.35-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.35-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.35-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Petr Pisar <ppisar@redhat.com> - 3.35-1
- 3.35 bump

* Thu Nov 13 2014 Petr Pisar <ppisar@redhat.com> - 3.34-1
- 3.34 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.33-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.33-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 3.33-1
- 3.33 bump

* Thu Jun 12 2014 Petr Pisar <ppisar@redhat.com> - 3.32-1
- 3.32 bump

* Mon Jun 09 2014 Petr Pisar <ppisar@redhat.com> - 3.31-1
- 3.31 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Petr Pisar <ppisar@redhat.com> - 3.30-2
- Obsolete perl-TAP-Harness-Env (bug #1067098)

* Mon Nov 18 2013 Petr Pisar <ppisar@redhat.com> - 3.30-1
- 3.30 bump

* Mon Oct 14 2013 Petr Pisar <ppisar@redhat.com> - 3.29-1
- 3.29 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.28-2
- Perl 5.18 rebuild

* Fri May 03 2013 Petr Pisar <ppisar@redhat.com> - 3.28-1
- 3.28 bump

* Thu May 02 2013 Petr Pisar <ppisar@redhat.com> - 3.27-1
- 3.27 bump

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> 3.26-1
- Specfile autogenerated by cpanspec 1.78.
