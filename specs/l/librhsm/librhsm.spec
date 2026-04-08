# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           librhsm
Version:        0.0.4
Release:        1%{?dist}
Summary:        Red Hat Subscription Manager library
License:        LGPL-2.1-or-later
URL:            https://github.com/rpm-software-management/librhsm
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
# Key exported from Petr Pisar's keyring
Source2:        gpgkey-E3F42FCE156830A80358E6E94FD1AEC3365AF7BF.gpg

BuildRequires:  gnupg2
BuildRequires:  meson >= 0.37.0
BuildRequires:  gcc
BuildRequires:  pkgconfig(gio-2.0) >= 2.44
BuildRequires:  pkgconfig(glib-2.0) >= 2.44
BuildRequires:  pkgconfig(gobject-2.0) >= 2.44
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.2
BuildRequires:  pkgconfig(openssl)

%description
%{summary}.

%package devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.0

%files devel
%{_libdir}/%{name}.so
%{_includedir}/rhsm/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Oct 17 2025 Petr Pisar <ppisar@redhat.com> - 0.0.4-1
- 0.0.4 bump

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 30 2024 Petr Pisar <ppisar@redhat.com> - 0.0.3-14
- Improve a documentation
- Refactor parse_entitlement_data()
- Fix relocating certificate paths to /etc/rhsm-host

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Petr Pisar <ppisar@redhat.com> - 0.0.3-11
- Convert a license tag to SPDX

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.0.3-6
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 24 2021 Daniel Mach - 0.0.3-4
- Fix License in spec to LGPLv2.1+ (was LGPLv2+)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Stephen Gallagher <sgallagh@redhat.com> - 0.0.3-1
- Initial release
