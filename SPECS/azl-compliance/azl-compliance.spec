%global debug_package   %{nil}

Summary:        Azure Linux compliance package to meet all sorts of compliance rules
Name:           azl-compliance
Version:        1.0.0
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
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
%autosetup

%build
cd azl-compliance
cargo build --release --offline

%install
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/
install -m 0644 ./LICENSE %{buildroot}%{_sysconfdir}/azl-compliance/
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
%{_bindir}/azl-compliance
%{_sysconfdir}/azl-compliance/LICENSE
%{_sysconfdir}/azl-compliance/fips
%{_sysconfdir}/azl-compliance/azl-compliance-fips.json
%{_sysconfdir}/azl-compliance/fedramp
%{_sysconfdir}/azl-compliance/azl-compliance-fedramp.json

%check
cd azl-compliance
cargo test --release --offline

%changelog
* Tue Mar 19 2024 Tobias Brick <tobiasb@microsoft.com> 1.0.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
