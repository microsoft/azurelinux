# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Type-Tiny-XS
Version:        0.025
Release: 13%{?dist}
Summary:        Provides an XS boost for some of Type::Tiny's built-in type constraints
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Type-Tiny-XS/
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-XS-%{version}.tar.gz

BuildRequires:  %{__chmod}
BuildRequires:  %{__perl}
BuildRequires:  %{__make}

BuildRequires:  gcc
BuildRequires:  perl-devel

BuildRequires:  perl(:VERSION) >= 5.10.1
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(overload)

BuildRequires:  perl(Test::More) >= 0.92
BuildRequires:  perl(Type::Parser)

# Optional run-time requirement of Type::Parser
# Implicitly required by the testsuite
BuildRequires:  perl(Text::Balanced)

# Optional run-time requirement
Recommends:     perl(Type::Parser)


%description
This module is optionally used by Type::Tiny 0.045_03 and above to provide
faster, C-based implementations of some type constraints. (This package has
only core dependencies, and does not depend on Type::Tiny, so other data
validation frameworks might also consider using it!)

%prep
%setup -q -n Type-Tiny-XS-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} DESTDIR="$RPM_BUILD_ROOT"
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%doc Changes CREDITS README
%license COPYRIGHT LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Type*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-11
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-8
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-4
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.025-2
- Reflect comments from package review.

* Wed Nov 09 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.025-1
- Update to 0.025.

* Fri Jul 01 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.022-1
- Initial Fedora package.
