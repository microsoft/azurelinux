# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Perform optional tests
%bcond_without perl_Syntax_Operator_In_enables_optional_test

Name:           perl-Syntax-Operator-In
Version:        0.10
Release:        4%{?dist}
Summary:        Infix element-of-list meta-operator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Syntax-Operator-In
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Syntax-Operator-In-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.14
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%define xs_parse_infix_minver 0.44
BuildRequires:  perl(XS::Parse::Infix::Builder) >= %{xs_parse_infix_minver}
# Run-time:
BuildRequires:  perl(Carp)
%global meta_min_ver 0.003.002
BuildRequires:  perl(meta) >= %{meta_min_ver}
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(XS::Parse::Infix) >= %{xs_parse_infix_minver}
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(utf8)
%if %{with perl_Syntax_Operator_In_enables_optional_test}
# Optional tests:
# Perl with PL_infix_plugin support is required (since 5.37.7)
BuildRequires:  perl(Syntax::Operator::Equ)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(meta) >= %{meta_min_ver}
Requires:       perl(XS::Parse::Infix) >= %{xs_parse_infix_minver}
%if %{defined perl_XS_Parse_Infix_ABI}
# XS::Parse::Infix ABI checked in XSParseInfix.h included from
# perl-XS-Parse-Keyword-Builder.
Requires:       %{perl_XS_Parse_Infix_ABI}
%endif

# Remove underspecied dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(meta\\) >= 0\\.003$

%description
This Perl module provides an infix meta-operator that implements an
element-of-list test on either strings or numbers.

%package tests
Summary:        Tests for %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
%if %{with perl_Syntax_Operator_In_enables_optional_test}
# Optional tests:
# Perl with PL_infix_plugin support is required (since 5.37.7)
Requires:       perl(Syntax::Operator::Equ)
%endif

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Syntax-Operator-In-%{version}
%if !%{with perl_Syntax_Operator_In_enables_optional_test}
for T in t/80in+equ.t t/99pod.t; do
    rm "$T"
    perl -i -ne 'print $_ unless m{^\Q'"$T"'\E}' MANIFEST
done
%endif
chmod +x t/*.t

%build
perl Build.PL --installdirs=vendor --optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -size 0 -delete
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
%if %{with perl_Syntax_Operator_In_enables_optional_test}
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
%dir %{perl_vendorarch}/auto/Syntax
%dir %{perl_vendorarch}/auto/Syntax/Operator
%{perl_vendorarch}/auto/Syntax/Operator/In
%dir %{perl_vendorarch}/Syntax
%{perl_vendorarch}/Syntax/Operator
%{_mandir}/man3/Syntax::Operator::*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jul 22 2024 Petr Pisar <ppisar@redhat.com> - 0.10-1
- 0.10 bump

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-2
- Perl 5.40 rebuild

* Wed Feb 14 2024 Petr Pisar <ppisar@redhat.com> - 0.09-1
- 0.09 bump

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Petr Pisar <ppisar@redhat.com> - 0.06-1
- 0.06 bump

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-4
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Petr Pisar <ppisar@redhat.com> - 0.04-2
- Unify buildroot references and a shell syntax

* Thu Jan 05 2023 Petr Pisar <ppisar@redhat.com> 0.04-1
- Specfile autogenerated by cpanspec 1.78.
