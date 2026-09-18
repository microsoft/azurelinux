# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-IO-Prompter
Version:        0.005004
Release:        1%{?dist}
Summary:        Prompt for input, read it, clean it, return it

# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://search.cpan.org/dist/IO-Prompter/
Source0:        https://www.cpan.org/modules/by-module/IO/IO-Prompter-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.010
BuildRequires:  perl(Carp)
BuildRequires:  perl(Contextual::Return)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(diagnostics)
BuildRequires:  perl(lib)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl(match::smart)


%description
IO::Prompter exports a single subroutine, prompt, that prints a prompt
(but only if the program's selected input and output streams are connected
to a terminal), then reads some input, then chomps it, and finally returns
an object representing that text.


%prep
%autosetup -n IO-Prompter-%{version} -p 1


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build


%install
%make_install
%{_fixperms} %{buildroot}/*


%check
%make_build test


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Fri Sep 05 2025 Björn Esser <besser82@fedoraproject.org> - 0.005004-1
- New upstream release
  Fixes: rhbz#2391686

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.005002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Feb 07 2025 Björn Esser <besser82@fedoraproject.org> - 0.005002-1
- New upstream release
  Fixes: rhbz#2344334

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.005001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 6 2024 Miroslav Suchý <msuchy@redhat.com> - 0.005001-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.005001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Björn Esser <besser82@fedoraproject.org> - 0.005001-1
- New upstream release
  Fixes rhbz#2224546

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.004015-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.004015-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.004015-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.004015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.004015-2
- Perl 5.30 rebuild

* Mon Feb 25 2019 Björn Esser <besser82@fedoraproject.org> - 0.004015-1
- Bump release to stable (#1680374)

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.004015-0.3
- Changes as suggested in review (#1680374)
- Add a BR for Perl required version
- Add a set of explicit BuildRequires
- Use %%make_install
- Drop cleanups using find
- Drop META.json fom %%doc

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.004015-0.2
- Add explicit perl module compat requires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.004015-0.1
- Initial rpm release (#1680374)
