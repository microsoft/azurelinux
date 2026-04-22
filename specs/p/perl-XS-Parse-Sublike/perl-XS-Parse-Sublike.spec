# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%if 0%{?rhel}
%bcond_with perl_XS_Parse_Sublike_enables_optional_tests
%else
%bcond_without perl_XS_Parse_Sublike_enables_optional_tests
%endif

# Break a build cycle with perl-Object-Pad
%if %{with perl_XS_Parse_Sublike_enables_optional_tests} && !%{defined perl_bootstrap}
%global optional_tests 1
%else
%global optional_tests 0
%endif

Name:           perl-XS-Parse-Sublike
Version:        0.41
Release: 2%{?dist}
Summary:        XS functions to assist in parsing sub-like syntax
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/XS-Parse-Sublike
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/XS-Parse-Sublike-%{version}.tar.gz
Source1:        macros.perl-XS-Parse-Sublike
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.16
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
# File::ShareDir 1.00 not used at tests
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(feature)
BuildRequires:  perl(Sub::Util)
BuildRequires:  perl(Test2::Require::Module)
BuildRequires:  perl(Test2::V0) >= 0.000147
%if %{optional_tests}
# Optional tests:
%global Future_AsyncAwait_min_ver 0.66
BuildRequires:  perl(Future::AsyncAwait) >= %{Future_AsyncAwait_min_ver}
%global Object_Pad_min_ver 0.800
BuildRequires:  perl(Object::Pad) >= %{Object_Pad_min_ver}
BuildRequires:  perl(Test::Pod) >= 1
%endif
# This module maintains multiple ABIs whose compatibility is checked at
# run-time by S_boot_xs_parse_sublike() compiled into the users of this module.
# This ABI range is defined with XS::Parse::Sublike/ABIVERSION_MIN and
# XS::Parse::Sublike/ABIVERSION_MAX in lib/XS/Parse/Sublike.xs.
Provides:       perl(:XS_Parse_Sublike_ABI) = 5
Provides:       perl(:XS_Parse_Sublike_ABI) = 6
Provides:       perl(:XS_Parse_Sublike_ABI) = 7
Provides:       perl(:XS_Parse_Sublike_ABI) = 8

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Future::AsyncAwait|Object::Pad)\\)$
# Filter private modules
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(testcase\\)
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(testcase\\)

%description
This module provides some XS functions to assist in writing parsers for
sub-like syntax, primarily for authors of keyword plugins using the
PL_keyword_plugin hook mechanism.

%package Builder
Summary:        Build-time support for XS::Parse::Sublike
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-interpreter
Requires:       perl(File::ShareDir) >= 1.00
Requires:       perl(File::Spec)
Requires:       perl(XS::Parse::Sublike)
# Subpackaged in 0.13
Conflicts:      %{name}%{?_isa} < 0.13

%description Builder
This module provides a build-time helper to assist authors writing XS modules
that use XS::Parse::Sublike. It prepares a Module::Build-using distribution to
be able to make use of XS::Parse::Sublike.

%package tests
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(XSLoader)
%if %{optional_tests}
# Optional tests:
Requires:       perl(Future::AsyncAwait) >= %{Future_AsyncAwait_min_ver}
Requires:       perl(Object::Pad) >= %{Object_Pad_min_ver}
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%autosetup -p1 -n XS-Parse-Sublike-%{version}
%if !%{optional_tests}
for F in t/80extended+async.t t/80extended+Object-Pad.t t/99pod.t; do
    rm "$F"
    perl -i -ne 'print $_ unless m{^\Q'"$F"'\E}' MANIFEST
