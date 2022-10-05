Summary:        Package for Mariner to meet Azure Security Baseline 
Name:           asc
Version:        1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Requires:       filesystem-asc

%description
Package for Mariner to meet Azure Security Baseline by adding multiple config files in /etc/modprobe.d

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
* Tue Aug 16 2022 Minghe Ren <mingheren@microsoft.com> 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
