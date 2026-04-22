# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-generators
Version:        1.16
Release: 9%{?dist}
Summary:        RPM Perl dependencies generators
License:        GPL-1.0-or-later
URL:            http://jplesnik.fedorapeople.org/generators
Source0:        %{url}/generators-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
%if !%{defined perl_bootstrap}
# Break build cycle: reflexive dependency
BuildRequires:  perl-generators
%endif
BuildRequires:  perl-interpreter >= 4:5.22.0-351
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(Fedora::VSP)
BuildRequires:  perl(File::Basename)
# Optional run-time:
# version not used at tests
# Tests:
BuildRequires:  perl(lib)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple)
Requires:       perl-interpreter >= 4:5.22.0-351
# Per Perl packaging guidelines, build-requiring perl-generators should
# deliver Perl macros
Requires:       perl-macros
%if %{defined perl_bootstrap}
# Supply run-time dependencies manually when perl-generators is not available
Requires:       perl(Fedora::VSP)
Requires:       perl(File::Basename)
%endif
Recommends:     perl(version)

# The generators and attribute files were split from rpm-build
Conflicts:      rpm-build < 4.11.2-15

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(PerlNS\\)

%description
This package provides RPM Perl dependencies generators which are used for
getting provides and requires from Perl binaries and modules.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{defined perl_bootstrap}
# Supply run-time dependencies manually when perl-generators is not available
Requires:       perl(Exporter)
Requires:       perl(lib)
Requires:       perl(strict)
Requires:       perl(Test::More)
Requires:       perl(Test::Simple)
Requires:       perl(warnings)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n generators-%{version}
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor INSTALLVENDORSCRIPT=%{_rpmconfigdir} \
     NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs/
install -p -m 644 fileattrs/* '%{buildroot}%{_rpmconfigdir}/fileattrs'

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
perl -i -pe "s{bin/perl}{%{_rpmconfigdir}/perl}" %{buildroot}%{_libexecdir}/%{name}/t/lib/PerlNS.pm
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
make test

%files
%doc Changes TODO
%{_rpmconfigdir}/perl*
%{_rpmconfigdir}/fileattrs/perl*.attr

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.16-1
- 1.16 bump

* Tue Dec 06 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-1
- 1.15 bump
- Package tests

* Tue Aug 16 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.14-1
- 1.14 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-7
- Perl 5.36 re-rebuild of bootstrapped packages

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-2
- Perl 5.34 rebuild

* Mon May 10 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-1
- 1.13 bump

* Wed Feb 10 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.12-1
- 1.12 bump
  Add perltest.attr to generate dependencies from /usr/libexec/

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jul 30 2020 Petr Pisar <ppisar@redhat.com> - 1.11-9
- Specify all dependencies

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-7
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-6
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.30 rebuild

* Thu May 23 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-1
- 1.11 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-9
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-8
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.10-5
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-4
- Perl 5.26 re-rebuild of bootstrapped packages

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-1
- 1.10 bump

* Thu Jun 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-1
- 1.09 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 1.08-4
- Run-require perl-macros to provide the Perl macros for building Perl packages

* Wed Jun 01 2016 Petr Pisar <ppisar@redhat.com> - 1.08-3
- Supply run-time depenencies manually when perl-generators is not available on
  bootstrap

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-2
- Perl 5.24 rebuild

* Mon Mar 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-1
- 1.08 bump; Resolves BZ#1318658

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Add epoch to perl BR

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-1
- 1.07 bump
- Return perl version as normalized perl(:VERSION) symbol

* Tue Oct 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump

* Tue Sep 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-1
- 1.05 bump
- Resolves: bug #1267267

* Wed Jul 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-1
- 1.03 bump
- Update parcing of here-doc and quoted section

* Fri Dec 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-1
- 1.02 bump

* Tue Oct 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-1
- 1.01 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-1
- Introduce Perl generators as a standalone package
