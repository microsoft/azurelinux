# https://github.com/open-policy-agent/opa
%global goipath     github.com/open-policy-agent/opa
# short_commit is used to display in opa version
%global short_commit    e88ad165
Summary:        Open source, general-purpose policy engine
Name:           opa
Version:        0.55.0
Release:        1%{?dist}
# Upstream license specification: MIT and Apache-2.0
# Main package:    ASL 2.0
# internal/jwx:    MIT
# internal/semver: ASL 2.0
License:        ASL 2.0 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner 
URL:            https://github.com/open-policy-agent/opa
#Source0:       https://github.com/open-policy-agent/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Make telemetry opt-out
Patch0:         0001-Make-telemetry-opt-out.patch
# Skip tests requiring network
Patch1:         0001-Skip-tests-requiring-network.patch
# Warn users about WebAssembly missing
BuildRequires:  golang
BuildRequires:  make
 
%description
An open source, general-purpose policy engine.
 
The Open Policy Agent (OPA) is an open source, general-purpose policy engine
that enables unified, context-aware policy enforcement across the entire
stack.
 
%prep
%autosetup -p1
mv internal/jwx/LICENSE LICENSE-jwx

%build
make build WASM_ENABLED=0
make man

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp opa_linux*          %{buildroot}%{_bindir}/opa
install -d -p -m 0755                   %{buildroot}%{_mandir}/man1
install -D -p -m 0644 man/*             %{buildroot}%{_mandir}/man1/

%files
%license LICENSE LICENSE-jwx
%doc docs/content CHANGELOG.md README.md MAINTAINERS.md ADOPTERS.md CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md GOVERNANCE.md SECURITY.md
%{_mandir}/man1/opa*.1*
%{_bindir}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.55.0-1
- Auto-upgrade to 0.55.0 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.50.2-7
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.50.2-6
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.50.2-5
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.50.2-4
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.50.2-3
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.50.2-2
- Bump release to rebuild with go 1.19.8

* Mon Mar 27 2023 Dallas Delaney <dadelan@microsoft.com> - 0.50.2-1
- Update to version 0.50.2

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.31.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.31.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.31.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.31.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.31.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.31.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.31.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.31.0-2
- Bump release to rebuild with golang 1.18.3

* Thu Sep 16 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.31.0-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License Verified
- Remove unused/un-supported macro usage

* Sun Aug 15 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.31.0-1
- Update to latest upstream 0.31.0 (fixes rhbz#1987088)
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Wed Jul 14 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.30.2-1
- Update to latest upstream 0.30.2 (fixes rhbz#1982007)
 
* Fri Jul 02 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.30.1-1
- Update to latest upstream 0.30.1 (fixes rhbz#1978733)
 
* Thu Jul 01 11:17:03 CEST 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.30.0-1
- Update to latest upstream 0.30.0 (fixes rhbz#1966363)
- Fix license (internal/jwx is licensed under MIT license)
 
* Fri May 28 17:03:56 CEST 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.29.3-1
- Update to latest upstream 0.29.3 (fixes rhbz#1965613)
 
* Mon May 10 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.28.0-1
- Update to latest upstream 0.28.0 (fixes rhbz#1954091)
 
* Sat Mar 13 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.27.1-2
- Fix failing test on 32-bit architectures
 
* Sat Mar 13 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.27.1-1
- Update to latest upstream 0.27.1 (fixes #1936740)
 
* Tue Jan 26 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.26.0-2
- Remove dependency on github.com/wasmerio/go-ext-wasm (Fixes #1919476)
- Use upstream fix for Go 1.16 compatibility
 
* Thu Jan 21 2021 Olivier Lemasle <o.lemasle@gmail.com> - 0.26.0-1
- Update to latest upstream 0.26 (note: wasm disabled)
 
* Tue Oct 27 2020 Olivier Lemasle <o.lemasle@gmail.com> - 0.24.0-2
- Fix failing tests on 32-bit architectures
- Make telemetry service opt-out
- Fix version output
 
* Tue Oct 27 2020 Olivier Lemasle <o.lemasle@gmail.com> - 0.24.0-1
- Update to latest upstream 0.24
 
* Tue Apr 07 08:15:00 CEST 2020 Olivier Lemasle <o.lemasle@gmail.com> - 0.18.0-1
- Initial package
