# Run optional test
%{bcond_without perl_FFI_Changes_enables_optional_test}

Name:           perl-FFI-CheckLib
Version:        0.31
Release:        7%{?dist}
Summary:        Check that a library is available for FFI
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/FFI-CheckLib
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/FFI-CheckLib-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.6
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Env)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
# File::Which is used from private functions which are only called on Darwin.
BuildRequires:  perl(List::Util) >= 1.33
# Tests:
# File::Which is a run-time dependency on Darwin only. The code is exhibited by a test,
# but never on Linux in production.
BuildRequires:  perl(File::Which)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test2::API) >= 1.302015
BuildRequires:  perl(Test2::Require::EnvVar) >= 0.000121
BuildRequires:  perl(Test2::Require::Module) >= 0.000121
BuildRequires:  perl(Test2::V0) >= 0.000121
%if %{with perl_FFI_Changes_enables_optional_test}
# Optional tests:
# Test/More.pl is not helpful
# FFI::Platypus not used
BuildRequires:  perl(Test2::Tools::Process)
%endif
Requires:       perl(DynaLoader)
Requires:       perl(File::Basename)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Test2::API|Test2::Require::EnvVar|Test2::Require::Module|Test2::V0)\\)$

# Remove private modules
%global __requires_exclude %{__requires_exclude}|^perl\\((Test2::Plugin::FauxOS|Test2::Tools::FauxDynaLoader|Test2::Tools::NoteStderr)\\)
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\((Alien::libbar|Test2::Plugin::FauxOS|Test2::Tools::FauxDynaLoader|Test2::Tools::NoteStderr)\\)

%description
This Perl module checks whether a particular dynamic library is available for
Foreign Function Interface (FFI) to use. It is modeled heavily on
Devel::CheckLib, but will find dynamic libraries even when development
packages are not installed. It also provides a find_lib function that will
return the full path to the found dynamic library, which can be feed directly
into FFI::Platypus or FFI::Raw.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# Tests:
# File::Which is a run-time dependency on Darwin only. The code is exhibited by a test,
# but never on Linux in production.
Requires:       perl(File::Which)
Requires:       perl(Test2::API) >= 1.302015
Requires:       perl(Test2::Require::EnvVar) >= 0.000121
Requires:       perl(Test2::Require::Module) >= 0.000121
Requires:       perl(Test2::V0) >= 0.000121

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n FFI-CheckLib-%{version}
%if !%{with perl_FFI_Changes_enables_optional_test}
rm t/ffi_checklib__exit.t
perl -i -ne 'print $_ unless m{\A\Qt/ffi_checklib__exit.t\E\b}' MANIFEST
%endif
# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
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
cp -a corpus t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
unset CIPSOMETHING FFI_CHECKLIB_PATH
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset CIPSOMETHING FFI_CHECKLIB_PATH
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
make test

%files
%license LICENSE
%doc Changes README
%dir %{perl_vendorlib}/FFI
%{perl_vendorlib}/FFI/CheckLib.pm
%{_mandir}/man3/FFI::CheckLib.*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Petr Pisar <ppisar@redhat.com> - 0.31-2
- Remove a bogus Alien::libbar RPM provide from perl-FFI-CheckLib-tests

* Fri Sep 30 2022 Petr Pisar <ppisar@redhat.com> - 0.31-1
- 0.31 bump

* Thu Sep 22 2022 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump

* Mon Sep 12 2022 Petr Pisar <ppisar@redhat.com> - 0.29-1
- 0.29 bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-2
- Perl 5.34 rebuild

* Mon May 17 2021 Petr Pisar <ppisar@redhat.com> - 0.28-1
- 0.28 bump
- Package the tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.32 rebuild

* Tue May 12 2020 Petr Pisar <ppisar@redhat.com> - 0.27-1
- 0.27 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Petr Pisar <ppisar@redhat.com> - 0.26-1
- 0.26 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Petr Pisar <ppisar@redhat.com> - 0.25-1
- 0.25 bump

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-2
- Perl 5.30 rebuild

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 0.24-1
- 0.24 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Petr Pisar <ppisar@redhat.com> - 0.23-1
- 0.23 bump

* Mon Oct 15 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-1
- 0.22 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.20-2
- Perl 5.28 rebuild

* Tue Jun 05 2018 Petr Pisar <ppisar@redhat.com> - 0.20-1
- 0.20 bump

* Thu May 31 2018 Petr Pisar <ppisar@redhat.com> - 0.19-1
- 0.19 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 26 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-1
- 0.18 bump

* Wed Aug 09 2017 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.26 rebuild

* Fri Mar 10 2017 Petr Pisar <ppisar@redhat.com> 0.15-1
- Specfile autogenerated by cpanspec 1.78.
