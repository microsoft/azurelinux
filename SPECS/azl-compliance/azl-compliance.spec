Summary:        Azure Linux compliance package to meet all sorts of compliance rules
Name:           azl-compliance
Version:        1.0.2
Release:        3%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
Patch0:         CVE-2025-4574.patch
Patch1:         CVE-2026-25541.patch
Patch2:         CVE-2026-25727.patch
Requires:       dnf
Requires:       gnutls
Requires:       grub2
Requires:       grubby
Requires:       rpm
Requires:       rsyslog
Requires:       sudo
BuildRequires:  rust

%description
Azure Linux compliance package to configure systems to meet FIPS and FedRAMP compliance.

%prep
%autosetup -p1

%build
cd azl-compliance
cargo build --release --offline

%install
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/
mkdir -p %{buildroot}%{_bindir}
install -m 0755 ./azl-compliance/target/release/azl-compliance %{buildroot}%{_bindir}/azl-compliance
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/fips
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/fedramp/remediation_scripts
install -m 0755 fips/*.sh %{buildroot}%{_sysconfdir}/azl-compliance/fips/
install -m 0755 fedramp/*.sh %{buildroot}%{_sysconfdir}/azl-compliance/fedramp/
install -m 0644 fedramp/*.txt %{buildroot}%{_sysconfdir}/azl-compliance/fedramp/
install -m 0755 fedramp/remediation_scripts/* %{buildroot}%{_sysconfdir}/azl-compliance/fedramp/remediation_scripts/
install -m 0644 azl-compliance-fips.json %{buildroot}%{_sysconfdir}/azl-compliance/
install -m 0644 azl-compliance-fedramp.json %{buildroot}%{_sysconfdir}/azl-compliance/

%files
%license LICENSE
%{_bindir}/azl-compliance
%{_sysconfdir}/azl-compliance/fips
%{_sysconfdir}/azl-compliance/azl-compliance-fips.json
%{_sysconfdir}/azl-compliance/fedramp
%{_sysconfdir}/azl-compliance/azl-compliance-fedramp.json

%check
cd azl-compliance
cargo test --release --offline

%changelog
* Fri Feb 13 2026 Aditya Singh <v-aditysing@microsoft.com> - 1.0.2-3
- Patch CVE-2026-25541, CVE-2026-25727

* Mon May 19 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.0.2-2
- Patch CVE-2025-4574

* Thu Jun 06 2024 Tobias Brick <tobiasb@microsoft.com> 1.0.2-1
- Update to version 1.0.2

* Tue Mar 19 2024 Tobias Brick <tobiasb@microsoft.com> 1.0.1-1
- Original version for CBL-Mariner.
- License verified
