Summary:        Represent and manage a libvirt hypervisor connection
Name:           perl-Sys-Virt
Version:        10.0.0
Release:        1%{?dist}
License:        GPLv2+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/dist/Sys-Virt
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DANBERR/Sys-Virt-v%{version}.tar.gz#/%{name}-v%{version}.tar.gz

# Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libvirt-devel >= %{version}
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  sed
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(XSLoader)

# Runtime
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if %{with_check}
BuildRequires:  perl(Sys::Hostname)
# Optional tests only
BuildRequires:  perl(Test::CPAN::Changes)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(XML::XPath)
BuildRequires:  perl(XML::XPath::XMLParser)
# Tests only
BuildRequires:  perl(base)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
The Sys::Virt module provides a Perl XS binding to the libvirt virtual
machine management APIs. This allows machines running within arbitrary
virtualization containers to be managed with a consistent API.

%prep
%autosetup -n Sys-Virt-v%{version}


%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0

%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%license LICENSE
%doc AUTHORS Changes README examples/
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Sys*
%{_mandir}/man3/*

%changelog
* Thu Feb 01 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 10.0.0-1
- Upgrade to 10.0.0

* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-4
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Thomas Crain <thcrain@microsoft.com> - 6.1.0-3
- Only pull in test dependencies during check builds
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 10 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.1.0-1
- Update to version 6.1.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.0-1
- Update to version 6.0.0

* Tue Oct 08 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.8.0-1
- Update to version 5.8.0

* Wed Sep 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.7.0-1
- Update to version 5.7.0

* Tue Aug 06 2019 Cole Robinson <crobinso@redhat.com> - 5.6.0-1
- Update to version 5.6.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Cole Robinson <crobinso@redhat.com> - 5.5.0-1
- Rebased to version 5.5.0

* Wed Jun 12 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.4.0-1
- Update to 5.4.0 release

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.2.0-2
- Perl 5.30 rebuild

* Wed Apr  3 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-1
- Update to 5.2.0 release

* Mon Mar  4 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-1
- Update to 5.1.0 release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Daniel P. Berrangé <berrange@redhat.com> - 5.0.0-1
- Update to 5.0.0 release

* Mon Dec  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.10.0-1
- Update to 4.10.0 release

* Fri Oct  5 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.8.0-1
- Update to 4.8.0 release

* Tue Sep  4 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.7.0-1
- Update to 4.7.0 release

* Mon Aug  6 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.6.0-1
- Update to 4.6.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Petr Pisar <ppisar@redhat.com> - 4.5.0-2
- Perl 5.28 rebuild

* Tue Jul  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.5.0-1
- Update to 4.5.0 release

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.4.0-2
- Perl 5.28 rebuild

* Tue Apr  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.2.0-1
- Update to 4.2.0 release

* Mon Mar  5 2018 Daniel P. Berrange <berrange@redhat.com> - 4.1.0-1
- Update to 4.1.0 release

* Mon Feb 19 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.0-3
- Add build-require gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Daniel P. Berrange <berrange@redhat.com> - 4.0.0-1
- Update to 4.0.0 release
