Summary:        Custom udev rules to transition SGX applications from the DCAP driver to in-kernel SGX support
Name:           sgx-backwards-compatibility
Version:        1.0.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
Source0:        99-sgx-backwards-compatibility.rules
Source1:        LICENSE

Requires(pre):  %{_sbindir}/groupadd
Requires(post): systemd-udev

%description
This package applies custom udev rules to create symlinks
from /dev/sgx/{enclave,provision} to /dev/sgx_{enclave,provision}

%prep

%pre
if ! getent group sgx_prv >/dev/null; then
    groupadd sgx_prv
fi

%build

%install
mkdir -p %{buildroot}/etc/udev/rules.d
install %{SOURCE0} %{buildroot}/etc/udev/rules.d/99-sgx-backwards-compatibility.rules
cp %{SOURCE1} LICENSE

%files
%license LICENSE
/etc/udev/rules.d/99-sgx-backwards-compatibility.rules

%post
udevadm trigger --subsystem-match=misc

%changelog
* Mon May 06 2024 Osama Esmail <osamaesmail@microsoft.com> - 1.0.0-2
- Fixing typo (compatability -> compatibility)

* Tue Oct 20 2022 Aadhar Agarwal <aadagarwal@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner
- Initial version of the sgx-backwards-compatability package
- License verified
