%global debug_package   %{nil}

Summary:        Security package for Mariner to meet all sorts of compliance rules
Name:           security
Version:        1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Source0:        security-1.0.tar.xz
Requires:       rust
Requires:       systemd
BuildRequires:  rust
BuildRequires:  systemd


%description
Security package for Mariner to meet all sorts of compliance rules like FedRAMP, STIG, FIPS, etc.

%package FedRAMP
Summary:        FedRAMP compliance
Requires:       asc
Requires:       openscap

%description FedRAMP
package to meet FedRAMP Compliance

%package FIPS
Summary:        FIPS compliance
Requires:       dracut-fips
Requires:       grubby

%description FIPS
package to meet FIPS Compliance

%package STIG
Summary:        STIG compliance
Requires:       complianceascode
Requires:       openscap

%description STIG
package to meet STIG Compliance

%prep
%setup -q 

%build
rustc compliance.rs

%install
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/
mkdir -p %{buildroot}%{_unitdir}
install -D -m 644 compliance.service %{buildroot}%{_unitdir}/compliance.service
install -m 0755 compliance %{buildroot}%{_sysconfdir}/Compliance/
cp -r FedRAMP/ %{buildroot}%{_sysconfdir}/Compliance/
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/FIPS
install -m 0755 FIPS/* %{buildroot}%{_sysconfdir}/Compliance/FIPS/
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/STIG
install -m 0755 STIG/* %{buildroot}%{_sysconfdir}/Compliance/STIG/

%post
%systemd_post compliance.service

%post FedRAMP
.%{_sysconfdir}/Compliance/FedRAMP/marketplace_compliance.sh --run_live --marketplace
.%{_sysconfdir}/Compliance/FedRAMP/run_oscap.sh

%post FIPS
.%{_sysconfdir}/Compliance/FIPS/fips.sh

%files
%{_sysconfdir}/Compliance/compliance
%{_unitdir}/compliance.service

%files FedRAMP
%{_sysconfdir}/Compliance/FedRAMP

%files FIPS
%{_sysconfdir}/Compliance/FIPS

%files STIG
%{_sysconfdir}/Compliance/STIG

%changelog
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Add compliance.service for security package
- Add FedRAMP, FIPS, STIG compliance