done
%endif
chmod +x t/*.t

%build
perl Build.PL --installdirs=vendor --optimize="$RPM_OPT_FLAGS"
./Build
# Build object files for tests now. They are installed into tests subpackage.
./Build testlib

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
install -D -m 0644 -t %{buildroot}%{_rpmmacrodir} %{SOURCE1}
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
find %{buildroot}%{_libexecdir}/%{name} -type f \
    \( -name '*.bs' -o -name '*.c' -o -name '*.o' \) -delete
%if %{optional_tests}
rm %{buildroot}%{_libexecdir}/%{name}/t/99pod.t
%endif
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
./Build test

%files
%license LICENSE
%doc Changes README
%dir %{perl_vendorarch}/auto/XS
%dir %{perl_vendorarch}/auto/XS/Parse
%{perl_vendorarch}/auto/XS/Parse/Sublike
%dir %{perl_vendorarch}/Sublike
%{perl_vendorarch}/Sublike/Extended.pm
%dir %{perl_vendorarch}/XS
%dir %{perl_vendorarch}/XS/Parse
%{perl_vendorarch}/XS/Parse/Sublike.pm
%{_mandir}/man3/Sublike::Extended.*
%{_mandir}/man3/XS::Parse::Sublike.*

%files Builder
%dir %{perl_vendorarch}/auto/share
%dir %{perl_vendorarch}/auto/share/module
%{perl_vendorarch}/auto/share/module/XS-Parse-Sublike
%{perl_vendorarch}/XS/Parse/Sublike
%{_mandir}/man3/XS::Parse::Sublike::*
%{_rpmmacrodir}/macros.%{name}

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jan 02 2026 Petr Pisar <ppisar@redhat.com> - 0.41-1
- 0.41 bump

* Wed Nov 19 2025 Petr Pisar <ppisar@redhat.com> - 0.40-1
- 0.40 bump

* Mon Sep 15 2025 Petr Pisar <ppisar@redhat.com> - 0.39-1
- 0.39 bump

* Thu Aug 14 2025 Petr Pisar <ppisar@redhat.com> - 0.38-1
- 0.38 bump

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-4
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-3
- Perl 5.42 rebuild

* Fri May 02 2025 Petr Pisar <ppisar@redhat.com> - 0.37-2
- Fix RPM-providing ABI 8

* Mon Feb 10 2025 Petr Pisar <ppisar@redhat.com> - 0.37-1
- 0.37 bump

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Petr Pisar <ppisar@redhat.com> - 0.36-1
- 0.36 bump

* Wed Jan 08 2025 Petr Pisar <ppisar@redhat.com> - 0.35-1
- 0.35 bump

* Tue Jan 07 2025 Petr Pisar <ppisar@redhat.com> - 0.34-1
- 0.34 bump

* Thu Jan 02 2025 Petr Pisar <ppisar@redhat.com> - 0.33-1
- 0.33 bump

* Mon Oct 21 2024 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump

* Tue Oct 15 2024 Petr Pisar <ppisar@redhat.com> - 0.29-1
- 0.29 bump

* Wed Oct 09 2024 Petr Pisar <ppisar@redhat.com> - 0.28-1
- 0.28 bump

* Tue Sep 24 2024 Petr Pisar <ppisar@redhat.com> - 0.27-1
- 0.27 bump

* Mon Sep 23 2024 Petr Pisar <ppisar@redhat.com> - 0.26-1
- 0.26 bump

* Thu Sep 19 2024 Petr Pisar <ppisar@redhat.com> - 0.25-1
- 0.25 bump

* Thu Aug 15 2024 Petr Pisar <ppisar@redhat.com> - 0.23-1
- 0.23 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Petr Pisar <ppisar@redhat.com> - 0.22-1
- 0.22 bump

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-5
- Perl 5.40 re-rebuild of bootstrapped packages

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.21-4
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Petr Pisar <ppisar@redhat.com> - 0.21-1
- 0.21 bump

* Mon Sep 11 2023 Petr Pisar <ppisar@redhat.com> - 0.20-1
- 0.20 bump

* Fri Sep 08 2023 Petr Pisar <ppisar@redhat.com> - 0.19-1
- 0.19 bump

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-2
- Perl 5.38 rebuild

* Thu Jun 15 2023 Petr Pisar <ppisar@redhat.com> - 0.18-1
- 0.18 bump

* Tue Mar 21 2023 Petr Pisar <ppisar@redhat.com> - 0.17-1
- 0.17 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.16-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Petr Pisar <ppisar@redhat.com> - 0.16-1
- 0.16 bump

* Thu Dec 16 2021 Petr Pisar <ppisar@redhat.com> - 0.15-1
- 0.15 bump

* Fri Oct 29 2021 Petr Pisar <ppisar@redhat.com> - 0.14-1
- 0.14 bump

* Wed Sep 01 2021 Petr Pisar <ppisar@redhat.com> - 0.13-1
- 0.13 bump
- XS::Parse::Sublike::Builder moved to perl-XS-Parse-Sublike-Builder
  subpackage

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Petr Pisar <ppisar@redhat.com> - 0.12-1
- 0.12 bump
- Package the tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Petr Pisar <ppisar@redhat.com> - 0.11-1
- 0.11 bump

* Wed Jul 22 2020 Petr Pisar <ppisar@redhat.com> 0.10-1
- Specfile autogenerated by cpanspec 1.78.
