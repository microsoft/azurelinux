Summary:        Package for Mariner to meet Azure Security Baseline 
Name:           asc
Version:        %{azl}.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
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
* Tue Feb 27 2024 Muhammad Falak <mwani@microsoft.com> - 3.0-1
- Bump version to 3.0 for AzureLiux 3.0

* Tue Aug 16 2022 Minghe Ren <mingheren@microsoft.com> - 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
