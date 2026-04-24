# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MouseX-Types-Common
Version:        0.001000
Release: 12%{?dist}
Summary:        Set of commonly-used type constraints
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            http://metacpan.org/dist/MouseX-Types-Common/
Source0:        http://cpan.metacpan.org/authors/id/G/GF/GFUJI/MouseX-Types-Common-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{__chmod}
BuildRequires:  %{__make}
BuildRequires:  %{__sed}
BuildRequires:  %{__perl}

BuildRequires:  perl-generators

BuildRequires:  perl(:VERSION) >= 5.6.2
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::WriteAll)
BuildRequires:  perl(Mouse) >= 0.42
BuildRequires:  perl(MouseX::Types) >= 0.01
BuildRequires:  perl(MouseX::Types::Mouse)
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(Test::Exception)

BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
A set of commonly-used type constraints that do not ship with Mouse
by default.

%prep
%setup -q -n MouseX-Types-Common-%{version}
# Remove bundled modules
rm -r inc
%{__sed} -i -e '/^inc\//d' MANIFEST

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{__make} test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001000-4
- Spec file cosmetics.
- Convert license to SPDX.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.001000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001000-2
- Post-review fixes.

* Thu Jun 16 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001000-1
- Initial Fedora package.
