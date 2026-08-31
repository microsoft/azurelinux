# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           appx-util
Version:        0.5
Release:        7%{?dist}
Summary:        Utility to create Microsoft .appx packages

# See LICENSING.md for details
License:        MPL-2.0 and BSD-3-Clause
URL:            https://github.com/OSInside/appx-util
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
# For tests
%if 0%{?el8}
BuildRequires:  /usr/bin/python3.6
%else
BuildRequires:  /usr/bin/python3
%endif

%description
appx is a tool which creates and optionally signs
Microsoft Windows APPX packages.


%prep
%autosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE* LICENSING.md
%doc README.md CONTRIBUTING.md
%{_bindir}/appx


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.5-2
- Fix BR for Python 3 for EL8 (RH#2237698)

* Mon Sep 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.5-1
- Update to 0.5
- Migrate to SPDX license identifiers

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 30 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.4-5
- Backport fix for OpenSSL 3.0 compatibility (RH#2018887)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.4-4
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Neal Gompa <ngompa13@gmail.com> - 0.4-2
- Update license tag

* Wed May 26 2021 Neal Gompa <ngompa13@gmail.com> - 0.4-1
- Update to 0.4

* Tue May 25 2021 Neal Gompa <ngompa13@gmail.com> - 0.3-1
- Update to 0.3

* Mon May 24 2021 Neal Gompa <ngompa13@gmail.com> - 0.2-1
- Initial package
