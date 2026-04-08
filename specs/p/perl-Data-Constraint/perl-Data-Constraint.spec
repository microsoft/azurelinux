# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Data-Constraint
Version:        1.205
Release:        3%{?dist}
Summary:        Prototypical value checking
License:        Artistic-2.0

URL:            https://metacpan.org/dist/Data-Constraint
Source0:        https://cpan.metacpan.org/authors/id/B/BR/BRIANDFOY/Data-Constraint-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  %{__make}
BuildRequires:  %{__perl}

BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(:VERSION) >= 5.8

BuildRequires:  perl(Class::Prototyped)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
A constraint is some sort of condition on a datum. This module checks one
condition against one value at a time, and I call the thing that checks
that condition the "constraint". A constraint returns true or false, and
that's it. It should have no side effects, it should not change program
flow, and it should mind its own business. Let the thing that calls the
constraint figure out what to do with it. I want something that says "yes"
or "no" (and I discuss why this needs a fancy module later).

%prep
%setup -q -n Data-Constraint-%{version}

# bogus permissions in source tarball
chmod -x lib/Data/Constraint.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%license LICENSE
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.205-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.205-1
- Update to 1.205.
- Reflect upstream URL having changed.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.204-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.204-1
- Update to 1.204.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.203-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.203-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.203-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.203-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.203-3
- Spec file cosmetics.

* Sat Aug 20 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.203-2
- Reflect feedback from review.

* Mon Jul 11 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.203-1
- Initial Fedora package.
