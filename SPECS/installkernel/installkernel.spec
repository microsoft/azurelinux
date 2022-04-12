Summary:        Custom installkernel script for installing the Linux kernel
Name:           installkernel
Version:        1.0.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
Source0:        installkernel
Source1:        COPYING
BuildArch:      noarch

%description
Custom installkernel script to easily install the Linux kernel onto a running
Mariner system. This script will get called automatically by the Linux kernel's
"make install" command.

%prep

%build

%install
install -vdm 755 %{buildroot}%{_sbindir}
install -vm 744 %{SOURCE0} %{buildroot}%{_sbindir}/installkernel
cp %{SOURCE1} COPYING

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/installkernel

%changelog
* Thu Mar 31 2022 Chris Co <chrco@microsoft.com> - 1.0.0-2
- Fix mariner.cfg symlink generation
- License verified

* Mon Mar 29 2021 Chris Co <chrco@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
- Initial version of the installkernel package
