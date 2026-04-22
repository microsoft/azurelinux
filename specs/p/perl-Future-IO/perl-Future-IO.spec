# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Future-IO
Version:        0.16
Release: 4%{?dist}
Summary:        Future-returning IO core methods
License:        GPL-1.0-or-later OR Artistic-1.0-Perl

URL:            https://metacpan.org/release/Future-IO
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Future-IO-%{version}.tar.gz

BuildArch:      noarch
# build requirements
BuildRequires:  perl-interpreter >= 5.10
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.4004
# runtime requirements
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Future)
BuildRequires:  perl(strict)
BuildRequires:  perl(Struct::Dumb)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(warnings)
# test requirements
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Test::ExpectAndCheck)
BuildRequires:  perl(Test::Future::IO::Impl)
BuildRequires:  perl(Test::Pod) >= 1.00

%{?perl_default_filter}

%description
This package provides a few basic methods that behave similarly to the
same-named core perl functions relating to IO operations but yield
their results asynchronously via Future instances.

%prep
%setup -q -n Future-IO-%{version}

%build
/usr/bin/perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/Future*
%{_mandir}/man3/Future*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 22 2024 Emmanuel Seyman <emmanuel@seyman.fr> - 0.16-1
- Update to 0.16

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 Emmanuel Seyman <emmanuel@seyman.fr> - 0.15-1
- Update to 0.15
- Migrate to SPDX license

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May 07 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 0.14-1
- Update to 0.14

* Sun Feb 19 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 0.13-1
- Update to 0.13

* Sun Feb 05 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 0.12-1
- Update to 0.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Emmanuel Seyman <emmanuel@seyman.fr> - 0.11-1
- Update to 0.11

* Sun Aug 29 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.10-1
- Update to 0.10

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 03 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 0.08-1
- Update to 0.08

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-2
- Perl 5.32 rebuild

* Sun Mar 29 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 0.07-1
- Update to 0.07
- Replace %%{__perl} with /usr/bin/perl

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.06-1
- Update to 0.06

* Sun Jun 16 2019 Emmanuel Seyman <emmanuel@seyman.fr> - 0.05-1
- Initial specfile, based on the one autogenerated by cpanspec 1.78.
