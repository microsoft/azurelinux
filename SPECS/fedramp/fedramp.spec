Summary:        Package for Mariner to meet FedRAMP rules
Name:           fedramp
Version:        1.0
Release:        1%{?dist}
License:        MIT
Requires:       filesystem-fedramp
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner

%description
Pacakge for Mariner to meet FedRAMP rules by adding multiple config files in /etc/modprobe.d

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
* Tue Aug 16 2022 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial packaging