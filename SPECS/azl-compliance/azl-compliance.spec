%global debug_package   %{nil}

Summary:        Azure Linux compliance package to meet all sorts of compliance rules
Name:           azl-compliance
Version:        1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        azl-compliance-1.0.tar.gz
Requires:       rust
Requires:       systemd
BuildRequires:  rust
BuildRequires:  systemd

%description
Azure Linux compliance package to meet all sorts of compliance rules like FedRAMP, STIG, FIPS, etc.

%package fips
Summary:        FIPS compliance
Requires:       dracut-fips
Requires:       grubby

%description fips
package to meet FIPS Compliance

%package fedramp
Summary:        FedRAMP compliance

%description fedramp
package to meet FedRAMP Compliance


%prep
%setup -c

%build
cd azl-compliance

%install
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/
mkdir -p %{buildroot}%{_unitdir}
install -D -m 644 azl-compliance.service %{buildroot}%{_unitdir}/azl-compliance.service
install -m 0755 ./azl-compliance/target/debug/azl-compliance %{buildroot}%{_sysconfdir}/azl-compliance/
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/fips
mkdir -p %{buildroot}%{_sysconfdir}/azl-compliance/fedramp
install -m 0755 fips/* %{buildroot}%{_sysconfdir}/azl-compliance/fips/
cp -r fedramp/* %{buildroot}%{_sysconfdir}/azl-compliance/fedramp
install -m 0755 azl-compliance-fips.json %{buildroot}%{_sysconfdir}/azl-compliance/
install -m 0755 azl-compliance-fedramp.json %{buildroot}%{_sysconfdir}/azl-compliance/

%post
%systemd_post azl-compliance.service

%files
%{_sysconfdir}/azl-compliance/azl-compliance
%{_unitdir}/azl-compliance.service

%files fips
%{_sysconfdir}/azl-compliance/fips
%{_sysconfdir}/azl-compliance/azl-compliance-fips.json

%files fedramp
%{_sysconfdir}/azl-compliance/fedramp
%{_sysconfdir}/azl-compliance/azl-compliance-fedramp.json

%changelog
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Add azl-compliance.service
- Add FIPS sub-package
- Add FedRAMP sub-package