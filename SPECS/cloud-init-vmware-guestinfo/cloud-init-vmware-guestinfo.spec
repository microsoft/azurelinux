%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           cloud-init-vmware-guestinfo
Version:        1.3.1
Release:        2%{?dist}
Summary:        A cloud-init datasource for VMware
Group:          System/Management
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/vmware/cloud-init-vmware-guestinfo

#Source0:      https://github.com/vmware/%{name}/archive/v%{version}.tar.gz
Source0:       %{name}-%{version}.tar.gz
BuildRequires: python3
Requires:      cloud-init
BuildArch:     noarch

%description
Provides a cloud-init datasource for pulling meta, user,
and vendor data from VMware vSphere's GuestInfo interface.

%prep
%setup -q

%build

%install
install -dm 0755 %{buildroot}%{_sysconfdir}/cloud/cloud.cfg.d
install -m 0644 99-DataSourceVMwareGuestInfo.cfg %{buildroot}%{_sysconfdir}/cloud/cloud.cfg.d/99-DataSourceVMwareGuestInfo.cfg
install -dm 0755 %{buildroot}%{python3_sitelib}/cloudinit/sources/
install -m 0644 DataSourceVMwareGuestInfo.py %{buildroot}%{python3_sitelib}/cloudinit/sources/DataSourceVMwareGuestInfo.py

%files
%license LICENSE
%config %{_sysconfdir}/cloud/cloud.cfg.d/99-DataSourceVMwareGuestInfo.cfg
%{python3_sitelib}/cloudinit/sources/DataSourceVMwareGuestInfo.py

%changelog
* Mon Oct 12 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.3.1-2
- Adding a missing %%{?dist} tag.
* Thu Sep 17 2020 Mateusz Malisz <mamalisz@microsoft.com> 1.3.1-1
- Original version for CBL-Mariner.
- License Verified
