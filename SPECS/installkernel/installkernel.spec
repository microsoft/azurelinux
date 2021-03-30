Summary:        Custom installkernel script for installing the Linux kernel
Name:           installkernel
Version:        1.0.0
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
Source0:        installkernel
BuildArch:      noarch

%description
Custom installkernel script to easily install the Linux kernel onto a running
Mariner system. This script will get called automatically by the Linux kernel's
"make install" command.

%prep

%build

%install
install -vm 744 %{SOURCE0} %{buildroot}/%{_sbindir}/installkernel

%files
%defattr(-,root,root)
%{_sbindir}/installkernel

%changelog
* Mon Mar 29 2021 Chris Co <chrco@microsoft.com> - 1.0.0-1
- Initial version of the installkernel package