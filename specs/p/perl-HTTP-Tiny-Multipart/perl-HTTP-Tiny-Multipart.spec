# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-HTTP-Tiny-Multipart
Version:        0.08
Release:        20%{?dist}
Summary:        Add post_multipart to HTTP::Tiny

License:        Artistic-2.0
URL:            https://search.cpan.org/dist/HTTP-Tiny-Multipart/
Source0:        https://www.cpan.org/modules/by-module/HTTP/HTTP-Tiny-Multipart-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >=  1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
%{summary}.


%prep
%autosetup -n HTTP-Tiny-Multipart-%{version} -p 1


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build


%install
%make_install
%{_fixperms} %{buildroot}/*


%check
%make_build test


%files
%doc Changes
%license CONTRIBUTORS LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Apr 20 2024 Miroslav Suchý <msuchy@redhat.com> - 0.08-17
- convert license to SPDX

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-8
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.30 rebuild

* Mon Feb 25 2019 Björn Esser <besser82@fedoraproject.org> - 0.08-1
- Bump release to stable (#1680373)

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.08-0.4
- Changes as suggested in review (#1680373)
- Add a set of explicit BuildRequires
- Improve Summary tag and %%description

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.08-0.3
- Add explicit perl module compat requires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.08-0.2
- Add missing BuildRequires: perl(Test::More)

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.08-0.1
- Initial rpm release (#1680373)
