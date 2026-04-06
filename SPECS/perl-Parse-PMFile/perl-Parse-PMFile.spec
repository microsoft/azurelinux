# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run optional test
%bcond_without perl_Parse_PMFile_enables_optional_test

Name:           perl-Parse-PMFile
Version:        0.47
Release:        4%{?dist}
Summary:        Parses .pm file as PAUSE does
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Parse-PMFile
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Parse-PMFile-%{version}.tar.gz
# Remove useless dependency on ExtUtils::MakeMaker::CPANfile
Patch0:         Parse-PMFile-0.41-Do-not-use-ExtUtils-MakeMaker-CPANfile.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Dumpvalue)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(JSON::PP) >= 2.00
BuildRequires:  perl(Safe)
BuildRequires:  perl(version) >= 0.83
# Tests
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Opcode)
BuildRequires:  perl(Test::More) >= 0.88
%if %{with perl_Parse_PMFile_enables_optional_test}
# Optional tests
# PAUSE::Permissions 0.08 not yet packaged
BuildRequires:  perl(version::vpp)
# Test::Pod not used
# Test::Pod::Coverage not used
%endif
Requires:       perl(JSON::PP) >= 2.00
Requires:       perl(version) >= 0.83

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((JSON::PP|version)\\)$

%description
The most of the code of this module is taken from the PAUSE code as of
April 2013 almost verbatim. Thus, the heart of this module should be quite
stable. However, I made it not to use pipe ("-|") as well as I stripped
database-related code. If you encounter any issue, that's most probably
because of my modification.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Parse-PMFile-%{version}
%patch -P0 -p1
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
rm -f %{buildroot}%{_libexecdir}/%{name}/t/99_pod*
for F in 10_self_check.t 80_version_overload.t 81_version_overload_with_explicit_vpp.t; do
    perl -i -pe 's{\$FindBin::Bin/../lib/}{%{perl_vendorlib}/}' %{buildroot}%{_libexecdir}/%{name}/t/$F
done
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset TEST_POD
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%doc Changes README
%{perl_vendorlib}/Parse*
%{_mandir}/man3/Parse::PMFile*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 23 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-1
- 0.47 bump (rhbz#2276274)

* Mon Apr 15 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-1
- 0.46 bump (rhbz#2275122)

* Thu Jan 25 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.45-1
- 0.45 bump (rhbz#2259976)

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.44-1
- 0.44 bump
- Package tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-1
- 0.43 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-3
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-1
- 0.42 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-7
- Perl 5.28 rebuild

* Fri Jun 01 2018 Petr Pisar <ppisar@redhat.com> - 0.41-6
- Remove useless dependency on ExtUtils::MakeMaker::CPANfile
- Modernize the spec file

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.41-1
- 0.41 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-2
- Perl 5.24 rebuild

* Mon Feb 22 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-1
- 0.40 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-1
- 0.39 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-2
- Perl 5.22 rebuild

* Mon Apr 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.36-1
- 0.36 bump

* Tue Feb 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.35-1
- 0.35 bump

* Mon Dec 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.33-1
- 0.33 bump

* Thu Dec 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-1
- 0.31 bump

* Mon Dec 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-1
- 0.30 bump

* Mon Oct 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.29-1
- 0.29 bump

* Wed Oct 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-1
- 0.28 bump

* Tue Sep 23 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-1
- Specfile autogenerated by cpanspec 1.78.
