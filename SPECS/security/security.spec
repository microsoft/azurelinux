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

%prep
%setup -q 

%build
cd compliance
cargo build --release

%install
mkdir -p %{buildroot}%{_sysconfdir}/Compliance/
mkdir -p %{buildroot}%{_unitdir}
install -D -m 644 compliance.service %{buildroot}%{_unitdir}/compliance.service
install -m 0755 ./compliance/target/release/compliance %{buildroot}%{_sysconfdir}/Compliance/

%post
%systemd_post compliance.service

%files
%{_sysconfdir}/Compliance/compliance
%{_unitdir}/compliance.service

%changelog
* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
- Add compliance.service for security package
