# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

%global public_key RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3

Name:           minisign
Version:        0.12
Release: 4%{?dist}
Summary:        A dead simple tool to sign files and verify digital signatures
License:        ISC
URL:            https://github.com/jedisct1/minisign
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz.minisig

BuildRequires:  libsodium-devel
BuildRequires:  cmake
BuildRequires:  gcc
%if %{without bootstrap}
BuildRequires:  minisign
%endif

%description
Minisign is a dead simple tool to sign files and verify signatures.

%prep
%if %{without bootstrap}
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%endif

%autosetup -c

%build
%cmake -DCMAKE_STRIP=0 .
%cmake_build

%install
%cmake_install

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%license LICENSE
%doc README.md

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 François Kooman <fkooman@tuxed.net> - 0.12-1
- update to 0.12

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Remi Collet <remi@remirepo.net> - 0.11-5
- rebuild for new libsodium

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 François Kooman <fkooman@tuxed.net> - 0.11-1
- update to 0.11
- update source URLs to point to release tarballs

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 11 2021 François Kooman <fkooman@tuxed.net> - 0.10-1
- update to 0.10
- the existing minisign signature verfies also the GitHub generated tagged
  archive, so we directly use that without specifying a commit

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 François Kooman <fkooman@tuxed.net> - 0.9-4
- switch to cmake_build and cmake_install

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 François Kooman <fkooman@tuxed.net> - 0.9-1
- update to 0.9
- verify source tarball (when not bootstrapping)
- do not strip binary during build

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 François Kooman <fkooman@tuxed.net> - 0.8-2
- use macros for Source0

* Wed Jul 17 2019 François Kooman <fkooman@tuxed.net> - 0.8-1
- initial package
