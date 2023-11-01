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

%prep
%setup -q 

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/
install -m 0755 compliance.service %{buildroot}%{_sysconfdir}/Compliance/
install -m 0755 compliance.sh %{buildroot}%{_sysconfdir}/Compliance/
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/FedRAMP
cp -r FedRAMP/ %{buildroot}%{_sysconfdir}/Compliance/
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/FIPS
install -m 0755 FIPS/* %{buildroot}%{_sysconfdir}/Compliance/FIPS/

%post FedRAMP
.%{_sysconfdir}/Compliance/FedRAMP/stig/stig_scripts/marketplace_compliance.sh --run_live --marketplace
.%{_sysconfdir}/Compliance/FedRAMP/stig/stig_scripts/run_oscap.sh

%post FIPS
.%{_sysconfdir}/Compliance/FedRAMP/asc_patches.sh
.%{_sysconfdir}/Compliance/FIPS/fips.sh

%files
%{_sysconfdir}/Compliance/compliance.service
%{_sysconfdir}/Compliance/compliance.sh

%files FedRAMP
%{_sysconfdir}/Compliance/FedRAMP

%files FIPS
%{_sysconfdir}/Compliance/FIPS

%changelog
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Add FedRAMP, FIPS compliance