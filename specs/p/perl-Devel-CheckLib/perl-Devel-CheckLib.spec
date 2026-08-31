# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Devel_CheckLib_enables_optional_test
%else
%bcond_with perl_Devel_CheckLib_enables_optional_test
%endif

Name:           perl-Devel-CheckLib
Version:        1.16
Release:        15%{?dist}
Summary:        Check that a library is available

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Devel-CheckLib
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Text::ParseWords)
# Tests:
BuildRequires:  gcc
BuildRequires:  perl(blib)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.88
# Optional tests
%if %{with perl_Devel_CheckLib_enables_optional_test}
BuildRequires:  perl(Mock::Config)
%endif
# perl inherits the compiler flags it was built with, hence we need this on hardened systems
Requires:       redhat-rpm-config

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       gcc
# Optional tests
%if %{with perl_Devel_CheckLib_enables_optional_test}
Requires:       perl(Mock::Config)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Devel-CheckLib-%{version}

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
perl -i -ne 'print $_ unless m{\Q'-Mblib'\E}' %{buildroot}%{_libexecdir}/%{name}/t/cmdline-LIBS-INC.t
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests need to write into temporary files/directories.
# Copy the tests into a writable directory and execute them from there.
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
%doc CHANGES README TODO
%{_bindir}/use-devel-checklib
%{perl_vendorlib}/Devel*
%{_mandir}/man1/use-devel-checklib.1*
%{_mandir}/man3/Devel::CheckLib.3*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-9
- Move redhat-rpm-config from tests to main package

* Thu Jun 22 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-8
- Requires: redhat-rpm-config for tests

* Wed Jun 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-7
- Package tests

* Wed Jun 21 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-6
- Add test BR gcc to not skip the tests

* Wed Apr 12 2023 Michal Josef Špaček <mspacek@redhat.com> - 1.16-5
- Update license to SPDX format

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-2
- Perl 5.36 rebuild

* Fri May 27 2022 Denis Fateyev <denis@fateyev.com> - 1.16-1
- Update to 1.16

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-7
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-5
- Disable optional test on RHEL

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Denis Fateyev <denis@fateyev.com> - 1.14-1
- Update to 1.14

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-2
- Perl 5.28 rebuild

* Wed Jun 20 2018 Denis Fateyev <denis@fateyev.com> - 1.13-1
- Update to 1.13

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.26 rebuild

* Thu Jun 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-1
- Update to 1.11

* Tue Apr 11 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-1
- Update to 1.10

* Sat Mar 25 2017 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.09-1
- Update to 1.09 (bug #1435192).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Perl 5.24 rebuild

* Sat Apr  9 2016 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.07-1
- Update to 1.07.

* Sun Apr  3 2016 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.06-1
- Update to 1.06.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 19 2015 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.05-1
- Update to 1.05.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Sat Mar 21 2015 Jose Pedro Oliveira <jose.p.oliveira.oss at gmail.com> - 1.03-1
- Update to 1.03.

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.99-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.99-2
- Perl 5.18 rebuild

* Thu Apr  4 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99-1
- Update to 0.99.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Petr Pisar <ppisar@redhat.com> - 0.98-4
- Specify all dependencies
- Package TODO

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.98-2
- Perl 5.16 rebuild

* Sat Mar 17 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.98-1
- Update to 0.98.

* Mon Feb 27 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-1
- Update to 0.97.

* Fri Feb  3 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.96-1
- Update to 0.96.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.95-1
- Update to 0.95.

* Wed Oct 19 2011 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.94-1
- First build.
