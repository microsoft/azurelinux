# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Log-Any-Adapter-Screen
Version:        0.141
Release:        4%{?dist}
Summary:        Send logs to screen, with colors and some other features

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://search.cpan.org/dist/Log-Any-Adapter-Screen/
Source0:        https://www.cpan.org/modules/by-module/Log/Log-Any-Adapter-Screen-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.010
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Log::Any)
BuildRequires:  perl(Log::Any::Adapter) >= 0.11
BuildRequires:  perl(Log::Any::Adapter::Base)
BuildRequires:  perl(Log::Any::Adapter::Util)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod) >=  1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
This Log::Any adapter prints log messages to screen (STDERR/STDOUT).  The
messages are colored according to level (unless coloring is turned off).
It has a few other features: allow passing formatter, allow setting level
from some environment variables, add prefix/timestamps.


%prep
%autosetup -n Log-Any-Adapter-Screen-%{version} -p 1


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
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.141-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.141-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.141-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 16 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.141-1
- 0.141 bump (rhbz#2251186)
- Update license to SPDX format

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.140-12
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.140-9
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.140-6
- Perl 5.32 rebuild

* Thu Mar 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.140-5
- Add perl(blib) for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.140-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.140-2
- Perl 5.30 rebuild

* Mon Feb 25 2019 Björn Esser <besser82@fedoraproject.org> - 0.140-1
- Bump release to stable (#1680375)

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.140-0.3
- Changes as suggested in review (#1680375)
- Add a set of explicit BuildRequires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.140-0.2
- Add explicit perl module compat requires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.140-0.1
- Initial rpm release (#1680375)
